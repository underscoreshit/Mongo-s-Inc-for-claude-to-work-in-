"""Belgium Motor Homes Store, sticker direction.
Run: OUT=<dir> python3 gen2.py   (fonttools + uharfbuzz, fonts in ./fonts). All text is outlined."""
import os, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
OUT = os.environ.get('OUT', '/tmp/claude-0/bmh/out2')
os.makedirs(OUT, exist_ok=True)

INK = '#141414'
CREAM = '#F2EDE1'
ORANGE = '#FFD400'   # the accent is now yellow; variable name kept
WHITE = '#FFFFFF'

_fonts = {}
def font(name):
    if name not in _fonts:
        p = os.path.join(FD, name + '.ttf'); tt = TTFont(p)
        _fonts[name] = (hb.Font(hb.Face(open(p, 'rb').read())), tt, tt['head'].unitsPerEm, tt.getGlyphSet())
    return _fonts[name]

def text(s, fname, size, x=0, y=0, track=0.0, anchor='start', fill=INK):
    f, tt, upm, gs = font(fname)
    buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(f, buf, {'kern': True})
    sc = size / upm; order = tt.getGlyphOrder()
    adv = [p.x_advance * sc for p in buf.glyph_positions]; tr = track * size
    total = sum(adv) + tr * (len(adv) - 1)
    if anchor == 'middle': x -= total / 2
    elif anchor == 'end': x -= total
    pen = SVGPathPen(gs); cx = x
    for info, p, a in zip(buf.glyph_infos, buf.glyph_positions, adv):
        gs[order[info.codepoint]].draw(TransformPen(pen, (sc, 0, 0, -sc, cx + p.x_offset * sc, y - p.y_offset * sc)))
        cx += a + tr
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', total

def width(s, fname, size, track=0.0): return text(s, fname, size, track=track)[1]

def fit(s, fname, w, x, y, fill=INK, anchor='start', track=0.0):
    """Text sized so its width is exactly w. Returns (path, size)."""
    size = w / width(s, fname, 100, track) * 100
    return text(s, fname, size, x, y, track, anchor, fill)[0], size

def svg(w, h, body, label='Belgium Motor Homes Store', bg=None):
    b = f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" role="img" aria-label="{label}">{b}{body}</svg>')

def save(name, c): open(os.path.join(OUT, name), 'w').write(c)

# ---------- The sticker: the lettering IS the living box, cab on the left so it reads in order ----------
# 100-unit grid. Cab x 4..36, alcove over the cab, body x 38..98, chassis bar, two wheels.
CAB = 'M6 70V54Q6 48 10 46.5L14 45.5L21.5 35.5Q22.5 34 24.5 34H38V70Z'
ALCOVE = 'M8 34V24Q8 14 18 14H38V34Z'   # overcab bunk, hanging over the windscreen
BODY = 'M38 12H92Q98 12 98 18V64Q98 70 92 70H38Z'
CHASSIS = 'M6 70H98V76Q98 79 95 79H9Q6 79 6 76Z'
WHEELS = [(24, 79), (80, 79)]
WIN = 'M16 45.5L23.5 36.5H34.5V45.5Z'
SIDEWIN = 'M24 49H34.5V59H24Z'

def silhouette_strokes(t_out, t_in, out_col, in_col):
    """Sticker edge: a fat dark stroke, then a cream keyline, behind the whole shape."""
    parts = [CAB, ALCOVE, BODY, CHASSIS]
    def paths(col, w):
        s = ''.join(f'<path d="{d}" fill="{col}" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>' for d in parts)
        s += ''.join(f'<circle cx="{x}" cy="{y}" r="{9 + w/2}" fill="{col}"/>' for x, y in WHEELS)
        return s
    return paths(out_col, t_out) + paths(in_col, t_in)

