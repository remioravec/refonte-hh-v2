#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Des avatars dessines pour animer les avis, a la place des initiales.

Un parti pris, assume : le visage est le MEME ton pour tous. Ce qui varie,
c'est la coiffure, la couleur des cheveux, le haut et le fond. Ces avis
portent des noms de vraies personnes ; leur attribuer un teint reviendrait
a leur prêter une apparence qu'on ne connait pas. Varier la coiffure anime
la rangee sans rien affirmer de personne.

Le tirage est deterministe : le meme nom donne toujours le meme avatar,
d'une page a l'autre et d'un deploiement au suivant.
"""

import hashlib
import urllib.parse

PEAU = "#F0C9A8"       # un seul ton, pour tout le monde
TRAIT = "#0f172a"

FONDS = ["#E0F2FE", "#DCFCE7", "#FEF3C7", "#EDE9FE", "#FFE4E6", "#CFFAFE"]
HAUTS = ["#0369A1", "#15803D", "#B45309", "#6D28D9", "#BE123C", "#0F766E"]
CHEVEUX = ["#2B2118", "#7C4A21", "#3F3F46", "#8B5E34", "#1F2937", "#A16207"]

# Six silhouettes de coiffure, dessinees par-dessus le crane.
COIFFES = [
    # courte
    "<path d='M30 44c0-14 9-22 20-22s20 8 20 22c0 0-4-9-20-9s-20 9-20 9z' fill='{c}'/>",
    # bouclee
    ("<g fill='{c}'><circle cx='36' cy='32' r='9'/><circle cx='50' cy='27' r='10'/>"
     "<circle cx='64' cy='32' r='9'/><circle cx='31' cy='42' r='7'/>"
     "<circle cx='69' cy='42' r='7'/></g>"),
    # mi-longue : deux meches qui tombent le long du visage, jamais dessus
    ("<g fill='{c}'><path d='M29 44c0-14 9-22 21-22s21 8 21 22c0 0-5-8-21-8s-21 8-21 8z'/>"
     "<path d='M29 42h4v22c0 3-4 3-4 0z'/><path d='M67 42h4v22c0 3-4 3-4 0z'/></g>"),
    # longue
    ("<g fill='{c}'><path d='M28 45c0-15 10-23 22-23s22 8 22 23c0 0-5-9-22-9s-22 9-22 9z'/>"
     "<path d='M28 43h5v30c0 3-5 3-5 0z'/><path d='M67 43h5v30c0 3-5 3-5 0z'/></g>"),
    # degarnie
    "<path d='M32 41c2-11 9-17 18-17s16 6 18 17c0 0-5-6-18-6s-18 6-18 6z' fill='{c}'/>",
    # avec frange
    ("<path d='M29 45c0-15 9-23 21-23s21 8 21 23c0 0-3-6-3-11 0 0-7 6-18 6s-18-6-18-6"
     "c0 5-3 11-3 11z' fill='{c}'/>"),
]


def _tirage(nom):
    h = hashlib.md5(nom.strip().lower().encode("utf-8")).digest()
    return [b for b in h]


def avatar(nom, taille=96):
    """Rend une image SVG en data URI, prête a poser dans un <img src>."""
    t = _tirage(nom)
    fond = FONDS[t[0] % len(FONDS)]
    haut = HAUTS[t[1] % len(HAUTS)]
    chev = CHEVEUX[t[2] % len(CHEVEUX)]
    coiffe = COIFFES[t[3] % len(COIFFES)].format(c=chev)
    sourire = 6 + t[4] % 4          # largeur du sourire

    # L'ordre compte : la coiffure se pose sur le crane AVANT les yeux, sinon
    # une meche longue vient couvrir un oeil. Et tout est decoupe au cercle,
    # sinon les epaules debordent du medaillon.
    ident = "a%s" % hashlib.md5(nom.encode("utf-8")).hexdigest()[:6]
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' "
        "viewBox='0 0 100 100'>"
        "<defs><clipPath id='%s'><circle cx='50' cy='50' r='50'/></clipPath></defs>"
        "<g clip-path='url(#%s)'>"
        "<rect width='100' height='100' fill='%s'/>"
        # epaules
        "<path d='M14 100c0-18 16-28 36-28s36 10 36 28z' fill='%s'/>"
        # col
        "<path d='M42 74l8 9 8-9' fill='none' stroke='#ffffff' stroke-width='2.5' "
        "stroke-opacity='.4' stroke-linecap='round'/>"
        # cou
        "<rect x='44' y='58' width='12' height='16' rx='6' fill='%s'/>"
        # oreilles, puis visage
        "<circle cx='30' cy='47' r='4.5' fill='%s'/><circle cx='70' cy='47' r='4.5' fill='%s'/>"
        "<ellipse cx='50' cy='46' rx='20' ry='22' fill='%s'/>"
        # la coiffure, sous les yeux
        "%s"
        # yeux
        "<circle cx='43' cy='46' r='2.5' fill='%s'/><circle cx='57' cy='46' r='2.5' fill='%s'/>"
        # sourire
        "<path d='M%d 55q%d 6 %d 0' fill='none' stroke='%s' stroke-width='2.4' "
        "stroke-linecap='round'/>"
        "</g></svg>"
    ) % (taille, taille, ident, ident, fond, haut, PEAU, PEAU, PEAU, PEAU,
         coiffe, TRAIT, TRAIT,
         50 - sourire, sourire, sourire * 2, TRAIT)

    # Dans une url() de feuille de style, seuls quelques caracteres genent
    # vraiment. Tout encoder gonfle l'image d'un bon tiers pour rien.
    return "data:image/svg+xml," + urllib.parse.quote(
        svg, safe="=:/,;'()*-_.~ +![]{}|^`@$&?")


def cle(nom):
    """Un identifiant court et stable, pour nommer la classe CSS."""
    return "t" + hashlib.md5(nom.strip().lower().encode("utf-8")).hexdigest()[:8]


def balise(nom, classe="", taille=96):
    """Le medaillon, sans l'image : elle vient de la feuille.

    Le meme avatar revient plusieurs fois dans une page — la piste du
    carrousel est doublee, et un avis peut servir a deux endroits. Poser
    l'image dans la feuille plutot que dans la balise la fait peser une
    seule fois au lieu d'une par occurrence.
    """
    cl = ("hh-tete " + cle(nom) + ((" " + classe) if classe else "")).strip()
    return '<i class="%s" aria-hidden="true"></i>' % cl


def feuille(noms, ident="hh-avatars"):
    """La feuille qui porte les images, une regle par personne distincte."""
    vus, regles = set(), []
    for n in noms:
        k = cle(n)
        if k in vus:
            continue
        vus.add(k)
        regles.append("#hh-page .%s,.%s{background-image:url(\"%s\") !important}"
                      % (k, k, avatar(n, 96)))
    return ('<style id="%s">\n'
            "#hh-page .hh-tete,.hh-tete{display:block !important;flex:none;"
            "border-radius:50%% !important;background:#E0F2FE no-repeat center/cover "
            "!important;font-style:normal !important;margin:0 !important}\n"
            "%s\n</style>" % (ident, "\n".join(regles)))


if __name__ == "__main__":
    noms = ["Julien B.", "Marie C.", "Philippe D.", "Sophie L.",
            "Thomas R.", "Claire M.", "Antoine V.", "Nadia K."]
    cel = "".join(
        "<figure style='margin:0;text-align:center'>"
        "<span style='display:block;width:104px;height:104px;margin:0 auto'>%s</span>"
        "<figcaption style='font:600 13px system-ui;color:#475569;margin-top:8px'>%s"
        "</figcaption></figure>" % (balise(n), n) for n in noms)
    open("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avatars.html",
         "w", encoding="utf-8").write(
        "<!doctype html><meta charset=utf-8>" + feuille(noms).replace("#hh-page ", "") +
        "<style>.hh-tete{width:104px;height:104px}</style>"
        "<body style='background:#fff;padding:28px'>"
        "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:26px;"
        "max-width:620px'>%s</div></body>" % cel)
    print("%d avatars · feuille de %d octets · %d octets par balise"
          % (len(noms), len(feuille(noms)), len(balise(noms[0]))))
