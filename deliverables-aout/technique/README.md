# Bon de travail technique — AOÛT 2026 · Hello Harel

Client : **Hello Harel** (helloharel.com) — éditeur ERP agroalimentaire.
Agence : **SEO Monkey** (Rémi Oravec). Livrable préparé le **2026-08-15**.

Ces fichiers sont **prêts à poser**. Aucune modification n'a été appliquée au site en
production : tout a été produit en inspection **lecture seule** (REST WordPress + crawl live
+ DataForSEO France/fr). Les valeurs de balises et snippets sont à coller manuellement.

---

## ⛔ Règle 0 — Pages protégées (ne jamais toucher)

URL / gabarit / balisage **inchangés** pour :
`/agroalimentaire/` (3e, citée AI Overview) · `/agroalimentaire/traiteur/` · `/agroalimentaire/charcutier/` ·
`/agroalimentaire/plats-cuisines-industriels/` (2e) · `/migration-as400/` (1er).

**Seule exception :** réparer la description bugguée de `/migration-as400/` (réparation de
défaut, pas optimisation) — couverte par **T1**, sans changement d'URL ni de gabarit.
Aucune de ces pages n'apparaît dans le tableau de balisage T3.

> Note de contrôle : `/comparatifs/meilleur-erp-charcuterie-salaison/` et
> `/comparatifs/meilleur-erp-traiteur/` **ne sont pas** protégées (seuls les gabarits *métier*
> traiteur/charcutier le sont). Elles sont donc traitées en T3/T4/T5.

---

## Récapitulatif des 7 tickets

| Ticket | Intitulé | Répartition | Heures | Statut de livraison |
|---|---|---|---|---|
| **T1** | Réparer le générateur de meta description | REMI | 3 | ✅ Prêt à poser (snippet PHP + liste URL) |
| **T2** | Canoniser les URL à ancre (#s-*) | REMI | 4 | ✅ Prêt à poser (snippet PHP + inventaire URL) |
| **T3** | Réécrire les 60 balises | REMI | 6 | ✅ Prêt à coller (CSV, 60 lignes validées) |
| **T4** | Resynchroniser le sitemap Rank Math | REMI | 1 | ✅ Procédure prête (manip admin) |
| **T5** | Dédoublonner le JSON-LD | REMI | 3 | ⚠️ Snippet prêt + **1 désactivation manuelle** requise |
| **T6** | Alléger le gabarit métier | REMI | 6 | ✅ Checklist prête (dépend de T7 pour les images) |
| **T7** | Convertir la médiathèque en WebP | **CLIENT** | 2 | ✅ Instructions prêtes (action côté client) |

Total REMI : **23 h** · Total CLIENT : **2 h**.

---

## T1 · Réparer le générateur de meta description  — REMI · 3 h

**Cause racine (vérifiée en live).** Le contenu de chaque page affectée **commence par un bloc
`<style id="hh-ux-fix">…</style>`** (correctif CSS de gabarit injecté dans le corps). Quand
aucune description manuelle n'est saisie dans Rank Math, celui-ci **auto-génère** la description
depuis le contenu et récupère la 1re chaîne de texte — le CSS. Sortie constatée sur les 3
canaux (`meta name="description"`, `og:description`, `twitter:description`) :

```
#hh-page .timeline-grid, .timeline-grid { grid-template-columns: repeat(3, 1fr) !important; }
```

**Ampleur réelle : 70 pages** (l'audit en comptait 55 au 07/08 → le bug a continué de se
propager). Répartition mesurée le 15/08 : 6 agro (métier) · 6 négoce · 6 fonctionnalités ·
6 médical · 6 IA · 10 implantations · 2 comparatifs · 26 blog · 2 autres (`/migration-as400/`,
`/integrateurs/`). **Liste exhaustive → `T1-urls-affectees.txt`.**

**Livrable :** `snippet-T1-meta-generator.php`. Il intercepte la description finale de Rank Math
et, **uniquement si elle ressemble à du CSS** (`{`/`}`/sélecteur), la régénère depuis le contenu
nettoyé (blocs `<style>`/`<script>` retirés, shortcodes et balises supprimés, tronqué ~155 car.).
Les pages à description propre ne sont jamais modifiées.

**Prêt à poser** : Code Snippets → *Run everywhere* → activer.

**ACCEPTATION : 0 description contenant `{` ou `}` au recrawl.**

**Remédiation de fond (optionnelle, à planifier) :** sortir le bloc `<style id="hh-ux-fix">` du
corps des pages vers *Apparence → Personnaliser → CSS additionnel*. Tant que ce n'est pas fait,
le snippet garantit la propreté à chaque publication. Pour les pages à fort enjeu, T3 fournit en
plus une description manuelle définitive (à coller dans Rank Math), qui prime sur l'auto-génération.

---

## T2 · Canoniser les URL à ancre (#s-*)  — REMI · 4 h

**Constat.** 163 URL `#s-*` indexées séparément = **119 439 impressions / 19 clics / 90 j**
(≈ 80 % des impressions du site). `/blog/cout-prix-au-kilo/` en disperse 50 241 sur 5 ancres.
**Source live confirmée :** le sommaire d'article est rendu en `<nav class="hha-toc">` (dans
`<div class="hh-blog-toc">`), fait de liens de saut `<a href="#s-0">…`. **Inventaire : 565
fragments `#s-*` sur 71 pages → `T2-urls-ancres.txt`.** Il n'existe **pas** de JSON-LD `ItemList`
listant les fragments (le seul `itemListElement` est un `BreadcrumbList` propre) — le vecteur
d'indexation est bien le sommaire HTML.

