#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les trois photos de heros choisies le 22/09, posees sur leurs pages.

Rémi a entoure trois vignettes dans l'artefact des candidats :
  · Pexels 4820817  → torrefacteur
  · Pexels 1267348  → brasseur
  · Pexels 29188957 → chocolatier

Aucune des trois pages n'est protegee par la regle 0 (1726, 2818, 2839,
5477, 11162) : l'ecriture est donc autorisee.

Le hero de ces pages porte son image dans un seul url('...') de l'attribut
style de la section. On remplace cette URL, et rien d'autre : le degrade,
le cadrage et le reste du markup ne bougent pas. Le contenu d'avant est
sauvegarde sur disque avant chaque ecriture.

Usage :  python3 heros_trois.py          (blanc : montre sans ecrire)
         python3 heros_trois.py --poser  (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w        # noqa: E402
import heros_metiers as H    # noqa: E402  (preparer, televerser)

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "heros-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

# (page, url, id Pexels, nom de fichier, texte alternatif)
CHOIX = [
    (10935, "/agroalimentaire/torrefacteur/", 4820817,
     "erp-torrefacteur-refroidissement-grains-cafe",
     "Torréfacteur plongeant la main dans les grains de café au refroidissement"),
    (10896, "/agroalimentaire/brasseur/", 1267348,
     "erp-brasseur-cuve-inox-artisan",
     "Brasseur souriant devant les cuves inox de sa brasserie artisanale"),
    (10894, "/agroalimentaire/chocolatier/", 29188957,
     "erp-chocolatier-enrobage-truffes",
     "Chocolatier disposant des truffes enrobées au comptoir de son atelier"),
]


def hero_url(contenu):
    """L'URL de fond du hero. On exige une seule occurrence : deux
    voudraient dire que la section n'est pas celle qu'on croit."""
    i = contenu.find('<section class="hero-section"')
    if i < 0:
        return None, None
    j = contenu.find(">", i)
    balise = contenu[i:j + 1]
    urls = re.findall(r"url\('([^']+)'\)", balise)
    if len(urls) != 1:
        return None, balise
    return urls[0], balise


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    os.makedirs(os.path.join(S, "px"), exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for page, url, px, nom, alt in CHOIX:
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        p = w.get_raw("pages", page)
        c = p["content"]["raw"]
        avant, balise = hero_url(c)
        if not avant:
            raise SystemExit("ARRET — hero introuvable ou ambigu sur %s" % url)

        print("%s  (page %d)" % (url, page))
        print("   avant : %s" % avant.split("/")[-1])

        chemin, ko, q = H.preparer(px, nom)
        print("   photo : Pexels %d → %s.webp  %d ko (qualite %d)" % (px, nom, ko, q))

        if not poser:
            print("   (blanc — rien n'est ecrit)\n")
            continue

        open(os.path.join(SAUV, "avant-%d.html" % page), "w", encoding="utf-8").write(c)
        m = H.televerser(chemin, nom, alt)
        apres = m["source_url"]
        neuf = c.replace(avant, apres)
        if neuf == c or neuf.count(apres) != 1:
            raise SystemExit("ARRET — le remplacement n'a pas eu lieu une seule fois")
        # Le reste du contenu doit etre rigoureusement identique : on ne
        # change qu'une URL, pas un octet de plus.
        if len(neuf) - len(c) != len(apres) - len(avant):
            raise SystemExit("ARRET — l'ecart de taille ne correspond pas a l'URL seule")
        w.update_content("pages", page, neuf, live=True)
        print("   apres : %s" % apres.split("/")[-1])
        print("   media #%d, alt pose\n" % m["id"])

    if poser:
        print("--- verification en ligne ---")
        import time
        time.sleep(4)
        import urllib.request
        for page, url, px, nom, alt in CHOIX:
            req = urllib.request.Request("https://www.helloharel.com" + url,
                                         headers={"User-Agent": "Mozilla/5.0"})
            h = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
            ok = nom in h
            i = h.find('<section class="hero-section"')
            u = re.findall(r"url\('([^']+)'\)", h[i:h.find(">", i) + 1]) if i > 0 else []
            print("   %-42s %s  %s" % (url, "OK " if ok else "KO ",
                                       u[0].split("/")[-1] if u else "?"))


if __name__ == "__main__":
    main()
