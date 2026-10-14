const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:769}});
for(const n of ['gig-1','gig-2','gig-3']){await p.goto('file://'+path.resolve(__dirname,n+'.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);await p.screenshot({path:path.resolve(__dirname,n+'.png')});}
await b.close();})();
