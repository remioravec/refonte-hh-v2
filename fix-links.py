#!/usr/bin/env python3
"""
Fix broken internal links in all WordPress blog posts via REST API.
Replaces 404 URLs and homepage-redirecting URLs with correct destinations.
"""

import os
import json
import re
import sys
import urllib.request
import urllib.error
import base64
import time

# Config — credentials are read from environment variables, never hardcoded.
#   export WP_USER="administration@remi-oravec.fr"
#   export WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"   # WP Application Password
SITE = os.environ.get("WP_SITE", "https://www.helloharel.com")
USER = os.environ.get("WP_USER")
PASS = os.environ.get("WP_PASS")
if not USER or not PASS:
    raise SystemExit("Missing WP_USER / WP_PASS environment variables.")
AUTH = base64.b64encode(f"{USER}:{PASS}".encode()).decode()
DRY_RUN = "--dry-run" in sys.argv

# URL replacement map: old -> new
# All URLs are relative (without domain) for matching both relative and absolute links
REPLACEMENTS = {
    # === 404s confirmes ===
    "/demo/": "/contact/",
    "/business-plan-calculer-la-marge-commerciale-et-le-taux-de-marge/": "/blog/calcul-du-prix-moyen/",
    "/comprendre-la-tracabilite-en-agroalimentaire-methodes-et-avantages/": "/blog/erp-tracabilite-agroalimentaire/",
    "/erp-agro-alimentaire/logiciel-gestion-des-stocks-agro-alimentaire/": "/fonctionnalites/gestion-de-stock/",
    "/erp-agroalimentaire/": "/agroalimentaire/",
    "/erp-production-optimisez-vos-processus-de-fabrication/": "/fonctionnalites/fabrication/",
    "/formation/": "/contact/",
    "/gestion-de-comptabilite/": "/fonctionnalites/facturation/",
    "/gestion-de-relation-client/": "/fonctionnalites/crm/",
    "/gestion-de-stock/": "/fonctionnalites/gestion-de-stock/",
    "/gestion-stocks/": "/fonctionnalites/gestion-de-stock/",
    "/les-meilleurs-erp-de-gestion-de-stock-agroalimentaire-en-2024/": "/fonctionnalites/gestion-de-stock/",
    "/logiciel-gestion-des-stocks-agro-alimentaire/": "/fonctionnalites/gestion-de-stock/",
    "/logiciel-inventaire-guide-complet-pour-choisir-le-meilleur-en-2024/": "/blog/gestion-des-inventaires/",
    "/solutions/": "/agroalimentaire/",
    "/roi-calculator/": "/blog/roi-erp/",
    "/blog/gestion-stock-reelle": "/blog/maitriser-la-gestion-des-stocks/",
    "/blog/maitriser-numeros-lot-tracabilite": "/blog/numeros-de-lot/",
    "/blog/calcul-prix-revient-pertes": "/blog/cout-de-revient/",

    # === Redirections vers homepage (perte de jus SEO) ===
    "/erp-cloud-vs-premise/": "/blog/erp-cloud-saas-vs-on-premise/",
    "/controle-qualite-agroalimentaire-le-guide-complet-pour-les-professionnels/": "/blog/conformite-haccp/",
    "/guide-complet-sur-les-erp-system-saas-lequel-choisir/": "/blog/erp-saas-cloud/",
    "/quel-erp-choisir-pour-une-pme-industrielle/": "/blog/erp-pme/",
    "/erp-qualite-agroalimentaire/": "/blog/kpi-qualite-agroalimentaire/",
    "/erp-agro-alimentaire/production/": "/fonctionnalites/fabrication/",
    "/erp-agro-alimentaire/tracabilite/": "/blog/erp-tracabilite-agroalimentaire/",

    # === Ancien slugs -> nouveau slugs (redirections existantes mais autant pointer direct) ===
    "/erp-agro-alimentaire/": "/agroalimentaire/",
    "/fifo-fefo-lifo-tout-sur-les-strategies-de-prelevement/": "/blog/fifo-fefo-lifo/",
    "/fefo-fifo-lifo/": "/blog/fifo-fefo-lifo/",
    "/logiciel-maree-mareyeur/": "/blog/logiciel-maree-mareyeur/",
    "/comment-calculer-le-stock-de-securite/": "/blog/calcul-stock-de-securite/",
    "/comment-calculer-les-variations-de-stock-guide-complet/": "/blog/calcul-variations-de-stock/",
    "/comment-optimiser-lagencement-de-votre-entrepot/": "/blog/optimisation-entrepot/",
    "/la-tracabilite-des-produits-alimentaires-tout-savoir-sur-les-numeros-de-lot/": "/blog/numeros-de-lot/",
    "/logiciel-bon-de-commande-simple-100-en-ligne/": "/blog/bon-de-commande/",
    "/logiciel-gratuit-pour-calculer-le-prix-de-revient-en-boulangerie-et-patisserie/": "/blog/calculer-le-prix-de-revient-en-boulangerie/",
    "/maitrisez-le-calcul-du-prix-moyen-en-quelques-etapes-simples": "/blog/calcul-du-prix-moyen/",
    "/ordre-de-fabrication-of-definition-exemple-utilisation-planification/": "/blog/ordre-de-fabrication/",
    "/etiquette-de-tracabilite-de-la-viande-guide-complet/": "/blog/tracabilite-de-la-viande/",
    "/logiciel-de-tracabilite-agroalimentaire/": "/blog/numeros-de-lot/",
    "/alerte-date-peremption/": "/blog/alerte-date-peremption/",
    "/bon-de-commande-traiteur/": "/blog/bon-de-commande-traiteur/",
    "/cout-de-revient/": "/blog/cout-de-revient/",
    "/cout-marginal/": "/blog/cout-marginal/",
    "/cout-prix-au-kilo/": "/blog/cout-prix-au-kilo/",
    "/couts-de-production/": "/blog/couts-de-production/",
    "/facture-traiteur/": "/blog/facture-traiteur/",
    "/kpi-qualite-agroalimentaire/": "/blog/kpi-qualite-agroalimentaire/",
    "/plan-de-controle-alimentaire/": "/blog/plan-de-controle-alimentaire/",
    "/roi-erp/": "/blog/roi-erp/",
    "/comparatif-des-methodes-de-gestion-de-stock-agroalimentaire/": "/fonctionnalites/gestion-de-stock/",
    "/comparatif-erp-traiteur/": "/agroalimentaire/traiteur/",
    "/logiciel-de-gestion-traiteur/": "/agroalimentaire/traiteur/",
    "/logiciel-devis-traiteur/": "/agroalimentaire/traiteur/",
    "/erp-traiteur/": "/agroalimentaire/traiteur/",
    "/erp-charcutier/": "/agroalimentaire/charcutier/",
    "/erp-fruits-et-legumes/": "/agroalimentaire/maraicher/",
    "/erp-finance/": "/fonctionnalites/facturation/",
    "/erp-inventaire/": "/fonctionnalites/gestion-de-stock/",
    "/erp-production-industrielle/": "/fonctionnalites/fabrication/",
    "/pourquoir-migrer-vers-un-saas/": "/blog/erp-saas-cloud/",

    # === URLs /erp-pme/ et /erp-saas/ redirigent vers homepage ===
    "/erp-pme/": "/blog/erp-pme/",
    "/erp-saas/": "/blog/erp-saas/",
}