BIG = os.environ.get('BIG', 'big-shoulders-display'); SMALL = os.environ.get('SMALL', 'big-shoulders-display')
def sticker(x=0, y=0, s=100, ink=INK, cream=CREAM, accent=ORANGE, edge=True, flat=False, bg_edge=None, body='accent', word=None):
    """flat=True drops the accent (one-colour use)."""
    acc = ink if flat else accent
    body = cream if (flat or body == 'cream') else (acc if body == 'accent' else body)   # the living-box panel
    word = ink if (flat or body == acc) else (word or acc)   # colour of HOMES
    g = []
    if edge:
        g.append(silhouette_strokes(9, 4.5, bg_edge or ink, cream))
    # cab, alcove, chassis dark; body cream
    g.append(f'<path d="{CAB}" fill="{ink}"/><path d="{ALCOVE}" fill="{ink}"/>')
    g.append(f'<path d="{BODY}" fill="{body}" stroke="{ink}" stroke-width="2.4"/>')
    g.append(f'<path d="{CHASSIS}" fill="{ink}"/>')
    g.append(f'<path d="{WIN}" fill="{cream}"/><path d="{SIDEWIN}" fill="{cream}"/>')
    for wx, wy in WHEELS:
        g.append(f'<circle cx="{wx}" cy="{wy}" r="9" fill="{ink}"/><circle cx="{wx}" cy="{wy}" r="4.2" fill="{cream}"/>'
                 f'<circle cx="{wx}" cy="{wy}" r="1.6" fill="{ink}"/>')
    # lettering
    p, _ = fit('BELGIUM', SMALL, 25, 23, 29, fill=cream, anchor='middle'); g.append(p)
    p, _ = fit('MOTOR', BIG, 54, 68, 41, fill=ink, anchor='middle'); g.append(p)
    p, _ = fit('HOMES', BIG, 54, 68, 65, fill=word, anchor='middle'); g.append(p)
    p, _ = fit('STORE', SMALL, 17, 52, 77.4, fill=cream, anchor='middle', track=.12); g.append(p)
    return f'<g transform="translate({x} {y}) scale({s/100})">{"".join(g)}</g>'

# ---------- Secondary marks ----------
def icon(x=0, y=0, s=100, ink=INK, cream=CREAM, accent=ORANGE, edge=True):
    """Just the vehicle, no words: app icon, favicon, stamp."""
    g = []
    if edge: g.append(silhouette_strokes(9, 4.5, ink, cream))
    g.append(f'<path d="{CAB}" fill="{ink}"/><path d="{ALCOVE}" fill="{ink}"/>')
    g.append(f'<path d="{BODY}" fill="{cream}" stroke="{ink}" stroke-width="2.4"/>')
    g.append(f'<path d="{CHASSIS}" fill="{ink}"/><path d="{WIN}" fill="{cream}"/><path d="{SIDEWIN}" fill="{cream}"/>')
    g.append(f'<rect x="46" y="24" width="16" height="12" rx="2" fill="{ink}"/><rect x="70" y="24" width="16" height="12" rx="2" fill="{ink}"/>')
    g.append(f'<path d="M38 50H98V58H38Z" fill="{accent}"/>')
    for wx, wy in WHEELS:
        g.append(f'<circle cx="{wx}" cy="{wy}" r="9" fill="{ink}"/><circle cx="{wx}" cy="{wy}" r="4.2" fill="{cream}"/>')
    return f'<g transform="translate({x} {y}) scale({s/100})">{"".join(g)}</g>'

def badge(x=0, y=0, s=100, ink=INK, cream=CREAM, accent=ORANGE):
    """Patch: rounded frame, vehicle, three lines of name, rules. 100 x 130."""
    g = [f'<rect x="3" y="3" width="94" height="124" rx="14" fill="{ink}"/>',
         f'<rect x="8.5" y="8.5" width="83" height="113" rx="10" fill="none" stroke="{cream}" stroke-width="2"/>',
         icon(18, 10, 64, ink, cream, accent, edge=False)]
    p, _ = fit('BELGIUM', SMALL, 60, 50, 80, fill=cream, anchor='middle'); g.append(p)
    p, _ = fit('MOTOR HOMES', SMALL, 72, 50, 97, fill=accent, anchor='middle'); g.append(p)
    p, _ = fit('STORE', SMALL, 40, 50, 112, fill=cream, anchor='middle', track=.1); g.append(p)
    g.append(f'<rect x="14" y="106" width="14" height="2.2" fill="{cream}"/><rect x="72" y="106" width="14" height="2.2" fill="{cream}"/>')
    g.append(f'<rect x="14" y="110.5" width="14" height="2.2" fill="{cream}"/><rect x="72" y="110.5" width="14" height="2.2" fill="{cream}"/>')
    return f'<g transform="translate({x} {y}) scale({s/100})">{"".join(g)}</g>'

