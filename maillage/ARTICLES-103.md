# Les 103 articles de blog — inventaire complet et arbitrage GSC

- **Trafic** : Google Search Console, propriété `https://www.helloharel.com/`, **16 mois**
  (2025-05-21 → 2026-09-18) et fenêtre courte **90 jours** (2026-06-20 → 2026-09-18)
- **Articles** : `wp-json/wp/v2/posts`, état live du 2026-09-21 → **103 articles**
  (le sitemap n'en liste que 102 : `erp-agroalimentaire` en est absent)
- **Mots** : corps réel, boilerplate Elementor retiré (9 766 mots de template par article dans l'export)
- Clics et impressions **agrégés par URL canonique** : les ancres `#s-1`, `#elementor-toc__*` et les
  variantes de slash sont recollées à leur page mère. Sans ça `cout-prix-au-kilo` perd 13 lignes.

## Le site en deux chiffres

| | 16 mois | 90 derniers jours |
|---|---:|---:|
| Clics, tout le site | 42 444 | 2 844 |
| Impressions | 3 009 237 | 352 176 |
| Clics/mois | ~2 653 | ~948 |
| Part du blog dans les clics | 80 % (34 072) | — |

Le trafic a été divisé par ~2,8 entre la moyenne 16 mois et le trimestre écoulé.

**74 % des clics du blog tiennent sur 4 articles** : `cout-prix-au-kilo` (14 112),
`maitriser-la-gestion-des-stocks` (6 025), `numeros-de-lot` (2 823),
`calculer-le-prix-de-revient-en-boulangerie` (2 147).

## Ce que la GSC a corrigé par rapport au proxy DataForSEO

La version précédente de ce document s'appuyait sur DataForSEO, faute d'accès Search Console.
Le proxy s'est trompé lourdement et ses verdicts sont annulés :

| Article | Proxy | GSC 16 mois | Correction |
|---|---|---|---|
| `facture-exacompta` | 0 → **supprimer** | **727 clics** / 27 511 impr, pos 8,7 | **Garder** — 6ᵉ article du site |
| `maitriser-la-gestion-des-stocks` | 4,2 d'ETV | **6 025 clics** / 103 733 impr | 2ᵉ article du site |
| `facture-traiteur` | 0 | **635 clics**, pos 4,4 | Garder |
| `kpi-qualite-agroalimentaire` | 0 | **329 clics** | Garder |
| `bon-de-commande-traiteur` | 0 | **235 clics** | Garder |
| `opc-ua` | 0 → **supprimer** | 12 clics / 3 365 impr | **Garder** |
| `alerte-date-peremption` | 0 → fusionner **dans** `dlc-ddm-dluo` | 132 clics vs 33 | **Cible inversée** |
| `alternative-sage-erp` | 0 → fusionner dans `alternatives-sage-agroalimentaire` | 260 impr vs 6 | **Cible inversée** |
| `alternative-cegid` | 0 → fusionner dans `alternatives-cegid-distribution-alimentaire` | 413 impr vs 0 | **Cible inversée** |
| `conditionnement-alimentaire-erp` | 0,1 → fusionner | 46 clics / 10 601 impr | **Fusion annulée** |
| 72 articles « à zéro » | 72 | **6** | le proxy ne voit pas la longue traîne |

Seuls **6 articles sur 103** n'ont aucune impression sur 16 mois, et 4 des 6 sont des cibles ou
sources de fusion. Ta règle tenait : le volume nul n'écarte rien.

## Résultat de l'arbitrage

| Verdict | Nb | Effet |
|---|---:|---|
| **Garder** | 73 | rattachés aux 8 sections du hub |
| **Fusionner** | 19 | absorbés dans 12 cibles, 301 obligatoire (ils portent des impressions) |
| **Retravailler** | 5 | grosses impressions, position hors page 1 |
| **Supprimer** | 2 | et seulement 2 |
| **Migrer** | 2 | contenu local → pages `/implantations/` |
| **Trop jeune** | 2 | publiés en juin 2026, à revoir dans 3 mois |
| | **103 → 80** | −22 % d'URL, 0 clic perdu |

### Les 5 à retravailler — le plus gros gisement du site

Ces pages captent déjà la demande mais ne la convertissent pas : elles sont hors page 1.

| Article | Impressions | Position | Clics |
|---|---:|---:|---:|
| `erp-pme` | 21 856 | 41,8 | 3 |
| `bon-de-commande` | 21 834 | 26,7 | 32 |
| `cout-de-revient` | 19 665 | 25,6 → **13,5** sur 90 j | 65 |
| `erp-saas` | 18 166 | 22,4 | 9 |
| `tracabilite-de-la-viande` | 7 513 | 23,3 → **13,6** sur 90 j | 57 |

À elles seules : **89 024 impressions pour 166 clics**. `cout-de-revient` et
`tracabilite-de-la-viande` remontent déjà sur le trimestre — ce sont les deux à pousser d'abord.

### Les 12 fusions

Cible = la page qui a le plus de clics. **Chaque fusion exige une 301** : toutes les sources
portent des impressions, aucune n'est à jeter.

| Cluster | Sources → cible | Clics cumulés |
|---|---|---:|
| Variation de stock | `calcul-variations-de-stock` (100) · `calcul-…-cump-…-2025` (64) · `gestion-automatisee-des-variations-de-stock` (2) → **`variation-de-stock-positif-negatif`** | 741 |
| Gestion de stock | `gestion-des-inventaires` (2) · `reapprovisionnement-stocks` (2) · `gestion-stock-multi-entrepots` (0) → **`maitriser-la-gestion-des-stocks`** | 6 029 |
| Péremption / DLC | `dlc-ddm-dluo` (33) → **`alerte-date-peremption`** (132) | 165 |
| Stock de sécurité | `alerte-stock-securite` (5) → **`calcul-stock-de-securite`** (48) | 53 |
| Conformité | `contraintes-reglementations-…` (5) · `erp-conformite-agroalimentaire` (7) → **`conformite-haccp`** | 15 |
| Traçabilité lot & DLC | `erp-tracabilite-agroalimentaire` (2) → **`tracabilite-lot-dlc-logiciel`** | 3 |
| Traçabilité viande | `tracabilite-viande-logiciel` (0) → **`tracabilite-de-la-viande`** | 57 |
| Découpe viande | `erp-viande-volaille` (2) · `erp-decoupe-viande-poisson` (1) → **`gestion-decoupe-viande-logiciel`** | 4 |
| ERP SaaS / cloud | `erp-saas-cloud` (3) · `erp-cloud-saas-vs-on-premise` (1) → **`erp-saas`** | 13 |
| Coût de revient | `calcul-cout-de-revient-logiciel` (0 impr) → **`cout-de-revient`** | 65 |
| Alternatives Sage | `alternatives-sage-agroalimentaire` (6 impr) → **`alternative-sage-erp`** | 1 |
| Alternatives Cegid | `alternatives-cegid-distribution-alimentaire` (0 impr) → **`alternative-cegid`** | 3 |

Les deux slugs datés `2025` disparaissent avec la fusion du cluster variation de stock.

### Les 2 suppressions, 2 migrations, 2 mises en attente

| Article | Clics / Impr. | Verdict | Motif |
|---|---:|---|---|
| `erp-agroalimentaire` | 0 / 0 | **Supprimer** → 301 `/agroalimentaire/` | absent du sitemap **et** doublon de la landing mère |
| `partenariat-toncarton` | 1 / 163 | **Supprimer** → 301 `/ecosysteme/` | position 60,5 sur 16 mois, actualité partenaire |
| `integrateur-erp-paris` | 0 / 273 | **Migrer** | le vieux slug fautif `integateur-erp-paris` capte 924 impr |
| `integrateur-erp-lyon` | 0 / 111 | **Migrer** | idem, `integateur-erp-lyon` capte 467 impr |
| `reporting-commercial-grossiste` | 0 / 0 | **Attendre** | publié le 2026-06-19, trop jeune |
| `grille-tarifaire-negoce-alimentaire` | 1 / 42 | **Attendre** | publié le 2026-06-19 |

## Trouvailles hors périmètre, à traiter à part

La GSC révèle des URL qui ne sont dans aucun de tes 103 articles et qui captent du trafic :

- `/cout-prix-au-kilo` (sans `/blog/`) — **1 720 clics / 37 094 impressions**. Ancienne URL
  toujours servie en parallèle de `/blog/cout-prix-au-kilo` : doublon sur ton 1er article.
- `/6-exercices-corriges-pour-maitriser-la-gestion-des-stocks` — **1 060 clics**. Ancienne URL.
- `/blog/meilleur-erp-agroalimentaire` (66 clics) et `/blog/meilleurs-erp-traiteur` (18 clics) —
  anciens articles devenus comparatifs.
- **Slugs fautifs indexés** : `integateur-erp-paris` (924 impr), `integateur-erp-lyon` (467),
  `prixdachat-definition`, `prix-d-achat-definition`, `calculer-le-prix-de-en-boulangerie`,
  `difference-prix-dachat-et-prix-drevenu`, `calcul-du-pmp`.
- **La catégorie « Non classé » est indexée et paginée** : `category/non-classe-fr-fr/` jusqu'à
  `/page/11`. Les 103 articles sont tous dans cette seule catégorie — aucun n'est catégorisé.
  C'était déjà le point 3.5 de `AUDIT-MAILLAGE-INTERNE.md`, la GSC le confirme.

---

## Les 103 articles

Triés par clics sur 16 mois. `§` = section du hub agroalimentaire (cf. `HUB-AGROALIMENTAIRE.md`).

| # | Article | Mots | Clics 16 mois | Impr. 16 mois | Pos. | Clics 90 j | § | Verdict | Note / cible |
|---:|---|---:|---:|---:|---:|---:|:---:|---|---|
| 1 | [`cout-prix-au-kilo`](https://www.helloharel.com/blog/cout-prix-au-kilo/) | 1793 | 14112 | 523258 | 5.1 | 806 | §2 | **Garder** |  |
| 2 | [`maitriser-la-gestion-des-stocks`](https://www.helloharel.com/blog/maitriser-la-gestion-des-stocks/) | 3258 | 6025 | 103733 | 11.1 | 239 | §3 | **Garder** |  |
| 3 | [`numeros-de-lot`](https://www.helloharel.com/blog/numeros-de-lot/) | 2246 | 2823 | 100086 | 8.2 | 205 | §1 | **Garder** |  |
| 4 | [`calculer-le-prix-de-revient-en-boulangerie`](https://www.helloharel.com/blog/calculer-le-prix-de-revient-en-boulangerie/) | 3244 | 2147 | 93513 | 9.1 | 175 | §2 | **Garder** |  |
| 5 | [`calcul-du-prix-moyen`](https://www.helloharel.com/blog/calcul-du-prix-moyen/) | 2139 | 1406 | 225656 | 8.6 | 102 | §2 | **Garder** |  |
| 6 | [`facture-exacompta`](https://www.helloharel.com/blog/facture-exacompta/) | 1807 | 727 | 27511 | 8.7 | 38 | §5 | **Garder** |  |
| 7 | [`facture-traiteur`](https://www.helloharel.com/blog/facture-traiteur/) | 1464 | 635 | 43260 | 4.4 | 69 | §5 | **Garder** |  |
| 8 | [`variation-de-stock-positif-negatif`](https://www.helloharel.com/blog/variation-de-stock-positif-negatif/) | 1881 | 575 | 57587 | 8.2 | 40 | §3 | **Garder** |  |
| 9 | [`erp-as400`](https://www.helloharel.com/blog/erp-as400/) | 1627 | 570 | 90447 | 9.9 | 45 | §7 | **Garder** |  |
| 10 | [`bon-de-livraison`](https://www.helloharel.com/blog/bon-de-livraison/) | 1712 | 528 | 88404 | 11.5 | 19 | §5 | **Garder** |  |
| 11 | [`cout-marginal`](https://www.helloharel.com/blog/cout-marginal/) | 1853 | 520 | 119213 | 8.3 | 29 | §2 | **Garder** |  |
| 12 | [`ordre-de-fabrication`](https://www.helloharel.com/blog/ordre-de-fabrication/) | 1504 | 331 | 39619 | 10.0 | 25 | §4 | **Garder** |  |
| 13 | [`kpi-qualite-agroalimentaire`](https://www.helloharel.com/blog/kpi-qualite-agroalimentaire/) | 1738 | 329 | 14765 | 12.1 | 35 | §1 | **Garder** |  |
| 14 | [`prix-dachat-definition`](https://www.helloharel.com/blog/prix-dachat-definition/) | 1490 | 306 | 139614 | 6.8 | 50 | §2 | **Garder** |  |
| 15 | [`relance-client`](https://www.helloharel.com/blog/relance-client/) | 2324 | 273 | 61369 | 18.2 | 2 | — | **Garder** |  |
| 16 | [`couts-de-production`](https://www.helloharel.com/blog/couts-de-production/) | 1783 | 238 | 51457 | 11.1 | 5 | §2 | **Garder** |  |
| 17 | [`bon-de-commande-traiteur`](https://www.helloharel.com/blog/bon-de-commande-traiteur/) | 1428 | 235 | 8532 | 12.6 | 10 | §5 | **Garder** |  |
| 18 | [`min`](https://www.helloharel.com/blog/min/) | 1510 | 218 | 111757 | 9.0 | 21 | §6 | **Garder** |  |
| 19 | [`difference-prix-dachat-et-prix-de-revient`](https://www.helloharel.com/blog/difference-prix-dachat-et-prix-de-revient/) | 2123 | 205 | 44286 | 6.9 | 22 | §2 | **Garder** |  |
| 20 | [`calcul-du-cout-achat`](https://www.helloharel.com/blog/calcul-du-cout-achat/) | 1549 | 194 | 70817 | 9.3 | 9 | §2 | **Garder** |  |
| 21 | [`enregistrement-comptable-variation-de-stock`](https://www.helloharel.com/blog/enregistrement-comptable-variation-de-stock/) | 1819 | 171 | 29668 | 12.6 | 15 | §3 | **Garder** |  |
| 22 | [`fifo-fefo-lifo`](https://www.helloharel.com/blog/fifo-fefo-lifo/) | 1711 | 163 | 61533 | 14.8 | 10 | §3 | **Garder** |  |
| 23 | [`impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025`](https://www.helloharel.com/blog/impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025/) | 1740 | 133 | 13542 | 10.5 | 20 | §3 | **Garder** |  |
| 24 | [`alerte-date-peremption`](https://www.helloharel.com/blog/alerte-date-peremption/) | 1074 | 132 | 5672 | 14.3 | 6 | §1 | **Garder** |  |
| 25 | [`plan-de-controle-alimentaire`](https://www.helloharel.com/blog/plan-de-controle-alimentaire/) | 1486 | 122 | 7541 | 12.2 | 13 | §1 | **Garder** |  |
| 26 | [`agreage-agroalimentaire`](https://www.helloharel.com/blog/agreage-agroalimentaire/) | 1152 | 119 | 11877 | 7.9 | 17 | §1 | **Garder** |  |
| 27 | [`calcul-variations-de-stock`](https://www.helloharel.com/blog/calcul-variations-de-stock/) | 1505 | 100 | 45154 | 12.4 | 7 | §3 | **Fusionner** | → `variation-de-stock-positif-negatif` |
| 28 | [`meilleurs-erp-maraichers-fruits-legumes`](https://www.helloharel.com/blog/meilleurs-erp-maraichers-fruits-legumes/) | 1790 | 95 | 7800 | 9.1 | 40 | §8 | **Garder** |  |
| 29 | [`cout-de-revient`](https://www.helloharel.com/blog/cout-de-revient/) | 6330 | 65 | 19665 | 25.6 | 19 | §2 | **Retravailler** | 19 665 impressions en position 26 — demande captée  page à refaire |
| 30 | [`calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025`](https://www.helloharel.com/blog/calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025/) | 1879 | 64 | 24652 | 11.7 | 9 | §3 | **Fusionner** | → `variation-de-stock-positif-negatif` |
| 31 | [`tracabilite-de-la-viande`](https://www.helloharel.com/blog/tracabilite-de-la-viande/) | 1696 | 57 | 7513 | 23.3 | 6 | §1 | **Retravailler** | 7 513 impressions en position 23 — demande captée  page à refaire |
| 32 | [`calcul-stock-de-securite`](https://www.helloharel.com/blog/calcul-stock-de-securite/) | 1709 | 48 | 20387 | 13.2 | 8 | §3 | **Garder** |  |
| 33 | [`meilleurs-erp-import-export`](https://www.helloharel.com/blog/meilleurs-erp-import-export/) | 1497 | 47 | 6362 | 17.2 | 10 | §8 | **Garder** |  |
| 34 | [`conditionnement-alimentaire-erp`](https://www.helloharel.com/blog/conditionnement-alimentaire-erp/) | 1105 | 46 | 10601 | 17.6 | 4 | §4 | **Garder** |  |
| 35 | [`dlc-ddm-dluo`](https://www.helloharel.com/blog/dlc-ddm-dluo/) | 1305 | 33 | 8230 | 35.0 | 2 | §1 | **Fusionner** | → `alerte-date-peremption` |
| 36 | [`bon-de-commande`](https://www.helloharel.com/blog/bon-de-commande/) | 2554 | 32 | 21834 | 26.7 | 3 | §5 | **Retravailler** | 21 834 impressions en position 27 — demande captée  page à refaire |
| 37 | [`processus-agroalimentaire-guide`](https://www.helloharel.com/blog/processus-agroalimentaire-guide/) | 1278 | 29 | 2751 | 17.2 | 10 | §4 | **Garder** |  |
| 38 | [`roi-erp`](https://www.helloharel.com/blog/roi-erp/) | 1848 | 14 | 5957 | 15.9 | 1 | §8 | **Garder** |  |
| 39 | [`opc-ua`](https://www.helloharel.com/blog/opc-ua/) | 1418 | 12 | 3365 | 31.1 | 3 | §4 | **Garder** |  |
| 40 | [`erp-saas`](https://www.helloharel.com/blog/erp-saas/) | 1533 | 9 | 18166 | 22.4 | 0 | §7 | **Retravailler** | 18 166 impressions en position 22 — demande captée  page à refaire |
| 41 | [`alternative-vif-erp`](https://www.helloharel.com/blog/alternative-vif-erp/) | 1425 | 8 | 818 | 8.3 | 1 | §8 | **Garder** |  |
| 42 | [`alternative-akanea-erp`](https://www.helloharel.com/blog/alternative-akanea-erp/) | 2250 | 8 | 349 | 16.7 | 4 | §8 | **Garder** |  |
| 43 | [`erp-conformite-agroalimentaire`](https://www.helloharel.com/blog/erp-conformite-agroalimentaire/) | 1481 | 7 | 895 | 13.0 | 0 | §1 | **Fusionner** | → `conformite-haccp` |
| 44 | [`calcul-stock-moyen`](https://www.helloharel.com/blog/calcul-stock-moyen/) | 1658 | 6 | 2687 | 19.6 | 1 | §3 | **Garder** |  |
| 45 | [`optimisation-entrepot`](https://www.helloharel.com/blog/optimisation-entrepot/) | 2303 | 5 | 3899 | 38.3 | 0 | §3 | **Garder** |  |
| 46 | [`contraintes-reglementations-logiciel-agroalimentaire`](https://www.helloharel.com/blog/contraintes-reglementations-logiciel-agroalimentaire/) | 1199 | 5 | 1331 | 21.9 | 0 | §1 | **Fusionner** | → `conformite-haccp` |
| 47 | [`alerte-stock-securite`](https://www.helloharel.com/blog/alerte-stock-securite/) | 1193 | 5 | 680 | 22.7 | 0 | §3 | **Fusionner** | → `calcul-stock-de-securite` |
| 48 | [`meilleurs-erp-boulangerie`](https://www.helloharel.com/blog/meilleurs-erp-boulangerie/) | 2386 | 4 | 727 | 39.0 | 1 | §8 | **Garder** |  |
| 49 | [`erp-pme`](https://www.helloharel.com/blog/erp-pme/) | 1498 | 3 | 21856 | 41.8 | 1 | §7 | **Retravailler** | 21 856 impressions en position 42 — demande captée  page à refaire |
| 50 | [`erp-saas-cloud`](https://www.helloharel.com/blog/erp-saas-cloud/) | 1481 | 3 | 5470 | 44.0 | 1 | §7 | **Fusionner** | → `erp-saas` |
| 51 | [`conformite-haccp`](https://www.helloharel.com/blog/conformite-haccp/) | 4064 | 3 | 573 | 17.5 | 3 | §1 | **Garder** |  |
| 52 | [`alternative-cegid`](https://www.helloharel.com/blog/alternative-cegid/) | 2424 | 3 | 413 | 13.7 | 0 | §8 | **Garder** |  |
| 53 | [`factur-x-e-facturation-logiciel`](https://www.helloharel.com/blog/factur-x-e-facturation-logiciel/) | 3912 | 3 | 210 | 9.5 | 3 | §5 | **Garder** |  |
| 54 | [`logiciel-grossiste-alimentaire`](https://www.helloharel.com/blog/logiciel-grossiste-alimentaire/) | 3312 | 3 | 85 | 10.1 | 2 | §6 | **Garder** |  |
| 55 | [`gestion-des-inventaires`](https://www.helloharel.com/blog/gestion-des-inventaires/) | 1417 | 2 | 1842 | 45.5 | 0 | §3 | **Fusionner** | → `maitriser-la-gestion-des-stocks` |
| 56 | [`erp-grossiste-distributeur`](https://www.helloharel.com/blog/erp-grossiste-distributeur/) | 2908 | 2 | 1406 | 25.3 | 1 | §6 | **Garder** |  |
| 57 | [`ordonnancement-planification`](https://www.helloharel.com/blog/ordonnancement-planification/) | 1533 | 2 | 1306 | 32.5 | 1 | §4 | **Garder** |  |
| 58 | [`reapprovisionnement-stocks`](https://www.helloharel.com/blog/reapprovisionnement-stocks/) | 1416 | 2 | 879 | 20.7 | 0 | §3 | **Fusionner** | → `maitriser-la-gestion-des-stocks` |
| 59 | [`meilleurs-erp-gestion-approvisionnements`](https://www.helloharel.com/blog/meilleurs-erp-gestion-approvisionnements/) | 1362 | 2 | 714 | 24.6 | 1 | §8 | **Garder** |  |
| 60 | [`erp-tracabilite-agroalimentaire`](https://www.helloharel.com/blog/erp-tracabilite-agroalimentaire/) | 1253 | 2 | 625 | 27.5 | 0 | §1 | **Fusionner** | → `tracabilite-lot-dlc-logiciel` |
| 61 | [`erp-boissons`](https://www.helloharel.com/blog/erp-boissons/) | 4008 | 2 | 395 | 14.6 | 1 | §6 | **Garder** |  |
| 62 | [`gestion-automatisee-des-variations-de-stock`](https://www.helloharel.com/blog/gestion-automatisee-des-variations-de-stock/) | 1692 | 2 | 386 | 18.7 | 0 | §3 | **Fusionner** | → `variation-de-stock-positif-negatif` |
| 63 | [`logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises`](https://www.helloharel.com/blog/logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises/) | 1773 | 2 | 206 | 16.8 | 0 | §6 | **Garder** |  |
| 64 | [`erp-viande-volaille`](https://www.helloharel.com/blog/erp-viande-volaille/) | 1219 | 2 | 121 | 9.0 | 0 | §2 | **Fusionner** | → `gestion-decoupe-viande-logiciel` |
| 65 | [`erp-cloud-saas-vs-on-premise`](https://www.helloharel.com/blog/erp-cloud-saas-vs-on-premise/) | 2681 | 1 | 755 | 23.1 | 0 | §7 | **Fusionner** | → `erp-saas` |
| 66 | [`cuisine-centrale`](https://www.helloharel.com/blog/cuisine-centrale/) | 3058 | 1 | 526 | 12.4 | 0 | §4 | **Garder** |  |
| 67 | [`tracabilite-lot-dlc-logiciel`](https://www.helloharel.com/blog/tracabilite-lot-dlc-logiciel/) | 4085 | 1 | 432 | 6.4 | 1 | §1 | **Garder** |  |
| 68 | [`alternative-sage-erp`](https://www.helloharel.com/blog/alternative-sage-erp/) | 2057 | 1 | 260 | 12.2 | 0 | §8 | **Garder** |  |
| 69 | [`partenariat-toncarton`](https://www.helloharel.com/blog/partenariat-toncarton/) | 1231 | 1 | 163 | 60.5 | 0 | — | **Supprimer** | 1 clic / 163 impressions en position 60 sur 16 mois → 301 vers /ecosysteme/ |
| 70 | [`alternative-archipelia`](https://www.helloharel.com/blog/alternative-archipelia/) | 1396 | 1 | 125 | 17.2 | 0 | §8 | **Garder** |  |
| 71 | [`gestion-decoupe-viande-logiciel`](https://www.helloharel.com/blog/gestion-decoupe-viande-logiciel/) | 1920 | 1 | 96 | 7.8 | 1 | §2 | **Garder** |  |
| 72 | [`penalites-logistiques-gms`](https://www.helloharel.com/blog/penalites-logistiques-gms/) | 1531 | 1 | 70 | 8.5 | 1 | §6 | **Garder** |  |
| 73 | [`erp-decoupe-viande-poisson`](https://www.helloharel.com/blog/erp-decoupe-viande-poisson/) | 1631 | 1 | 67 | 26.8 | 0 | §2 | **Fusionner** | → `gestion-decoupe-viande-logiciel` |
| 74 | [`logiciel-gestion-calibre-fruits-legumes`](https://www.helloharel.com/blog/logiciel-gestion-calibre-fruits-legumes/) | 1457 | 1 | 64 | 19.0 | 1 | §4 | **Garder** |  |
| 75 | [`logiciel-prix-du-jour-fruits-legumes`](https://www.helloharel.com/blog/logiciel-prix-du-jour-fruits-legumes/) | 1492 | 1 | 54 | 26.9 | 1 | §6 | **Garder** |  |
| 76 | [`grille-tarifaire-negoce-alimentaire`](https://www.helloharel.com/blog/grille-tarifaire-negoce-alimentaire/) | 1405 | 1 | 42 | 7.7 | 1 | §6 | **Garder** |  |
| 77 | [`remplacer-excel-gestion-agroalimentaire`](https://www.helloharel.com/blog/remplacer-excel-gestion-agroalimentaire/) | 3100 | 1 | 10 | 6.5 | 1 | §7 | **Garder** |  |
| 78 | [`alternatives-divalto-agroalimentaire`](https://www.helloharel.com/blog/alternatives-divalto-agroalimentaire/) | 2562 | 0 | 293 | 7.7 | 0 | §8 | **Garder** |  |
| 79 | [`integrateur-erp-paris`](https://www.helloharel.com/blog/integrateur-erp-paris/) | 2082 | 0 | 273 | 14.0 | 0 | — | **Migrer** | 0 clic mais 273 impr · le vieux slug `integateur-erp-paris` en capte 924 → page sous /implantations/ |
| 80 | [`edi-logiciel-agroalimentaire`](https://www.helloharel.com/blog/edi-logiciel-agroalimentaire/) | 1836 | 0 | 157 | 31.4 | 0 | §6 | **Garder** |  |
| 81 | [`integrateur-erp-lyon`](https://www.helloharel.com/blog/integrateur-erp-lyon/) | 1424 | 0 | 111 | 13.6 | 0 | — | **Migrer** | 0 clic mais 111 impr · le vieux slug `integateur-erp-lyon` en capte 467 → page sous /implantations/ |
| 82 | [`migration-erp-agroalimentaire`](https://www.helloharel.com/blog/migration-erp-agroalimentaire/) | 1783 | 0 | 70 | 14.8 | 0 | §7 | **Garder** |  |
| 83 | [`logiciel-maree-mareyeur`](https://www.helloharel.com/blog/logiciel-maree-mareyeur/) | 1951 | 0 | 47 | 7.6 | 0 | §6 | **Garder** |  |
| 84 | [`hello-harel-vs-divalto`](https://www.helloharel.com/blog/hello-harel-vs-divalto/) | 2432 | 0 | 47 | 17.0 | 0 | §8 | **Garder** |  |
| 85 | [`hello-harel-vs-sage`](https://www.helloharel.com/blog/hello-harel-vs-sage/) | 2489 | 0 | 39 | 26.2 | 0 | §8 | **Garder** |  |
| 86 | [`calcul-freinte-charcuterie-logiciel`](https://www.helloharel.com/blog/calcul-freinte-charcuterie-logiciel/) | 1692 | 0 | 36 | 7.4 | 0 | §2 | **Garder** |  |
| 87 | [`logiciel-televente-alimentaire`](https://www.helloharel.com/blog/logiciel-televente-alimentaire/) | 3547 | 0 | 26 | 6.8 | 0 | §6 | **Garder** |  |
| 88 | [`hello-harel-vs-odoo`](https://www.helloharel.com/blog/hello-harel-vs-odoo/) | 2463 | 0 | 25 | 7.4 | 0 | §8 | **Garder** |  |
| 89 | [`alternatives-odoo-agroalimentaire`](https://www.helloharel.com/blog/alternatives-odoo-agroalimentaire/) | 2686 | 0 | 23 | 23.2 | 0 | §8 | **Garder** |  |
| 90 | [`tracabilite-viande-logiciel`](https://www.helloharel.com/blog/tracabilite-viande-logiciel/) | 1835 | 0 | 17 | 8.1 | 0 | §1 | **Fusionner** | → `tracabilite-de-la-viande` |
| 91 | [`logiciel-commande-grande-surface-traiteur`](https://www.helloharel.com/blog/logiciel-commande-grande-surface-traiteur/) | 1495 | 0 | 15 | 7.5 | 0 | §6 | **Garder** |  |
| 92 | [`alternatives-silog-agroalimentaire`](https://www.helloharel.com/blog/alternatives-silog-agroalimentaire/) | 2403 | 0 | 11 | 9.6 | 0 | §8 | **Garder** |  |
| 93 | [`logiciel-calcul-cout-de-revient-traiteur`](https://www.helloharel.com/blog/logiciel-calcul-cout-de-revient-traiteur/) | 1460 | 0 | 6 | 5.2 | 0 | §2 | **Garder** |  |
| 94 | [`alternatives-sage-agroalimentaire`](https://www.helloharel.com/blog/alternatives-sage-agroalimentaire/) | 2746 | 0 | 6 | 4.8 | 0 | §8 | **Fusionner** | → `alternative-sage-erp` |
| 95 | [`alternatives-copilote-traiteur`](https://www.helloharel.com/blog/alternatives-copilote-traiteur/) | 2683 | 0 | 4 | 9.8 | 0 | §8 | **Garder** |  |
| 96 | [`logiciel-gestion-recette-multi-niveaux-traiteur`](https://www.helloharel.com/blog/logiciel-gestion-recette-multi-niveaux-traiteur/) | 1395 | 0 | 3 | 4.3 | 0 | §2 | **Garder** |  |
| 97 | [`logiciel-tracabilite-dlc-traiteur`](https://www.helloharel.com/blog/logiciel-tracabilite-dlc-traiteur/) | 1474 | 0 | 3 | 4.3 | 0 | §1 | **Garder** |  |
| 98 | [`reporting-commercial-grossiste`](https://www.helloharel.com/blog/reporting-commercial-grossiste/) | 1409 | 0 | 0 | 0.0 | 0 | §6 | **Trop jeune** | jamais mesuré sur 16 mois — publié récemment, à revoir dans 3 mois |
| 99 | [`erp-agroalimentaire`](https://www.helloharel.com/blog/erp-agroalimentaire/) | 1625 | 0 | 0 | 0.0 | 0 | — | **Supprimer** | absent du sitemap + doublon de la landing mère → 301 vers /agroalimentaire/ |
| 100 | [`hello-harel-vs-silog`](https://www.helloharel.com/blog/hello-harel-vs-silog/) | 2354 | 0 | 0 | 0.0 | 0 | §8 | **Trop jeune** | jamais mesuré sur 16 mois — publié récemment, à revoir dans 3 mois |
| 101 | [`alternatives-cegid-distribution-alimentaire`](https://www.helloharel.com/blog/alternatives-cegid-distribution-alimentaire/) | 2644 | 0 | 0 | 0.0 | 0 | §8 | **Fusionner** | → `alternative-cegid` |
| 102 | [`gestion-stock-multi-entrepots`](https://www.helloharel.com/blog/gestion-stock-multi-entrepots/) | 4140 | 0 | 0 | 0.0 | 0 | §3 | **Fusionner** | → `maitriser-la-gestion-des-stocks` |
| 103 | [`calcul-cout-de-revient-logiciel`](https://www.helloharel.com/blog/calcul-cout-de-revient-logiciel/) | 4538 | 0 | 0 | 0.0 | 0 | §2 | **Fusionner** | → `cout-de-revient` |