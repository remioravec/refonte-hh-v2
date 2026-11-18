#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les reponses de FAQ, reecrites pour le metier de la page.

POURQUOI. Sur cinq pages, les reponses etaient celles d'une autre page,
avec un mot echange. Sur brasseur, « L'ERP permet-il le suivi du malt et du
houblon ? » repondait farine, beurre et levure. Sur poissonnier, « nos
consultants parlent votre langage » etait suivi de melee, boyaux, poussoir
et etuvage — du vocabulaire de charcutier. Un lecteur du metier comprend en
trois lignes que le texte ne lui est pas destine.

TROIS REGLES D'ECRITURE, tenues ligne par ligne.

1. Chaque reponse repond a la question posee, avec le vocabulaire du
   metier de la page et aucun autre.

2. Ce qu'on prete au logiciel vient de ce que la page annonce deja dans sa
   section fonctionnalites. On ne promet rien que les ecrans ne montrent.

3. AUCUN chiffre invente. Les anciennes reponses avançaient des taux de
   perte, des parts de cout matiere et des delais : ils venaient d'un autre
   metier et n'ont pas ete transposes, ils ont ete retires. Les seuls
   elements chiffres ou reglementaires cites sont des faits publics et
   verifiables — le reglement (UE) 1379/2013 pour l'etiquetage des produits
   de la peche, la declaration recapitulative mensuelle et les droits
   d'accises pour la biere, le reglement INCO pour les allergenes.

