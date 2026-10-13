"""Portfolio-video (15 s, 1080x1920): een gsm waarin vijf voorbeeldsites scrollen.
Genereert portfolio-fr.html en portfolio-nl.html.
Renderen: AD=portfolio node render.js nl <map>"""
import json
import math
from pathlib import Path

HERE = Path(__file__).parent

T = {
 "fr": dict(title="Du travail<br>qui se voit.", concept="Concept", sub="Des sites pour des commerces imaginaires, pour vous montrer le style.",
            cta="Demander un devis", url="kadestudio.be", end="Votre commerce<br>est le suivant ?", bio="Lien<br>en bio",
            band=["Sites web pour petites entreprises belges", "Prix fixe", "FR + NL"],
            sites=[
             dict(name="Boulangerie Vanhove", short="Vanhove", city="Gand", bg="var(--sun)", fg="var(--ink)", acc="var(--cobalt)", accfg="var(--white)", h="Le levain<br>depuis 1987.", p="Pain, viennoiseries et tartes, cuits chaque nuit.", btn="Commander pour demain", items=["Pain de campagne", "Croissant", "Tarte au riz", "Pistolets"], prices=["4,20 €", "1,40 €", "14 €", "0,70 €"]),
             dict(name="Atelier 12", short="Atelier 12", city="Namur", bg="var(--ink)", fg="var(--paper)", acc="var(--acid)", accfg="var(--ink)", h="Barbier.<br>Sans rendez-vous<br>raté.", p="Coupe, barbe, rasage à l'ancienne. Réservez en ligne, 7j/7.", btn="Réserver", items=["Coupe", "Barbe", "Coupe + barbe", "Rasage"], prices=["25 €", "15 €", "35 €", "20 €"]),
             dict(name="Fleurs de Julie", short="Julie", city="Mons", bg="var(--bubble)", fg="var(--ink)", acc="var(--tomato)", accfg="var(--ink)", h="Des bouquets<br>qui parlent.", p="Fleurs de saison, livrées le jour même à Mons et alentours.", btn="Commander un bouquet", items=["Bouquet du jour", "Roses (12)", "Plante verte", "Mariage"], prices=["25 €", "39 €", "dès 18 €", "sur devis"]),
             dict(name="Garage Peeters", short="Peeters", city="Hasselt", bg="var(--cobalt)", fg="var(--white)", acc="var(--sun)", accfg="var(--ink)", h="Votre voiture,<br>bien suivie.", p="Entretien, pneus, contrôle technique. Devis clair avant toute intervention.", btn="Prendre rendez-vous", items=["Entretien", "Pneus (4)", "Pré-contrôle", "Diagnostic"], prices=["dès 149 €", "dès 320 €", "49 €", "39 €"]),
             dict(name="Friterie Chez Mo", short="Chez Mo", city="Liège", bg="var(--tomato)", fg="var(--ink)", acc="var(--sun)", accfg="var(--ink)", h="La vraie frite<br>liégeoise.", p="Cuite deux fois, servie chaude. Ouvert jusqu'à 23 h.", btn="Voir la carte", items=["Grande frite", "Fricadelle", "Boulet sauce lapin", "Mitraillette"], prices=["3,50 €", "2,50 €", "6 €", "8 €"]),
            ]),
 "nl": dict(title="Werk dat<br>opvalt.", concept="Concept", sub="Sites voor verzonnen zaken, om u de stijl te tonen.",
            cta="Offerte aanvragen", url="kadestudio.be", end="Uw zaak<br>is de volgende?", bio="Link<br>in bio",
            band=["Websites voor kleine Belgische bedrijven", "Vaste prijs", "NL + FR"],
            sites=[
             dict(name="Bakkerij Vanhove", short="Vanhove", city="Gent", bg="var(--sun)", fg="var(--ink)", acc="var(--cobalt)", accfg="var(--white)", h="Zuurdesem<br>sinds 1987.", p="Brood, koffiekoeken en taarten, elke nacht gebakken.", btn="Bestel voor morgen", items=["Boerenbrood", "Croissant", "Rijsttaart", "Pistolets"], prices=["4,20 €", "1,40 €", "14 €", "0,70 €"]),
             dict(name="Atelier 12", short="Atelier 12", city="Namen", bg="var(--ink)", fg="var(--paper)", acc="var(--acid)", accfg="var(--ink)", h="Barbier.<br>Nooit meer<br>wachten.", p="Knippen, baard, klassiek scheren. Reserveer online, 7 op 7.", btn="Reserveren", items=["Knippen", "Baard", "Knippen + baard", "Scheren"], prices=["25 €", "15 €", "35 €", "20 €"]),
             dict(name="Fleurs de Julie", short="Julie", city="Bergen", bg="var(--bubble)", fg="var(--ink)", acc="var(--tomato)", accfg="var(--ink)", h="Boeketten<br>die spreken.", p="Seizoensbloemen, dezelfde dag geleverd in Bergen en omgeving.", btn="Boeket bestellen", items=["Boeket van de dag", "Rozen (12)", "Kamerplant", "Huwelijk"], prices=["25 €", "39 €", "vanaf 18 €", "op offerte"]),
             dict(name="Garage Peeters", short="Peeters", city="Hasselt", bg="var(--cobalt)", fg="var(--white)", acc="var(--sun)", accfg="var(--ink)", h="Uw auto,<br>goed gevolgd.", p="Onderhoud, banden, keuring. Duidelijke offerte voor elke ingreep.", btn="Afspraak maken", items=["Onderhoud", "Banden (4)", "Pre-keuring", "Diagnose"], prices=["vanaf 149 €", "vanaf 320 €", "49 €", "39 €"]),
             dict(name="Frituur Chez Mo", short="Chez Mo", city="Luik", bg="var(--tomato)", fg="var(--ink)", acc="var(--sun)", accfg="var(--ink)", h="De echte<br>Luikse friet.", p="Twee keer gebakken, warm geserveerd. Open tot 23 u.", btn="Bekijk de kaart", items=["Grote friet", "Frikandel", "Boulet", "Mitraillette"], prices=["3,50 €", "2,50 €", "6 €", "8 €"]),
            ]),
}

