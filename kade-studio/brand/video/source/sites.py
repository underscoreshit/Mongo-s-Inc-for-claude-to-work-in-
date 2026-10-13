"""Vijf voorbeeldsites (736 px breed, mobiel) voor de portfolio-video.
Elke site heeft een eigen stijl: lettertype, kleuren, opbouw. Teksten in nl en fr.
sites_html(lang) -> lijst van (naam, stad, html)."""

GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .6 0'/%3E"
         "%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")")

CSS = r"""
@font-face{font-family:Playfair;src:url(fonts/playfair-700-normal.woff2) format("woff2");font-weight:700}
@font-face{font-family:Lora;src:url(fonts/lora-400-normal.woff2) format("woff2");font-weight:400}
@font-face{font-family:Lora;src:url(fonts/lora-700-normal.woff2) format("woff2");font-weight:700}
@font-face{font-family:Lora;src:url(fonts/lora-400-italic.woff2) format("woff2");font-weight:400;font-style:italic}
@font-face{font-family:Oswald;src:url(fonts/oswald-600-normal.woff2) format("woff2");font-weight:600}
@font-face{font-family:InterT;src:url(fonts/intertight-400-normal.woff2) format("woff2");font-weight:400}
@font-face{font-family:InterT;src:url(fonts/intertight-700-normal.woff2) format("woff2");font-weight:700}
@font-face{font-family:Nunito;src:url(fonts/nunito-400-normal.woff2) format("woff2");font-weight:400}
@font-face{font-family:Nunito;src:url(fonts/nunito-800-normal.woff2) format("woff2");font-weight:800}
@font-face{font-family:Barlow;src:url(fonts/barlow-700-normal.woff2) format("woff2");font-weight:700}
@font-face{font-family:Lilita;src:url(fonts/lilita-400-normal.woff2) format("woff2");font-weight:400}
.site{position:absolute;left:0;top:0;width:736px;line-height:1.35}
.site *{box-sizing:border-box}
.site img,.site svg{display:block}
.ph{position:relative;overflow:hidden}
.ph::after{content:"";position:absolute;inset:0;opacity:.22;mix-blend-mode:multiply;background-image:GRAIN}
.stars{letter-spacing:2px;font-size:26px}
.map{position:relative;overflow:hidden;background:#E9E5DC}
.map svg{width:100%;height:100%}
.ig{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.ig div{aspect-ratio:1;position:relative;overflow:hidden}
.ig svg{position:absolute;inset:0;width:100%;height:100%}
""".replace("GRAIN", GRAIN)

# ---------- illustraties (SVG, eenvoudig en vlak) ----------
def svg_bread(c1="#C27A3C", c2="#8E4F22", bg="none"):
    return f'''<svg viewBox="0 0 400 300"><rect width="400" height="300" fill="{bg}"/>
<ellipse cx="200" cy="200" rx="150" ry="70" fill="{c2}"/><ellipse cx="200" cy="180" rx="150" ry="78" fill="{c1}"/>
<path d="M120 150q30-20 50 0M180 140q30-20 50 0M240 150q30-20 50 0" stroke="#F6E2B8" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M60 250h280" stroke="#5a3417" stroke-width="6" stroke-linecap="round" opacity=".4"/></svg>'''

def svg_croissant(c1="#D99A4E", c2="#A86A2A"):
    return f'''<svg viewBox="0 0 400 300"><path d="M70 200c0-90 70-140 150-140s130 60 130 130c0 20-30 10-40-10-20-50-50-70-90-70s-70 30-80 70c-10 30-70 40-70 20z" fill="{c1}"/>
<path d="M120 190c10-40 40-70 80-70M200 120c40 0 70 20 90 60" stroke="{c2}" stroke-width="10" fill="none" stroke-linecap="round"/></svg>'''

def svg_scissors(c="#C8A24A"):
    return f'''<svg viewBox="0 0 400 300"><g stroke="{c}" stroke-width="14" fill="none" stroke-linecap="round">
<circle cx="110" cy="210" r="40"/><circle cx="110" cy="90" r="40"/><path d="M145 180L330 95M145 120L330 205"/></g>
<circle cx="330" cy="95" r="12" fill="{c}"/><circle cx="330" cy="205" r="12" fill="{c}"/></svg>'''

def svg_comb(c="#C8A24A"):
    return f'''<svg viewBox="0 0 400 300"><rect x="40" y="120" width="320" height="60" rx="14" fill="{c}"/>
<g fill="{c}">{''.join(f'<rect x="{60+i*26}" y="180" width="12" height="50" rx="4"/>' for i in range(12))}</g></svg>'''

