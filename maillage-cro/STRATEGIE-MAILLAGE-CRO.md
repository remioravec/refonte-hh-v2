# Stratégie Maillage interne + CRO — helloharel.com

> Toolkit `maillage-cro/`. Données **live** via l'API REST WordPress (lecture
> seule pour l'inventaire). **Aucune écriture n'est faite en production** : tout
> est en DRY-RUN, à valider avant application.

## 1. Principes appliqués (surfeur raisonnable)

Inspirés de la « bible du maillage interne » ThotSEO + Value Equation (Hormozi).

1. **Liens contextuels > boilerplate.** ~70 % du poids d'un lien vient du contenu
   éditorial. L'inventaire **sépare** les liens dans la prose `<p>` (contextuels)
   du header/footer/nav (boilerplate) — seuls les contextuels comptent ici.
2. **Premier lien = ancre retenue.** Sur une page, Google ne retient que l'ancre
   du premier lien vers une cible donnée. Les pools d'ancres sont **ordonnés**
   (intention forte d'abord) ; le lien montant stratégique est placé **en haut**.
3. **Diversification d'ancres.** Objectif ≥ 11 ancres distinctes vers les pages
   money. Le sélecteur n'utilise **jamais** une ancre déjà employée vers la cible
   → chaque nouveau lien fait grimper le compteur d'ancres distinctes.
4. **Zéro cannibalisation.** Une ancre = une seule cible (garde-fou global, sur
   le plan **et** l'existant). Audit dans `MAILLAGE-DRY-RUN.md` (objectif : 0).
5. **Direction du cocon / boucles.** L3 (articles) → L2 (page fille du cluster) →
   L1 (hub mère) en haut de contenu ; latéral en anneau **avant** (i→i+1, i+2)
   pour privilégier les boucles plutôt que la pure réciprocité.
6. **Budget de liens.** `clamp(mots/180, 5, 11)` liens contextuels par article ;
   les liens existants sont décomptés (idempotent : pas de doublon de cible).

## 2. Architecture du cocon

| Niveau | Pages | Rôle |
|---|---|---|
| L0 | `/` | Accueil |
| L1 | `/agroalimentaire/`, `/fonctionnalites/`, `/negoce/`, `/comparatifs/` | Hubs mères (bento) |
| L2 | `/agroalimentaire/{métier}/`, `/fonctionnalites/{module}/` | Pages filles |
| L3 | `/blog/*` (99 articles) | Pages petites-filles |

13 clusters thématiques (`clusters.py`) : stock, coûts, traçabilité, fabrication,
facturation, traiteur, viande, maraîcher, boulanger, négoce, erp_techno,
comparatifs, intégrateur. Chaque cluster déclare ses cibles **montantes**.

## 3. État des lieux (inventaire live)

- **36 vrais orphelins** (0 lien contextuel entrant).
- 45 articles avec ≤ 1 lien contextuel sortant.
- Pages money filles **affamées** : `/agroalimentaire/boulanger/` (0), `industrie-laitiere`
  (2), `plats-cuisines-industriels` (2/1 ancre), `crm` (3), `import-export` (3),
  `maraicher` (5).
- Cannibalisation existante : « en savoir plus » → 13 cibles, « traçabilité » → 5.

## 4. Plan généré (DRY-RUN)

- **81 articles** enrichis, **~254 liens contextuels** nouveaux, **0 cannibalisation**.
- Passe 1 : montants (cocon) + latéral (anneau). Passe 2 : équilibrage des pages
  money sous le plancher de 8 ancres distinctes (par affinité de mots-clés).
- Détail + table de projection par page money : `MAILLAGE-DRY-RUN.md`.

## 5. Template CRO article (pages petites-filles)

Chaque article reçoit (`cro_tools.py`, `CRO-PLAN.md`) :

1. **Outil interactif en haut**, choisi selon la micro-intention :
   `roi` (calcul ROI), `safety_stock` (stock de sécurité + point de commande),
   `cost` (coût de revient avec freinte + prix de vente), `fefo` (méthode de
   rotation), `diagnostic` (fallback orienté parcours).
2. **Visuel HTML/CSS inter-H2** entre chaque section (rupture du mur de texte,
   aux tokens de marque).
3. **Échelle de CTA multi-niveaux** (surfeur raisonnable / Hormozi) :
   J'explore → Je compare → Je me décide → Je suis prêt
   (hub cluster → `/comparatifs/` → `/tarifs/` → `/contact/`).

Previews navigables dans `preview/<slug>.html`.

## 6. Workflow d'application (après validation)

1. `inventory.py` — rafraîchir l'inventaire (lecture seule).
2. `maillage.py` / `cro_article.py` — régénérer plans + previews.
3. **Validation** des rapports DRY-RUN.
4. Backup REST complet, puis script d'application **gaté `--live`** (à ajouter
   une fois le plan validé) qui :
   - insère les liens montants dans le **1er paragraphe** sous le H1, le latéral
     au fil des sections ;
   - injecte l'outil après l'intro, les visuels entre H2, l'échelle de CTA avant
     la FAQ ;
   - est **idempotent** (marqueurs `<!-- HH-CRO:* -->` et détection des liens
     existants).

## 7. Sécurité

- Identifiants lus en **variables d'environnement** (`WP_USER`, `WP_PASS`),
  jamais commités.
- ⚠️ **À purger** : les anciens identifiants en clair dans `fix-links.py` et
  `faq-template.py` (commités). Régénérer le mot de passe d'application concerné.
