#!/usr/bin/env python3
"""
Batch update (audit remediation):
  A. MAILLAGE négoce — insert a contextual editorial <p> (in-prose links) into
     the négoce hub articles, pointing DOWN to the 5 orphan négoce money pages.
  B. FAQ — add a "Questions fréquentes" block (=> home-style FAQ + FAQPage
     JSON-LD) to the 15 articles that lacked any in-<main> FAQ.

Same pipeline as enrich_pricing.py: read the pristine pre-template body from
backup-live-20260529-223414/, insert before the "Aller Plus Loin" outro, then
extract()+render() (now also emits BreadcrumbList) and re-publish via REST.

Run:
  python3 batch_update.py            # DRY-RUN -> preview-tpl/<slug>.html
  python3 batch_update.py --live     # publish
"""
import sys, os, re, json, glob
import template as T
from enrich_pricing import insert_before_outro, faq_block

META = json.load(open("post_meta.json"))

# ---- A. maillage contextual paragraphs (in-<p> => counted as contextual) -----
MAILLAGE = {
    "erp-grossiste-distributeur":
        '<p>Pour un grossiste-distributeur, la performance se joue sur trois piliers métier : '
        'des <a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a> pilotés en temps réel, '
        'un circuit <a href="/negoce/ventes-devis-commandes/">ventes, devis et commandes</a> fluide, '
        'et une plateforme <a href="/negoce/">ERP de négoce</a> qui relie achats, logistique et '
        'facturation sur un socle unique.</p>',
    "logiciel-grossiste-alimentaire":
        '<p>Au quotidien, deux fonctions structurent l\'activité d\'un grossiste alimentaire : la '
        'maîtrise des <a href="/negoce/achats-approvisionnements/">achats et approvisionnements</a> '
        '(acheter au bon prix au bon moment) et la <a href="/negoce/tracabilite-lots/">traçabilité '
        'des lots</a>, indispensable en frais pour sécuriser DLC et retraits-rappels.</p>',
    "meilleurs-erp-gestion-approvisionnements":
        '<p>Au-delà du choix de l\'outil, c\'est l\'organisation des '
        '<a href="/negoce/achats-approvisionnements/">achats et approvisionnements</a> qui fait la '
        'différence : calcul des besoins, réapprovisionnement automatique et négociation des '
        'conditions fournisseurs sur un même socle de négoce.</p>',
    "logiciel-televente-alimentaire":
        '<p>La télévente s\'appuie directement sur le cœur commercial de l\'ERP : un parcours '
        '<a href="/negoce/ventes-devis-commandes/">ventes, devis et commandes</a> rapide pour le '
        'télévendeur, adossé à des <a href="/negoce/tarifs-reporting-edi/">tarifs, reporting et EDI</a> '
        'qui appliquent automatiquement les bonnes grilles par client.</p>',
    "erp-boissons":
        '<p>Distribuer des boissons impose une logistique exigeante : des '
        '<a href="/negoce/stocks-multi-depots/">stocks répartis sur plusieurs dépôts</a> et une '
        '<a href="/negoce/tracabilite-lots/">traçabilité des lots</a> sans faille, du chai jusqu\'au '
        'point de livraison.</p>',
}

