#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maquette du menu complete, posee sur la home telle qu'elle est en ligne.

On ne touche NI la feuille de style NI le JavaScript du site : seuls deux
blocs de markup sont remplaces, la navigation de bureau et le contenu du menu
mobile. Tout le reste de l'entete — logo, boutons d'action, hamburger — reste
en place, avec ses classes.

MAQUETTE. Rien n'est ecrit sur WordPress.

Usage :  python3 maquette_menu.py [id_de_page]
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402
import menu_home as N                       # noqa: E402
from maquette_agro import (convertir, POLICE, REPOS, SVG_FA, nettoyer, reparer,
                           controler, remplacer_video)  # noqa: E402

PAGE = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "maquette-menu.html")


def poser(c):
    """Remplace la navigation de bureau et le contenu du menu mobile."""
    faits = []

    # --- navigation de bureau
    i = c.find('<nav class="desktop-nav">')
    if i < 0:
        raise SystemExit("ARRET — <nav class=\"desktop-nav\"> introuvable")
    j = c.find("</nav>", i)
    if j < 0:
        raise SystemExit("ARRET — fin de la navigation introuvable")
    if "<nav" in c[i + 25:j]:
        raise SystemExit("ARRET — navigation imbriquee, borne incertaine")
    c = c[:i] + N.desktop() + c[j + 6:]
    faits.append("navigation de bureau remplacee")

    # --- contenu du menu mobile : on garde le conteneur .mobile-menu
    i = c.find('<div class="mobile-menu-inner">')
    if i < 0:
        raise SystemExit("ARRET — .mobile-menu-inner introuvable")
    j = c.find("</div>\n    </div>", i)
    if j < 0:
        j = c.find('<section', i)
        if j < 0:
            raise SystemExit("ARRET — fin du menu mobile introuvable")
        j = c.rfind("</div>", i, j)
    c = c[:i] + N.mobile() + c[j + len("</div>\n    </div>"):] if c[j:j + 17] == "</div>\n    </div>" \
        else c[:i] + N.mobile() + c[j:]
    faits.append("menu mobile remplace")
    return c, faits


def main():
    c = w.get_raw("pages", PAGE)["content"]["raw"]
    avant = len(c)
    print("page %d lue : %d octets" % (PAGE, avant))
    c, faits = poser(c)
    for f in faits:
        print("  ·", f)

    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    ok = 0
    for u in sorted(urls):
        d = convertir(u)
        if d:
            c = c.replace(u, d)
            ok += 1
    for cls, svg in SVG_FA.items():
        c = c.replace('<i class="%s"></i>' % cls, svg)
    c = re.sub(r"<link[^>]+cdnjs\.cloudflare\.com[^>]*>", "", c)
    c, _v = remplacer_video(c)
    c, _ = reparer(c)
    c = nettoyer(c)
    print("  images integrees : %d" % ok)

    html = "<title>Menu Hello Harel — maquette</title>\n" + POLICE + "\n" + REPOS + "\n" + c
    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\necrit : %s (%d ko)" % (SORTIE, len(html) // 1024))

    pb = controler(html) + N.controler()
    for quoi, attendu in (('<nav class="desktop-nav">', 1),
                          ('class="mobile-menu-inner"', 1),
                          ('class="mega-industries-inner"', 1),
                          ("hamburgerBtn", 1)):
        if html.count(quoi) < attendu:
            pb.append("%s : %d fois, attendu %d" % (quoi, html.count(quoi), attendu))
    for mort in ("/negoce/", "/medical/"):
        i = html.find('<nav class="desktop-nav">')
        j = html.find("</nav>", i)
        if mort in html[i:j]:
            pb.append("%s encore dans la navigation" % mort)
    n = len(set(re.findall(r'href="(/agroalimentaire/[^"]*)"', html[html.find('<nav class="desktop-nav">'):html.find("</nav>", html.find('<nav class="desktop-nav">'))])))
    print("  metiers agroalimentaires dans la navigation : %d" % n)
    if n != 16:
        pb.append("%d metiers au lieu de 16" % n)
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
