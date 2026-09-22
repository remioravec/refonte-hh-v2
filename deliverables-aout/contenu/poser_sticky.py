#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose la section fonctionnalites en defilement colle sur les trois pages.

Torrefacteur (10935), brasseur (10896), chocolatier (10894). Aucune n'est
protegee par la regle 0 — le script refuse de demarrer si l'une d'elles y
figurait.

Le markup vient de scroll_sticky.section(), nourri par le module a onglets
deja en place sur chaque page : titres, chapos, puces, liens de maillage et
ecrans sont repris tels quels. Seule la mise en scene change.

Ce qu'on ne touche pas : la feuille de style d'agro_ui, qui vit AVANT la
section et que le nouveau module continue d'utiliser via la classe .hhf.

Usage :  python3 poser_sticky.py            (blanc)
         python3 poser_sticky.py --poser    (ecrit)
"""

import os
import re
import sys
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w         # noqa: E402
import scroll_sticky as SY    # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "sticky-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]

        i = c.find('<section class="features-section"')
        j = c.find("</section>", i) + len("</section>")
        if i < 0 or j <= i:
            raise SystemExit("ARRET — section introuvable sur %s" % url)
        if "<section" in c[i + 10:j]:
            raise SystemExit("ARRET — section imbriquee sur %s" % url)
        if 'class="hhf-bar"' not in c[i:j]:
            raise SystemExit("ARRET — %s ne porte pas le module a onglets" % url)

        entete, blocs = SY.extraire(c)
        neuf = c[:i] + SY.section(entete, blocs) + c[j:]

        # Aucun lien ne doit se perdre a la conversion : c'est le maillage.
        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        av = re.findall(r'href="([^"]+)"', corps(c))
        ap = re.findall(r'href="([^"]+)"', corps(neuf))
        if sorted(av) != sorted(ap):
            perdus = set(av) - set(ap)
            raise SystemExit("ARRET — %d lien(s) perdu(s) sur %s : %s"
                             % (len(perdus), url, list(perdus)[:4]))
        # Les ecrans non plus. Le nouveau module les porte DEUX fois : une
        # dans la colonne collee du bureau, une sous chaque texte pour le
        # telephone. Un seul des deux jeux s'affiche a la fois — mais les
        # deux pesent dans la page, et c'est le prix de cette mise en scene.
        av_ui, ap_ui = corps(c).count('class="ui"'), corps(neuf).count('class="ui"')
        if ap_ui != 2 * av_ui:
            raise SystemExit("ARRET — %d ecrans avant, %d apres (attendu %d) sur %s"
                             % (av_ui, ap_ui, 2 * av_ui, url))

        print("%-42s %d fonctionnalites · %d liens · %d ecrans (%d affiches a la fois)"
              " · %+d ko"
              % (url, len(blocs), len(ap), ap_ui, av_ui, (len(neuf) - len(c)) // 1024))

        if not poser:
            continue
        open(os.path.join(SAUV, "avant-%d.html" % page), "w", encoding="utf-8").write(c)
        w.update_content("pages", page, neuf, live=True)
        print("   pose (sauvegarde : sticky-avant/avant-%d.html)" % page)

    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")
        return

    print("\n--- verification en ligne ---")
    import time
    time.sleep(4)
    for cle, (page, url) in SY.PAGES.items():
        req = urllib.request.Request("https://www.helloharel.com" + url,
                                     headers={"User-Agent": "Mozilla/5.0"})
        h = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
        pas = h.count('class="sy-pas"')
        ecr = len(re.findall(r'<li data-actif="[01]" aria-hidden=', h))
        onglets = h.count('class="hhf-bar"')
        hhf = 'class="sy hhf"' in h
        ok = pas == 1 and ecr >= 5 and onglets == 0 and hhf
        print("   %-42s %s  %d pas · %d ecrans · onglets restants %d · .hhf %s"
              % (url, "OK " if ok else "KO ", pas, ecr, onglets, "oui" if hhf else "NON"))


if __name__ == "__main__":
    main()
