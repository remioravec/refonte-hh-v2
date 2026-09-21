# Allô (withallo.com) — fiche d'inspiration

- **URL** : https://www.withallo.com/fr
- **Capté le** : 2026-09-21
- **Stack** : Next.js (App Router, Turbopack) sur Vercel + Tailwind v4 (tokens `@theme`)
- **Secteur** : SaaS B2B — système téléphonique avec agents IA
- **Fichiers** : `withallo-fr-home.html` (DOM rendu complet), `withallo-fr-home.md` (version contenu propre exposée par le site)

## Pourquoi c'est retenu

Landing SaaS FR très cadrée : une seule promesse, déclinée en 9 sections qui répondent
chacune à une objection. Palette quasi monochrome vert profond + un seul accent jaune.
Et surtout un travail SEO/AEO en avance (voir plus bas) directement transposable à la refonte HH.

## Design system relevé

**Couleurs**
| Rôle | Valeur |
|---|---|
| Vert de marque (texte + fonds) | `#0b2120` |
| Vert foncé / bandeau top | `#001f1d` |
| Vert mid (dégradés) | `#005c48` |
| Vert action (CTA appel) | `#006647` → dégradé `linear-gradient(238deg,#006647 10%,#004734 90%)` |
| Accent jaune | `#ffe016` (+ `#ffeb79` / `#ffeb66` en light) |
| Neutres | `#fff` → `#fafaf8` → `#f6f5f2` (3 niveaux z0/z1/z2) |
| Crème | `#d1cebd` |
| Texte secondaire | `#546a65`, muted = vert à 75 % d'opacité |
| Succès / danger | `#00cc5f` / `#ed3821` |

Astuce : les gris sont dérivés du vert de marque par opacité (`#0b2120` + `1a/33/66/80/bf`),
pas par des gris neutres — c'est ce qui donne la cohérence chromatique de l'ensemble.

**Typo**
- Display : `ESRebondGrotesque` (Medium / Semibold)
- Corps : `ABC Normal` avec `Inter` en fallback
- Mono : JetBrains Mono
- Graisses utilisées : 300 / 400 / 500 / 600 / 700

**Formes**
- Rayon dominant **5px** (`--radius-card`, `--radius-chip`, `--radius-page`) → parti pris
  anguleux, à contre-courant des 16-24px habituels. Exceptions : bulles de chat 16px, pills 9999px.
- Conteneur max `1440px`, gouttières `20px` mobile → `32px` md → `132px` xl.

## Patterns d'interface à retenir

1. **Nav en deux étages** — bandeau `#0b1f1d` (40px, desktop only) avec une phrase de
   positionnement concurrentiel + lien avis G2, au-dessus de la nav principale (84px).
   Au scroll le bandeau part et la nav passe de transparente à blanche + `backdrop-filter: blur(12px)`
   (classe `nav-at-top` posée par un script inline avant hydratation → zéro flash).
2. **Hero** — image full-bleed préchargée (`fetchPriority="high"` + srcset 640→3840) : le LCP est traité.
3. **Onboarding en 3 temps** — « Passer à Allo, c'est simple et rapide » : numéro → équipe → règles.
   Lever le frein du changement avant même de parler fonctionnalités.
4. **Titres à double ligne** — « Un numéro sonne, / les bonnes personnes répondent ».
   Sujet + bénéfice sur deux lignes forcées, répété sur 4 cartes.
5. **Section par métier** — « Chaque équipe, chaque type d'appel », vignettes illustrées par
   industrie (`/images/industries/*.webp`, préchargées elles aussi).
6. **Bloc intégrations** — « Connecté aux outils que vous utilisez déjà ».
7. **FAQ orientée objection** — « Les questions qu'on nous pose avant de changer » : le H2 nomme
   le moment de doute au lieu du mot FAQ.
8. **CTA final court** — « Faites travailler vos appels ».

## SEO / AEO — le vrai morceau

- **JSON-LD en `@graph`** : `Organization` + `WebSite` + `SoftwareApplication` liés par `@id`,
  avec `sameAs` vers LinkedIn, G2, Capterra, TrustRadius **et Wikidata**, `founder` en `Person`
  sourcé, `contactPoint` multilingue, `offers` et `aggregateRating` (4.7 / 207 avis).
- **Version markdown de chaque page** : `<link rel="alternate" type="text/markdown" href="/fr/home.md">`
  → contenu servi en propre aux LLM. C'est exactement le pattern à reprendre pour HH.
- **`llms.txt`** déclaré en `rel="service-meta"`, + `api-catalog`, `service-doc`, `service-desc` (OpenAPI).
- **hreflang complet** : en / fr / es / de + `x-default`.
- **OG et Twitter dédiés par locale** (`og-default-fr.webp`), et un `og:title` différent du `<title>`.

## À creuser / ne pas copier tel quel

- Le rayon 5px est un choix de marque fort : à valider contre la DA HH avant de le reprendre.
- Beaucoup de tokens morts dans le CSS (palettes Tailwind + restes d'un autre design system) —
  ne pas prendre la liste des variables pour la charte réelle.
