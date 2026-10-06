#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventaire du menu sur 100 % des contenus, avant toute ecriture."""
import json, re, sys
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import wp_common as w

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PROTEGEES = {1726, 2818, 2839, 5477, 11162}
inv = []
for kind in ("pages", "posts"):
    for it in w.get_all(kind):
        p = w.get_raw(kind, it["id"])
        c = p["content"]["raw"]
        el = (p.get("meta", {}).get("_elementor_data") or "").strip()
        i = c.find('<nav class="desktop-nav">')
        j = c.find("</nav>", i) if i >= 0 else -1
        nav = c[i:j] if i >= 0 and j > 0 else ""
        k = c.find('<div class="mobile-menu-inner">')
        inv.append({
            "kind": kind, "id": it["id"], "slug": it["slug"], "link": it["link"],
            "octets": len(c),
            "elementor": el if el not in ("", "[]", "[ ]", "null") else "",
            "protegee": it["id"] in PROTEGEES,
            "nav": i >= 0, "nav_imbrique": "<nav" in nav[25:] if nav else False,
            "mobile": k >= 0,
            "agro": len(set(re.findall(r'href="(/agroalimentaire/[^"]*)"', nav))),
            "negoce": len(set(re.findall(r'href="(/negoce/[^"]*)"', nav))),
            "medical": len(set(re.findall(r'href="(/medical/[^"]*)"', nav))),
            "agro_mob": len(set(re.findall(
                r'href="(/agroalimentaire/[^"]*)"', c[k:c.find("</div>\n    </div>", k)] if k >= 0 else ""))),
            "header": c.count("<header"),
        })
json.dump(inv, open(S + "/inventaire-menu.json", "w"), ensure_ascii=False, indent=1)
print("analyses :", len(inv))
