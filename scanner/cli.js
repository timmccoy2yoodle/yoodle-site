#!/usr/bin/env node
// Run one scan from the command line:  node cli.js https://example.edu [out-folder]
const fs = require('fs'), path = require('path');
const { scan } = require('./lib/scan'), { render } = require('./lib/report');
(async () => {
  const [url, out = 'out'] = process.argv.slice(2);
  if (!url) { console.error('Usage: node cli.js <url> [out-folder]'); process.exit(1); }
  const result = await scan(url, { log: m => console.log(m) });
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, 'scan.json'), JSON.stringify(result, null, 2));
  fs.writeFileSync(path.join(out, 'report.html'), render({ result }, { draft: true }));
  if (!result.ok) { console.log('Not scanned: ' + result.reason); return; }
  console.log(`\n${result.tested} pages tested of ${result.discovery.total}. ${result.wcagIssues} kinds of WCAG failure (${result.fixNow} fix now, ${result.needsDeveloper} developer), ${result.advisories} advisories. Platform: ${result.profile.platform}. Size: ${result.profile.size}.`);
  console.log('Wrote ' + path.join(out, 'report.html'));
})().catch(e => { console.error('Scan failed: ' + e.message); process.exit(1); });
