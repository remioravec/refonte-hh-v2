# Les 103 articles de blog — inventaire complet et arbitrage

- **Source** : `wp-json/wp/v2/posts` (état live), relevé le 2026-09-21 → **103 articles**
  (le sitemap n'en liste que 102 : `erp-agroalimentaire` en est absent)
- **Mots** : corps réel de l'article, boilerplate Elementor retiré (le template pesait 9 766 mots par article dans l'export)
- **ETV / Kw** : trafic organique estimé et nombre de mots-clés positionnés, **DataForSEO France**

## ⚠️ La donnée GSC n'a pas pu être utilisée

Le compte Search Console connecté à cette session expose 14 propriétés (destockcbd, aurlane,
nishikidori, akademiaformation, pawy, risqeo, raisefx, getsillage, spn-net, logopsietudes,
lecomptoirdespoivres, authentiquegypte, spa-alina) — **helloharel.com n'en fait pas partie**.

Les colonnes ETV / Kw sont donc un **proxy DataForSEO**, pas la GSC. Ce que ça change :

- le proxy ne voit **ni les impressions sans clic, ni la longue traîne** — or c'est exactement
  ce que ta méthode utilise pour décider (« le volume nul n'écarte rien si la GSC mesure des affichages ») ;
- il se trompe déjà au moins une fois de façon vérifiable : `erp-pme` est à 0 dans le proxy alors
  que le point d'avancement d'août mesurait **~799 vues/mois** sur l'ancienne URL redirigée.

**Aucune suppression ne doit être exécutée sur cette base seule.** Les verdicts ci-dessous sont
une présélection à confirmer en GSC, par : `helloharel.com` ajouté au compte Google connecté,
ou un export Pages + Requêtes sur 16 mois déposé dans le repo.

## Résultat de l'arbitrage

| Verdict | Nb | Effet |
|---|---:|---|
| **Garder** | 77 | rattachés aux 8 sections du hub (2 hors hub) |
| **Fusionner** | 20 | 20 articles absorbés dans 13 cibles |
| **Supprimer** | 4 | hors silo ou doublon de landing |
| **Migrer** | 2 | contenu local à basculer en page |
| | **103 → 77** | −25 % d'URL, à ETV constant |

### Les 13 fusions

| Cluster | Articles | Cible | ETV consolidé |
|---|---:|---|---:|
| Variation de stock (calcul) | 4 → 1 | `variation-de-stock-positif-negatif` | 25,2 |
| Variation de stock (comptable/fiscal) | 2 → 1 | `enregistrement-comptable-variation-de-stock` | 4,7 |
| Gestion de stock | 3 → 1 | `maitriser-la-gestion-des-stocks` | 4,2 |
| Coût de revient | 2 → 1 | `cout-de-revient` | 0 |
| Conformité réglementaire | 3 → 1 | `conformite-haccp` | 0 |
| Découpe viande | 3 → 1 | `gestion-decoupe-viande-logiciel` | 0 |
| ERP SaaS / cloud | 3 → 1 | `erp-saas` | 1,6 |
| Traçabilité lot & DLC | 2 → 1 | `tracabilite-lot-dlc-logiciel` | 0 |
| Traçabilité viande | 2 → 1 | `tracabilite-de-la-viande` | 2,7 |
| Stock de sécurité | 2 → 1 | `calcul-stock-de-securite` | 1,4 |
| Date de péremption | 2 → 1 | `dlc-ddm-dluo` | 17,5 |
| Alternatives Sage | 2 → 1 | `alternatives-sage-agroalimentaire` | 0 |
| Alternatives Cegid | 2 → 1 | `alternatives-cegid-distribution-alimentaire` | 0 |

Deux slugs portent encore `2025` et disparaissent avec leur fusion :
`calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025` et
`impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025`.

### Les 4 suppressions et 2 migrations

| Article | ETV | Verdict | Motif |
|---|---:|---|---|
| `erp-agroalimentaire` | 0 | Supprimer → `/agroalimentaire/` | absent du sitemap **et** doublon de la landing mère |
| `partenariat-toncarton` | 0 | Supprimer → `/ecosysteme/` | actualité partenaire, aucun rôle SEO |
| `opc-ua` | 0 | Supprimer | industrie 4.0 pure, hors silo agro/négoce |
| `facture-exacompta` | 0 | Supprimer | Exacompta = papeterie, hors sujet ERP — à confirmer en GSC |
| `integrateur-erp-paris` | 0 | Migrer | contenu local → page sous `/implantations/` |
| `integrateur-erp-lyon` | 0 | Migrer | contenu local → page sous `/implantations/` |

### Concentration du trafic

Sur **1 560 d'ETV** pour tout le blog : **73 % sur 4 articles** (`cout-prix-au-kilo` 608,
`cout-marginal` 335, `prix-dachat-definition` 116, `calcul-du-prix-moyen` 85).
**72 articles sur 103 sont à zéro** dans le proxy.

