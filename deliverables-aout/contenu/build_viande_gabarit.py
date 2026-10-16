#!/usr/bin/env python3
"""
/agroalimentaire/viande/ — GABARIT DES PAGES SOEURS (etape 3 du process).
Gabarit de reference : /agroalimentaire/charcutier/ (id 2818) — soeur la plus
proche (filiere carnee) et la mieux positionnee (2e sur « erp charcutier »).
Modules, Hn, JSON-LD (FAQPage + BreadcrumbList + LocalBusiness), CTA et maillage
sont repris a l'identique. Seul le contenu filiere change.
Regle 0 : aucune ancre exact-match ne pointe vers une page protegee.
DRY par defaut ; --live pour publier.
"""
import sys, re, json
import wp_common as w

SRC, DEST = 2818, 11332
TITLE = "ERP Viande • Découpe & Rendement Matière • Traçabilité ☁️"

REPL = [
 ('<div class="hero-badge"><span class="dot"></span>ERP Charcutier</div>',
  '<div class="hero-badge"><span class="dot"></span>ERP Viande</div>', True),
 ('<h1 class="hero-title" style="color:#fff">Gérez vos lots, assurez <span class="accent" style="color:#60a5fa">votre traçabilité</span></h1>',
  '<h1 class="hero-title" style="color:#fff">Suivez vos rendements, <span class="accent" style="color:#60a5fa">pièce par pièce</span></h1>', True),
 ("""<p class="hero-description">Charcuterie et boucherie : rendement matière, coût de revient, traçabilité de la viande, DLC courtes et étiquetage — l'ERP qui protège vos marges et sécurise vos audits. Voir notre <a href="/comparatifs/meilleur-erp-charcuterie-salaison/">comparatif des meilleurs ERP charcuterie &amp; salaison</a>.</p>""",
  """<p class="hero-description">Découpe, transformation et négoce de viande : rendement matière à la découpe, poids variable, traçabilité du lot d'abattage et DLC courtes — l'ERP qui rend visible ce que vous perdez entre la carcasse et le colis. Voir nos <a href="/comparatifs/">comparatifs ERP agroalimentaire</a>.</p>""", True),
 ("L'ERP conçu pour la charcuterie", "L'ERP conçu pour la filière viande", True),
 ("Boucherie &amp; charcuterie, traçabilité de la viande, rendements matière, DLC",
  "Ateliers de découpe, transformation et négoce : rendement matière, poids variable et traçabilité", True),
 ("Découvrir l'ERP charcutier", "Découvrir l'ERP viande", True),
 ("Conformité HACCP", "Conformité sanitaire et vétérinaire", True),
 ("Conformite HACCP en charcuterie", "Conformite sanitaire en filiere viande", True),
 ("poids après cuisson, pertes au tranchage", "poids après découpe, freinte et pertes au désossage", True),
 ("Chaque lot tracé depuis la matière première jusqu'au produit fini : numéros vétérinaires, dates d'abattage, poids, températures.",
  "Chaque lot tracé de la carcasse au colis expédié : numéro d'agrément, estampille sanitaire, lot d'abattage, poids réel et températures.", True),
 ("Voyez Hello Harel sur votre atelier de charcuterie",
  "Voyez Hello Harel sur votre atelier de découpe", True),
 ("Rendement matière, poids variable, traçabilité de la viande, coût de revient : l'ERP démontré sur vos cas concrets, en 30 minutes.",
  "Rendement à la découpe, poids variable, lot d'abattage, coût de revient au kilo : l'ERP démontré sur vos propres pièces, en 30 minutes.", True),
]

