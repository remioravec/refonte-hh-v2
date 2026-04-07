# Implémentation — Refonte SEO `/agroalimentaire/`
**Date : 7 avril 2026**
**Statut : Phase 2 — Draft éditorial rédigé, en attente validation client**

---

## RÉSUMÉ DE L'AUDIT (Phase 1)

| Élément | Valeur actuelle |
|---------|----------------|
| **Éditeur** | Elementor (header/footer) + template custom PHP `#hh-page` (body) |
| **Title** | `ERP Agroalimentaire • Logiciel De Traçabilité, Production, HACCP ☁️` |
| **H1** | `Optimisez votre production, maîtrisez vos coûts, respectez vos normes` |
| **Mot-clé "ERP agroalimentaire" dans H1** | ❌ ABSENT |

### URLs vérifiées

| URL | Status |
|-----|--------|
| `/agroalimentaire/industrie-laitiere/` | ✅ 200 |
| `/agroalimentaire/laitier/` | ❌ 404 |
| `/agroalimentaire/plats-cuisines-industriels/` | ✅ 200 |
| `/agroalimentaire/plats-cuisines/` | ❌ 404 |

### Dates contradictoires trouvées

| Emplacement | Date |
|------------|------|
| Header/footer (x38) | "Depuis 2014" |
| Bloc diagnostic | "depuis 2007" + stat card "2007" |
| FAQ (Q1, Q4, Q5) | "depuis plus de 30 ans" |

**Date confirmée par le client : 2014**

---

## CORRECTIONS CRITIQUES (Phase 3)

### 1. Harmonisation des dates → "Depuis 2014" partout

#### 1a. Bloc diagnostic (ligne ~2745)
```html
<!-- AVANT -->
<p class="diag-footer-text">Ce diagnostic reflète les problématiques que nous rencontrons quotidiennement depuis 2007 auprès de <strong>+600 entreprises agroalimentaires</strong> accompagnées.</p>

<!-- APRÈS -->
<p class="diag-footer-text">Ce diagnostic reflète les problématiques que nous rencontrons quotidiennement depuis 2014 auprès de <strong>+200 entreprises agroalimentaires</strong> accompagnées.</p>
```

#### 1b. Stat card "2007" (ligne ~2748 environ)
```html
<!-- AVANT -->
<div class="about-stat-card"><span class="stat-number">2007</span><span class="stat-label">Depuis</span></div>

<!-- APRÈS -->
<div class="about-stat-card"><span class="stat-number">2014</span><span class="stat-label">Depuis</span></div>
```

#### 1c. FAQ — Remplacer "depuis plus de 30 ans" par "depuis 2014"

**FAQ Q1** (Qu'est-ce qu'un ERP agroalimentaire ?) :
```
AVANT : "Hello Harel est un ERP agroalimentaire français, édité depuis plus de 30 ans"
APRÈS : "Hello Harel est un ERP agroalimentaire français, édité depuis 2014"
```

**FAQ Q4** (ROI moyen) :
```
AVANT : "Les données recueillies auprès de nos clients Hello Harel sur plus de 30 ans"
APRÈS : "Les données recueillies auprès de nos clients Hello Harel sur plus de 10 ans"
```

**FAQ Q5** (Déploiement) :
```
AVANT : "une méthodologie éprouvée, rodée sur plus de 30 ans"
APRÈS : "une méthodologie éprouvée, rodée sur plus de 10 ans"
```

**FAQ Q5 charcutier** (dans faq-agroalimentaire.json) :
```
AVANT : "conçu depuis plus de 30 ans pour les métiers de bouche"
APRÈS : "conçu depuis 2014 pour les métiers de bouche"
```

**FAQ Q6 charcutier** :
```
AVANT : "depuis trois décennies"
APRÈS : "depuis 2014"
```

**FAQ Q1 maraîcher** :
```
AVANT : "le fruit de plus de 30 ans de collaboration"
APRÈS : "le fruit de plus de 10 ans de collaboration"
```

⚠️ **Note** : Il faut aussi corriger dans le Schema.org JSON-LD qui reprend les mêmes textes FAQ.

---

### 2. Liens cassés — Slugs incorrects

#### 2a. Dans la FAQ Q1 (ligne ~3136)

```html
<!-- AVANT -->
<a href="/agroalimentaire/laitier/" style="color:#00B1F5;font-weight:600;text-decoration:underline;">industrie laitière</a>
<a href="/agroalimentaire/plats-cuisines/" style="color:#00B1F5;font-weight:600;text-decoration:underline;">plats cuisinés</a>

<!-- APRÈS -->
<a href="/agroalimentaire/industrie-laitiere/" style="color:#00B1F5;font-weight:600;text-decoration:underline;">industrie laitière</a>
<a href="/agroalimentaire/plats-cuisines-industriels/" style="color:#00B1F5;font-weight:600;text-decoration:underline;">plats cuisinés</a>
```

