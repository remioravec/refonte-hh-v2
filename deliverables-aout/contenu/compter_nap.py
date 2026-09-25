#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Combien de pages portent le bloc NAP, et lesquelles n'en ont pas."""
import os, sys
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp_common as w, ns_api      # noqa: E402

PROTEGEES = {1726, 2818, 2839, 5477, 11162}
pages, p = [], 1
while True:
    lot = ns_api.call("wp/v2/pages?per_page=100&page=%d&status=publish&_fields=id,link" % p)
    if not lot:
        break
    pages += lot
    if len(lot) < 100:
        break
    p += 1
avec, sans, proteg = 0, [], []
for x in pages:
    c = w.get_raw("pages", x["id"])["content"]["raw"]
    u = x["link"].replace("https://www.helloharel.com", "") or "/"
    if 'class="hh-nap"' in c:
        avec += 1
    elif x["id"] in PROTEGEES:
        proteg.append(u)
    else:
        sans.append((u, "pied du theme" if "<footer" not in c else "pied sans bloc de marque"))
print("NAP pose sur %d page(s) sur %d" % (avec, len(pages)))
print("\nregle 0, exclues (%d) :" % len(proteg))
for u in sorted(proteg):
    print("   %s" % u)
print("\nsans NAP (%d) :" % len(sans))
for u, q in sorted(sans):
    print("   %-44s %s" % (u[:44], q))