def svg_flowers(p="#E85D8A", p2="#F4A7C0", s="#5E7B5A"):
    f = ""
    for x, h, col in ((110, 120, p), (200, 80, p2), (290, 130, p), (160, 160, p2), (250, 150, p)):
        f += f'<path d="M{x} 300V{h+40}" stroke="{s}" stroke-width="10" stroke-linecap="round"/>'
        f += f'<ellipse cx="{x-26}" cy="{h+60}" rx="22" ry="10" fill="{s}" transform="rotate(-30 {x-26} {h+60})"/>'
        for a in range(0, 360, 72):
            f += f'<ellipse cx="{x}" cy="{h-26}" rx="14" ry="30" fill="{col}" transform="rotate({a} {x} {h})"/>'
        f += f'<circle cx="{x}" cy="{h}" r="14" fill="#FFD23F"/>'
    return f'<svg viewBox="0 0 400 300">{f}</svg>'

def svg_car(body="#F5C400", dark="#1D232C"):
    return f'''<svg viewBox="0 0 400 300"><path d="M40 200v-40l40-20 40-60h140l60 60h50v60z" fill="{body}"/>
<path d="M130 140l30-45h100l45 45z" fill="#BFD8E8"/><rect x="30" y="200" width="340" height="16" fill="{dark}"/>
<circle cx="120" cy="212" r="34" fill="{dark}"/><circle cx="120" cy="212" r="14" fill="#9aa3ad"/>
<circle cx="300" cy="212" r="34" fill="{dark}"/><circle cx="300" cy="212" r="14" fill="#9aa3ad"/></svg>'''

def svg_wrench(c="#F5C400"):
    return f'''<svg viewBox="0 0 400 300"><g transform="rotate(-40 200 150)"><rect x="90" y="130" width="220" height="40" rx="10" fill="{c}"/>
<circle cx="90" cy="150" r="46" fill="{c}"/><rect x="60" y="120" width="40" height="60" fill="#0000" stroke="#1D232C" stroke-width="0"/>
<rect x="70" y="135" width="46" height="30" fill="#2B3340"/></g></svg>'''

def svg_fries(cone="#D7262B", fry="#FFD23F"):
    return f'''<svg viewBox="0 0 400 300">{''.join(f'<rect x="{120+i*28}" y="{60+(i%3)*18}" width="20" height="150" rx="6" fill="{fry}" transform="rotate({(i-4)*4} 200 220)"/>' for i in range(7))}
<path d="M100 150h200l-30 140H130z" fill="{cone}"/><path d="M110 170h180" stroke="#fff" stroke-width="10" opacity=".7"/></svg>'''

def svg_burger(bun="#E8A84B", meat="#6B3A1E", cheese="#FFD23F", salad="#5BB04D"):
    return f'''<svg viewBox="0 0 400 300"><path d="M90 130c0-50 50-80 110-80s110 30 110 80z" fill="{bun}"/>
<rect x="80" y="130" width="240" height="22" rx="11" fill="{salad}"/><rect x="90" y="152" width="220" height="26" rx="6" fill="{meat}"/>
<path d="M85 178h230l-20 20H105z" fill="{cheese}"/><rect x="90" y="198" width="220" height="40" rx="20" fill="{bun}"/></svg>'''

def svg_map(street="#fff", road="#D9D4C7", pin="#E03A2F", bg="#EDE9DF"):
    roads = "".join(f'<rect x="0" y="{40+i*60}" width="400" height="14" fill="{street}"/>' for i in range(4))
    roads += "".join(f'<rect x="{50+i*90}" y="0" width="14" height="260" fill="{street}"/>' for i in range(4))
    return f'''<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice"><rect width="400" height="260" fill="{bg}"/>
<rect x="150" y="60" width="90" height="70" fill="#CFE3C4"/>{roads}
<rect x="100" y="140" width="40" height="40" fill="{road}"/><rect x="290" y="80" width="60" height="50" fill="{road}"/>
<path d="M200 170c-30-40-40-60-40-80a40 40 0 0180 0c0 20-10 40-40 80z" fill="{pin}"/><circle cx="200" cy="90" r="16" fill="#fff"/></svg>'''

def stars(col="#F5B301", n=5):
    return f'<span class="stars" style="color:{col}">{"★"*n}</span>'

def ig_tiles(cols, icon_fn):
    return '<div class="ig">' + "".join(f'<div style="background:{c}">{icon_fn(i)}</div>' for i, c in enumerate(cols)) + "</div>"


