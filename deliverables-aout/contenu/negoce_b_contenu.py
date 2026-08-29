# -*- coding: utf-8 -*-
"""
Contenu des variantes A et B du test negoce — persona dirigeant de PME
grossiste, distributeur food-service ou negociant en produits alimentaires.

Le fond precedent portait l'angle import-export : frais d'approche, conteneur
20 pieds, incoterms, ecart de change, stock sous douane. Le releve du 29/08/2026
sur les trois pages qui occupent le champ « negoce alimentaire » — Orisha,
TRADE.EASY, Prismasoft — montre qu'aucune ne parle de conteneurs, d'incoterms ni
de frais d'approche. Le vocabulaire du champ est celui du grossiste : cadencier,
UVC, poids variable, DLC, tournees, televente, EDI et GMS, prefacturation.

A et B partagent ce fichier : c'est ce qui garantit qu'une seule variable
distingue les deux variantes, l'UX.

Fait date et source unique : Code de commerce, articles L441-10 et L441-11
(Legifrance), delais maximaux de paiement en produits alimentaires.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from negoce_contenu import SOURCE, DELAIS, FAQ, CALC  # noqa: F401  (fond commun)

BADGE = "ERP Négoce Alimentaire"

H1_MOTS = ["Vous", "achetez", "au", "kilo.", "Vous", "facturez", "à", "l'unité.",
           "<em>C'est&nbsp;là&nbsp;que&nbsp;la&nbsp;marge&nbsp;se&nbsp;perd.</em>"]

HERO_TICKS = [
    "Facturez au <b>poids réellement pesé</b>, pas au poids commandé",
    "Distinguez le stock <b>réservé, disponible et en préparation</b>, dépôt par dépôt",
    "Sortez par lot la <b>DLC</b> et la liste des clients livrés",
    "Appliquez l'<b>échéance légale</b> propre à chaque produit alimentaire",
]

HERO_REASSURE = ("Édité en France depuis 2014, spécialisé agroalimentaire. "
                 "Démonstration de 30 minutes, sans engagement.")

PREUVE = ("Rejoignez les <b>+200 entreprises agroalimentaires</b> qui pilotent leurs "
          "opérations avec Hello Harel")

STATS = [
    ("200+",     "entreprises agroalimentaires équipées"),
    ("5,0/5",    "sur 31 avis clients"),
    ("2014",     "édité en France depuis"),
    ("4–8 sem.", "du cadrage à la bascule"),
]

ICONES = {
 "euro": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8V7m0 1v8m0 0v1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
 "boite": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>',
 "cmd": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>',
 "graph": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m4 10v-6m4 6V9M5 21h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z"/>',
}

ONGLETS = [
    {
        "cle": "achats", "onglet": "Achats et cours du jour", "icone": "euro", "img": "cout",
        "h2": "Le prix d'achat bouge plus vite que votre tarif",
        "ticks": [
            "Achat <b>au cours du jour</b> enregistré à la réception : le coût de revient suit le "
            "marché, il n'est pas figé au tarif catalogue",
            "<b>Grilles tarifaires par canal</b> — RHF, GMS, détail, collectivités — et conditions "
            "particulières par client, dans une base unique",
            "<b>Marge en temps réel</b>, référence par référence et client par client",
            "<b>Alerte sur les lignes vendues sous le seuil</b> que vous fixez, avant l'édition de "
            "la facture",
            "Hausse fournisseur <b>simulée sur la gamme</b> avant d'être appliquée",
        ],
        "lien": ("/negoce/achats-approvisionnements/", "Voir les achats et approvisionnements"),
    },
    {
        "cle": "stock", "onglet": "Stock, dépôts et DLC", "icone": "boite", "img": "stock",
        "h2": "Un stock, ce n'est pas un chiffre : c'est un emplacement, une température et une date",
        "ticks": [
            "<b>Un stock par emplacement</b>, avec sa température : plateforme, chambres positives "
            "et négatives, dépôt avancé",
            "<b>Réservé, disponible, en préparation</b> : trois états distincts, pour ne pas "
            "engager deux fois la même palette",
            "<b>Transferts inter-dépôts tracés</b> : un colis qui change de site garde son lot et "
            "sa DLC",
            "Rotation en <b>premier périmé, premier sorti</b>, avec alerte avant péremption",
            "Stock <b>en poids et en colis</b> à la fois : vous achetez au kilo, vous préparez à "
            "l'unité de vente",
        ],
        "lien": ("/negoce/stocks-multi-depots/", "Découvrir les stocks multi-dépôts"),
    },
    {
        "cle": "cmd", "onglet": "Commandes, tournées et EDI", "icone": "cmd", "img": "cmd",
        "h2": "Quatre canaux de commande, une seule file",
        "ticks": [
            "<b>Cadencier par client</b> à la saisie : le télévendeur ne repart pas d'une page "
            "blanche",
            "<b>Télévente assistée</b> : manquants, substitutions et promotions proposés pendant "
            "l'appel, pas après",
            "<b>EDI</b> pour les comptes qui l'imposent, saisie assistée pour les autres — même "
            "flux, même stock",
            "<b>Préparation par tournée</b>, avec l'ordre de chargement inverse de l'ordre de "
            "livraison",
            "<b>Bon de livraison au poids réel</b>, signé sur terminal, transformé en facture sans "
            "ressaisie",
        ],
        "lien": ("/negoce/ventes-devis-commandes/", "Voir les ventes, devis et commandes"),
    },
    {
        "cle": "marge", "onglet": "Marge et échéance", "icone": "graph", "img": "marge",
        "h2": "Ce qui reste vraiment, et quand vous l'encaissez",
        "ticks": [
            "Marge lue <b>par référence, par client, par tournée et par commercial</b>",
            "Calculée sur le <b>coût d'achat réel</b> du jour, pas sur un tarif catalogue",
            "<b>Échéance légale appliquée selon la nature du produit</b> — 20 ou 30 jours, et pas "
            "le même point de départ",
            "<b>Reporting par tournée</b> : ce qu'elle a rapporté, ce qu'elle a coûté",
        ],
        "lien": ("/negoce/tarifs-reporting-edi/", "Voir les tarifs, reporting et EDI"),
    },
]

# --------------------------------------------------------------------- calcul
CALC_TITRE = "Sur une ligne pesée, l'écart ne se voit jamais ligne à ligne."
CALC_INTRO = ("Vous achetez au kilo, vous vendez à l'unité de vente consommateur. Si la "
              "facturation part du poids commandé et non du poids réellement pesé, la marge "
              "affichée est fausse — et elle est fausse dans le bon sens, ce qui la rend "
              "invisible jusqu'à la clôture du trimestre.")
CALC_CARTE = "Une unité de vente pesée — exemple"
CALC_LIGNES = [
    ("Prix d'achat", "8,50 €/kg"),
    ("Poids commandé de l'unité", "2,000 kg"),
    ("Poids réellement pesé", "2,060 kg"),
    ("Coût si l'on facture au poids commandé", "17,00 €"),
    ("Coût réel de l'unité", "17,51 €"),
    ("Prix de vente de l'unité", "21,90 €"),
]
CALC_TOTAL = ("Marge réelle", "4,39 € · 20,0 %")
CALC_COEF = ("Marge affichée au poids commandé", "4,90 € · 22,4 %")
CALC_NOTE = ("Exemple à remplacer par vos chiffres. Le calculateur de la page "
             "ERP négoce alimentaire refait ce calcul avec vos valeurs.")
CALC_WARN = [
    "L'écart est de <b>0,51 € par unité</b>. Sur 1 200 unités par mois, cela fait <b>612 € par "
    "mois</b> et <b>7 344 € par an</b> de marge affichée mais jamais encaissée.",
    "Hello Harel facture au poids saisi à la pesée : le bon de pesée, l'étiquette et la facture "
    "sortent de la même donnée, et disent donc la même chose. Il n'y a pas d'avoir à émettre "
    "derrière, et la marge lue est la marge réelle.",
]

# --------------------------------------------------------------------- terrain
TERRAIN_TITRE = "L'outil ne vit pas dans un bureau."
TERRAIN_INTRO = ("Il vit sur le quai, en chambre froide et dans le camion. C'est là qu'il fait "
                 "gagner du temps — ou qu'il en fait perdre.")
TERRAIN = [
    ("À la réception", "Contrôle de température, pesée, affectation du lot et de sa DLC dès le "
                       "quai, sur terminal mobile."),
    ("À la préparation", "Picking en premier périmé premier sorti, poids réel saisi à la pesée, "
                         "étiquette éditée dans la foulée."),
    ("À la livraison", "Bon de livraison au poids réel signé sur terminal, retours et manquants "
                       "constatés et répercutés sur la facture."),
]

# --------------------------------------------------------------------- comparatif
CMP_TITRE = "Tableur, ERP généraliste, ERP métier : trois façons de se tromper de marge."
CMP_INTRO = ("La question n'est pas de savoir lequel gère des articles et des clients — les trois "
             "le font. Elle est de savoir lequel sait qu'un kilo commandé n'est pas un kilo livré, "
             "et qu'un lot n'est pas une référence.")
CMP_COLS = ["Ce que vous cherchez", "Tableur", "ERP généraliste", "Hello Harel"]
CMP_LIGNES = [
    ("Facturer au poids réellement pesé", "ressaisie manuelle", "développement spécifique", "natif"),
    ("Suivre la DLC par lot et non par référence", "non", "non", "natif, avec rotation FEFO"),
    ("Cadencier client et télévente assistée", "non", "partiel", "natif"),
    ("EDI avec la grande distribution", "non", "module en supplément", "natif"),
    ("Stock par dépôt et par température", "non", "partiel", "réservé, disponible, en préparation"),
    ("Échéance légale selon la nature du produit", "non", "30 jours pour tout le monde",
     "par famille de produit"),
    ("Marge par référence, client et tournée", "recalcul manuel", "sur coût estimé",
     "sur coût d'achat réel"),
]

# --------------------------------------------------------------------- modules
MOD_TITRE = "Chaque brique du négoce a sa page."
MODULES = [
    ("01", "m-achats", "/negoce/achats-approvisionnements/", "gérer les achats et approvisionnements",
     "Cadenciers fournisseurs, contrats d'achat, engagements et suivi des arrivages."),
    ("02", "m-stocks", "/negoce/stocks-multi-depots/", "stocks multi-dépôts",
     "Plusieurs entrepôts, chambres froides, marchandise réservée et transferts tracés."),
    ("03", "m-trace", "/negoce/tracabilite-lots/", "traçabilité des lots",
     "Lot d'origine, DLC, certificats et liste des clients livrés en cas de rappel."),
    ("04", "m-ventes", "/negoce/ventes-devis-commandes/", "ventes, devis et commandes",
     "Télévente, cadencier, commandes et bons de livraison au poids réel."),
    ("05", "m-edi", "/negoce/tarifs-reporting-edi/", "tarifs, reporting et EDI",
     "Grilles par canal, échanges EDI avec la GMS et reporting de marge."),
]

# --------------------------------------------------------------------- CTA final
CTA_TITRE = "Voyez-le sur vos propres lignes de commande."
CTA_INTRO = ("30 minutes, sans engagement, avec quelqu'un qui connaît le poids variable, les "
             "cadenciers et les contraintes d'une plateforme de distribution alimentaire. On part "
             "de vos références réelles.")

FAQ_TITRE = "Ce qu'on nous demande avant de choisir."

LOGOS = [
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Logo_Pro-inter_Magasins_Orientaux.webp", "Pro-Inter"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/1.webp", "Leclerc"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.14.24-300x64-1.webp", "Corseprim"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.12.46.webp", "Les Primeurs"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.10.42-300x226-1.webp", "HPS"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.08.48-300x86-1.webp", "Kore"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.07.48-300x165-1.webp", "Poujauran"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.06.38-300x131-1.webp", "Eatmotion"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.03.06-300x170-1.webp", "Ciao Gusto"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.04.34-300x103-1.webp", "Chef Cheffe"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.01.39-300x163-1.webp", "Savary"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.00.01-300x218-1.webp", "Karine & Jeff"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-14.57.18-300x122-1.webp", "Chrono Primeurs"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-14.56.24-300x154-1.webp", "Maison Aléna"),
]

# --------------------------------------------------------------------- les huit
# La variante A rend ces huit points en paragraphes numerotes, la variante B les
# regroupe en quatre onglets a puces. Meme fond, deux mises en scene : c'est ce
# qui fait que le test ne compare que l'UX.
HUIT = [
 ("Poids variable, de la pesée à la facture",
  "On commande vingt colis, on en reçoit vingt qui ne pèsent pas le poids annoncé. Si la "
  "facturation se fait au poids commandé, il faut ensuite émettre un avoir ; si elle se fait au "
  "poids réellement pesé, le problème n'existe pas. Le poids variable est natif : le bon de "
  "pesée, l'étiquette et la facture sortent de la même donnée, et disent donc la même chose. "
  "C'est le point où un ERP généraliste facture un développement spécifique."),
 ("Achat au cours du jour et coût de revient réel",
  "Le prix d'achat bouge plus vite que le tarif client. Enregistré à la réception, au cours du "
  "jour, il fait suivre le coût de revient au marché au lieu de le figer au tarif catalogue. La "
  "marge se lit alors sur ce que la marchandise a réellement coûté, pas sur une estimation "
  "vieille de trois semaines — et une hausse fournisseur peut être simulée sur la gamme avant "
  "d'être répercutée."),
 ("Trois états de stock : réservé, disponible, en préparation",
  "Un stock n'est pas un chiffre. C'est un emplacement, une température et une date. La "
  "marchandise réservée pour la tournée de demain n'est pas disponible ; celle qui est en "
  "préparation non plus. Confondre les trois, c'est vendre ce qu'on n'a plus ou racheter ce "
  "qu'on possède déjà. Chaque dépôt, chaque chambre froide et chaque transfert inter-site sont "
  "suivis séparément, le lot et la DLC conservés d'un bout à l'autre."),
 ("DLC portée par le lot, rotation en premier périmé premier sorti",
  "Deux lots de la même référence n'ont pas la même date, et cela change à qui l'on peut les "
  "vendre et à quel prix. La DLC est portée par le lot, pas par la référence. La rotation se "
  "fait en premier périmé premier sorti, avec des alertes avant péremption et la possibilité de "
  "déclencher une remise ciblée sur les lots qui approchent — plutôt que de constater la perte "
  "à l'inventaire."),
 ("Cadencier client et télévente assistée",
  "La commande arrive par quatre canaux qui n'ont rien à voir entre eux. Au téléphone, le "
  "télévendeur ne doit pas repartir d'une page blanche : le cadencier affiche les trois "
  "dernières commandes du client, propose les manquants, les substitutions et les promotions "
  "pendant l'appel, et contrôle la disponibilité réelle, DLC comprise, au moment de la saisie."),
 ("EDI avec la grande distribution",
  "Certains comptes imposent l'EDI, les autres appellent. Les messages de commande, d'avis "
  "d'expédition et de facture circulent avec les enseignes qui l'exigent, et rejoignent la même "
  "file que les commandes saisies à la main. Un seul stock, une seule préparation, une seule "
  "facturation : l'EDI n'est pas un circuit parallèle."),
 ("Préparation par tournée et bon de livraison au poids réel",
  "La préparation se fait par tournée, avec l'ordre de chargement inverse de l'ordre de "
  "livraison — sinon le chauffeur décharge tout à chaque arrêt. Le poids est saisi à la pesée, "
  "le bon de livraison édité dans la foulée et signé sur terminal. Les retours et les manquants "
  "constatés à la livraison sont répercutés directement sur la facture."),
 ("Marge par référence, par client, par tournée — et l'échéance qui va avec",
  "La question utile n'est pas « quel est mon chiffre d'affaires » mais « quelles lignes gagnent "
  "de l'argent ». Une fois le coût réel connu, la marge se lit par référence, par client, par "
  "tournée et par commercial. Et la facture part avec l'échéance légale propre à la nature du "
  "produit — 20 jours pour les viandes fraîches, 30 pour les périssables ou les boissons "
  "alcooliques, avec des points de départ différents."),
]
