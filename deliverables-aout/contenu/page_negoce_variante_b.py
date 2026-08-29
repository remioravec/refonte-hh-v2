#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variante B du test A/B negoce — page 11495.

Le fond vient de la variante A (page 11493), sans reecriture. Ce qui change,
et c'est la seule variable du test, c'est l'UX : structure d'accueil SaaS
(hero a deux colonnes, bande de preuve avec defilement de logos, onglets de
fonctionnalites, sections alternees texte/image, cartes de modules, FAQ en
accordeon) portee par la DA Hello Harel — Inter, bleu #00B1F5, CTA vert,
cartes a 24 px, survols et apparitions au defilement.

Usage :  python3 page_negoce_variante_b.py           (essai a blanc)
         python3 page_negoce_variante_b.py --live    (ecriture)
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)

import wp_common as w
import negoce_b_contenu as C
from negoce_b_css import CSS

PAGE = 11495
TITRE = "[TEST B] ERP Import Export Alimentaire • Frais d'Approche & Lots"
LIVE = "--live" in sys.argv
IMG = json.load(open(os.path.join(ICI, "images-negoce-b.json"), encoding="utf-8"))


# --------------------------------------------------------------------- briques
def check():
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" '
            'd="M5 13l4 4L19 7"/></svg>')


def fleche():
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" '
            'd="M9 5l7 7-7 7"/></svg>')


def ticks(items):
    out = ['<div class="ticks">']
    for t in items:
        out.append('<div class="tick">' + check() + '<span>' + t + '</span></div>')
    out.append('</div>')
    return "".join(out)


def img(cle, classe=""):
    d = IMG[cle]
    c = (' class="' + classe + '"') if classe else ""
    return ('<img src="' + d["url"] + '" alt="' + d["alt"] + '" loading="lazy" '
            'decoding="async"' + c + '>')


def lien_plus(href, libelle):
    return '<a class="more" href="' + href + '">' + libelle + ' ' + fleche() + '</a>'


# --------------------------------------------------------------------- sections
def hero():
    mots = "".join('<span class="wd">' + m + '</span> ' for m in C.H1_MOTS)
    return (
        '<section class="hero">'
        '<div class="w"><div class="hero-grid">'
        '<div>'
        '<span class="pill"><i></i>' + C.BADGE + '</span>'
        '<h1 data-anim="words" data-stagger="70">' + mots + '</h1>'
        + ticks(C.HERO_TICKS) +
        '<div class="btns">'
        '<a class="btn btn-1" href="/contact/">Voir sur mes opérations</a>'
        '<a class="btn btn-2" href="/fonctionnalites/import-export/">Le module import export</a>'
        '</div>'
        '<p class="reassure">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
        'd="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 '
        '01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 '
        '9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>'
        + C.HERO_REASSURE + '</p>'
        '</div>'
        '<div class="hero-media" data-anim="rise">' + img("hero") + '</div>'
        '</div></div></section>'
    )


def preuve():
    stats = "".join('<div class="stat"><b>' + v + '</b><span>' + l + '</span></div>'
                    for v, l in C.STATS)
    piste = "".join('<img src="' + u + '" alt="' + a + '" loading="lazy" decoding="async">'
                    for u, a in C.LOGOS)
    return (
        '<section class="proof">'
        '<div class="w">'
        '<div class="proof-top"><p>' + C.PREUVE + '</p>'
        '<span class="rate"><span class="stars">★★★★★</span> 5,0/5 sur 31 avis</span></div>'
        '<div class="stats">' + stats + '</div>'
        '</div>'
        '<div class="marq"><div class="marq-t" id="hvb-marq">' + piste + '</div></div>'
        '</section>'
    )


