#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retirer le bouton fixe « Demander ma démo » du bas de l'ecran.

Il n'apparait qu'apres quarante pour cent de defilement, ce qui explique
qu'on ne le voie pas en ouvrant la page. Il n'est pas non plus propre au
telephone : le meme element se pose sur grand ecran. Il vit sur
quarante-trois pages, sous deux libelles — « Demander une démo » partout,
« Demander ma démo gratuite » sur la page pilier.

Sur telephone, il se superpose a la pastille de Maxence, posee au meme
endroit : deux appels a l'action fixes dans le meme coin, l'un par-dessus
l'autre, au-dessus du texte qu'on est en train de lire.

Partent avec lui sa feuille de style et le script qui le declenche au
defilement — sinon on laisse du code qui n'anime plus rien. Le lien vers
/contact/ qu'il portait est verifie present ailleurs sur chaque page
avant d'accepter sa disparition.

Usage :  python3 retirer_sticky_cta.py           (blanc)
         python3 retirer_sticky_cta.py --poser   (ecrit)
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
import alleger_css as A          # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/sticky-avant")


def traiter(url, c, notes):
    depart = c
    hors = re.sub(r"<(style|script)[^>]*>.*?</\1>",
                  lambda m: " " * len(m.group(0)), c, flags=re.S)
    m = re.search(r'<div class="sticky-cta"[^>]*>.*?</div>', hors, re.S)
    if not m:
        return depart
    bloc = c[m.start():m.end()]
    if D.solde(bloc) != 0:
        raise SystemExit("ARRET — bloc non clos sur %s" % url)
    lib = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", bloc)).strip()
    c = c[:m.start()] + c[m.end():]
    notes.append("bouton « %s »" % lib)

    # Le script qui le montre au defilement n'a plus d'objet.
    for mm in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>",
                               c, re.S))[::-1]:
        if "hh2StickyCta" in mm.group(1):
            if "hh2StickyCta" not in re.sub(r"<script.*?</script>", "", c, flags=re.S):
                c = c[:mm.start()] + c[mm.end():]
                notes.append("script de defilement (%d o)" % len(mm.group(0)))

    # On ne retire que SES regles. Un balayage general du code mort
    # toucherait quarante-trois pages qu'on n'a pas a reecrire aujourd'hui,
    # et demanderait de comparer le rendu de chacune.
    gagne = 0
    for mm in list(re.finditer(r"<style([^>]*)>(.*?)</style>", c, re.S))[::-1]:
        garde, retire = [], 0
        for r in A.decouper(mm.group(2)):
            sel = r.split("{", 1)[0]
            if "sticky-cta" in sel and not sel.strip().startswith("@"):
                retire += len(r)
            else:
                garde.append(r)
        if retire:
            neuve = "".join(garde)
            if neuve.count("{") != neuve.count("}"):
                raise SystemExit("ARRET — accolades desequilibrees sur %s" % url)
            c = c[:mm.start(2)] + neuve + c[mm.end(2):]
            gagne += retire
    # Les blocs @media qui ne portaient que lui deviennent vides.
    c, nv = re.subn(r"@media[^{]*\{\s*\}", "", c)
    if gagne:
        notes.append("%d o de CSS" % gagne)

    # ── controles ────────────────────────────────────────────────────────
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
    if c.count("<section class=") != depart.count("<section class="):
        raise SystemExit("ARRET — le nombre de sections bouge sur %s" % url)
    if "sticky-cta" in re.sub(r"<(style|script)[^>]*>.*?</\1>", "", c, flags=re.S):
        raise SystemExit("ARRET — le bouton est encore la sur %s" % url)
    perdus = sorted(set(D.liens(depart)) - set(D.liens(c)))
    if perdus:
        # Le seul lien qu'il portait est /contact/ : il doit rester joignable.
        raise SystemExit("ARRET — lien(s) perdu(s) sur %s : %s" % (url, perdus))
    if "/contact/" not in D.liens(c):
        raise SystemExit("ARRET — plus aucun lien vers /contact/ sur %s" % url)
    if len(c) > D.PLAFOND and len(c) >= len(depart):
        raise SystemExit("ARRET — %d o sur %s" % (len(c), url))
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
    n, gagne = 0, 0
    for t, pid, url in sorted(tout, key=lambda z: z[2]):
        c = w.get_raw(t, pid)["content"]["raw"]
        notes = []
        c2 = traiter(url, c, notes)
        if not notes:
            continue
        n += 1
        gagne += len(c) - len(c2)
        print("%-52s %d -> %d o · %s" % (url[:52], len(c), len(c2),
                                         " · ".join(notes)))
        if poser:
            os.makedirs(SAUV, exist_ok=True)
            open(os.path.join(SAUV, "avant-%s-%d.html" % (t, pid)), "w",
                 encoding="utf-8").write(c)
            w.update_content(t, pid, c2, live=True)
            time.sleep(0.15)
    print("\n%d page(s), %d o rendus" % (n, gagne))
    if not poser:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
