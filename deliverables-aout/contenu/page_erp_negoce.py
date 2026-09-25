#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mise a jour de /agroalimentaire/negoce-alimentaire/ (page 10934) — requete
« erp negoce alimentaire », persona dirigeant de PME grossiste ou distributeur.

Ce que le script pose :
  1. le H1, qui annoncait « votre production » sur une page destinee a des
     entreprises qui ne produisent pas, et l'accroche du hero ;
  2. une section d'attention au-dessus du deuxieme ecran : reponse en une
     phrase, delais de paiement legaux en chiffres sources, calculateur de la
     marge reelle sur une ligne a poids variable, tableau des delais par nature
     de produit ;
  3. les sept reponses de FAQ. Les six existantes venaient du gabarit maraicher
     — elles parlaient de calibres, de saisonnalite, de fraises et de melons
     sous des questions qui, elles, portaient bien sur le negoce. Le JSON-LD
     envoye a Google portait lui aussi les questions du maraicher ;
  4. la carte de fonctionnalites qui renvoyait vers l'ERP maraicher.

La section reprend les classes du gabarit (section-header, overline, about-card,
about-stats, about-stat-card, stat-number, stat-label, section-tag, bento-card,
tilted-icon) : aucune direction artistique parallele n'est creee.

Usage :  python3 page_erp_negoce.py            (essai a blanc)
         python3 page_erp_negoce.py --live     (ecriture)
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)

import wp_common as w
import negoce_contenu as C

PAGE = 10934
LIVE = "--live" in sys.argv
SAUV = os.path.join(ICI, "backup-negoce-alim-10934.html")