**Livrable :** `snippet-T2-canonical-ancres.php`, deux leviers :
- **(A)** `rel=canonical` sans fragment, auto-référent, assertée sur chaque page single (chaque
  `#s-*` hérite du canonical de sa page mère → consolidation).
- **(B)** neutralise les liens de saut crawlables : dans le seul bloc `.hha-toc`, les
  `<a href="#s-N">` deviennent des `<a role="link" data-jump="s-N">` **sans href**, avec un JS
  minimal qui conserve le défilement doux (et n'écrit pas le `#` dans l'URL). Google n'a plus
  d'URL fragmentée à indexer. Le reste du contenu et les ancres de destination `id="s-N"` sont
  intacts.

**Prêt à poser.** Après activation : recrawl, puis (accélérateur) demander dans GSC la
*suppression temporaire* du motif `#s-` pour purger l'index plus vite.

**ACCEPTATION : plus aucune URL contenant `#` dans le rapport Pages de la Search Console à J+30.**

---

## T3 · Réécrire les 60 balises  — REMI · 6 h

**Constat.** Sur le crawl calibré (record vérifié : **972 px** sur
`/blog/edi-logiciel-agroalimentaire/**`), ~45 titles dépassent 561 px et ~80 descriptions
dépassent 985 px. Deux familles de défauts : (a) titles historiques à double suffixe
`… - Hello Harel` (gabarit `%title% %sep% %sitename%`), qui explosent la largeur ; (b) descriptions
à ~160-170 car. légèrement au-dessus de 985 px.

**Livrable :** `tableau-de-balisage-aout.csv` — **60 lignes**, triées par impressions puis par
sévérité, **pages protégées exclues**. Colonnes :
`URL | Requête cible | Ancien title | NOUVEAU title (≤561px) | NOUVELLE description (≤985px) | px title estimé | Impressions/90j`.

Règles appliquées et **auto-vérifiées (0 anomalie)** :
- **Exact match** de la requête cible présent **littéralement** dans le NOUVEAU title, placé au
  plus tôt.
- La description **reprend** la requête en variante.
- Tous les NOUVEAUX titles **≤ 561 px**, toutes les NOUVELLES descriptions **≤ 985 px**.
- Volumes DataForSEO (France, fr) ayant servi d'ancrage : `coût de revient` 3 600 · `prix au kilo`
  1 600 · `marché d'intérêt national` 480 · `prix d'achat` 390 · `erp agroalimentaire` 390 ·
  `erp pme` 320 · `coût d'achat` 320 · `erp saas` 260 · `prix moyen pondéré` 210 · `erp as400` 90.

