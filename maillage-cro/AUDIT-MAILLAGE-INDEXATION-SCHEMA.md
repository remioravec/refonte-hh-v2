# Audit SEO — Maillage interne (surfeur raisonnable) & Indexation / Schema

**Site :** https://www.helloharel.com · **Périmètre :** 162 URL indexables (99 articles + 63 pages)
**Date de l'audit :** 2026-06-10

**Sources de données**
- *Maillage* : `inventory.json` — graphe de liens avec **classification de zone réelle** (lien contextuel = ancre située dans un `<p>` éditorial ; le boilerplate header/footer/menu est exclu), + `surfer.json` (PageRank pondéré surfeur-raisonnable). Snapshot du graphe éditorial **antérieur** à la publication de l'article EDI (1ᵉʳ juin) et des derniers enrichissements — les chiffres d'orphelins du négoce/coûts sont donc un **majorant** (déjà partiellement résorbé).
- *Indexation / Schema* : crawl **frais ce jour** (`audit-indexation.json`, `audit_index_schema.py`) — statut HTTP, canonical, meta robots, sitemaps XML et **tous les `@type` JSON-LD** servis (Rank Math, côté serveur).

---

## Partie 1 — Maillage interne · modèle du surfeur raisonnable

Le « surfeur raisonnable » ne suit pas tous les liens à poids égal : un lien **éditorial, dans le corps du texte** vaut beaucoup plus qu'un lien de **menu/footer** répété sur tout le site. Tout l'audit ci-dessous ne compte donc que les **liens contextuels** (in-`<p>`).

### 1.1 Vue d'ensemble

| Indicateur | Valeur |
|---|---|
| URL indexables | 162 (99 articles, 63 pages) |
| Liens **contextuels** internes (vers URL propres) | **417** |
| Liens contextuels entrants par URL | moyenne **2,49** · médiane **1** · max 51 |
| **Orphelins contextuels** (0 lien éditorial entrant) | **77** (36 articles, 41 pages) |
| **Culs-de-sac contextuels** (0 lien éditorial sortant) | **83** |
| Ancres contextuelles distinctes | 349 |
| Ancres « cannibales » (1 ancre → plusieurs cibles) | **7 seulement** ✅ |

> **Lecture :** la *diversification d'ancres* est saine (349 ancres pour 417 liens ; `/agroalimentaire/` reçoit 72 liens via **51 ancres** distinctes). En revanche la **distribution est très concentrée** : médiane à 1 lien entrant, et près de la moitié des URL sans aucun lien éditorial entrant.

### 1.2 Le point critique — des pages « money » privées de jus éditorial

9 pages de conversion ont **0 lien contextuel entrant** :

| Page money | Liens éditoriaux entrants |
|---|---|
| `/comparatifs/` | **0** |
| `/agroalimentaire/boulanger/` | **0** |
| `/fonctionnalites/planification-production-erp/` | **0** |
| `/fonctionnalites/gestion-consigne-bouteille-logiciel/` | **0** |
| `/fonctionnalites/logiciel-devis-commande-bon-livraison/` | **0** |
| `/negoce/achats-approvisionnements/` | **0** |
| `/negoce/stocks-multi-depots/` | **0** |
| `/negoce/tarifs-reporting-edi/` | **0** |
| `/negoce/ventes-devis-commandes/` | **0** |

> **Tout le cocon « négoce » (5 pages filles sur 6) est en orphelin éditorial**, et la mère `/negoce/` ne reçoit que 3 liens. À l'inverse, le cocon « fonctionnalités » est bien irrigué (`gestion-de-stock` 58, `fabrication` 36, `vente` 29, `logistique` 21, `facturation` 18). C'est un **déséquilibre de cocon**, pas un problème global.

### 1.3 PageRank pondéré (surfeur raisonnable)

- **Tête** : `/fonctionnalites/gestion-de-stock/` (20,08), `/agroalimentaire/traiteur/`, `/fonctionnalites/fabrication/`, `/fonctionnalites/vente/` — cohérent, les piliers concentrent le jus.
- **Queue** : pages `/implantation-*` (SEO local, ~0,99) et quelques articles (`integrateur-erp-lyon/paris`, `calcul-du-cout-achat`, `logiciel-maree-mareyeur`) proches du minimum → quasi invisibles dans le graphe interne.
- `/comparatifs/` à **2,04** : très faible pour une page commerciale.

