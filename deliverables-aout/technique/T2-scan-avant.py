#!/usr/bin/env python3
"""T2 - releve live de l'empreinte des ancres #s-* : liens de saut, canonical, JSON-LD."""
import re, ssl, json, urllib.request
from concurrent.futures import ThreadPoolExecutor

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
SCRATCH = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
URLS = [l.strip() for l in open(SCRATCH + "/t2-pages.txt") if l.strip()]

def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (compatible; HH-audit/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
            return u, r.getcode(), r.read().decode("utf-8", "replace")
    except Exception as e:
        return u, None, str(e)

def analyse(t):
    u, code, html = t
    if code != 200:
        return {"url": u, "code": code}
    liens = re.findall(r'href="#(s-[0-9a-z\-]+)"', html, re.I)
    can = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', html, re.I)
    # JSON-LD contenant des URL fragmentees vers #s-
    ld_frag = 0
    for m in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        ld_frag += len(re.findall(r'"[^"]*#s-[0-9a-z\-]+"', m, re.I))
    # conteneur du sommaire
    conteneurs = set(re.findall(r'class="([^"]*(?:hha-toc|hh-blog-toc|pri-som)[^"]*)"', html))
    return {"url": u, "code": 200, "liens": len(liens), "uniques": len(set(liens)),
            "canonical": can.group(1) if can else None, "ld_frag": ld_frag,
            "conteneurs": sorted(conteneurs)}

with ThreadPoolExecutor(max_workers=6) as ex:
    res = [analyse(r) for r in ex.map(fetch, URLS)]

json.dump(res, open(SCRATCH + "/t2-scan.json", "w"), ensure_ascii=False, indent=1)

ok = [r for r in res if r.get("code") == 200]
ko = [r for r in res if r.get("code") != 200]
avec = [r for r in ok if r["liens"]]
print("pages testees      :", len(res))
print("HTTP 200           :", len(ok), "| en erreur :", len(ko))
print("pages avec #s-*    :", len(avec))
print("liens de saut      :", sum(r["liens"] for r in avec))
print("fragments uniques  :", sum(r["uniques"] for r in avec))
print("JSON-LD fragmentes :", sum(r["ld_frag"] for r in ok), "occurrences")
mauvais = [r for r in ok if r["canonical"] is None or "#" in (r["canonical"] or "")
           or r["canonical"].rstrip("/") != r["url"].rstrip("/")]
print("canonical non auto-referent ou fragmente :", len(mauvais))
for r in mauvais[:10]:
    print("   ", r["url"], "->", r["canonical"])
for r in ko:
    print("   ERREUR", r["url"], r.get("code"))
cs = {}
for r in ok:
    for c in r["conteneurs"]:
        cs[c] = cs.get(c, 0) + 1
print("conteneurs de sommaire rencontres :")
for c, n in sorted(cs.items(), key=lambda x: -x[1]):
    print("   %3d  %s" % (n, c))