CSS = """<style>
#hh-page .hnb-section{padding:clamp(4.5rem,9vw,8rem) 0!important;background:#fff!important;display:block!important}
#hh-page .hnb-section .section-header>p{max-width:740px!important}
#hh-page .hnb-stats{max-width:940px!important;margin:0 auto 0.75rem!important}
#hh-page .hnb-section .about-stat-card{border:1px solid rgba(0,0,0,0.06)!important}
#hh-page .hnb-stats .stat-number{font-size:1.85rem!important}
#hh-page .hnb-src{color:var(--hh-slate-500)!important;font-size:0.8125rem!important;line-height:1.65!important;margin:0.75rem 0 0!important}
#hh-page .hnb-src-top{text-align:center!important;max-width:760px!important;margin:0 auto 3rem!important}
#hh-page .hnb-block{max-width:1080px!important;margin:0 auto!important}
#hh-page .hnb-calc{margin-bottom:1.5rem!important}
#hh-page .hnb-calc h3{font-size:clamp(1.35rem,2.4vw,1.75rem)!important;font-weight:900!important;letter-spacing:-0.02em!important;color:var(--hh-slate-900)!important;line-height:1.2!important;margin:0 0 0.75rem!important}
#hh-page .hnb-calc>.about-card-inner>p.hnb-intro{color:var(--hh-slate-600)!important;font-size:1rem!important;line-height:1.75!important;margin:0 0 1.75rem!important;max-width:740px!important}
#hh-page .hnb-fields{display:grid!important;grid-template-columns:repeat(5,1fr)!important;gap:0.9rem!important}
#hh-page .hnb-f label{display:block!important;font-size:0.7rem!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:0.045em!important;color:var(--hh-slate-500)!important;margin:0 0 0.5rem!important;line-height:1.3!important;min-height:2.1em!important}
#hh-page .hnb-f input{width:100%!important;font-family:inherit!important;font-size:0.9375rem!important;font-weight:600!important;color:var(--hh-slate-900)!important;background:#fff!important;border:1px solid rgba(0,0,0,0.1)!important;border-radius:0.875rem!important;padding:0.72rem 0.85rem!important;box-shadow:0 1px 3px rgba(0,0,0,0.04)!important}
#hh-page .hnb-f input:focus{outline:2px solid #00B1F5!important;outline-offset:1px!important}
#hh-page .hnb-outs{margin:1.5rem 0 0!important}
#hh-page .hnb-outs .stat-number{font-size:1.4rem!important;font-variant-numeric:tabular-nums!important}
#hh-page .hnb-outs .about-stat-card{min-height:88px!important;display:flex!important;flex-direction:column!important;justify-content:center!important}
#hh-page .hnb-verdict{font-size:0.9375rem!important;font-weight:600!important;line-height:1.6!important;border-radius:1rem!important;padding:0.9rem 1.15rem!important;margin:1.25rem 0 0!important;background:var(--hh-amber-50)!important;color:#92400E!important;border:1px solid #FDE68A!important}
#hh-page .hnb-verdict.hnb-ok{background:var(--hh-emerald-50)!important;color:#065f46!important;border-color:#a7f3d0!important}
#hh-page .hnb-table h3{font-size:clamp(1.25rem,2.2vw,1.5rem)!important;font-weight:900!important;letter-spacing:-0.02em!important;color:var(--hh-slate-900)!important;margin:0 0 1.25rem!important}
#hh-page .hnb-tw{overflow-x:auto!important;-webkit-overflow-scrolling:touch!important}
#hh-page .hnb-table table{width:100%!important;border-collapse:collapse!important;font-size:0.9375rem!important;min-width:640px!important}
#hh-page .hnb-table th,#hh-page .hnb-table td{text-align:left!important;padding:0.85rem 1rem!important;border-top:1px solid rgba(0,0,0,0.06)!important;color:var(--hh-slate-600)!important;vertical-align:top!important;line-height:1.55!important}
#hh-page .hnb-table thead th{background:var(--hh-blue-50)!important;color:var(--hh-slate-900)!important;font-weight:700!important;font-size:0.6875rem!important;text-transform:uppercase!important;letter-spacing:0.08em!important;border-top:none!important}
#hh-page .hnb-table thead th:first-child{border-top-left-radius:0.875rem!important}
#hh-page .hnb-table thead th:last-child{border-top-right-radius:0.875rem!important}
#hh-page .hnb-table tbody td:first-child{color:var(--hh-slate-900)!important;font-weight:600!important}
#hh-page .hnb-table td.hnb-num{font-variant-numeric:tabular-nums!important;white-space:nowrap!important;font-weight:800!important;color:#00B1F5!important}
#hh-page .hnb-foot{max-width:1080px!important;margin:2rem auto 0!important;color:var(--hh-slate-600)!important;font-size:1rem!important;line-height:1.8!important}
#hh-page .hnb-foot a{color:#00B1F5!important;font-weight:700!important}
@media(max-width:1100px){#hh-page .hnb-fields{grid-template-columns:repeat(3,1fr)!important}}
@media(max-width:820px){#hh-page .hnb-outs{flex-direction:row!important;display:grid!important;grid-template-columns:repeat(2,1fr)!important}}
@media(max-width:560px){#hh-page .hnb-fields{grid-template-columns:1fr!important}
#hh-page .hnb-f label{min-height:0!important}
#hh-page .hnb-stats{display:grid!important;grid-template-columns:1fr!important;gap:0.6rem!important}
#hh-page .hnb-outs{grid-template-columns:repeat(2,1fr)!important;gap:0.7rem!important}
#hh-page .hnb-outs .stat-number{font-size:1.2rem!important}}
</style>"""

