# T2 & T4 — rapport d'exécution — 27/08/2026

Client : Hello Harel · helloharel.com
Périmètre : tickets **T2 · Canoniser les URL à ancre** et **T4 · Resynchroniser le sitemap Rank Math**.

---

## T4 · Resynchroniser le sitemap Rank Math — **fait, vérifié**

### Diagnostic
Les 8 URL signalées répondaient toutes **200**, en `index, follow`, avec un canonical
auto-référent : elles n'étaient donc pas exclues, elles étaient **absentes d'un sitemap figé**.
`page-sitemap.xml` affichait 66 URL pour 77 pages publiées, et chaque `lastmod` était
gelé (articles au 19/06, pages au 03/07) alors que des pages avaient été modifiées le jour même.
Le cache HTTP a été écarté (`x-cache: MISS`).

Le premier correctif a échoué : il purgeait les *transients* et une table. Un point de
diagnostic temporaire a montré que Rank Math stocke ses sitemaps **dans des fichiers sur disque**,
suivis par l'option `rank_math_sitemap_cache_files`.

### Correctif posé
Extrait « T4 — Purge du cache sitemap Rank Math », qui appelle
`\RankMath\Sitemap\Cache::invalidate_storage()` et `Cache_Watcher::invalidate_storage()`,
supprime `rank_math_sitemap_cache_files`, les reliquats d'options Yoast et les transients
`rank_math_sitemap%`, puis **se neutralise** via un marqueur daté (idempotent).

### Acceptation
| Mesure | Avant | Après |
|---|---|---|
| URL dans `page-sitemap.xml` | 66 | **77** = nombre de pages publiées |
| `lastmod` | gelé (19/06 – 03/07) | **27/08/2026** |
| Les 8 URL cibles présentes | 0/8 | **8/8** |
| URL dans `post-sitemap.xml` | — | 102 |

Un seul article reste hors sitemap : **id 5290, `/blog/erp-agroalimentaire/`**, en
`follow, noindex`. Son exclusion est **correcte**, pas un défaut : 102/103 est le bon compte.

### Reste à la charge du client
**Resoumettre le sitemap dans la Search Console** (`Sitemaps` → resoumettre
`sitemap_index.xml`). La console n'est pas connectée ici, cette moitié de l'acceptation
ne peut ni être exécutée ni être mesurée de mon côté.

---

## T2 · Canoniser les URL à ancre (`#s-*`) — **fait, avec une réserve à lire**

### Ce que le ticket demandait, et ce qui est réellement implémentable

> « Poser rel=canonical de chaque #s-* vers l'URL mère »

**Ce n'est pas implémentable, et c'est déjà satisfait.** Un fragment n'est jamais transmis
au serveur : `…/page/#s-3` et `…/page/` reçoivent le même HTML, donc le **même `<head>`,
donc le même canonical**. Il n'existe aucun moyen — et aucun besoin — de servir un canonical
par fragment.

Vérifié en direct le 27/08 sur les 71 pages porteuses :
**70 portent un canonical auto-référent sans fragment.** La 71e,
`/blog/erp-agroalimentaire/`, n'en porte pas parce qu'elle est en `noindex` —
comportement normal de Rank Math. Chaque `#s-*` pointe donc déjà vers son URL mère.

Aucun filtre n'a été posé sur le canonical : le balisage est correct, et y toucher
aurait modifié le `<head>` des pages protégées (Règle 0).

> « retirer les liens de saut du sommaire des données structurées »

**Déjà satisfait aussi.** Relevé sur les 71 pages : **0 occurrence** d'URL fragmentée
dans les blocs JSON-LD. Rien à retirer.

### Ce qui restait donc à faire, et qui est fait

La seule chose qui produisait réellement ces URL : les **liens de saut crawlables du sommaire**.

Relevé live du 27/08 :

| Mesure | Valeur |
|---|---|
| Pages porteuses | **71**, toutes sous `/blog/` |
| Liens de saut `<a href="#s-…">` | **1 147** |
| Fragments uniques | **567** |
| Blocs sommaire | 2 par page (carte mobile en tête + carte latérale desktop) |
| Pages protégées concernées | **0** |
| Plus gros porteur | `/blog/maitriser-la-gestion-des-stocks/` — 70 liens / 35 cibles |

Deux gabarits de sommaire coexistent, tous deux traités :
`<nav class="hha-toc">` (gabarit historique) et `<div class="som">` (gabarit blog validé,
prix de revient et distributeurs de produits frais).

**Correctif posé** — extrait « T2 · Canonisation des URL à ancre » :
`<a href="#s-N">Label</a>` devient
`<a class="hha-jump" role="link" tabindex="0" data-jump="s-N">Label</a>`,
avec un JS délégué qui restitue le défilement doux, la validation clavier
(Entrée / Espace) et déplace le focus sur la section atteinte.

