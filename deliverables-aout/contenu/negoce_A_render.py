#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VARIANTE A — rendu « fiche technique editoriale ».
Le contenu vient de negoce_variante_A.py ; ce fichier ne fait que le RENDU.

Direction arretee apres releve concurrentiel (trade-easy, akanea, dashdoc),
design-system ui-ux-pro-max et reperage 21st.dev (19075 hero editorial asymetrique,
9682 gouttiere a label pivote et chiffre fantome) :

  - typo : Instrument Serif (titres) + IBM Plex Sans (corps) + IBM Plex Mono (donnees).
    Plex a un heritage industriel/technique, coherent avec un ERP qui vend de la
    precision sur des poids, des couts et des lots.
  - mise en page : gouttiere a numeros de section, titres alignes a droite,
    bandes images pleine largeur, filets 1px, chiffres tabulaires.
  - ce qu'on s'interdit : degrade, carte arrondie 20px, chip a icone, tout centrer.
    Le cyan de marque ne sert QUE pour les liens et l'unique bouton.
"""
import sys, json, importlib.util

spec = importlib.util.spec_from_file_location("dataA", "negoce_variante_A.py")
D = importlib.util.module_from_spec(spec)
_argv = sys.argv; sys.argv = ["x"]
spec.loader.exec_module(D)
sys.argv = _argv

import wp_common as w

SLUG, TITLE, IMG = D.SLUG, D.TITLE, D.IMG

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style id="hh-vA">
#hva{
 --ink:#10151C; --ink2:#3C4753; --ink3:#79838F;
 --paper:#FCFCFD; --wash:#F2F4F7; --rule:#DCE2E9;
 --acc:#0090C8; --acc-d:#00658C;
 --serif:'Instrument Serif',Georgia,serif;
 --sans:'IBM Plex Sans',system-ui,sans-serif;
 --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
 font-family:var(--sans); color:var(--ink); background:var(--paper);
 font-size:17px; line-height:1.62; -webkit-font-smoothing:antialiased}
#hva *{box-sizing:border-box}
#hva .w{max-width:1200px;margin:0 auto;padding:0 32px}
#hva p{color:var(--ink2);margin:0 0 1rem}
#hva a{color:var(--acc-d);text-decoration:none;border-bottom:1px solid rgba(0,144,200,.34)}
#hva a:hover{border-bottom-color:var(--acc)}
#hva strong,#hva b{font-weight:600;color:var(--ink)}

/* --- gouttiere a numeros : la grille qui tient toute la page --- */
#hva .blk{display:grid;grid-template-columns:112px 1fr;gap:0;
 border-top:1px solid var(--rule);padding:clamp(46px,5.4vw,88px) 0}
#hva .gut{position:sticky;top:24px;align-self:start}
#hva .gut .no{font-family:var(--mono);font-size:.72rem;letter-spacing:.16em;color:var(--acc);
 font-weight:600;display:block;margin-bottom:14px}
#hva .gut .vert{font-family:var(--mono);font-size:.66rem;letter-spacing:.22em;
 text-transform:uppercase;color:var(--ink3);writing-mode:vertical-rl;transform:rotate(180deg)}
#hva .bd{min-width:0}

/* --- titres : serif, alignes a droite sur les grands blocs --- */
#hva h2{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,4.4vw,3.4rem);
 line-height:1.04;letter-spacing:-.012em;color:var(--ink);margin:0 0 1.1rem;max-width:19ch}
#hva h2 em{font-style:italic;color:var(--acc-d)}
#hva h3{font-family:var(--sans);font-size:1.02rem;font-weight:600;margin:0 0 .35rem;
 letter-spacing:-.005em}
#hva .kick{font-family:var(--mono);font-size:.72rem;letter-spacing:.17em;text-transform:uppercase;
 color:var(--ink3);margin:0 0 1.5rem}
#hva .intro{font-size:1.14rem;color:var(--ink2);max-width:62ch}

/* --- HERO : tagline a gauche, titre a droite, bande image dessous --- */
#hva .hero{padding:clamp(40px,5vw,84px) 0 0}
#hva .hero .row{display:grid;grid-template-columns:112px 1fr;gap:0;align-items:start}
#hva .hero .lab{font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ink3);line-height:1.8;padding-top:.9rem}
#hva .hero h1{font-family:var(--serif);font-weight:400;font-size:clamp(2.5rem,6.6vw,5.1rem);
 line-height:.99;letter-spacing:-.02em;margin:0 0 1.3rem;max-width:15ch;color:var(--ink)}
#hva .hero h1 em{font-style:italic;color:var(--acc-d)}
#hva .hero .sub{font-size:1.16rem;max-width:56ch;color:var(--ink2)}
#hva .band{margin-top:clamp(34px,4.2vw,64px);height:clamp(240px,32vw,420px);overflow:hidden;
 border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
#hva .band img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.92)}

/* --- bandeau de preuve en mono --- */
#hva .facts{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--rule)}
#hva .facts div{padding:22px 26px;border-right:1px solid var(--rule)}
#hva .facts div:last-child{border-right:none}
#hva .facts .n{font-family:var(--mono);font-size:1.42rem;font-weight:600;color:var(--ink);
 font-variant-numeric:tabular-nums;line-height:1}
#hva .facts .l{font-size:.83rem;color:var(--ink3);margin-top:7px;line-height:1.4}

/* --- le calcul : tableau technique, pas une carte --- */
#hva .calc{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(28px,4vw,60px);align-items:start}
#hva table.led{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:.9rem}
#hva table.led caption{font-family:var(--mono);font-size:.7rem;letter-spacing:.15em;
 text-transform:uppercase;color:var(--ink3);text-align:left;padding-bottom:12px}
#hva table.led td{padding:11px 0;border-bottom:1px solid var(--rule);color:var(--ink2)}
#hva table.led td:last-child{text-align:right;font-variant-numeric:tabular-nums;color:var(--ink);font-weight:500}
#hva table.led tr.sum td{border-top:2px solid var(--ink);border-bottom:none;padding-top:15px;
 color:var(--ink);font-weight:600;font-size:1.02rem}
#hva table.led tr.coef td{border-bottom:none;padding-top:3px;color:var(--acc-d);font-weight:600}
#hva .cap{font-family:var(--mono);font-size:.74rem;line-height:1.65;color:var(--ink3);margin-top:14px}

/* --- fonctions : liste numerotee a filets, PAS de cartes --- */
#hva .fx{border-top:1px solid var(--rule);margin-top:2rem}
#hva .fx .it{display:grid;grid-template-columns:56px 1fr;gap:0;
 padding:26px 0;border-bottom:1px solid var(--rule)}
#hva .fx .k{font-family:var(--mono);font-size:.78rem;color:var(--acc);font-weight:600;padding-top:.25rem}
#hva .fx p{margin:0;font-size:.98rem;color:var(--ink2);max-width:66ch}

/* --- triptyque plein cadre, angles droits --- */
#hva .trip{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);
 border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-top:2rem}
#hva .trip figure{margin:0;background:var(--paper)}
#hva .trip img{width:100%;aspect-ratio:5/4;object-fit:cover;display:block;filter:saturate(.92)}
#hva .trip figcaption{padding:18px 22px;font-size:.92rem;color:var(--ink2);line-height:1.55}
#hva .trip .t{font-family:var(--mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;
 color:var(--acc);display:block;margin-bottom:6px}

/* --- comparatif : grille technique --- */
#hva .cmpw{overflow-x:auto;margin-top:2rem;border-top:1px solid var(--ink)}
#hva table.cmp{width:100%;border-collapse:collapse;font-size:.94rem;min-width:660px}
#hva table.cmp th{text-align:left;padding:14px 18px 14px 0;font-family:var(--mono);font-size:.7rem;
 letter-spacing:.13em;text-transform:uppercase;color:var(--ink3);font-weight:500;
 border-bottom:1px solid var(--rule);vertical-align:bottom}
#hva table.cmp th:last-child{color:var(--acc)}
#hva table.cmp td{padding:13px 18px 13px 0;border-bottom:1px solid var(--rule);color:var(--ink2)}
#hva table.cmp td:first-child{color:var(--ink);font-weight:500;width:30%}
#hva table.cmp td:last-child{color:var(--ink);font-weight:500}
#hva table.cmp tr:hover td{background:var(--wash)}

/* --- index du silo --- */
#hva .idx{border-top:1px solid var(--rule);margin-top:2rem}
#hva .idx a{display:grid;grid-template-columns:56px 1fr auto;gap:0;align-items:baseline;
 padding:22px 0;border-bottom:1px solid var(--rule);border-bottom-color:var(--rule);
 color:var(--ink);transition:padding-left .18s ease}
#hva .idx a:hover{padding-left:10px;background:var(--wash)}
#hva .idx .k{font-family:var(--mono);font-size:.78rem;color:var(--acc);font-weight:600}
#hva .idx .t{font-size:1.06rem;font-weight:600}
#hva .idx .d{display:block;font-weight:400;font-size:.93rem;color:var(--ink3);margin-top:3px;max-width:56ch}
#hva .idx .ar{font-family:var(--mono);color:var(--acc);font-size:.9rem}

/* --- FAQ a filets --- */
#hva .qa{border-top:1px solid var(--rule);margin-top:2rem}
#hva details{border-bottom:1px solid var(--rule)}
#hva summary{list-style:none;cursor:pointer;padding:20px 0;font-weight:600;font-size:1.02rem;
 display:flex;justify-content:space-between;gap:22px;align-items:baseline}
#hva summary::-webkit-details-marker{display:none}
#hva summary:after{content:"+";font-family:var(--mono);color:var(--acc);font-weight:500;flex:0 0 auto}
#hva details[open] summary:after{content:"\\2212"}
#hva details p{padding:0 0 22px;max-width:70ch;font-size:.98rem}

/* --- CTA plein cadre --- */
#hva .end{background:var(--ink);color:#fff;margin-top:0}
#hva .end .in{display:grid;grid-template-columns:1.1fr .9fr;align-items:center;gap:clamp(28px,4vw,58px);
 padding:clamp(48px,5.6vw,86px) 0}
#hva .end h2{color:#fff;margin-bottom:.9rem}
#hva .end p{color:rgba(255,255,255,.72);max-width:48ch}
#hva .end img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;filter:saturate(.9)}
#hva .cta{display:inline-block;font-family:var(--mono);font-size:.86rem;letter-spacing:.1em;
 text-transform:uppercase;font-weight:600;background:var(--acc);color:#fff!important;
 padding:17px 34px;border:none;margin-top:.7rem;transition:background .18s ease}
#hva .cta:hover{background:#00a6e6}
#hva .cta.line{background:transparent;color:var(--acc-d)!important;border:1px solid var(--rule);padding:15px 28px}
#hva .cta.line:hover{border-color:var(--acc);background:transparent}
#hva a.cta{border-bottom:none}
#hva .note{font-family:var(--mono);font-size:.76rem;background:var(--wash);
 border-left:2px solid var(--acc);padding:14px 18px;color:var(--ink2);margin:0}
#hva :focus-visible{outline:2px solid var(--acc);outline-offset:3px}
@media(prefers-reduced-motion:reduce){#hva *{transition:none!important}}
@media(max-width:940px){
 #hva .blk,#hva .hero .row{grid-template-columns:1fr}
 #hva .gut{position:static;display:flex;gap:14px;align-items:center;margin-bottom:18px}
 #hva .gut .vert{writing-mode:horizontal-tb;transform:none}
 #hva .gut .no{margin:0}
 #hva .hero .lab{padding-top:0;margin-bottom:1.1rem}
 #hva .calc,#hva .trip,#hva .end .in{grid-template-columns:1fr}
 #hva .facts{grid-template-columns:1fr 1fr}
 #hva .facts div:nth-child(2){border-right:none}
 #hva h2{max-width:none}
}
</style>
"""

