#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deux reponses de la FAQ glacier renvoyaient a un calculateur retire.

« Le calculateur en haut de cette page » : il n'y en a plus. Le lecteur
suit l'indication, ne trouve rien, et la reponse perd sa conclusion. On
remplace le renvoi par ce qu'il promettait — le resultat lui-meme.
"""

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

REMPLACEMENTS = [
 ("<p>Le calculateur en haut de cette page fait les trois premières étapes "
  "avec vos chiffres. Pour la méthode complète, poste par poste, voyez notre "
  '<a href="/blog/calculer-le-prix-de-revient-en-boulangerie/" '
  'style="color:#00B1F5;font-weight:600;text-decoration:underline;">'
  "logiciel de prix de revient</a>.</p>",

  "<p>L'ordre compte : un coût de mix juste, divisé par un foisonnement faux, "
  "donne un prix au litre faux. Reprenez le foisonnement réel de chaque "
  "turbine, mesuré sur une production et non sur la fiche machine — c'est là "
  "que se loge l'essentiel de l'écart. La méthode complète, poste par poste, "
  'est détaillée dans notre <a href="/blog/calculer-le-prix-de-revient-en-'
  'boulangerie/" style="color:#00B1F5;font-weight:600;text-decoration:'
  'underline;">logiciel de prix de revient</a>.</p>'),

 ("Le calculateur en haut de page pose le verdict sur votre propre mix.",

  "Le calcul se fait dans l'autre sens que l'intuition : partez du poids "
  "minimal imposé par votre dénomination, divisez la densité du mix par ce "
  "poids, retirez un, et vous tenez le foisonnement maximal autorisé."),
]


def main():
    poser = "--poser" in sys.argv
    pid = dict((u, p) for p, u in D.cibles())["/agroalimentaire/glacier/"]
    c = w.get_raw("pages", pid)["content"]["raw"]
    depart = c
    for avant, apres in REMPLACEMENTS:
        if avant not in c:
            raise SystemExit("ARRET — passage introuvable : %s" % avant[:70])
        if c.count(avant) != 1:
            raise SystemExit("ARRET — %d occurrences de %s"
                             % (c.count(avant), avant[:50]))
        c = c.replace(avant, apres)

    import re
    reste = re.findall(r"calculateur|calculette|simulateur|quiz", c, re.I)
    if reste:
        raise SystemExit("ARRET — il reste %d renvoi(s) : %s" % (len(reste), reste))
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge")
    perdus = [x for x in D.liens(depart) if x not in D.liens(c)]
    if perdus:
        raise SystemExit("ARRET — lien(s) perdu(s) : %s" % perdus)
    if c.count("<details") != depart.count("<details"):
        raise SystemExit("ARRET — la FAQ a bouge")
    if len(c) > 275_000:
        raise SystemExit("ARRET — %d o, au-dela du plafond" % len(c))

    print("/agroalimentaire/glacier/  %d -> %d o · 2 renvois au calculateur "
          "remplaces par leur reponse" % (len(depart), len(c)))
    if poser:
        w.update_content("pages", pid, c, live=True)
        print("pose.")
    else:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