# ---------- teksten ----------
TX = {
 "nl": dict(
  hours="Openingsuren", reviews="Wat klanten zeggen", find="Hier vindt u ons", order="Bestel", book="Reserveer", menu="Menu", contact="Contact",
  days=["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"], closed="gesloten", route="Route", call="Bel ons",
  bak=dict(name="Bakkerij Vanhove", city="Gent", nav=["Brood", "Gebak", "Bestellen"], h1="Elke nacht gebakken, elke ochtend vers.", p="Zuurdesem, boerenbrood en koffiekoeken sinds 1987. Bestel voor 18 u, haal morgen af.",
           btn="Bestel voor morgen", sec="Deze week in de toog", items=[("Boerenbrood", "4,20 €"), ("Zuurdesem", "5,10 €"), ("Croissant", "1,40 €"), ("Rijsttaart", "14 €")],
           rev=("Het beste brood van Gent. En de rijsttaart... zeg maar niets.", "Lien D., Gentbrugge"), addr="Dampoortstraat 112, 9000 Gent", hrs=["6:30-18:00"]*5+["6:30-14:00", "gesloten"]),
  bar=dict(name="Atelier 12", city="Namen", nav=["Diensten", "Team", "Reserveren"], h1="Knippen. Baard. Klaar.", p="Barbier in hartje Namen. Reserveer online en wacht nooit meer.",
           btn="Reserveer een plek", sec="Prijzen", items=[("Knippen", "25 €"), ("Baard trimmen", "15 €"), ("Knippen + baard", "35 €"), ("Klassiek scheren", "20 €")],
           slots=["10:00", "10:45", "11:30", "14:00", "14:45", "16:15"], today="Vandaag vrij", rev=("Strak werk, op tijd, en goede koffie erbij.", "Mehdi K."), addr="Rue de Fer 12, 5000 Namur", hrs=["gesloten", "9:00-18:30", "9:00-18:30", "9:00-20:00", "9:00-18:30", "8:30-17:00", "gesloten"]),
  flo=dict(name="Fleurs de Julie", city="Bergen", nav=["Boeketten", "Huwelijk", "Atelier"], h1="Bloemen die iets zeggen.", p="Seizoensbloemen van kwekers uit de streek. Dezelfde dag geleverd in Bergen.",
           btn="Stel een boeket samen", sec="Favorieten van de week", items=[("Boeket van de dag", "25 €"), ("Wilde tuin", "39 €"), ("Pioenen", "45 €"), ("Droogbloemen", "29 €")],
           rev=("Mijn moeder belde in tranen. Dat zegt genoeg.", "Sofie V."), addr="Rue d'Havré 7, 7000 Mons", deliv="Levering vandaag bij bestelling voor 14 u", hrs=["gesloten"]+["9:30-18:00"]*4+["9:00-17:00", "9:00-12:30"]),
  gar=dict(name="Garage Peeters", city="Hasselt", nav=["Onderhoud", "Banden", "Afspraak"], h1="Uw auto, zonder verrassingen.", p="Onderhoud, banden en keuring. Altijd een duidelijke prijs voor we beginnen.",
           btn="Maak een afspraak", sec="Onze diensten", items=[("Klein onderhoud", "vanaf 149 €"), ("Banden wisselen", "49 €"), ("Pre-keuring", "49 €"), ("Diagnose", "39 €")],
           checks=["Offerte vooraf", "Vervangwagen", "Alle merken", "Erkend keuringsklaar"], rev=("Eerlijk, snel en ze leggen alles uit. Eindelijk een garage die ik vertrouw.", "Tom W., Zonhoven"), addr="Kempische Steenweg 304, 3500 Hasselt", hrs=["8:00-17:30"]*5+["8:30-12:00", "gesloten"]),
  fri=dict(name="Frituur Chez Mo", city="Luik", nav=["Kaart", "Afhalen", "Waar"], h1="De echte Luikse friet.", p="Twee keer gebakken in rundvet. Boulet sauce lapin van de chef. Open tot 23 u.",
           btn="Bestel om af te halen", sec="Toppers", items=[("Grote friet", "3,50 €"), ("Boulet sauce lapin", "6 €"), ("Mitraillette", "8 €"), ("Frikandel speciaal", "3 €")],
           open="Nu open, tot 23:00", rev=("Beste boulet van Luik, en ik heb ze allemaal geprobeerd.", "Jean-Luc P."), addr="Place du Marché 3, 4000 Liège", hrs=["gesloten"]+["11:30-23:00"]*5+["17:00-23:00"]),
 ),
 "fr": dict(
  hours="Heures d'ouverture", reviews="Ce que disent les clients", find="Nous trouver", order="Commander", book="Réserver", menu="Carte", contact="Contact",
  days=["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"], closed="fermé", route="Itinéraire", call="Appelez-nous",
  bak=dict(name="Boulangerie Vanhove", city="Gand", nav=["Pains", "Pâtisserie", "Commander"], h1="Cuit chaque nuit, frais chaque matin.", p="Levain, pain de campagne et viennoiseries depuis 1987. Commandez avant 18 h, retirez demain.",
           btn="Commander pour demain", sec="Cette semaine en vitrine", items=[("Pain de campagne", "4,20 €"), ("Levain", "5,10 €"), ("Croissant", "1,40 €"), ("Tarte au riz", "14 €")],
           rev=("Le meilleur pain de Gand. Et la tarte au riz... je ne dis rien.", "Lien D., Gentbrugge"), addr="Dampoortstraat 112, 9000 Gand", hrs=["6:30-18:00"]*5+["6:30-14:00", "fermé"]),
  bar=dict(name="Atelier 12", city="Namur", nav=["Services", "Équipe", "Réserver"], h1="Coupe. Barbe. Terminé.", p="Barbier au cœur de Namur. Réservez en ligne et n'attendez plus jamais.",
           btn="Réserver une place", sec="Tarifs", items=[("Coupe", "25 €"), ("Taille de barbe", "15 €"), ("Coupe + barbe", "35 €"), ("Rasage à l'ancienne", "20 €")],
           slots=["10:00", "10:45", "11:30", "14:00", "14:45", "16:15"], today="Libre aujourd'hui", rev=("Travail net, à l'heure, et un bon café en prime.", "Mehdi K."), addr="Rue de Fer 12, 5000 Namur", hrs=["fermé", "9:00-18:30", "9:00-18:30", "9:00-20:00", "9:00-18:30", "8:30-17:00", "fermé"]),
  flo=dict(name="Fleurs de Julie", city="Mons", nav=["Bouquets", "Mariage", "Atelier"], h1="Des fleurs qui disent quelque chose.", p="Fleurs de saison de producteurs de la région. Livrées le jour même à Mons.",
           btn="Composer un bouquet", sec="Les favoris de la semaine", items=[("Bouquet du jour", "25 €"), ("Jardin sauvage", "39 €"), ("Pivoines", "45 €"), ("Fleurs séchées", "29 €")],
           rev=("Ma mère a appelé en larmes. Ça dit tout.", "Sofie V."), addr="Rue d'Havré 7, 7000 Mons", deliv="Livraison aujourd'hui si commande avant 14 h", hrs=["fermé"]+["9:30-18:00"]*4+["9:00-17:00", "9:00-12:30"]),
  gar=dict(name="Garage Peeters", city="Hasselt", nav=["Entretien", "Pneus", "Rendez-vous"], h1="Votre voiture, sans surprises.", p="Entretien, pneus et contrôle technique. Toujours un prix clair avant de commencer.",
           btn="Prendre rendez-vous", sec="Nos services", items=[("Petit entretien", "dès 149 €"), ("Changement de pneus", "49 €"), ("Pré-contrôle", "49 €"), ("Diagnostic", "39 €")],
           checks=["Devis avant travaux", "Voiture de remplacement", "Toutes marques", "Prêt pour le contrôle"], rev=("Honnête, rapide, et ils expliquent tout. Enfin un garage de confiance.", "Tom W., Zonhoven"), addr="Kempische Steenweg 304, 3500 Hasselt", hrs=["8:00-17:30"]*5+["8:30-12:00", "fermé"]),
  fri=dict(name="Friterie Chez Mo", city="Liège", nav=["Carte", "À emporter", "Où"], h1="La vraie frite liégeoise.", p="Cuite deux fois dans la graisse de bœuf. Boulet sauce lapin du chef. Ouvert jusqu'à 23 h.",
           btn="Commander à emporter", sec="Les incontournables", items=[("Grande frite", "3,50 €"), ("Boulet sauce lapin", "6 €"), ("Mitraillette", "8 €"), ("Fricadelle spéciale", "3 €")],
           open="Ouvert, jusqu'à 23:00", rev=("Meilleur boulet de Liège, et je les ai tous essayés.", "Jean-Luc P."), addr="Place du Marché 3, 4000 Liège", hrs=["fermé"]+["11:30-23:00"]*5+["17:00-23:00"]),
 ),
}


