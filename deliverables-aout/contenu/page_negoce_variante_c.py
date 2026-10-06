#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variante C du test negoce.

Meme fond que A et B — il vient du meme fichier, negoce_b_contenu — et meme
structure que B. Une seule chose change : les six ecrans du logiciel ne sont
plus des captures matricielles mais des reproductions en HTML et CSS.

Ce que ca rachete, mesurable :
  - nettete a toutes les densites d'ecran, la ou une capture de 1 200 px
    s'affiche floue sur un ecran a deux fois la densite ;
  - environ 21 ko de balisage contre 224 ko d'images ;
  - une mise en page qui s'adapte : le menu lateral et les colonnes secondaires
    se replient en mobile au lieu d'imposer un defilement horizontal ;
  - du texte selectionnable, et des dates qui ne vieillissent pas.

La variante C est construite a partir du constructeur de B : la structure, les
sections et le contenu ne sont ecrits qu'une fois. Seul le composant d'ecran est
substitue.

Usage :  python3 page_negoce_variante_c.py           (essai a blanc)
         python3 page_negoce_variante_c.py --live    (ecriture)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)

import wp_common as w
import negoce_b_contenu as C
import negoce_ui as UI
import page_negoce_variante_b as B

TITRE = "[TEST C] ERP Négoce Alimentaire • Poids Réel, DLC et Marge"
SLUG = "negoce-variante-c"
LIVE = "--live" in sys.argv

# la capture de B <-> l'ecran code de C
ECRAN = {
    "hh-erp-tableau-de-bord-vente": "vente",
    "hh-erp-tableau-de-bord-achats": "achats",
    "hh-erp-stock-fefo-peremption": "stock",
    "hh-erp-quantite-manquante-poids": "preparation",
    "hh-erp-comptabilite-factures-attente": "compta",
    "hh-erp-catalogue-tarifs-marge": "tarifs",
}


def construire():
    # on substitue le composant d'ecran dans le constructeur de B, puis on
    # rebascule l'identifiant de racine et les identifiants du script.
    B.capture = lambda cle, titre=None: UI.ecran(ECRAN[cle])
    html = B.construire()
    html = html.replace("hvb", "hvc")
    html = html.replace("VARIANTE B — test A/B", "VARIANTE C — test A/B")
    html = html.replace("Même contenu que la variante A, UX différente.",
                        "Même contenu que les variantes A et B. "
                        "Les écrans du logiciel sont reproduits en HTML et CSS, pas en image.")
    # le kit d'interface s'ajoute apres la feuille de style de la variante
    html = html.replace('<div id="hvc">', UI.CSS + '<div id="hvc">', 1)
    # une seule mention, discrete, sous la section des onglets
    html = html.replace(
        '</div></section>\n\n' if False else '<div id="hvc-panes">',
        '<p class="ui-note">Interfaces reproduites en HTML et CSS d\'après la '
        '<a href="https://doc.harelsystems.io/doc/basic" rel="nofollow">documentation produit</a>.</p>'
        '<div id="hvc-panes">', 1)
    html = html.replace("</style>", """
#hvc .ui-note{text-align:center;font-size:.8125rem;color:var(--ink3);margin:0 0 1.5rem}
#hvc .ui-note a{color:var(--brand-d);text-decoration:underline}
</style>""", 1)
    return html


def controles(html):
    pb = []
    for t in ("div", "section", "table", "figure", "a", "span", "p"):
        o = len(re.findall(r"<" + t + r"[ >]", html))
        f = len(re.findall(r"</" + t + r">", html))
        if o != f:
            pb.append("balises <%s> desequilibrees : %d / %d" % (t, o, f))
    if "hvb" in html:
        pb.append("un identifiant de la variante B subsiste")

    # les six ecrans sont bien codes, et plus aucune capture matricielle du produit
    # cinq ecrans codes : le hero porte desormais une photo de situation
    if len(re.findall(r'<figure class="ui"', html)) != 5:
        pb.append("les cinq ecrans ne sont pas tous presents")
    if "hero-photo" not in html:
        pb.append("le hero ne porte pas la photo de situation")
    if 'class="shotui"' in html:
        pb.append("une capture matricielle subsiste")
    for u in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if "hh-erp-" in u:
            pb.append("une capture du logiciel est encore chargee en image : " + u[-46:])
    for f in re.findall(r'<figure class="ui" role="img" aria-label="([^"]*)"', html):
        if len(f) < 25:
            pb.append("alternative textuelle trop courte sur un ecran")
    if len(re.findall(r'role="img"', html)) != 5:
        pb.append("un ecran n'est pas annonce comme illustration")

    # aucun marqueur du gabarit de tableau ne doit atteindre le rendu
    for m in re.findall(r'<t[dh][^>]*>([~!@^])', html):
        pb.append("marqueur de gabarit visible dans un tableau : " + m)

    # aplat : ni ombre portee ni degrade lineaire dans le kit d'interface
    kit = re.search(r'<style id="hh-vC-ui">.*?</style>', html, re.S)
    if kit:
        if "box-shadow" in kit.group(0):
            pb.append("une ombre portee subsiste dans le kit d'interface")
        if "linear-gradient" in kit.group(0):
            pb.append("un degrade lineaire subsiste dans le kit d'interface")
    else:
        pb.append("le kit d'interface est absent")

    # le fond reste celui de A et B
    for att in (C.CALC_TOTAL[1], C.CALC_COEF[1], "17,51 €", "0,51 €", "7 344 €"):
        if att not in html:
            pb.append("valeur du fond commun absente : " + att)
    for q, _m, _r in C.FAQ:
        if q not in html:
            pb.append("question absente : " + q[:44])
    PROT = ("/agroalimentaire/", "/agroalimentaire/traiteur/", "/agroalimentaire/charcutier/",
            "/agroalimentaire/plats-cuisines-industriels/", "/migration-as400/")
    for h in re.findall(r'<a[^>]+href="([^"]+)"', html):
        if h in PROT:
            pb.append("Regle 0 — lien vers une page protegee : " + h)
    return pb


def page_c():
    """Retrouve la page de la variante C, ou la cree."""
    for p in w.get_all("pages", fields="id,slug", status="draft"):
        if p["slug"] == SLUG:
            return p["id"]
    r = w.api("pages", "POST", {"title": TITRE, "slug": SLUG, "status": "draft",
                                "content": "", "template": "elementor_canvas"})
    print("  page creee : id", r["id"])
    return r["id"]


def main():
    html = construire()
    pb = controles(html)
    print("  taille        : %d caracteres" % len(html))
    print("  ecrans codes  : %d" % len(re.findall(r'<figure class="ui"', html)))
    print("  images        : %d (photos de terrain, cartes de modules et logos)"
          % len(re.findall(r"<img", html)))
    print("  controles     : %s" % ("AUCUN DEFAUT" if not pb else "%d point(s)" % len(pb)))
    for p in pb:
        print("     !", p)
    open(os.path.join(ICI, "preview-negoce-c.html"), "w", encoding="utf-8").write(html)
    if LIVE:
        if pb:
            raise SystemExit("ecriture refusee : des controles ont echoue")
        pid = page_c()
        w.api("pages/%d" % pid, "POST", {"content": html, "title": TITRE, "status": "draft"})
        print("\n  ECRIT sur la page %d (brouillon) — %s" % (pid, TITRE))
    else:
        print("\n  essai a blanc — rien n'a ete ecrit sur le site")


if __name__ == "__main__":
    main()
