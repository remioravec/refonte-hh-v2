#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module a onglets « la journee d'un grossiste de carreau » — page MIN fille.

D'OU VIENT CE MODULE
====================
Code source fourni par le client : la page
https://groupe-bellon.fr/gasc-m-i-n-carreau-produits-carnes/ du Groupe Bellon.
Sa mecanique, relevee le 12/09/2026 : un H2 d'introduction, un schema, puis un
module Elementor « nested-tabs » de TREIZE onglets — un onglet par module
fonctionnel, avec titre, paragraphe, liste a puces et capture 1024x576.
Leurs treize libelles : Achat assiste · Agreage, reclamation et tracabilite ·
Vente/televente · Preparation, fabrication et decoupe · Gestion des dechets ·
Assemblage/conditionnement · Transport · Statistiques · Frais et taxes ·
Finances/comptabilite · GED · CRM · EDI.

CE QU'ON GARDE — la mecanique. Toute la couverture fonctionnelle dans un seul
ecran de page, choisie au lieu d'etre deroulee.

CE QU'ON CORRIGE
----------------
1. LE NOMBRE.  Treize onglets, c'est une liste deguisee. On descend a SEPT, et
   les sept suivent la journee reelle, dans l'ordre ou elle se passe.
2. LE VOCABULAIRE.  Bellon nomme ses onglets comme son cahier des charges
   interne. Mesure le 11/09/2026 au planificateur Google Ads, France : huit de
   leurs neuf termes metier sont sous le seuil de mesure (< 10 recherches par
   mois). On nomme chaque onglet par le geste du grossiste.
3. LE JAVASCRIPT.  Chez eux, les douze panneaux non actifs dependent du script
   Elementor. Ici : boutons radio et labels, zero JavaScript. Sans CSS, les
   sept panneaux s'affichent a la suite.
4. LES CAPTURES.  Leurs treize JPG deviennent ici des ecrans en HTML/CSS : du
   texte reel, redimensionnable, lisible par un lecteur d'ecran.
5. LES QUATRE ONGLETS QU'ON NE REPREND PAS — dechets, GED, CRM, EDI. Ce sont
   des fonctions d'editeur, pas des contraintes du carreau.

LA SCENE EST DATEE, ET ELLE SE TIENT
------------------------------------
Les sept ecrans racontent LA MEME journee : jeudi 10 septembre 2026, 5 h 45.
Jeudi parce que la boucherie ne tourne que du lundi au vendredi ; 5 h 45 parce
que les fruits et legumes ouvrent a 5 h 30 et que la maree ferme a 6 h — les
horaires sont ceux de la frise publiee plus bas sur la meme page.
Quatre lots traversent les sept ecrans sans changer ni de numero ni de poids :
  L2609-081 tomate grappe · L2609-084 bar de ligne ·
  L2609-086 courgette verte · L2609-087 epaule de porc
Chaque montant affiche se recalcule a partir du poids PESE et du prix paye.
Toute retouche d'un chiffre doit etre repercutee dans les sept ecrans : c'est
la continuite d'un ecran a l'autre qui rend la demonstration credible.

DA — celle du blog Hello Harel : entete « mn », colonne de 860 px, ecrans plats
« hhf/ui » des maquettes agroalimentaire et traiteur. Barre d'onglets centree.

