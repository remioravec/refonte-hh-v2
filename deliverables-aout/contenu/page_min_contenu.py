# -*- coding: utf-8 -*-
"""
Page « MIN » sur le gabarit des PAGES — /negoce/marches-interet-national/.

4.1 BRIEF
---------
REQUETES VISEES — la grappe « MIN + localite », 5 270 recherches par mois.
Google Ads, France, francais, moyenne 12 mois arretee en juillet 2026 :
  min de rungis 1 600 · min de nantes 1 600 · min de rouen 480 ·
  min de toulouse 260 · min de montpellier 210 · min de nice 210 ·
  min de grenoble 170 · min de cavaillon 170 · min de chateaurenard 140 ·
  min de bordeaux 110 · min de marseille 110 · min de strasbourg 50 ·
  min de lyon 40 · min d'avignon 40 · min d'angers 40 · min d'agen 40

ANTI-CANNIBALISATION — verdict MODERE. /blog/min/ (post 5274) capte deja
« marche d'interet national », la requete de DEFINITION, en 10e position
organique et 14e a l'ecran. Les deux pages ne portent donc pas la meme chose :
  · /blog/min/ ................ la definition, le statut, l'histoire — TOFU
  · cette page ................ les marches un par un et ce que le carreau
                                impose a la gestion — MOFU, adressee au pro
Elles se lient l'une a l'autre. Aucune des deux ne reprend le title de l'autre.

SERP « min de <ville> » RELEVEE LE 11/09/2026 — sur « min de rungis » comme sur
« min de nantes », dix positions : site officiel du marche, questions posees,
cours FranceAgriMer, Wikipedia, offres d'emploi, reseaux sociaux, fiche Google.
ZERO editeur de logiciel. La page ne prendra pas la premiere place sur le nom
d'un marche — le site officiel est imprenable — mais la SERP n'a AUCUNE reponse
pour « je travaille sur un MIN, comment je gere ».

ANGLE TRANCHE — plus demontre, et adresse au professionnel : les dix-sept
marches dans un tableau exploitable, puis les trois contraintes que le carreau
impose a la gestion, chiffrees. C'est la seule porte d'entree d'un editeur.

PROMESSE — Les 17 MIN de France, et ce que travailler sur un carreau impose a
votre gestion.

PLAN DE LIENS — la page est une FILLE de /negoce/.
  · lien mere dans les 100 premiers mots : « ERP negoce alimentaire » → /negoce/
  · vers les soeurs : achats, ventes, stocks multi-depots, tracabilite des lots,
    tarifs et EDI
  · vers le guide : « marche d'interet national » → /blog/min/
  · vers les metiers : fruits et legumes, poissonnier
  · entrants a poser : /negoce/ et les cinq soeurs, plus /blog/min/

SIGNAL GA4 DECLARE — interaction avec le tableau des 17 MIN (tri ou filtre) et
avec le calculateur d'ecart de poids.
"""

SLUG = "/negoce/marches-interet-national/"
TITLE = "MIN : les 17 Marchés d'Intérêt National et leur Gestion"
DESC = ("Les 17 MIN de France dans un tableau triable, et ce que le carreau impose à "
        "la gestion d'un grossiste : poids réellement pesé, DLC du lot, stocks éclatés.")
H1 = "MIN : les 17 marchés d'intérêt national, et ce qu'ils imposent à votre gestion"
# La page est la MERE d'un silo de 17 filles, une par marche :
#   /negoce/marches-interet-national/rungis/  … /agen/
# Chaque fille reprendra la fiche de sa mere, l'enrichira de ses horaires, de
# ses secteurs et de ses grossistes, et pointera vers la mere en retour.
CHAPO = ("Rungis, Nantes, Rouen, Toulouse : dix-sept marchés d'intérêt national "
         "approvisionnent la France en produits frais. Voici où ils sont, et les trois "
         "contraintes que le travail sur un carreau impose à la gestion d'un grossiste.")