#### 2b. Dans la FAQ Q2 (vérifier si les mêmes liens apparaissent)

Chercher toute occurrence de `/agroalimentaire/laitier/` et `/agroalimentaire/plats-cuisines/` et remplacer.

---

### 3. Liens auto-référencés → Remplacer par des vraies cibles

#### 3a. Card "Gestion des lots et traçabilité" (bento grid, ligne ~3136 environ)
```html
<!-- AVANT -->
<a href="/agroalimentaire/" class="card-link">Découvrir l'ERP agroalimentaire →</a>

<!-- APRÈS -->
<a href="/fonctionnalites/tracabilite/" class="card-link">Voir le module de traçabilité ascendante →</a>
```

#### 3b. Card "Grossiste" dans le carousel métiers (ligne ~2992)
```html
<!-- AVANT -->
<a href="/agroalimentaire/" class="metier-slide scroll-reveal">
    ...
    <h3>Grossiste</h3>
    <p>Volumes importants, marges serrées, télévente ultra-rapide.</p>
    <span class="card-link">Logiciel grossiste alimentaire →</span>
</a>

<!-- APRÈS : SUPPRIMER ce bloc (doublon, voir point 4) -->
```

#### 3c. Card "Grossiste alimentaire" (ligne ~3016)
```html
<!-- AVANT -->
<a href="/agroalimentaire/" class="metier-slide scroll-reveal">
    ...
    <h3>Grossiste alimentaire</h3>
    <p>Volumes importants, marges serrees, televente et gestion multi-depots.</p>
    <span class="card-link">Decouvrir →</span>
</a>

<!-- APRÈS : Garder ce bloc, corriger le lien, les accents et l'ancre -->
<a href="/agroalimentaire/maraicher/" class="metier-slide scroll-reveal">
    ...
    <h3>Grossiste alimentaire</h3>
    <p>Volumes importants, marges serrées, télévente et gestion multi-dépôts.</p>
    <span class="card-link">Logiciel grossiste alimentaire →</span>
</a>
```

> **Note** : Il n'existe pas de page `/agroalimentaire/grossiste/`. La page la plus pertinente est `/agroalimentaire/maraicher/` (qui couvre les grossistes en fruits et légumes). **À valider avec le client** : faut-il créer une page dédiée grossiste ou pointer vers maraîcher ?

---

### 4. Suppression du doublon "Grossiste"

**Action** : Supprimer le bloc `<a href="/agroalimentaire/" class="metier-slide">` contenant `<h3>Grossiste</h3>` (ligne ~2992-2997).

Garder uniquement le bloc "Grossiste alimentaire" corrigé (voir point 3c).

La section "Nos secteurs d'expertise" passe de 8 à 7 cards :
1. Mareyeur → `/blog/logiciel-maree-mareyeur/`
2. Boulangerie → `/agroalimentaire/boulanger/`
3. ~~Grossiste~~ → SUPPRIMÉ
4. Traiteur / Plats cuisinés → `/agroalimentaire/plats-cuisines-industriels/`
5. Fruits & Légumes → `/agroalimentaire/maraicher/`
6. Charcutier → `/agroalimentaire/charcutier/`
7. Grossiste alimentaire → `/agroalimentaire/maraicher/` (corrigé)
8. Laitiers → `/agroalimentaire/industrie-laitiere/`

---

### 5. Erreurs d'encodage — Accents manquants

| Ligne | Avant | Après |
|-------|-------|-------|
| H2 FAQ (~3065) | `Les reponses a vos questions` | `Les réponses à vos questions` |
| Sous-titre FAQ (~3067) | `Tout savoir sur l'ERP specialise pour l'agroalimentaire.` | `Tout savoir sur l'ERP spécialisé pour l'agroalimentaire.` |
| Meta description | `...acteurs specialises.` | `...acteurs spécialisés.` |
| Card Grossiste alimentaire | `marges serrees, televente et gestion multi-depots` | `marges serrées, télévente et gestion multi-dépôts` |
| Card Grossiste alimentaire | `Decouvrir →` | `Découvrir →` |

---

### 6. Bug FAQ — Fragments parasites dans `faq-card-meta`

Les `<span class="faq-card-meta">` affichent des mots-clés fragmentés extraits des titres.

