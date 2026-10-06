#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variante A du test negoce — page 11493.

Sa mise en forme editoriale (gouttiere a numeros, serif, blocs § 01 a § 06) est
reprise telle quelle : c'est elle qui est testee contre l'UX d'accueil SaaS de
la variante B. Seul le fond change, et il devient celui de B, mot pour mot, tire
de negoce_b_contenu — c'est ce qui garantit qu'une seule variable distingue les
deux variantes.

Le fond precedent portait l'angle import-export. Le releve du 29/08/2026 sur les
trois pages qui occupent le champ « negoce alimentaire » montre qu'aucune ne
parle de conteneurs, d'incoterms ni de frais d'approche : ce champ est celui du
grossiste.

Usage :  python3 page_negoce_variante_a.py           (essai a blanc)
         python3 page_negoce_variante_a.py --live    (ecriture)
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)

import wp_common as w
import negoce_b_contenu as C
from negoce_a_css import CSS

PAGE = 11493
TITRE = "[TEST A] ERP Négoce Alimentaire • Poids Réel, DLC et Marge"
LIVE = "--live" in sys.argv

IMG = {
    "hero": ("https://www.helloharel.com/wp-content/uploads/2026/08/"
             "ERP-logiciel-pour-les-grossistes-en-lait.webp",
             "Entrepôt de négoce alimentaire, palettes et préparation de commandes"),
    "t1": ("https://www.helloharel.com/wp-content/uploads/2026/08/"
           "Logiciel-de-grossistes-alimentaire-1.webp",
           "Réception de marchandise sur le quai d'une plateforme de distribution alimentaire"),
    "t2": ("https://www.helloharel.com/wp-content/uploads/2026/08/"
           "Logiciel-de-grossistes-alimentaire-2.webp",
           "Préparation de commandes et pesée en entrepôt"),
    "t3": ("https://www.helloharel.com/wp-content/uploads/2026/08/"
           "Logiciel-de-grossistes-alimentaire-4.webp",
           "Chargement d'une tournée de livraison"),
    "end": ("https://www.helloharel.com/wp-content/uploads/2026/08/"
            "Logiciel-pour-grossiste-industriel.webp",
            "Responsable d'exploitation en plateforme de distribution alimentaire"),
}

# La variante A n'a pas de classe dediee au bandeau : on reprend le style exact
# de la page d'origine, une note dans la gouttiere.
BANDEAU = ('<div class="w" style="padding-top:26px"><p class="note">VARIANTE A — test A/B, '
           'brouillon non indexé. Même contenu que la variante B, mise en forme différente. '
           'Ne pas publier sans avoir posé le noindex.</p></div>')


def img(cle, eager=False):
    u, a = IMG[cle]
    return ('<img src="' + u + '" alt="' + a + '" loading="'
            + ("eager" if eager else "lazy") + '" decoding="async">')


def blk(no, vert, kick, h2, corps, intro=None):
    return ('<div class="blk"><div class="gut"><span class="no">§ ' + no + '</span>'
            '<span class="vert">' + vert + '</span></div><div class="bd">'
            '<p class="kick">' + kick + '</p><h2>' + h2 + '</h2>'
            + ('<p class="intro">' + intro + '</p>' if intro else '')
            + corps + '</div></div>')


def hero():
    facts = "".join('<div><div class="n">' + n + '</div><div class="l">' + l + '</div></div>'
                    for n, l in C.STATS)
    return (
        '<header class="hero"><div class="w"><div class="row">'
        '<div class="lab">Négoce<br>Alimentaire</div>'
        '<div><h1>Vous achetez au kilo. Vous facturez à l\'unité. '
        '<em>C\'est là que la marge se perd.</em></h1>'
        '<p class="sub">Hello Harel facture au poids réellement pesé, applique la DLC du lot et '
        'l\'échéance légale du produit — là où un ERP généraliste facture au poids commandé et à '
        'trente jours pour tout le monde.</p>'
        '<a class="cta" href="/contact/">Voir sur mes lignes de commande</a></div>'
        '</div></div>'
        '<div class="band">' + img("hero", eager=True) + '</div>'
        '<div class="w"><div class="facts">' + facts + '</div></div></header>'
    )


