#!/usr/bin/env python3
"""
Cree /agroalimentaire/viande/ — priorite n°1 du brief CLAUDE.md.
Gabarit SXO metier (maquette-sxo-page-metier-hello-harel.html), 8 sections.
Page autonome et LEGERE (sert aussi le ticket T6 : gabarit metier a alleger).
Regle 0 respectee : aucune ancre interne optimisee vers une page protegee
(/agroalimentaire/, /traiteur/, /charcutier/, /plats-cuisines-industriels/, /migration-as400/).
DRY par defaut ; --live pour publier.
"""
import sys, json
import wp_common as w

SLUG = "viande"
PARENT = 1726  # /agroalimentaire/
TITLE = "ERP Viande • Logiciel Découpe, Rendement Matière & Traçabilité"

CSS = """
<style id="hh-viande">
#hhv{--c:#0090c8;--c2:#00B1F5;--ink:#0f172a;--gr:#475569;--gl:#64748b;--bd:#e2e8f0;--bg:#f8fafc;
font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.6}
#hhv *{box-sizing:border-box}
#hhv .w{max-width:1080px;margin:0 auto;padding:0 22px}
#hhv section{padding:clamp(44px,6vw,76px) 0}
#hhv .alt{background:var(--bg)}
#hhv .bc{font-size:.85rem;color:var(--gl);padding-top:26px}
#hhv .bc a{color:var(--gl);text-decoration:none}#hhv .bc a:hover{text-decoration:underline}
#hhv h1{font-size:clamp(1.9rem,4.2vw,3rem);line-height:1.14;font-weight:800;margin:.7rem 0 .9rem;letter-spacing:-.02em}
#hhv h2{font-size:clamp(1.45rem,3vw,2.1rem);line-height:1.2;font-weight:800;margin:0 0 .5rem;letter-spacing:-.01em}
#hhv h3{font-size:1.05rem;font-weight:700;margin:0 0 .35rem}
#hhv .lead{font-size:1.12rem;color:var(--gr);max-width:760px;margin:0 0 1.5rem}
#hhv .sub{color:var(--gr);max-width:760px;margin:0 0 1.9rem}
#hhv .eyebrow{display:inline-block;background:#e0f2fe;color:var(--c);font-weight:700;font-size:.72rem;
letter-spacing:.07em;text-transform:uppercase;padding:.4rem .85rem;border-radius:999px}
#hhv .proof{display:flex;flex-wrap:wrap;gap:10px;margin:1.4rem 0 0}
#hhv .proof span{background:#fff;border:1px solid var(--bd);border-radius:999px;padding:7px 14px;font-size:.88rem;font-weight:600;color:var(--gr)}
#hhv .btn{display:inline-flex;align-items:center;gap:9px;background:linear-gradient(135deg,var(--c),var(--c2));
color:#fff!important;font-weight:800;font-size:1.05rem;padding:15px 28px;border-radius:14px;text-decoration:none;
box-shadow:0 10px 24px rgba(0,144,200,.28)}
#hhv .btn:hover{transform:translateY(-2px);transition:.15s}
/* signature */
#hhv .sig{background:linear-gradient(135deg,#0090c8,#00B1F5);color:#fff;border-radius:24px;padding:clamp(24px,3.4vw,40px);
box-shadow:0 20px 50px rgba(0,120,180,.25)}
#hhv .sig h2{color:#fff}
#hhv .sig p{color:rgba(255,255,255,.94)}
#hhv .calc{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:1.5rem}
#hhv .calc div{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.24);border-radius:14px;padding:16px}
#hhv .calc b{display:block;font-size:1.7rem;font-weight:800;line-height:1.1}
#hhv .calc small{font-size:.85rem;color:rgba(255,255,255,.9)}
/* compare */
#hhv .cmp{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:1.4rem}
#hhv .cmp>div{border-radius:18px;padding:22px 20px;border:1px solid var(--bd);background:#fff}
#hhv .cmp .bad{background:#fff7f7;border-color:#fecaca}
#hhv .cmp .good{background:#f0fdf4;border-color:#bbf7d0}
#hhv .cmp ul{list-style:none;margin:.6rem 0 0;padding:0}
#hhv .cmp li{padding-left:26px;position:relative;margin:0 0 .55rem;font-size:.95rem;color:var(--gr)}
#hhv .cmp .bad li:before{content:"✕";position:absolute;left:0;color:#dc2626;font-weight:800}
#hhv .cmp .good li:before{content:"✓";position:absolute;left:0;color:#16a34a;font-weight:800}
/* fonctions */
#hhv .fx{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:1.4rem}
#hhv .fx article{background:#fff;border:1px solid var(--bd);border-radius:18px;padding:22px 20px}
#hhv .fx .ic{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:12px;
background:linear-gradient(135deg,var(--c),var(--c2));color:#fff;margin-bottom:12px}
#hhv .fx p{color:var(--gl);font-size:.94rem;margin:0}
/* maillage */
#hhv .mesh{margin-top:1.2rem;color:var(--gr);line-height:1.85}
#hhv .mesh a{color:var(--c);font-weight:600;text-decoration:underline}
/* faq */
#hhv details{background:#fff;border:1px solid var(--bd);border-radius:14px;padding:16px 18px;margin:0 0 10px}
#hhv summary{font-weight:700;cursor:pointer;list-style:none}
#hhv summary::-webkit-details-marker{display:none}
#hhv summary:after{content:"+";float:right;color:var(--c);font-weight:800}
#hhv details[open] summary:after{content:"–"}
#hhv details p{color:var(--gr);margin:.7rem 0 0;font-size:.96rem}
#hhv .cta{text-align:center}
#hhv .cta h2{margin-bottom:.6rem}
@media(max-width:780px){#hhv .cmp,#hhv .fx,#hhv .calc{grid-template-columns:1fr}}
</style>
"""

