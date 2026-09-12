# Maillage interne — Plan DRY-RUN

Généré par `maillage.py` à partir de `inventory.json` (données live).
Aucune écriture n'a été faite sur WordPress. Étape d'application séparée et validée.

## Synthèse

- Articles concernés : **81**
- Liens contextuels NOUVEAUX proposés : **254**
- Cannibalisation d'ancres dans le plan : **1** (objectif : 0)

## Pages money — liens contextuels entrants projetés (ajouts)

| Page money | ctx entrants actuels | ancres distinctes actuelles | + liens (plan) | + ancres distinctes |
|---|---|---|---|---|
| /agroalimentaire/ | 72 | 53 | +10 | +10 |
| /fonctionnalites/gestion-de-stock/ | 58 | 27 | +7 | +7 |
| /fonctionnalites/fabrication/ | 36 | 18 | +6 | +6 |
| /fonctionnalites/planification-production-erp/ | 0 | 0 | +3 | +3 |
| /fonctionnalites/crm/ | 3 | 3 | +0 | +0 |
| /fonctionnalites/facturation/ | 18 | 11 | +4 | +4 |
| /fonctionnalites/logistique/ | 21 | 9 | +0 | +0 |
| /fonctionnalites/import-export/ | 3 | 3 | +1 | +1 |
| /fonctionnalites/vente/ | 29 | 19 | +4 | +4 |
| /fonctionnalites/achat/ | 5 | 4 | +3 | +3 |
| /agroalimentaire/traiteur/ | 13 | 8 | +3 | +3 |
| /agroalimentaire/boulanger/ | 0 | 0 | +2 | +2 |
| /agroalimentaire/charcutier/ | 14 | 9 | +3 | +3 |
| /agroalimentaire/maraicher/ | 5 | 4 | +4 | +4 |
| /agroalimentaire/industrie-laitiere/ | 2 | 2 | +0 | +0 |
| /agroalimentaire/plats-cuisines-industriels/ | 2 | 1 | +3 | +3 |
| /negoce/ | 3 | 1 | +4 | +4 |
| /comparatifs/ | 0 | 0 | +4 | +4 |
| /tarifs/ | 22 | 9 | +0 | +0 |
| /contact/ | 13 | 6 | +0 | +0 |

## ⚠️ Ancres cannibales détectées

- `meilleur erp agroalimentaire` → /blog/erp-agroalimentaire/, /comparatifs/

## Détail par article

### /blog/agreage-agroalimentaire/
_Agréage Agroalimentaire • Contrôle & Qualité • Guide_ — cluster **tracabilite** · 903 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Réglementation Agro | /blog/contraintes-reglementations-logiciel-agroalimentaire/ |
| body | lateral | Processus Agroalimentaire | /blog/processus-agroalimentaire-guide/ |
| body | lateral | Conditionnement Alimentaire | /blog/conditionnement-alimentaire-erp/ |

### /blog/alerte-date-peremption/
_Alerte Péremption • Automatisez Vos DLC • Zéro Perte_ — cluster **tracabilite** · 815 mots · 1 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Agréage Agroalimentaire | /blog/agreage-agroalimentaire/ |
| body | lateral | Réglementation Agro | /blog/contraintes-reglementations-logiciel-agroalimentaire/ |
| body | lateral | Processus Agroalimentaire | /blog/processus-agroalimentaire-guide/ |

### /blog/alerte-stock-securite/
_Alerte Stock • Seuils & Réappro Auto • Guide ERP_ — cluster **stock** · 870 mots · 1 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Optimisation Entrepôt | /blog/optimisation-entrepot/ |
| body | lateral | Maîtriser Ses Stocks | /blog/maitriser-la-gestion-des-stocks/ |
| body | lateral | FIFO, FEFO & LIFO | /blog/fifo-fefo-lifo/ |

### /blog/alternative-akanea-erp/
_Alternative Akanea • ERP Agro Plus Agile • Depuis 2014_ — cluster **comparatifs** · 1653 mots · 0 liens ctx existants · budget 9

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Alternative Archipelia | /blog/alternative-archipelia/ |
| body | lateral | Alternative Cegid | /blog/alternative-cegid/ |
| body | lateral | Alternative Sage | /blog/alternative-sage-erp/ |

### /blog/alternative-archipelia/
_Alternative Archipelia • 100% Négoce Agro • Expert_ — cluster **comparatifs** · 1202 mots · 0 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Alternative Cegid | /blog/alternative-cegid/ |
| body | lateral | Alternative Sage | /blog/alternative-sage-erp/ |
| body | lateral | Alternative VIF ERP | /blog/alternative-vif-erp/ |

### /blog/alternative-cegid/
_Alternative Cegid • ERP Agro Agile & Accessible • PME_ — cluster **comparatifs** · 1720 mots · 0 liens ctx existants · budget 9

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | solution de gestion pour l'agroalimentaire | /agroalimentaire/ |
| body | lateral | Alternative Sage | /blog/alternative-sage-erp/ |
| body | lateral | Alternative VIF ERP | /blog/alternative-vif-erp/ |
| body | lateral | Alternatives à Cegid pour la Distribution Alimentaire | /blog/alternatives-cegid-distribution-alimentaire/ |

