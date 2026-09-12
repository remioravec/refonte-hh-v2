#!/usr/bin/env python3
"""
Enrich 5 EXISTING articles (cannibalization study said: do NOT create, deepen
the existing URL). For each, we add substantive H2 section(s) targeting the
requested SERP micro-intentions + surfer-reasonable outbound links, then run the
SAME extract()+render() pipeline and re-publish.

Insertion: new sections go just before the FAQ heading (or a "pour aller plus
loin" heading, else before </main>). cout-marginal also receives a proper
"Questions fréquentes" section (it had none in the home card/drawer format).

Run:
  python3 enrich.py            # DRY-RUN -> preview-tpl/<slug>.html
  python3 enrich.py --live     # re-publish the enriched articles
"""
import sys, os, re, json, glob
import template as T
import wp_common as wp

DATE_FALLBACK = "2026-06-01T09:00:00"


def src_file(slug):
    for f in glob.glob(f"backup-live-2026052*/*{slug}*"):
        return f
    return None


# ---- authored enrichment sections (HTML) -----------------------------------
FAQ_DIV = ('<div class="faq-item"><div class="faq-question">{q}</div>'
           '<div class="faq-answer"><p>{a}</p></div></div>')


def faq_block(title, pairs):
    items = "".join(FAQ_DIV.format(q=q, a=a) for q, a in pairs)
    return f'<h2>{title}</h2>{items}'


