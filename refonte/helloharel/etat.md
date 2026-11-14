# Refonte Hello Harel — état du dossier

Site : https://www.helloharel.com/
Dépôt : remioravec/refonte-hh-v2 · branche de travail `refonte`
Ouverture du dossier : 14/11/2026

## Cadrage

| Élément | Valeur |
|---|---|
| Plateforme de départ | WordPress · Elementor + Elementor Pro · thème Hello Elementor · JetEngine · LiteSpeed Cache (détecté) |
| Plateforme d'arrivée | Site codé : GitHub + Vercel (choix de Rémi, encore modifiable jusqu'à la validation 1) |
| Mode graphique | Sans changement graphique : la charte du site actuel est conservée (à confirmer) |
| Date visée pour la bascule | À donner |
| Accès client (éditeur, DNS, GTM en publication) | À confirmer |

## Données

| Source | Détail | État |
|---|---|---|
| Search Console | `https://www.helloharel.com/` (propriété de préfixe, propriétaire) · Composio, compte `google_search_console_vat-daven` | OK : données depuis le 03/07/2025, 12 mois complets disponibles (11/2025 → 10/2026) |
| GA4 | `properties/387997464` (www.helloharel.com) · Composio, compte `google_analytics_freeze-refont` | OK : événements clés `purchase` et `Demande de demo - Page Contact` |
| DataForSEO | Labs, France / fr | OK : 200 mots-clés positionnés, 12 en top 3, 44 en positions 4 à 10 |
| Rapprochement des URL | Search Console et site sur `https://www.helloharel.com`, barre finale | OK |
| Crawl Screaming Frog | `inventaire/internal_all.csv`, `inventaire/all_inlinks.csv` | **En attente de Rémi** (point bloquant) |
| Audit précédent | Fichiers d'avril 2026 à la racine du dépôt (maillage, 404, redirections, sauvegarde du 10/04/2026) | Plus de 3 mois : étapes 2 à 4 à refaire, sauvegarde réutilisable comme source |
| Clé Gemini | Enregistrée dans l'environnement « Remi Oravec », pas dans celui-ci | À demander à l'étape 11 |
| Taux de décote AI Overview | Aucun relevé | Requêtes marquées, clics non décotés |

## Technique relevée

| Élément | Valeur |
|---|---|
| Extension SEO | Rank Math (API `rankmath/v1`) |
| Outil de redirection | Rank Math, à confirmer par le crawl. Plan existant : `redirections-import.csv` (avril 2026), à reprendre et aplatir à l'étape 6 |
| GTM | `GTM-PWN3THCS` |
| Balise Google | `GT-T9CQF23` (posée par Site Kit), à reprendre telle quelle |
| Formulaire de contact | `#hh-contact-form`, envoi par `hh-mailer/v1`, événement `generate_lead` |
| Consentement cookies | CookieYes |
| Volumes | 72 pages et 100 articles (API REST) · sitemaps : 72 pages, 99 articles |
| Adresses techniques | `/feed/` en 200 · `/category/…` en 404 |

## Migration vers Vercel : les trois chiffres (estimation sur 12 mois Search Console)

- **Pages protégées** (top 3 sur leur requête principale, au moins un clic) : **16**, dont 10 sur la marque. Liste définitive à l'étape 5.
- **Adresses qui changeront** : **0 imposée par la plateforme.** Toutes les adresses sont gardées au caractère près (`/blog/<slug>/`, barre finale). Les changements viendront seulement des décisions de l'étape 5, des médias (`/wp-content/uploads/…`) et du flux `/feed/`.
- **Fonctions à reconstruire** : **5** : formulaire de contact avec son envoi et l'événement `generate_lead` · consentement CookieYes · avis Trustindex · listes dynamiques JetEngine · sommaires d'articles (ancres `#s-n` et `#elementor-toc__heading-anchor-n` à conserver).

## Étape en cours

0 · Contrôle de départ : bloqué sur le crawl Screaming Frog.

## Validations

| Validation | Date |
|---|---|
| 1 · Stratégie | — |
| 2 · Conception | — |
| 3 · Recette | — |
| 4 · Production | — |

## En attente de Rémi

- `internal_all.csv` et `all_inlinks.csv` dans `refonte/helloharel/inventaire/` → bloque l'étape 0.
- Confirmation du mode graphique, date visée, accès client.

## Écarts

- Taux de décote AI Overview inconnu : clics non décotés.
- Clé Gemini absente de cet environnement.