### /blog/alternative-sage-erp/
_Alternative Sage • Spécialiste Négoce Agro • +200_ — cluster **comparatifs** · 1308 mots · 0 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | logiciel de production agroalimentaire | /agroalimentaire/ |
| body | lateral | Alternative VIF ERP | /blog/alternative-vif-erp/ |
| body | lateral | Alternatives à Cegid pour la Distribution Alimentaire | /blog/alternatives-cegid-distribution-alimentaire/ |
| body | lateral | Alternatives à Divalto pour les PME Agro | /blog/alternatives-divalto-agroalimentaire/ |

### /blog/alternative-vif-erp/
_Alternative VIF ERP • Négoce Plutôt Qu’Industrie • SaaS_ — cluster **comparatifs** · 1318 mots · 0 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Alternatives à Cegid pour la Distribution Alimentaire | /blog/alternatives-cegid-distribution-alimentaire/ |
| body | lateral | Alternatives à Divalto pour les PME Agro | /blog/alternatives-divalto-agroalimentaire/ |
| body | lateral | Alternatives à Odoo pour l’Agroalimentaire | /blog/alternatives-odoo-agroalimentaire/ |

### /blog/alternatives-divalto-agroalimentaire/
_Alternatives à Divalto pour les PME Agro • ERP Plus Agile_ — cluster **comparatifs** · 3002 mots · 9 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | comparatif des ERP agroalimentaires | /comparatifs/ |
| body | lateral | Alternatives à Odoo pour l’Agroalimentaire | /blog/alternatives-odoo-agroalimentaire/ |

### /blog/alternatives-sage-agroalimentaire/
_Alternatives à Sage pour l’Agroalimentaire • ERP Agro Spécialisé_ — cluster **comparatifs** · 3116 mots · 10 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | comparer les ERP du marché | /comparatifs/ |

### /blog/bon-de-commande-traiteur/
_Bon de Commande Traiteur • Modèle & Astuces • Guide_ — cluster **facturation** · 999 mots · 3 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | module de facturation | /fonctionnalites/facturation/ |
| top | up | module de vente et devis | /fonctionnalites/vente/ |

### /blog/bon-de-commande/
_Bon de Commande • Modèle & Gestion ERP • Guide 2026_ — cluster **facturation** · 2156 mots · 6 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Bon de Livraison | /blog/bon-de-livraison/ |
| body | lateral | Bon de Commande Traiteur | /blog/bon-de-commande-traiteur/ |
| body | lateral | Relance Client | /blog/relance-client/ |

### /blog/bon-de-livraison/
_Bon de Livraison • Modèle & Automatisation • Guide_ — cluster **facturation** · 1057 mots · 1 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | facturation électronique | /fonctionnalites/facturation/ |
| top | up | accélérer vos ventes et devis | /fonctionnalites/vente/ |
| body | lateral | Bon de Commande Traiteur | /blog/bon-de-commande-traiteur/ |
| body | lateral | Relance Client | /blog/relance-client/ |

### /blog/calcul-cout-de-revient-logiciel/
_Coût de Revient Agro • Calcul & Logiciel ERP • Guide PME 2026_ — cluster **couts** · 5220 mots · 10 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Prix Revient Boulangerie | /blog/calculer-le-prix-de-revient-en-boulangerie/ |

### /blog/calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025/
_Variation Stock CUMP • Méthode & Exemples • Guide_ — cluster **stock** · 1171 mots · 0 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion de stock agroalimentaire | /fonctionnalites/gestion-de-stock/ |
| body | lateral | Stock de Sécurité | /blog/calcul-stock-de-securite/ |
| body | lateral | Calcul Stock Moyen | /blog/calcul-stock-moyen/ |
| body | lateral | Variation de Stock | /blog/calcul-variations-de-stock/ |

### /blog/calcul-freinte-charcuterie-logiciel/
_Calcul freinte charcuterie : pilotage perte de séchage salaison au logiciel ERP_ — cluster **fabrication** · 1878 mots · 4 liens ctx existants · budget 10

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | ERP de production agroalimentaire | /fonctionnalites/fabrication/ |
| top | up | ordonnancement de la production | /fonctionnalites/planification-production-erp/ |
| body | lateral | Ordre de Fabrication | /blog/ordre-de-fabrication/ |
| body | lateral | Ordonnancement | /blog/ordonnancement-planification/ |
| body | lateral | OPC UA | /blog/opc-ua/ |

### /blog/calcul-stock-de-securite/
_Stock de Sécurité • Calcul & Formules • Guide Pratique_ — cluster **stock** · 1246 mots · 5 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Calcul Stock Moyen | /blog/calcul-stock-moyen/ |

### /blog/calcul-stock-moyen/
_Calcul Stock Moyen • Méthode & Exemples • Outil Gratuit_ — cluster **stock** · 1225 mots · 2 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Variation de Stock | /blog/calcul-variations-de-stock/ |
| body | lateral | Gestion des Inventaires | /blog/gestion-des-inventaires/ |
| body | lateral | Gestion Stock Multi-Entrepôts | /blog/gestion-stock-multi-entrepots/ |

