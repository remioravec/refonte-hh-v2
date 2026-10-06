# Sitemap — état & action

## Constat (audit live)
- Plugin SEO : **Rank Math** → sitemap servi sur `https://www.helloharel.com/sitemap_index.xml`
  (sous-sitemaps `post-sitemap.xml`, `page-sitemap.xml`).
- Le sitemap Rank Math est **périmé** : 88 URLs seulement, **11 articles récents absents**,
  `lastmod` figé au 23 avril 2026 (mes mises à jour du 1er juin ne sont pas reflétées).
- `/blog/logiciel-maree-mareyeur/` est dans le sitemap mais renvoie **404** (problème de
  permaliens du post 5910).

Les enregistrements via l'API REST ne déclenchent pas la régénération du cache sitemap de
Rank Math, et l'upload d'un `.xml` en médiathèque est bloqué par WordPress (type interdit).
La régénération du sitemap Rank Math nécessite donc **une action admin**.

## Sitemap complet généré (référence)
`maillage-cro/sitemap-hellohrarel.xml` — **161 URLs** (99 articles + 63 pages), **sans** l'URL
404, avec `lastmod` réels. Régénérable via :
```
python3 build_sitemap.py   # (ou le bloc dans l'historique) -> sitemap-hellohrarel.xml
```

## Action côté admin (1 étape qui règle tout)
**Réglages → Permaliens → Enregistrer les modifications.**
Cela :
1. **flush les rewrite rules** → corrige le 404 de `logiciel-maree-mareyeur`,
2. **régénère le sitemap Rank Math** → ajoute les 11 articles manquants + met à jour `lastmod`.

(Alternative : Rank Math → Réglages du sitemap → Enregistrer ; ou vider le cache Rank Math.)

## Relancer l'indexation (Google Search Console)
1. Purger le cache (WP Rocket / LiteSpeed + CDN).
2. GSC → **Sitemaps** → soumettre `https://www.helloharel.com/sitemap_index.xml`.
3. GSC → **Inspection d'URL** → demander l'indexation des pages clés
   (`/blog/`, `/agroalimentaire/`, articles vitrines).
