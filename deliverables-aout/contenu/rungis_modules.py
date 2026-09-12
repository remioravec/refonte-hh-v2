#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module a onglets « ce que le logiciel fait du carreau » — page MIN fille.

POURQUOI CE MODULE
==================
Source d'inspiration fournie par le client : la page
https://groupe-bellon.fr/gasc-m-i-n-carreau-produits-carnes/ du Groupe Bellon,
premier concurrent legitime sur le terrain MIN. Sa mecanique, relevee le
12/09/2026 dans son code source :

  · un H2 d'introduction + un schema d'ensemble ;
  · un module Elementor « nested-tabs » de TREIZE onglets ;
  · un onglet = un module fonctionnel = un titre, un paragraphe, une liste a
    puces, une capture 1024x576.

CE QU'ON GARDE — la mecanique. Un seul ecran de page pour toute la couverture
fonctionnelle, choisie au lieu d'etre deroulee. C'est exactement le geste qui
termine une session au lieu de la rendre a la SERP.

CE QU'ON CORRIGE, ET POURQUOI
-----------------------------
1. LE NOMBRE.  Treize onglets, c'est une liste deguisee : personne ne clique
   au-dela du quatrieme. On descend a SEPT, et les sept suivent la journee
   reelle d'un grossiste de carreau, dans l'ordre ou elle se passe.

2. LE VOCABULAIRE.  Bellon nomme ses onglets comme son cahier des charges
   interne : « Agreage », « GED », « EDI », « GASC ». Mesure le 11/09/2026 au
   planificateur Google Ads, France : huit de leurs neuf termes metier
   n'atteignent pas le seuil de mesure (< 10 recherches / mois). On nomme
   chaque onglet par le geste du grossiste, pas par le nom du module.

3. LE JAVASCRIPT.  Chez eux, les douze panneaux non actifs sont replies par le
   script Elementor ; le contenu existe mais depend du script. Ici : boutons
   radio + labels, ZERO JavaScript. Sans CSS les sept panneaux s'affichent a la
   suite. Aucun contenu n'est injecte au clic.

4. LES CAPTURES.  Leurs treize captures sont des JPG de 1024x576 : invisibles
   pour un moteur, illisibles sur mobile, lourdes. Ici les ecrans sont en
   HTML/CSS — du texte reel, redimensionnable, lisible par un lecteur d'ecran.

CE QU'ON LAISSE TOMBER, ET POURQUOI — quatre des treize onglets de Bellon ne
passent pas le filtre du carreau : gestion des dechets, GED, CRM et EDI. Ce
sont des fonctions d'editeur, pas des contraintes du MIN. Elles ont leur place
sur une page produit, pas sur la page d'un marche.

DA — celle du blog Hello Harel : l'entete « mn » (kicker / sous-titre / titre),
la colonne de 820 px, les ecrans plats « hhf/ui » deja utilises sur les
maquettes agroalimentaire et traiteur. Barre d'onglets centree.

