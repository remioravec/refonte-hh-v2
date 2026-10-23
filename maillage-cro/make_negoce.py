#!/usr/bin/env python3
"""
Create 3 NEW négoce articles (cannibalization-checked, no existing duplicates).
Each links DOWN to the orphan négoce money pages (audit remediation) and through
the standard extract()+render() pipeline (tool, breadcrumb, FAQ + FAQPage, CTA).

Run:
  python3 make_negoce.py            # DRY-RUN -> preview-tpl/<slug>.html
  python3 make_negoce.py --live     # create + publish (idempotent)
"""
import sys
import template as T

CATEGORY = 157          # négoce cluster (same as edi-logiciel-agroalimentaire)
AUTHOR = 2
DATE = "2026-06-19T09:00:00"

ARTICLES = [
{
 "slug": "penalites-logistiques-gms",
 "title": "Pénalités logistiques GMS : causes, calcul et prévention pour les fournisseurs",
 "source": """<h1>Pénalités logistiques GMS : causes, calcul et prévention pour les fournisseurs</h1>
<main class="article-content">
<p>Livrer la grande distribution, c'est accepter un cahier des charges logistique exigeant — et des <strong>pénalités</strong> dès le moindre écart. Retard de livraison, taux de service insuffisant, palette non conforme : chaque manquement se traduit par une refacturation qui ampute directement la marge. Pour un <a href="/blog/erp-grossiste-distributeur/">grossiste-distributeur</a> ou un industriel, comprendre comment naissent et se calculent ces pénalités est la première étape pour les faire disparaître.</p>

<h2>Qu'est-ce qu'une pénalité logistique en grande distribution ?</h2>
<p>Une pénalité logistique est une somme facturée par une enseigne (Carrefour, Leclerc, Système U, Intermarché, Auchan…) à son fournisseur lorsque la livraison ne respecte pas les conditions contractuelles : date, quantité, qualité de la préparation ou des documents. Elle est prévue dans la convention fournisseur et appliquée automatiquement par la centrale, souvent sans discussion préalable.</p>
<p>Le principe est simple : l'enseigne calibre ses linéaires et ses entrepôts au plus juste. Une commande qui arrive en retard ou incomplète désorganise toute la chaîne aval, d'où une compensation financière exigée du fournisseur.</p>

<h2>Les principales causes de pénalités</h2>
<p>Trois familles concentrent l'essentiel des pénalités :</p>
<table>
<thead><tr><th>Cause</th><th>Exemple</th></tr></thead>
<tbody>
<tr><td><strong>Taux de service insuffisant</strong></td><td>quantités livrées inférieures à la commande (rupture, casse)</td></tr>
<tr><td><strong>Retard ou avance de livraison</strong></td><td>créneau de rendez-vous entrepôt non respecté</td></tr>
<tr><td><strong>Non-conformité</strong></td><td>palette mal filmée, étiquette logistique (SSCC) absente, DLC trop courte, erreur de DESADV</td></tr>
</tbody>
</table>
<p>La plupart de ces causes remontent à un même problème de fond : un stock mal piloté et des informations dispersées. Un suivi des <a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a> en temps réel évite la promesse de quantités indisponibles, première source de mauvais taux de service.</p>

<h2>Comment sont calculées les pénalités logistiques ?</h2>
<p>Le calcul varie selon les enseignes, mais repose presque toujours sur une base forfaitaire ou proportionnelle. On retrouve fréquemment :</p>
<p><strong>Pénalité = montant forfaitaire par anomalie + pourcentage de la valeur des marchandises concernées.</strong> Par exemple, un retard peut coûter un forfait de traitement administratif (quelques dizaines d'euros) auquel s'ajoute un pourcentage (souvent 5 à 15 %) de la valeur de la commande livrée hors créneau. Un taux de service de 95 % au lieu des 98,5 % exigés déclenche, lui, une pénalité proportionnelle au manquant.</p>
<p>Ces montants, pris isolément, semblent modestes ; cumulés sur des centaines de commandes, ils pèsent lourd dans le <a href="/blog/roi-erp/">ROI d'un projet ERP</a> et justifient à eux seuls d'industrialiser la préparation.</p>

<h2>Prévenir les pénalités : les bons réflexes</h2>
<p>La prévention se joue à chaque étape de la commande à la livraison :</p>
<p>1. <strong>Fiabiliser la promesse de commande</strong> grâce à un stock juste et à un parcours <a href="/negoce/ventes-devis-commandes/">ventes, devis et commandes</a> qui bloque ce qui n'est pas disponible. 2. <strong>Respecter les créneaux</strong> en planifiant les tournées et les rendez-vous entrepôt. 3. <strong>Sécuriser la conformité</strong> : étiquette SSCC, DESADV juste, DLC suffisante, palette homogène. 4. <strong>Mesurer son propre taux de service</strong> pour corriger avant que l'enseigne ne le fasse.</p>

<h2>Le rôle de l'ERP et de l'EDI dans la maîtrise des pénalités</h2>
<p>La meilleure arme contre les pénalités est l'intégration de bout en bout. Quand la commande arrive en <a href="/blog/edi-logiciel-agroalimentaire/">EDI</a> et crée directement la préparation, réserve le stock par lot et génère un avis d'expédition conforme, le risque d'erreur humaine s'effondre. Un <a href="/negoce/">ERP de négoce</a> spécialisé pilote la logistique, la traçabilité et la facturation sur un même socle : il alerte sur les ruptures avant la livraison, applique les bons formats EDI par enseigne et fournit le taux de service réel, enseigne par enseigne.</p>

<h2>FAQ : pénalités logistiques GMS</h2>
<div class="faq-item"><div class="faq-question">Qu'est-ce qu'une pénalité logistique GMS ?</div><div class="faq-answer"><p>C'est une somme facturée par une enseigne de grande distribution à son fournisseur quand la livraison ne respecte pas les conditions prévues (date, quantité, conformité). Elle est définie dans la convention fournisseur et appliquée automatiquement par la centrale.</p></div></div>
<div class="faq-item"><div class="faq-question">Comment se calcule une pénalité logistique ?</div><div class="faq-answer"><p>Le plus souvent par un montant forfaitaire par anomalie auquel s'ajoute un pourcentage de la valeur des marchandises concernées (fréquemment 5 à 15 %). Un taux de service inférieur au seuil exigé déclenche une pénalité proportionnelle au manquant.</p></div></div>
<div class="faq-item"><div class="faq-question">Comment éviter les pénalités de la grande distribution ?</div><div class="faq-answer"><p>En fiabilisant le stock et la promesse de commande, en respectant les créneaux de livraison, en sécurisant la conformité logistique (SSCC, DESADV, DLC) et en mesurant son taux de service. L'EDI et un ERP de négoce intégré automatisent ces contrôles.</p></div></div>
<div class="faq-item"><div class="faq-question">L'EDI réduit-il les pénalités ?</div><div class="faq-answer"><p>Oui : en supprimant la ressaisie et en générant des messages conformes (commande, avis d'expédition, facture), l'EDI réduit fortement les erreurs de quantité et de documents, deux causes majeures de pénalités.</p></div></div>
</main>""",
},
{
 "slug": "grille-tarifaire-negoce-alimentaire",
 "title": "Grille tarifaire en négoce alimentaire : conditions clients, remises et tarifs",
 "source": """<h1>Grille tarifaire en négoce alimentaire : conditions clients, remises et tarifs</h1>
<main class="article-content">
<p>En négoce alimentaire, le même produit ne se vend presque jamais au même prix à tous les clients. Restaurateurs, collectivités, GMS, détaillants : chacun a sa <strong>grille tarifaire</strong>, ses remises et ses conditions. Bien construire et bien appliquer ces tarifs, c'est protéger sa marge et éviter les litiges de facturation. Voici comment structurer ses conditions commerciales et les fiabiliser.</p>

<h2>Qu'est-ce qu'une grille tarifaire en négoce alimentaire ?</h2>
<p>Une grille tarifaire est l'ensemble des prix de vente d'un catalogue, déclinés selon des critères commerciaux : catégorie de client, volume, canal, zone géographique ou saison. C'est le référentiel qui détermine, pour chaque ligne de <a href="/negoce/ventes-devis-commandes/">devis ou de commande</a>, le bon prix à appliquer — automatiquement, idéalement.</p>
<p>En agroalimentaire, la grille doit aussi composer avec le prix du marché (produits frais à cours variable), ce qui impose des tarifs faciles à réviser et historisés.</p>

<h2>Tarifs par client et par volume : structurer ses conditions</h2>
<p>Une grille efficace combine plusieurs niveaux. Le <strong>tarif de base</strong> (prix catalogue) sert de référence. On y greffe des <strong>tarifs par catégorie de client</strong> (CHR, GMS, collectivités), puis des <strong>paliers de volume</strong> (dégressifs par quantité commandée). Un grossiste qui maîtrise sa <a href="/blog/logiciel-grossiste-alimentaire/">gestion commerciale</a> sait à tout moment quelle marge il dégage sur chaque client et chaque référence.</p>

<h2>Remises, ristournes et conditions particulières</h2>
<p>Au-delà des tarifs, les conditions commerciales incluent les remises sur facture (immédiates), les ristournes de fin de période (calculées sur le chiffre d'affaires réalisé), les conditions de paiement et les promotions ponctuelles. Le risque : que ces avantages, négociés par le commercial, soient mal reportés en facturation. C'est l'une des premières causes d'écart de marge et de <a href="/blog/relance-client/">litiges clients</a>.</p>

<h2>Automatiser l'application des tarifs</h2>
<p>La grille la plus fine ne vaut rien si elle est appliquée à la main. L'enjeu est que chaque commande récupère <strong>automatiquement</strong> le bon prix selon le client et le volume, calcule la marge en temps réel et bloque les ventes à perte. C'est exactement ce qu'apporte un <a href="/negoce/">ERP de négoce</a> : le tarif juste, sans ressaisie, du devis à la facture, en cohérence avec le calcul du <a href="/blog/calcul-du-prix-moyen/">prix moyen pondéré</a> de vos stocks.</p>

<h2>Grille tarifaire, reporting et EDI : un même socle</h2>
<p>Les grilles tarifaires alimentent directement deux autres briques. Le <a href="/negoce/tarifs-reporting-edi/">reporting et l'EDI</a> : côté reporting, l'analyse des marges par client/produit s'appuie sur les tarifs réellement appliqués ; côté <a href="/blog/edi-logiciel-agroalimentaire/">EDI</a>, les prix transmis aux centrales doivent correspondre exactement aux conditions négociées, sous peine de rejets et de litiges. Centraliser tarifs, ventes et facturation sur un seul système supprime ces écarts.</p>

<h2>FAQ : grille tarifaire en négoce alimentaire</h2>
<div class="faq-item"><div class="faq-question">Comment construire une grille tarifaire en négoce alimentaire ?</div><div class="faq-answer"><p>On part d'un tarif catalogue de référence, puis on décline par catégorie de client (CHR, GMS, collectivités), par paliers de volume et, si besoin, par zone ou saison. La grille doit rester facile à réviser pour suivre le cours des produits frais.</p></div></div>
<div class="faq-item"><div class="faq-question">Quelle différence entre remise et ristourne ?</div><div class="faq-answer"><p>La remise est une réduction appliquée immédiatement sur la facture ; la ristourne est calculée a posteriori sur le chiffre d'affaires réalisé sur une période (par exemple un avoir trimestriel selon les volumes atteints).</p></div></div>
<div class="faq-item"><div class="faq-question">Comment éviter les erreurs de prix en facturation ?</div><div class="faq-answer"><p>En automatisant l'application des tarifs : la commande récupère le bon prix selon le client et le volume, calcule la marge en temps réel et bloque les ventes à perte. Un ERP de négoce garantit la cohérence du devis à la facture.</p></div></div>
<div class="faq-item"><div class="faq-question">Pourquoi relier la grille tarifaire à l'EDI ?</div><div class="faq-answer"><p>Parce que les prix transmis aux centrales d'achat par EDI doivent correspondre exactement aux conditions négociées. Un écart entraîne des rejets de messages et des litiges. Un socle unique tarifs/ventes/EDI supprime ces désynchronisations.</p></div></div>
</main>""",
},
{
 "slug": "reporting-commercial-grossiste",
 "title": "Reporting commercial pour grossistes : marges, tableaux de bord et pilotage",
 "source": """<h1>Reporting commercial pour grossistes : marges, tableaux de bord et pilotage</h1>
<main class="article-content">
<p>Un grossiste qui ne mesure pas ses marges par client et par produit pilote à l'aveugle. Le <strong>reporting commercial</strong> transforme la masse des ventes en décisions : quels clients sont rentables, quels produits décrochent, où la marge fuit. Encore faut-il qu'il soit fiable et produit sans ressaisie. Voici les indicateurs clés et la méthode pour bâtir un pilotage commercial solide en négoce.</p>

<h2>Pourquoi le reporting commercial est vital en négoce</h2>
<p>Le négoce alimentaire vit sur des marges faibles et des volumes élevés : un point de marge perdu sur une gamme se chiffre vite en milliers d'euros. Le reporting commercial sert à détecter ces dérives tôt — un client dont la remise dérape, une référence vendue sous son coût, une tournée non rentable — et à réagir avant que le résultat ne soit entamé. C'est le prolongement naturel d'une bonne <a href="/blog/erp-grossiste-distributeur/">gestion de négoce</a>.</p>

<h2>Les KPI commerciaux à suivre</h2>
<p>Quelques indicateurs concentrent l'essentiel du pilotage :</p>
<table>
<thead><tr><th>Indicateur</th><th>Ce qu'il révèle</th></tr></thead>
<tbody>
<tr><td><strong>Chiffre d'affaires par client / produit</strong></td><td>concentration et dépendance commerciale</td></tr>
<tr><td><strong>Marge brute et taux de marge</strong></td><td>rentabilité réelle, au-delà du volume</td></tr>
<tr><td><strong>Taux de service</strong></td><td>capacité à livrer ce qui est commandé</td></tr>
<tr><td><strong>Rotation et couverture de stock</strong></td><td>efficacité du capital immobilisé</td></tr>
<tr><td><strong>Panier moyen et fréquence</strong></td><td>dynamique de chaque compte client</td></tr>
</tbody>
</table>
<p>La marge se lit toujours à partir d'un coût juste : c'est pourquoi le reporting s'appuie sur la valorisation des stocks en <a href="/blog/calcul-du-prix-moyen/">prix moyen pondéré</a>.</p>

<h2>Tableaux de bord : du suivi client au pilotage des marges</h2>
<p>Un bon tableau de bord commercial se lit en quelques secondes : évolution du CA et de la marge, top et flop clients, top et flop produits, alertes sur les marges anormales. L'idéal est de croiser ces vues avec le <a href="/fonctionnalites/crm/">CRM</a> pour relier performance commerciale et action terrain des commerciaux.</p>

<h2>Construire un reporting fiable sans ressaisie</h2>
<p>Le piège classique est l'export manuel vers un tableur : chronophage, vite obsolète et truffé d'erreurs. Un reporting utile est <strong>connecté à la source</strong> — les ventes, les <a href="/negoce/achats-approvisionnements/">achats</a> et les stocks — et se met à jour en temps réel. Les bons tarifs, le bon coût, les bonnes quantités : tout part du même référentiel.</p>

<h2>Reporting, tarifs et EDI : connecter la donnée commerciale</h2>
<p>Le reporting commercial ne vit pas seul. Il s'alimente des <a href="/negoce/tarifs-reporting-edi/">tarifs, du reporting et de l'EDI</a> gérés sur un socle unique : les conditions clients déterminent la marge analysée, et les flux <a href="/blog/edi-logiciel-agroalimentaire/">EDI</a> avec la grande distribution remontent automatiquement dans les indicateurs. Un <a href="/negoce/">ERP de négoce</a> spécialisé fournit ce pilotage clé en main, sans ressaisie.</p>

<h2>FAQ : reporting commercial pour grossistes</h2>
<div class="faq-item"><div class="faq-question">Quels indicateurs suivre dans un reporting commercial de négoce ?</div><div class="faq-answer"><p>Le chiffre d'affaires par client et par produit, la marge brute et le taux de marge, le taux de service, la rotation et la couverture de stock, ainsi que le panier moyen et la fréquence d'achat par compte.</p></div></div>
<div class="faq-item"><div class="faq-question">Comment calculer la marge dans un reporting fiable ?</div><div class="faq-answer"><p>En partant d'un coût d'achat juste, idéalement valorisé en prix moyen pondéré (CUMP), et des tarifs réellement appliqués. La marge brute = prix de vente net − coût d'achat valorisé ; le taux de marge la rapporte au prix de vente.</p></div></div>
<div class="faq-item"><div class="faq-question">Pourquoi éviter le reporting sur tableur ?</div><div class="faq-answer"><p>Parce que l'export manuel est chronophage, vite obsolète et source d'erreurs. Un reporting connecté aux ventes, achats et stocks se met à jour en temps réel à partir d'un référentiel unique, sans ressaisie.</p></div></div>
<div class="faq-item"><div class="faq-question">Un ERP de négoce fournit-il le reporting commercial ?</div><div class="faq-answer"><p>Oui : un ERP de négoce spécialisé centralise ventes, tarifs, achats, stocks et flux EDI, et en tire des tableaux de bord de marge et de performance client clé en main, actualisés en continu.</p></div></div>
</main>""",
},
]