HTML = r"""<!doctype html><html lang="__LANG__"><head><meta charset="utf-8"><style>
@font-face{font-family:BS;src:url(../../../fonts/big-shoulders-var-latin.woff2) format("woff2");font-weight:800 900}
@font-face{font-family:BR;src:url(../../../fonts/bricolage-400-800-latin.woff2) format("woff2");font-weight:400 800}
@font-face{font-family:CP;src:url(../../../fonts/courier-prime-700-latin.woff2) format("woff2");font-weight:700}
:root{--acid:#74DB4B;--tomato:#FF5426;--sun:#FFD43A;--bubble:#FFB8E0;--cobalt:#3B6BFF;--ink:#151515;--paper:#F1F2EC;--white:#fff}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--paper)}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;color:var(--ink);font-family:BR,sans-serif}
.abs{position:absolute}
.poster{font-family:BS;font-weight:900;text-transform:uppercase;line-height:.84}
.disp{font-family:BR;font-weight:800;letter-spacing:-.025em;line-height:.92;font-variation-settings:"wdth" 75,"opsz" 96}
.mono{font-family:CP;font-weight:700}
.band{left:0;right:0;height:84px;background:var(--sun);border-block:7px solid var(--ink);white-space:nowrap;font-family:BS;font-weight:900;text-transform:uppercase;font-size:44px;display:flex;align-items:center;z-index:5}
.band .tr{display:flex;gap:40px}
.band span{display:inline-flex;gap:40px;align-items:center}
.band span::after{content:"✶";color:var(--tomato)}
/* gsm */
#phone{left:150px;top:520px;width:780px;height:1500px;background:var(--ink);border-radius:90px;padding:22px;box-shadow:24px 24px 0 rgba(21,21,21,.18)}
#screen{position:relative;width:100%;height:100%;border-radius:70px;overflow:hidden;background:var(--white)}
__SITECSS__
/* label met naam en stad */
#tag{left:150px;top:1735px;width:780px;z-index:6}
#tagin{display:inline-flex;align-items:center;gap:22px;background:var(--white);border:7px solid var(--ink);box-shadow:14px 14px 0 var(--ink);padding:22px 36px;font-size:46px;font-weight:800;white-space:nowrap}
#tagin .c{font-family:CP;font-size:26px;border:4px solid var(--ink);border-radius:999px;padding:4px 18px}
#tagin .city{font-family:CP;font-size:30px;font-weight:700;color:#444}
.burst{display:grid;place-items:center;text-align:center;background:var(--white);clip-path:__STAR__;font-family:BS;font-weight:900;text-transform:uppercase;line-height:.92}
.bsh{background:var(--ink);clip-path:__STAR__}
#grain{position:absolute;inset:0;pointer-events:none;opacity:.14;mix-blend-mode:multiply;z-index:50;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .9 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
/* 4:5-feed: zonder titel, kortere gsm; wordt uitgesneden op y=285..1635 */
html.feed #title,html.feed #sub{display:none}
html.feed #phone{top:330px;height:1230px}
html.feed #tag{top:1500px}
html.feed #endh{top:360px}
html.feed #logo{top:690px}
html.feed #cta{top:1170px}
html.feed #bs{top:1295px}
html.feed #bb{top:1280px}
html.feed #url{top:1380px}
</style></head><body><div id="stage">
<div class="abs band" id="b1" style="top:0;border-top:0"><div class="tr" id="b1t">__BAND__</div></div>
<h1 class="abs disp" id="title" style="left:70px;top:160px;width:940px;font-size:150px">__TITLE__</h1>
<p class="abs" id="sub" style="left:74px;top:420px;width:760px;font-size:34px;font-weight:500;line-height:1.25">__SUB__</p>
<div class="abs" id="phone"><div id="screen">__SITES__</div></div>
<div class="abs" id="tag"><div id="tagin"><span class="c">__CONCEPT__</span><span id="tname"></span><span class="city" id="tcity"></span></div></div>

<!-- einde -->
<div class="abs" id="end" style="inset:0;background:var(--acid)">
  <div class="abs band" style="top:0;border-top:0"><div class="tr" id="b2t">__BAND__</div></div>
  <h2 class="abs disp" id="endh" style="left:70px;top:330px;width:940px;font-size:160px">__END__</h2>
  <img class="abs" id="logo" src="../../logo/kade-logo.svg" style="left:90px;top:760px;width:900px">
  <div class="abs" id="cta" style="left:70px;top:1330px;padding:38px 64px;background:var(--tomato);border:8px solid var(--ink);border-radius:999px;box-shadow:14px 14px 0 var(--ink);font-size:66px;font-weight:800;white-space:nowrap">__CTA__</div>
  <div class="abs bsh" id="bs" style="left:725px;top:1455px;width:300px;height:300px"></div>
  <div class="abs burst" id="bb" style="left:710px;top:1440px;width:300px;height:300px;font-size:76px;background:var(--sun)"><span style="transform:rotate(-8deg)">__BIO__</span></div>
  <p class="abs mono" id="url" style="left:76px;top:1540px;font-size:58px">__URL__</p>
  <div class="abs band" style="top:1836px;background:var(--ink);color:var(--acid)"><div class="tr" id="b3t">__BAND__</div></div>
</div>
<div id="grain"></div>
</div>
<script>
const DURATION=15;window.DURATION=DURATION;
const SITES=__SITEDATA__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const p=(t,a,b)=>cl((t-a)/(b-a));
const io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const oc=x=>1-Math.pow(1-x,3);
const oq=x=>1-Math.pow(1-x,4);
const ob=x=>{const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const lerp=(a,b,x)=>a+(b-a)*x;
function set(id,css){const e=$(id);for(const k in css)e.style[k]=css[k]}
function band(id,t,dir){$(id).style.transform=`translateX(${(dir*t*140)%1200-(dir>0?1200:0)}px)`}
if(location.hash==='#feed')document.documentElement.classList.add('feed');
const H=[...document.querySelectorAll('.site')].map(e=>e.offsetHeight);
const SCREEN=$('screen').offsetHeight, PER=2.4, START=0.9;   // elke site 2,3 s in beeld
function render(t){
  band('b1t',t,-1);band('b2t',t,-1);band('b3t',t,1);
  set('title',{transform:`translateY(${lerp(60,0,oc(p(t,.05,.5)))}px)`,opacity:p(t,.05,.3)});
  set('sub',{opacity:p(t,.35,.6)});
  set('phone',{transform:`translateY(${lerp(1500,0,oq(p(t,.3,1.0)))}px)`});
  // sites: horizontaal binnen, scrollen, horizontaal weg
  let cur=0;
  SITES.forEach((s,i)=>{
    const t0=START+i*PER, tin=p(t,t0,t0+.4), tout=p(t,t0+PER,t0+PER+.4);
    const x=lerp(760,0,oq(tin))-lerp(0,760,io(tout));
    const scroll=io(p(t,t0+.45,t0+PER-.05))*Math.max(0,H[i]-SCREEN);
    set('site'+i,{transform:`translate(${x}px,${-scroll}px)`,visibility:(tin>0&&tout<1)?'visible':'hidden'});
    if(t>=t0+.15&&t<t0+PER+.15)cur=i;
  });
  const s=SITES[cur];$('tname').textContent=s.name;$('tcity').textContent=s.city;
  const t0=START+cur*PER;const k=t<t0+.35?oq(p(t,t0+.1,t0+.4)):1-oq(p(t,t0+PER-.1,t0+PER+.15));
  set('tagin',{transform:`translateY(${lerp(60,0,k)}px) rotate(${lerp(2,-2,k)}deg)`,opacity:t<START+.1?0:k});
  // einde
  const E=START+SITES.length*PER+.1;   // 12,6 s
  set('end',{transform:`translateY(${lerp(1920,0,oq(p(t,E,E+.4)))}px)`});
  set('endh',{transform:`translateY(${lerp(80,0,oc(p(t,E+.3,E+.7)))}px)`,opacity:p(t,E+.3,E+.5)});
  const l=ob(p(t,E+.55,E+.95));set('logo',{transform:`scale(${lerp(2.2,1,l)}) rotate(${lerp(-12,-3,l)}deg)`,opacity:p(t,E+.55,E+.6)});
  set('cta',{transform:`scale(${ob(p(t,E+.9,E+1.2))})`,transformOrigin:'0 50%'});
  const b=ob(p(t,E+1.1,E+1.4));for(const id of ['bb','bs'])set(id,{transform:`scale(${b}) rotate(${(t-E-1.1)*-30}deg)`,opacity:t>E+1.1?1:0});
  set('url',{opacity:p(t,E+1.3,E+1.45)});
}
window.render=render;render(0);
</script></body></html>"""


