# Audit Maillage Interne - helloharel.com
**Date : 31 mars 2026**
**Perimetre : 100% des pages et articles du site**

---

## 1. INVENTAIRE DU SITE

| Type | Nombre | Source |
|------|--------|--------|
| Pages principales | 16 | page-sitemap.xml |
| Pages hors sitemap (nav/footer) | ~25 | crawl homepage |
| Articles de blog | 71 | post-sitemap.xml |
| Categories | 1 | category-sitemap.xml |
| **TOTAL URLs indexables** | **~113** | |

---

## 2. LIENS 404 CONFIRMES

### 2.1 Dans la navigation principale (CRITIQUE)

| URL cassee | Ancre | Trouve sur |
|------------|-------|------------|
| `/?page_id=5455` | "ERP Boissons" | Menu header (toutes pages) |
| `/logiciel-maree-mareyeur/` | (dynamique) | Homepage body |
| `/negoce/boissons/` | (dynamique) | Homepage footer/nav |

### 2.2 Dans le corps des articles de blog

| URL 404 | Ancre utilisee | Article source |
|---------|----------------|----------------|
| `/business-plan-calculer-la-marge-commerciale-et-le-taux-de-marge/` | "Business plan : calculer la marge commerciale et le taux de marge" | maitriser-la-gestion-des-stocks |
| `/comprendre-la-tracabilite-en-agroalimentaire-methodes-et-avantages/` | "Comprendre la tracabilite en agroalimentaire" | tracabilite-de-la-viande |
| `/demo/` | "VOIR LA DEMO..." | alternative-cegid, logiciel-maree-mareyeur, erp-cloud-saas-vs-on-premise, logiciel-grossiste-boissons |
| `/erp-agro-alimentaire/logiciel-gestion-des-stocks-agro-alimentaire/` | "ce lien sur les logiciels de gestion des stocks agroalimentaires" | numeros-de-lot |
| `/erp-agroalimentaire/` | "ERP specialise" | erp-conformite-agroalimentaire, erp-decoupe-viande-poisson |
| `/erp-production-optimisez-vos-processus-de-fabrication/` | "ERP de production" / "Optimisation des processus de fabrication" | bon-de-commande |
| `/formation/` | "Hello Harel" | meilleurs-erp-boulangerie |
| `/gestion-de-comptabilite/` | "solution de gestion de comptabilite" | calcul-stock-de-securite, facture-exacompta |
| `/gestion-de-relation-client/` | "systeme de gestion de la relation client (CRM)" | bon-de-commande |
| `/gestion-de-stock/` | "Hello Harel" / "gestion de stock" | calcul-stock-de-securite, calcul-variations-de-stock, optimisation-entrepot |
| `/gestion-stocks/` | "seuils de reapprovisionnement" | meilleurs-erp-boulangerie |
| `/les-meilleurs-erp-de-gestion-de-stock-agroalimentaire-en-2024/` | "meilleurs ERP de gestion de stock agroalimentaire" | numeros-de-lot, optimisation-entrepot |
| `/logiciel-gestion-des-stocks-agro-alimentaire/` | "logiciel de gestion des stocks" | contraintes-reglementations |
| `/logiciel-inventaire-guide-complet-pour-choisir-le-meilleur-en-2024/` | "logiciel inventaire" | calcul-stock-de-securite, optimisation-entrepot |
| `/roi-calculator/` | "simulateur ROI" | meilleurs-erp-boulangerie |
| `/solutions/` | "Solutions Agroalimentaires" / "Retour aux Solutions ERP" | erp-viande-volaille, alternative-cegid, logiciel-grossiste-boissons |
| `/blog/gestion-stock-reelle` | "gestion de stock reelle" | erp-viande-volaille |
| `/blog/maitriser-numeros-lot-tracabilite` | "Maitriser la tracabilite" | erp-viande-volaille |
| `/blog/calcul-prix-revient-pertes` | "Comprendre le calcul du prix de revient" | erp-viande-volaille |

**Total : 19 URLs en 404 dans le corps des articles**

### 2.3 Redirections problematiques (pointent vers la homepage au lieu d'une page pertinente)

