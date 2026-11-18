#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le pied de page, apres le depart du medical : trois places, neuf orphelines.

Le balayage du site montre neuf pages publiees qu'aucune autre ne cite.
Une page sans lien entrant n'est pas crawlee ; elle n'existe pas. Cinq
d'entre elles ont leur place dans le pied, qui vient justement de perdre
trois entrees medicales et n'en listait que huit sur quinze du cote des
fonctionnalites.

Au passage, une erreur d'ancre : le pied etiquetait « ERP Fruits et
légumes » un lien vers /agroalimentaire/maraicher/, dont le titre et le
chapeau disent « ERP Maraîcher ». La page qui porte exactement ce nom
existe — et c'est l'une des neuf orphelines. Chacune recupere son ancre.

Usage :  python3 pied_agro.py           (blanc)
         python3 pied_agro.py --poser   (ecrit)
"""

import os
import re
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import ns_api                    # noqa: E402
import deployer_gabarit as D     # noqa: E402

# L'ancre mal attribuee, rendue a la page qui la porte.
CORRIGE = ('<li><a href="/agroalimentaire/maraicher/">ERP Fruits et légumes</a></li>',
           '<li><a href="/agroalimentaire/maraicher/">ERP Maraîcher</a></li>')

# Colonne « Industries » : apres quelle entree, quoi ajouter.
INDUSTRIES = ('<li><a href="/negoce/"',
              '<li><a href="/agroalimentaire/fruits-et-legumes/">ERP Fruits et légumes</a></li>'
              '<li><a href="/agroalimentaire/produits-de-la-mer/">ERP Produits de la mer</a></li>'
              '<li><a href="/agroalimentaire/pme-en-croissance/">ERP PME agroalimentaire</a></li>')
# Colonne « Fonctionnalités ».
FONCTIONS = ('<li><a href="/fonctionnalites/import-export/">Logiciel Import Export</a></li>',
             '<li><a href="/fonctionnalites/import-export/">Logiciel Import Export</a></li>'
             '<li><a href="/fonctionnalites/logiciel-devis-commande-bon-livraison/">'
             'Logiciel Devis Commande BL</a></li>'
             '<li><a href="/fonctionnalites/gestion-consigne-bouteille-logiciel/">'
             'Logiciel de Consigne Bouteille</a></li>')
NEUFS = ("/agroalimentaire/fruits-et-legumes/", "/agroalimentaire/produits-de-la-mer/",
         "/agroalimentaire/pme-en-croissance/",
         "/fonctionnalites/logiciel-devis-commande-bon-livraison/",
         "/fonctionnalites/gestion-consigne-bouteille-logiciel/")
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/pied-agro-avant")


def nettoyer(url, c, notes):
    depart = c
    if CORRIGE[0] in c:
        c = c.replace(CORRIGE[0], CORRIGE[1])
        notes.append("ancre maraicher rendue")
    # On n'ajoute que dans le pied, et une seule fois.
    i = c.find(INDUSTRIES[0])
    if i >= 0 and "/agroalimentaire/fruits-et-legumes/" not in c[i:i + 900]:
        fin = c.find("</li>", i) + len("</li>")
        c = c[:fin] + INDUSTRIES[1] + c[fin:]
        notes.append("3 metiers ajoutes")
    if FONCTIONS[0] in c and "/fonctionnalites/logiciel-devis-commande" not in c:
        c = c.replace(FONCTIONS[0], FONCTIONS[1], 1)
        notes.append("2 fonctionnalites ajoutees")
    if not notes:
        return depart

    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
    if set(D.liens(depart)) - set(D.liens(c)):
        raise SystemExit("ARRET — lien(s) perdu(s) sur %s : %s"
                         % (url, sorted(set(D.liens(depart)) - set(D.liens(c)))[:3]))
    if c.count("<section class=") != depart.count("<section class="):
        raise SystemExit("ARRET — le nombre de sections bouge sur %s" % url)
    for cible in NEUFS:
        n = len(re.findall(r'href="(?:https://www\.helloharel\.com)?%s"'
                           % re.escape(cible), c))
        if n > 1 and cible not in url:
            raise SystemExit("ARRET — %s cite %d fois sur %s" % (cible, n, url))
    if "ERP Fruits et légumes</a></li>" in c and \
            c.count('href="/agroalimentaire/maraicher/">ERP Fruits et légumes') :
        raise SystemExit("ARRET — l'ancre mal attribuee est encore la sur %s" % url)
    if len(c) > D.PLAFOND:
        # Une page deja au-dessus du seuil de rendu ne doit pas grossir de
        # plus. On la laisse telle quelle et on la signale.
        notes.clear()
        notes.append("LOURDE — %d o, non touchee" % len(depart))
        return depart
    return c


def main():
    poser = "--poser" in sys.argv
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    tout = []
    for t in ("pages", "posts"):
        p = 1
        while True:
            lot = ns_api.call("wp/v2/%s?per_page=100&page=%d&status=publish"
                              "&_fields=id,link" % (t, p))
            if not lot:
                break
            tout += [(t, x["id"],
                      x["link"].replace("https://www.helloharel.com", "") or "/")
                     for x in lot]
            if len(lot) < 100:
                break
            p += 1
    n = 0
    for t, pid, url in sorted(tout, key=lambda z: z[2]):
        c = w.get_raw(t, pid)["content"]["raw"]
        notes = []
        c2 = nettoyer(url, c, notes)
        if not notes:
            continue
        n += 1
        if n <= 3 or not poser:
            print("%-52s %d -> %d o · %s" % (url[:52], len(c), len(c2),
                                             " · ".join(notes)))
        if poser:
            os.makedirs(SAUV, exist_ok=True)
            open(os.path.join(SAUV, "avant-%s-%d.html" % (t, pid)), "w",
                 encoding="utf-8").write(c)
            w.update_content(t, pid, c2, live=True)
            time.sleep(0.15)
    print("\n%d page(s) touchee(s)" % n)
    if not poser:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