JS = """<script>
(function () {
  var a = document.getElementById('ng-achat');
  if (!a) { return; }
  var th = document.getElementById('ng-theo'), re_ = document.getElementById('ng-reel'),
      pv = document.getElementById('ng-vente'), vol = document.getElementById('ng-vol'),
      oCout = document.getElementById('ng-cout'), oReel = document.getElementById('ng-mreel'),
      oAff = document.getElementById('ng-maff'), oAn = document.getElementById('ng-an'),
      verdict = document.getElementById('ng-verdict');

  function fr(n, d) {
    /* Formatage francais natif : separateur de milliers et virgule decimale,
       sans expression reguliere maison. */
    return n.toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function nb(el, def) { var v = parseFloat(el.value); return isNaN(v) || v < 0 ? def : v; }

  function calc() {
    var pa = nb(a, 0), pt = nb(th, 0), pr = nb(re_, 0), pvu = nb(pv, 0), n = nb(vol, 0);
    var coutReel = pa * pr, coutTheo = pa * pt;
    var mReel = pvu - coutReel, mAff = pvu - coutTheo;
    var ecart = mAff - mReel;
    oCout.textContent = fr(coutReel, 2) + ' \\u20AC';
    oReel.textContent = fr(mReel, 2) + ' \\u20AC' + (pvu > 0 ? ' \\u00B7 ' + fr(mReel / pvu * 100, 1) + ' %' : '');
    oAff.textContent = fr(mAff, 2) + ' \\u20AC' + (pvu > 0 ? ' \\u00B7 ' + fr(mAff / pvu * 100, 1) + ' %' : '');
    oAn.textContent = fr(ecart * n * 12, 0) + ' \\u20AC';
    if (ecart > 0.0005) {
      verdict.className = 'hnb-verdict';
      verdict.textContent = 'Facturée au poids commandé, cette ligne affiche ' + fr(ecart, 2)
        + ' \\u20AC de marge qui n\\u2019existe pas. Sur ' + fr(n, 0)
        + ' unités par mois, cela fait ' + fr(ecart * n, 0) + ' \\u20AC par mois et '
        + fr(ecart * n * 12, 0) + ' \\u20AC par an de marge affichée mais jamais encaissée.';
    } else if (ecart < -0.0005) {
      verdict.className = 'hnb-verdict';
      verdict.textContent = 'Le poids réel est inférieur au poids commandé : facturée au poids '
        + 'commandé, cette ligne se paie ' + fr(-ecart, 2) + ' \\u20AC de trop. C\\u2019est un avoir '
        + 'à émettre, ou un litige client.';
    } else {
      verdict.className = 'hnb-verdict hnb-ok';
      verdict.textContent = 'Poids réel et poids commandé coïncident : la marge affichée est la '
        + 'marge réelle. C\\u2019est le cas le plus rare en produits pesés.';
    }
  }
  [a, th, re_, pv, vol].forEach(function (el) {
    el.addEventListener('input', calc);
    el.addEventListener('change', calc);
  });
  calc();
})();
</script>"""

ICONE = ('<div class="tilted-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">'
         '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
         'd="M8 7V3m8 4V3M3 11h18M5 21h14a2 2 0 002-2V7H3v12a2 2 0 002 2z"/></svg></div>')


