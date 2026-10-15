# Semaine du 19/10/2026 — la boucle complète

Hello Harel · 15 octobre 2026 · [roadmap](https://docs.google.com/spreadsheets/d/1SImCHCu7gmSW3aIKTmu_jAhbukPeOv0U3_ONS-96_hM/edit)

---

## 1 · Pages générant des démos

Mesure sur la base d'attribution, **64 demandes depuis le 01/07/2026**, par
page de première visite :

| Page d'entrée | Demandes |
|---|---|
| `/` (accueil) | **29** |
| `/negoce/` | **8** |
| `/agroalimentaire/` | **5** |
| `/blog/meilleurs-erp-maraichers-fruits-legumes/` | 3 |
| `/contact/` · `/negoce/tracabilite-lots/` · `/qui-sommes-nous/` · `/blog/numeros-de-lot/` | 2 chacune |
| 11 autres pages | 1 chacune |

**Aucune page `/fonctionnalites/` n'a jamais porté une seule demande.** Zéro
sur 64.

C'est le fait qui commande toute la semaine. Les trois pages du 19/10
appartiennent à la famille qui ne convertit pas. Les réécrire ne suffisait
donc pas : il fallait leur ajouter l'étage qui manque, et les **brancher sur
les pages qui, elles, convertissent** — l'accueil, `/negoce/`,
`/agroalimentaire/`, `/tarifs/`, `/contact/`.

## 2 · Requêtes secondaires

Search Console, page par page, du 17/07 au 12/10/2026. Ce sont ces lignes qui
ont dicté les sections ajoutées — rien n'a été inventé.

### `/fonctionnalites/logistique/`

| Requête secondaire | Impressions | Position |
|---|---|---|
| prestataire logistique connecté erp | **55** | 67 |
| crm agroalimentaire | 48 | 96 |
| erp gestion approvisionnement restauration collective | 8 | 88 |
| logiciel logistique produits frais | 8 | 81 |
| erp de localisation pour suivi des livraisons | 7 | 46 |
| wms agroalimentaire / wms industrie agroalimentaire / wms pour l'agroalimentaire | 6 | 51–91 |
| erp réception marchandises restaurant + logiciel de gestion des réceptions | 6 | 86–94 |

### `/fonctionnalites/planification-production-erp/`

| Requête secondaire | Impressions | Position |
|---|---|---|
| **devis** logiciel d'ordonnancement | **60** | 38 |
| outil d'ordonnancement et de planification de la production | 40 | 77 |
| logiciel ordonnancement atelier | 36 | 56 |
| logiciel planification fabrication alimentaire | 24 | 93 |
| logiciel ordonnancement | 9 | 17 |
| outil planning de production cuisine | 9 | 57 |
| erp ordonnancement (+ production) | 14 | 56–58 |

### `/fonctionnalites/vente/`

| Requête secondaire | Impressions | Position |
|---|---|---|
| hello harel / helloharel / hello harel connexion | **445** | **1** |
| crm agroalimentaire | 20 | 87 |
| logiciel négoce fruits et légumes | 12 | 91 |
| devis préparation agroalimentaire | 4 | 33 |

## 3 · Cartographie de la demande — deux enseignements

**La page planification vise le mauvais mot.** Les formulations en
**ordonnancement** cumulent 60 + 40 + 36 + 14 = **150 impressions**, contre
quelques unités pour « planification ». Le H1 portait déjà les deux ; le bloc
MOFU creuse le second et ouvre sur la différence entre planifier et
ordonnancer, qui est la vraie question du visiteur.

**La page vente capte des clients qui cherchent leur connexion.** Elle est en
**position 1** sur « hello harel connexion » (26 impressions) et
« helloharel » (44) — soit 445 impressions de marque au total, pour **1 clic**.
Des clients existants atterrissent sur une page commerciale au lieu de leur
espace. C'est un défaut d'expérience autant qu'un signal gâché. Une carte du
bloc MOFU le dit et les réoriente ; **la vraie correction est ailleurs** : il
faut une page d'accès client, ou une redirection. À arbitrer.

## 4 · Ce qui est en ligne

| Page | Posé |
|---|---|
| [`/fonctionnalites/logistique/`](https://www.helloharel.com/fonctionnalites/logistique/) | badge, H1 à l'exact match, accroche, signature, **MOFU 5 cartes + BOFU 3 étapes**, FAQPage JSON-LD, title et description |
| [`/fonctionnalites/planification-production-erp/`](https://www.helloharel.com/fonctionnalites/planification-production-erp/) | **MOFU + BOFU orienté devis**, title et description |
| [`/fonctionnalites/vente/`](https://www.helloharel.com/fonctionnalites/vente/) | badge, H1, accroche, signature, **MOFU + BOFU**, FAQPage JSON-LD, title et description |

**Contrôles au rendu.** Zéro débordement horizontal à 390 px comme à 1280 px,
un seul H1 par page, 0 bloc JSON-LD illisible, titles entre 440 et 464 px,
descriptions entre 902 et 924 px. Les 3 titles sont épinglés dans l'extrait 12
— le réglage « Capitaliser les titles » de Rank Math est toujours sur ON.

**Sitemap** purgé, régénéré et resoumis : 72 URL dans `page-sitemap.xml`, les
3 pages présentes. **Statuts** passés à TERMINE, lignes en vert.

## 5 · Le BOFU branche sur ce qui convertit

Chaque page renvoie désormais, en bas de parcours, vers les pages qui portent
réellement des demandes :

- logistique → `/negoce/` · `/agroalimentaire/` · `/tarifs/` · `/contact/`
- planification → `/fonctionnalites/fabrication/` · `/tarifs/` · `/contact/`
- vente → `/negoce/` · `/agroalimentaire/` · `/tarifs/` · `/contact/`

C'est le seul moyen mesurable de faire remonter une famille de pages qui
n'avait jamais converti : on ne lui demande pas de convertir seule, on la
branche sur ce qui convertit.

## 6 · À mesurer à J+21

- Les requêtes **ordonnancement** gagnent-elles des positions sur la page
  planification (point de départ : 38, 56, 77) ?
- `prestataire logistique connecté erp` sort-il de la position 67 ?
- Une demande arrive-t-elle, pour la première fois, depuis une page
  `/fonctionnalites/` ?