### /blog/calcul-variations-de-stock/
_Variation de Stock • Calcul & Formules • Guide 2026_ — cluster **stock** · 1036 mots · 1 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Gestion des Inventaires | /blog/gestion-des-inventaires/ |
| body | lateral | Gestion Stock Multi-Entrepôts | /blog/gestion-stock-multi-entrepots/ |
| body | lateral | Réapprovisionnement | /blog/reapprovisionnement-stocks/ |

### /blog/calculer-le-prix-de-revient-en-boulangerie/
_Prix Revient Boulangerie • Calcul & Exercices • Guide_ — cluster **boulanger** · 1152 mots · 4 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion boulangerie | /agroalimentaire/boulanger/ |
| body | lateral | Meilleurs ERP Boulangerie | /blog/meilleurs-erp-boulangerie/ |

### /blog/conformite-haccp/
_Conformité HACCP • Logiciel & Automatisation • Guide_ — cluster **tracabilite** · 3022 mots · 0 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | ERP gestion de stock | /fonctionnalites/gestion-de-stock/ |
| body | lateral | Plan Contrôle Alimentaire | /blog/plan-de-controle-alimentaire/ |
| body | lateral | KPI Qualité Agro | /blog/kpi-qualite-agroalimentaire/ |
| body | lateral | DLC, DDM & DLUO | /blog/dlc-ddm-dluo/ |

### /blog/contraintes-reglementations-logiciel-agroalimentaire/
_Réglementation Agro • Logiciel & Conformité • 2026_ — cluster **tracabilite** · 830 mots · 2 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Processus Agroalimentaire | /blog/processus-agroalimentaire-guide/ |
| body | lateral | Conditionnement Alimentaire | /blog/conditionnement-alimentaire-erp/ |
| body | lateral | Numéros de Lot | /blog/numeros-de-lot/ |

### /blog/cout-marginal/
_Coût Marginal • Définition & Calcul • Guide Pratique_ — cluster **couts** · 1066 mots · 4 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Prix au Kilo | /blog/cout-prix-au-kilo/ |

### /blog/cuisine-centrale/
_Cuisine Centrale • Logiciel & Gestion • Guide Complet_ — cluster **traiteur** · 2418 mots · 0 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Logiciel calcul coût de revient traiteur | /blog/logiciel-calcul-cout-de-revient-traiteur/ |
| body | lateral | Logiciel commande grande surface traiteur | /blog/logiciel-commande-grande-surface-traiteur/ |
| body | lateral | Logiciel gestion recette multi-niveaux traiteur | /blog/logiciel-gestion-recette-multi-niveaux-traiteur/ |
| top | up | logiciel pour plats cuisinés industriels | /agroalimentaire/plats-cuisines-industriels/ |

### /blog/difference-prix-dachat-et-prix-de-revient/
_Prix d’Achat vs Prix de Revient • La Différence • Guide_ — cluster **couts** · 1070 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | pilotage de la production agroalimentaire | /fonctionnalites/fabrication/ |
| body | lateral | Coût de Revient Agro | /blog/calcul-cout-de-revient-logiciel/ |
| body | lateral | Prix Revient Boulangerie | /blog/calculer-le-prix-de-revient-en-boulangerie/ |
| body | lateral | Coût de Revient | /blog/cout-de-revient/ |
| top | up | logiciel de gestion des achats | /fonctionnalites/achat/ |

### /blog/dlc-ddm-dluo/
_DLC, DDM & DLUO • Différences & Gestion • Guide 2026_ — cluster **tracabilite** · 839 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Alerte Péremption | /blog/alerte-date-peremption/ |
| body | lateral | Agréage Agroalimentaire | /blog/agreage-agroalimentaire/ |
| body | lateral | Réglementation Agro | /blog/contraintes-reglementations-logiciel-agroalimentaire/ |

### /blog/enregistrement-comptable-variation-de-stock/
_Écriture Comptable Stock • Enregistrement • Guide_ — cluster **stock** · 1095 mots · 0 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | pilotage des stocks | /fonctionnalites/gestion-de-stock/ |
| body | lateral | Variation Stock & Résultat Fiscal | /blog/impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025/ |
| body | lateral | Variation Stock CUMP | /blog/calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025/ |
| body | lateral | Stock de Sécurité | /blog/calcul-stock-de-securite/ |

### /blog/erp-agroalimentaire/
_Meilleur ERP Agroalimentaire • Comparatif PME • 2026_ — cluster **erp_techno** · 1002 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Migration ERP Agro | /blog/migration-erp-agroalimentaire/ |
| body | lateral | ROI d’un ERP | /blog/roi-erp/ |
| body | lateral | Migration AS400 | /blog/erp-as400/ |

### /blog/erp-as400/
_Migration AS400 • Vers un ERP Moderne & SaaS • 2026_ — cluster **erp_techno** · 1026 mots · 2 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | ERP SaaS | /blog/erp-saas/ |
| body | lateral | ERP Cloud vs On-Premise | /blog/erp-cloud-saas-vs-on-premise/ |