def section():
    lignes = "".join(
        '<tr><td>%s</td><td class="hnb-num">%s</td><td>%s</td></tr>' % (n, d, p)
        for n, d, p in C.DELAIS)
    v = C.CALC
    return (
        '<section class="hnb-section">' + CSS + '<div class="container">'

        '<div class="section-header">'
        '<p class="overline">ERP négoce alimentaire</p>'
        '<h2>Vous achetez au kilo. Vous facturez à l\'unité. C\'est là que la marge se perd.</h2>'
        '<p>Un ERP négoce alimentaire facture au poids réellement pesé, applique la DLC du lot et '
        'l\'échéance légale du produit — là où un ERP généraliste facture au poids commandé et à '
        'trente jours pour tout le monde.</p>'
        '</div>'

        '<div class="about-stats hnb-stats">'
        '<div class="about-stat-card"><span class="stat-number">20 jours</span>'
        '<span class="stat-label">Viandes fraîches · après livraison</span></div>'
        '<div class="about-stat-card"><span class="stat-number">30 jours</span>'
        '<span class="stat-label">Produits périssables · fin de décade</span></div>'
        '<div class="about-stat-card"><span class="stat-number">30 jours</span>'
        '<span class="stat-label">Boissons alcooliques · fin de mois</span></div>'
        '</div>'
        '<p class="hnb-src hnb-src-top">Délais maximaux de paiement propres aux produits '
        'alimentaires, fixés par le ' + C.SOURCE + '. Ce ne sont pas trente jours pour tout le '
        'monde, et le point de départ change avec la nature du produit.</p>'

        '<div class="hnb-block">'

        '<div class="about-card hnb-calc"><div class="about-card-inner">'
        '<p class="section-tag">Calculateur</p>'
        '<h3>La marge réelle d\'une ligne à poids variable</h3>'
        '<p class="hnb-intro">Vous achetez un produit au kilo, vous le vendez à l\'unité de vente '
        'consommateur. Si la facturation part du poids commandé et non du poids réellement pesé, '
        'l\'écart n\'apparaît nulle part ligne à ligne — il apparaît en fin de trimestre, quand la '
        'marge globale ne correspond plus aux marges affichées. Remplacez les valeurs de départ '
        'par les vôtres.</p>'
        '<div class="hnb-fields">'
        '<div class="hnb-f"><label for="ng-achat">Prix d\'achat (€/kg)</label>'
        '<input id="ng-achat" type="number" step="0.01" min="0" value="' + v["achat"] + '"></div>'
        '<div class="hnb-f"><label for="ng-theo">Poids commandé de l\'unité (kg)</label>'
        '<input id="ng-theo" type="number" step="0.001" min="0" value="' + v["theorique"] + '"></div>'
        '<div class="hnb-f"><label for="ng-reel">Poids réellement pesé (kg)</label>'
        '<input id="ng-reel" type="number" step="0.001" min="0" value="' + v["reel"] + '"></div>'
        '<div class="hnb-f"><label for="ng-vente">Prix de vente de l\'unité (€)</label>'
        '<input id="ng-vente" type="number" step="0.01" min="0" value="' + v["vente"] + '"></div>'
        '<div class="hnb-f"><label for="ng-vol">Unités vendues par mois</label>'
        '<input id="ng-vol" type="number" step="10" min="0" value="' + v["volume"] + '"></div>'
        '</div>'
        '<div class="about-stats hnb-outs">'
        '<div class="about-stat-card"><output class="stat-number" id="ng-cout">17,51 €</output>'
        '<span class="stat-label">Coût réel de l\'unité</span></div>'
        '<div class="about-stat-card"><output class="stat-number" id="ng-mreel">4,39 € · 20,0 %</output>'
        '<span class="stat-label">Marge réelle</span></div>'
        '<div class="about-stat-card"><output class="stat-number" id="ng-maff">4,90 € · 22,4 %</output>'
        '<span class="stat-label">Marge affichée au poids commandé</span></div>'
        '<div class="about-stat-card"><output class="stat-number" id="ng-an">7 344 €</output>'
        '<span class="stat-label">Écart sur douze mois</span></div>'
        '</div>'
        '<p class="hnb-verdict" id="ng-verdict">Facturée au poids commandé, cette ligne affiche '
        '0,51 € de marge qui n’existe pas. Sur 1 200 unités par mois, cela fait 612 € par mois '
        'et 7 344 € par an de marge affichée mais jamais encaissée.</p>'
        '</div></div>'

        '<div class="bento-card hnb-table">' + ICONE +
        '<h3>Sous combien de jours devez-vous être payé, selon le produit</h3>'
        '<div class="hnb-tw"><table>'
        '<thead><tr><th scope="col">Nature du produit</th><th scope="col">Délai maximal</th>'
        '<th scope="col">Point de départ</th></tr></thead>'
        '<tbody>' + lignes + '</tbody></table></div>'
        '<p class="hnb-src">Relevé le 29/08/2026 dans le ' + C.SOURCE + '. Ces délais sont des '
        'maximums : les parties peuvent convenir plus court. Un ERP qui ignore la nature du '
        'produit applique la même échéance à tout, et l\'écart se paie en trésorerie.</p>'
        '</div>'

        '</div>'

        '<p class="hnb-foot">À approfondir : '
        '<a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a>, '
        '<a href="/negoce/tarifs-reporting-edi/">tarifs, reporting et EDI</a>, '
        '<a href="/fonctionnalites/tracabilite-alimentaire/">traçabilité alimentaire</a>. '
        'À lire ensuite : <a href="/blog/logiciel-grossiste-alimentaire/">logiciel grossiste alimentaire</a> '
        'et <a href="/blog/erp-grossiste-distributeur/">ERP pour distributeurs de produits frais</a>.</p>'

        '</div>' + JS + '</section>'
    )