def api_request(endpoint, method="GET", data=None):
    """Make an authenticated WordPress REST API request."""
    url = f"{SITE}/wp-json/wp/v2/{endpoint}"
    headers = {
        "Authorization": f"Basic {AUTH}",
        "Content-Type": "application/json",
    }

    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error {e.code}: {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def fix_urls_in_content(content):
    """Replace broken URLs in content. Returns (new_content, list_of_changes)."""
    changes = []
    new_content = content

    for old_path, new_path in REPLACEMENTS.items():
        # Match both absolute and relative URLs
        # Pattern 1: href="https://www.helloharel.com/old-path"
        old_absolute = f"{SITE}{old_path}"
        new_absolute = f"{SITE}{new_path}"

        # Pattern 2: href="/old-path"
        # But be careful not to match longer paths (e.g. /erp-saas/ should not match /erp-saas-cloud/)
        # We handle this by sorting replacements by length (longest first)

        if old_absolute in new_content:
            count = new_content.count(old_absolute)
            new_content = new_content.replace(old_absolute, new_absolute)
            changes.append((old_path, new_path, count, "absolute"))

        # For relative URLs, only match in href attributes to avoid replacing in text content
        if f'href="{old_path}"' in new_content:
            count = new_content.count(f'href="{old_path}"')
            new_content = new_content.replace(f'href="{old_path}"', f'href="{new_path}"')
            changes.append((old_path, new_path, count, "relative"))

    return new_content, changes

def get_all_posts():
    """Fetch all blog posts."""
    all_posts = []
    page = 1
    while True:
        posts = api_request(f"posts?per_page=20&page={page}&_fields=id,slug&status=publish")
        if not posts or isinstance(posts, dict):
            break
        all_posts.extend(posts)
        if len(posts) < 20:
            break
        page += 1
        time.sleep(0.3)
    return all_posts

def main():
    mode = "DRY RUN" if DRY_RUN else "LIVE"
    print(f"=== Correction des liens internes ({mode}) ===\n")

    # Sort replacements by path length (longest first) to avoid partial matches
    global REPLACEMENTS
    REPLACEMENTS = dict(sorted(REPLACEMENTS.items(), key=lambda x: len(x[0]), reverse=True))

    # Get all posts
    print("Recuperation de tous les articles...")
    posts = get_all_posts()
    print(f"  {len(posts)} articles trouves\n")

    total_changes = 0
    total_posts_modified = 0
    all_changes_log = []

    for i, post in enumerate(posts):
        post_id = post["id"]
        slug = post["slug"]

        # Get full content in edit context
        full_post = api_request(f"posts/{post_id}?context=edit&_fields=id,slug,content")
        if not full_post:
            print(f"  [{i+1}/{len(posts)}] ERREUR lecture {slug}")
            continue

        raw_content = full_post.get("content", {}).get("raw", "")
        if not raw_content:
            continue

        # Fix URLs
        new_content, changes = fix_urls_in_content(raw_content)

        if changes:
            total_posts_modified += 1
            change_count = sum(c[2] for c in changes)
            total_changes += change_count

            print(f"  [{i+1}/{len(posts)}] {slug} — {change_count} lien(s) corrige(s):")
            for old, new, count, url_type in changes:
                print(f"    {old}")
                print(f"    -> {new} ({count}x, {url_type})")
                all_changes_log.append({
                    "post": slug,
                    "old": old,
                    "new": new,
                    "count": count
                })

            if not DRY_RUN:
                result = api_request(f"posts/{post_id}", method="POST", data={"content": new_content})
                if result:
                    print(f"    ✓ Sauvegarde OK")
                else:
                    print(f"    ✗ ERREUR sauvegarde!")
                time.sleep(0.5)  # Rate limiting

        # Progress indicator for unchanged posts
        if not changes and (i+1) % 10 == 0:
            print(f"  [{i+1}/{len(posts)}] ... (aucun lien a corriger)")

    # Summary
    print(f"\n{'='*50}")
    print(f"RESUME ({mode})")
    print(f"{'='*50}")
    print(f"Articles analyses  : {len(posts)}")
    print(f"Articles modifies  : {total_posts_modified}")
    print(f"Liens corriges     : {total_changes}")

    # Save log
    log_path = "/workspaces/refonte-hh-v2/fix-links-log.json"
    with open(log_path, "w") as f:
        json.dump({
            "mode": mode,
            "total_posts": len(posts),
            "posts_modified": total_posts_modified,
            "total_changes": total_changes,
            "changes": all_changes_log
        }, f, indent=2, ensure_ascii=False)
    print(f"\nLog sauvegarde: {log_path}")

if __name__ == "__main__":
    main()