### /blog/erp-boissons/
_ERP Boissons • Négoce, Accises & Consignes • Logiciel Spécialisé_ — cluster **negoce** · 4564 mots · 8 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | ERP distribution et négoce | /negoce/ |
| top | up | gestion du calibre et du poids variable | /agroalimentaire/maraicher/ |
| body | lateral | Logiciel Marée & Mareyeur | /blog/logiciel-maree-mareyeur/ |

### /blog/erp-cloud-saas-vs-on-premise/
_ERP Cloud vs On-Premise • Le Bon Choix PME • 2026_ — cluster **erp_techno** · 1905 mots · 4 liens ctx existants · budget 10

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | ERP de traçabilité alimentaire | /agroalimentaire/ |
| body | lateral | ERP Pour PME | /blog/erp-pme/ |
| body | lateral | Meilleur ERP Agroalimentaire | /blog/erp-agroalimentaire/ |
| body | lateral | Migration ERP Agro | /blog/migration-erp-agroalimentaire/ |

### /blog/erp-decoupe-viande-poisson/
_ERP Découpe • Viande & Poisson • Rendements Matière_ — cluster **viande** · 1381 mots · 4 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | ERP pour les métiers de la viande | /agroalimentaire/charcutier/ |
| body | lateral | Traçabilité viande logiciel : suivi lot charcutier & numéro de lot réglementation | /blog/tracabilite-viande-logiciel/ |
| body | lateral | ERP Viande & Volaille | /blog/erp-viande-volaille/ |

### /blog/erp-grossiste-distributeur/
_ERP Grossiste • Distribution & Marges • Spécialiste_ — cluster **negoce** · 931 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Logiciel Grossiste Alimentaire | /blog/logiciel-grossiste-alimentaire/ |
| body | lateral | Logiciel Boissons & Cave | /blog/logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises/ |
| body | lateral | ERP Boissons | /blog/erp-boissons/ |

### /blog/erp-pme/
_ERP Pour PME • Simple & Rentable • Guide Complet 2026_ — cluster **erp_techno** · 881 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Meilleur ERP Agroalimentaire | /blog/erp-agroalimentaire/ |
| body | lateral | Migration ERP Agro | /blog/migration-erp-agroalimentaire/ |
| body | lateral | ROI d’un ERP | /blog/roi-erp/ |

### /blog/erp-saas-cloud/
_ERP SaaS Cloud • Mobilité & Sécurité • Éditeur FR_ — cluster **erp_techno** · 1006 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | ERP Cloud vs On-Premise | /blog/erp-cloud-saas-vs-on-premise/ |
| body | lateral | ERP Pour PME | /blog/erp-pme/ |
| body | lateral | Meilleur ERP Agroalimentaire | /blog/erp-agroalimentaire/ |

### /blog/erp-saas/
_ERP SaaS • Avantages & Fonctionnalités • Guide 2026_ — cluster **erp_techno** · 988 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | ERP SaaS Cloud | /blog/erp-saas-cloud/ |
| body | lateral | ERP Cloud vs On-Premise | /blog/erp-cloud-saas-vs-on-premise/ |
| body | lateral | ERP Pour PME | /blog/erp-pme/ |

### /blog/erp-viande-volaille/
_ERP Viande & Volaille • Traçabilité & Poids Variable_ — cluster **viande** · 1120 mots · 1 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion de la découpe et des rendements | /agroalimentaire/charcutier/ |
| top | up | ERP distribution alimentaire | /agroalimentaire/ |
| body | lateral | ERP Découpe | /blog/erp-decoupe-viande-poisson/ |
| body | lateral | Traçabilité viande logiciel : suivi lot charcutier & numéro de lot réglementation | /blog/tracabilite-viande-logiciel/ |

### /blog/factur-x-e-facturation-logiciel/
_Factur-X • E-Facturation Obligatoire 2026 • Guide PME Agro_ — cluster **facturation** · 4652 mots · 9 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Bon de Commande | /blog/bon-de-commande/ |
| body | lateral | Bon de Commande Traiteur | /blog/bon-de-commande-traiteur/ |

### /blog/facture-exacompta/
_Facture Exacompta • Alternative Numérique • ERP Agro_ — cluster **facturation** · 1453 mots · 1 liens ctx existants · budget 8

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Facture Traiteur | /blog/facture-traiteur/ |
| body | lateral | Factur-X | /blog/factur-x-e-facturation-logiciel/ |
| body | lateral | Bon de Commande | /blog/bon-de-commande/ |

### /blog/facture-traiteur/
_Facture Traiteur • Modèle & Mentions • Guide 2026_ — cluster **facturation** · 1180 mots · 3 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion des factures et échéances | /fonctionnalites/facturation/ |
| top | up | gestion commerciale agroalimentaire | /fonctionnalites/vente/ |
| body | lateral | Factur-X | /blog/factur-x-e-facturation-logiciel/ |

