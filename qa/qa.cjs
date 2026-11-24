const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');
const root = path.resolve(process.argv[2] || 'site'), out = path.resolve(process.argv[3] || 'qa');
fs.mkdirSync(out, { recursive: true });
const types = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.svg':'image/svg+xml', '.webp':'image/webp', '.png':'image/png', '.jpg':'image/jpeg', '.xml':'application/xml', '.txt':'text/plain', '.json':'application/json', '.woff2':'font/woff2' };
const server = http.createServer((req, res) => {
  let p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
  if (!p.startsWith(root) || !fs.existsSync(p)) { res.writeHead(404); return res.end('404'); }
  res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
});
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.html') ? [path.join(d, e.name)] : []);
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}/`;
  const pages = walk(root).map(f => path.relative(root, f).split(path.sep).join('/'));
  const browser = await chromium.launch(), problems = [], seo = {};
  const add = (page, width, issue) => problems.push({ page, width, issue });
  const shots = (process.env.SHOTS || '').split(',');
  for (const pg of pages) for (const width of [1440, 768, 375]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.addInitScript('window.__noPopup=true');
    page.on('console', m => m.type() === 'error' && add(pg, width, 'console error: ' + m.text()));
    page.on('pageerror', e => add(pg, width, 'script error: ' + e.message));
    page.on('response', r => r.status() >= 400 && add(pg, width, `failed request ${r.status()}: ${r.url().replace(base, '')}`));
    await page.goto(base + pg, { waitUntil: 'networkidle' });
    const d = await page.evaluate(() => {
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      return {
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        title: document.title, desc: document.querySelector('meta[name=description]')?.content || '',
        h1: document.querySelectorAll('h1').length, lang: document.documentElement.lang,
        small: [...document.querySelectorAll('a,button,input[type=submit],summary')].filter(vis).filter(e => { const r = e.getBoundingClientRect(); return r.height < 44 && getComputedStyle(e).display !== 'inline'; }).map(e => (e.textContent || e.value || '').trim().slice(0, 30)),
        links: [...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => h.startsWith(location.origin)),
        forms: [...document.forms].map(f => ({ netlify: f.hasAttribute('data-netlify'), name: f.getAttribute('name'), hidden: !!f.querySelector('input[name=form-name]') })),
      };
    });
    if (d.overflow) add(pg, width, 'sideways scroll');
    if (width === 375) d.small.forEach(t => add(pg, width, `tap target under 44px: "${t}"`));
    if (width === 1440) {
      seo[pg] = { title: d.title, desc: d.desc };
      if (!d.title) add(pg, width, 'missing <title>');
      if (d.title.length > 70) add(pg, width, 'title over 70 chars: ' + d.title.length);
      if (!d.desc) add(pg, width, 'missing meta description');
      if (d.desc.length > 160) add(pg, width, 'description over 160 chars: ' + d.desc.length);
      if (d.h1 !== 1) add(pg, width, `expected one h1, found ${d.h1}`);
      if (!d.lang) add(pg, width, 'missing lang');
      for (const l of [...new Set(d.links)]) { const r = await page.request.get(l.split('#')[0]); if (!r.ok()) add(pg, width, `broken link ${r.status()}: ${l.replace(base, '')}`); }
      d.forms.forEach(f => { if (f.netlify && (!f.name || !f.hidden)) add(pg, width, 'Netlify form missing name or hidden form-name field'); });
    }
    if (shots.includes(pg) && width !== 768) await page.screenshot({ path: path.join(out, `${pg.replace(/[\/.]/g, '_')}-${width}.png`), fullPage: width===1440 });
    await page.close();
  }
  for (const k of ['title', 'desc']) { const seen = {}; for (const [pg, v] of Object.entries(seo)) if (v[k]) (seen[v[k]] ||= []).push(pg); for (const [val, ps] of Object.entries(seen)) if (ps.length > 1) add(ps.join(', '), 1440, `duplicate ${k}: "${val.slice(0, 50)}"`); }
  for (const f of ['sitemap.xml', 'robots.txt']) if (!fs.existsSync(path.join(root, f))) add(f, '-', 'file missing');
  await browser.close(); server.close();
  console.log(`${pages.length} pages x 3 widths checked. ${problems.length} problems.`);
  const seenI = {}; problems.forEach(p => { const k = p.issue + '@' + p.width; (seenI[k] ||= []).push(p.page); });
  Object.entries(seenI).slice(0, 40).forEach(([k, v]) => console.log(`- ${k}  [${v.length} pages, e.g. ${v[0]}]`));
})();