**Où coller :** champ **Rank Math → Title** (il prime sur le gabarit — pas de `- Hello Harel`
ajouté) et **Rank Math → Description**. Le `post_title` peut rester tel quel ; c'est le champ
Rank Math Title qui pilote le `<title>` rendu. Coller la description ici la rend en plus
**définitive** (prime sur l'auto-génération), ce qui verrouille T1 sur ces 60 pages.

> Convention de style conservée : séparateur `•` et marqueur `☁️`, cohérente avec les titles déjà
> optimisés du site. Le px estimé est calculé avec un estimateur calibré sur le point dur connu
> (edi = 972 px) ; considérer ±3 % de marge.

**ACCEPTATION : tous les titles entre 200 et 561 px.**

---

## T4 · Resynchroniser le sitemap Rank Math  — REMI · 1 h

**8 pages répondent 200 mais sont absentes du sitemap** (vérifiées présentes/publiées en REST) :

```
/agroalimentaire/brasseur/
/agroalimentaire/chocolatier/
/agroalimentaire/glacier/
/agroalimentaire/torrefacteur/
/agroalimentaire/conserverie/
/fonctionnalites/tracabilite-alimentaire/
/comparatifs/meilleur-erp-charcuterie-salaison/
/comparatifs/meilleur-erp-traiteur/
```

**Procédure exacte :**
1. **WP Admin → Rank Math → Réglages du sitemap.** Vérifier que le type de contenu **Pages** est
   activé dans le sitemap, et que ces pages ne sont pas en `noindex` (Rank Math exclut du sitemap
   toute URL `noindex`) : ouvrir chacune → onglet Rank Math → *Advanced* → s'assurer
   « Index » (pas « No Index ») et que « Include in Sitemap » est coché.
2. **Purger le cache du sitemap :** Rank Math → Sitemap → cliquer sur le lien du sitemap pour le
   régénérer, ou Rank Math → *Status & Tools → Database Tools →* « **Regenerate** » /
   vider le cache. Si un cache de page global est actif (LiteSpeed/WP Rocket/host), le purger aussi.
3. **Contrôler** `https://www.helloharel.com/sitemap_index.php` → `page-sitemap.xml` : les 8 URL
   doivent y figurer.
4. **Search Console → Sitemaps :** resoumettre `sitemap_index.php` (ou le `page-sitemap.xml`).
   Puis **Inspection d'URL** sur les 8 → « Demander une indexation ».

**ACCEPTATION : les 8 URL présentes au sitemap et vues dans la Search Console.**

---

## T5 · Dédoublonner le JSON-LD  — REMI · 3 h  (⚠️ 1 action manuelle client)

**État mesuré (accueil) : 5 Organization · 3 WebSite · 2 SoftwareApplication · 2 AggregateRating**
sur 3 blocs `ld+json`. Générateurs identifiés :

- **Bloc Rank Math** (auto) — `Organization + WebSite + WebPage + SearchAction`. **Propre → à
  garder.** Source unique correcte d'Organization/WebSite.
- **Bloc A** — snippet custom `SoftwareApplication + AggregateRating (5.0/31) + Offer`, présent
  sur **toutes** les pages. **C'est lui qui affiche les étoiles** (5,0/31 du comparatif
  charcuterie). **À garder** comme unique porteur de la note.
- **Bloc B** — snippet custom `LocalBusiness` (~4 559 car.), **sur l'accueil uniquement** :
  contient le **2e AggregateRating**, un **2e SoftwareApplication**, +2 WebSite, +3 Organization.
  **C'est le coupable** de tous les doublons de l'accueil, dont le double AggregateRating qui
  risque de faire sauter les étoiles.

**Ce qu'il faut faire :**
1. **(Manuel, client/admin — ~5 min) DÉSACTIVER le Bloc B.** Le repérer dans Code Snippets /
   Elementor Custom Code / en-tête du thème via les signatures : `OpeningHoursSpecification`,
   `GeoCoordinates`, `OfferCatalog`, `Timothy Jollivet`, `Belgium`, `Mauritius`. Ne **pas**
   toucher au Bloc A ni à Rank Math. → l'accueil retombe à 1 de chaque type.
2. **Poser `snippet-T5-jsonld.php`** comme filet de sécurité : il retire automatiquement tout 2e
   `AggregateRating` résiduel du `<head>` (garde le 1er = Bloc A, celui des étoiles). Une section
   (1) commentée est fournie si un jour tu veux que ce snippet devienne l'émetteur **unique et
   versionné** de la note (après avoir désactivé A **et** B).

**JSON-LD cible par gabarit :**
- **Accueil** : Rank Math (`Organization`+`WebSite`+`WebPage`) **+** Bloc A (`SoftwareApplication`+`AggregateRating`). → 1 de chaque.
- **Métier** : Rank Math (`Breadcrumb`+`FAQPage`) **+** Bloc A (`SoftwareApplication`+`AggregateRating`) **+** LocalBusiness court NAP (sans note). → pas de doublon de note.
- **Comparatif** : idem métier — le Bloc A conserve les étoiles.

**ACCEPTATION : Rich Results Test sans avertissement de doublon sur les 3 gabarits, étoiles conservées.**

---

## T6 · Alléger le gabarit métier  — REMI · 6 h  (images = T7, client)

**Lighthouse desktop 15/08 sur `/agroalimentaire/boulanger/` :** perf **0,79** · LCP **3 536 ms** ·
poids **4,7 Mo** · TTFB **851 ms** · FCP **934 ms**. Diagnostic : **le serveur va bien**
(FCP 934 ms) — le problème est le **poids chargé après**, dominé par les images.

**Point dur n°1 identifié en live (LCP) :** un **seul PNG hero de 2,28 Mo** servi en pleine
définition :
`/wp-content/uploads/2025/10/ERP-logiciel-pour-les-grossistes-en-cremerie.png`.
À lui seul, il pèse plus que tout le reste du gabarit. **Le régler règle l'essentiel du LCP.**