### /blog/fifo-fefo-lifo/
_FIFO, FEFO & LIFO • Méthodes de Stock • Guide 2026_ — cluster **stock** · 980 mots · 2 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Variation Stock + ou | /blog/variation-de-stock-positif-negatif/ |
| body | lateral | Variation Stock Auto | /blog/gestion-automatisee-des-variations-de-stock/ |
| body | lateral | Écriture Comptable Stock | /blog/enregistrement-comptable-variation-de-stock/ |

### /blog/gestion-automatisee-des-variations-de-stock/
_Variation Stock Auto • ERP & Automatisation • Guide_ — cluster **stock** · 1014 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion des stocks en temps réel | /fonctionnalites/gestion-de-stock/ |
| body | lateral | Écriture Comptable Stock | /blog/enregistrement-comptable-variation-de-stock/ |
| body | lateral | Variation Stock & Résultat Fiscal | /blog/impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025/ |
| body | lateral | Variation Stock CUMP | /blog/calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025/ |

### /blog/gestion-decoupe-viande-logiciel/
_Gestion découpe viande au logiciel : rendement matière charcuterie & taux découpe porc_ — cluster **fabrication** · 2112 mots · 5 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion de la production | /fonctionnalites/fabrication/ |
| top | up | logiciel de planification industrielle | /fonctionnalites/planification-production-erp/ |
| body | lateral | Ordre de Fabrication | /blog/ordre-de-fabrication/ |
| body | lateral | Ordonnancement | /blog/ordonnancement-planification/ |

### /blog/gestion-des-inventaires/
_Gestion des Inventaires • Méthode & Logiciel • Guide_ — cluster **stock** · 1220 mots · 1 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Gestion Stock Multi-Entrepôts | /blog/gestion-stock-multi-entrepots/ |
| body | lateral | Réapprovisionnement | /blog/reapprovisionnement-stocks/ |
| body | lateral | Alerte Stock | /blog/alerte-stock-securite/ |

### /blog/hello-harel-vs-divalto/
_Hello Harel vs Divalto • Comparatif ERP Agroalimentaire 2026_ — cluster **comparatifs** · 2719 mots · 8 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Hello Harel vs Odoo | /blog/hello-harel-vs-odoo/ |
| body | lateral | Hello Harel vs Sage | /blog/hello-harel-vs-sage/ |
| body | lateral | Hello Harel vs Silog | /blog/hello-harel-vs-silog/ |

### /blog/hello-harel-vs-odoo/
_Hello Harel vs Odoo • ERP Spécialisé vs Généraliste 2026_ — cluster **comparatifs** · 2833 mots · 8 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | guide comparatif ERP | /comparatifs/ |
| body | lateral | Hello Harel vs Sage | /blog/hello-harel-vs-sage/ |
| body | lateral | Hello Harel vs Silog | /blog/hello-harel-vs-silog/ |

### /blog/hello-harel-vs-sage/
_Hello Harel vs Sage • PME Agro : Spécialisé vs Généraliste_ — cluster **comparatifs** · 2764 mots · 9 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | meilleur ERP agroalimentaire | /comparatifs/ |
| body | lateral | Hello Harel vs Silog | /blog/hello-harel-vs-silog/ |

### /blog/hello-harel-vs-silog/
_Hello Harel vs Silog • Comparatif ERP Agro PME 2026_ — cluster **comparatifs** · 2652 mots · 10 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Meilleurs ERP Import-Export | /blog/meilleurs-erp-import-export/ |

### /blog/impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025/
_Variation Stock & Résultat Fiscal • Impact • Guide_ — cluster **stock** · 1051 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | optimisation des stocks alimentaires | /fonctionnalites/gestion-de-stock/ |
| body | lateral | Variation Stock CUMP | /blog/calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025/ |
| body | lateral | Stock de Sécurité | /blog/calcul-stock-de-securite/ |
| body | lateral | Calcul Stock Moyen | /blog/calcul-stock-moyen/ |

### /blog/integrateur-erp-lyon/
_Intégrateur ERP Lyon • Agro & Négoce • Éditeur Direct_ — cluster **integrateur** · 1323 mots · 0 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Intégrateur ERP Paris | /blog/integrateur-erp-paris/ |

### /blog/integrateur-erp-paris/
_Intégrateur ERP Paris • Agro & Négoce • Direct_ — cluster **integrateur** · 1468 mots · 0 liens ctx existants · budget 8

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Intégrateur ERP Lyon | /blog/integrateur-erp-lyon/ |

### /blog/kpi-qualite-agroalimentaire/
_KPI Qualité Agro • 7 Indicateurs Clés • Guide Expert_ — cluster **tracabilite** · 1651 mots · 1 liens ctx existants · budget 9

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | DLC, DDM & DLUO | /blog/dlc-ddm-dluo/ |
| body | lateral | Alerte Péremption | /blog/alerte-date-peremption/ |
| body | lateral | Agréage Agroalimentaire | /blog/agreage-agroalimentaire/ |

