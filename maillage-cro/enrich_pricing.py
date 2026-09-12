#!/usr/bin/env python3
"""
Enrich 3 EXISTING pricing articles (cannibalization study: do NOT create new
URLs that duplicate them — deepen the existing pages instead):

  - cout-prix-au-kilo   (id 4470) : ajoute "méthode + formule" + FAQ
  - couts-de-production (id 4436) : ajoute "méthode et formule" + FAQ
  - calcul-du-prix-moyen(id 2847) : ajoute "prix moyen pondéré (PMP/CUMP)" + FAQ

Source = the pristine pre-template body (<main class="article-content">) in
backup-live-20260529-223414/, exactly like enrich.py. New prose H2 + a
"Questions fréquentes" block are inserted just before the "Besoin d'Aller Plus
Loin" internal-links section, then the SAME extract()+render() pipeline rebuilds
the page (interactive tool, inter-H2 visuals, home-style FAQ + JSON-LD, chrome).

These articles had NO FAQ inside <main> (their old FAQ lived outside the marker
and was therefore dropped by render), so the FAQ block is genuine enrichment.

Run:
  python3 enrich_pricing.py            # DRY-RUN -> preview-tpl/<slug>.html
  python3 enrich_pricing.py --live     # re-publish the enriched articles
"""
import sys, os, re, json, glob
import template as T

SRC_DIR = "backup-live-20260529-223414"

FAQ_DIV = ('<div class="faq-item"><div class="faq-question">{q}</div>'
           '<div class="faq-answer"><p>{a}</p></div></div>')


def faq_block(pairs):
    items = "".join(FAQ_DIV.format(q=q, a=a) for q, a in pairs)
    return f'<h2>Questions fréquentes</h2>{items}'


