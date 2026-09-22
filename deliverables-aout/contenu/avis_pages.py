#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les avis Google des trois pages metier passent en carrousel continu, et les
initiales cedent la place a des avatars dessines.

Le carrousel est celui deja pose sur /agroalimentaire/ : une piste doublee
qui defile en boucle, qui s'arrete au survol et au focus, et qui redevient
un simple defilement horizontal si le visiteur a demande moins d'animation.

Les cartes d'avis ne sont pas reecrites : on reprend celles de la page,
telles quelles, et on remplace seulement le medaillon d'initiales par
l'avatar correspondant au nom. Le texte des avis reste intact — ce sont de
vrais avis Google.

Usage :  python3 avis_pages.py            (blanc)
         python3 avis_pages.py --poser    (ecrit)
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
import remanier_agro as RA     # noqa: E402
import avatars as AV           # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "avis-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def FRAIS():
    """Une URL unique par controle : le cache du site sert sinon la
    version d'avant la pose, et le controle annonce un echec faux."""
    import random
    return "?hh=%d" % random.randrange(10 ** 9)

CSS_TETE = """<style id="hh-avis-avatars">
#hh-page .review-avatar,.review-avatar{overflow:hidden !important;padding:0 !important;
 font-size:0 !important;background:transparent !important}
#hh-page .review-avatar .hh-tete,.review-avatar .hh-tete{width:100% !important;
 height:100% !important}
</style>"""


def cartes(section):
    """Rend la liste des .review-card, chacune fermee correctement."""
    out = []
    for m in re.finditer(r'<div class="review-card">', section):
        out.append(section[m.start():RA.div_complet(section, m.start())])
    return out


def poser_tete(carte):
    """Remplace le medaillon d'initiales par l'avatar du nom."""
    nom = re.search(r'<div class="review-name">([^<]+)</div>', carte)
    if not nom:
        return carte, None
    nom = nom.group(1).strip()
    neuve, n = re.subn(r'(<div class="review-avatar">)([^<]*)(</div>)',
                       lambda m: m.group(1) + AV.balise(nom) + m.group(3),
                       carte, count=1)
    return neuve, (nom if n else None)


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        i = c.find('<section class="reviews-section"')
        if i < 0:
            raise SystemExit("ARRET — section des avis introuvable sur %s" % url)
        j = c.find("</section>", i) + len("</section>")
        sec = c[i:j]
        if 'class="avis-file"' in sec:
            raise SystemExit("ARRET — %s porte deja le carrousel" % url)

        liste = cartes(sec)
        if len(liste) < 3:
            raise SystemExit("ARRET — %d carte(s) d'avis sur %s" % (len(liste), url))

        neuves, noms = [], []
        for k in liste:
            n, nom = poser_tete(k)
            if not nom:
                raise SystemExit("ARRET — carte d'avis sans nom sur %s" % url)
            neuves.append(n)
            noms.append(nom)

        # La grille devient la piste ; l'en-tete et la note ne bougent pas.
        g = sec.find('<div class="reviews-grid">')
        if g < 0:
            raise SystemExit("ARRET — grille des avis introuvable sur %s" % url)
        gf = RA.div_complet(sec, g)
        neuve = (sec[:g] + AV.feuille(noms, "hh-avis-tetes") + CSS_TETE
                 + RA.avis_carrousel(neuves) + sec[gf:])
        neuf = c[:i] + neuve + c[j:]

        # Aucun texte d'avis ne doit avoir bouge.
        av = re.findall(r'<p class="review-text">(.*?)</p>', sec, re.S)
        ap = re.findall(r'<p class="review-text">(.*?)</p>', neuve, re.S)
        if sorted(set(av)) != sorted(set(ap)):
            raise SystemExit("ARRET — un texte d'avis a change sur %s" % url)
        if len(ap) != 2 * len(av):
            raise SystemExit("ARRET — %d textes attendus (piste doublee), %d obtenus sur %s"
                             % (2 * len(av), len(ap), url))
        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        if sorted(re.findall(r'href="([^"]+)"', corps(c))) != \
           sorted(re.findall(r'href="([^"]+)"', corps(neuf))):
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s" % url)
        if neuve.count('class="hh-tete ') != 2 * len(liste):
            raise SystemExit("ARRET — %d medaillons au lieu de %d sur %s"
                             % (neuve.count('class="hh-tete '), 2 * len(liste), url))
        if len(set(re.findall(r"background-image:url", neuve))) and \
           neuve.count("background-image:url") != len(set(noms)):
            raise SystemExit("ARRET — %d images pour %d personnes sur %s"
                             % (neuve.count("background-image:url"), len(set(noms)), url))

        print("%-42s %d avis · %s · %+d ko"
              % (url, len(liste), ", ".join(noms), (len(neuf) - len(c)) // 1024))
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
    time.sleep(4)
    for cle, (page, url) in SY.PAGES.items():
        h = urllib.request.urlopen(urllib.request.Request(
            "https://www.helloharel.com" + url + FRAIS(),
            headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")
        piste = h.count('class="avis-file"')
        tetes = len(re.findall(r'<div class="review-avatar"><i class="hh-tete', h))
        grille = h.count('class="reviews-grid"')
        ok = piste == 1 and tetes >= 6 and grille == 0
        print("   %-42s %s  piste %d · %d avatars · grille restante %d"
              % (url, "OK " if ok else "KO ", piste, tetes, grille))


if __name__ == "__main__":
    main()
