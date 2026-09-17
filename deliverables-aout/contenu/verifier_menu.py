#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification EN LIGNE du menu, contenu par contenu."""
import json, re, subprocess, sys

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def bloc_div(s, i):
    prof, j = 0, i
    while j < len(s):
        a, b = s.find("<div", j), s.find("</div>", j)
        if b < 0:
            return -1
        if 0 <= a < b:
            prof += 1; j = a + 4
        else:
            prof -= 1; j = b + 6
            if prof == 0:
                return j
    return -1


def main():
    inv = json.load(open(S + "/inventaire-menu.json"))
    cibles = [x for x in inv if x["nav"] and x["mobile"] and not x["elementor"]]
    ok, pb = 0, []
    for k, x in enumerate(cibles, 1):
        u = x["link"]
        r = subprocess.run(["curl", "-sS", "-m", "25", "-w", "\n%{http_code}", u],
                           capture_output=True, text=True)
        s = r.stdout
        code = s.rsplit("\n", 1)[-1].strip()
        if code != "200":
            pb.append((x["id"], u, "HTTP %s" % code)); continue
        i = s.find('<nav class="desktop-nav">')
        if i < 0:
            pb.append((x["id"], u, "navigation absente")); continue
        nav = s[i:s.find("</nav>", i)]
        agro = len(set(re.findall(r'href="(/agroalimentaire/[^"]*)"', nav)))
        j = s.find('<div class="mobile-menu-inner">')
        mob = s[j:bloc_div(s, j)] if j >= 0 else ""
        agrom = len(set(re.findall(r'href="(/agroalimentaire/[^"]*)"', mob)))
        d = []
        if agro != 16:
            d.append("bureau %d metiers" % agro)
        if agrom != 16:
            d.append("mobile %d metiers" % agrom)
        if "/negoce/" in nav or "/medical/" in nav:
            d.append("negoce/medical dans la navigation")
        if "/negoce/" in mob or "/medical/" in mob:
            d.append("negoce/medical en mobile")
        if s.count("<h1") != 1:
            d.append("%d H1" % s.count("<h1"))
        if d:
            pb.append((x["id"], u, " · ".join(d)))
        else:
            ok += 1
        if k % 25 == 0:
            print("   %d / %d verifies" % (k, len(cibles)), flush=True)
    print("\nconformes en ligne : %d / %d" % (ok, len(cibles)))
    if pb:
        print("ecarts (%d) :" % len(pb))
        for i, u, e in pb:
            print("   %-6s %-52s %s" % (i, u.replace("https://www.helloharel.com", "")[:52], e))
    else:
        print("aucun ecart : le meme menu sur la totalite des contenus")


if __name__ == "__main__":
    main()