def main():
    live = "--live" in sys.argv
    import os
    os.makedirs("preview-tpl", exist_ok=True)
    for art in ARTICLES:
        slug, title, source = art["slug"], art["title"], art["source"]
        data = T.extract(source)
        assert data and data["body"] and data["title"], f"{slug} extract failed"
        rendered = T.render(slug, data, DATE, AUTHOR)
        assert "hha-tpl" in rendered and "BreadcrumbList" in rendered, f"{slug} guard"
        assert len(data["faq_qa"]) >= 2, f"{slug} FAQ not parsed ({len(data['faq_qa'])})"
        print(f"{slug}: h2={len(data['toc'])} faq={len(data['faq_qa'])}")
        if not live:
            open(f"preview-tpl/{slug}.html", "w").write(rendered)
            print(f"  dry -> preview-tpl/{slug}.html")
            continue
        import wp_common as wp
        existing = wp.api(f"posts?slug={slug}&status=publish,draft&_fields=id,slug")
        if isinstance(existing, list) and existing:
            pid = existing[0]["id"]
            wp.api(f"posts/{pid}", method="POST", data={"content": rendered, "title": title})
            print(f"  UPDATED {pid} -> https://www.helloharel.com/blog/{slug}/")
        else:
            res = wp.api("posts", method="POST", data={
                "title": title, "slug": slug, "status": "publish", "content": rendered,
                "author": AUTHOR, "categories": [CATEGORY], "template": "elementor_canvas",
                "date": DATE})
            print(f"  CREATED {res['id']} -> https://www.helloharel.com/blog/{slug}/")


if __name__ == "__main__":
    main()
