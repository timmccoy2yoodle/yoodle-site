#!/usr/bin/env node
// Yoodle ADA scanner service.
//   POST /hooks/scan-request?token=HOOK_TOKEN   Netlify form webhook (form "scan-request") -> queues a scan
//   GET  /review/<id>?key=ADMIN_KEY             Tim's draft: report + price/note + approve
//   POST /review/<id>?key=ADMIN_KEY             approve and email the customer, or hold
//   GET  /r/<token>                             the customer's report (only after approval)
//   GET  /review/<id>/plan?key=ADMIN_KEY        remediation plan and scope: Tim fills in hours (POST saves)
//   GET  /r/<token>/plan                        the customer's copy of the plan (only when Tim turns it on)
//   GET  /jobs?key=ADMIN_KEY                    list of every scan
//   GET  /health
const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');
const { scan } = require('./lib/scan'), { render } = require('./lib/report');
const { normalizeInput } = require('./lib/discover');
const plan = require('./lib/plan');
const BOOK = process.env.BOOKING_URL || 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ19B4FBJCID1vLALGmp7HljuV-Cma5K1_z87p5Yf5_WTdactEM9nSq5C4BJ1KBa7WeHK_F0_JLf?gv=true';

const PORT = Number(process.env.PORT) || 8080;
const DATA = path.resolve(process.env.DATA_DIR || './data');
const BASE = (process.env.PUBLIC_URL || `http://localhost:${PORT}`).replace(/\/$/, '');
const HOOK_TOKEN = process.env.HOOK_TOKEN, ADMIN_KEY = process.env.ADMIN_KEY;
const NOTIFY = process.env.NOTIFY_EMAIL || 'tim@yoodle.com', FROM = process.env.MAIL_FROM || 'Yoodle <hello@yoodle.com>';
if (!HOOK_TOKEN || !ADMIN_KEY) { console.error('Set HOOK_TOKEN and ADMIN_KEY before starting.'); process.exit(1); }
for (const d of ['jobs', 'outbox']) fs.mkdirSync(path.join(DATA, d), { recursive: true });

const id = n => crypto.randomBytes(n).toString('hex');
const same = (a, b) => { const x = Buffer.from(String(a || '')), y = Buffer.from(String(b)); return x.length === y.length && crypto.timingSafeEqual(x, y); };
const jobPath = jid => path.join(DATA, 'jobs', jid + '.json');
const load = jid => /^[a-f0-9]{16}$/.test(jid) && fs.existsSync(jobPath(jid)) ? JSON.parse(fs.readFileSync(jobPath(jid), 'utf8')) : null;
const save = job => { const t = jobPath(job.id) + '.tmp'; fs.writeFileSync(t, JSON.stringify(job)); fs.renameSync(t, jobPath(job.id)); };
const all = () => fs.readdirSync(path.join(DATA, 'jobs')).filter(f => f.endsWith('.json')).map(f => JSON.parse(fs.readFileSync(path.join(DATA, 'jobs', f), 'utf8')));
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Email goes out over SMTP when SMTP_URL is set. Without it, messages are written to data/outbox so nothing is lost.
let transport = null;
if (process.env.SMTP_URL) transport = require('nodemailer').createTransport(process.env.SMTP_URL);
async function mail(to, subject, text) {
  const msg = { from: FROM, to, subject, text };
  if (transport) { await transport.sendMail(msg); return 'sent'; }
  fs.writeFileSync(path.join(DATA, 'outbox', Date.now() + '-' + id(3) + '.json'), JSON.stringify(msg, null, 2));
  console.log(`[mail not configured] to ${to}: ${subject}`); return 'saved to outbox';
}

// One scan at a time, so a burst of requests can't overload the server or the sites being scanned.
const queue = []; let running = false;
async function work() {
  if (running) return; running = true;
  while (queue.length) {
    const job = load(queue.shift()); if (!job) continue;
    job.status = 'scanning'; save(job);
    try {
      job.result = await Promise.race([scan(job.url, { log: m => console.log(`[${job.id}] ${m}`) }), new Promise((_, rej) => setTimeout(() => rej(new Error('The scan took too long and was stopped.')), 20 * 60 * 1000))]);
      job.status = 'review';
    } catch (e) { job.status = 'failed'; job.error = e.message; }
    job.finished = new Date().toISOString(); save(job);
    const r = job.result, link = `${BASE}/review/${job.id}?key=${ADMIN_KEY}`;
    const summary = job.status === 'failed' ? `Scan failed: ${job.error}` : !r.ok ? `Not scanned: ${r.reason}`
      : `${r.tested} of ${r.discovery.total} pages tested. ${r.wcagIssues} kinds of WCAG failure (${r.fixNow} fix now, ${r.needsDeveloper} need a developer).\nPlatform: ${r.profile.platform}. Size: ${r.profile.size} (${r.profile.sizeNote}).`;
    await mail(NOTIFY, `Scan ready to review: ${job.url}`, `${job.name} at ${job.organization} <${job.email}> asked for a scan of ${job.url}.\n\n${summary}\n\nReview and send: ${link}`).catch(e => console.error('notify failed', e.message));
  }
  running = false;
}