Les quatre points en attente d'arbitrage — duree de deploiement,
anciennete de l'editeur, nombre de clients, prix — n'apparaissent dans
AUCUNE de ces reponses. Tant qu'ils se contredisent d'une page a l'autre,
les reecrire reviendrait a figer une contradiction.
"""


def _li(paires):
    return "".join("<li><strong>%s</strong> : %s</li>" % (t, d) for t, d in paires)


def _rep(chapo, paires, chute=""):
    return ("<p>%s</p><ul>%s</ul>%s"
            % (chapo, _li(paires), ("<p>%s</p>" % chute) if chute else ""))


# ═══════════════════════════════════════════════════════ TORREFACTEUR
TORREFACTEUR = [
 ("Comment calculer le prix de revient en torréfaction ?",
  _rep("Le coût d'un café torréfié se joue sur trois postes : le café vert, "
       "la freinte de torréfaction et le conditionnement. Hello Harel les "
       "tient ensemble, pour chaque référence.",
   [("Le café vert au lot",
     "chaque sac entre avec son origine, son importateur et son prix payé. "
     "Le coût matière suit le lot réellement utilisé, pas une moyenne."),
    ("La freinte intégrée au rendement",
     "la perte d'eau au grillage est saisie comme un rendement vert vers "
     "torréfié, par profil. Elle entre dans le coût au kilo au lieu d'être "
     "estimée à part."),
    ("Les assemblages",
     "un blend est une recette : ses composants sont valorisés à leur propre "
     "coût, et la modification d'une origine recalcule l'ensemble."),
    ("Le conditionnement",
     "sachet, valve, étiquette et carton sont portés par la fiche du produit "
     "fini, au format vendu."),
    ("La mise à jour au cours",
     "une nouvelle réception de vert à un autre prix met à jour le coût de "
     "revient des références concernées, sans ressaisie.")],
   "La marge se lit ensuite par référence — origine, assemblage, mouture — "
   "et par canal de vente.")),

 ("L'ERP gère-t-il la planification des torréfactions ?",
  _rep("Oui. La contrainte d'un torréfacteur n'est pas le nombre de "
       "commandes, c'est la capacité du tambour et l'enchaînement des lots.",
   [("La charge de l'atelier",
     "les ordres du jour s'affichent avec le taux de charge avant lancement. "
     "On voit ce qui tient dans la journée et ce qui déborde."),
    ("Le lot de torréfaction",
     "chaque passage est un ordre de fabrication : origine ou assemblage, "
     "quantité de vert engagée, profil appliqué, quantité de torréfié "
     "obtenue."),
    ("L'enchaînement",
     "les lots se planifient dans un ordre qui limite les changements de "
     "profil et les nettoyages entre deux origines."),
    ("Le dégazage",
     "le délai entre torréfaction et conditionnement est porté par le "
     "produit, pour que la préparation de commande ne parte pas sur un café "
     "trop frais."),
    ("Les besoins en vert",
     "ils se calculent depuis le plan de torréfaction, pas après coup : on "
     "sait ce qu'il faut commander et quand.")])),

 ("Comment gérer plusieurs points de vente ?",
  _rep("Boutique, site marchand, CHR et clients B2B tirent sur le même "
       "stock. L'ERP le consolide au lieu de le dupliquer.",
   [("Un stock, plusieurs lieux",
     "torréfaction, dépôts et boutiques apparaissent sur un seul écran, avec "
     "les quantités par emplacement."),
    ("Les transferts",
     "un mouvement entre l'atelier et un point de vente est tracé, et le lot "
     "suit — la traçabilité ne s'arrête pas à la porte de l'atelier."),
    ("Les seuils",
     "les références passées sous leur seuil de réassort remontent seules, "
     "par point de vente."),
    ("Les tarifs par canal",
     "le prix d'un même café n'est pas celui de la boutique, du CHR et du "
     "grossiste. Chaque canal a sa grille, appliquée automatiquement."),
    ("Les ventes au même compteur",
     "caisse boutique, commandes web et livraisons professionnelles "
     "alimentent le même suivi de marge.")])),

 ("L'ERP permet-il le suivi des matières premières ?",
  _rep("C'est le cœur du sujet en torréfaction : un café se vend sur son "
       "origine, et cette origine doit être démontrable.",
   [("Le lot de vert",
     "origine, terroir, récolte, importateur, qualité et date de réception "
     "sont portés par le lot, pas par la référence."),
    ("La traçabilité amont",
     "depuis un paquet livré, on remonte au lot de vert et au fournisseur "
     "qui l'a fourni."),
    ("La traçabilité aval",
     "depuis un lot de vert, on obtient la liste des clients servis et des "
     "bons de livraison concernés."),
    ("Les DDM",
     "celles du vert en stock et celles du torréfié conditionné sont suivies "
     "par emplacement, avec alerte à l'approche."),
    ("Les certifications",
     "bio, commerce équitable ou label d'origine sont attachés au lot et "
     "ressortent dans le dossier présenté au certificateur.")])),

 ("Qu'est-ce qu'un ERP torréfaction ?",
  _rep("C'est un logiciel de gestion qui connaît la transformation du café : "
       "un produit qui perd du poids en cuisant, qui change de nom entre "
       "l'entrée et la sortie, et dont la valeur tient à une origine.",
   [("Il raisonne en lots, pas en références",
     "deux sacs de la même origine achetés à deux mois d'écart n'ont ni le "
     "même prix ni la même traçabilité."),
    ("Il gère un rendement",
     "un kilo de vert ne donne pas un kilo de torréfié. Un logiciel "
     "généraliste ne sait pas modéliser cette perte."),
    ("Il connaît les assemblages",
     "un blend est une nomenclature dont un composant peut changer en cours "
     "d'année sans changer la référence vendue."),
    ("Il suit plusieurs canaux",
     "boutique, e-commerce, CHR et B2B, avec des tarifs et des "
     "conditionnements différents."),
    ("Il prépare les contrôles",
     "traçabilité, DDM, allergènes et mentions d'étiquetage sortent du même "
     "dossier.")])),

 ("Pourquoi un ERP plutôt qu'un tableur Excel ?",
  _rep("Un tableur tient tant que l'activité tient dans une tête. Il cède "
       "sur trois points précis, et toujours au même moment.",
   [("Le recalcul",
     "quand un cours du vert bouge, il faut rouvrir chaque fiche. L'ERP "
     "propage la nouvelle valeur à toutes les références concernées."),
    ("La traçabilité",
     "un tableur ne relie pas un bon de livraison à un lot de vert. Le jour "
     "d'un rappel, cette chaîne se reconstitue à la main, classeur par "
     "classeur."),
    ("Le temps réel",
     "le stock d'un tableur est celui de la dernière saisie. Celui de l'ERP "
     "est celui de la dernière réception et de la dernière vente."),
    ("Le travail à plusieurs",
     "deux personnes ne modifient pas le même classeur en même temps sans "
     "écraser le travail de l'autre."),
    ("La mémoire",
     "un ERP conserve l'historique des prix, des rendements et des lots. "
     "Un tableur conserve la dernière version.")],
   "Le tableur garde sa place pour une simulation ponctuelle. Il ne tient "
   "pas le quotidien d'un atelier qui produit et livre tous les jours.")),
]


# ═══════════════════════════════════════════════════════ BRASSEUR
BRASSEUR = [
 ("Comment calculer le prix de revient de mes bières ?",
  _rep("Le coût d'une bière se joue sur le brassin, pas sur la bouteille. "
       "Hello Harel part du brassin et redescend jusqu'au format vendu.",
   [("Les matières au lot",
     "malt, houblon, levure et adjuvants entrent avec leur lot et leur prix "
     "payé. Le coût suit le lot réellement empâté."),
    ("Le rendement brassicole",
     "les volumes sont saisis à chaque étape — moût chaud, moût froid, après "
     "garde, après soutirage. Les pertes entrent dans le coût au litre au "
     "lieu d'être ignorées."),
    ("Le conditionnement par format",
     "fût, bouteille, canette et bag-in-box n'ont ni le même contenant ni le "
     "même coût de ligne. Chaque format porte le sien."),
    ("Les droits d'accises",
     "ils dépendent du volume et du titre alcoométrique. Ils se calculent "
     "sur les quantités réellement mises en circulation, pas sur une "
     "estimation."),
    ("La mise à jour",
     "un nouveau prix de malt ou de houblon recalcule les recettes "
     "concernées sans ressaisie.")],
   "La marge se lit ensuite par recette et par format, et non sur une "
   "moyenne de brasserie.")),

 ("L'ERP gère-t-il les recettes et les brassins ?",
  _rep("Oui, et il les distingue : la recette est le modèle, le brassin est "
       "ce qui a réellement été produit ce jour-là.",
   [("La recette",
     "profil d'eau, malts et houblons avec leurs quantités, levure, "
     "températures et durées de palier. C'est elle qui sert de référence."),
    ("Le brassin",
     "chaque production est un ordre de fabrication rattaché à une recette, "
     "avec les lots de matières réellement engagés et les volumes obtenus."),
    ("Les cuves comme emplacements",
     "on sait quelle bière est dans quelle cuve, depuis quand, et jusqu'à "
     "quand elle doit y rester."),
    ("Les étapes",
     "empâtage, houblonnage, fermentation, garde et soutirage sont des "
     "jalons datés du brassin, pas des cases à cocher."),
    ("Les écarts",
     "quand un brassin sort en dessous du volume prévu, l'écart est visible "
     "sur le brassin, pas noyé dans un total mensuel.")])),

 ("Comment gérer plusieurs points de vente ?",
  _rep("CHR, cavistes, boutique et site marchand tirent sur le même stock, "
       "avec des conditions différentes. L'ERP tient les deux.",
   [("Un stock, plusieurs lieux",
     "brasserie, dépôts et boutique apparaissent sur un seul écran, avec les "
     "quantités par emplacement et par format."),
    ("Les tarifs par canal",
     "le prix d'un fût pour un bar n'est pas celui d'une bouteille en "
     "boutique. Chaque canal a sa grille."),
    ("Les consignes",
     "fûts et bouteilles consignés sont suivis par client : ce qui est sorti, "
     "ce qui est revenu, ce qui manque."),
    ("Les transferts",
     "un mouvement entre la brasserie et un point de vente est tracé, et le "
     "lot suit avec lui."),
    ("Les encours",
     "l'ancienneté de la relation et les retards de règlement s'affichent sur "
     "la fiche du client, pas dans un tableur à part.")])),

 ("L'ERP permet-il le suivi du malt et du houblon ?",
  _rep("Oui, au lot. C'est ce qui permet de remonter d'une bouteille à son "
       "sac de malt et à sa variété de houblon.",
   [("Le lot de matière",
     "fournisseur, numéro de lot, date de réception, DDM et quantité "
     "restante sont portés par le lot, pas par la référence."),
    ("Les conditions de stockage",
     "les emplacements du malt et du houblon ont leur consigne de "
     "température, avec relevé courant et alerte au dépassement."),
    ("La traçabilité amont",
     "depuis un brassin, on obtient la liste des lots de matières qui y sont "
     "entrés."),
    ("La traçabilité aval",
     "depuis un lot de malt ou de houblon, on obtient les brassins produits "
     "et les clients livrés."),
    ("Le réapprovisionnement",
     "il se déclenche au seuil et non à la rupture, ce qui compte pour un "
     "houblon dont la variété n'est pas substituable.")])),

 ("Qu'est-ce qu'un ERP brasserie ?",
  _rep("C'est un logiciel de gestion qui connaît la fabrication de la bière "
       "et les obligations qui vont avec : un produit qui fermente, qui "
       "occupe une cuve pendant des semaines, et qui est soumis à accises.",
   [("Il raisonne en brassins",
     "l'unité de production n'est pas la bouteille, c'est le brassin — avec "
     "son volume, ses lots et son rendement propre."),
    ("Il gère les cuves",
     "une cuve est un emplacement occupé dans le temps, pas une simple "
     "quantité en stock."),
    ("Il tient les accises",
     "déclaration récapitulative mensuelle, droits dus et mouvements en "
     "suspension se calculent sur les quantités réelles."),
    ("Il suit les consignes",
     "le parc de fûts est un actif qui circule et revient, ce qu'un logiciel "
     "généraliste ne sait pas modéliser."),
    ("Il gère le multi-format",
     "une même recette se vend en fût, en bouteille et en canette, avec des "
     "coûts et des DDM différents.")])),

 ("Pourquoi un ERP plutôt qu'un tableur Excel ?",
  _rep("Un tableur tient tant que la brasserie tient dans une tête. Il cède "
       "sur des points précis, et toujours au mauvais moment.",
   [("Le recalcul",
     "un nouveau prix de malt oblige à rouvrir chaque recette. L'ERP le "
     "propage à toutes les bières concernées."),
    ("La traçabilité",
     "un tableur ne relie pas une palette livrée à un lot de houblon. Le jour "
     "d'un rappel, cette chaîne se reconstitue à la main."),
    ("Les cuves",
     "l'occupation des cuves se gère mal dans une grille : c'est une "
     "contrainte de temps, pas une quantité."),
    ("Les accises",
     "une déclaration se construit sur des mouvements datés. Un tableau "
     "recopié en fin de mois est une source d'erreur."),
    ("Le travail à plusieurs",
     "deux personnes ne modifient pas le même classeur en même temps sans "
     "écraser le travail de l'autre.")],
   "Le tableur reste utile pour une simulation. Il ne tient pas une "
   "brasserie qui produit, conditionne et livre chaque semaine.")),
]


# ═══════════════════════════════════════════════════════ CHOCOLATIER
CHOCOLATIER = [
 ("Comment calculer le prix de revient au gramme en chocolaterie ?",
  _rep("En chocolaterie, le coût se joue au gramme : quelques grammes de "
       "couverture en plus par bonbon changent la marge d'une production "
       "entière. Hello Harel calcule à cette maille.",
   [("La recette au gramme",
     "couverture, praliné, fruits secs, alcools et arômes sont saisis avec "
     "leurs quantités exactes. Le coût matière du bonbon en découle."),
    ("Les sous-recettes",
     "une ganache ou un praliné utilisé dans plusieurs produits est valorisé "
     "une fois. Si son coût bouge, tous les produits qui l'emploient "
     "suivent."),
    ("Les pertes",
     "les pertes de tempérage et d'enrobage sont intégrées au rendement de "
     "la recette, et non retranchées après coup."),
    ("Les coffrets",
     "un assortiment est une nomenclature d'assemblage : son coût est la "
     "somme de ses bonbons, plus l'emballage."),
    ("Le cours du cacao",
     "une nouvelle réception de couverture à un autre prix recalcule les "
     "références concernées sans ressaisie.")],
   "La marge se lit ensuite par référence — bonbon, tablette, coffret — et "
   "par point de vente.")),

 ("L'ERP gère-t-il les recettes et le tempérage ?",
  _rep("Oui. La recette porte la matière, et le tempérage est suivi comme "
       "une étape de production avec ses contrôles.",
   [("La fiche recette",
     "composants, quantités au gramme, sous-recettes et rendement attendu. "
     "C'est elle qui sert de référence à chaque production."),
    ("La courbe de tempérage",
     "températures de fonte, de cristallisation et de travail sont portées "
     "par la recette, et les relevés réels sont consignés sur l'ordre de "
     "fabrication."),
    ("Le plan de production",
     "les ordres du jour s'affichent avec le taux de charge de l'atelier "
     "avant lancement — ce qui compte quand une enrobeuse est le goulot."),
    ("Les besoins matière",
     "ils se calculent depuis le plan, pas après : on sait ce qu'il faut "
     "sortir de la réserve avant de commencer."),
    ("La saisonnalité",
     "les pics de Pâques et de Noël se lissent sur les semaines qui "
     "précèdent, au lieu de se découvrir la veille.")])),

 ("Comment gérer plusieurs points de vente ?",
  _rep("Atelier, boutiques, corners et site marchand tirent sur la même "
       "production. L'ERP les met sur un seul compteur.",
   [("Un stock, plusieurs lieux",
     "atelier, boutiques et corners apparaissent sur un seul écran, avec les "
     "quantités par emplacement."),
    ("Les transferts",
     "un mouvement de l'atelier vers une boutique est tracé, et le lot suit "
     "— la DLC d'une ganache ne s'arrête pas à la porte du laboratoire."),
    ("Les seuils",
     "les références sous leur seuil de réassort remontent seules, par point "
     "de vente."),
    ("Les tarifs par canal",
     "boutique, corner et vente professionnelle n'ont pas la même grille. "
     "Chacune est appliquée automatiquement."),
    ("Les ventes consolidées",
     "caisse, commandes web et ventes professionnelles alimentent le même "
     "suivi de marge.")])),

 ("L'ERP permet-il le suivi des matières premières ?",
  _rep("Oui, au lot — ce qui compte pour des matières dont la DLC va de "
       "quelques jours à plusieurs mois selon le produit.",
   [("Le lot de matière",
     "couverture, praliné, fruits secs et alcools entrent avec leur "
     "fournisseur, leur numéro de lot et leur date limite."),
    ("Les conditions de stockage",
     "chaque emplacement a sa consigne de température, avec relevé courant "
     "et alerte au dépassement — un chocolat qui blanchit est une perte "
     "sèche."),
    ("Les DLC et DDM",
     "les ganaches fraîches et les tablettes ne se suivent pas de la même "
     "façon. Chaque produit porte la sienne."),
    ("L'origine",
     "l'origine des fèves et les certifications sont attachées au lot et "
     "ressortent dans le dossier de contrôle."),
    ("La traçabilité",
     "depuis un coffret livré, on remonte aux lots de couverture qui y sont "
     "entrés, et inversement.")])),

 ("Qu'est-ce qu'un ERP chocolaterie ?",
  _rep("C'est un logiciel de gestion qui connaît le travail du chocolat : "
       "une matière sensible à la température, des recettes au gramme, et "
       "une activité dont une large part se joue sur quelques semaines.",
   [("Il calcule au gramme",
     "la maille du coût n'est pas le kilo, c'est le bonbon."),
    ("Il gère les sous-recettes",
     "ganaches et pralinés sont des produits intermédiaires valorisés une "
     "fois et employés partout."),
    ("Il gère les assortiments",
     "un coffret est une nomenclature à quantités variables, pas une "
     "référence simple."),
    ("Il surveille les températures",
     "les consignes de stockage et les relevés font partie du dossier de "
     "production, pas d'un cahier à part."),
    ("Il absorbe la saison",
     "le plan de production se construit sur les semaines qui précèdent le "
     "pic, avec la charge de l'atelier comme contrainte.")])),

 ("Pourquoi un ERP plutôt qu'un tableur Excel ?",
  _rep("Un tableur tient tant que l'atelier tient dans une tête. Il cède sur "
       "des points précis, et toujours en pleine saison.",
   [("Le recalcul",
     "un nouveau prix de couverture oblige à rouvrir chaque fiche. L'ERP le "
     "propage à toutes les recettes qui l'emploient, sous-recettes "
     "comprises."),
    ("Les sous-recettes",
     "une ganache utilisée dans quinze produits se gère mal dans une grille. "
     "C'est une arborescence, pas une ligne."),
    ("La traçabilité",
     "un tableur ne relie pas un coffret livré à un lot de couverture. Le "
     "jour d'un rappel, cette chaîne se reconstitue à la main."),
    ("Le temps réel",
     "le stock d'un tableur est celui de la dernière saisie. En décembre, "
     "cet écart coûte cher."),
    ("Le travail à plusieurs",
     "deux personnes ne modifient pas le même classeur en même temps sans "
     "écraser le travail de l'autre.")],
   "Le tableur garde sa place pour une simulation. Il ne tient pas un "
   "atelier qui produit et livre tous les jours.")),
]


# ═══════════════════════════════════════════════════════ POISSONNIER
POISSONNIER = [
 ("L'ERP peut-il calculer mes rendements au filetage ?",
  _rep("Oui, et c'est la mesure qui décide de la marge en poissonnerie : "
       "entre le poisson entier acheté et le filet vendu, le poids change "
       "plusieurs fois.",
   [("Les pesées successives",
     "poids à la réception, poids après parage et poids du filet sont saisis "
     "sur le même lot. Le rendement se déduit des pesées, pas d'un "
     "barème."),
    ("Le rendement par espèce",
     "il se suit espèce par espèce, et se compare d'un arrivage à l'autre. "
     "Un écart se voit sur le lot concerné."),
    ("Le glaçage",
     "le poids net égoutté est distingué du poids brut, ce qui évite de "
     "vendre de l'eau au prix du poisson."),
    ("Les coproduits",
     "têtes, arêtes et parures sont valorisés ou constatés en perte, au lieu "
     "de disparaître du calcul."),
    ("Le coût réel",
     "le coût du filet intègre le prix payé à la criée et le rendement "
     "constaté, pas une moyenne de saison.")])),

 ("Peut-on lancer des promotions sur produits proches DLC ?",
  _rep("Oui, et c'est le levier le plus direct contre la démarque quand les "
       "DLC se comptent en jours.",
   [("L'alerte",
     "les lots qui approchent de leur date limite remontent seuls, avec le "
     "nombre de jours restants."),
    ("La promotion ciblée",
     "elle porte sur les lots concernés et pas sur la référence entière : le "
     "poisson arrivé ce matin ne part pas au prix de celui d'avant-hier."),
    ("L'étiquette",
     "une étiquette dédiée est générée pour le lot en promotion, avec le "
     "prix appliqué."),
    ("Le suivi",
     "ce qui est parti en promotion et ce qui a été jeté se comptent "
     "séparément, ce qui permet de mesurer le gain réel."),
    ("La règle de sortie",
     "les lots se servent dans l'ordre de leur date limite, sans dépendre de "
     "la mémoire de l'équipe.")])),

 ("L'ERP gère-t-il l'étiquetage et l'origine du poisson ?",
  _rep("Oui. Les mentions obligatoires des produits de la pêche sont portées "
       "par le lot, et ressortent sur l'étiquette sans ressaisie. Le "
       "règlement (UE) 1379/2013 en fixe la liste.",
   [("La dénomination",
     "la dénomination commerciale et le nom scientifique de l'espèce "
     "accompagnent chaque lot."),
    ("La méthode de production",
     "pêché en mer, pêché en eau douce ou élevé — la mention suit le lot et "
     "ne se choisit pas à l'impression."),
    ("La zone de capture",
     "la zone FAO, et le cas échéant la sous-zone, sont attachées au lot dès "
     "l'achat."),
    ("L'engin de pêche",
     "la catégorie d'engin est portée par le lot pour les produits "
     "concernés."),
    ("L'étiquette générée",
     "elle reprend ces mentions telles qu'elles ont été saisies à l'achat, "
     "ce qui supprime la recopie et l'erreur qui va avec.")])),

 ("Comment éviter un rappel produit total ?",
  _rep("Un rappel total arrive quand on ne sait pas dire précisément qui a "
       "reçu quoi. La traçabilité au lot transforme un rappel de gamme en "
       "rappel de lot.",
   [("La traçabilité aval",
     "depuis un lot, on obtient la liste des clients servis, les quantités "
     "et les bons de livraison correspondants."),
    ("La traçabilité amont",
     "depuis un produit fini, on remonte au lot acheté, au fournisseur et à "
     "la marée concernée."),
    ("Les transformations",
     "filetage, fumage ou marinade créent un nouveau lot rattaché au lot "
     "d'origine. La chaîne ne se coupe pas à la transformation."),
    ("Les registres",
     "températures, nettoyages et contrôles sont consignés au même endroit "
     "que les lots, ce que demande un contrôle sanitaire."),
    ("Le dossier",
     "l'ensemble se sort en quelques clics, au moment où l'on n'a pas le "
     "temps de le reconstituer.")])),

 ("Qu'est-ce qu'un ERP poissonnier et pourquoi en avoir un ?",
  _rep("C'est un logiciel de gestion qui connaît le produit de la mer : un "
       "poids qui varie à chaque étape, une date limite très courte et des "
       "mentions d'étiquetage imposées par la réglementation.",
   [("Il gère le poids variable",
     "un lot ne se compte pas en pièces mais en kilos, et ces kilos changent "
     "entre la réception et la vente."),
    ("Il raisonne en marées",
     "l'achat à la criée, le prix du jour et la qualité de l'arrivage "
     "conditionnent la marge de la journée."),
    ("Il porte les mentions obligatoires",
     "espèce, nom scientifique, méthode de production, zone de capture et "
     "engin suivent le lot jusqu'à l'étiquette."),
    ("Il surveille les DLC",
     "quelques jours d'écart séparent une vente d'une perte. Les alertes "
     "sont quotidiennes, pas hebdomadaires."),
    ("Il prépare les contrôles",
     "traçabilité, registres sanitaires et dossier de rappel sortent du même "
     "endroit.")])),

 ("Hello Harel vs un ERP généraliste pour la poissonnerie ?",
  _rep("Un ERP généraliste sait gérer des références et des quantités. Il ne "
       "sait pas gérer un produit dont le poids et la date limite bougent.",
   [("Le poids variable",
     "il faut le modéliser à l'achat, à la transformation et à la vente. "
     "Ajouter un champ à un logiciel généraliste ne suffit pas."),
    ("Le rendement",
     "un ERP généraliste ne sait pas qu'un poisson entier de dix kilos donne "
     "moins de dix kilos de filet, ni mesurer l'écart."),
    ("L'étiquetage réglementaire",
     "les mentions des produits de la pêche ne sont pas des champs libres : "
     "elles doivent suivre le lot et ressortir à l'impression."),
    ("Les DLC courtes",
     "une alerte mensuelle ne sert à rien quand la marchandise se périme en "
     "trois jours."),
    ("Le paramétrage",
     "ce qui manque à un logiciel généraliste se rattrape en développement "
     "spécifique, avec le coût et la fragilité que cela suppose.")])),
]


# ═══════════════════════════════════════════════════════ CONSERVERIE
CONSERVERIE = [
 ("Comment gérer les recettes multi-niveaux en conserves ?",
  _rep("Une conserve est rarement une recette plate : une préparation entre "
       "dans une autre, qui entre elle-même dans le produit appertisé. "
       "Hello Harel gère cette arborescence sans limite de niveaux.",
   [("Les nomenclatures multi-niveaux",
     "une sauce, une garniture ou un bouillon sont des produits "
     "intermédiaires avec leur propre fiche et leur propre coût."),
    ("La valorisation une seule fois",
     "une préparation employée dans plusieurs références est calculée une "
     "fois. Si son coût bouge, toutes les références qui l'emploient "
     "suivent."),
    ("Les substitutions",
     "remplacer une matière par une autre montre son impact sur le prix de "
     "revient avant de décider, pas après."),
    ("Le rendement par étape",
     "les pertes de parage, de cuisson et de remplissage sont portées au "
     "niveau où elles se produisent."),
    ("Le format",
     "boîte, bocal ou poche n'ont ni le même contenant ni le même "
     "remplissage. Chaque format porte son coût.")])),

 ("L'ERP gère-t-il les commandes GMS et l'étiquetage INCO ?",
  _rep("Oui, et ce sont deux exigences qui vont ensemble : une enseigne "
       "commande par EDI et refuse une palette mal étiquetée.",
   [("Les commandes EDI",
     "les commandes des enseignes sont intégrées sans ressaisie, avec leurs "
     "références et leurs délais."),
    ("Le colisage",
     "la palettisation et les étiquettes logistiques sont générées depuis la "
     "préparation réelle, pas depuis un modèle."),
    ("Les mentions INCO",
     "liste des ingrédients, allergènes mis en évidence, valeurs "
     "nutritionnelles et DDM sortent de la fiche produit."),
    ("Les cahiers des charges",
     "une même recette produite en marque propre et en marque de "
     "distributeur porte deux étiquetages distincts."),
    ("Les documents",
     "bons de livraison, étiquettes et documents d'accompagnement sont "
     "générés au même moment, à partir des mêmes données.")])),

 ("Comment optimiser mes coûts de production ?",
  _rep("En conserverie, le coût se construit sur une campagne : une matière "
       "disponible quelques semaines est transformée pour l'année. Ce qui se "
       "mesure se pilote.",
   [("Le prix de revient en temps réel",
     "il se recalcule à chaque réception de matière et à chaque changement "
     "de recette, à tous les niveaux de la nomenclature."),
    ("Le rendement matière",
     "l'écart entre la quantité engagée et la quantité obtenue se suit par "
     "lot de fabrication, pas en fin de mois."),
    ("La charge d'atelier",
     "les ordres se planifient avec la capacité des cuiseurs et des "
     "autoclaves comme contrainte, ce qui évite les à-coups."),
    ("Les substitutions",
     "l'impact d'un changement de matière est visible avant arbitrage."),
    ("La marge par référence",
     "elle se lit produit par produit et format par format, au lieu d'une "
     "moyenne qui masque les références déficitaires.")])),

 ("Comment gérer les allergènes sur des produits complexes ?",
  _rep("Un produit appertisé peut compter des dizaines d'ingrédients répartis "
       "sur plusieurs niveaux de recette. Déclarer les allergènes à la main "
       "est une source d'erreur, et l'erreur se paie en rappel.",
   [("La remontée automatique",
     "l'allergène déclaré sur une matière première remonte à toutes les "
     "préparations et à tous les produits finis qui l'emploient."),
    ("Les niveaux",
     "un allergène présent dans une sauce entrant dans un plat entrant dans "
     "une conserve reste visible jusqu'à l'étiquette."),
    ("Les traces",
     "l'ingrédient volontairement ajouté et la trace possible liée à la "
     "ligne sont distingués, comme le demande la réglementation."),
    ("Le changement de fournisseur",
     "une nouvelle fiche matière met à jour les déclarations des produits "
     "concernés, sans reprendre chaque étiquette."),
    ("L'étiquette générée",
     "les allergènes y sont mis en évidence automatiquement, dans la liste "
     "des ingrédients.")])),

 ("Qu'est-ce qu'un ERP pour conserves ?",
  _rep("C'est un logiciel de gestion qui connaît l'appertisation : un "
       "traitement thermique qui rend le produit stable à température "
       "ambiante, avec une date de durabilité minimale qui se compte en "
       "années.",
   [("Il suit la charge d'autoclave",
     "le traitement thermique porte un numéro de charge, rattaché aux lots "
     "de produits finis qui l'ont subi."),
    ("Il gère les barèmes",
     "le barème de stérilisation appliqué fait partie du dossier de "
     "fabrication, au même titre que la recette."),
    ("Il raisonne en DDM longues",
     "un stock stable sur plusieurs années ne se pilote pas comme un stock "
     "frais : la rotation et les alertes n'ont pas la même échelle."),
    ("Il gère les campagnes",
     "une matière disponible quelques semaines par an impose de produire "
     "pour douze mois de vente, avec le stock que cela suppose."),
    ("Il tient les nomenclatures profondes",
     "plusieurs niveaux de préparation entre la matière première et la "
     "boîte.")])),

 ("Quels avantages vs une solution ERP non spécialisée ?",
  _rep("Un ERP généraliste sait gérer des articles et des commandes. Il ne "
       "connaît ni le traitement thermique, ni les nomenclatures profondes, "
       "ni les obligations d'étiquetage alimentaire.",
   [("La charge d'autoclave",
     "c'est un objet de production à part entière, rattaché à des lots. Un "
     "logiciel généraliste n'a pas cette notion."),
    ("Les nomenclatures profondes",
     "au-delà de deux niveaux, la propagation des coûts et des allergènes "
     "devient un développement spécifique."),
    ("Les allergènes",
     "leur remontée automatique à travers les niveaux n'est pas une option "
     "d'un ERP généraliste."),
    ("L'EDI des enseignes",
     "les formats et les exigences de la grande distribution demandent un "
     "paramétrage métier, pas un connecteur générique."),
    ("Le vocabulaire",
     "un interlocuteur qui parle de barème, de valeur stérilisatrice et de "
     "DDM comprend la question avant qu'on ait fini de la poser.")])),
]


# Le lien vers le hub des fonctionnalites vivait dans les anciennes
# reponses. Il revient dans la definition du metier, avec une ancre
# exacte, contiguë et differente d'une page a l'autre — jamais un
# « cliquez ici ».
_HUB = {
 "torrefacteur": "Le détail de ce que couvre l'outil se lit sur la page des "
                 "<a href=\"/fonctionnalites/\">fonctionnalités de l'ERP "
                 "agroalimentaire</a>.",
 "brasseur": "Le périmètre complet est décrit sur la page des "
             "<a href=\"/fonctionnalites/\">modules de l'ERP agroalimentaire</a>.",
 "chocolatier": "Ce que chaque module couvre est détaillé sur la page des "
                "<a href=\"/fonctionnalites/\">fonctionnalités de l'ERP "
                "agroalimentaire</a>.",
 "poissonnier": "Le détail module par module figure sur la page des "
                "<a href=\"/fonctionnalites/\">fonctionnalités de l'ERP "
                "agroalimentaire</a>.",
 "conserverie": "Le périmètre fonctionnel est décrit sur la page des "
                "<a href=\"/fonctionnalites/\">modules de l'ERP agroalimentaire</a>.",
}


def _avec_hub(bloc, cle):
    """Ajoute la phrase de renvoi a la reponse qui definit le metier."""
    out = []
    for q, r in bloc:
        if q.startswith("Qu'est-ce qu'un ERP"):
            r = r + "<p>%s</p>" % _HUB[cle]
        out.append((q, r))
    return out


TORREFACTEUR = _avec_hub(TORREFACTEUR, "torrefacteur")
BRASSEUR = _avec_hub(BRASSEUR, "brasseur")
CHOCOLATIER = _avec_hub(CHOCOLATIER, "chocolatier")
POISSONNIER = _avec_hub(POISSONNIER, "poissonnier")
CONSERVERIE = _avec_hub(CONSERVERIE, "conserverie")

PAGES = {10935: ("torrefacteur", TORREFACTEUR),
         10896: ("brasseur", BRASSEUR),
         10894: ("chocolatier", CHOCOLATIER),
         10868: ("poissonnier", POISSONNIER),
         10933: ("conserverie", CONSERVERIE)}

# Les mots qui n'ont rien a faire sur chaque page — le controle qui aurait
# du exister des le debut.
INTRUS = {
 "torrefacteur": ["baguette", "croissant", "pain au chocolat", "petrissage",
                  "patisserie", "feuilletee", "farine", "boulanger", "levure"],
 "brasseur": ["baguette", "croissant", "petrissage", "feuilletee", "farine",
              "boulanger", "patissier", "ganache", "four "],
 "chocolatier": ["baguette", "croissant", "petrissage", "feuilletee", "farine",
                 "boulanger", "brassin", "houblon", "malt"],
 "poissonnier": ["melee", "boyaux", "poussoir", "etuvage", "jambon", "rillettes",
                 "saucisson", "porc", "charcuterie"],
 "conserverie": ["hachis", "lasagnes", "bechamel", "gratin", "farine",
                 "chaine du froid", "surgele"],
}


def sans_accent(t):
    for a, b in zip("éèêëàâçôöûüîï", "eeeeaacoouuii"):
        t = t.replace(a, b)
    return t.lower()


def controler():
    pb = []
    for pid, (nom, L) in PAGES.items():
        if len(L) != 6:
            pb.append("%s : %d reponses au lieu de 6" % (nom, len(L)))
        for q, r in L:
            t = sans_accent(r)
            for mot in INTRUS[nom]:
                if sans_accent(mot) in t:
                    pb.append("%s : %r dans « %s »" % (nom, mot, q[:40]))
            if len(r) < 500:
                pb.append("%s : reponse trop courte pour « %s »" % (nom, q[:40]))
    return pb


if __name__ == "__main__":
    import re
    pb = controler()
    for x in pb:
        print("   !", x)
    for pid, (nom, L) in PAGES.items():
        n = [len(re.sub(r"<[^>]+>", "", r)) for _, r in L]
        print("%-14s %d reponses · %d a %d caracteres" % (nom, len(L), min(n), max(n)))
    print("\ncontrole :", "aucun mot d'un autre metier" if not pb
          else "%d ecart(s)" % len(pb))
