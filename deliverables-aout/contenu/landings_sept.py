#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trois landings de septembre 2026 — contenu et arbitrage.

ETAPE 1, ANTI-CANNIBALISATION, MESUREE LE 17/09/2026
====================================================
  erp pme agroalimentaire ...... 20 rech./mois. SERP : /agroalimentaire/ est
      DEJA en position 5 organique, 7 absolue. Verdict FORT. Creer une seconde
      page sur la meme requete la ferait concurrencer une page qui rank deja
      en page 1. L'angle est donc deplace : non pas « erp pme agroalimentaire »
      mais la PME qui SORT D'EXCEL et structure sa croissance. Intention
      differente, pas de collision.
  erp fruits et legumes ........ 10 rech./mois. SERP : c'est le comparatif de
      blog /blog/meilleurs-erp-maraichers-fruits-legumes/ qui rank, 8e absolu ;
      /agroalimentaire/maraicher/ ne rank pas. Verdict MODERE. La SERP est
      tenue par le NEGOCE (CSB « grossistes », Caplaser « erp negoce fruits et
      legumes », Akanea). La landing prend donc l'angle negoce et grossiste ;
      /maraicher/ garde l'angle producteur.
  erp produits de la mer ....... sous le seuil de mesure de Google Ads.
      /agroalimentaire/poissonnier/ existe et couvre le comptoir. La landing
      prend l'amont : criee, maree, mareyage, zone de peche.

Ces trois angles sont choisis pour ne PAS entrer en concurrence avec une page
qui rank deja. C'est la seule raison pour laquelle ils different de l'intitule
de la roadmap.

