#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trois corrections sur /fonctionnalites/.

1. « Solutions specialisees — Cas d'usage metier dedies agroalimentaire et
   negoce » : une seconde section .features-section, retiree a la demande.

2. « Les fonctionnalites de l'ERP agroalimentaire… » en bas de page, meme
   famille que le bloc d'aout retire sur la page brasseur.

3. Le fond du Hero pointait sur bg-line-v7.png, qui repond 404 : c'est le
   seul Hero casse du site, et c'est pour cela qu'il n'y avait pas de photo.
   Il recoit une photo de la mediatheque, non utilisee ailleurs en fond.

Les liens qui partent avec les deux sections sont nommes un par un : le
script dit lesquels subsistent ailleurs sur la page et lesquels non.

Usage :  python3 nettoyer_hub_fonctions.py            (blanc)
         python3 nettoyer_hub_fonctions.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import retirer_maj_aout as R     # noqa: E402

PAGE = 4728
URL = "/fonctionnalites/"
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/hub-avant")
PHOTO = ("https://www.helloharel.com/wp-content/uploads/2026/09/"
         "erp-negoce-entrepot-allees-preparation.webp")
CASSEE = "bg-line-v7.png"


def bloc(c, ouverture):
    i = c.find(ouverture)
    if i < 0:
        return None, None
    j = c.find("</section>", i) + len("</section>")
    if "<section" in c[i + 10:j]:
        raise SystemExit("ARRET — section imbriquee : %s" % ouverture[:40])
    return i, j


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    c = w.get_raw("pages", PAGE)["content"]["raw"]
    depart = c
    partis = []

    # ── 1. la section « Cas d'usage metier » ──────────────────────────────
    m = re.search(r'<section class="features-section"[^>]*>(?:(?!</section>).)*?'
                  r"Cas d'usage m[eé]tier", c, re.S)
    if m:
        i = c.rfind('<section class="features-section"', 0, m.end())
        j = c.find("</section>", i) + len("</section>")
        sec = c[i:j]
        partis += re.findall(r'href="([^"]+)"', D.sans_code(sec))
        titre = re.search(r"<h2[^>]*>(.*?)</h2>", sec, re.S)
        print("1. « %s » — %d o, %d lien(s)"
              % (re.sub(r"<[^>]+>", "", titre.group(1)).strip()[:58] if titre else "?",
                 len(sec), len(re.findall(r'href="', D.sans_code(sec)))))
        c = c[:i] + c[j:]
    else:
        print("1. section « Cas d'usage metier » introuvable")

    # ── 2. le bloc d'aout en bas de page ──────────────────────────────────
    i, j = bloc(c, '<section class="hh-maj-aout-fonctions"')
    if i is not None:
        sec = c[i:j]
        partis += re.findall(r'href="([^"]+)"', D.sans_code(sec))
        titre = re.search(r"<h2[^>]*>(.*?)</h2>", sec, re.S)
        print("2. « %s » — %d o, %d lien(s)"
              % (re.sub(r"<[^>]+>", "", titre.group(1)).strip()[:58] if titre else "?",
                 len(sec), len(re.findall(r'href="', D.sans_code(sec)))))
        c = c[:i] + c[j:]
    else:
        print("2. bloc hh-maj-aout-fonctions introuvable")

    # ── 3. le fond du Hero ────────────────────────────────────────────────
    if CASSEE in c:
        h = c.find('<section class="hero-section"')
        fin = c.find(">", h)
        tag = c[h:fin]
        if tag.count("url('") != 1:
            raise SystemExit("ARRET — plusieurs images dans le Hero")
        neuf_tag = re.sub(r"url\('[^']+'", "url('%s'" % PHOTO, tag)
        c = c[:h] + neuf_tag + c[fin:]
        print("3. fond du Hero : %s (404) -> %s" % (CASSEE, PHOTO.rsplit("/", 1)[-1]))
    else:
        print("3. le Hero ne porte pas l'image cassee")

    # ── controles ─────────────────────────────────────────────────────────
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge")
    if c.count("<section class=") != depart.count("<section class=") - 2:
        raise SystemExit("ARRET — %d sections au lieu de %d"
                         % (c.count("<section class="),
                            depart.count("<section class=") - 2))
    restants = D.liens(c)
    perdus = [x for x in dict.fromkeys(partis) if x not in restants]
    gardes = [x for x in dict.fromkeys(partis) if x in restants]
    reste = D.liens(depart)
    for x in partis:
        if x in reste:
            reste.remove(x)
    if reste != restants:
        raise SystemExit("ARRET — lien(s) perdu(s) hors des deux sections")

    print("\n   %d -> %d ko · %d sections" % (len(depart) // 1024, len(c) // 1024,
                                              c.count("<section class=")))
    print("   liens conserves ailleurs : %s" % (", ".join(gardes) or "aucun"))
    print("   LIENS PERDUS             : %s" % (", ".join(perdus) or "aucun"))

    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")
        return
    open(os.path.join(SAUV, "avant-%d.html" % PAGE), "w", encoding="utf-8").write(depart)
    w.update_content("pages", PAGE, c, live=True)
    print("\n   pose")
    import time
    time.sleep(6)
    h = R.lire_page(URL)
    corps = D.sans_code(h)
    print("   en ligne : %d ko · %d sections · « Cas d'usage » %s · bloc d'aout %s · Hero %s"
          % (len(h) // 1024, h.count("<section class="),
             "absent" if "Cas d'usage m" not in corps else "PRESENT",
             "absent" if "hh-maj-aout-fonctions" not in h else "PRESENT",
             "repare" if CASSEE not in h else "TOUJOURS CASSE"))


if __name__ == "__main__":
    main()
