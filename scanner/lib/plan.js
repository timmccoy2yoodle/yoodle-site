// Builds the remediation plan and project scope from a scan. Hours are Tim's to fill in; nothing is estimated here.
const e = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const RATE = Number(process.env.RATE) || 125;
const money = n => '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
// Problems that live in page content (fixed page by page) rather than in templates and styles (fixed once).
const CONTENT = new Set(['image-alt', 'input-image-alt', 'role-img-alt', 'svg-img-alt', 'area-alt', 'object-alt', 'link-name', 'empty-heading', 'heading-order', 'image-redundant-alt', 'video-caption', 'td-headers-attr', 'th-has-data-cells', 'valid-lang', 'list', 'listitem', 'definition-list', 'dlitem']);

function lines(r) {
  const basis = i => `${i.wcag.length ? 'WCAG ' + i.wcag.join(', ') + ' · ' : ''}${i.count} found on ${i.pages} of ${r.tested} pages tested`;
  const wcag = r.issues.filter(i => !i.advisory), o = r.outside, L = [];
  const add = (phase, id, task, note) => L.push({ phase, id, task, note });
  for (const i of wcag.filter(i => i.fix === 'fix' && !CONTENT.has(i.id))) add('Template and style fixes', 't-' + i.id, i.name, basis(i) + '. Fixed once in the template or stylesheet.');
  for (const i of wcag.filter(i => i.fix === 'fix' && CONTENT.has(i.id))) add('Content fixes', 'c-' + i.id, i.name, basis(i) + `. Fixed page by page; the full site has ${r.discovery.total.toLocaleString('en-US')} pages.`);
  for (const i of wcag.filter(i => i.fix === 'developer')) add('Developer work', 'd-' + i.id, i.name, basis(i) + '. Needs a developer to rebuild or rework.');
  const adv = r.issues.filter(i => i.advisory);
  if (adv.length) add('Recommended improvements', 'adv', 'Good-practice items: ' + adv.map(a => a.name.toLowerCase()).join('; '), 'Not WCAG failures. Optional.');
  add('Full audit and manual checks', 'm-crawl', `Test all ${r.discovery.total.toLocaleString('en-US')} pages`, `The free scan tested ${r.tested}. The full audit covers every page.`);
  add('Full audit and manual checks', 'm-keyboard', 'Keyboard-only pass, focus order and visible focus', 'WCAG 2.1.1, 2.1.2, 2.4.3, 2.4.7. One pass per template.');
  add('Full audit and manual checks', 'm-mobile', 'Phone menu, 200% zoom and 320-pixel reflow', 'WCAG 1.4.4, 1.4.10, 2.1.1');
  add('Full audit and manual checks', 'm-sr', 'Screen reader pass', 'WCAG 1.3.1, 2.4.6, 4.1.2');
  add('Full audit and manual checks', 'm-alt', 'Review existing image descriptions for accuracy', 'WCAG 1.1.1');
  if (o.contrastToCheckByHand) add('Full audit and manual checks', 'm-contrast', 'Contrast of text over images and gradients', `WCAG 1.4.3 · ${o.contrastToCheckByHand} places flagged on the pages tested`);
  if (o.forms) add('Full audit and manual checks', 'm-forms', 'Forms: labels, errors and instructions', `WCAG 3.3.1, 3.3.2, 3.3.3 · ${o.forms} forms on the pages tested`);
  if (o.videos) add('Full audit and manual checks', 'm-media', 'Video and audio: captions and transcripts', `WCAG 1.2.1 to 1.2.5 · ${o.videos} found on the pages tested`);
  add('Retest and conformance report', 'r-retest', 'Retest every page after fixes', '');
  add('Retest and conformance report', 'r-report', 'Conformance report', 'Page-by-page result against WCAG 2.1 AA');
  add('Project management', 'pm', 'Kickoff, access setup, status updates and client review', '');
  add('Optional', 'o-train', 'Training for content editors', 'So new pages stay accessible');
  const pdfs = o.pdfLinks + r.discovery.pdfsInSitemap;
  if (pdfs) add('Optional', 'o-pdf', 'PDF and document remediation', `${pdfs} PDFs found so far. Quoted separately once the full count is known.`);
  add('Optional', 'o-monitor', 'Monthly monitoring: rescans and fixes for new issues', 'Per month');
  return L;
}

