# Repo Village

The best GitHub repos as a living pixel village: every category is a building you can walk into. 1,259 repos across 15 categories
(Python, Learn to Code, Homelab, DevOps, Linux, Networking, Cybersecurity, AI, Web, Data,
Systems languages, Dev tools, Awesome lists, Fitness & Food, Rising in 2026).

- **Live (claude.ai artifact):** https://claude.ai/artifact/JmHpEktGEynLnvgr9QmWJa
- **Search:** press `/`, type anything (name, topic, language). Results light up on the map.
- **Village:** click a building to go inside and browse its repos. Click a villager for a random pick.
  Light follows your local time (button top-right switches to midday / golden hour / night).
- **Start here:** the green "Start here" picks and the learning path in the sidebar are hand-picked.
- **Add a repo:** "Add repo" → paste `https://github.com/owner/repo`. In the artifact it is saved
  to the artifact's database (synced across your devices). Stars/description fill in
  automatically in the standalone version; in the artifact, ask Claude to enrich pending repos.

## Layout
```
src/app.html          the app shell (one file, no framework)
src/village.js        the pixel village (drawn in code, inlined at build)
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
  name `Village`, shortcut `rv`, URL `https://<your-host>/?q=%s`. Then type `rv proxmox` in the bar.