---

## Les 103 articles

Triés par ETV décroissant. `§` = section du hub agroalimentaire (cf. `HUB-AGROALIMENTAIRE.md`).

| # | Article | Mots | ETV | Kw | § hub | Verdict | Note / cible |
|---:|---|---:|---:|---:|:---:|---|---|
| 1 | [`cout-prix-au-kilo`](https://www.helloharel.com/blog/cout-prix-au-kilo/) | 1793 | 608.5 | 20 | §2 | **Garder** | pilier §2 — 1re source de trafic du site |
| 2 | [`cout-marginal`](https://www.helloharel.com/blog/cout-marginal/) | 1853 | 335.4 | 19 | §2 | **Garder** |  |
| 3 | [`prix-dachat-definition`](https://www.helloharel.com/blog/prix-dachat-definition/) | 1490 | 116.3 | 8 | §2 | **Garder** |  |
| 4 | [`calcul-du-prix-moyen`](https://www.helloharel.com/blog/calcul-du-prix-moyen/) | 2139 | 84.5 | 15 | §2 | **Garder** |  |
| 5 | [`numeros-de-lot`](https://www.helloharel.com/blog/numeros-de-lot/) | 2246 | 79.9 | 10 | §1 | **Garder** | pilier §1 |
| 6 | [`difference-prix-dachat-et-prix-de-revient`](https://www.helloharel.com/blog/difference-prix-dachat-et-prix-de-revient/) | 2123 | 74.0 | 13 | §2 | **Garder** |  |
| 7 | [`erp-as400`](https://www.helloharel.com/blog/erp-as400/) | 1627 | 63.0 | 7 | §7 | **Garder** | pilier §7 — porte l'offre de migration |
| 8 | [`calculer-le-prix-de-revient-en-boulangerie`](https://www.helloharel.com/blog/calculer-le-prix-de-revient-en-boulangerie/) | 3244 | 32.6 | 2 | §2 | **Garder** |  |
| 9 | [`fifo-fefo-lifo`](https://www.helloharel.com/blog/fifo-fefo-lifo/) | 1711 | 24.0 | 14 | §3 | **Garder** | pilier §3 |
| 10 | [`variation-de-stock-positif-negatif`](https://www.helloharel.com/blog/variation-de-stock-positif-negatif/) | 1881 | 21.4 | 8 | §3 | **Garder** | cible de fusion du cluster variation |
| 11 | [`dlc-ddm-dluo`](https://www.helloharel.com/blog/dlc-ddm-dluo/) | 1305 | 17.5 | 8 | §1 | **Garder** | cible de fusion péremption |
| 12 | [`min`](https://www.helloharel.com/blog/min/) | 1510 | 13.2 | 5 | §6 | **Garder** | corriger les 14 liens morts href=# |
| 13 | [`processus-agroalimentaire-guide`](https://www.helloharel.com/blog/processus-agroalimentaire-guide/) | 1278 | 12.6 | 2 | §4 | **Garder** | cible de fusion conditionnement |
| 14 | [`calcul-du-cout-achat`](https://www.helloharel.com/blog/calcul-du-cout-achat/) | 1549 | 11.9 | 3 | §2 | **Garder** | intention proche de prix-dachat-definition — à surveiller |
| 15 | [`relance-client`](https://www.helloharel.com/blog/relance-client/) | 2324 | 9.1 | 3 | — | **Garder** | hors silo (recouvrement) — garder, ne pas mailler au hub |
| 16 | [`plan-de-controle-alimentaire`](https://www.helloharel.com/blog/plan-de-controle-alimentaire/) | 1486 | 8.5 | 4 | §1 | **Garder** |  |
| 17 | [`bon-de-livraison`](https://www.helloharel.com/blog/bon-de-livraison/) | 1712 | 6.5 | 7 | §5 | **Garder** | pilier §5 |
| 18 | [`couts-de-production`](https://www.helloharel.com/blog/couts-de-production/) | 1783 | 6.3 | 12 | §2 | **Garder** |  |
| 19 | [`bon-de-commande`](https://www.helloharel.com/blog/bon-de-commande/) | 2554 | 5.2 | 1 | §5 | **Garder** |  |
| 20 | [`agreage-agroalimentaire`](https://www.helloharel.com/blog/agreage-agroalimentaire/) | 1152 | 5.0 | 2 | §1 | **Garder** |  |
| 21 | [`ordre-de-fabrication`](https://www.helloharel.com/blog/ordre-de-fabrication/) | 1504 | 4.7 | 3 | §4 | **Garder** | pilier §4 |
| 22 | [`maitriser-la-gestion-des-stocks`](https://www.helloharel.com/blog/maitriser-la-gestion-des-stocks/) | 3258 | 4.2 | 1 | §3 | **Garder** | cible de fusion gestion de stock |
| 23 | [`enregistrement-comptable-variation-de-stock`](https://www.helloharel.com/blog/enregistrement-comptable-variation-de-stock/) | 1819 | 3.9 | 7 | §3 | **Garder** | garder : intention comptable distincte |
| 24 | [`calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025`](https://www.helloharel.com/blog/calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025/) | 1879 | 3.6 | 10 | §3 | **Fusionner** | → `variation-de-stock-positif-negatif` |
| 25 | [`tracabilite-de-la-viande`](https://www.helloharel.com/blog/tracabilite-de-la-viande/) | 1696 | 2.7 | 2 | §1 | **Garder** | cible de fusion traçabilité viande |
| 26 | [`erp-saas`](https://www.helloharel.com/blog/erp-saas/) | 1533 | 1.6 | 1 | §7 | **Garder** | cible de fusion SaaS/cloud |
| 27 | [`calcul-stock-moyen`](https://www.helloharel.com/blog/calcul-stock-moyen/) | 1658 | 1.6 | 3 | §3 | **Garder** |  |
| 28 | [`calcul-stock-de-securite`](https://www.helloharel.com/blog/calcul-stock-de-securite/) | 1709 | 1.4 | 3 | §3 | **Garder** | cible de fusion stock de sécurité |
| 29 | [`impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025`](https://www.helloharel.com/blog/impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025/) | 1740 | 0.8 | 1 | §3 | **Fusionner** | → `enregistrement-comptable-variation-de-stock` |
| 30 | [`calcul-variations-de-stock`](https://www.helloharel.com/blog/calcul-variations-de-stock/) | 1505 | 0.2 | 1 | §3 | **Fusionner** | → `variation-de-stock-positif-negatif` |
| 31 | [`conditionnement-alimentaire-erp`](https://www.helloharel.com/blog/conditionnement-alimentaire-erp/) | 1105 | 0.1 | 1 | §4 | **Fusionner** | → `processus-agroalimentaire-guide` |
| 32 | [`alerte-date-peremption`](https://www.helloharel.com/blog/alerte-date-peremption/) | 1074 | 0.0 | 0 | §1 | **Fusionner** | → `dlc-ddm-dluo` |
| 33 | [`alerte-stock-securite`](https://www.helloharel.com/blog/alerte-stock-securite/) | 1193 | 0.0 | 0 | §3 | **Fusionner** | → `calcul-stock-de-securite` |
| 34 | [`contraintes-reglementations-logiciel-agroalimentaire`](https://www.helloharel.com/blog/contraintes-reglementations-logiciel-agroalimentaire/) | 1199 | 0.0 | 0 | §1 | **Fusionner** | → `conformite-haccp` |
| 35 | [`erp-viande-volaille`](https://www.helloharel.com/blog/erp-viande-volaille/) | 1219 | 0.0 | 0 | §2 | **Fusionner** | → `gestion-decoupe-viande-logiciel` |
| 36 | [`partenariat-toncarton`](https://www.helloharel.com/blog/partenariat-toncarton/) | 1231 | 0.0 | 0 | — | **Supprimer** | actualité partenaire, aucun rôle SEO → rediriger /ecosysteme/ |
| 37 | [`erp-tracabilite-agroalimentaire`](https://www.helloharel.com/blog/erp-tracabilite-agroalimentaire/) | 1253 | 0.0 | 0 | §1 | **Fusionner** | → `tracabilite-lot-dlc-logiciel` |
| 38 | [`meilleurs-erp-gestion-approvisionnements`](https://www.helloharel.com/blog/meilleurs-erp-gestion-approvisionnements/) | 1362 | 0.0 | 0 | §8 | **Garder** |  |
| 39 | [`logiciel-gestion-recette-multi-niveaux-traiteur`](https://www.helloharel.com/blog/logiciel-gestion-recette-multi-niveaux-traiteur/) | 1395 | 0.0 | 0 | §2 | **Garder** | silo traiteur |
| 40 | [`alternative-archipelia`](https://www.helloharel.com/blog/alternative-archipelia/) | 1396 | 0.0 | 0 | §8 | **Garder** |  |
| 41 | [`grille-tarifaire-negoce-alimentaire`](https://www.helloharel.com/blog/grille-tarifaire-negoce-alimentaire/) | 1405 | 0.0 | 0 | §6 | **Garder** |  |
| 42 | [`reporting-commercial-grossiste`](https://www.helloharel.com/blog/reporting-commercial-grossiste/) | 1409 | 0.0 | 0 | §6 | **Garder** |  |
| 43 | [`reapprovisionnement-stocks`](https://www.helloharel.com/blog/reapprovisionnement-stocks/) | 1416 | 0.0 | 0 | §3 | **Fusionner** | → `maitriser-la-gestion-des-stocks` |
| 44 | [`gestion-des-inventaires`](https://www.helloharel.com/blog/gestion-des-inventaires/) | 1417 | 0.0 | 0 | §3 | **Fusionner** | → `maitriser-la-gestion-des-stocks` |
| 45 | [`opc-ua`](https://www.helloharel.com/blog/opc-ua/) | 1418 | 0.0 | 0 | — | **Supprimer** | industrie 4.0 pure, hors silo agro/négoce |
| 46 | [`integrateur-erp-lyon`](https://www.helloharel.com/blog/integrateur-erp-lyon/) | 1424 | 0.0 | 0 | — | **Migrer** | local → basculer en page sous /implantations/ |
| 47 | [`alternative-vif-erp`](https://www.helloharel.com/blog/alternative-vif-erp/) | 1425 | 0.0 | 0 | §8 | **Garder** |  |
| 48 | [`bon-de-commande-traiteur`](https://www.helloharel.com/blog/bon-de-commande-traiteur/) | 1428 | 0.0 | 0 | §5 | **Garder** | silo traiteur |
| 49 | [`logiciel-gestion-calibre-fruits-legumes`](https://www.helloharel.com/blog/logiciel-gestion-calibre-fruits-legumes/) | 1457 | 0.0 | 0 | §4 | **Garder** | silo maraîcher |
| 50 | [`logiciel-calcul-cout-de-revient-traiteur`](https://www.helloharel.com/blog/logiciel-calcul-cout-de-revient-traiteur/) | 1460 | 0.0 | 0 | §2 | **Garder** | silo traiteur |
| 51 | [`facture-traiteur`](https://www.helloharel.com/blog/facture-traiteur/) | 1464 | 0.0 | 0 | §5 | **Garder** | silo traiteur |
| 52 | [`logiciel-tracabilite-dlc-traiteur`](https://www.helloharel.com/blog/logiciel-tracabilite-dlc-traiteur/) | 1474 | 0.0 | 0 | §1 | **Garder** | silo traiteur |
| 53 | [`erp-conformite-agroalimentaire`](https://www.helloharel.com/blog/erp-conformite-agroalimentaire/) | 1481 | 0.0 | 0 | §1 | **Fusionner** | → `conformite-haccp` |
| 54 | [`erp-saas-cloud`](https://www.helloharel.com/blog/erp-saas-cloud/) | 1481 | 0.0 | 0 | §7 | **Fusionner** | → `erp-saas` |
| 55 | [`logiciel-prix-du-jour-fruits-legumes`](https://www.helloharel.com/blog/logiciel-prix-du-jour-fruits-legumes/) | 1492 | 0.0 | 0 | §6 | **Garder** | silo maraîcher |
| 56 | [`logiciel-commande-grande-surface-traiteur`](https://www.helloharel.com/blog/logiciel-commande-grande-surface-traiteur/) | 1495 | 0.0 | 0 | §6 | **Garder** | silo traiteur |
| 57 | [`meilleurs-erp-import-export`](https://www.helloharel.com/blog/meilleurs-erp-import-export/) | 1497 | 0.0 | 0 | §8 | **Garder** |  |
| 58 | [`erp-pme`](https://www.helloharel.com/blog/erp-pme/) | 1498 | 0.0 | 0 | — | **Garder** | ⚠ 0 en proxy mais ~799 vues/mois mesurées en août — NE PAS toucher sans GSC |
| 59 | [`penalites-logistiques-gms`](https://www.helloharel.com/blog/penalites-logistiques-gms/) | 1531 | 0.0 | 0 | §6 | **Garder** | pilier §6 |
| 60 | [`ordonnancement-planification`](https://www.helloharel.com/blog/ordonnancement-planification/) | 1533 | 0.0 | 0 | §4 | **Garder** |  |
| 61 | [`erp-agroalimentaire`](https://www.helloharel.com/blog/erp-agroalimentaire/) | 1625 | 0.0 | 0 | — | **Supprimer** | absent du sitemap + doublon de la landing mère → rediriger /agroalimentaire/ |
| 62 | [`erp-decoupe-viande-poisson`](https://www.helloharel.com/blog/erp-decoupe-viande-poisson/) | 1631 | 0.0 | 0 | §2 | **Fusionner** | → `gestion-decoupe-viande-logiciel` |
| 63 | [`calcul-freinte-charcuterie-logiciel`](https://www.helloharel.com/blog/calcul-freinte-charcuterie-logiciel/) | 1692 | 0.0 | 0 | §2 | **Garder** | silo charcutier |
| 64 | [`gestion-automatisee-des-variations-de-stock`](https://www.helloharel.com/blog/gestion-automatisee-des-variations-de-stock/) | 1692 | 0.0 | 0 | §3 | **Fusionner** | → `variation-de-stock-positif-negatif` |
| 65 | [`kpi-qualite-agroalimentaire`](https://www.helloharel.com/blog/kpi-qualite-agroalimentaire/) | 1738 | 0.0 | 0 | §1 | **Garder** |  |
| 66 | [`logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises`](https://www.helloharel.com/blog/logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises/) | 1773 | 0.0 | 0 | §6 | **Garder** | slug à raccourcir |
| 67 | [`migration-erp-agroalimentaire`](https://www.helloharel.com/blog/migration-erp-agroalimentaire/) | 1783 | 0.0 | 0 | §7 | **Garder** |  |
| 68 | [`meilleurs-erp-maraichers-fruits-legumes`](https://www.helloharel.com/blog/meilleurs-erp-maraichers-fruits-legumes/) | 1790 | 0.0 | 0 | §8 | **Garder** |  |
| 69 | [`facture-exacompta`](https://www.helloharel.com/blog/facture-exacompta/) | 1807 | 0.0 | 0 | — | **Supprimer** | Exacompta = papeterie, hors sujet ERP — à confirmer en GSC |
| 70 | [`tracabilite-viande-logiciel`](https://www.helloharel.com/blog/tracabilite-viande-logiciel/) | 1835 | 0.0 | 0 | §1 | **Fusionner** | → `tracabilite-de-la-viande` |
| 71 | [`edi-logiciel-agroalimentaire`](https://www.helloharel.com/blog/edi-logiciel-agroalimentaire/) | 1836 | 0.0 | 0 | §6 | **Garder** |  |
| 72 | [`roi-erp`](https://www.helloharel.com/blog/roi-erp/) | 1848 | 0.0 | 0 | §8 | **Garder** |  |
| 73 | [`gestion-decoupe-viande-logiciel`](https://www.helloharel.com/blog/gestion-decoupe-viande-logiciel/) | 1920 | 0.0 | 0 | §2 | **Garder** | cible de fusion découpe viande |
| 74 | [`logiciel-maree-mareyeur`](https://www.helloharel.com/blog/logiciel-maree-mareyeur/) | 1951 | 0.0 | 0 | §6 | **Garder** | silo poissonnier |
| 75 | [`alternative-sage-erp`](https://www.helloharel.com/blog/alternative-sage-erp/) | 2057 | 0.0 | 0 | §8 | **Fusionner** | → `alternatives-sage-agroalimentaire` |
| 76 | [`integrateur-erp-paris`](https://www.helloharel.com/blog/integrateur-erp-paris/) | 2082 | 0.0 | 0 | — | **Migrer** | local → basculer en page sous /implantations/ |
| 77 | [`alternative-akanea-erp`](https://www.helloharel.com/blog/alternative-akanea-erp/) | 2250 | 0.0 | 0 | §8 | **Garder** |  |
| 78 | [`optimisation-entrepot`](https://www.helloharel.com/blog/optimisation-entrepot/) | 2303 | 0.0 | 0 | §3 | **Garder** |  |
| 79 | [`hello-harel-vs-silog`](https://www.helloharel.com/blog/hello-harel-vs-silog/) | 2354 | 0.0 | 0 | §8 | **Garder** |  |
| 80 | [`meilleurs-erp-boulangerie`](https://www.helloharel.com/blog/meilleurs-erp-boulangerie/) | 2386 | 0.0 | 0 | §8 | **Garder** |  |
| 81 | [`alternatives-silog-agroalimentaire`](https://www.helloharel.com/blog/alternatives-silog-agroalimentaire/) | 2403 | 0.0 | 0 | §8 | **Garder** |  |
| 82 | [`alternative-cegid`](https://www.helloharel.com/blog/alternative-cegid/) | 2424 | 0.0 | 0 | §8 | **Fusionner** | → `alternatives-cegid-distribution-alimentaire` |
| 83 | [`hello-harel-vs-divalto`](https://www.helloharel.com/blog/hello-harel-vs-divalto/) | 2432 | 0.0 | 0 | §8 | **Garder** |  |
| 84 | [`hello-harel-vs-odoo`](https://www.helloharel.com/blog/hello-harel-vs-odoo/) | 2463 | 0.0 | 0 | §8 | **Garder** |  |
| 85 | [`hello-harel-vs-sage`](https://www.helloharel.com/blog/hello-harel-vs-sage/) | 2489 | 0.0 | 0 | §8 | **Garder** |  |
| 86 | [`alternatives-divalto-agroalimentaire`](https://www.helloharel.com/blog/alternatives-divalto-agroalimentaire/) | 2562 | 0.0 | 0 | §8 | **Garder** |  |
| 87 | [`alternatives-cegid-distribution-alimentaire`](https://www.helloharel.com/blog/alternatives-cegid-distribution-alimentaire/) | 2644 | 0.0 | 0 | §8 | **Garder** | cible de fusion Cegid |
| 88 | [`erp-cloud-saas-vs-on-premise`](https://www.helloharel.com/blog/erp-cloud-saas-vs-on-premise/) | 2681 | 0.0 | 0 | §7 | **Fusionner** | → `erp-saas` |
| 89 | [`alternatives-copilote-traiteur`](https://www.helloharel.com/blog/alternatives-copilote-traiteur/) | 2683 | 0.0 | 0 | §8 | **Garder** |  |
| 90 | [`alternatives-odoo-agroalimentaire`](https://www.helloharel.com/blog/alternatives-odoo-agroalimentaire/) | 2686 | 0.0 | 0 | §8 | **Garder** |  |
| 91 | [`alternatives-sage-agroalimentaire`](https://www.helloharel.com/blog/alternatives-sage-agroalimentaire/) | 2746 | 0.0 | 0 | §8 | **Garder** | cible de fusion Sage |
| 92 | [`erp-grossiste-distributeur`](https://www.helloharel.com/blog/erp-grossiste-distributeur/) | 2908 | 0.0 | 0 | §6 | **Garder** | ~200 vues/mois mesurées en août |
| 93 | [`cuisine-centrale`](https://www.helloharel.com/blog/cuisine-centrale/) | 3058 | 0.0 | 0 | §4 | **Garder** |  |
| 94 | [`remplacer-excel-gestion-agroalimentaire`](https://www.helloharel.com/blog/remplacer-excel-gestion-agroalimentaire/) | 3100 | 0.0 | 0 | §7 | **Garder** | pilier §7 |
| 95 | [`logiciel-grossiste-alimentaire`](https://www.helloharel.com/blog/logiciel-grossiste-alimentaire/) | 3312 | 0.0 | 0 | §6 | **Garder** |  |
| 96 | [`logiciel-televente-alimentaire`](https://www.helloharel.com/blog/logiciel-televente-alimentaire/) | 3547 | 0.0 | 0 | §6 | **Garder** |  |
| 97 | [`factur-x-e-facturation-logiciel`](https://www.helloharel.com/blog/factur-x-e-facturation-logiciel/) | 3912 | 0.0 | 0 | §5 | **Garder** | pilier §5 |
| 98 | [`erp-boissons`](https://www.helloharel.com/blog/erp-boissons/) | 4008 | 0.0 | 0 | §6 | **Garder** | silo brasseur |
| 99 | [`conformite-haccp`](https://www.helloharel.com/blog/conformite-haccp/) | 4064 | 0.0 | 0 | §1 | **Garder** | cible de fusion conformité |
| 100 | [`tracabilite-lot-dlc-logiciel`](https://www.helloharel.com/blog/tracabilite-lot-dlc-logiciel/) | 4085 | 0.0 | 0 | §1 | **Garder** | pilier §1 |
| 101 | [`gestion-stock-multi-entrepots`](https://www.helloharel.com/blog/gestion-stock-multi-entrepots/) | 4140 | 0.0 | 0 | §3 | **Garder** |  |
| 102 | [`calcul-cout-de-revient-logiciel`](https://www.helloharel.com/blog/calcul-cout-de-revient-logiciel/) | 4538 | 0.0 | 0 | §2 | **Fusionner** | → `cout-de-revient` |
| 103 | [`cout-de-revient`](https://www.helloharel.com/blog/cout-de-revient/) | 6330 | 0.0 | 0 | §2 | **Garder** | cible de fusion coût de revient — 6 330 mots pour 0 visibilité |