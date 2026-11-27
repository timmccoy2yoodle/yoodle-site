#!/usr/bin/env python3
"""yoodle.com generator. python3 tools/build.py [--preview]
site/    = real paths for Netlify.   preview/ = flat files with relative links for the review artifact."""
import os, re, sys, json, shutil, html
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *
from data import PILLARS, RH_REV, YEARS_ARCHIVE
from logos import LOGOS, WALL, CLEAR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = "--preview" in sys.argv
OUT = os.path.join(ROOT, "preview" if PREVIEW else "site")
TEST_BUILD = True
# Yoodle review widget: tap-to-comment on *.netlify.app and localhost only. Not in artifact previews.
REVIEW_TAG = "" if PREVIEW else '<script src="/yoodle-review.js" data-project="Yoodle" defer></script>'
DOMAIN = "https://yoodle.com"
EMAIL = "hello@yoodle.com"
TODAY = date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)
PAGES = []
OLDSITE = json.load(open(os.path.join(ROOT, "tools/old_site.json")))
OLD = {}
_have = {p["slug"] for p in P}
_sec = lambda c: "higher-ed" if "Education" in c and "Nonprofit" not in c else "government" if "Government" in c else "nonprofit" if "Nonprofit" in c else "business"
for o in OLDSITE["projects"]:
    OLD[o["slug"]] = o
    if o["slug"] in _have: continue
    first = next((t for k, t in o["blocks"] if k == "p"), "")
    P.append(dict(slug=o["slug"], name=o["name"], sector=_sec(o["cats"]), url="", place="", platform="", about=first, features=[], kind="Project"))
# Posts Tim removed (Nov 26 2026) and where their old addresses now go.
GONE = {"brands-that-speak-the-podcast": "/content/", "png": "/content/", "unscripted-mental-health-x-covid-19-edition": "/content/",
        "yoodle-education-services-x-fec-kc": "/work/yoodle-education-services/", "yoodle-education-services-x-umkc": "/work/yoodle-education-services/",
        "variety-kansas-city-and-yoodle-team-up-to-talk-inclusion-in-a-covid-19-world": "/work/variety-kc/"}
assert not set(GONE) - {x["slug"] for x in OLDSITE["posts"]}
POSTS = [x for x in OLDSITE["posts"] if x["slug"] not in GONE]
def cover_img(p):
    if os.path.exists(os.path.join(ROOT, "assets/img/shots", p["slug"] + ".webp")): return dict(src=f'/img/shots/{p["slug"]}.webp', w=1600, h=1200)
    o = OLD.get(p["slug"])
    return o["imgs"][0] if o and o["imgs"] else None
def rich(blocks):
    out, li = [], []
    def flush():
        if li: out.append("<ul class='sect'>" + "".join(f"<li>{e(x)}</li>" for x in li) + "</ul>"); li.clear()
    blocks = [x for i, x in enumerate(blocks) if not (x[0] == "h" and (i + 1 == len(blocks) or blocks[i + 1][0] == "h"))]
    for k, t in blocks:
        if k == "li": li.append(t); continue
        flush()
        out.append(f"<h3 style='margin:1.4em 0 .5em'>{e(t)}</h3>" if k == "h" else f"<p>{e(t)}</p>")
    flush(); return "".join(out)

def confirm(t): return f'<span class="confirm">CONFIRM: {e(t)}</span>'

