
(function(){
var d=document,h=d.documentElement;h.classList.add('js');
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(_){return null}}
var mb=d.getElementById('menu'),nv=d.getElementById('nav');
if(mb){mb.addEventListener('click',function(){var o=nv.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
 d.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&nv.classList.contains('open')){nv.classList.remove('open');mb.setAttribute('aria-expanded','false');mb.focus()}})}
var mq=d.getElementById('mq'),mqb=d.getElementById('mqbtn');
if(mqb)mqb.addEventListener('click',function(){var p=mq.classList.toggle('paused');mqb.setAttribute('aria-pressed',p);mqb.setAttribute('aria-label',p?'Play scrolling logos':'Pause scrolling logos')});
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