ENRICH = {
    "cout-prix-au-kilo": {
        "id": 4470, "date": "2025-02-19T17:20:39", "author": 2,
        "section": """<h2>Prix au kilo : la formule et la méthode de calcul pas à pas</h2>
<p>La formule est simple : <strong>prix au kilo = prix total ÷ poids total (en kg)</strong>. Mais en agroalimentaire, c'est le choix du poids et du coût de départ qui fait toute la différence. La méthode tient en trois étapes : partir du bon prix, ramener au poids réellement vendable, puis convertir dans l'unité utile à la vente.</p>
<p><strong>1. Partir du prix d'achat… ou du coût de revient.</strong> Pour un prix au kilo « brut », on divise le prix payé par le poids du colis : un jambon de 2,5 kg acheté 18 € revient à <strong>7,20 €/kg</strong>. Pour un prix au kilo « rentable », on part plutôt du <a href="/blog/cout-de-revient/">coût de revient</a>, qui intègre matière, main-d'œuvre et <a href="/blog/couts-de-production/">coûts de production</a>, avant d'appliquer la marge.</p>
<p><strong>2. Raisonner en poids net, pas en poids brut.</strong> Le parage, l'égouttage ou le séchage réduisent le poids vendable. Si ce jambon de 2,5 kg ne donne que 2,2 kg après désossage, le coût réel grimpe à <strong>8,18 €/kg</strong> (18 € ÷ 2,2). Oublier la freinte, c'est sous-estimer son prix au kilo — la même erreur que confondre <a href="/blog/difference-prix-dachat-et-prix-de-revient/">prix d'achat et prix de revient</a>.</p>
<p><strong>3. Convertir entre les unités.</strong> Du prix au kilo, on déduit le prix à la portion : à 7,20 €/kg, une part de 180 g se vend 1,30 €. À l'inverse, un prix au colis se ramène au kilo en divisant par le poids net. C'est exactement ce que fait le calculateur en haut de page : saisissez prix et poids, il renvoie le prix au kilo et la conversion instantanément.</p>""",
        "faq": [
            ("Comment calculer un prix au kilo à partir d'un prix au colis ?",
             "Divisez le prix du colis par son poids net en kilos. Un colis facturé 45 € pour 6 kg nets revient à 7,50 €/kg. Si le poids est indiqué en grammes, ramenez-le d'abord en kilos (6 000 g = 6 kg) avant de diviser."),
            ("Faut-il calculer le prix au kilo sur le poids brut ou le poids net ?",
             "Toujours sur le poids net réellement vendable, après parage, désossage ou égouttage. Calculer sur le poids brut sous-estime le prix au kilo et rogne la marge, car vous facturez moins de matière que celle réellement payée."),
        ],
    },
    "couts-de-production": {
        "id": 4436, "date": "2025-02-12T17:36:09", "author": 2,
        "section": """<h2>Coût de production : la formule complète (coûts fixes + variables)</h2>
<p>Le coût de production regroupe toutes les charges engagées pour fabriquer un produit, avant sa distribution. <strong>La formule de base : coût de production total = charges directes + charges indirectes.</strong> Les charges directes (matières premières, main-d'œuvre de fabrication) sont affectables au produit ; les charges indirectes (énergie, amortissement des machines, frais d'atelier) se répartissent sur l'ensemble de la production.</p>
<p>Le <strong>coût de production unitaire</strong> s'obtient en divisant ce total par la quantité produite : <strong>coût unitaire = coût de production total ÷ quantité</strong>. C'est l'indicateur clé, car il distingue ce qui varie avec le volume de ce qui reste fixe.</p>
<p><strong>Coûts fixes vs coûts variables.</strong> Les coûts variables (matière, emballage) évoluent proportionnellement aux quantités, si bien que le coût variable unitaire reste à peu près constant. Les coûts fixes (loyer, machines, encadrement) ne bougent pas à court terme : leur poids unitaire <em>diminue</em> quand le volume augmente — c'est l'effet d'échelle.</p>
<p><strong>Exemple chiffré.</strong> Pour 1 000 unités : 4 000 € de charges variables + 2 000 € de charges fixes = 6 000 €, soit <strong>6 €/unité</strong>. En passant à 2 000 unités, les charges fixes se diluent : (8 000 + 2 000) ÷ 2 000 = <strong>5 €/unité</strong>. Le coût de production est ainsi la première brique du <a href="/blog/cout-de-revient/">coût de revient</a> ; pour décider d'accepter un volume supplémentaire, on le complète par le <a href="/blog/cout-marginal/">coût marginal</a>, et on le ramène souvent au <a href="/blog/cout-prix-au-kilo/">prix au kilo</a>. Un <a href="/fonctionnalites/fabrication/">module de fabrication</a> calcule tout cela automatiquement à partir des nomenclatures.</p>""",
        "faq": [
            ("Quelle est la différence entre coût de production et coût de revient ?",
             "Le coût de production s'arrête à la fabrication (matières, main-d'œuvre, charges d'atelier). Le coût de revient y ajoute les coûts de distribution (logistique, commercialisation, emballage de vente) : c'est le coût total du produit avant la marge."),
            ("Comment réduire son coût de production unitaire ?",
             "Trois leviers : augmenter le volume pour diluer les charges fixes, réduire les pertes et freintes sur la matière, et optimiser les temps de main-d'œuvre. Suivre le coût unitaire en temps réel permet d'identifier le poste le plus lourd avant d'agir."),
        ],
    },
    "calcul-du-prix-moyen": {
        "id": 2847, "date": "2024-04-29T14:51:36", "author": 2,
        "section": """<h2>Prix moyen pondéré (PMP / CUMP) : formule et calcul</h2>
<p>Le <strong>prix moyen pondéré</strong> — aussi appelé <strong>CUMP</strong> (coût unitaire moyen pondéré) — est la méthode de référence pour valoriser un stock dont les entrées arrivent à des prix différents. Contrairement à une simple moyenne, il <em>pondère chaque prix par la quantité</em> concernée : un lot important pèse davantage qu'un petit lot dans le prix moyen.</p>
<p><strong>La formule : PMP = (valeur du stock + valeur de l'entrée) ÷ (quantité en stock + quantité entrée).</strong> Concrètement, à chaque réception on additionne les valeurs et les quantités, puis on divise.</p>
<p><strong>Exemple.</strong> Vous avez 100 kg en stock à 4 €/kg (soit 400 €) et vous recevez 50 kg à 7 €/kg (soit 350 €). Le PMP = (400 + 350) ÷ (100 + 50) = 750 ÷ 150 = <strong>5 €/kg</strong>. À comparer avec la <em>moyenne simple</em> de 4 et 7, qui donnerait 5,50 €/kg : c'est faux, car elle ignore que vous déteniez deux fois plus du lot à 4 €. C'est toute la différence du « pondéré ».</p>
<p><strong>PMP après chaque entrée ou de fin de période ?</strong> Le CUMP peut se recalculer à chaque réception (suivi permanent) ou une fois par période sur l'ensemble des entrées. C'est l'alternative aux méthodes par flux comme le <a href="/blog/fifo-fefo-lifo/">FIFO / FEFO</a> : le PMP lisse les variations de prix, là où le FIFO épouse l'ordre des lots — un choix structurant pour la valorisation du stock et le calcul du <a href="/blog/cout-de-revient/">coût de revient</a>. Un <a href="/fonctionnalites/gestion-de-stock/">logiciel de gestion de stock</a> recalcule le CUMP automatiquement à chaque mouvement.</p>""",
        "faq": [
            ("Quelle est la différence entre prix moyen et prix moyen pondéré ?",
             "Le prix moyen simple additionne les prix et divise par leur nombre, sans tenir compte des quantités. Le prix moyen pondéré (PMP/CUMP) pondère chaque prix par la quantité associée : c'est la seule méthode juste pour valoriser un stock alimenté par des lots de tailles différentes."),
            ("PMP ou FIFO : quelle méthode de valorisation des stocks choisir ?",
             "Le PMP (CUMP) lisse le coût des entrées et simplifie la gestion quand les prix fluctuent souvent. Le FIFO (premier entré, premier sorti) reflète l'ordre réel des lots et s'impose pour les denrées périssables pilotées par DLC. Beaucoup d'ERP agroalimentaires gèrent les deux selon le type de produit."),
        ],
    },
}