CSS = r'''
@font-face{font-family:"Inter";src:url("/fonts/inter.woff2") format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Bricolage Grotesque";src:url("/fonts/bricolage-grotesque.woff2") format("woff2");font-weight:200 800;font-display:swap}
:root{--bg:#F7F4EE;--ink:#111110;--mute:#55524c;--line:#11111022;--acc:#2c2a6f;--acc-t:#2c2a6f;--acc-l:#b9b6f5;--white:#fff;--amber:#ffe9a8;--amber-t:#4d3400;--max:1320px}
*{box-sizing:border-box}
html{scroll-padding-top:80px;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;font-family:"Inter",system-ui,sans-serif;font-size:18px;line-height:1.5;color:var(--ink);background:var(--bg);overflow-wrap:anywhere;-webkit-font-smoothing:antialiased}
h1,h2,h3,.big,.brand,.idx{font-family:"Bricolage Grotesque","Inter",system-ui,sans-serif;font-weight:650;letter-spacing:-.035em;line-height:.98;margin:0}
h1{font-size:clamp(3rem,10.5vw,9.5rem);letter-spacing:-.045em;line-height:.9}
h1.md{font-size:clamp(2.6rem,7.5vw,6.4rem)}
h2{font-size:clamp(2.3rem,6vw,5rem)}
h3{font-size:clamp(1.4rem,2.4vw,2rem);letter-spacing:-.025em;line-height:1.08}
h1 .r,h2 .r{color:var(--acc);display:block}
.dark h1 .r,.dark h2 .r{color:var(--acc-l)}
p{margin:0 0 1em}
a{color:inherit;text-underline-offset:4px;text-decoration-thickness:1px}
:focus-visible{outline:3px solid var(--acc-t);outline-offset:3px}
.dark :focus-visible{outline-color:#fff}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
section{padding:clamp(56px,9vw,128px) 0}
section.tight{padding-top:0}
.dark{background:var(--ink);color:var(--bg)}
.lede{font-size:clamp(1.2rem,2vw,1.6rem);line-height:1.35;max-width:34em;letter-spacing:-.01em}
.small{font-size:.95rem;color:var(--mute)}
.dark .small{color:#cfcbc2}
.tag{font-size:1rem;font-weight:500;margin:0 0 18px}
.skip{position:absolute;left:-999px;top:0;background:#fff;color:#111;padding:12px 16px;min-height:44px;z-index:99;font-weight:600}
.skip:focus{left:8px;top:8px}
.testbar{background:var(--amber);color:var(--amber-t);font-size:.9rem;text-align:center;padding:8px 16px;font-weight:600}
.confirm{display:inline-block;background:var(--amber);color:var(--amber-t);font-size:.8rem;font-weight:700;padding:2px 8px;border-radius:3px;letter-spacing:0;font-family:"Inter",sans-serif;line-height:1.5}
header.site{position:sticky;top:0;background:var(--bg);z-index:20;border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px}
.brand{font-size:1.7rem;text-decoration:none;display:inline-flex;align-items:center;min-height:44px}
.brand span{color:var(--acc)}
nav.main ul{display:flex;gap:2px;align-items:center;list-style:none;margin:0;padding:0}
nav.main a{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;text-decoration:none;font-weight:500}
nav.main a:hover,nav.main a[aria-current]{text-decoration:underline}
nav.main a.talk{background:var(--ink);color:var(--bg);border-radius:999px;padding:0 20px;margin-left:8px}
.menu{display:none;width:48px;height:48px;padding:0;border:0;background:none;color:inherit;cursor:pointer;position:relative}
.menu i{position:absolute;left:9px;right:9px;height:2px;background:currentColor;border-radius:2px;transition:transform .35s cubic-bezier(.2,.7,.2,1),top .35s cubic-bezier(.2,.7,.2,1),width .3s,opacity .2s}
.menu i:nth-child(1){top:16px}.menu i:nth-child(2){top:23px}.menu i:nth-child(3){top:30px}
.menu:hover i:nth-child(2){transform:translateX(5px)}.menu:hover i:nth-child(3){transform:translateX(-3px)}
.menu[aria-expanded=true] i:nth-child(1){top:23px;transform:rotate(45deg)}
.menu[aria-expanded=true] i:nth-child(2){opacity:0;transform:none}
.menu[aria-expanded=true] i:nth-child(3){top:23px;transform:rotate(-45deg)}
@media (prefers-reduced-motion:reduce){.menu i{transition:none}}
@media (max-width:760px){
 .js .menu{display:block}
 .js nav.main{display:none;position:absolute;left:0;right:0;top:100%;background:var(--acc);color:#fff;padding:14px 24px 26px;box-shadow:0 24px 40px -18px #11111080}
 .js nav.main a{color:#fff}
 .js nav.main a.talk,html[data-band=dark] header.site .js nav.main a.talk{background:#fff;color:var(--ink)}
 .js nav.main.open{display:block}
 nav.main ul{flex-direction:column;align-items:stretch}
 nav.main a{font-size:1.3rem;min-height:52px;padding:0}
 nav.main a.talk{justify-content:center;margin:8px 0 0}
 html:not(.js) header.site .wrap{flex-wrap:wrap;padding-bottom:8px}
}
.go{display:inline-flex;align-items:center;gap:.4em;min-height:46px;font-weight:500;text-decoration:underline}
.go::after{content:"\2192";display:inline-block;transition:transform .2s}
.go:hover::after{transform:translateX(4px)}
@media (prefers-reduced-motion:reduce){.go::after{transition:none}}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:56px;padding:0 28px;font:inherit;font-weight:600;font-size:1.05rem;border:0;border-radius:999px;background:var(--ink);color:var(--bg);cursor:pointer;text-decoration:none}
.btn:hover{background:var(--acc-t);color:#fff}
.dark .btn{background:var(--bg);color:var(--ink)}
.hero{padding:clamp(40px,7vw,90px) 0 clamp(48px,7vw,96px)}
.herogrid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:40px;align-items:end;margin-top:clamp(28px,5vw,60px)}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:clamp(24px,5vw,80px)}
.two>*,.herogrid>*,.cols>*,.grid>*{min-width:0}
@media (max-width:860px){.two,.herogrid{grid-template-columns:1fr}}
.crumbs{font-size:.95rem;margin:0 0 22px;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:0 8px}
.crumbs li+li::before{content:"/";margin-right:8px;color:var(--mute)}
.crumbs a{display:inline-flex;min-height:46px;align-items:center}
.crumbs li{display:inline-flex;align-items:center;min-height:44px}
.logos{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;list-style:none;padding:1px;margin:0}
.logos li{background:#fff;box-shadow:0 0 0 1px var(--line);aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;padding:14%;min-width:0}
.logos img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
@media (max-width:720px){.logos{grid-template-columns:repeat(2,minmax(0,1fr))}}
.mq{overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:22px 0}
.track{display:flex;width:max-content;animation:mq 70s linear infinite}
.track ul{display:flex;list-style:none;margin:0;padding:0}
.track li{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:clamp(1.3rem,2.4vw,2rem);letter-spacing:-.02em;padding:0 28px;white-space:nowrap}
.track li::after{content:"\00B7";margin-left:56px;color:var(--acc)}
.mq.paused .track{animation-play-state:paused}
.mq.lg{padding:26px 0}.mq.lg .track{animation-duration:90s}
.mq.lg .track+.track{margin-top:30px}
.mq.lg .track.rev{animation-direction:reverse}
.mq.js .track{animation:none}
.mq.lg .track li{padding:0;margin:0 clamp(20px,3vw,44px);height:70px;display:flex;align-items:center;flex:none}
.mq.lg .track li::after{content:none}
.mq.lg .track img{width:var(--w);height:auto;max-width:none;display:block}
@media (max-width:620px){.mq.lg .track li{height:54px}.mq.lg .track img{width:calc(var(--w)*.76)}.mq.lg .track+.track{margin-top:18px}}
.caps{margin-top:clamp(20px,3vw,36px)}
.pillar{padding:clamp(36px,5vw,72px) 0;border-top:1px solid #f7f4ee44}
.pillar:first-of-type{border-top:0;padding-top:clamp(24px,3vw,40px)}
.pillar .ph{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:24px;align-items:end}
.pillar .tagc,.eyebrow{font-size:.85rem;letter-spacing:.14em;text-transform:uppercase;opacity:.8;margin:0 0 14px;font-weight:500}
.sub{font-size:.95rem;letter-spacing:.02em;opacity:.72;margin:10px 0 0}
.dark.cta{background:var(--acc)}
.cta .lede{max-width:34ch}
.cta .go{color:#fff}
.cta .ends>div{border-top:0}
.cols.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
@media (max-width:760px){.cols.c2{grid-template-columns:1fr}.cta .ends>div+div{border-top:1px solid #f7f4ee44}}
.pillar h3{font-size:clamp(2rem,4.4vw,3.6rem);margin:0}
details.cap{border-top:1px solid #f7f4ee33}
details.cap:last-of-type{border-bottom:1px solid #f7f4ee33}
details.cap summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:64px;padding:10px 0;font-family:"Bricolage Grotesque",sans-serif;font-weight:500;font-size:clamp(1.15rem,1.9vw,1.5rem);letter-spacing:-.01em}
details.cap summary::-webkit-details-marker{display:none}
details.cap summary::after{content:"+";flex:none;width:34px;height:34px;border:1.5px solid #f7f4ee;color:#f7f4ee;border-radius:50%;display:grid;place-items:center;font-family:Inter,sans-serif;font-weight:300;font-size:1.5rem;line-height:1;padding-bottom:2px;transition:transform .3s,background .2s,color .2s}
details.cap[open] summary::after{transform:rotate(45deg);background:var(--bg);color:var(--ink)}
details.cap summary:hover{opacity:.8}
details.cap p{margin:0 0 20px;max-width:60ch;opacity:.86}
.pillar .more{margin-top:22px;display:flex;gap:28px;flex-wrap:wrap}
@media (max-width:760px){.pillar .ph{grid-template-columns:1fr}}
.kw{font-size:1rem;opacity:.82;margin-top:10px!important}
.rows>li>div>p+p{margin-top:10px}
.posts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,3vw,40px) clamp(16px,2.4vw,32px);list-style:none;padding:0;margin:clamp(28px,4vw,48px) 0 0}
.posts li{min-width:0}
.posts a{display:block;text-decoration:none;color:inherit}
.posts .th{aspect-ratio:16/10;border-radius:8px;overflow:hidden;background:var(--acc);display:flex;align-items:flex-end;padding:18px;color:#fff;font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:1.3rem;letter-spacing:-.02em}
.posts .th.im{padding:0;background:#e9e5dc}
.posts .th img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}
.posts a:hover .th img{transform:scale(1.03)}
.posts h3{font-size:clamp(1.15rem,1.7vw,1.4rem);line-height:1.12;margin-top:8px}
.posts a:hover h3{text-decoration:underline}
.posts .small{display:block;margin-top:14px}
@media (max-width:900px){.posts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.posts{grid-template-columns:1fr}}
.timcta{display:flex;gap:22px;align-items:center}
.timcta img{width:132px;height:132px;border-radius:50%;object-fit:cover;flex:none}
.reg{font-size:.4em;font-weight:500;vertical-align:baseline;position:relative;top:-.95em;margin-left:.1em;letter-spacing:0;line-height:0;color:inherit}
.brand .reg{color:currentColor}
.spots{border-top:1.5px solid currentColor;padding-top:18px;margin-top:28px}
.xlogo{height:64px;display:flex;align-items:center;margin-bottom:18px}
.xlogo img{max-height:100%;max-width:220px;width:auto;height:auto;object-fit:contain}
.xlogo.dk{background:#141414;border-radius:6px;padding:10px 16px;width:max-content;height:84px;margin-bottom:-2px}
@keyframes mq{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.track{animation:none;width:auto;flex-wrap:wrap}.track ul{flex-wrap:wrap}.track ul[aria-hidden]{display:none}.track li{white-space:normal}}
.mqbtn{margin-top:14px;width:44px;height:44px;border:1.5px solid var(--ink);border-radius:50%;background:none;color:inherit;cursor:pointer;display:grid;place-items:center;padding:0}
.mqbtn::before{content:"";width:12px;height:14px;border-left:4px solid currentColor;border-right:4px solid currentColor;box-sizing:border-box}
.mqbtn[aria-pressed=true]::before{width:0;height:0;border:0;border-left:13px solid currentColor;border-top:8px solid transparent;border-bottom:8px solid transparent;margin-left:3px}
@media (prefers-reduced-motion:reduce){.mqbtn,.prog{display:none}header.site{transition:none}
 .mq.lg{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:22px 28px;align-items:center;justify-items:center;padding:26px max(24px,calc((100% - var(--max))/2 + 24px))}
 .mq.lg .track,.mq.lg .track ul{display:contents}.mq.lg .track ul[aria-hidden]{display:none}.mq.lg .track li{margin:0;width:100%;justify-content:center}.mq.lg .track img{max-width:100%}}
@media (prefers-reduced-motion:reduce) and (max-width:620px){.mq.lg{grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:14px 18px}}
.linkbtn{margin-top:12px;background:none;border:0;font:inherit;font-size:.95rem;text-decoration:underline;min-height:44px;cursor:pointer;color:inherit;padding:0}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,3vw,48px);margin-top:clamp(32px,5vw,64px)}
.cols.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (max-width:980px){.cols.c4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:760px){.cols,.cols.c4{grid-template-columns:1fr}}
.col{border-top:1.5px solid currentColor;padding-top:20px}
.col h3{margin-bottom:12px}
.rows{list-style:none;margin:clamp(32px,5vw,64px) 0 0;padding:0}
.rows>li{display:grid;grid-template-columns:90px minmax(0,1fr) minmax(0,1.2fr);gap:24px;align-items:baseline;border-top:1px solid var(--line);padding:26px 0}
.rows>li:last-child{border-bottom:1px solid var(--line)}
.dark .rows>li,.dark .col,.dark .ends>div{border-color:#f7f4ee44}
.idx{font-size:1.1rem;color:var(--acc-t);letter-spacing:0}
.dark .idx{color:var(--acc-l)}
.rows p{margin:0}
.rows h3 a{text-decoration:none}.rows h3 a:hover{text-decoration:underline}
@media (max-width:760px){.rows>li{grid-template-columns:48px minmax(0,1fr);row-gap:10px}.rows>li>p,.rows>li>div{grid-column:1/-1}}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:32px 0 0}
.chipb{min-height:46px;padding:0 18px;border:1.5px solid var(--ink);border-radius:999px;background:none;font:inherit;font-weight:600;color:var(--ink);cursor:pointer}
.chipb[aria-pressed=true]{background:var(--ink);color:var(--bg)}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,2.4vw,36px);margin-top:36px;list-style:none;padding:0}
@media (max-width:980px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:620px){.grid{grid-template-columns:1fr}}
.card{display:block;text-decoration:none}
.card:hover h3{text-decoration:underline}
.cover{display:flex;flex-direction:column;justify-content:space-between;aspect-ratio:4/3;padding:clamp(18px,2vw,28px);color:#fff;border-radius:6px;overflow:hidden;position:relative}
.cover.lg{aspect-ratio:16/8;border-radius:10px;padding:clamp(22px,4vw,56px)}
@media (max-width:620px){.cover.lg{aspect-ratio:4/3}}
.cover .k{font-size:.9rem;font-weight:600;display:flex;justify-content:space-between;gap:12px}
.cover .n{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;letter-spacing:-.04em;line-height:.95;font-size:clamp(1.7rem,3vw,2.6rem)}
.cover.lg .n{font-size:clamp(2rem,6.4vw,5.6rem)}
.cover::after{content:"";position:absolute;right:-12%;bottom:-38%;width:62%;aspect-ratio:1;border-radius:50%;border:1.5px solid #ffffff40}
.cover::before{content:"";position:absolute;right:6%;bottom:-52%;width:62%;aspect-ratio:1;border-radius:50%;border:1.5px solid #ffffff26}
.card h3{font-size:1.25rem;margin:14px 0 2px;letter-spacing:-.02em}
.card p{margin:0}
.facts{margin:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 32px}
.facts div{border-top:1.5px solid var(--ink);padding:14px 0 22px;min-width:0}
.facts dt{font-size:.9rem;color:var(--mute)}
.facts dd{margin:4px 0 0;font-weight:600}
.bleed{margin:0 0 clamp(56px,9vw,128px);padding:0}
.bleed img{display:block;width:100%;height:clamp(300px,52vw,820px);object-fit:cover;object-position:50% 35%}
.vids,.made{display:grid;gap:clamp(10px,1.4vw,20px);margin-top:clamp(32px,5vw,64px)}
.vids{grid-template-columns:repeat(3,minmax(0,1fr))}
.made{grid-template-columns:minmax(0,300px) minmax(0,300px) minmax(0,1fr);align-items:center;gap:clamp(16px,3vw,48px)}
.vids figure,.made figure{margin:0;min-width:0}
.vids video,.made img,.made video{display:block;width:100%;border-radius:6px;object-fit:cover;background:#e7e2d8}
.vids video{aspect-ratio:4/3}.made video,.yt{aspect-ratio:9/16}
.yt{display:flex;flex-direction:column;justify-content:flex-end;gap:10px;padding:22px;border-radius:6px;background:var(--ink);color:var(--bg);text-decoration:none;position:relative;overflow:hidden}
.yt .small{color:#cfcbc2}
.yttitle{font-family:"Bricolage Grotesque","Inter",system-ui,sans-serif;font-weight:650;font-size:1.5rem;line-height:1.05;letter-spacing:-.03em}
.ytplay{position:absolute;left:22px;top:22px;width:56px;height:56px;border-radius:50%;background:var(--bg)}
.ytplay::after{content:"";position:absolute;left:22px;top:17px;border-left:17px solid var(--ink);border-top:11px solid transparent;border-bottom:11px solid transparent}
.yt:hover .ytplay{background:var(--acc-l)}
.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.laptop{margin:clamp(32px,5vw,64px) auto 0;max-width:1240px;padding:0 5%}
.laptop .scr{background:#2a2a28;border-radius:16px 16px 0 0;padding:clamp(6px,1.2vw,14px);border:1px solid #f7f4ee33;border-bottom:0}
.laptop img{display:block;width:100%;height:auto;border-radius:4px}
.laptop .base{height:clamp(8px,1.4vw,16px);background:#c9c5bb;border-radius:0 0 14px 14px;margin:0 -5.5%}
.vids figcaption,.made figcaption{font-size:.9rem;color:var(--mute);margin-top:8px}
.vidbar{margin:10px 0 0}
.vidbtn{min-height:44px;padding:0 16px;border:1.5px solid var(--ink);border-radius:999px;background:none;color:var(--ink);font:inherit;font-size:.9rem;font-weight:600;cursor:pointer}
.vidbtn:hover{background:var(--ink);color:var(--bg)}
@media (max-width:760px){.vids{grid-template-columns:1fr}.vids video{aspect-ratio:16/10}.made{grid-template-columns:1fr 1fr}.made .lede{grid-column:1/-1}}
.facts.nums div{display:flex;flex-direction:column;justify-content:space-between}
.facts.nums dd{font-family:"Bricolage Grotesque","Inter",system-ui,sans-serif;font-weight:650;font-size:clamp(2.6rem,6vw,5rem);letter-spacing:-.04em;line-height:1;color:var(--acc-t)}
@media (max-width:760px){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
.sect{list-style:none;padding:0;margin:14px 0 0}
.sect li{padding:10px 0;border-top:1px solid var(--line)}
.names{columns:3;list-style:none;padding:0;margin:28px 0 0}
.names li{padding:8px 0;border-top:1px solid var(--line);break-inside:avoid}
@media (max-width:760px){.names{columns:1}}
details{border-top:1px solid var(--line)}
details:last-of-type{border-bottom:1px solid var(--line)}
summary{cursor:pointer;font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:clamp(1.2rem,2.2vw,1.6rem);letter-spacing:-.02em;padding:22px 0;min-height:44px;list-style:none;display:flex;justify-content:space-between;gap:16px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--acc-t)}
details[open] summary::after{content:"\2013"}
details p{max-width:44em}
.ends{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
.ends>div{padding:clamp(40px,7vw,96px) 24px;border-top:1px solid #f7f4ee44;min-width:0}
.ends>div+div{border-left:1px solid #f7f4ee44}
@media (max-width:760px){.ends{grid-template-columns:1fr}.ends>div+div{border-left:0}}
.pn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;border-top:1px solid var(--line);padding-top:24px}
.pn a{display:block;text-decoration:none;min-height:44px}.pn a:hover strong{text-decoration:underline}
.pn .nx{text-align:right}
form.f{display:grid;gap:16px;max-width:640px}
form.f label{display:block;font-weight:600;margin-bottom:6px}
form.f input,form.f textarea{width:100%;min-height:52px;padding:12px 18px;font:inherit;border:1.5px solid var(--ink);background:#fff;color:var(--ink);border-radius:10px}
form.f textarea{min-height:140px}
form.f select{width:100%;min-height:52px;padding:12px 18px;font:inherit;border:1.5px solid var(--ink);background:#fff;color:var(--ink);border-radius:10px}
form.f fieldset{border:0;padding:0;margin:0;min-width:0}form.f legend{font-weight:600;margin-bottom:10px;padding:0}
form.f .checks{display:flex;flex-wrap:wrap;gap:10px}
form.f .checks label{display:inline-flex;align-items:center;gap:8px;margin:0;font-weight:500;border:1.5px solid var(--ink);border-radius:999px;padding:0 16px;min-height:46px;cursor:pointer;background:#fff}
form.f .checks input{width:18px;height:18px;min-height:0;padding:0;accent-color:var(--acc)}
form.f .checks label:has(input:checked){background:var(--ink);color:var(--bg)}
.hp{position:absolute;left:-9999px}
form.f input:hover,form.f textarea:hover,form.f select:hover{border-color:var(--acc)}
form.f [aria-invalid=true]{border-color:#a4161a;border-width:2.5px}
form.f .err{margin:6px 0 0;color:#a4161a;font-weight:600;font-size:.95rem}
::selection{background:var(--acc);color:#fff}
.dark ::selection{background:var(--bg);color:var(--ink)}
.status{margin-top:4px;padding:12px 16px;background:var(--amber);color:var(--amber-t);font-weight:600;display:none;border-radius:6px}
.status.show{display:block}
dialog.lead{border:0;border-radius:14px;padding:0;max-width:560px;width:calc(100% - 32px);background:var(--bg);color:var(--ink)}
dialog.lead::backdrop{background:#111110b3}
dialog.lead .in{padding:clamp(24px,4vw,40px)}
dialog.lead h2{font-size:clamp(2rem,5vw,3rem);margin-bottom:12px}
dialog.lead .x{float:right;min-width:44px;min-height:44px;border:0;background:none;font:inherit;font-size:1.6rem;cursor:pointer;color:inherit}
footer{background:var(--ink);color:#cfcbc2;padding:48px 0 56px;font-size:.95rem;border-top:1px solid #f7f4ee44}
footer a{color:#fff;display:inline-flex;min-height:44px;align-items:center}
footer .fg{display:grid;grid-template-columns:minmax(0,1.4fr) repeat(3,minmax(0,1fr));gap:32px}
@media (max-width:760px){footer .fg{grid-template-columns:1fr 1fr}}
footer ul{list-style:none;margin:0;padding:0}
footer h2{font-size:1rem;letter-spacing:0;color:#fff;margin-bottom:8px;font-family:"Inter",sans-serif}
.pick{position:fixed;left:0;right:0;bottom:0;z-index:30;background:var(--amber);color:var(--amber-t);padding:8px 12px;display:flex;gap:8px;align-items:center;overflow-x:auto;font-size:.9rem;font-weight:600}
.pick>*{flex:0 0 auto}
.pick button{min-height:44px;padding:0 14px 0 10px;border:2px solid transparent;border-radius:999px;background:#fff;color:#111;font:inherit;font-weight:600;display:inline-flex;align-items:center;gap:8px;cursor:pointer}
.pick button[aria-pressed=true]{border-color:#111}
.pick i{width:20px;height:20px;border-radius:50%;display:inline-block}
.cover.ph{padding:0;background:#e9e5dc}
.cover.ph img,.gal img{width:100%;height:100%;object-fit:cover;display:block}
.cover.ph::after,.cover.ph::before{display:none}
.gal{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(12px,2vw,28px);list-style:none;padding:0;margin:0}
.gal li{border-radius:8px;overflow:hidden;background:#e9e5dc;aspect-ratio:4/3;min-width:0}
@media (max-width:620px){.gal{grid-template-columns:1fr}}
.post{max-width:46em}
.post p{font-size:1.1rem}
.plist{list-style:none;padding:0;margin:32px 0 0}
.plist li{border-top:1px solid #f7f4ee44;padding:18px 0;display:grid;grid-template-columns:120px minmax(0,1fr);gap:20px;align-items:baseline}
.plist a{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:clamp(1.2rem,2.2vw,1.6rem);letter-spacing:-.02em;text-decoration:none;display:inline-flex;min-height:44px;align-items:center}
.plist a:hover{text-decoration:underline}
@media (max-width:620px){.plist li{grid-template-columns:1fr;gap:0}}

/* ---- motion layer: only when JS is on and the visitor has not asked for reduced motion */
header.site{transition:transform .45s cubic-bezier(.2,.7,.2,1),background-color .5s,color .5s,border-color .5s}
header.site.hide{transform:translateY(-101%)}
html[data-band=dark] header.site{background:var(--ink);color:var(--bg);border-color:#f7f4ee33}
html[data-band=dark] header.site nav.main a.talk{background:var(--bg);color:var(--ink)}
html[data-band=dark] header.site .menu{color:var(--bg)}
html[data-band=dark] header.site .brand span{color:var(--acc-l)}
html[data-band=dark] .js nav.main,html.js[data-band=dark] nav.main{background:var(--ink)}
.prog{position:fixed;left:0;top:0;height:3px;width:100%;background:var(--acc);transform-origin:0 50%;transform:scaleX(0);z-index:40;pointer-events:none}
@media (prefers-reduced-motion:no-preference){
 .mo .rv{opacity:0;transform:translateY(34px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .9s cubic-bezier(.2,.7,.2,1);transition-delay:calc(var(--i,0)*70ms)}
 .mo .rv.in{opacity:1;transform:none}
 .mo .rh .hl{display:block;clip-path:inset(0 0 100% 0);transform:translateY(.32em);transition:clip-path 1s cubic-bezier(.2,.7,.2,1),transform 1s cubic-bezier(.2,.7,.2,1)}
 .mo .rh.in .hl{clip-path:inset(-10% -5% -20% -5%);transform:none}
 .mo .rh .r{opacity:0;transform:translateY(.25em);transition:opacity .7s .35s,transform .9s .35s cubic-bezier(.2,.7,.2,1)}
 .mo .rh.in .r{opacity:1;transform:none}
 .mo .rows>li{border-top-color:transparent;background:linear-gradient(currentColor,currentColor) 0 0/0 1px no-repeat;transition:opacity .8s,transform .9s cubic-bezier(.2,.7,.2,1),background-size 1.1s cubic-bezier(.2,.7,.2,1);transition-delay:calc(var(--i,0)*70ms)}
 .mo .rows>li.in{background-size:100% 1px}
 .mo .rows>li{opacity:.0}.mo .rows>li.in{opacity:1}
 .mo .rows>li h3{transition:transform .35s cubic-bezier(.2,.7,.2,1)}
 .mo .rows>li:hover h3{transform:translateX(14px)}
 .mo .cover{transition:transform .6s cubic-bezier(.2,.7,.2,1)}
 .mo .card:hover .cover{transform:scale(.975)}
 .mo .cover .n{transition:transform .6s cubic-bezier(.2,.7,.2,1)}
 .mo .card:hover .cover .n{transform:translateY(-8px)}
 .mo .cover::after,.mo .cover::before{transform:translateY(var(--py,0px));will-change:transform}
 .mo .cover.lg{transform:scale(var(--sc,1));transform-origin:50% 0;will-change:transform}
 .mo .dark.band{clip-path:inset(0 var(--in,0px) round var(--rd,0px));will-change:clip-path}
 .btn{transition:background-color .25s,color .25s,transform .25s}
 .btn:hover{transform:translateY(-2px)}
}
'''

