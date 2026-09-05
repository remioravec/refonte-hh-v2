# Briefs contenu — Sprint 1 (livraison 17/08/2026) · Hello Harel

> Process `operationnel-contenu` — étapes 1→4. **GO consultant requis avant rédaction (étape 5).**
> Relevés SERP en direct du 15/08/2026 (France, fr). Anti-cannibalisation GSC : propriété `https://www.helloharel.com/`, fenêtre 15/05→12/08/2026.
> DA de rendu : Google Store. Cible : dirigeants / resp. production-qualité de PME agro (20-300 sal.).

## ⚠️ Correction de roadmap imposée par l'anti-cannibalisation

Deux des trois sujets du 17/08, tels qu'écrits dans la roadmap, **cannibaliseraient la page protégée `/agroalimentaire/`** (Règle 0 : #1-#3 sur ses requêtes, citée en AI Overview — interdiction d'y toucher ET de lui prendre ses requêtes) :

| Sujet roadmap | Page cible roadmap | Ce que dit la donnée | Décision |
|---|---|---|---|
| logiciel de gestion agroalimentaire | /fonctionnalites/ | `/agroalimentaire/` capte déjà « logiciel (de gestion / erp) agroalimentaire » à **pos 6,7-13,6** (683+479 impr). `/fonctionnalites/` = 0 impression dessus. | **Ne pas** viser la requête tête. `/fonctionnalites/` vise l'intention **fonctionnelle** et **alimente** le hub. |
| meilleur erp agroalimentaire | /comparatifs/ | `/agroalimentaire/` est **#1 organique live** / pos 2,2 GSC. `/comparatifs/` = 0 impression. | **Ne pas** viser « meilleur erp agroalimentaire ». `/comparatifs/` devient l'**index comparatif** sur « comparatif erp agroalimentaire » (champ libre) et **pointe vers** le hub. |
| erp boulangerie industrielle | /agroalimentaire/boulanger/ | `/boulanger/` capte déjà « erp boulangerie » pos 6,9 / « erp boulanger » pos 2,7. Aucune autre page concurrente. | **MàJ propre**, sans cannibalisation. |

Sans cette correction, on ferait chuter la seule page du site qui rapporte des clics business. Ci-dessous les 3 briefs corrigés.

---

## BRIEF 1 · `/fonctionnalites/` — MàJ · « fonctionnalités ERP agroalimentaire »

**1. Contexte.** Verdict cannibalisation **FORT** sur la requête tête (« logiciel de gestion agroalimentaire ») : portée par `/agroalimentaire/`. On **réoriente** `/fonctionnalites/` vers l'intention *fonctionnelle* (« que fait le logiciel »), distincte de l'intention *catégorie/comparaison* du hub. Angle tranché : **la seule page qui montre les fonctions par preuve écran, module par module** (traçabilité, coût de revient, poids variable, DLC/DDM, rendement matière) là où les concurrents restent en généralités. Promesse : *« Voyez exactement ce que fait l'ERP sur chaque fonction critique de l'agro — pas une liste, des démonstrations. »*

**2. Structure Hn** (dérivée de la SERP : appvizer/agro-media comparent des *fonctionnalités*, vif/infologic décrivent des *modules* ; personne ne montre la fonction en action) :
- H1 : Fonctionnalités de l'ERP agroalimentaire Hello Harel
- H2 Traçabilité ascendante/descendante par lot *(sous-intention : rappel produit, DLC/DDM)*
- H2 Coût de revient & marge au produit *(la fonction la plus demandée en agro)*
- H2 Poids variable & pesée *(différenciant métier fort, absent des concurrents généralistes)*
- H2 Gestion de production & nomenclatures/recettes
- H2 Stocks, DLC/DDM et préparation de commandes
- H2 Étiquetage & conformité (INCO)
- H2 FAQ (≥7 questions)

**3. Gabarit** (pages sœurs : les pages `/fonctionnalites/<fonction>/` existantes — achat, fabrication, crm…). Reprendre : bandeau titre + preuve sociale (+200 clients, 5/5·31 avis), blocs fonction en bento avec check-lists, capture/visuel par fonction, CTA démo, FAQ, JSON-LD. **Attention intégration** : vérifier si `/fonctionnalites/` porte un layout Elementor (`_elementor_data` non vide) → passer par `_elementor_data`, ne pas écraser `post_content` (vigilance client.json).

**4. Maillage sortant** (≤8, ancres uniques) : vers chaque `/fonctionnalites/<fonction>/` (traçabilité-alimentaire, fabrication, achat…) ancre = nom de la fonction ; vers `/agroalimentaire/` ancre « ERP agroalimentaire » (remontée au hub) ; vers 2-3 comparatifs métier.

