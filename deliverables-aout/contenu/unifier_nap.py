#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Une seule ecriture du NAP sur tout le site.

Remi a tranche le 22/09 : le telephone est le 06 18 06 00 18, l'adresse
electronique est contact@helloharel.com. Ce script applique ces deux
decisions partout, et unifie au passage ce qui variait autour.

CE QU'IL FAIT :
  1. contact@helloharel.com remplace support@helloharel.com, dans le texte
     comme dans le balisage JSON-LD ;
  2. le 01 85 54 01 54 du bouton « Appeler un expert » devient le
     06 18 06 00 18 — deux numeros valent zero pour un NAP ;
  3. « 6 Avenue de Rueil » s'ecrit « 6 avenue de Rueil » : une casse
     differente affaiblit la correspondance ;
  4. l'adresse electronique entre dans le bloc NAP du pied de page, sous le
     telephone.

LA REGLE 0 ET CE SCRIPT. Les cinq pages protegees ne recoivent PAS le bloc
NAP — ce serait ajouter une section. Elles recoivent en revanche les
corrections 1 a 3, qui ne touchent ni a l'URL, ni au gabarit, ni au title,
ni a la structure : elles remplacent une valeur fausse par la bonne. C'est
reparer, pas optimiser.

Usage :  python3 unifier_nap.py            (blanc)
         python3 unifier_nap.py --poser    (ecrit)
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

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/unifier-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

MAIL = "contact@helloharel.com"
TEL_LIEN = "+33618060018"
TEL_AFFICHE = "06 18 06 00 18"

LIGNE_MAIL = ('<span><a href="mailto:%s">%s</a></span>' % (MAIL, MAIL))


def corriger(c):
    """Rend (contenu, [ce qui a change])."""
    notes = []

    n = c.count("support@helloharel.com")
    if n:
        c = c.replace("support@helloharel.com", MAIL)
        notes.append("support@ -> contact@ ×%d" % n)

    # le second numero, sous toutes ses ecritures
    for motif, quoi in ((r"\+33185540154", "lien tel:"),
                        (r"01[\s.\-]?85[\s.\-]?54[\s.\-]?01[\s.\-]?54", "affichage")):
        m = re.findall(motif, c)
        if m:
            c = re.sub(motif, TEL_LIEN if quoi == "lien tel:" else TEL_AFFICHE, c)
            notes.append("01 85 54 01 54 -> 06 18 06 00 18 (%s ×%d)" % (quoi, len(m)))

    n = len(re.findall(r"6 Avenue de Rueil", c))
    if n:
        c = c.replace("6 Avenue de Rueil", "6 avenue de Rueil")
        notes.append("« 6 Avenue » -> « 6 avenue » ×%d" % n)

    # l'adresse electronique dans le bloc NAP, juste apres le telephone
    if 'class="hh-nap"' in c and "mailto:%s" % MAIL not in c:
        m = re.search(r'(<span>Tél\. <a href="tel:[^"]+">[^<]+</a></span>)', c)
        if m:
            c = c[:m.end(1)] + LIGNE_MAIL + c[m.end(1):]
            notes.append("e-mail ajoute au bloc NAP")
    return c, notes


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    pages, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/pages?per_page=100&page=%d&status=publish&_fields=id,link" % p)
        if not lot:
            break
        pages += lot
        if len(lot) < 100:
            break
        p += 1

    touchees = 0
    for x in sorted(pages, key=lambda t: t["link"]):
        pid = x["id"]
        url = x["link"].replace("https://www.helloharel.com", "") or "/"
        c = w.get_raw("pages", pid)["content"]["raw"]
        neuf, notes = corriger(c)
        if not notes:
            continue
        if D.solde(neuf) != D.solde(c):
            print("%-46s REFUSEE — le solde des <div> bouge" % url[:46])
            continue
        # aucun lien ne disparait ; seuls mailto: et tel: peuvent changer
        net = lambda t: sorted(y for y in D.liens(t)
                               if not y.startswith(("mailto:", "tel:")))
        if net(c) != net(neuf):
            print("%-46s REFUSEE — lien(s) perdu(s)" % url[:46])
            continue
        if neuf.count("<section class=") != c.count("<section class="):
            print("%-46s REFUSEE — une section a bouge" % url[:46])
            continue
        touchees += 1
        marque = "  (regle 0)" if pid in PROTEGEES else ""
        print("%-46s %s%s" % (url[:46], " · ".join(notes), marque))
        if poser:
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(c)
            w.update_content("pages", pid, neuf, live=True)
    print("\n%d page(s) %s" % (touchees, "modifiees" if poser else "a modifier"))
    if not poser:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
