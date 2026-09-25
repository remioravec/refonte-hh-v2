#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose les images sous les H2 et remplace l'appel a l'action.

Les images viennent de la mediatheque et sont choisies par le sujet du
titre, sans jamais se repeter dans un meme article. Un titre dont tous les
themes sont deja pris n'en recoit pas : une image de hasard sous un titre
est pire que pas d'image.

L'appel a l'action reprend ce que Remi demande — le client doit se
reconnaitre : une photo de son quotidien, le probleme tel qu'il le vit, la
reponse ensuite. Le probleme est tire de ce que l'article decrit.

Usage :  python3 poser_blog_visuels.py            (blanc)
         python3 poser_blog_visuels.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import blog_visuels as V         # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/blog-visuels-avant")
ARTICLE = 7761
URL = "/blog/tracabilite-lot-dlc-logiciel/"


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    c = w.get_raw("posts", ARTICLE)["content"]["raw"]
    depart = c

    i = c.find('<article class="hha-art"')
    j = c.find("</article>", i)
    if i < 0 or j < 0:
        raise SystemExit("ARRET — corps d'article introuvable")
    corps = c[i:j]

    # les H2 du corps, dans l'ordre
    h2 = list(re.finditer(r"<h2[^>]*>(.*?)</h2>", corps, re.S))
    titres = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() for m in h2]
    themes = V.repartir(titres)
    poses = []
    for m, t, th in list(zip(h2, titres, themes))[::-1]:
        if not th:
            continue
        corps = corps[:m.end()] + V.figure(th) + corps[m.end():]
        poses.append((t, th))
    c = c[:i] + corps + c[j:]

    # l'appel a l'action : on reprend les liens de l'ancien bloc
    m = re.search(r'<h2 class="hhb-cta-t">.*?</ul>', c, re.S)
    if not m:
        raise SystemExit("ARRET — bloc d'appel a l'action introuvable")
    liens = re.findall(r'href="([^"]+)"', m.group(0))
    if len(liens) < 2:
        raise SystemExit("ARRET — %d lien(s) dans l'ancien bloc" % len(liens))
    theme_art = V.theme_du_titre(" ".join(titres[:2])) or "defaut"
    c = c[:m.start()] + V.bloc_accroche(theme_art, liens[0], liens[1]) + c[m.end():]

    if '<style id="hh-blog-visuels">' in c:
        c = re.sub(r'<style id="hh-blog-visuels">.*?</style>', V.CSS, c, flags=re.S)
    else:
        c = c[:c.find('<article class="hha-art"')] + V.CSS \
            + c[c.find('<article class="hha-art"'):]

    # ── controles ─────────────────────────────────────────────────────────
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge")
    for x in liens:
        if x not in D.liens(c):
            raise SystemExit("ARRET — lien d'action perdu : %s" % x)
    if c.count("<h2") != depart.count("<h2") - 1:
        raise SystemExit("ARRET — %d H2 au lieu de %d (le titre du bloc d'action part)"
                         % (c.count("<h2"), depart.count("<h2") - 1))
    img = len(re.findall(r'<figure class="hhb-img"', c))
    if img != len(poses):
        raise SystemExit("ARRET — %d figures pour %d attendues" % (img, len(poses)))

    print("%-46s %d -> %d ko" % (URL, len(depart) // 1024, len(c) // 1024))
    for t, th in poses[::-1]:
        print("   %-56s %s" % (t[:56], th))
    print("   accroche : theme %s, %d octets" % (theme_art, len(V.bloc_accroche(theme_art, *liens[:2]))))
    if poser:
        open(os.path.join(SAUV, "avant-%d.html" % ARTICLE), "w",
             encoding="utf-8").write(depart)
        w.update_content("posts", ARTICLE, c, live=True)
        print("\n   pose")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
