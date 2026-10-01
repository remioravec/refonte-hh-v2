# Roadmap au 01/10/2026 — ce qui est fait, ce qui reste, ce qui attend une décision

Tout ce qui suit est mesuré sur la page servie, avant et après, par deux crawls
des 172 URL publiées : un le 01/10 au matin, un après les corrections. Aucune
ligne n'est déduite.

---

## 1 · Roadmap contenu — septembre en retard et première semaine d'octobre

Neuf lignes étaient en **A FAIRE** sur les trois dates. Huit sont livrées, une
est refusée et remplacée.

| date | requête cible | page | statut |
|---|---|---|---|
| 21/09 | erp distribution alimentaire | `/agroalimentaire/distribution-alimentaire/` | **ANNULÉE** — voir plus bas |
| 21/09 | logiciel achat agroalimentaire | [`/fonctionnalites/achat/`](https://www.helloharel.com/fonctionnalites/achat/) | **TERMINE** |
| 21/09 | crm agroalimentaire | [`/fonctionnalites/crm/`](https://www.helloharel.com/fonctionnalites/crm/) | **TERMINE** |
| 28/09 | logiciel de fabrication agroalimentaire | [`/fonctionnalites/fabrication/`](https://www.helloharel.com/fonctionnalites/fabrication/) | **TERMINE** |
| 28/09 | logiciel de facturation agroalimentaire | [`/fonctionnalites/facturation/`](https://www.helloharel.com/fonctionnalites/facturation/) | **TERMINE** |
| 28/09 | logiciel facturation automatique bon de livraison | [`/fonctionnalites/facturation-automatique-bon-livraison/`](https://www.helloharel.com/fonctionnalites/facturation-automatique-bon-livraison/) | **TERMINE** |
| 05/10 | logiciel de gestion des consignes bouteille | [`/fonctionnalites/gestion-consigne-bouteille-logiciel/`](https://www.helloharel.com/fonctionnalites/gestion-consigne-bouteille-logiciel/) | **TERMINE** |
| 05/10 | logiciel de gestion de stock agroalimentaire | [`/fonctionnalites/gestion-de-stock/`](https://www.helloharel.com/fonctionnalites/gestion-de-stock/) | **TERMINE** |
| 05/10 | logiciel de rendement matière | [`/fonctionnalites/gestion-rendement-matiere-logiciel/`](https://www.helloharel.com/fonctionnalites/gestion-rendement-matiere-logiciel/) | **TERMINE** |

### Ce qui a changé sur les cinq pages d'avril

`achat`, `crm`, `fabrication`, `facturation` et `gestion-de-stock` dataient
d'avril et portaient un H1 de bénéfice — « Optimisez vos coûts et sécurisez vos
approvisionnements ». La requête cible n'apparaissait **nulle part** dans le
premier écran. Quatre corrections par page :

1. **H1 qui porte l'expression exacte**, différent du title ;
2. **accroche qui répond dès la première phrase**, expression exacte dans les
   premiers mots ;
3. **signature datée** — auteur, date de publication, date de mise à jour,
   temps de lecture — reprise du gabarit déjà en ligne sur les trois pages de
   septembre ;
4. **FAQPage JSON-LD** construit sur la FAQ déjà publiée. Ces pages portaient
   chacune six questions et 1 500 caractères de réponse par question, et
   **aucun balisage** : les réponses existaient, Google ne pouvait pas les
   lire comme telles.

Les trois pages de septembre étaient déjà rédigées ; elles n'ont reçu que le
balisage.

### La requête de la roadmap n'est pas toujours celle qui a du volume

Vérification faite requête par requête avant d'écrire les title. Sept des huit
requêtes de la roadmap ne mesurent **aucun volume**, alors que la requête
voisine, plus large, en a :

| requête de la roadmap | volume | requête retenue en plus | volume / difficulté |
|---|---|---|---|
| logiciel achat agroalimentaire | 0 | `logiciel achat` | 110 |
| crm agroalimentaire | 70 | — | 70 |
| logiciel de fabrication agroalimentaire | 0 | `logiciel gestion production` | 90 |
| logiciel de facturation agroalimentaire | 0 | `logiciel facturation` | 2 900 / KD 62 |
| logiciel facturation automatique bon de livraison | 0 | `bon de livraison` | 2 400 |
| logiciel de gestion des consignes bouteille | 0 | **`consigne bouteille`** | **140 / KD 1** |
| logiciel de gestion de stock agroalimentaire | 10 | **`logiciel gestion de stock`** | **1 300 / KD 9** |
| logiciel de rendement matière | 0 | `rendement matière` | 10 |

Les title gardent le qualificatif agroalimentaire — c'est lui qui qualifie le
trafic — mais ils sont construits sur l'expression qui se cherche. Les deux
lignes en gras sont les deux vrais gisements de la série.

### La ligne annulée, et pourquoi

`/agroalimentaire/distribution-alimentaire/` devait être créée sur **erp
distribution alimentaire**. Quatre pages du site reçoivent déjà des
impressions sur cette requête et ses variantes, dont `/negoce/` et le
comparatif négoce. La requête mesure 10 recherches par mois. Créer une
cinquième page revenait à se disputer sa propre requête pour dix recherches :
le contenu a été versé dans `/negoce/`, qui portait déjà le sujet.

---

## 2 · Roadmap technique — octobre

### T9 · Trois landings de septembre sortaient en noindex — **TERMINE**

`/agroalimentaire/fruits-et-legumes/`, `/pme-en-croissance/`,
`/produits-de-la-mer/` et `/blog/erp-agroalimentaire/` sortaient
`nofollow, noindex` alors que la roadmap les donnait indexées. Ce n'était pas
l'extrait « pages de test A/B » : un réglage Rank Math posé page par page.

**ACCEPTATION** : 4 URL en `index, follow`. Au recrawl : **0 page en noindex
sur 172**. ✅

### T10 · Le générateur de meta description avait relâché — **TERMINE, cause toujours ouverte**

Quatre pages créées depuis août resservaient du CSS brut comme description, et
`/conformite-loi-anti-fraude-tva/` n'en avait aucune.

**ACCEPTATION** : 0 description contenant `{` ou `}`. Au recrawl : **0**, et
0 description vide. ✅
**La cause n'est pas traitée** : le gabarit continue de servir du CSS quand le
champ est vide. Tant qu'elle l'est, chaque nouvelle page naîtra avec le défaut.
❌ **à faire**

### T11 · 88 descriptions dépassaient 985 px — **TERMINE**

Le relevé montrait un motif, pas 88 cas particuliers : la plupart finissaient
par une signature de marque — « Guide par Hello Harel, éditeur spécialisé
agroalimentaire depuis 2014. » — qui pèse 50 à 70 caractères. C'est exactement
ce qui dépassait, et c'est la partie la moins utile dans une SERP, puisque la
marque est déjà dans le title et dans l'URL affichée.

- **55** traitées par règle : la signature est raccourcie, retirée, ou
  remplacée par le CTA, jusqu'à passer sous 985 px sans jamais couper une
  phrase ;
- **31** réécrites à la main : celles sans signature finale, où retirer une
  phrase entière aurait fait perdre un argument ;
- **2** laissées de côté : `/blog/erp-boissons/` répond 301 (décision à
  prendre), `/comparatifs/` a été réécrite dans T16.

**ACCEPTATION** : toutes les descriptions entre 400 et 985 px. Au recrawl :
**0 au-dessus de 985 px, 0 en dessous de 400 px**. ✅

Au passage, `/migration-as400/` servait une description **coupée en plein
mot** (« …piloté par l'ERP agroaliment »). Réparer un défaut n'est pas
optimiser : la phrase a été refermée, à l'identique pour le reste. Le title,
l'URL, le gabarit et la structure de la page n'ont pas bougé.

### T12 · 39 titles en casse anglaise — **BLOQUÉ sur une case à cocher**

Le diagnostic du 01/10 au matin était faux. Ce n'est ni le thème ni un filtre
maison : le réglage Rank Math **« Capitalize Titles »** est sur ON. Rank Math
passe un `ucwords()` **dans sa propre composition du title**, donc avant
`pre_get_document_title` et avant les filtres Open Graph — ce qui explique
pourquoi la version du matin, qui renvoyait fidèlement le title de Rank Math,
rendait encore « Coût De Revient ».

Les titles sont **corrects en base**. Deux temps :

- **13 titles étaient faux en base aussi** : décocher le réglage ne les
  aurait pas corrigés. Ils sont réécrits, à l'identique au mot près, seule la
  casse change (`Implantation Hauts-de-France`, `ERP pour PME`, `Tarifs ERP
  agro • Transparent et sans engagement • 99 €`…). ✅
- **26 titles n'attendent plus que la case** : leur valeur stockée est juste.

**Ce qu'il reste à faire, et c'est un clic** :
Rank Math → Réglages généraux → **Titres & Méta** → décocher **« Capitaliser
les titles »** (`capitalize_titles`), puis enregistrer.
→ [Réglages Titres & Méta](https://www.helloharel.com/wp-admin/admin.php?page=rank-math-options-titles)

Je n'ai pas pu le faire moi-même : l'écriture de ce réglage a été refusée côté
sécurité de ma session. Je n'ai pas cherché de contournement.

Les **9 pages livrées ce mois** (les 8 de la roadmap contenu + `/comparatifs/`)
ne t'attendent pas : leur title est figé dans l'extrait « Casse française des
titles » et sort déjà dans la bonne casse. Même mécanisme pour
`/agroalimentaire/charcutier/` et `/migration-as400/`, dont le title est figé
**à l'octet près** pour que la bascule du réglage ne les touche pas — Règle 0.

### T13 · Le balisage structuré dupliqué — **TERMINE, et le chiffre du matin était faux**

Le relevé annonçait « Organization ×10, AggregateRating ×10 sur 133 pages ».
C'était un **comptage à plat** des `"@type"` dans le source, et il est faux :
sur une page comparative, l'ItemList porte légitimement un
`SoftwareApplication` et un `AggregateRating` **par concurrent**, et chaque
Article porte légitimement son `publisher`.

Mesuré entité par entité, le défaut réel est **33 pages** qui déclarent la
note de Hello Harel plus d'une fois, sur des entités que rien ne relie :

| source | pages |
|---|---|
| extrait Elementor 4143 « Shcema », global, dans le `<head>` | 172 — `SoftwareApplication` + note |
| bloc `LocalBusiness` dans le contenu | 26 — + note |
| `@graph` `Organization#organization` des pages `/negoce/` | 5 — + note |
| ligne « Hello Harel » de l'ItemList comparatif | 2 — + note |

Correction : l'extrait global reçoit `@id = /#software` et devient LA fiche
logiciel du site ; toute entité Hello Harel de type `SoftwareApplication`
reçoit ce même `@id`, ce qui la **fusionne** au lieu de la dupliquer ; la note
est retirée des entités `LocalBusiness` et `Organization`, que Google ignore
de toute façon pour les avis auto-déclarés.

**ACCEPTATION** : une seule entité notée par page. Au recrawl : **33 → 2**. ✅

Les deux qui restent sont une **décision, pas un oubli** — voir plus bas.

### T14 · Les images hors WebP — **TERMINE**

Le relevé comptait 207 images sur 103 pages. Ce sont en réalité **17 fichiers
distincts**, dont trois pèsent 183 des 207 occurrences. Tous appelés depuis le
contenu, aucun depuis un gabarit : la conversion s'est faite entièrement par
l'API.

Pour chaque fichier, WebP avec perte **et** WebP sans perte sont essayés, et le
plus petit est retenu — une capture d'écran à larges aplats se compresse mieux
en PNG qu'en WebP avec perte, et convertir à l'aveugle aurait **alourdi** les
pages.

Les gains qui comptent :

| fichier | occurrences | avant | après |
|---|---|---|---|
| `Optimiser-la-relation-client…png` | 1 | 648 ko | 27 ko |
| `Optimiser-la-gestion-de-votre-inventaire…png` | 1 | 619 ko | 34 ko |
| `Hello-Harel-Gestion-des-stocks.png` | 70 | 171 ko | 28 ko |
| `Logiciel-de-gestion-PME-1024x576.png` | 2 | 160 ko | 46 ko |
| `Timothy-Jolliver-President-de-Hello-Harel.jpeg` | 99 | 17 ko | 11 ko |

Les attributs `srcset` et `sizes` des `<img>` convertis sont retirés : ils
pointaient vers les déclinaisons PNG générées par WordPress, qui n'existent
pas pour le WebP et auraient continué à être servies.

### T15 · Les pages lourdes — **PARTIEL**

Les deux pages comparatives servent toujours 432 ko. Le relevé les désignait
seules ; le crawl en compte **48 au-dessus de 300 ko**. Le seuil de rendu
n'est pas atteint — elles rendent leurs 22 sections — mais il n'y a aucune
marge, et c'est un ticket de gabarit, pas de page : le CSS et le JS du
gabarit métier pèsent l'essentiel, et les alléger demande de mesurer quelles
règles sont réellement utilisées par gabarit avant d'en retirer une.

**ACCEPTATION** : moins de 300 ko servis. **Non atteint.** ❌
**Charge restante** : 3 h, après la conversion WebP qui vient d'en retirer une
part.

### T16 · Les H1 — **PARTIEL**

`/comparatifs/` servait **deux H1** : celui du gabarit du thème
(`h1.entry-title`, qui imprimait le titre du post — « Comparatifs ERP
Agroalimentaire • Par Métier • 2026 ☁️ », un title de SERP, pas un H1) et
celui du contenu. Le titre du post redevient un titre de page, le H1 du
contenu devient un H2. Le hub ne listait que 3 des 4 comparatifs publiés ; les
4 y sont, ancres en exact match, aucune ancre neutre.

**Au recrawl : 0 page à deux H1.** ✅

Quatre pages restent **sans H1** : `/cgu/`, `/mentions-legales/`,
`/politique-de-confidentialite/` et `/conformite-loi-anti-fraude-tva/`. Les
trois premières sont construites dans Elementor — leur H1 est un widget
titre, il se change dans l'éditeur, et la règle est de ne pas toucher au
`_elementor_data` par l'API. La quatrième n'a ni contenu ni données Elementor
en base : elle est rendue par un gabarit, et son H1 se corrige au niveau du
gabarit. Enjeu faible sur les trois pages légales, réel sur la quatrième.

### Trouvé en route, corrigé : `/tarifs/` servait un bloc JSON-LD illisible

Un IIFE JavaScript avait été collé **à l'intérieur** du
`<script type="application/ld+json">`. Deux défauts en un :

1. le bloc n'était plus du JSON valide (« Extra data », caractère 4679), donc
   Google ignorait **tout** le balisage de la page — `LocalBusiness`,
   `Organization`, `WebSite`, `WebPage`, `BreadcrumbList` ;
2. le script ne s'exécutait jamais — un navigateur n'exécute pas un
   `type="application/ld+json"`. Les puces du carrousel de tarifs étaient
   mortes depuis leur mise en ligne.

Les deux sont séparés en deux balises, et le script a reçu la garde qui lui
manquait (il lisait `.offsetWidth` sur un `.pricing-card` supposé présent).

### Trouvé en route : cinq images cassées sur quatre pages

Trois fichiers référencés dans le contenu répondent **404**. L'avatar de
Timothy `timothy-jollivet-hello-harel.jpg` est appelé par la signature de
`/fonctionnalites/facturation-automatique-bon-livraison/` et des **deux pages
comparatives** — les trois pages affichaient une image cassée sous le nom de
l'auteur, exactement là où le lecteur cherche la preuve d'expertise.

---

## 3 · Ce qui attend une décision de ta part

1. **La case Rank Math « Capitaliser les titles »** — un clic, et 26 titles
   passent en casse française. Lien ci-dessus (T12).
2. **Les notes éditoriales des comparatifs.** Les deux pages comparatives
   déclarent un `aggregateRating` **par logiciel comparé**, avec
   `reviewCount: 1` : ce sont nos scores de comparatif, pas des avis clients.
   Deux problèmes : Hello Harel y est noté **4,7/1** alors que la fiche
   logiciel déclare **5/31** — deux notes contradictoires pour la même entité —
   et nous déclarons une note pour le produit d'un concurrent sur notre propre
   site. Schema.org a un type pour ça : `Review` avec `reviewRating`, pas
   `aggregateRating`. Je ne l'ai pas changé parce que ça touche la crédibilité
   de la page et le risque de pénalité : c'est ton arbitrage.
3. **`/blog/erp-boissons/` et `/blog/logiciel-maree-mareyeur/`** répondent 301
   vers une autre page alors qu'ils sont publiés. Les rouvrir ou les supprimer
   pour de bon.
4. **L'article Akanea**, supprimé avec sa 301, était en position 18 sur
   « akanea » (1 600 recherches/mois). Confirmer la suppression ou le
   restaurer.
5. **Les trois chiffres contradictoires.** Le site annonce selon les pages
   100, 150, 42 ou 500 clients ; 30 ou 12 ans d'expérience ; des durées de
   déploiement différentes. Les descriptions que j'ai réécrites **ne
   réaffirment aucun de ces chiffres** : on ne republie pas un chiffre qu'on
   ne sait pas vrai. Tranche-les et je les repose partout d'un coup.
6. **L'envoi de mail.** L'envoi fonctionne, la **délivrabilité n'est pas
   prouvée** : le domaine expéditeur `remi-oravec.fr` n'a ni SPF, ni DKIM, ni
   DMARC, et helloharel.com publie **deux enregistrements SPF en conflit** —
   ce qui invalide les deux. À faire chez Gandi : supprimer un des deux SPF,
   poser DKIM, poser DMARC. Et un mot de passe d'application sur un compte
   **@helloharel.com**, saisi par toi dans les réglages du plugin ou dans
   `wp-config.php` — jamais dans un message.
7. **Google Ads** : réimporter `hh-expression-et-exact.csv` (un groupe en
   expression sur les têtes, le reste en exact), et reconnecter le compte
   Hello Harel à Composio pour que je puisse reprendre la main sur les types
   de correspondance.

---

## 4 · Relevé avant / après, 172 URL

| indicateur | 01/10 matin | après |
|---|---|---|
| URL en erreur | 0 | 0 |
| pages en `noindex` | 4 | **0** |
| descriptions en CSS brut | 4 | **0** |
| descriptions absentes | 1 | **0** |
| descriptions > 985 px | 88 | **0** |
| descriptions < 400 px | 1 | **0** |
| titles > 561 px | 1 | **0** |
| pages sans H1 | 4 | 4 |
| pages à deux H1 | 1 | **0** |
| pages avec un FAQPage | 69 | **74** |
| pages déclarant deux fois la note | 33 | **2** (décision) |
| blocs JSON-LD illisibles | 1 | **0** |
| pages > 300 ko servis | 48 | 48 |
