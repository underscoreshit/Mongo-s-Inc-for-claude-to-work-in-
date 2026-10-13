import sys,os,json,math
FD,LOGO,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
logo=open(LOGO+'/kade-logo.svg').read()
logo_w=open(LOGO+'/kade-logo-white.svg').read()
logo_ink=open(LOGO+'/kade-logo-ink.svg').read()
mark=open(LOGO+'/kade-mark.svg').read()
def star(n=14,r=.76):
    pts=[]
    for i in range(2*n):
        rr=50 if i%2==0 else 50*r;a=math.pi*i/n-math.pi/2
        pts.append(f"{50+rr*math.cos(a):.1f}% {50+rr*math.sin(a):.1f}%")
    return "polygon("+",".join(pts)+")"
STAR=star()
CSS=f'''
@font-face{{font-family:BS;src:url(file://{FD}/f1.ttf);font-weight:900}}
@font-face{{font-family:BR;src:url(file://{FD}/f2.ttf);font-weight:800}}
@font-face{{font-family:BR;src:url(file://{FD}/f4.ttf);font-weight:500}}
@font-face{{font-family:CP;src:url(file://{FD}/f3.ttf);font-weight:700}}
@font-face{{font-family:CP;src:url(file://{FD}/f5.ttf);font-weight:400}}
:root{{--acid:#74DB4B;--tomato:#FF5426;--sun:#FFD43A;--bubble:#FFB8E0;--cobalt:#3B6BFF;--ink:#151515;--paper:#F1F2EC;--white:#fff}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:transparent}}
.f{{position:relative;overflow:hidden;color:var(--ink);font-family:BR,sans-serif}}
.f::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.16;mix-blend-mode:multiply;z-index:40;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .9 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
.poster{{font-family:BS;font-weight:900;text-transform:uppercase;line-height:.84}}
.disp{{font-family:BR;font-weight:800;letter-spacing:-.025em;line-height:.92;font-stretch:75%}}
.mono{{font-family:CP}}
.band{{position:absolute;left:0;right:0;background:var(--sun);border-block:6px solid var(--ink);white-space:nowrap;font-family:BS;font-weight:900;text-transform:uppercase;font-size:38px;padding:10px 0;display:flex;gap:34px;overflow:hidden}}
.band span{{display:inline-flex;gap:34px;align-items:center}}
.band span::after{{content:"✶";color:var(--tomato)}}
.burst{{position:absolute;display:grid;place-items:center;text-align:center;background:var(--white);clip-path:{STAR};font-family:BS;font-weight:900;text-transform:uppercase;line-height:.92}}
.burst-sh{{position:absolute;background:var(--ink);clip-path:{STAR}}}
.pill{{display:inline-block;border:5px solid currentColor;border-radius:999px;padding:6px 26px;font-family:CP;font-weight:700}}
.card{{position:absolute;border:8px solid var(--ink);box-shadow:16px 16px 0 var(--ink)}}
.tape{{position:absolute;width:200px;height:56px;background:rgba(255,255,255,.6);border:2px solid rgba(21,21,21,.15)}}
.dots{{position:absolute;background-image:radial-gradient(circle,currentColor 4px,transparent 4.6px);background-size:22px 22px;-webkit-mask-image:linear-gradient(to top,#000,transparent)}}
.handle{{position:absolute;font-family:CP;font-weight:700;font-size:30px}}
.disp em{{font-style:normal;display:inline-block;background:var(--ink);color:var(--acid);padding:0 .12em .06em;border-radius:.1em;transform:rotate(-2deg)}}
.logo svg{{width:100%;height:auto;display:block}}
'''
def page(w,h,body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="f" style="width:{w}px;height:{h}px">{body}</div></body></html>'
def band(top,items,extra=''):
    s=''.join(f'<span>{t}</span>' for t in items*3)
    return f'<div class="band" style="top:{top}px;{extra}">{s}</div>'
def burst(x,y,size,html,fs,bg='var(--white)',rot=-8):
    return (f'<div class="burst-sh" style="left:{x+10}px;top:{y+10}px;width:{size}px;height:{size}px"></div>'
            f'<div class="burst" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;font-size:{fs}px;background:{bg}"><span style="transform:rotate({rot}deg)">{html}</span></div>')
HANDLE="@kadestudio"
L={
'fr':dict(band=["Sites web pour petites entreprises belges","Bruxelles, Wallonie, Flandre","Français et Nederlands"],
  h1='Des sites web qui ont de la <em>gueule.</em>',sub="Sites vitrines pour les petites entreprises belges.",
  formule="Formule",offer="Vitrine",price="1 490 €",tax="HTVA",pills=["jusqu'à 6 pages","textes rédigés","FR + NL","référencement local","3 semaines"],
  fast="Livré en<br>3 semaines",fast_sub="De l'appel à la mise en ligne. Prix fixe, annoncé avant de commencer.",
  who="Le commerce<br>du coin",who_p="Horaires à jour, produits en photo, itinéraire en un clic. Les gens vous trouvent et passent la porte.",
  newsite="Nouveau site<br>en ligne",client="Nom du client, Ville",shot="Votre capture ici",
  tip="Astuce",tip_h="Vos horaires sur Google sont à jour?",tip_p="C'est la première chose que vos clients regardent. Vérifiez-les avant chaque jour férié.",
  st_h="Un site pour votre commerce?",st_sticker="Lien<br>en bio",cta="Demander un devis",
  st2="Nouveau<br>projet",swipe="Voir le site",
  hl=[("Travaux","var(--sun)"),("Offres","var(--acid)"),("Avis","var(--bubble)"),("Contact","var(--cobalt)")]),
'nl':dict(band=["Websites voor kleine Belgische bedrijven","Brussel, Wallonië, Vlaanderen","Nederlands en Frans"],
  h1='Websites die <em>opvallen.</em>',sub="Websites voor kleine Belgische bedrijven.",
  formule="Formule",offer="Etalage",price="1 490 €",tax="excl. btw",pills=["tot 6 pagina's","teksten geschreven","NL + FR","lokale SEO","3 weken"],
  fast="Online in<br>3 weken",fast_sub="Van eerste gesprek tot lancering. Vaste prijs, vooraf meegedeeld.",
  who="De winkel<br>om de hoek",who_p="Openingsuren up-to-date, producten in beeld, route in één klik. Mensen vinden u en stappen binnen.",
  newsite="Nieuwe site<br>online",client="Naam klant, Stad",shot="Uw screenshot hier",
  tip="Tip",tip_h="Kloppen uw openingsuren op Google?",tip_p="Dat is het eerste wat klanten bekijken. Controleer ze voor elke feestdag.",
  st_h="Een website voor uw zaak?",st_sticker="Link<br>in bio",cta="Offerte aanvragen",
  st2="Nieuw<br>project",swipe="Bekijk de site",
  hl=[("Werk","var(--sun)"),("Prijzen","var(--acid)"),("Reviews","var(--bubble)"),("Contact","var(--cobalt)")]),
}
files={}
# profile (language-free)
files['profile-picture']=(1080,1080,f'<div style="position:absolute;inset:0;background:var(--acid)"></div><div class="logo" style="position:absolute;left:115px;top:115px;width:850px">{mark}</div>')
files['logo-on-acid']=(1600,900,f'<div style="position:absolute;inset:0;background:var(--acid)"></div><div class="logo" style="position:absolute;left:250px;top:200px;width:1100px">{logo}</div>')
files['logo-on-ink']=(1600,900,f'<div style="position:absolute;inset:0;background:var(--ink)"></div><div class="logo" style="position:absolute;left:250px;top:200px;width:1100px">{logo}</div>')
for lg,t in L.items():
    # FB cover 1640x624, safe center
    files[f'{lg}/facebook-cover']=(1640,624,
      f'<div style="position:absolute;inset:0;background:var(--acid)"></div>'+band(0,t['band'],'border-top:0')+
      f'<div class="logo" style="position:absolute;left:330px;top:150px;width:900px">{logo}</div>'+
      burst(1170,120,300,t['fast'],46)+
      f'<div class="card" style="left:-60px;top:230px;width:330px;height:260px;background:var(--cobalt);transform:rotate(-8deg)"></div>'+
      f'<div class="card" style="left:1420px;top:420px;width:300px;height:240px;background:var(--bubble);transform:rotate(6deg)"></div>')
    P=(1080,1350)
    files[f'{lg}/post-1-intro']=(*P,
      f'<div style="position:absolute;inset:0;background:var(--acid)"></div>'+band(0,t['band'],'border-top:0')+
      f'<h1 class="disp" style="position:absolute;left:70px;top:180px;width:940px;font-size:150px">{t["h1"]}</h1>'+
      f'<p style="position:absolute;left:70px;top:720px;width:760px;font-size:44px;font-weight:500;line-height:1.25">{t["sub"]}</p>'+
      f'<div class="logo" style="position:absolute;left:60px;top:900px;width:760px">{logo}</div>'+
      burst(770,840,250,"FR<br>+ NL",70,'var(--sun)'))
    pills=''.join(f'<span class="pill" style="font-size:32px;margin:0 12px 14px 0">{p}</span>' for p in t['pills'])
    files[f'{lg}/post-2-offre']=(*P,
      f'<div style="position:absolute;inset:0;background:var(--ink)"></div>'+
      f'<p class="mono" style="position:absolute;left:70px;top:80px;color:var(--paper);font-size:34px;font-weight:700">{t["formule"]}</p>'+
      f'<h2 class="poster" style="position:absolute;left:62px;top:130px;font-size:300px;color:transparent;-webkit-text-stroke:6px var(--acid)">{t["offer"]}</h2>'+
      f'<div style="position:absolute;left:70px;top:470px;width:940px;color:var(--acid)">{pills}</div>'+
      f'<div class="card" style="left:70px;top:820px;width:640px;height:330px;background:var(--sun);transform:rotate(-3deg);padding:40px 46px;box-shadow:16px 16px 0 var(--acid)"><p class="poster" style="font-size:190px">{t["price"]}</p><p class="mono" style="font-size:36px;font-weight:700;margin-top:14px">{t["tax"]}</p></div>'+
      f'<div class="handle" style="right:70px;bottom:60px;color:var(--paper)">{HANDLE}</div>')
    files[f'{lg}/post-3-delai']=(*P,
      f'<div style="position:absolute;inset:0;background:var(--cobalt)"></div>'+
      burst(70,90,940,t['fast'],128)+
      f'<p style="position:absolute;left:80px;top:1080px;width:900px;font-size:44px;font-weight:500;line-height:1.25;color:var(--white)">{t["fast_sub"]}</p>'+
      f'<div class="handle" style="right:70px;bottom:50px;color:var(--white)">{HANDLE}</div>')
    files[f'{lg}/post-4-pour-qui']=(*P,
      f'<div style="position:absolute;inset:0;background:var(--bubble)"></div>'+
      f'<h2 class="poster" style="position:absolute;left:70px;top:90px;font-size:180px">{t["who"]}</h2>'+
      f'<p style="position:absolute;left:70px;top:560px;width:600px;font-size:42px;font-weight:500;line-height:1.3">{t["who_p"]}</p>'+
      f'<div class="poster" style="position:absolute;right:-40px;bottom:-150px;font-size:820px;color:transparent;-webkit-text-stroke:10px var(--ink)">€</div>'+
      f'<div class="handle" style="left:70px;bottom:60px">{HANDLE}</div>')
    files[f'{lg}/post-5-nouveau-projet']=(*P,
      f'<div style="position:absolute;inset:0;background:var(--sun)"></div>'+
      f'<h2 class="poster" style="position:absolute;left:70px;top:70px;font-size:150px">{t["newsite"]}</h2>'+
      f'<div class="card" style="left:110px;top:400px;width:860px;height:690px;background:var(--white);transform:rotate(-2deg);display:grid;place-items:center"><div class="tape" style="left:330px;top:-34px;transform:rotate(-4deg)"></div><p class="mono" style="font-size:40px;font-weight:700;border:5px dashed var(--ink);padding:30px 50px">{t["shot"]}</p></div>'+
      f'<p style="position:absolute;left:70px;top:1170px;font-size:50px;font-weight:800">{t["client"]}</p>'+
      f'<div class="handle" style="right:70px;bottom:60px">{HANDLE}</div>')
    files[f'{lg}/post-6-astuce']=(*P,
      f'<div style="position:absolute;inset:0;background:var(--tomato)"></div>'+
      f'<span class="pill" style="position:absolute;left:70px;top:80px;font-size:38px;background:var(--white);border-color:var(--ink);transform:rotate(-4deg)">{t["tip"]} #1</span>'+
      f'<h2 class="disp" style="position:absolute;left:70px;top:220px;width:940px;font-size:140px">{t["tip_h"]}</h2>'+
      f'<p style="position:absolute;left:70px;top:860px;width:760px;font-size:46px;font-weight:500;line-height:1.28">{t["tip_p"]}</p>'+
      f'<div class="handle" style="left:70px;bottom:60px">{HANDLE}</div>'+
      f'<div class="logo" style="position:absolute;right:50px;bottom:40px;width:300px">{logo_ink}</div>')
    S=(1080,1920)
    files[f'{lg}/story-1-contact']=(*S,
      f'<div style="position:absolute;inset:0;background:var(--acid)"></div>'+band(250,t['band'])+
      f'<h1 class="disp" style="position:absolute;left:70px;top:430px;width:940px;font-size:170px">{t["st_h"]}</h1>'+
      burst(640,880,340,t['st_sticker'],80,'var(--sun)')+
      f'<span style="position:absolute;left:70px;top:1170px;background:var(--tomato);border:7px solid var(--ink);border-radius:999px;padding:26px 46px;font-size:50px;font-weight:800;box-shadow:12px 12px 0 var(--ink)">{t["cta"]}</span>'+
      f'<div class="logo" style="position:absolute;left:70px;top:1500px;width:620px">{logo}</div>')
    files[f'{lg}/story-2-projet']=(*S,
      f'<div style="position:absolute;inset:0;background:var(--cobalt)"></div>'+
      f'<h2 class="poster" style="position:absolute;left:70px;top:230px;font-size:220px;color:var(--white);-webkit-text-stroke:8px var(--ink);paint-order:stroke fill;text-shadow:12px 12px 0 var(--ink)">{t["st2"]}</h2>'+
      f'<div class="card" style="left:200px;top:720px;width:680px;height:860px;background:var(--white);border-radius:60px;transform:rotate(3deg);display:grid;place-items:center"><p class="mono" style="font-size:38px;font-weight:700;border:5px dashed var(--ink);padding:26px 40px">{t["shot"]}</p></div>'+
      f'<span style="position:absolute;left:290px;top:1660px;background:var(--sun);border:7px solid var(--ink);border-radius:999px;padding:22px 50px;font-size:48px;font-weight:800">{t["swipe"]} ↗</span>')
    for i,(lab,col) in enumerate(t['hl'],1):
        fs=200 if len(lab)<=5 else (160 if len(lab)<=7 else 140)
        files[f'{lg}/highlight-{i}-{lab.lower()}']=(1080,1080,
          f'<div style="position:absolute;inset:0;background:{col}"></div>'
          f'<div style="position:absolute;inset:0;display:grid;place-items:center"><span class="poster" style="font-size:{fs}px;{"color:var(--white);-webkit-text-stroke:6px var(--ink);paint-order:stroke fill" if col=="var(--cobalt)" else ""};transform:rotate(-6deg)">{lab}</span></div>')

# ---------- first post: launch carousel (5 slides) + OG image ----------
FP={
'fr':dict(s1a="Kade Studio",s1b="est ouvert.",swipe="Glissez",
  s2="Un client vous cherche sur Google.",s2b="Il trouve quoi?",s2c="Pas de site, des horaires faux, une photo floue de 2017. Il va chez le voisin.",
  s3="Un site clair, rapide, en FR et NL.",s3p=["Horaires et itinéraire","Lisible sur téléphone","Trouvable sur Google"],s3s="Livré en<br>3 semaines",
  s4="Prix fixe.",s4b="Annoncé avant de commencer.",rows=[("Une page","690 €"),("Vitrine","1 490 €"),("Boutique","dès 2 900 €")],tax="Montants HTVA",
  s5="Votre devis est gratuit.",s5p="Dites-moi votre métier et votre ville. Je vous réponds sous 24 h ouvrables.",bio="Lien<br>en bio",
  og="Sites web pour petites entreprises belges"),
'nl':dict(s1a="Kade Studio",s1b="is open.",swipe="Swipe",
  s2="Een klant zoekt u op Google.",s2b="Wat vindt die?",s2c="Geen website, verkeerde openingsuren, een wazige foto uit 2017. Die gaat naar de buren.",
  s3="Een heldere, snelle site, in NL en FR.",s3p=["Openingsuren en route","Leesbaar op de gsm","Vindbaar op Google"],s3s="Online in<br>3 weken",
  s4="Vaste prijs.",s4b="Vooraf meegedeeld.",rows=[("Eén pagina","690 €"),("Etalage","1 490 €"),("Webshop","vanaf 2 900 €")],tax="Bedragen excl. btw",
  s5="Uw offerte is gratis.",s5p="Vertel me uw vak en uw stad. U krijgt antwoord binnen 24 werkuren.",bio="Link<br>in bio",
  og="Websites voor kleine Belgische bedrijven"),
}
def dots(n,i,col):
    return '<div style="position:absolute;left:0;right:0;bottom:46px;display:flex;justify-content:center;gap:14px">'+''.join(f'<span style="width:18px;height:18px;border-radius:50%;border:4px solid {col};background:{col if j==i else "transparent"}"></span>' for j in range(n))+'</div>'
for lg,t in FP.items():
    P=(1080,1350)
    files[f'{lg}/first-post/slide-1']=(*P,
      '<div style="position:absolute;inset:0;background:var(--acid)"></div>'+band(0,L[lg]['band'],'border-top:0')+
      f'<div class="logo" style="position:absolute;left:70px;top:190px;width:940px">{logo}</div>'+
      f'<h1 class="disp" style="position:absolute;left:70px;top:740px;width:940px;font-size:170px"><em>{t["s1b"]}</em></h1>'+
      f'<p style="position:absolute;left:70px;top:960px;width:700px;font-size:44px;font-weight:500;line-height:1.25">{L[lg]["sub"]}</p>'+
      burst(760,1030,250,t['swipe'],56,'var(--sun)')+dots(5,0,'var(--ink)'))
    files[f'{lg}/first-post/slide-2']=(*P,
      '<div style="position:absolute;inset:0;background:var(--ink)"></div>'+
      f'<h2 class="disp" style="position:absolute;left:70px;top:110px;width:940px;font-size:120px;color:var(--paper)">{t["s2"]}</h2>'+
      f'<h2 class="poster" style="position:absolute;left:66px;top:560px;width:960px;font-size:230px;color:transparent;-webkit-text-stroke:6px var(--acid)">{t["s2b"]}</h2>'+
      f'<p style="position:absolute;left:70px;top:1010px;width:820px;font-size:44px;font-weight:500;line-height:1.3;color:var(--paper)">{t["s2c"]}</p>'+dots(5,1,'var(--acid)'))
    pills=''.join(f'<span class="pill" style="font-size:36px;background:var(--white);border-color:var(--ink);transform:rotate({[-3,2,-1][i]}deg)">{x}</span>' for i,x in enumerate(t['s3p']))
    files[f'{lg}/first-post/slide-3']=(*P,
      '<div style="position:absolute;inset:0;background:var(--sun)"></div>'+
      f'<h2 class="disp" style="position:absolute;left:70px;top:110px;width:940px;font-size:140px">{t["s3"]}</h2>'+
      f'<div style="position:absolute;left:70px;top:720px;width:620px;display:flex;flex-direction:column;align-items:flex-start;gap:26px">{pills}</div>'+
      burst(640,660,400,t['s3s'],62,'var(--white)')+dots(5,2,'var(--ink)'))
    rows=''.join(f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;border-bottom:6px solid var(--ink);padding:26px 0"><span class="disp" style="font-size:66px">{a}</span><span class="poster" style="font-size:110px;white-space:nowrap">{b}</span></div>' for a,b in t['rows'])
    files[f'{lg}/first-post/slide-4']=(*P,
      '<div style="position:absolute;inset:0;background:var(--bubble)"></div>'+
      f'<h2 class="poster" style="position:absolute;left:70px;top:90px;font-size:180px;white-space:nowrap">{t["s4"]}</h2>'+
      f'<p style="position:absolute;left:74px;top:270px;font-size:48px;font-weight:800">{t["s4b"]}</p>'+
      f'<div style="position:absolute;left:70px;top:430px;width:940px;border-top:6px solid var(--ink)">{rows}</div>'+
      f'<p class="mono" style="position:absolute;left:74px;top:1100px;font-size:34px;font-weight:700">{t["tax"]}</p>'+dots(5,3,'var(--ink)'))
    files[f'{lg}/first-post/slide-5']=(*P,
      '<div style="position:absolute;inset:0;background:var(--cobalt)"></div>'+
      f'<h2 class="poster" style="position:absolute;left:70px;top:100px;width:940px;font-size:200px;color:var(--white);-webkit-text-stroke:8px var(--ink);paint-order:stroke fill;text-shadow:12px 12px 0 var(--ink)">{t["s5"]}</h2>'+
      f'<p style="position:absolute;left:70px;top:660px;width:640px;font-size:46px;font-weight:500;line-height:1.3;color:var(--white)">{t["s5p"]}</p>'+
      f'<span style="position:absolute;left:70px;top:940px;background:var(--tomato);border:7px solid var(--ink);border-radius:999px;padding:24px 44px;font-size:48px;font-weight:800;box-shadow:12px 12px 0 var(--ink)">{L[lg]["cta"]}</span>'+
      burst(700,760,320,t['bio'],78,'var(--sun)')+
      f'<div class="handle" style="left:74px;top:1130px;color:var(--white);font-size:38px">{HANDLE}</div>'+dots(5,4,'var(--white)'))
    files[f'{lg}/og-image']=(1200,630,
      '<div style="position:absolute;inset:0;background:var(--acid)"></div>'+band(0,L[lg]['band'],'border-top:0')+
      f'<div class="logo" style="position:absolute;left:70px;top:140px;width:640px">{logo}</div>'+
      f'<p class="disp" style="position:absolute;left:74px;top:500px;width:1060px;font-size:50px">{t["og"]}</p>'+
      burst(830,130,300,L[lg]['fast'],52,'var(--white)'))
os.makedirs(OUT,exist_ok=True)
man=[]
for k,(w,h,body) in files.items():
    p=os.path.join(OUT,k+'.html');os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w').write(page(w,h,body));man.append([k,w,h])
json.dump(man,open(os.path.join(OUT,'manifest.json'),'w'))
print(len(man))