const recent = new Map(); // email -> timestamps, to cap repeat requests
function limited(email) { const now = Date.now(), list = (recent.get(email) || []).filter(t => now - t < 864e5); list.push(now); recent.set(email, list); return list.length > 3; }

function body(req, max = 200000) { return new Promise((res, rej) => { let b = ''; req.on('data', c => { b += c; if (b.length > max) { rej(new Error('too large')); req.destroy(); } }); req.on('end', () => res(b)); req.on('error', rej); }); }
const send = (res, code, type, text) => { res.writeHead(code, { 'content-type': type + '; charset=utf-8', 'x-robots-tag': 'noindex, nofollow', 'cache-control': 'no-store', 'referrer-policy': 'no-referrer' }); res.end(text); };
const page = (title, inner) => `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(title)}</title><style>body{font:17px/1.5 system-ui,sans-serif;max-width:860px;margin:0 auto;padding:24px;background:#F7F4EE;color:#111}input,textarea{font:inherit;width:100%;padding:12px;border:1.5px solid #111;border-radius:8px;box-sizing:border-box}label{display:block;font-weight:600;margin:16px 0 6px}button{font:inherit;font-weight:600;min-height:48px;padding:0 22px;border-radius:999px;border:0;background:#111;color:#fff;cursor:pointer;margin:18px 10px 0 0}button.alt{background:#fff;color:#111;box-shadow:inset 0 0 0 1.5px #111}iframe{width:100%;height:70vh;border:1px solid #1112;border-radius:10px;background:#fff;margin-top:20px}td,th{text-align:left;padding:8px 12px;border-bottom:1px solid #1112}a{color:#2c2a6f}</style></head><body>${inner}</body></html>`;

