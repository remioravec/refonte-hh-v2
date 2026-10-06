# -*- coding: utf-8 -*-
"""
Contenu de la mise a jour de /agroalimentaire/glacier/ — requete cible « erp glacier ».

Toutes les valeurs reglementaires viennent d'une source unique, citee dans la page :
CNGF/SFIG, Code des pratiques loyales des glaces alimentaires (CPLGA), version du
4 mars 2008, points 2.3.1 a 2.3.8 et tableau de synthese.
"""

SOURCE = ("Code des pratiques loyales des glaces alimentaires, CNGF/SFIG, "
          "version du 4 mars 2008, points 2.3.1 à 2.3.8")

# denomination, poids minimal par litre (g), seuil caracteristique
DENOMINATIONS = [
    ("Glace à l'eau, glaçon",      450, "extrait sec total ≥ 12 %"),
    ("Glace",                      450, "matières grasses alimentaires + protéines"),
    ("Glace au lait",              450, "matière grasse laitière ≥ 2,5 %, extrait sec dégraissé ≥ 6 %"),
    ("Glace aux œufs",             550, "jaune d'œuf ≥ 7 %, matières grasses exclusivement laitières"),
    ("Crème glacée",               450, "matière grasse laitière ≥ 5 %"),
    ("Glace au(x) fruit(s)",       450, "fruits ≥ 15 % — 10 % agrumes et fruits acides, 5 % fruits à coques"),
    ("Sorbet",                     450, "fruits ≥ 25 % — 15 % fruits acides ou à saveur forte"),
    ("Sorbet plein fruit",         650, "fruits ≥ 45 % — 20 % fruits acides, à saveur forte ou pâteux"),
]

HERO_IMG = ("https://www.helloharel.com/wp-content/uploads/2026/08/"
            "erp-glacier-laboratoire-production.webp")

H1 = ('ERP glacier : la recette, le lot et le <span class="accent" style="color:#7dd3fc">'
      'coût de revient au litre</span>')

HERO_DESC = ("Un ERP glacier relie le mix, le foisonnement, le lot et la DLC au coût de revient "
             "réel du litre produit — là où un logiciel de caisse s'arrête au ticket. "
             "Pour les fabricants de glaces, sorbets et desserts glacés.")

