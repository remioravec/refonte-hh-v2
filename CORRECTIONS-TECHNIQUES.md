# Corrections techniques a appliquer

## 1. Schema.org - Remplacer helloharel.fr par helloharel.com

Dans le JSON-LD de TOUTES les pages, remplacer :
```json
// AVANT
"creator": { "url": "https://helloharel.fr" }

// APRES
"creator": { "url": "https://www.helloharel.com" }
```

Localisation probable : theme WordPress > header.php ou plugin SEO (Yoast/RankMath)

---

## 2. LinkedIn - Corriger l'URL du footer

```html
<!-- AVANT -->
<a href="https://www.linkedin.com/company/26042947/admin/dashboard/">

<!-- APRES -->
<a href="https://www.linkedin.com/company/26042947/">
```

Localisation : Footer Elementor ou Customizer WordPress

---

## 3. Cookie Policy - Remplacer le placeholder #

```html
<!-- AVANT -->
<a href="#">Cookie Policy</a>

<!-- APRES -->
<a href="/politique-de-confidentialite/">Politique de cookies</a>
```

Localisation : Plugin cookie consent (probablement CookieYes ou GDPR Cookie Consent)

---

## 4. Sitemap XML - Ajouter les pages manquantes

Ajouter ces URLs dans page-sitemap.xml (via Yoast/RankMath > Sitemaps) :

```
/fonctionnalites/import-export/
/medical/
/medical/dispositifs-medicaux/
/medical/laboratoires/
/medical/materiel-dentaire/
/medical/maintien-a-domicile/
/medical/hygiene-professionnelle/
/negoce/
/negoce/achats-approvisionnements/
/negoce/ventes-devis-commandes/
/negoce/stocks-multi-depots/
/negoce/tracabilite-lots/
/negoce/tarifs-reporting-edi/
/qui-sommes-nous/
/integrateurs/
/erp-ia/
/intelligence-artificielle/
/blog/
/cgu/
/mentions-legales/
/politique-de-confidentialite/
```

**NE PAS ajouter** (404 ou a noindexer) :
- `/negoce/boissons/` (404)
- `/logiciel-maree-mareyeur/` (404)
- `/blog/category/non-classe-fr-fr/` (a noindexer)

---

## 5. Noindex - Categorie par defaut

Dans Yoast/RankMath, noindexer :
- `/blog/category/non-classe-fr-fr/`

Ou mieux : reassigner les articles de cette categorie et la supprimer.

---

## 6. Typos dans les slugs (necessite redirections)

```
/blog/integateur-erp-paris/  -->  /blog/integrateur-erp-paris/
/blog/integateur-erp-lyon/   -->  /blog/integrateur-erp-lyon/
```

Etapes :
1. Modifier le slug de chaque article dans WordPress
2. Verifier que Yoast/RankMath cree automatiquement la redirection 301
3. Si non, ajouter manuellement dans le plugin Redirection

---

## 7. Page /fonctionnalites/ - Creer un hub

Creer une page `/fonctionnalites/` qui liste tous les modules :
- CRM
- Facturation
- Vente / Gestion commerciale
- Gestion de stock
- Fabrication
- Logistique
- Achats
- Import-Export

Cette page servira de hub SEO pour distribuer le jus vers les pages fonctionnalites.

---

## 8. Breadcrumbs - Ajouter sur toutes les pages

Activer les breadcrumbs dans Yoast/RankMath :
- Format : Accueil > Blog > Titre de l'article
- Format : Accueil > Fonctionnalites > Nom du module
- Format : Accueil > Agroalimentaire > Metier

---

## 9. Section "Articles similaires" - Ajouter sur le blog

Options :
- Plugin : "Yet Another Related Posts Plugin (YARPP)" ou "Related Posts for WordPress"
- Ou : bloc Elementor "Posts" filtre par categorie

Afficher 3-4 articles lies en bas de chaque article de blog.

---

## 10. Navigation - Ajouter un fallback HTML

Le menu est 100% JS. Ajouter un `<noscript>` fallback ou un rendu cote serveur :

```html
<noscript>
  <nav>
    <a href="/">Accueil</a>
    <a href="/agroalimentaire/">Agroalimentaire</a>
    <a href="/negoce/">Negoce</a>
    <a href="/medical/">Medical</a>
    <a href="/fonctionnalites/crm/">CRM</a>
    <a href="/fonctionnalites/facturation/">Facturation</a>
    <a href="/fonctionnalites/gestion-de-stock/">Stocks</a>
    <a href="/tarifs/">Tarifs</a>
    <a href="/blog/">Blog</a>
    <a href="/contact/">Contact</a>
  </nav>
</noscript>
```

Localisation : header.php du theme ou via un plugin "Insert Headers and Footers"