| URL d'origine | Redirige vers | Ancre | Probleme |
|---------------|---------------|-------|----------|
| `/erp-cloud-vs-premise/` | `/` (homepage) | "ERP Cloud vs Premise" | Perte de pertinence |
| `/erp-pme/` | `/` (homepage) | "ERP PME" | Perte de pertinence |
| `/erp-saas/` | `/` (homepage) | "ERP SaaS" | Perte de pertinence |
| `/controle-qualite-agroalimentaire-le-guide-complet-pour-les-professionnels/` | `/` (homepage) | "Controle qualite" | Perte de pertinence |
| `/guide-complet-sur-les-erp-system-saas-lequel-choisir/` | `/` (homepage) | "ERP SaaS" | Perte de pertinence |
| `/quel-erp-choisir-pour-une-pme-industrielle/` | `/` (homepage) | "production industrielle" | Perte de pertinence |
| `/erp-qualite-agroalimentaire/` | `/agroalimentaire/` | "ERP qualite agroalimentaire" | Redirect generique |
| `/erp-agro-alimentaire/production/` | `/agroalimentaire/` | "production agroalimentaire" | Redirect generique |
| `/erp-agro-alimentaire/tracabilite/` | `/agroalimentaire/` | "ERP tracabilite" | Redirect generique |

---

## 3. ANOMALIES STRUCTURELLES

### 3.1 Domaine helloharel.fr dans le Schema.org
- Sur TOUTES les pages, le schema.org JSON-LD reference `https://helloharel.fr` comme "creator"
- Le site est sur `https://www.helloharel.com`
- `helloharel.fr` est inaccessible (erreur SSL)
- **Impact SEO** : confusion pour les moteurs de recherche

### 3.2 Typos dans les URLs du sitemap
| URL avec typo | Correction |
|---------------|------------|
| `/blog/integateur-erp-paris/` | `/blog/integrateur-erp-paris/` |
| `/blog/integateur-erp-lyon/` | `/blog/integrateur-erp-lyon/` |

### 3.3 LinkedIn admin URL dans le footer
- Lien actuel : `https://www.linkedin.com/company/26042947/admin/dashboard/`
- Devrait etre : `https://www.linkedin.com/company/26042947/`

### 3.4 Cookie Policy placeholder
- Lien `href="#"` sur toutes les pages — ne pointe vers rien

### 3.5 Categorie par defaut indexee
- `/blog/category/non-classe-fr-fr/` — slug WordPress par defaut, a noindexer ou supprimer