# --- FAQ filiere viande : (question, meta, reponse HTML) ---
FAQ = [
("L'ERP peut-il calculer mon rendement à la découpe ?", "L'ERP, peut-il, calculer",
 "<p>Oui. Le <strong>rendement matière</strong> est le rapport entre le poids de produit fini obtenu et le poids de matière première engagée. Hello Harel le calcule automatiquement à chaque opération de découpe, sans ressaisie.</p>"
 "<p>Le suivi se fait à trois niveaux :</p><ul>"
 "<li><strong>Par lot</strong> : ce qu'une carcasse ou un lot d'entrée a réellement produit, muscle par muscle.</li>"
 "<li><strong>Par pièce</strong> : le rendement propre à chaque référence, du désossage à la mise sous vide.</li>"
 "<li><strong>Par opérateur et par poste</strong> : les écarts entre équipes deviennent visibles, ce qui permet d'agir sur la formation plutôt que sur le prix d'achat.</li></ul>"
 "<p>La <strong>freinte</strong> — la perte entre le poids entré et le poids vendable — cesse d'être un écart constaté en fin de mois pour devenir une donnée pilotable au fil de l'eau. C'est la différence majeure avec un suivi sous tableur, où le rendement est reconstitué après coup, à partir de chiffres déjà figés.</p>"
 "<p>Le rendement se compare aussi dans le temps et entre sites : un même muscle travaillé sur deux ateliers ne donne pas toujours le même résultat, et l'écart n'a rien d'anecdotique une fois rapporté au tonnage annuel. En rendant cette comparaison possible, l'ERP transforme une intuition d'atelier en arbitrage chiffré : faut-il revoir la technique de découpe, changer de fournisseur, ou repositionner le prix de vente ?</p><p>Le rendement alimente enfin directement le <strong>coût de revient</strong> : tant qu'il est estimé, le prix de revient l'est aussi, et la marge annoncée reste théorique.</p>"),

("Peut-on lancer des promotions sur lots proches DLC ?", "Peut-on, lancer, promotions",
 "<p>Oui. En filière viande, les durées de vie sont courtes et un lot qui approche de sa <strong>date limite de consommation</strong> perd toute sa valeur s'il n'est pas écoulé à temps.</p>"
 "<p>Hello Harel identifie automatiquement les lots dont la DLC approche et permet de :</p><ul>"
 "<li>déclencher une remise ciblée sur ces lots précis, sans toucher au tarif général ;</li>"
 "<li>imprimer les étiquettes correspondantes, avec le prix promotionnel et la DLC réelle du lot ;</li>"
 "<li>prioriser ces lots à la préparation de commande, en <strong>FEFO</strong> — premier périmé, premier sorti ;</li>"
 "<li>suivre l'écoulement réel et l'impact sur la marge.</li></ul>"
 "<p>L'intérêt n'est pas seulement commercial : chaque kilo écoulé avant péremption est un kilo qui ne part pas en perte, et la perte sur produit fini coûte la matière première, la découpe et l'emballage réunis.</p>"
 "<p>La mécanique fonctionne parce que la DLC est portée par le lot et non par la référence : deux lots du même produit n'ont pas la même date, donc pas la même urgence commerciale. Un outil qui raisonne à la référence ne sait pas faire cette distinction.</p><p>Le même mécanisme sert la relation client : plutôt que de subir une perte, on propose l'offre au client dont la fréquence de commande correspond au délai restant.</p>"),

("L'ERP gère-t-il l'étiquetage et l'estampille sanitaire ?", "L'ERP, gère-t-il, étiquettes",
 "<p>Oui. L'étiquetage des produits carnés cumule plusieurs obligations, et une étiquette non conforme peut immobiliser un lot entier.</p>"
 "<p>Hello Harel génère les étiquettes à partir des données réelles du lot :</p><ul>"
 "<li><strong>Estampille sanitaire</strong> et numéro d'agrément de l'atelier ;</li>"
 "<li><strong>Origine</strong> — né, élevé, abattu, découpé — telle qu'exigée pour les viandes ;</li>"
 "<li><strong>Poids réel pesé</strong> de la pièce, et non un poids théorique ;</li>"
 "<li>DLC calculée depuis le lot, dénomination, conditions de conservation et allergènes au format <strong>INCO</strong> (règlement n° 1169/2011).</li></ul>"
 "<p>Comme l'étiquette est produite depuis la même base que la traçabilité et la facturation, l'information ne peut pas diverger entre le bon de pesée, l'étiquette et la facture — un écart fréquent quand ces trois documents sortent d'outils différents.</p>"
 "<p>L'étiquette se génère au moment de la pesée, à partir du poids réel constaté : c'est ce qui évite l'écart classique entre le poids annoncé et le poids livré, source de litiges et d'avoirs.</p><p>Les modèles d'étiquettes sont paramétrables par client et par circuit de distribution — la grande distribution imposant ses propres formats, codes et mentions.</p>"),

("Comment éviter un rappel produit total ?", "Comment, éviter, rappel",
 "<p>Un rappel produit se joue sur la précision de la traçabilité. Sans traçabilité fine, on ne sait pas quels lots sont concernés : il faut rappeler large, donc rappeler beaucoup.</p>"
 "<p>Hello Harel maintient une <strong>traçabilité ascendante et descendante</strong> complète :</p><ul>"
 "<li><strong>Ascendante</strong> — depuis un produit fini, retrouver le lot d'abattage, le fournisseur et la date d'entrée ;</li>"
 "<li><strong>Descendante</strong> — depuis un lot d'entrée suspect, retrouver tous les produits qui en sont issus et tous les clients livrés.</li></ul>"
 "<p>Concrètement, la liste des clients réellement concernés s'obtient en quelques minutes, alors que la même recherche menée entre des bons papier et plusieurs tableurs prend des jours — pendant lesquels le périmètre du rappel s'élargit par précaution.</p>"
 "<p>C'est aussi ce qui est demandé lors d'un contrôle des services vétérinaires : pouvoir remonter et redescendre la chaîne sur demande, avec les enregistrements à l'appui.</p>"
 "<p>Au-delà de l'urgence, cette traçabilité sert au quotidien : réclamation client, non-conformité fournisseur, audit d'un donneur d'ordre. Dans chaque cas, la question est la même — quel lot, parti où, quand — et la réponse doit être immédiate.</p><p>Les enregistrements étant produits automatiquement par les opérations, il n'existe pas de registre parallèle à tenir : la traçabilité est un sous-produit du travail, pas une tâche supplémentaire.</p>"),

("Qu'est-ce qu'un ERP viande et pourquoi en avoir un ?", "Qu'est-ce, qu'un, viande",
 "<p>Un <strong>ERP viande</strong> est un logiciel de gestion qui centralise les processus d'une entreprise de la filière carnée dans un seul outil : achats de matière, réception, découpe et transformation, stocks, préparation de commandes, expédition et facturation.</p>"
 "<p>Pourquoi un outil spécialisé plutôt qu'un ERP généraliste ? Parce que la filière cumule des contraintes qu'un ERP classique ne modélise pas :</p><ul>"
 "<li><strong>Le poids variable</strong> : on entre une carcasse et on sort des pièces de poids tous différents. La facturation doit se faire au poids réellement pesé, pas au poids commandé.</li>"
 "<li><strong>Le rendement matière</strong> : c'est l'indicateur qui décide de la marge, et il doit être suivi par lot et par pièce.</li>"
 "<li><strong>Les DLC courtes</strong>, qui imposent une rotation en FEFO et des alertes avant péremption.</li>"
 "<li><strong>La traçabilité réglementaire</strong> : lot d'abattage, agrément, estampille, origine.</li></ul>"
 "<p>Sans outil spécialisé, ces contraintes se rattrapent à la main : un tableur pour les rendements, un autre pour les DLC, des bons de pesée papier. L'information existe, mais elle arrive trop tard pour décider.</p>"
 "<p>Un dernier point distingue la filière : la <strong>valeur se dégrade vite</strong>. Un retard de décision sur un stock de viande fraîche ne se rattrape pas, contrairement à un produit sec. L'intérêt d'un ERP spécialisé tient donc autant à la fraîcheur de l'information qu'à sa précision.</p><p>C'est aussi ce qui explique que les entreprises de la filière basculent rarement pour des raisons informatiques : elles basculent quand la marge devient illisible, ou après un contrôle qui a montré les limites du suivi papier.</p>"),

("Hello Harel face à un ERP généraliste en filière viande ?", "Hello, Harel, généraliste",
 "<p>La question se pose légitimement : pourquoi un ERP spécialisé plutôt qu'une solution généraliste reconnue ?</p>"
 "<p>Trois différences pèsent au quotidien :</p><ul>"
 "<li><strong>Le modèle de données</strong> : un ERP généraliste raisonne en unités et en poids fixe. Le poids variable s'y ajoute par développement spécifique — coûteux à l'achat, et à maintenir à chaque montée de version.</li>"
 "<li><strong>Le délai de mise en route</strong> : les processus de la filière sont préconfigurés chez Hello Harel, ce qui ramène le déploiement à <strong>4 à 8 semaines</strong>, là où un projet généraliste se compte en mois de paramétrage.</li>"
 "<li><strong>L'expertise de l'éditeur</strong> : nos consultants connaissent le métier et en parlent le vocabulaire — freinte, désossage, muscle, poids variable, estampille. Le cadrage ne consiste pas à leur expliquer votre activité.</li></ul>"
 "<p>Hello Harel est un <strong>ERP SaaS français</strong> dédié à l'agroalimentaire, utilisé par plus de 200 entreprises du secteur et noté 5,0 sur 5 par ses clients. La démonstration se fait sur vos propres pièces et vos propres rendements, pas sur un jeu de données générique.</p>"
 "<p>Reste la question du coût total. Un ERP généraliste affiche souvent une licence attractive, mais le développement spécifique du poids variable, sa maintenance et le temps de paramétrage se rattrapent sur la facture finale — puis se représentent à chaque montée de version.</p><p>La bonne comparaison n'est donc pas licence contre licence, mais coût complet sur trois ans, délai de mise en service inclus.</p>"),
]

