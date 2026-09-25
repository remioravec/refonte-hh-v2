#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retire les cartes bento posees hors de toute section, sur les pages deja
passees par le deploiement.

Sur /agroalimentaire/glacier/, une grille legitime precedait une carte
orpheline : l'etape de reparation s'arretait a la premiere carte trouvee et
laissait la seconde en place. Ce passage rattrape ce cas, sans rejouer le
reste du gabarit.

Usage :  python3 retirer_orphelines.py            (blanc)
         python3 retirer_orphelines.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/orphelines-avant")


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    touchees = 0
    for pid, url in D.cibles() + [(10935, "/agroalimentaire/torrefacteur/"),
                                  (10896, "/agroalimentaire/brasseur/"),
                                  (10894, "/agroalimentaire/chocolatier/")]:
        c = w.get_raw("pages", pid)["content"]["raw"]
        notes = []
        neuf, perdus = D.etape_reparer(c, notes)
        if neuf == c:
            continue
        if D.solde(neuf) != D.solde(c):
            raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
        if neuf.count("<section class=") != c.count("<section class="):
            raise SystemExit("ARRET — une section a disparu sur %s" % url)
        reste = D.liens(c)
        for x in perdus:
            if x in reste:
                reste.remove(x)
        if reste != D.liens(neuf):
            raise SystemExit("ARRET — lien(s) perdu(s) hors des cartes sur %s" % url)
        touchees += 1
        print("%-46s %d -> %d ko · %s · lien(s) : %s"
              % (url[:46], len(c) // 1024, len(neuf) // 1024, " · ".join(notes),
                 ", ".join(sorted(set(perdus))) or "aucun"))
        if poser:
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(c)
            w.update_content("pages", pid, neuf, live=True)
            print("%-46s   pose" % "")
    print("\n%d page(s) concernee(s)%s"
          % (touchees, "" if poser else " — blanc, rien n'a ete ecrit"))


if __name__ == "__main__":
    main()