def star(n=14, r=.76):
    pts = []
    for i in range(2 * n):
        rr = 50 if i % 2 == 0 else 50 * r
        a = math.pi * i / n - math.pi / 2
        pts.append(f"{50+rr*math.cos(a):.1f}% {50+rr*math.sin(a):.1f}%")
    return "polygon(" + ",".join(pts) + ")"


import sys; sys.path.insert(0, str(HERE))
import sites as SITES_MOD

for lang, t in T.items():
    gen = SITES_MOD.sites_html(lang)
    sites = "".join(html.replace('class="site"', f'class="site" id="site{i}"', 1) for i, (_, _, html) in enumerate(gen))
    html = HTML
    for k, v in {"__LANG__": lang, "__STAR__": star(), "__BAND__": "".join(f"<span>{b}</span>" for b in t["band"] * 4),
                 "__TITLE__": t["title"], "__SUB__": t["sub"], "__SITES__": sites, "__CONCEPT__": t["concept"],
                 "__END__": t["end"], "__CTA__": t["cta"], "__BIO__": t["bio"], "__URL__": t["url"], "__SITECSS__": SITES_MOD.CSS,
                 "__SITEDATA__": json.dumps([{"name": n, "city": c} for n, c, _ in gen], ensure_ascii=False)}.items():
        html = html.replace(k, v)
    (HERE / f"portfolio-{lang}.html").write_text(html, encoding="utf-8")
print("ok")
