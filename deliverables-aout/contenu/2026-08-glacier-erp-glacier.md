# /agroalimentaire/glacier/ — requête « erp glacier » — 27/08/2026

Mise à jour de landing, poussée directement en ligne. Pas de brief ni de rédaction en docx,
conformément à la demande.

---

## Réserve méthodologique, à lire avant les chiffres

**Étape 1 — anti-cannibalisation : non exécutable.** La Search Console n'est pas connectée et
aucune clé DataForSEO n'est disponible dans cet environnement. Le verdict FORT / MODÉRÉ / FAIBLE
n'a donc pas été posé sur des données de requête.

**Étape 2 — relevé SERP : dégradé.** L'accès Google direct est bloqué ; DuckDuckGo répond une page
anti-robot. Le relevé a été fait par recherche web sur index américain, puis par lecture directe
des pages concurrentes. Les positions ne sont pas mesurées : seules les **structures de pages**
le sont, et c'est ce qui a servi à trancher l'angle.

**Signal de cannibalisation à surveiller** : sur une requête logiciel + glacier, c'est
`/agroalimentaire/` — le hub, page protégée — qui ressort, pas la landing glacier. C'est le même
motif que sur « erp fruits et légumes » et « erp import export ». À mesurer dès le retour de la
Search Console ; si le hub capte, la landing devra recevoir des ancres exactes depuis lui, ce que
la Règle 0 interdit — l'arbitrage sera à faire avec vous.

---

## Étape 2 — ce que montre le haut de SERP

Trois constats, tirés de la lecture des pages qui occupent le terrain
(FoodTracks, ChefsTouch, Crémix, Quantara, AC-Log, allocaisse) :

1. **Aucune des pages en tête ne porte d'outil interactif.** FoodTracks a un tableau comparatif et
   une FAQ, ChefsTouch une FAQ seule. Zéro calculateur, zéro simulateur.
2. **Aucun chiffre n'y est sourcé.** Sur la page la plus complète du lot, tous les chiffres
   (70-80 % du CA en été, corrélation > 0,85, 30-100 €/mois) sont donnés sans source externe ni date.
3. **Le terrain est occupé par la caisse.** Le comparatif de référence oppose FoodTracks, L'Addition,
   Lightspeed et Excel — trois logiciels de point de vente et un tableur. Personne ne parle
   production : ni foisonnement, ni lot, ni poids au litre, ni dénomination réservée.

**Angle tranché — plus démontré.** Ce que la caisse ne mesure pas : le litre.

**Promesse de page, en une phrase.** Un ERP glacier relie la recette du mix, le lot, le
foisonnement, la DLC et le coût de revient au litre — là où un logiciel de caisse s'arrête au ticket.

---

## Ce qui a été posé en ligne

### Hero
Nouvelle photo : laboratoire de production laitière, cuves inox et opérateur — le persona
**fabricant**, pas le salon de glace. Recherchée via l'API Pexels, convertie en WebP (199 ko,
1920 px), déposée dans la médiathèque avec `alt` et crédit.
H1 refondu : « ERP glacier : la recette, le lot et le coût de revient au litre » — exact match en
tête, angle lisible. L'ancien H1 (« Pilotez vos productions, maîtrisez vos coûts ») ne portait
aucune occurrence de la requête.

### Section d'attention, insérée au-dessus du deuxième écran
Elle reprend les classes du gabarit (`section-header`, `overline`, `about-card`, `about-stats`,
`about-stat-card`, `stat-number`, `bento-card`, `tilted-icon`) : aucune DA parallèle n'a été créée.

| Module | Contenu | Constat SERP qui le justifie |
|---|---|---|
| **Réponse encadrée** | la promesse en une phrase, extractible hors contexte | aucune page du haut de SERP ne définit l'objet en une phrase |
| **Chiffre daté** | 450 g / 550 g / 650 g, poids minimal par litre | aucun chiffre sourcé chez les concurrents |
| **Calculateur** | poids au litre, foisonnement maximal admissible, coût matière au litre et au bac de 5 L, verdict de conformité | zéro outil interactif dans le top |
| **Tableau** | les 8 dénominations réservées, poids minimal, foisonnement maximal, seuil caractéristique | donnée structurée citable par un modèle |

**Source unique et datée de toutes les valeurs réglementaires** : Code des pratiques loyales des
glaces alimentaires, CNGF/SFIG, version du 4 mars 2008, points 2.3.1 à 2.3.8 et tableau de synthèse.
Extraite du document lui-même, pas d'un article de seconde main.

Le calculateur n'a **aucune dépendance externe**, ses champs sont étiquetés (`<label for>`), ses
sorties sont des `<output>`, et ses valeurs par défaut sont pré-rendues dans le HTML : sans
JavaScript il affiche un cas cohérent, et le tableau juste en dessous donne la référence complète.
Aucun décalage de mise en page : les cartes de sortie ont une hauteur minimale.