def bloc_calcul():
    lignes = "".join('<tr><td>' + a + '</td><td>' + b + '</td></tr>' for a, b in C.CALC_LIGNES)
    warn = "".join('<p>' + p + '</p>' for p in C.CALC_WARN)
    corps = (
        '<div class="calc"><div><table class="led">'
        '<caption>' + C.CALC_CARTE + '</caption><tbody>' + lignes +
        '<tr class="sum"><td>' + C.CALC_TOTAL[0] + '</td><td>' + C.CALC_TOTAL[1] + '</td></tr>'
        '<tr class="coef"><td>' + C.CALC_COEF[0] + '</td><td>' + C.CALC_COEF[1] + '</td></tr>'
        '</tbody></table>'
        '<p class="cap">' + C.CALC_NOTE + '</p></div>'
        '<div><h3>Ce que ça change concrètement</h3>' + warn +
        '<p><a href="/agroalimentaire/negoce-alimentaire/">Le calculateur de marge au poids '
        'variable</a></p></div></div>')
    return blk("01", "Le calcul", "Ce que personne ne vous montre", C.CALC_TITRE, corps,
               C.CALC_INTRO)


def bloc_huit():
    items = "".join(
        '<div class="it"><div class="k">' + ("%02d" % (i + 1)) + '</div>'
        '<div><h3>' + t + '</h3><p>' + p + '</p></div></div>'
        for i, (t, p) in enumerate(C.HUIT))
    return blk("02", "Fonctions", "Huit terrains de vérité",
               "Là où les outils généralistes <em>s\'arrêtent</em>.",
               '<div class="fx">' + items + '</div>',
               "Ce ne sont pas des options : ce sont les points sur lesquels un ERP généraliste "
               "facture un développement spécifique, et sur lesquels un tableur ne se prononce "
               "pas.")


def bloc_terrain():
    figs = "".join(
        '<figure>' + img(c) + '<figcaption><span class="t">' + t + '</span>' + d
        + '</figcaption></figure>'
        for c, (t, d) in zip(("t1", "t2", "t3"), C.TERRAIN))
    return blk("03", "Terrain", "Réception, préparation, livraison", C.TERRAIN_TITRE,
               '<div class="trip">' + figs + '</div>', C.TERRAIN_INTRO)


def bloc_comparatif():
    th = "".join('<th>' + c + '</th>' for c in C.CMP_COLS)
    tr = "".join('<tr>' + "".join('<td>' + c + '</td>' for c in l) + '</tr>'
                 for l in C.CMP_LIGNES)
    corps = ('<div class="cmpw"><table class="cmp"><thead><tr>' + th + '</tr></thead>'
             '<tbody>' + tr + '</tbody></table></div>')
    return blk("04", "Se situer", "Tableur, ERP généraliste, ERP métier",
               "Trois façons de se tromper de <em>marge</em>.", corps, C.CMP_INTRO)


def bloc_modules():
    liens = "".join(
        '<a href="' + href + '"><span class="k">' + no + '</span>'
        '<span class="t">' + t + '<span class="d">' + d + '</span></span>'
        '<span class="ar">&rarr;</span></a>'
        for no, _cle, href, t, d in C.MODULES)
    return blk("05", "Modules", "Par où entrer",
               "Chaque brique du négoce a <em>sa page</em>.",
               '<div class="idx">' + liens + '</div>')


def bloc_faq():
    qa = "".join('<details><summary>' + q + '</summary>' + r + '</details>'
                 for q, _m, r in C.FAQ)
    return blk("06", "Questions", "Les réponses",
               "Ce qu'on nous demande <em>avant</em> de choisir.",
               '<div class="qa">' + qa + '</div>')


