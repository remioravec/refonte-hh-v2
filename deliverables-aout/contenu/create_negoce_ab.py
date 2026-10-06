#!/usr/bin/env python3
"""
Variante A/B SXO de /negoce/ — BROUILLON NOINDEX.

HYPOTHESE (donnees GSC 15/05->12/08/2026) :
  Le silo /negoce/ fait 173 impressions et 0 clic ; la mere plafonne en position
  51,7 sur « erp negoce » et attire le negoce BTP (« erp negoce plomberie et
  chauffage », « erp negoce sanitaires et decoration »), pas l'alimentaire.
  Sa tete est ecartee (orisha.com, autorite 78 > seuil 60).
  A cote, l'univers import-export est DEJA en page 1 sans un seul clic :
  « erp import export » pos 9,6 (143 impr) · « erp importateur » pos 9,2 (60) ·
  « logiciel import export » pos 13,5 (449) · « logiciel gestion commerciale
  import export » pos 13,2 (176). Total ~1 100 impressions, 0 clic.

  => On teste le reciblage de la page vers l'import-export alimentaire,
     avec une mise en page SXO : reponse des le premier ecran, preuve chiffree,
     et le silo des 5 pages filles remonte en preuve fonctionnelle.

Statut : brouillon (inaccessible au public, donc non indexable).
Au moment de publier pour le test : appliquer le noindex (snippet fourni).
DRY par defaut ; --live pour creer.
"""
import sys, json
import wp_common as w

SLUG = "negoce-test-a-import-export"
PARENT = 0
TITLE = "[TEST A] ERP Import Export • Négoce Alimentaire • Douane & Traçabilité"

# les 5 pages filles du silo /negoce/ — maillage exact-match
FILLES = [
    ("/negoce/achats-approvisionnements/", "achats et approvisionnements",
     "Cadenciers fournisseurs, contrats d'achat, devises et incoterms."),
    ("/negoce/ventes-devis-commandes/", "ventes, devis et commandes",
     "Télévente, devis multi-devises, commandes clients et bons de livraison."),
    ("/negoce/stocks-multi-depots/", "stocks multi-dépôts",
     "Plusieurs entrepôts, transit, sous douane et stock en cours de route."),
    ("/negoce/tracabilite-lots/", "traçabilité des lots",
     "Lot d'origine, pays de provenance, certificats et rappel produit."),
    ("/negoce/tarifs-reporting-edi/", "tarifs, reporting et EDI",
     "Grilles tarifaires par client, échanges EDI et reporting de marge."),
]

FAQ = [
 ("Qu'est-ce qu'un ERP import export ?",
  "Un ERP import export est un logiciel de gestion qui pilote les flux de marchandises entre plusieurs pays : achats en devises, incoterms, transit et dédouanement, stock sous douane, traçabilité de l'origine et facturation multi-devises. Pour une entreprise alimentaire, il ajoute la gestion des lots, des DLC et des certificats sanitaires."),
 ("En quoi diffère-t-il d'un ERP de gestion commerciale classique ?",
  "Un ERP classique raisonne en une devise, un entrepôt et un prix d'achat fixe. À l'import-export, le coût de revient d'une marchandise intègre le transport, les droits de douane, l'assurance et le taux de change du jour : sans ces éléments, la marge affichée est fausse."),
 ("L'ERP gère-t-il les incoterms et le dédouanement ?",
  "Oui. Chaque ligne d'achat porte son incoterm, ce qui détermine à quel moment la marchandise entre dans votre coût et dans votre stock. Le stock sous douane est suivi séparément du stock disponible à la vente."),
 ("Comment est calculé le coût de revient à l'import ?",
  "Le prix payé au fournisseur est majoré des frais d'approche réels — fret, assurance, droits, frais de dossier — répartis au prorata sur chaque référence du conteneur. Le coût obtenu est celui sur lequel se calcule la marge."),
 ("La traçabilité de l'origine est-elle couverte ?",
  "Lot fournisseur, pays d'origine, certificats sanitaires et phytosanitaires sont attachés au lot et remontent jusqu'au client livré, ce qui permet de répondre à un contrôle ou à un rappel sans reconstitution manuelle."),
 ("L'ERP fonctionne-t-il en multi-devises ?",
  "Oui, avec le taux de change à la date de l'opération et l'écart de change constaté au règlement, pour que la marge réelle soit connue et non estimée."),
 ("Convient-il à une PME de négoce alimentaire ?",
  "C'est le segment servi : des importateurs, exportateurs et grossistes alimentaires qui ont dépassé le tableur mais pour qui un ERP d'industriel lourd est disproportionné."),
]