def onglets():
    barre, panneaux = [], []
    for i, o in enumerate(C.ONGLETS):
        sel = "true" if i == 0 else "false"
        barre.append(
            '<button class="tabbtn" role="tab" id="hvb-t' + str(i) + '" '
            'aria-controls="hvb-p' + str(i) + '" aria-selected="' + sel + '" '
            'tabindex="' + ("0" if i == 0 else "-1") + '">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">'
            + C.ICONES[o["icone"]] + '</svg>' + o["onglet"] + '</button>')
        href, lib = o["lien"]
        panneaux.append(
            '<div class="tabpane" role="tabpanel" id="hvb-p' + str(i) + '" '
            'aria-labelledby="hvb-t' + str(i) + '"' + ("" if i == 0 else " hidden") + '>'
            '<div><h2>' + o["h2"] + '</h2>' + ticks(o["ticks"]) + lien_plus(href, lib) + '</div>'
            '<div class="shot">' + img(o["img"]) + '</div>'
            '</div>')
    return (
        '<section class="sec wash"><div class="w">'
        '<div class="head"><p class="over">Huit terrains de vérité</p>'
        '<h2>Là où les outils généralistes s\'arrêtent.</h2>'
        '<p class="lead">Ce ne sont pas des options : ce sont les points sur lesquels un ERP '
        'généraliste facture un développement spécifique, et sur lesquels un TMS ne se '
        'prononce pas.</p></div>'
        '<div class="tabbar" role="tablist" aria-label="Fonctions de l\'ERP import export">'
        + "".join(barre) + '</div>'
        '<div id="hvb-panes">' + "".join(panneaux) + '</div>'
        '</div></section>'
    )


def calcul():
    lignes = "".join('<tr><td>' + a + '</td><td>' + b + '</td></tr>' for a, b in C.CALC_LIGNES)
    warn = "".join('<p>' + p + '</p>' for p in C.CALC_WARN)
    return (
        '<section class="sec"><div class="w"><div class="calc-grid">'
        '<div>'
        '<p class="over">Le calcul — ce que personne ne vous montre</p>'
        '<h2>' + C.CALC_TITRE + '</h2>'
        '<p class="lead">' + C.CALC_INTRO + '</p>'
        '<div class="warn">' + warn + '</div>'
        + lien_plus("/fonctionnalites/import-export/", "Le module import export") +
        '</div>'
        '<div class="card" data-anim="rise">'
        '<p class="card-h">' + C.CALC_CARTE + '</p>'
        '<table class="lines"><tbody>' + lignes +
        '<tr class="tot"><td>' + C.CALC_TOTAL[0] + '</td><td>' + C.CALC_TOTAL[1] + '</td></tr>'
        '<tr class="coef"><td>' + C.CALC_COEF[0] + '</td><td>' + C.CALC_COEF[1] + '</td></tr>'
        '</tbody></table>'
        '<p class="note">' + C.CALC_NOTE + '</p>'
        '</div>'
        '</div></div></section>'
    )


def terrain():
    items = ["<b>" + t + "</b> — " + d for t, d in C.TERRAIN]
    return (
        '<section class="sec wash"><div class="w"><div class="split">'
        '<div class="shot" data-anim="rise">' + img("terrain") + '</div>'
        '<div>'
        '<p class="over">Réception, contrôle, préparation</p>'
        '<h2>' + C.TERRAIN_TITRE + '</h2>'
        '<p class="lead">' + C.TERRAIN_INTRO + '</p>'
        + ticks(items) +
        '</div>'
        '</div></div></section>'
    )


def comparatif():
    th = "".join('<th scope="col">' + c + '</th>' for c in C.CMP_COLS)
    tr = "".join('<tr>' + "".join('<td>' + c + '</td>' for c in l) + '</tr>'
                 for l in C.CMP_LIGNES)
    return (
        '<section class="sec"><div class="w">'
        '<div class="head"><p class="over">Se situer — TMS, ERP généraliste, ERP métier</p>'
        '<h2>' + C.CMP_TITRE + '</h2><p class="lead">' + C.CMP_INTRO + '</p></div>'
        '<div class="tw" data-anim="rise"><table class="cmp">'
        '<thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table></div>'
        '</div></section>'
    )


def modules():
    cartes = []
    for no, cle, href, titre, desc in C.MODULES:
        cartes.append(
            '<a class="mod" href="' + href + '">'
            '<div class="mod-img"><span class="mod-no">' + no + '</span>' + img(cle) + '</div>'
            '<div class="mod-b"><h3>' + titre[0].upper() + titre[1:] + '</h3>'
            '<p>' + desc + '</p>'
            '<span class="more">En savoir plus ' + fleche() + '</span></div>'
            '</a>')
    return (
        '<section class="sec wash"><div class="w">'
        '<div class="head"><p class="over">Modules — par où entrer</p>'
        '<h2>' + C.MOD_TITRE + '</h2></div>'
        '<div class="mods">' + "".join(cartes) + '</div>'
        '</div></section>'
    )


def cta_final():
    return (
        '<section class="sec"><div class="w"><div class="final" data-anim="rise">'
        '<p class="over" style="color:#7DD3FC">Démonstration</p>'
        '<h2>' + C.CTA_TITRE + '</h2>'
        '<p class="lead">' + C.CTA_INTRO + '</p>'
        '<div class="btns">'
        '<a class="btn btn-1" href="/contact/">Réserver la démonstration</a>'
        '<a class="btn btn-2" href="/negoce/">Voir toutes les briques du négoce</a>'
        '</div>'
        '</div></div></section>'
    )


