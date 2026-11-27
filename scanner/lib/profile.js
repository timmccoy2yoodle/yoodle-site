// Works out what a site is built on from its home page markup and response headers.
const SIGNS = [
  ['WordPress', /wp-content|wp-includes|<meta[^>]+generator[^>]+WordPress/i],
  ['Drupal', /Drupal\.settings|drupal-settings-json|\/sites\/default\/files|<meta[^>]+generator[^>]+Drupal/i],
  ['Modern Campus CMS', /omniupdate\.com|\/_resources\/|ou-campus|moderncampus/i],
  ['Squarespace', /static1\.squarespace\.com|<meta[^>]+generator[^>]+Squarespace|squarespace-cdn/i],
  ['Wix', /static\.wixstatic\.com|<meta[^>]+generator[^>]+Wix/i],
  ['Webflow', /<meta[^>]+generator[^>]+Webflow|assets\.website-files\.com|data-wf-site/i],
  ['Shopify', /cdn\.shopify\.com|Shopify\.theme/i],
  ['Cascade CMS', /Cascade (Server|CMS)|hannonhill/i],
  ['TerminalFour', /terminalfour|t4_/i],
  ['Joomla', /<meta[^>]+generator[^>]+Joomla|\/media\/jui\//i],
  ['HubSpot CMS', /hs-scripts\.com|<meta[^>]+generator[^>]+HubSpot/i],
  ['Framer', /framerusercontent\.com|<meta[^>]+generator[^>]+Framer/i],
];
const BUILDERS = [['Divi', /et_pb_|et-boc|Divi/], ['Elementor', /elementor/i], ['WPBakery', /vc_row|wpb_/], ['Beaver Builder', /fl-builder/], ['Gutenberg blocks', /wp-block-/]];
const OVERLAYS = [['UserWay', /userway\.org/i], ['accessiBe', /acsbapp?\.com|accessibe/i], ['AudioEye', /audioeye\.com/i], ['EqualWeb', /equalweb\.com/i]];
function profile(html, headers, pageCount) {
  const hit = SIGNS.find(([, re]) => re.test(html));
  const gen = (html.match(/<meta[^>]+name=["']generator["'][^>]+content=["']([^"']+)/i) || [])[1] || null;
  const size = pageCount > 1000 ? 'large' : pageCount >= 100 ? 'medium' : 'small';
  return {
    platform: hit ? hit[0] : (gen || 'Not detected (static or custom)'),
    generator: gen,
    builders: BUILDERS.filter(([, re]) => re.test(html)).map(b => b[0]),
    overlays: OVERLAYS.filter(([, re]) => re.test(html)).map(o => o[0]),
    server: headers.get('server') || null, poweredBy: headers.get('x-powered-by') || null,
    size, sizeNote: { small: 'Under 100 pages', medium: '100 to 1,000 pages', large: 'More than 1,000 pages: priced for the site, with a call' }[size],
  };
}
module.exports = { profile };
