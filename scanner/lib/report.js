// Turns a scan result into the report page. Same page for Tim's draft and the customer's copy.
const e = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const BOOK = process.env.BOOKING_URL || 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ19B4FBJCID1vLALGmp7HljuV-Cma5K1_z87p5Yf5_WTdactEM9nSq5C4BJ1KBa7WeHK_F0_JLf?gv=true';
const plural = (n, w) => `${n.toLocaleString('en-US')} ${w}${n === 1 ? '' : 's'}`;
const CSS = `:root{--bg:#F7F4EE;--ink:#111110;--mute:#55524c;--line:#11111022;--acc:#2c2a6f;--amber:#ffe9a8;--amber-t:#4d3400;--ok:#0b6b3a}
*{box-sizing:border-box}body{margin:0;font:17px/1.55 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--bg);overflow-wrap:anywhere}
.w{max-width:980px;margin:0 auto;padding:0 22px}header{padding:28px 0;border-bottom:1px solid var(--line)}.brand{font-weight:700;font-size:1.6rem;letter-spacing:-.03em;text-decoration:none;color:var(--ink)}.brand span{color:var(--acc)}
h1{font-size:clamp(2.2rem,7vw,4rem);line-height:1;letter-spacing:-.04em;margin:36px 0 12px;font-weight:650}h2{font-size:clamp(1.6rem,4vw,2.4rem);letter-spacing:-.03em;line-height:1.05;margin:56px 0 16px}h3{font-size:1.1rem;margin:0 0 4px}
a{color:var(--acc)}:focus-visible{outline:3px solid var(--acc);outline-offset:3px}.mute{color:var(--mute)}.lede{font-size:1.2rem;max-width:40em}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:28px 0;padding:0;list-style:none}.stats li{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px}.stats b{display:block;font-size:2rem;letter-spacing:-.03em;line-height:1.1}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;margin:0 0 12px;padding:18px 20px}.pill{display:inline-block;font-size:.78rem;font-weight:700;border:1px solid currentColor;border-radius:999px;padding:1px 10px;margin:0 6px 6px 0}.fix{color:var(--acc)}.dev{color:#7a3e00}.pass{color:var(--ok)}
code{font:13px/1.4 ui-monospace,Menlo,monospace;background:var(--bg);padding:2px 6px;border-radius:4px;display:inline-block;max-width:100%}details{margin-top:8px}summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:600}
table{border-collapse:collapse;width:100%;background:#fff;border-radius:12px;overflow:hidden}th,td{text-align:left;padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:.85rem}
.note{background:var(--amber);color:var(--amber-t);padding:14px 18px;border-radius:10px;font-weight:600}.btn{display:inline-flex;align-items:center;min-height:52px;padding:0 26px;border-radius:999px;background:var(--ink);color:var(--bg);text-decoration:none;font-weight:600;border:0;font:inherit;font-weight:600;cursor:pointer}
footer{margin-top:72px;padding:28px 0 48px;border-top:1px solid var(--line);font-size:.92rem;color:var(--mute)}ul.plain{padding-left:1.1em}`;

function issueCard(i) {
  const kind = i.fix === 'fix' ? '<span class="pill fix">Fix it now</span>' : '<span class="pill dev">Needs a developer</span>';
  return `<div class="card"><p style="margin:0">${i.advisory ? '<span class="pill">Advisory</span>' : `<span class="pill">${e(i.severity)}</span>${kind}`}</p>
<h3>${e(i.name)}</h3>
<p class="mute" style="margin:0">${i.wcag.length ? 'WCAG ' + i.wcag.map(e).join(', ') + ' · ' : ''}${plural(i.count, 'instance')} on ${plural(i.pages, 'tested page')} · affects ${e(i.affects)}</p>
<details><summary>Examples</summary>${i.samples.map(s => `<p style="margin:0 0 10px"><a href="${e(s.url)}">${e(s.url)}</a><br><code>${e(s.html)}</code></p>`).join('')}</details></div>`;
}