JS = r'''
(function(){
var d=document,h=d.documentElement;h.classList.add('js');
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(_){return null}}
var mb=d.getElementById('menu'),nv=d.getElementById('nav');
if(mb){mb.addEventListener('click',function(){var o=nv.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
 d.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&nv.classList.contains('open')){nv.classList.remove('open');mb.setAttribute('aria-expanded','false');mb.focus()}})}
var mq=d.getElementById('mq'),mqb=d.getElementById('mqbtn');
if(mqb)mqb.addEventListener('click',function(){var p=mq.classList.toggle('paused');mqb.setAttribute('aria-pressed',p);mqb.setAttribute('aria-label',p?'Play scrolling logos':'Pause scrolling logos')});
if(mq&&window.requestAnimationFrame&&!(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches)){mq.classList.add('js');
 var tr=[].slice.call(mq.querySelectorAll('.track')),mw=[],mx=tr.map(function(){return 0}),ml=0;
 var msz=function(){tr.forEach(function(el,i){mw[i]=el.firstElementChild.getBoundingClientRect().width})};msz();addEventListener('resize',msz);addEventListener('load',msz);
 var mstep=function(t){var dt=ml?Math.min(t-ml,64):0;ml=t;if(!mq.classList.contains('paused'))tr.forEach(function(el,i){var w=mw[i];if(!w)return;mx[i]=(mx[i]+w/90000*dt)%w;el.style.transform='translateX('+(el.classList.contains('rev')?mx[i]-w:-mx[i]).toFixed(2)+'px)'});requestAnimationFrame(mstep)};requestAnimationFrame(mstep)}
var fb=d.querySelectorAll('[data-f]'),cards=d.querySelectorAll('[data-s]'),cnt=d.getElementById('count');
function setF(k){var n=0;cards.forEach(function(c){var on=k==='all'||c.getAttribute('data-s')===k;c.hidden=!on;if(on)n++});fb.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-f')===k)});if(cnt)cnt.textContent=n+' projects shown';}
fb.forEach(function(b){b.addEventListener('click',function(){setF(b.getAttribute('data-f'));if(history.replaceState)try{history.replaceState(null,'','#'+b.getAttribute('data-f'))}catch(_){}})});
if(fb.length&&location.hash){var k=location.hash.slice(1);if(d.querySelector('[data-f="'+k+'"]'))setF(k)}
var live=/(^|\.)yoodle\.com$|\.netlify\.app$/.test(location.hostname);
d.querySelectorAll('form[data-netlify]').forEach(function(f){f.addEventListener('submit',function(ev){
 var s=f.querySelector('.status');
 f.querySelectorAll('.err').forEach(function(x){x.remove()});f.querySelectorAll('[aria-invalid]').forEach(function(x){x.removeAttribute('aria-invalid');x.removeAttribute('aria-describedby')});
 if(!f.checkValidity()){ev.preventDefault();var bads=[].slice.call(f.querySelectorAll('input:invalid,textarea:invalid,select:invalid'));
  bads.forEach(function(x){var m=x.validity.valueMissing?'Required. Please fill this in.':x.type==='email'?'Enter an email address like name@example.com.':'Please check this answer.';
   var er=d.createElement('p');er.className='err';er.id=x.id+'-err';er.textContent=m;x.setAttribute('aria-invalid','true');x.setAttribute('aria-describedby',er.id);x.parentNode.appendChild(er);
   x.addEventListener('input',function(){if(x.checkValidity()){x.removeAttribute('aria-invalid');x.removeAttribute('aria-describedby');if(er.parentNode)er.remove()}})});
  s.classList.add('show');s.textContent=bads.length===1?'One field needs attention. It is marked above.':bads.length+' fields need attention. They are marked above.';if(bads[0])bads[0].focus();return}
 if(!live){ev.preventDefault();s.classList.add('show');s.textContent='Test build: this form is connected when the site goes live on Netlify. Nothing was sent.'}
 ls('y-lead',String(Date.now()));
})});
var dl=d.getElementById('lead');
if(dl&&dl.showModal&&!window.__noPopup&&!h.hasAttribute('data-nopop')){
 var last=+ls('y-lead')||0,views=(+ls('y-views')||0)+1;ls('y-views',String(views));
 var shown=false;function show(){if(shown||Date.now()-last<2592e6)return;shown=true;ls('y-lead',String(Date.now()));dl.showModal()}
 if(views>1)setTimeout(show,4000);else{setTimeout(show,20000);addEventListener('scroll',function(){if((scrollY+innerHeight)/h.scrollHeight>.6)show()},{passive:true})}
 dl.querySelector('.x').addEventListener('click',function(){dl.close()});
 dl.addEventListener('click',function(ev){if(ev.target===dl)dl.close()});
}
var pb=d.querySelectorAll('.pick button');pb.forEach(function(x){x.addEventListener('click',function(){var r=h.style;r.setProperty('--acc',x.dataset.a);r.setProperty('--acc-t',x.dataset.t);r.setProperty('--acc-l',x.dataset.l);pb.forEach(function(y){y.setAttribute('aria-pressed',y===x)});ls('y-acc',x.dataset.a)})});
var sa=ls('y-acc');if(sa)pb.forEach(function(x){if(x.dataset.a===sa)x.click()});
})();
(function(){
var d=document,h=d.documentElement,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
var hd=d.querySelector('header.site'),bar=d.createElement('div');bar.className='prog';bar.setAttribute('aria-hidden','true');d.body.appendChild(bar);
var darks=[].slice.call(d.querySelectorAll('main section.dark'));
if(!rm&&'IntersectionObserver' in window){
 h.classList.add('mo');
 var heads=d.querySelectorAll('main h1,main section h2');
 heads.forEach(function(x){x.classList.add('rh');var s=d.createElement('span');s.className='hl';while(x.firstChild)s.appendChild(x.firstChild);x.appendChild(s)});
 var sel='.lede,.tag,.crumbs,.grid>li,.col,.facts>div,.sect>li,.names>li,details,.ends>div>*,form.f,.filters,.pn,.herogrid>*,.hero .btn,section p:not(.lede):not(.small)';
 d.querySelectorAll('main '+sel).forEach(function(x){if(x.closest('.rv,dialog,.rows')||x.classList.contains('rh'))return;x.classList.add('rv')});
 d.querySelectorAll('main .rows>li').forEach(function(x){x.classList.add('rw')});
 d.querySelectorAll('.grid,.cols,.rows,.facts,.sect,.names,.ends>div').forEach(function(p){[].forEach.call(p.children,function(c,i){c.style.setProperty('--i',Math.min(i%6,5))})});
 var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
 d.querySelectorAll('.rv,.rh,.rw').forEach(function(x){io.observe(x)});
 darks.forEach(function(s){if(!s.classList.contains('cta'))s.classList.add('band')});
}
var ly=scrollY,tick=false;
function frame(){tick=false;
 var y=scrollY,vh=innerHeight,max=h.scrollHeight-vh;
 bar.style.transform='scaleX('+(max>0?Math.min(1,y/max):0)+')';
 if(hd){var nav=d.getElementById('nav');if(y>ly+6&&y>240&&!(nav&&nav.classList.contains('open')))hd.classList.add('hide');else if(y<ly-6||y<=240)hd.classList.remove('hide')}
 ly=y;
 var band='';darks.forEach(function(s){var r=s.getBoundingClientRect();if(r.top<=40&&r.bottom>40)band='dark'});
 if(band)h.setAttribute('data-band',band);else h.removeAttribute('data-band');
 if(!rm&&h.classList.contains('mo')){
  d.querySelectorAll('.dark.band').forEach(function(s){var r=s.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;var t=Math.max(0,Math.min(1,(vh-r.top)/(vh*.55)));s.style.setProperty('--in',(1-t)*Math.min(48,innerWidth*.04)+'px');s.style.setProperty('--rd',(1-t)*28+'px')});
  d.querySelectorAll('.cover').forEach(function(c){var r=c.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;var p=(r.top+r.height/2-vh/2)/vh;c.style.setProperty('--py',(p*-40).toFixed(1)+'px');if(c.classList.contains('lg')){var t=Math.max(0,Math.min(1,(vh-r.top)/(vh*.7)));c.style.setProperty('--sc',(.9+.1*t).toFixed(3))}});
 }
}
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(frame)}},{passive:true});addEventListener('resize',frame);frame();
})();
'''

YEARS = date.today().year - 2007
NAV = [("/work/", "Work"), ("/services/", "Services"), ("/content/", "Content"), ("/experience/", "Experience")]

def header(cur):
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if cur.startswith(h) else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to main content</a>
{'<aside class="testbar" aria-label="Test build notice">Test build for Tim. Amber tags mark facts to confirm before launch.</aside>' if TEST_BUILD else ''}
<header class="site"><div class="wrap">
<a class="brand" href="/" aria-label="Yoodle home">yoodle<span>.</span><sup class="reg" aria-hidden="true">&reg;</sup></a>
<button class="menu" id="menu" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><i></i><i></i><i></i></button>
<nav class="main" id="nav" aria-label="Main"><ul>{li}<li><a class="talk" href="/contact/">Contact</a></li></ul></nav>
</div></header>'''

def footer():
    return f'''<footer><div class="wrap"><div class="fg">
