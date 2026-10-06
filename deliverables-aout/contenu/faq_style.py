#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remet a jour la seule feuille de style de l'accordeon FAQ, sur place.

On ne retouche ni les questions, ni les reponses, ni le balisage : on
remplace le bloc <style id="hh-faq-accordeon"> par celui de
faq_accordeon.CSS, qui reste la source unique. Le script refuse d'ecrire
si le corps de la page a bouge d'un seul caractere en dehors de ce bloc.

Usage :  python3 faq_style.py            (blanc)
         python3 faq_style.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w         # noqa: E402
import scroll_sticky as SY    # noqa: E402
import faq_accordeon as F     # noqa: E402

PROTEGEES = {1726, 2818, 2839, 5477, 11162}
MARQUE = '<style id="hh-faq-accordeon">'


def main():
    poser = "--poser" in sys.argv
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        i = c.find(MARQUE)
        if i < 0:
            raise SystemExit("ARRET — feuille de l'accordeon absente sur %s" % url)
        j = c.find("</style>", i) + len("</style>")
        neuf = c[:i] + F.CSS + c[j:]

        # Hors de la feuille, rien ne doit changer.
        net = lambda t: t[:t.find(MARQUE)] + t[t.find("</style>", t.find(MARQUE)) + 8:]
        if net(c) != net(neuf):
            raise SystemExit("ARRET — le corps a bouge hors de la feuille sur %s" % url)
        print("%-42s feuille %d -> %d octets" % (url, j - i, len(F.CSS)))
        if poser:
            w.update_content("pages", page, neuf, live=True)
            print("   pose")
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
