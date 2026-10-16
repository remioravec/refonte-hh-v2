#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification de ce qui est VISIBLE, pas de ce qui est dans le code.

Le controle precedent comptait les liens du document et declarait seize
metiers alors que huit seulement apparaissaient a l'ecran. Celui-ci ouvre
reellement le menu dans un navigateur, a 390 px, deplie l'accordeon et compte
les liens dont la boite tient dans celle du sous-menu.

En complement, il relit le plafond CSS sur la totalite des contenus : c'est
bon marche, et c'est la cause racine.

Usage :  python3 verifier_visible.py [nombre_de_pages_rendues]
"""

import json
import re
import subprocess
import sys

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
N_RENDU = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def alleger(s):
    s = re.sub(r'<script[^>]+src="[^"]+"[^>]*>\s*</script>', "", s)
    s = re.sub(r'<link[^>]+href="https?://[^"]+"[^>]*>', "", s)
    s = re.sub(r'<img([^>]+)src="https?://[^"]*"', r'<img\1src=""', s)
    s = re.sub(r"url\((?:&#039;|')?https?://[^)]*(?:&#039;|')?\)", "none", s)
    return s


def main():
    inv = json.load(open(S + "/inventaire-menu.json"))
    cibles = [x for x in inv if x["nav"] and x["mobile"] and not x["elementor"]]

    # --- 1. le plafond CSS, sur la totalite
    print("1. plafond du sous-menu mobile, sur %d contenus" % len(cibles))
    bas, absent, ok = [], [], 0
    for x in cibles:
        r = subprocess.run(["curl", "-sSL", "-m", "25", x["link"]],
                           capture_output=True, text=True)
        m = re.search(r'\.mobile-submenu\.open,\s*\.mobile-submenu\.open\s*\{\s*'
                      r'max-height:\s*(\d+)px', r.stdout)
        u = x["link"].replace("https://www.helloharel.com", "")
        if not m:
            absent.append(u)
        elif int(m.group(1)) < 1200:
            bas.append((u, int(m.group(1))))
        else:
            ok += 1
    print("   au-dessus de 1200 px : %d / %d" % (ok, len(cibles)))
    for u, v in bas:
        print("   ! %-52s plafond %d px" % (u[:52], v))
    for u in absent:
        print("   ! %-52s regle absente" % u[:52])

    # --- 2. le rendu reel, sur un echantillon
    ech = [cibles[i] for i in range(0, len(cibles), max(1, len(cibles) // N_RENDU))][:N_RENDU]
    print("\n2. rendu a 390 px, %d pages" % len(ech))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for x in ech:
            u = x["link"]
            r = subprocess.run(["curl", "-sSL", "-m", "25", u], capture_output=True, text=True)
            f = S + "/rendu-tmp.html"
            open(f, "w", encoding="utf-8").write(alleger(r.stdout))
            pg = b.new_page(viewport={"width": 390, "height": 844})
            err = []
            pg.on("pageerror", lambda e: err.append(str(e)[:70]))
            try:
                pg.goto("file://" + f, wait_until="domcontentloaded")
                pg.wait_for_timeout(1500)
                pg.click("#hamburgerBtn")
                pg.wait_for_timeout(300)
                pg.eval_on_selector_all(".mobile-accordion-btn",
                                        "(l)=>l[1].click()")
                pg.wait_for_timeout(700)
                d = pg.evaluate("""()=>{const s=document.querySelectorAll('.mobile-submenu')[1];
                  const sr=s.getBoundingClientRect();
                  const liens=[...s.querySelectorAll('a')];
                  const vis=liens.filter(a=>{const r=a.getBoundingClientRect();
                    return r.height>0 && r.bottom<=sr.bottom+1;});
                  return {total:liens.length, visibles:vis.length,
                          haut:Math.round(sr.height), reel:s.scrollHeight};}""")
                etat = "OK" if d["visibles"] == 16 else "COUPE"
                print("   %-5s %-44s %2d/%2d visibles · %d px sur %d · exc %s"
                      % (etat, u.replace("https://www.helloharel.com", "")[:44],
                         d["visibles"], d["total"], d["haut"], d["reel"], err or 0))
            except Exception as e:
                print("   ERR   %-44s %s" % (u[:44], str(e)[:60]))
            pg.close()
        b.close()


if __name__ == "__main__":
    main()