Ce fichier ne produit rien seul : il est appele par page_rungis_b.py.
"""

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import agro_ui as UI                            # noqa: E402
import page_min_contenu as PC                   # noqa: E402
from blog_rungis_infographies import _sc        # noqa: E402

JOUR = "jeudi 10/09"


# --------------------------------------------------------------- les briques
def _top(actif):
    """Barre de navigation du logiciel, en vocabulaire negoce."""
    items = ["Achats", "Ventes", "Stock", "Analyse", "Comptabilité"]
    nav = "".join('<span%s>%s</span>' % (' class="on"' if i == actif else '', i)
                  for i in items)
    return ('<div class="ui-top"><span class="ui-logo">' + UI._nuage() + 'Hello Harel</span>'
            '<span class="ui-nav">' + nav + '</span>'
            '<span class="ui-me">Paul Dupont ▾</span></div>')


def _boxes(trois):
    return ('<div class="ui-boxes">' + "".join(
        '<span class="ui-box"><i style="background:%s">%s</i>'
        '<div><b>%s</b>%s</div></span>' % t for t in trois) + '</div>')


# ---------------------------------------------------------------- les ecrans
def ecran_achat():
    corps = (
        _top("Achats") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Cotations RNM", "Saisie carreau", "Commandes",
                    "Fournisseurs", "Réceptions"], 2)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Saisie carreau — %s, 5 h 45</span><em>+ ⎙</em></div>' % JOUR
        + _boxes([("#275E80", "4", "lots achetés", "Au carreau, entre 5 h 45 et 6 h 30"),
                  ("#0F7A45", "2", "sous la cotation", "Le bar et la tomate"),
                  ("#B45309", "2", "au-dessus", "La courgette et l'épaule")])
        + '<div class="ui-grid one">'
        + UI._card("Ce que vous venez d'acheter, pavillon par pavillon",
                   UI._tab(["Pavillon", "Produit", "^Colis", "^Prix payé",
                            "^Cotation RNM", "Écart"],
                           [["@Marée — pavillon A4", "Bar de ligne 400/600", "^12",
                             "^18,40 €", "^19,10 €", '<span class="ui-pill a">−3,7 %</span>'],
                            ["~@Fruits et légumes", "Tomate grappe cat. I", "^40",
                             "^1,95 €", "^2,10 €", '<span class="ui-pill a">−7,1 %</span>'],
                            ["@Fruits et légumes", "Courgette verte", "^24",
                             "^1,42 €", "^1,30 €", '<span class="ui-pill c">+9,2 %</span>'],
                            ["!@Boucherie, porc, triperie", "Épaule de porc", "^8",
                             "^4,80 €", "^4,25 €", '<span class="ui-pill b">+12,9 %</span>']]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Saisie carreau de Hello Harel : quatre achats du matin "
        "comparés à la dernière cotation FranceAgriMer, avec l'écart de prix ligne à ligne",
        corps, "Hello Harel — Achats",
        "La dernière cotation RNM publiée est chargée avant le départ au marché. "
        "Données de démonstration.")


def ecran_agreage():
    corps = (
        _top("Achats") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Cotations RNM", "Saisie carreau", "Commandes",
                    "Fournisseurs", "Réceptions"], 5)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Agréage à quai — %s</span><em>⎙</em></div>' % JOUR
        + _boxes([("#275E80", "840", "kg annoncés", "Sur les bons des fournisseurs"),
                  ("#0F7A45", "818", "kg pesés", "Réellement entrés en stock"),
                  ("#C0392B", "−2,6%", "21,6 kg", "Écart constaté à quai")])
        + '<div class="ui-grid one">'
        + UI._card("Lots reçus ce matin",
                   UI._tab(["Lot", "Produit", "^Annoncé", "^Pesé", "^Écart", "Suite donnée"],
                           [["@L2609-081", "Tomate grappe cat. I", "^400,0 kg", "^391,2 kg",
                             "^−8,8 kg", '<span class="ui-pill c">Réclamation</span>'],
                            ["~@L2609-084", "Bar de ligne 400/600", "^96,0 kg", "^95,4 kg",
                             "^−0,6 kg", '<span class="ui-pill a">Accepté</span>'],
                            ["!@L2609-086", "Courgette verte", "^240,0 kg", "^228,6 kg",
                             "^−11,4 kg", '<span class="ui-pill b">Avoir demandé</span>'],
                            ["@L2609-087", "Épaule de porc", "^104,0 kg", "^103,2 kg",
                             "^−0,8 kg", '<span class="ui-pill a">Accepté</span>']]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Agréage de Hello Harel : quatre lots reçus avec leur poids "
        "annoncé, leur poids réellement pesé, l'écart et la suite donnée au fournisseur",
        corps, "Hello Harel — Agréage",
        "L'écart se constate à quai, tant qu'il est réclamable. Données de démonstration.")


def ecran_dlc():
    """Le meme ecran que sur les autres maquettes, mais sur les lots du carreau.

    UI.ecran_dlc() affiche de la creme UHT et des epinards : sur cette page, les
    sept ecrans doivent montrer les quatre memes lots, sinon la demonstration se
    lit comme sept captures sans rapport.
    """
    corps = (
        _top("Stock") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Produits stockés", "Tout le stock", "Emplacements",
                    "Inventaires", "Transferts"], 2)
        + '<div class="ui-main"><div class="ui-h"><span>Dates limites — %s</span>'
          '<em>+ ⎙</em></div>' % JOUR
        + _boxes([("#C0392B", "1", "lot à sortir", "Le bar de ligne, date limite au 11/09"),
                  ("#275E80", "304", "kg en stock", "Sur les quatre lots du carreau"),
                  ("#0F7A45", "3,5", "jours en moyenne", "Avant date limite, tous lots confondus")])
        + '<div class="ui-grid one">'
        + UI._card("Stratégie de prélèvement appliquée",
                   '<span class="ui-donut">' + UI._ring([("#FA8F92", 71), ("#FFDDA8", 29)])
                   + UI._leg([("#FA8F92", "Par date limite — au plus près de la DLC",
                               "71 %", "34"),
                              ("#FFDDA8", "Par ordre d'entrée — au plus ancien",
                               "29 %", "14")])
                   + '</span>')
        + UI._card("À prélever en priorité",
                   UI._tab(["Lot", "Produit", "^En stock", "DLC", "^Reste"],
                           [["!@L2609-084", "Bar de ligne 400/600", "^18 kg",
                             "11/09/2026", "^1 j"],
                            ["@L2609-086", "Courgette verte", "^96 kg",
                             "12/09/2026", "^2 j"],
                            ["~@L2609-081", "Tomate grappe cat. I", "^148 kg",
                             "14/09/2026", "^4 j"],
                            ["@L2609-087", "Épaule de porc", "^42 kg",
                             "17/09/2026", "^7 j"]]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Dates limites de Hello Harel : la part des prélèvements faits "
        "par date limite, et les quatre lots du carreau classés par date limite restante",
        corps, "Hello Harel — Stock",
        "La ligne rouge périme demain : c'est le bar acheté ce matin. "
        "Données de démonstration.")


def ecran_preparation():
    corps = (
        _top("Ventes") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Commandes clients", "Préparation", "Colisage",
                    "Expéditions", "Clients"], 2)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Préparation — CDE/2609-118, Brasserie du Port</span>'
        '<em>⎙</em></div><div class="ui-grid one">'
        + UI._card("Lignes préparées",
                   UI._tab(["Ligne", "Produit", "Lot prélevé", "^Commandé", "^Pesé", "^Colis"],
                           [["01", "Bar de ligne 400/600", "@L2609-084", "^12,000 kg",
                             "^12,340 kg", "^2"],
                            ["~02", "Tomate grappe cat. I", "@L2609-081", "^25,000 kg",
                             "^24,810 kg", "^5"],
                            ["03", "Courgette verte", "@L2609-086", "^18,000 kg",
                             "^18,220 kg", "^3"],
                            ["~04", "Épaule de porc", "@L2609-087", "^9,000 kg",
                             "^9,060 kg", "^1"]]))
        + UI._card("Contrôle de sortie",
                   _boxes([("#0F7A45", "11", "colis", "Étiquetés, lot et date limite portés"),
                           ("#275E80", "64", "kg pesés", "64,430 kg exactement"),
                           ("#B45309", "3,1", "°C", "Relevé au chargement, consigne 0 à 4 °C")]),
                   croix=False)
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Préparation de Hello Harel : quatre lignes de commande avec "
        "le lot prélevé, le poids commandé, le poids réellement pesé et le nombre de colis",
        corps, "Hello Harel — Préparation",
        "Les 64,430 kg pesés ici sont ceux qui partiront sur la facture. "
        "Données de démonstration.")


def ecran_tournee():
    corps = (
        _top("Ventes") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Commandes clients", "Préparation", "Colisage",
                    "Expéditions", "Clients"], 4)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Tournées du %s — départ carreau 7 h 10</span><em>⎙</em></div>' % JOUR
        + _boxes([("#275E80", "3", "tournées", "Au départ de Rungis"),
                  ("#0F7A45", "42", "clients", "À livrer avant 11 h"),
                  ("#C0392B", "1", "retard", "Créneau dépassé de 20 min")])
        + '<div class="ui-grid one">'
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
        "avec pour chaque client le créneau, le nombre de colis, la température et l'état",
        corps, "Hello Harel — Expéditions",
        "Les 11 colis de la première ligne sont ceux préparés à l'écran précédent. "
        "Données de démonstration.")


def ecran_facture():
    corps = (
        _top("Comptabilité") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Factures de vente", "Factures d'achat", "Règlements",
                    "Taxes et contributions", "Export comptable"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Facture FA/2609-341 — Brasserie du Port</span><em>⎙</em></div>'
        '<div class="ui-grid one">'
        + UI._card("Lignes facturées",
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
                   _boxes([("#275E80", "5,5", "% de TVA", "Un seul taux, porté par la fiche produit"),
                           ("#0F7A45", "499", "€ HT", "Soit 499,49 € au poids livré"),
                           ("#B45309", "64", "kg facturés", "Exactement le poids préparé")]),
                   croix=False)
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Facture de Hello Harel : quatre lignes facturées au poids "
        "réellement livré, pour un total de 499,49 euros hors taxes",
        corps, "Hello Harel — Comptabilité",
        "64,430 kg préparés, 64,430 kg facturés. Données de démonstration.")


def ecran_marge():
    corps = (
        _top("Analyse") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Marge par lot", "Marge par client", "Rotation",
                    "Démarque", "Exports"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Marge par lot — semaine du 7 au 11 septembre</span><em>⎙</em></div>'
        + _boxes([("#0F7A45", "26,5", "% de marge", "Après écart de poids et démarque"),
                  ("#B45309", "135", "€ de perte", "Démarque sur date limite"),
                  ("#C0392B", "1", "lot en perte", "La courgette, −18,8 %")])
        + '<div class="ui-grid one">'
        + UI._card("Où la marge théorique est partie",
                   '<span class="ui-donut">'
                   + UI._ring([("#0F7A45", 90), ("#B45309", 10)])
                   + UI._leg([("#0F7A45", "Marge réalisée", "90 %", "1 251 €"),
                              ("#B45309", "Perte sur date limite", "10 %", "135 €")])
                   + '</span>')
        + UI._card("Lot par lot, au poids pesé",
                   UI._tab(["Lot", "Produit", "^Acheté", "^Vendu", "^Perte", "^Taux de marge"],
                           [["@L2609-084", "Bar de ligne 400/600", "^1 755 €", "^2 375 €",
                             "^0 €", "^26,1 %"],
                            ["~@L2609-081", "Tomate grappe cat. I", "^763 €", "^1 176 €",
                             "^23 €", "^33,2 %"],
                            ["@L2609-087", "Épaule de porc", "^495 €", "^805 €",
                             "^0 €", "^38,5 %"],
                            ["!@L2609-086", "Courgette verte", "^325 €", "^368 €",
                             "^112 €", "^−18,8 %"]]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Marge de Hello Harel : la répartition de la marge théorique "
        "et le taux de marge des quatre lots du carreau, dont un lot vendu en perte",
        corps, "Hello Harel — Analyse",
        "La ligne rouge est le lot de courgettes : payé 9,2 % au-dessus de la cotation, reçu "
        "avec 11,4 kg de moins, écoulé trop tard. Données de démonstration.")


# --------------------------------------------------------------- les onglets
#   (libelle court, titre H3, chapo, puces, fabrique d'ecran)
#   Les longueurs sont volontairement inegales : 3, 4, 5, 3, 4, 4, 3 puces, des
#   chapos de une a trois phrases, des titres tantot verbe tantot nom. Sept
#   blocs coules dans le meme moule se lisent comme du remplissage.
MODULES = [
    ("Acheter",
     "Acheter au carreau avec la dernière cotation sous les yeux",
     "Le prix du carreau se négocie de vive voix, et la seule référence commune aux deux "
     "parties est la cotation publiée par FranceAgriMer.",
     ["La dernière cotation RNM est chargée avant le départ au marché",
      "La saisie se fait pavillon par pavillon, au fil de la tournée d'achat",
      "L'écart à la cotation s'affiche sur la ligne, à la saisie"],
     ecran_achat),

    ("Agréer",
     "Le poids à quai, et la réclamation dans la foulée",
     "Un colis annoncé à 10 kg qui en pèse 9,7 laisse 300 grammes sur le quai. Constaté à "
     "la pesée, l'écart se réclame ; découvert au moment de payer, il est perdu.",
     ["Poids annoncé et poids pesé sur la même ligne de réception",
      "L'écart ouvre la réclamation fournisseur ou la demande d'avoir",
      "Le lot fournisseur entre dans le système dès la pesée",
      "L'historique des écarts par fournisseur s'ouvre avant de renégocier"],
     ecran_agreage),

    ("Suivre le lot",
     "La date limite appartient au lot, pas au produit",
     "Deux palettes du même produit n'ont ni la même date ni la même origine. Ce qui se "
     "suit, c'est le lot.",
     ["Le prélèvement suit la date limite par défaut, produit par produit",
      "L'ordre d'entrée reste applicable là où il a du sens",
      "La date limite du lot voyage jusqu'au bon de livraison",
      "Un rappel remonte au fournisseur et redescend aux clients livrés",
      "Le reste à écouler s'affiche en jours"],
     ecran_dlc),

    ("Préparer",
     "Préparer en pesant",
     "Entre la commande et le camion, la marchandise repasse sur la balance. Ce poids-là "
     "est le seul qui compte. Il remonte dans la ligne avant que le camion parte.",
     ["Le poids pesé à la préparation remplace le poids commandé",
      "Chaque colis sort étiqueté avec son lot et sa date limite",
      "La chute de découpe retourne en stock sous son lot d'origine"],
     ecran_preparation),

    ("Livrer",
     "Livrer avant l'ouverture des clients, et le prouver",
     "Une commande partie du marché à 7 h doit être chez le restaurateur avant son service. "
     "Le créneau tenu et la température relevée sont ce qu'il contrôle à la réception.",
     ["Les tournées se construisent depuis les commandes du matin",
      "Le créneau de chaque client est tenu ou signalé en retard",
      "La température du chargement suit le bon de livraison",
      "Le bon signé revient dans le dossier client"],
     ecran_tournee),

    ("Facturer",
     "La facture d'un grossiste de produits frais",
     "Des poids à trois décimales, un taux de TVA porté par la fiche produit, et bientôt un "
     "format structuré à produire. Peu d'outils généralistes savent sortir cette facture-là.",
     ["Le poids livré remonte automatiquement dans la ligne de facture",
      "Le taux de TVA vient de la fiche produit, sans arbitrage à la main",
      "Les mentions obligatoires sont portées par le modèle de document",
      "Le format Factur-X est produit en même temps que le PDF"],
     ecran_facture),

    ("Mesurer",
     "Mesurer la marge une fois la perte déduite",
     "La marge théorique se calcule à l'achat. La marge réelle se connaît une fois la "
     "démarque déduite, lot par lot.",
     ["La marge se lit par lot acheté, au poids pesé",
      "La perte sur date limite est rattachée au lot qui l'a produite",
      "Un lot vendu en perte se voit dans la semaine"],
     ecran_marge),
]


# ------------------------------------------------------------- le schema d'intro
def schema():
    """Les trois contraintes du carreau, sans la frise a cinq etapes.

    page_min_visuels.contraintes() affiche AUSSI un flux en cinq etapes. Sur
    cette page, le module a onglets EST le flux, en sept etapes : afficher les
    deux, c'est donner au lecteur deux modeles concurrents de la meme journee.
    """
    c = "".join('<div class="mn-c"><b>%s</b><span>%s</span><em>%s</em></div>' % t
                for t in PC.CONTRAINTES)
    return ('<figure class="mn" id="mn-contraintes">'
            '<figcaption class="mn-h"><p class="mn-k">Le carreau</p>'
            '<p class="mn-s">Ce que le marché impose, avant tout logiciel</p>'
            '<p class="mn-t">Trois contraintes, et ce qu\'elles coûtent</p></figcaption>'
            '<div class="mn-tri">' + c + '</div></figure>')


# ------------------------------------------------------------------ la feuille
def _css(n):
    base = """
