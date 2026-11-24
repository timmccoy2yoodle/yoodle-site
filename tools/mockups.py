# Compose live-site screenshots into browser-frame mockups: python3 tools/mockups.py <shots-dir>
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC = sys.argv[1]; OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/img/shots")
os.makedirs(OUT, exist_ok=True)
ORDER = [("nevada-state-university","nevadastate.edu","#2c2a6f"),("san-bernardino-community-college-district","sbccd.edu","#2c2a6f"),("compton-college","compton.edu","#2c2a6f"),("rio-hondo-college","riohondo.edu","#2c2a6f"),("ut-austin-extended-campus","extendedcampus.utexas.edu","#2c2a6f"),("earth-center","earthcntr.org","#2c2a6f"),("fsu-career-center","career.fsu.edu","#2c2a6f"),("cochise-college","cochise.edu","#2c2a6f"),("crowder-college","crowder.edu","#2c2a6f"),("palm-beach-state-college","pbsc.edu","#2c2a6f"),("miracosta-college","miracosta.edu","#2c2a6f"),("ci3t","ci3t.org","#2c2a6f"),("swift-education-center","swiftschools.org","#2c2a6f"),("missouri-kinship-navigator","mokin4kid.org","#2c2a6f"),("kansas-judicial-branch","kscourts.gov","#111110"),("multistate-tax-commission","mtc.gov","#111110"),("neighborworks-america","neighborworks.org","#111110"),("kc-streetcar","kcstreetcar.org","#111110"),("marc-head-start","marcheadstart.org","#783a92"),("music-theater-heritage","musictheaterheritage.com","#783a92"),("variety-socal","varietysocal.org","#783a92"),("variety-kc","varietykc.org","#783a92"),("wentworth-financial-communications","wentworthwriting.com","#953c92"),("dr-amy-k-patel","dramykpatel.com","#953c92"),("savvy-bridal","savvybridalboutique.com","#953c92"),("nick-and-jakes","nickandjakes.com","#953c92"),("brous-law","brouslaw.com","#953c92")]
CROP = {"ut-austin-extended-campus": (0, 0, 0, 132), "palm-beach-state-college": (0, 0, 0, 72), "swift-education-center": (40, 24, 0, 12)}  # left, top, right, bottom trims
files = sorted((f for f in glob.glob(os.path.join(SRC, "*.jpg")) if int(os.path.basename(f).split("-")[5]) >= 1795506496894), key=lambda f: int(os.path.basename(f).split("-")[5]))
assert len(files) == len(ORDER), (len(files), len(ORDER))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20) if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") else ImageFont.load_default()
W, H, WW = 1600, 1200, 1320
for f, (slug, host, col) in zip(files, ORDER):
    im = Image.open(f).convert("RGB"); l, t, r, b = CROP.get(slug, (0, 0, 0, 12))
    im = im.crop((l, t, im.width - r, im.height - b))
    hh = min(int(WW * im.height / im.width), 660); im = im.resize((WW, int(WW * im.height / im.width)), Image.LANCZOS).crop((0, 0, WW, hh))
    bar = 46; win = Image.new("RGB", (WW, hh + bar), "#ecebe7"); d = ImageDraw.Draw(win)
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]): d.ellipse((20 + i * 24, 16, 34 + i * 24, 30), fill=c)
    d.rounded_rectangle((330, 9, WW - 330, 37), 14, fill="#ffffff"); tw = d.textlength(host, font=font); d.text(((WW - tw) / 2, 11), host, fill="#55524c", font=font)
    win.paste(im, (0, bar))
    mask = Image.new("L", win.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, win.width - 1, win.height - 1), 18, fill=255)
    bg = Image.new("RGB", (W, H), col); g = ImageDraw.Draw(bg)
    for k, rad in enumerate((760, 560)): g.ellipse((W - rad - 40 + k * 120, H - rad + 180, W + rad - 40 + k * 120, H + rad + 180), outline=(255, 255, 255), width=2)
    bg = Image.blend(bg, Image.new("RGB", (W, H), col), 0.72)
    x, y = (W - WW) // 2, (H - win.height) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x, y + 26, x + WW, y + win.height + 26), 18, fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(28))
    bg = Image.alpha_composite(bg.convert("RGBA"), sh).convert("RGB"); bg.paste(win, (x, y), mask)
    bg.save(os.path.join(OUT, slug + ".webp"), "WEBP", quality=84, method=6)
print(len(files), "mockups")
