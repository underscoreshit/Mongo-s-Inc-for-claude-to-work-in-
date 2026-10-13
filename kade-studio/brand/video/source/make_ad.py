"""Genereert ad-fr.html en ad-nl.html (animatie van 15 s, 1080x1920).
Renderen naar MP4: node render.js  (zie README in brand/video)."""
import json, math
from pathlib import Path
HERE = Path(__file__).parent
CUR = json.loads((HERE / "cursors.json").read_text())

T = {
 "fr": dict(s1h="Votre client<br>vous cherche.", query="boulangerie wavre", zero="0 résultat", none="Aucun site trouvé.",
            s2a="Alors il va", s2b="chez le<br>voisin.",
            s3=["Clair.", "Rapide sur mobile.", "FR + NL.", "Trouvable."],
            s4="Prix fixe", frm="dès", tax="HTVA", burst="Livré en<br>3 semaines",
            cta="Demander un devis", bio="Lien<br>en bio", url="kadestudio.be",
            band=["Sites web pour petites entreprises belges", "Prix fixe", "FR + NL"]),
 "nl": dict(s1h="Uw klant<br>zoekt u.", query="bakkerij leuven", zero="0 resultaten", none="Geen website gevonden.",
            s2a="Dus gaat die", s2b="naar de<br>buren.",
            s3=["Helder.", "Snel op de gsm.", "NL + FR.", "Vindbaar."],
            s4="Vaste prijs", frm="vanaf", tax="excl. btw", burst="Online in<br>3 weken",
            cta="Offerte aanvragen", bio="Link<br>in bio", url="kadestudio.be",
            band=["Websites voor kleine Belgische bedrijven", "Vaste prijs", "NL + FR"]),
}

def star(n=14, r=.76):
    pts = []
    for i in range(2 * n):
        rr = 50 if i % 2 == 0 else 50 * r
        a = math.pi * i / n - math.pi / 2
        pts.append(f"{50+rr*math.cos(a):.1f}% {50+rr*math.sin(a):.1f}%")
    return "polygon(" + ",".join(pts) + ")"

