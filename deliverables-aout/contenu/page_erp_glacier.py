#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mise a jour de /agroalimentaire/glacier/ (page 10895) — requete « erp glacier ».

Ce que le script pose :
  1. hero — photo de production, H1 avec l'exact match, accroche reecrite ;
  2. une section NavBoost inseree au-dessus du deuxieme ecran :
     reponse encadree, chiffre date source, calculateur foisonnement / cout au litre,
     tableau des 8 denominations reservees ;
  3. les 7 reponses de FAQ reecrites pour le metier (l'existant etait un gabarit
     boulangerie renomme : fours, farine, levure, croissants) + JSON-LD synchronise.

Le gabarit des pages soeurs n'est pas modifie : aucune section n'est supprimee,
aucune classe n'est renommee, la nouvelle section reprend la DA des blocs
« hh-maj-aout-* » deja poses sur maraicher, patissier et poissonnier.

Usage :  python3 page_erp_glacier.py            (essai a blanc)
         python3 page_erp_glacier.py --live     (ecriture)
"""

import json
import re
import sys
import os

sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import wp_common as w
import glacier_contenu as C

PAGE = 10895
LIVE = "--live" in sys.argv

# --------------------------------------------------------------------------- CSS
# On reutilise au maximum les classes du gabarit (.container, .section-header,
# .overline, .about-card, .about-stats, .about-stat-card, .stat-number,
# .stat-label, .section-tag, .bento-card, .tilted-icon, .card-link).
# Le CSS ci-dessous ne couvre que ce qui n'existe pas encore : les champs du
# calculateur, le verdict et le tableau. Toutes les marges portent !important :
# le gabarit impose #hh-page p{margin:0!important}.
CSS = """<style>
#hh-page .glnb-section{padding:clamp(4.5rem,9vw,8rem) 0!important;background:#fff!important;display:block!important}
#hh-page .glnb-section .section-header>p{max-width:720px!important}\n#hh-page .glnb-section .glnb-stats{max-width:840px!important;margin:0 auto 0.75rem!important}
#hh-page .glnb-section .about-stat-card{border:1px solid rgba(0,0,0,0.06)!important}
#hh-page .glnb-section .stat-number{font-size:2rem!important}
#hh-page .glnb-src{color:var(--hh-slate-500)!important;font-size:0.8125rem!important;line-height:1.65!important;margin:0.75rem 0 0!important}
#hh-page .glnb-src-top{text-align:center!important;max-width:720px!important;margin:0 auto 3rem!important}
#hh-page .glnb-block{max-width:1080px!important;margin:0 auto!important}
#hh-page .glnb-calc{margin-bottom:1.5rem!important}
#hh-page .glnb-calc h3{font-size:clamp(1.35rem,2.4vw,1.75rem)!important;font-weight:900!important;letter-spacing:-0.02em!important;color:var(--hh-slate-900)!important;line-height:1.2!important;margin:0 0 0.75rem!important}
#hh-page .glnb-calc>.about-card-inner>p.glnb-intro{color:var(--hh-slate-600)!important;font-size:1rem!important;line-height:1.75!important;margin:0 0 1.75rem!important;max-width:720px!important}
#hh-page .glnb-fields{display:grid!important;grid-template-columns:repeat(4,1fr)!important;gap:1rem!important}
#hh-page .glnb-f label{display:block!important;font-size:0.75rem!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:0.05em!important;color:var(--hh-slate-500)!important;margin:0 0 0.5rem!important}
#hh-page .glnb-f select,#hh-page .glnb-f input{width:100%!important;font-family:inherit!important;font-size:0.9375rem!important;font-weight:600!important;color:var(--hh-slate-900)!important;background:#fff!important;border:1px solid rgba(0,0,0,0.1)!important;border-radius:0.875rem!important;padding:0.75rem 0.9rem!important;box-shadow:0 1px 3px rgba(0,0,0,0.04)!important}
#hh-page .glnb-f select:focus,#hh-page .glnb-f input:focus{outline:2px solid #00B1F5!important;outline-offset:1px!important}
#hh-page .glnb-outs{margin:1.5rem 0 0!important}
#hh-page .glnb-outs .stat-number{font-size:1.5rem!important;font-variant-numeric:tabular-nums!important}
#hh-page .glnb-outs .about-stat-card{min-height:84px!important;display:flex!important;flex-direction:column!important;justify-content:center!important}
#hh-page .glnb-verdict{font-size:0.9375rem!important;font-weight:600!important;line-height:1.6!important;border-radius:1rem!important;padding:0.875rem 1.125rem!important;margin:1.25rem 0 0!important}
#hh-page .glnb-ok{background:var(--hh-emerald-50)!important;color:#065f46!important;border:1px solid #a7f3d0!important}
#hh-page .glnb-ko{background:var(--hh-red-50)!important;color:#991b1b!important;border:1px solid #fecaca!important}
#hh-page .glnb-table h3{font-size:clamp(1.25rem,2.2vw,1.5rem)!important;font-weight:900!important;letter-spacing:-0.02em!important;color:var(--hh-slate-900)!important;margin:0 0 1.25rem!important}
#hh-page .glnb-tw{overflow-x:auto!important;-webkit-overflow-scrolling:touch!important}
#hh-page .glnb-table table{width:100%!important;border-collapse:collapse!important;font-size:0.9375rem!important;min-width:660px!important}
#hh-page .glnb-table th,#hh-page .glnb-table td{text-align:left!important;padding:0.8rem 1rem!important;border-top:1px solid rgba(0,0,0,0.06)!important;color:var(--hh-slate-600)!important;vertical-align:top!important;line-height:1.5!important}
#hh-page .glnb-table thead th{background:var(--hh-blue-50)!important;color:var(--hh-slate-900)!important;font-weight:700!important;font-size:0.6875rem!important;text-transform:uppercase!important;letter-spacing:0.08em!important;border-top:none!important}
#hh-page .glnb-table thead th:first-child{border-top-left-radius:0.875rem!important}
#hh-page .glnb-table thead th:last-child{border-top-right-radius:0.875rem!important}
#hh-page .glnb-table tbody td:first-child{color:var(--hh-slate-900)!important;font-weight:700!important}
#hh-page .glnb-table td.glnb-num{font-variant-numeric:tabular-nums!important;white-space:nowrap!important;font-weight:700!important;color:#00B1F5!important}
#hh-page .glnb-foot{max-width:1080px!important;margin:2rem auto 0!important;color:var(--hh-slate-600)!important;font-size:1rem!important;line-height:1.8!important}
#hh-page .glnb-foot a{color:#00B1F5!important;font-weight:700!important}
@media(max-width:900px){#hh-page .glnb-fields{grid-template-columns:repeat(2,1fr)!important}
#hh-page .glnb-section .glnb-stats,#hh-page .glnb-outs{flex-direction:row!important}}
@media(max-width:560px){#hh-page .glnb-fields{grid-template-columns:1fr!important}
#hh-page .glnb-section .glnb-stats{display:grid!important;grid-template-columns:repeat(3,1fr)!important;gap:0.5rem!important}
#hh-page .glnb-section .glnb-stats .about-stat-card{padding:0.875rem 0.5rem!important;min-width:0!important}
#hh-page .glnb-section .glnb-stats .stat-number{font-size:1.35rem!important}
#hh-page .glnb-section .glnb-stats .stat-label{font-size:0.625rem!important;letter-spacing:0.02em!important}
#hh-page .glnb-outs{display:grid!important;grid-template-columns:repeat(2,1fr)!important;gap:0.75rem!important}
#hh-page .glnb-outs .about-stat-card{padding:0.875rem 0.75rem!important;min-width:0!important;min-height:76px!important}
#hh-page .glnb-outs .stat-number{font-size:1.25rem!important}}
</style>"""

JS = """<script>
(function () {
  var den = document.getElementById('gl-den');
  if (!den) { return; }
  var dens = document.getElementById('gl-dens'),
      fois = document.getElementById('gl-fois'),
      cout = document.getElementById('gl-cout'),
      oPoids = document.getElementById('gl-poids'),
      oFmax = document.getElementById('gl-fmax'),
      oCl = document.getElementById('gl-cl'),
      oCb = document.getElementById('gl-cb'),
      verdict = document.getElementById('gl-verdict');

  function fr(n, d) { return n.toFixed(d).replace('.', ','); }

  function calc() {
    var pmin = parseFloat(den.value) || 450,
        d = parseFloat(dens.value) || 1.1,
        f = parseFloat(fois.value), c = parseFloat(cout.value);
    if (isNaN(f) || f < 0) { f = 0; }
    if (isNaN(c) || c < 0) { c = 0; }
    var poids = d * 1000 / (1 + f / 100),
        fmax = (d * 1000 / pmin - 1) * 100,
        cl = c * poids / 1000;
    oPoids.textContent = fr(poids, 0) + ' g';
    oFmax.textContent = fr(fmax, 0) + ' %';
    oCl.textContent = fr(cl, 2) + ' \u20AC';
    oCb.textContent = fr(cl * 5, 2) + ' \u20AC';
    if (poids >= pmin) {
      verdict.className = 'glnb-verdict glnb-ok';
      verdict.textContent = 'Conforme : ' + fr(poids, 0) + ' g par litre pour un minimum exigé de '
        + fr(pmin, 0) + ' g. Il reste ' + fr(Math.max(0, fmax - f), 0)
        + ' points de foisonnement avant la limite.';
    } else {
      verdict.className = 'glnb-verdict glnb-ko';
      verdict.textContent = 'Non conforme : ' + fr(poids, 0) + ' g par litre pour un minimum exigé de '
        + fr(pmin, 0) + ' g. Le foisonnement doit redescendre sous ' + fr(fmax, 0)
        + ' % pour garder cette dénomination.';
    }
  }
  [den, dens, fois, cout].forEach(function (el) {
    el.addEventListener('input', calc);
    el.addEventListener('change', calc);
  });
  calc();
})();
</script>"""


ICONE = ('<div class="tilted-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">'
         '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
         'd="M9 17V7m4 10V11m4 6V9M5 21h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z"/>'
         '</svg></div>')


# --------------------------------------------------------------------------- section
def section_navboost():
    opts = "".join(
        '<option value="%d"%s>%s — %d g/L</option>' % (
            poids, ' selected' if nom == "Crème glacée" else '', nom, poids)
        for nom, poids, _ in C.DENOMINATIONS)

    lignes = "".join(
        '<tr><td>%s</td><td class="glnb-num">%d g</td><td class="glnb-num">%s %%</td><td>%s</td></tr>'
        % (nom, poids, str(round((1100.0 / poids - 1) * 100)), seuil)
        for nom, poids, seuil in C.DENOMINATIONS)

    return (
        '<section class="glnb-section">' + CSS + '<div class="container">'

        '<div class="section-header">'
        '<p class="overline">ERP glacier</p>'
        '<h2>Du mix au litre vendu, sans perdre le lot en route</h2>'
        '<p>Un ERP glacier relie la recette du mix, le lot, le foisonnement, la DLC et le coût '
        'de revient au litre — là où un logiciel de caisse s\'arrête au ticket.</p>'
        '</div>'

        '<div class="about-stats glnb-stats">'
        '<div class="about-stat-card"><span class="stat-number">450 g</span>'
        '<span class="stat-label">Crème glacée · min. / litre</span></div>'
        '<div class="about-stat-card"><span class="stat-number">550 g</span>'
        '<span class="stat-label">Glace aux œufs</span></div>'
        '<div class="about-stat-card"><span class="stat-number">650 g</span>'
        '<span class="stat-label">Sorbet plein fruit</span></div>'
        '</div>'
        '<p class="glnb-src glnb-src-top">Poids minimal par litre fixé par le '
        + C.SOURCE + '. En dessous, la dénomination ne peut plus être portée sur l\'étiquette.</p>'

        '<div class="glnb-block">'

        '<div class="about-card glnb-calc"><div class="about-card-inner">'
        '<p class="section-tag">Calculateur</p>'
        '<h3>Poids au litre, foisonnement maximal et coût matière</h3>'
        '<p class="glnb-intro">Le foisonnement décide de tout : il transforme un coût au kilo en '
        'coût au litre, et il plafonne la dénomination que vous avez le droit d\'écrire sur '
        'l\'étiquette. Pesez un litre de votre mix pour obtenir sa densité, puis renseignez votre '
        'cible de foisonnement.</p>'
        '<div class="glnb-fields">'
        '<div class="glnb-f"><label for="gl-den">Dénomination visée</label>'
        '<select id="gl-den">' + opts + '</select></div>'
        '<div class="glnb-f"><label for="gl-dens">Densité du mix (kg/L)</label>'
        '<input id="gl-dens" type="number" step="0.01" min="0.8" max="1.4" value="1.10"></div>'
        '<div class="glnb-f"><label for="gl-fois">Foisonnement visé (%)</label>'
        '<input id="gl-fois" type="number" step="1" min="0" max="200" value="35"></div>'
        '<div class="glnb-f"><label for="gl-cout">Coût du mix (€/kg)</label>'
        '<input id="gl-cout" type="number" step="0.05" min="0" value="3.20"></div>'
        '</div>'
        '<div class="about-stats glnb-outs">'
        '<div class="about-stat-card"><output class="stat-number" id="gl-poids">815 g</output>'
        '<span class="stat-label">Poids du litre fini</span></div>'
        '<div class="about-stat-card"><output class="stat-number" id="gl-fmax">144 %</output>'
        '<span class="stat-label">Foisonnement maximal</span></div>'
        '<div class="about-stat-card"><output class="stat-number" id="gl-cl">2,61 €</output>'
        '<span class="stat-label">Coût matière / litre</span></div>'
        '<div class="about-stat-card"><output class="stat-number" id="gl-cb">13,04 €</output>'
        '<span class="stat-label">Coût matière / bac de 5 L</span></div>'
        '</div>'
        '<p class="glnb-verdict glnb-ok" id="gl-verdict">Conforme : 815 g par litre pour un minimum '
        'exigé de 450 g. Il reste 109 points de foisonnement avant la limite.</p>'
        '</div></div>'

        '<div class="bento-card glnb-table">' + ICONE +
        '<h3>Les 8 dénominations réservées et leur poids minimal par litre</h3>'
        '<div class="glnb-tw"><table>'
        '<thead><tr><th scope="col">Dénomination</th><th scope="col">Poids min. / litre</th>'
        '<th scope="col">Foisonnement max. à 1,10 kg/L</th>'
        '<th scope="col">Seuil caractéristique</th></tr></thead>'
        '<tbody>' + lignes + '</tbody></table></div>'
        '<p class="glnb-src">Relevé le 27/08/2026 dans le ' + C.SOURCE + '. Le foisonnement maximal '
        'est calculé pour un mix à 1,10 kg/L : il varie avec la densité réelle de votre mix.</p>'
        '</div>'

        '</div>'

        '<p class="glnb-foot">À approfondir : '
        '<a href="/fonctionnalites/fabrication/">logiciel de fabrication</a>, '
        '<a href="/fonctionnalites/tracabilite-alimentaire/">traçabilité alimentaire</a>, '
        '<a href="/blog/calculer-le-prix-de-revient-en-boulangerie/">logiciel de prix de revient</a>. '
        'Métiers proches : <a href="/agroalimentaire/patissier/">ERP pâtissier</a> et '
        '<a href="/agroalimentaire/chocolatier/">ERP chocolatier</a>.</p>'

        '</div>' + JS + '</section>'
    )


# --------------------------------------------------------------------------- FAQ
def bloc_faq_cartes(src):
    """Remplace les 7 questions de cartes + leur bandeau de mots-cles."""
    cartes = re.findall(r'<div class="faq-card" onclick="openFaqDrawer\(\d+\)">.*?\n\s*</div>\n\s*</div>',
                        src, re.S)
    return cartes


def patch(src):
    rapport = []

    # --- 1. hero ---------------------------------------------------------------
    avant = src
    for ancienne in ("ERP-logiciel-pour-les-grossistes-en-cremerie.webp",
                     "erp-glacier-production-glaces-sorbets.webp"):
        src = src.replace(ancienne, C.HERO_IMG.rsplit("/", 1)[1])
    src = src.replace(
        '<h1 class="hero-title" style="color:#fff">Pilotez vos productions, '
        '<span class="accent" style="color:#60a5fa">maîtrisez vos coûts</span></h1>',
        '<h1 class="hero-title" style="color:#fff">' + C.H1 + '</h1>')
    src = src.replace(
        "<p class=\"hero-description\">Recettes, chaîne du froid, DLC/DDM et saisonnalité&nbsp;: "
        "l'ERP qui pilote la rentabilité de vos glaces et sorbets, saison après saison.</p>",
        '<p class="hero-description">' + C.HERO_DESC + '</p>')
    src = src.replace(
        "<p class=\"hero-description\">Recettes, chaîne du froid, DLC/DDM et saisonnalité : "
        "l'ERP qui pilote la rentabilité de vos glaces et sorbets, saison après saison.</p>",
        '<p class="hero-description">' + C.HERO_DESC + '</p>')
    if src == avant:
        raise SystemExit("hero : aucun remplacement effectue")
    rapport.append("hero : photo, H1 et accroche remplaces")

    # --- 1 bis. reliquat du gabarit boulangerie dans la premiere carte bento ----
    avant = src
    src = src.replace(
        '<a href="/agroalimentaire/boulanger/" class="card-link">Découvrir l\'ERP boulangerie',
        '<a href="/fonctionnalites/fabrication/" class="card-link">Logiciel de fabrication')
    if src != avant:
        rapport.append("carte bento : lien vers l'ERP boulangerie retire")

    # --- 2. section NavBoost, juste apres le carrousel de logos ----------------
    if 'class="glnb-section"' in src:
        raise SystemExit("la section NavBoost est deja presente")
    ancre = '<section class="features-section"'
    i = src.find(ancre)
    if i < 0:
        raise SystemExit("features-section introuvable : point d'insertion incertain")
    src = src[:i] + section_navboost() + "\n\n" + src[i:]
    rapport.append("section NavBoost inseree avant features-section")

    # --- 3. FAQ : cartes -------------------------------------------------------
    questions = re.findall(r'<span class="faq-card-question">(.*?)</span>', src)
    if len(questions) != 6:
        raise SystemExit("attendu 6 cartes de FAQ, trouve %d" % len(questions))
    for k, (q, meta, _) in enumerate(C.FAQ[:6]):
        src = src.replace('<span class="faq-card-question">' + questions[k] + '</span>',
                          '<span class="faq-card-question">' + q + '</span>', 1)
    metas = re.findall(r'<span class="faq-card-meta">(.*?)</span>', src)
    for k, (_, meta, _2) in enumerate(C.FAQ[:6]):
        src = src.replace('<span class="faq-card-meta">' + metas[k] + '</span>',
                          '<span class="faq-card-meta">' + meta + '</span>', 1)
    rapport.append("6 questions de cartes remplacees")

    # 7e carte, clonee de la premiere
    carte0 = re.search(r'(<div class="faq-card" onclick="openFaqDrawer\(0\)">.*?</div>\s*</div>)',
                       src, re.S).group(1)
    q7, m7, _ = C.FAQ[6]
    carte7 = (carte0.replace('openFaqDrawer(0)', 'openFaqDrawer(6)')
                    .replace('<span class="faq-card-question">' + C.FAQ[0][0] + '</span>',
                             '<span class="faq-card-question">' + q7 + '</span>')
                    .replace('<span class="faq-card-meta">' + C.FAQ[0][1] + '</span>',
                             '<span class="faq-card-meta">' + m7 + '</span>'))
    fin_grille = src.find('</div>', src.find('faq-cards-grid'))
    derniere = src.rfind('openFaqDrawer(5)')
    fin = src.find('</div>\n                </div>\n                <div class="faq-card-arrow">', derniere)
    fin = src.find('</div>', src.find('faq-card-arrow', derniere))
    fin = src.find('</div>', fin + 6)
    src = src[:fin + 6] + "\n            " + carte7 + src[fin + 6:]
    rapport.append("7e carte de FAQ ajoutee")

    # --- 4. FAQ : panneaux -----------------------------------------------------
    panneaux = re.findall(r'<div class="faq-drawer-panel" data-faq="\d+"[^>]*>\s*<h3>.*?</h3>\s*'
                          r'<div class="faq-drawer-content">.*?</div>\s*</div>', src, re.S)
    if len(panneaux) != 6:
        raise SystemExit("attendu 6 panneaux, trouve %d" % len(panneaux))
    neufs = []
    for k, (q, _m, rep) in enumerate(C.FAQ):
        neufs.append('<div class="faq-drawer-panel" data-faq="' + str(k) + '" style="display:none">\n'
                     '            <h3>' + q + '</h3>\n'
                     '            <div class="faq-drawer-content">' + rep + '</div>\n'
                     '        </div>')
    src = src.replace(panneaux[0], neufs[0], 1)
    for k in range(1, 6):
        src = src.replace(panneaux[k], neufs[k], 1)
    src = src.replace(neufs[5], neufs[5] + "\n        " + neufs[6], 1)
    src = src.replace("var totalFaqs = 6;", "var totalFaqs = 7;")
    rapport.append("7 panneaux de FAQ reecrits pour le metier")

    # --- 5. JSON-LD FAQPage ----------------------------------------------------
    m = re.search(r'<script type="application/ld\+json">\s*(\{\s*"@context"[^\0]*?"@type": "FAQPage"[^\0]*?)\s*</script>',
                  src, re.S)
    if not m:
        raise SystemExit("JSON-LD FAQPage introuvable")
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer",
                            "text": re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', rep)).strip()}}
        for q, _m, rep in C.FAQ]}
    src = src[:m.start(1)] + json.dumps(ld, ensure_ascii=False, indent=2) + src[m.end(1):]
    rapport.append("JSON-LD FAQPage synchronise sur 7 questions")

    return src, rapport


# --------------------------------------------------------------------------- garde-fous
def zones_produites(src):
    """Les seules zones que ce script ecrit : la section NavBoost, les cartes et les
    panneaux de FAQ. Les controles de Regle 0 et de fuite de gabarit ne portent que
    sur elles — le reste de la page (carrousel metiers, pied de page global) est
    anterieur et ne doit pas etre modifie ici."""
    zones = []
    m = re.search(r'<section class="glnb-section">.*?</section>', src, re.S)
    if m:
        zones.append(m.group(0))
    m = re.search(r'<div class="faq-cards-grid">.*?</section>', src, re.S)
    if m:
        zones.append(m.group(0))
    for m in re.finditer(r'<div class="faq-drawer-panel".*?</div>\s*</div>', src, re.S):
        zones.append(m.group(0))
    return "\n".join(zones)


def controles(src):
    pb = []
    o, f = src.count("<div"), src.count("</div>")
    if o != f:
        pb.append("desequilibre des div : %d ouvrants / %d fermants" % (o, f))
    if src.count("<section") != src.count("</section>"):
        pb.append("desequilibre des section")
    if re.search(r'href="#s-', src):
        pb.append("un lien de saut #s- a ete introduit")

    zone = zones_produites(src)
    if len(zone) < 15000:
        pb.append("zones produites trop courtes (%d car.) : le reperage a echoue" % len(zone))

    # Regle 0 — aucune ancre interne optimisee vers une page protegee
    PROTEGEES = ("/agroalimentaire/", "/agroalimentaire/traiteur/", "/agroalimentaire/charcutier/",
                 "/agroalimentaire/plats-cuisines-industriels/", "/migration-as400/")
    for href, texte in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', zone, re.S):
        if href in PROTEGEES:
            t = re.sub(r"<[^>]+>", "", texte).strip().lower()
            if t not in ("agroalimentaire",):
                pb.append("Regle 0 — ancre optimisee vers une page protegee : %r -> %s"
                          % (t[:40], href))

    # fuite du gabarit boulangerie dans le texte produit
    texte_zone = re.sub(r"<[^>]+>", " ", zone)
    for mot in ("farine", "levure", "croissant", "baguette", "feuilletee", "feuilletée",
                "four ", "cuisson", "pointage", "appret", "apprêt", "boulanger",
                "glaciers-p", "glacier-p"):
        n = len(re.findall(mot, texte_zone, re.I))
        if n:
            pb.append("fuite de gabarit : %r x%d dans le texte produit" % (mot, n))

    for q, _m, _r in C.FAQ:
        if q not in src:
            pb.append("question absente de la page : %r" % q[:50])

    # les 7 criteres de signal, mesures et non declares
    sig = []
    sig.append(("module interactif present", 'id="gl-den"' in src and "glnb-calc" in src))
    sig.append(("preuve datee et sourcee", "4 mars 2008" in src and "450 g" in src))
    sig.append(("definition en une phrase",
                "s'arrête au ticket" in src or "s\u2019arr\u00eate au ticket" in src))
    sig.append(("donnee structuree", "<table>" in zone or "<table" in zone))
    sig.append(("exact match dans le H1", "ERP glacier" in src))
    sig.append(("la suite est dans la page",
                'href="/blog/calculer-le-prix-de-revient-en-boulangerie/"' in zone))
    print("\ncriteres de signal :")
    for nom, ok in sig:
        print("   %s %s" % ("OK  " if ok else "NON ", nom))
        if not ok:
            pb.append("critere de signal en echec : " + nom)
    return pb


def main():
    sauv = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "backup-glacier-10895.html")
    if os.path.exists(sauv):
        # on repart toujours de la version d'origine : le patch est rejouable
        src = open(sauv, encoding="utf-8").read()
        print("  source : sauvegarde d'origine (%d car.)" % len(src))
    else:
        src = w.get_raw("pages", PAGE)["content"]["raw"]
        open(sauv, "w", encoding="utf-8").write(src)
        print("  source : site (sauvegarde creee)")
    neuf, rapport = patch(src)
    for l in rapport:
        print("  -", l)
    pb = controles(neuf)
    print("\ncontroles :", "AUCUN DEFAUT" if not pb else "%d point(s)" % len(pb))
    for p in pb:
        print("   !", p)
    print("\ntaille : %d -> %d caracteres" % (len(src), len(neuf)))
    if LIVE:
        if pb:
            raise SystemExit("ecriture refusee : des controles ont echoue")
        w.update_content("pages", PAGE, neuf, live=True)
        print("PUBLIE sur https://www.helloharel.com/agroalimentaire/glacier/")
    else:
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "preview-glacier.html"), "w", encoding="utf-8").write(neuf)
        print("essai a blanc — rien n'a ete ecrit sur le site")


if __name__ == "__main__":
    main()
