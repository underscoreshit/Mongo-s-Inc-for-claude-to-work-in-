"""Add hand-picked repos (via search repo: qualifiers) and mark 'start here' picks."""
import json, subprocess, time, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / "data/repos.json"
d = json.load(open(P)); idx = {r["n"].lower(): r for r in d["repos"]}
EXTRA = {
 "learn": ["kamranahmedse/developer-roadmap","trekhleb/learn-python","realpython/python-guide","asweigart/inventwithpython","ossu/computer-science","EbookFoundation/free-programming-books","practical-tutorials/project-based-learning","codecrafters-io/build-your-own-x"],
 "python": ["trekhleb/learn-python","realpython/python-guide","asweigart/inventwithpython","vinta/awesome-python","TheAlgorithms/Python","fastapi/fastapi","geekcomputers/Python"],
 "homelab": ["jellyfin/jellyfin","nextcloud/server","kahun/awesome-sysadmin","awesome-selfhosted/awesome-selfhosted","pi-hole/pi-hole","louislam/uptime-kuma","portainer/portainer","community-scripts/ProxmoxVE","mealie-recipes/mealie","immich-app/immich","home-assistant/core"],
 "network": ["wireguard/wireguard-go","tailscale/tailscale","netbirdio/netbird","pi-hole/pi-hole","AdguardTeam/AdGuardHome"],
 "security": ["wazuh/wazuh","crowdsecurity/crowdsec","OWASP/CheatSheetSeries","OWASP/wstg","Hacker0x01/hacker101","apsdehal/awesome-ctf","trimstray/the-book-of-secret-knowledge","CISOfy/lynis","sbilly/awesome-security","juice-shop/juice-shop","ossec/ossec-hids","fail2ban/fail2ban"],
 "linux": ["jlevy/the-art-of-command-line","tldr-pages/tldr","ohmyzsh/ohmyzsh","junegunn/fzf"],
 "health": ["wger-project/wger","TandoorRecipes/recipes","mealie-recipes/mealie"],
}
START = {"learn":["kamranahmedse/developer-roadmap","ossu/computer-science","codecrafters-io/build-your-own-x","practical-tutorials/project-based-learning"],
 "python":["trekhleb/learn-python","asweigart/inventwithpython","TheAlgorithms/Python","vinta/awesome-python","fastapi/fastapi"],
 "homelab":["awesome-selfhosted/awesome-selfhosted","community-scripts/ProxmoxVE","portainer/portainer","pi-hole/pi-hole","louislam/uptime-kuma","jellyfin/jellyfin"],
 "network":["tailscale/tailscale","AdguardTeam/AdGuardHome"],
 "security":["OWASP/CheatSheetSeries","Hacker0x01/hacker101","juice-shop/juice-shop","trimstray/the-book-of-secret-knowledge","CISOfy/lynis","crowdsecurity/crowdsec"],
 "linux":["jlevy/the-art-of-command-line","tldr-pages/tldr"],
 "health":["wger-project/wger","TandoorRecipes/recipes"]}
need = sorted({n for v in EXTRA.values() for n in v if n.lower() not in idx})
for i in range(0, len(need), 6):
    q = " ".join("repo:"+n for n in need[i:i+6])
    r = subprocess.run(["gh","api","-X","GET","search/repositories","-f",f"q={q}","-f","per_page=10"],capture_output=True,text=True)
    for it in json.loads(r.stdout).get("items", []):
        rec = {"n": it["full_name"], "d": (it.get("description") or "")[:220], "s": it["stargazers_count"], "l": it.get("language") or "",
               "t": (it.get("topics") or [])[:8], "p": it["pushed_at"][:10], "c": it["created_at"][:10], "cats": []}
        d["repos"].append(rec); idx[rec["n"].lower()] = rec
    time.sleep(2.2)
for cat, names in EXTRA.items():
    for n in names:
        r = idx.get(n.lower())
        if r and cat not in r["cats"]: r["cats"].append(cat)
miss = []
for cat, names in START.items():
    for n in names:
        r = idx.get(n.lower())
        if r: r["k"] = 1
        else: miss.append(n)
json.dump(d, open(P,"w"), separators=(",",":"), ensure_ascii=False)
print("repos", len(d["repos"]), "missing", miss)
