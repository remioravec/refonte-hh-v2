# Marque test — structure Hn et titles

Cocon : https://claude.ai/artifact/B6hw3b7JU6FjiFdJYqWHKJ
79 pages · 581 liens internes · 581 ancres uniques · tous les seuils 3.3 tenus.
DA : 7shifts (indigo #4570ff action, orange #ff6808 accent, lime #c6ff94 sur fond sombre).

**Le produit derrière est celui du client. Son nom n'apparaît nulle part sur le site public.**

---

## 1 · Les cinq gabarits Hn

### Mère — `/`
```
H1  L'ERP agroalimentaire quand le poids, la date et le lot décident du prix
H2  Pourquoi un ERP généraliste ne suffit pas en agroalimentaire
    H3  Le poids variable
    H3  La date de vie du produit
    H3  Le numéro de lot
H2  Comment le lot remonte de la matière première au produit fini
    H3  À la réception · H3 En stock · H3 En fabrication · H3 À l'expédition
H2  Comment suivre la marge quand le poids varie
    H3  Le coût de revient réel · H3 L'écart de facturation
H2  Le logiciel est-il compatible avec la facturation électronique
    H3  Factur-X · H3 Chorus Pro
H2  Quel métier, quel paramétrage
    H3  Transformation · H3 Produits frais · H3 Boissons et épicerie
H2  Combien ça coûte et en combien de temps c'est déployé
    H3  Les licences · H3 L'atelier de conception
```
Les six H2 sont les six questions que les demandes reçues posent le plus souvent.

### Hub — `/metiers/` et `/fonctionnalites/`
```
H1  L'ERP agroalimentaire, métier par métier
H2  Transformation          H3 × 5 métiers
H2  Produits frais          H3 × 4 métiers
H2  Boissons et épicerie    H3 × 3 métiers
H2  Ce qui change d'un métier à l'autre
H2  Ce qui ne change pas
```

### Fille métier — `/metiers/{slug}/`
```
H1  {promesse métier, requête exacte en tête}
H2  {sous-fonctionnalité 1}   → lien vers sa petite-fille
H2  {sous-fonctionnalité 2}   → lien vers sa petite-fille
H2  {sous-fonctionnalité 3}   → lien vers sa petite-fille
H2  {sous-fonctionnalité 4}   → lien vers sa petite-fille
H2  Ce que le socle apporte à tous les métiers
H2  Questions de la filière
```

### Fille fonctionnalité — `/fonctionnalites/{slug}/`
```
H1  {fonctionnalité, requête exacte}
H2  Ce que ça règle
H2  En {métier A}   H2  En {métier B}   H2  En {métier C}   H2  En {métier D}
H2  Comment c'est paramétré
H2  Questions
```

### Petite-fille — `/metiers/{slug}/{sous}/`
```
Réponse en 2 à 3 phrases, avant tout le reste, écrite pour l'extrait et l'aperçu IA
H1  {sous-fonctionnalité} {métier}
H2  La question précise
H2  La méthode
H2  Le cas limite
```
Les quatre modules NavBoost sont présents ici aussi : sommaire, simulateur, FAQ, quiz.

---

## 2 · Les 31 titles, mesurés

Règle 1 : exact match le plus tôt possible, 200 à 561 px.
Colonne « reste » = place disponible pour « • MARQUE » une fois le nom choisi
(« • Lotrace » coûte 68 px, à titre d'exemple).

| px | reste | Page | Title |
|---:|---:|---|---|
| 343 | 218 | `/` | ERP agroalimentaire : lots, DLC et coût de revient |
| 370 | 190 | `/metiers/` | ERP agroalimentaire par métier : 12 filières couvertes |
| 370 | 192 | `/fonctionnalites/` | Fonctionnalités ERP agroalimentaire : les 14 modules |
| 348 | 213 | `/contact/` | Démo ERP agroalimentaire sur vos propres articles |
| 420 | 140 | boulangerie-patisserie | Logiciel de gestion boulangerie : coût de revient et fournées |
| 402 | 158 | chocolaterie | Logiciel de gestion chocolaterie : coût matière au gramme |
| 418 | 142 | glacerie | Logiciel de gestion glacier : coût au litre et chaîne du froid |
| 410 | 150 | charcuterie-salaison | Logiciel de gestion charcuterie : lots et rendement matière |
| 426 | 134 | viande-decoupe | Logiciel de gestion filière viande : rendement pièce par pièce |
| 364 | 197 | maree-poissonnerie | Logiciel de gestion mareyage : criée, agréage et DLC |
| 386 | 175 | fruits-et-legumes | Logiciel de gestion fruits et légumes : cours et agréage |
| 367 | 194 | fromagerie-laitiere | Logiciel de gestion fromagerie : collecte et affinage |
| 359 | 202 | traiteur-plats-cuisines | Logiciel de gestion traiteur : recettes et allergènes |
| 383 | 178 | conserverie | Logiciel de gestion conserverie : recettes, lots et DDM |
| 412 | 149 | brasserie-boissons | Logiciel de gestion brasserie : coût du brassin et consigne |
| 421 | 140 | torrefaction | Logiciel de gestion torréfaction : lots de café vert au paquet |
| 410 | 152 | gestion-de-stock | Logiciel de gestion de stock agroalimentaire : FEFO et DLC |
| 360 | 201 | tracabilite-alimentaire | Logiciel de traçabilité alimentaire : du lot au client |
| 340 | 221 | cout-de-revient | Logiciel de calcul de coût de revient alimentaire |
| 390 | 172 | rendement-matiere | Logiciel de rendement matière : freinte et parure par lot |
| 386 | 176 | planification-production | Logiciel de planification de production agroalimentaire |
| 388 | 172 | fabrication | Logiciel de fabrication agroalimentaire : nomenclatures |
| 346 | 216 | facturation | Logiciel de facturation agroalimentaire : Factur-X |
| 356 | 206 | facturation-bon-livraison | Facturation automatique depuis le bon de livraison |
| 318 | 243 | devis-commande-livraison | Logiciel devis, commande et bon de livraison |
| 376 | 186 | vente-prise-commande | Logiciel de prise de commande : télévente alimentaire |
| 351 | 210 | crm | Logiciel CRM agroalimentaire : clients et relances |
| 350 | 210 | achats-approvisionnements | Logiciel d'achat et approvisionnement alimentaire |
| 315 | 246 | logistique-tournees | Logiciel de gestion des tournées de livraison |
| 380 | 180 | import-export | Logiciel import export alimentaire : douane et devises |
| 385 | 176 | consigne | Logiciel de gestion de consigne bouteille et emballage |

**31 sur 31 dans les bornes. Aucun titre en double.**

### Les 48 petites-filles
Formule : `{sous-fonctionnalité} {métier}`, exact match en tête.
Exemples mesurés : « Coût de revient boulangerie et pâtisserie » 280 px ·
« Planification de production boulangerie et pâtisserie » 366 px ·
« Traçabilité des lots boulangerie et pâtisserie » 310 px.
Les 48 tiennent dans les bornes sans suffixe de marque ; avec le suffixe, vérifier
les quatre plus longues (planification de production, allergènes et étiquetage).

---

## 3 · Ce qui reste à décider avant la production

1. **Le nom de la marque et son logo.** Rien n'est nommé : les titles portent un emplacement de suffixe.
2. **L'adresse de destination des formulaires**, pour que l'attribution des leads tienne.
3. **La preuve sociale.** Les avis Google et les logos clients du site d'origine ne sont pas
   transférables à une marque qui ne doit pas lui être reliée. Il faut décider ce que la nouvelle
   marque affiche à la place — et ça ne peut pas être inventé.
