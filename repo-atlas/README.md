# Repo Cortex

The best GitHub repos, mapped as a neural network. 1,259 repos across 15 categories
(Python, Learn to Code, Homelab, DevOps, Linux, Networking, Cybersecurity, AI, Web, Data,
Systems languages, Dev tools, Awesome lists, Fitness & Food, Rising in 2026).

- **Live (claude.ai artifact):** https://claude.ai/artifact/JmHpEktGEynLnvgr9QmWJa
- **Search:** press `/`, type anything (name, topic, language). Results light up on the map.
- **Map:** click a hub to filter that category, click a neuron to jump to its repo.
- **Start here:** amber neurons and the "Start here picks" toggle are a hand-picked learning path.
- **Add a repo:** "Add repo" → paste `https://github.com/owner/repo`. In the artifact it is saved
  to the artifact's database (synced across your devices). Stars/description fill in
  automatically in the standalone version; in the artifact, ask Claude to enrich pending repos.

## Layout
```
src/app.html          the app (one file, no framework)
data/repos.json       repo data (generated)
tools/fetch.py        pulls top repos per category from the GitHub search API (needs `gh`)
tools/curate.py       adds hand-picked classics + marks "start here" picks
tools/build.py        -> dist/artifact.html (claude.ai) + dist/index.html (installable PWA)
dist/                 static site: index.html, manifest, service worker, icons, opensearch.xml
```

## Refresh the data
```bash
python3 tools/fetch.py && python3 tools/curate.py && python3 tools/build.py
```
Edit the `CATS` list in `tools/fetch.py` to add categories or queries.

## Use it as an app from your browser bar
Host `dist/` on any static host (GitHub Pages, Netlify, Cloudflare Pages). Then:
- **Install:** Chrome/Edge address bar → install icon, or phone → "Add to Home screen". Works offline.
- **Search from the address bar:** Chrome → Settings → Search engine → Manage → Site search → Add:
  name `Cortex`, shortcut `rc`, URL `https://<your-host>/?q=%s`. Then type `rc proxmox` in the bar.