def ic(p):
    return ('<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'style="width:24px;height:24px"><path stroke-linecap="round" stroke-linejoin="round" d="%s"/></svg></span>' % p)

FONCTIONS = [
    ("M4 7h16M4 12h16M4 17h10", "Rendement matière à la découpe",
     "Chaque carcasse, chaque muscle : rendement réel par pièce, par lot et par opérateur. L'écart entre le poids entré et le poids vendu cesse d'être une surprise de fin de mois."),
    ("M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z", "Traçabilité sanitaire et estampille",
     "Numéro d'agrément, estampille, lot d'abattage : traçabilité ascendante et descendante complète, prête pour un rappel produit ou un contrôle des services vétérinaires."),
    ("M3 6l3 1m0 0l-3 9a5 5 0 006 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5 5 0 006 0M18 7l3 9", "Poids variable et pesée",
     "Facturation au poids réel pesé, pas au poids commandé. Étiquettes, bons de pesée et factures parlent enfin le même langage."),
    ("M12 8c-1.7 0-3 .9-3 2s1.3 2 3 2 3 .9 3 2-1.3 2-3 2m0-8V4m0 12v2", "Coût de revient au kilo",
     "Le prix de revient réel au kilo de produit fini : matière, découpe, main-d'œuvre, freinte et emballage compris."),
    ("M8 7V3m8 4V3M3 11h18M5 21h14a2 2 0 002-2V7H3v12a2 2 0 002 2z", "DLC courtes et rotation",
     "Gestion des DLC serrées propres à la viande fraîche, FEFO à la préparation, alertes avant péremption."),
    ("M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10", "Commandes, GMS et EDI",
     "Prise de commande, préparation au poids, expédition et facturation — y compris les contraintes de la grande distribution."),
]

FAQ = [
    ("Qu'est-ce qu'un ERP viande ?",
     "Un ERP viande est un logiciel de gestion conçu pour les entreprises de découpe, transformation et négoce de produits carnés. Il pilote la traçabilité par lot d'abattage, le rendement matière à la découpe, le poids variable, les DLC courtes et le coût de revient au kilo — des contraintes qu'un ERP généraliste ne modélise pas."),
    ("En quoi un ERP viande diffère-t-il d'un ERP classique ?",
     "Un ERP classique raisonne en unités et en poids fixe. La filière viande travaille en poids variable : on entre une carcasse et on sort des pièces de poids différents. Sans gestion native du poids variable et du rendement matière, l'écart se rattrape à la main dans des tableurs."),
    ("Comment est calculé le rendement matière ?",
     "Le rendement est le rapport entre le poids de produit fini obtenu et le poids de matière première engagée, mesuré par lot, par pièce et par opérateur. Suivi en continu, il rend visible la freinte et permet d'arbitrer sur les achats et les techniques de découpe."),
    ("L'ERP gère-t-il la traçabilité réglementaire ?",
     "Oui : lot d'abattage, numéro d'agrément sanitaire, estampille, traçabilité ascendante et descendante. En cas de rappel produit, la liste des clients concernés s'obtient en quelques minutes plutôt qu'en quelques jours."),
    ("Combien de temps dure le déploiement ?",
     "Le déploiement d'Hello Harel se fait généralement en 4 à 10 semaines selon le périmètre et le nombre de sites, avec accompagnement et reprise des données existantes."),
    ("L'ERP fonctionne-t-il en SaaS ?",
     "Oui. Hello Harel est un ERP SaaS français : pas de serveur à administrer, mises à jour incluses, accès depuis l'atelier, le bureau ou en mobilité."),
    ("Convient-il à une PME de 20 à 300 salariés ?",
     "C'est précisément le segment servi : des PME de la filière carnée qui ont dépassé le tableur mais pour qui un ERP d'industriel lourd est disproportionné."),
    ("Peut-on voir l'outil sur nos propres données ?",
     "Oui. La démonstration se fait sur vos cas réels — vos pièces, vos rendements, vos bons de pesée — et non sur un jeu de données générique."),
]

def build():
    fx = "".join(
        '<article>%s<h3>%s</h3><p>%s</p></article>' % (ic(p), t, d)
        for p, t, d in FONCTIONS)
    faq = "".join(
        '<details><summary>%s</summary><p>%s</p></details>' % (q, a)
        for q, a in FAQ)
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
    }
    return (
        CSS +
        '<div id="hhv">'
        # 1 · fil d'Ariane + H1 exact match
        '<div class="w bc">Accueil › Agroalimentaire › <b>Viande</b></div>'
        '<section style="padding-top:14px">'
        '<div class="w">'
        '<span class="eyebrow">Découpe, transformation &amp; négoce de viande</span>'
        '<h1>ERP viande : l\'ERP qui suit le rendement matière, pièce par pièce</h1>'
        '<p class="lead">De la carcasse au colis expédié, Hello Harel pilote le poids variable, '
        'la traçabilité du lot d\'abattage et le coût de revient au kilo — sans reprise sous tableur.</p>'
        '<a class="btn" href="/contact/">Voir l\'ERP sur mes rendements →</a>'
        '<div class="proof"><span>+200 entreprises agroalimentaires équipées</span>'
        '<span>Noté 5,0/5 sur 31 avis</span><span>ERP SaaS français</span>'
        '<span>Déploiement en 4 à 10 semaines</span></div>'
        '</div></section>'
        # 2 · element signature du metier
        '<section class="alt"><div class="w"><div class="sig">'
        '<h2>Ce que vous perdez sur l\'écart de rendement</h2>'
        '<p>En découpe, un point de rendement perdu ne se voit pas à la pièce : il se voit à la fin du mois, '
        'quand la marge ne correspond plus au prix d\'achat. Sur un atelier qui engage 40 tonnes par mois, '
        'un seul point de rendement représente 400 kg de produit fini évaporés.</p>'
        '<div class="calc">'
        '<div><b>40 t</b><small>matière engagée par mois</small></div>'
        '<div><b>1 point</b><small>de rendement perdu</small></div>'
        '<div><b>400 kg</b><small>de produit fini en moins</small></div>'
        '</div>'
        '<p style="margin-top:1.2rem">Hello Harel mesure ce point en continu : par lot, par pièce et par opérateur. '
        'La freinte cesse d\'être un écart constaté pour devenir une donnée pilotable.</p>'
        '</div></div></section>'
        # 3 · ce qu'un ERP generaliste ne sait pas faire
        '<section><div class="w">'
        '<h2>Ce qu\'un ERP généraliste ne sait pas faire en viande</h2>'
        '<p class="sub">Le problème n\'est pas la puissance de l\'outil, c\'est son modèle de données : '
        'un ERP classique raisonne en unités et en poids fixe.</p>'
        '<div class="cmp">'
        '<div class="bad"><h3>ERP généraliste</h3><ul>'
        '<li>Poids fixe : la pièce pèse ce que dit la fiche article</li>'
        '<li>Rendement matière calculé hors système, sous tableur</li>'
        '<li>Traçabilité par référence, pas par lot d\'abattage</li>'
        '<li>Facturation au poids commandé, régularisée après coup</li>'
        '<li>DLC gérée comme une date de stock ordinaire</li>'
        '</ul></div>'
        '<div class="good"><h3>Hello Harel</h3><ul>'
        '<li>Poids variable natif, de la réception à la facture</li>'
        '<li>Rendement suivi par lot, par pièce et par opérateur</li>'
        '<li>Lot d\'abattage, agrément et estampille tracés</li>'
        '<li>Facturation au poids réellement pesé</li>'
        '<li>DLC courtes, FEFO et alertes avant péremption</li>'
        '</ul></div></div>'
        '</div></section>'
        # 4 · les fonctions du metier
        '<section class="alt"><div class="w">'
        '<h2>Six fonctions écrites pour la filière carnée</h2>'
        '<p class="sub">Elles ne sont pas des options : ce sont les contraintes quotidiennes d\'un atelier de découpe.</p>'
        '<div class="fx">%s</div>'
        '</div></section>'
        # 5 · resultats chiffres (a completer avec un client nomme + accord)
        '<section><div class="w">'
        '<h2>Ce que ça change concrètement</h2>'
        '<p class="sub">Trois effets constatés par les entreprises de transformation équipées : '
        'le rendement devient visible en temps réel plutôt qu\'en fin de mois, la traçabilité d\'un rappel '
        'passe de plusieurs jours à quelques minutes, et la facturation au poids réel supprime les avoirs de régularisation.</p>'
        '<a class="btn" href="/contact/">Demander la démonstration →</a>'
        '</div></section>'
        # 6 · maillage (Regle 0 : aucune ancre optimisee vers page protegee)
        '<section class="alt"><div class="w">'
        '<h2>Pour aller plus loin</h2>'
        '<p class="mesh">Les fonctions au cœur de la filière viande : '
        '<a href="/fonctionnalites/gestion-rendement-matiere-logiciel/">logiciel de gestion du rendement matière</a>, '
        '<a href="/fonctionnalites/tracabilite-alimentaire/">logiciel de traçabilité alimentaire</a> et '
        '<a href="/fonctionnalites/fabrication/">logiciel de fabrication agroalimentaire</a>.<br>'
        'Filières voisines qui partagent le poids variable et les DLC courtes : '
        '<a href="/agroalimentaire/poissonnier/">ERP poissonnier</a> et '
        '<a href="/agroalimentaire/conserverie/">ERP conserverie</a>.<br>'
        'Pour comparer les solutions du marché : <a href="/comparatifs/">comparatifs ERP agroalimentaire</a>.</p>'
        '</div></section>'
        # 7 · FAQ deux etages
        '<section><div class="w">'
        '<h2>Les réponses à vos questions</h2>'
        '<div style="margin-top:1.3rem">%s</div>'
        '</div></section>'
        # 8 · CTA
        '<section class="alt cta"><div class="w">'
        '<h2>Voyez-le sur vos propres bons de pesée</h2>'
        '<p class="sub" style="margin:0 auto 1.6rem">30 minutes, sans engagement, avec un interlocuteur '
        'qui connaît la découpe — pas une visite générique du logiciel.</p>'
        '<a class="btn" href="/contact/">Réserver ma démonstration →</a>'
        '</div></section>'
        '</div>'
        '<script type="application/ld+json">%s</script>'
    ) % (fx, faq, json.dumps(faq_ld, ensure_ascii=False))


def main():
    live = "--live" in sys.argv
    content = build()
    existing = w.api("pages?slug=%s&status=any&_fields=id,slug,link" % SLUG)
    print("Taille du contenu : %d caracteres (~%.1f Ko)" % (len(content), len(content)/1024))
    if existing:
        pid = existing[0]["id"]
        print("Page existante id=%s -> mise a jour" % pid)
        if live:
            w.update_content("pages", pid, content, live=True)
        return
    payload = {"title": TITLE, "slug": SLUG, "parent": PARENT,
               "status": "publish", "content": content, "template": "elementor_canvas"}
    if not live:
        print("DRY-RUN — ajouter --live pour publier")
        print("title :", TITLE)
        print("slug  :", SLUG, "| parent :", PARENT)
        return
    r = w.api("pages", method="POST", data=payload)
    print("CREEE id=%s -> %s" % (r.get("id"), r.get("link")))


if __name__ == "__main__":
    main()
