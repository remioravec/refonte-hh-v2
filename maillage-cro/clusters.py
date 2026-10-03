#!/usr/bin/env python3
"""
Cocon architecture for helloharel.com.

Levels (reasonable-surfer direction):
  L0  /                                   home
  L1  mother bento hubs                    /agroalimentaire/, /fonctionnalites/, /negoce/, /comparatifs/
  L2  daughter pages                       /agroalimentaire/{metier}/, /fonctionnalites/{module}/
  L3  granddaughter blog articles          /blog/*

Direction rules encoded by the engine:
  - L3 -> L2 (its cluster's daughter) and L3 -> L1 (mother) placed HIGH in body,
    strategic anchor FIRST (first-link-counts).
  - L3 -> L3 lateral links to cluster siblings, placed lower, as a forward ring
    (article i -> i+1, i+2) to favour loops over pure reciprocity.
"""

# Each cluster: ordered "up" targets (daughter first, then mother), and the set
# of blog slugs (without /blog/) that belong to it. A post may match several
# clusters; the first match in CLUSTER_ORDER wins as primary.
CLUSTERS = {
    "stock": {
        "up": ["/fonctionnalites/gestion-de-stock/", "/agroalimentaire/"],
        "members": [
            "calcul-stock-de-securite", "calcul-stock-moyen", "calcul-variations-de-stock",
            "gestion-des-inventaires", "gestion-stock-multi-entrepots", "reapprovisionnement-stocks",
            "alerte-stock-securite", "optimisation-entrepot", "maitriser-la-gestion-des-stocks",
            "fifo-fefo-lifo", "variation-de-stock-positif-negatif",
            "gestion-automatisee-des-variations-de-stock", "enregistrement-comptable-variation-de-stock",
            "impact-de-la-variation-de-stock-sur-le-resultat-fiscal-explications-et-exemples-2025",
            "calcul-de-la-variation-de-stock-methode-cump-explications-et-exemples-2025",
        ],
    },
    "couts": {
        "up": ["/fonctionnalites/fabrication/", "/agroalimentaire/"],
        "members": [
            "cout-de-revient", "cout-marginal", "cout-prix-au-kilo", "couts-de-production",
            "calcul-du-cout-achat", "calcul-du-prix-moyen", "prix-dachat-definition",
            "difference-prix-dachat-et-prix-de-revient", "calcul-cout-de-revient-logiciel",
            "calculer-le-prix-de-revient-en-boulangerie",
        ],
    },
    "tracabilite": {
        "up": ["/agroalimentaire/", "/fonctionnalites/gestion-de-stock/"],
        "members": [
            "numeros-de-lot", "tracabilite-de-la-viande", "tracabilite-viande-logiciel",
            "tracabilite-lot-dlc-logiciel", "erp-tracabilite-agroalimentaire", "conformite-haccp",
            "plan-de-controle-alimentaire", "kpi-qualite-agroalimentaire", "dlc-ddm-dluo",
            "alerte-date-peremption", "agreage-agroalimentaire",
            "contraintes-reglementations-logiciel-agroalimentaire", "processus-agroalimentaire-guide",
            "conditionnement-alimentaire-erp",
        ],
    },
    "fabrication": {
        "up": ["/fonctionnalites/fabrication/", "/fonctionnalites/planification-production-erp/"],
        "members": [
            "ordre-de-fabrication", "ordonnancement-planification", "opc-ua",
            "gestion-decoupe-viande-logiciel", "calcul-freinte-charcuterie-logiciel",
        ],
    },
    "facturation": {
        "up": ["/fonctionnalites/facturation/", "/fonctionnalites/vente/"],
        "members": [
            "facture-exacompta", "facture-traiteur", "factur-x-e-facturation-logiciel",
            "bon-de-commande", "bon-de-livraison", "bon-de-commande-traiteur", "relance-client",
        ],
    },
    "traiteur": {
        "up": ["/agroalimentaire/traiteur/", "/agroalimentaire/"],
        "members": [
            "logiciel-calcul-cout-de-revient-traiteur", "logiciel-commande-grande-surface-traiteur",
            "logiciel-gestion-recette-multi-niveaux-traiteur", "logiciel-tracabilite-dlc-traiteur",
            "alternatives-copilote-traiteur", "cuisine-centrale",
        ],
    },
    "viande": {
        "up": ["/agroalimentaire/charcutier/", "/agroalimentaire/"],
        "members": [
            "erp-viande-volaille", "erp-decoupe-viande-poisson", "tracabilite-viande-logiciel",
        ],
    },
    "maraicher": {
        "up": ["/agroalimentaire/maraicher/", "/negoce/"],
        "members": [
            "logiciel-gestion-calibre-fruits-legumes", "logiciel-prix-du-jour-fruits-legumes",
            "meilleurs-erp-maraichers-fruits-legumes", "min",
        ],
    },
    "boulanger": {
        "up": ["/agroalimentaire/boulanger/", "/agroalimentaire/"],
        "members": ["calculer-le-prix-de-revient-en-boulangerie", "meilleurs-erp-boulangerie"],
    },
    "negoce": {
        "up": ["/negoce/", "/agroalimentaire/maraicher/"],
        "members": [
            "erp-grossiste-distributeur", "logiciel-grossiste-alimentaire",
            "logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises", "erp-boissons",
            "logiciel-maree-mareyeur", "logiciel-televente-alimentaire",
            "meilleurs-erp-gestion-approvisionnements", "edi-logiciel-agroalimentaire",
        ],
    },
    "erp_techno": {
        "up": ["/agroalimentaire/", "/fonctionnalites/"],
        "members": [
            "erp-as400", "erp-saas", "erp-saas-cloud", "erp-cloud-saas-vs-on-premise",
            "erp-pme", "erp-agroalimentaire", "migration-erp-agroalimentaire", "roi-erp",
        ],
    },
    "comparatifs": {
        "up": ["/comparatifs/", "/agroalimentaire/"],
        "members": [
            "alternative-akanea-erp", "alternative-archipelia", "alternative-cegid",
            "alternative-sage-erp", "alternative-vif-erp", "alternatives-cegid-distribution-alimentaire",
            "alternatives-divalto-agroalimentaire", "alternatives-odoo-agroalimentaire",
            "alternatives-sage-agroalimentaire", "alternatives-silog-agroalimentaire",
            "hello-harel-vs-divalto", "hello-harel-vs-odoo", "hello-harel-vs-sage",
            "hello-harel-vs-silog", "meilleurs-erp-import-export",
        ],
    },
    "integrateur": {
        "up": ["/integrateurs/", "/implantations/"],
        "members": ["integrateur-erp-paris", "integrateur-erp-lyon"],
    },
}