<div><p><strong style="color:#fff;font-size:1.3rem">yoodle.<sup class="reg">&reg;</sup></strong></p><p>The content experience agency. Brand, technology and marketing for ambitious organizations.</p><p>Built on experience. Made for what&rsquo;s next.</p><p>Kansas City, Missouri<br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h2>Work</h2><ul><li><a href="/work/#higher-ed">Higher education</a></li><li><a href="/work/#government">Government</a></li><li><a href="/work/#nonprofit">Nonprofit</a></li><li><a href="/work/#business">Small business</a></li><li><a href="/work/#content">Podcasts</a></li></ul></div>
<div><h2>Services</h2><ul><li><a href="/services/brand/">Brand</a></li><li><a href="/services/technology/">Technology</a></li><li><a href="/services/#marketing">Marketing</a></li><li><a href="/experience/">Fractional CMO</a></li><li><a href="/accessibility/">ADA compliance</a></li><li><a href="/bridal/">Bridal</a></li></ul></div>
<div><h2>Yoodle</h2><ul><li><a href="/content/">Content</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="https://www.linkedin.com/company/yoodle">LinkedIn</a></li></ul></div>
</div><p style="margin-top:32px">&copy; {date.today().year} Yoodle LLC. Yoodle&reg; is a registered trademark.</p></div></footer>'''

PICK = '''<aside class="pick" aria-label="Accent color options, test build only"><span>Accent:</span><button type="button" aria-pressed="true" data-a="#2c2a6f" data-t="#2c2a6f" data-l="#b9b6f5"><i style="background:#2c2a6f"></i>Deep purple</button><button type="button" aria-pressed="false" data-a="#783a92" data-t="#783a92" data-l="#d9b3ea"><i style="background:#783a92"></i>Plum</button><button type="button" aria-pressed="false" data-a="#953c92" data-t="#953c92" data-l="#e8b0e5"><i style="background:#953c92"></i>Magenta</button><button type="button" aria-pressed="false" data-a="#c23c7c" data-t="#c03b7b" data-l="#f4aecd"><i style="background:#c23c7c"></i>Berry</button><button type="button" aria-pressed="false" data-a="#d5466d" data-t="#cc2e59" data-l="#f8b1c2"><i style="background:#d5466d"></i>Rose</button></aside>'''

def field(id, label, type="text", req=True, ac="", pre=""):
    r = " required" if req else ""
    a = f' autocomplete="{ac}"' if ac else ""
    if isinstance(type, tuple) and type[0] == "select": return f'<div><label for="{pre}{id}">{label}</label><select id="{pre}{id}" name="{id}"{r}><option value="">Choose one</option>{"".join(f"<option>{o}</option>" for o in type[1])}</select></div>'
    if isinstance(type, tuple) and type[0] == "checks": return f'<fieldset><legend>{label}</legend><div class="checks">{"".join(f"<label><input type=checkbox name={chr(34)}{id}[]{chr(34)} value={chr(34)}{o}{chr(34)}> <span>{o}</span></label>" for o in type[1])}</div></fieldset>'
    if type == "textarea": return f'<div><label for="{pre}{id}">{label}</label><textarea id="{pre}{id}" name="{id}"{r}></textarea></div>'
    return f'<div><label for="{pre}{id}">{label}</label><input id="{pre}{id}" name="{id}" type="{type}"{a}{r}></div>'

def form(name, fields, button, pre=""):
    return f'''<form class="f" name="{name}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="company-site" novalidate>
<input type="hidden" name="form-name" value="{name}"><p class="hp"><label>Leave this empty <input name="company-site" tabindex="-1" autocomplete="off"></label></p>
{"".join(field(*f, pre=pre) for f in fields)}
<div><button class="btn" type="submit">{button}</button></div><p class="status" role="status" aria-live="polite"></p></form>'''

SCAN_FIELDS = [("name", "Your name", "text", True, "name"), ("email", "Work email", "email", True, "email"),
               ("organization", "Organization", "text", True, "organization"), ("url", "Website address to scan", "text", True, "url")]

LEAD = f'''<dialog class="lead" id="lead" aria-labelledby="leadh"><div class="in"><button class="x" type="button" aria-label="Close">&times;</button>
<h2 id="leadh">Is your website ADA compliant?</h2><p>Get a free WCAG 2.1 AA report on your site. We read it with you, then fix what fails.</p>
{form("scan-request", SCAN_FIELDS, "Send my free report", pre="d-")}</div></dialog>'''

def flat(href):
    """/work/x/ -> work-x.html for the preview artifact."""
    m = re.match(r'^/([^#?"]*)(#.*)?$', href)
    if not m: return href
    p, frag = m.group(1), m.group(2) or ""
    if p.startswith(("fonts/", "img/")) or "." in p.split("/")[-1]: return p + frag
    p = p.strip("/")
    return (p.replace("/", "-") + ".html" if p else "index.html") + frag

_CONTR = [("do not", "don't"), ("does not", "doesn't"), ("did not", "didn't"), ("cannot", "can't"), ("is not", "isn't"), ("are not", "aren't"),
          ("it is", "it's"), ("that is", "that's"), ("we will", "we'll"), ("you will", "you'll"), ("we are", "we're"), ("you are", "you're"), ("they are", "they're")]
def contract(html):
    """House style (Tim, Nov 2026): contractions in running copy. Text nodes only; never tags, scripts or quotes from clients."""
    out = []
    skip = 0
    for part in re.split(r"(<[^>]+>)", html):
        if part.startswith("<"):
            low = part.lower()
            if re.match(r"<(script|style|blockquote|form|select)\b", low): skip += 1
            elif re.match(r"</(script|style|blockquote|form|select)>", low): skip = max(0, skip - 1)
            out.append(part); continue
        if not skip:
            for a, c in _CONTR:
                part = re.sub(r"\b" + a + r"\b(?=\s+[A-Za-z])", lambda m, c=c: (c[0].upper() + c[1:]) if m.group(0)[0].isupper() else c, part, flags=re.I)
        out.append(part)
    return "".join(out)

def page(path, title, desc, body, schema=None, h_nopop=False, index=True):
    if not (path.startswith("/content/") and path.count("/") > 2): body = contract(body)
    canon = DOMAIN + path
    crumbs = []
    parts = [x for x in path.strip("/").split("/") if x]
    graph = [{"@type": "Organization", "@id": DOMAIN + "/#org", "name": "Yoodle", "legalName": "Yoodle LLC", "url": DOMAIN + "/", "email": EMAIL,
              "foundingDate": "2007", "slogan": "Built on experience. Made for what's next.",
              "address": {"@type": "PostalAddress", "addressLocality": "Kansas City", "addressRegion": "MO", "addressCountry": "US"},
              "sameAs": ["https://www.linkedin.com/company/yoodle"],
              "knowsAbout": ["Higher education marketing", "Website design and development", "WCAG 2.1 AA accessibility", "Brand strategy", "SEO and AI search", "Podcast production"]},
             {"@type": "WebPage", "@id": canon, "url": canon, "name": title, "description": desc, "isPartOf": {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Yoodle"}, "dateModified": TODAY}]
    if schema: graph += schema
    robots = '<meta name="robots" content="noindex">' if (TEST_BUILD or not index) else ""
    out = f'''<!DOCTYPE html>
<html lang="en"{' data-nopop' if h_nopop else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canon}"><meta property="og:site_name" content="Yoodle">
<meta name="theme-color" content="#F7F4EE">{robots}
<link rel="preload" href="/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css">
</head>
<body{' class="test"' if TEST_BUILD else ''}>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
{'' if h_nopop else LEAD}

<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
<script src="/js/site.js" defer></script>
{REVIEW_TAG}
</body>
</html>
'''
    if PREVIEW:
        out = re.sub(r'(href|src|action)="(/[^"]*)"', lambda m: f'{m.group(1)}="{flat(m.group(2))}"', out)
        fp = os.path.join(OUT, flat(path))
    else:
        fp = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(out)
    if index: PAGES.append(path)

def crumbs(items):
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for h, t in items)
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{lis}</ol></nav>'

def crumb_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, **({"item": DOMAIN + h} if h else {})} for i, (h, t) in enumerate(items)]}

def faq_block(faq):
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)

def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def cover(p, lg=False, n=None):
    ci = cover_img(p)
    if ci: return f'<div class="cover ph{" lg" if lg else ""}"><img src="{ci["src"]}" alt="{e(p["name"])} {"website homepage" if p["url"] else "project"} by Yoodle" width="{ci["w"]}" height="{ci["h"]}"{"" if lg else " loading=\"lazy\""}></div>'
    lab, col = SECTORS[p["sector"]]
    host = re.sub(r"^https?://(www\.)?|/$", "", p["url"]) if p["url"] else p["kind"]
    return f'<div class="cover{" lg" if lg else ""}" style="background:{col}"><div class="k"><span>{lab}</span><span>{e(host)}</span></div><div class="n">{e(p["name"])}</div></div>'

def related(k, n=3):
    """Related work for a service page: Tim's ranked picks, then the projects that are most purely that service. Never untagged work."""
    top = SVC_TOP.get(k, [])
    pool = [(i, p) for i, p in enumerate(P) if k in SVC_TAGS.get(p["slug"], [])]
    def key(ip):
        i, p = ip
        return (top.index(p["slug"]) if p["slug"] in top else len(top), p["kind"] != SVC_KIND[k], len(SVC_TAGS[p["slug"]]),
                p["kind"] == "Project" or p["slug"] in SVC_OLDER, i)
    return [p for _, p in sorted(pool, key=key)][:n]

def svc_names(p):
    return ", ".join(SVC_LABEL[t] for t in SVC_TAGS.get(p["slug"], []))

def card(p):
    lab = SECTORS[p["sector"]][0]
    sub = p["place"] or p["kind"]
    if p["kind"] == "Project": sub = svc_names(p) or "Brand and web"; return f'<li data-s="{p["sector"]}"><a class="card" href="/work/{p["slug"]}/">{cover(p)}<h3>{e(p["name"])}</h3><p class="small">{e(sub)}</p></a></li>'
    return f'<li data-s="{p["sector"]}"><a class="card" href="/work/{p["slug"]}/">{cover(p)}<h3>{e(p["name"])}</h3><p class="small">{e(p["kind"])}{" · " + e(sub) if sub != p["kind"] else ""}</p></a></li>'

CTA_TEXT = "Bring the challenge. We&rsquo;ll bring the experience, the curiosity, and the people to make it happen."
ADA_END = ("Check your site.", "Get a free WCAG 2.1 AA accessibility report.", "/accessibility/", "Get my report.")
def closer(text=CTA_TEXT, button=("/contact/", "Start the conversation"), b=ADA_END):
    return f'''<section class="dark cta" style="padding:0" aria-label="Next steps"><div class="wrap ends">
<div><p class="eyebrow">Your next chapter starts with a conversation.</p><h2>What&rsquo;s next for you?</h2><p class="lede" style="margin:20px 0 28px">{text}</p><a class="btn" href="{button[0]}">{button[1]}</a></div>
<div><h2>{b[0]}</h2><p class="lede" style="margin:20px 0">{b[1]}</p><a class="go" href="{b[2]}">{b[3]}</a></div></div></section>'''

def marquee():
    half = (len(CLEAR) + 1) // 2
    def row(items, rev):
        def lw(s):  # equal visual weight: same area for every logo, capped so none is too wide or too tall
            a = s[0] / s[1]
            return round(min((9600 * a) ** .5, 210, 66 * a, s[0] * 1.2))
        lis = "".join(f'<li><img src="/img/logos/{fn}" alt="{e(n)}" width="{s[0]}" height="{s[1]}" style="--w:{lw(s)}px"></li>' for fn, n, s in items)
        dup = re.sub(r'alt="[^"]*"', 'alt=""', lis)
        return f'<div class="track{" rev" if rev else ""}"><ul>{lis}</ul><ul aria-hidden="true">{dup}</ul></div>'
    return f'''<div class="wrap"><p class="small" style="margin-bottom:10px">A few of the organizations that trust us with their name</p></div>
<div class="mq lg" id="mq">{row(CLEAR[:half], False)}{row(CLEAR[half:], True)}</div>
<div class="wrap"><button class="mqbtn" id="mqbtn" type="button" aria-pressed="false" aria-label="Pause scrolling logos"></button></div>'''

# ------------------------------------------------------------------ pages
def home():
    feat = [p for p in P if p["slug"] in ("nevada-state-university", "kansas-judicial-branch", "ut-austin-extended-campus", "kc-streetcar", "variety-kc", "fsu-career-center")]
    svc = "".join(f'<li><span class="idx" aria-hidden="true">0{i+1}</span><h3><a href="/services/#{v["key"]}">{v["name"]}</a></h3><div><p>{e(v["lede"])}</p><p class="sub">{e(v["sub"])}</p></div></li>' for i, v in enumerate(PILLARS))
    body = f'''<section class="hero"><div class="wrap">
