#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VARIANTE B de /negoce/ — LE HUB « comment choisir ». BROUILLON NOINDEX.

Format tire du releve SERP du 21/08/2026 sur « logiciel import export » :
  #1 akanea.com  — glossaire, structure 100 %% en questions (Qu'est-ce que /
     Quels avantages / Comment choisir / Quels logiciels du marche)
  #2 dashdoc.com — 9 H2 et 26 H3, 2592 mots, comparatif du marche + FAQ
  => la SERP recompense le question-led dense avec comparatif et FAQ.

Modele de maillage (skill maillage-interne, profil SAAS) : le hub EXPLIQUE,
ne vise jamais la requete de sa landing, arrose les 5 pages filles, et ne fait
qu'UN SEUL lien editorial sortant, vers la landing.

DRY par defaut ; --live pour publier.
"""
import sys, json
import wp_common as w

SLUG = "negoce-test-b-hub"
TITLE = "[TEST B] Comment Choisir son Logiciel de Négoce Alimentaire • Guide"
LANDING = "/fonctionnalites/import-export/"
U = "https://www.helloharel.com/wp-content/uploads/"
IMG = {
 "hero": U + "2026/08/Logiciel-de-grossistes-alimentaire-1.webp",
 "terrain": U + "2026/08/Logiciel-de-grossistes-alimentaire-2.webp",
 "prod": U + "2025/06/Hello-Harel-Gestion-de-la-logistique.png",
}

# H2 > H3 : la densite qui fait ranker Dashdoc
BLOCS = [
("Qu’est-ce qu’un logiciel de négoce alimentaire ?",
 "<p>Un logiciel de négoce alimentaire centralise l’achat, le stock, la vente et la facturation "
 "de marchandises que l’on revend sans les transformer — ou en les transformant à peine. Il se "
 "distingue d’un logiciel de gestion commerciale classique sur trois points qui ne sont pas des "
 "options dans l’alimentaire : la marchandise se pèse, elle périme, et elle doit être traçable "
 "jusqu’au lot d’origine.</p>",
 [("En quoi diffère-t-il d’une gestion commerciale classique ?",
   "Une gestion commerciale raisonne en unités et en prix fixe. En négoce alimentaire, on commande "
   "vingt cartons qui ne pèsent pas le poids annoncé, on vend une marchandise dont la durée de vie "
   "se réduit chaque jour, et on doit pouvoir dire à qui est parti tel lot. Ces trois écarts se "
   "rattrapent à la main tant que l’outil ne les porte pas nativement."),
  ("Faut-il un ERP ou un logiciel spécialisé ?",
   "La question est mal posée : un ERP est un logiciel spécialisé quand il couvre votre filière. "
   "Le vrai partage est entre un outil généraliste qu’il faudra adapter — au prix d’un "
   "développement spécifique à maintenir — et un outil qui porte déjà les contraintes du métier."),
  ("À partir de quelle taille est-ce justifié ?",
   "Le déclencheur n’est pas l’effectif mais le nombre de tableurs parallèles. Dès que le stock, "
   "les tarifs clients et les marges vivent dans trois fichiers différents que personne ne "
   "réconcilie, l’information existe mais arrive trop tard pour décider.")]),

("Quelles fonctions départagent réellement les solutions ?",
 "<p>La plupart des outils cochent les mêmes cases sur une plaquette. Les différences se voient "
 "sur cinq terrains précis — et ce sont ceux-là qu’il faut faire démontrer sur vos propres "
 "données, pas sur un jeu de démonstration.</p>",
 [("Les achats et l’engagement fournisseur",
   "Un cadencier tenu dans l’outil, des contrats d’achat avec les quantités engagées, et la "
   "visibilité sur ce qui est commandé mais pas encore arrivé. C’est l’amont qui désorganise le "
   "reste quand il est mal tenu : <a href=\"/negoce/achats-approvisionnements/\">gérer les achats "
   "et approvisionnements</a>."),
  ("Le stock, dans ses trois états",
   "En transit, sous douane, disponible : trois réalités différentes qu’un outil généraliste "
   "confond en un seul chiffre. Vendre du stock en transit sans le savoir, c’est promettre une "
   "date qu’on ne tiendra pas — voir les <a href=\"/negoce/stocks-multi-depots/\">stocks "
   "multi-dépôts</a>."),
  ("La traçabilité jusqu’au lot",
   "La question posée en contrôle est toujours la même : ce lot est parti où, et qu’y a-t-il "
   "dedans. Si la réponse suppose de rouvrir des bons papier, le périmètre du rappel s’élargit "
   "par précaution — voir la <a href=\"/negoce/tracabilite-lots/\">traçabilité des lots</a>."),
  ("La prise de commande et la télévente",
   "Une grande part des commandes se prend au téléphone, vite, avec des prix qui bougent. Le point "
   "à regarder n’est pas l’écran de saisie mais ce qui suit : le devis devient-il commande, puis "
   "bon de livraison, puis facture, sans ressaisie — voir <a href=\"/negoce/ventes-devis-commandes/\">"
   "ventes, devis et commandes</a>."),
  ("Les grilles tarifaires et l’EDI",
   "Un tarif par client, des remises par volume, des accords annuels, et pour la grande "
   "distribution des échanges normalisés. C’est là que beaucoup d’outils s’arrêtent — voir "
   "<a href=\"/negoce/tarifs-reporting-edi/\">tarifs, reporting et EDI</a>.")]),

("Comment choisir : les six questions à poser en démonstration",
 "<p>Une démonstration réussie ne prouve rien : elle a été préparée. Ces six questions font "
 "sortir les outils de leur scénario.</p>",
 [("« Montrez-moi une facture au poids réel »",
   "Prenez une commande de vingt colis, faites-en peser dix-huit à un poids différent, et "
   "demandez la facture. Si elle sort au poids commandé et qu’il faut un avoir derrière, le "
   "poids variable n’est pas natif."),
  ("« Prenez mon client le plus compliqué »",
   "Celui qui cumule remise de volume, accord annuel et tarif dérogatoire. Demandez à voir la "
   "facture sortir juste, sans intervention manuelle."),
  ("« D’où vient ce lot, et où est-il parti ? »",
   "Depuis un produit fini, remontez au fournisseur ; depuis un lot suspect, redescendez à tous "
   "les clients livrés. Chronométrez."),
  ("« Que se passe-t-il si la DLC approche ? »",
   "L’outil doit alerter, prioriser en premier périmé premier sorti, et permettre une remise "
   "ciblée sur les lots concernés — pas sur la référence entière."),
  ("« Combien m’a coûté ce conteneur, vraiment ? »",
   "Si la réponse est le prix fournisseur, le calcul des frais d’approche se fait ailleurs, donc "
   "après coup, donc sur une marge estimée."),
  ("« Qui reprend mes données, et en combien de temps ? »",
   "Le catalogue, les tarifs clients et les encours doivent être repris. C’est là que les projets "
   "dérapent — rarement sur les fonctionnalités.")]),
]

# comparatif marche — les deux pages du top 2 en ont un
MARCHE = [
 ("Solution", "Ce qu’elle fait le mieux", "Pour qui"),
 ("Akanea TMS Freight Forwarding", "Le dossier de transport et les formalités douanières, de bout en bout", "Commissionnaires de transport et transitaires"),
 ("Dashdoc", "Le suivi d’acheminement et la relation avec les transporteurs", "Chargeurs et transporteurs"),
 ("Trade.easy", "Le pilotage commercial de l’import-export, tous secteurs", "Négoce international généraliste"),
 ("Ellipson", "L’ERP import-export orienté logistique et stock", "Import-export généraliste"),
 ("Hello Harel", "Le négoce alimentaire : poids variable, DLC, lot d’origine et coût de revient réel", "PME agroalimentaires de 20 à 300 salariés"),
]

ERREURS = [
 ("Choisir sur la démonstration plutôt que sur ses propres données",
  "Toute solution est convaincante sur un jeu de données préparé. La seule démonstration qui "
  "informe est celle qui part de vos grilles tarifaires, de vos lots et de vos conteneurs réels."),
 ("Sous-estimer la reprise de l’existant",
  "Catalogue, tarifs clients, encours, historique des mouvements. C’est le poste qui allonge les "
  "projets, et il ne se voit pas dans une comparaison de fonctionnalités."),
 ("Comparer des licences au lieu de comparer des coûts complets",
  "Un généraliste affiche souvent une licence attractive, puis facture le développement du poids "
  "variable, sa maintenance, et sa reprise à chaque montée de version. La bonne unité de "
  "comparaison est le coût sur trois ans, délai de mise en service inclus."),
 ("Attendre d’avoir le temps",
  "Le moment n’arrive jamais. Les entreprises qui basculent le font rarement pour des raisons "
  "informatiques : elles le font quand la marge devient illisible, ou après un contrôle qui a "
  "montré les limites du suivi papier."),
]

FAQ = [
 ("Combien coûte un logiciel de négoce alimentaire ?",
  "Le tarif dépend du nombre d’utilisateurs et des modules retenus. Le point à comparer n’est pas la licence seule mais le coût complet sur trois ans : licence, mise en service, reprise de données, formation et développements spécifiques éventuels. Un outil moins cher à l’achat mais qui demande un développement pour le poids variable revient plus cher sur la durée."),
 ("Combien de temps dure la mise en place ?",
  "Comptez 4 à 8 semaines entre le cadrage et la bascule sur un périmètre de négoce alimentaire, reprise des données comprise. Ce délai suppose que les processus de la filière soient préconfigurés ; sur un outil généraliste à paramétrer, le projet se compte en mois."),
 ("Peut-on démarrer sur une partie seulement du périmètre ?",
  "Oui, et c’est souvent le bon choix : démarrer sur les achats et les stocks, puis brancher la vente et la facturation une fois les données propres. Cela évite de tout bloquer sur un cas particulier de tarification."),
 ("Faut-il un serveur ?",
  "Plus nécessairement. En mode SaaS, il n’y a pas de serveur à administrer ni de sauvegarde à gérer, les mises à jour sont incluses, et l’accès se fait depuis le bureau comme depuis l’entrepôt."),
 ("Le logiciel fonctionne-t-il sur l’entrepôt ?",
  "C’est un critère à vérifier explicitement. Réception, pesée, préparation et inventaire doivent se faire sur terminal mobile, avec remontée immédiate. Sinon l’information se ressaisit le soir, avec les erreurs que cela suppose."),
 ("Que devient l’historique de l’ancien outil ?",
  "Le catalogue, les tarifs clients, les encours et l’historique des mouvements se reprennent. Ce qui ne se reprend jamais proprement, ce sont les tableurs parallèles : c’est le moment de trancher ce qui fait foi."),
 ("Un TMS peut-il remplacer un logiciel de négoce ?",
  "Non, les deux ne résolvent pas le même problème. Un TMS pilote le transport : où est la marchandise, quels documents l’accompagnent. Il ne calcule ni votre coût de revient, ni votre stock vendable, ni votre marge. Les deux sont complémentaires."),
 ("Comment savoir si l’outil gère vraiment ma filière ?",
  "Faites-lui décrire votre métier avec votre vocabulaire. Si l’interlocuteur parle de freinte, de poids variable, de DLC et de lot d’origine sans que vous ayez à l’expliquer, le produit a probablement été construit pour cette filière."),
]
