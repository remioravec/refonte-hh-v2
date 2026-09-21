# Inventaire des pages, classé selon le schéma de maillage

- **Source** : `https://www.helloharel.com/sitemap.xml` (Rank Math) → `page-sitemap.xml` + `post-sitemap.xml`
- **Relevé le** : 2026-09-21
- **Volume** : **178 URL** = 76 pages + 102 articles
- **Référence méthode** : schéma de maillage (landing mère → filles BOFU → hub guide d'achat 8 sections → articles de choix)

⚠️ Le sitemap est la seule source ici. Les liens réellement posés en HTML ne sont pas vérifiés dans
ce document — voir `AUDIT-MAILLAGE-INTERNE.md` pour l'état des liens existants.

---

## 1. Ce que le sitemap donne, rôle par rôle

| Rôle du schéma | Site | Compte |
|---|---|---|
| Racine | `/` | 1 |
| **Landing mère** | `/agroalimentaire/` · `/negoce/` · `/medical/` · `/fonctionnalites/` | 4 |
| Landing mère à plat | `/implantations/` · `/intelligence-artificielle/` + `/erp-ia/` | 2 (+1 doublon) |
| **Fille business BOFU** | 15 métiers agro · 5 négoce · 5 medical · 13 fonctionnalités · 10 implantations · 4 IA | 52 |
| **Hub — guide d'achat** | **aucun** | **0** |
| Quasi-hub | `/comparatifs/` + 4 comparatifs | 5 |
| **Article de choix** | `/blog/*` | 102 |
| Support / conversion | `/tarifs/` `/contact/` `/qui-sommes-nous/` `/ecosysteme/` `/integrateurs/` `/blog/` `/migration-as400/` `/conformite-loi-anti-fraude-tva/` | 8 |
| Légal | `/cgu/` `/mentions-legales/` `/politique-de-confidentialite/` | 3 |

### Détail des filles par silo

**`/agroalimentaire/` (15)** — boulanger, brasseur, charcutier, chocolatier, conserverie, fromager,
glacier, industrie-laitiere, maraicher, patissier, plats-cuisines-industriels, poissonnier,
torrefacteur, traiteur, viande

**`/negoce/` (5)** — achats-approvisionnements, ventes-devis-commandes, stocks-multi-depots,
tracabilite-lots, tarifs-reporting-edi

**`/medical/` (5)** — dispositifs-medicaux, laboratoires, materiel-dentaire, maintien-a-domicile,
hygiene-professionnelle

**`/fonctionnalites/` (13+1)** — deux granularités mélangées au même palier :
- *courtes / tête* : achat, vente, crm, facturation, fabrication, logistique, gestion-de-stock, import-export, tracabilite-alimentaire
- *longue traîne* : facturation-automatique-bon-livraison, gestion-rendement-matiere-logiciel, planification-production-erp, logiciel-devis-commande-bon-livraison, gestion-consigne-bouteille-logiciel

**Implantations (10, à la racine)** — auvergne-rhone-alpes, belgique, bretagne, hauts-de-france,
ile-de-france, maurice, nouvelle-aquitaine, occitanie, reunion

**IA (4, à la racine)** — ia-analyse-predictive, ia-assistant-commercial, ia-automatisation-comptable,
ia-optimisation-stocks

---

## 2. Les écarts au schéma

### 2.1 Aucun hub guide d'achat — le trou central

Le schéma fait du hub la pièce maîtresse : page boost, 8 sections numérotées, lien réciproque avec la
landing mère, et **cible du « lien 1 » de chaque article de choix**. Aucune URL du site ne joue ce rôle.

Conséquence directe : les 102 articles n'ont aucun `§N` à viser. Le montage à 2 liens montants
(hub §N + landing) prévu par le schéma est aujourd'hui inapplicable — ce qui explique mécaniquement
les 14 articles orphelins relevés dans `AUDIT-MAILLAGE-INTERNE.md`.

`/comparatifs/` est ce qui s'en approche le plus, mais un comparatif n'est pas un guide d'achat :
il tranche entre éditeurs, il ne déplie pas les critères de choix en sections adressables.

### 2.2 Deux landings mères pour le silo IA

`/erp-ia/` **et** `/intelligence-artificielle/` coexistent, avec 4 filles `ia-*`. Le schéma impose de
vérifier la cannibalisation *avant* de mailler : à trancher en premier, sinon les liens montants des
4 filles se répartissent entre deux mères concurrentes.

### 2.3 URLs à plat qui ne portent pas leur silo

Les 10 `/implantation-x/` ne sont pas sous `/implantations/`, les 4 `/ia-x/` ne sont pas sous leur mère.
Le lien montant peut exister en HTML, mais l'URL ne signale pas l'appartenance au silo.

### 2.4 Clusters à vérifier pour cannibalisation

| Cluster | URL | Doublons les plus francs |
|---|---|---|
| Variation de stock | 6 | `calcul-variations-de-stock` · `calcul-de-la-variation-de-stock-methode-cump-...-2025` · `impact-...-resultat-fiscal-...-2025` (slugs datés 2025, on est en 2026) |
| Alternatives / vs | 16 | `alternatives-sage-agroalimentaire` **vs** `alternative-sage-erp` · `alternatives-cegid-distribution-alimentaire` **vs** `alternative-cegid` |
| Traçabilité | 7 sur 3 paliers | `tracabilite-de-la-viande` **vs** `tracabilite-viande-logiciel` · `/fonctionnalites/tracabilite-alimentaire/` **vs** `/negoce/tracabilite-lots/` |
| Coût / prix de revient | 12 | `cout-de-revient` · `calcul-cout-de-revient-logiciel` · `difference-prix-dachat-et-prix-de-revient` |
| Facturation | 6 | `/fonctionnalites/facturation/` **vs** `/fonctionnalites/facturation-automatique-bon-livraison/` |
| ERP SaaS | 2 | `erp-saas` **vs** `erp-saas-cloud` |

---

## 3. Le silo pilote

**Traiteur** est le plus avancé et le meilleur candidat pour poser le premier hub :

- fille business : `/agroalimentaire/traiteur/`
- comparatif : `/comparatifs/meilleur-erp-traiteur/`
- 6 articles déjà en place : `logiciel-calcul-cout-de-revient-traiteur`, `logiciel-gestion-recette-multi-niveaux-traiteur`,
  `logiciel-commande-grande-surface-traiteur`, `logiciel-tracabilite-dlc-traiteur`, `bon-de-commande-traiteur`,
  `facture-traiteur` (+ `alternatives-copilote-traiteur`)

Il manque le hub. Les 6 articles couvrent déjà de quoi alimenter 6 des 8 sections.
