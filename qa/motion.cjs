const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for(const w of [1440,375]){const p=await b.newPage({viewport:{width:w,height:900}});await p.addInitScript('window.__noPopup=true');
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
for(const u of ['','work/','work/nevada-state-university/','services/','accessibility/']){
 await p.goto('http://localhost:8765/'+u,{waitUntil:'networkidle'});
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);
 for(let y=0;y<H;y+=300){await p.mouse.wheel(0,300);await p.waitForTimeout(60)}
 await p.waitForTimeout(1300);
 const r=await p.evaluate(()=>({left:[...document.querySelectorAll('.rv,.rh,.rw')].filter(e=>!e.classList.contains('in')&&!e.closest('[hidden]')).length,total:document.querySelectorAll('.rv,.rh,.rw').length,ov:document.documentElement.scrollWidth>innerWidth+1,hide:document.querySelector('header.site').classList.contains('hide')}));
 console.log(w,u||'home',JSON.stringify(r));
 if(u===''){await p.evaluate(()=>scrollTo(0,1500));await p.waitForTimeout(900);await p.screenshot({path:`qa/out/motion-${w}-mid.png`});await p.mouse.wheel(0,-200);await p.waitForTimeout(700);await p.screenshot({path:`qa/out/motion-${w}-up.png`})}
}
console.log('errors',errs.length,errs.slice(0,3));await p.close()}
await b.close()})();