def blk(no, label, inner):
    return ('<div class="blk"><div class="gut"><span class="no">%s</span>'
            '<span class="vert">%s</span></div><div class="bd">%s</div></div>') % (no, label, inner)


def build():
    # fonctions en liste numerotee a filets
    fx = "".join(
        '<div class="it"><div class="k">%02d</div><div><h3>%s</h3><p>%s</p></div></div>'
        % (i, t, d) for i, (_p, t, d) in enumerate(D.CARTES, 1))

    idx = "".join(
        '<a href="%s"><span class="k">%02d</span><span class="t">%s<span class="d">%s</span></span>'
        '<span class="ar">&rarr;</span></a>' % (u, i, a, d)
        for i, (u, a, d) in enumerate(D.FILLES, 1))

    qa = "".join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in D.FAQ)

    head, rows = D.COMPARATIF[0], D.COMPARATIF[1:]
    cmp_t = ('<table class="cmp"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (
        "".join("<th>%s</th>" % c for c in head),
        "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)))

    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in D.FAQ]}

    body = (
'<div id="hva">'
'<div class="w" style="padding-top:26px"><p class="note">VARIANTE A — test A/B, brouillon non indexé. '
'Ne pas publier sans avoir posé le noindex.</p></div>'

# HERO
'<header class="hero"><div class="w"><div class="row">'
'<div class="lab">Import<br>Export<br>Alimentaire</div>'
'<div><h1>Le prix payé au fournisseur n\'est <em>jamais</em> votre coût.</h1>'
'<p class="sub">Hello Harel répartit le fret, les droits de douane, l\'assurance et l\'écart de '
'change sur chaque référence du conteneur — à la réception, pas au bilan. Vous connaissez votre '
'coût de revient au kilo avant la première vente.</p>'
'<a class="cta" href="/contact/">Voir sur mes opérations</a></div>'
'</div></div>'
'<div class="band"><img src="%(hero)s" alt="Entrepôt de négoce alimentaire, palettes et préparation de commandes" loading="eager"></div>'
'<div class="w"><div class="facts">'
'<div><div class="n">200+</div><div class="l">entreprises agroalimentaires équipées</div></div>'
'<div><div class="n">5,0/5</div><div class="l">sur 31 avis clients</div></div>'
'<div><div class="n">2014</div><div class="l">édité en France depuis</div></div>'
'<div><div class="n">4–8 sem.</div><div class="l">du cadrage à la bascule</div></div>'
'</div></div></header>'

'<div class="w">'

# 01 · LE CALCUL
+ blk("§ 01", "Le calcul", (
 '<p class="kick">Ce que personne ne vous montre</p>'
 '<h2>Sur un conteneur, l\'écart dépasse <em>20 %%</em>.</h2>'
 '<p class="intro">Tant que la répartition des frais d\'approche se fait dans un tableur, après '
 'coup, la marge inscrite sur vos factures est une estimation. Voici le calcul, poste par poste.</p>'
 '<div class="calc"><div>'
 '<table class="led"><caption>Conteneur 20 pieds — exemple</caption><tbody>'
 '<tr><td>Marchandise, prix fournisseur</td><td>32 000 €</td></tr>'
 '<tr><td>Fret maritime</td><td>2 400 €</td></tr>'
 '<tr><td>Assurance transport</td><td>310 €</td></tr>'
 '<tr><td>Droits de douane</td><td>2 560 €</td></tr>'
 '<tr><td>Transitaire, frais de dossier</td><td>640 €</td></tr>'
 '<tr><td>Écart de change au règlement</td><td>480 €</td></tr>'
 '<tr class="sum"><td>Coût de revient réel</td><td>38 390 €</td></tr>'
 '<tr class="coef"><td>Coefficient appliqué</td><td>× 1,20</td></tr>'
 '</tbody></table>'
 '<p class="cap">Exemple illustratif. Les postes et la clé de répartition — au poids, à la valeur '
 'ou au volume — se paramètrent par type d\'opération.</p></div>'
 '<div><h3>Ce que ça change concrètement</h3>'
 '<p>Vendre à <b>+15 %%</b> du prix fournisseur, sur cet exemple, c\'est vendre <b>à perte</b>. '
 'C\'est l\'erreur la plus fréquente du négoce à l\'import, et elle ne se voit pas ligne à ligne : '
 'elle se voit à la fin du trimestre, quand la marge globale ne correspond plus aux marges affichées.</p>'
 '<p>Hello Harel applique le coefficient <b>à la réception</b>, référence par référence. La marge '
 'se lit ensuite par conteneur, par client et par référence — pas seulement en cumul.</p>'
 '<a class="cta line" href="%(land)s">Le module import export</a></div></div>'))

# 02 · LES FONCTIONS
+ blk("§ 02", "Fonctions", (
 '<p class="kick">Huit terrains de vérité</p>'
 '<h2>Là où les outils généralistes <em>s\'arrêtent</em>.</h2>'
 '<p class="intro">Ce ne sont pas des options : ce sont les points sur lesquels un ERP généraliste '
 'facture un développement spécifique, et sur lesquels un TMS ne se prononce pas.</p>'
 '<div class="fx">%(fx)s</div>'))

# 03 · LE TERRAIN
+ blk("§ 03", "Terrain", (
 '<p class="kick">Réception, contrôle, préparation</p>'
 '<h2>L\'outil ne vit pas dans un bureau.</h2>'
 '<p class="intro">Il vit sur le quai, au contrôle et à la préparation. C\'est là qu\'il fait '
 'gagner du temps — ou qu\'il en fait perdre.</p>'
 '<div class="trip">'
 '<figure><img src="%(t1)s" alt="Réception de marchandise en entrepôt de négoce alimentaire" loading="lazy">'
 '<figcaption><span class="t">À la réception</span>Pesée, contrôle de température et affectation '
 'du lot dès le quai, sur terminal mobile.</figcaption></figure>'
 '<figure><img src="%(t2)s" alt="Contrôle qualité et agréage sur palettes" loading="lazy">'
 '<figcaption><span class="t">Au contrôle</span>Agréage, écarts constatés et photos rattachées au '
 'lot, opposables au fournisseur.</figcaption></figure>'
 '<figure><img src="%(t3)s" alt="Préparation de commandes et expédition" loading="lazy">'
 '<figcaption><span class="t">À la préparation</span>Picking en FEFO, poids réel saisi à la pesée, '
 'bon de livraison édité dans la foulée.</figcaption></figure>'
 '</div>'))

# 04 · TMS / ERP
+ blk("§ 04", "Se situer", (
 '<p class="kick">TMS, ERP généraliste, ERP métier</p>'
 '<h2>Trois outils, trois problèmes <em>différents</em>.</h2>'
 '<p class="intro">La confusion est fréquente parce que les trois parlent d\'import-export. '
 'Un TMS sait où est la marchandise ; un ERP métier sait ce qu\'elle coûte et ce qu\'elle rapporte.</p>'
 '<div class="cmpw">%(cmp)s</div>'))

# 05 · LE SILO
+ blk("§ 05", "Modules", (
 '<p class="kick">Par où entrer</p>'
 '<h2>Chaque brique du négoce a <em>sa page</em>.</h2>'
 '<div class="idx">%(idx)s</div>'))

# 06 · FAQ
+ blk("§ 06", "Questions", (
 '<p class="kick">Les réponses</p>'
 '<h2>Ce qu\'on nous demande <em>avant</em> de choisir.</h2>'
 '<div class="qa">%(qa)s</div>'))

+ '</div>'

# CTA
'<section class="end"><div class="w"><div class="in"><div>'
'<p class="kick" style="color:rgba(255,255,255,.5)">Démonstration</p>'
'<h2>Voyez-le sur vos propres conteneurs.</h2>'
'<p>30 minutes, sans engagement, avec quelqu\'un qui connaît les incoterms, les frais d\'approche '
'et les contraintes de la marchandise alimentaire. On part de vos opérations réelles.</p>'
'<a class="cta" href="/contact/">Réserver la démonstration</a></div>'
'<div><img src="%(demo)s" alt="Responsable d\'exploitation en site agroalimentaire" loading="lazy"></div>'
'</div></div></section>'
'</div>'
'<script type="application/ld+json">%(ld)s</script>'
) % {"hero": IMG["hero"], "t1": IMG["t1"], "t2": IMG["t2"], "t3": IMG["t3"], "demo": IMG["demo"],
     "land": D.LANDING if hasattr(D, "LANDING") else "/fonctionnalites/import-export/",
     "fx": fx, "idx": idx, "qa": qa, "cmp": cmp_t,
     "ld": json.dumps(ld, ensure_ascii=False)}

    return CSS + body


def main():
    live = "--live" in sys.argv
    c = build()
    import re
    mots = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', c, flags=re.S)).split())
    print("taille %d car. | mots %d | images %d" % (len(c), mots, len(re.findall(r'<img ', c))))
    for tag in ('div', 'section', 'table', 'figure', 'details', 'header'):
        o = len(re.findall(r'<%s[\s>]' % tag, c)); f = len(re.findall(r'</%s>' % tag, c))
        if o != f: print("  DESEQUILIBRE <%s> %d/%d" % (tag, o, f))
    print("degrade:", c.count('gradient'), "| border-radius:", c.count('border-radius'),
          "| ancres neutres:", len(re.findall(r'>(?:En savoir plus|Voir la page)<', c)))
    if not live:
        print("DRY-RUN — ajouter --live"); return
    ex = w.api("pages?slug=%s&status=any&_fields=id,status" % SLUG)
    w.update_content("pages", ex[0]["id"], c, live=True)
    print("MISE A JOUR id=%s (%s)" % (ex[0]["id"], ex[0]["status"]))


if __name__ == "__main__":
    main()
