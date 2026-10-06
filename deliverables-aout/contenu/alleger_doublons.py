#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trois pages portent deux fois la meme feuille de style, l'une derriere
l'autre. Treize mille huit cent trente-deux octets ecrits deux fois.

Ce n'est pas un detail de proprete. Au-dela d'environ 280 ko de contenu,
le site sert un document complet et vide de toutes ses sections — on l'a
mesure en cassant trois pages. Ces trois-la sont a 274-275 ko : elles
tiennent encore, mais la prochaine modification, meme d'une ligne, les
fait basculer. Retirer le doublon leur rend leur marge.

On ne retire que des blocs strictement identiques, et on verifie que le
rendu ne bouge pas : meme nombre de sections servies avant et apres.
"""

import os
import re
import sys
import time
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

CIBLES = ("/agroalimentaire/fruits-et-legumes/",
          "/agroalimentaire/produits-de-la-mer/",
          "/agroalimentaire/pme-en-croissance/")
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/allege-avant")


def servie(url):
    for essai in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(
                "https://www.helloharel.com" + url + "?v=%d" % time.time(),
                headers={"User-Agent": "Mozilla/5.0"}), timeout=120
            ).read().decode("utf-8", "replace")
            if "</html>" in h:
                return len(re.findall(r'<section class="[^"]+"', h))
        except Exception:                      # noqa: BLE001
            pass
        time.sleep(2 * (essai + 1))
    return None


def main():
    poser = "--poser" in sys.argv
    cib = dict((u, p) for p, u in D.cibles())
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    for url in CIBLES:
        pid = cib[url]
        c = w.get_raw("pages", pid)["content"]["raw"]
        depart = c
        avant = servie(url) if poser else None

        blocs = [m for m in re.finditer(
            r'<style id="hh-agro-fonctionnalites">.*?</style>', c, re.S)]
        if len(blocs) != 2:
            print("%-42s %d bloc(s) — rien a faire" % (url[:42], len(blocs)))
            continue
        if blocs[0].group(0) != blocs[1].group(0):
            print("%-42s les deux blocs different — on n'y touche pas" % url[:42])
            continue
        c = c[:blocs[1].start()] + c[blocs[1].end():]

        if D.solde(c) != D.solde(depart):
            raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
        perdus = [x for x in D.liens(depart) if x not in D.liens(c)]
        if perdus:
            raise SystemExit("ARRET — lien(s) perdu(s) : %s" % perdus[:3])
        for motif in (r'<section class="[^"]+"', r"<details", r'<style id="'):
            a, b = len(re.findall(motif, depart)), len(re.findall(motif, c))
            attendu = a - (1 if motif == r'<style id="' else 0)
            if b != attendu:
                raise SystemExit("ARRET — %s : %d -> %d sur %s" % (motif, a, b, url))

        print("%-42s %d -> %d o (%+d)" % (url[:42], len(depart), len(c),
                                          len(c) - len(depart)))
        if poser:
            os.makedirs(SAUV, exist_ok=True)
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(depart)
            w.update_content("pages", pid, c, live=True)
            time.sleep(3)
            apres = servie(url)
            if avant is None or apres is None:
                print("   page illisible — a revoir a la main")
            elif apres != avant:
                print("   ALERTE — %s sections servies avant, %s apres"
                      % (avant, apres))
            else:
                print("   %s sections servies, inchange" % apres)
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
