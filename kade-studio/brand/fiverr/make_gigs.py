"""Gig-afbeeldingen voor Fiverr (1280x769). Genereert gig-1..3.html; renderen met render_gigs.js.
Opbouw per beeld (marketing): 1 = wat je krijgt in één oogopslag (merk + site-structuren),
2 = waarom bij Kade (zes troeven als iconen), 3 = pakketten met de middelste als aanrader."""
import json
import math
from pathlib import Path

HERE = Path(__file__).parent
B = HERE.parent
logo = (B / "logo/kade-logo.svg").read_text()
cur = json.loads((B / "video/source/cursors.json").read_text())


def star(n=14, r=.76):
    pts = []
    for i in range(2 * n):
        rr = 50 if i % 2 == 0 else 50 * r
        a = math.pi * i / n - math.pi / 2
        pts.append(f"{50+rr*math.cos(a):.1f}% {50+rr*math.sin(a):.1f}%")
    return "polygon(" + ",".join(pts) + ")"


CSS = f"""
@font-face{{font-family:BS;src:url(../../fonts/big-shoulders-var-latin.woff2);font-weight:800 900}}
@font-face{{font-family:BR;src:url(../../fonts/bricolage-400-800-latin.woff2);font-weight:400 800}}
@font-face{{font-family:CP;src:url(../../fonts/courier-prime-700-latin.woff2);font-weight:700}}
:root{{--acid:#74DB4B;--tomato:#FF5426;--sun:#FFD43A;--bubble:#FFB8E0;--cobalt:#3B6BFF;--ink:#151515;--paper:#F1F2EC;--white:#fff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1280px;height:769px;overflow:hidden;font-family:BR,sans-serif;color:var(--ink)}}
.f{{position:relative;width:1280px;height:769px;overflow:hidden}}
.f::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.12;mix-blend-mode:multiply;z-index:40;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .9 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
.abs{{position:absolute}}
.logo svg{{width:100%;height:auto;display:block}}
.poster{{font-family:BS;font-weight:900;text-transform:uppercase;line-height:.84}}
.disp{{font-family:BR;font-weight:800;letter-spacing:-.025em;line-height:.95;font-variation-settings:"wdth" 75,"opsz" 96}}
.mono{{font-family:CP;font-weight:700}}
.band{{left:0;right:0;height:52px;background:var(--sun);border-block:5px solid var(--ink);white-space:nowrap;font-family:BS;font-weight:900;text-transform:uppercase;font-size:27px;display:flex;align-items:center;gap:26px;padding-left:20px;overflow:hidden}}
.band span::after{{content:" ✶";color:var(--tomato)}}
.burst{{display:grid;place-items:center;text-align:center;background:var(--white);clip-path:{star()};font-family:BS;font-weight:900;text-transform:uppercase;line-height:.92}}
.bsh{{background:var(--ink);clip-path:{star()}}}
/* wireframes: website-structuren zonder tekst */
.win{{position:absolute;background:var(--white);border:5px solid var(--ink);box-shadow:12px 12px 0 var(--ink);overflow:hidden}}
.win .bar{{height:34px;background:var(--paper);border-bottom:5px solid var(--ink);display:flex;align-items:center;gap:8px;padding:0 12px}}
.win .bar i{{width:14px;height:14px;border-radius:50%;border:3px solid var(--ink);display:block}}
.win .bar u{{flex:1;height:14px;margin-left:12px;background:#fff;border:3px solid var(--ink);border-radius:999px}}
.nav{{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:4px solid var(--ink)}}
.nav b{{width:46px;height:16px;background:var(--ink);display:block}}
.nav s{{flex:1}}
.nav i{{width:34px;height:10px;background:var(--ink);opacity:.35;display:block;border-radius:999px}}
.nav em{{width:60px;height:22px;background:var(--tomato);border:3px solid var(--ink);border-radius:999px;display:block}}
.ln{{height:12px;background:var(--ink);border-radius:999px}}
.ln.l{{opacity:.3;height:8px}}
.btn{{height:26px;border:3px solid var(--ink);border-radius:999px;background:var(--tomato);box-shadow:4px 4px 0 var(--ink)}}
.img{{border:3px solid var(--ink);position:relative;overflow:hidden}}
.img::after{{content:"";position:absolute;inset:auto 0 0 0;height:50%;background-image:radial-gradient(circle,rgba(21,21,21,.5) 1.6px,transparent 2px);background-size:8px 8px;-webkit-mask-image:linear-gradient(to top,#000,transparent);mask-image:linear-gradient(to top,#000,transparent)}}
.phone{{position:absolute;background:var(--ink);border-radius:34px;padding:10px;box-shadow:12px 12px 0 rgba(21,21,21,.25)}}
.phone .scr{{background:var(--white);border-radius:26px;overflow:hidden;height:100%}}
.tile{{background:var(--white);border:5px solid var(--ink);box-shadow:10px 10px 0 var(--ink);padding:22px 24px;display:flex;flex-direction:column;gap:14px}}
.tile .ic{{width:64px;height:64px;display:grid;place-items:center}}
.tile .ic svg{{width:64px;height:64px}}
.tile h3{{font-size:30px;font-weight:800;line-height:1.05;letter-spacing:-.02em}}
.tile p{{font-size:21px;line-height:1.25;font-weight:500;color:#333}}
.pk{{flex:1;border:6px solid var(--ink);padding:30px 28px;display:flex;flex-direction:column;gap:14px;position:relative}}
.pk .n{{font-family:BS;font-weight:900;text-transform:uppercase;font-size:36px;line-height:.9}}
.pk .p{{font-family:BS;font-weight:900;font-size:86px;line-height:.9;font-variant-numeric:tabular-nums}}
.pk .d{{font-size:21px;line-height:1.35;font-weight:600;border-top:3px solid currentColor;padding-top:14px}}
.pk .d div::before{{content:"✓ "}}
"""