Ce fichier ne produit rien seul : il est appele par page_rungis.py.
"""

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import agro_ui as UI                            # noqa: E402
from blog_rungis_infographies import _sc        # noqa: E402


# --------------------------------------------------------------- les ecrans
def _top(actif):
    """Barre de navigation du logiciel, en vocabulaire negoce."""
    items = ["Achats", "Ventes", "Stock", "Qualité", "Comptabilité"]
    nav = "".join('<span%s>%s</span>' % (' class="on"' if i == actif else '', i)
                  for i in items)
    return ('<div class="ui-top"><span class="ui-logo">' + UI._nuage() + 'Hello Harel</span>'
            '<span class="ui-nav">' + nav + '</span>'
            '<span class="ui-me">Paul Dupont ▾</span></div>')


def ecran_achat():
    boxes = ('<div class="ui-boxes">'
             '<span class="ui-box"><i style="background:#3C8DBC">€</i>'
             '<div><b>2,10 €/kg</b>Cours du jour, RNM</div></span>'
             '<span class="ui-box"><i style="background:#00A65A">✓</i>'
             '<div><b>1,95 €/kg</b>Négocié au carreau</div></span>'
             '<span class="ui-box"><i style="background:#F39C12">−7%</i>'
             '<div><b>0,15 €/kg</b>Sous le cours</div></span>'
             '</div>')
    corps = (
        _top("Achats") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Cours du jour", "Saisie carreau", "Commandes",
                    "Fournisseurs", "Réceptions"], 2)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Saisie carreau — mardi 12/09, 5 h 12</span><em>+ ⎙</em></div>'
        + boxes + '<div class="ui-grid one">'
        + UI._card("Ce que vous venez d\'acheter, carreau par carreau",
                   UI._tab(["Carreau", "Produit", "^Colis", "^Prix payé", "^Cours RNM", "Écart"],
                           [["@B14 — Marée", "Bar de ligne 400/600", "^12", "^18,40 €",
                             "^19,10 €", '<span class="ui-pill a">−3,7 %</span>'],
                            ["~@C08 — Fruits et légumes", "Tomate grappe cat. I", "^40",
                             "^1,95 €", "^2,10 €", '<span class="ui-pill a">−7,1 %</span>'],
                            ["@C08 — Fruits et légumes", "Courgette verte", "^24", "^1,42 €",
                             "^1,30 €", '<span class="ui-pill c">+9,2 %</span>'],
                            ["!@A03 — Boucherie", "Épaule de porc", "^8", "^4,80 €",
                             "^4,25 €", '<span class="ui-pill b">+12,9 %</span>']]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Saisie carreau de Hello Harel : quatre achats du matin "
        "comparés au cours du jour publié par FranceAgriMer, avec l'écart de prix ligne à ligne",
        corps, "Hello Harel — Achats",
        "Le cours du jour est chargé avant l'ouverture : on négocie en le voyant. "
        "Données de démonstration.")


def ecran_agreage():
    boxes = ('<div class="ui-boxes">'
             '<span class="ui-box"><i style="background:#3C8DBC">10</i>'
             '<div><b>840 kg</b>Annoncés sur les bons</div></span>'
             '<span class="ui-box"><i style="background:#00A65A">9,7</i>'
             '<div><b>818,4 kg</b>Réellement pesés</div></span>'
             '<span class="ui-box"><i style="background:#DD4B39">−2,6%</i>'
             '<div><b>21,6 kg</b>Écart du matin</div></span>'
             '</div>')
    corps = (
        _top("Achats") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Cours du jour", "Saisie carreau", "Commandes",
                    "Fournisseurs", "Réceptions"], 5)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Agréage à quai — 12/09/2026</span><em>⎙</em></div>'
        + boxes + '<div class="ui-grid one">'
        + UI._card("Poids annoncé, poids pesé, réclamation ouverte",
                   UI._tab(["Lot reçu", "Produit", "^Annoncé", "^Pesé", "^Écart", "Suite donnée"],
                           [["@R-2609-084", "Tomate grappe cat. I", "^400,0 kg", "^391,2 kg",
                             "^−8,8 kg", '<span class="ui-pill c">Réclamation</span>'],
                            ["~@R-2609-085", "Bar de ligne 400/600", "^96,0 kg", "^95,4 kg",
                             "^−0,6 kg", '<span class="ui-pill a">Accepté</span>'],
                            ["!@R-2609-086", "Courgette verte", "^240,0 kg", "^228,6 kg",
                             "^−11,4 kg", '<span class="ui-pill b">Avoir demandé</span>'],
                            ["@R-2609-087", "Épaule de porc", "^104,0 kg", "^103,2 kg",
                             "^−0,8 kg", '<span class="ui-pill a">Accepté</span>']]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Agréage de Hello Harel : quatre lots reçus avec leur poids "
        "annoncé, leur poids réellement pesé, l'écart et la suite donnée au fournisseur",
        corps, "Hello Harel — Agréage",
        "L'écart n'est pas constaté en fin de mois : il ouvre la réclamation à quai. "
        "Données de démonstration.")


def ecran_preparation():
    corps = (
        _top("Ventes") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Commandes clients", "Préparation", "Colisage",
                    "Expéditions", "Clients"], 2)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Préparation — commande CDE/2609-118, Brasserie du Port</span>'
        '<em>⎙</em></div><div class="ui-grid one">'
        + UI._card("Ce qui est pesé sort tel qu'il est pesé",
                   UI._tab(["Ligne", "Produit", "Lot prélevé", "^Commandé", "^Pesé", "^Colis"],
                           [["01", "Bar de ligne 400/600", "@L2609-084", "^12,0 kg",
                             "^12,340 kg", "^2"],
                            ["~02", "Tomate grappe cat. I", "@L2609-081", "^25,0 kg",
                             "^24,810 kg", "^5"],
                            ["03", "Courgette verte", "@L2609-086", "^18,0 kg",
                             "^18,220 kg", "^3"],
                            ["~04", "Épaule de porc", "@L2609-087", "^9,0 kg",
                             "^9,060 kg", "^1"]]))
        + UI._card("Contrôle de sortie",
                   '<div class="ui-boxes">'
                   '<span class="ui-box"><i style="background:#00A65A">11</i>'
                   '<div><b>11 colis</b>Étiquetés, lot et DLC portés</div></span>'
                   '<span class="ui-box"><i style="background:#3C8DBC">64,4</i>'
                   '<div><b>64,430 kg</b>Poids réel de la commande</div></span>'
                   '<span class="ui-box"><i style="background:#F39C12">3°</i>'
                   '<div><b>3,1 °C</b>Relevé au chargement</div></span>'
                   '</div>', croix=False)
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Préparation de Hello Harel : quatre lignes de commande avec "
        "le lot prélevé, le poids commandé, le poids réellement pesé et le nombre de colis",
        corps, "Hello Harel — Préparation",
        "Le poids pesé à la préparation est celui qui partira sur la facture. "
        "Données de démonstration.")


def ecran_tournee():
    boxes = ('<div class="ui-boxes">'
             '<span class="ui-box"><i style="background:#3C8DBC">3</i>'
             '<div><b>3 tournées</b>Au départ de Rungis</div></span>'
             '<span class="ui-box"><i style="background:#00A65A">42</i>'
             '<div><b>42 clients</b>À livrer avant 11 h</div></span>'
             '<span class="ui-box"><i style="background:#DD4B39">1</i>'
             '<div><b>1 retard</b>Créneau dépassé de 20 min</div></span>'
             '</div>')
    corps = (
        _top("Ventes") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Commandes clients", "Préparation", "Colisage",
                    "Expéditions", "Clients"], 4)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Tournées du 12/09 — départ carreau 7 h 10</span><em>⎙</em></div>'
        + boxes + '<div class="ui-grid one">'
        + UI._card("Où en est chaque camion",
                   UI._tab(["Tournée", "Client", "Créneau", "^Colis", "^T° caisse", "État"],
                           [["@T1 — Paris 11e", "Brasserie du Port", "08 h 00 – 08 h 30",
                             "^11", "^3,1 °C", '<span class="ui-pill a">Livré, signé</span>'],
                            ["~@T1 — Paris 11e", "Table d'Armand", "08 h 45 – 09 h 15",
                             "^6", "^3,0 °C", '<span class="ui-pill a">Livré, signé</span>'],
                            ["!@T2 — Sud 92", "Collège Jean-Moulin", "09 h 00 – 09 h 30",
                             "^18", "^3,4 °C", '<span class="ui-pill b">Retard 20 min</span>'],
                            ["@T3 — Est 94", "Traiteur Le Verger", "10 h 00 – 10 h 30",
                             "^9", "^2,8 °C", '<span class="ui-pill c">En route</span>']]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Tournées de Hello Harel : trois tournées au départ de Rungis, "
        "avec pour chaque client le créneau, le nombre de colis, la température relevée et l'état",
        corps, "Hello Harel — Expéditions",
        "La température du chargement suit le bon : elle est opposable à la réception. "
        "Données de démonstration.")


def ecran_facture():
    corps = (
        _top("Comptabilité") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Factures de vente", "Factures d'achat", "Règlements",
                    "Taxes et contributions", "Export comptable"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Facture FA/2609-341 — Brasserie du Port</span><em>⎙</em></div>'
        '<div class="ui-grid one">'
        + UI._card("Facturé au poids livré, pas au poids commandé",
                   UI._tab(["Ligne", "Produit", "^Commandé", "^Livré", "^PU HT", "^Total HT"],
                           [["01", "Bar de ligne 400/600", "^12,000 kg", "^12,340 kg",
                             "^24,90 €", "^307,27 €"],
                            ["~02", "Tomate grappe cat. I", "^25,000 kg", "^24,810 kg",
                             "^3,10 €", "^76,91 €"],
                            ["03", "Courgette verte", "^18,000 kg", "^18,220 kg",
                             "^2,45 €", "^44,64 €"],
                            ["~04", "Épaule de porc", "^9,000 kg", "^9,060 kg",
                             "^7,80 €", "^70,67 €"]]))
        + UI._card("Ce que la facture porte en plus",
                   '<div class="ui-boxes">'
                   '<span class="ui-box"><i style="background:#3C8DBC">TVA</i>'
                   '<div><b>5,5 % et 20 %</b>Deux taux sur la même facture</div></span>'
                   '<span class="ui-box"><i style="background:#00A65A">499</i>'
                   '<div><b>499,49 € HT</b>Poids réel, pas poids rond</div></span>'
                   '<span class="ui-box"><i style="background:#F39C12">e</i>'
                   '<div><b>Factur-X</b>Format structuré prêt</div></span>'
                   '</div>', croix=False)
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Facture de Hello Harel : quatre lignes facturées au poids "
        "réellement livré, avec les deux taux de TVA et le format Factur-X",
        corps, "Hello Harel — Comptabilité",
        "Entre le poids commandé et le poids livré, l'écart est facturé, pas offert. "
        "Données de démonstration.")


def ecran_marge():
    corps = (
        _top("Achats") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Marge par lot", "Marge par client", "Rotation",
                    "Casse et démarque", "Exports"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Marge réelle — semaine 37</span><em>⎙</em></div>'
        '<div class="ui-grid one">'
        + UI._card("Où part la marge du carreau",
                   '<span class="ui-donut">'
                   + UI._ring([("#00A65A", 62), ("#F39C12", 21), ("#DD4B39", 11),
                               ("#CBD5E1", 6)])
                   + UI._leg([("#00A65A", "Marge conservée", "62 %", "62"),
                              ("#F39C12", "Écart de poids non refacturé", "21 %", "21"),
                              ("#DD4B39", "Casse et démarque DLC", "11 %", "11"),
                              ("#CBD5E1", "Remises de fin de tournée", "6 %", "6")])
                   + '</span>')
        + UI._card("Marge par lot acheté au carreau",
                   UI._tab(["Lot", "Produit", "^Acheté", "^Vendu", "^Perte", "^Marge nette"],
                           [["@L2609-081", "Tomate grappe cat. I", "^1 240 €", "^1 612 €",
                             "^38 €", "^26,9 %"],
                            ["~@L2609-084", "Bar de ligne 400/600", "^1 766 €", "^2 288 €",
                             "^0 €", "^29,6 %"],
                            ["!@L2609-086", "Courgette verte", "^341 €", "^396 €",
                             "^74 €", "^−5,6 %"],
                            ["@L2609-087", "Épaule de porc", "^499 €", "^688 €",
                             "^12 €", "^35,5 %"]]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Marge de Hello Harel : la répartition de la marge perdue et "
        "la marge nette lot par lot, dont un lot en perte",
        corps, "Hello Harel — Analyse",
        "La ligne rouge est un lot acheté trop cher et écoulé trop tard. "
        "Données de démonstration.")


# --------------------------------------------------------------- les onglets
#   (court, titre H3, chapo, points, fabrique d'ecran, equivalent chez Bellon)
MODULES = [
    ("Acheter",
     "Acheter au carreau avec le cours du jour sous les yeux",
     "Le prix du carreau bouge dans la matinée. La seule façon de savoir si on achète bien, "
     "c'est de voir le cours public au moment où l'on négocie, pas le lendemain.",
     ["Les cours FranceAgriMer du MIN de Rungis chargés avant l'ouverture",
      "La saisie se fait carreau par carreau, au fil de la tournée d'achat",
      "L'écart au cours s'affiche à la ligne, pas en fin de mois",
      "Le cadencier reprend ce que vous avez payé la semaine précédente"],
     ecran_achat, "Achat assisté"),

    ("Agréer",
     "Peser à quai, et ouvrir la réclamation dans la foulée",
     "Un colis annoncé à 10 kg qui en pèse 9,7, c'est 3 % offerts à chaque ligne. "
     "L'agréage sert à ce que cet écart soit constaté à quai, tant qu'il est réclamable.",
     ["Poids annoncé et poids pesé sur la même ligne de réception",
      "L'écart déclenche la réclamation fournisseur ou l'avoir",
      "Le lot fournisseur entre dans le système à la pesée, pas à la facture",
      "L'historique des écarts par fournisseur se consulte avant de renégocier"],
     ecran_agreage, "Agréage, réclamation et traçabilité"),

    ("Suivre le lot",
     "Suivre le lot et sa DLC, pas la référence produit",
     "Sur le carreau, deux palettes du même produit n'ont ni la même date ni la même origine. "
     "C'est le lot qui porte la DLC, et c'est le lot qu'il faut sortir en premier.",
     ["Prélèvement FEFO : ce qui périme le plus tôt sort d'abord",
      "La DLC du lot suit la marchandise jusqu'au bon de livraison",
      "Un rappel remonte en amont et redescend en aval depuis le même écran",
      "Le reste à écouler s'affiche en jours, pas en dates à interpréter"],
     UI.ecran_dlc, "Traçabilité (volet lot)"),

    ("Préparer",
     "Préparer en pesant, pour que le poids parte sur la facture",
     "Entre la commande et le camion, la marchandise est pesée une deuxième fois. Si ce poids "
     "ne remonte pas dans la ligne, l'écart se paie deux fois : à l'achat et à la vente.",
     ["Le poids pesé à la préparation remplace le poids commandé",
      "Chaque colis sort étiqueté avec son lot et sa DLC",
      "La température de chargement est relevée sur le même écran",
      "Le reliquat repart en stock au lieu de disparaître"],
     ecran_preparation, "Préparation, fabrication et découpe · Assemblage"),

    ("Livrer",
     "Livrer avant l'ouverture des clients, et le prouver",
     "Une commande partie du marché à 7 h doit être chez le restaurateur avant son service. "
     "Le créneau et la température sont ce que le client contrôle à la réception.",
     ["Les tournées se construisent depuis les commandes du matin",
      "Le créneau de chaque client est tenu ou signalé en retard",
      "La température du chargement suit le bon de livraison",
      "Le bon signé revient dans le dossier client, pas dans un classeur"],
     ecran_tournee, "Transport"),

    ("Facturer",
     "Facturer le poids livré, avec les mentions qui deviennent obligatoires",
     "La facture d'un grossiste de produits frais n'est pas une facture ronde : elle porte des "
     "poids à trois décimales, deux taux de TVA et bientôt un format structuré.",
     ["Le poids livré remonte automatiquement dans la ligne de facture",
      "Deux taux de TVA cohabitent sur la même facture sans ressaisie",
      "Les mentions obligatoires sont portées par le modèle, pas par l'utilisateur",
      "Le format Factur-X est produit en même temps que le PDF"],
     ecran_facture, "Finances et comptabilité · Frais et taxes"),

    ("Mesurer",
     "Mesurer la marge réelle, après écart de poids et après casse",
     "La marge théorique d'un lot se calcule à l'achat. La marge réelle se connaît une fois "
     "l'écart de poids et la démarque DLC déduits — et l'écart est de 38 % dans cet exemple.",
     ["La marge se lit par lot acheté, pas seulement par produit",
      "L'écart de poids non refacturé est isolé des autres pertes",
      "La casse liée à la DLC est rattachée au lot qui l'a produite",
      "Un lot vendu en perte se voit dans la semaine, pas au bilan"],
     ecran_marge, "Statistiques"),
]


# ------------------------------------------------------------------ la feuille
def _css(n):
    base = """
