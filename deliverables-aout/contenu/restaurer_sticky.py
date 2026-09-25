#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remet les trois pages metier dans l'etat sauvegarde avant la derniere pose.

Motif : apres la pose du 22/09 qui ajoutait 18 ko a chaque page (un second
jeu d'ecrans pour que le titre arrive avant le tableau de bord sur
telephone), le site a cesse de rendre le contenu. La page servie est
complete — en-tete, pied, balises fermees — mais vide de ses neuf sections.
Le contenu en base, lui, est intact : c'est donc le rendu qui lache, pas
l'enregistrement.

On revient a la derniere version qui s'affichait, puis on cherche.

Usage :  python3 restaurer_sticky.py            (blanc)
         python3 restaurer_sticky.py --poser    (ecrit)
"""

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w          # noqa: E402
import scroll_sticky as SY     # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/sticky-avant")


def main():
    poser = "--poser" in sys.argv
    print("mode :", "RESTAURATION REELLE" if poser else "blanc", "\n")
    for cle, (page, url) in SY.PAGES.items():
        f = os.path.join(SAUV, "avant-%d.html" % page)
        if not os.path.exists(f):
            raise SystemExit("ARRET — pas de sauvegarde pour %s" % url)
        av = open(f, encoding="utf-8").read()
        act = w.get_raw("pages", page)["content"]["raw"]
        # La sauvegarde doit etre une vraie page, pas un fragment.
        if av.count("<section class=") < 8:
            raise SystemExit("ARRET — sauvegarde incomplete pour %s (%d sections)"
                             % (url, av.count("<section class=")))
        print("%-42s actuel %d ko -> sauvegarde %d ko (%+d ko) · %d sections"
              % (url, len(act) // 1024, len(av) // 1024,
                 (len(av) - len(act)) // 1024, av.count("<section class=")))
        if poser:
            w.update_content("pages", page, av, live=True)
            print("   restaure")
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