def hours_rows(days, hrs, style):
    return "".join(f'<div style="display:flex;justify-content:space-between;{style}"><span>{d}</span><span>{h}</span></div>' for d, h in zip(days, hrs))


# ---------- 1. Bakkerij: warm, serif, rustiek ----------
def site_bak(t, d):
    items = "".join(f'''<div style="background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(74,44,26,.12)">
      <div class="ph" style="height:170px;background:{"#F0D9A8" if i%2 else "#E7C78F"}">{svg_bread() if i%2==0 else svg_croissant()}</div>
      <div style="padding:18px 20px"><div style="font-family:Playfair;font-size:30px;color:#4A2C1A">{n}</div><div style="font-family:Lora;font-size:26px;color:#C9622B;margin-top:4px">{p}</div></div></div>'''
                    for i, (n, p) in enumerate(d["items"]))
    return f'''<div class="site" style="background:#F6EEDC;color:#4A2C1A;font-family:Lora,serif">
<div style="display:flex;justify-content:space-between;align-items:center;padding:36px 40px;background:#F6EEDC">
  <div style="font-family:Playfair;font-size:38px">Vanhove <span style="color:#C9622B">·</span> 1987</div>
  <div style="display:flex;gap:22px;font-size:24px">{''.join(f'<span>{n}</span>' for n in d["nav"])}</div></div>
<div class="ph" style="height:520px;background:radial-gradient(circle at 30% 30%,#F3D7A0,#C9874A 70%,#8E4F22)"><div style="position:absolute;inset:40px 60px 0">{svg_bread("#D99A4E","#8E4F22")}</div>
  <div style="position:absolute;left:30px;bottom:30px;background:#F6EEDC;padding:10px 22px;border-radius:999px;font-size:24px;font-weight:700">★ 4,9 · 212 Google-reviews</div></div>
<div style="padding:50px 40px 30px;text-align:center"><h1 style="font-family:Playfair;font-size:72px;line-height:1.05;margin:0">{d["h1"]}</h1>
  <p style="font-size:29px;margin:24px auto 0;max-width:580px;line-height:1.4">{d["p"]}</p>
  <div style="display:inline-block;margin-top:34px;background:#C9622B;color:#fff;padding:24px 50px;border-radius:999px;font-size:30px;font-weight:700">{d["btn"]}</div></div>
<div style="padding:30px 40px"><div style="font-family:Playfair;font-size:40px;margin-bottom:22px">{d["sec"]}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">{items}</div></div>
<div style="margin:30px 40px;padding:40px;background:#4A2C1A;color:#F6EEDC;border-radius:24px;font-style:italic;font-size:30px;line-height:1.4">{stars()}<br>“{d["rev"][0]}”<div style="font-style:normal;font-size:24px;margin-top:14px;opacity:.8">{d["rev"][1]}</div></div>
<div style="padding:20px 40px 40px;display:grid;grid-template-columns:1fr 1fr;gap:24px;font-size:24px">
  <div><div style="font-family:Playfair;font-size:32px;margin-bottom:12px">{t["hours"]}</div>{hours_rows(t["days"], d["hrs"], "padding:6px 0;border-bottom:1px solid #E2CFA8")}</div>
  <div><div style="font-family:Playfair;font-size:32px;margin-bottom:12px">{t["find"]}</div><div class="map" style="height:230px;border-radius:16px">{svg_map(pin="#C9622B")}</div><div style="margin-top:12px">{d["addr"]}</div></div></div>
<div style="background:#4A2C1A;color:#F6EEDC;padding:40px;font-size:22px;display:flex;justify-content:space-between"><span>© Bakkerij Vanhove</span><span>{d["addr"].split(',')[0]}</span></div></div>'''