Portée strictement limitée à l'intérieur des deux conteneurs de sommaire. Les titres
cibles (`id="s-N"`), le corps de l'article, le CSS `.hha-toc a` et le scroll-spy
(indexé sur la position, pas sur le `href`) sont inchangés.

### Contrôle après pose

| Mesure | Avant | Après |
|---|---|---|
| Liens de saut crawlables, sur les 71 pages | 1 147 | **0** |
| Liens de saut crawlables, **sur les 179 URL du sitemap** | — | **0** |
| Liens neutralisés | — | 1 147 |
| Blocs sommaire toujours rendus | 144 | **144** |
| Cibles `id="s-*"` intactes | 985 | **985** |
| Pages où le JS de saut manque | — | **0** |
| Pages protégées : code HTTP / `data-jump` / title | 200 / 0 / inchangé | 200 / 0 / inchangé |

Contrôle visuel des deux gabarits de sommaire (capture de l'élément en ligne) :
rendu identique, aucun décalage, aucun libellé perdu.

### Deux réserves à connaître

**1 — Dégradation sans JavaScript.** Le sommaire reste lisible (il annonce le plan) mais
le saut ne fonctionne plus : le lecteur fait défiler. Aucune information n'est perdue,
tout le contenu est dans la page. C'est le prix à payer pour retirer les URL fragmentées ;
c'est le seul point du gabarit qui s'écarte de la règle « le module fonctionne sans JS ».

**2 — Ce qui est mesuré n'est pas forcément un défaut d'indexation.** Les 119 439 impressions
sur 163 URL `#s-*` sont des lignes du rapport **Performances**, pas des pages indexées
séparément : Google attribue une ligne distincte quand il affiche un **lien de section**
dans la SERP. Ces impressions appartiennent à la page mère, elles ne sont pas dispersées.
Le vrai signal d'alarme du chiffre est ailleurs : **19 clics pour 119 439 impressions**,
soit un problème d'angle et de title — le levier NavBoost, pas le levier canonical.
Retirer les liens de section fait donc disparaître ces lignes du rapport (l'acceptation
sera tenue), mais **fait aussi disparaître les liens de section de la SERP**, qui occupent
de la surface d'affichage.

**Réversible en un clic** : désactiver l'extrait restaure les `href` à la requête suivante.
Aucune écriture en base, le `post_content` n'a pas été touché.

### Acceptation
« Plus aucune URL contenant `#` dans le rapport Pages de la Search Console à J+30. »
La source est tarie côté site (0 lien de saut crawlable sur les 179 URL du sitemap).
La vérification à J+30 demande un accès Search Console, qui n'est pas connecté ici.

---

## Extraits déposés / modifiés sur le site

| id | Nom | État | Rôle |
|---|---|---|---|
| 9 | T4 — Purge du cache sitemap Rank Math | inactif | a fait son travail, marqueur posé ; conservé pour réemploi |
| 10 | DIAG — sitemap | **neutralisé** (code vidé, inactif) | le plugin refuse la suppression par API — **à supprimer à la main dans Code Snippets** |
| 11 | T2 — Canonisation des URL à ancre `#s-*` | **actif** | retire les liens de saut crawlables des deux gabarits de sommaire |
| 12 | Casse française des titles refondus | **actif** | corrige la capitalisation sur les posts 3430 et 5269 uniquement |

Le point de diagnostic `/wp-json/hh/v1/diag-sitemap` répond désormais **404**.

---

## En marge : les deux titles refondus, enfin posés

Ils ne l'étaient pas. La refonte de `/blog/calculer-le-prix-de-revient-en-boulangerie/`
tournait encore sous son ancien title, celui qui promettait un guide d'exercices de
boulangerie dans une SERP d'acheteurs de logiciel. Posés par
`rankmath/v1/updateMeta` :

| Post | Title | Meta description |
|---|---|---|
| 3430 · prix de revient | `Logiciel Prix de Revient • Simulateur Gratuit et Comparatif 2026` (64 car.) | 154 car. |
| 5269 · distributeurs de produits frais | `ERP pour Distributeurs de Produits Frais • Comparatif 2026` (58 car.) | 152 car. |

**Défaut découvert au passage** : le site capitalise chaque mot du title rendu —
« Prix **De** Revient », ce qui casse l'expression exacte à l'œil et n'est pas de la
typographie française. La capitalisation s'applique **après** le filtre
`rank_math/frontend/title` (vérifié en direct) ; seul `pre_get_document_title` la précède.
L'extrait 12 corrige la casse **sur ces deux posts seulement** : couper le réglage
globalement aurait modifié le title des 5 pages protégées.

Ce défaut touche **tout le site**. Il mérite son propre ticket, à arbitrer avec vous,
car le correctif global change le title des pages protégées et tombe sous la Règle 0.
