#!/usr/bin/env python3
"""
Anchor pools for internal linking, seeded from real GSC queries
(helloharel.com export, May 2026) + LSI variants.

Principles applied (ThotSEO "bible du maillage interne"):
  - Diversify anchors: aim for 11+ DISTINCT anchors toward each money page.
  - First link on a page is the one Google counts for the anchor => the pool is
    ordered by SEO priority; the engine consumes from the top.
  - Avoid cannibal anchors: a given anchor must point to ONE target only. The
    selector enforces global uniqueness across the whole plan + existing site.
  - Reuse-aware: anchors already pointing to a target (from inventory) are
    skipped so every new link grows the distinct-anchor count.
"""

# Ordered best-first. Exact-match / high-intent queries come first.
POOLS = {
    "/agroalimentaire/": [
        "ERP agroalimentaire", "logiciel ERP agroalimentaire",
        "ERP pour l'industrie agroalimentaire", "ERP PME agroalimentaire",
        "solution ERP agroalimentaire", "logiciel de gestion agroalimentaire",
        "ERP métier agroalimentaire", "ERP spécialisé agroalimentaire",
        "logiciel agroalimentaire", "ERP pour l'agroalimentaire",
        "ERP de traçabilité alimentaire", "solution de gestion pour l'agroalimentaire",
        "ERP distribution alimentaire", "logiciel de production agroalimentaire",
    ],
    "/fonctionnalites/gestion-de-stock/": [
        "logiciel de gestion de stock", "ERP gestion de stock",
        "gestion des stocks en temps réel", "module de gestion de stock",
        "suivi de stock multi-entrepôts", "logiciel de gestion des stocks",
        "optimisation des stocks alimentaires", "gestion de stock agroalimentaire",
        "pilotage des stocks", "gestion multi-dépôts",
    ],
    "/fonctionnalites/fabrication/": [
        "logiciel de fabrication", "ERP de production agroalimentaire",
        "gestion de la production", "module fabrication",
        "ordres de fabrication", "pilotage de la production agroalimentaire",
        "gestion des nomenclatures", "calcul du coût de revient en production",
        "logiciel de production alimentaire",
    ],
    "/fonctionnalites/planification-production-erp/": [
        "planification de production", "ordonnancement de la production",
        "logiciel de planification industrielle", "planifier vos fournées et ordres de fabrication",
    ],
    "/fonctionnalites/crm/": [
        "logiciel CRM agroalimentaire", "gestion de la relation client",
        "CRM pour PME agroalimentaire", "suivi client et prospection",
        "module CRM", "outil de relation client B2B",
    ],
    "/fonctionnalites/facturation/": [
        "logiciel de facturation", "facturation automatisée",
        "module de facturation", "automatiser votre facturation",
        "gestion des factures et échéances", "facturation électronique",
    ],
    "/fonctionnalites/logistique/": [
        "logiciel de logistique", "ERP logistique",
        "gestion de la logistique et des expéditions", "module logistique",
        "optimisation des tournées et expéditions", "logistique agroalimentaire",
    ],
    "/fonctionnalites/import-export/": [
        "module import-export", "logiciel import-export agroalimentaire",
        "gestion des échanges internationaux", "ERP pour l'import-export",
    ],
    "/fonctionnalites/vente/": [
        "logiciel de gestion commerciale", "module de vente et devis",
        "gestion commerciale agroalimentaire", "accélérer vos ventes et devis",
    ],
    "/fonctionnalites/achat/": [
        "logiciel de gestion des achats", "module achats et approvisionnements",
        "gestion des approvisionnements", "pilotage des achats",
    ],
    "/agroalimentaire/traiteur/": [
        "ERP traiteur", "logiciel de gestion traiteur",
        "solution traiteur", "gestion de commandes traiteur",
        "logiciel pour traiteurs et cuisines centrales",
    ],
    "/agroalimentaire/boulanger/": [
        "ERP boulangerie", "logiciel boulangerie-pâtisserie",
        "gestion boulangerie", "ERP pour artisans boulangers",
        "logiciel de gestion pour boulangerie",
    ],
    "/agroalimentaire/charcutier/": [
        "ERP charcutier", "logiciel pour charcutier-traiteur",
        "gestion de la découpe et des rendements", "ERP pour les métiers de la viande",
    ],
    "/agroalimentaire/maraicher/": [
        "ERP fruits et légumes", "logiciel pour maraîchers",
        "ERP pour grossistes en fruits et légumes", "gestion du calibre et du poids variable",
        "logiciel pour exportateurs de fruits et légumes",
    ],
    "/agroalimentaire/industrie-laitiere/": [
        "ERP industrie laitière", "logiciel pour l'industrie laitière",
        "gestion de la collecte et de la maturation", "ERP pour les produits laitiers",
    ],
    "/agroalimentaire/plats-cuisines-industriels/": [
        "ERP plats cuisinés", "logiciel pour plats cuisinés industriels",
        "gestion des recettes et conformité INCO", "ERP pour la cuisine industrielle",
    ],
    "/negoce/": [
        "ERP négoce alimentaire", "logiciel pour grossistes alimentaires",
        "ERP distribution et négoce", "logiciel de négoce alimentaire",
    ],
    "/comparatifs/": [
        "comparatif des ERP agroalimentaires", "comparer les ERP du marché",
        "meilleur ERP agroalimentaire", "guide comparatif ERP",
    ],
    "/tarifs/": [
        "tarifs Hello Harel", "découvrir nos tarifs",
        "grille tarifaire de l'ERP", "combien coûte un ERP agroalimentaire",
    ],
    "/contact/": [
        "demander une démonstration", "planifier une démo personnalisée",
        "découvrir Hello Harel en action", "échanger avec un expert ERP",
        "obtenir un devis personnalisé", "contacter notre équipe",
    ],
}


def build_selector(inventory_items):
    """Return a stateful anchor selector.

    Tracks (a) anchors already used site-wide per target (from inventory) and
    (b) a global anchor->target map to forbid cannibalization.
    """
    used_per_target = {}      # target -> set(anchor_lower)
    anchor_owner = {}         # anchor_lower -> target  (cannibalization guard)
    for x in inventory_items:
        for lk in x.get("internal_links", []):
            a = (lk.get("anchor") or "").strip().lower()
            t = lk.get("path")
            if not a:
                continue
            used_per_target.setdefault(t, set()).add(a)
            anchor_owner.setdefault(a, t)

    def pick(target):
        """Pick the best unused, non-cannibal anchor for `target`. None if pool dry."""
        used = used_per_target.setdefault(target, set())
        for cand in POOLS.get(target, []):
            cl = cand.lower()
            if cl in used:
                continue
            owner = anchor_owner.get(cl)
            if owner is not None and owner != target:
                continue  # would cannibalize another page
            used.add(cl)
            anchor_owner[cl] = target
            return cand
        return None

    return pick
