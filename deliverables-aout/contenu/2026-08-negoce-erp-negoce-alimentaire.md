# Négoce — requête « erp négoce alimentaire » — 29/08/2026

Déclencheur : « on s'adresse à des dirigeants agroalimentaire, pas d'import export ».
Vous aviez raison, et le problème était plus large que les deux brouillons.

---

## Réserve méthodologique

**Étape 1 sur données de requête : impossible.** La Search Console n'est pas connectée et
DataForSEO s'est déconnecté de la session en cours de route. L'anti-cannibalisation a donc été
faite sur **les données du site**, qui sont incontestables, pas sur des impressions.

**Étape 2 : relevé de structure, pas de position.** L'accès Google direct est bloqué ici. J'ai lu
directement les trois pages qui occupent le champ — Orisha Distribution, TRADE.EASY, Prismasoft —
et relevé ce qu'elles contiennent. Leurs positions ne sont pas mesurées.

---

## Étape 2 — trois constats

1. **Aucun outil, aucune FAQ, aucun chiffre sourcé.** Sur les trois pages qui occupent le champ :
   0 calculateur, 0 FAQ, 0 chiffre daté avec source, 0 témoignage nommé. TRADE.EASY aligne 11 H2
   de description de fonctions, Orisha 4, Prismasoft 7. Ce sont des catalogues.
2. **0 sur 3 ne parle de conteneurs, d'incoterms ni de frais d'approche.** Le champ « négoce
   alimentaire » est celui du **grossiste**, pas de l'importateur. Le vocabulaire commun aux trois :
   grossiste et demi-gros, cadencier, UVC et unités de conditionnement, poids variable, DLC/DLUO,
   lots et traçabilité, tournées et force de vente mobile, EDI et GMS, préfacturation, retours
   magasins, cross-docking.
3. **Sur votre site, 19 pages parlent de négoce, et deux se disputent la requête.**
   `/negoce/`, mère du silo, sortait un title par défaut — « Negoce - Hello Harel » — et n'employait
   « grossiste » que 2 fois, contre 19 pour `/agroalimentaire/negoce-alimentaire/`.

**Angle tranché — plus démontré.** Les trois pages décrivent des fonctions ; aucune ne montre le
calcul qui décide de la marge d'un grossiste.

**Promesse, en une phrase.** Un ERP négoce alimentaire facture au poids réellement pesé, applique
la DLC du lot et l'échéance légale du produit — là où un ERP généraliste facture au poids commandé
et à trente jours pour tout le monde.

---

## Étape 1 — verdict et arbitrage

**MODÉRÉ tirant vers FORT.** Vous avez tranché : `/agroalimentaire/negoce-alimentaire/` porte la
requête, `/negoce/` redevient la porte du silo fonctionnel. Les deux ont reçu leur title.

---

## Ce qui n'allait pas, et qui est corrigé

Le problème n'était pas seulement l'import-export. **La page porteuse était un gabarit maraîcher
renommé à moitié.**

| Défaut | État avant | Après |
|---|---|---|
| H1 | « Gérez votre **production**, vos prix et vos flux saisonniers » — un négociant ne produit pas | exact match + la thèse de la page |
| Les 6 réponses de FAQ | contenu **maraîcher** : calibres, saisonnalité, fraises de mars à juin, melons | 7 réponses écrites pour le grossiste |
| JSON-LD `FAQPage` | portait **les questions du maraîcher**, désynchronisé de l'affichage | 7 questions, synchronisé |
| Fil d'Ariane balisé | 3ᵉ niveau nommé « **Maraîcher** » | « Négoce alimentaire » |
| Titre de section fonctionnalités | « **ERP Maraîcher** » | « ERP Négoce Alimentaire » |
| En-tête de la FAQ | « **FAQ Maraicher** » · « Gerez le poids variable et la saisonnalite » | « FAQ Négoce alimentaire » · poids réel, DLC, cadencier, tournées, marges |
| Carte de fonctionnalités | « Traçabilité **par parcelle** », « **Calibres, variétés** et origines », lien « Découvrir l'ERP maraîcher » | traçabilité du lot au fournisseur, cours du jour et conditions, lien vers les stocks multi-dépôts |
| Bloc « Pour approfondir » | renvoyait vers deux articles **fruits et légumes** | logiciel grossiste alimentaire, grille tarifaire en négoce |

**Mesure sur la page rendue** : « maraîch » 26 → 0 hors navigation, « calibre » 31 → 0 hors
témoignage client authentique, « saisonnalité » 9 → 0, « fraise » 4 → 0, « melon » 2 → 0.
Vocabulaire du persona après passage : grossiste 17, dépôt 17, EDI 17, DLC 13, tournée 11,
poids variable 9, cadencier 7, télévente 4.

---

## Ce qui a été ajouté