SOURCE = "rungisinternational.com et sites officiels des marchés, relevés le 11 septembre 2026"

PHOTOS = {
    "hero": ("min-carreau-cagettes-palettes.webp",
             "Cagettes de fruits empilées sur palettes sur le carreau d'un marché de gros"),
    "pesee": ("min-pesee-balance-poids-variable.webp",
              "Main d'un opérateur sur une balance de pesée dans un entrepôt de produits frais"),
    "stock": ("min-chariot-palettes-chambre-froide.webp",
              "Chariot élévateur déplaçant des palettes de cartons dans un entrepôt frigorifique"),
}

# Les trois contraintes du carreau, avec ce qu'elles cassent et la reponse.
CONTRAINTES = [
    ("Le poids", "Vous achetez au kilo pesé, vous facturez au colis annoncé.",
     "L'écart part en marge à chaque ligne."),
    ("La date", "Les DLC sont courtes, parfois trois jours après l'arrivage.",
     "Un lot prélevé dans le mauvais ordre finit en perte."),
    ("Le lieu", "La marchandise est sur le carreau, en chambre froide et déjà chargée.",
     "Le stock théorique n'est jamais le stock réel."),
]

FLUX = [
    ("Le carreau", "Achat au poids affiché sur le lot, au prix du matin."),
    ("Le chargement", "Le poids réel du colis diffère du poids commandé."),
    ("La réception", "Entrée en stock avec DLC et numéro de lot."),
    ("La préparation", "Préparation à l'unité de vente du client, pas à celle d'achat."),
    ("La facture", "Facturation au poids réellement pesé — ou perte de la différence."),
]

# Chronologie d'un lot a DLC courte, du carreau au client.
DLC = [
    ("J", "Arrivage sur le carreau", "Le lot entre avec sa DLC fournisseur."),
    ("J", "Réception en chambre froide", "Le numéro de lot et la DLC suivent la palette."),
    ("J+1", "Prélèvement au plus près de la date", "Le FEFO sort d'abord ce qui périme le plus tôt."),
    ("J+2", "Préparation et chargement", "Le lot part rattaché à sa commande et à son client."),
    ("J+3", "DLC atteinte", "Ce qui reste est une perte — sauf si l'alerte est tombée avant."),
]

FAQ = [
    ("Qu'est-ce qu'un MIN ?",
     "MIN est l'abréviation de marché d'intérêt national : un marché de gros auquel les "
     "pouvoirs publics ont accordé un statut particulier, défini par les articles L761-1 à "
     "L761-11 du Code de commerce. La France en compte <strong>17 en activité</strong>."),
    ("Quels sont les MIN en France ?",
     "Rungis, Nantes, Rouen, Toulouse, Montpellier, Nice — alimentaire et fleurs —, "
     "Grenoble, Cavaillon, Châteaurenard, Bordeaux, Marseille, Strasbourg, Lyon, Avignon, "
     "Angers et Agen. Le tableau plus haut donne pour chacun sa commune réelle, qui n'est "
     "pas toujours celle du nom : le MIN de Nantes est à Rezé, celui de Lyon à Corbas."),
    ("Qui peut acheter dans un MIN ?",
     "Uniquement les professionnels : commerçants de détail, métiers de bouche, "
     "restaurateurs, traiteurs, collectivités et grossistes. L'entrée suppose une carte "
     "d'acheteur délivrée sur justificatif d'activité."),
    ("Quel logiciel pour un grossiste qui travaille sur un MIN ?",
     "Il faut un outil qui facture au poids réellement pesé et non au poids commandé, qui "
     "suive la DLC du lot et non la date du produit, et qui réconcilie un stock éclaté entre "
     "le carreau, la chambre froide et le camion. C'est ce que couvre un ERP de négoce "
     "alimentaire, et ce qu'un logiciel de facturation généraliste ne sait pas faire."),
]