// mode: 'edit' (Tim fills hours), 'view' (customer copy)
function render(job, mode) {
  const r = job.result, plan = job.plan || {}, hours = plan.hours || {}, custom = plan.custom || [];
  const host = new URL(r.site).host, L = lines(r), edit = mode === 'edit';
  const date = new Date(plan.updated || r.finished).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const val = id => hours[id] === undefined || hours[id] === '' ? '' : Number(hours[id]);
  const row = (id, task, note, optional) => {
    const h = val(id);
    return `<tr${optional ? ' class="opt"' : ''}><td><strong>${e(task)}</strong>${note ? `<br><span class="mute">${e(note)}</span>` : ''}</td>
<td class="n">${edit ? `<input type="number" min="0" step="0.25" inputmode="decimal" name="h-${e(id)}" value="${h}" aria-label="Hours: ${e(task)}" data-opt="${optional ? 1 : 0}">` : (h === '' ? '<span class="tbc">To be confirmed</span>' : h)}</td>
<td class="n amt">${h === '' ? '' : money(h * RATE)}</td></tr>`;
  };
  let body = '', phase = null;
  for (const l of L) { if (l.phase !== phase) { phase = l.phase; body += `<tr class="ph"><th scope="colgroup" colspan="3">${e(phase)}</th></tr>`; } body += row(l.id, l.task, l.note, l.phase === 'Optional'); }
  const rowsCustom = edit ? [0, 1, 2].map(k => { const c = custom[k] || {}; return `<tr><td><input type="text" name="ct-${k}" value="${e(c.task || '')}" placeholder="Add a line" aria-label="Extra line ${k + 1}"></td><td class="n"><input type="number" min="0" step="0.25" name="ch-${k}" value="${c.hours ?? ''}" aria-label="Hours for extra line ${k + 1}" data-opt="0"></td><td class="n amt">${c.hours ? money(c.hours * RATE) : ''}</td></tr>`; }).join('')
    : custom.filter(c => c.task).map(c => `<tr><td><strong>${e(c.task)}</strong></td><td class="n">${c.hours ?? '<span class="tbc">To be confirmed</span>'}</td><td class="n amt">${c.hours ? money(c.hours * RATE) : ''}</td></tr>`).join('');
  if (rowsCustom) body += `<tr class="ph"><th scope="colgroup" colspan="3">Additional items</th></tr>` + rowsCustom;

  const core = L.filter(l => l.phase !== 'Optional' && l.phase !== 'Recommended improvements');
  const filled = core.every(l => val(l.id) !== '');
  const sum = core.reduce((t, l) => t + (val(l.id) || 0), 0) + custom.reduce((t, c) => t + (Number(c.hours) || 0), 0);
  const total = filled ? `${sum} hours · ${money(sum * RATE)}` : (edit ? `${sum} hours · ${money(sum * RATE)} so far` : 'To be confirmed');
  const field = (name, label, ph) => edit ? `<label for="${name}">${label}</label><textarea id="${name}" name="${name}" rows="2" placeholder="${e(ph)}">${e(plan[name] || '')}</textarea>` : `<h3>${label}</h3><p>${plan[name] ? e(plan[name]) : '<span class="tbc">To be confirmed</span>'}</p>`;

  return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Remediation plan: ${e(host)} | Yoodle</title>
<style>:root{--bg:#F7F4EE;--ink:#111110;--mute:#55524c;--line:#11111022;--acc:#2c2a6f;--amber:#ffe9a8;--amber-t:#4d3400}*{box-sizing:border-box}body{margin:0;font:17px/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--bg);overflow-wrap:anywhere}.w{max-width:980px;margin:0 auto;padding:0 22px}
header{padding:28px 0;border-bottom:1px solid var(--line)}.brand{font-weight:700;font-size:1.6rem;letter-spacing:-.03em;text-decoration:none;color:var(--ink)}.brand span{color:var(--acc)}h1{font-size:clamp(2rem,6vw,3.4rem);line-height:1.02;letter-spacing:-.04em;margin:32px 0 10px}h2{font-size:clamp(1.4rem,3.4vw,2rem);letter-spacing:-.03em;margin:48px 0 14px}h3{font-size:1.05rem;margin:20px 0 4px}
.mute{color:var(--mute);font-size:.93rem}.tbc{color:var(--mute);font-style:italic}a{color:var(--acc)}:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
table{border-collapse:collapse;width:100%;background:#fff;border-radius:12px;overflow:hidden}td,th{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}thead th{font-size:.85rem}tr.ph th{background:var(--ink);color:var(--bg);font-size:.95rem}tr.opt td{background:#fbfaf7}.n{text-align:right;white-space:nowrap;width:1%}
input,textarea{font:inherit;border:1.5px solid var(--ink);border-radius:8px;padding:8px 10px;background:#fff;color:var(--ink)}input[type=number]{width:5.5em;text-align:right;min-height:44px}input[type=text],textarea{width:100%;min-height:44px}label{display:block;font-weight:600;margin:18px 0 6px}
.total{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-top:14px;font-size:1.25rem;font-weight:650}.note{background:var(--amber);color:var(--amber-t);padding:14px 18px;border-radius:10px;font-weight:600}
button,.btn{font:inherit;font-weight:600;min-height:48px;padding:0 22px;border-radius:999px;border:0;background:var(--ink);color:var(--bg);cursor:pointer;margin:18px 10px 0 0;display:inline-flex;align-items:center;text-decoration:none}ul{padding-left:1.1em}footer{margin-top:64px;padding:26px 0 48px;border-top:1px solid var(--line);font-size:.92rem;color:var(--mute)}
@media (max-width:640px){td,th{padding:10px}.amt{display:none}}@media print{header,button,.noprint{display:none!important}body{background:#fff}}</style></head><body>
<header><div class="w"><a class="brand" href="https://yoodle.com/">yoodle<span>.</span></a></div></header><main class="w">
${edit ? `<p class="note noprint" style="margin-top:24px">Your working copy. Fill in the hours; totals use $${RATE} an hour. Blank lines show as &ldquo;To be confirmed&rdquo; on the customer copy.${plan.shared ? ' The customer link is on.' : ' The customer cannot see this yet.'}</p>` : ''}
<p class="mute" style="margin:28px 0 0">Remediation plan and project scope · ${e(date)}${job.organization ? ' · prepared for ' + e(job.organization) : ''}</p>
<h1>${e(host)}</h1>
<p>Based on an automated scan of ${r.tested} of ${r.discovery.total.toLocaleString('en-US')} pages across ${r.templates.length} page templates on ${e(r.profile.platform)}. Goal: conformance with WCAG 2.1 Level AA.</p>
${edit ? `<form method="post">` : ''}
<h2>Scope of work.</h2>
<table><thead><tr><th scope="col">Task</th><th scope="col" class="n">Hours</th><th scope="col" class="n amt">At $${RATE}/hour</th></tr></thead><tbody>${body}</tbody></table>
<div class="total"><span>Estimate, excluding optional items</span><span id="total">${total}</span></div>
<p class="mute">Rate: $${RATE} an hour. Optional and recommended items are priced separately if chosen.</p>
<h2>Plan.</h2>
${field('timeline', 'Timeline', 'e.g. 6 weeks from kickoff')}
${field('access', 'Access we need', `e.g. admin account on ${r.profile.platform}, staging site`)}
${field('assumptions', 'Assumptions and exclusions', 'e.g. third-party tools the site embeds are outside scope')}
${field('notes', 'Notes', '')}
${edit ? `<label style="display:flex;gap:10px;align-items:center;font-weight:500"><input type="checkbox" name="shared" value="1"${plan.shared ? ' checked' : ''} style="width:22px;height:22px"> Turn on the customer link to this plan</label>
<button>Save plan</button> <button type="button" class="noprint" style="background:#fff;color:#111;box-shadow:inset 0 0 0 1.5px #111" onclick="window.print()">Print or save as PDF</button></form>` : ''}
<h2>How we work.</h2>
<ul><li>Fixes are made in the site&rsquo;s own code and content. No overlay, no widget.</li><li>We back up before changing anything and work on a staging copy when one exists.</li><li>After the fixes we do the manual checks, retest every page and deliver a conformance report.</li></ul>
<p class="mute">This is an estimate, not an offer or a contract. It is based on a sample of pages and may change after the full audit. Work begins only under a signed agreement. It is not legal advice and not a certification of conformance.</p>
</main><footer><div class="w"><p>Yoodle LLC · Kansas City, Missouri · yoodle.com</p></div></footer>
${edit ? `<script>(function(){var R=${RATE},f=document.forms[0];function m(n){return '$'+n.toLocaleString('en-US',{maximumFractionDigits:2})}function calc(){var s=0;f.querySelectorAll('input[type=number]').forEach(function(i){var v=parseFloat(i.value),c=i.closest('tr').querySelector('.amt');if(c)c.textContent=isNaN(v)?'':m(v*R);if(!isNaN(v)&&i.dataset.opt!=='1'&&!/^h-adv$/.test(i.name))s+=v});document.getElementById('total').textContent=s+' hours · '+m(s*R)+' so far'}f.addEventListener('input',calc)})();</script>` : ''}
</body></html>`;
}
function fromForm(f, prev) {
  const hours = {}, custom = [];
  for (const [k, v] of f) if (k.startsWith('h-') && v !== '' && !isNaN(Number(v)) && Number(v) >= 0) hours[k.slice(2)] = Number(v);
  for (const k of [0, 1, 2]) { const task = (f.get('ct-' + k) || '').trim().slice(0, 200), h = f.get('ch-' + k); if (task) custom.push({ task, hours: h !== '' && h !== null && !isNaN(Number(h)) ? Number(h) : null }); }
  const t = n => (f.get(n) || '').trim().slice(0, 1500);
  return { ...(prev || {}), hours, custom, timeline: t('timeline'), access: t('access'), assumptions: t('assumptions'), notes: t('notes'), shared: f.get('shared') === '1', updated: new Date().toISOString() };
}
module.exports = { render, fromForm, lines, RATE };