PROTEGEES = ["/agroalimentaire/", "/agroalimentaire/traiteur/", "/agroalimentaire/charcutier/",
             "/agroalimentaire/plats-cuisines-industriels/", "/migration-as400/"]


LABELS = {
    "/agroalimentaire/": "Agroalimentaire",
    "/agroalimentaire/traiteur/": "Traiteur",
    "/agroalimentaire/charcutier/": "Charcuterie",
    "/agroalimentaire/plats-cuisines-industriels/": "Plats cuisinés",
    "/migration-as400/": "Migration AS/400",
}


def neutraliser_regle0(c):
    """Regle 0 : pas d'ancre interne EXACT MATCH vers une page protegee.
    On conserve le lien de navigation ; on remplace seulement le libelle optimise
    par le nom de la filiere. Les blocs structurels (cartes avec balises internes)
    ne sont pas des ancres editoriales : on ne les touche pas."""
    n = 0
    def repl(m):
        nonlocal n
        href, inner = m.group(1), m.group(2)
        if href not in PROTEGEES or "<" in inner:
            return m.group(0)
        txt = inner.strip().lower()
        if re.search(r"\berp\s+(agroalimentaire|charcutier|traiteur|viande|plats)\b|"
                     r"\blogiciel\s+(agroalimentaire|charcutier)\b", txt):
            n += 1
            return m.group(0).replace(">" + inner + "<", ">" + LABELS[href] + "<")
        return m.group(0)
    return re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', repl, c, flags=re.S), n


