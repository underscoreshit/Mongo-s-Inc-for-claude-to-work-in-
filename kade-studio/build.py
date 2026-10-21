"""Bouwt de Nederlandse pagina's uit de Franse bronpagina's.

Gebruik:  python3 build.py

    index.html     ->  nl/index.html      (de huidige site, v1)
    v2/index.html  ->  v2/nl/index.html   (de nieuwe illustratieve versie)

- Teksten: i18n/nl.json, gedeeld door v1 en v2 (sleutel = data-i18n, data-i18n-ph of data-i18n-aria).
- Pas altijd de Franse index.html en nl.json aan, nooit een nl/index.html: die wordt overschreven.
- Domein wijzigen: vervang https://kadestudio.be in index.html, v2/index.html, sitemap.xml en robots.txt.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
nl = json.loads((ROOT / "i18n" / "nl.json").read_text(encoding="utf-8"))


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


def sub_once(html, old, new, name):
    if old not in html:
        raise SystemExit("Niet gevonden in %s: %s" % (name, old[:80]))
    return html.replace(old, new)


def build(page, url_path, path_prefixes):
    """page: map van de Franse pagina ('' of 'v2'); url_path: pad op de site ('' of 'v2/');
    path_prefixes: relatieve paden die in nl/ een map dieper komen te staan."""
    folder = ROOT / page if page else ROOT
    name = (page + "/" if page else "") + "index.html"
    src = (folder / "index.html").read_text(encoding="utf-8")
    site = re.search(r'<link rel="canonical" href="(https?://[^/"]+)', src).group(1)

    out, missing = src, []
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
        raise SystemExit("Ontbrekende vertalingen in i18n/nl.json (%s): %s" % (name, ", ".join(sorted(missing))))

    # <head>
    out = sub_once(out, '<html lang="fr-BE">', '<html lang="nl-BE">', name)
    out = re.sub(r"<title>.*?</title>", "<title>%s</title>" % nl["title"], out, count=1)
    out = re.sub(r'(<meta name="description" id="meta-desc" content=")[^"]*', r"\g<1>" + nl["desc"], out, count=1)
    out = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + nl["ogt"], out, count=1)
    out = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + nl["ogd"], out, count=1)
    out = sub_once(out, '<meta property="og:locale" content="fr_BE">', '<meta property="og:locale" content="nl_BE">', name)
    out = sub_once(out, '<meta property="og:locale:alternate" content="nl_BE">', '<meta property="og:locale:alternate" content="fr_BE">', name)
    out = sub_once(out, 'content="%s/brand/og-image.png"' % site, 'content="%s/brand/social/nl/og-image.png"' % site, name)
    out = sub_once(out, '<meta property="og:url" content="%s/%s">' % (site, url_path), '<meta property="og:url" content="%s/%snl/">' % (site, url_path), name)
    out = sub_once(out, '<link rel="canonical" href="%s/%s">' % (site, url_path), '<link rel="canonical" href="%s/%snl/">' % (site, url_path), name)
    out = out.replace('"description":"Création de sites web pour commerces et artisans de Westerlo et des Kempen."',
                      '"description":"Websites voor handelaars en vakmensen uit Westerlo en de Kempen."')

    # Relatieve paden: nl/ zit een map dieper (vóór de taalknop, die zelf al klopt)
    alt = "|".join(re.escape(p) for p in path_prefixes)
    out = re.sub(r'(href|src)="(%s)' % alt, r'\1="../\2', out)
    out = re.sub(r'url\((%s)' % alt, r'url(../\1', out)

    # Taalknop: deze pagina is NL
    out = sub_once(out,
        '<a href="index.html" hreflang="fr-BE" lang="fr" data-lang="fr" aria-current="page">FR</a><a href="nl/index.html" hreflang="nl-BE" lang="nl" data-lang="nl">NL</a>',
        '<a href="../index.html" hreflang="fr-BE" lang="fr" data-lang="fr">FR</a><a href="index.html" hreflang="nl-BE" lang="nl" data-lang="nl" aria-current="page">NL</a>', name)

    (folder / "nl").mkdir(exist_ok=True)
    (folder / "nl" / "index.html").write_text(out, encoding="utf-8")
    print("%snl/index.html gebouwd (%d vertaalde teksten)" % (page + "/" if page else "", len(keys)))


build("", "", ["brand/", "fonts/", "demos/"])
if (ROOT / "v2" / "index.html").exists():
    build("v2", "v2/", ["../", "fonts/", "img/"])