**Checklist de réduction (par ordre d'impact) :**
1. **Hero LCP** — redimensionner `ERP-logiciel-...-cremerie.png` à sa taille d'affichage réelle
   (largeur max ~1200 px), le convertir en **WebP** (cible < 150 ko), et le **précharger** :
   `<link rel="preload" as="image" href="…webp" fetchpriority="high">`. **Ne pas** le lazy-loader
   (c'est le LCP) — au contraire `loading="eager"` / `fetchpriority="high"`.
2. **Toutes les autres images** (24 restantes, 22 PNG + 3 JPEG sur cette page) →
   `loading="lazy"` + `decoding="async"` pour tout ce qui est **sous la ligne de flottaison**
   (captures d'écran de fonctionnalités, logos partenaires, blocs bas de page).
3. **Servir en WebP** l'ensemble de la médiathèque → **T7** (action client). Gain attendu :
   PNG → WebP ≈ -70 % de poids.
4. **Différer le JS non critique** : passer les scripts tiers et Elementor non essentiels en
   `defer`, retirer les widgets/animations inutilisés du gabarit métier.
5. **Réduire le CSS/JS Elementor** : purger les Global Styles inutiles, activer « Improved CSS
   Loading » et « Inline Font Icons » dans Elementor → Réglages → Fonctionnalités.
6. **Fonts** : `font-display: swap` + précharger la police du titre H1 (déjà rapide au FCP,
   à surveiller seulement).
7. **Cache/CDN** : purger après conversion WebP ; vérifier que le host sert bien
   `Cache-Control` long + compression sur les images.

**ACCEPTATION : LCP sous 2 500 ms et poids sous 2 Mo sur le gabarit métier.**
La conversion WebP (T7) est le prérequis matériel de cette acceptation.

---

## T7 · Convertir la médiathèque en WebP  — **CLIENT** · 2 h

**Constat :** ~1 image sur 41 seulement est en format moderne (le reste PNG/JPEG). Sur le gabarit
métier vérifié, **22 PNG sur 25 images**.

**Les fichiers lourds à traiter EN PRIORITÉ (mesurés en live) :**
1. **`/wp-content/uploads/2025/10/ERP-logiciel-pour-les-grossistes-en-cremerie.png` — 2,28 Mo**
   (c'est le hero LCP du gabarit métier ; le convertir **et** le redimensionner à ~1200 px).
2. Les 2 PNG signalés à l'audit (**648 ko** et **619 ko**) : ce sont les originaux pleine
   définition d'illustrations de blog/gabarit. Les repérer dans *Médiathèque → trier par taille*
   et les convertir en premier.

**Instructions de conversion (au choix) :**
- **Option plugin (recommandée, sans risque)** : installer **Converter for Media** (WebP Express
  équivalent) ou **ShortPixel** / **Imagify**. Régler : format **WebP**, qualité **75-80**,
  **redimensionnement max 1600 px**, conversion **en masse** de la médiathèque existante +
  conversion **automatique** des futurs uploads. Garder les originaux (rollback possible).
- **Vérifier** ensuite qu'aucune image de contenu ne dépasse **200 ko** (critère d'acceptation)
  et que le `<picture>`/rewrite WebP est bien servi (regarder le `Content-Type: image/webp` en
  réseau).
- **Après conversion** : purger le cache (page + CDN), relancer Lighthouse sur `boulanger`,
  confirmer LCP < 2 500 ms (boucle avec T6).

**ACCEPTATION : 100 % des images de contenu en WebP, aucune au-dessus de 200 ko.**

---

## Inventaire des fichiers livrés

| Fichier | Ticket | Nature |
|---|---|---|
| `README.md` | — | Ce bon de travail |
| `snippet-T1-meta-generator.php` | T1 | PHP Code Snippets — prêt |
| `T1-urls-affectees.txt` | T1 | 70 URL affectées (groupées) |
| `snippet-T2-canonical-ancres.php` | T2 | PHP Code Snippets — prêt |
| `T2-urls-ancres.txt` | T2 | 565 fragments `#s-*` / 71 pages |
| `tableau-de-balisage-aout.csv` | T3 | 60 balises réécrites, validées |
| `snippet-T5-jsonld.php` | T5 | PHP Code Snippets — prêt (+ 1 désactivation manuelle) |

**Applied-ready (à poser tel quel par REMI) :** T1, T2, T3, T4, T6 (checklist).
**Nécessite une action côté client :** T7 (conversion WebP), et l'unique désactivation manuelle
du Bloc B pour T5.
