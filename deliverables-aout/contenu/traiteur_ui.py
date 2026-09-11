# -*- coding: utf-8 -*-
"""
Les cinq fonctionnalites de la page traiteur, avec leur ecran du logiciel.

CONSTAT DU 11/09/2026 : la section fonctionnalites de /agroalimentaire/traiteur/
n'est pas celle d'un traiteur. L'overline dit « ERP Charcutier », le titre dit
« L'ERP concu pour la charcuterie », et les cinq cartes parlent de numeros
veterinaires, de dates d'abattage, de poids apres cuisson et de pertes au
tranchage. C'est le bloc charcutier repris tel quel, sans meme renommer les
titres. Meme cause que sur glacier et negoce : un gabarit d'un autre metier.

Le contenu ci-dessous est celui du metier : la fiche technique au gramme par
convive, le devis d'evenement, le cout au couvert, les quatorze allergenes et
le chargement par tournee.

Le kit graphique — palette, briques, CSS — est celui de agro_ui : une seule
mise en forme pour tout le parc.
"""

from agro_ui import CSS, _check, _card, _fig, _leg, _ring, _side, _tab, _nuage  # noqa: F401
import agro_ui


def _top(actif):
    items = ["Produits", "Production", "Vente", "Qualité", "Comptabilité"]
    nav = "".join('<span%s>%s</span>' % (' class="on"' if i == actif else '', i) for i in items)
    return ('<div class="ui-top"><span class="ui-logo">' + _nuage() + 'Hello Harel</span>'
            '<span class="ui-nav">' + nav + '</span>'
            '<span class="ui-me">Paul Dupont ▾</span></div>')