# Order in which clusters claim a post as PRIMARY (more specific first).
CLUSTER_ORDER = [
    "comparatifs", "integrateur", "traiteur", "viande", "maraicher", "boulanger",
    "negoce", "fabrication", "facturation", "couts", "tracabilite", "stock", "erp_techno",
]

# Mother hub each cluster ultimately rolls up to (L1).
MOTHER = {
    "stock": "/fonctionnalites/", "couts": "/fonctionnalites/", "fabrication": "/fonctionnalites/",
    "facturation": "/fonctionnalites/", "tracabilite": "/agroalimentaire/", "traiteur": "/agroalimentaire/",
    "viande": "/agroalimentaire/", "maraicher": "/agroalimentaire/", "boulanger": "/agroalimentaire/",
    "negoce": "/negoce/", "erp_techno": "/agroalimentaire/", "comparatifs": "/comparatifs/",
    "integrateur": "/integrateurs/",
}


# Demand balancing: starved money pages + the slug/title keywords that make an
# article a legitimate, contextual source of an UP link to them.
MONEY_AFFINITY = {
    "/fonctionnalites/crm/": ["relance", "televente", "télévente", "client", "commercial", "prospection"],
    "/fonctionnalites/import-export/": ["import-export", "import", "export", "international", "douane"],
    "/fonctionnalites/logistique/": ["logistique", "livraison", "expedition", "expédition", "entrepot", "entrepôt", "tournee", "tournée", "preparation-commande"],
    "/fonctionnalites/achat/": ["achat", "approvisionnement", "cout-achat", "coût-achat", "prix-dachat", "fournisseur"],
    "/fonctionnalites/vente/": ["vente", "devis", "commande", "televente", "bon-de-commande"],
    "/agroalimentaire/industrie-laitiere/": ["lait", "laitier", "laitiere", "laitière", "fromage", "collecte"],
    "/agroalimentaire/plats-cuisines-industriels/": ["plats-cuisines", "plats cuisinés", "recette", "cuisine-centrale", "cuisine centrale", "inco", "traiteur"],
    "/agroalimentaire/maraicher/": ["fruits-legumes", "fruits et légumes", "maraicher", "maraîcher", "calibre", "prix-du-jour", "grossiste"],
    "/agroalimentaire/boulanger/": ["boulang", "patiss", "pâtiss", "fournée", "fournee"],
    "/negoce/": ["negoce", "négoce", "grossiste", "distributeur", "distribution", "edi"],
    "/comparatifs/": ["alternative", "alternatives", "vs", "meilleur", "comparatif", "comparaison"],
}

# Minimum distinct contextual anchors we want each money page to reach.
MONEY_ANCHOR_FLOOR = 8


def slug_of(path):
    return path.rstrip("/").rsplit("/", 1)[-1]


def cluster_of(slug):
    """Return (primary_cluster, all_clusters) for a blog slug."""
    matches = [c for c in CLUSTER_ORDER if slug in CLUSTERS[c]["members"]]
    primary = matches[0] if matches else None
    return primary, matches