# ---------- 2. Barbier: donker, goud, condensed ----------
def site_bar(t, d):
    prices = "".join(f'<div style="display:flex;align-items:baseline;gap:10px;padding:18px 0;border-bottom:1px solid #2a2a2a;font-size:28px"><span>{n}</span><span style="flex:1;border-bottom:2px dotted #444;transform:translateY(-8px)"></span><span style="color:#C8A24A;font-family:Oswald;font-size:32px">{p}</span></div>' for n, p in d["items"])
    slots = "".join(f'<span style="border:2px solid {"#C8A24A" if i==1 else "#444"};color:{"#111" if i==1 else "#eee"};background:{"#C8A24A" if i==1 else "transparent"};padding:14px 0;text-align:center;font-family:Oswald;font-size:26px">{s}</span>' for i, s in enumerate(d["slots"]))
    return f'''<div class="site" style="background:#111;color:#eee;font-family:InterT,sans-serif">
<div style="display:flex;justify-content:space-between;align-items:center;padding:34px 40px;border-bottom:1px solid #2a2a2a">
  <div style="font-family:Oswald;font-size:40px;letter-spacing:.08em;color:#C8A24A">ATELIER 12</div><div style="display:flex;gap:22px;font-size:22px;text-transform:uppercase;letter-spacing:.1em">{''.join(f'<span>{n}</span>' for n in d["nav"])}</div></div>
<div class="ph" style="height:560px;background:linear-gradient(160deg,#2b2b2b,#0c0c0c)"><div style="position:absolute;inset:60px 90px 40px">{svg_scissors()}</div>
  <div style="position:absolute;left:40px;top:40px;font-family:Oswald;font-size:22px;letter-spacing:.3em;color:#C8A24A">BARBIER · NAMUR</div></div>
<div style="padding:50px 40px 20px"><h1 style="font-family:Oswald;font-size:96px;line-height:.95;margin:0;text-transform:uppercase">{d["h1"]}</h1>
  <p style="font-size:28px;color:#bbb;margin:26px 0 0;max-width:560px">{d["p"]}</p>
  <div style="display:inline-block;margin-top:34px;background:#C8A24A;color:#111;padding:24px 46px;font-family:Oswald;font-size:30px;text-transform:uppercase;letter-spacing:.08em">{d["btn"]}</div></div>
<div style="padding:40px 40px 10px"><div style="font-family:Oswald;font-size:26px;letter-spacing:.3em;color:#C8A24A;margin-bottom:16px">{d["today"].upper()}</div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">{slots}</div></div>
<div style="padding:40px"><div style="font-family:Oswald;font-size:26px;letter-spacing:.3em;color:#C8A24A;margin-bottom:6px">{d["sec"].upper()}</div>{prices}</div>
<div style="margin:0 40px;display:grid;grid-template-columns:1fr 1fr;gap:14px"><div class="ph" style="height:240px;background:#1d1d1d">{svg_comb()}</div><div class="ph" style="height:240px;background:#C8A24A">{svg_scissors("#111")}</div></div>
<div style="padding:40px;font-size:28px;line-height:1.4;color:#ddd">{stars("#C8A24A")}<br>“{d["rev"][0]}”<div style="font-size:22px;color:#888;margin-top:10px">{d["rev"][1]}</div></div>
<div style="padding:0 40px 40px;display:grid;grid-template-columns:1fr 1fr;gap:24px;font-size:22px;color:#bbb"><div><div style="font-family:Oswald;color:#C8A24A;font-size:24px;letter-spacing:.2em;margin-bottom:10px">{t["hours"].upper()}</div>{hours_rows(t["days"], d["hrs"], "padding:5px 0")}</div>
  <div><div style="font-family:Oswald;color:#C8A24A;font-size:24px;letter-spacing:.2em;margin-bottom:10px">{t["find"].upper()}</div><div class="map" style="height:200px;filter:invert(.92) hue-rotate(180deg)">{svg_map(pin="#3a5dd6")}</div><div style="margin-top:10px">{d["addr"]}</div></div></div>
<div style="padding:34px 40px;border-top:1px solid #2a2a2a;font-size:20px;color:#777;letter-spacing:.1em">ATELIER 12 · {d["addr"].upper()}</div></div>'''


