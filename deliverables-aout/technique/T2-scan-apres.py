#!/usr/bin/env python3
"""T2 - verification apres depose du snippet : plus aucun lien de saut crawlable,
sommaire toujours rendu, JS de defilement present."""
import re, ssl, json, random, urllib.request
from concurrent.futures import ThreadPoolExecutor

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
URLS = [l.strip() for l in open(S + "/t2-pages.txt") if l.strip()]

def fetch(u):
    q = u + "?nc=%d" % random.randint(1, 10**9)
    req = urllib.request.Request(q, headers={"User-Agent": "Mozilla/5.0 (compatible; HH-audit/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
            return u, r.getcode(), r.read().decode("utf-8", "replace")
    except Exception as e:
        return u, None, str(e)

def an(t):
    u, code, h = t
    if code != 200:
        return {"url": u, "code": code}
    return {
        "url": u, "code": 200,
        "href": len(re.findall(r'href="#s-[0-9a-z\-]+"', h, re.I)),
        "jump": len(re.findall(r'data-jump="s-[0-9a-z\-]+"', h, re.I)),
        "js":   1 if "function sauter(el)" in h else 0,
        "cibles": len(set(re.findall(r'id="(s-[0-9a-z\-]+)"', h, re.I))),
        "som": len(re.findall(r'<nav class="hha-toc">', h)) + len(re.findall(r'<div class="som">', h)),
    }

with ThreadPoolExecutor(max_workers=6) as ex:
    res = [an(r) for r in ex.map(fetch, URLS)]

ok = [r for r in res if r.get("code") == 200]
print("pages verifiees            :", len(res), "| HTTP 200 :", len(ok))
print("liens de saut crawlables   :", sum(r["href"] for r in ok), "  (avant : 1147)")
print("liens neutralises          :", sum(r["jump"] for r in ok))
print("blocs sommaire rendus      :", sum(r["som"] for r in ok))
print("cibles id=s-* intactes     :", sum(r["cibles"] for r in ok))
print("pages sans le JS de saut   :", len([r for r in ok if not r["js"]]))
mauv = [r for r in ok if r["href"]]
for r in mauv: print("   RESTE", r["url"], r["href"])
sansjs = [r for r in ok if not r["js"] and r["jump"]]
for r in sansjs: print("   JS MANQUANT", r["url"])
ko = [r for r in res if r.get("code") != 200]
for r in ko: print("   ERREUR", r["url"], r.get("code"))
json.dump(res, open(S + "/t2-verif.json", "w"), ensure_ascii=False, indent=1)
