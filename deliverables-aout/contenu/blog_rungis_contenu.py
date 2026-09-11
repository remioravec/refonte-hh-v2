# -*- coding: utf-8 -*-
"""
Contenu de l'article « MIN de Rungis ».

GRAPPE DE REQUETES — Google Ads, France, francais, moyenne 12 mois arretee en
juillet 2026 :
  marche de rungis .......... 5 400 /mois
  rungis marche ............. 4 400
  min rungis ................ 1 600
  min de rungis ............. 1 600
  grossiste rungis .......... 210
  carte acheteur rungis ..... 170
  min de rungis plan ........ 70
  min rungis prix ........... 50
  acheter a rungis .......... 10
  --------------------------------
  total ..................... 13 510 /mois

RELEVE SERP « min de rungis » DU 11/09/2026 — dix positions, ZERO editeur de
logiciel : site officiel, questions posees, cours FranceAgriMer, Wikipedia,
Indeed (emplois), Facebook, MyRungis, YouTube, videos courtes, fiche Google
(adresse, horaires, 656 avis). Recherches associees : recrutement, prix, plan,
histoire, restaurant.

ANGLE TRANCHE — plus DEMONTRE, et adresse au professionnel. Personne ne publie
les horaires REELS secteur par secteur sous forme lisible, ni ce que le
fonctionnement du carreau impose a la gestion d'un grossiste. C'est la seule
porte d'entree legitime pour un editeur dans cette SERP.

PROMESSE — Le MIN de Rungis vu du cote de celui qui y achete : quand chaque
secteur ouvre, comment on y entre, et ce que le carreau impose a la gestion.

Toutes les donnees ci-dessous viennent du site officiel du marche, releve le
11 septembre 2026. Aucune n'est estimee.
"""

TITLE = "MIN de Rungis : Horaires, Carte Acheteur et Secteurs 2026"           # 526 px
DESC = ("MIN de Rungis : horaires réels par secteur, qui peut y acheter, comment obtenir "
        "la carte acheteur et comment le prix se fixe sur le carreau.")           # 856 px
H1 = "MIN de Rungis : comment y acheter quand on est professionnel"

SOURCE = ("rungisinternational.com, chiffres et horaires relevés le 11 septembre 2026")

CHIFFRES = [
    ("234", "hectares", "la surface du marché"),
    ("1 226", "entreprises", "implantées sur le site"),
    ("12,02", "milliards d'euros", "de chiffre d'affaires en 2024"),
    ("12 000", "salariés", "travaillent sur le marché"),
]

# secteur, jours, debut (heure decimale), fin, couleur
HORAIRES = [
    ("Marée — pavillon A4", "mardi au samedi", 2.0, 6.0, "#0EA5E9"),
    ("Marée — tour de glace", "mardi au samedi", 2.0, 7.0, "#38BDF8"),
    ("Boucherie, porc, triperie", "lundi au vendredi", 3.0, 9.0, "#EF4444"),
    ("Volaille et gibier", "mardi au samedi", 3.0, 9.0, "#F97316"),
    ("Fleurs coupées", "mardi au samedi", 4.0, 11.0, "#EC4899"),
    ("Produits laitiers", "lundi au vendredi", 5.0, 13.0, "#FACC15"),
    ("Gastronomie et pavillon bio", "lundi au vendredi", 5.0, 13.0, "#A855F7"),
    ("Fruits et légumes", "mardi au vendredi", 5.5, 11.0, "#22C55E"),
    ("Plantes en pot, pépiniéristes", "mercredi, vendredi, samedi", 5.0, 12.0, "#14B8A6"),
    ("Accessoires et décoration", "lundi et samedi", 6.5, 13.5, "#94A3B8"),
    ("Tour administrative", "lundi au vendredi", 6.0, 20.0, "#CBD5E1"),
]

CARTE = [
    ("Justifier d'une activité professionnelle",
     "Extrait Kbis, numéro de TVA intracommunautaire ou équivalent. Le marché est fermé "
     "aux particuliers en dehors des visites organisées."),
    ("Créer son compte acheteur en ligne",
     "Les pièces se déposent sur l'espace client du marché, qui instruit la demande."),
    ("Recevoir sa carte et son badge d'accès",
     "La carte conditionne l'entrée sur le site et l'accès aux pavillons."),
    ("Payer le droit d'entrée à chaque passage",
     "Le tarif dépend du véhicule et de la fréquence. Un abonnement existe pour les "
     "acheteurs réguliers."),
]

FLUX = [
    ("Le carreau", "Vous achetez au poids affiché sur le lot, au prix du matin."),
    ("Le chargement", "Le poids réel du colis diffère du poids commandé. L'écart commence ici."),
    ("Le retour", "La marchandise entre en stock avec sa DLC et son numéro de lot."),
    ("La préparation", "Vous préparez à l'unité de vente de votre client, pas à celle d'achat."),
    ("La facture", "Vous facturez le poids réellement pesé — ou vous perdez la différence."),
]

FAQ = [
    ("C'est quoi le MIN de Rungis ?",
     "Le MIN de Rungis est le marché d'intérêt national qui approvisionne l'Île-de-France en "
     "produits frais. Il s'étend sur <strong>234 hectares</strong> à cheval sur les communes "
     "de Rungis et de Chevilly-Larue, accueille <strong>1 226 entreprises</strong> et "
     "<strong>12 000 salariés</strong>, pour un chiffre d'affaires de "
     "<strong>12,02 milliards d'euros en 2024</strong>. Il a ouvert en 1969, en remplacement "
     "des halles de Paris."),
    ("Qui est propriétaire du MIN de Rungis ?",
     "Le marché est exploité par la Semmaris, une société d'économie mixte. Un marché "
     "d'intérêt national est un service public de gestion de marché au sens des articles "
     "L761-1 à L761-11 du Code de commerce : la puissance publique en fixe le cadre, une "
     "société en assure l'exploitation."),
    ("Qui peut acheter au MIN de Rungis ?",
     "Uniquement les professionnels : commerçants de détail, métiers de bouche, "
     "restaurateurs, traiteurs, collectivités et grossistes. L'entrée suppose une carte "
     "d'acheteur, délivrée sur justificatif d'activité. Les particuliers n'y font pas leurs "
     "courses, mais peuvent participer aux visites organisées."),
    ("À quelle heure ouvre le MIN de Rungis ?",
     "Cela dépend du secteur. La marée ouvre à <strong>2 h</strong>, la boucherie et la "
     "volaille à <strong>3 h</strong>, les fleurs coupées à <strong>4 h</strong>, les "
     "produits laitiers et la gastronomie à <strong>5 h</strong>, les fruits et légumes à "
     "<strong>5 h 30</strong>. Les jours d'ouverture varient aussi : la marée et la volaille "
     "fonctionnent du mardi au samedi, la boucherie du lundi au vendredi."),
]
