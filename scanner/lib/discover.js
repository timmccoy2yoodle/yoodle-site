// Finds a site's pages: robots.txt -> sitemaps -> (fallback) links on the home page.
const dns = require('dns').promises, net = require('net');
const UA = 'YoodleAccessibilityScan/1.0 (+https://yoodle.com/accessibility/)';
const MAX_URLS = 20000, MAX_SITEMAPS = 40;

function isPrivate(ip) {
  if (net.isIPv6(ip)) return ip === '::1' || /^f[cd]/i.test(ip) || /^fe80/i.test(ip) || ip.startsWith('::ffff:') && isPrivate(ip.slice(7));
  const p = ip.split('.').map(Number);
  return p[0] === 10 || p[0] === 127 || p[0] === 0 || (p[0] === 172 && p[1] >= 16 && p[1] <= 31) || (p[0] === 192 && p[1] === 168) || (p[0] === 169 && p[1] === 254) || p[0] >= 224;
}
// Refuse anything that is not a public http(s) site, so the scanner can't be pointed at internal systems.
async function assertPublic(u) {
  const url = new URL(u);
  if (!/^https?:$/.test(url.protocol)) throw new Error('Only http and https addresses can be scanned.');
  if (process.env.ALLOW_LOCAL === '1') return url;
  if (url.port && !['80', '443'].includes(url.port)) throw new Error('Only standard web ports can be scanned.');
  const addrs = net.isIP(url.hostname) ? [{ address: url.hostname }] : await dns.lookup(url.hostname, { all: true });
  if (!addrs.length || addrs.some(a => isPrivate(a.address))) throw new Error('That address is not a public website.');
  return url;
}
function normalizeInput(raw) {
  let v = String(raw || '').trim();
  if (!v) throw new Error('No web address given.');
  if (!/^https?:\/\//i.test(v)) v = 'https://' + v;
  const u = new URL(v); u.hash = '';
  return u;
}
async function get(url, timeout = 15000) {
  const r = await fetch(url, { headers: { 'user-agent': UA }, redirect: 'follow', signal: AbortSignal.timeout(timeout) });
  return { ok: r.ok, status: r.status, url: r.url, headers: r.headers, text: r.ok ? await r.text() : '' };
}
function parseRobots(txt) {
  const sitemaps = [], disallow = []; let applies = false;
  for (const line of txt.split(/\r?\n/)) {
    const m = line.replace(/#.*/, '').match(/^\s*([A-Za-z-]+)\s*:\s*(.*?)\s*$/); if (!m) continue;
    const k = m[1].toLowerCase(), v = m[2];
    if (k === 'sitemap') sitemaps.push(v);
    else if (k === 'user-agent') applies = v === '*' || /yoodle/i.test(v);
    else if (k === 'disallow' && applies && v) disallow.push(v);
  }
  return { sitemaps, disallow };
}
const locs = xml => [...xml.matchAll(/<loc>\s*(?:<!\[CDATA\[)?\s*([^<\]]+?)\s*(?:\]\]>)?\s*<\/loc>/gi)].map(m => m[1].replace(/&amp;/g, '&'));
const isPage = u => !/\.(pdf|docx?|xlsx?|pptx?|zip|jpe?g|png|gif|webp|svg|mp4|mp3|ics|xml|json|css|js)(\?|$)/i.test(u);

async function discover(start) {
  const origin = start.origin, notes = [];
  let robots = { sitemaps: [], disallow: [] };
  try { const r = await get(origin + '/robots.txt'); if (r.ok) robots = parseRobots(r.text); } catch {}
  const allowed = u => { try { const p = new URL(u).pathname; return !robots.disallow.some(d => p.startsWith(d)); } catch { return false; } };
  if (robots.disallow.includes('/')) return { origin, urls: [], total: 0, pdfs: 0, source: 'blocked', notes: ['robots.txt asks crawlers not to visit this site, so it was not scanned.'] };

  const queue = [...robots.sitemaps, origin + '/sitemap.xml', origin + '/sitemap_index.xml'];
  const seen = new Set(), urls = new Set(); let pdfs = 0, fetched = 0;
  while (queue.length && fetched < MAX_SITEMAPS && urls.size < MAX_URLS) {
    const sm = queue.shift(); if (seen.has(sm)) continue; seen.add(sm);
    try {
      const r = await get(sm); if (!r.ok || !/<(urlset|sitemapindex)/i.test(r.text)) continue; fetched++;
      const found = locs(r.text);
      if (/<sitemapindex/i.test(r.text)) queue.push(...found);
      else for (const u of found) { if (/\.pdf(\?|$)/i.test(u)) pdfs++; else if (isPage(u) && u.startsWith(origin)) urls.add(u.split('#')[0]); }
    } catch {}
  }
  let source = 'sitemap';
  if (!urls.size) {
    source = 'home page links';
    notes.push('No sitemap was found, so pages were taken from links on the home page. The real page count is likely higher.');
    try {
      const r = await get(start.href);
      for (const m of r.text.matchAll(/href\s*=\s*["']([^"'#]+)["']/gi)) {
        try { const u = new URL(m[1], r.url); if (u.origin === new URL(r.url).origin) { if (isPage(u.href)) urls.add(u.href); } } catch {}
      }
    } catch (e) { notes.push('The home page could not be read: ' + e.message); }
  }
  urls.add(start.href);
  if (urls.size >= MAX_URLS) notes.push(`Page count stopped at ${MAX_URLS}; the site is larger.`);
  return { origin, urls: [...urls].filter(allowed), total: urls.size, pdfs, source, notes };
}

// Group pages into likely templates by URL shape, then sample across groups so every template gets tested.
function templateKey(u) {
  const segs = new URL(u).pathname.split('/').filter(Boolean);
  if (!segs.length) return '/';
  return '/' + segs[0] + (segs.length > 1 ? '/*'.repeat(Math.min(segs.length - 1, 2)) : '');
}
function sample(urls, home, cap) {
  const groups = new Map();
  for (const u of urls) { const k = templateKey(u); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(u); }
  for (const g of groups.values()) g.sort((a, b) => a.length - b.length || a.localeCompare(b));
  const picked = [home], lists = [...groups.entries()].sort((a, b) => b[1].length - a[1].length);
  for (let i = 0; picked.length < cap; i++) {
    let added = false;
    for (const [, g] of lists) { if (picked.length >= cap) break; if (g[i] && !picked.includes(g[i])) { picked.push(g[i]); added = true; } }
    if (!added) break;
  }
  return { picked, templates: lists.map(([k, g]) => ({ pattern: k, pages: g.length })) };
}
module.exports = { UA, normalizeInput, assertPublic, discover, sample, templateKey };