ENRICH = {
    # #4 — suivi paiement client / encaissements / impayés (cluster facturation)
    "relance-client": {
        "sections": ["""<h2>Du suivi des encaissements à la relance automatique des impayés</h2>
<p>Relancer, c'est bien ; mais piloter l'encaissement de bout en bout, c'est ce qui protège la trésorerie. Le suivi du paiement client commence dès l'émission de la facture : échéance, mode de règlement attendu, puis <strong>lettrage</strong> automatique des encaissements pour solder chaque pièce sans pointage manuel. Une <strong>balance âgée</strong> à jour révèle en un coup d'œil les créances à 30, 60 et 90 jours.</p>
<p>Dans un <a href="/agroalimentaire/">ERP agroalimentaire</a>, ce suivi se branche directement sur la <a href="/fonctionnalites/facturation/">facturation</a> : dès qu'une échéance est dépassée, une relance est déclenchée automatiquement, par paliers (rappel courtois, relance ferme, mise en demeure), sans que personne n'ait à y penser. C'est le prolongement naturel des modèles d'e-mails ci-dessus, mais piloté par la donnée comptable plutôt qu'à la main.</p>
<p>Cette mécanique gagne encore en fiabilité avec la <a href="/blog/factur-x-e-facturation-logiciel/">facture électronique (Factur-X)</a> : statut de la facture connu en temps réel, rapprochement automatique du paiement, et relance ciblée uniquement sur les vrais impayés. Côté relation client, l'historique des échanges remonte dans le <a href="/fonctionnalites/crm/">CRM</a> pour ne jamais relancer un client déjà à jour.</p>"""],
        "faq": [
            ("Comment automatiser la relance des impayés ?",
             "On définit des règles par paliers déclenchées sur l'échéance de la facture : J+1 rappel, J+8 relance ferme, J+15 mise en demeure. L'ERP envoie l'e-mail ou le courrier automatiquement et arrête la relance dès que l'encaissement est lettré."),
            ("Qu'est-ce que le lettrage des encaissements ?",
             "Le lettrage rapproche automatiquement un paiement reçu de la ou des factures qu'il solde. Il évite le pointage manuel, fiabilise la balance âgée et garantit qu'aucun client déjà payé n'est relancé par erreur."),
        ],
    },
    # #6 — droits d'accises / DSA / capsule (cluster negoce)
    "logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises": {
        "sections": ["""<h2>Droits d'accises, DSA et capsules : automatiser vos obligations</h2>
<p>Distribuer de l'alcool, c'est gérer un stock <strong>sous douane</strong> et des taxes spécifiques : les <strong>droits d'accises</strong>. Chaque sortie de chai modifie votre compte d'entrepositaire agréé et alimente la <strong>DRM</strong> (déclaration récapitulative mensuelle) adressée à la douane. Tenir ce suivi à la main, c'est l'erreur garantie ; un <a href="/negoce/">ERP de négoce</a> paramétré pour le liquide calcule les droits dus en temps réel, par catégorie fiscale et par degré.</p>
<p>La circulation des produits soumis à accises s'accompagne d'un <strong>DSA/DSAC</strong> (document simplifié d'accompagnement) ou d'un e-DSA via EMCS pour le suivi dématérialisé. Les bouteilles, elles, portent une <strong>capsule CRD</strong> (capsule représentative de droits) dont les stocks doivent être justifiés. Un logiciel spécialisé édite ces documents depuis la commande et rapproche automatiquement capsules consommées et volumes expédiés.</p>
<p>Le vrai gain apparaît quand accises, capsules et <a href="/blog/erp-boissons/">gestion des consignes</a> partagent le même socle que la logistique et la facturation — et que les flux vers la grande distribution passent en <a href="/blog/edi-logiciel-agroalimentaire/">EDI</a>. La traçabilité réglementaire des lots, jusqu'aux <a href="/blog/tracabilite-lot-dlc-logiciel/">DLC et numéros de lot</a>, complète le dispositif douanier.</p>"""],
        "faq": [
            ("Comment un logiciel gère-t-il les droits d'accises sur l'alcool ?",
             "Il classe chaque référence par catégorie fiscale et degré, calcule les droits dus à chaque sortie de stock sous douane, tient le compte d'entrepositaire agréé et prépare la DRM mensuelle à transmettre à la douane."),
            ("Qu'est-ce que le DSA et la capsule CRD ?",
             "Le DSA (document simplifié d'accompagnement) accompagne la circulation des produits soumis à accises ; sa version dématérialisée passe par EMCS. La capsule CRD (capsule représentative de droits) matérialise l'acquittement des droits sur la bouteille : ses stocks doivent être justifiés et rapprochés des volumes expédiés."),
        ],
    },
    # #7 — coût de revient : définition + calcul complet (cluster couts)
    "cout-de-revient": {
        "sections": ["""<h2>Coût de revient : définition complète et méthode de calcul pas à pas</h2>
<p><strong>Définition.</strong> Le coût de revient d'un produit est la somme de toutes les charges — directes et indirectes — engagées pour le fabriquer et le mettre à disposition du client. Autrement dit : tout ce qu'il a coûté avant d'être vendu. C'est la base qui détermine votre prix de vente plancher et votre marge réelle.</p>
<p><strong>La formule complète</strong> s'articule en trois blocs : coût d'<a href="/blog/calcul-du-cout-achat/">achat</a> des matières (prix d'achat + frais d'approche) + coût de <a href="/fonctionnalites/fabrication/">production</a> (main-d'œuvre directe + charges d'atelier + pertes et freintes) + coût de distribution (logistique, commissions, emballage). On obtient le coût de revient unitaire en divisant ce total par la quantité produite.</p>
<p><strong>Exemple.</strong> Pour 100 kg de produit fini : 320 € de matières + 110 € de main-d'œuvre + 45 € de charges atelier + 25 € de distribution = 500 €, soit 5,00 €/kg de coût de revient. Si la freinte de séchage fait passer le rendement à 92 kg vendables, le coût grimpe mécaniquement à 5,43 €/kg — d'où l'importance d'intégrer les pertes dans le calcul. Ce coût de revient « réel » se distingue du <a href="/blog/cout-marginal/">coût marginal</a> (coût d'une unité supplémentaire) et ne doit pas être confondu avec le <a href="/blog/difference-prix-dachat-et-prix-de-revient/">simple prix d'achat</a>.</p>"""],
        "faq": [
            ("Quelle est la différence entre coût de revient et prix de revient ?",
             "Les deux termes désignent la même réalité : l'ensemble des coûts engagés pour produire et distribuer un bien. « Prix de revient » est l'usage courant, « coût de revient » l'usage comptable. Tous deux s'opposent au prix d'achat, qui ne couvre que la matière."),
            ("Comment intégrer les pertes et freintes au coût de revient ?",
             "On rapporte le total des charges à la quantité réellement vendable, pas à la quantité engagée. Si 100 kg engagés donnent 92 kg vendables, le coût de revient se calcule sur 92 kg : le rendement matière fait donc partie intégrante du calcul."),
        ],
    },
    # #8 — coût marginal : refonte + FAQ enrichie (cluster couts) — had NO standard FAQ
    "cout-marginal": {
        "sections": ["""<h2>Coût marginal, coût moyen et coût de revient : ne plus les confondre</h2>
<p>Trois notions, trois décisions différentes. Le <strong>coût marginal</strong> est le coût de production d'une unité supplémentaire : il guide la décision d'accepter ou non une commande additionnelle. Le <strong>coût moyen</strong> (ou coût unitaire) rapporte le coût total au volume produit. Le <a href="/blog/cout-de-revient/">coût de revient</a>, lui, agrège toutes les charges jusqu'à la mise à disposition du client.</p>
<p>En pratique : tant que le prix proposé par un client couvre le coût marginal, une commande supplémentaire reste rentable à court terme, même sous le coût moyen — à condition que les charges fixes soient déjà absorbées. C'est ce raisonnement qui permet d'arbitrer un volume promotionnel sans détruire la marge globale, et il se prolonge naturellement vers la <a href="/blog/couts-de-production/">maîtrise des coûts de production</a> et le <a href="/blog/cout-prix-au-kilo/">coût au kilo</a>.</p>"""],
        "faq_title": "Questions fréquentes",
        "faq": [
            ("C'est quoi le coût marginal, simplement ?",
             "C'est ce que coûte la production d'une unité de plus. Si produire 100 unités coûte 1 000 € et 101 unités 1 008 €, le coût marginal de la 101ᵉ est de 8 €."),
            ("Quelle est la formule du coût marginal ?",
             "Coût marginal = variation du coût total ÷ variation de la quantité (ΔCT / ΔQ). On mesure l'écart de coût total entre deux niveaux de production puis on le divise par le nombre d'unités ajoutées."),
            ("Pourquoi le coût marginal est-il décisif pour accepter une commande ?",
             "Parce qu'une commande reste rentable tant que son prix dépasse le coût marginal, même si ce prix est inférieur au coût moyen : les charges fixes étant déjà couvertes, chaque unité supplémentaire dégage une marge sur coûts variables."),
            ("Coût marginal et coût de revient, est-ce pareil ?",
             "Non. Le coût de revient additionne toutes les charges (achat, production, distribution) pour fixer un prix plancher durable. Le coût marginal ne mesure que le surcoût d'une unité supplémentaire et sert aux décisions ponctuelles de volume."),
            ("Le coût marginal peut-il diminuer puis augmenter ?",
             "Oui. Il baisse d'abord avec les économies d'échelle, puis remonte quand on sature les capacités (heures supplémentaires, maintenance, gaspillage). Le minimum du coût marginal indique le niveau de production le plus efficient."),
        ],
    },
    # #9 — prix de revient : approfondir l'existant (cluster couts)
    "difference-prix-dachat-et-prix-de-revient": {
        "sections": ["""<h2>Approfondir : calculer le prix de revient complet en agroalimentaire</h2>
<p>Au-delà de la distinction prix d'achat / prix de revient, voici la méthode complète pour obtenir un prix de revient fiable en agroalimentaire. On part du <a href="/blog/prix-dachat-definition/">prix d'achat</a> des matières, auquel on ajoute les <strong>frais d'approche</strong> (transport, douane, manutention) pour obtenir le coût d'achat, puis le <a href="/blog/calcul-du-cout-achat/">coût d'achat rendu</a>.</p>
<p>On y intègre ensuite la <strong>main-d'œuvre directe</strong>, les charges d'atelier et surtout les <strong>pertes et freintes</strong> propres au métier (parage, séchage, casse) : c'est l'étape la plus souvent oubliée, et celle qui fait dériver la marge. Le prix de revient se calcule toujours sur la quantité réellement vendable, jamais sur la quantité engagée.</p>
<p>Cette logique est identique au <a href="/blog/cout-de-revient/">coût de revient</a> et se décline par filière : on la retrouve par exemple détaillée pour la <a href="/blog/calculer-le-prix-de-revient-en-boulangerie/">boulangerie</a>, où la fournée et les invendus pèsent directement sur le prix de revient unitaire.</p>"""],
        "faq": [
            ("Le prix de revient inclut-il la main-d'œuvre ?",
             "Oui. Le prix de revient additionne le coût d'achat des matières, la main-d'œuvre directe, les charges indirectes et les coûts de distribution. Seul le prix d'achat se limite à la matière."),
            ("Sur quelle quantité calculer le prix de revient ?",
             "Sur la quantité réellement vendable, après pertes et freintes. Calculer sur la quantité engagée sous-estime systématiquement le prix de revient et donne une marge théorique trop optimiste."),
        ],
    },
}


