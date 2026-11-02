"""Fetch top GitHub repos per category via `gh api` search. Output: data/repos.json"""
import json, subprocess, time, sys, pathlib

CATS = [
 ("python","Python","Language, frameworks, libraries",["language:python stars:>25000","topic:python topic:tutorial stars:>3000","topic:fastapi stars:>3000","topic:django stars:>8000"]),
 ("learn","Learn to Code","Roadmaps, courses, interview prep",["topic:roadmap stars:>5000","topic:education topic:programming stars:>5000","topic:interview stars:>15000","topic:computer-science stars:>10000"]),
 ("homelab","Homelab & Self-hosted","Run your own servers at home",["topic:homelab stars:>2000","topic:self-hosted stars:>15000","topic:proxmox stars:>1500","topic:home-automation stars:>5000"]),
 ("devops","DevOps & Containers","Docker, Kubernetes, CI, infra as code",["topic:docker stars:>15000","topic:kubernetes stars:>12000","topic:terraform stars:>5000","topic:ansible stars:>3000"]),
 ("linux","Linux & Terminal","Shell, CLI tools, dotfiles",["topic:cli stars:>20000","topic:linux stars:>15000","topic:shell stars:>12000","topic:dotfiles stars:>3000"]),
 ("network","Networking","DNS, VPN, proxies, monitoring",["topic:vpn stars:>5000","topic:dns stars:>5000","topic:monitoring stars:>8000","topic:networking stars:>8000"]),
 ("security","Cybersecurity","Learning, hardening, defense, CTF practice",["topic:security topic:awesome-list stars:>3000","topic:ctf stars:>3000","topic:owasp stars:>3000","topic:hardening stars:>1000","topic:security stars:>15000"]),
 ("ai","AI & LLMs","Models, agents, local AI",["topic:llm stars:>25000","topic:machine-learning stars:>25000","topic:local-llm stars:>3000","topic:ai-agents stars:>10000"]),
 ("web","Web Development","Frontend, backend, frameworks",["topic:react stars:>40000","topic:javascript stars:>50000","topic:typescript stars:>40000","topic:css stars:>20000"]),
 ("data","Databases & Data","SQL, NoSQL, analytics",["topic:database stars:>15000","topic:data-engineering stars:>5000","topic:sql stars:>12000"]),
 ("systems","Systems Languages","Rust, Go, C",["language:rust stars:>30000","language:go stars:>40000","language:c stars:>30000"]),
 ("tools","Dev Tools & Editors","Editors, git, productivity",["topic:neovim stars:>10000","topic:git stars:>12000","topic:developer-tools stars:>15000","topic:vscode stars:>15000"]),
 ("awesome","Awesome Lists","Curated mega-lists of everything",["topic:awesome-list stars:>40000","awesome in:name stars:>60000"]),
 ("health","Fitness & Food","Open-source workout and nutrition apps",["topic:fitness stars:>300","topic:nutrition stars:>200","topic:workout stars:>200","topic:recipes stars:>1500"]),
 ("rising","Rising in 2026","Newest repos picking up stars fast",["created:>2026-05-01 stars:>3000","created:>2026-08-01 stars:>1000"]),
]
out, seen = {"generated": time.strftime("%Y-%m-%d"), "categories": [], "repos": []}, {}
for key, name, desc, queries in CATS:
    out["categories"].append({"id": key, "name": name, "desc": desc})
    for q in queries:
        r = subprocess.run(["gh","api","-X","GET","search/repositories","-f",f"q={q} archived:false","-f","sort=stars","-f","per_page=40"],capture_output=True,text=True)
        if r.returncode: print("ERR",q,r.stderr[:200],file=sys.stderr); time.sleep(10); continue
        for it in json.loads(r.stdout)["items"]:
            fn = it["full_name"]
            if fn in seen:
                if key not in seen[fn]["cats"]: seen[fn]["cats"].append(key)
                continue
            rec = {"n": fn, "d": (it.get("description") or "")[:220], "s": it["stargazers_count"], "l": it.get("language") or "",
                   "t": (it.get("topics") or [])[:8], "p": it["pushed_at"][:10], "c": it["created_at"][:10], "cats": [key]}
            seen[fn] = rec; out["repos"].append(rec)
        print(f"{key:9} {q[:45]:45} total={len(out['repos'])}", file=sys.stderr)
        time.sleep(2.2)
pathlib.Path(__file__).resolve().parent.parent.joinpath("data").mkdir(exist_ok=True)
pathlib.Path(__file__).resolve().parent.parent.joinpath("data/repos.json").write_text(json.dumps(out,separators=(",",":"),ensure_ascii=False))
print("done", len(out["repos"]))
