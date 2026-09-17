#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maquette du nouveau menu, posee sur une vraie page du site.

On ne montre pas le menu sur fond blanc : on le pose sur /negoce/, telle
qu'elle est en ligne, pour qu'il se juge en situation — au-dessus du hero,
puis en entete pleine au defilement.

L'ancien entete et l'ancien menu mobile sont retires, et le script du theme
qui les pilotait est neutralise : sans cela il appellerait addEventListener
sur des elements disparus et couperait tout le JavaScript de la page.

MAQUETTE. Rien n'est ecrit sur WordPress.

Usage :  python3 maquette_menu.py
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402
import mega_menu as M                       # noqa: E402
from maquette_agro import (convertir, POLICE, REPOS, SVG_FA, nettoyer, reparer,
                           controler, remplacer_video)  # noqa: E402

PAGE = 5957
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "maquette-menu.html")

LOGO = ('<img src="https://www.helloharel.com/wp-content/uploads/2019/05/'
        'hello-harel-logo-white.svg" alt="Hello Harel, ERP agroalimentaire" width="150" '
        'height="38">')


def couper(c, ouvrant, fermant, quoi):
    i = c.find(ouvrant)
    if i < 0:
        raise SystemExit("ARRET — %s introuvable" % quoi)
    j = c.find(fermant, i)
    if j < 0:
        raise SystemExit("ARRET — fin de %s introuvable" % quoi)
    return c[:i], c[j + len(fermant):]


def main():
    c = w.get_raw("pages", PAGE)["content"]["raw"]
    print("page %d lue : %d octets" % (PAGE, len(c)))

    # 1. l'ancien entete
    avant, apres = couper(c, "<header", "</header>", "l'entete")
    c = avant + M.desktop(LOGO) + apres
    print("  entete remplace")

    # 2. l'ancien menu mobile — il se termine juste avant la section suivante
    i = c.find('<div class="mobile-menu')
    if i < 0:
        raise SystemExit("ARRET — menu mobile introuvable")
    j = c.find("<section", i)
    if j < 0:
        raise SystemExit("ARRET — fin du menu mobile introuvable")
    c = c[:i] + M.mobile() + c[j:]
    print("  menu mobile remplace")

    # 3. le script du theme pilotait hamburgerBtn et mobileMenu : sans garde,
    #    il leve une exception sur des elements qui n'existent plus et coupe
    #    tout le JavaScript de la page.
    n = 0
    for v in ("hamburgerBtn", "mobileMenu"):
        for m in list(re.finditer(r"document\.getElementById\('%s'\)" % v, c)):
            n += 1
    c = re.sub(r"document\.getElementById\('(hamburgerBtn|mobileMenu)'\)",
               "(document.getElementById('\\1')||{addEventListener:function(){},"
               "classList:{toggle:function(){},remove:function(){},add:function(){}},"
               "setAttribute:function(){},style:{}})", c)
    print("  ancien script du menu neutralise : %d appels gardes" % n)

    c += M.CSS + M.JS

    # 4. mise en artefact
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

    pb = controler(html)
    pb += M.controler()
    for quoi, attendu in (('id="hhm-header"', 1), ('id="hhm-mobile"', 1),
                          ('id="hhm-metiers"', 1), ('id="hhm-fonctions"', 1),
                          ("hh-mega-menu-js", 1)):
        if html.count(quoi) != attendu:
            pb.append("%s : %d fois, attendu %d" % (quoi, html.count(quoi), attendu))
    for vieux in ('class="desktop-nav"', 'class="mobile-menu"',
                  'class="dropdown-panel', 'class="nav-dropdown"'):
        if vieux in html:
            pb.append("reste de l'ancien menu dans le markup : %s" % vieux)
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
