const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});await p.addInitScript('window.__noPopup=true');
for(const [u,n] of [['work/the-netherland/','neth'],['work/','work'],['content/ga4-migration-gains-and-losses/','post']]){
 await p.goto('http://localhost:8766/'+u,{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.rv,.rh .hl,.rh .r,.rows>li{opacity:1!important;transform:none!important;clip-path:none!important}.pick,.testbar{display:none!important}'});
 const dead=await p.evaluate(async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,40))}scrollTo(0,0);await new Promise(r=>setTimeout(r,500));return [...document.images].filter(i=>!i.naturalWidth).length+'/'+document.images.length});
 console.log(u,'dead imgs',dead);
 await p.screenshot({path:`qa/out/s-${n}.png`,fullPage:true});}
await b.close()})();
