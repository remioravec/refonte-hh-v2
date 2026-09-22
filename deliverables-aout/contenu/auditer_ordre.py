#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le gabarit attendu, page par page : qui l'a, qui ne l'a pas, dans quel ordre.

Ordre de reference, celui des trois pages pilotes :
  hero · logos · fonctionnalites · a-propos · process · metiers · equipe ·
  faq · avis · cta

On releve aussi ce qui n'a rien a y faire : calculateurs, simulateurs,
quiz, et toute section hors de cette liste.
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

ATTENDU = ["hero-section", "logos-section", "features-section", "about-card-section",
           "process-section", "metiers-section", "team-section", "faq-section",
           "reviews-section", "cta-banner"]

INTRUS = [("calculateur", r"calculateur|calculette|simulateur|simulate|estimez vos|"
                          r"roi-|quiz|hhq-|hh-roi"),
          ("comparatif", r"comparatif-section|hh-comparo"),
          ("presse", r"presse-section|logos-presse"),
          ("bloc d'aout", r'<section class="hh-maj-aout'),
          ("bento orpheline", r'<div class="bento-card')]


def pages():
    return D.cibles() + [(10935, "/agroalimentaire/torrefacteur/"),
                         (10896, "/agroalimentaire/brasseur/"),
                         (10894, "/agroalimentaire/chocolatier/")]


def main():
    lignes = []
    for pid, url in sorted(pages(), key=lambda t: t[1]):
        c = w.get_raw("pages", pid)["content"]["raw"]
        ordre = [m.group(1).split()[0] for m in re.finditer(r'<section class="([^"]+)"', c)]
        # ce qui manque, ce qui est en trop, et l'ordre
        manque = [x for x in ATTENDU if x not in ordre]
        hors = [x for x in ordre if x not in ATTENDU]
        rang = [ATTENDU.index(x) for x in ordre if x in ATTENDU]
        desordre = rang != sorted(rang)
        intrus = []
        for nom, mot in INTRUS:
            n = len(re.findall(mot, c, re.I))
            if n:
                intrus.append("%s×%d" % (nom, n))
        # la FAQ
        i = c.find('<section class="faq-section"')
        nq = 0
        if i >= 0:
            j = c.find("</section>", i)
            nq = c[i:j].count("<details")
        lignes.append((url, pid, len(c) // 1024, nq, manque, hors, desordre, intrus, ordre))

    print("%-46s %4s %3s  %s" % ("url", "ko", "FAQ", "anomalies"))
    print("-" * 124)
    for url, pid, ko, nq, manque, hors, des, intrus, ordre in lignes:
        a = []
        if manque:
            a.append("manque: " + ",".join(x.replace("-section", "") for x in manque))
        if hors:
            a.append("en trop: " + ",".join(hors))
        if des:
            a.append("ORDRE")
        if intrus:
            a.append("intrus: " + ", ".join(intrus))
        print("%-46s %4d %3d  %s" % (url[:46], ko, nq, " · ".join(a) or "conforme"))

    print("\n=== ordres rencontres ===")
    from collections import Counter
    c2 = Counter(tuple(x[8]) for x in lignes)
    for o, n in c2.most_common():
        print("  %2d page(s) : %s" % (n, " > ".join(y.replace("-section", "") for y in o)))


if __name__ == "__main__":
    main()