def faq():
    blocs = []
    for i, (q, r) in enumerate(C.FAQ):
        blocs.append(
            '<div class="qa" data-open="' + ("1" if i == 0 else "0") + '">'
            '<button type="button" aria-expanded="' + ("true" if i == 0 else "false") + '" '
            'aria-controls="hvb-a' + str(i) + '"><span>' + q + '</span>'
            '<span class="ic" aria-hidden="true"></span></button>'
            '<div class="ans" id="hvb-a' + str(i) + '"><p>' + r + '</p></div>'
            '</div>')
    return (
        '<section class="sec wash"><div class="w">'
        '<div class="head"><p class="over">Questions — les réponses</p>'
        '<h2>' + C.FAQ_TITRE + '</h2></div>'
        '<div class="faq">' + "".join(blocs) + '</div>'
        '</div></section>'
    )


JS = """<script>
(function () {
  var r = document.getElementById('hvb');
  if (!r) { return; }
  var doux = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Les etats masques n'existent que sous .anim-on : si ce script ne tourne pas,
     ou s'il casse avant cette ligne, la page reste entierement lisible. */
  var animable = doux && 'IntersectionObserver' in window;
  if (animable) { r.classList.add('anim-on'); }

  /* --- titre mot a mot : on echelonne les delais --- */
  r.querySelectorAll('[data-anim="words"]').forEach(function (el) {
    var pas = parseInt(el.getAttribute('data-stagger'), 10) || 70;
    el.querySelectorAll('.wd').forEach(function (m, i) {
      m.style.transitionDelay = (i * pas) + 'ms';
    });
  });

  /* --- apparitions au defilement --- */
  var cibles = Array.prototype.slice.call(r.querySelectorAll('[data-anim]'));
  if (!animable) {
    cibles.forEach(function (el) { el.classList.add('seen'); });
  } else {
    var obs = new IntersectionObserver(function (ent) {
      ent.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('seen'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    cibles.forEach(function (el) { obs.observe(el); });

    /* Filet : au bout de 4 s, tout ce qui n'a pas ete revele l'est d'office.
       Aucun contenu ne peut rester invisible parce qu'un observateur n'a pas
       declenche. */
    setTimeout(function () {
      cibles.forEach(function (el) {
        if (!el.classList.contains('seen')) { el.classList.add('seen'); }
      });
    }, 4000);
  }

  /* --- defilement des logos : on duplique la piste pour une boucle sans couture --- */
  var piste = document.getElementById('hvb-marq');
  if (piste && !piste.dataset.double) {
    Array.prototype.slice.call(piste.children).forEach(function (n) {
      var c = n.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      piste.appendChild(c);
    });
    piste.dataset.double = '1';
  }

  /* --- onglets : clic, clavier, et rotation automatique jusqu'au premier clic --- */
  var bar = r.querySelector('.tabbar');
  if (bar) {
    var bts = Array.prototype.slice.call(bar.querySelectorAll('.tabbtn'));
    var pans = Array.prototype.slice.call(r.querySelectorAll('.tabpane'));
    var actif = 0, minuteur = null, arrete = false;

    function montrer(i) {
      actif = i;
      bts.forEach(function (b, k) {
        b.setAttribute('aria-selected', k === i ? 'true' : 'false');
        b.setAttribute('tabindex', k === i ? '0' : '-1');
      });
      pans.forEach(function (p, k) { p.hidden = (k !== i); });
    }
    function stop() { arrete = true; clearInterval(minuteur); minuteur = null; }

    bts.forEach(function (b, i) {
      b.addEventListener('click', function () { stop(); montrer(i); });
      b.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : (e.key === 'ArrowLeft' ? -1 : 0);
        if (!d) { return; }
        e.preventDefault(); stop();
        var n = (i + d + bts.length) % bts.length;
        montrer(n); bts[n].focus();
      });
    });

    if (doux && 'IntersectionObserver' in window) {
      var o2 = new IntersectionObserver(function (ent) {
        ent.forEach(function (e) {
          if (e.isIntersecting && !arrete && !minuteur) {
            minuteur = setInterval(function () { montrer((actif + 1) % bts.length); }, 15000);
            o2.unobserve(e.target);
          }
        });
      }, { threshold: 0.3 });
      o2.observe(bar);
    }
  }

  /* --- FAQ en accordeon --- */
  r.querySelectorAll('.qa button').forEach(function (b) {
    b.addEventListener('click', function () {
      var qa = b.closest('.qa');
      var ouvert = qa.getAttribute('data-open') === '1';
      qa.setAttribute('data-open', ouvert ? '0' : '1');
      b.setAttribute('aria-expanded', ouvert ? 'false' : 'true');
    });
  });
})();
</script>"""

