# -*- coding: utf-8 -*-
"""Contenu de la refonte — /blog/calculer-le-prix-de-revient-en-boulangerie/
Cible « logiciel prix de revient ». Donnees du releve SERP du 27/08/2026."""

# --- le comparatif, releve sur la SERP du 27/08/2026 (module 4, triable) ---
SOLUTIONS = [
 # nom, type, gratuit(0/1), pour qui, maj_auto(0/1)
 ("Simulateur de cette page", "Calculateur en ligne", 1, "Vérifier une recette, sans inscription", 0),
 ("Modèle de tableur", "Feuille de calcul", 1, "Quelques recettes, prix stables", 0),
 ("Yokitup", "Logiciel de restauration", 1, "Restauration, fiches techniques", 0),
 ("INBP-CR", "Logiciel de coût de revient", 0, "Boulangerie-pâtisserie artisanale", 0),
 ("Otami", "Logiciel de gestion des achats", 0, "Boulangerie, pâtisserie, restauration", 1),
 ("Quantara", "Module coût de revient", 0, "Boulangerie, pâtisserie, chocolaterie", 0),
 ("incwo", "Application de gestion", 0, "TPE et PME, tous secteurs", 1),
 ("Hello Harel", "ERP agroalimentaire", 0, "PME agroalimentaires, 20 à 300 salariés", 1),
]

# --- FAQ : questions PAA relevees mot pour mot le 27/08/2026 + questions metier ---
FAQ = [
 ("Quelle est la formule pour calculer le prix de revient ?",
  "Prix de revient = matières premières consommées + pertes et freinte + main-d’œuvre de production + énergie + quote-part de frais fixes, le tout rapporté à la quantité <em>réellement</em> produite. Le piège le plus fréquent est d’oublier la freinte : à la cuisson, un kilo de pâte crue ne donne pas un kilo de produit fini, donc le coût au kilo vendu est toujours supérieur au coût au kilo produit."),
 ("Quel logiciel gratuit puis-je utiliser pour calculer le prix de revient des recettes de pâtisserie ?",
  "En pratique le gratuit se limite à trois options : un simulateur en ligne comme celui de cette page, un modèle de tableur, ou la version gratuite d’un logiciel de restauration comme Yokitup. Les solutions dédiées à la boulangerie-pâtisserie — INBP-CR, Otami, Quantara — sont toutes payantes. Le simulateur suffit pour vérifier une recette ; au-delà d’une trentaine de fiches à conserver et à mettre à jour, il faut un outil qui garde l’historique."),
 ("Comment calculer le coût de revient dans Excel ?",
  "Une colonne par poste — matière, perte, main-d’œuvre, énergie, frais fixes — une ligne par ingrédient, et un total rapporté à la quantité produite. Le tableur calcule très bien : sa limite n’est pas le calcul mais la <strong>mise à jour</strong>, puisqu’il faut ressaisir chaque nouveau tarif fournisseur dans toutes les fiches concernées."),
 ("Quel est le meilleur logiciel de calcul de prix de revient ?",
  "Il n’y a pas de meilleur absolu, il y a un seuil. En dessous d’une trentaine de références avec des prix stables, un simulateur ou un tableur suffisent. Au-delà, ou dès que les tarifs fournisseurs bougent plusieurs fois par trimestre, il faut un outil qui recalcule seul : c’est ce que font Otami, incwo ou un ERP. Le tableau ci-dessus classe les solutions relevées sur cette recherche selon ce critère."),
 ("À partir de quand un logiciel devient-il rentable ?",
  "Le seuil n’est pas le chiffre d’affaires mais le produit du nombre de références par la fréquence de changement des prix. Dix recettes et des tarifs annuels : le tableur tient. Cinquante références et des tarifs trimestriels, c’est 200 mises à jour par an — le temps de ressaisie dépasse le coût de l’outil, et l’écart de marge sur des coûts périmés le dépasse encore plus vite."),
 ("Faut-il inclure le salaire du dirigeant dans le prix de revient ?",
  "Oui dès qu’il produit. La règle est simple : tout temps passé à fabriquer entre dans le coût de revient, quel que soit le statut de la personne. Ne pas le compter donne un coût artificiellement bas, et une marge qui n’existe que sur le papier."),
]

# --- les postes du calcul (module 5, valeurs par defaut reelles et cohérentes) ---
DEFAUTS = {
 "matieres": 12.40,   # € de matières pour la fournée
 "quantite": 100,     # pièces produites
 "perte": 8,          # % de freinte
 "temps": 45,         # minutes de production
 "taux": 24.00,       # € / h chargé
 "fixes": 6.00,       # € de frais fixes imputés
}