# --------------------------------------------------------------------------- FAQ
# Q, meta (3 mots du bandeau), reponse HTML
FAQ = [
    (
        "Comment calculer le prix de revient d'un litre de glace ?",
        "Comment, revient, litre",
        "<p>Le prix de revient d'une glace ne se calcule pas au kilo de mix, mais "
        "<strong>au litre de produit fini</strong> — et l'écart entre les deux, c'est le "
        "foisonnement. Un mix à 1,10 kg/L turbiné à 35 % donne un litre qui pèse 815 g : "
        "vous vendez du volume, vous achetez de la masse.</p>"
        "<p>Le calcul complet enchaîne quatre étapes :</p>"
        "<ul>"
        "<li><strong>Le coût du mix</strong> : lait, crème, sucres, poudre de lait, stabilisants, "
        "fruits ou pâtes aromatiques, valorisés au prix d'achat réel du dernier lot reçu.</li>"
        "<li><strong>Les sous-recettes</strong> : une base blanche ou une base jaune sert vingt "
        "parfums. Si le prix de la crème bouge, les vingt coûts de revient bougent avec elle.</li>"
        "<li><strong>Le foisonnement</strong> : c'est lui qui convertit un coût au kilo en coût au "
        "litre. Sans lui, la marge affichée est fausse dans le même sens que l'air incorporé.</li>"
        "<li><strong>Les pertes</strong> : fonds de cuve, purges de turbine, écarts de "
        "conditionnement, invendus de fin de saison.</li>"
        "</ul>"
        "<p>Le calculateur en haut de cette page fait les trois premières étapes avec vos chiffres. "
        "Pour la méthode complète, poste par poste, voyez notre "
        "<a href=\"/blog/calculer-le-prix-de-revient-en-boulangerie/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">logiciel de prix de revient</a>.</p>"
    ),
    (
        "Comment l'ERP suit-il la pasteurisation, la maturation et le turbinage ?",
        "Pasteurisation, maturation, turbinage",
        "<p>Chaque étape du process glacier devient une opération datée et tracée dans l'ERP : "
        "<strong>pasteurisation</strong> (couple temps/température relevé), "
        "<strong>maturation</strong> (durée en cuve, température de maturation), "
        "<strong>turbinage</strong> (foisonnement mesuré sur le bac de sortie), "
        "<strong>surgélation et conservation à −18 °C</strong>.</p>"
        "<p>Concrètement :</p>"
        "<ul>"
        "<li><strong>Ordre de fabrication par cuve</strong> : quantité de mix, parfum, lot des "
        "matières premières engagées, opérateur, machine.</li>"
        "<li><strong>Relevés de température</strong> saisis ou remontés des sondes, rattachés au "
        "lot et non à une feuille volante — c'est ce qui rend un contrôle sanitaire tenable.</li>"
        "<li><strong>Foisonnement réel</strong> : le poids du bac de sortie divisé par son volume "
        "donne le foisonnement effectif, comparé à la cible de la recette.</li>"
        "<li><strong>DLC et DDM</strong> calculées à partir de la date de fabrication et de la "
        "règle propre à chaque famille de produit.</li>"
        "<li><strong>Traçabilité ascendante et descendante</strong> : d'un lot de crème reçu à "
        "tous les bacs livrés, et l'inverse, en quelques secondes.</li>"
        "</ul>"
        "<p>Voir le module de <a href=\"/fonctionnalites/fabrication/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">gestion de production</a>.</p>"
    ),
    (
        "Comment piloter un laboratoire central et plusieurs points de vente ?",
        "Laboratoire, boutiques, transferts",
        "<p>La configuration la plus fréquente en glacerie : un <strong>laboratoire central</strong> "
        "qui produit, des <strong>boutiques</strong> et un circuit <strong>B2B</strong> "
        "(restaurants, hôtels, collectivités, GMS) qui consomment. L'ERP tient les trois flux dans "
        "le même stock.</p>"
        "<ul>"
        "<li><strong>Commandes inter-sites</strong> : chaque boutique commande au laboratoire dans "
        "l'ERP ; les besoins sont consolidés en ordres de fabrication.</li>"
        "<li><strong>Stocks par emplacement</strong> : matières premières au labo, bacs et pots en "
        "chambre négative, produits en vitrine — chacun son emplacement, chacun sa température.</li>"
        "<li><strong>Transferts tracés</strong> : un bac qui part du labo vers une boutique reste "
        "attaché à son lot et à sa DLC.</li>"
        "<li><strong>Tarifs par circuit</strong> : le prix boutique n'est pas le prix grossiste ; "
        "les deux cohabitent sans double saisie.</li>"
        "<li><strong>Marge par point de vente et par parfum</strong>, pour arbitrer une gamme "
        "avant la saison plutôt qu'après.</li>"
        "</ul>"
        "<p>Voir la <a href=\"/fonctionnalites/gestion-de-stock/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">gestion de stock</a> multi-emplacements.</p>"
    ),
    (
        "Comment sont suivis les lots de matières premières et les DLC ?",
        "Lots, DLC, FEFO",
        "<p>En glacerie, les matières sensibles sont le <strong>lait</strong>, la "
        "<strong>crème</strong>, les <strong>ovoproduits</strong>, les <strong>fruits</strong> et "
        "les <strong>pâtes aromatiques</strong> — toutes datées, toutes réglementées.</p>"
        "<ul>"
        "<li><strong>Réception par lot</strong> : numéro fournisseur, date, DLC, température de "
        "livraison. Le lot devient l'unité de suivi, pas la référence.</li>"
        "<li><strong>FEFO automatique</strong> : l'ERP propose d'abord le lot qui périme le plus "
        "tôt, ce qui vide les frigos dans le bon ordre.</li>"
        "<li><strong>Alertes de péremption</strong> avant que le produit ne devienne une perte.</li>"
        "<li><strong>Étiquetage INCO</strong> : allergènes et déclaration nutritionnelle calculés "
        "depuis la recette, pas ressaisis.</li>"
        "<li><strong>Prix d'achat réel</strong> à chaque réception : le coût de revient suit le "
        "marché sans intervention manuelle.</li>"
        "</ul>"
        "<p>Voir la <a href=\"/fonctionnalites/tracabilite-alimentaire/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">traçabilité alimentaire</a>.</p>"
    ),
    (
        "Qu'est-ce qu'un ERP glacier ?",
        "Définition, périmètre, cible",
        "<p>Un <strong>ERP glacier</strong> est un logiciel de gestion intégré qui relie, dans une "
        "seule base, la recette du mix, le lot de fabrication, le foisonnement, la DLC et le coût "
        "de revient au litre d'un fabricant de glaces, sorbets et desserts glacés.</p>"
        "<p>Ce qui le sépare d'un logiciel de caisse ou d'un tableur :</p>"
        "<ul>"
        "<li><strong>Il descend au lot</strong>, pas seulement à la référence : c'est la condition "
        "d'un retrait-rappel ciblé.</li>"
        "<li><strong>Il connaît le foisonnement</strong>, donc la différence entre un coût au kilo "
        "et un coût au litre.</li>"
        "<li><strong>Il connaît les dénominations réservées</strong> et leur poids minimal par "
        "litre — 450 g pour une crème glacée, 550 g pour une glace aux œufs, 650 g pour un sorbet "
        "plein fruit (" + SOURCE + ").</li>"
        "<li><strong>Il couvre la chaîne entière</strong> : achat, réception, production, stock, "
        "expédition, facturation.</li>"
        "</ul>"
        "<p>Il devient pertinent dès que l'activité dépasse le comptoir : laboratoire de production, "
        "livraisons B2B, plusieurs points de vente, gamme étendue. Hello Harel est un ERP SaaS "
        "français spécialisé agroalimentaire, également déployé chez des "
        "<a href=\"/agroalimentaire/patissier/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">ERP pâtissier</a> et des "
        "<a href=\"/agroalimentaire/chocolatier/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">ERP chocolatier</a>.</p>"
    ),
    (
        "Combien doit peser un litre de glace ?",
        "Poids, litre, réglementation",
        "<p>Le poids minimal par litre est fixé par dénomination. Il n'est pas indicatif : c'est la "
        "condition d'emploi de la dénomination sur l'étiquette.</p>"
        "<ul>"
        "<li><strong>450 g par litre</strong> : glace, glace à l'eau, glaçon, glace au lait, "
        "crème glacée, glace au(x) fruit(s), sorbet.</li>"
        "<li><strong>550 g par litre</strong> : glace aux œufs.</li>"
        "<li><strong>650 g par litre</strong> : sorbet plein fruit.</li>"
        "</ul>"
        "<p>Ces valeurs viennent du " + SOURCE + ". Elles plafonnent mécaniquement le "
        "foisonnement : avec un mix à 1,10 kg/L, on ne peut pas dépasser environ 144 % de "
        "foisonnement sur une crème glacée, 100 % sur une glace aux œufs et 69 % sur un sorbet "
        "plein fruit. Le calculateur en haut de page pose le verdict sur votre propre mix.</p>"
    ),
    (
        "Pourquoi un ERP plutôt qu'un tableur ?",
        "Tableur, limites, fiabilité",
        "<p>Le tableur tient tant que rien ne bouge. En glacerie, tout bouge : le prix de la crème, "
        "le foisonnement d'une cuve, la DLC d'un lot, la commande d'un restaurant.</p>"
        "<ul>"
        "<li><strong>Données reliées</strong> : un prix fournisseur mis à jour recalcule les coûts "
        "de revient, les marges et les prix conseillés de tous les parfums concernés.</li>"
        "<li><strong>Une seule saisie</strong> au lieu d'une saisie par fichier.</li>"
        "<li><strong>Traçabilité par lot</strong> et étiquetage INCO : hors de portée d'un tableur, "
        "et pourtant obligatoires.</li>"
        "<li><strong>Travail simultané</strong> du labo, du commerce et de la comptabilité sur la "
        "même donnée.</li>"
        "<li><strong>Historique</strong> : ce qu'on a produit, à quel coût, avec quel lot — "
        "consultable un an après, quand la question arrive.</li>"
        "</ul>"
        "<p>Hello Harel est un ERP SaaS spécialisé agroalimentaire, noté 5,0/5 sur 31 avis, "
        "avec plus de 200 entreprises agroalimentaires équipées.</p>"
    ),
]