# -------------------------------------------------------------------- ecrans
def ecran_fiches():
    corps = (
        _top("Production") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Fiches techniques", "Recettes", "Nomenclatures",
                 "Ordres de fabrication", "Rendements"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Fiche technique — Cocktail dînatoire 120 couverts</span><em>+ ⎙</em></div>'
        '<div class="ui-grid one">'
        + _card("Composants et grammages",
                _tab(["Composant", "Unité", "^Par couvert", "^Pour 120", "^Coût unitaire", "^Total"],
                     [["@0212 — Mini-burger effiloché", "pièce", "^3", "^360", "^0,62 €", "^223,20 €"],
                      ["~@0218 — Verrine saumon aneth", "pièce", "^2", "^240", "^0,84 €", "^201,60 €"],
                      ["@0231 — Wrap végétarien", "pièce", "^2", "^240", "^0,51 €", "^122,40 €"],
                      ["~@0407 — Plateau fromages affinés", "kg", "^0,06", "^7,2 kg", "^18,40 €", "^132,48 €"],
                      ["@0512 — Mignardises assorties", "pièce", "^3", "^360", "^0,38 €", "^136,80 €"]]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Fiche technique de Hello Harel : les composants d'un cocktail "
        "dînatoire, leur grammage par couvert et le total pour 120 convives",
        corps, "Hello Harel — Fiche technique",
        "Le grammage est saisi par couvert. Changez le nombre de convives, tout se recalcule. "
        "Données de démonstration.")


def ecran_evenements():
    corps = (
        _top("Vente") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Devis", "Commandes", "Événements", "Préparations",
                 "Livraisons", "Journal des ventes"], 3)
        + '<div class="ui-main"><div class="ui-h"><span>Événements — semaine 38</span>'
        '<em>+ ⎙</em></div><div class="ui-grid one">'
        + _card("Prestations programmées",
                _tab(["Événement", "Date", "Client", "^Couverts", "^Montant HT", "Statut"],
                     [["@EVT/2609-041", "19/09/2026", "@Mairie de Vaucresson", "^120", "^2 640,00 €",
                       '<span class="ui-pill a">Confirmé</span>'],
                      ["~@EVT/2609-044", "20/09/2026", "@Groupe Lafarge", "^260", "^7 150,00 €",
                       '<span class="ui-pill a">Confirmé</span>'],
                      ["!@EVT/2609-047", "21/09/2026", "@Mariage Berthier", "^85", "^3 315,00 €",
                       '<span class="ui-pill b">Devis en attente</span>'],
                      ["@EVT/2609-052", "24/09/2026", "@Clinique du Parc", "^45", "^810,00 €",
                       '<span class="ui-pill c">Option posée</span>']]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Événements de Hello Harel : quatre prestations d'une même "
        "semaine avec leur date, leur nombre de couverts, leur montant et leur statut",
        corps, "Hello Harel — Événements",
        "Le devis, la commande et la prestation sont le même objet, suivi par date. "
        "Données de démonstration.")


def ecran_cout():
    corps = (
        _top("Comptabilité") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Coût de revient", "Marges", "Facturation",
                 "Règlements", "Journal"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Coût au couvert — EVT/2609-041</span><em>⎙</em></div>'
        '<div class="ui-grid one">'
        + _card("Décomposition du coût d'un couvert",
                '<span class="ui-donut">'
                + _ring([("#FA8F92", 54), ("#3C8DBC", 27), ("#FFDDA8", 11), ("#3ECF8E", 8)])
                + _leg([("#FA8F92", "Matières et denrées", "6,81 €", "54 %"),
                        ("#3C8DBC", "Personnel de production et de service", "3,40 €", "27 %"),
                        ("#FFDDA8", "Location de matériel et vaisselle", "1,39 €", "11 %"),
                        ("#3ECF8E", "Transport et logistique", "1,01 €", "8 %")])
                + '</span>')
        + _card("Marge par prestation",
                _tab(["Événement", "^Couverts", "^Revient/couvert", "^Vendu/couvert", "^Marge", "Statut"],
                     [["@EVT/2609-041", "^120", "^12,61 €", "^22,00 €", "^42,7 %",
                       '<span class="ui-pill a">Dans la cible</span>'],
                      ["~@EVT/2609-044", "^260", "^17,04 €", "^27,50 €", "^38,0 %",
                       '<span class="ui-pill a">Dans la cible</span>'],
                      ["!@EVT/2609-047", "^85", "^32,10 €", "^39,00 €", "^17,7 %",
                       '<span class="ui-pill b">Sous le seuil</span>']]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Coût au couvert de Hello Harel : décomposition du coût d'un "
        "couvert en quatre postes et marge de trois prestations dont une sous le seuil",
        corps, "Hello Harel — Coût au couvert",
        "La marge se lit prestation par prestation, avant la facture et non après. "
        "Données de démonstration.")


def ecran_allergenes():
    corps = (
        _top("Qualité") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Allergènes", "Étiquetage INCO", "Contrôles",
                 "Non-conformités", "Rappels"], 1)
        + '<div class="ui-main"><div class="ui-h">'
        '<span>Allergènes — Cocktail dînatoire 120 couverts</span><em>⎙</em></div>'
        '<div class="ui-grid one">'
        + _card("Déclaration remontée des matières premières",
                _tab(["Recette", "Allergène", "Origine", "Présence", "Étiquette"],
                     [["@0212 — Mini-burger effiloché", "Gluten", "@Pain brioché — lot F-90211",
                       "Ingrédient", '<span class="ui-pill b">À déclarer</span>'],
                      ["~@0218 — Verrine saumon aneth", "Poisson", "@Saumon fumé — lot F-88417",
                       "Ingrédient", '<span class="ui-pill b">À déclarer</span>'],
                      ["@0218 — Verrine saumon aneth", "Lait", "@Crème épaisse — lot F-88602",
                       "Ingrédient", '<span class="ui-pill b">À déclarer</span>'],
                      ["~@0231 — Wrap végétarien", "Fruits à coque", "@Atelier partagé",
                       "Traces possibles", '<span class="ui-pill c">Mention traces</span>'],
                      ["@0512 — Mignardises assorties", "Œuf", "@Appareil à génoise — lot F-91004",
                       "Ingrédient", '<span class="ui-pill b">À déclarer</span>']]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Allergènes de Hello Harel : cinq recettes d'un même menu, "
        "l'allergène détecté, le lot de matière première d'où il vient et la mention à porter",
        corps, "Hello Harel — Allergènes",
        "L'allergène remonte du lot de matière première, il n'est pas ressaisi à la main. "
        "Données de démonstration.")


def ecran_logistique():
    corps = (
        '<div class="ui-modal">'
        '<p>Chargement de la tournée<em>Vendredi 19/09 — camion 2</em></p>'
        '<div class="ui-warn">Deux prestations partent du même camion : '
        'le chargement suit l\'ordre inverse des livraisons.</div>'
        + _tab(["Ordre", "Événement", "Client", "Heure sur place", "^Bacs", "Température"],
               [["3", "@EVT/2609-052", "Clinique du Parc", "18 h 30", "^6", "0 à 4 °C"],
                ["~2", "@EVT/2609-044", "Groupe Lafarge", "12 h 00", "^24", "0 à 4 °C"],
                ["1", "@EVT/2609-041", "Mairie de Vaucresson", "09 h 45", "^11", "0 à 4 °C"]])
        + '<div class="ui-opts">'
        '<span><i class="on"></i>Éditer les bons de livraison et les étiquettes de bac dans '
        'l\'ordre de chargement</span>'
        '<span><i></i>Éditer dans l\'ordre de préparation</span>'
        '</div>'
        '<div class="ui-acts"><span class="ui-btn">Annuler</span>'
        '<span class="ui-btn pr">Éditer ➜</span></div>'
        '</div>')
    return _fig(
        "Reproduction de l'écran Chargement de tournée de Hello Harel : trois prestations d'une "
        "même journée chargées dans l'ordre inverse des livraisons",
        corps, "Hello Harel — Logistique",
        "Le dernier livré est chargé en premier. C'est une règle de camion, pas de tableur. "
        "Données de démonstration.")


# ------------------------------------------------------------------- montage
COURTS = ["Fiches techniques", "Devis et événements", "Coût au couvert",
          "Allergènes et INCO", "Chargement et livraison"]

BLOCS = [
    ("Fiches techniques et grammages",
     "La recette se saisit au gramme par convive. Passez de 85 à 260 couverts et tout se "
     "recalcule : les quantités, les achats à lancer et le coût de la prestation.",
     ["Grammage par couvert, décliné par nombre de convives",
      "Coût de la fiche technique mis à jour au prix d'achat réel",
      "Besoins d'achat déduits des événements confirmés"],
     ecran_fiches),

    ("Devis, commandes et événements",
     "Le devis, la commande et la prestation sont le même objet, suivi par date d'événement. "
     "Vous voyez la semaine qui arrive avec ses couverts, ses montants et ce qui n'est pas "
     "encore confirmé.",
     ["Planning par date de prestation, pas par date de commande",
      "Options, devis en attente et confirmations distingués",
      "Relance automatique des devis sans réponse"],
     ecran_evenements),

    ("Coût de revient au couvert",
     "Denrées, personnel, location de matériel, transport : le coût d'un couvert se décompose "
     "poste par poste. La marge de chaque prestation se lit avant de facturer, pas au bilan.",
     ["Coût au couvert et à la prestation",
      "Personnel de production et de service intégrés au calcul",
      "Marge comparée à votre seuil, événement par événement"],
     ecran_cout),

    ("Allergènes et étiquetage INCO",
     "Les quatorze allergènes remontent des lots de matières premières jusqu'à la recette et "
     "jusqu'au menu remis au client. Vous ne les ressaisissez pas, et vous ne les oubliez pas.",
     ["Remontée automatique depuis le lot fournisseur",
      "Distinction ingrédient et traces possibles",
      "Menu client et étiquettes générés depuis la même source"],
     ecran_allergenes),

    ("Production, chargement et livraison",
     "Le planning de production se cale sur les dates d'événement, et le camion se charge dans "
     "l'ordre inverse des livraisons. Les bons et les étiquettes de bac sortent dans cet ordre-là.",
     ["Planning de production par date de prestation",
      "Ordre de chargement inverse de l'ordre de livraison",
      "Bons de livraison et étiquettes de bac édités ensemble"],
     ecran_logistique),
]


def section(entete):
    return agro_ui.section(entete, BLOCS, COURTS)
