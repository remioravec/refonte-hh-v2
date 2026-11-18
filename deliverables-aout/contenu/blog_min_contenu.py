# -*- coding: utf-8 -*-
"""
Contenu de /blog/min/ — requete « marche d'interet national ».

RELEVE SERP DU 11/09/2026, France, francais
  1  Wikipedia — definition + liste en prose
  2  Questions posees (4), au-dessus du 2e organique
  3  Legifrance — articles L761-1 a L761-11
  4-6 trois fiches locales de MIN (Rouen, Toulouse, Bordeaux)
  7  Akanea — glossaire agroalimentaire : le seul editeur d'ERP de la page
  8  Le Courrier des maires · 9 et 11 Grenoble · 10 FoodBiome · 12 MIN Bordeaux
  13 Cairn · 14 helloharel.com/blog/min/
  + 3 autres fiches locales, et « Marche d'interet national liste » en
    PREMIERE recherche associee.

TROIS CONSTATS CHIFFRES
  1. Six fiches locales dans la page : la SERP est a moitie locale. Hello Harel
     est 10e organique mais 14e a l'ecran — c'est rank_absolute qu'on lit.
  2. Les deux premieres positions donnent la definition ; AUCUNE ne donne la
     liste sous une forme exploitable. Wikipedia la livre en prose.
  3. La premiere recherche associee est « Marche d'interet national liste ».
     La demande est explicite et personne ne la sert.

ANGLE TRANCHE — plus demontre : la liste des 17 MIN, triable, avec une colonne
que personne d'autre ne publie, le volume de recherche mensuel de chaque
marche, et les cinq declassements dates.

PROMESSE — Les 17 marches d'interet national de France, leur ville, leur
statut et ce qu'on y achete, dans un tableau.

CANNIBALISATION — verdict FORT : /blog/min/ (post 5274) capte deja la requete.
On met a jour cette page, on n'en cree pas une seconde.

TOFU — page de definition. Un seul lien contextuel vers l'offre, dans une
phrase d'usage. Pas d'offre commerciale dans le corps.
"""

TITLE = "Marché d'Intérêt National : les 17 MIN de France en 2026"          # 509 px
DESC = ("Les 17 marchés d'intérêt national de France, dans un tableau triable : ville, "
        "région, volume. Statut, accès professionnel et les cinq MIN déclassés.")   # 900 px
H1 = "Marché d'intérêt national : les 17 MIN de France"

# ville, commune reelle, region, volume mensuel « min de <ville> », site officiel
# Volumes : Google Ads, France, francais, moyenne 12 mois arretee en juillet 2026.
# Communes et regions : liste Wikipedia du 11/09/2026, recoupee avec les fiches
# Google des marches quand elles existent.
MIN = [
    ("Rungis", "Rungis et Chevilly-Larue (94)", "Île-de-France", 1600,
     "https://www.rungisinternational.com/"),
    ("Nantes", "Rezé (44)", "Pays de la Loire", 1600, "https://www.minnantes.com/"),
    ("Rouen", "Rouen (76)", "Normandie", 480, "http://www.minderouen.fr/"),
    ("Toulouse", "Toulouse (31)", "Occitanie", 260, "http://www.lgm-mintoulouse.com/"),
    ("Montpellier", "Montpellier (34)", "Occitanie", 210, None),
    ("Nice — produits alimentaires", "Nice (06)", "Provence-Alpes-Côte d'Azur", 210, None),
    ("Nice — fleurs", "Nice (06)", "Provence-Alpes-Côte d'Azur", None, None),
    ("Grenoble", "Grenoble (38)", "Auvergne-Rhône-Alpes", 170, "http://www.min-grenoble.fr/"),
    ("Cavaillon", "Cavaillon (84)", "Provence-Alpes-Côte d'Azur", 170, None),
    ("Châteaurenard", "Châteaurenard (13)", "Provence-Alpes-Côte d'Azur", 140, None),
    ("Bordeaux — Brienne", "Bordeaux (33)", "Nouvelle-Aquitaine", 110,
     "https://min-bordeaux-brienne.fr/"),
    ("Marseille", "Marseille (13)", "Provence-Alpes-Côte d'Azur", 110, None),
    ("Strasbourg", "Strasbourg (67)", "Grand Est", 50, None),
    ("Lyon — Corbas", "Corbas (69)", "Auvergne-Rhône-Alpes", 40, None),
    ("Avignon", "Avignon (84)", "Provence-Alpes-Côte d'Azur", 40, None),
    ("Angers", "Angers (49)", "Pays de la Loire", 40, None),
    ("Agen", "Agen (47)", "Nouvelle-Aquitaine", 40, None),
]

DECLASSES = [
    ("Lille", 2019), ("Lyon — Perrache", 2006), ("Nîmes", 1992),
    ("Montauban", 1991), ("Villeneuve-sur-Lot", 1978),
]

SOURCE_LOI = ("Code de commerce, articles L761-1 à L761-11 "
              "(Légifrance, consulté le 11 septembre 2026)")

# Les quatre questions posees, reprises MOT POUR MOT dans la SERP du 11/09.
FAQ = [
    ("Qu'est-ce qu'un marché d'intérêt national ?",
     "Un marché d'intérêt national est un marché de gros auquel les pouvoirs publics ont "
     "accordé un statut particulier. Les articles L761-1 à L761-11 du Code de commerce en "
     "font des <strong>services publics de gestion de marché</strong>, qui offrent à des "
     "grossistes et à des producteurs des services de gestion collective : quais, chambres "
     "froides, contrôle sanitaire, sécurité, gestion des déchets."),
    ("Qu'est-ce qu'un MIN ?",
     "MIN est l'abréviation de marché d'intérêt national. Le premier a ouvert en 1953, le "
     "plus connu est celui de Rungis, ouvert en 1969. La France en compte "
     "<strong>17 en activité</strong> au 11 septembre 2026."),
    ("Qui peut acheter au MIN ?",
     "L'accès est réservé aux professionnels : commerçants de détail, métiers de bouche, "
     "restaurateurs, traiteurs, collectivités, grossistes. Il faut une carte d'acheteur, "
     "délivrée sur présentation d'un justificatif d'activité — extrait Kbis le plus souvent. "
     "Les particuliers n'y achètent pas, sauf lors des visites organisées."),
    ("Quels sont les plus gros MIN de France ?",
     "Rungis est le premier, et se présente comme le plus grand marché de produits frais au "
     "monde. Nantes Métropole se présente comme le premier MIN de région et le deuxième de "
     "France. Sur la recherche Google, Rungis et Nantes concentrent "
     "<strong>61 % du volume</strong> des dix-sept marchés."),
]
