#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rendre son lien entrant a /blog/grille-tarifaire-negoce-alimentaire/.

Le bloc « Pour approfondir » retire du bas de /negoce/ etait le seul
endroit du site qui citait cet article. Sans lui, zero lien entrant : une
page que rien ne cite n'est pas crawlee, et n'existe pas.

On le reloge la ou il a du sens, pas la ou c'est commode : la page
/negoce/tarifs-reporting-edi/ porte une carte « Tarification
multi-niveaux » dont le texte parle de « centaines de grilles
tarifaires ». L'ancre reprend le sujet exact de l'article et se pose
dans la phrase qui le porte, au lieu d'un « en savoir plus » neutre.

Le paragraphe est reecrit d'un mot : « grilles tarifaires » devient le
lien. Rien d'autre ne bouge.
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import ns_api                    # noqa: E402
import deployer_gabarit as D     # noqa: E402

PID, URL = 6078, "/negoce/tarifs-reporting-edi/"
CIBLE = "/blog/grille-tarifaire-negoce-alimentaire/"
AVANT = ("<p>Gérez des centaines de grilles tarifaires : par client, par "
         "segment, par volume, par saison. Mises à jour en masse.</p>")
# L'ancre reprend les mots deja ecrits. Allonger la phrase pour y loger
# une correspondance exacte serait reecrire une page qu'on n'a pas a
# toucher : « grilles tarifaires », sur une page de negoce, est naturelle,
# contigue, et tout sauf neutre.
APRES = ('<p>Gérez des centaines de <a href="%s">grilles tarifaires</a> : par '
         "client, par segment, par volume, par saison. Mises à jour en "
         "masse.</p>" % CIBLE)
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/orpheline-avant")


def entrants(cible, sauf=None):
    n, pages = 0, []
    for t in ("pages", "posts"):
        p = 1
        while True:
            lot = ns_api.call("wp/v2/%s?per_page=100&page=%d&status=publish"
                              "&_fields=id,link" % (t, p))
            if not lot:
                break
            for x in lot:
                if x["id"] == sauf:
                    continue
                c = w.get_raw(t, x["id"])["content"]["raw"]
                if re.search(r'href="(?:https://www\.helloharel\.com)?%s"'
                             % re.escape(cible),
                             re.sub(r"<(style|script)[^>]*>.*?</\1>", "", c, flags=re.S)):
                    n += 1
                    pages.append(x["link"].replace("https://www.helloharel.com", ""))
            if len(lot) < 100:
                break
            p += 1
    return n, pages


def main():
    poser = "--poser" in sys.argv
    n, ou = entrants(CIBLE)
    print("%s\n   liens entrants avant : %d %s\n" % (CIBLE, n, ou or ""))

    c = w.get_raw("pages", PID)["content"]["raw"]
    depart = c
    if CIBLE in c:
        raise SystemExit("ARRET — la page cite deja l'article")
    if c.count(AVANT) != 1:
        raise SystemExit("ARRET — %d occurrence(s) du paragraphe vise"
                         % c.count(AVANT))
    c = c.replace(AVANT, APRES)

    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge")
    if len(D.liens(c)) != len(D.liens(depart)) + 1:
        raise SystemExit("ARRET — %d liens au lieu de %d"
                         % (len(D.liens(c)), len(D.liens(depart)) + 1))
    if set(D.liens(depart)) - set(D.liens(c)):
        raise SystemExit("ARRET — lien(s) perdu(s)")
    if c.count("<section class=") != depart.count("<section class="):
        raise SystemExit("ARRET — le nombre de sections bouge")
    if len(c) > D.PLAFOND:
        raise SystemExit("ARRET — %d o, au-dela du seuil de rendu" % len(c))
    # Le texte visible ne doit pas changer : seule une ancre s'ajoute.
    nu = lambda t: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
    if nu(APRES) != nu(AVANT):
        raise SystemExit("ARRET — le texte visible a change")

    print("%s  %d -> %d o" % (URL, len(depart), len(c)))
    print("   ancre posee : « grilles tarifaires »")
    print("   dans : Tarification multi-niveaux (section fonctionnalites)")
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % PID), "w",
             encoding="utf-8").write(depart)
        w.update_content("pages", PID, c, live=True)
        n2, ou2 = entrants(CIBLE)
        print("\n   liens entrants apres : %d %s" % (n2, ou2))
        if n2 < 1:
            print("   ALERTE — toujours orpheline")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
