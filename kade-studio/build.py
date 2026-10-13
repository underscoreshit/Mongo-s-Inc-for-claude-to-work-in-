"""Bouwt de Nederlandse pagina (nl/index.html) uit de Franse bronpagina (index.html).

Gebruik:  python3 build.py

- Teksten: i18n/nl.json (sleutel = data-i18n, data-i18n-ph of data-i18n-aria in index.html)
- Pas altijd index.html en nl.json aan, nooit nl/index.html zelf: die wordt overschreven.
- Domein wijzigen: vervang https://kadestudio.be in index.html, sitemap.xml en robots.txt.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / "index.html").read_text(encoding="utf-8")
nl = json.loads((ROOT / "i18n" / "nl.json").read_text(encoding="utf-8"))
SITE = re.search(r'<link rel="canonical" href="([^"]+)/">', src).group(1)
missing = []


def replace_inner(html, key, value):
    """Vervangt de inhoud van elk element met data-i18n="key", geneste tags inbegrepen."""
    out, pos = [], 0
    start_re = re.compile(r'<(span|option)\b[^>]*\sdata-i18n="%s"[^>]*>' % re.escape(key))
    while True:
        m = start_re.search(html, pos)
        if not m:
            break
        tag = m.group(1)
        depth, i = 1, m.end()
        tok = re.compile(r"<(/?)%s\b[^>]*>" % tag)
        while depth:
            t = tok.search(html, i)
            depth += -1 if t.group(1) else 1
            i = t.end()
        close_start = i - len("</%s>" % tag)
        out.append(html[pos:m.end()] + value)
        pos = close_start
    out.append(html[pos:])
    return "".join(out)


def sub_once(html, old, new):
    if old not in html:
        raise SystemExit("Niet gevonden in index.html: " + old[:80])
    return html.replace(old, new)


out = src
keys = set(re.findall(r'data-i18n="([^"]+)"', src))
for k in sorted(keys):
    if k not in nl:
        missing.append(k)
        continue
    out = replace_inner(out, k, nl[k])
for attr, html_attr in (("data-i18n-ph", "placeholder"), ("data-i18n-aria", "aria-label")):
    for k in set(re.findall(attr + r'="([^"]+)"', src)):
        if k not in nl:
            missing.append(k)
            continue
        out = re.sub(r'%s="[^"]*"(\s+%s="%s")' % (html_attr, attr, re.escape(k)),
                     lambda m: '%s="%s"%s' % (html_attr, nl[k], m.group(1)), out)
if missing:
    raise SystemExit("Ontbrekende vertalingen in i18n/nl.json: " + ", ".join(sorted(missing)))

# <head>
out = sub_once(out, '<html lang="fr-BE">', '<html lang="nl-BE">')
out = re.sub(r"<title>.*?</title>", "<title>%s</title>" % nl["title"], out, count=1)
out = re.sub(r'(<meta name="description" id="meta-desc" content=")[^"]*', r"\g<1>" + nl["desc"], out, count=1)
out = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + nl["ogt"], out, count=1)
out = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + nl["ogd"], out, count=1)
out = sub_once(out, '<meta property="og:locale" content="fr_BE">', '<meta property="og:locale" content="nl_BE">')
out = sub_once(out, '<meta property="og:locale:alternate" content="nl_BE">', '<meta property="og:locale:alternate" content="fr_BE">')
out = sub_once(out, 'content="%s/brand/og-image.png"' % SITE, 'content="%s/brand/social/nl/og-image.png"' % SITE)
out = sub_once(out, '<meta property="og:url" content="%s/">' % SITE, '<meta property="og:url" content="%s/nl/">' % SITE)
out = sub_once(out, '<link rel="canonical" href="%s/">' % SITE, '<link rel="canonical" href="%s/nl/">' % SITE)
out = out.replace('"description":"Création de sites web pour petites entreprises belges."',
                  '"description":"Websites voor kleine Belgische bedrijven."')

# Taalknop: deze pagina is NL
out = sub_once(out,
    '<a href="index.html" hreflang="fr-BE" lang="fr" data-lang="fr" aria-current="page">FR</a><a href="nl/index.html" hreflang="nl-BE" lang="nl" data-lang="nl">NL</a>',
    '<a href="../index.html" hreflang="fr-BE" lang="fr" data-lang="fr">FR</a><a href="index.html" hreflang="nl-BE" lang="nl" data-lang="nl" aria-current="page">NL</a>')

# Relatieve paden: nl/ zit een map dieper
out = re.sub(r'(href|src)="(brand|fonts)/', r'\1="../\2/', out)
out = out.replace("url(fonts/", "url(../fonts/")

(ROOT / "nl").mkdir(exist_ok=True)
(ROOT / "nl" / "index.html").write_text(out, encoding="utf-8")
print("nl/index.html gebouwd (%d vertaalde teksten)" % len(keys))
