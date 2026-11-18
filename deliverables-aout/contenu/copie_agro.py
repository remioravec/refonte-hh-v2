#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/agroalimentaire/ a l'identique, en artefact.

Aucune refonte, aucune reparation, aucun ajout : le code source de la page
1726 est repris tel quel. Les seules transformations sont celles qu'impose la
politique de securite des artefacts, qui bloque toute ressource distante :

  1. les images passent en data URI — sinon elles s'affichent en cadres vides ;
  2. les 34 icones Font Awesome, servies par un CDN, deviennent des SVG en
     ligne — sinon ce sont 34 carres vides ;
  3. les blocs animes a l'apparition sont poses a l'arret — le JS du theme
     n'est pas la, et sans lui ils resteraient invisibles.

Rien d'autre n'est touche. Pas une balise, pas une regle CSS, pas un mot.

MAQUETTE, PAS MISE EN LIGNE. La page 1726 est protegee par la regle 0 :
ce script lit la page, il ne l'ecrit jamais.

Usage :  python3 copie_agro.py
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w      # noqa: E402
import maquette_agro as M  # noqa: E402  (on y reprend convertir() et SVG_FA)

PAGE = 1726
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "copie-agro.html")
SITE = "https://www.helloharel.com"

POLICE = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
          'family=Inter:wght@300;400;500;600;700;800;900&display=swap">')

# Le site anime ses blocs a l'apparition, et c'est son JS qui leve
# l'opacite. Hors du site, ce JS n'existe pas : sans cette feuille, une
# bonne moitie de la page reste invisible. On ne change pas le CSS de la
# page, on ajoute un etat de repos par-dessus.
REPOS = """<style id="hh-copie-repos">
#hh-page .scroll-reveal,#hh-page .metier-slide{opacity:1 !important;transform:none !important}

body{margin:0;background:#fff}
</style>"""


def controler(html, source):
    pb = []
    if len(html) > 15_500_000:
        pb.append("depasse la limite de 16 Mo d'un artefact")
    for m in re.finditer(r'<(img|source)[^>]+src="((?:https?:)?/[^"]*)"', html):
        pb.append("image non integree : " + m.group(2)[:70])
    for m in re.finditer(r'<link[^>]+rel="stylesheet"[^>]+href="(https?://[^"]+)"', html):
        if "fonts.googleapis.com" not in m.group(1):
            pb.append("feuille de style distante bloquee : " + m.group(1)[:70])
    if re.search(r'<i class="fa[sbr]? ', html):
        pb.append("il reste une icone Font Awesome sans police")
    if re.search(r"<iframe", html):
        pb.append("iframe : bloquee dans un artefact")

    # Le controle qui compte : ce qui portait du contenu doit etre intact.
    corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
    for quoi, motif in [("sections", r"<section[\s>]"), ("H1", r"<h1[\s>]"),
                        ("H2", r"<h2[\s>]"), ("H3", r"<h3[\s>]"),
                        ("liens", r'href="'), ("boutons", r"<button[\s>]")]:
        a = len(re.findall(motif, corps(source)))
        b = len(re.findall(motif, corps(html)))
        print("   %-10s source %3d   copie %3d   %s" % (quoi, a, b, "=" if a == b else "ECART"))
        if a != b:
            pb.append("%s : %d dans la source, %d dans la copie" % (quoi, a, b))

    # Le texte visible doit etre le meme, mot pour mot. On compare les corps :
    # le <title> ajoute dans l'en-tete est celui de la page, exige par le
    # format artefact, et n'apparait pas dans le corps.
    def texte(t):
        t = t[t.find("<body>") + 6:] if "<body>" in t else t
        t = corps(t)
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()
    ta, tb = texte(source), texte(html)
    print("   %-10s source %3d   copie %3d   %s"
          % ("mots", len(ta.split()), len(tb.split()), "=" if ta == tb else "ECART"))
    if ta != tb:
        pb.append("le texte visible a change")
    return pb


def main():
    c = w.get_raw("pages", PAGE)["content"]["raw"]
    source = c
    print("page %d lue : %d octets" % (PAGE, len(c)))

    # 1 — les images, integrees
    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    urls |= set(re.findall(r"url\(&#039;(https?://[^&]+\.(?:png|jpe?g|webp|svg|gif))&#039;\)", c))
    ok = ko = 0
    for u in sorted(urls):
        d = M.convertir(u)
        if d:
            c = c.replace(u, d)
            ok += 1
        else:
            ko += 1
            print("   ! image non recuperee :", u[:90])
    # Certaines images sont referencees en chemin relatif : elles resolvent sur
    # le site, jamais dans un artefact. On les prefixe avant de les integrer.
    rel = set(re.findall(r'(?:src|data-src)="(/wp-content/[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    rel |= set(re.findall(r"url\('?(/wp-content/[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    for u in sorted(rel):
        d = M.convertir(SITE + u)
        if d:
            c = c.replace('"%s"' % u, '"%s"' % d)
            ok += 1
        else:
            ko += 1
            print("   ! image relative non recuperee :", u[:90])
    print("images integrees : %d (%d en echec)" % (ok, ko))

    # 2 — Font Awesome : le CDN est refuse, les icones deviennent des SVG
    n = 0
    for cls, svg in M.SVG_FA.items():
        for balise in ('<i class="%s"></i>' % cls, '<i class="%s"/>' % cls):
            n += c.count(balise)
            c = c.replace(balise, svg)
    c = re.sub(r'<link[^>]+cdnjs\.cloudflare\.com[^>]*>', "", c)
    print("icones Font Awesome remplacees par des SVG : %d" % n)

    html = ('<!doctype html><html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>ERP Agroalimentaire • Spécialiste PME • Depuis 2014 ☁️</title>'
            + POLICE + REPOS + '</head><body>' + c + '</body></html>')

    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\necrit : %s  (%d ko)\n" % (SORTIE, len(html) // 1024))

    pb = controler(html, source)
    print()
    for x in pb:
        print("   !", x)
    print("controles : %s" % ("tout est vert" if not pb else "%d ecart(s)" % len(pb)))


if __name__ == "__main__":
    main()
