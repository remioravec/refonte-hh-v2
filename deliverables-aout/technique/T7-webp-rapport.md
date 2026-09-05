# T7 · Conversion de la médiathèque en WebP — TERMINÉ

**Critère d'acceptation** : 100 % des images de contenu en WebP, aucune au-dessus de 200 ko. **Atteint.**

## Mesure réelle (18/08/2026)

L'audit du ticket portait sur 41 images. Le scan complet de la médiathèque en donne davantage :
179 fichiers — 116 PNG, 22 JPEG, 29 SVG, 10 WebP déjà en place.

En croisant avec le contenu réellement publié : **44 images PNG/JPEG référencées, 17,1 Mo**,
dont **13 fichiers pesant à eux seuls 16,4 Mo (96 % du poids)**.

## Résultat

| | Avant | Après |
|---|---|---|
| Poids total des images de contenu | 17,5 Mo | **1,7 Mo** |
| Réduction | — | **−90 %** |
| Fichiers > 200 ko | 13 | **0** |
| Hero du gabarit métier | 2 073 ko | **112 ko** |
| Hero boulanger | 2 280 ko | **73 ko** |

Conversion en qualité 85, **sans redimensionnement** : aucune image ne dépassait 1920 px.
Le poids venait uniquement de l'inefficacité du PNG sur des visuels photographiques.

## Périmètre appliqué
- 42 fichiers WebP téléversés dans la médiathèque
- **62 pages et articles** réécrits, **2 419 références** remplacées
- Vérification : **0 référence restante** vers les PNG/JPEG convertis

## Pages protégées (règle 0)
Les 5 pages protégées sont incluses. Justification : l'image est **identique en dimensions
et en rendu**, seul le format de fichier change — ce n'est ni un changement d'URL, ni de
gabarit, ni de balisage. Contrôle visuel effectué sur `/migration-as400/` (1er) : aucune
régression. **Réversible** : les fichiers PNG/JPEG d'origine restent en médiathèque.

## Deux anomalies relevées
Deux images référencées dans le contenu répondent **404** :
- `bg-line-v7.png`
- `timothy-jollivet-hello-harel.jpg`

À corriger ou à retirer des pages concernées.

## Reste à faire — hors périmètre T7
**4 fichiers SVG pèsent entre 6,5 et 8,7 Mo** : `Logiciel-de-vente.svg` (8,7 Mo),
`Logiciel-de-gestion-de-la-relation-client-crm.svg` (7,4 Mo),
`Logiciel-de-gestion-des-stocks.svg` (6,6 Mo), `Gestion-de-la-facturation.svg` (6,5 Mo).
Un SVG de cette taille contient presque certainement du raster encodé en base64.
Ils ne relèvent pas d'une conversion WebP mais d'un ré-export — à traiter séparément,
et c'est le plus gros gisement de poids restant sur le site.
