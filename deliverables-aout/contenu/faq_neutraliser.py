#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retire le balisage FAQPage de l'accordeon, et ne deplie plus la premiere
question par defaut.

Pourquoi : les reponses de ces FAQ sont, pour cinq des six questions de
chaque page, du texte de boulangerie avec un mot echange. Sur la page
torrefacteur, la reponse « Comment calculer le prix de revient en
torrefaction ? » parle de baguette tradition, de croissant, de perte au
petrissage et de pate feuilletee. C'est anterieur a la mise en accordeon
— le texte dormait dans le tiroir. Mais un balisage FAQPage rend ce texte
eligible aux resultats enrichis et aux reponses generatives : Google
pourrait citer « baguette tradition » sous une requete ERP torrefaction.

Tant que les reponses ne sont pas reecrites metier par metier, on ne
declare rien a Google et on n'ouvre rien d'office. Le balisage revient
avec du texte juste — pas avant.

Usage :  python3 faq_neutraliser.py            (blanc)
         python3 faq_neutraliser.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w         # noqa: E402
import scroll_sticky as SY    # noqa: E402

PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def main():
    poser = "--poser" in sys.argv
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        i = c.find('<section class="faq-section"')
        j = c.find("</section>", i) + len("</section>")
        if i < 0 or j <= i:
            raise SystemExit("ARRET — section FAQ introuvable sur %s" % url)
        sec = c[i:j]

        av_ld = len(re.findall(r'<script type="application/ld\+json">', sec))
        sec = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*?'
                     r'FAQPage(?:(?!</script>).)*?</script>', "", sec, flags=re.S)
        av_ip = len(re.findall(r'\sitem(?:scope|prop|type)(?:="[^"]*")?', sec))
        sec = re.sub(r'\sitem(?:scope|prop|type)(?:="[^"]*")?', "", sec)
        sec = sec.replace("<details open ", "<details ").replace("<details open>", "<details>")

        reste = sec.count("FAQPage") + sec.count("itemprop")
        if reste:
            raise SystemExit("ARRET — %d marque(s) de balisage survivent sur %s" % (reste, url))
        if sec.count("<details") != 6:
            raise SystemExit("ARRET — %d accordeons apres coup sur %s"
                             % (sec.count("<details"), url))
        if " open" in sec[:sec.find("</summary>")]:
            raise SystemExit("ARRET — la premiere question reste depliee sur %s" % url)

        neuf = c[:i] + sec + c[j:]
        av = re.findall(r'href="([^"]+)"', c)
        if sorted(av) != sorted(re.findall(r'href="([^"]+)"', neuf)):
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s" % url)

        print("%-42s %d JSON-LD retire · %d attributs de balisage retires · "
              "premiere question repliee" % (url, av_ld, av_ip))
        if poser:
            w.update_content("pages", page, neuf, live=True)
            print("   pose")
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