def patch(src):
    r = []

    # 1 · H1 et accroche
    avant = src
    src = re.sub(r'(<h1 class="hero-title" style="color:#fff">).*?(</h1>)',
                 lambda m: m.group(1) + C.H1 + m.group(2), src, count=1, flags=re.S)
    src = re.sub(r'(<p class="hero-description">).*?(</p>)',
                 lambda m: m.group(1) + C.HERO_DESC + m.group(2), src, count=1, flags=re.S)
    if src == avant:
        raise SystemExit("hero : aucun remplacement effectue")
    r.append("hero : H1 et accroche remplaces — « votre production » n'avait rien a faire ici")

    # 2 · carte de fonctionnalites qui renvoyait vers le maraicher
    avant = src
    src = src.replace(
        '<a href="/agroalimentaire/maraicher/" class="card-link">Découvrir l\'ERP maraîcher',
        '<a href="/negoce/stocks-multi-depots/" class="card-link">Voir les stocks multi-dépôts')
    if src != avant:
        r.append("carte de fonctionnalites : le lien vers l'ERP maraicher est retargete")

    # 2 bis · les derniers reliquats du gabarit maraicher
    reliquats = [
        ('<p class="overline">ERP Maraîcher</p>',
         '<p class="overline">ERP Négoce Alimentaire</p>',
         "overline des fonctionnalites : « ERP Maraîcher » sur une page negoce"),
        ('{"@type": "ListItem", "position": 3, "name": "Maraîcher", '
         '"item": "https://www.helloharel.com/agroalimentaire/negoce-alimentaire/"}',
         '{"@type": "ListItem", "position": 3, "name": "Négoce alimentaire", '
         '"item": "https://www.helloharel.com/agroalimentaire/negoce-alimentaire/"}',
         "fil d'Ariane balise : le 3e niveau annoncait « Maraicher »"),
        ('Traçabilité par parcelle et fournisseur',
         'Traçabilité du lot au fournisseur',
         "carte achats : la tracabilite « par parcelle » ne concerne pas un negociant"),
        ('Calibres, variétés et origines',
         'Cours du jour, remises et conditions fournisseurs',
         "carte achats : les calibres et varietes sont du maraichage"),
        ('<p class="overline">FAQ Maraicher</p>',
         '<p class="overline">FAQ Négoce alimentaire</p>',
         "en-tete de la FAQ : elle annoncait « FAQ Maraicher »"),
        ('<p>Gerez le poids variable et la saisonnalite.</p>',
         '<p>Poids réel, DLC, cadencier, tournées et marges.</p>',
         "sous-titre de la FAQ : la saisonnalite est du maraichage"),
        ('Découvrez nos articles spécialisés : <a href="https://www.helloharel.com/blog/'
         'logiciel-gestion-calibre-fruits-legumes/" style="color:#16DB7F;font-weight:600">'
         'gestion des calibres et agréages F&L</a> · <a href="https://www.helloharel.com/blog/'
         'logiciel-prix-du-jour-fruits-legumes/" style="color:#16DB7F;font-weight:600">'
         'tarification variable et prix du jour</a>.',
         'Découvrez nos articles spécialisés : <a href="https://www.helloharel.com/blog/'
         'logiciel-grossiste-alimentaire/" style="color:#16DB7F;font-weight:600">logiciel '
         'grossiste alimentaire</a> · <a href="https://www.helloharel.com/blog/'
         'grille-tarifaire-negoce-alimentaire/" style="color:#16DB7F;font-weight:600">grille '
         'tarifaire en négoce alimentaire</a>.',
         "bloc « Pour approfondir » : il renvoyait vers deux articles fruits et legumes"),
    ]
    for av, ap, note in reliquats:
        if av in src:
            src = src.replace(av, ap)
            r.append(note)

    # 3 · section d'attention, juste avant les fonctionnalites
    if 'class="hnb-section"' in src:
        raise SystemExit("la section est deja presente")
    i = src.find('<section class="features-section"')
    if i < 0:
        raise SystemExit("features-section introuvable")
    src = src[:i] + section() + "\n\n" + src[i:]
    r.append("section d'attention inseree avant features-section")

    # 4 · FAQ : cartes, bandeaux, panneaux
    qs = re.findall(r'<span class="faq-card-question">(.*?)</span>', src)
    ms = re.findall(r'<span class="faq-card-meta">(.*?)</span>', src)
    if len(qs) != 6 or len(ms) != 6:
        raise SystemExit("attendu 6 cartes de FAQ, trouve %d / %d" % (len(qs), len(ms)))
    for k, (q, meta, _rep) in enumerate(C.FAQ[:6]):
        src = src.replace('<span class="faq-card-question">' + qs[k] + '</span>',
                          '<span class="faq-card-question">' + q + '</span>', 1)
        src = src.replace('<span class="faq-card-meta">' + ms[k] + '</span>',
                          '<span class="faq-card-meta">' + meta + '</span>', 1)
    r.append("6 questions et 6 bandeaux de cartes remis en face de leur reponse")

    carte0 = re.search(r'(<div class="faq-card" onclick="openFaqDrawer\(0\)">.*?</div>\s*</div>)',
                       src, re.S).group(1)
    q7, m7, _ = C.FAQ[6]
    carte7 = (carte0.replace('openFaqDrawer(0)', 'openFaqDrawer(6)')
                    .replace('<span class="faq-card-question">' + C.FAQ[0][0] + '</span>',
                             '<span class="faq-card-question">' + q7 + '</span>')
                    .replace('<span class="faq-card-meta">' + C.FAQ[0][1] + '</span>',
                             '<span class="faq-card-meta">' + m7 + '</span>'))
    d = src.rfind('openFaqDrawer(5)')
    fin = src.find('</div>', src.find('faq-card-arrow', d))
    fin = src.find('</div>', fin + 6)
    src = src[:fin + 6] + "\n            " + carte7 + src[fin + 6:]
    r.append("7e carte ajoutee : l'echeance legale, qui porte le fait date")

    pans = re.findall(r'<div class="faq-drawer-panel" data-faq="\d+"[^>]*>\s*<h3>.*?</h3>\s*'
                      r'<div class="faq-drawer-content">.*?</div>\s*</div>', src, re.S)
    if len(pans) != 6:
        raise SystemExit("attendu 6 panneaux, trouve %d" % len(pans))
    neufs = ['<div class="faq-drawer-panel" data-faq="' + str(k) + '" style="display:none">\n'
             '            <h3>' + q + '</h3>\n'
             '            <div class="faq-drawer-content">' + rep + '</div>\n'
             '        </div>' for k, (q, _m, rep) in enumerate(C.FAQ)]
    for k in range(6):
        src = src.replace(pans[k], neufs[k], 1)
    src = src.replace(neufs[5], neufs[5] + "\n        " + neufs[6], 1)
    src = src.replace("var totalFaqs = 6;", "var totalFaqs = 7;")
    r.append("7 panneaux reecrits : les 6 anciens venaient du gabarit maraicher")

    # 5 · JSON-LD FAQPage
    m = re.search(r'<script type="application/ld\+json">\s*(\{\s*"@context"[^\0]*?'
                  r'"@type": "FAQPage"[^\0]*?)\s*</script>', src, re.S)
    if not m:
        raise SystemExit("JSON-LD FAQPage introuvable")
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer",
                            "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", rep)).strip()}}
        for q, _m, rep in C.FAQ]}
    src = src[:m.start(1)] + json.dumps(ld, ensure_ascii=False, indent=2) + src[m.end(1):]
    r.append("JSON-LD FAQPage resynchronise — il portait les questions du maraicher")

    return src, r