# ---------- 3. Bloemist: zacht, rond, pastel ----------
def site_flo(t, d):
    cols = ["#FADCE4", "#E8F0E4", "#FFF1D6", "#F3E3F7"]
    items = "".join(f'''<div style="background:{cols[i]};border-radius:28px;padding:16px 16px 20px"><div class="ph" style="height:190px;border-radius:20px;background:#fff">{svg_flowers(*(["#E85D8A","#F4A7C0"] if i%2==0 else ["#F28C28","#FFD23F"]))}</div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:14px"><span style="font-weight:800;font-size:27px">{n}</span><span style="font-size:26px;color:#5E7B5A;font-weight:800">{p}</span></div></div>''' for i, (n, p) in enumerate(d["items"]))
    return f'''<div class="site" style="background:#FFF8FA;color:#3B3B3B;font-family:Nunito,sans-serif">
<div style="display:flex;justify-content:space-between;align-items:center;padding:34px 40px"><div style="font-family:Lora;font-style:italic;font-size:40px;color:#5E7B5A">Fleurs de Julie</div><div style="display:flex;gap:20px;font-size:24px;font-weight:800">{''.join(f'<span>{n}</span>' for n in d["nav"])}</div></div>
<div style="margin:0 24px;border-radius:40px;overflow:hidden;background:#FADCE4"><div class="ph" style="height:480px">{svg_flowers()}</div>
  <div style="padding:40px 36px 44px"><h1 style="font-family:Lora;font-weight:400;font-size:66px;line-height:1.05;margin:0;color:#3B3B3B">{d["h1"]}</h1><p style="font-size:28px;margin:20px 0 0;line-height:1.4">{d["p"]}</p>
  <div style="display:inline-block;margin-top:30px;background:#5E7B5A;color:#fff;padding:22px 44px;border-radius:999px;font-weight:800;font-size:28px">{d["btn"]}</div></div></div>
<div style="margin:24px 24px 0;background:#E8F0E4;border-radius:999px;padding:18px 30px;font-size:24px;font-weight:800;color:#2F4A2C;text-align:center">🚲 {d["deliv"]}</div>
<div style="padding:44px 24px 10px"><div style="font-family:Lora;font-style:italic;font-size:42px;margin:0 16px 20px">{d["sec"]}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">{items}</div></div>
<div style="margin:30px 24px;padding:36px;background:#fff;border-radius:28px;border:3px solid #FADCE4;font-size:28px;line-height:1.4">{stars("#F28C28")}<br>“{d["rev"][0]}”<div style="font-size:23px;opacity:.7;margin-top:10px">{d["rev"][1]}</div></div>
{ig_tiles(["#E85D8A", "#5E7B5A", "#FFD23F", "#F4A7C0", "#F28C28", "#E8F0E4"], lambda i: svg_flowers("#fff", "#FFF8FA", "#2F4A2C") if i % 2 == 0 else svg_flowers("#E85D8A", "#F28C28", "#fff")).replace('class="ig"', 'class="ig" style="padding:0 24px"')}
<div style="padding:40px 24px;display:grid;grid-template-columns:1fr 1fr;gap:24px;font-size:23px"><div><div style="font-weight:800;font-size:28px;margin-bottom:10px">{t["hours"]}</div>{hours_rows(t["days"], d["hrs"], "padding:5px 0;border-bottom:2px dotted #FADCE4")}</div>
  <div><div style="font-weight:800;font-size:28px;margin-bottom:10px">{t["find"]}</div><div class="map" style="height:210px;border-radius:24px">{svg_map(pin="#E85D8A", bg="#F3EFE6")}</div><div style="margin-top:10px">{d["addr"]}</div></div></div>
<div style="background:#5E7B5A;color:#fff;padding:36px 40px;font-size:22px;border-radius:40px 40px 0 0">Fleurs de Julie · {d["addr"]}</div></div>'''