def build():
    c = w.get_raw('pages', SRC)['content']['raw']
    rapport = []
    for old, new, oblig in REPL:
        k = c.count(old)
        if k == 0 and oblig:
            raise SystemExit("Remplacement obligatoire introuvable : %s" % old[:70])
        c = c.replace(old, new)
        rapport.append(("ok x%d" % k, old[:54]))

    # --- FAQ : cartes de la grille ---
    cards = re.findall(r'<div class="faq-card-question">(.*?)</div>', c, re.S)
    for i, old_q in enumerate(cards):
        if i < len(FAQ):
            c = c.replace('<div class="faq-card-question">%s</div>' % old_q,
                          '<div class="faq-card-question">%s</div>' % FAQ[i][0], 1)
    metas = re.findall(r'<div class="faq-card-meta">(.*?)</div>', c, re.S)
    for i, old_m in enumerate(metas):
        if i < len(FAQ):
            c = c.replace('<div class="faq-card-meta">%s</div>' % old_m,
                          '<div class="faq-card-meta">%s</div>' % FAQ[i][1], 1)

    # --- FAQ : panneaux (question + reponse longue) ---
    def panel(m):
        idx = int(m.group(1))
        if idx >= len(FAQ):
            return m.group(0)
        q, _meta, rep = FAQ[idx]
        return ('<div class="faq-drawer-panel" data-faq="%s"%s>\n            <h3>%s</h3>\n'
                '            <div class="faq-drawer-content">%s</div>') % (
                m.group(1), m.group(2), q, rep)
    c, npan = re.subn(
        r'<div class="faq-drawer-panel" data-faq="(\d+)"([^>]*)>\s*<h3>.*?</h3>\s*<div class="faq-drawer-content">.*?</div>',
        panel, c, flags=re.S)

    # --- JSON-LD ---
    def ld(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        t = d.get("@type")
        if t == "FAQPage":
            d["mainEntity"] = [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer",
                                                   "text": re.sub(r'<[^>]+>', ' ', rep).strip()}}
                               for q, _m, rep in FAQ]
        elif t == "BreadcrumbList":
            for e in d.get("itemListElement", []):
                if e.get("name") == "Charcutier":
                    e["name"] = "Viande"
                if isinstance(e.get("item"), str) and e["item"].endswith("/agroalimentaire/charcutier/"):
                    e["item"] = "https://www.helloharel.com/agroalimentaire/viande/"
        else:
            return m.group(0)
        return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)
    c = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, c, flags=re.S)

    c, n0 = neutraliser_regle0(c)
    return c, rapport, n0, npan


def main():
    live = "--live" in sys.argv
    c, rapport, n0, npan = build()
    for etat, frag in rapport:
        print("  [%-6s] %s" % (etat, frag))
    print("\npanneaux FAQ reecrits : %d/6" % npan)
    print("Regle 0 — ancres neutralisees : %d" % n0)
    print("taille : %d caracteres" % len(c))
    # controle de fuite
    fuites = [s for s in re.findall(r'(?i).{60}charcut.{40}', c)
              if '/agroalimentaire/charcutier/' not in s]
    print("FUITES charcuterie (hors liens vers la soeur) : %d" % len(fuites))
    for f in fuites[:6]:
        print("    ...", re.sub(r'\s+', ' ', f)[:112])
    if not live:
        print("\nDRY-RUN — ajouter --live")
        return
    w.update_content('pages', DEST, c, live=True)
    w.api('pages/%d' % DEST, method='POST', data={'title': TITLE})
    print("\nPUBLIE — /agroalimentaire/viande/  |  title :", TITLE)


if __name__ == "__main__":
    main()