def _items_in_pattern(region, pairs):
    """Build FAQ items in the SAME markup pattern the region already uses, so
    faqs.parse() (which returns on the FIRST matching pattern B>A>C) keeps both
    the original and the new items together."""
    if re.search(r'class="faq-question"', region):
        return "".join(FAQ_DIV.format(q=q, a=a) for q, a in pairs)          # B
    if re.search(r'<p>\s*<strong>', region):
        return "".join(f'<p><strong>{q}</strong><br>{a}</p>' for q, a in pairs)  # A
    return "".join(f'<h3>{q}</h3><p>{a}</p>' for q, a in pairs)             # C


def insert_sections(raw, sections_html, faq_pairs, faq_title=None):
    """Insert new prose H2 sections just before the FAQ heading (or before
    </main>), and merge FAQ items in the article's native FAQ pattern."""
    mo = re.search(r'<main class="article-content"[^>]*>', raw, re.I)
    if not mo:
        return None
    start = mo.end()
    end_m = re.search(r'</main>', raw[start:], re.I)
    end = start + end_m.start() if end_m else len(raw)
    body = raw[start:end]

    # locate the FAQ heading inside the body
    faq_h = None
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', body, re.S):
        if re.search(r'faq|questions?\s+fr[ée]quentes', re.sub(r'<[^>]+>', ' ', m.group(1)), re.I):
            faq_h = m
            break

    add = "".join(sections_html)

    if faq_h:
        h_start, h_end = faq_h.start(), faq_h.end()
        nh = re.search(r'<h2[^>]*>', body[h_end:])           # next h2 after FAQ heading
        region = body[h_end: h_end + nh.start()] if nh else body[h_end:]
        items = _items_in_pattern(region, faq_pairs) if faq_pairs else ""
        # 1) FAQ items right after the heading (positions <= h_start unaffected)
        body = body[:h_end] + items + body[h_end:]
        # 2) new prose sections before the FAQ heading
        body = body[:h_start] + add + body[h_start:]
    else:
        body = body + add
        if faq_pairs:
            body = body + faq_block(faq_title or "Questions fréquentes", faq_pairs)

    return raw[:start] + body + raw[end:]