<h1>Built on experience.<span class="r">Made for what&rsquo;s next.</span></h1>
<div class="herogrid"><p class="lede" style="margin:0">For {YEARS} years, we&rsquo;ve helped ambitious organizations turn complex challenges into brands, digital experiences, and marketing that move people.</p>
<p style="margin:0"><a class="btn" href="/work/">See the work</a> &nbsp; <a class="go" href="/contact/">Start a project.</a></p></div>
</div></section>
{marquee()}
<section><div class="wrap two"><h2>What your brand needs next.</h2><div>
<p class="lede">Experience tells us which playbook fits, and when to put it down. Curiosity keeps us looking for a better way to do it.</p>
<p>Most challenges don&rsquo;t arrive neatly labeled. Enrollment that has stalled, a launch that has to land, a website that no longer says who you are: each one touches brand, technology and marketing at once. So we think across all three, then deliver the whole answer.</p>
<p>What you get is finished work. A brand your people can carry, a digital experience that works for everyone who uses it, marketing you can measure. And if you&rsquo;d rather run it yourselves afterward, we&rsquo;ll train your team to do it.</p>
<p><a class="go" href="/services/">See what we do.</a></p></div></div></section>
<section class="dark"><div class="wrap"><p class="eyebrow">What we bring to the table</p><h2>Good thinking.<span class="r">Fully delivered.</span></h2><ol class="rows">{svc}
<li><span class="idx" aria-hidden="true">04</span><h3><a href="/experience/">Fractional CMO</a></h3><div><p>Put senior leadership behind the plan, and a team behind the leader.</p><p class="sub">Leadership / Planning / Execution</p></div></li></ol></div></section>
<section><div class="wrap"><div class="two" style="align-items:end"><h2>The work.<span class="r">Judge for yourself.</span></h2><p class="lede">{len(P)} projects, chosen from a much longer list. Most are live, so you can open them and see how they hold up.</p></div>
<ul class="grid">{"".join(card(p) for p in feat)}</ul><p style="margin-top:28px"><a class="go" href="/work/">See all the work.</a></p></div></section>
<section class="dark"><div class="wrap"><div class="two" style="align-items:end"><h2>Who we work with.</h2><p class="lede">Organizations with a mission to serve, a public to answer to, and more to get done than the team on hand can carry.</p></div><div class="cols">
<div class="col"><h3>The stakes are public.</h3><p>Your audience is a community: students, residents, donors, customers. When the brand or the website falls short, they notice first.</p></div>
<div class="col"><h3>The team is stretched.</h3><p>Good people, too many priorities. We add senior thinking and the hands to finish, then leave your team stronger.</p></div>
<div class="col"><h3>The challenge keeps coming back.</h3><p>Enrollment, awareness, compliance, growth: the same questions return every quarter. We design answers that hold up next year too.</p></div>
</div><p style="margin-top:36px"><a class="go" href="/work/">See who we&rsquo;ve done it for.</a></p></div></section>
<section><div class="wrap two"><h2>ADA website compliance.<span class="r">Before the deadline.</span></h2><div>
<p class="lede">Public colleges and larger governments must meet WCAG 2.1 AA by April 26, 2027. We audit, fix the site's own code, retest and certify.</p>
<p><a class="btn" href="/accessibility/">Get a free report</a></p></div></div></section>
{closer(b=("Fractional CMO.", "Senior marketing leadership inside your organization, with a team behind it.", "/experience/", "See how it works."))}'''
    page("/", "Yoodle | The Content Experience Agency: Brand, Technology, Marketing",
         f"Yoodle is the content experience agency. For {YEARS} years we've helped ambitious organizations turn complex challenges into brands and marketing that move people.", body,
         [{"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Yoodle", "publisher": {"@id": DOMAIN + "/#org"}}])

def work():
    fl = '<button class="chipb" type="button" data-f="all" aria-pressed="true">All</button>' + "".join(f'<button class="chipb" type="button" data-f="{k}" aria-pressed="false">{v[0]}</button>' for k, v in SECTORS.items())
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Work</p><h1>The work.<span class="r">Judge for yourself.</span></h1>
<p class="lede" style="margin-top:32px">{len(P)} projects, picked from a much longer client list. Many of the websites are live, so don't just take our word for it.</p>
<div class="filters" role="group" aria-label="Filter work by sector">{fl}</div><p class="small" id="count" role="status" style="margin:14px 0 0">{len(P)} projects shown</p>
<ul class="grid" id="grid">{"".join(card(p) for p in P)}</ul></div></section>
{closer()}'''
    items = [("/", "Home"), ("", "Work")]
    page("/work/", "Our Work: Higher Education, Government and Nonprofit Websites | Yoodle",
         f"{len(P)} selected projects by Yoodle: live websites for colleges, government agencies, nonprofits and small businesses, plus podcasts and video.", body,
         [crumb_schema(items), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{DOMAIN}/work/{p["slug"]}/', "name": p["name"]} for i, p in enumerate(P)]}])

RH_VID = '''<div style="position:relative;aspect-ratio:16/9;border-radius:8px;overflow:hidden;background:#000"><iframe src="https://player.vimeo.com/video/1230352325?dnt=1&amp;title=0&amp;byline=0&amp;portrait=0" title="Río Hondo College reel by Yoodle" allow="fullscreen; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe></div>'''
RH_NEW_PICK = ['Areas of Study', 'Nursing', 'Automotive Technology', 'Fire Technology & Emergency Response', 'Computer Science', 'Animation, Games & Entertainment Art', 'Business', 'Child Development', 'Psychology', 'Welding Technology']
RH_OPT_PICK = ['Admissions & Records Office', 'Class Registration', 'Academic Calendar', 'Counseling Center', 'Career & Technical Education', 'Automotive Technology Bachelor of Science', 'Continuing Education & Noncredit Division', 'Disabled Students Program & Services', 'Child Development Center', 'Commencement', 'Clubs & Organizations', 'Adult Re-Entry Program', 'Admissions FAQ', 'Academics', 'About']
def case_html(p):
    c = p["case"]
    names = lambda L: "".join(f"<li>{e(x)}</li>" for x in L)
    return f'''<section class="dark"><div class="wrap"><h2>By the numbers.</h2><div class="cols c4">{"".join(f'<div class="col"><p class="big" style="font-size:clamp(3.2rem,7vw,6rem);margin:8px 0 14px">{n}</p><p>{e(t)}</p></div>' for n, t in c["stats"])}</div></div></section>
<section><div class="wrap"><h2>Nine goals.<span class="r">Fully delivered.</span></h2><ol class="rows">{"".join(f'<li><span class="idx" aria-hidden="true">0{i + 1}</span><h3>{e(a)}.</h3><p>{e(t)}</p></li>' for i, (a, t) in enumerate(c["goals"]))}</ol></div></section>
<section class="tight"><div class="wrap two"><h2>Pages we built.</h2><div><p class="lede">Fifty new pages, written and built by Yoodle: the homepage, an Areas of Study hub and a page for every area of study.</p><p>A few of them:</p><ul class="sect">{names(RH_NEW_PICK)}</ul><p>The other forty follow the same model, one for each program a student can choose. Thirty-three were revised in a second round and finished in August 2024.</p></div></div></section>
<section class="tight"><div class="wrap two"><h2>Pages we rewrote.</h2><div><p class="lede">Seventy-seven existing pages rewritten and optimized, from admissions and registration to student services.</p><p>A few of them:</p><ul class="sect">{names(RH_OPT_PICK)}</ul><p>The rest cover the college&rsquo;s academic divisions, programs and support offices. All were approved by the college in May 2024.</p></div></div></section>
<section class="dark"><div class="wrap two"><h2>On camera.</h2><div><p class="lede">Ten video series and a photo library, shot on campus for the new pages, with vertical cuts for social.</p><ul class="sect">{names(RH_VIDEO)}</ul><p style="margin-top:24px"><a class="go" href="https://vimeo.com/1230352325">Watch the reel on Vimeo.</a></p></div></div>
</section>'''

VERDICT = {"Workforce training": "Taught.", "Brand and marketing": "Delivered.", "Website": "Launched.", "Podcast": "Produced.", "Video and content": "Produced.", "Project": "Delivered."}
def project(i, p):
    lab = SECTORS[p["sector"]][0]
    prev, nxt = P[i - 1], P[(i + 1) % len(P)]
    host = re.sub(r"^https?://(www\.)?|/$", "", p["url"])
    facts = [("Client", e(p["name"])), ("Sector", lab), ("Type", p["kind"])]
    if p["platform"]: facts.append(("Platform", e(p["platform"])))
    elif p["kind"] == "Website": facts.append(("Platform", confirm("platform")))
    if p["place"]: facts.append(("Location", e(p["place"])))
    eng = p.get("eng") or ((YEARS_ARCHIVE[p["slug"]], "") if p["slug"] in YEARS_ARCHIVE else None)
    if eng and eng[0]: facts.append(("Year" if p["kind"] == "Project" else "Engagement", e(eng[0])))
    if p["url"]: facts.append(("Live site", f'<a href="{p["url"]}">{host}</a>'))
    about = f'<p class="lede">{e(p["case"]["lede"])}</p>' if p.get("case") else f'<p class="lede">{e(p["about"])}</p>' if p["about"] else f'<p class="lede">{e(p["name"])} is a {p["kind"].lower()} produced by Yoodle.</p>'
    need = {"Website": "Yoodle's scope (strategy, design, build, migration, support), launch year, results and a client quote",
            "Podcast": "exact show name, link, host and cover art",
            "Video and content": "project details from the client folder: what was produced, how many videos and pages, and when",
            "Project": "year, and whether to keep this project on the new site",
            "Brand and marketing": "results to cite and the final brand strategy deliverable",
            "Workforce training": "the years the program ran, and how many cohorts and graduates"}[p["kind"]]
    o = OLD.get(p["slug"])
    story = gal = ""
    if o:
        facts.insert(3, ("Services", e(svc_names(p) or "Brand and web")))
        blk = o["blocks"] if p["kind"] != "Project" else [x for x in o["blocks"] if x[1] != p["about"]]
        if blk: story = f'<section class="tight"><div class="wrap two"><h2>{"The work." if p["kind"] == "Project" else "The story."}</h2><div>{rich(blk)}</div></div></section>'
        rest = o["imgs"][1:] if not (cover_img(p) or {"src": ""})["src"].startswith("/img/shots/") else o["imgs"]
        if rest: gal = '<section class="tight"><div class="wrap"><ul class="gal">' + "".join(f'<li><img src="{g["src"]}" alt="{e(p["name"])}: work by Yoodle, image {k + 1}" width="{g["w"]}" height="{g["h"]}" loading="lazy"></li>' for k, g in enumerate(rest)) + '</ul></div></section>'
    if not story and p.get("story"):
        src = "".join(f'<a href="{u}" rel="noopener">{e(t)}</a>' + (", " if k < len(p["story_src"]) - 1 else ".") for k, (t, u) in enumerate(p.get("story_src", [])))
        story = f'<section class="tight"><div class="wrap two"><h2>The story.</h2><div>{"".join(f"<p>{e(x)}</p>" for x in p["story"])}{f'<p class="small" style="opacity:.7">Sources: {src}</p>' if src else ""}</div></div></section>'
    quote = f'<section class="dark band"><div class="wrap"><figure style="margin:0;max-width:22ch;font-size:{"clamp(32px,5.2vw,72px)" if len(p["quote"][0]) < 90 else "clamp(22px,2.6vw,36px)"};max-width:{"22ch" if len(p["quote"][0]) < 90 else "36ch"}"><blockquote style="margin:0;font-family:var(--hd,inherit);font-weight:600;letter-spacing:-.03em;line-height:1.02">\u201c{e(p["quote"][0])}\u201d</blockquote></figure><p style="margin-top:28px;max-width:52ch;opacity:.8">{e(p["quote"][1])}</p></div></section>' if p.get("quote") else ""
    nums = f'<section class="dark"><div class="wrap"><h2>{"By the numbers." if p.get("stats_src") else "The site today."}</h2><div class="cols c4">{"".join(f'<div class="col"><p class="big" style="font-size:clamp(3.2rem,7vw,6rem);margin:8px 0 14px">{n}</p><p>{e(x)}</p></div>' for n, x in p["stats"])}</div><p style="margin-top:28px;opacity:.7;font-size:.9rem">Source: {p.get("stats_src") or GA_RANGE}.</p></div></section>' if p.get("stats") else ""
    if p.get("gallery"): gal = '<section class="tight"><div class="wrap"><ul class="gal">' + "".join(f'<li style="aspect-ratio:{g[1]}/{g[2]};background:#fff"><img src="/img/work/{p["slug"]}/{k}.webp" alt="{e(p["name"])}: {e(g[0])}" width="{g[1]}" height="{g[2]}" loading="lazy"></li>' for k, g in enumerate(p["gallery"])) + '</ul></div></section>'
    if os.path.exists(os.path.join(ROOT, "assets/img/process", p["slug"], "0.webp")): gal += f'<section class="tight"><div class="wrap two"><h2>Before the build.</h2><div><p>Every Yoodle site is worked out as wireframes first: the navigation, the page types and what each page has to do, agreed with the client before design starts.</p></div></div><div class="wrap" style="margin-top:clamp(20px,3vw,40px)"><div style="border-radius:8px;overflow:hidden;border:1px solid #d9d4c8"><img src="/img/process/{p["slug"]}/0.webp" alt="{e(p["name"])}: wireframes by Yoodle for the homepage and two inner pages" width="1600" height="1200" loading="lazy" style="display:block;width:100%;height:auto"></div></div></section>'
    feats = f'<section class="tight"><div class="wrap two"><h2>On the site.</h2><ul class="sect">{"".join(f"<li>{e(f)}</li>" for f in p["features"])}</ul></div></section>' if p["features"] else ""
    if p["kind"] == "Brand and marketing": visit = ""
    if p["kind"] != "Website" and p["features"]:
        feats = feats.replace("On the site.", "What we made.")
    visit = f'<p><a class="btn" href="{p["url"]}">Visit {host}</a></p>' if p["url"] else ""
    lk = p.get("links") or []
    if lk and p.get('case'): facts[:] = [f for f in facts if f[0] != 'Live site'] + [('Year', '2024')]
    if lk: visit = '<p style="display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center">' + f'<a class="btn" href="{lk[0][1]}">{e(lk[0][0])}</a>' + "".join(f'<a class="go" href="{u}">{e(t)}</a>' for t, u in lk[1:]) + "</p>"
    body = f'''<section class="hero"><div class="wrap">{crumbs([("/", "Home"), ("/work/", "Work"), ("", e(p["name"]))])}
<h1 class="md">{e(p["name"])}.<span class="r">{VERDICT[p["kind"]]}</span></h1>
<div style="margin-top:clamp(28px,5vw,56px)">{RH_VID if p.get("case") else cover(p, lg=True)}</div>
{"" if cover_img(p) else '<p class="small" style="margin-top:10px">' + confirm("real screenshots of the live site replace this cover" if p["url"] else "images replace this cover once the rest of the backup is brought over") + "</p>"}
</div></section>
<section class="tight"><div class="wrap"><dl class="facts">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)}</dl></div></section>
<section class="tight"><div class="wrap two"><h2>The project.</h2><div>{about}{'<p>' + e(eng[1]) + '</p>' if eng and eng[1] else ''}{'' if ((p['kind'] == 'Podcast' and p['about']) or p.get('case') or eng or p['kind'] == 'Project') else '<p>' + confirm(need) + '</p>'}{visit}</div></div></section>
{case_html(p) if p.get("case") else feats}
{story}
{nums}{gal}{quote}
<section class="tight"><div class="wrap"><nav class="pn" aria-label="More work"><a href="/work/{prev["slug"]}/"><span class="small">Previous</span><br><strong>{e(prev["name"])}</strong></a><a class="nx" href="/work/{nxt["slug"]}/"><span class="small">Next</span><br><strong>{e(nxt["name"])}</strong></a></nav></div></section>
{closer(b=("See more work.", "Projects chosen from a much longer list.", "/work/", "See the work."))}'''
    t = {"Website": f'{p["name"]} Website | {lab} Web Design by Yoodle', "Podcast": f'{p["name"]} | Podcast Production by Yoodle', "Video and content": f'{p["name"]} | Video Production by Yoodle', "Project": f'{p["name"]} | {lab} Brand and Web Work by Yoodle', "Brand and marketing": f'{p["name"]} | Rebrand and Marketing by Yoodle', "Workforce training": f'{p["name"]} | Workforce Training'}[p["kind"]]
    if len(t) > 68: t = f'{p["name"]} | {"Web Design" if p["kind"] == "Website" else "Work"} by Yoodle'
    d = (p["about"] or f'{p["name"]}, a {p["kind"].lower()} produced by Yoodle, the content experience agency.')
    d = (f'{p["name"]}: ' if p["name"] not in d[:60] else "") + d
    d = d if len(d) <= 158 else d[:155].rsplit(" ", 1)[0] + "..."
    cw = {"@type": "CreativeWork", "name": p["name"], "creator": {"@id": DOMAIN + "/#org"}, "about": lab, "genre": p["kind"]}
    if p["url"]: cw["url"] = p["url"]
    page(f'/work/{p["slug"]}/', t, d, body, [crumb_schema([("/", "Home"), ("/work/", "Work"), ("", p["name"])]), cw])

def services():
    rows = "".join(f'''<div class="pillar" id="{v["key"]}"><div class="ph"><div><p class="tagc">{e(v["sub"])}</p><h3>{v["name"]}.</h3></div><p class="lede" style="margin:0">{e(v["lede"])}</p></div>
<div class="caps">{"".join(f"<details class=cap><summary>{e(n)}</summary><p>{e(x)}</p></details>" for n, x in v["caps"])}</div>
<p class="more">{"".join(f'<a class="go" href="{u}">{l}</a>' for u, l in v["links"])}</p></div>''' for v in PILLARS)
    faq = [("What does Yoodle do?", f"Yoodle is the content experience agency, working across brand, technology and marketing. For {YEARS} years we have helped ambitious organizations turn complex challenges into brands, digital experiences and marketing that move people."),
           ("Who does Yoodle work with?", "Public colleges and universities, government agencies and commissions, nonprofits and owner-run businesses. We also work as a teaming partner or subcontractor to prime contractors."),
           ("How does a project start?", "With a scope. You tell us the outcome, we write down what will be delivered, when and for how much, and work starts once you approve it.")]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Services</p><h1>Brand, technology and marketing.<span class="r">One team.</span></h1>
<p class="lede" style="margin-top:32px">Three practices and one team. Bring us in for one, or bring the whole challenge and let them work together.</p></div></section>
<section class="dark"><div class="wrap"><p class="eyebrow">What we bring to the table</p><h2>Good thinking.<span class="r">Fully delivered.</span></h2>{rows}
<div class="pillar" id="fractional-cmo"><div class="ph"><div><p class="tagc">Leadership / Planning / Execution</p><h3>Fractional CMO.</h3></div><div><p class="lede" style="margin:0 0 18px">Put senior leadership behind the plan, and a team behind the leader.</p><p class="more" style="margin:0"><a class="go" href="/experience/">More on fractional CMO.</a></p></div></div></div>
</div></section>
<section><div class="wrap"><h2>How we work.</h2><ol class="rows">
<li><span class="idx" aria-hidden="true">01</span><h3>Think it through.</h3><p>We start with the challenge, then put the answer on one page: the outcome, what we deliver, the date and the price.</p></li>
<li><span class="idx" aria-hidden="true">02</span><h3>Build it.</h3><p>A senior team does the work, quickly. When the plan meets something unexpected, we reach for whatever does the job best, and a person answers for everything that ships.</p></li>
<li><span class="idx" aria-hidden="true">03</span><h3>Launch it.</h3><p>Tested for accessibility, speed and accuracy before it goes out under your name.</p></li>
<li><span class="idx" aria-hidden="true">04</span><h3>Hand it over, or run it.</h3><p>We train your team to own it, or we keep running it. Your choice.</p></li></ol></div></section>
<section class="tight"><div class="wrap two"><h2>Partner with us.</h2><div><p class="lede">Prime contractors and agencies bring Yoodle in for the brand, web, accessibility and content parts of larger public-sector contracts.</p>
<p>We work to your process, your schedule and your reporting.</p><p><a class="go" href="/contact/">Talk about teaming.</a></p></div></div></section>
<section class="tight"><div class="wrap two"><h2>Questions.</h2><div>{faq_block(faq)}</div></div></section>
{closer()}'''
    items = [("/", "Home"), ("", "Services")]
    page("/services/", "Services: Brand, Technology and Marketing | Yoodle",
         "Yoodle's capabilities across brand, technology and marketing: strategy, identity, websites, accessibility, digital experiences, campaigns and content.", body, [crumb_schema(items), faq_schema(faq)])
    for k, v in SERVICES.items():
        rel = related(k)
        body = f'''<section class="hero"><div class="wrap">{crumbs([("/", "Home"), ("/services/", "Services"), ("", v["name"])])}
<h1 class="md">{v["name"]}.<span class="r">{v["verdict"]}</span></h1><p class="lede" style="margin-top:32px">{e(v["lede"])}</p></div></section>
<section class="tight"><div class="wrap two"><h2>The approach.</h2><div>{"".join(f"<p>{e(b)}</p>" for b in v["body"])}</div></div></section>
<section class="dark"><div class="wrap"><h2>What you get.</h2><ol class="rows">{"".join(f'<li><span class="idx" aria-hidden="true">0{i+1}</span><h3>{e(a)}.</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(v["items"]))}</ol></div></section>
<section><div class="wrap"><h2>Related work.</h2><ul class="grid">{"".join(card(p) for p in rel)}</ul><p style="margin-top:28px"><a class="go" href="/work/">See all the work.</a></p></div></section>
<section class="tight"><div class="wrap two"><h2>Questions.</h2><div>{faq_block(v["faq"])}</div></div></section>
{closer()}'''
        its = [("/", "Home"), ("/services/", "Services"), ("", v["name"])]
        page(f"/services/{k}/", v["title"] + " | Yoodle", v["desc"], body,
             [crumb_schema(its), faq_schema(v["faq"]), {"@type": "Service", "name": v["title"], "serviceType": v["name"], "provider": {"@id": DOMAIN + "/#org"}, "areaServed": "US", "description": v["desc"]}])

def experience():
    steps = [("Diagnose", "Thirty days inside your business. We run the CX Finder diagnostic across your brand, channels, data and team, and name what is working."),
             ("Pivot", "A plain plan: what stops, what starts, what it costs and what it should return."),
             ("Create", "We build the missing pieces: positioning, website fixes, campaigns, content, dashboards."),
             ("Optimize", "Weekly numbers, monthly decisions. Spend moves to what works."),
             ("Amplify", "Scale the winners, and train your team or your first marketing hire to take over.")]
    faq = [("What is a fractional CMO?", "A fractional CMO is a senior marketing leader who works inside your organization part time on a fixed contract. You get the strategy, the plan and the management of the work without a full-time executive salary."),
           ("How long is an engagement?", "Six months. The first 90 days are a sprint to diagnose, plan and launch. The following months run and improve the system."),
           ("Who hires a fractional CMO?", "Organizations with a marketing staff and no senior marketing leader: growing companies, multi-location businesses, nonprofits and public-sector teams. We lead the team you have and build it up in house."),
           ("How many clients does Tim take on?", "Only a few at a time. Two openings are available now.")]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Experience</p><h1>Your fractional CMO.<span class="r">With a team.</span></h1>
<div class="herogrid"><p class="lede" style="margin:0">A fractional CMO and the agency behind him, inside your organization for six months. For companies with a marketing staff that needs senior leadership, and a plan to grow it.</p>
<div class="timcta"><img src="/img/tim-mccoy.webp" alt="Tim McCoy, fractional CMO and president of Yoodle" width="900" height="900"><div><p style="margin:0 0 12px"><strong>Tim McCoy</strong><br><span class="small">Fractional CMO, president of Yoodle</span></p><a class="btn" href="/contact/">Talk to Tim</a></div></div></div></div></section>
<section class="tight"><div class="wrap two"><h2>A fractional CMO who operates.</h2><div><p class="lede">Tim McCoy has led Yoodle for {YEARS} years and is the fractional CMO of Savvy Bridal and Vow Ready, a five-store bridal retail group. The systems we bring to clients are already at work there.</p>
<p>Most fractional CMOs bring a plan and leave the work to you. Here you get the leader and the hands. Tim leads the people you already have, and Yoodle builds what they can&rsquo;t yet: the brand, the website, the campaigns, the reporting.</p>
<p>The goal is an in-house team that no longer needs us. We coach your staff, help you make the next hire, and hand over the playbook.</p>
<p class="spots"><strong>Two openings left.</strong> Tim works with only a few companies at a time, so each one gets a leader who is actually in the room. <a class="go" href="/contact/">Ask about a spot.</a></p></div></div></section>
<section class="dark"><div class="wrap"><h2>Six months.</h2><ol class="rows">{"".join(f'<li><span class="idx" aria-hidden="true">0{i+1}</span><h3>{a}.</h3><p>{b}</p></li>' for i, (a, b) in enumerate(steps))}</ol></div></section>
<section><div class="wrap"><h2>Fractional CMO work.<span class="r">In practice.</span></h2><div class="cols c2">
<div class="col"><div class="xlogo"><img src="/img/logos/t-w20.webp" alt="Savvy Bridal logo" width="480" height="170" loading="lazy"></div><h3>Savvy Bridal and Vow Ready.</h3><p>Five bridal stores in three states. Tim serves as their fractional CMO, an in-house team runs the day to day, and Yoodle builds what the team needs: websites, dashboards, campaigns.</p><a class="go" href="/bridal/">The bridal story.</a></div>
<div class="col"><div class="xlogo"><img src="/img/logos/t-w16.webp" alt="American Jazz Museum logo" width="311" height="220" loading="lazy"></div><h3>American Jazz Museum.</h3><p>A twelve-month fractional CMO retainer, 2023 to 2024. Tim led marketing for the museum at 18th and Vine and reported to its executive director and board, while Yoodle supplied the creative, technical and production teams.</p><p>In that year: quarterly marketing reports to the board, the annual report, the Free February campaign, online tickets and memberships, the museum newsletter, and The Big Break podcast with its own marketing plan. Tim also ran the search for a Director of Marketing and Communications, and left with two trained hires in place.</p><a class="go" href="/work/the-big-break/">The Big Break.</a></div>
</div></div></section>
<section class="tight"><div class="wrap two"><h2>Questions.</h2><div>{faq_block(faq)}</div></div></section>
{closer(text="Need a marketing leader? Bring the challenge. We&rsquo;ll bring the experience, the curiosity, and the people to make it happen.", button=("/contact/", "Talk to a fractional CMO"), b=("See the bridal story.", "The model, proven in five stores.", "/bridal/", "Read it."))}'''
    its = [("/", "Home"), ("", "Experience")]
    page("/experience/", "Fractional CMO and Marketing Leadership | Yoodle",
         "Fractional CMO and marketing director services from Yoodle. A senior leader and a full team inside your organization on a six-month contract.", body, [crumb_schema(its), faq_schema(faq)])

def bridal():
    solved = [("A website that couldn't keep up", "savvybridalboutique.com", "Three cities, one front door. Rebuilt from the ground up to move faster than she can change her mind.", "/work/savvy-bridal/"),
              ("She needs a gown now", "vowready.com", "The gown she wants, ready the day she finds it.", ""),
              ("Brides order too late", "Timeline", "She gives us one date. We give her back every deadline that matters.", ""),
              ("Stylists met her cold", "Stylist Edit", "Her stylist knows her taste before she walks through the door.", ""),
              ("Competitors move quietly", "Competitor and ad dashboard", "Our ads and theirs, side by side. Nothing in the market moves unnoticed.", ""),
              ("Great selling lived in a few heads", "Training platform", "How the Savvy way of selling gets passed on.", "")]
    nums = [("Revenue", "+35%"), ("Gown orders", "+35%"), ("Ad spend", "+7%"), ("Ad spend per gown order", "&minus;21%")]
    team = [("Creative direction", "Every campaign starts with one idea and one voice. Savvy Bridal sounds like a private appointment. Vow Ready sounds like a gown she takes home today. Nothing ships that blurs the two."),
            ("A production team", f"An in-house crew shoots in the stores and publishes every day. We hired them with the owner, trained them, and built the system that moves work from idea to post without the owner chasing it. {confirm('team roles and publishing rhythm')}"),
            ("Launches", "When the fifth store opened in St. Louis on November 2, 2026, the site, the listings, the ads and the content were ready. It booked 40 new brides in its first three weeks."),
            ("Leadership", "Tim answers to the CEO and sits down with the store managers every quarter, so the stores and the marketing team work from one plan.")]
    ceo = [("Positioning", "Who she is to her industry, in one line. For Imene McCoy, the founder of Savvy Bridal, it became Higher Standards: good enough was never the plan."),
           ("Brand design", "A name, a look, channel art and a thumbnail style you can pick out of a feed."),
           ("Content planning", "A weekly queue of topics drawn from her own stories: hiring, mistakes, and growing to five stores."),
           ("Creative direction and production", "Unscripted conversations shot in the stores, then edited into a full episode and a set of shorts."),
           ("Posting", "Each episode goes out on YouTube, as a Substack post, and as cuts for LinkedIn and Meta. One recording, four places."),
           ("Metrics analysis", "We read what gets watched and what gets skipped, and next week's plan follows it.")]
    faq = [("Do you work with shops other than Savvy Bridal and Vow Ready?", "Yes. The system was built with them so it could be installed in other shops."),
           ("What does a fractional CMO do for a bridal shop?", "Leads marketing as a member of your team: sets the plan, manages the budget, the agency work and your outside partners, and builds and trains your in-house team so the shop is not dependent on outside help."),
           ("What results has the model produced?", "From January to September 2026, against the same months of 2025, revenue at the three Savvy Bridal stores rose 35% and gown orders rose 35%, while ad spend rose 7%."),
           ("Is Savvy Bridal your only fractional CMO client?", "No. It is the second. The first was the American Jazz Museum in Kansas City, a twelve-month engagement in 2023 and 2024."),
           ("Will you work with a shop in my city?", "Not within 60 miles of a Savvy Bridal or Vow Ready store, open or planned. Everywhere else, yes."),
           ("How long is an engagement?", "Six months. The first 90 days install the system. The rest trains your team to run it.")]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Bridal</p><h1>Bridal marketing.<span class="r">Proven in five stores.</span></h1>
<div class="herogrid"><p class="lede" style="margin:0">Savvy Bridal and Vow Ready run five stores in Kansas City, St. Louis and Fort Lauderdale. Tim McCoy is their fractional CMO, and Yoodle builds their tools and trains their team. It's the same model we bring to your shop.</p>
<p style="margin:0"><a class="btn" href="/contact/">Talk about your shop</a></p></div></div></section>
<figure class="bleed"><img src="/img/bridal/hero-three-brides-1600.webp" srcset="/img/bridal/hero-three-brides-960.webp 960w, /img/bridal/hero-three-brides-1600.webp 1600w" sizes="100vw" alt="Three brides in Savvy Bridal gowns posed around an arched mirror in a white studio" width="1600" height="1067"></figure>
<section class="tight"><div class="wrap two"><h2>A true story.</h2><div><p class="lede">Savvy Bridal opened in 2013. It grew to three cities, then added Vow Ready, an off-the-rack brand, in 2026.</p>
<p>It did not grow on an agency retainer alone, and it did not grow on an in-house team alone. It took four parts working together, and that's the model we bring to other shops. Savvy Bridal is Yoodle's second fractional CMO client, after the <a href="/experience/">American Jazz Museum</a>.</p></div></div></section>
<section class="tight"><div class="wrap"><h2>The numbers.<span class="r">Year over year.</span></h2><p class="lede" style="margin:24px 0 clamp(28px,4vw,48px)">January to September 2026 against the same months of 2025, at the three Savvy Bridal stores.</p>
<dl class="facts nums">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in nums)}</dl>
<p class="lede" style="margin-top:clamp(20px,3vw,36px)">Sales grew five times faster than the ad budget. Fort Lauderdale, in its second year, is up 128%.</p></div></section>
<section class="dark"><div class="wrap"><h2>Four parts.</h2><ol class="rows">
<li><span class="idx" aria-hidden="true">01</span><h3>A marketing leader.</h3><p>A fractional CMO who owns the plan, the budget and the numbers, and answers to the owner.</p></li>
<li><span class="idx" aria-hidden="true">02</span><h3>An agency behind them.</h3><p>Yoodle builds what the plan calls for: brand, websites, ads, content and reporting. No hiring wait.</p></li>
<li><span class="idx" aria-hidden="true">03</span><h3>An in-house team.</h3><p>Your own people run the day to day: social, events, follow-up, the stores. We hire with you, train them and hand over the playbook.</p></li>
<li><span class="idx" aria-hidden="true">04</span><h3>Partners, managed.</h3><p>BridalLive, I Do Society, Yelp, TikTok, Meta, Google: a bridal shop runs on platforms, and every one needs setting up, customizing and watching. We manage them all, and the people behind them, so you don't have to.</p></li></ol></div></section>
<section><div class="wrap"><h2>A full marketing team.<span class="r">Firing on all cylinders.</span></h2><p class="lede" style="margin-top:24px">What a five-store bridal group looks like once the four parts are in place.</p>
<div class="vids">{"".join(f'<figure><video src="/img/bridal/{k}.mp4" poster="/img/bridal/{k}-poster.webp" muted loop playsinline preload="metadata" aria-label="Inside Savvy Bridal {c}"></video><figcaption>{c}</figcaption></figure>' for k, c in (("kc", "Kansas City"), ("stl", "St. Louis"), ("ftl", "Fort Lauderdale")))}</div>
<p class="vidbar"><button type="button" class="vidbtn" hidden aria-pressed="false">Pause video</button></p>
<ol class="rows">{"".join(f'<li><span class="idx" aria-hidden="true">0{i + 1}</span><h3>{e(n)}.</h3><p>{t}</p></li>' for i, (n, t) in enumerate(team))}</ol>
<div class="made"><figure><video src="/img/bridal/hiring.mp4" poster="/img/bridal/hiring-poster.webp" controls playsinline preload="none" aria-label="Savvy Bridal St. Louis hiring event video"></video><figcaption>The St. Louis hiring video.</figcaption></figure>
<figure><a class="yt" href="https://www.youtube.com/watch?v=6E99vobWrpY" data-yt="6E99vobWrpY"><span class="ytplay" aria-hidden="true"></span><span class="yttitle">What it&rsquo;s like working at Savvy Bridal</span><span class="small">Watch on YouTube</span></a><figcaption>The culture video, from the Savvy Bridal YouTube channel.</figcaption></figure>
<p class="lede">Recruiting is marketing too. The team that sells the gown also tells the story of working here.</p></div></div></section>
<figure class="bleed"><img src="/img/bridal/curb-appeal-1600.webp" srcset="/img/bridal/curb-appeal-960.webp 960w, /img/bridal/curb-appeal-1600.webp 1600w" sizes="100vw" alt="A Savvy Bridal storefront with flowers climbing the windows under a blue sky" width="1600" height="1067" loading="lazy"></figure>
<section class="tight"><div class="wrap"><h2>Problems, solved.<span class="r">For her and for the team.</span></h2><p class="lede" style="margin-top:24px">Each of these started as a problem on the shop floor. When no software fixed it, we built the tool.</p>
<div class="cols c2">
<div class="col"><h3>Walk-ins had nowhere to wait.</h3><p>Vow Ready takes walk-ins, and nobody wants to spend a Saturday standing in a bridal shop waiting for a turn.</p><p>So we built the Q. She joins the line from a kiosk or her phone, leaves for coffee, and gets a text when her stylist is ready. The store sees the whole line on one screen.</p></div>
<div class="col"><h3>Five stores, and no single view of them.</h3><p>Sales lived in one system, ads in several more, and every store had its own logins. The owners could not see the business in one place.</p><p>So we built the growth dashboard: sales, bookings and ad spend, store by store, on one screen the leadership team opens every week.</p></div>
</div>
<ol class="rows">{"".join(f'<li><span class="idx" aria-hidden="true">0{i + 1}</span><h3>{e(pr)}.</h3><div><p><strong>{f"<a href={chr(34)}{u}{chr(34)}>{e(n)}</a>" if u else e(n)}.</strong> {e(t)}</p></div></li>' for i, (pr, n, t, u) in enumerate(solved))}</ol>
<p class="lede" style="margin-top:clamp(28px,4vw,48px)">How each one works, and which your shop needs first, is the conversation.</p><p><a class="btn" href="/contact/">Talk about your shop</a></p></div></section>
<section class="dark"><div class="wrap"><h2>The owner, as a brand.<span class="r">CEO brand development.</span></h2><p class="lede" style="margin-top:24px">Shop owners buy from people they trust. So we build the owner's own platform next to the shop's. The proof is Higher Standards with Imene McCoy: 40 videos published so far.</p>
<figure class="laptop"><div class="scr"><img src="/img/bridal/higher-standards-youtube.webp" alt="The Higher Standards with Imene McCoy YouTube channel page, showing its banner and three recent videos" width="1440" height="802" loading="lazy"></div><div class="base" aria-hidden="true"></div></figure>
<ol class="rows">{"".join(f'<li><span class="idx" aria-hidden="true">0{i + 1}</span><h3>{e(n)}.</h3><p>{e(t)}</p></li>' for i, (n, t) in enumerate(ceo))}</ol></div></section>
<figure class="bleed" style="margin-top:clamp(56px,9vw,128px)"><img src="/img/bridal/hero-bride-sofa-1600.webp" srcset="/img/bridal/hero-bride-sofa-960.webp 960w, /img/bridal/hero-bride-sofa-1600.webp 1600w" sizes="100vw" alt="A bride in a strapless lace gown seated on a blush sofa, laughing" width="1600" height="1067" loading="lazy"></figure>
<section class="tight"><div class="wrap two"><h2>Questions.</h2><div>{faq_block(faq)}</div></div></section>
<script>(function(){{[].forEach.call(document.querySelectorAll('a.yt[data-yt]'),function(a){{a.addEventListener('click',function(ev){{ev.preventDefault();var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+a.getAttribute('data-yt')+'?autoplay=1&rel=0';f.title='What it is like working at Savvy Bridal';f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';a.appendChild(f)}})}});var v=[].slice.call(document.querySelectorAll('.vids video')),b=document.querySelector('.vidbtn');if(!v.length||!b||!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;var on=true;b.hidden=false;var io=new IntersectionObserver(function(es){{es.forEach(function(x){{x.target._in=x.isIntersecting;if(on&&x.isIntersecting){{var p=x.target.play();if(p&&p.catch)p.catch(function(){{}})}}else x.target.pause()}})}},{{threshold:.25}});v.forEach(function(x){{io.observe(x)}});b.addEventListener('click',function(){{on=!on;b.textContent=on?'Pause video':'Play video';b.setAttribute('aria-pressed',String(!on));v.forEach(function(x){{if(on&&x._in){{var p=x.play();if(p&&p.catch)p.catch(function(){{}})}}else x.pause()}})}})}})();</script>
{closer(text="Own a bridal shop? Tell us where marketing is stuck. We&rsquo;d love to help.")}'''
    its = [("/", "Home"), ("", "Bridal")]
    page("/bridal/", "Bridal Shop Marketing and Fractional CMO | Yoodle", "Fractional CMO services for bridal shops from the team behind Savvy Bridal and Vow Ready: a leader, an agency and an in-house team, proven in five stores.", body,
         [crumb_schema(its), faq_schema(faq), {"@type": "Service", "name": "Bridal shop marketing and fractional CMO", "provider": {"@id": DOMAIN + "/#org"}, "areaServed": "US"}])

def content():
    shows = [p for p in P if p["sector"] == "content"]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Content</p><h1>Shows and writing.<span class="r">Worth your time.</span></h1>
<p class="lede" style="margin-top:32px">The podcasts we produce and publish, and Soapbox, the Yoodle blog.</p></div></section>
<section class="tight"><div class="wrap"><h2>Our shows.</h2><ul class="grid">{"".join(card(p) for p in shows)}</ul></div></section>
<section><div class="wrap two"><h2>Soapbox.</h2><div><p class="lede">Notes on brand, web, accessibility and AI search for people who answer to the public.</p>
</div></div>
<div class="wrap"><ul class="posts">{"".join(f'<li><a href="/content/{x["slug"]}/">' + (f'<div class="th im"><img src="{x["img"]["src"]}" alt="" width="{x["img"]["w"]}" height="{x["img"]["h"]}" loading="lazy"></div>' if x.get("img") else '<div class="th" aria-hidden="true">Soapbox</div>') + f'<span class="small">{x["date"][:7]}</span><h3>{e(x["title"])}</h3></a></li>' for x in POSTS)}</ul></div></section>
{closer(b=("Have a show in mind?", "We plan it, produce it and publish it.", "/services/content/", "See content services."))}'''
    its = [("/", "Home"), ("", "Content")]
    page("/content/", "Content: Podcasts and the Soapbox Blog | Yoodle", "Podcasts produced by Yoodle, plus Soapbox, the Yoodle blog on brand, web, accessibility and AI search.", body, [crumb_schema(its)])

def posts():
    for x in POSTS:
        first = next((t for k, t in x["blocks"] if k == "p"), x["title"])
        dsc = first if len(first) <= 158 else first[:155].rsplit(" ", 1)[0] + "..."
        its = [("/", "Home"), ("/content/", "Content"), ("", x["title"])]
        body = f'''<section class="hero"><div class="wrap">{crumbs([("/", "Home"), ("/content/", "Content"), ("", e(x["title"]))])}
<p class="tag">Soapbox · {x["date"]}</p><h1 class="md">{e(x["title"])}</h1>{f'<div class="cover ph lg" style="margin-top:clamp(28px,5vw,56px)"><img src="{x["img"]["src"]}" alt="" width="{x["img"]["w"]}" height="{x["img"]["h"]}"></div>' if x.get("img") else ""}</div></section>
<section class="tight"><div class="wrap"><article class="post">{rich(x["blocks"])}</article><p style="margin-top:32px"><a class="go" href="/content/">More from Soapbox.</a></p></div></section>
{closer()}'''
        t = x["title"] + " | Yoodle Soapbox"
        if len(t) > 68: t = x["title"][:60].rsplit(" ", 1)[0] + " | Yoodle"
        page(f'/content/{x["slug"]}/', t, dsc, body, [crumb_schema(its), {"@type": "BlogPosting", "headline": x["title"], "datePublished": x["date"], "author": {"@id": DOMAIN + "/#org"}, "publisher": {"@id": DOMAIN + "/#org"}, "mainEntityOfPage": DOMAIN + f'/content/{x["slug"]}/'}])

def accessibility():
    faq = [("What is the ADA Title II website compliance deadline?", "April 26, 2027 for state and local governments serving 50,000 people or more, and April 26, 2028 for smaller governments and special districts. The Department of Justice extended both dates by one year in April 2026. The standard is WCAG 2.1 Level AA."),
           ("Does the ADA web rule apply to colleges and universities?", "Public colleges and universities are covered by ADA Title II and the WCAG 2.1 AA rule. Private institutions fall under ADA Title III and, if they take federal funds, Section 504."),
           ("Can an automated scan make my website compliant?", "No. A scan finds a large share of issues, but not all. Conformance needs manual testing too. Our fix includes the manual checks and a retest."),
           ("Do you use an accessibility overlay or plugin widget?", "No. We fix the site's own code, templates and content."),
           ("Which platforms do you work with?", "Any. WordPress, Drupal, Modern Campus, static HTML and hosted builders all go through the same steps.")]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Websites that work for everyone.</p><h1>ADA website compliance.<span class="r">Before the deadline.</span></h1>
<div class="herogrid"><div><h2 style="font-size:clamp(1.6rem,3vw,2.4rem);margin-bottom:18px" id="scan">Get your free report.</h2>{form("scan-request", SCAN_FIELDS, "Send my free report")}
<p class="small" style="margin-top:12px">Free. Any website, any platform. A person reviews every report before it reaches you.</p></div>
<p class="lede" style="margin:0">Tell us your web address. We test it against WCAG 2.1 AA and send you what passes and what fails. Then we fix it in your site's own code.</p></div></div></section>
<section class="dark" style="padding:clamp(48px,7vw,96px) 0"><div class="wrap two" style="align-items:end"><p class="big" style="font-size:clamp(3.4rem,10vw,8rem);margin:0">April 26, 2027.</p>
<p class="lede">The ADA Title II web deadline for larger governments and most public colleges. Smaller governments and special districts have until April 26, 2028.</p></div></section>
<section><div class="wrap"><h2>Approach.</h2><ol class="rows">
<li><span class="idx" aria-hidden="true">01</span><h3>Send your URL.</h3><p>We read your sitemap, test your pages against WCAG 2.1 AA and note your platform and page templates.</p></li>
<li><span class="idx" aria-hidden="true">02</span><h3>Read your report.</h3><p>What passes, what fails, where it is and who it affects, in plain language.</p></li>
<li><span class="idx" aria-hidden="true">03</span><h3>We fix it.</h3><p>In your code and content. No overlay, no widget. Fixes start at $1,500 for a site under 100 pages. Larger sites are priced on the report, before any work begins.</p></li>
<li><span class="idx" aria-hidden="true">04</span><h3>Retest and certify.</h3><p>Manual checks, a retest and a conformance report you can show your board or counsel.</p></li></ol></div></section>
<section class="tight"><div class="wrap two"><h2>Proof.</h2><div><p class="lede">SWIFT Education Center, University of Kansas. Audited, fixed, retested and certified in fall 2026.</p>
<p><a class="go" href="/work/swift-education-center/">See the project.</a></p></div></div></section>
<section class="tight"><div class="wrap two"><h2>Questions.</h2><div>{faq_block(faq)}<p class="small" style="margin-top:20px">Sources: U.S. Department of Justice interim final rule, <a href="https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web">Federal Register, April 20, 2026</a>. General information, not legal advice.</p></div></div></section>
{closer(b=("See our web work.", "Live sites for colleges, courts and agencies.", "/work/", "See the work."))}'''
    its = [("/", "Home"), ("", "ADA website compliance")]
    page("/accessibility/", "ADA Website Compliance and WCAG 2.1 AA Fixes | Yoodle",
         "Free WCAG 2.1 AA website report. Yoodle audits, fixes your site's own code, retests and certifies ahead of the April 26, 2027 ADA Title II deadline.", body,
         [crumb_schema(its), faq_schema(faq), {"@type": "Service", "name": "ADA website compliance and WCAG 2.1 AA remediation", "provider": {"@id": DOMAIN + "/#org"}, "areaServed": "US"}], h_nopop=True)

def contact():
    f = [("name", "What's your name?", "text", True, "name"), ("email", "And your email address?", "email", True, "email"),
         ("organization", "Where do you work?", "text", True, "organization"), ("role", "What's your role there?", "text", False, "organization-title"),
         ("website", "Your website", "text", False, "url"),
         ("help", "What can we help with?", ("checks", ["Brand", "Marketing", "Technology", "Fractional CMO", "ADA compliance", "Not sure yet"]), False, ""),
         ("budget", "What's the budget?", ("select", ["Under $25,000", "$25,000 to $50,000", "$50,000 to $100,000", "$100,000 to $250,000", "More than $250,000", "Not set yet"]), False, ""),
         ("timeline", "When does it need to be live?", ("select", ["Within 30 days", "One to three months", "Three to six months", "Six months or more", "No fixed date"]), False, ""),
         ("message", "What's the challenge?", "textarea", True, ""),
         ("source", "How did you hear about us?", "text", False, "")]
    body = f'''<section class="hero"><div class="wrap"><p class="eyebrow">Your next chapter starts with a conversation.</p><h1>What&rsquo;s next for you?<span class="r">Bring the challenge.</span></h1>
<div class="herogrid" style="align-items:start">{form("contact", f, "Send")}
<div><p class="lede">We&rsquo;ll bring the experience, the curiosity, and the people to make it happen. Tell us what you&rsquo;re facing and you&rsquo;ll hear from a person within one business day.</p><p>Or write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><p>Yoodle LLC<br>Kansas City, Missouri</p></div></div></div></section>'''
    page("/contact/", "Contact Yoodle | Start a Brand, Technology or Marketing Project", "Contact Yoodle, the content experience agency in Kansas City. Bring the challenge and hear from a person within one business day.", body, [crumb_schema([("/", "Home"), ("", "Contact")])], h_nopop=True)
    page("/thanks/", "Thank You | Yoodle", "Your message reached Yoodle. We reply within one business day.",
         '<section class="hero"><div class="wrap"><h1>Got it.<span class="r">Thank you.</span></h1><p class="lede" style="margin-top:32px">We reply within one business day.</p><p><a class="go" href="/work/">See the work while you wait.</a></p></div></section>', h_nopop=True, index=False)
    page("/privacy/", "Privacy Policy | Yoodle", "How Yoodle collects, uses and protects information submitted through yoodle.com.",
         f'<section class="hero"><div class="wrap"><h1 class="md">Privacy.</h1><div style="max-width:44em;margin-top:32px"><p>Yoodle LLC collects the information you send through forms on this site: your name, email, organization, website address and message. We use it to reply to you and to prepare any report you asked for. We do not sell it.</p><p>Form submissions are stored by our hosting provider, Netlify. To ask what we hold about you or to have it removed, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><p>We use Google Analytics to count visits and see which pages people read. It sets cookies and records information such as your approximate location, device and the pages you view. It does not tell us who you are. You can block it with your browser settings or with Google&rsquo;s opt-out add-on.</p></div></div></section>', [], h_nopop=True)
    page("/404.html", "Page Not Found | Yoodle", "That page is not here. Find Yoodle's work, services and contact details.",
         '<section class="hero"><div class="wrap"><h1>Page not found.</h1><p class="lede" style="margin-top:32px">That page moved or never existed.</p><p><a class="go" href="/work/">See the work.</a> <a class="go" href="/">Go home.</a></p></div></section>', h_nopop=True, index=False)

def assets():
    os.makedirs(os.path.join(OUT, "css"), exist_ok=True); os.makedirs(os.path.join(OUT, "js"), exist_ok=True); os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
    css = CSS.replace('url("/fonts/', 'url("../fonts/') if PREVIEW else CSS
    open(os.path.join(OUT, "css/site.css"), "w").write(css)
    open(os.path.join(OUT, "js/site.js"), "w").write(JS)
    nm = os.path.join(ROOT, "node_modules/@fontsource-variable")
    shutil.copy(f"{nm}/inter/files/inter-latin-wght-normal.woff2", os.path.join(OUT, "fonts/inter.woff2"))
    shutil.copy(f"{nm}/bricolage-grotesque/files/bricolage-grotesque-latin-opsz-normal.woff2", os.path.join(OUT, "fonts/bricolage-grotesque.woff2"))
    if os.path.isdir(os.path.join(ROOT, "assets/img")): shutil.copytree(os.path.join(ROOT, "assets/img"), os.path.join(OUT, "img"), dirs_exist_ok=True)
    if PREVIEW: return
    for f in ("yoodle-review.js", "yoodle-review-form.html", "yoodle-resolved.json"): shutil.copy(os.path.join(ROOT, "tools/review", f), os.path.join(OUT, f))
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(("User-agent: *\nDisallow: /\n" if TEST_BUILD else "User-agent: *\nAllow: /\n") + f"Sitemap: {DOMAIN}/sitemap.xml\n")
    llms = ["# Yoodle", "", "> Yoodle is the content experience agency, working across brand, technology and marketing. Built on experience, made for what's next: brands, digital experiences and marketing for ambitious organizations in higher education, government, nonprofits and business. Founded 2007, Kansas City, Missouri. Contact: " + EMAIL, "",
            "## Services"] + [f"- [{v['name']}]({DOMAIN}/services/{k}/): {v['lede']}" for k, v in SERVICES.items()] + [f"- [ADA website compliance]({DOMAIN}/accessibility/): WCAG 2.1 AA audit, fixes, retest and conformance report.", f"- [Fractional marketing leadership]({DOMAIN}/experience/): six-month senior marketing leadership contracts.", "", "## Work"] + \
           [f"- [{p['name']}]({DOMAIN}/work/{p['slug']}/): {SECTORS[p['sector']][0]} {p['kind'].lower()}" + (f", live at {p['url']}" if p['url'] else "") for p in P]
    open(os.path.join(OUT, "llms.txt"), "w").write("\n".join(llms) + "\n")
    old = ["about", "work/work-by-services", "blog", "careers", "careers/*", "vpat", "dir", "shop", "cart", "checkout", "my-account", "skill-up", "skill-up/*", "workforce-training", "workforce-training/*", "contentum", "contentum/*", "project/*"]
    dest = {"about": "/services/", "blog": "/content/", "vpat": "/accessibility/", "work/work-by-services": "/work/", "project/*": "/work/"}
    code = 302 if TEST_BUILD else 301
    spec = f"/services/interactive/  /services/technology/  {code}\n/work/rio-hondo-college-video/  /work/rio-hondo-college/  {code}\n" + "".join(f"/project/{o['old']}/  /work/{o['slug']}/  {code}\n" for o in OLDSITE["projects"]) + "".join(f"/{x['old']}/  /content/{x['slug']}/  {code}\n" for x in POSTS) + "".join(f"/content/{x['slug']}/  {GONE[x['slug']]}  {code}\n/{x['old']}/  {GONE[x['slug']]}  {code}\n" for x in OLDSITE["posts"] if x["slug"] in GONE)
    open(os.path.join(OUT, "_redirects"), "w").write(spec + "".join(f"/{o}  {dest.get(o, '/')}  {code}\n" for o in old))
    open(os.path.join(OUT, "netlify.toml"), "w").write('[build]\n  publish = "."\n  command = ""\n')

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
home(); work()
for i, p in enumerate(P): project(i, p)
services(); experience(); bridal(); content(); posts(); accessibility(); contact(); assets()
print(f"{len(PAGES)} indexable pages -> {OUT}")