BAND = '<div class="abs band" style="top:0;border-top:0">' + "".join(
    f"<span>{x}</span>" for x in ["Websites for small businesses", "EN · NL · FR", "Fixed price", "Delivered in 3 weeks"] * 2) + "</div>"


def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="f">{body}</div></body></html>'


def lines(widths, gap=8, light=False):
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px">' + "".join(f'<div class="ln{" l" if light else ""}" style="width:{w}%"></div>' for w in widths) + "</div>"


# browservenster met een site-structuur (hero, drie kaarten, knop)
def window(x, y, w, h, hero, c1, c2, c3, rot=0):
    return f'''<div class="win" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">
  <div class="bar"><i></i><i></i><i></i><u></u></div>
  <div class="nav"><b></b><s></s><i></i><i></i><i></i><em></em></div>
  <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:18px;padding:22px 20px;align-items:center">
    <div style="display:flex;flex-direction:column;gap:14px">{lines([92, 70])}{lines([100, 86, 60], 6, True)}<div class="btn" style="width:120px;margin-top:6px"></div></div>
    <div class="img" style="height:150px;background:{hero}"></div></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:0 20px 20px">
    <div class="img" style="height:96px;background:{c1}"></div><div class="img" style="height:96px;background:{c2}"></div><div class="img" style="height:96px;background:{c3}"></div></div>
  <div style="padding:0 20px 20px;display:flex;flex-direction:column;gap:10px">{lines([40, 100, 90, 70], 6, True)}</div>
</div>'''


# gsm met een site-structuur
def phone(x, y, w, h, hero, c1, c2, rot=0):
    return f'''<div class="phone" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)"><div class="scr">
  <div class="nav" style="padding:16px 14px"><b></b><s></s><i style="width:22px;height:4px;box-shadow:0 7px 0 var(--ink),0 -7px 0 var(--ink);opacity:1;border-radius:0"></i></div>
  <div style="padding:16px 14px;display:flex;flex-direction:column;gap:12px">{lines([95, 75], 7)}{lines([100, 80], 5, True)}<div class="btn" style="width:100px"></div></div>
  <div class="img" style="margin:0 14px;height:120px;background:{hero}"></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:14px"><div class="img" style="height:70px;background:{c1}"></div><div class="img" style="height:70px;background:{c2}"></div></div>
  <div style="padding:0 14px 14px;display:flex;flex-direction:column;gap:8px">{lines([100, 100, 60], 5, True)}</div>
</div></div>'''