def fin():
    return (
        '<section class="end"><div class="w"><div class="in"><div>'
        '<p class="kick" style="color:rgba(255,255,255,.5)">Démonstration</p>'
        '<h2>' + C.CTA_TITRE + '</h2><p>' + C.CTA_INTRO + '</p>'
        '<a class="cta" href="/contact/">Réserver la démonstration</a></div>'
        '<div>' + img("end") + '</div></div></div></section>'
    )


def construire():
    corps = (BANDEAU + hero() + '<div class="w">' + bloc_calcul() + bloc_huit() + bloc_terrain()
             + bloc_comparatif() + bloc_modules() + bloc_faq() + '</div>' + fin())
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer",
                            "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()}}
        for q, _m, r in C.FAQ]}
    return (CSS + '<div id="hva">' + corps + '</div>'
            '<script type="application/ld+json">'
            + json.dumps(ld, ensure_ascii=False) + '</script>')


def controles(html):
    pb = []
    for t in ("div", "section", "table", "details", "figure", "a"):
        o = len(re.findall(r"<" + t + r"[ >]", html))
        f = len(re.findall(r"</" + t + r">", html))
        if o != f:
            pb.append("balises <%s> desequilibrees : %d / %d" % (t, o, f))

    for u in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if not u.startswith("https://www.helloharel.com/"):
            pb.append("image hors mediatheque : " + u[:70])
    if re.search(r'<img(?![^>]*\balt=")', html):
        pb.append("une image sans alternative textuelle")

    PROT = ("/agroalimentaire/", "/agroalimentaire/traiteur/", "/agroalimentaire/charcutier/",
            "/agroalimentaire/plats-cuisines-industriels/", "/migration-as400/")
    for h in re.findall(r'<a[^>]+href="([^"]+)"', html):
        if h in PROT:
            pb.append("Regle 0 — lien vers une page protegee : " + h)

    texte = re.sub(r"<[^>]+>", " ", html)
    for mot in ("conteneur", "incoterm", "frais d'approche", "transitaire", "douane",
                "écart de change", "maraîch", "calibre"):
        n = len(re.findall(mot, texte, re.I))
        if n:
            pb.append("vocabulaire hors persona : %r x%d" % (mot, n))

    # meme fond que la variante B : les reperes du fond commun doivent y etre
    for att in (C.CALC_TOTAL[1], C.CALC_COEF[1], "17,51 €", "0,51 €", "7 344 €"):
        if att not in html:
            pb.append("valeur du fond commun absente : " + att)
    for q, _m, _r in C.FAQ:
        if q not in html:
            pb.append("question absente : " + q[:44])
    for t, _p in C.HUIT:
        if t not in html:
            pb.append("terrain absent : " + t[:44])

    # aucun lien ni aucune image inventes
    import subprocess
    for u in sorted(set(re.findall(r'<img[^>]+src="([^"]+)"', html))
                    | {"https://www.helloharel.com" + h
                       for h in re.findall(r'href="(/[^"#]+)"', html)}):
        code = subprocess.run(["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}", u],
                              capture_output=True, text=True, timeout=45).stdout.strip()
        if code != "200":
            pb.append("ressource en %s : %s" % (code, u.replace("https://www.helloharel.com", "")))
    return pb


def main():
    html = construire()
    pb = controles(html)
    print("  taille      : %d caracteres" % len(html))
    print("  blocs       : %d · huit terrains : %d · questions : %d"
          % (len(re.findall(r'class="blk"', html)), len(C.HUIT), len(C.FAQ)))
    print("  controles   : %s" % ("AUCUN DEFAUT" if not pb else "%d point(s)" % len(pb)))
    for p in pb:
        print("     !", p)
    open(os.path.join(ICI, "preview-negoce-a.html"), "w", encoding="utf-8").write(html)
    if LIVE:
        if pb:
            raise SystemExit("ecriture refusee : des controles ont echoue")
        w.api("pages/%d" % PAGE, "POST", {"content": html, "title": TITRE, "status": "draft"})
        print("\n  ECRIT sur la page %d (brouillon) — %s" % (PAGE, TITRE))
    else:
        print("\n  essai a blanc — rien n'a ete ecrit sur le site")


if __name__ == "__main__":
    main()