ETAPE 3, GABARIT — celui des fiches metier, clone de /agroalimentaire/fromager/
(10867) : hero, logos, module a onglets, about, process, metiers, equipe, FAQ,
avis. Le module a onglets est celui pose sur les trente et une pages le 17/09.
"""

# ---------------------------------------------------------------- les ecrans
ECRANS = {
 "fruits-et-legumes": ["achat", "agreage", "tracabilite", "preparation", "marge"],
 "produits-de-la-mer": ["achat", "agreage", "tracabilite", "dlc", "tournee"],
 "pme-en-croissance": ["production", "stocks", "dlc", "facture", "marge"],
}

PAGES = {
 # =====================================================================
 "fruits-et-legumes": {
  "titre_page": "ERP Fruits et Légumes : Agréage, Poids Réel et Marge au Lot",
  "description": "L'ERP des grossistes en fruits et légumes : achat au cours du jour, "
                 "agréage à quai, poids réellement pesé sur la facture et marge calculée "
                 "lot par lot.",
  "badge": "ERP Fruits et Légumes",
  "h1": "L'ERP des fruits et légumes,",
  "h1_accent": "du carreau à la facture",
  "chapo": "Le colis annoncé à 10 kg en pèse 9,7, la salade perd un jour de DLC à chaque "
           "rupture de froid et le cours change dans la matinée. Un ERP fruits et légumes "
           "tient ces trois contraintes ; un ERP généraliste n'en tient aucune.",
  "overline": "ERP Fruits et Légumes",
  "h2": "L'ERP conçu pour le négoce de fruits et légumes",
  "sous_titre": "Achat au cours du jour, agréage à quai, poids réel sur la facture",
  "photo": (11772036, "erp-fruits-legumes-dechargement-cageots-agrumes",
            "Deux professionnels déchargeant des cageots d'agrumes d'un camion devant un "
            "commerce de fruits et légumes"),
  "fonctions": [
   ("Acheter au cours du jour",
    "Le prix des fruits et légumes bouge dans la matinée. La seule référence commune à "
    "l'acheteur et au vendeur est la cotation publiée chaque jour par FranceAgriMer.",
    ["La dernière cotation RNM est chargée avant le départ au marché",
     "La saisie se fait pavillon par pavillon, au fil de la tournée d'achat",
     "L'écart à la cotation s'affiche sur la ligne, au moment de la saisie",
     "L'historique de vos prix d'achat s'ouvre à côté de la cotation"]),
   ("L'agréage à quai, et la réclamation dans la foulée",
    "Un colis annoncé à 10 kg qui en pèse 9,7 laisse 300 grammes sur le quai. Constaté à la "
    "pesée, l'écart se réclame ; découvert au moment de payer, il est perdu.",
    ["Poids annoncé et poids pesé sur la même ligne de réception",
     "L'écart ouvre la réclamation fournisseur ou la demande d'avoir",
     "Le lot fournisseur entre dans le système dès la pesée",
     "L'historique des écarts par fournisseur s'ouvre avant de renégocier"]),
   ("La traçabilité du lot et de son origine",
    "Deux palettes du même produit n'ont ni la même origine, ni le même calibre, ni la même "
    "date. Le règlement (CE) 178/2002 impose de savoir, en une étape, d'où vient chaque lot "
    "et où il est parti.",
    ["Origine, variété, calibre et catégorie portés par le lot",
     "Un rappel remonte au fournisseur et redescend aux clients livrés",
     "Le numéro de lot suit jusqu'au bon de livraison",
     "Les registres sortent prêts pour un contrôle"]),
   ("Préparer en pesant, colis par colis",
    "Entre la commande et le camion, la marchandise repasse sur la balance. Ce poids-là est "
    "celui qui partira sur la facture.",
    ["Le poids pesé à la préparation remplace le poids commandé",
     "Chaque colis sort étiqueté avec son lot et sa date limite",
     "Le reliquat retourne en stock sous son lot d'origine"]),
   ("La marge réelle, lot par lot",
    "La marge théorique se calcule à l'achat. La marge réelle se connaît une fois la "
    "démarque déduite, et elle se lit par lot, pas seulement par produit.",
    ["La marge se lit par lot acheté, au poids pesé",
     "La perte sur date limite est rattachée au lot qui l'a produite",
     "Un lot vendu en perte se voit dans la semaine, pas au bilan"]),
  ],
  "faq": [
   ("Qu'est-ce qu'un ERP fruits et légumes ?",
    "C'est un logiciel de gestion qui prend en charge les trois contraintes propres à la "
    "filière : le <strong>poids variable</strong>, puisqu'on achète et on vend au kilo "
    "réellement pesé et non au colis annoncé ; la <strong>date limite courte</strong>, qui "
    "impose de sortir d'abord ce qui périme le plus tôt ; et le <strong>prix du jour</strong>, "
    "qui change chaque matin. Un ERP généraliste facture au poids commandé et à trente jours "
    "pour tout le monde."),
   ("Comment gérer le poids variable en fruits et légumes ?",
    "En pesant deux fois et en faisant remonter le poids dans la ligne. À la réception, "
    "l'agréage enregistre le poids annoncé et le poids pesé sur la même ligne : l'écart ouvre "
    "la réclamation fournisseur tant qu'elle est recevable. À la préparation, le poids pesé "
    "remplace le poids commandé, et c'est lui qui part sur la facture."),
   ("L'ERP suit-il les cours de FranceAgriMer ?",
    "Oui. Le réseau des nouvelles des marchés publie chaque jour les cours des grossistes "
    "relevés sur les marchés d'intérêt national. La dernière cotation publiée est chargée "
    "avant le départ au marché, et l'écart entre le prix payé et la cotation s'affiche sur "
    "chaque ligne au moment de la saisie."),
   ("Quelle différence avec un ERP pour producteur ?",
    "Un producteur pilote des parcelles, des semis et une récolte ; un grossiste pilote un "
    "achat, un agréage et une revente dans la journée. Si vous produisez vous-même, la page "
    "<a href=\"/agroalimentaire/maraicher/\">ERP maraîcher</a> décrit la gestion côté "
    "production."),
   ("Combien de temps pour déployer l'ERP ?",
    "Le déploiement est clé en main et ne demande pas d'informaticien chez vous. La reprise "
    "des articles, des clients et des tarifs se fait depuis vos fichiers existants, y compris "
    "des classeurs Excel."),
  ],
  "liens": ["/negoce/", "/agroalimentaire/maraicher/", "/negoce/tracabilite-lots/",
            "/negoce/achats-approvisionnements/", "/agroalimentaire/",
            "/fonctionnalites/gestion-de-stock/"],
 },

 # =====================================================================
 "produits-de-la-mer": {
  "titre_page": "ERP Produits de la Mer : Criée, Marée et Traçabilité des Lots",
  "description": "L'ERP des mareyeurs et grossistes en marée : achat à la criée, zone de pêche "
                 "tracée, dates limites très courtes et chaîne du froid prouvée.",
  "badge": "ERP Produits de la Mer",
  "h1": "L'ERP des produits de la mer,",
  "h1_accent": "de la criée au client",
  "chapo": "Deux jours de DLC, un poids qui bouge au filetage, une zone de pêche à porter sur "
           "chaque étiquette. La filière mer laisse moins de marge d'erreur qu'aucune autre, "
           "et c'est ce que cet ERP prend en charge.",
  "overline": "ERP Produits de la Mer",
  "h2": "L'ERP conçu pour le mareyage et le négoce de marée",
  "sous_titre": "Achat à la criée, zone de pêche tracée, froid prouvé",
  "photo": (8352350, "erp-produits-mer-caisse-poissons-glace",
            "Professionnel en gants versant une caisse de poissons rouges sur un étal de glace "
            "dans une halle à marée"),
  "fonctions": [
   ("Acheter à la criée, au prix du jour",
    "Le cours de la marée se fait à la criée, lot par lot, et il ne ressemble à celui de la "
    "veille sur aucune espèce. Ce qui se saisit le matin doit être valorisé dans l'heure.",
    ["La saisie se fait lot par lot, à la sortie de la criée",
     "Le prix payé se compare à la dernière cotation connue",
     "L'espèce, la taille et le calibre entrent avec le lot",
     "L'historique par fournisseur s'ouvre avant de renégocier"]),
   ("L'agréage et le poids au débarquement",
    "Entre le poids annoncé au débarquement et le poids réellement pesé, l'écart se constate "
    "à quai. Passé la réception, il n'est plus réclamable.",
    ["Poids annoncé et poids pesé sur la même ligne",
     "L'écart ouvre la réclamation ou la demande d'avoir",
     "Le rendement au filetage se calcule par lot",
     "La glace et la tare sont déduites du poids net"]),
   ("Zone de pêche, engin et date de débarquement",
    "Le règlement (UE) 1379/2013 impose l'affichage de la zone de capture, de l'engin de pêche "
    "et de la méthode de production sur chaque lot mis en vente. Ces trois mentions se portent "
    "au lot, pas au produit.",
    ["Zone FAO, sous-zone et engin portés par le lot",
     "Nom scientifique et nom commercial de l'espèce",
     "Un rappel remonte au navire et redescend aux clients livrés",
     "Les étiquettes sortent avec les mentions réglementaires"]),
   ("Des dates limites qui se comptent en jours",
    "Une marée fraîche tient deux à cinq jours. Ce qui périme le plus tôt doit sortir "
    "d'abord, et l'écart entre le stock théorique et le stock réel ne pardonne pas.",
    ["Le prélèvement suit la date limite par défaut",
     "Le reste à écouler s'affiche en jours, pas en dates",
     "Les lots proches de la limite remontent en tête de liste",
     "La démarque est rattachée au lot qui l'a produite"]),
   ("Le froid, de l'expédition à la réception",
    "La température relevée au chargement est ce que le client contrôle à la livraison. Sans "
    "trace, une contestation se règle à la parole.",
    ["La température du chargement suit le bon de livraison",
     "Les tournées se construisent depuis les commandes du matin",
     "Le bon signé revient dans le dossier client"]),
  ],
  "faq": [
   ("Qu'est-ce qu'un ERP produits de la mer ?",
    "C'est un logiciel de gestion conçu pour le mareyage et le négoce de marée. Il porte trois "
    "contraintes que les ERP généralistes ignorent : la <strong>zone de pêche et l'engin</strong>, "
    "obligatoires sur chaque lot au titre du règlement (UE) 1379/2013 ; le <strong>poids "
    "variable</strong>, entre le débarquement, le filetage et l'expédition ; et une "
    "<strong>date limite de deux à cinq jours</strong>."),
   ("Quelles mentions sont obligatoires sur un lot de poisson ?",
    "La dénomination commerciale et le <strong>nom scientifique</strong> de l'espèce, la "
    "<strong>méthode de production</strong> (pêché, pêché en eaux douces, élevé), la "
    "<strong>zone de capture</strong> et la <strong>catégorie d'engin de pêche</strong>. "
    "Elles sont portées par le lot, ce qui suppose que le lot soit suivi et non la seule "
    "référence produit."),
   ("Comment suivre le rendement au filetage ?",
    "En rattachant le poids entrant et le poids sortant au même lot. Le rendement se calcule "
    "alors par lot et par espèce, et l'écart entre le rendement théorique et le rendement réel "
    "se voit dans la semaine plutôt qu'au bilan."),
   ("Quelle différence avec un ERP pour poissonnerie ?",
    "Une poissonnerie vend au comptoir, à l'unité et au particulier ; un mareyeur achète à la "
    "criée et revend au professionnel, au lot et au poids. Si vous tenez un comptoir, la page "
    "<a href=\"/agroalimentaire/poissonnier/\">ERP poissonnerie</a> décrit cette gestion-là."),
   ("Le logiciel gère-t-il la chaîne du froid ?",
    "La température relevée au chargement suit le bon de livraison et reste attachée à "
    "l'expédition. Elle est donc opposable à la réception, ce qu'un relevé sur papier libre "
    "n'est pas."),
  ],
  "liens": ["/agroalimentaire/poissonnier/", "/negoce/tracabilite-lots/", "/agroalimentaire/",
            "/negoce/", "/fonctionnalites/gestion-de-stock/",
            "/negoce/achats-approvisionnements/"],
 },

 # =====================================================================
 "pme-en-croissance": {
  "titre_page": "ERP PME Agroalimentaire : Sortir d'Excel sans Tout Casser",
  "description": "L'ERP des PME agroalimentaires en croissance : reprise de vos classeurs Excel, "
                 "production, stocks et dates limites, facturation et marge, sans "
                 "informaticien.",
  "badge": "ERP PME Agroalimentaire",
  "h1": "L'ERP des PME agroalimentaires",
  "h1_accent": "en croissance",
  "chapo": "Il arrive un moment où le classeur Excel ne suit plus : trois personnes le "
           "modifient, la traçabilité tient dans un cahier et la marge se calcule après coup. "
           "Voici comment une PME agroalimentaire passe à un ERP sans arrêter de produire.",
  "overline": "ERP PME Agroalimentaire",
  "h2": "L'ERP conçu pour les PME agroalimentaires qui grandissent",
  "sous_titre": "Reprise de vos fichiers, production, stocks, marge — sans informaticien",
  "photo": (18429457, "erp-pme-agroalimentaire-atelier-operatrices",
            "Deux opératrices en charlotte et blouse blanche dans un atelier de production "
            "alimentaire"),
  "fonctions": [
   ("Reprendre vos fichiers, pas repartir de zéro",
    "Une PME qui change d'outil ne peut pas s'arrêter de produire. Les articles, les clients, "
    "les tarifs et les recettes se reprennent depuis vos classeurs existants.",
    ["Import des articles, clients et tarifs depuis Excel",
     "Les recettes et nomenclatures se reprennent telles quelles",
     "Le déploiement est clé en main, sans informaticien chez vous"]),
   ("La production et les recettes",
    "Tant que les recettes vivent dans des classeurs, le besoin matière se calcule à la main "
    "et l'ordre de fabrication part sans qu'on sache si la matière est là.",
    ["Le besoin matière se calcule depuis la recette",
     "Un ordre sans matière disponible est bloqué avant d'être lancé",
     "Le rendement réel se compare au rendement théorique",
     "Les coûts de revient se recalculent quand les matières bougent"]),
   ("Les stocks et les dates limites",
    "Le stock théorique et le stock réel divergent dès qu'ils vivent dans deux endroits. Et "
    "une date limite oubliée se paie en démarque.",
    ["Le prélèvement suit la date limite par défaut",
     "Le stock est juste entre l'atelier, la chambre froide et le camion",
     "Les alertes remontent avant la rupture, pas après"]),
   ("La facturation et la comptabilité",
    "Une facture d'agroalimentaire porte des poids à trois décimales et des mentions qui "
    "deviennent obligatoires. La ressaisie comptable est le premier poste de temps perdu.",
    ["Le bon de livraison devient facture sans ressaisie",
     "Les mentions obligatoires sont portées par le modèle de document",
     "Le format Factur-X est produit en même temps que le PDF",
     "L'export comptable part vers votre logiciel existant"]),
   ("Savoir où passe la marge",
    "Tant que la marge se calcule en fin de mois, on découvre les pertes une fois qu'elles "
    "sont faites. Le seul chiffre utile est celui de la semaine.",
    ["La marge se lit par lot, par produit et par client",
     "La perte sur date limite est isolée des autres écarts",
     "Un produit vendu en perte se voit dans la semaine"]),
  ],
  "faq": [
   ("À partir de quelle taille une PME agroalimentaire a-t-elle besoin d'un ERP ?",
    "Ce n'est pas une question d'effectif mais de points de rupture. Trois signaux reviennent : "
    "plusieurs personnes modifient le même classeur, la traçabilité d'un lot demande de "
    "rouvrir un cahier, et la marge d'un produit ne se connaît qu'en fin de mois. Dès que deux "
    "des trois sont là, le tableur coûte plus qu'il ne rapporte."),
   ("Peut-on reprendre nos fichiers Excel existants ?",
    "Oui. Les articles, les clients, les tarifs, les recettes et les nomenclatures s'importent "
    "depuis vos classeurs. C'est le point de départ du déploiement, pas une option payante."),
   ("Faut-il un informaticien dans l'entreprise ?",
    "Non. Le logiciel est en SaaS : il n'y a pas de serveur à installer ni de sauvegarde à "
    "gérer. Le déploiement est clé en main et la formation se fait sur vos propres données."),
   ("Combien de temps dure le déploiement ?",
    "Cela dépend du nombre de modules ouverts et de l'état de vos fichiers. La reprise des "
    "données est le poste le plus long, et c'est pourquoi elle est faite avec vous plutôt que "
    "laissée à votre charge."),
   ("Quelle différence avec un ERP généraliste moins cher ?",
    "Un ERP généraliste facture au poids commandé, applique une date d'échéance unique et "
    "ignore le numéro de lot. En agroalimentaire, ces trois points sont exactement là où la "
    "marge et la conformité se jouent. Le comparatif des "
    "<a href=\"/agroalimentaire/\">ERP agroalimentaires</a> détaille ce que couvre un outil "
    "métier."),
  ],
  "liens": ["/agroalimentaire/", "/fonctionnalites/fabrication/",
            "/fonctionnalites/gestion-de-stock/", "/fonctionnalites/facturation/",
            "/negoce/tracabilite-lots/", "/tarifs/"],
 },
}