### 1.4 Lien interne vers une 404

`/blog/logiciel-maree-mareyeur/` est **référencé en interne** (et listé au sitemap) alors qu'il renvoie **404** → gaspillage de jus + signal de qualité négatif (voir §2.2).

### 1.5 Recommandations maillage (priorisées)

1. **P0 — Irriguer le cocon négoce.** Depuis chaque article « grossiste / distribution / EDI / stock multi-dépôts » et depuis `/negoce/`, ajouter 1 lien éditorial descendant vers chacune des 5 filles négoce. Cible : ≥ 3 liens contextuels entrants par page money sous 1 sprint.
2. **P0 — Réparer la 404** `logiciel-maree-mareyeur` (republier l'article ou rediriger 301) et purger le lien interne + l'entrée sitemap.
3. **P1 — `/comparatifs/` et `/agroalimentaire/boulanger/`** : créer des liens descendants depuis les articles de leur thématique (boulangerie, comparatifs d'ERP).
4. **P2 — Réduire les 83 culs-de-sac** : chaque page de fin de parcours doit proposer ≥ 2 liens éditoriaux « pour aller plus loin » vers sa mère + une sœur (anti-rebond, redistribution du jus).
5. **Conserver** la diversification d'ancres actuelle (très bonne) ; surveiller seulement l'ancre de marque « hello harel » (3 cibles).

---

## Partie 2 — Indexation & Données structurées (Schema.org)

### 2.1 Santé d'indexation (crawl du jour)

| Contrôle | Résultat |
|---|---|
| Codes HTTP | **161 × 200**, **1 × 404** |
| Redirections internes | **0** ✅ |
| Canonical auto-référente | **100 %** (0 canonical croisée) ✅ |
| `meta robots` noindex | **1 page** : `/blog/erp-agroalimentaire/` |
| Robots.txt / sitemap_index | OK (`post-sitemap` + `page-sitemap`) |

Hygiène technique **excellente** (canonical et redirections), à deux exceptions près traitées ci-dessous.

### 2.2 Couverture du sitemap — 10 articles indexables manquants + 1 URL morte listée

Le sitemap déclare **88 articles** alors que **98 sont en ligne et indexables**. **10 articles `index,follow` sont absents du sitemap** (Google les découvrira plus lentement) :

```
/blog/calcul-freinte-charcuterie-logiciel/
/blog/gestion-decoupe-viande-logiciel/
/blog/gestion-stock-multi-entrepots/
/blog/logiciel-calcul-cout-de-revient-traiteur/
/blog/logiciel-commande-grande-surface-traiteur/
/blog/logiciel-gestion-calibre-fruits-legumes/
/blog/logiciel-gestion-recette-multi-niveaux-traiteur/
/blog/logiciel-prix-du-jour-fruits-legumes/
/blog/logiciel-tracabilite-dlc-traiteur/
/blog/tracabilite-viande-logiciel/
```

À l'inverse, le sitemap **liste une URL en 404** : `/blog/logiciel-maree-mareyeur/`.
→ Sitemap **désynchronisé** : forcer la régénération Rank Math, vérifier qu'aucune exclusion n'est posée sur ces 10 articles, retirer l'URL morte. (`/blog/erp-agroalimentaire/` en `noindex` est, lui, **correctement** exclu — à confirmer que le noindex est volontaire.)

### 2.3 ⚠️ Schema « aggregating » — une note d'avis identique sur **toutes** les pages

C'est le point le plus à risque. Le bloc `SoftwareApplication` + **`AggregateRating` + `Offer`** est injecté sur **161 / 161 pages**, avec **exactement la même valeur partout** :

```
ratingValue = 5.0   ·   reviewCount = 31
```

…y compris sur `/mentions-legales/`, sur chaque article de blog, sur les pages négoce, etc.

**Pourquoi c'est un problème.** Les règles Google sur les données structurées exigent qu'un `AggregateRating` :
- porte sur **l'entité principale de la page** (or ici un article « prix au kilo » ou une page « mentions légales » n'est pas l'application notée) ;
- soit **adossé à des avis réellement visibles sur la page**.

Stamper la même note **5,0/31** sur 161 URL hétérogènes correspond au motif que Google sanctionne (rich-results invalides, voire **action manuelle** « avis » à l'échelle du site). Le **5,0 parfait** est en outre un signal de défiance.

**Reco P0 :** restreindre `SoftwareApplication`/`AggregateRating` aux **seules pages produit légitimes** (accueil, piliers `/agroalimentaire/`, `/fonctionnalites/`, `/negoce/`, `/tarifs/`) **et** y afficher de vrais avis. Le **retirer de tous les articles de blog et des pages légales**. (Réglage Rank Math : désactiver le schema produit global, le poser par type de contenu.)

### 2.4 Données structurées — couverture & cohérence

| `@type` | Présence | Lecture |
|---|---|---|
| Organization / SoftwareApplication / Offer / **AggregateRating** | 161/161 | cf. §2.3 — sur-déployé |
| Article (BlogPosting) | **98/98 articles** ✅ | parfait |
| **FAQPage** | **79/98 articles** | **19 articles sans FAQ** + **5 pages négoce sans FAQ** |
| **BreadcrumbList** | **57/62 pages — mais 0/99 articles** | incohérence : **aucun fil d'Ariane structuré sur le blog** |
| LocalBusiness (+Geo/OpeningHours) | 52 pages | OK sur pages locales/piliers |

**19 articles sans `FAQPage`** (opportunité de rich-result « FAQ ») :
```
bon-de-commande-traiteur · calcul-du-cout-achat · calcul-du-prix-moyen ·
calcul-stock-de-securite · calcul-stock-moyen · calcul-variations-de-stock ·
calculer-le-prix-de-revient-en-boulangerie · contraintes-reglementations-logiciel-agroalimentaire ·
cout-prix-au-kilo · couts-de-production · erp-as400 · facture-exacompta ·
facture-traiteur · maitriser-la-gestion-des-stocks · numeros-de-lot ·
optimisation-entrepot · ordonnancement-planification · partenariat-toncarton ·
tracabilite-de-la-viande
```
> Les 3 articles **cout-prix-au-kilo, couts-de-production, calcul-du-prix-moyen** reçoivent justement un bloc FAQ + JSON-LD `FAQPage` dans l'enrichissement en attente de publication (branche `claude/eloquent-gates-74uAa`).

**5 pages négoce sans FAQPage** (et qui sont aussi orphelines, cf. §1.2) : `achats-approvisionnements`, `stocks-multi-depots`, `tarifs-reporting-edi`, `tracabilite-lots`, `ventes-devis-commandes` → ces pages utilisent un **template différent** (pas de `LocalBusiness`, pas de `FAQPage`), d'où une incohérence de balisage avec les autres pages money.

### 2.5 Recommandations Schema/indexation (priorisées)

1. **P0 — Avis (`AggregateRating`)** : sortir le schema produit/avis des articles et pages légales ; le réserver aux pages produit avec avis visibles (§2.3). Risque d'action manuelle.
2. **P0 — Sitemap** : régénérer, intégrer les 10 articles manquants, retirer l'URL 404.
3. **P1 — BreadcrumbList sur le blog** : activer le fil d'Ariane structuré sur les 99 articles (cohérence + rich-result fil d'Ariane).
4. **P1 — FAQPage** : compléter les 19 articles + 5 pages négoce (commencer par les 3 déjà enrichis, puis les pages money négoce).
5. **P2 — Uniformiser le template négoce** sur le standard des autres pages money (LocalBusiness + FAQ).
6. **P2** — confirmer le `noindex` volontaire de `/blog/erp-agroalimentaire/`.

---

## Synthèse — top 5 actions

| # | Action | Axe | Effort | Impact |
|---|---|---|---|---|
| 1 | Sortir `AggregateRating` des articles + pages légales | Schema | Moyen | **Élevé (risque pénalité)** |
| 2 | Régénérer le sitemap (+10 articles, −1 URL 404) | Indexation | Faible | Élevé |
| 3 | Irriguer le cocon négoce (liens éditoriaux descendants) | Maillage | Moyen | Élevé |
| 4 | Réparer/rediriger la 404 `logiciel-maree-mareyeur` | Maillage+Index | Faible | Moyen |
| 5 | BreadcrumbList + FAQPage manquants sur le blog | Schema | Moyen | Moyen |

*Données reproductibles : `audit_index_schema.py` → `audit-indexation.json` ; `surfer_study.py` → `surfer.json` ; graphe contextuel dans `inventory.json`.*
