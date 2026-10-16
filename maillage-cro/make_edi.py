#!/usr/bin/env python3
"""
Create the NEW article "EDI logiciel agroalimentaire" (cluster negoce).
- Genuinely new (cannibalization study: no dedicated EDI article exists).
- Source body authored for the SERP micro-intentions, with surfer-reasonable
  contextual OUTBOUND links to mother (/negoce/) + sister articles.
- Goes through the exact same extract()+render() template pipeline as every
  other article (interactive tool, inter-H2 visuals, FAQ cards/drawer, CTA, chrome).

Run:
  python3 make_edi.py            # DRY-RUN -> preview-tpl/edi-logiciel-agroalimentaire.html
  python3 make_edi.py --live     # create + publish the post
"""
import sys
import template as T

SLUG = "edi-logiciel-agroalimentaire"
TITLE = "EDI logiciel agroalimentaire : échange de données informatisé & connexion grande distribution"
CATEGORY = 157
AUTHOR = 2
DATE = "2026-06-01T09:00:00"

# Source body — <main class="article-content"> is the marker extract() reads.
SOURCE = """<h1>""" + TITLE + """</h1>
<main class="article-content">
<p>Travailler avec la grande distribution sans <strong>EDI</strong>, c'est ressaisir à la main des centaines de commandes, multiplier les litiges sur les bons de livraison et risquer des pénalités logistiques. L'<strong>échange de données informatisé</strong> (EDI) automatise le dialogue entre votre système et celui de vos clients GMS : commandes, avis d'expédition et factures circulent en quelques secondes, sans ressaisie. Pour un <a href="/blog/erp-grossiste-distributeur/">grossiste-distributeur</a> ou un industriel agroalimentaire, c'est devenu un prérequis pour référencer ses produits en centrale.</p>

<h2>Qu'est-ce que l'EDI en agroalimentaire ?</h2>
<p>L'EDI (Electronic Data Interchange) désigne l'échange de documents commerciaux structurés, d'ordinateur à ordinateur, dans un format normalisé — sans intervention humaine. Concrètement, la commande qu'un acheteur Carrefour, Leclerc ou Système U saisit dans son système arrive directement dans votre <a href="/blog/logiciel-grossiste-alimentaire/">logiciel de gestion grossiste</a> sous forme de message exploitable, prêt à être préparé.</p>
<p>En agroalimentaire, l'EDI couvre tout le flux : la commande (ORDERS), l'accusé de réception, l'avis d'expédition avec les lots et DLC (DESADV), puis la facture dématérialisée (INVOIC). Cette continuité est essentielle car elle relie l'EDI à la <a href="/blog/tracabilite-viande-logiciel/">traçabilité des lots</a> et au pilotage des dates de péremption.</p>

<h2>Les messages EDI incontournables pour un grossiste</h2>
<p>Un projet EDI réussi commence par cartographier les messages attendus par chaque enseigne. Voici les standards EDIFACT que tout <a href="/negoce/">ERP de négoce</a> doit savoir produire et consommer :</p>
<table>
<thead><tr><th>Message</th><th>Rôle</th><th>Sens</th></tr></thead>
<tbody>
<tr><td><strong>ORDERS</strong></td><td>Commande de l'enseigne vers le fournisseur</td><td>Entrant</td></tr>
<tr><td><strong>ORDRSP</strong></td><td>Accusé / réponse à la commande</td><td>Sortant</td></tr>
<tr><td><strong>DESADV</strong></td><td>Avis d'expédition (colis, lots, DLC, SSCC)</td><td>Sortant</td></tr>
<tr><td><strong>RECADV</strong></td><td>Accusé de réception marchandise</td><td>Entrant</td></tr>
<tr><td><strong>INVOIC</strong></td><td>Facture dématérialisée</td><td>Sortant</td></tr>
</tbody>
</table>
<p>Le DESADV est le plus structurant en frais : il transporte le SSCC (numéro de colis logistique) et les lots, ce qui permet à l'enseigne de réceptionner au scan. Côté facturation, l'INVOIC s'articule désormais avec la <a href="/blog/factur-x-e-facturation-logiciel/">facturation électronique (Factur-X)</a> imposée par la réforme.</p>

<h2>Connexion EDI avec la grande distribution (GMS)</h2>
<p>Chaque enseigne impose son cahier des charges : codes GLN (identifiant de lieu-fonction), GTIN sur les produits, plages horaires de transmission, et souvent un portail de recette à valider avant la mise en production. Une connexion EDI grande surface mal calibrée se traduit par des rejets de messages et des pénalités. Le bon réflexe : s'appuyer sur un <a href="/blog/meilleurs-erp-gestion-approvisionnements/">ERP qui industrialise les approvisionnements</a> et embarque les mappings des principales centrales.</p>
<p>On distingue deux modes de raccordement : l'EDI via un opérateur (réseau à valeur ajoutée ou plateforme cloud) et le Web-EDI, un portail web où l'on saisit/valide les messages quand les volumes sont faibles. Les grossistes en télévente combinent souvent les deux, l'EDI pour la GMS et la saisie assistée pour les petits comptes — un sujet proche de la <a href="/blog/logiciel-televente-alimentaire/">gestion de la télévente alimentaire</a>.</p>

<h2>EDI, Web-EDI ou API : quelle solution choisir ?</h2>
<p>Le choix dépend du volume de commandes et de l'exigence de vos clients. L'EDI intégré à l'ERP est imbattable au-delà de quelques dizaines de commandes par jour : zéro ressaisie, zéro litige de réception. Le Web-EDI convient au démarrage ou aux clients occasionnels. Les API temps réel, elles, montent en puissance pour les marketplaces et le e-commerce, mais ne remplacent pas l'EDIFACT exigé par la grande distribution.</p>
<p>L'erreur classique consiste à brancher un boîtier EDI isolé, déconnecté de la gestion : on automatise l'échange mais on ressaisit quand même côté stock et facturation. La valeur naît de l'intégration de bout en bout, du même socle qui gère vos <a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a>.</p>

<h2>Combien coûte la mise en place de l'EDI ?</h2>
<p>Le coût d'un projet EDI se décompose en trois postes : le raccordement à l'opérateur (abonnement mensuel + coût au message), le paramétrage des mappings par enseigne, et la recette. Un EDI natif à l'ERP réduit fortement le deuxième poste, puisque les formats sont déjà intégrés. À l'inverse, un connecteur sur mesure facturé par un intégrateur peut représenter plusieurs milliers d'euros par enseigne — un point à anticiper dans le <a href="/blog/roi-erp/">ROI de votre projet ERP</a>.</p>

<h2>Intégrer l'EDI dans un ERP agroalimentaire</h2>
<p>La vraie performance vient quand l'EDI n'est pas une brique à part mais une fonction native de l'ERP : la commande EDI crée la préparation, réserve le stock par lot, génère le DESADV avec les DLC réelles, puis l'INVOIC en conformité. C'est l'approche d'un <a href="/agroalimentaire/">ERP agroalimentaire spécialisé</a> comme Hello Harel, où l'échange de données informatisé s'inscrit dans un flux unique avec la traçabilité, les stocks et la facturation.</p>

<h2>FAQ : EDI et logiciel agroalimentaire</h2>
<div class="faq-item"><div class="faq-question">Qu'est-ce que l'échange de données informatisé (EDI) ?</div><div class="faq-answer"><p>C'est l'échange automatique de documents commerciaux (commandes, avis d'expédition, factures) entre deux systèmes informatiques, dans un format normalisé comme EDIFACT, sans ressaisie manuelle. En agroalimentaire, il relie votre ERP à celui de vos clients de la grande distribution.</p></div></div>
<div class="faq-item"><div class="faq-question">L'EDI est-il obligatoire pour vendre en grande distribution ?</div><div class="faq-answer"><p>La plupart des centrales d'achat (Carrefour, Leclerc, Système U, Intermarché, Auchan…) imposent l'EDI dans leur cahier des charges fournisseur. Sans EDI, le référencement est souvent refusé ou pénalisé. Le Web-EDI est parfois toléré pour les petits volumes au démarrage.</p></div></div>
<div class="faq-item"><div class="faq-question">Quelle est la différence entre EDI et Web-EDI ?</div><div class="faq-answer"><p>L'EDI intégré échange directement de système à système, sans intervention. Le Web-EDI est un portail web où l'on saisit et valide manuellement les messages : moins coûteux à démarrer, mais il ne supprime pas la ressaisie et ne passe pas à l'échelle.</p></div></div>
<div class="faq-item"><div class="faq-question">Le DESADV gère-t-il les lots et les DLC ?</div><div class="faq-answer"><p>Oui. L'avis d'expédition (DESADV) transporte le SSCC du colis, les numéros de lot et les DLC, ce qui permet à l'enseigne de réceptionner au scan et assure la continuité de la traçabilité réglementaire jusqu'au point de vente.</p></div></div>
<div class="faq-item"><div class="faq-question">Faut-il un ERP pour mettre en place l'EDI ?</div><div class="faq-answer"><p>Techniquement non, mais un EDI isolé oblige à ressaisir les flux dans la gestion. L'EDI natif à un ERP agroalimentaire automatise tout le cycle — commande, préparation, stock par lot, DESADV, facture — et c'est là que le retour sur investissement se joue.</p></div></div>
</main>"""