CSS = """
<style id="hh-ab">
#hhab{--c:#0090c8;--c2:#00B1F5;--ink:#0f172a;--gr:#475569;--gl:#64748b;--bd:#e2e8f0;--bg:#f8fafc;
font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:var(--ink);line-height:1.6}
#hhab *{box-sizing:border-box}
#hhab .w{max-width:1080px;margin:0 auto;padding:0 22px}
#hhab section{padding:clamp(40px,5.5vw,70px) 0}
#hhab .alt{background:var(--bg)}
#hhab h1{font-size:clamp(1.85rem,4vw,2.85rem);line-height:1.14;font-weight:800;letter-spacing:-.02em;margin:.7rem 0 .8rem}
#hhab h2{font-size:clamp(1.4rem,2.9vw,2rem);line-height:1.2;font-weight:800;margin:0 0 .5rem;letter-spacing:-.01em}
#hhab h3{font-size:1.02rem;font-weight:700;margin:0 0 .3rem}
#hhab .eyebrow{display:inline-block;background:#e0f2fe;color:var(--c);font-weight:700;font-size:.72rem;
letter-spacing:.07em;text-transform:uppercase;padding:.4rem .85rem;border-radius:999px}
#hhab .lead{font-size:1.1rem;color:var(--gr);max-width:760px;margin:0 0 1.4rem}
#hhab .sub{color:var(--gr);max-width:740px;margin:0 0 1.7rem}
#hhab .btn{display:inline-flex;align-items:center;gap:9px;background:linear-gradient(135deg,var(--c),var(--c2));
color:#fff!important;font-weight:800;font-size:1.04rem;padding:15px 28px;border-radius:14px;text-decoration:none;
box-shadow:0 10px 24px rgba(0,144,200,.26)}
#hhab .proof{display:flex;flex-wrap:wrap;gap:10px;margin:1.3rem 0 0}
#hhab .proof span{background:#fff;border:1px solid var(--bd);border-radius:999px;padding:7px 14px;font-size:.87rem;font-weight:600;color:var(--gr)}
/* reponse premier ecran — le coeur du SXO */
#hhab .answer{background:linear-gradient(135deg,#0090c8,#00B1F5);color:#fff;border-radius:24px;
padding:clamp(22px,3.2vw,38px);box-shadow:0 20px 50px rgba(0,120,180,.24);margin-top:1.6rem}
#hhab .answer h2{color:#fff;font-size:clamp(1.2rem,2.4vw,1.6rem)}
#hhab .answer p{color:rgba(255,255,255,.95);margin:.4rem 0 0;max-width:none}
#hhab .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:1.4rem}
#hhab .kpis div{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.24);border-radius:14px;padding:15px}
#hhab .kpis b{display:block;font-size:1.55rem;font-weight:800;line-height:1.1}
#hhab .kpis small{font-size:.83rem;color:rgba(255,255,255,.9)}
/* comparatif */
#hhab .cmp{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:1.3rem}
#hhab .cmp>div{border-radius:18px;padding:21px 19px;border:1px solid var(--bd);background:#fff}
#hhab .cmp .bad{background:#fff7f7;border-color:#fecaca}
#hhab .cmp .good{background:#f0fdf4;border-color:#bbf7d0}
#hhab .cmp ul{list-style:none;margin:.55rem 0 0;padding:0}
#hhab .cmp li{padding-left:25px;position:relative;margin:0 0 .5rem;font-size:.94rem;color:var(--gr)}
#hhab .cmp .bad li:before{content:"\\2715";position:absolute;left:0;color:#dc2626;font-weight:800}
#hhab .cmp .good li:before{content:"\\2713";position:absolute;left:0;color:#16a34a;font-weight:800}
/* silo — maillage descendant */
#hhab .silo{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:1.3rem}
#hhab .silo a{display:block;background:#fff;border:1px solid var(--bd);border-radius:16px;padding:19px 20px;
text-decoration:none;transition:border-color .15s,transform .15s}
#hhab .silo a:hover{border-color:var(--c);transform:translateY(-2px)}
#hhab .silo h3{color:var(--c)}
#hhab .silo p{color:var(--gl);font-size:.92rem;margin:0}
#hhab details{background:#fff;border:1px solid var(--bd);border-radius:14px;padding:15px 18px;margin:0 0 10px}
#hhab summary{font-weight:700;cursor:pointer;list-style:none}
#hhab summary::-webkit-details-marker{display:none}
#hhab summary:after{content:"+";float:right;color:var(--c);font-weight:800}
#hhab details[open] summary:after{content:"\\2013"}
#hhab details p{color:var(--gr);margin:.6rem 0 0;font-size:.95rem}
#hhab .cta{text-align:center}
#hhab .note{background:#fffbeb;border:1px solid #fde68a;color:#92400e;border-radius:12px;
padding:14px 18px;font-size:.9rem;margin:0 0 6px}
@media(max-width:780px){#hhab .cmp,#hhab .silo,#hhab .kpis{grid-template-columns:1fr}}
</style>
"""

