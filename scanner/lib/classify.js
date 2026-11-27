// Plain-language names for axe-core rules, who each one affects, and how Yoodle handles the fix.
// fix: "fix" = known safe correction; "developer" = needs judgment or changes how something works.
const R = {
  'image-alt': ['Images missing text alternatives', 'screen reader users', 'fix'],
  'input-image-alt': ['Image buttons missing text alternatives', 'screen reader users', 'fix'],
  'role-img-alt': ['Graphics missing text alternatives', 'screen reader users', 'fix'],
  'svg-img-alt': ['SVG graphics missing text alternatives', 'screen reader users', 'fix'],
  'area-alt': ['Image map areas missing text alternatives', 'screen reader users', 'fix'],
  'color-contrast': ['Text contrast too low', 'low-vision users', 'fix'],
  'link-in-text-block': ['Links told apart from text by color alone', 'low-vision and color-blind users', 'fix'],
  'label': ['Form fields without labels', 'screen reader and voice-control users', 'fix'],
  'select-name': ['Dropdowns without labels', 'screen reader and voice-control users', 'fix'],
  'link-name': ['Links with no readable name', 'screen reader and voice-control users', 'fix'],
  'button-name': ['Buttons with no readable name', 'screen reader and voice-control users', 'fix'],
  'frame-title': ['Embedded frames without titles', 'screen reader users', 'fix'],
  'html-has-lang': ['Page language not set', 'screen reader users', 'fix'],
  'html-lang-valid': ['Page language set incorrectly', 'screen reader users', 'fix'],
  'valid-lang': ['Language of a passage set incorrectly', 'screen reader users', 'fix'],
  'document-title': ['Pages without a title', 'screen reader users and anyone with many tabs', 'fix'],
  'meta-viewport': ['Zoom is disabled on phones', 'low-vision users', 'fix'],
  'bypass': ['No way to skip repeated navigation', 'keyboard users', 'fix'],
  'list': ['Lists marked up incorrectly', 'screen reader users', 'fix'],
  'listitem': ['List items outside a list', 'screen reader users', 'fix'],
  'definition-list': ['Definition lists marked up incorrectly', 'screen reader users', 'fix'],
  'dlitem': ['Definition items outside a list', 'screen reader users', 'fix'],
  'duplicate-id-aria': ['Duplicate IDs that break labels', 'screen reader users', 'fix'],
  'meta-refresh': ['Page refreshes or redirects on a timer', 'screen reader and cognitive-disability users', 'fix'],
  'td-headers-attr': ['Data table cells point to the wrong headers', 'screen reader users', 'developer'],
  'th-has-data-cells': ['Data table headers with no cells', 'screen reader users', 'developer'],
  'scrollable-region-focusable': ['Scrolling areas that keyboards cannot reach', 'keyboard users', 'developer'],
  'nested-interactive': ['Controls nested inside other controls', 'screen reader and keyboard users', 'developer'],
  'video-caption': ['Videos without captions', 'deaf and hard-of-hearing users', 'developer'],
  'object-alt': ['Embedded objects missing text alternatives', 'screen reader users', 'developer'],
  'autocomplete-valid': ['Form fields with wrong autofill hints', 'users with motor and cognitive disabilities', 'fix'],
  'target-size': ['Tap targets too small', 'users with motor disabilities', 'fix'],
  'heading-order': ['Heading levels skip', 'screen reader users', 'fix'],
  'empty-heading': ['Empty headings', 'screen reader users', 'fix'],
  'page-has-heading-one': ['Pages without a main heading', 'screen reader users', 'fix'],
  'region': ['Content outside page landmarks', 'screen reader users', 'fix'],
  'landmark-one-main': ['Pages without a main landmark', 'screen reader users', 'fix'],
  'landmark-unique': ['Landmarks that cannot be told apart', 'screen reader users', 'fix'],
  'image-redundant-alt': ['Image descriptions that repeat nearby text', 'screen reader users', 'fix'],
  'skip-link': ['Skip link points nowhere', 'keyboard users', 'fix'],
  'tabindex': ['Custom tab order', 'keyboard users', 'developer'],
};
const SC = { '111': '1.1.1', '121': '1.2.1', '122': '1.2.2', '131': '1.3.1', '135': '1.3.5', '141': '1.4.1', '143': '1.4.3', '144': '1.4.4', '1410': '1.4.10', '1412': '1.4.12', '211': '2.1.1', '221': '2.2.1', '222': '2.2.2', '241': '2.4.1', '242': '2.4.2', '244': '2.4.4', '258': '2.5.8', '311': '3.1.1', '312': '3.1.2', '332': '3.3.2', '411': '4.1.1', '412': '4.1.2' };
function describe(v) {
  const r = R[v.id];
  const aria = /^aria-/.test(v.id);
  const wcag = (v.tags || []).filter(t => /^wcag\d{3,4}$/.test(t)).map(t => SC[t.slice(4)] || t.slice(4).split('').join('.'));
  const advisory = !wcag.length; // axe "best-practice" rules are not WCAG failures
  return {
    name: r ? r[0] : (aria ? 'ARIA attributes used incorrectly: ' + v.help : v.help),
    affects: r ? r[1] : 'screen reader users',
    fix: r ? r[2] : 'developer',
    wcag, advisory,
    severity: { critical: 'Critical', serious: 'Serious', moderate: 'Moderate', minor: 'Minor' }[v.impact] || 'Moderate',
  };
}
module.exports = { describe };
