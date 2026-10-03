#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applique la mise en lecture au corps de l'article temoin.

Aucun mot du texte n'est touche. Ce qui change : la feuille de style du
corps, et l'etiquette de colonne ajoutee a chaque cellule de tableau pour
que les lignes repliees en fiches sur telephone gardent leurs intitules.

Usage :  python3 poser_blog_lecture.py            (blanc)
         python3 poser_blog_lecture.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import blog_lecture as BL        # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/blog-lecture-avant")
ARTICLE = 7761
URL = "/blog/tracabilite-lot-dlc-logiciel/"


def mots(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    c = w.get_raw("posts", ARTICLE)["content"]["raw"]
    depart = c

    c, n_tab = BL.etiqueter_tableaux(c)
    if '<style id="hh-blog-lecture">' in c:
        c = re.sub(r'<style id="hh-blog-lecture">.*?</style>', BL.CSS, c, flags=re.S)
        pose = "feuille remplacee"
    else:
        i = c.find('<article class="hha-art"')
        if i < 0:
            raise SystemExit("ARRET — corps d'article introuvable")
        c = c[:i] + BL.CSS + c[i:]
        pose = "feuille posee"

    # le texte ne doit pas avoir bouge d'un mot
    av, ap = mots(D.sans_code(depart)), mots(D.sans_code(c))
    if av != ap:
        import difflib
        d = [x for x in difflib.ndiff(av.split(), ap.split()) if x[0] in "+-"][:6]
        raise SystemExit("ARRET — le texte a bouge : %s" % d)
    # Envelopper un tableau ajoute une paire equilibree : le solde ne
    # bouge pas. C'est ce qu'on verifie.
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    if sorted(D.liens(c)) != sorted(D.liens(depart)):
        raise SystemExit("ARRET — lien(s) perdu(s)")
    if "hha-tool" not in c:
        raise SystemExit("ARRET — le simulateur a disparu")
    cell = len(re.findall(r'<td[^>]*data-l="', c))

    print("%-46s %d -> %d ko" % (URL, len(depart) // 1024, len(c) // 1024))
    print("   %s (%d octets)" % (pose, len(BL.CSS)))
    print("   %d tableau(x) etiquete(s), %d cellule(s)" % (n_tab, cell))
    print("   texte : inchange, mot pour mot")
    if poser:
        open(os.path.join(SAUV, "avant-%d.html" % ARTICLE), "w",
             encoding="utf-8").write(depart)
        w.update_content("posts", ARTICLE, c, live=True)
        print("\n   pose")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