def zone_produite(src):
    z = []
    m = re.search(r'<section class="hnb-section">.*?</section>', src, re.S)
    if m:
        z.append(m.group(0))
    m = re.search(r'<div class="faq-cards-grid">.*?</section>', src, re.S)
    if m:
        z.append(m.group(0))
    for m in re.finditer(r'<div class="faq-drawer-panel".*?</div>\s*</div>', src, re.S):
        z.append(m.group(0))
    return "\n".join(z)


def controles(src):
    pb = []
    o, f = src.count("<div"), src.count("</div>")
    if o != f:
        pb.append("desequilibre des div : %d / %d" % (o, f))
    if src.count("<section") != src.count("</section>"):
        pb.append("desequilibre des section")
    if re.search(r'href="#s-', src):
        pb.append("un lien de saut #s- a ete introduit")

    z = zone_produite(src)
    if len(z) < 15000:
        pb.append("zone produite trop courte (%d car.)" % len(z))

    PROT = ("/agroalimentaire/", "/agroalimentaire/traiteur/", "/agroalimentaire/charcutier/",
            "/agroalimentaire/plats-cuisines-industriels/", "/migration-as400/")
    for href, texte in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', z, re.S):
        if href in PROT:
            t = re.sub(r"<[^>]+>", "", texte).strip().lower()
            if t not in ("agroalimentaire",):
                pb.append("Regle 0 — ancre optimisee vers une page protegee : %r -> %s"
                          % (t[:40], href))

    # Le vocabulaire hors persona se controle sur TOUTE la page, pas seulement sur
    # la zone reecrite : les reliquats du gabarit maraicher etaient disperses.
    # Le carrousel des metiers et le temoignage client sont exclus : le premier
    # est de la navigation, le second est une citation authentique.
    page = src
    for coupe in (r'<section class="metiers-section".*?</section>',
                  r'<section class="reviews-section".*?</section>',
                  r'<footer.*?</footer>'):
        page = re.sub(coupe, " ", page, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", page)
    for mot in ("maraîch", "maraich", "calibre", "saisonnalité", "fraise", "melon",
                "parcelle", "récolte", "conteneur", "incoterm", "frais d'approche"):
        n = len(re.findall(mot, txt, re.I))
        if n:
            pb.append("vocabulaire hors persona : %r x%d dans la page" % (mot, n))

    for q, _m, _r in C.FAQ:
        if q not in src:
            pb.append("question absente : %r" % q[:48])

    # Aucun lien interne invente : chacun doit repondre 200 en direct.
    import subprocess
    for href in sorted(set(re.findall(r'href="(/[^"#]+)"', z))):
        code = subprocess.run(
            ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}",
             "https://www.helloharel.com" + href],
            capture_output=True, text=True, timeout=45).stdout.strip()
        if code != "200":
            pb.append("lien interne en %s : %s" % (code, href))

    sig = [
        ("module interactif present", 'id="ng-achat"' in src and "hnb-calc" in src),
        ("preuve datee et sourcee", "L441-11" in src and "20 jours" in src),
        ("reponse en une phrase", "trente jours pour tout le monde" in src),
        ("donnee structuree", "<table>" in z),
        ("exact match dans le H1", "ERP négoce alimentaire" in src),
        ("la suite est dans la page", 'href="/negoce/tarifs-reporting-edi/"' in z),
    ]
    print("\ncriteres de signal :")
    for nom, ok in sig:
        print("   %s %s" % ("OK  " if ok else "NON ", nom))
        if not ok:
            pb.append("critere de signal en echec : " + nom)
    return pb


def main():
    if os.path.exists(SAUV):
        src = open(SAUV, encoding="utf-8").read()
        print("  source : sauvegarde d'origine (%d car.)" % len(src))
    else:
        src = w.get_raw("pages", PAGE)["content"]["raw"]
        open(SAUV, "w", encoding="utf-8").write(src)
        print("  source : site (sauvegarde creee)")

    neuf, rapport = patch(src)
    for l in rapport:
        print("  -", l)
    pb = controles(neuf)
    print("\ncontroles : %s" % ("AUCUN DEFAUT" if not pb else "%d point(s)" % len(pb)))
    for p in pb:
        print("   !", p)
    print("\ntaille : %d -> %d caracteres" % (len(src), len(neuf)))

    open(os.path.join(ICI, "preview-negoce-alim.html"), "w", encoding="utf-8").write(neuf)
    if LIVE:
        if pb:
            raise SystemExit("ecriture refusee : des controles ont echoue")
        w.update_content("pages", PAGE, neuf, live=True)
        print("PUBLIE sur https://www.helloharel.com/agroalimentaire/negoce-alimentaire/")
    else:
        print("essai a blanc — rien n'a ete ecrit sur le site")


if __name__ == "__main__":
    main()