# ---------- 4. Garage: industrieel, hoekig, geel/staal ----------
def site_gar(t, d):
    cards = "".join(f'''<div style="background:#fff;border-left:10px solid #F5C400;padding:22px 24px;display:flex;justify-content:space-between;align-items:center"><div><div style="font-family:Barlow;font-size:34px;text-transform:uppercase">{n}</div><div style="font-size:22px;color:#667">{t["book"]} →</div></div><div style="font-family:Barlow;font-size:36px;color:#2B3340">{p}</div></div>''' for n, p in d["items"])
    checks = "".join(f'<div style="display:flex;gap:14px;align-items:center;font-size:26px;font-weight:700"><span style="width:36px;height:36px;background:#F5C400;color:#1D232C;display:grid;place-items:center;font-size:22px;flex:none">✓</span>{c}</div>' for c in d["checks"])
    return f'''<div class="site" style="background:#EEF0F3;color:#1D232C;font-family:InterT,sans-serif">
<div style="background:#1D232C;color:#fff;padding:30px 40px;display:flex;justify-content:space-between;align-items:center"><div style="font-family:Barlow;font-size:42px;text-transform:uppercase;letter-spacing:.02em"><span style="background:#F5C400;color:#1D232C;padding:2px 12px;margin-right:10px">GP</span>Garage Peeters</div><div style="display:flex;gap:20px;font-size:22px;text-transform:uppercase;font-family:Barlow">{''.join(f'<span>{n}</span>' for n in d["nav"])}</div></div>
<div style="background:#1D232C;color:#fff;padding:10px 40px 50px"><div class="ph" style="height:400px;background:repeating-linear-gradient(135deg,#2B3340 0 40px,#242b36 40px 80px)"><div style="position:absolute;inset:30px 60px 0">{svg_car()}</div></div>
  <h1 style="font-family:Barlow;font-size:92px;line-height:.95;text-transform:uppercase;margin:40px 0 0">{d["h1"]}</h1><p style="font-size:28px;color:#C9CFD8;margin:22px 0 0;max-width:580px">{d["p"]}</p>
  <div style="display:flex;gap:14px;margin-top:32px;flex-wrap:wrap"><div style="background:#F5C400;color:#1D232C;padding:22px 40px;font-family:Barlow;font-size:32px;text-transform:uppercase">{d["btn"]}</div><div style="border:3px solid #fff;padding:19px 34px;font-family:Barlow;font-size:32px;text-transform:uppercase">☎ {t["call"]}</div></div></div>
<div style="padding:44px 40px 10px"><div style="font-family:Barlow;font-size:40px;text-transform:uppercase;margin-bottom:18px">{d["sec"]}</div><div style="display:grid;gap:12px">{cards}</div></div>
<div style="margin:30px 40px;padding:34px;background:#F5C400;display:grid;grid-template-columns:1fr 1fr;gap:18px">{checks}</div>
<div style="margin:0 40px;display:grid;grid-template-columns:1fr 1fr;gap:14px"><div class="ph" style="height:230px;background:#2B3340">{svg_wrench()}</div><div style="background:#fff;padding:26px;font-size:26px;line-height:1.35">{stars()}<br>“{d["rev"][0]}”<div style="font-size:20px;color:#667;margin-top:8px">{d["rev"][1]}</div></div></div>
<div style="padding:40px;display:grid;grid-template-columns:1fr 1fr;gap:24px;font-size:23px"><div><div style="font-family:Barlow;font-size:30px;text-transform:uppercase;margin-bottom:10px">{t["hours"]}</div>{hours_rows(t["days"], d["hrs"], "padding:5px 0;border-bottom:1px solid #D5D9E0")}</div>
  <div><div style="font-family:Barlow;font-size:30px;text-transform:uppercase;margin-bottom:10px">{t["find"]}</div><div class="map" style="height:210px">{svg_map(pin="#F5C400", bg="#DDE1E7", street="#f7f8fa")}</div><div style="margin-top:10px">{d["addr"]}</div></div></div>
<div style="background:#1D232C;color:#9aa3ad;padding:34px 40px;font-size:22px;display:flex;justify-content:space-between"><span>Garage Peeters bv</span><span>BE 0456.789.123</span></div></div>'''


