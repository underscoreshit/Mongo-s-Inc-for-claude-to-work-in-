// Gebruik: node render.js <lang> <uit-map> [tijden...]  (zonder tijden: alle 450 beelden aan 30 fps)
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const [lang,out,...times]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(__dirname,`ad-${lang}.html`));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
fs.mkdirSync(out,{recursive:true});
const T=times.length?times.map(Number):[...Array(Math.round(30*(await p.evaluate(()=>window.DURATION)))).keys()].map(f=>f/30);
for(let i=0;i<T.length;i++){await p.evaluate(t=>window.render(t),T[i]);
  await p.screenshot({path:path.join(out,(times.length?'t'+T[i]:String(i).padStart(4,'0'))+'.jpg'),type:'jpeg',quality:93});}
await b.close();})();