### /blog/logiciel-calcul-cout-de-revient-traiteur/
_Logiciel calcul coût de revient traiteur_ — cluster **traiteur** · 1321 mots · 2 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion de commandes traiteur | /agroalimentaire/traiteur/ |
| top | up | ERP métier agroalimentaire | /agroalimentaire/ |
| body | lateral | Logiciel commande grande surface traiteur | /blog/logiciel-commande-grande-surface-traiteur/ |
| body | lateral | Logiciel traçabilité DLC traiteur | /blog/logiciel-tracabilite-dlc-traiteur/ |
| top | up | ERP pour la cuisine industrielle | /agroalimentaire/plats-cuisines-industriels/ |

### /blog/logiciel-commande-grande-surface-traiteur/
_Logiciel commande grande surface traiteur_ — cluster **traiteur** · 1315 mots · 0 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | logiciel pour traiteurs et cuisines centrales | /agroalimentaire/traiteur/ |
| top | up | ERP spécialisé agroalimentaire | /agroalimentaire/ |
| body | lateral | Logiciel gestion recette multi-niveaux traiteur | /blog/logiciel-gestion-recette-multi-niveaux-traiteur/ |
| body | lateral | Logiciel traçabilité DLC traiteur | /blog/logiciel-tracabilite-dlc-traiteur/ |
| body | lateral | Alternatives à Copilote pour les Traiteurs | /blog/alternatives-copilote-traiteur/ |

### /blog/logiciel-gestion-calibre-fruits-legumes/
_Logiciel gestion calibre fruits et légumes_ — cluster **maraicher** · 1336 mots · 2 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | logiciel pour maraîchers | /agroalimentaire/maraicher/ |
| top | up | ERP négoce alimentaire | /negoce/ |
| body | lateral | Top 8 ERP Fruits & Légumes | /blog/meilleurs-erp-maraichers-fruits-legumes/ |
| body | lateral | MIN | /blog/min/ |

### /blog/logiciel-gestion-recette-multi-niveaux-traiteur/
_Logiciel gestion recette multi-niveaux traiteur_ — cluster **traiteur** · 1249 mots · 0 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | ERP pour l'agroalimentaire | /agroalimentaire/ |
| body | lateral | Logiciel traçabilité DLC traiteur | /blog/logiciel-tracabilite-dlc-traiteur/ |
| body | lateral | Alternatives à Copilote pour les Traiteurs | /blog/alternatives-copilote-traiteur/ |
| body | lateral | Cuisine Centrale | /blog/cuisine-centrale/ |
| top | up | gestion des recettes et conformité INCO | /agroalimentaire/plats-cuisines-industriels/ |

### /blog/logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises/
_Logiciel Boissons & Cave • Consignes & Accises • 2026_ — cluster **negoce** · 915 mots · 3 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | logiciel de négoce alimentaire | /negoce/ |
| top | up | logiciel pour exportateurs de fruits et légumes | /agroalimentaire/maraicher/ |

### /blog/logiciel-maree-mareyeur/
_Logiciel Marée & Mareyeur • Rendements & Criée • 2026_ — cluster **negoce** · 1425 mots · 3 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Télévente Alimentaire | /blog/logiciel-televente-alimentaire/ |
| body | lateral | ERP Approvisionnement | /blog/meilleurs-erp-gestion-approvisionnements/ |
| body | lateral | ERP Grossiste | /blog/erp-grossiste-distributeur/ |

### /blog/logiciel-prix-du-jour-fruits-legumes/
_Logiciel prix du jour fruits et légumes_ — cluster **maraicher** · 1333 mots · 0 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | ERP pour grossistes en fruits et légumes | /agroalimentaire/maraicher/ |
| top | up | logiciel pour grossistes alimentaires | /negoce/ |
| top | up | ERP pour l'industrie agroalimentaire | /agroalimentaire/ |
| body | lateral | Top 8 ERP Fruits & Légumes | /blog/meilleurs-erp-maraichers-fruits-legumes/ |
| body | lateral | MIN | /blog/min/ |
| body | lateral | Logiciel gestion calibre fruits et légumes | /blog/logiciel-gestion-calibre-fruits-legumes/ |

### /blog/logiciel-televente-alimentaire/
_Télévente Alimentaire • Logiciel Saisie Rapide • 50+ Cmd/Jour_ — cluster **negoce** · 4111 mots · 9 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | ERP Approvisionnement | /blog/meilleurs-erp-gestion-approvisionnements/ |
| body | lateral | Logiciel Grossiste Alimentaire | /blog/logiciel-grossiste-alimentaire/ |

### /blog/logiciel-tracabilite-dlc-traiteur/
_Logiciel traçabilité DLC traiteur_ — cluster **traiteur** · 1286 mots · 2 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | solution traiteur | /agroalimentaire/traiteur/ |
| top | up | ERP PME agroalimentaire | /agroalimentaire/ |
| body | lateral | Alternatives à Copilote pour les Traiteurs | /blog/alternatives-copilote-traiteur/ |
| body | lateral | Cuisine Centrale | /blog/cuisine-centrale/ |
| body | lateral | Logiciel calcul coût de revient traiteur | /blog/logiciel-calcul-cout-de-revient-traiteur/ |