Une section d'attention au-dessus du deuxième écran, bâtie sur les classes du gabarit — aucune
direction artistique parallèle.

| Module | Contenu | Constat SERP qui le justifie |
|---|---|---|
| **Réponse en une phrase** | la promesse, extractible hors contexte | aucune des trois pages ne définit l'objet |
| **Chiffre daté** | 20 / 30 / 30 jours, délais légaux de paiement en alimentaire | 0 chiffre sourcé chez les trois |
| **Calculateur** | la marge réelle d'une ligne à poids variable : coût réel, marge réelle, marge affichée au poids commandé, écart sur douze mois | 0 outil interactif chez les trois |
| **Tableau** | les délais de paiement par nature de produit | donnée structurée citable |

**Source unique et vérifiable** : Code de commerce, articles L441-10 et L441-11, relevés sur
Légifrance le 29/08/2026. 20 jours après livraison pour les viandes fraîches, 30 jours fin de
décade pour les périssables en facturation périodique, 30 jours fin de mois pour les boissons
alcooliques.

**Le calculateur, vérifié en navigateur réel** : valeurs par défaut 17,51 € de coût réel,
4,39 € de marge réelle contre 4,90 € affichés au poids commandé, soit 7 344 € d'écart sur douze
mois. Testé sur trois cas — poids réel supérieur, inférieur et égal au poids commandé : le verdict
change correctement à chaque fois. Aucune erreur JavaScript, aucun débordement horizontal en
1440 px comme en 390 px.

**Balisage** : `ERP Négoce Alimentaire • Poids Réel, DLC et Marge Grossiste` (59 car.), meta de
147 car. `/negoce/`, qui n'avait aucun title, reçoit `ERP Négoce • Achats, Stocks, Ventes et Tarifs`.

---

## Les deux brouillons A/B, refaits

Vous avez choisi de les refaire sur le persona grossiste plutôt que de les rebasculer sur
l'import-export. C'est fait, et le test est désormais propre : **A et B partagent le même fichier
de contenu**, ce qui garantit qu'une seule variable les distingue — la mise en scène.

- **A (11493)** garde sa mise en forme éditoriale : gouttière à numéros, serif, blocs § 01 à § 06.
  Les huit « terrains de vérité » sont réécrits pour le grossiste : poids variable de la pesée à
  la facture, achat au cours du jour, trois états de stock, DLC par lot et FEFO, cadencier et
  télévente, EDI, préparation par tournée, marge et échéance.
- **B (11495)** garde la structure d'accueil SaaS : hero à deux colonnes, bande de logos,
  onglets, sections alternées, cartes, FAQ en accordéon. Les huit points y sont regroupés en
  quatre onglets à puces.

Deux images ont été cherchées via l'**API Pexels** pour remplacer le port à conteneurs et les
documents d'expédition : un entrepôt de cagettes et un poste de télévente. Toutes deux en WebP,
sous 190 ko, déposées avec alternative textuelle et crédit.

Les deux pages restent en **brouillon**, l'extrait noindex les couvre.

---

## Contrôles

Automatiques, refusant la publication en cas d'échec : équilibre des balises, aucune ancre vers
une page protégée (Règle 0), **aucun lien ni aucune image inventés — chaque URL est appelée et
doit répondre 200**, aucun vocabulaire hors persona dans le texte produit, présence des valeurs du
fond commun, des sept questions et des huit terrains, rôles ARIA.

Un lien inventé a d'ailleurs été attrapé par ce contrôle : `/agroalimentaire/negoce/`, qui n'existe
pas. C'est pour cette raison que le contrôle a été ajouté.

---

## Deux tickets ouverts au passage

1. **Le pied de page global envoie l'ancre « ERP Négoce alimentaire » vers `/agroalimentaire/maraicher/`.**
   Sur toutes les pages du site. L'ancre exact-match de la page négoce alimente donc la page
   maraîcher depuis une centaine de pages. C'est une réparation, pas une optimisation, mais elle
   demande d'éditer le pied de page sur l'ensemble du site : à lancer sur votre accord.
2. **Deux `<meta name="description">` par page.** Déjà signalé sur glacier et pâtissier, constaté
   aussi sur `/negoce/` et `/agroalimentaire/negoce-alimentaire/`. L'injecteur reste introuvable
   dans `post_content`, dans les extraits Code Snippets et dans les métadonnées exposées par l'API.

---

## À J+21

Position sur « erp négoce alimentaire », **`rank_absolute` et pas seulement `rank_group`**, CTR
comparé à la courbe, temps d'engagement face aux pages sœurs, et vérification à la main que le
calculateur est en ligne et fonctionnel. Et la mesure qui manque toujours : **la valeur d'une
demande CRM**, sans laquelle aucun de ces travaux ne se convertit en euros.
