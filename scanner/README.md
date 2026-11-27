# Yoodle ADA scanner (v1)

Turns a "Get your free report" form submission on yoodle.com/accessibility/ into a drafted WCAG 2.1 AA report that Tim approves before it is emailed. Nothing reaches a customer without approval.

## Flow
1. Visitor submits the `scan-request` form (page or popup): name, work email, organization, URL.
2. Netlify sends the submission to `POST /hooks/scan-request?token=…`.
3. The scanner reads robots.txt and the sitemap, counts pages, groups them into templates by URL shape, and tests up to 50 pages (at least one per template) with axe-core at 1440 and 375 pixels wide.
4. Tim gets an email with a review link: summary, the draft report, an optional price and note.
5. "Approve and email the report" sends the customer a private link (`/r/<token>`). Until then that link returns 404.

## What the report says
Pages found vs. tested, kinds of WCAG failure (grouped by issue, with examples), which are "fix it now" vs. "needs a developer", advisories that are not WCAG failures, what the scan did not find, platform and size, and what sits outside an automated scan (PDFs, video captions, text over images, third-party embeds). Every report states that a scan is not a certification.

## Run it
```
npm install && npx playwright install chromium
node cli.js https://example.edu out/            # one scan, writes out/report.html and out/scan.json
HOOK_TOKEN=… ADMIN_KEY=… node server.js         # the service
```
| Variable | Purpose |
|---|---|
| `HOOK_TOKEN` | Secret in the Netlify webhook URL. Required. |
| `ADMIN_KEY` | Secret in Tim's review links. Required. |
| `PUBLIC_URL` | The service's public https address, used in emailed links. |
| `SMTP_URL` | `smtps://user:pass@host:465`. Without it, emails are saved to `data/outbox/` instead of sent. |
| `NOTIFY_EMAIL`, `MAIL_FROM` | Default `tim@yoodle.com` and `Yoodle <hello@yoodle.com>`. |
| `DATA_DIR` | Where jobs are stored (JSON files). Needs a persistent disk. |
| `PAGE_CAP` | Pages tested per scan. Default 50. |

Netlify: Project `yoodle-site` → Forms → Form notifications → Outgoing webhook → form `scan-request` → `https://<scanner host>/hooks/scan-request?token=<HOOK_TOKEN>`.

## Tested (Nov 27, 2026)
- Scan of a local copy of yoodle.com: 90 pages found from the sitemap, 12 templates, 14 tested, 0 failures (matches the site's own QA).
- Scan of `test/fixture/` (a deliberately broken page): 9 kinds of WCAG failure and 3 advisories found, WordPress and Divi detected.
- Webhook → scan → review → approve → customer link, including wrong token (403), honeypot, and the customer link staying 404 until approval.
- The report page itself: 0 axe violations at 1280 and 375 wide.

Not yet tested: the Dockerfile on a real host, real SMTP delivery, the real Netlify webhook payload, and scans of sites that block automated browsers.

## Safeguards
- Only public http(s) addresses on standard ports; private and local addresses are refused (`ALLOW_LOCAL=1` lifts this for testing only).
- robots.txt is honored; a site that disallows crawling is not scanned.
- One scan at a time, 400 ms between pages, 20-minute ceiling per scan, 3 requests per email per day.
- Animations are finished and the page is scrolled before testing, so scroll-reveal effects don't read as contrast failures.
- Reports are noindex and reachable only by an unguessable link.

## Not in v1
Card checkout, storing customer site logins, the fix queue, monitoring rescans, chat. See `strategy/compliance-product-model-nov2026.md` in the Yoodle project.