### /blog/maitriser-la-gestion-des-stocks/
_Maîtriser Ses Stocks • 6 Exercices Corrigés • Guide_ — cluster **stock** · 3008 mots · 1 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | FIFO, FEFO & LIFO | /blog/fifo-fefo-lifo/ |
| body | lateral | Variation Stock + ou | /blog/variation-de-stock-positif-negatif/ |
| body | lateral | Variation Stock Auto | /blog/gestion-automatisee-des-variations-de-stock/ |

### /blog/meilleurs-erp-boulangerie/
_Meilleurs ERP Boulangerie • Comparatif Complet • 2026_ — cluster **boulanger** · 1796 mots · 0 liens ctx existants · budget 9

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | logiciel boulangerie-pâtisserie | /agroalimentaire/boulanger/ |
| body | lateral | Prix Revient Boulangerie | /blog/calculer-le-prix-de-revient-en-boulangerie/ |

### /blog/meilleurs-erp-gestion-approvisionnements/
_ERP Approvisionnement • Supply Chain & MRP • 2026_ — cluster **negoce** · 989 mots · 1 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | ERP Grossiste | /blog/erp-grossiste-distributeur/ |
| body | lateral | Logiciel Grossiste Alimentaire | /blog/logiciel-grossiste-alimentaire/ |
| body | lateral | Logiciel Boissons & Cave | /blog/logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises/ |
| top | up | pilotage des achats | /fonctionnalites/achat/ |

### /blog/meilleurs-erp-import-export/
_Meilleurs ERP Import-Export • Négoce International • 2026_ — cluster **comparatifs** · 1188 mots · 1 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Alternative Akanea | /blog/alternative-akanea-erp/ |
| body | lateral | Alternative Archipelia | /blog/alternative-archipelia/ |
| body | lateral | Alternative Cegid | /blog/alternative-cegid/ |
| top | up | logiciel import-export agroalimentaire | /fonctionnalites/import-export/ |

### /blog/migration-erp-agroalimentaire/
_Migration ERP Agro • Sécurisée & Rapide • En 5 Jours_ — cluster **erp_techno** · 1871 mots · 8 liens ctx existants · budget 10

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Migration AS400 | /blog/erp-as400/ |
| body | lateral | ERP SaaS | /blog/erp-saas/ |

### /blog/min/
_MIN • Marché d’Intérêt National • Guide & Logiciel_ — cluster **maraicher** · 1032 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Logiciel gestion calibre fruits et légumes | /blog/logiciel-gestion-calibre-fruits-legumes/ |
| body | lateral | Logiciel prix du jour fruits et légumes | /blog/logiciel-prix-du-jour-fruits-legumes/ |
| body | lateral | Top 8 ERP Fruits & Légumes | /blog/meilleurs-erp-maraichers-fruits-legumes/ |

### /blog/numeros-de-lot/
_Numéros de Lot • Gestion & Traçabilité • Guide Pratique_ — cluster **tracabilite** · 1674 mots · 6 liens ctx existants · budget 9

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Traçabilité viande logiciel : suivi lot charcutier & numéro de lot réglementation | /blog/tracabilite-viande-logiciel/ |
| body | lateral | Traçabilité Lot & DLC | /blog/tracabilite-lot-dlc-logiciel/ |

### /blog/opc-ua/
_OPC UA • Protocole Industriel & ERP • Guide Tech_ — cluster **fabrication** · 896 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | calcul du coût de revient en production | /fonctionnalites/fabrication/ |
| top | up | planifier vos fournées et ordres de fabrication | /fonctionnalites/planification-production-erp/ |
| body | lateral | Gestion découpe viande au logiciel : rendement matière charcuterie & taux découpe porc | /blog/gestion-decoupe-viande-logiciel/ |
| body | lateral | Calcul freinte charcuterie : pilotage perte de séchage salaison au logiciel ERP | /blog/calcul-freinte-charcuterie-logiciel/ |
| body | lateral | Ordre de Fabrication | /blog/ordre-de-fabrication/ |

### /blog/optimisation-entrepot/
_Optimisation Entrepôt • Logistique & ERP • Guide PME_ — cluster **stock** · 1945 mots · 6 liens ctx existants · budget 10

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Maîtriser Ses Stocks | /blog/maitriser-la-gestion-des-stocks/ |
| body | lateral | Variation Stock + ou | /blog/variation-de-stock-positif-negatif/ |

### /blog/ordonnancement-planification/
_Ordonnancement • Planification & Production • Guide_ — cluster **fabrication** · 1109 mots · 0 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | logiciel de production alimentaire | /fonctionnalites/fabrication/ |
| body | lateral | OPC UA | /blog/opc-ua/ |
| body | lateral | Gestion découpe viande au logiciel : rendement matière charcuterie & taux découpe porc | /blog/gestion-decoupe-viande-logiciel/ |
| body | lateral | Calcul freinte charcuterie : pilotage perte de séchage salaison au logiciel ERP | /blog/calcul-freinte-charcuterie-logiciel/ |

