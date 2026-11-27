// Runs the scan: discover pages, sample across templates, test each page with axe-core at desktop and phone widths.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const { UA, normalizeInput, assertPublic, discover, sample } = require('./discover');
const { profile } = require('./profile');
const { describe } = require('./classify');
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const AXE_VERSION = require('axe-core/package.json').version;
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'];
const WIDTHS = [[1440, 900, 'desktop'], [375, 800, 'phone']];

async function scan(rawUrl, opts = {}) {
  const cap = opts.cap || Number(process.env.PAGE_CAP) || 50;
  const log = opts.log || (() => {});
  const started = new Date();
  const input = normalizeInput(rawUrl);
  await assertPublic(input.href);

  // Follow redirects on the home page first, so the scan runs on the address the site really lives at.
  const grab = u => fetch(u, { headers: { 'user-agent': UA }, redirect: 'follow', signal: AbortSignal.timeout(20000) });
  let home;
  try { home = await grab(input.href); }
  catch (err) {
    // No scheme typed and https did not answer: try plain http before giving up.
    if (/^https?:\/\//i.test(String(rawUrl).trim())) throw new Error('The site did not respond.');
    input.protocol = 'http:';
    try { home = await grab(input.href); } catch { throw new Error('The site did not respond.'); }
  }
  const homeHtml = await home.text();
  const start = new URL(home.url); start.hash = '';
  await assertPublic(start.href);

  const found = await discover(start);
  if (found.source === 'blocked') return { ok: false, input: input.href, site: start.origin, reason: found.notes[0], started, finished: new Date() };
  const { picked, templates } = sample(found.urls, start.href, cap);
  log(`${found.total} pages found (${found.source}), ${templates.length} templates, testing ${picked.length}`);

  const browser = await chromium.launch();
  const rules = new Map(), passed = new Map(), pages = [], thirdParty = new Map();
  let manualContrast = 0, pdfLinks = new Set(), forms = 0, videos = 0;
  try {
    for (const url of picked) {
      const rec = { url, title: '', status: null, error: null, issues: 0 };
      const seen = new Set();
      for (const [w, h, label] of WIDTHS) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, userAgent: UA + ' ' + label, bypassCSP: true, reducedMotion: 'reduce' });
        const page = await ctx.newPage();
        await page.route('**/*', r => /^(https?|data|blob):/.test(r.request().url()) ? r.continue() : r.abort());
        try {
          const resp = await page.goto(url, { waitUntil: 'load', timeout: 30000 });
          rec.status = resp ? resp.status() : null;
          if (!resp || resp.status() >= 400) throw new Error('HTTP ' + rec.status);
          // Scroll-reveal effects hide text until it is scrolled into view, which reads as a contrast failure.
          // Finish every animation and scroll the whole page first, so the test sees what a visitor sees.
          await page.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;scroll-behavior:auto!important}' }).catch(() => {});
          await page.evaluate(async () => {
            const step = Math.max(300, innerHeight - 100), max = Math.min(document.documentElement.scrollHeight, 40000);
            for (let y = 0; y < max; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
            scrollTo(0, 0);
          });
          await page.waitForTimeout(500);
          await page.evaluate(AXE);
          const r = await page.evaluate(async tags => {
            const res = await axe.run(document, { runOnly: { type: 'tag', values: tags }, resultTypes: ['violations', 'incomplete', 'passes'] });
            return {
              title: document.title,
              violations: res.violations.map(v => ({ id: v.id, impact: v.impact, tags: v.tags, help: v.help, nodes: v.nodes.map(n => ({ target: n.target.join(' '), html: n.html.slice(0, 160) })) })),
              contrastManual: (res.incomplete.find(i => i.id === 'color-contrast') || { nodes: [] }).nodes.length,
              passes: res.passes.map(p => p.id),
              frames: [...document.querySelectorAll('iframe[src]')].map(f => { try { return new URL(f.src).hostname; } catch { return null; } }).filter(Boolean),
              pdfs: [...document.querySelectorAll('a[href$=".pdf" i]')].map(a => a.href),
              forms: document.forms.length, videos: document.querySelectorAll('video, iframe[src*="youtube"], iframe[src*="vimeo"]').length,
            };
          }, TAGS);
          rec.title = r.title;
          for (const v of r.violations) {
            if (!rules.has(v.id)) rules.set(v.id, { id: v.id, impact: v.impact, tags: v.tags, help: v.help, pages: new Set(), count: 0, widths: new Set(), samples: [] });
            const agg = rules.get(v.id); agg.widths.add(label);
            for (const n of v.nodes) {
              const key = v.id + '|' + n.target; if (seen.has(key)) continue; seen.add(key);
              agg.count++; agg.pages.add(url); rec.issues++;
              if (agg.samples.length < 3) agg.samples.push({ url, target: n.target, html: n.html });
            }
          }
          for (const id of r.passes) passed.set(id, (passed.get(id) || 0) + 1);
          if (label === 'desktop') {
            manualContrast += r.contrastManual; forms += r.forms; videos += r.videos;
            r.pdfs.forEach(p => pdfLinks.add(p));
            const host = new URL(url).hostname;
            r.frames.filter(f => f !== host).forEach(f => thirdParty.set(f, (thirdParty.get(f) || 0) + 1));
          }
        } catch (e) { rec.error = e.message.split('\n')[0]; }
        await ctx.close();
      }
      pages.push(rec); log(`${rec.error ? 'FAILED' : 'ok'} ${url}${rec.error ? ' (' + rec.error + ')' : ''}`);
      await new Promise(r => setTimeout(r, 400)); // be polite to the site being scanned
    }
  } finally { await browser.close(); }

  const tested = pages.filter(p => !p.error);
  const issues = [...rules.values()].map(a => ({ id: a.id, ...describe(a), count: a.count, pages: a.pages.size, widths: [...a.widths], samples: a.samples }));
  const rank = { Critical: 0, Serious: 1, Moderate: 2, Minor: 3 };
  issues.sort((a, b) => a.advisory - b.advisory || rank[a.severity] - rank[b.severity] || b.count - a.count);
  const failedIds = new Set(rules.keys());
  const { describe: d } = require('./classify');
  const passes = [...passed.keys()].filter(id => !failedIds.has(id)).map(id => d({ id, tags: [], help: id })).filter(p => !/^ARIA|^[a-z-]+$/.test(p.name)).map(p => p.name);

  return {
    ok: true, input: input.href, site: start.origin, started, finished: new Date(),
    tool: { engine: 'axe-core ' + AXE_VERSION, standard: 'WCAG 2.1 Level A and AA', widths: WIDTHS.map(w => w[0]) },
    discovery: { total: found.total, source: found.source, pdfsInSitemap: found.pdfs, notes: found.notes },
    templates, profile: profile(homeHtml, home.headers, found.total),
    tested: tested.length, failedToLoad: pages.filter(p => p.error).map(p => ({ url: p.url, error: p.error })),
    pages, issues,
    wcagIssues: issues.filter(i => !i.advisory).length, advisories: issues.filter(i => i.advisory).length,
    fixNow: issues.filter(i => !i.advisory && i.fix === 'fix').length, needsDeveloper: issues.filter(i => !i.advisory && i.fix === 'developer').length,
    passes,
    outside: { pdfLinks: pdfLinks.size, videos, forms, thirdPartyFrames: [...thirdParty.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12).map(([host, n]) => ({ host, pages: n })), contrastToCheckByHand: manualContrast },
  };
}
module.exports = { scan };