.mnm{display:block;margin:0 !important}
.mnm-pick{position:absolute;opacity:0;width:1px;height:1px;margin:-1px;overflow:hidden;
 clip-path:inset(50%);pointer-events:none}
.mnm-bar{display:flex;gap:.4rem;overflow-x:auto;scrollbar-width:thin;padding:.3rem;
 margin:0 auto 1.8rem !important;background:#f1f5f9;border-radius:999px;
 width:max-content;max-width:100%}
.mnm-bar label{display:flex;align-items:center;gap:.45rem;white-space:nowrap;
 padding:.62rem 1rem;border-radius:999px;font-size:.9rem;font-weight:600;color:#475569;
 cursor:pointer;transition:background .18s ease,color .18s ease;user-select:none;
 margin:0 !important}
.mnm-bar label:hover{background:#e2e8f0;color:#0f172a}
.mnm-bar label b{font-variant-numeric:tabular-nums;font-size:.7rem;font-weight:800;
 color:#94a3b8;letter-spacing:.04em}
.mnm-panels>.mnm-p{display:none}
.mnm-p>*{margin:0 !important}
.mnm-n{display:inline-flex;align-items:center;gap:.55rem;font-size:.72rem;font-weight:700;
 letter-spacing:.12em;text-transform:uppercase;color:#0891b2;margin:0 0 .85rem !important}
.mnm-n b{display:grid;place-items:center;width:25px;height:25px;border-radius:8px;
 background:#ecfeff;color:#0e7490;font-size:.75rem;font-weight:800;letter-spacing:0}
.mnm-p h3{font-size:clamp(1.25rem,2.2vw,1.6rem);line-height:1.25;color:#0f172a;
 font-weight:700;margin:0 0 .75rem !important;letter-spacing:-.02em}
.mnm-c{color:#475569;font-size:1rem;line-height:1.68;margin:0 0 1.1rem !important}
.mnm-l{list-style:none;padding:0 !important;margin:0 0 1.5rem !important;display:grid;
 grid-template-columns:1fr 1fr;gap:.65rem 1.4rem}
.mnm-l li{display:flex;gap:.6rem;align-items:flex-start;color:#334155;font-size:.93rem;
 line-height:1.5;margin:0 !important;padding:0 !important}
.mnm-l li svg{width:18px;height:18px;flex:0 0 18px;margin-top:2px;color:#16DB7F}
.mnm-eq{font-size:.8rem;color:#64748b;margin:1rem 0 0 !important;text-align:center}
.mnm-aide{margin:1.6rem 0 0 !important;font-size:.87rem;color:#64748b;text-align:center}
@media(max-width:700px){
 .mnm-bar{border-radius:16px}
 .mnm-bar label{padding:.55rem .8rem;font-size:.84rem}
 .mnm-l{grid-template-columns:1fr}
}
"""
    r = []
    for k in range(1, n + 1):
        r.append(".mnm-pick:nth-of-type(%d):checked ~ .mnm-bar label[for=\"mnm-o%d\"]"
                 "{background:#00B1F5;color:#fff;box-shadow:0 8px 18px -10px rgba(0,177,245,.9)}"
                 % (k, k))
        r.append(".mnm-pick:nth-of-type(%d):checked ~ .mnm-bar label[for=\"mnm-o%d\"] b"
                 "{color:rgba(255,255,255,.8)}" % (k, k))
        r.append(".mnm-pick:nth-of-type(%d):checked ~ .mnm-panels > .mnm-p:nth-child(%d)"
                 "{display:block}" % (k, k))
        r.append(".mnm-pick:nth-of-type(%d):focus-visible ~ .mnm-bar label[for=\"mnm-o%d\"]"
                 "{outline:3px solid #0f172a;outline-offset:2px}" % (k, k))
    return '<style id="hh-min-modules">' + _sc(base + "\n".join(r)) + "</style>"


CSS = _css(len(MODULES))


def section(kicker="Dans le logiciel",
            sous_titre="Sept gestes, sept écrans, un seul écran de page",
            titre="La journée d'un grossiste de Rungis, module par module"):
    """Le module a onglets, en DA blog, sans une ligne de JavaScript."""
    radios, onglets, panneaux = [], [], []
    for k, (court, h3, chapo, points, fabrique, bellon) in enumerate(MODULES):
        n = k + 1
        radios.append('<input class="mnm-pick" type="radio" name="mnm-onglet" id="mnm-o%d"%s>'
                      % (n, ' checked' if k == 0 else ''))
        onglets.append('<label for="mnm-o%d"><b>%02d</b>%s</label>' % (n, n, court))
        pts = "".join("<li>%s%s</li>" % (UI._check(), p) for p in points)
        panneaux.append(
            '<div class="mnm-p">'
            '<p class="mnm-n"><b>%02d</b>Étape %d sur %d</p>'
            '<h3>%s</h3><p class="mnm-c">%s</p><ul class="mnm-l">%s</ul>'
            '<div class="hhf">%s</div>'
            '<p class="mnm-eq">Chez les éditeurs du marché, cette étape s\'appelle '
            '« %s ».</p></div>'
            % (n, n, len(MODULES), h3, chapo, pts, fabrique(), bellon))

    return ('<figure class="mn" id="mn-modules">'
            '<figcaption class="mn-h"><p class="mn-k">%s</p>'
            '<p class="mn-s">%s</p><p class="mn-t">%s</p></figcaption>'
            % (kicker, sous_titre, titre)
            + '<div class="mnm">' + "".join(radios)
            + '<div class="mnm-bar">' + "".join(onglets) + '</div>'
            + '<div class="mnm-panels">' + "".join(panneaux) + '</div>'
            + '<p class="mnm-aide">Sept étapes, sept écrans. Choisissez la vôtre — '
              'aucune n\'est masquée au robot ni au lecteur d\'écran.</p>'
            '</div></figure>')


if __name__ == "__main__":
    h = CSS + section()
    print("%d onglets, %d octets" % (len(MODULES), len(h)))
    for c in ("mnm-pick", "mnm-p", "<h3"):
        print("  %-10s %d" % (c, h.count(c)))
