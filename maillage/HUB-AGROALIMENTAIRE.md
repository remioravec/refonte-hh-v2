# Hub agroalimentaire global — `/agroalimentaire/guide-achat/`

Page boost du silo agro, montée selon le schéma de maillage : 8 sections numérotées,
chacune avec **une cible unique** et un lien réciproque. C'est la pièce qui manque
aujourd'hui sur tout le site (cf. `INVENTAIRE-SILOS.md`).

- **Mère** : `/agroalimentaire/` — lien réciproque « boost » ↔ hub
- **Filles** : les 15 métiers, atteints depuis le hub et renvoyant vers lui
- **Articles** : 80 articles après arbitrage GSC, répartis sur les 8 sections (cf. `ARTICLES-103.md`)

## Les 8 sections

| § | Section | Cible du lien | Articles rattachés |
|:---:|---|---|---:|
| 1 | Traçabilité et conformité : ce que la réglementation impose | `/fonctionnalites/tracabilite-alimentaire/` | 9 |
| 2 | Coût de revient, rendement matière et freinte | `/fonctionnalites/gestion-rendement-matiere-logiciel/` | 13 |
| 3 | Lots, DLC et rotation des stocks | `/fonctionnalites/gestion-de-stock/` | 8 |
| 4 | Planifier la production et la fabrication | `/fonctionnalites/planification-production-erp/` | 7 |
| 5 | Commandes, bons de livraison et facturation | `/fonctionnalites/facturation-automatique-bon-livraison/` | 6 |
| 6 | Vendre à la GMS : EDI, pénalités, tarifs | `/negoce/tarifs-reporting-edi/` | 13 |
| 7 | Sortir d'Excel ou d'un AS/400 | `/migration-as400/` | 5 |
| 8 | Comparer les éditeurs du marché | `/comparatifs/` | 18 |

Chaque section porte **une ancre orange** (le lien vers sa cible), et chaque article de la
section pose ses **2 liens montants** : `guide-achat/#section-N` + la landing du silo.

## Les 8 piliers, désignés par la GSC

Un pilier = l'article qui porte déjà le trafic de sa section. C'est lui qui pose son lien vers
son `§N` en premier, les autres suivent. Clics sur 16 mois (Search Console).

| § | Pilier | Clics | Pourquoi |
|:---:|---|---:|---|
| 2 | `cout-prix-au-kilo` | 14 112 | 1re source de trafic du site, à elle seule 41 % du blog |
| 3 | `maitriser-la-gestion-des-stocks` | 6 025 | 2ᵉ article du site |
| 1 | `numeros-de-lot` | 2 823 | tête du cluster traçabilité |
| 5 | `facture-exacompta` | 727 | et `facture-traiteur` (635) juste derrière |
| 7 | `erp-as400` | 570 | porte déjà l'offre de migration |
| 4 | `ordre-de-fabrication` | 331 | |
| 6 | `min` | 218 | à condition de corriger ses 14 liens morts `href="#"` |
| 8 | `meilleurs-erp-maraichers-fruits-legumes` | 95 | 40 clics sur les 90 derniers jours : la section monte |

## Ce que le hub corrige, structurellement

**Le §2 se cannibalise.** `cout-prix-au-kilo` (1 793 mots) fait 14 112 clics, quand
`cout-de-revient` (6 330 mots) en fait 65 pour **19 665 impressions en position 25,6**. Sur les
90 derniers jours cette position remonte à 13,5 : la page est en train de sortir, le hub doit
l'accompagner plutôt que la laisser seule.

**Les pages qui vendent ne ressortent pas.** Le blog capte 80 % des clics du site
(34 072 sur 42 444). Tout ce trafic arrive sur des articles de définition comptable — coût au
kilo, prix moyen, variation de stock — qui ne parlent pas d'agroalimentaire. Le hub est ce qui
relie ce flux aux pages métier : les §2 et §3 récupèrent ces lecteurs et les font descendre vers
les filles.

**74 % du trafic tient sur 4 articles.** `cout-prix-au-kilo`, `maitriser-la-gestion-des-stocks`,
`numeros-de-lot` et `calculer-le-prix-de-revient-en-boulangerie` = 25 107 des 33 987 clics du
blog. Ces 4 articles posent leurs liens montants avant tous les autres.

**Le trafic baisse.** ~2 653 clics/mois en moyenne sur 16 mois, ~948/mois sur le trimestre
écoulé. Le hub ne suffira pas à inverser ça seul, mais il concentre la valeur des 19 fusions
au lieu de la laisser se disperser sur des doublons.

**89 024 impressions dorment en page 2-3.** Cinq articles (`erp-pme`, `bon-de-commande`,
`cout-de-revient`, `erp-saas`, `tracabilite-de-la-viande`) captent 89 024 impressions pour
166 clics. C'est le premier gisement du site, et quatre d'entre eux sont dans les §2, §3, §5 et §7.

## Réserve de méthode

Les cibles §1 à §7 pointent vers des pages `/fonctionnalites/` et `/negoce/` — donc vers des
**filles d'autres silos**. C'est assumé : le hub agro est global, il traverse les silos
fonctionnels. Si tu préfères garder chaque hub dans son silo, il faut alors créer les pages
cibles sous `/agroalimentaire/` et non réutiliser les fonctionnalités — c'est un arbitrage
à trancher avant la rédaction.