def build():
    silo = "".join(
        '<a href="%s"><h3>%s</h3><p>%s</p></a>' % (u, lbl, d)
        for u, lbl, d in FILLES)
    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQ)
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    ld_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://www.helloharel.com/"},
        {"@type": "ListItem", "position": 2, "name": "Négoce",
         "item": "https://www.helloharel.com/negoce/"},
        {"@type": "ListItem", "position": 3, "name": "Import export"}]}
    return (
        CSS +
        '<div id="hhab">'
        '<section class="w" style="padding-bottom:0">'
        '<p class="note"><b>Variante A — test A/B, brouillon non indexé.</b> '
        'Hypothèse testée : recibler la page du négoce vers l’import-export alimentaire, '
        'déjà en page 1 sans clic. Ne pas publier sans avoir posé le noindex.</p>'
        '</section>'
        # 1 · hero + reponse immediate (SXO)
        '<section style="padding-top:18px"><div class="w">'
        '<span class="eyebrow">Import-export alimentaire</span>'
        '<h1>ERP import export pour le négoce alimentaire</h1>'
        '<p class="lead">Achats en devises, incoterms, stock sous douane, coût de revient réel '
        'au conteneur et traçabilité de l’origine — le tout dans un seul outil, sans reprise sous tableur.</p>'
        '<a class="btn" href="/contact/">Voir l’ERP sur mes flux d’import →</a>'
        '<div class="proof"><span>+200 entreprises agroalimentaires équipées</span>'
        '<span>Noté 5,0/5 sur 31 avis</span><span>ERP SaaS français</span>'
        '<span>Déploiement en 4 à 8 semaines</span></div>'
        '<div class="answer">'
        '<h2>La réponse en une phrase</h2>'
        '<p>Un ERP import-export calcule le <b>coût de revient réel</b> d’une marchandise importée — '
        'prix fournisseur, fret, droits de douane, assurance et écart de change répartis sur chaque '
        'référence du conteneur — puis suit cette marchandise du transit au client livré, lot par lot.</p>'
        '<div class="kpis">'
        '<div><b>Multi-devises</b><small>taux à la date de l’opération, écart de change au règlement</small></div>'
        '<div><b>Sous douane</b><small>stock en transit suivi séparément du stock vendable</small></div>'
        '<div><b>Lot &amp; origine</b><small>certificats et pays de provenance jusqu’au client</small></div>'
        '</div></div>'
        '</div></section>'
        # 2 · ce qu'un ERP generaliste ne sait pas faire
        '<section class="alt"><div class="w">'
        '<h2>Ce qu’un ERP généraliste ne sait pas faire à l’import</h2>'
        '<p class="sub">Le problème n’est pas la puissance de l’outil, c’est son modèle : '
        'une devise, un entrepôt, un prix d’achat fixe.</p>'
        '<div class="cmp">'
        '<div class="bad"><h3>ERP de gestion commerciale classique</h3><ul>'
        '<li>Une seule devise, conversion faite à la main</li>'
        '<li>Frais d’approche saisis hors système, marge estimée</li>'
        '<li>Pas de distinction entre stock sous douane et stock vendable</li>'
        '<li>Incoterm absent : on ne sait pas quand la marchandise devient vôtre</li>'
        '<li>Traçabilité par référence, pas par lot d’origine</li>'
        '</ul></div>'
        '<div class="good"><h3>Hello Harel</h3><ul>'
        '<li>Multi-devises natif, écart de change constaté au règlement</li>'
        '<li>Fret, droits et assurance répartis au prorata sur le conteneur</li>'
        '<li>Transit, sous douane et disponible suivis séparément</li>'
        '<li>Incoterm porté par la ligne d’achat</li>'
        '<li>Lot fournisseur, pays d’origine et certificats attachés</li>'
        '</ul></div></div>'
        '</div></section>'
        # 3 · le silo remonte en preuve fonctionnelle (maillage descendant exact-match)
        '<section><div class="w">'
        '<h2>Les cinq briques du négoce, une page chacune</h2>'
        '<p class="sub">Chaque fonction a sa page dédiée : voici par où entrer selon ce que '
        'vous cherchez à régler en premier.</p>'
        f'<div class="silo">{silo}</div>'
        '</div></section>'
        # 4 · FAQ
        '<section class="alt"><div class="w">'
        '<h2>Les réponses à vos questions</h2>'
        f'<div style="margin-top:1.2rem">{faq}</div>'
        '</div></section>'
        # 5 · CTA
        '<section class="cta"><div class="w">'
        '<h2>Voyez-le sur vos propres conteneurs</h2>'
        '<p class="sub" style="margin:0 auto 1.5rem">30 minutes, sans engagement, avec quelqu’un '
        'qui connaît les incoterms et le dédouanement.</p>'
        '<a class="btn" href="/contact/">Réserver ma démonstration →</a>'
        '</div></section>'
        '</div>'
        '<script type="application/ld+json">%s</script>'
        '<script type="application/ld+json">%s</script>'
    ) % (json.dumps(ld_faq, ensure_ascii=False), json.dumps(ld_bc, ensure_ascii=False))


def main():
    live = "--live" in sys.argv
    c = build()
    print("taille : %d caracteres (~%.1f Ko)" % (len(c), len(c) / 1024))
    ex = w.api("pages?slug=%s&status=any&_fields=id,link,status" % SLUG)
    if ex:
        pid = ex[0]["id"]
        print("existe deja id=%s (%s)" % (pid, ex[0]["status"]))
        if live:
            w.update_content("pages", pid, c, live=True)
            print("mise a jour")
        return
    if not live:
        print("DRY-RUN — ajouter --live")
        print("slug :", SLUG, "| statut : draft (non indexable)")
        return
    r = w.api("pages", method="POST", data={
        "title": TITLE, "slug": SLUG, "parent": PARENT,
        "status": "draft", "content": c, "template": "elementor_canvas"})
    print("CREEE id=%s statut=%s -> %s" % (r.get("id"), r.get("status"), r.get("link")))


if __name__ == "__main__":
    main()