**5. Maillage entrant** (≥2, depuis pages DÉJÀ INDEXÉES) : depuis `/agroalimentaire/` (bloc « Fonctionnalités » → ancre « toutes les fonctionnalités »), depuis 2-3 pages métier (`/boulanger/`, `/charcutier/`… bloc corps → ancre « les fonctions de l'ERP »). **C'est ce bloc qui décide de l'indexation — à poser et à vérifier à J+21.**

**6. Balisage** — ⚠️ *bloqué tant que le ticket technique T1 (générateur de meta cassé) n'est pas corrigé ; Rank Math non éditable en REST → saisie manuelle.*
- Title (≤60) : `Fonctionnalités ERP Agroalimentaire • Traçabilité, Coût de Revient`
- Meta (≤155) : `Découvrez les fonctions de l'ERP agroalimentaire Hello Harel : traçabilité par lot, coût de revient, poids variable, DLC. +200 sites équipés.`
- H1 (≠ title, sentence case) : `Les fonctionnalités de l'ERP agroalimentaire, démontrées une par une`
- JSON-LD attendu : `SoftwareApplication` (unique — voir T5 dédoublonnage) + `FAQPage`.

**7. Objectifs chiffrés** (client.json) : FAQ ≥7, liens sortants ≤8, entrants ≥2, CTA ≥2 (démo). Cible position : entrer top 10 sur « fonctionnalités erp agroalimentaire » / « logiciel gestion de production agroalimentaire » (le hub garde la tête).

**8. Attention.** 1er écran : le titre + une capture réelle de la fonction traçabilité (pas une illustration) + les 3 preuves (200 clients / 5·31 / français depuis 2014). 2e écran : le bloc « coût de revient au produit » avec un chiffre concret, pour retenir le resp. production.

---

## BRIEF 2 · `/comparatifs/` — MàJ · « comparatif erp agroalimentaire » (index)

**1. Contexte.** Verdict **FORT** : `/agroalimentaire/` est **#1 organique** sur « meilleur erp agroalimentaire » — on ne lui prend pas la requête. « comparatif erp agroalimentaire » = **champ libre** (0 impression HH, verdict FAIBLE). Angle tranché : `/comparatifs/` devient l'**index/hub des comparatifs métier** — la porte d'entrée neutre « comment choisir + tous nos face-à-face », qui distribue vers les comparatifs métier et **remonte le hub**. La SERP « meilleur/comparatif » est tenue par des comparateurs tiers (agro-media #2 qui liste HH en #4, tool-advisor, appvizer) → notre contre-jeu = **notre propre comparatif méthodique et daté**.

**2. Structure Hn** :
- H1 : Comparatifs ERP agroalimentaire
- H2 Comment choisir son ERP agroalimentaire (critères : spécialisation métier, poids variable, DLC, coût de revient, délai de déploiement) *(reprend l'intention « comment choisir » que les comparateurs monétisent)*
- H2 Nos comparatifs par métier → cartes vers meilleur-erp-charcuterie-salaison, meilleur-erp-traiteur, etc.
- H2 Hello Harel face aux ERP généralistes (Sage, Odoo) — tableau daté
- H2 FAQ

**3. Gabarit** : pages sœurs = les `/comparatifs/meilleur-erp-<métier>/` existants. Reprendre le gabarit article/comparatif (tableau, verdict, étoiles 5/31, CTA). ⚠️ L'audit signale un **2e H1 hors contenu éditable** sur `/comparatifs/` (côté template) — le résoudre à l'intégration (ticket).

**4. Maillage sortant** (≤8) : vers chaque comparatif métier (ancre = « meilleur ERP <métier> ») ; vers `/agroalimentaire/` (ancre « ERP agroalimentaire spécialisé ») ; vers `/migration-as400/` (ancre « migrer depuis un AS/400 »).

**5. Maillage entrant** (≥2) : depuis `/agroalimentaire/` (bloc comparaison → ancre « voir les comparatifs ») ; depuis les pages métier (ancre « comparer les ERP <métier> »).

**6. Balisage** (⚠️ après T1) :
- Title : `Comparatif ERP Agroalimentaire • Nos Face-à-Face par Métier 2026`
- Meta : `Comparez les ERP agroalimentaires par métier : charcuterie, traiteur, boulangerie. Critères de choix, tableaux datés et retours terrain. +200 sites.`
- H1 : `Comparatifs ERP agroalimentaire : nos face-à-face par métier`
- JSON-LD : `ItemList` (les comparatifs) + `FAQPage`. **Éviter un 2e AggregateRating** (ticket T5).

**7. Objectifs** : FAQ ≥7, cible top 10 sur « comparatif erp agroalimentaire » / « liste erp agroalimentaire » (related search vue en SERP). Ne PAS viser « meilleur erp agroalimentaire » (réservé au hub).

**8. Attention.** 1er écran : la grille de critères « comment choisir » (utile immédiatement) + les cartes comparatifs métier. 2e écran : le tableau HH vs généralistes avec les étoiles 5/31.

---

## BRIEF 3 · `/agroalimentaire/boulanger/` — MàJ · « erp boulangerie industrielle »

**1. Contexte.** Verdict **propre** (MODÉRÉ) : `/boulanger/` capte déjà « erp boulangerie » (pos 6,9 / 3 clics) et « erp boulanger » (pos 2,7) ; « logiciel boulangerie » traîne à pos 45,4 → à récupérer. Piège d'intention relevé en SERP : **« erp boulangerie » est disputé par l'autre sens d'ERP** (Établissement Recevant du Public — normes incendie/accessibilité : legalrenov, mapa, boulangerie.org). L'ajout de **« industrielle »** rebascule vers le logiciel (CSB #1, VIF #2, Infologic #3). Angle tranché : **lever l'ambiguïté dès le H1** (« logiciel/ERP de gestion ») et **posséder le terrain industriel** (panification industrielle : traçabilité lots farine/levure/fourrages, poids variable, planification des fournées) que CSB/VIF/Infologic couvrent. Promesse : *« L'ERP de gestion des boulangeries industrielles : de la traçabilité des lots de farine au coût de revient à la baguette. »*

**2. Structure Hn** (dérivée de CSB/VIF/Infologic — les 3 vrais concurrents software) :
- H1 : ERP boulangerie industrielle — le logiciel de gestion des fournils industriels
- H2 Traçabilité des lots (farine, levure, fourrages, inclusions) *(exact snippet vif/infologic)*
- H2 Planification des fournées & ordres de fabrication
- H2 Coût de revient à la référence (baguette, viennoiserie)
- H2 Poids variable, DLC/DDM et étiquetage
- H2 Multi-sites / multi-dépôts *(besoin « industrielle »)*
- H2 FAQ (≥7 — inclure « Quel type d'ERP pour une boulangerie ? » vu en PAA, en désambiguïsant logiciel vs norme ERP)

**3. Gabarit** : pages sœurs = les autres `/agroalimentaire/<métier>/` (charcutier, maraîcher). Gabarit métier standard : hero + preuve sociale + bento fonctions + secteurs + FAQ + bande démo. Page **self-contained** (canvas) → `post_content` éditable sans risque. Réutiliser la bande démo premium déjà déployée. **NB : `/boulanger/` n'est pas protégée.**

**4. Maillage sortant** (≤8) : vers `/fonctionnalites/tracabilite-alimentaire/`, `/fonctionnalites/fabrication/` (ancres fonction) ; vers `/agroalimentaire/` (ancre « ERP agroalimentaire ») ; vers `/comparatifs/` (ancre « comparer les ERP boulangerie »).

**5. Maillage entrant** (≥2) : depuis `/agroalimentaire/` (carrousel métiers → déjà en place, ancre « Boulangerie ») ; depuis `/blog/meilleurs-erp-boulangerie/` (qui rank pos 8,5 sur « erp boulanger » → ancre « notre ERP boulangerie ») ; depuis `/fonctionnalites/fabrication/`.

**6. Balisage** (⚠️ après T1) :
- Title : `ERP Boulangerie Industrielle • Logiciel Gestion & Traçabilité`
- Meta : `Le logiciel ERP des boulangeries industrielles : traçabilité des lots de farine, planification des fournées, coût de revient, poids variable. Démo gratuite.`
- H1 : `ERP boulangerie industrielle : le logiciel de gestion des fournils`
- JSON-LD : `SoftwareApplication` + `FAQPage` (dont la Q de désambiguïsation logiciel vs norme ERP).

**7. Objectifs** : FAQ ≥7, CTA démo ≥2. Cibles : maintenir « erp boulanger » (top 3), gagner « erp boulangerie industrielle » (nouveau) et récupérer « logiciel boulangerie » (45 → top 10).

**8. Attention.** 1er écran : H1 désambiguïsé + une phrase qui tranche « logiciel de gestion, pas mise aux normes » + les 3 preuves. 2e écran : le bloc traçabilité des lots de farine (le besoin n°1 de la panification industrielle), avec un visuel.

---

### Reste à la charge du client / intégration
- Balises (title/meta) : **saisie manuelle Rank Math** + **corriger d'abord T1** (générateur de meta cassé) sinon écrasement à la publication.
- Vérifier le layout (`/fonctionnalites/` et `/comparatifs/` possiblement Elementor → passer par `_elementor_data`).
- Purger LiteSpeed après intégration.
- **Contrôle J+21** (étape 8) : page en ligne à l'URL prévue, indexée, liens entrants réellement posés, position sur la requête cible.

### GO attendu
Valider ces 3 briefs (surtout la réorientation de #1 et #2 pour protéger le hub) → je lance la **rédaction** (étape 5).
