#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ou se trouvent les variantes a unifier, page par page."""
import os, re, sys
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp_common as w, ns_api      # noqa: E402

VARIANTES = [("support@helloharel.com", "support@helloharel.com"),
             ("+33185540154", r"\+33185540154|01[\s.\-]?85[\s.\-]?54[\s.\-]?01[\s.\-]?54"),
             ("6 Avenue (majuscule)", r"6 Avenue de Rueil"),
             ("HAREL SYSTEMS", r"HAREL SYSTEMS"),
             ("Harel Systems (sans SAS)", r"Harel Systems(?! SAS)")]

pages, p = [], 1
while True:
    lot = ns_api.call("wp/v2/pages?per_page=100&page=%d&status=publish&_fields=id,link" % p)
    if not lot:
        break
    pages += lot
    if len(lot) < 100:
        break
    p += 1
trouve = {n: [] for n, _ in VARIANTES}
for x in pages:
    c = w.get_raw("pages", x["id"])["content"]["raw"]
    u = x["link"].replace("https://www.helloharel.com", "") or "/"
    for nom, motif in VARIANTES:
        n = len(re.findall(motif, c))
        if n:
            trouve[nom].append((u, n, x["id"]))
for nom, _ in VARIANTES:
    L = trouve[nom]
    print("\n=== %s — %d page(s), %d occurrence(s) ==="
          % (nom, len(L), sum(n for _, n, _ in L)))
    for u, n, pid in sorted(L):
        print("   %-6d %-46s ×%d" % (pid, u[:46], n))