def main():
    live = "--live" in sys.argv
    data = T.extract(SOURCE)
    assert data and data["body"] and data["title"], "extraction failed"
    print(f"title={data['title'][:60]}… | h2={len(data['toc'])} | faq={len(data['faq_qa'])}")
    rendered = T.render(SLUG, data, DATE, AUTHOR)
    assert "hha-tpl" in rendered and "<h1" in rendered, "render guard failed"

    if not live:
        import os
        os.makedirs("preview-tpl", exist_ok=True)
        open(f"preview-tpl/{SLUG}.html", "w").write(rendered)
        print(f"DRY-RUN -> preview-tpl/{SLUG}.html ({len(rendered)} bytes)")
        return

    import wp_common as wp
    # Does it already exist? (idempotent)
    existing = wp.api(f"posts?slug={SLUG}&status=publish,draft&_fields=id,slug")
    if isinstance(existing, list) and existing:
        pid = existing[0]["id"]
        wp.api(f"posts/{pid}", method="POST", data={"content": rendered, "title": TITLE})
        print(f"UPDATED existing post {pid}")
    else:
        res = wp.api("posts", method="POST", data={
            "title": TITLE, "slug": SLUG, "status": "publish", "content": rendered,
            "author": AUTHOR, "categories": [CATEGORY], "template": "elementor_canvas",
            "date": DATE,
        })
        pid = res["id"]
        print(f"CREATED post {pid} -> {res.get('link')}")
    print(f"LINK: https://www.helloharel.com/blog/{SLUG}/")


if __name__ == "__main__":
    main()
