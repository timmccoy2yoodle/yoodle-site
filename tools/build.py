#!/usr/bin/env python3
"""yoodle.com generator. python3 tools/build.py [--preview]
site/    = real paths for Netlify.   preview/ = flat files with relative links for the review artifact."""
import os, re, sys, json, shutil, html
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = "--preview" in sys.argv
OUT = os.path.join(ROOT, "preview" if PREVIEW else "site")
TEST_BUILD = True
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
POSTS = OLDSITE["posts"]
def cover_img(p):
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
@font-face{font-family:"Inter Tight";src:url("/fonts/inter-tight.woff2") format("woff2");font-weight:100 900;font-display:swap}
:root{--bg:#F7F4EE;--ink:#111110;--mute:#55524c;--line:#11111022;--acc:#2c2a6f;--acc-t:#2c2a6f;--acc-l:#b9b6f5;--white:#fff;--amber:#ffe9a8;--amber-t:#4d3400;--max:1320px}
*{box-sizing:border-box}
html{scroll-padding-top:80px;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;font-family:"Inter",system-ui,sans-serif;font-size:18px;line-height:1.5;color:var(--ink);background:var(--bg);overflow-wrap:anywhere;-webkit-font-smoothing:antialiased}
h1,h2,h3,.big,.brand,.idx{font-family:"Inter Tight","Inter",system-ui,sans-serif;font-weight:600;letter-spacing:-.035em;line-height:.98;margin:0}
h1{font-size:clamp(3rem,10.5vw,9.5rem);letter-spacing:-.05em;line-height:.92}
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
.menu{display:none;min-height:44px;padding:0 16px;border:1.5px solid var(--ink);border-radius:999px;background:none;font:inherit;font-weight:600;color:inherit;cursor:pointer}
@media (max-width:760px){
 .js .menu{display:inline-flex;align-items:center}
 .js nav.main{display:none;position:absolute;left:0;right:0;top:100%;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 24px 20px}
 .js nav.main.open{display:block}
 nav.main ul{flex-direction:column;align-items:stretch}
 nav.main a{font-size:1.3rem;min-height:52px;padding:0}
 nav.main a.talk{justify-content:center;margin:8px 0 0}
 html:not(.js) header.site .wrap{flex-wrap:wrap;padding-bottom:8px}
}
.go{display:inline-flex;align-items:center;gap:.4em;min-height:44px;font-weight:500;text-decoration:underline}
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
.mq{overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:22px 0}
.track{display:flex;width:max-content;animation:mq 70s linear infinite}
.track ul{display:flex;list-style:none;margin:0;padding:0}
.track li{font-family:"Inter Tight",sans-serif;font-weight:600;font-size:clamp(1.3rem,2.4vw,2rem);letter-spacing:-.02em;padding:0 28px;white-space:nowrap}
.track li::after{content:"\00B7";margin-left:56px;color:var(--acc)}
.mq.paused .track{animation-play-state:paused}
@keyframes mq{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.track{animation:none;width:auto;flex-wrap:wrap}.track ul{flex-wrap:wrap}.track ul[aria-hidden]{display:none}.track li{white-space:normal}.mqbtn{display:none}}
.mqbtn,.linkbtn{margin-top:12px;background:none;border:0;font:inherit;font-size:.95rem;text-decoration:underline;min-height:44px;cursor:pointer;color:inherit;padding:0}
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
@media (max-width:760px){.rows>li{grid-template-columns:48px minmax(0,1fr)}.rows>li p{grid-column:2}}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:32px 0 0}
.chipb{min-height:44px;padding:0 18px;border:1.5px solid var(--ink);border-radius:999px;background:none;font:inherit;font-weight:600;color:var(--ink);cursor:pointer}
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
.cover .n{font-family:"Inter Tight",sans-serif;font-weight:600;letter-spacing:-.04em;line-height:.95;font-size:clamp(1.7rem,3vw,2.6rem)}
.cover.lg .n{font-size:clamp(2rem,6.4vw,5.6rem)}
.cover::after{content:"";position:absolute;right:-12%;bottom:-38%;width:62%;aspect-ratio:1;border-radius:50%;border:1.5px solid #ffffff40}
.cover::before{content:"";position:absolute;right:6%;bottom:-52%;width:62%;aspect-ratio:1;border-radius:50%;border:1.5px solid #ffffff26}
.card h3{font-size:1.25rem;margin:14px 0 2px;letter-spacing:-.02em}
.card p{margin:0}
.facts{margin:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 32px}
.facts div{border-top:1.5px solid var(--ink);padding:14px 0 22px;min-width:0}
.facts dt{font-size:.9rem;color:var(--mute)}
.facts dd{margin:4px 0 0;font-weight:600}
@media (max-width:760px){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
.sect{list-style:none;padding:0;margin:14px 0 0}
.sect li{padding:10px 0;border-top:1px solid var(--line)}
.names{columns:3;list-style:none;padding:0;margin:28px 0 0}
.names li{padding:8px 0;border-top:1px solid var(--line);break-inside:avoid}
@media (max-width:760px){.names{columns:1}}
details{border-top:1px solid var(--line)}
details:last-of-type{border-bottom:1px solid var(--line)}
summary{cursor:pointer;font-family:"Inter Tight",sans-serif;font-weight:600;font-size:clamp(1.2rem,2.2vw,1.6rem);letter-spacing:-.02em;padding:22px 0;min-height:44px;list-style:none;display:flex;justify-content:space-between;gap:16px}
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
.hp{position:absolute;left:-9999px}
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
body.test{padding-bottom:64px}
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
.plist a{font-family:"Inter Tight",sans-serif;font-weight:600;font-size:clamp(1.2rem,2.2vw,1.6rem);letter-spacing:-.02em;text-decoration:none;display:inline-flex;min-height:44px;align-items:center}
.plist a:hover{text-decoration:underline}
@media (max-width:620px){.plist li{grid-template-columns:1fr;gap:0}}

/* ---- motion layer: only when JS is on and the visitor has not asked for reduced motion */
header.site{transition:transform .45s cubic-bezier(.2,.7,.2,1),background-color .5s,color .5s,border-color .5s}
header.site.hide{transform:translateY(-101%)}
html[data-band=dark] header.site{background:var(--ink);color:var(--bg);border-color:#f7f4ee33}
html[data-band=dark] header.site nav.main a.talk{background:var(--bg);color:var(--ink)}
html[data-band=dark] header.site .menu{border-color:var(--bg)}
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
if(mqb)mqb.addEventListener('click',function(){var p=mq.classList.toggle('paused');mqb.setAttribute('aria-pressed',p);mqb.textContent=p?'Resume scrolling names':'Pause scrolling names'});
var fb=d.querySelectorAll('[data-f]'),cards=d.querySelectorAll('[data-s]'),cnt=d.getElementById('count');
function setF(k){var n=0;cards.forEach(function(c){var on=k==='all'||c.getAttribute('data-s')===k;c.hidden=!on;if(on)n++});fb.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-f')===k)});if(cnt)cnt.textContent=n+' projects shown';}
fb.forEach(function(b){b.addEventListener('click',function(){setF(b.getAttribute('data-f'));if(history.replaceState)try{history.replaceState(null,'','#'+b.getAttribute('data-f'))}catch(_){}})});
if(fb.length&&location.hash){var k=location.hash.slice(1);if(d.querySelector('[data-f="'+k+'"]'))setF(k)}
var live=/(^|\.)yoodle\.com$|\.netlify\.app$/.test(location.hostname);
d.querySelectorAll('form[data-netlify]').forEach(function(f){f.addEventListener('submit',function(ev){
 var s=f.querySelector('.status');
 if(!f.checkValidity()){ev.preventDefault();s.classList.add('show');s.textContent='Please fill in every required field with a valid value.';var bad=f.querySelector(':invalid');if(bad)bad.focus();return}
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
 var sel='.lede,.tag,.crumbs,.grid>li,.col,.facts>div,.sect>li,.names>li,details,.ends>div>*,form.f,.filters,.pn,.herogrid>*,.hero .btn,.mq,section p:not(.lede):not(.small)';
 d.querySelectorAll('main '+sel).forEach(function(x){if(x.closest('.rv,dialog,.rows')||x.classList.contains('rh'))return;x.classList.add('rv')});
 d.querySelectorAll('main .rows>li').forEach(function(x){x.classList.add('rw')});
 d.querySelectorAll('.grid,.cols,.rows,.facts,.sect,.names,.ends>div').forEach(function(p){[].forEach.call(p.children,function(c,i){c.style.setProperty('--i',Math.min(i%6,5))})});
 var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
 d.querySelectorAll('.rv,.rh,.rw').forEach(function(x){io.observe(x)});
 darks.forEach(function(s){if(!s.querySelector('.ends'))s.classList.add('band')});
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

NAV = [("/work/", "Work"), ("/services/", "Services"), ("/content/", "Content"), ("/experience/", "Experience")]

def header(cur):
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if cur.startswith(h) else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to main content</a>
{'<aside class="testbar" aria-label="Test build notice">Test build for Tim. Amber tags mark facts to confirm before launch.</aside>' if TEST_BUILD else ''}
<header class="site"><div class="wrap">
<a class="brand" href="/" aria-label="Yoodle home">yoodle<span>.</span></a>
<button class="menu" id="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="main" id="nav" aria-label="Main"><ul>{li}<li><a class="talk" href="/contact/">Contact</a></li></ul></nav>
</div></header>'''

def footer():
    return f'''<footer><div class="wrap"><div class="fg">
<div><p><strong style="color:#fff;font-size:1.3rem">yoodle.</strong></p><p>The content experience agency. Brand, web, growth and content for organizations that answer to the public. Since 2007.</p><p>Kansas City, Missouri<br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h2>Work</h2><ul><li><a href="/work/#higher-ed">Higher education</a></li><li><a href="/work/#government">Government</a></li><li><a href="/work/#nonprofit">Nonprofit</a></li><li><a href="/work/#business">Small business</a></li><li><a href="/work/#content">Podcasts</a></li></ul></div>
<div><h2>Services</h2><ul>{"".join(f'<li><a href="/services/{k}/">{v["name"]}</a></li>' for k, v in SERVICES.items())}<li><a href="/accessibility/">ADA compliance</a></li><li><a href="/experience/">Fractional leadership</a></li></ul></div>
<div><h2>Yoodle</h2><ul><li><a href="/content/">Content</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="https://www.linkedin.com/company/yoodle">LinkedIn</a></li></ul></div>
</div><p style="margin-top:32px">&copy; {date.today().year} Yoodle LLC. Yoodle&reg; is a registered trademark.</p></div></footer>'''

PICK = '''<aside class="pick" aria-label="Accent color options, test build only"><span>Accent:</span><button type="button" aria-pressed="true" data-a="#2c2a6f" data-t="#2c2a6f" data-l="#b9b6f5"><i style="background:#2c2a6f"></i>Deep purple</button><button type="button" aria-pressed="false" data-a="#783a92" data-t="#783a92" data-l="#d9b3ea"><i style="background:#783a92"></i>Plum</button><button type="button" aria-pressed="false" data-a="#953c92" data-t="#953c92" data-l="#e8b0e5"><i style="background:#953c92"></i>Magenta</button><button type="button" aria-pressed="false" data-a="#c23c7c" data-t="#c03b7b" data-l="#f4aecd"><i style="background:#c23c7c"></i>Berry</button><button type="button" aria-pressed="false" data-a="#d5466d" data-t="#cc2e59" data-l="#f8b1c2"><i style="background:#d5466d"></i>Rose</button></aside>'''

def field(id, label, type="text", req=True, ac="", pre=""):
    r = " required" if req else ""
    a = f' autocomplete="{ac}"' if ac else ""
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

def page(path, title, desc, body, schema=None, h_nopop=False, index=True):
    canon = DOMAIN + path
    crumbs = []
    parts = [x for x in path.strip("/").split("/") if x]
    graph = [{"@type": "Organization", "@id": DOMAIN + "/#org", "name": "Yoodle", "legalName": "Yoodle LLC", "url": DOMAIN + "/", "email": EMAIL,
              "foundingDate": "2007", "slogan": "The content experience agency",
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
<link rel="preload" href="/fonts/inter-tight.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css">
</head>
<body{' class="test"' if TEST_BUILD else ''}>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
{'' if h_nopop else LEAD}
{PICK if TEST_BUILD else ''}
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
<script src="/js/site.js" defer></script>
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
    if ci: return f'<div class="cover ph{" lg" if lg else ""}"><img src="{ci["src"]}" alt="{e(p["name"])} project by Yoodle" width="{ci["w"]}" height="{ci["h"]}"{"" if lg else " loading=\"lazy\""}></div>'
    lab, col = SECTORS[p["sector"]]
    host = re.sub(r"^https?://(www\.)?|/$", "", p["url"]) if p["url"] else p["kind"]
    return f'<div class="cover{" lg" if lg else ""}" style="background:{col}"><div class="k"><span>{lab}</span><span>{e(host)}</span></div><div class="n">{e(p["name"])}</div></div>'

def card(p):
    lab = SECTORS[p["sector"]][0]
    sub = p["place"] or p["kind"]
    if p["kind"] == "Project": sub = ", ".join(OLD[p["slug"]]["tags"]) or "Brand and web"; return f'<li data-s="{p["sector"]}"><a class="card" href="/work/{p["slug"]}/">{cover(p)}<h3>{e(p["name"])}</h3><p class="small">{e(sub)}</p></a></li>'
    return f'<li data-s="{p["sector"]}"><a class="card" href="/work/{p["slug"]}/">{cover(p)}<h3>{e(p["name"])}</h3><p class="small">{e(p["kind"])}{" · " + e(sub) if sub != p["kind"] else ""}</p></a></li>'

def closer(a=("Start a project.", "Tell us what needs to get done. We reply within one business day.", "/contact/", "Contact us."),
           b=("Check your site.", "Get a free WCAG 2.1 AA accessibility report.", "/accessibility/", "Get my report.")):
    return f'''<section class="dark" style="padding:0" aria-label="Next steps"><div class="wrap ends">
<div><h2>{a[0]}</h2><p class="lede" style="margin:20px 0">{a[1]}</p><a class="go" href="{a[2]}">{a[3]}</a></div>
<div><h2>{b[0]}</h2><p class="lede" style="margin:20px 0">{b[1]}</p><a class="go" href="{b[2]}">{b[3]}</a></div></div></section>'''

def marquee():
    lis = "".join(f"<li>{e(c)}</li>" for c in CLIENTS)
    return f'''<div class="wrap"><p class="small" style="margin-bottom:10px">Brand, web and marketing work since 2007 for</p></div>
<div class="mq" id="mq"><div class="track"><ul>{lis}</ul><ul aria-hidden="true">{lis}</ul></div></div>
<div class="wrap"><button class="mqbtn" id="mqbtn" type="button" aria-pressed="false">Pause scrolling names</button> {confirm("client logos replace these names once the logo files are collected")}</div>'''

# ------------------------------------------------------------------ pages
def home():
    feat = [p for p in P if p["slug"] in ("nevada-state-university", "kansas-judicial-branch", "ut-austin-extended-campus", "kc-streetcar", "variety-kc", "fsu-career-center")]
    svc = "".join(f'<li><span class="idx" aria-hidden="true">0{i+1}</span><h3><a href="/services/{k}/">{v["name"]}. {v["verdict"]}</a></h3><p>{e(v["lede"])}</p></li>' for i, (k, v) in enumerate(SERVICES.items()))
    body = f'''<section class="hero"><div class="wrap">
<p class="tag">Yoodle. The content experience agency.</p>
<h1>Brand, web and marketing.<span class="r">Done.</span></h1>
<div class="herogrid"><p class="lede" style="margin:0">Colleges, public agencies and nonprofits bring us the work that has to get finished. We scope it, build it and launch it, on any platform.</p>
<p style="margin:0"><a class="btn" href="/work/">See the work</a> &nbsp; <a class="go" href="/contact/">Start a project.</a></p></div>
</div></section>
{marquee()}
<section><div class="wrap two"><h2>We get it done.</h2><div>
<p class="lede">Most organizations do not lack ideas. They lack the hands to finish them. Yoodle is a senior, distributed team with nearly every skill a marketing department needs.</p>
<p>Give us the outcome. We write the scope, do the work and hand you something that runs: a brand your staff can use, a website that passes an accessibility audit, a campaign you can measure, a show that publishes on time. If you want to run it yourselves afterward, we train your team to do it.</p>
<p><a class="go" href="/services/">See what we do.</a></p></div></div></section>
<section class="dark"><div class="wrap"><h2>Services.</h2><ol class="rows">{svc}
<li><span class="idx" aria-hidden="true">05</span><h3><a href="/experience/">Experience. Led.</a></h3><p>Senior marketing leadership on a six-month contract, for teams that need a head of marketing before they can hire one.</p></li></ol></div></section>
<section><div class="wrap"><div class="two" style="align-items:end"><h2>Work.<span class="r">Launched.</span></h2><p class="lede">{len(P)} projects since 2007: live websites, brands and campaigns for higher education, government, nonprofits and business, plus the podcasts we produce.</p></div>
<ul class="grid">{"".join(card(p) for p in feat)}</ul><p style="margin-top:28px"><a class="go" href="/work/">See all the work.</a></p></div></section>
<section class="dark"><div class="wrap"><h2>Who we work for.</h2><div class="cols">
<div class="col"><h3>Higher education.</h3><p>Colleges, universities and the centers inside them. Enrollment sites, program finders, accessibility and content.</p><a class="go" href="/work/#higher-ed">Higher ed work.</a></div>
<div class="col"><h3>Government.</h3><p>Courts, commissions, transit and regional agencies. Direct, or as a teaming partner to a prime contractor.</p><a class="go" href="/work/#government">Government work.</a></div>
<div class="col"><h3>Nonprofit and business.</h3><p>Charities, arts organizations and owner-run companies that need a full marketing team without hiring one.</p><a class="go" href="/work/#nonprofit">Nonprofit work.</a></div>
</div></div></section>
<section><div class="wrap two"><h2>ADA website compliance.<span class="r">Fixed.</span></h2><div>
<p class="lede">Public colleges and larger governments must meet WCAG 2.1 AA by April 26, 2027. We audit, fix the site's own code, retest and certify.</p>
<p><a class="btn" href="/accessibility/">Get a free report</a></p></div></div></section>
{closer()}'''
    page("/", "Yoodle | Brand, Web and Marketing for Higher Ed and Government",
         "Yoodle is the content experience agency. Since 2007 we have scoped, built and launched brands, websites and campaigns for colleges, agencies and nonprofits.", body,
         [{"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Yoodle", "publisher": {"@id": DOMAIN + "/#org"}}])

def work():
    fl = '<button class="chipb" type="button" data-f="all" aria-pressed="true">All</button>' + "".join(f'<button class="chipb" type="button" data-f="{k}" aria-pressed="false">{v[0]}</button>' for k, v in SECTORS.items())
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Work</p><h1>The work.<span class="r">Launched.</span></h1>
<p class="lede" style="margin-top:32px">Websites, brands, campaigns and shows Yoodle has built since 2007. Many of the websites are live, so you can open them and judge for yourself.</p>
<div class="filters" role="group" aria-label="Filter work by sector">{fl}</div><p class="small" id="count" role="status" style="margin:14px 0 0">{len(P)} projects shown</p>
<ul class="grid" id="grid">{"".join(card(p) for p in P)}</ul></div></section>
{closer()}'''
    items = [("/", "Home"), ("", "Work")]
    page("/work/", "Our Work: Higher Education, Government and Nonprofit Websites | Yoodle",
         f"See {len(P)} projects by Yoodle: live websites for colleges, government agencies, nonprofits and small businesses, plus podcasts and video.", body,
         [crumb_schema(items), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{DOMAIN}/work/{p["slug"]}/', "name": p["name"]} for i, p in enumerate(P)]}])

VERDICT = {"Website": "Launched.", "Podcast": "Produced.", "Video and content": "Produced.", "Project": "Delivered."}
def project(i, p):
    lab = SECTORS[p["sector"]][0]
    prev, nxt = P[i - 1], P[(i + 1) % len(P)]
    host = re.sub(r"^https?://(www\.)?|/$", "", p["url"])
    facts = [("Client", e(p["name"])), ("Sector", lab), ("Type", p["kind"])]
    if p["platform"]: facts.append(("Platform", e(p["platform"])))
    elif p["kind"] == "Website": facts.append(("Platform", confirm("platform")))
    if p["place"]: facts.append(("Location", e(p["place"])))
    if p["url"]: facts.append(("Live site", f'<a href="{p["url"]}">{host}</a>'))
    about = f'<p class="lede">{e(p["about"])}</p>' if p["about"] else f'<p class="lede">{e(p["name"])} is a {p["kind"].lower()} produced by Yoodle.</p>'
    need = {"Website": "Yoodle's scope (strategy, design, build, migration, support), launch year, results and a client quote",
            "Podcast": "exact show name, client, host, episode count, where to listen, cover art and Yoodle's role",
            "Video and content": "project details from the Drive client folder and the Vimeo links",
            "Project": "year, and whether to keep this project on the new site"}[p["kind"]]
    o = OLD.get(p["slug"])
    story = gal = ""
    if o:
        facts.insert(3, ("Services", e(", ".join(o["tags"]) or "Brand and web")))
        blk = o["blocks"] if p["kind"] != "Project" else [x for x in o["blocks"] if x[1] != p["about"]]
        if blk: story = f'<section class="tight"><div class="wrap two"><h2>{"The work." if p["kind"] == "Project" else "The story."}</h2><div>{rich(blk)}</div></div></section>'
        rest = o["imgs"][1:]
        if rest: gal = '<section class="tight"><div class="wrap"><ul class="gal">' + "".join(f'<li><img src="{g["src"]}" alt="{e(p["name"])}: work by Yoodle, image {k + 1}" width="{g["w"]}" height="{g["h"]}" loading="lazy"></li>' for k, g in enumerate(rest)) + '</ul></div></section>'
    feats = f'<section class="tight"><div class="wrap two"><h2>On the site.</h2><ul class="sect">{"".join(f"<li>{e(f)}</li>" for f in p["features"])}</ul></div></section>' if p["features"] else ""
    if p["kind"] != "Website" and p["features"]:
        feats = feats.replace("On the site.", "What we made.")
    visit = f'<p><a class="btn" href="{p["url"]}">Visit {host}</a></p>' if p["url"] else ""
    body = f'''<section class="hero"><div class="wrap">{crumbs([("/", "Home"), ("/work/", "Work"), ("", e(p["name"]))])}
<h1 class="md">{e(p["name"])}.<span class="r">{VERDICT[p["kind"]]}</span></h1>
<div style="margin-top:clamp(28px,5vw,56px)">{cover(p, lg=True)}</div>
{"" if cover_img(p) else '<p class="small" style="margin-top:10px">' + confirm("real screenshots of the live site replace this cover" if p["url"] else "images replace this cover once the rest of the backup is brought over") + "</p>"}
</div></section>
<section class="tight"><div class="wrap"><dl class="facts">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)}</dl></div></section>
<section class="tight"><div class="wrap two"><h2>The project.</h2><div>{about}<p>{confirm(need)}</p>{visit}</div></div></section>
{feats}
{story}
{gal}
<section class="tight"><div class="wrap"><nav class="pn" aria-label="More work"><a href="/work/{prev["slug"]}/"><span class="small">Previous</span><br><strong>{e(prev["name"])}</strong></a><a class="nx" href="/work/{nxt["slug"]}/"><span class="small">Next</span><br><strong>{e(nxt["name"])}</strong></a></nav></div></section>
{closer(a=("Need one like it?", "Tell us what has to get done.", "/contact/", "Start a project."))}'''
    t = {"Website": f'{p["name"]} Website | {lab} Web Design by Yoodle', "Podcast": f'{p["name"]} | Podcast Production by Yoodle', "Video and content": f'{p["name"]} | Video Production by Yoodle', "Project": f'{p["name"]} | {lab} Brand and Web Work by Yoodle'}[p["kind"]]
    if len(t) > 68: t = f'{p["name"]} | {"Web Design" if p["kind"] == "Website" else "Work"} by Yoodle'
    d = (p["about"] or f'{p["name"]}, a {p["kind"].lower()} produced by Yoodle, the content experience agency.')
    d = (f'{p["name"]}: ' if p["name"] not in d[:60] else "") + d
    d = d if len(d) <= 158 else d[:155].rsplit(" ", 1)[0] + "..."
    cw = {"@type": "CreativeWork", "name": p["name"], "creator": {"@id": DOMAIN + "/#org"}, "about": lab, "genre": p["kind"]}
    if p["url"]: cw["url"] = p["url"]
    page(f'/work/{p["slug"]}/', t, d, body, [crumb_schema([("/", "Home"), ("/work/", "Work"), ("", p["name"])]), cw])

def services():
    rows = "".join(f'<li><span class="idx" aria-hidden="true">0{i+1}</span><h3><a href="/services/{k}/">{v["name"]}. {v["verdict"]}</a></h3><p>{e(v["lede"])} <a href="/services/{k}/">More on {v["name"].lower()}.</a></p></li>' for i, (k, v) in enumerate(SERVICES.items()))
    faq = [("What does Yoodle do?", "Yoodle is a brand, web and marketing agency. We scope, build and launch brands, websites, growth campaigns and content for higher education, government, nonprofits and small businesses."),
           ("Who does Yoodle work with?", "Public colleges and universities, government agencies and commissions, nonprofits and owner-run businesses. We also work as a teaming partner or subcontractor to prime contractors."),
           ("How does a project start?", "With a scope. You tell us the outcome, we write down what will be delivered, when and for how much, and work starts once you approve it.")]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Services</p><h1>Four services.<span class="r">One team.</span></h1>
<p class="lede" style="margin-top:32px">Brand, interactive, growth and content. Buy one, or let us run all four as your marketing department.</p></div></section>
<section class="dark"><div class="wrap"><h2>What we do.</h2><ol class="rows">{rows}</ol></div></section>
<section><div class="wrap"><h2>How we work.</h2><ol class="rows">
<li><span class="idx" aria-hidden="true">01</span><h3>Scope it.</h3><p>One page: the outcome, what we deliver, the date and the price.</p></li>
<li><span class="idx" aria-hidden="true">02</span><h3>Build it.</h3><p>A senior team does the work, fast, with AI for speed and a person accountable for everything that ships.</p></li>
<li><span class="idx" aria-hidden="true">03</span><h3>Launch it.</h3><p>Tested for accessibility, speed and accuracy before it goes out under your name.</p></li>
<li><span class="idx" aria-hidden="true">04</span><h3>Hand it over, or run it.</h3><p>We train your team to own it, or we keep running it. Your choice.</p></li></ol></div></section>
<section class="tight"><div class="wrap two"><h2>Partner with us.</h2><div><p class="lede">Prime contractors and agencies bring Yoodle in for the brand, web, accessibility and content parts of larger public-sector contracts.</p>
<p>We work to your process, your schedule and your reporting. {confirm("certifications and contract vehicles to list here, such as MBE or DBE status")}</p><p><a class="go" href="/contact/">Talk about teaming.</a></p></div></div></section>
<section class="tight"><div class="wrap two"><h2>Questions.</h2><div>{faq_block(faq)}</div></div></section>
{closer()}'''
    items = [("/", "Home"), ("", "Services")]
    page("/services/", "Services: Brand, Web, Growth and Content Marketing | Yoodle",
         "Yoodle's four services: brand, interactive, growth and content. One senior team that scopes, builds and launches marketing for colleges and agencies.", body, [crumb_schema(items), faq_schema(faq)])
    for k, v in SERVICES.items():
        rel = [p for p in P if (k == "content") == (p["sector"] == "content")][:3]
        body = f'''<section class="hero"><div class="wrap">{crumbs([("/", "Home"), ("/services/", "Services"), ("", v["name"])])}
<h1>{v["name"]}.<span class="r">{v["verdict"]}</span></h1><p class="lede" style="margin-top:32px">{e(v["lede"])}</p></div></section>
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
    faq = [("What is fractional marketing leadership?", "A senior marketing leader works inside your organization part time on a fixed contract. You get the strategy, the plan and the management of the work without a full-time executive salary."),
           ("How long is an engagement?", "Six months. The first 90 days are a sprint to diagnose, plan and launch. The following months run and improve the system."),
           ("Who is it for?", "Organizations with real revenue or a real mandate and no senior marketing lead: growing companies, multi-location businesses, nonprofits and public-sector teams between hires.")]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Experience</p><h1>Marketing leadership.<span class="r">Led.</span></h1>
<div class="herogrid"><p class="lede" style="margin:0">A senior marketing leader and the team behind him, inside your organization for six months. For teams that need a head of marketing before they can hire one.</p>
<p style="margin:0"><a class="btn" href="/contact/">Talk to Tim</a></p></div></div></section>
<section class="tight"><div class="wrap two"><h2>Run by an operator.</h2><div><p class="lede">Tim McCoy has led Yoodle since 2007 and is chief marketing officer of a five-store bridal retail group. The systems we bring to clients are ones we run on our own businesses first.</p>
<p>You get the leader and the hands. Strategy comes with a team that can build the brand, the website, the campaigns and the reporting, so the plan does not wait on hiring.</p></div></div></section>
<section class="dark"><div class="wrap"><h2>Six months.</h2><ol class="rows">{"".join(f'<li><span class="idx" aria-hidden="true">0{i+1}</span><h3>{a}.</h3><p>{b}</p></li>' for i, (a, b) in enumerate(steps))}</ol></div></section>
<section><div class="wrap two"><h2>Questions.</h2><div>{faq_block(faq)}</div></div></section>
{closer(a=("Need a leader?", "Tell us where marketing is stuck.", "/contact/", "Start the conversation."))}'''
    its = [("/", "Home"), ("", "Experience")]
    page("/experience/", "Fractional CMO and Marketing Leadership | Yoodle",
         "Fractional CMO and marketing director services from Yoodle. A senior leader and a full team inside your organization on a six-month contract.", body, [crumb_schema(its), faq_schema(faq)])

def content():
    shows = [p for p in P if p["sector"] == "content"]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Content</p><h1>Shows and writing.<span class="r">Published.</span></h1>
<p class="lede" style="margin-top:32px">The podcasts we produce and publish, and Soapbox, the Yoodle blog.</p></div></section>
<section class="tight"><div class="wrap"><h2>Our shows.</h2><ul class="grid">{"".join(card(p) for p in shows)}</ul></div></section>
<section class="dark"><div class="wrap two"><h2>Soapbox.</h2><div><p class="lede">Notes on brand, web, accessibility and AI search for people who answer to the public.</p>
<p>{confirm("these posts came over as written, 2019 to 2023; tell me which to retire")}</p></div></div>
<div class="wrap"><ul class="plist">{"".join(f'<li><span class="small">{x["date"][:7]}</span><a href="/content/{x["slug"]}/">{e(x["title"])}</a></li>' for x in POSTS)}</ul></div></section>
{closer(a=("Have a show in mind?", "We plan it, produce it and publish it.", "/services/content/", "See content services."))}'''
    its = [("/", "Home"), ("", "Content")]
    page("/content/", "Content: Podcasts and the Soapbox Blog | Yoodle", "Podcasts produced by Yoodle, plus Soapbox, the Yoodle blog on brand, web, accessibility and AI search.", body, [crumb_schema(its)])

def posts():
    for x in POSTS:
        first = next((t for k, t in x["blocks"] if k == "p"), x["title"])
        dsc = first if len(first) <= 158 else first[:155].rsplit(" ", 1)[0] + "..."
        its = [("/", "Home"), ("/content/", "Content"), ("", x["title"])]
        body = f'''<section class="hero"><div class="wrap">{crumbs([("/", "Home"), ("/content/", "Content"), ("", e(x["title"]))])}
<p class="tag">Soapbox · {x["date"]}</p><h1 class="md">{e(x["title"])}</h1></div></section>
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
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Websites that work for everyone.</p><h1>ADA website compliance.<span class="r">Fixed.</span></h1>
<div class="herogrid"><div><h2 style="font-size:clamp(1.6rem,3vw,2.4rem);margin-bottom:18px" id="scan">Get your free report.</h2>{form("scan-request", SCAN_FIELDS, "Send my free report")}
<p class="small" style="margin-top:12px">Free. Any website, any platform. {confirm("instant self-serve scan replaces this form when the scanner goes live")}</p></div>
<p class="lede" style="margin:0">Tell us your web address. We test it against WCAG 2.1 AA and send you what passes and what fails. Then we fix it in your site's own code.</p></div></div></section>
<section class="dark" style="padding:clamp(48px,7vw,96px) 0"><div class="wrap two" style="align-items:end"><p class="big" style="font-size:clamp(3.4rem,10vw,8rem);margin:0">April 26, 2027.</p>
<p class="lede">The ADA Title II web deadline for larger governments and most public colleges. Smaller governments and special districts have until April 26, 2028.</p></div></section>
<section><div class="wrap"><h2>Approach.</h2><ol class="rows">
<li><span class="idx" aria-hidden="true">01</span><h3>Send your URL.</h3><p>We read your sitemap, test your pages against WCAG 2.1 AA and note your platform and page templates.</p></li>
<li><span class="idx" aria-hidden="true">02</span><h3>Read your report.</h3><p>What passes, what fails, where it is and who it affects, in plain language.</p></li>
<li><span class="idx" aria-hidden="true">03</span><h3>We fix it.</h3><p>In your code and content. No overlay, no widget. {confirm("pricing")}</p></li>
<li><span class="idx" aria-hidden="true">04</span><h3>Retest and certify.</h3><p>Manual checks, a retest and a conformance report you can show your board or counsel.</p></li></ol></div></section>
<section class="tight"><div class="wrap two"><h2>Proof.</h2><div><p class="lede">SWIFT Education Center, University of Kansas. Audited, fixed, retested and certified in fall 2026.</p>
<p><a class="go" href="/work/swift-education-center/">See the project.</a> {confirm("KU sign-off to name the project")}</p></div></div></section>
<section class="tight"><div class="wrap two"><h2>Questions.</h2><div>{faq_block(faq)}<p class="small" style="margin-top:20px">Sources: U.S. Department of Justice interim final rule, <a href="https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web">Federal Register, April 20, 2026</a>. General information, not legal advice.</p></div></div></section>
{closer(b=("See our web work.", "Live sites for colleges, courts and agencies.", "/work/", "See the work."))}'''
    its = [("/", "Home"), ("", "ADA website compliance")]
    page("/accessibility/", "ADA Website Compliance and WCAG 2.1 AA Fixes | Yoodle",
         "Free WCAG 2.1 AA website report. Yoodle audits, fixes your site's own code, retests and certifies ahead of the April 26, 2027 ADA Title II deadline.", body,
         [crumb_schema(its), faq_schema(faq), {"@type": "Service", "name": "ADA website compliance and WCAG 2.1 AA remediation", "provider": {"@id": DOMAIN + "/#org"}, "areaServed": "US"}], h_nopop=True)

def contact():
    f = [("name", "Your name", "text", True, "name"), ("email", "Email", "email", True, "email"), ("organization", "Organization", "text", False, "organization"), ("message", "What needs to get done?", "textarea", True, "")]
    body = f'''<section class="hero"><div class="wrap"><p class="tag">Contact</p><h1>Tell us what needs<span class="r">to get done.</span></h1>
<div class="herogrid" style="align-items:start">{form("contact", f, "Send")}
<div><p class="lede">We reply within one business day.</p><p>Or write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><p>Yoodle LLC<br>Kansas City, Missouri</p></div></div></div></section>'''
    page("/contact/", "Contact Yoodle | Start a Brand, Web or Marketing Project", "Contact Yoodle, the content experience agency in Kansas City. Tell us what needs to get done and we reply within one business day.", body, [crumb_schema([("/", "Home"), ("", "Contact")])], h_nopop=True)
    page("/thanks/", "Thank You | Yoodle", "Your message reached Yoodle. We reply within one business day.",
         '<section class="hero"><div class="wrap"><h1>Got it.<span class="r">Thank you.</span></h1><p class="lede" style="margin-top:32px">We reply within one business day.</p><p><a class="go" href="/work/">See the work while you wait.</a></p></div></section>', h_nopop=True, index=False)
    page("/privacy/", "Privacy Policy | Yoodle", "How Yoodle collects, uses and protects information submitted through yoodle.com.",
         f'<section class="hero"><div class="wrap"><h1 class="md">Privacy.</h1><div style="max-width:44em;margin-top:32px"><p>Yoodle LLC collects the information you send through forms on this site: your name, email, organization, website address and message. We use it to reply to you and to prepare any report you asked for. We do not sell it.</p><p>Form submissions are stored by our hosting provider, Netlify. To ask what we hold about you or to have it removed, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><p>{confirm("analytics tools in use and legal review of this policy")}</p></div></div></section>', [], h_nopop=True)
    page("/404.html", "Page Not Found | Yoodle", "That page is not here. Find Yoodle's work, services and contact details.",
         '<section class="hero"><div class="wrap"><h1>Page not found.</h1><p class="lede" style="margin-top:32px">That page moved or never existed.</p><p><a class="go" href="/work/">See the work.</a> <a class="go" href="/">Go home.</a></p></div></section>', h_nopop=True, index=False)

def assets():
    os.makedirs(os.path.join(OUT, "css"), exist_ok=True); os.makedirs(os.path.join(OUT, "js"), exist_ok=True); os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
    css = CSS.replace('url("/fonts/', 'url("../fonts/') if PREVIEW else CSS
    open(os.path.join(OUT, "css/site.css"), "w").write(css)
    open(os.path.join(OUT, "js/site.js"), "w").write(JS)
    nm = os.path.join(ROOT, "node_modules/@fontsource-variable")
    shutil.copy(f"{nm}/inter/files/inter-latin-wght-normal.woff2", os.path.join(OUT, "fonts/inter.woff2"))
    shutil.copy(f"{nm}/inter-tight/files/inter-tight-latin-wght-normal.woff2", os.path.join(OUT, "fonts/inter-tight.woff2"))
    if os.path.isdir(os.path.join(ROOT, "assets/img")): shutil.copytree(os.path.join(ROOT, "assets/img"), os.path.join(OUT, "img"), dirs_exist_ok=True)
    if PREVIEW: return
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(("User-agent: *\nDisallow: /\n" if TEST_BUILD else "User-agent: *\nAllow: /\n") + f"Sitemap: {DOMAIN}/sitemap.xml\n")
    llms = ["# Yoodle", "", "> Yoodle is the content experience agency: brand, web, growth and content for higher education, government, nonprofits and small business. Founded 2007, Kansas City, Missouri. Contact: " + EMAIL, "",
            "## Services"] + [f"- [{v['name']}]({DOMAIN}/services/{k}/): {v['lede']}" for k, v in SERVICES.items()] + [f"- [ADA website compliance]({DOMAIN}/accessibility/): WCAG 2.1 AA audit, fixes, retest and conformance report.", f"- [Fractional marketing leadership]({DOMAIN}/experience/): six-month senior marketing leadership contracts.", "", "## Work"] + \
           [f"- [{p['name']}]({DOMAIN}/work/{p['slug']}/): {SECTORS[p['sector']][0]} {p['kind'].lower()}" + (f", live at {p['url']}" if p['url'] else "") for p in P]
    open(os.path.join(OUT, "llms.txt"), "w").write("\n".join(llms) + "\n")
    old = ["about", "work/work-by-services", "blog", "careers", "careers/*", "vpat", "dir", "shop", "cart", "checkout", "my-account", "skill-up", "skill-up/*", "workforce-training", "workforce-training/*", "contentum", "contentum/*", "project/*"]
    dest = {"about": "/services/", "blog": "/content/", "vpat": "/accessibility/", "work/work-by-services": "/work/", "project/*": "/work/"}
    code = 302 if TEST_BUILD else 301
    spec = "".join(f"/project/{o['old']}/  /work/{o['slug']}/  {code}\n" for o in OLDSITE["projects"]) + "".join(f"/{x['old']}/  /content/{x['slug']}/  {code}\n" for x in POSTS)
    open(os.path.join(OUT, "_redirects"), "w").write(spec + "".join(f"/{o}  {dest.get(o, '/')}  {code}\n" for o in old))
    open(os.path.join(OUT, "netlify.toml"), "w").write('[build]\n  publish = "."\n  command = ""\n')

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
home(); work()
for i, p in enumerate(P): project(i, p)
services(); experience(); content(); posts(); accessibility(); contact(); assets()
print(f"{len(PAGES)} indexable pages -> {OUT}")