def main():
    live = "--live" in sys.argv
    only = None
    if "--slug" in sys.argv:
        only = sys.argv[sys.argv.index("--slug") + 1]
    os.makedirs("preview-tpl", exist_ok=True)

    posts = wp.api("posts?per_page=100&status=publish&_fields=id,slug")
    by_slug = {p["slug"]: p["id"] for p in posts}

    for slug, cfg in ENRICH.items():
        if only and slug != only:
            continue
        f = src_file(slug)
        if not f:
            print(f"SKIP {slug}: no pristine source"); continue
        raw = (json.load(open(f)).get("content") or {}).get("raw", "") or ""
        enriched = insert_sections(raw, cfg["sections"], cfg.get("faq", []), cfg.get("faq_title"))
        if not enriched:
            print(f"SKIP {slug}: no <main> marker"); continue
        data = T.extract(enriched)
        if not data or not data["body"]:
            print(f"SKIP {slug}: extraction failed"); continue
        pid = by_slug.get(slug)
        full = wp.get_raw("posts", pid) if pid else {}
        rendered = T.render(slug, data, full.get("date", DATE_FALLBACK), full.get("author", 2))
        assert "hha-tpl" in rendered and "<h1" in rendered, f"{slug} guard"
        print(f"{slug}: h2={len(data['toc'])} faq={len(data['faq_qa'])} bytes={len(rendered)}")
        if live:
            wp.api(f"posts/{pid}", method="POST", data={"content": rendered})
            print(f"  WROTE post {pid} -> /blog/{slug}/")
        else:
            open(f"preview-tpl/{slug}.html", "w").write(rendered)
            print(f"  dry -> preview-tpl/{slug}.html")


if __name__ == "__main__":
    main()
