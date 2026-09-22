#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les medaillons des avis passent de l'avatar dessine a la marque Google.

Rien d'autre ne bouge : ni le carrousel, ni le texte des avis, ni les noms.
On remplace la feuille des avatars par celle de la marque, et la classe
propre a chaque personne par une classe unique.

Usage :  python3 avis_google.py            (blanc)
         python3 avis_google.py --poser    (ecrit)
"""

import os
import re
import sys
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w          # noqa: E402
import scroll_sticky as SY     # noqa: E402
import avatars as AV           # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "avis-google-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        neuf = c

        # 1. les deux feuilles d'avatars — celle des avis et celle du sticky —
        #    laissent la place a celle de la marque
        feuilles = 0
        for ident in ("hh-avis-tetes", "hh-sy-tetes"):
            feuilles += len(re.findall(r'<style id="%s">' % ident, neuf))
            neuf = re.sub(r'<style id="%s">.*?</style>' % ident,
                          lambda m, i=ident: AV.feuille_google(i), neuf, flags=re.S)

        # 2. la classe propre a chaque personne devient la classe unique. Le
        #    sticky en porte une troisieme derriere : on ne touche qu'aux deux
        #    premieres.
        med = len(re.findall(r'hh-tete t[0-9a-f]{8}', neuf))
        neuf = re.sub(r'hh-tete t[0-9a-f]{8}', 'hh-tete hh-tete-g', neuf)

        if not feuilles or not med:
            raise SystemExit("ARRET — %s ne porte pas les avatars attendus "
                             "(%d feuille, %d medaillon)" % (url, feuilles, med))
        if re.search(r'hh-tete t[0-9a-f]{8}', neuf):
            raise SystemExit("ARRET — il reste un avatar personnel sur %s" % url)

        # les noms et les textes d'avis doivent etre intacts
        for motif in (r'<div class="review-name">([^<]+)</div>',
                      r'<p class="review-text">(.*?)</p>'):
            if re.findall(motif, c, re.S) != re.findall(motif, neuf, re.S):
                raise SystemExit("ARRET — le contenu des avis a bouge sur %s" % url)
        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        if sorted(re.findall(r'href="([^"]+)"', corps(c))) != \
           sorted(re.findall(r'href="([^"]+)"', corps(neuf))):
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s" % url)

        print("%-42s %d medaillons · feuille %d -> %d octets · %+d ko"
              % (url, med, len(re.search(r'<style id="hh-avis-tetes">.*?</style>',
                                         c, re.S).group(0)),
                 len(AV.feuille_google("hh-avis-tetes")), (len(neuf) - len(c)) // 1024))
        if not poser:
            continue
        open(os.path.join(SAUV, "avant-%d.html" % page), "w", encoding="utf-8").write(c)
        w.update_content("pages", page, neuf, live=True)
        print("   pose")

    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")
        return
    print("\n--- verification en ligne ---")
    import time
    time.sleep(5)
    for cle, (page, url) in SY.PAGES.items():
        h = urllib.request.urlopen(urllib.request.Request(
            "https://www.helloharel.com" + url,
            headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")
        g = len(re.findall(r'class="hh-tete hh-tete-g"', h))
        reste = len(re.findall(r'hh-tete t[0-9a-f]{8}', h))
        ok = g >= 8 and reste == 0
        print("   %-42s %s  %d marques Google · %d avatars restants"
              % (url, "OK " if ok else "KO ", g, reste))


if __name__ == "__main__":
    main()
