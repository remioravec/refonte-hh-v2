#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quatre ecrans de plus, pour couvrir les cartes que la bibliotheque ignorait.

Les dix-neuf ecrans existants couvrent la tracabilite, les dates limites, le
cout de revient, les stocks, l'HACCP, l'achat, l'agreage, la preparation, la
tournee, la facture et la marge. Il manquait quatre familles qui reviennent
dans les bentos des pages fonctionnalites et des fiches metier : la relation
client, les echanges EDI, la planification de production et le multi-site.

Memes briques que le reste du parc : agro_ui fournit la fenetre, le menu, les
tableaux et les cartes. Rien de neuf cote style.
"""

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import agro_ui as UI                        # noqa: E402


def _top(actif, items=None):
    items = items or ["Achats", "Ventes", "Stock", "Production", "Comptabilité"]
    nav = "".join('<span%s>%s</span>' % (' class="on"' if i == actif else '', i)
                  for i in items)
    return ('<div class="ui-top"><span class="ui-logo">' + UI._nuage() + 'Hello Harel</span>'
            '<span class="ui-nav">' + nav + '</span>'
            '<span class="ui-me">Paul Dupont ▾</span></div>')


def _boxes(trois):
    return ('<div class="ui-boxes">' + "".join(
        '<span class="ui-box"><i style="background:%s">%s</i>'
        '<div><b>%s</b>%s</div></span>' % t for t in trois) + '</div>')


# ------------------------------------------------------------ relation client
def ecran_clients():
    corps = (
        _top("Ventes") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Clients", "Contacts", "Opportunités",
                    "Encours", "Relances"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Fiche client — 0021, Grossiste Ouest</span><em>⎙</em></div>'
        + _boxes([("#275E80", "18", "mois de relation", "Depuis mars 2025"),
                  ("#0F7A45", "312", "k€ facturés", "Sur douze mois glissants"),
                  ("#B45309", "14", "jours de retard", "Encours moyen de paiement")])
        + '<div class="ui-grid one">'
        + UI._card("Dernières commandes",
                   UI._tab(["Commande", "Date", "^Lignes", "^Montant HT", "État"],
                           [["@CDE/2609-118", "10/09/2026", "^4", "^499,49 €",
                             '<span class="ui-pill a">Livrée</span>'],
                            ["~@CDE/2609-102", "08/09/2026", "^7", "^1 284,10 €",
                             '<span class="ui-pill a">Livrée</span>'],
                            ["@CDE/2609-081", "05/09/2026", "^3", "^318,00 €",
                             '<span class="ui-pill c">Facturée</span>'],
                            ["!@CDE/2608-944", "28/08/2026", "^9", "^2 106,75 €",
                             '<span class="ui-pill b">Impayée</span>']]))
        + UI._card("Conditions négociées",
                   UI._tab(["Famille", "Remise", "Franco", "Délai"],
                           [["Fruits et légumes", "−6 %", "350 €", "30 j fin de mois"],
                            ["~Marée", "−4 %", "350 €", "30 j fin de mois"],
                            ["Boucherie", "−3 %", "500 €", "45 j"]]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Fiche client de Hello Harel : l'historique des commandes "
        "d'un grossiste, son encours et ses conditions tarifaires négociées",
        corps, "Hello Harel — Relation client",
        "Les conditions négociées s'appliquent seules à la saisie de commande. "
        "Données de démonstration.")


# ------------------------------------------------------------- echanges EDI
def ecran_edi():
    corps = (
        _top("Ventes") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Partenaires", "Flux EDI", "Messages",
                    "Anomalies", "Journal"], 2)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Flux EDI — journée du 10/09</span><em>⎙</em></div>'
        + _boxes([("#0F7A45", "146", "messages reçus", "Commandes et avis d'expédition"),
                  ("#275E80", "138", "intégrés", "Sans intervention"),
                  ("#C0392B", "8", "en anomalie", "À reprendre à la main")])
        + '<div class="ui-grid one">'
        + UI._card("Derniers messages",
                   UI._tab(["Partenaire", "Type", "Référence", "Heure", "État"],
                           [["@0021 — Grossiste Ouest", "ORDERS", "@CDE/2609-118", "05 h 12",
                             '<span class="ui-pill a">Intégré</span>'],
                            ["~@0008 — Enseigne régionale", "DESADV", "@BL/2609-341", "06 h 40",
                             '<span class="ui-pill a">Intégré</span>'],
                            ["@0034 — Traiteur Le Verger", "INVOIC", "@FA/2609-341", "07 h 05",
                             '<span class="ui-pill a">Envoyé</span>'],
                            ["!@0011 — Centrale Sud", "ORDERS", "@—", "07 h 22",
                             '<span class="ui-pill b">Code article inconnu</span>']]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Flux EDI de Hello Harel : les messages échangés avec les "
        "partenaires dans la journée, et ceux qui restent en anomalie",
        corps, "Hello Harel — EDI",
        "Seules les huit anomalies demandent une reprise : le reste s'intègre seul. "
        "Données de démonstration.")


# ------------------------------------------------- planification de production
def ecran_production():
    corps = (
        _top("Production") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Plan de production", "Ordres de fabrication",
                    "Recettes", "Besoins matière", "Rendements"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Plan de production — jeudi 10/09</span><em>+ ⎙</em></div>'
        + _boxes([("#275E80", "12", "ordres du jour", "Dont 3 en série longue"),
                  ("#0F7A45", "94", "% de charge", "Sur l'atelier principal"),
                  ("#B45309", "2", "manquants", "Matières à commander")])
        + '<div class="ui-grid one">'
        + UI._card("Ce qui se fabrique aujourd'hui",
                   UI._tab(["Ordre", "Produit", "^Quantité", "Créneau", "Matière", "État"],
                           [["@OF-2609-041", "Terrine de campagne", "^120 kg",
                             "05 h – 08 h", "Complète",
                             '<span class="ui-pill a">Lancé</span>'],
                            ["~@OF-2609-042", "Rillettes nature", "^80 kg",
                             "08 h – 10 h", "Complète",
                             '<span class="ui-pill a">Lancé</span>'],
                            ["!@OF-2609-043", "Pâté en croûte", "^45 kg",
                             "10 h – 13 h", "Manque 8 kg",
                             '<span class="ui-pill b">Bloqué</span>'],
                            ["@OF-2609-044", "Saucisson à cuire", "^60 kg",
                             "13 h – 15 h", "Complète",
                             '<span class="ui-pill c">À lancer</span>']]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Plan de production de Hello Harel : les ordres de fabrication "
        "du jour, leur créneau, la disponibilité matière et leur état",
        corps, "Hello Harel — Production",
        "Le besoin matière est calculé depuis les recettes : l'ordre bloqué l'est avant "
        "d'être lancé. Données de démonstration.")


# ------------------------------------------------------------------ multi-site
def ecran_sites():
    corps = (
        _top("Stock") + '<div class="ui-body">'
        + UI._side(["Tableau de bord", "Tous les sites", "Transferts", "Réassort",
                    "Inventaires", "Emplacements"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Stock consolidé — quatre sites</span><em>⎙</em></div>'
        + _boxes([("#275E80", "4", "sites", "Entrepôt, deux dépôts, un carreau"),
                  ("#0F7A45", "312", "références", "Vue consolidée"),
                  ("#B45309", "7", "à réassortir", "Sous le seuil sur un site")])
        + '<div class="ui-grid one">'
        + UI._card("Répartition par site",
                   UI._tab(["Produit", "^Entrepôt", "^Dépôt Nord", "^Dépôt Sud",
                            "^Carreau", "^Total"],
                           [["@0142 — Terrine de campagne", "^186 kg", "^42 kg",
                             "^0 kg", "^12 kg", "^240 kg"],
                            ["~@0004 — Épaule de porc", "^320 kg", "^88 kg",
                             "^64 kg", "^0 kg", "^472 kg"],
                            ["!@0016 — Carottes râpées", "^12 kg", "^0 kg",
                             "^4 kg", "^0 kg", "^16 kg"],
                            ["@0088 — Crème UHT 35 %", "^240 L", "^60 L",
                             "^60 L", "^0 L", "^360 L"]]))
        + '</div></div></div>')
    return UI._fig(
        "Reproduction de l'écran Stock consolidé de Hello Harel : la répartition de quatre "
        "produits entre l'entrepôt, deux dépôts et le carreau",
        corps, "Hello Harel — Multi-sites",
        "La ligne rouge est sous le seuil sur un site alors que le total semble suffisant. "
        "Données de démonstration.")