BANDEAU = ('<div class="draft">VARIANTE B — test A/B, brouillon non indexé. '
           'Même contenu que la variante A, UX différente. '
           'Ne pas publier sans avoir posé le noindex.</div>')

SCHEMA_FAQ = None


def construire():
    corps = (hero() + preuve() + onglets() + calcul() + terrain() + comparatif()
             + modules() + cta_final() + faq())
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", r)}}
        for q, r in C.FAQ]}
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
            'family=Inter:wght@400;500;600;700;800;900&display=swap">'
            + CSS +
            '<div id="hvb">' + BANDEAU + corps + '</div>' + JS +
            '<script type="application/ld+json">'
            + json.dumps(ld, ensure_ascii=False) + '</script>')


# --------------------------------------------------------------------- controles
def controles(html):
    pb = []
    for t in ("div", "section", "table", "button", "a"):
        o = len(re.findall(r"<" + t + r"[ >]", html))
        f = len(re.findall(r"</" + t + r">", html))
        if o != f:
            pb.append("balises <%s> desequilibrees : %d / %d" % (t, o, f))
    if html.count("<style") != html.count("</style>"):
        pb.append("style desequilibre")
    if html.count("<script") != html.count("</script>"):
        pb.append("script desequilibre")

    # toutes les images pointent bien sur la mediatheque du site
    for u in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if not u.startswith("https://www.helloharel.com/"):
            pb.append("image hors mediatheque : " + u[:70])
    if len(re.findall(r"<img", html)) != 11 + len(C.LOGOS):
        pb.append("nombre d'images inattendu : %d" % len(re.findall(r"<img", html)))
    for c in re.findall(r'<img[^>]*alt=""', html):
        pb.append("image sans alternative textuelle")

    # Regle 0 : aucune ancre vers une page protegee
    PROT = ("/agroalimentaire/", "/agroalimentaire/traiteur/", "/agroalimentaire/charcutier/",
            "/agroalimentaire/plats-cuisines-industriels/", "/migration-as400/")
    for h in re.findall(r'<a[^>]+href="([^"]+)"', html):
        if h in PROT:
            pb.append("Regle 0 — lien vers une page protegee : " + h)

    # le fond doit etre celui de la variante A
    for att in (C.CALC_TOTAL[1], C.CALC_COEF[1], "38 390", "× 1,20"):
        if att not in html:
            pb.append("valeur du calcul absente : " + att)
    for q, _r in C.FAQ:
        if q not in html:
            pb.append("question absente : " + q[:44])
    for _n, _c, href, _t, _d in C.MODULES:
        if 'href="' + href + '"' not in html:
            pb.append("lien de module absent : " + href)

    # accessibilite des onglets et de la FAQ
    if html.count('role="tab"') != 4 or html.count('role="tabpanel"') != 4:
        pb.append("onglets : roles ARIA incomplets")
    if html.count('aria-expanded=\"') != len(C.FAQ):
        pb.append("FAQ : aria-expanded manquant")
    return pb


def main():
    html = construire()
    pb = controles(html)
    print("  taille        : %d caracteres" % len(html))
    print("  images        : %d (11 Pexels + %d logos clients)"
          % (len(re.findall(r"<img", html)), len(C.LOGOS)))
    print("  sections      : %d" % len(re.findall(r"<section", html)))
    print("  controles     : %s" % ("AUCUN DEFAUT" if not pb else "%d point(s)" % len(pb)))
    for p in pb:
        print("     !", p)

    open(os.path.join(ICI, "preview-negoce-b.html"), "w", encoding="utf-8").write(html)
    if LIVE:
        if pb:
            raise SystemExit("ecriture refusee : des controles ont echoue")
        w.api("pages/%d" % PAGE, "POST",
              {"content": html, "title": TITRE, "status": "draft"})
        print("\n  ECRIT sur la page %d (brouillon) — %s" % (PAGE, TITRE))
    else:
        print("\n  essai a blanc — rien n'a ete ecrit sur le site")


if __name__ == "__main__":
    main()