# ---- B. FAQ pairs per article (topic-accurate) -------------------------------
FAQ = {
    "bon-de-commande-traiteur": [
        ("Que doit contenir un bon de commande traiteur ?",
         "Le client, la date et l'heure de livraison ou de prestation, le détail des menus et les quantités par convive, les allergènes, les prix unitaires HT/TTC, l'acompte versé et les conditions de règlement."),
        ("Bon de commande et devis traiteur, quelle différence ?",
         "Le devis est une proposition chiffrée non engageante ; le bon de commande vaut accord ferme du client et déclenche la production puis la facturation."),
    ],
    "calcul-du-cout-achat": [
        ("Comment calculer le coût d'achat ?",
         "Coût d'achat = prix d'achat HT + frais d'approche (transport, douane, manutention, assurance). C'est la valeur réelle d'entrée en stock de la marchandise."),
        ("Quelle différence entre coût d'achat et prix d'achat ?",
         "Le prix d'achat est le montant facturé par le fournisseur ; le coût d'achat y ajoute tous les frais engagés pour amener la marchandise en stock."),
    ],
    "calcul-stock-de-securite": [
        ("Quelle est la formule du stock de sécurité ?",
         "Une formule courante : (consommation max × délai max) − (consommation moyenne × délai moyen). On peut aussi le calculer via l'écart-type de la demande × coefficient de service × racine du délai."),
        ("À quoi sert le stock de sécurité ?",
         "À absorber les aléas de la demande et les retards fournisseurs pour éviter la rupture, sans tomber dans le surstock qui immobilise de la trésorerie."),
    ],
    "calcul-stock-moyen": [
        ("Comment calculer le stock moyen ?",
         "Stock moyen = (stock initial + stock final) ÷ 2. Sur une période, on fait la moyenne des stocks relevés à intervalles réguliers."),
        ("À quoi sert le stock moyen ?",
         "À calculer le taux de rotation et la couverture de stock, et à valoriser le stock immobilisé sur la période."),
    ],
    "calcul-variations-de-stock": [
        ("Comment calculer la variation de stock ?",
         "Variation = stock final − stock initial. Positive, elle traduit un stockage ; négative, un déstockage (consommation supérieure aux entrées)."),
        ("Où apparaît la variation de stock en comptabilité ?",
         "Au compte de résultat : elle ajuste les achats consommés pour refléter la consommation réelle de la période, et non les seuls achats facturés."),
    ],
    "calculer-le-prix-de-revient-en-boulangerie": [
        ("Comment calculer le prix de revient d'une baguette ?",
         "On additionne le coût des matières (farine, levure, sel, eau), l'énergie du four, la main-d'œuvre et les charges, puis on divise par le nombre de pièces, en intégrant les invendus."),
        ("Quelle marge appliquer en boulangerie ?",
         "Après le prix de revient, on applique un coefficient tenant compte des charges fixes et de la marge cible. Mieux vaut piloter le taux de marge global que le seul prix d'une pièce."),
    ],
    "contraintes-reglementations-logiciel-agroalimentaire": [
        ("Quelles réglementations un logiciel agroalimentaire doit-il couvrir ?",
         "La traçabilité (règlement CE 178/2002), la méthode HACCP, l'étiquetage INCO 1169/2011, la gestion des DLC/DDM, des lots et des procédures de retrait-rappel."),
        ("Un logiciel garantit-il la conformité sanitaire ?",
         "Il l'outille (traçabilité ascendante/descendante, enregistrements HACCP, alertes DLC) mais la conformité reste de la responsabilité de l'exploitant."),
    ],
    "erp-as400": [
        ("Pourquoi migrer d'un AS/400 vers un ERP cloud ?",
         "Pour sortir d'une technologie vieillissante et gagner en mobilité, mises à jour automatiques, sécurité et coût maîtrisé en mode OpEx (abonnement)."),
        ("Comment se passe une migration depuis l'AS/400 ?",
         "En cinq temps : audit de l'existant, reprise des données, paramétrage, phase de tests, puis bascule (go-live) progressive."),
    ],
    "facture-exacompta": [
        ("Peut-on remplacer un manifold Exacompta par un logiciel ?",
         "Oui : un logiciel de facturation reprend les mêmes mentions mais ajoute la numérotation continue, les calculs automatiques et l'archivage légal, sans ressaisie."),
        ("La facturation électronique remplace-t-elle le carnet Exacompta ?",
         "Oui. Avec la réforme, la facture électronique (Factur-X) devient obligatoire et impose un format structuré que le papier ne permet pas."),
    ],
    "facture-traiteur": [
        ("Que doit comporter une facture traiteur ?",
         "Les mentions légales (SIREN, TVA), la date de prestation, le détail des prestations et menus, les quantités, les taux de TVA applicables et l'acompte déjà déduit."),
        ("Quel taux de TVA pour un traiteur ?",
         "Selon la prestation : généralement 10 % sur la nourriture à consommer et 20 % sur les boissons alcoolisées et certaines prestations de service. À vérifier au cas par cas."),
    ],
    "maitriser-la-gestion-des-stocks": [
        ("Quels indicateurs pour bien gérer ses stocks ?",
         "Le taux de rotation, la couverture de stock, le taux de service, le taux de rupture, la valeur du stock et le taux de démarque."),
        ("Comment éviter ruptures et surstocks ?",
         "En combinant point de commande, stock de sécurité calculé et prévisions de demande, idéalement pilotés en temps réel par un ERP."),
    ],
    "numeros-de-lot": [
        ("À quoi sert un numéro de lot ?",
         "À identifier un ensemble de produits fabriqués dans les mêmes conditions, pour assurer la traçabilité et cibler précisément un retrait-rappel."),
        ("Le numéro de lot est-il obligatoire ?",
         "Oui pour les denrées alimentaires (directive 2011/91/UE), sauf exceptions : il doit permettre de remonter la chaîne de production."),
    ],
    "optimisation-entrepot": [
        ("Comment optimiser l'organisation d'un entrepôt ?",
         "Adresser les emplacements, ranger selon la rotation (méthode ABC), optimiser les circuits de picking et appliquer FIFO/FEFO pour les denrées périssables."),
        ("Qu'est-ce que la méthode ABC en entrepôt ?",
         "Classer les références selon leur rotation (A = forte, C = faible) pour placer les A près des zones d'expédition et réduire les déplacements."),
    ],
    "ordonnancement-planification": [
        ("Quelle différence entre ordonnancement et planification ?",
         "La planification définit quoi produire et quand sur un horizon moyen ; l'ordonnancement séquence précisément les ordres sur les ressources, à court terme."),
        ("Comment optimiser l'ordonnancement de production ?",
         "En tenant compte des capacités, des changements de série, des DLC et des priorités clients — ce qu'un module de planification calcule automatiquement."),
    ],
    "tracabilite-de-la-viande": [
        ("Quelles informations tracer pour la viande ?",
         "L'origine (naissance, élevage, abattage), le numéro de lot, les dates, les températures et les destinataires, conformément au règlement CE 1760/2000."),
        ("Comment assurer la traçabilité de la viande en pratique ?",
         "En enregistrant chaque lot à réception et à chaque transformation, et en reliant matières et produits finis, idéalement via un logiciel qui édite la traçabilité ascendante et descendante."),
    ],
}


