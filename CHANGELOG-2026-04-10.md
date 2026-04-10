# Changelog — 10 avril 2026

## 1. Correction des liens internes rompus (Semrush)

**19 pages corrigées, 46 liens cassés réparés via API REST WordPress.**

| Lien cassé | Correction | Pages affectées |
|---|---|---|
| `/logiciel-maree-mareyeur/` | `/blog/logiciel-maree-mareyeur/` | 12 pages (tarifs, qui-sommes-nous, fonctionnalités, écosystème...) |
| `/negoce/boissons/` | `/blog/logiciel-grossiste-boissons-cave-...` | 12 pages |
| `/fonctionnalites/gestion-de-production/` | `/fonctionnalites/fabrication/` | 7 pages agroalimentaire |
| `/fonctionnalites/tracabilite/` | `/fonctionnalites/gestion-de-stock/` | 7 pages agroalimentaire |
| `/fonctionnalites/prise-de-commande/` | `/fonctionnalites/vente/` | 7 pages agroalimentaire |
| `/agroalimentaire/laitier/` | `/agroalimentaire/industrie-laitiere/` | /agroalimentaire/ |
| `/agroalimentaire/plats-cuisines/` | `/agroalimentaire/plats-cuisines-industriels/` | /agroalimentaire/ |

Redirections 301 actives via Rank Math : `/logiciel-maree-mareyeur/`, `/agroalimentaire/plats-cuisines/`, `/fonctionnalites/tracabilite/`.

---

## 2. Refonte page /agroalimentaire/ — 7 nouveaux blocs

Tous les blocs utilisent le préfixe CSS `hh2-`, sont mobile-first, et scoped sous `#hh-page` avec `!important`.

| Bloc | Position | Détails |
|---|---|---|
| Tableau filtrable par filière | Après Bento Features | Cards filtrables par secteur (7 onglets), 28 modules |
| ROI Calculateur interactif | Avant Qui sommes-nous | 3 sliders, calcul temps réel, gain NET après abonnement |
| Encart auteur EEAT | Après vidéo YouTube | Timothy Jollivet, photo, bio, tags, Schema.org Person |
| Cas Clients carousel | Après Qui sommes-nous | 3 cards (Charcuterie, Traiteur, Fruits & Légumes) |
| Presse + Trust Badges | Après Cas clients | 4 citations presse + 5 badges confiance |
| Comparatif ERP | Après Cards métiers | 8 cards comparatif spécialisé vs généraliste |
| FAQ Accordéons | Remplace ancien FAQ cards | 8 questions (6 existantes + 2 nouvelles), Schema.org FAQPage |

### Sections supprimées
- Auto-diagnostic ERP interactif (HTML + JS)
- Bouton LinkedIn dans la card auteur Timothy

---

## 3. Audit NAP & corrections

### Mentions légales & CGU
- SARL → **SAS** (forme juridique réelle)
- Capital 1 000 € → **1 200 908 €** (registre officiel)
- Adresse standardisée : `6 avenue de Rueil, 92420 Vaucresson, France`

### Schema JSON-LD — 35 pages
- `addressCountry: "FR"` → `"France"`
- `streetAddress: "6 Avenue"` → `"6 avenue"` (minuscule)
- `legalName: "Harel Systems SAS"` ajouté/corrigé
- `email: "support@helloharel.com"` uniformisé

### Schema enrichi — 15 sous-pages
- BreadcrumbList ajouté (fil d'Ariane SERP)
- LocalBusiness ajouté (signaux NAP locaux)

### Page /contact/
- "HAREL SYSTEMS" → "Harel Systems SAS"
- Adresse normalisée

---

## 4. SEO Technique

### Meta descriptions — 21 pages
Toutes raccourcies de 169-188 chars à < 155 chars via Rank Math API.

### H1 dupliqué corrigé
- `/agroalimentaire/industrie-laitiere/` : "Maîtrisez vos marges et vos stocks en temps réel" → **"Pilotez vos flux laitiers, de la collecte à l'affinage"**

---

## Actions manuelles restantes

| Action | Où |
|---|---|
| Mettre à jour LinkedIn : adresse Vaucresson, année 2014, URL HTTPS | linkedin.com/company/harel-systems |
| Changer og:type par défaut "article" → "website" | WP Admin > Rank Math > Titres & Méta > Pages |
| Créer og:image 1200x630 par page | Design |
| Contacter verif.com, manageo.fr pour "F.L.J. Distribution" | Externe |
| Révoquer le mot de passe API | WP Admin > Profil > Mots de passe d'application |