**Fragments actuels** :
```
Qu'est-ce, qu'un, agroalimentaire
Pourquoi, spécialisé, plutôt
Quels, métiers, l'agroalimentaire
Comment, l'ERP, assure
moyen, agroalimentaire
Comment, passe, déploiement
```

**Cause** : Le code prend le titre de la question, le split sur les espaces, et extrait certains mots comme "tags". Mais les apostrophes et la ponctuation cassent le parsing.

**Solution A** (recommandée) : Remplacer les fragments par des vrais tags métier pertinents pour le SEO :

```html
<!-- Q1 -->
<span class="faq-card-meta">ERP, agroalimentaire, définition</span>

<!-- Q2 -->
<span class="faq-card-meta">ERP spécialisé, ERP généraliste, comparatif</span>

<!-- Q3 -->
<span class="faq-card-meta">métiers, filières, couverture</span>

<!-- Q4 -->
<span class="faq-card-meta">HACCP, INCO, conformité réglementaire</span>

<!-- Q5 -->
<span class="faq-card-meta">ROI, retour sur investissement, gains</span>

<!-- Q6 -->
<span class="faq-card-meta">déploiement, accompagnement, planning</span>
```

**Solution B** : Masquer les `faq-card-meta` en CSS (`display: none`) si les tags ne sont pas utiles visuellement.

**Solution C** : Corriger le JS qui génère ces fragments (si généré dynamiquement).

---

## OPTIMISATIONS SEO (Phase 4)

### 7. Nouveau H1 — VALIDÉ

```html
<!-- AVANT -->
<h1 class="hero-title" style="color:#fff">Optimisez votre production, <span class="accent" style="color:#00B4FC">maîtrisez vos coûts, respectez vos normes</span></h1>

<!-- APRÈS -->
<h1 class="hero-title" style="color:#fff">L'ERP agroalimentaire conçu pour les PME : <span class="accent" style="color:#00B4FC">traçabilité, HACCP et marges sous contrôle</span></h1>
```

---

### 8. Bloc éditorial (~800 mots) — Structure proposée

**EMPLACEMENT** : Après `</section><!-- fin .metiers-section -->` et avant `<section class="team-section">` (entre les lignes ~3033 et ~3035).

#### Structure HTML proposée :

```html
<section class="editorial-section">
  <div class="container">

    <h2>Pourquoi un ERP spécialisé est indispensable dans l'agroalimentaire</h2>

    <h3>La traçabilité alimentaire : une obligation réglementaire, un avantage concurrentiel</h3>
    <p>~150-200 mots — Traçabilité ascendante/descendante, CE 178/2002, plan de rappel, FEFO/FIFO, équilibrage matière, agréage.</p>
    <p><a href="/fonctionnalites/tracabilite/">Découvrir le module de traçabilité Hello Harel</a></p>

    <h3>Gestion de production et calcul du coût de revient réel</h3>
    <p>~150-200 mots — Nomenclatures multi-niveaux, rendements de cuisson, freintes, poids variable, CCP, ordonnancement.</p>
    <p><a href="/fonctionnalites/fabrication/">Explorer le module de fabrication et production</a></p>

    <h3>Conformité réglementaire : HACCP, INCO, allergènes et au-delà</h3>
    <p>~150-200 mots — IFS, BRC, ISO 22000, ANSES, CIQUAL, Nutri-Score, allergènes majeurs, EGALIM, DLC/DDM/DLUO, chaîne du froid.</p>

    <h3>Gestion des stocks et logistique sous contrainte agroalimentaire</h3>
    <p>~150-200 mots — FEFO, DLC/DDM, poids variable, chaîne du froid, multi-dépôts.</p>
    <p><a href="/fonctionnalites/gestion-de-stock/">Optimiser la gestion de vos stocks alimentaires</a></p>

    <h3>Pourquoi les PME agroalimentaires choisissent un ERP spécialisé plutôt qu'un généraliste</h3>
    <p>~150-200 mots — Couverture fonctionnelle immédiate, déploiement rapide, ROI, comparaison avec ERP généraliste.</p>
    <p><a href="/blog/meilleurs-erp-agroalimentaire-2026/">Lire notre comparatif : Meilleur ERP agroalimentaire 2026</a></p>

  </div>
</section>
```

**Vocabulaire LSI intégré** : FEFO, FIFO, traçabilité ascendante, traçabilité descendante, plan de rappel, équilibrage matière, agréage, allergènes majeurs, INCO, Nutri-Score, CIQUAL, ANSES, EGALIM, IFS, BRC, ISO 22000, CE 178/2002, DLC, DDM, DLUO, CCP, nomenclatures multi-niveaux, rendements de cuisson, freintes, poids variable, chaîne du froid.

