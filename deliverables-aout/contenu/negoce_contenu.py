# -*- coding: utf-8 -*-
"""
Contenu de la mise a jour de /agroalimentaire/negoce-alimentaire/ — requete
« erp negoce alimentaire », persona : dirigeant de PME grossiste, distributeur
food-service ou negociant en produits alimentaires.

Fait date et source unique de la page :
Code de commerce, articles L441-10 et L441-11 (Legifrance), delais maximaux de
paiement applicables aux produits alimentaires.
"""

SOURCE = "Code de commerce, articles L441-10 et L441-11 (Légifrance)"

H1 = ('ERP négoce alimentaire : le poids réellement pesé, '
      '<span class="accent" style="color:#7dd3fc">la DLC et l\'échéance légale</span>')

HERO_DESC = ("Négoce, distribution et gros de produits alimentaires : un ERP qui facture au poids "
             "réellement pesé, applique la DLC du lot et l'échéance légale du produit — là où un "
             "ERP généraliste facture au poids commandé et à trente jours pour tout le monde.")

# --------------------------------------------------------------- delais legaux
DELAIS = [
    ("Bétail sur pied destiné à la consommation, viandes fraîches dérivées",
     "20 jours", "après le jour de livraison"),
    ("Produits alimentaires périssables, viandes congelées ou surgelées, poissons surgelés, "
     "plats cuisinés, conserves fabriquées à partir de produits périssables",
     "30 jours", "après la fin de la décade de livraison, en facturation périodique"),
    ("Boissons alcooliques passibles des droits de consommation",
     "30 jours", "après la fin du mois de livraison"),
    ("Régime général, à défaut de convention",
     "30 jours", "après la réception des marchandises"),
    ("Régime général, si les parties en conviennent au contrat",
     "60 jours", "à compter de la date d'émission de la facture — ou 45 jours fin de mois"),
]

