const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const [H,O]=process.argv.slice(2);const man=JSON.parse(fs.readFileSync(H+'/manifest.json'));
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const [k,w,h] of man){await p.setViewportSize({width:w,height:h});await p.goto('file://'+H+'/'+k+'.html');await p.evaluate(()=>document.fonts.ready);
const out=path.join(O,k+'.png');fs.mkdirSync(path.dirname(out),{recursive:true});await p.screenshot({path:out,clip:{x:0,y:0,width:w,height:h}});}
for(const f of ['kade-logo','kade-logo-ink','kade-logo-white','kade-mark']){const svg=fs.readFileSync(O+'/../logo/'+f+'.svg','utf8');const m=svg.match(/width="(\d+)" height="(\d+)"/);const w=+m[1]*3,h=+m[2]*3;
await p.setViewportSize({width:w,height:h});await p.setContent(`<style>html,body{margin:0;background:transparent}svg{width:${w}px;height:${h}px;display:block}</style>`+svg);
await p.screenshot({path:O+'/../logo/'+f+'.png',omitBackground:true,clip:{x:0,y:0,width:w,height:h}});}
await b.close();})();