### 3.6 Pages absentes du sitemap XML
- `/blog/` — existe mais pas dans le sitemap
- `/fonctionnalites/` — pas de page index (404 si un visiteur tente d'y acceder)
- `/fonctionnalites/import-export/` — absente du page-sitemap.xml
- **Toutes les pages `/medical/*`** (6 pages) — absentes du sitemap
- **Toutes les pages `/negoce/*`** (6 pages + 1 en 404) — absentes du sitemap
- `/qui-sommes-nous/` — absente du sitemap
- `/integrateurs/` — absente du sitemap
- `/erp-ia/` — absente du sitemap
- `/intelligence-artificielle/` — absente du sitemap
- `/cgu/`, `/mentions-legales/`, `/politique-de-confidentialite/` — absentes du sitemap

**Au total, ~25 pages existent sur le site mais ne sont pas dans le sitemap XML.** Seules 16 pages sont declarees dans `page-sitemap.xml`.

### 3.7 Footer cache en CSS
- `display: none !important` sur `.elementor-location-footer`
- Les liens du footer existent dans le DOM mais sont invisibles si le JS echoue

### 3.8 Navigation 100% JS
- Tout le menu est injecte via JavaScript
- Si un crawler n'execute pas le JS, il ne voit que le lien `/contact/`
- Risque pour l'indexation

---

## 4. ANALYSE DU MAILLAGE INTERNE DES ARTICLES

### 4.1 Articles SANS aucun lien interne dans le body (pages orphelines)

| Article | Probleme |
|---------|----------|
| relance-client | 0 lien body |
| gestion-des-inventaires | 0 lien body |
| alerte-stock-securite | 0 lien body |
| agreage-agroalimentaire | 0 lien body |
| min | 0 lien body |
| partenariat-toncarton | 0 lien body |
| conformite-haccp | 0 lien body |
| cuisine-centrale | 0 lien body |
| integateur-erp-paris | 0 lien body |
| integateur-erp-lyon | 0 lien body |
| alternative-archipelia | 0 lien body |
| meilleurs-erp-import-export | 0 lien body |
| alternative-akanea-erp | 0 lien body |
| alternative-sage-erp | 0 lien body |

**14 articles sur 71 (20%) n'ont AUCUN lien interne dans leur contenu.**

### 4.2 Articles avec des liens internes mais pointant vers des anciennes URLs

La majorite des articles utilisent des URLs de l'ancien site (avant refonte) qui sont soit en 404, soit redirigees vers la homepage. Cela dilue le jus SEO.

### 4.3 Ancres sur-utilisees (manque de diversification)

| Ancre repetee | Nb occurrences | Pages ciblees |
|---------------|----------------|---------------|
| "Demander une demo" | ~300+ (toutes pages x3) | /contact/ |
| "En savoir plus" | 5 | Diverses pages fonctionnalites |
| "ERP SaaS Hello Harel" | 8+ | /erp-saas/ (redirige vers /) |
| "ERP PME Hello Harel" | 6+ | /erp-pme/ (redirige vers /) |
| "ERP Inventaire Hello Harel" | 5+ | /erp-inventaire/ (redirige vers gestion-de-stock) |
| "ROI ERP Hello Harel" | 7+ | /roi-erp/ |
| "ERP Qualite agroalimentaire Hello Harel" | 6+ | /erp-qualite-agroalimentaire/ (redirige vers /agroalimentaire/) |
| "/blog/" via breadcrumb "Blog" | 142 (2x par article) | /blog/ |

### 4.4 Section "Articles similaires" : ABSENTE
- Aucun article n'a de section "Articles similaires" ou "A lire aussi"
- Aucun breadcrumb visible
- Aucune sidebar de navigation entre articles

---

## 5. RECOMMANDATIONS D'AMELIORATION DES ANCRES

### 5.1 Remplacer les ancres generiques "En savoir plus" par des mots-cles secondaires

| Page ciblee | Ancre actuelle | Ancre recommandee |
|-------------|---------------|-------------------|
| /fonctionnalites/vente/ | "En savoir plus" | "decouvrir notre module de gestion commerciale" |
| /fonctionnalites/facturation/ | "En savoir plus" | "automatiser votre facturation" |
| /fonctionnalites/gestion-de-stock/ | "En savoir plus" | "optimiser la gestion de vos stocks" |
| /fonctionnalites/fabrication/ | "En savoir plus" | "piloter vos ordres de fabrication" |
| /fonctionnalites/logistique/ | "En savoir plus" | "gerer votre logistique et vos expeditions" |
| /qui-sommes-nous/ | "En savoir plus" | "decouvrir l'equipe Hello Harel" |

### 5.2 Diversifier les ancres du blog vers les pages piliers

Au lieu de toujours utiliser "ERP SaaS Hello Harel" ou "ERP PME Hello Harel", varier avec :

| Page ciblee | Ancres actuelles | Ancres secondaires recommandees |
|-------------|-----------------|-------------------------------|
| /agroalimentaire/ | "ERP Agroalimentaire", "logiciel agroalimentaire" | "solution de gestion pour l'agroalimentaire", "ERP metier agro", "logiciel de tracabilite alimentaire" |
| /fonctionnalites/gestion-de-stock/ | "gestion de stock", "Logiciel de Gestion de stock" | "gestion multi-entrepots", "suivi de stock en temps reel", "optimisation des inventaires" |
| /fonctionnalites/fabrication/ | "Logiciel de Fabrication" | "gestion de la production agroalimentaire", "module fabrication ERP", "ordres de fabrication en ligne" |
| /agroalimentaire/traiteur/ | "ERP Traiteur" | "logiciel de gestion traiteur", "solution traiteur en ligne", "gestion de commandes traiteur" |
| /agroalimentaire/boulanger/ | "ERP Boulangerie" | "logiciel boulangerie-patisserie", "gestion boulangerie en ligne", "ERP artisan boulanger" |
| /fonctionnalites/crm/ | "Logiciel CRM" | "gestion de la relation client", "suivi client et prospection", "CRM pour PME agroalimentaire" |
| /blog/fifo-fefo-lifo/ | "FIFO, FEFO, LIFO" | "strategies de prelevement en entrepot", "methodes de rotation des stocks", "gestion FEFO agroalimentaire" |
| /blog/roi-erp/ | "ROI ERP" | "calculer le retour sur investissement d'un ERP", "rentabilite d'un projet ERP" |
| /contact/ | "Demander une demo" (x300) | "essayer gratuitement", "planifier une demonstration", "decouvrir Hello Harel en action", "obtenir un devis personnalise" |

### 5.3 Liens internes recommandes entre articles (clusters thematiques)

#### Cluster COUTS & PRIX
| Depuis | Vers | Ancre suggeree |
|--------|------|---------------|
| cout-de-revient | calcul-du-cout-achat | "calculer le cout d'achat de vos matieres premieres" |
| cout-de-revient | calculer-le-prix-de-revient-en-boulangerie | "exemple concret en boulangerie" |
| cout-marginal | couts-de-production | "comprendre les couts de production" |
| prix-dachat-definition | difference-prix-dachat-et-prix-de-revient | "difference avec le prix de revient" |
| calcul-du-prix-moyen | calcul-stock-moyen | "calculer votre stock moyen" |

#### Cluster STOCK & INVENTAIRE
| Depuis | Vers | Ancre suggeree |
|--------|------|---------------|
| maitriser-la-gestion-des-stocks | calcul-stock-de-securite | "definir votre stock de securite" |
| maitriser-la-gestion-des-stocks | reapprovisionnement-stocks | "automatiser le reapprovisionnement" |
| calcul-stock-de-securite | alerte-stock-securite | "configurer des alertes de stock" |
| gestion-des-inventaires | fifo-fefo-lifo | "choisir la bonne methode de prelevement" |
| optimisation-entrepot | gestion-des-inventaires | "optimiser vos inventaires" |
| alerte-stock-securite | alerte-date-peremption | "gerer aussi les alertes de peremption" |

#### Cluster TRACABILITE & QUALITE
| Depuis | Vers | Ancre suggeree |
|--------|------|---------------|
| numeros-de-lot | tracabilite-de-la-viande | "tracabilite specifique viande bovine" |
| tracabilite-de-la-viande | erp-tracabilite-agroalimentaire | "solution complete de tracabilite ERP" |
| conformite-haccp | plan-de-controle-alimentaire | "mettre en place un plan de controle" |
| conformite-haccp | kpi-qualite-agroalimentaire | "suivre les KPI qualite" |
| dlc-ddm-dluo | alerte-date-peremption | "automatiser les alertes de peremption" |
| agreage-agroalimentaire | processus-agroalimentaire-guide | "comprendre les processus agroalimentaires" |

#### Cluster ERP & TECHNOLOGIE
| Depuis | Vers | Ancre suggeree |
|--------|------|---------------|
| erp-saas-cloud | erp-as400 | "migrer depuis un AS400" |
| erp-pme | roi-erp | "calculer le ROI de votre ERP" |
| migration-erp-agroalimentaire | erp-saas-cloud | "avantages du cloud pour l'agroalimentaire" |
| opc-ua | ordonnancement-planification | "planifier et ordonnancer la production" |

#### Cluster METIER TRAITEUR
| Depuis | Vers | Ancre suggeree |
|--------|------|---------------|
| facture-traiteur | bon-de-commande-traiteur | "gerer vos bons de commande traiteur" |
| bon-de-commande-traiteur | facture-traiteur | "generer une facture traiteur" |

#### Cluster ALTERNATIVES ERP
| Depuis | Vers | Ancre suggeree |
|--------|------|---------------|
| alternative-vif-erp | alternative-sage-erp | "comparer aussi avec Sage" |
| alternative-sage-erp | alternative-cegid | "alternative a Cegid" |
| alternative-cegid | alternative-akanea-erp | "alternative a Akanea" |
| alternative-akanea-erp | alternative-archipelia | "alternative a Archipelia" |

### 5.4 Articles orphelins a relier en priorite (0 lien interne)

| Article orphelin | Liens a ajouter vers | Ancre suggeree |
|-----------------|---------------------|---------------|
| relance-client | /fonctionnalites/crm/ | "automatiser vos relances avec un CRM" |
| relance-client | /fonctionnalites/facturation/ | "gerer vos factures et echeances" |
| gestion-des-inventaires | fifo-fefo-lifo | "methodes de prelevement FIFO/FEFO" |
| gestion-des-inventaires | calcul-stock-de-securite | "definir votre stock de securite" |
| alerte-stock-securite | calcul-stock-de-securite | "calculer votre stock de securite optimal" |
| alerte-stock-securite | reapprovisionnement-stocks | "automatiser le reapprovisionnement" |
| conformite-haccp | plan-de-controle-alimentaire | "mettre en place un plan de controle HACCP" |
| conformite-haccp | kpi-qualite-agroalimentaire | "mesurer la qualite avec des KPI" |
| cuisine-centrale | conformite-haccp | "assurer la conformite HACCP" |
| cuisine-centrale | processus-agroalimentaire-guide | "maitriser les processus agroalimentaires" |
| min | erp-grossiste-distributeur | "ERP pour grossistes et distributeurs" |
| agreage-agroalimentaire | erp-tracabilite-agroalimentaire | "tracabilite complete avec un ERP" |
| integateur-erp-paris | migration-erp-agroalimentaire | "reussir votre migration ERP" |
| integateur-erp-lyon | migration-erp-agroalimentaire | "reussir votre migration ERP" |
| alternative-archipelia | alternative-vif-erp | "comparer avec Vif ERP" |
| meilleurs-erp-import-export | /fonctionnalites/import-export/ | "module import-export Hello Harel" |
| alternative-akanea-erp | meilleurs-erp-maraichers-fruits-legumes | "ERP pour maraichers" |
| alternative-sage-erp | erp-pme (via blog) | "choisir un ERP PME adapte" |

---

## 6. PLAN D'ACTION PRIORITAIRE

### URGENT (Impact SEO immediat)
1. **Corriger les 3 liens 404 dans la navigation** (ERP Boissons, logiciel-maree-mareyeur, negoce/boissons)
2. **Corriger les 19 liens 404 dans les articles** (voir tableau 2.2)
3. **Corriger les 3 liens 404 dans les liens blog-to-blog** (erp-viande-volaille)
4. **Remplacer `helloharel.fr` par `www.helloharel.com` dans le Schema.org**
5. **Corriger le lien LinkedIn** (retirer `/admin/dashboard/`)

### IMPORTANT (Amelioration du maillage)
6. **Ajouter des liens internes dans les 14 articles orphelins** (section 5.4)
7. **Mettre a jour les 9 redirections vers la homepage** pour pointer vers des pages pertinentes (section 2.3)
8. **Remplacer les ancres "En savoir plus"** par des ancres descriptives (section 5.1)
9. **Ajouter une section "Articles similaires"** en bas de chaque article de blog
10. **Ajouter des breadcrumbs** sur toutes les pages

### RECOMMANDE (Optimisation)
11. **Diversifier les ancres** selon les suggestions de la section 5.2
12. **Implementer les liens inter-clusters** (section 5.3)
13. **Creer une page `/fonctionnalites/`** comme hub des modules
14. **Noindexer** `/blog/category/non-classe-fr-fr/`
15. **Corriger les typos** dans les slugs "integateur" -> "integrateur"
16. **Ajouter un fallback HTML** pour la navigation (ne pas dependre a 100% du JS)
17. **Ajouter `/blog/` dans le sitemap** page-sitemap.xml
18. **Corriger le lien Cookie Policy** `href="#"` vers une vraie page
