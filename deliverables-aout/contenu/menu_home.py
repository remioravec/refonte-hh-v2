#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le menu de Hello Harel — celui du site, complete, et genere depuis UN arbre.

DECISION DU 17/09/2026 — on garde le menu actuel : son gabarit, ses classes,
sa feuille de style et son JavaScript ne bougent pas. On ne remplace que le
MARKUP de la navigation, a l'interieur de l'entete existante.

CE QU'ON CORRIGE
----------------
1. Le meme menu n'est pas le meme partout. Releve du 17/09/2026 :
     home (page 2) .......... 7 metiers agroalimentaires
     /negoce/ (page 5957) ... 14 en desktop, 7 en mobile
   Trois versions du meme menu coexistent.

2. Neuf metiers agroalimentaires n'apparaissent nulle part dans le menu de la
   home : patisserie, chocolaterie, glacier, fromagerie, poissonnerie,
   torrefaction, viande, conserverie, brasserie. Toutes ces pages existent et
   repondent 200.

3. Negoce et medical sortent du menu, a la demande du client.

LA METHODE — l'arbre est ecrit UNE fois ci-dessous ; `desktop()` et `mobile()`
en derivent tous les deux. Ils ne peuvent plus diverger, et `controler()` le
verifie en comparant les deux jeux de liens.

