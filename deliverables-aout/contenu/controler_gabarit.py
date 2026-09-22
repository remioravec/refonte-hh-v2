#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ou en est chaque page, lu dans WordPress et non dans un journal."""
import os, re, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro"); sys.path.insert(0, ICI)
import wp_common as w          # noqa: E402
import deployer_gabarit as D   # noqa: E402

MARQUES = [("defilement", 'class="sy-ecrans"'), ("FAQ", "<details"),
           ("avis", 'class="avis-file"'), ("equipe", 'class="eq-rail"'),
           ("metiers", 'class="mt-f"'), ("Hero", 'class="hh-conf"'),
           ("Maxence", 'class="hh-max"')]

pages = D.cibles() + [(p, u) for u, p in
                      (("/agroalimentaire/torrefacteur/", 10935),
                       ("/agroalimentaire/brasseur/", 10896),
                       ("/agroalimentaire/chocolatier/", 10894))]
print("%-46s %5s %6s  %s" % ("url", "ko", "solde", " ".join(n for n, _ in MARQUES)))
print("-" * 104)
manquants = 0
for pid, url in sorted(pages, key=lambda t: t[1]):
    c = w.get_raw("pages", pid)["content"]["raw"]
    etat = []
    for nom, t in MARQUES:
        etat.append(("oui" if t in c else "—").ljust(len(nom)))
    complet = all(t in c for _, t in MARQUES)
    s = D.solde(c)
    if not complet or s != 0 or len(c) > 275000:
        manquants += 1
    print("%-46s %5d %+6d  %s%s" % (url[:46], len(c) // 1024, s, " ".join(etat),
                                    "" if complet and s == 0 else "   <<<"))
print("\n%d page(s) incompletes ou en defaut" % manquants)