**Liens internes** (4) :
1. `/fonctionnalites/tracabilite/` — "Découvrir le module de traçabilité Hello Harel"
2. `/fonctionnalites/fabrication/` — "Explorer le module de fabrication et production"
3. `/fonctionnalites/gestion-de-stock/` — "Optimiser la gestion de vos stocks alimentaires"
4. `/blog/meilleurs-erp-agroalimentaire-2026/` — "Lire notre comparatif : Meilleur ERP agroalimentaire 2026"

> ✅ **Draft rédigé** : voir `bloc-editorial-agroalimentaire.html` (~850 mots de contenu texte, hors balises). Inspiré de l'analyse SERP concurrentielle (VIF, Infologic, Akanea, Difagro, articles Agro-Media et Ellipson). Exploite les gaps identifiés : "piège Excel", cahiers des charges GMS, audit-readiness, volatilité matières premières, comparaison concrète généraliste vs spécialisé.

---

### 9. Remplacement "En savoir plus" par des ancres descriptives

| Ancre actuelle | Cible | Nouvelle ancre |
|---------------|-------|----------------|
| "En savoir plus →" | `/fonctionnalites/gestion-de-stock/` (card DLC/DLUO) | "Gérer vos DLC et stocks alimentaires →" |
| "En savoir plus →" | `/fonctionnalites/fabrication/` (card coût de revient) | "Calculer vos coûts de revient en production →" |
| "En savoir plus →" | `/fonctionnalites/gestion-de-stock/` (card stocks sensibles) | "Piloter vos stocks sensibles →" |
| "En savoir plus →" | `/qui-sommes-nous/` | "Découvrir l'équipe Hello Harel →" |

---

### 10. Embed vidéo YouTube (lite-youtube-embed)

Remplacer le lien externe par un embed léger :

```html
<!-- AVANT (chaque card avec lien YouTube) -->
<a href="https://www.youtube.com/watch?v=pANFAv6-sJk" class="card-link" target="_blank" rel="noopener">Regarder la vidéo</a>

<!-- APRÈS (une seule section vidéo, après le hero ou dans la section "Hello Harel, l'ERP pensé...") -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lite-youtube-embed@0.3.2/src/lite-yt-embed.min.css">
<script src="https://cdn.jsdelivr.net/npm/lite-youtube-embed@0.3.2/src/lite-yt-embed.min.js" defer></script>

<lite-youtube videoid="pANFAv6-sJk" playlabel="Découvrir Hello Harel en vidéo" style="max-width:720px;margin:2rem auto;border-radius:12px;overflow:hidden;">
  <a href="https://www.youtube.com/watch?v=pANFAv6-sJk" class="lty-playbtn" title="Regarder la vidéo">
    <span class="lyt-visually-hidden">Regarder la vidéo de présentation Hello Harel</span>
  </a>
</lite-youtube>
```

**Note** : Les liens "Regarder la vidéo" dans les cards bento peuvent être conservés ou remplacés par des liens vers la section vidéo intégrée (ancre `#video`).

---

## CHECKLIST POST-DÉPLOIEMENT

- [ ] Vider le cache WordPress (WP Rocket / LiteSpeed / autre)
- [ ] Vider le cache CDN (Cloudflare / autre)
- [ ] Vérifier le rendu mobile des modifications (H1, bloc éditorial, cards métiers)
- [ ] Soumettre `/agroalimentaire/` dans Google Search Console (Inspection d'URL > Demander l'indexation)
- [ ] Vérifier que les 404 `/agroalimentaire/laitier/` et `/agroalimentaire/plats-cuisines/` ne sont plus liées
- [ ] Tester les 6 FAQ drawer en cliquant chaque question
- [ ] Vérifier le Schema.org JSON-LD (dates, FAQ text) via Rich Results Test
- [ ] Vérifier Core Web Vitals après ajout lite-youtube-embed

## MONITORING 30 JOURS (KPIs GSC)

| KPI | Baseline à noter J0 | Objectif J+30 |
|-----|---------------------|---------------|
| Position moyenne "ERP agroalimentaire" | Relever J0 | Top 5 |
| Impressions /agroalimentaire/ | Relever J0 | +20% |
| CTR /agroalimentaire/ | Relever J0 | +15% (grâce au title optimisé) |
| Pages indexées (couverture) | Relever J0 | 0 erreur 404 interne |
| Nombre de liens internes vers /agroalimentaire/ | Relever J0 | +10 liens contextuels |
| Position "logiciel agroalimentaire" | Relever J0 | Apparition top 20 |
| Position "ERP traçabilité agroalimentaire" | Relever J0 | Apparition top 20 |