def src_file(slug):
    fs = glob.glob(f"{SRC_DIR}/*{slug}*")
    return fs[0] if fs else None


def insert_before_outro(raw, addition):
    """Insert `addition` just before the '...Aller Plus Loin' internal-links
    section (inside <main>); fall back to before </main>."""
    mo = re.search(r'<main class="article-content"[^>]*>', raw, re.I)
    if not mo:
        return None
    start = mo.end()
    end_m = re.search(r'</main>', raw[start:], re.I)
    end = start + end_m.start() if end_m else len(raw)
    body = raw[start:end]

    # Locate the "Aller Plus Loin" outro and back up to its wrapping <section>.
    h = re.search(r'Aller\s+Plus\s+Loin', body, re.I)
    if h:
        sec = None
        for m in re.finditer(r'<section\b[^>]*>', body):
            if m.start() < h.start():
                sec = m
            else:
                break
        pos = sec.start() if sec else h.start()
    else:
        pos = len(body)

    body = body[:pos] + addition + body[pos:]
    return raw[:start] + body + raw[end:]


def main():
    live = "--live" in sys.argv
    only = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else None
    os.makedirs("preview-tpl", exist_ok=True)

    for slug, cfg in ENRICH.items():
        if only and slug != only:
            continue
        f = src_file(slug)
        if not f:
            print(f"SKIP {slug}: no pristine source in {SRC_DIR}"); continue
        raw = (json.load(open(f)).get("content") or {}).get("raw", "") or ""
        addition = cfg["section"] + faq_block(cfg["faq"])
        enriched = insert_before_outro(raw, addition)
        if not enriched:
            print(f"SKIP {slug}: no <main> marker"); continue

        data = T.extract(enriched)
        if not data or not data["body"]:
            print(f"SKIP {slug}: extraction failed"); continue
        rendered = T.render(slug, data, cfg["date"], cfg["author"])
        assert "hha-tpl" in rendered and "<h1" in rendered, f"{slug} render guard"
        assert len(data["faq_qa"]) >= 2, f"{slug} FAQ not picked up ({len(data['faq_qa'])})"
        print(f"{slug}: h2={len(data['toc'])} faq={len(data['faq_qa'])} bytes={len(rendered)}")

        if live:
            import wp_common as wp
            wp.api(f"posts/{cfg['id']}", method="POST", data={"content": rendered})
            print(f"  WROTE post {cfg['id']} -> https://www.helloharel.com/blog/{slug}/")
        else:
            open(f"preview-tpl/{slug}.html", "w").write(rendered)
            print(f"  dry -> preview-tpl/{slug}.html")


if __name__ == "__main__":
    main()