# ---------- beeld 1: merk + structuren ----------
g1 = (f'<div class="abs" style="inset:0;background:var(--acid)"></div>{BAND}'
      f'<div class="abs logo" style="left:60px;top:110px;width:520px">{logo}</div>'
      f'<h1 class="abs disp" style="left:64px;top:430px;width:560px;font-size:70px">Websites that <em style="font-style:normal;background:var(--ink);color:var(--acid);padding:0 .12em .05em;border-radius:.1em;display:inline-block;transform:rotate(-2deg)">stand out.</em></h1>'
      f'<p class="abs" style="left:66px;top:625px;width:520px;font-size:27px;font-weight:500;line-height:1.3">Custom design for shops, salons, trades and cafés.<br>English · Dutch · French.</p>'
      + window(640, 110, 540, 520, "var(--cobalt)", "var(--sun)", "var(--bubble)", "var(--tomato)", -3)
      + phone(1000, 330, 210, 420, "var(--tomato)", "var(--acid)", "var(--cobalt)", 5)
      + f'<div class="abs bsh" style="left:598px;top:548px;width:190px;height:190px"></div><div class="abs burst" style="left:590px;top:540px;width:190px;height:190px;font-size:34px;background:var(--sun)"><span style="transform:rotate(-8deg)">3 weeks<br>delivery</span></div>'
      f'<img class="abs" src="{cur["point2"]}" style="left:1120px;top:590px;width:64px;image-rendering:pixelated;z-index:30">')

# ---------- beeld 2: zes troeven als iconen ----------
ICONS = {
 "design": '<svg viewBox="0 0 64 64"><rect x="6" y="10" width="52" height="44" rx="4" fill="#fff" stroke="#151515" stroke-width="5"/><rect x="12" y="18" width="20" height="14" fill="#3B6BFF"/><rect x="36" y="18" width="16" height="5" fill="#151515"/><rect x="36" y="27" width="12" height="5" fill="#151515"/><rect x="12" y="38" width="40" height="5" fill="#FF5426"/></svg>',
 "copy": '<svg viewBox="0 0 64 64"><path d="M14 50L44 20l8 8-30 30H14z" fill="#FFD43A" stroke="#151515" stroke-width="5" stroke-linejoin="round"/><path d="M40 24l8 8" stroke="#151515" stroke-width="5"/><rect x="8" y="54" width="48" height="5" fill="#151515"/></svg>',
 "mobile": '<svg viewBox="0 0 64 64"><rect x="16" y="4" width="32" height="56" rx="6" fill="#fff" stroke="#151515" stroke-width="5"/><rect x="22" y="12" width="20" height="30" fill="#74DB4B"/><circle cx="32" cy="51" r="3" fill="#151515"/><path d="M4 30l6-6M4 36l10-10" stroke="#151515" stroke-width="4" stroke-linecap="round"/></svg>',
 "google": '<svg viewBox="0 0 64 64"><circle cx="26" cy="26" r="17" fill="#fff" stroke="#151515" stroke-width="6"/><path d="M39 39l18 18" stroke="#151515" stroke-width="8" stroke-linecap="round"/><path d="M18 26h16M26 18v16" stroke="#3B6BFF" stroke-width="5" stroke-linecap="round"/></svg>',
 "lang": '<svg viewBox="0 0 64 64"><path d="M6 12h34v26H22l-10 10V38H6z" fill="#FFB8E0" stroke="#151515" stroke-width="5" stroke-linejoin="round"/><path d="M26 24h32v22H46v8l-8-8H26z" fill="#fff" stroke="#151515" stroke-width="5" stroke-linejoin="round"/></svg>',
 "price": '<svg viewBox="0 0 64 64"><path d="M10 8h30l14 14v34H10z" fill="#fff" stroke="#151515" stroke-width="5" stroke-linejoin="round"/><path d="M40 8v14h14" fill="none" stroke="#151515" stroke-width="5"/><text x="20" y="48" font-family="Arial Black,Arial" font-weight="900" font-size="24" fill="#FF5426">€</text><path d="M34 36h12M34 44h12" stroke="#151515" stroke-width="4"/></svg>',
}
tiles = [("design", "Custom design", "Built for your trade, not from a template."),
         ("copy", "Copy included", "I write the texts, you approve them."),
         ("mobile", "Mobile-first", "Fast and readable on every phone."),
         ("google", "Found on Google", "Local SEO basics done right."),
         ("lang", "EN · NL · FR", "Bilingual sites, written natively."),
         ("price", "Fixed price", "Agreed before we start. No surprises.")]