def panel(label, x=0, y=0, h=40, ink=INK, cream=CREAM, accent=ORANGE, arrow=True):
    """Metro-style sign panel: arrow square + label. Returns (svg group, width)."""
    size = h * .5
    tw = width(label, BIG, size)
    w = (h if arrow else 0) + tw + h * .7
    g = [f'<rect width="{w:.1f}" height="{h}" rx="{h*.2}" fill="{ink}"/>']
    if arrow:
        g.append(f'<rect width="{h}" height="{h}" rx="{h*.2}" fill="{accent}"/>'
                 f'<path transform="translate({h*.5} {h*.5}) scale({h/40})" d="M-9 -9H9V9H4V-0.5L-5.5 9L-9 5.5L0.5 -4H-9Z" fill="{ink}"/>')
    p, _ = text(label, BIG, size, (h if arrow else 0) + h * .35, h * .68, fill=cream); g.append(p)
    return f'<g transform="translate({x} {y})">{"".join(g)}</g>', w

def wordmark(ink=INK, accent=ORANGE):
    """Type only, for narrow spots: BELGIUM / MOTOR HOMES / STORE, left aligned, 3 rows."""
    big, W = text('MOTOR HOMES', BIG, 44, 0, 62, fill=ink)
    top, _ = text('BELGIUM', SMALL, 14, 1, 20, fill=ink, track=.1)
    bot, bw = text('STORE', SMALL, 14, W, 86, fill=ink, track=.1, anchor='end')
    rule = f'<rect x="0" y="79" width="{W - bw - 10:.1f}" height="4" fill="{accent}"/>'
    return svg(round(W + 2), 92, top + big + bot + rule)

def lockup_h(ink=INK, cream=CREAM, accent=ORANGE, bg=None):
    """Sticker + wordmark side by side."""
    wm_w = width('MOTOR HOMES', BIG, 44)
    g = [sticker(0, 4, 104, ink, cream, accent)]
    x0 = 126
    g.append(text('MOTOR HOMES', BIG, 44, x0, 66, fill=ink)[0])
    g.append(text('BELGIUM', SMALL, 14, x0 + 1, 24, fill=ink, track=.1)[0])
    bot, bw = text('STORE', SMALL, 14, x0 + wm_w, 90, fill=ink, track=.1, anchor='end'); g.append(bot)
    g.append(f'<rect x="{x0}" y="83" width="{wm_w - bw - 10:.1f}" height="4" fill="{accent}"/>')
    return svg(round(x0 + wm_w + 4), 112, ''.join(g), bg=bg)

# ---------- Facebook ----------
def grain(id_='g'):
    return (f'<filter id="{id_}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
            f'<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .07 0"/></filter>')

COVER = {
    'nl': dict(h=['Elke mobilhome', 'vertrekt in orde.'], panels=['Grote onderhoudsbeurt', '2 jaar keuring', '12 maanden garantie'],
               band='Enkel op afspraak', place='Aarschot'),
    'fr': dict(h=['Chaque motorhome', 'part en ordre.'], panels=['Grand entretien', '2 ans de contrôle', '12 mois de garantie'],
               band='Uniquement sur rendez-vous', place='Aarschot'),
}
PHONE = '0497 37 32 60'

def cover(lang, safe=False):
    c = COVER[lang]; W, H = 1640, 624
    g = [f'<defs>{grain()}</defs><rect width="{W}" height="{H}" fill="{INK}"/>',
         f'<rect width="{W}" height="{H}" filter="url(#g)"/>']
    # big sticker on the right, slightly tilted like a slapped-on sticker
    g.append(f'<g transform="translate(1120 150) rotate(-4)">{sticker(0, 0, 300, INK, CREAM, ORANGE, bg_edge=CREAM)}</g>')
    x = 300
    hs = 88
    p, _ = text(c['h'][0], BIG, hs, x, 196, fill=CREAM); g.append(p)
    p, _ = text(c['h'][1], BIG, hs, x, 196 + hs * .98, fill=CREAM); g.append(p)
    px, py = x, 352
    for lab in c['panels']:
        pg, pw = panel(lab, px, py, 54, CREAM, INK, ORANGE)
        g.append(pg); px += pw + 14
    pg, pw = panel(c['place'], x, py + 70, 54, ORANGE, INK, CREAM); g.append(pg)
    pg2, pw2 = panel(c['band'], x + pw + 14, py + 70, 54, CREAM, INK, ORANGE, arrow=False); g.append(pg2)
    p, w1 = text(PHONE, BIG, 42, x, 568, fill=ORANGE); g.append(p)
    p, _ = text('motorhomestore.be', BIG, 32, x + w1 + 40, 568, fill=CREAM); g.append(p)
    if safe:
        mw = H * 16 / 9; x0 = (W - mw) / 2
        g.append(f'<rect width="{x0:.0f}" height="{H}" fill="#fff" fill-opacity=".35"/><rect x="{W-x0:.0f}" width="{x0:.0f}" height="{H}" fill="#fff" fill-opacity=".35"/>')
    return svg(W, H, ''.join(g), label='Facebook-omslagfoto Belgium Motor Homes Store')