# ------------------------------------------------------------------ FAQ
# Les six questions affichees en carte etaient deja justes. Les reponses, elles,
# venaient du gabarit maraicher : elles sont reecrites ici en face de leur
# question. La septieme porte le fait date.
FAQ = [
    (
        "Comment gérer les stocks multi-dépôts en négoce alimentaire ?",
        "Dépôts, chambres froides, transferts",
        "<p>Un grossiste alimentaire ne tient pas un stock, il en tient plusieurs : la plateforme, "
        "les chambres froides positives et négatives, parfois un dépôt avancé, et la marchandise "
        "déjà réservée pour une tournée du lendemain. Les confondre, c'est vendre ce qu'on n'a "
        "plus ou racheter ce qu'on possède déjà.</p>"
        "<ul>"
        "<li><strong>Un stock par emplacement</strong>, avec sa température : chaque référence sait "
        "où elle est et dans quelles conditions elle est conservée.</li>"
        "<li><strong>Réservé, disponible, en préparation</strong> : trois états distincts, pour ne "
        "pas engager deux fois la même palette.</li>"
        "<li><strong>Transferts inter-dépôts tracés</strong> : un colis qui change de site garde "
        "son lot et sa DLC.</li>"
        "<li><strong>Inventaires tournants</strong> par zone, sans arrêter l'activité.</li>"
        "<li><strong>Stock en poids et en colis</strong> à la fois, parce que vous achetez au kilo "
        "et préparez à l'unité de vente consommateur.</li>"
        "</ul>"
        "<p>Voir la <a href=\"/fonctionnalites/gestion-de-stock/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">gestion de stock</a> "
        "et les <a href=\"/negoce/stocks-multi-depots/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">stocks multi-dépôts</a>.</p>"
    ),
    (
        "L'ERP gère-t-il le cadencier et les commandes clients ?",
        "Cadencier, télévente, EDI",
        "<p>Oui, et c'est le poste où un grossiste gagne le plus de temps. La commande arrive par "
        "quatre canaux qui n'ont rien à voir entre eux : le téléphone, le mail, l'EDI de la grande "
        "distribution et le portail client. L'ERP les ramène à une seule file.</p>"
        "<ul>"
        "<li><strong>Cadencier par client</strong> : l'historique des trois dernières commandes "
        "s'affiche à la saisie, le télévendeur ne repart pas d'une page blanche.</li>"
        "<li><strong>Télévente assistée</strong> : manquants, substitutions et promotions proposés "
        "pendant l'appel, pas après.</li>"
        "<li><strong>EDI</strong> pour les comptes qui l'imposent, saisie assistée pour les "
        "autres — la même commande dans le même flux.</li>"
        "<li><strong>Contrôle de la disponibilité réelle</strong> au moment de la prise de "
        "commande, DLC comprise.</li>"
        "<li><strong>Préparation par tournée</strong>, avec l'ordre de chargement inverse de "
        "l'ordre de livraison.</li>"
        "</ul>"
        "<p>Voir <a href=\"/negoce/ventes-devis-commandes/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">ventes, devis et commandes</a>.</p>"
    ),
    (
        "Comment piloter mes tarifs et marges au cours du jour ?",
        "Cours du jour, grilles, marges",
        "<p>En négoce alimentaire, le prix d'achat bouge plus vite que le tarif client. Entre le "
        "moment où vous achetez et celui où vous facturez, la marge se fabrique — ou se perd — "
        "sans que personne ne la regarde.</p>"
        "<ul>"
        "<li><strong>Achat au cours du jour</strong> enregistré à la réception : le coût de "
        "revient suit le marché, il n'est pas figé au tarif catalogue.</li>"
        "<li><strong>Grilles tarifaires par canal</strong> — RHF, GMS, détail, collectivités — et "
        "conditions particulières par client, dans une base unique.</li>"
        "<li><strong>Marge en temps réel</strong>, référence par référence et client par client, "
        "pas seulement en cumul mensuel.</li>"
        "<li><strong>Alerte sur les lignes vendues sous le seuil</strong> que vous fixez, avant "
        "l'édition de la facture.</li>"
        "<li><strong>Répercussion d'une hausse fournisseur</strong> simulée sur la gamme avant "
        "d'être appliquée.</li>"
        "</ul>"
        "<p>Voir <a href=\"/negoce/tarifs-reporting-edi/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">tarifs, reporting et EDI</a>.</p>"
    ),
    (
        "L'ERP est-il adapté aux grossistes et distributeurs alimentaires ?",
        "Grossistes, food-service, GMS",
        "<p>C'est le métier pour lequel il est fait. Hello Harel est un ERP SaaS français "
        "exclusivement spécialisé agroalimentaire, utilisé par plus de 200 entreprises de la "
        "filière, noté 5,0 sur 5 sur 31 avis.</p>"
        "<p>Concrètement, il est pertinent si vous vous reconnaissez dans au moins trois de ces "
        "situations :</p>"
        "<ul>"
        "<li>Vous achetez au kilo et vous vendez à l'unité de vente consommateur.</li>"
        "<li>Deux lots de la même référence n'ont pas la même DLC, et ça change à qui vous "
        "pouvez les vendre.</li>"
        "<li>Vous livrez des restaurants, des collectivités ou des magasins, en tournées.</li>"
        "<li>Un de vos clients exige l'EDI et les autres appellent au téléphone.</li>"
        "<li>Vous devez sortir la liste des clients livrés d'un lot en cas d'alerte.</li>"
        "</ul>"
        "<p>Si vous transformez au lieu de redistribuer, c'est le <a href=\"/fonctionnalites/fabrication/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">logiciel de fabrication</a> "
        "qui vous parlera davantage.</p>"
    ),
    (
        "Qu'est-ce qu'un ERP négoce alimentaire ?",
        "Définition, périmètre, cible",
        "<p>Un <strong>ERP négoce alimentaire</strong> est un logiciel de gestion intégré qui "
        "relie, dans une seule base, l'achat au cours du jour, le lot et sa DLC, le poids "
        "réellement pesé, la tournée de livraison et la facturation d'un grossiste ou d'un "
        "distributeur de produits alimentaires.</p>"
        "<p>Ce qui le sépare d'un ERP généraliste tient en quatre points :</p>"
        "<ul>"
        "<li><strong>Il facture au poids pesé</strong>, pas au poids commandé — donc sans avoir à "
        "émettre un avoir derrière.</li>"
        "<li><strong>Il descend au lot</strong> et non à la référence : c'est la condition d'un "
        "retrait-rappel ciblé.</li>"
        "<li><strong>Il connaît les échéances légales propres à l'alimentaire</strong>, qui ne "
        "sont pas de trente jours pour tout le monde.</li>"
        "<li><strong>Il sort la marge réelle</strong> par référence, par client et par tournée, "
        "sur un coût d'achat qui a bougé depuis le catalogue.</li>"
        "</ul>"
        "<p>Il devient pertinent dès que l'activité dépasse le tableur : plusieurs dépôts, "
        "plusieurs canaux de commande, une gamme à rotation rapide.</p>"
    ),
    (
        "L'ERP gère-t-il l'EDI et la livraison (GMS, RHF) ?",
        "EDI, tournées, bons de livraison",
        "<p>Oui, et les deux bouts sont reliés : la commande EDI entre, le bon de livraison et la "
        "facture sortent de la même donnée.</p>"
        "<ul>"
        "<li><strong>Messages EDI</strong> de commande, d'avis d'expédition et de facture avec les "
        "enseignes qui l'imposent.</li>"
        "<li><strong>Préparation par tournée</strong> : picking en premier périmé premier sorti, "
        "poids réel saisi à la pesée, étiquette éditée dans la foulée.</li>"
        "<li><strong>Bon de livraison</strong> au poids réel, signé sur terminal, transformé en "
        "facture sans ressaisie.</li>"
        "<li><strong>Retours et manquants</strong> constatés à la livraison et répercutés "
        "directement sur la facturation.</li>"
        "<li><strong>Reporting par tournée</strong> : ce qu'elle a rapporté, ce qu'elle a coûté.</li>"
        "</ul>"
        "<p>Voir la <a href=\"/fonctionnalites/logistique/\" style=\"color:#00B1F5;font-weight:600;text-decoration:underline;\">logistique et les tournées</a>.</p>"
    ),
    (
        "Sous combien de jours dois-je être payé en alimentaire ?",
        "Délais légaux, trésorerie",
        "<p>Pas trente jours pour tout le monde : le Code de commerce fixe des délais maximaux "
        "propres aux produits alimentaires, plus courts que le régime général, et le point de "
        "départ change selon la nature du produit.</p>"
        "<ul>"
        "<li><strong>20 jours après le jour de livraison</strong> pour le bétail sur pied destiné "
        "à la consommation et les viandes fraîches qui en dérivent.</li>"
        "<li><strong>30 jours après la fin de la décade de livraison</strong> pour les produits "
        "alimentaires périssables, les viandes congelées ou surgelées, les poissons surgelés, les "
        "plats cuisinés et les conserves fabriquées à partir de produits périssables, en "
        "facturation périodique.</li>"
        "<li><strong>30 jours après la fin du mois de livraison</strong> pour les boissons "
        "alcooliques passibles des droits de consommation.</li>"
        "</ul>"
        "<p>Source : " + SOURCE + ". Ces délais sont des maximums : rien n'interdit de convenir "
        "plus court. Un ERP qui ignore la nature du produit applique la même échéance à tout, et "
        "c'est votre trésorerie qui absorbe l'écart.</p>"
    ),
]

# ------------------------------------------------------------------ calculateur
# Valeurs de depart, a remplacer par celles du lecteur : elles ne sont pas
# presentees comme une reference mais comme un point de depart.
CALC = {
    "achat": "8.50", "theorique": "2.000", "reel": "2.060", "vente": "21.90", "volume": "1200",
}