def src_file(slug):
    fs = glob.glob(f"backup-live-20260529-223414/*{slug}*")
    return fs[0] if fs else None


def main():
    live = "--live" in sys.argv
    os.makedirs("preview-tpl", exist_ok=True)
    slugs = sorted(set(MAILLAGE) | set(FAQ))
    done = []
    for slug in slugs:
        f = src_file(slug)
        if not f or slug not in META:
            print(f"SKIP {slug}: no source/meta"); continue
        raw = (json.load(open(f)).get("content") or {}).get("raw", "") or ""
        addition = ""
        if slug in MAILLAGE:
            addition += MAILLAGE[slug]
        if slug in FAQ:
            addition += faq_block(FAQ[slug])
        enriched = insert_before_outro(raw, addition)
        if not enriched:
            print(f"SKIP {slug}: no <main>"); continue
        data = T.extract(enriched)
        if not data or not data["body"]:
            print(f"SKIP {slug}: extract failed"); continue
        m = META[slug]
        rendered = T.render(slug, data, m["date"], m["author"])
        assert "hha-tpl" in rendered and "BreadcrumbList" in rendered, f"{slug} guard"
        if slug in FAQ:
            assert len(data["faq_qa"]) >= 2, f"{slug} FAQ not parsed"
        tag = ("+maillage" if slug in MAILLAGE else "") + ("+faq" if slug in FAQ else "")
        print(f"{slug}: h2={len(data['toc'])} faq={len(data['faq_qa'])} {tag}")
        if live:
            import wp_common as wp
            wp.api(f"posts/{m['id']}", method="POST", data={"content": rendered})
            print(f"  WROTE {m['id']} -> /blog/{slug}/")
            done.append(slug)
        else:
            open(f"preview-tpl/{slug}.html", "w").write(rendered)
    if live:
        print("PUBLISHED:", len(done))


if __name__ == "__main__":
    main()