def profile(bg=INK):
    S = 720
    return svg(S, S, f'<defs>{grain("p")}</defs><rect width="{S}" height="{S}" fill="{bg}"/><rect width="{S}" height="{S}" filter="url(#p)"/>'
                     f'<g transform="translate(360 372) rotate(-4) translate(-360 -372)">{sticker(140, 150, 440, INK, CREAM, ORANGE, bg_edge=CREAM, body='accent' if bg == INK else 'cream')}</g>',
               label='Profielfoto Belgium Motor Homes Store')

if __name__ == '__main__':
    save('logo-sticker.svg', svg(106, 94, sticker(3, 2)))
    save('logo-sticker-op-donker.svg', svg(106, 94, sticker(3, 2, bg_edge=CREAM), bg=INK))
    save('logo-sticker-op-geel.svg', svg(106, 94, sticker(3, 2, body='cream', bg_edge=CREAM), bg=ORANGE))
    save('logo-sticker-creme.svg', svg(106, 94, sticker(3, 2, body='cream')))
    save('logo-sticker-1kleur.svg', svg(106, 94, sticker(3, 2, flat=True)))
    save('logo-horizontaal.svg', lockup_h())
    save('logo-horizontaal-donker.svg', lockup_h(ink=CREAM, cream=INK, bg=INK))
    save('woordmerk.svg', wordmark())
    save('merkteken.svg', svg(106, 94, icon(3, 2)))
    save('merkteken-op-geel.svg', svg(106, 94, icon(3, 2), bg=ORANGE))
    save('badge.svg', svg(100, 130, badge()))
    save('badge-geel.svg', svg(100, 130, badge(ink=ORANGE, cream=INK, accent=INK)))
    pg, pw = panel('Aarschot', 0, 0, 40); save('paneel-aarschot.svg', svg(round(pw + 1), 40, pg))
    pg, pw = panel('Enkel op afspraak', 0, 0, 40, arrow=False); save('paneel-afspraak.svg', svg(round(pw + 1), 40, pg))
    save('favicon.svg', svg(64, 64, f'<rect width="64" height="64" rx="14" fill="{ORANGE}"/>' + icon(4, 6, 56, edge=False)))
    for lang in ('nl', 'fr'): save(f'facebook-cover-{lang}.svg', cover(lang))
    save('facebook-cover-nl-veilige-zone.svg', cover('nl', safe=True))
    save('profielfoto.svg', profile())
    save('profielfoto-geel.svg', profile(ORANGE))
    old = ('<rect width="100" height="100" rx="22" fill="#FDDA24"/>'
           '<path fill="#151515" d="M10 62 V33 q0-7 7-7 H57 q4 0 7 2 l9 6 l10 10 q7 1 7 7 v11 z"/>'
           '<rect x="16" y="33" width="13" height="9" rx="1.5" fill="#FDDA24"/><rect x="33" y="33" width="13" height="9" rx="1.5" fill="#FDDA24"/>'
           '<rect x="50" y="35" width="8" height="13" rx="1.5" fill="#FDDA24"/><path fill="#FDDA24" d="M63 35 h7 l9 9 h-16 z"/>'
           '<circle cx="27" cy="62" r="7.5" fill="#151515"/><circle cx="27" cy="62" r="2.8" fill="#FDDA24"/><circle cx="76" cy="62" r="7.5" fill="#151515"/><circle cx="76" cy="62" r="2.8" fill="#FDDA24"/>'
           '<rect x="10" y="75" width="26.6" height="6" rx="1.5" fill="#151515"/><rect x="63.4" y="75" width="26.6" height="6" rx="1.5" fill="#EF3340"/>')
    save('oud-logo-sq.svg', svg(100, 100, old, label='Huidig logo'))
    print('ok', OUT)