### /blog/ordre-de-fabrication/
_Ordre de Fabrication • Gestion & ERP • Guide Complet_ — cluster **fabrication** · 1192 mots · 2 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Ordonnancement | /blog/ordonnancement-planification/ |
| body | lateral | OPC UA | /blog/opc-ua/ |
| body | lateral | Gestion découpe viande au logiciel : rendement matière charcuterie & taux découpe porc | /blog/gestion-decoupe-viande-logiciel/ |

### /blog/plan-de-controle-alimentaire/
_Plan Contrôle Alimentaire • Méthode & Outils • 2026_ — cluster **tracabilite** · 1434 mots · 1 liens ctx existants · budget 7

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | KPI Qualité Agro | /blog/kpi-qualite-agroalimentaire/ |
| body | lateral | DLC, DDM & DLUO | /blog/dlc-ddm-dluo/ |
| body | lateral | Alerte Péremption | /blog/alerte-date-peremption/ |

### /blog/prix-dachat-definition/
_Prix d’Achat • Définition & Calcul • Guide Comptable_ — cluster **couts** · 979 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion des nomenclatures | /fonctionnalites/fabrication/ |
| body | lateral | Prix d’Achat vs Prix de Revient | /blog/difference-prix-dachat-et-prix-de-revient/ |
| body | lateral | Coût de Revient Agro | /blog/calcul-cout-de-revient-logiciel/ |
| body | lateral | Prix Revient Boulangerie | /blog/calculer-le-prix-de-revient-en-boulangerie/ |
| top | up | module achats et approvisionnements | /fonctionnalites/achat/ |

### /blog/reapprovisionnement-stocks/
_Réapprovisionnement • Méthodes & ERP • Guide 2026_ — cluster **stock** · 850 mots · 0 liens ctx existants · budget 5

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | gestion multi-dépôts | /fonctionnalites/gestion-de-stock/ |
| body | lateral | Alerte Stock | /blog/alerte-stock-securite/ |
| body | lateral | Optimisation Entrepôt | /blog/optimisation-entrepot/ |
| body | lateral | Maîtriser Ses Stocks | /blog/maitriser-la-gestion-des-stocks/ |

### /blog/relance-client/
_Relance Client • Automatisation & ERP • Guide Pratique_ — cluster **facturation** · 1578 mots · 1 liens ctx existants · budget 8

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | facturation automatisée | /fonctionnalites/facturation/ |
| top | up | logiciel de gestion commerciale | /fonctionnalites/vente/ |
| body | lateral | Facture Exacompta | /blog/facture-exacompta/ |
| body | lateral | Facture Traiteur | /blog/facture-traiteur/ |
| body | lateral | Factur-X | /blog/factur-x-e-facturation-logiciel/ |

### /blog/roi-erp/
_ROI d’un ERP • Calcul & Résultats Concrets • Guide_ — cluster **erp_techno** · 1238 mots · 0 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Migration AS400 | /blog/erp-as400/ |
| body | lateral | ERP SaaS | /blog/erp-saas/ |
| body | lateral | ERP SaaS Cloud | /blog/erp-saas-cloud/ |

### /blog/tracabilite-de-la-viande/
_Traçabilité Viande • Lots & Normes • Guide Complet_ — cluster **tracabilite** · 1250 mots · 3 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Traçabilité viande logiciel : suivi lot charcutier & numéro de lot réglementation | /blog/tracabilite-viande-logiciel/ |
| body | lateral | Traçabilité Lot & DLC | /blog/tracabilite-lot-dlc-logiciel/ |

### /blog/tracabilite-lot-dlc-logiciel/
_Traçabilité Lot & DLC • Logiciel de Suivi Réglementaire • Guide 2026_ — cluster **tracabilite** · 4649 mots · 10 liens ctx existants · budget 11

| zone | type | ancre | → cible |
|---|---|---|---|
| body | lateral | Plan Contrôle Alimentaire | /blog/plan-de-controle-alimentaire/ |

### /blog/tracabilite-viande-logiciel/
_Traçabilité viande logiciel : suivi lot charcutier & numéro de lot réglementation_ — cluster **viande** · 1964 mots · 4 liens ctx existants · budget 10

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | logiciel pour charcutier-traiteur | /agroalimentaire/charcutier/ |
| top | up | logiciel ERP agroalimentaire | /agroalimentaire/ |
| body | lateral | ERP Viande & Volaille | /blog/erp-viande-volaille/ |
| body | lateral | ERP Découpe | /blog/erp-decoupe-viande-poisson/ |

### /blog/variation-de-stock-positif-negatif/
_Variation Stock + ou – • Impact & Analyse • Guide_ — cluster **stock** · 1142 mots · 1 liens ctx existants · budget 6

| zone | type | ancre | → cible |
|---|---|---|---|
| top | up | suivi de stock multi-entrepôts | /fonctionnalites/gestion-de-stock/ |
| body | lateral | Variation Stock Auto | /blog/gestion-automatisee-des-variations-de-stock/ |
| body | lateral | Écriture Comptable Stock | /blog/enregistrement-comptable-variation-de-stock/ |
| body | lateral | Variation Stock & Résultat Fiscal | /blog/impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025/ |