function render(job, opts = {}) {
  const r = job.result, host = new URL(r.site).host;
  const date = new Date(r.finished).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const wcag = r.issues.filter(i => !i.advisory), adv = r.issues.filter(i => i.advisory);
  const o = r.outside;
  const head = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Accessibility scan: ${e(host)} | Yoodle</title><style>${CSS}</style></head><body>
<header><div class="w"><a class="brand" href="https://yoodle.com/">yoodle<span>.</span></a></div></header><main class="w">`;
  if (!r.ok) return head + `<h1>We could not scan ${e(host)}.</h1><p class="lede">${e(r.reason)}</p></main></body></html>`;
  return head + `
${opts.draft ? '<p class="note" style="margin-top:24px">Draft. Not yet sent to the customer.</p>' : ''}
<p class="mute" style="margin:32px 0 0">Automated accessibility scan · ${e(date)}${job.organization ? ' · prepared for ' + e(job.organization) : ''}</p>
<h1>${e(host)}</h1>
<p class="lede">We tested ${plural(r.tested, 'page')} of the ${r.discovery.total.toLocaleString('en-US')} we found, at least one from each of ${plural(r.templates.length, 'page template')}, against ${e(r.tool.standard)}. ${wcag.length ? `The scan found ${plural(wcag.length, 'kind')} of WCAG failure.` : 'The scan found no WCAG failures on the pages tested.'}</p>
<ul class="stats"><li><b>${r.discovery.total.toLocaleString('en-US')}</b>pages found</li><li><b>${r.tested}</b>pages tested</li><li><b>${wcag.length}</b>kinds of WCAG failure</li><li><b>${r.fixNow}</b>we can fix now</li><li><b>${r.needsDeveloper}</b>need a developer</li></ul>
${job.note ? `<div class="card"><p style="margin:0">${e(job.note)}</p></div>` : ''}
<div class="card"><p style="margin:0 0 12px"><strong>Next: 30 minutes with Tim McCoy.</strong> We walk through this report together, and you leave with an estimate and a remediation plan.</p><a class="btn" href="${e(BOOK)}" target="_blank" rel="noopener">Book 30 minutes</a>${opts.planUrl ? ` <a href="${e(opts.planUrl)}" style="margin-left:14px">See your remediation plan</a>` : ''}</div>
<p class="note">A scan is the start, not a certification. Automated testing finds a large share of accessibility problems but not all of them. Keyboard access, focus order, zoom, captions and whether descriptions make sense need a person. Our fix includes those checks.</p>

<h2>What fails.</h2>
${wcag.length ? wcag.map(issueCard).join('') : '<p>Nothing the scanner can detect on the pages tested.</p>'}
${adv.length ? `<h2>Worth improving.</h2><p class="mute">Good practice, not WCAG failures. These never block conformance.</p>${adv.map(issueCard).join('')}` : ''}
<h2>What passes.</h2>
${r.passes.length ? `<p class="mute">Problems the scan looked for and did not find on the pages tested:</p><p>${r.passes.slice(0, 14).map(p => `<span class="pill pass">${e(p)}</span>`).join('')}</p>` : '<p class="mute">No checks passed on every tested page.</p>'}

<h2>Your site.</h2>
<table><tbody>
<tr><th scope="row">Platform</th><td>${e(r.profile.platform)}${r.profile.builders.length ? ' · ' + r.profile.builders.map(e).join(', ') : ''}</td></tr>
<tr><th scope="row">Size</th><td>${e(r.profile.sizeNote)} (${r.discovery.total.toLocaleString('en-US')} found from the ${e(r.discovery.source)})</td></tr>
<tr><th scope="row">Page templates</th><td>${r.templates.slice(0, 12).map(t => `<code>${e(t.pattern)}</code> ${t.pages}`).join(' · ')}${r.templates.length > 12 ? ` · and ${r.templates.length - 12} more` : ''}</td></tr>
${r.profile.overlays.length ? `<tr><th scope="row">Accessibility overlay</th><td>${r.profile.overlays.map(e).join(', ')} detected. An overlay does not make the underlying pages conform.</td></tr>` : ''}
</tbody></table>
${r.discovery.notes.map(n => `<p class="mute">${e(n)}</p>`).join('')}

<h2>Outside this scan.</h2>
<ul class="plain">
<li>${o.pdfLinks + r.discovery.pdfsInSitemap ? `${plural(o.pdfLinks + r.discovery.pdfsInSitemap, 'PDF')} linked or listed. Documents are not tested here and are quoted separately.` : 'No PDFs were found on the pages tested.'}</li>
<li>${o.videos ? `${plural(o.videos, 'video')} found. Captions are checked by hand.` : 'No video was found on the pages tested.'}</li>
<li>${o.contrastToCheckByHand ? `${plural(o.contrastToCheckByHand, 'place')} where text sits over an image or gradient. Contrast there is checked by hand.` : 'No text over images needed a hand check.'}</li>
${o.thirdPartyFrames.length ? `<li>Embedded third-party tools the site owner may not control: ${o.thirdPartyFrames.map(f => e(f.host)).join(', ')}.</li>` : ''}
${r.failedToLoad.length ? `<li>${plural(r.failedToLoad.length, 'page')} did not load and could not be tested.</li>` : ''}
</ul>

<h2>Pages tested.</h2>
<details><summary>Show all ${r.pages.length}</summary><table><thead><tr><th scope="col">Page</th><th scope="col">Issues found</th></tr></thead><tbody>
${r.pages.map(p => `<tr><td><a href="${e(p.url)}">${e(p.title || p.url)}</a><br><span class="mute">${e(new URL(p.url).pathname)}</span></td><td>${p.error ? 'Did not load' : p.issues}</td></tr>`).join('')}</tbody></table></details>

<h2>Next step.</h2>
<p class="lede">Book 30 minutes with Tim McCoy to review this report. You get an estimate and a remediation plan. Fixes are made in your site's own code and content, followed by manual checks, a retest and a conformance report. No overlay, no widget.</p>
<p><a class="btn" href="${e(BOOK)}" target="_blank" rel="noopener">Book 30 minutes</a></p>
</main><footer><div class="w"><p>Tested with ${e(r.tool.engine)} at ${r.tool.widths.join(' and ')} pixels wide on ${e(date)}. This report is general information about the pages tested on that date. It is not legal advice and not a certification of conformance. Use of this report is covered by Yoodle's <a href="https://yoodle.com/terms/">Terms</a>.</p><p>Yoodle LLC · Kansas City, Missouri · yoodle.com</p></div></footer></body></html>`;
}
module.exports = { render };