HTML = r"""<!doctype html><html lang="__LANG__"><head><meta charset="utf-8"><style>
@font-face{font-family:BS;src:url(../../../fonts/big-shoulders-var-latin.woff2) format("woff2");font-weight:800 900}
@font-face{font-family:BR;src:url(../../../fonts/bricolage-400-800-latin.woff2) format("woff2");font-weight:400 800}
@font-face{font-family:CP;src:url(../../../fonts/courier-prime-700-latin.woff2) format("woff2");font-weight:700}
:root{--acid:#74DB4B;--tomato:#FF5426;--sun:#FFD43A;--bubble:#FFB8E0;--cobalt:#3B6BFF;--ink:#151515;--paper:#F1F2EC;--white:#fff}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--acid)}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;color:var(--ink);font-family:BR,sans-serif}
.abs{position:absolute}
.scene{position:absolute;inset:0;overflow:hidden}
.poster{font-family:BS;font-weight:900;text-transform:uppercase;line-height:.84}
.disp{font-family:BR;font-weight:800;letter-spacing:-.025em;line-height:.92;font-variation-settings:"wdth" 75,"opsz" 96}
.mono{font-family:CP;font-weight:700}
.band{left:0;right:0;height:84px;background:var(--sun);border-block:7px solid var(--ink);white-space:nowrap;font-family:BS;font-weight:900;text-transform:uppercase;font-size:44px;display:flex;align-items:center}
.band .tr{display:flex;gap:40px}
.band span{display:inline-flex;gap:40px;align-items:center}
.band span::after{content:"✶";color:var(--tomato)}
.burst{display:grid;place-items:center;text-align:center;background:var(--white);clip-path:__STAR__;font-family:BS;font-weight:900;text-transform:uppercase;line-height:.92}
.bsh{background:var(--ink);clip-path:__STAR__}
.pill{border:8px solid var(--ink);border-radius:999px;box-shadow:14px 14px 0 var(--ink)}
.px{position:absolute;width:20px;height:20px;box-shadow:5px 5px 0 var(--ink)}
#grain{position:absolute;inset:-200px;pointer-events:none;opacity:.16;mix-blend-mode:multiply;z-index:50;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .9 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.cur{width:102px;height:102px;image-rendering:pixelated;z-index:40}
</style></head><body><div id="stage">

<!-- SCENE 1: zoeken -->
<div class="scene" id="s1" style="background:var(--acid)">
  <div class="abs band" id="b1" style="top:160px"><div class="tr" id="b1t">__BAND__</div></div>
  <h1 class="abs disp" id="s1h" style="left:70px;top:330px;width:940px;font-size:150px;transform-origin:0 100%">__S1H__</h1>
  <div class="abs pill" id="search" style="left:70px;top:700px;width:940px;height:150px;background:var(--white);display:flex;align-items:center;gap:26px;padding:0 44px">
    <svg width="56" height="56" viewBox="0 0 14 14" shape-rendering="crispEdges" style="flex:none"><path fill="#151515" d="M4 0h4v1h1v1h1v1h1v4h-1v1h-1v1h-1v1H4V9H3V8H2V7H1V3h1V2h1V1h1zm0 2v1H3v4h1v1h4V7h1V3H8V2zm6 8h1v1h1v1h1v1h1v1h-2v-1h-1v-1h-1zm0-1h1v1h-1z"/></svg>
    <span class="mono" id="q" style="font-size:54px;white-space:pre"></span><span id="caret" style="width:6px;height:66px;background:var(--ink)"></span>
  </div>
  <div class="abs" id="none" style="left:110px;top:940px;width:860px;padding:44px 50px;background:var(--white);border:8px solid var(--ink);box-shadow:14px 14px 0 var(--ink)">
    <p class="mono" style="font-size:34px;color:#444">__ZERO__</p>
    <p class="disp" style="font-size:84px;margin-top:14px">__NONE__</p>
    <div class="abs poster" id="stamp" style="right:-40px;top:-70px;font-size:96px;color:var(--tomato);border:10px solid var(--tomato);padding:6px 26px 0;background:var(--white);transform:rotate(-12deg)">404</div>
  </div>
</div>

<!-- SCENE 2: de buren -->
<div class="scene" id="s2" style="background:var(--ink)">
  <p class="abs disp" id="s2a" style="left:70px;top:430px;font-size:120px;color:var(--paper)">__S2A__</p>
  <h2 class="abs poster" id="s2b" style="left:62px;top:600px;font-size:290px;color:transparent;-webkit-text-stroke:9px var(--acid)">__S2B__</h2>
</div>

<!-- SCENE 3: blokken -->
<div class="scene" id="s3" style="background:var(--paper)">
  __BLOCKS__
</div>

<!-- SCENE 4: prijs -->
<div class="scene" id="s4" style="background:var(--sun)">
  <h2 class="abs poster" id="s4h" style="left:70px;top:330px;font-size:190px;white-space:nowrap">__S4__</h2>
  <p class="abs disp" id="frm" style="left:76px;top:520px;font-size:90px">__FRM__</p>
  <p class="abs poster" id="price" style="left:62px;top:600px;font-size:440px;font-variant-numeric:tabular-nums;color:var(--white);-webkit-text-stroke:12px var(--ink);paint-order:stroke fill;text-shadow:18px 18px 0 var(--ink)">0 €</p>
  <p class="abs mono" id="tax" style="left:80px;top:1000px;font-size:52px">__TAX__</p>
  <div class="abs bsh" id="b4s" style="left:615px;top:1035px;width:400px;height:400px"></div>
  <div class="abs burst" id="b4" style="left:600px;top:1020px;width:400px;height:400px;font-size:74px"><span style="transform:rotate(-8deg)">__BURST__</span></div>
</div>

<!-- SCENE 5: logo + actie -->
<div class="scene" id="s5" style="background:var(--acid)">
  <div class="abs band" id="b5" style="top:160px"><div class="tr" id="b5t">__BAND__</div></div>
  <img class="abs" id="logo" src="../../logo/kade-logo.svg" style="left:90px;top:330px;width:900px">
  <div class="abs pill" id="cta" style="left:70px;top:900px;padding:38px 64px;background:var(--tomato);font-size:66px;font-weight:800;white-space:nowrap">__CTA__</div>
  <div class="abs bsh" id="b5s" style="left:725px;top:1085px;width:300px;height:300px"></div>
  <div class="abs burst" id="b5b" style="left:710px;top:1070px;width:300px;height:300px;font-size:76px;background:var(--sun)"><span style="transform:rotate(-8deg)">__BIO__</span></div>
  <p class="abs mono" id="url" style="left:76px;top:1110px;font-size:58px">__URL__</p>
  <div class="abs band" id="b6" style="top:1500px;background:var(--ink);color:var(--acid)"><div class="tr" id="b6t">__BAND__</div></div>
</div>

<img class="abs cur" id="cur" src="__CURA__">
<div id="pxs"></div>
<div id="grain"></div>
</div>
<script>
const QUERY="__QUERY__";
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const p=(t,a,b)=>cl((t-a)/(b-a));
const oc=x=>1-Math.pow(1-x,3);
const ob=x=>{const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const st=(x,n)=>Math.floor(x*n)/n;           // stappen: "game"-beweging
const lerp=(a,b,x)=>a+(b-a)*x;
function set(id,css){const e=$(id);for(const k in css)e.style[k]=css[k]}
function show(id,on){$(id).style.visibility=on?'visible':'hidden'}
const COLS=['var(--acid)','var(--sun)','var(--bubble)','var(--cobalt)','var(--tomato)'];
function burst(t,t0,x,y){const box=$('pxs');let h='';const k=p(t,t0,t0+.5);if(k>0&&k<1){const s=st(k,6);
  for(let i=0;i<10;i++){const a=i*Math.PI/5,r=40+s*120+(i%2)*30;h+=`<span class="px" style="left:${Math.round((x+Math.cos(a)*r)/10)*10}px;top:${Math.round((y+Math.sin(a)*r)/10)*10}px;background:${COLS[i%5]};opacity:${1-s}"></span>`}}
  return h}
function band(id,t,dir){$(id).style.transform=`translateX(${(dir*t*140)%1200-(dir>0?1200:0)}px)`}
function render(t){
  // welke scène
  const sc=t<3?1:t<5.2?2:t<9?3:t<12?4:5;
  for(let i=1;i<=5;i++)show('s'+i,i===sc||(i===2&&t>=3&&t<3.3)||(i===1&&t>=3&&t<3.3));
  let px='';
  // S1
  if(sc===1||t<3.3){
    band('b1t',t,-1);
    const h=ob(p(t,.1,.5));set('s1h',{transform:`scale(${lerp(1.5,1,h)})`,opacity:p(t,.1,.18)});
    set('search',{transform:`translateY(${lerp(400,0,oc(p(t,.25,.6)))}px)`});
    const n=Math.floor(p(t,.85,1.8)*QUERY.length);$('q').textContent=QUERY.slice(0,n);
    $('caret').style.opacity=(t>.8&&Math.floor(t*3)%2===0)?1:0;
    const r=ob(p(t,2.05,2.35));set('none',{transform:`translateY(${lerp(500,0,r)}px) rotate(${lerp(8,-2,r)}deg)`,opacity:p(t,2.05,2.1)});
    const s=p(t,2.45,2.6);set('stamp',{transform:`rotate(-12deg) scale(${lerp(3,1,ob(s))})`,opacity:s>0?1:0});
    const sh=t>2.6&&t<2.9?Math.sin(t*90)*12:0;set('none',{marginLeft:sh+'px'});
    if(t>=2.05&&t<2.35)px+='';
  }
  // overgang S1 -> S2: zwart schuift omhoog in stappen
  set('s2',{transform:`translateY(${t<3.3?(1-st(p(t,3,3.3),5))*1920:0}px)`});
  if(sc===2){
    set('s2a',{opacity:p(t,3.35,3.45),transform:`translateX(${lerp(-200,0,oc(p(t,3.35,3.6)))}px)`});
    const k=ob(p(t,3.75,4.05));const shake=t>4.05&&t<4.35?Math.sin(t*120)*14:0;
    set('s2b',{transform:`scale(${lerp(2.2,1,k)}) translate(${shake}px,${-shake/2}px)`,opacity:p(t,3.75,3.8),transformOrigin:'0 0'});
  }
  // S3 blokken
  if(sc===3){
    for(let i=0;i<4;i++){
      const tin=5.25+i*.45,tout=8.45+i*.1;
      const x=t<tout?(1-st(oc(p(t,tin,tin+.4)),6))*-1100:st(p(t,tout,tout+.35),5)*1100;
      set('blk'+i,{transform:`translateX(${x}px)`});
    }
  }
  // S4 prijs
  if(sc===4){
    set('s4h',{transform:`translateY(${(1-st(oc(p(t,9.05,9.4)),6))*-600}px)`});
    set('frm',{opacity:p(t,9.4,9.5)});
    const c=oc(p(t,9.45,10.5));$('price').textContent=Math.round(690*c)+' €';
    set('price',{transform:`scale(${t>10.5&&t<10.75?1+.06*Math.sin(p(t,10.5,10.75)*Math.PI):1})`,transformOrigin:'0 50%'});
    set('tax',{opacity:p(t,10.5,10.6)});
    const b=ob(p(t,10.7,11.1));const rot=(t-10.7)*40;
    for(const id of ['b4','b4s'])set(id,{transform:`scale(${b}) rotate(${rot}deg)`,opacity:t>10.7?1:0});
  }
  // S5 logo + CTA + klik
  if(sc===5){
    band('b5t',t,-1);band('b6t',t,1);
    const l=ob(p(t,12.05,12.5));set('logo',{transform:`scale(${lerp(2.4,1,l)}) rotate(${lerp(-14,-3,l)}deg)`,opacity:p(t,12.05,12.12)});
    const press=t>13.75&&t<13.95;const c=ob(p(t,12.55,12.85));
    set('cta',{transform:`translate(${press?14:0}px,${press?14:0}px) scale(${c})`,boxShadow:press?'0 0 0 #151515':'14px 14px 0 #151515',transformOrigin:'0 50%'});
    const b=ob(p(t,12.9,13.2));for(const id of ['b5b','b5s'])set(id,{transform:`scale(${b}) rotate(${(t-12.9)*-30}deg)`,opacity:t>12.9?1:0});
    set('url',{opacity:p(t,14,14.1),transform:`translateY(${lerp(30,0,oc(p(t,14,14.3)))}px)`});
    px+=burst(t,13.8,520,990);
  }
  // pixel-cursor: S1 naar zoekbalk, S5 naar de knop
  let cx=-200,cy=-200,src='__CURA__';
  if(t<3){const k=st(oc(p(t,.3,.75)),8);cx=lerp(1100,860,k);cy=lerp(1400,760,k);if(t>.75){src='__CURP__'}px+=burst(t,.78,870,770)}
  else if(t>=13.15){const k=st(oc(p(t,13.15,13.7)),8);cx=lerp(1100,560,k);cy=lerp(1600,970,k);src='__CURP__';if(t>13.75&&t<13.95){cx+=14;cy+=14}}
  set('cur',{left:cx+'px',top:cy+'px'});if($('cur').getAttribute('src')!==src)$('cur').setAttribute('src',src);
  $('pxs').innerHTML=px;
  // korrel verschuift per beeld, zoals film
  const f=Math.floor(t*30/5);$('grain').style.transform=`translate(${(f*73)%160-80}px,${(f*131)%160-80}px)`;
}
window.render=render;render(0);
</script></body></html>"""