# ---------- 5. Frituur: speels, rood/geel ----------
def site_fri(t, d):
    items = "".join(f'''<div style="background:#fff;border-radius:22px;padding:14px;border:4px solid #FFD23F"><div class="ph" style="height:160px;border-radius:14px;background:{"#FFE9A8" if i%2==0 else "#FFD6D6"}">{svg_fries() if i%2==0 else svg_burger()}</div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:12px;gap:8px"><span style="font-weight:800;font-size:25px;line-height:1.1">{n}</span><span style="font-family:Lilita;font-size:32px;color:#D7262B;white-space:nowrap">{p}</span></div></div>''' for i, (n, p) in enumerate(d["items"]))
    return f'''<div class="site" style="background:#FFF4D6;color:#2A1A10;font-family:Nunito,sans-serif">
<div style="background:#D7262B;color:#fff;padding:30px 40px;display:flex;justify-content:space-between;align-items:center"><div style="font-family:Lilita;font-size:46px;letter-spacing:.01em">Chez Mo</div><div style="display:flex;gap:20px;font-size:24px;font-weight:800">{''.join(f'<span>{n}</span>' for n in d["nav"])}</div></div>
<div class="ph" style="height:500px;background:#D7262B"><div style="position:absolute;inset:30px 80px 0">{svg_fries(cone="#FFF4D6")}</div><div style="position:absolute;right:30px;top:30px;background:#D7262B;color:#fff;padding:14px 24px;border-radius:999px;font-weight:800;font-size:24px;transform:rotate(6deg)">● {d["open"]}</div></div>
<div style="padding:46px 40px 20px"><h1 style="font-family:Lilita;font-size:88px;line-height:.98;margin:0;color:#D7262B">{d["h1"]}</h1><p style="font-size:28px;margin:22px 0 0;max-width:580px;line-height:1.4">{d["p"]}</p>
  <div style="display:inline-block;margin-top:30px;background:#D7262B;color:#fff;padding:24px 46px;border-radius:999px;font-family:Lilita;font-size:32px;box-shadow:0 8px 0 #9d1a1e">{d["btn"]}</div></div>
<div style="padding:30px 40px 10px"><div style="font-family:Lilita;font-size:44px;margin-bottom:18px">{d["sec"]}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">{items}</div></div>
<div style="margin:34px 40px;padding:34px;background:#D7262B;color:#fff;border-radius:26px;font-size:28px;line-height:1.4;transform:rotate(-1deg)">{stars("#FFD23F")}<br>“{d["rev"][0]}”<div style="font-size:22px;opacity:.85;margin-top:10px">{d["rev"][1]}</div></div>
<div style="padding:10px 40px 40px;display:grid;grid-template-columns:1fr 1fr;gap:24px;font-size:23px"><div><div style="font-family:Lilita;font-size:32px;margin-bottom:10px">{t["hours"]}</div>{hours_rows(t["days"], d["hrs"], "padding:5px 0;border-bottom:2px dashed #F2C56B")}</div>
  <div><div style="font-family:Lilita;font-size:32px;margin-bottom:10px">{t["find"]}</div><div class="map" style="height:210px;border-radius:20px">{svg_map(pin="#D7262B", bg="#FBEFCB", street="#fff")}</div><div style="margin-top:10px">{d["addr"]}</div></div></div>
<div style="background:#2A1A10;color:#FFD23F;padding:36px 40px;font-family:Lilita;font-size:26px;display:flex;justify-content:space-between"><span>Chez Mo</span><span>Liège · 04 222 10 10</span></div></div>'''


def sites_html(lang):
    t = TX[lang]
    out = []
    for key, fn in (("bak", site_bak), ("bar", site_bar), ("flo", site_flo), ("gar", site_gar), ("fri", site_fri)):
        d = t[key]
        out.append((d["name"], d["city"], fn(t, d)))
    return out