http.createServer(async (req, res) => {
  try {
    const u = new URL(req.url, BASE), parts = u.pathname.split('/').filter(Boolean), key = u.searchParams.get('key');
    if (u.pathname === '/health') return send(res, 200, 'text/plain', 'ok');

    if (req.method === 'POST' && u.pathname === '/hooks/scan-request') {
      if (!same(u.searchParams.get('token'), HOOK_TOKEN)) return send(res, 403, 'text/plain', 'forbidden');
      const raw = JSON.parse(await body(req)), d = raw.data || raw;
      if (d['company-site']) return send(res, 200, 'text/plain', 'ignored'); // honeypot field was filled in
      const email = String(d.email || '').trim().toLowerCase();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return send(res, 400, 'text/plain', 'email required');
      let url; try { url = normalizeInput(d.url).href; } catch { return send(res, 400, 'text/plain', 'url required'); }
      if (limited(email)) return send(res, 429, 'text/plain', 'too many requests');
      const job = { id: id(8), token: id(16), status: 'queued', created: new Date().toISOString(), name: String(d.name || '').slice(0, 120), email, organization: String(d.organization || '').slice(0, 160), url };
      // The form requires a tick confirming authorization and agreement to the Terms. Keep the record; never scan without it.
      const agreed = /^(yes|on|true|1)$/i.test(String(d.agree || ''));
      job.consent = { agreed, termsVersion: String(d['terms-version'] || '').slice(0, 20), at: job.created, ip: String(raw.ip || d.ip || '').slice(0, 60) };
      if (!agreed) {
        job.status = 'held'; job.error = 'The form submission did not include the terms agreement, so the site was not scanned.'; save(job);
        await mail(NOTIFY, `Scan NOT run (no terms agreement): ${url}`, `${job.name} at ${job.organization} <${email}> asked for a scan of ${url}, but the submission had no terms agreement. Nothing was scanned.`).catch(() => {});
        return send(res, 202, 'application/json', JSON.stringify({ held: job.id }));
      }
      save(job); queue.push(job.id); work();
      return send(res, 202, 'application/json', JSON.stringify({ queued: job.id }));
    }

    if (parts[0] === 'r' && parts[1]) {
      const job = all().find(j => same(parts[1], j.token));
      if (!job || job.status !== 'sent') return send(res, 404, 'text/plain', 'Not found');
      const shared = job.plan && job.plan.shared;
      if (parts[2] === 'plan') return shared ? send(res, 200, 'text/html', plan.render(job, 'view')) : send(res, 404, 'text/plain', 'Not found');
      return send(res, 200, 'text/html', render(job, { planUrl: shared ? `${BASE}/r/${job.token}/plan` : null }));
    }

    if (!same(key, ADMIN_KEY)) return send(res, 404, 'text/plain', 'Not found');

    if (u.pathname === '/jobs') {
      const rows = all().sort((a, b) => b.created.localeCompare(a.created)).map(j => `<tr><td>${esc(j.created.slice(0, 10))}</td><td>${esc(j.organization)}<br>${esc(j.email)}</td><td>${esc(j.url)}</td><td>${esc(j.status)}</td><td><a href="/review/${j.id}?key=${esc(key)}">Open</a></td></tr>`).join('');
      return send(res, 200, 'text/html', page('Scans', `<h1>Scans</h1><table><thead><tr><th>Date</th><th>Who</th><th>Site</th><th>Status</th><th></th></tr></thead><tbody>${rows || '<tr><td colspan="5">None yet.</td></tr>'}</tbody></table>`));
    }

    if (parts[0] === 'review' && parts[1]) {
      const job = load(parts[1]); if (!job) return send(res, 404, 'text/plain', 'Not found');
      if (parts[2] === 'plan') {
        if (!job.result || !job.result.ok) return send(res, 200, 'text/html', page('Not ready', '<p>There is no scan to plan from yet.</p>'));
        if (req.method === 'POST') { job.plan = plan.fromForm(new URLSearchParams(await body(req)), job.plan); save(job); res.writeHead(303, { location: `/review/${job.id}/plan?key=${encodeURIComponent(key)}` }); return res.end(); }
        return send(res, 200, 'text/html', plan.render(job, 'edit'));
      }
      if (parts[2] === 'draft') return send(res, 200, 'text/html', job.result ? render(job, { draft: job.status !== 'sent' }) : page('Not ready', `<p>${esc(job.error || 'This scan has not finished.')}</p>`));
      if (req.method === 'POST') {
        const f = new URLSearchParams(await body(req));
        job.note = (f.get('note') || '').trim().slice(0, 1200);
        if (f.get('action') === 'send' && job.result && job.result.ok && job.status !== 'sent') {
          job.status = 'sent'; job.sent = new Date().toISOString(); save(job);
          const host = new URL(job.result.site).host;
          job.mail = await mail(job.email, `Your accessibility report for ${host}`, `Hi ${job.name || 'there'},\n\nYour accessibility report for ${host} is ready:\n${BASE}/r/${job.token}\n\nIt shows what passed and what failed on the pages we tested. A scan is the start, not a certification.\n\nNext step: book 30 minutes with me to walk through it. You will leave with an estimate and a remediation plan.\n${BOOK}\n\nReply to this email with any questions.\n\nTim McCoy\nYoodle`);
        } else if (f.get('action') === 'hold') job.status = job.status === 'sent' ? 'sent' : 'held';
        save(job);
        res.writeHead(303, { location: `/review/${job.id}?key=${encodeURIComponent(key)}` }); return res.end();
      }
      const r = job.result;
      const state = { queued: 'Waiting to scan.', scanning: 'Scanning now. Refresh in a few minutes.', failed: 'Scan failed: ' + (job.error || ''), review: 'Ready for your review. Nothing has been sent.', held: 'On hold. Nothing has been sent.', sent: `Sent to ${job.email} on ${(job.sent || '').slice(0, 10)} (${job.mail || ''}).` }[job.status];
      return send(res, 200, 'text/html', page('Review: ' + job.url, `<p><a href="/jobs?key=${esc(key)}">All scans</a></p><h1>${esc(job.url)}</h1><p>${esc(job.name)} · ${esc(job.organization)} · ${esc(job.email)}</p><p><strong>${esc(state)}</strong></p>
${r && r.ok ? `<p>${r.tested} of ${r.discovery.total} pages tested · ${r.wcagIssues} kinds of WCAG failure · ${esc(r.profile.platform)} · size ${esc(r.profile.size)}</p>
<p>Terms agreed: ${job.consent && job.consent.agreed ? 'yes, version ' + esc(job.consent.termsVersion || 'not recorded') + ' on ' + esc((job.consent.at || '').slice(0, 10)) : 'no record'}</p>
<p><a href="/review/${job.id}/plan?key=${esc(key)}"><strong>Open the remediation plan and scope</strong></a> (${job.plan ? 'saved ' + esc((job.plan.updated || '').slice(0, 10)) + (job.plan.shared ? ', customer link on' : ', not shared') : 'hours not filled in yet'})</p>
<form method="post"><label for="note">Note to the customer (optional)</label><textarea id="note" name="note" rows="3">${esc(job.note || '')}</textarea>
${job.status === 'sent' ? '' : '<button name="action" value="send">Approve and email the report</button>'}<button class="alt" name="action" value="save">Save</button>${job.status === 'sent' ? '' : '<button class="alt" name="action" value="hold">Hold, do not send</button>'}</form>
<iframe title="Report preview" src="/review/${job.id}/draft?key=${esc(key)}"></iframe>` : r ? `<p>${esc(r.reason)}</p>` : ''}`));
    }
    send(res, 404, 'text/plain', 'Not found');
  } catch (e) { console.error(e); send(res, 500, 'text/plain', 'Something went wrong.'); }
}).listen(PORT, () => {
  console.log(`Yoodle scanner listening on ${PORT}`);
  // Pick up anything that was queued or mid-scan when the server last stopped.
  for (const j of all()) if (j.status === 'queued' || j.status === 'scanning') queue.push(j.id);
  work();
});