Le panneau Industries garde ses TROIS colonnes et sa largeur de 780 px : les
seize metiers y sont repartis en trois familles, donc aucune regle de style
n'a besoin d'etre forcee.
"""

import re

# ------------------------------------------------------- icones du site
#   Jeu Heroicons « outline », au format exact des icones deja en place.
P = {
 "feu":     'M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z',
 "gateau":  'M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18z',
 "etoile":  'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z',
 "flocon":  'M12 3v18M4.5 7.5l15 9M19.5 7.5l-15 9',
 "balance": 'M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3',
 "panier":  'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z',
 "goutte":  'M20 12a8 8 0 01-8 8m0 0a8 8 0 01-8-8m8 8V4m0 0L8 8m4-4l4 4',
 "cube":    'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
 "archive": 'M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4',
 "usine":   'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
 "tasse":   'M3 10h13v5a4 4 0 01-4 4H7a4 4 0 01-4-4v-5zm13 1h2.5a2.5 2.5 0 010 5H16',
 "clients": 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z',
 "facture": 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
 "rouage":  'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z',
 "camion":  'M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0',
 "echange": 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4',
}


def _svg(cle, style=""):
    return ('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"%s>'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
            'd="%s"/></svg>' % (style, P[cle]))


# --------------------------------------------------------------- l'arbre
#   UNE seule source pour le bureau et le mobile.
FONCTIONS = [
 ("Gestion de la relation client", "/fonctionnalites/crm/", "CRM", "clients"),
 ("Gestion de la facturation", "/fonctionnalites/facturation/", "Facturation", "facture"),
 ("Gestion commerciale", "/fonctionnalites/vente/", "Commercial", "panier"),
 ("Gestion des stocks", "/fonctionnalites/gestion-de-stock/", "Stocks", "cube"),
 ("Gestion de la fabrication", "/fonctionnalites/fabrication/", "Fabrication", "rouage"),
 ("Gestion des achats", "/fonctionnalites/achat/", "Achats", "panier"),
 ("Gestion de la logistique", "/fonctionnalites/logistique/", "Logistique", "camion"),
 ("Gestion des imports exports", "/fonctionnalites/import-export/", "Import-Export", "echange"),
]

#   (titre de colonne, icone du titre, [(libelle, url, libelle court, icone)])
INDUSTRIES = [
 ("Métiers de bouche", "feu", [
   ("Boulangerie", "/agroalimentaire/boulanger/", "Boulangerie", "feu"),
   ("Pâtisserie", "/agroalimentaire/patissier/", "Pâtisserie", "gateau"),
   ("Chocolaterie", "/agroalimentaire/chocolatier/", "Chocolaterie", "etoile"),
   ("Glacier", "/agroalimentaire/glacier/", "Glacier", "flocon"),
   ("Charcuterie", "/agroalimentaire/charcutier/", "Charcuterie", "balance"),
   ("Traiteur", "/agroalimentaire/traiteur/", "Traiteur", "feu"),
 ]),
 ("Produits frais", "goutte", [
   ("Fromagerie", "/agroalimentaire/fromager/", "Fromagerie", "goutte"),
   ("Poissonnerie", "/agroalimentaire/poissonnier/", "Poissonnerie", "goutte"),
   ("Fruits et légumes", "/agroalimentaire/maraicher/", "Fruits & Légumes", "panier"),
   ("Viande", "/agroalimentaire/viande/", "Viande", "balance"),
   ("Industrie laitière", "/agroalimentaire/industrie-laitiere/", "Laitier", "goutte"),
 ]),
 ("Transformation", "usine", [
   ("ERP agroalimentaire", "/agroalimentaire/", "Agroalimentaire", "usine"),
   ("Plats cuisinés", "/agroalimentaire/plats-cuisines-industriels/", "Plats cuisinés", "archive"),
   ("Conserverie", "/agroalimentaire/conserverie/", "Conserverie", "archive"),
   ("Brasserie", "/agroalimentaire/brasseur/", "Brasserie", "tasse"),
   ("Torréfaction", "/agroalimentaire/torrefacteur/", "Torréfaction", "tasse"),
 ]),
]

SIMPLES = [("Tarifs", "/tarifs/"), ("Écosystème", "/ecosysteme/")]

CHEVRON = ('<svg class="chevron-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
           '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
           'd="M19 9l-7 7-7-7"/></svg>')


# ------------------------------------------------------------------ bureau
def desktop():
    fonc = "".join(
        '<a href="%s" class="dropdown-link">'
        '<div class="dropdown-link-icon tilted-icon">%s</div>'
        '<span class="dropdown-link-text">%s</span></a>' % (u, _svg(i), lib)
        for lib, u, court, i in FONCTIONS)

    cols = ""
    for titre, ico, liens in INDUSTRIES:
        cols += ('<div class="mega-col">\n<h5>%s %s</h5>\n' % (
                 _svg(ico, ' style="width:1rem;height:1rem"'), titre))
        cols += "".join(
            '<a href="%s" class="industry-link"><div class="tilted-icon-mini">%s</div>'
            '<span>%s</span></a>\n' % (u, _svg(i), lib)
            for lib, u, court, i in liens)
        cols += '</div>\n'

    return ('<nav class="desktop-nav">\n'
            '            <a href="/">Accueil</a>\n'
            '            <div class="nav-dropdown">\n'
            '                <button class="nav-dropdown-trigger">Fonctionnalités %s</button>\n'
            '                <div class="dropdown-panel" style="width:420px;max-width:95vw">\n'
            '                    <div class="dropdown-card">%s</div>\n'
            '                </div>\n            </div>\n'
            '            <div class="nav-dropdown">\n'
            '                <button class="nav-dropdown-trigger">Industries %s</button>\n'
            '                <div class="dropdown-panel mega-industries-card">\n'
            '                    <div class="dropdown-card" style="padding:0;overflow:hidden">\n'
            '                        <div class="mega-industries-inner">\n%s</div>\n'
            '                    </div>\n                </div>\n            </div>\n'
            '%s        </nav>'
            % (CHEVRON, fonc, CHEVRON, cols,
               "".join('            <a href="%s">%s</a>\n' % (u, t) for t, u in SIMPLES)))


# ------------------------------------------------------------------ mobile
def mobile():
    def _acc(titre, contenu):
        return ('<div><button class="mobile-accordion-btn" '
                'onclick="this.classList.toggle(\'open\');'
                'this.nextElementSibling.classList.toggle(\'open\')">%s %s</button>'
                '<div class="mobile-submenu">%s</div></div>' % (titre, CHEVRON, contenu))

    fonc = "".join('<a href="%s"><span class="tilted-icon-mini">%s</span>%s</a>'
                   % (u, _svg(i), court) for lib, u, court, i in FONCTIONS)

    ind = ""
    for titre, ico, liens in INDUSTRIES:
        ind += '\n<span class="mobile-sector-title">%s</span>\n' % titre
        ind += "".join('<a href="%s"><span class="tilted-icon-mini">%s</span>%s</a>\n'
                       % (u, _svg(i), court) for lib, u, court, i in liens)

    return ('<div class="mobile-menu-inner">\n'
            '            <a href="/">Accueil</a>\n'
            '            %s\n            %s\n'
            '%s'
            '            <div class="mobile-ctas">'
            '<a href="/contact/" class="mobile-cta-primary" '
            'style="background:#22C55E !important;border-color:#22C55E !important;">'
            'Demander une démo</a>'
            '<a href="/contact/" class="mobile-cta-secondary">Contactez-nous</a></div>\n'
            '        </div>'
            % (_acc("Fonctionnalités", fonc), _acc("Industries", ind),
               "".join('            <a href="%s">%s</a>\n' % (u, t) for t, u in SIMPLES)))


# ---------------------------------------------------------------- controle
def controler():
    pb = []
    d = set(re.findall(r'href="([^"]+)"', desktop()))
    m = set(re.findall(r'href="([^"]+)"', mobile())) - {"/contact/"}
    if d - m:
        pb.append("en desktop et pas en mobile : %s" % sorted(d - m))
    if m - d:
        pb.append("en mobile et pas en desktop : %s" % sorted(m - d))
    for t, u, c, i in FONCTIONS:
        if i not in P:
            pb.append("icone inconnue : %s" % i)
    for t, ico, liens in INDUSTRIES:
        if ico not in P:
            pb.append("icone de colonne inconnue : %s" % ico)
        for lib, u, c, i in liens:
            if i not in P:
                pb.append("icone inconnue : %s" % i)
    for mot in ("/negoce/", "/medical/"):
        if mot in desktop() or mot in mobile():
            pb.append("%s est encore dans le menu" % mot)
    n = sum(len(l) for _, _, l in INDUSTRIES)
    if n != 16:
        pb.append("%d metiers au lieu de 16" % n)
    return pb


if __name__ == "__main__":
    d, m = desktop(), mobile()
    print("desktop %d octets — %d liens" % (len(d), d.count("<a href=")))
    print("mobile  %d octets — %d liens" % (len(m), m.count("<a href=")))
    print("metiers : %d · fonctionnalites : %d"
          % (sum(len(l) for _, _, l in INDUSTRIES), len(FONCTIONS)))
    for x in controler():
        print("  !", x)
    if not controler():
        print("controle : desktop et mobile portent les memes liens")
