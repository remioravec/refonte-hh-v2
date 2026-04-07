# Corrections 404 - Guide d'implementation

## 1. NAVIGATION PRINCIPALE (3 corrections)

### 1.1 ERP Boissons - lien mort `/?page_id=5455`
- **Ou** : Menu header, dropdown "Metiers"
- **Action** : Creer la page `/negoce/boissons/` OU remplacer le lien par `/negoce/` en attendant
- **Ancre actuelle** : "ERP Boissons"

### 1.2 Logiciel maree mareyeur - lien mort `/logiciel-maree-mareyeur/`
- **Ou** : Homepage, element dynamique
- **Action** : Creer la page OU retirer le lien
- **Note** : L'article `/blog/logiciel-maree-mareyeur/` existe, le lien devrait pointer vers `/blog/logiciel-maree-mareyeur/`

### 1.3 Negoce boissons - lien mort `/negoce/boissons/`
- **Ou** : Homepage nav/footer
- **Action** : Creer la page OU rediriger vers `/negoce/`

---

## 2. LIENS DANS LES ARTICLES DE BLOG (19 corrections)

### Format : Article > Ancienne URL > Nouvelle URL recommandee

#### Article : `maitriser-la-gestion-des-stocks`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/business-plan-calculer-la-marge-commerciale-et-le-taux-de-marge/` | `/blog/calcul-du-prix-moyen/` | "calculer la marge commerciale et le taux de marge" |

#### Article : `tracabilite-de-la-viande`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/comprendre-la-tracabilite-en-agroalimentaire-methodes-et-avantages/` | `/blog/erp-tracabilite-agroalimentaire/` | "Comprendre la tracabilite en agroalimentaire" |

#### Articles : `alternative-cegid`, `logiciel-maree-mareyeur`, `erp-cloud-saas-vs-on-premise`, `logiciel-grossiste-boissons`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/demo/` | `/contact/` | Garder l'ancre actuelle (ex: "VOIR LA DEMO") |

#### Article : `numeros-de-lot`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/erp-agro-alimentaire/logiciel-gestion-des-stocks-agro-alimentaire/` | `/fonctionnalites/gestion-de-stock/` | "logiciels de gestion des stocks agroalimentaires" |

#### Articles : `erp-conformite-agroalimentaire`, `erp-decoupe-viande-poisson`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/erp-agroalimentaire/` | `/agroalimentaire/` | "ERP specialise" |

#### Article : `bon-de-commande`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/erp-production-optimisez-vos-processus-de-fabrication/` | `/fonctionnalites/fabrication/` | "ERP de production" / "Optimisation des processus de fabrication" |

#### Article : `meilleurs-erp-boulangerie`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/formation/` | `/contact/` | "Hello Harel" |
| `/gestion-stocks/` | `/fonctionnalites/gestion-de-stock/` | "seuils de reapprovisionnement" |
| `/roi-calculator/` | `/blog/roi-erp/` | "simulateur ROI" |

#### Articles : `calcul-stock-de-securite`, `facture-exacompta`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/gestion-de-comptabilite/` | `/fonctionnalites/facturation/` | "solution de gestion de comptabilite" |

#### Article : `bon-de-commande`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/gestion-de-relation-client/` | `/fonctionnalites/crm/` | "systeme de gestion de la relation client (CRM)" |

#### Articles : `calcul-stock-de-securite`, `calcul-variations-de-stock`, `optimisation-entrepot`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/gestion-de-stock/` | `/fonctionnalites/gestion-de-stock/` | "gestion de stock" / "Hello Harel" |

#### Articles : `numeros-de-lot`, `optimisation-entrepot`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/les-meilleurs-erp-de-gestion-de-stock-agroalimentaire-en-2024/` | `/fonctionnalites/gestion-de-stock/` | "meilleurs ERP de gestion de stock agroalimentaire" |

#### Article : `contraintes-reglementations-logiciel-agroalimentaire`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/logiciel-gestion-des-stocks-agro-alimentaire/` | `/fonctionnalites/gestion-de-stock/` | "logiciel de gestion des stocks" |

#### Articles : `calcul-stock-de-securite`, `optimisation-entrepot`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/logiciel-inventaire-guide-complet-pour-choisir-le-meilleur-en-2024/` | `/blog/gestion-des-inventaires/` | "logiciel inventaire" |

#### Articles : `erp-viande-volaille`, `alternative-cegid`, `logiciel-grossiste-boissons`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/solutions/` | `/agroalimentaire/` | "Solutions Agroalimentaires" / "Retour aux Solutions ERP" |

#### Article : `erp-viande-volaille`
| Ancienne URL | Nouvelle URL | Ancre |
|-------------|-------------|-------|
| `/blog/gestion-stock-reelle` | `/blog/maitriser-la-gestion-des-stocks/` | "gestion de stock reelle" |
| `/blog/maitriser-numeros-lot-tracabilite` | `/blog/numeros-de-lot/` | "Maitriser la tracabilite" |
| `/blog/calcul-prix-revient-pertes` | `/blog/cout-de-revient/` | "Comprendre le calcul du prix de revient" |

---

## 3. REDIRECTIONS A METTRE A JOUR (9 corrections)

Ces anciennes URLs redirigent vers la homepage `/` au lieu d'une page pertinente. Mettre a jour les redirections dans WordPress (ou .htaccess / plugin Redirection) :

| Ancienne URL | Redirige vers (actuel) | Devrait rediriger vers |
|-------------|----------------------|----------------------|
| `/erp-cloud-vs-premise/` | `/` | `/blog/erp-cloud-saas-vs-on-premise/` |
| `/erp-pme/` | `/` | `/blog/erp-pme/` |
| `/erp-saas/` | `/` | `/blog/erp-saas/` ou `/blog/erp-saas-cloud/` |
| `/controle-qualite-agroalimentaire-le-guide-complet-pour-les-professionnels/` | `/` | `/blog/conformite-haccp/` |
| `/guide-complet-sur-les-erp-system-saas-lequel-choisir/` | `/` | `/blog/erp-saas-cloud/` |
| `/quel-erp-choisir-pour-une-pme-industrielle/` | `/` | `/blog/erp-pme/` |
| `/erp-qualite-agroalimentaire/` | `/agroalimentaire/` | `/blog/kpi-qualite-agroalimentaire/` |
| `/erp-agro-alimentaire/production/` | `/agroalimentaire/` | `/fonctionnalites/fabrication/` |
| `/erp-agro-alimentaire/tracabilite/` | `/agroalimentaire/` | `/blog/erp-tracabilite-agroalimentaire/` |
