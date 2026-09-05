# Étude de cannibalisation — 100 % du site helloharel.com

**Source :** Google Search Console, dimensions requête × page, 01/04 → 30/06/2026 (11 095 couples).
**Méthodo :** URLs normalisées (fragments `#…` retirés — sinon 90 % des « doublons » sont de faux positifs : une page vs ses ancres de sommaire), requêtes de marque exclues.

## Chiffres clés
- Requêtes non-marque : **6 411**
- Requêtes en **vraie cannibalisation** (≥2 pages distinctes) : **1 105 (17 %)**
- Dont **sérieuses** (≥2 pages en top 20) : **428**
- ⚠️ Artefact important : les **URLs à fragment** (`/blog/x/#s-2`) sont comptées comme des pages par GSC → à ignorer (même page).

## Clusters à traiter (par priorité)

### 🔴 Cluster 1 — « Prix / coûts d'achat / prix de revient » (LE plus gros)
Pages qui se cannibalisent :
- `/blog/prix-dachat-definition` (impliquée dans **162** requêtes — épicentre)
- `/blog/difference-prix-dachat-et-prix-de-revient` (111)
- `/blog/calcul-du-cout-achat` (106)
- `/blog/calcul-du-prix-moyen` (60)
- `/blog/cout-prix-au-kilo` (59)
- `/blog/cout-de-revient` (57)
- `/blog/couts-de-production`, `/blog/calculer-le-prix-de-revient-en-boulangerie`

Chevauchements les plus forts : `calcul-du-cout-achat` ⚔ `prix-dachat-definition` (**86 requêtes communes**), `difference-prix-dachat…` ⚔ `prix-dachat-definition` (70).
**Actions :**
- **1 page pilier par intention** : « prix d'achat » → `prix-dachat-definition` ; « coût d'achat » → `calcul-du-cout-achat` ; « coût de revient » → `cout-de-revient` ; « prix au kilo » → `cout-prix-au-kilo` ; « prix moyen » → `calcul-du-prix-moyen`.
- **Fusionner** les quasi-doublons (`calcul-du-cout-achat` très proche de `prix-dachat-definition` → 86 req. communes) ou différencier nettement les angles + canonical.
- Maillage : chaque article secondaire pointe vers le pilier de son intention avec ancre exacte.

### 🔴 Cluster 2 — « Variation de stock »
- `/blog/variation-de-stock-positif-negatif` (pilier, 41)
- `/blog/calcul-variations-de-stock` (41)
- `/blog/impact-de-la-variation-de-stock-sur-le-resultat-fiscal…` (23)
- `/blog/calcul-de-la-variation-de-stock-methode-cump…` (20)
- `/blog/enregistrement-comptable-variation-de-stock` (18)

**Actions :** garder `variation-de-stock-positif-negatif` comme **pilier généraliste** ; différencier les autres sur leur angle précis (CUMP, résultat fiscal, écriture comptable) + canonical/liens vers le pilier ; **fusionner** `calcul-variations-de-stock` (redondant, 24 req. communes avec le pilier).

### 🔴 Cluster 3 — « ERP agroalimentaire »
- `/agroalimentaire/` (hub, 41)
- `/blog/meilleur-erp-agroalimentaire` (32)
- `/` (homepage)
- `/fonctionnalites/crm` (20)

Hub ⚔ blog comparatif : 22 requêtes communes, 8 608 impressions, tous en pos 12-19 → **personne ne perce**.
**Actions :** **hub `/agroalimentaire/` = pilier transactionnel** (« erp agroalimentaire », « logiciel agroalimentaire »…) ; repositionner le blog sur l'intention **comparatif/informationnel** (« meilleur », « comparatif », « avis ») + lien fort blog→hub ; retirer le ciblage de ce terme sur la homepage.

### 🟠 Cluster 4 — « ERP fruits et légumes »
- `/agroalimentaire/maraicher/` (money page, **pos 41**)
- `/blog/meilleurs-erp-maraichers-fruits-legumes` (blog, **pos 6,3 — ranke MIEUX que la money page**)

**Actions :** lien fort blog → `/maraicher/` (ancre « erp fruits et légumes ») ; optimiser la money page (déjà P1 dans l'audit précédent) ; envisager canonical si le blog reste dominant.

### 🟠 Cluster 5 — pages métier agro clonées (déjà traité en partie)
Les pages métier (patissier/chocolatier/glacier/brasseur…) se cannibalisent sur des requêtes génériques à cause du contenu cloné (voir audit du 03/07). Différenciation du haut de page faite ; corps de fonctionnalités à divariser.

## Récapitulatif priorités
| Prio | Cluster | Pages | Action clé |
|---|---|---|---|
| 1 | Prix / coûts | 8 articles | Pilier par intention + fusion des doublons |
| 2 | Variation de stock | 5 articles | Pilier généraliste + angles + fusion |
| 3 | ERP agroalimentaire | hub + blog + home | Hub = pilier ; blog = comparatif |
| 4 | Fruits & légumes | money vs blog | Lien blog→money + optimisation |
| 5 | Pages métier clonées | 4-6 pages | Différencier le corps |
