#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retirer le bloc « Pour approfondir » du bas de page.

Attention au nom : ces deux mots designent deux choses differentes sur
le site. Une section <container> de sept cent cinquante octets posee
sous le dernier module, sur quatre pages ; et un titre interne au corps
de dix-huit articles de blog. Seule la premiere est « en bas de page ».
On ne touche pas a la seconde.

Je l'avais gardee au motif qu'elle nourrissait deux articles que rien
d'autre ne citait. C'etait faux, verification faite : les deux recoivent
des liens de l'index du blog, de /blog/min/ et l'un de l'autre. Le bloc
part sans creer d'orpheline.

Usage :  python3 retirer_approfondir.py              (blanc)
         python3 retirer_approfondir.py --poser      (ecrit)
         python3 retirer_approfondir.py --toutes     (les 4 pages)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import pilier_gabarit as P       # noqa: E402

# La page du jour, dont la Regle 0 a ete levee.
PILIER = [(1726, "/agroalimentaire/")]
# Les trois autres. Deux sont sous Regle 0 — elles attendent un accord.
AUTRES = [(5957, "/negoce/"),
          (2839, "/agroalimentaire/traiteur/"),                  # Regle 0
          (5477, "/agroalimentaire/plats-cuisines-industriels/")]  # Regle 0
PROTEGEES = {2839, 5477}
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/approfondir-avant")


def traiter(pid, url, poser):
    c = w.get_raw("pages", pid)["content"]["raw"]
    depart = c
    i = c.find("Pour approfondir")
    if i < 0:
        print("%-46s rien a retirer" % url[:46])
        return
    sec = c.rfind('<section class="', 0, i)
    nom = re.search(r'<section class="([^"]+)"', c[sec:sec + 80]).group(1).split()[0]
    if nom != "container":
        print("%-46s « Pour approfondir » est dans <%s>, pas en bas de "
              "page — on n'y touche pas" % (url[:46], nom))
        return
    fin = P.bornes(c, sec)
    if fin is None:
        raise SystemExit("ARRET — section non fermee sur %s" % url)
    bloc = c[sec:fin]
    if D.solde(bloc) != 0:
        raise SystemExit("ARRET — %d <div> non clos dans le bloc" % D.solde(bloc))
    c = c[:sec] + c[fin:]

    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
    attendus = set(re.findall(r'href="([^"]+)"', bloc))
    partis = set(D.liens(depart)) - set(D.liens(c))
    if partis - attendus:
        raise SystemExit("ARRET — lien(s) perdu(s) en trop : %s"
                         % sorted(partis - attendus)[:3])
    if c.count("<section class=") != depart.count("<section class=") - 1:
        raise SystemExit("ARRET — %d sections au lieu de %d"
                         % (c.count("<section class="),
                            depart.count("<section class=") - 1))
    if "Pour approfondir" in c:
        raise SystemExit("ARRET — le bloc est encore la sur %s" % url)

    print("%-46s %d -> %d o (-%d) · %d section(s) · liens rendus : %s"
          % (url[:46], len(depart), len(c), len(depart) - len(c),
             c.count("<section class="),
             sorted(x.replace("https://www.helloharel.com", "") for x in attendus)))
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
             encoding="utf-8").write(depart)
        w.update_content("pages", pid, c, live=True)
        print("%-46s   pose" % "")


def main():
    poser = "--poser" in sys.argv
    cibles = PILIER + (AUTRES if "--toutes" in sys.argv else [])
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    for pid, url in cibles:
        if pid in PROTEGEES and "--regle0" not in sys.argv:
            print("%-46s Regle 0 — passee (ajouter --regle0)" % url[:46])
            continue
        traiter(pid, url, poser)
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
