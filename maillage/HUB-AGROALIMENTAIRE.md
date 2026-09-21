# Hub agroalimentaire global — `/agroalimentaire/guide-achat/`

Page boost du silo agro, montée selon le schéma de maillage : 8 sections numérotées,
chacune avec **une cible unique** et un lien réciproque. C'est la pièce qui manque
aujourd'hui sur tout le site (cf. `INVENTAIRE-SILOS.md`).

- **Mère** : `/agroalimentaire/` — lien réciproque « boost » ↔ hub
- **Filles** : les 15 métiers, atteints depuis le hub et renvoyant vers lui
- **Articles** : 77 articles après arbitrage, répartis sur les 8 sections (cf. `ARTICLES-103.md`)

## Les 8 sections

| § | Section | Cible du lien | Articles rattachés |
|:---:|---|---|---:|
| 1 | Traçabilité et conformité : ce que la réglementation impose | `/fonctionnalites/tracabilite-alimentaire/` | 9 |
| 2 | Coût de revient, rendement matière et freinte | `/fonctionnalites/gestion-rendement-matiere-logiciel/` | 13 |
| 3 | Lots, DLC et rotation des stocks | `/fonctionnalites/gestion-de-stock/` | 8 |
| 4 | Planifier la production et la fabrication | `/fonctionnalites/planification-production-erp/` | 5 |
| 5 | Commandes, bons de livraison et facturation | `/fonctionnalites/facturation-automatique-bon-livraison/` | 5 |
| 6 | Vendre à la GMS : EDI, pénalités, tarifs | `/negoce/tarifs-reporting-edi/` | 13 |
| 7 | Sortir d'Excel ou d'un AS/400 | `/migration-as400/` | 4 |
| 8 | Comparer les éditeurs du marché | `/comparatifs/` | 18 |

Chaque section porte **une ancre orange** (le lien vers sa cible), et chaque article de la
section pose ses **2 liens montants** : `guide-achat/#section-N` + la landing du silo.

## Les 4 piliers à traiter en premier

Un pilier = l'article qui porte déjà le trafic ou le volume de sa section. C'est lui qui
fait le lien vers son `§N` en premier, les autres suivent.

| § | Pilier | ETV | Pourquoi |
|:---:|---|---:|---|
| 2 | `cout-prix-au-kilo` | 608 | 1re source de trafic du site à lui seul |
| 1 | `numeros-de-lot` | 80 | seul article traçabilité qui ressort |
| 7 | `erp-as400` | 63 | porte déjà l'offre de migration |
| 3 | `fifo-fefo-lifo` | 24 | tête du cluster rotation |

## Ce que le hub corrige, structurellement

**Le §2 est cannibalisé.** `cout-de-revient` fait 6 330 mots pour **zéro** visibilité, alors
que `cout-prix-au-kilo` (1 793 mots) ramène 608 d'ETV. Deux autres articles couvrent le même
sujet. Le hub force à désigner une tête de cluster — ici `cout-de-revient` comme page de fond,
`cout-prix-au-kilo` comme entrée de trafic, et une fusion des deux doublons.

**Les pages qui vendent ne ressortent pas.** Sur les 178 URL du site, seules 39 ont une
visibilité mesurable, et une seule page métier y figure (`/agroalimentaire/boulanger/`, position
61-70). Tout le trafic est porté par des articles de définition comptable — du TOFU qui ne parle
pas d'agroalimentaire. Le hub est ce qui relie ce trafic aux pages métier : les §2 et §3 captent
les lecteurs « coût de revient » et les font descendre vers les filles.

**73 % du trafic tient sur 4 articles.** `cout-prix-au-kilo`, `cout-marginal`,
`prix-dachat-definition`, `calcul-du-prix-moyen` = 1 145 des 1 560 d'ETV du blog. Ces 4 articles
doivent poser leurs liens montants avant tous les autres.

## Réserve de méthode

Les cibles §1 à §7 pointent vers des pages `/fonctionnalites/` et `/negoce/` — donc vers des
**filles d'autres silos**. C'est assumé : le hub agro est global, il traverse les silos
fonctionnels. Si tu préfères garder chaque hub dans son silo, il faut alors créer les pages
cibles sous `/agroalimentaire/` et non réutiliser les fonctionnalités — c'est un arbitrage
à trancher avant la rédaction.
