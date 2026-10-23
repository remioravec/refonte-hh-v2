#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qui peut recevoir le gabarit des trois pages metier refaites ?

On ne deploie rien ici : on releve, page par page, ce qui s'y trouve. Une
page ne recoit un composant que si elle porte deja celui qu'il remplace —
autrement ce n'est plus un deploiement, c'est une refonte, et ca se decide
page par page.

Trois verrous non negociables :
  · les cinq pages de la regle 0 sont exclues d'office ;
  · une page dont _elementor_data n'est pas vide n'est jamais touchee ;
  · le contenu rendu lache au-dela d'environ 280 ko : toute page qui s'en
    approche est signalee avant, pas apres.
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w      # noqa: E402
import ns_api             # noqa: E402

PROTEGEES = {1726: "regle 0", 2818: "regle 0", 2839: "regle 0",
             5477: "regle 0", 11162: "regle 0"}
FAITES = {10935, 10896, 10894}
PLAFOND = 280_000

COMPOSANTS = [
    ("fonctionnalites", lambda c: 'class="hhf-bar"' in c or 'class="sy-ecrans"' in c),
    ("ecrans agro_ui", lambda c: c.count('class="ui"') >= 3),
    ("FAQ a tiroir", lambda c: 'id="faqDrawerOverlay"' in c),
    ("FAQ accordeon", lambda c: "<details" in c),
    ("avis grille", lambda c: 'class="reviews-grid"' in c),
    ("avis carrousel", lambda c: 'class="avis-file"' in c),
    ("equipe 15", lambda c: c.count('class="team-card') > 4),
    ("equipe rail", lambda c: 'class="eq-rail"' in c),
    ("cartes metier", lambda c: 'class="metier-slide' in c),
    ("Hero + sous-titre", lambda c: 'class="hero-cta-sub"' in c),
    ("carte orpheline", lambda c: 'class="bento-card' in c),
]


def solde(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", lambda m: " " * len(m.group(0)), t, flags=re.S)
    return len(re.findall(r"<div\b", t)) - len(re.findall(r"</div>", t))


def pages():
    out, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/pages?per_page=100&page=%d&status=publish&_fields=id,link" % p)
        if not lot:
            break
        out += lot
        if len(lot) < 100:
            break
        p += 1
    return out


def main():
    cibles = []
    for x in pages():
        u = x["link"].replace("https://www.helloharel.com", "")
        if u.startswith("/agroalimentaire/") or u.startswith("/fonctionnalites/"):
            cibles.append((x["id"], u))
    cibles.sort(key=lambda t: t[1])

    print("%-6s %-46s %6s %-9s %s" % ("id", "url", "ko", "elementor", "composants"))
    print("-" * 132)
    for pid, u in cibles:
        if pid in PROTEGEES:
            print("%-6d %-46s %6s %-9s  >>> EXCLUE (%s)" % (pid, u[:46], "", "", PROTEGEES[pid]))
            continue
        d = w.get_raw("pages", pid)
        c = d["content"]["raw"]
        el = (d.get("meta") or {}).get("_elementor_data")
        if el in (None, "", "[]"):
            el = "vide"
        else:
            el = "PLEIN"
        marques = [n for n, t in COMPOSANTS if t(c)]
        alerte = ""
        if len(c) > PLAFOND * 0.93:
            alerte += " !! %d ko, proche du plafond de rendu" % (len(c) // 1024)
        if solde(c) != 0:
            alerte += " !! solde des <div> %+d" % solde(c)
        if pid in FAITES:
            alerte += "  (deja faite)"
        print("%-6d %-46s %6d %-9s %s%s"
              % (pid, u[:46], len(c) // 1024, el, ", ".join(marques) or "—", alerte))


if __name__ == "__main__":
    main()