COLORS = [("var(--sun)", "var(--ink)"), ("var(--bubble)", "var(--ink)"), ("var(--cobalt)", "var(--white)"), ("var(--tomato)", "var(--ink)")]
for lang, t in T.items():
    blocks = ""
    for i, (txt, (bg, fg)) in enumerate(zip(t["s3"], COLORS)):
        fs = 190 if len(txt) <= 9 else (140 if len(txt) <= 14 else 116)
        blocks += (f'<div class="abs" id="blk{i}" style="left:0;top:{290+i*290}px;width:1080px;height:290px;background:{bg};color:{fg};'
                   f'border-block:7px solid var(--ink);display:flex;align-items:center;padding:0 70px">'
                   f'<span class="poster" style="font-size:{fs}px;white-space:nowrap">{txt}</span></div>')
    band = "".join(f"<span>{b}</span>" for b in t["band"] * 4)
    html = HTML
    for k, v in {"__LANG__": lang, "__STAR__": star(), "__BAND__": band, "__S1H__": t["s1h"], "__NONE__": t["none"],
                 "__S2A__": t["s2a"], "__S2B__": t["s2b"], "__BLOCKS__": blocks, "__S4__": t["s4"], "__FRM__": t["frm"],
                 "__TAX__": t["tax"], "__BURST__": t["burst"], "__CTA__": t["cta"], "__BIO__": t["bio"], "__URL__": t["url"],
                 "__QUERY__": t["query"], "__ZERO__": t["zero"], "__CURA__": CUR["arrow2"], "__CURP__": CUR["point2"]}.items():
        html = html.replace(k, v)
    (HERE / f"ad-{lang}.html").write_text(html, encoding="utf-8")
print("ok")