g2 = (f'<div class="abs" style="inset:0;background:var(--ink)"></div>'
      f'<div class="abs" style="left:60px;top:56px;display:flex;align-items:flex-end;gap:30px;width:1160px">'
      f'<h2 class="poster" style="font-size:112px;color:transparent;-webkit-text-stroke:5px var(--acid);white-space:nowrap">What you get</h2>'
      f'<div class="logo" style="width:180px;margin-left:auto;margin-bottom:8px">{logo}</div></div>'
      f'<div class="abs" style="left:60px;top:220px;width:1160px;display:grid;grid-template-columns:repeat(3,1fr);gap:30px 34px">'
      + "".join(f'<div class="tile"><div class="ic">{ICONS[k]}</div><h3>{h}</h3><p>{p}</p></div>' for k, h, p in tiles)
      + '</div>'
      f'<div class="abs mono" style="left:66px;top:716px;font-size:24px;color:var(--acid)">kadestudio.be · Belgium · replies within a few hours</div>')

# ---------- beeld 3: pakketten ----------
pk = [("One page", "€ 350", ["1 page", "contact form + map", "7 days"], "var(--white)", "var(--ink)", ""),
      ("Business site", "€ 890", ["up to 6 pages", "copy written for you", "local SEO", "14 days"], "var(--sun)", "var(--ink)", "transform:translateY(-34px);box-shadow:14px 14px 0 var(--ink)"),
      ("Bilingual + shop", "€ 1 690", ["up to 8 pages", "second language", "booking or catalogue", "21 days"], "var(--cobalt)", "var(--white)", "")]
cards = "".join(f'<div class="pk" style="background:{bg};color:{fg};{ex}"><div class="n">{n}</div><div class="p">{p}</div><div class="d">{"".join(f"<div>{x}</div>" for x in d)}</div></div>' for n, p, d, bg, fg, ex in pk)
g3 = (f'<div class="abs" style="inset:0;background:var(--bubble)"></div>'
      f'<h2 class="abs poster" style="left:60px;top:56px;font-size:90px;white-space:nowrap">Fixed price. <span style="color:var(--tomato)">No jargon.</span></h2>'
      f'<p class="abs" style="left:64px;top:160px;font-size:26px;font-weight:600">Pick a package or message me for a custom offer.</p>'
      f'<div class="abs" style="left:60px;top:250px;width:1160px;display:flex;gap:30px;align-items:flex-start">{cards}</div>'
      f'<div class="abs bsh" style="left:748px;top:168px;width:140px;height:140px"></div><div class="abs burst" style="left:740px;top:160px;width:140px;height:140px;font-size:25px;background:var(--acid);z-index:5"><span style="transform:rotate(-10deg)">Most<br>popular</span></div>'
      f'<div class="abs mono" style="left:66px;top:716px;font-size:24px">Prices excl. VAT · message me before ordering · kadestudio.be</div>')

for n, b in (("gig-1", g1), ("gig-2", g2), ("gig-3", g3)):
    (HERE / f"{n}.html").write_text(page(b), encoding="utf-8")
print("ok")
