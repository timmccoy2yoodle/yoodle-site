const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:375,height:900}});await p.addInitScript('window.__noPopup=true');
await p.goto('http://localhost:8765/',{waitUntil:'networkidle'});
const H=await p.evaluate(()=>document.documentElement.scrollHeight);
for(let y=0;y<H;y+=300){await p.mouse.wheel(0,300);await p.waitForTimeout(60)}await p.waitForTimeout(1300);
console.log(await p.evaluate(()=>[...document.querySelectorAll('.rv,.rh,.rw')].filter(e=>!e.classList.contains('in')).map(e=>e.tagName+'.'+e.className+':'+e.textContent.trim().slice(0,25)+' y='+Math.round(e.getBoundingClientRect().top+scrollY)+'/'+document.documentElement.scrollHeight+' sy='+Math.round(scrollY))));
await p.goto('http://localhost:8765/work/nick-and-jakes/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>[...document.querySelectorAll('.crumbs a')].map(a=>a.textContent+' '+JSON.stringify(a.getBoundingClientRect().toJSON()))));
await b.close()})();
