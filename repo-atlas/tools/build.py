"""Build: src/app.html + data/repos.json -> dist/artifact.html (claude.ai) and dist/index.html (standalone PWA)."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
src = (R/"src/app.html").read_text().replace("/*VILLAGE*/", (R/"src/village.js").read_text())
data = json.dumps(json.loads((R/"data/repos.json").read_text()), separators=(",",":"), ensure_ascii=False).replace("</", "<\\/")
page = src.replace("/*DATA*/", data)
(R/"dist").mkdir(exist_ok=True)
(R/"dist/artifact.html").write_text(page.replace("<!--HEAD-->", ""))
head = ('<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#070a12">'
        '<link rel="icon" href="icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="icon-192.png">'
        '<meta name="apple-mobile-web-app-capable" content="yes"><link rel="search" type="application/opensearchdescription+xml" title="Repo Cortex" href="opensearch.xml">')
sw = "<script>if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>"
full = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        + page.replace("<!--HEAD-->", head) .replace("<header", "</head><body><header", 1) + sw + "</body></html>")
# move <title>/<style> (before header) into head: they already are, since we split at <header
(R/"dist/index.html").write_text(full)
print("built", len(page)//1024, "KB")
