#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deux reparations de structure sur les trois pages metier.

1. UN </div> MANQUANT DANS LE HERO. En remplacant le badge de reassurance,
   mon expression reguliere exigeait trois </div> la ou le badge n'en ferme
   que deux : elle a emporte celui de .hero-text. Consequence : #hh-page ne
   se fermait plus, et tout ce qui suit se retrouvait dans un conteneur
   jamais clos.

2. LA CARTE ORPHELINE ENTRE LA FAQ ET LES AVIS. Un <div class="bento-card">
   pose en enfant direct de #hh-page, hors de toute section, sans la grille
   qui lui donnait sa mise en page. Il se rend en bloc blanc de 300 px avec
   une icone perdue dedans — c'est la « petite image dans le vide » signalee
   des le 22/09, que j'avais attribuee a tort au tiroir de la FAQ. Elle est
   anterieure a mes interventions.

   Elle emporte avec elle un lien vers /agroalimentaire/, ancre « Voir
   toutes les solutions metiers agro ». Le carrousel des metiers de la meme
   page pointe deja vers cette destination : le maillage ne perd pas sa
   cible, seulement un doublon casse.

Le script refuse d'ecrire si l'equilibre des <div> n'est pas exactement
retabli.

Usage :  python3 reparer_structure.py            (blanc)
         python3 reparer_structure.py --poser    (ecrit)
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

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "structure-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def FRAIS():
    import random
    return "?hh=%d" % random.randrange(10 ** 9)


def lire_page(url):
    import time
    for essai in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(
                "https://www.helloharel.com" + url + FRAIS(),
                headers={"User-Agent": "Mozilla/5.0"}),
                timeout=90).read().decode("utf-8", "replace")
            if "</html>" in h:
                return h
        except Exception:
            pass
        time.sleep(2 * (essai + 1))
    raise SystemExit("ARRET — page %s illisible en entier" % url)


def sans_code(t):
    """Le contenu, scripts et styles neutralises, longueurs preservees."""
    return re.sub(r"<(script|style)[^>]*>.*?</\1>",
                  lambda m: " " * len(m.group(0)), t, flags=re.S)


def solde(t):
    t = sans_code(t)
    return len(re.findall(r"<div\b", t)) - len(re.findall(r"</div>", t))


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        avant = solde(c)
        neuf = c

        # ── 1. le </div> de .hero-text ────────────────────────────────────
        i = neuf.find('<section class="hero-section"')
        j = neuf.find("</section>", i)
        hero = neuf[i:j]
        if solde(hero) == 1:
            m = re.search(r'(</div></div>)(\s*)(<div class="hero-image-spacer">)', hero)
            if not m:
                raise SystemExit("ARRET — point de recollement introuvable sur %s" % url)
            hero2 = hero[:m.end(1)] + "</div>" + hero[m.end(1):]
            if solde(hero2) != 0:
                raise SystemExit("ARRET — le Hero reste desequilibre sur %s" % url)
            neuf = neuf[:i] + hero2 + neuf[j:]
            hero_ok = "recolle"
        elif solde(hero) == 0:
            hero_ok = "deja sain"
        else:
            raise SystemExit("ARRET — Hero a %+d sur %s, cas non prevu"
                             % (solde(hero), url))

        # ── 2. la carte orpheline ─────────────────────────────────────────
        m = re.search(r'<div class="bento-card[^"]*"', neuf)
        if m:
            fin = RA.div_complet(neuf, m.start())
            carte = neuf[m.start():fin]
            if solde(carte) != 0:
                raise SystemExit("ARRET — la carte orpheline n'est pas un bloc clos sur %s" % url)
            # elle doit bien etre hors de toute section
            ouv = neuf.rfind("<section", 0, m.start())
            fer = neuf.rfind("</section>", 0, m.start())
            if ouv > fer:
                raise SystemExit("ARRET — la carte est DANS une section sur %s" % url)
            perdus = re.findall(r'href="([^"]+)"', carte)
            neuf = neuf[:m.start()] + neuf[fin:]
            carte_ok = "retiree (%d o, lien %s)" % (len(carte), ", ".join(perdus) or "aucun")
        else:
            carte_ok = "absente"
            perdus = []

        apres = solde(neuf)
        if apres != 0:
            raise SystemExit("ARRET — solde des <div> a %+d apres reparation sur %s"
                             % (apres, url))

        # les liens : seul celui de la carte a le droit de partir
        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        av = re.findall(r'href="([^"]+)"', corps(c))
        ap = re.findall(r'href="([^"]+)"', corps(neuf))
        reste = list(av)
        for x in perdus:
            if x in reste:
                reste.remove(x)
        if sorted(reste) != sorted(ap):
            raise SystemExit("ARRET — lien(s) perdu(s) hors de la carte sur %s" % url)
        if neuf.count("<section class=") != c.count("<section class="):
            raise SystemExit("ARRET — une section a disparu sur %s" % url)

        print("%-42s solde %+d -> %+d · Hero %s · carte %s"
              % (url, avant, apres, hero_ok, carte_ok))
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
    time.sleep(6)
    for cle, (page, url) in SY.PAGES.items():
        h = lire_page(url)
        i = h.find('<div id="hh-page">')
        f = h.find("</footer>")
        corps = sans_code(h[i:f]) if i >= 0 else ""
        d = len(re.findall(r"<div\b", corps)) - len(re.findall(r"</div>", corps))
        sect = h.count("<section class=")
        bento = h.count("bento-card")
        ok = sect >= 8 and bento == 0
        print("   %-42s %s  %d sections · carte orpheline %s · solde du corps %+d"
              % (url, "OK " if ok else "KO ", sect,
                 "absente" if bento == 0 else "PRESENTE", d))


if __name__ == "__main__":
    main()