.mnm{display:block;margin:0 !important;background:#fff;border:1px solid #E2E8F0;border-radius:16px;padding:1.5rem}
.mnm-pick{position:absolute;opacity:0;width:1px;height:1px;margin:-1px;overflow:hidden;
 clip-path:inset(50%);pointer-events:none}
.mnm-bar{display:flex;gap:.4rem;overflow-x:auto;scrollbar-width:thin;padding:.3rem;
 margin:0 auto 2rem !important;background:#f1f5f9;border-radius:999px;
 width:max-content;max-width:100%}
.mnm-bar label{display:flex;align-items:center;gap:.45rem;white-space:nowrap;
 min-height:44px;padding:.55rem 1rem;border-radius:999px;font-size:.9rem;font-weight:600;
 color:#3f4c5f;cursor:pointer;transition:background .18s ease,color .18s ease;
 user-select:none;margin:0 !important}
.mnm-bar label:hover{background:#e2e8f0;color:#0f172a}
.mnm-bar label b{font-variant-numeric:tabular-nums;font-size:.7rem;font-weight:800;
 color:#475569;letter-spacing:.04em}
.mnm-panels{display:grid}
.mnm-panels>.mnm-p{grid-column:1;grid-row:1;visibility:hidden}
.mnm-p>*{margin:0 !important}
.mnm-n{font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
 color:#046C93;margin:0 0 .7rem !important}
.mnm-p h3{font-size:clamp(1.05rem,1.6vw,1.2rem);line-height:1.3;color:#101828;
 font-weight:700;margin:0 0 .75rem !important;letter-spacing:-.02em}
.mnm-c{color:#101828;font-size:1rem;line-height:1.68;margin:0 0 1.2rem !important}
.mnm-l{list-style:none;padding:0 !important;margin:0 0 1.6rem !important;display:grid;
 grid-template-columns:1fr 1fr;gap:.7rem 1.5rem}
.mnm-l li{display:flex;gap:.6rem;align-items:flex-start;color:#334155;font-size:.93rem;
 line-height:1.5;margin:0 !important;padding:0 !important}
.mnm-l li svg{width:18px;height:18px;flex:0 0 18px;margin-top:2px;color:#0ea5e9}
.mnm-aide{margin:1.6rem 0 0 !important;font-size:.87rem;color:#546174;text-align:center}
@media(max-width:820px){
 .mnm-bar{flex-wrap:wrap;justify-content:center;overflow:visible;border-radius:20px}
 .mnm-bar label{padding:.5rem .8rem;font-size:.84rem}
 .mnm-l{grid-template-columns:1fr}
}
"""
    r = []
    for k in range(1, n + 1):
        r.append(".mnm-pick:nth-of-type(%d):checked ~ .mnm-bar label[for=\"mnm-o%d\"]"
                 "{background:#0079b8;color:#fff}" % (k, k))
        r.append(".mnm-pick:nth-of-type(%d):checked ~ .mnm-bar label[for=\"mnm-o%d\"] b"
                 "{color:rgba(255,255,255,.82)}" % (k, k))
        r.append(".mnm-pick:nth-of-type(%d):checked ~ .mnm-panels > .mnm-p:nth-child(%d)"
                 "{visibility:visible}" % (k, k))
        r.append(".mnm-pick:nth-of-type(%d):focus-visible ~ .mnm-bar label[for=\"mnm-o%d\"]"
                 "{outline:3px solid #0f172a;outline-offset:2px}" % (k, k))
    return '<style id="hh-min-modules">' + _sc(base + "\n".join(r)) + "</style>"


CSS = _css(len(MODULES))


def section(kicker="Dans le logiciel",
            sous_titre="Sept étapes, sept écrans, une seule journée",
            titre="La journée du 10 septembre, module par module"):
    """Le module a onglets, en DA blog, sans une ligne de JavaScript."""
    radios, onglets, panneaux = [], [], []
    for k, (court, h3, chapo, points, fabrique) in enumerate(MODULES):
        n = k + 1
        radios.append('<input class="mnm-pick" type="radio" name="mnm-onglet" id="mnm-o%d"%s>'
                      % (n, ' checked' if k == 0 else ''))
        onglets.append('<label for="mnm-o%d"><b>%02d</b>%s</label>' % (n, n, court))
        pts = "".join("<li>%s%s</li>" % (UI._check(), p) for p in points)
        panneaux.append(
            '<div class="mnm-p">'
            '<p class="mnm-n">Étape %d sur %d</p>'
            '<h3>%s</h3><p class="mnm-c">%s</p><ul class="mnm-l">%s</ul>'
            '<div class="hhf">%s</div></div>'
            % (n, len(MODULES), h3, chapo, pts, fabrique()))

    return ('<figure class="mn" id="mn-modules">'
            '<figcaption class="mn-h"><p class="mn-k">%s</p>'
            '<p class="mn-s">%s</p><p class="mn-t">%s</p></figcaption>'
            % (kicker, sous_titre, titre)
            + '<div class="mnm">' + "".join(radios)
            + '<div class="mnm-bar">' + "".join(onglets) + '</div>'
            + '<div class="mnm-panels">' + "".join(panneaux) + '</div>'
            + '<p class="mnm-aide">Les sept étapes sont sur cette page.</p>'
            '</div></figure>')


if __name__ == "__main__":
    h = CSS + schema() + section()
    print("%d onglets, %d octets" % (len(MODULES), len(h)))
    print("  puces par onglet :", [len(m[3]) for m in MODULES])