### FAQ — 7 questions, réécrites
**Défaut trouvé** : les 6 réponses en place étaient un gabarit **boulangerie** renommé. On y lisait
« chaque four a une capacité limitée », « farine, beurre, sucre, œufs, levure », « pas de croissants
le dimanche matin », « pâte feuilletée », « la farine représente 30 à 40 % du coût matière » — sur
une page glacier. Le même gabarit portait aussi des promesses chiffrées non sourcées
(« réduire les invendus de 15 à 25 % », « 10 heures par semaine », « 15 à 20 heures par semaine »),
interdites par le brief.

Les 7 réponses sont réécrites sur le métier réel : pasteurisation, maturation, turbinage,
foisonnement mesuré en sortie de turbine, conservation à −18 °C, FEFO, étiquetage INCO,
laboratoire central et circuits boutique/B2B. Les promesses non sourcées ont disparu.
Une 7e question a été ajoutée — « Combien doit peser un litre de glace ? » — parce qu'elle porte
le fait le plus citable de la page. Le JSON-LD `FAQPage` est resynchronisé sur les 7.

### Autre reliquat corrigé
La première carte de la grille de fonctionnalités renvoyait vers
`/agroalimentaire/boulanger/` avec l'ancre « Découvrir l'ERP boulangerie », sur une page glacier.
Retargetée vers `/fonctionnalites/fabrication/`, ancre « logiciel de fabrication ».

### Balisage
- **Title** : `ERP Glacier • Foisonnement, Lots et Coût de Revient au Litre` (60 car.)
- **Meta description** : 140 car., porte l'exact match
- **H1 ≠ title**, exact match dans les deux

### Maillage
**Sortant, depuis la nouvelle section** : logiciel de fabrication, traçabilité alimentaire,
logiciel de prix de revient, ERP pâtissier, ERP chocolatier. Aucun lien vers une page protégée
avec une ancre optimisée — vérifié par un contrôle automatique dans le script de publication.

**Entrant, deux ancres éditoriales exactes « ERP glacier »** posées dans la ligne « À approfondir »
existante de :
- `/agroalimentaire/patissier/`
- `/agroalimentaire/industrie-laitiere/`

Le carrousel « Nos secteurs d'expertise » pointait déjà vers Glacier depuis 20 pages, mais c'est
de la navigation, pas du maillage.

---

## Contrôle — les critères de signal, mesurés

| Critère | Verdict |
|---|---|
| Le title porte l'angle | oui — « foisonnement, lots, coût au litre » |
| P1 = la réponse, requête exacte dans les 60 premiers mots | oui |
| Module interactif au-dessus du 2e écran, données réelles, sans dépendance | oui |
| Preuve datée et sourcée dans le premier tiers | oui — CPLGA, 4 mars 2008 |
| La suite est dans la page | oui — logiciel de prix de revient, ERP pâtissier, ERP chocolatier |
| Citable : fait daté / définition en une phrase / donnée structurée | les trois |

Contrôles automatiques passés à la publication : équilibre des balises, aucun lien de saut `#s-`
introduit, aucune ancre optimisée vers une page protégée, aucune fuite du gabarit boulangerie dans
le texte produit, les 7 questions présentes.

Rendu vérifié en capture, desktop et mobile (390 px) : la section est indiscernable du reste du
gabarit, le tableau défile dans son propre conteneur, la page ne défile pas horizontalement.

---

## Deux défauts trouvés au passage, qui ne relèvent pas de cette page

1. **Deux `<meta name="description">` sur la page.** Le second est injecté par un bloc de code
   personnalisé (voisin du correctif « Logo Crop Fix v2 » et du script Oremi), il n'est ni dans
   `post_content`, ni dans les extraits Code Snippets, ni dans les métadonnées exposées par l'API.
   Il porte une ancienne description qui contredit celle de Rank Math.
   Constaté aussi sur `/agroalimentaire/patissier/` ; absent de charcutier, viande et du blog.
   **Ticket technique à ouvrir** : localiser l'injecteur et le retirer.

2. **Le site capitalise chaque mot du title rendu** (« Coût De Revient »). Corrigé sur cette page
   par l'extrait ciblé n° 12, comme sur les posts 3430 et 5269. Le correctif global est bloqué par
   la Règle 0 : il changerait le title des 5 pages protégées. À arbitrer avec vous.

---

## À J+21

À relever quand la Search Console sera reconnectée : position sur « erp glacier », **`rank_absolute`
et pas seulement `rank_group`**, CTR comparé à la courbe (27 · 15 · 11 · 8 · 7 · 5 · 4 · 3,5 · 3 · 2,5 %),
temps d'engagement comparé aux pages sœurs du même gabarit, et vérification à la main que le
calculateur est toujours en ligne et fonctionnel.
