# -*- coding: utf-8 -*-
"""
Les cinq infographies de l'article Rungis, en HTML, CSS et JS.

Regles tenues sur les cinq : aucune dependance externe, aucun contenu injecte
au clic, aucun decalage de mise en page, et TOUT est lisible sans JavaScript —
le JS n'ajoute que l'animation des compteurs et le calcul de l'ecart de poids.
Les donnees sont celles du site officiel du marche, pas des valeurs d'exemple.

Portee : #hh-page .rg — doublee en .rg pour survivre aux blocs poses hors du
conteneur du site.
"""

import blog_rungis_contenu as C


def _double(sel):
    """« .rg-nums » devient « #hh-page .rg-nums, .rg-nums »."""
    sels = []
    for x in sel.split(","):
        x = x.strip()
        if not x:
            continue
        sels.append("#hh-page " + x)
        sels.append(x)
    return ", ".join(sels)


def _sc(css):
    """Emet chaque regle dans les deux portees, Y COMPRIS dans les @media.

    La version precedente recopiait les blocs @media tels quels : les regles
    mobiles gardaient leur selecteur simple et perdaient la cascade contre les
    regles de base portees par #hh-page. Resultat mesure a 390 px : la grille
    des chiffres restait sur quatre colonnes de 68 px et decoupait « 234 » en
    « 23 / 4 ». On descend donc d'un niveau dans les media queries.
    """
    import re as _re
    out = []
    i = 0
    for m in _re.finditer(r"@media[^{]*\{", css):
        out.append(_regles(css[i:m.start()]))
        # fin du bloc @media : on suit la profondeur d'accolades
        prof, j = 1, m.end()
        while j < len(css) and prof:
            prof += 1 if css[j] == "{" else (-1 if css[j] == "}" else 0)
            j += 1
        out.append(m.group(0) + _regles(css[m.end():j - 1]) + "}")
        i = j
    out.append(_regles(css[i:]))
    return "".join(out)


def _regles(css):
    out = []
    for bloc in css.split("}"):
        if "{" not in bloc:
            out.append(bloc)
            continue
        sel, corps = bloc.split("{", 1)
        out.append(_double(sel) + "{" + corps + "}")
    return "".join(out)


CSS = "<style id=\"hh-rungis\">" + _sc("""
.rg{margin:3.2rem 0 !important;font-family:inherit}
.rg-h{display:flex;align-items:baseline;justify-content:flex-start;column-gap:.75rem;
 row-gap:.35rem;flex-wrap:wrap;margin:0 0 1rem !important}
.rg-k{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:#046C93;background:#e6f7fe;padding:.25rem .6rem !important;
 border-radius:99px;margin:0 !important}
#rg-ecart .rg-k{background:#e7fbf1;color:#0b7a47}
.rg-s{position:relative;padding-left:.75rem !important;font-size:.78rem;color:#64748b;margin:0 !important}
.rg-s::before{content:"";position:absolute;left:0;top:.35em;width:1px;height:1em;background:#cbd5e1}
.rg-t{font-size:1.3rem;line-height:1.3;font-weight:700;color:#0f172a;
 margin:.45rem 0 0 !important;letter-spacing:-.018em;flex:1 1 100%}

/* 1 — le marche en chiffres */
.rg-nums{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#e2e8f0;
 border:1px solid #e2e8f0;border-radius:16px;overflow:hidden}
.rg-num{background:#fff;padding:1.2rem 1rem;text-align:center}
.rg-num b{display:block;font-size:clamp(1.5rem,4vw,2.1rem);font-weight:800;color:#007AAE;
 letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.rg-num i{display:block;font-style:normal;font-size:.78rem;font-weight:700;color:#0f172a;
 margin-top:.35rem}
.rg-num span{display:block;font-size:.72rem;color:#64748b;margin-top:.2rem;line-height:1.4}

/* 2 — la journee de Rungis */
.rg-day{border:1px solid #e2e8f0;border-radius:16px;background:#fff;overflow:hidden}
.rg-scale{display:grid;grid-template-columns:150px 1fr;align-items:center;
 padding-right:.8rem;border-bottom:1px solid #eef2f6;background:#f8fafc;
 font-size:.7rem;color:#64748b}
.rg-scale>span:first-child{padding:.5rem .8rem}
.rg-ticks{position:relative;height:26px}
.rg-ticks u{position:absolute;top:6px;text-decoration:none;transform:translateX(-50%);
 font-variant-numeric:tabular-nums;white-space:nowrap}
.rg-ticks u:first-child{transform:none}
.rg-ticks u:last-child{transform:translateX(-100%)}
.rg-row{display:grid;grid-template-columns:150px 1fr;align-items:center;
 border-bottom:1px solid #f1f5f9}
@media(min-width:761px){
 .rg-scale,.rg-row{grid-template-columns:200px 1fr}
 .rg-row{min-height:56px}
}
.rg-row:last-child{border-bottom:0}
.rg-lab{padding:.55rem .8rem;min-width:0}
.rg-lab b{display:block;font-size:.8rem;font-weight:600;color:#0f172a;line-height:1.25}
.rg-lab span{display:block;font-size:.68rem;color:#64748b;margin-top:.1rem}
.rg-track{position:relative;height:30px;margin-right:.8rem}
.rg-track::before{content:"";position:absolute;inset:0;border-radius:2px;background:
 linear-gradient(#f1f5f9,#f1f5f9) 0 50%/100% 3px no-repeat,
 repeating-linear-gradient(90deg,#e9eef4 0 1px,transparent 1px calc(100%/6))}
.rg-band{position:absolute;top:7px;height:16px;border-radius:99px;display:flex;
 align-items:center;padding:0 .5rem;color:#0f172a;font-size:.7rem;font-weight:700;
 white-space:nowrap;font-variant-numeric:tabular-nums}
.rg-src{font-size:.72rem;color:#64748b;padding:.7rem .8rem !important;border-top:1px solid #eef2f6;
 background:#f8fafc;margin:0 !important}

/* 3 — le parcours de la carte */
.rg-steps{counter-reset:s;display:grid;gap:.7rem}
.rg-step{display:grid;grid-template-columns:38px 1fr;gap:.9rem;align-items:start;
 border:1px solid #e2e8f0;border-radius:14px;padding:.95rem 1.1rem;background:#fff}
.rg-step::before{counter-increment:s;content:counter(s);width:38px;height:38px;
 border-radius:50%;background:#ecfeff;color:#0e7490;font-weight:800;font-size:.9rem;
 display:grid;place-items:center}
.rg-step b{display:block;font-size:.95rem;color:#0f172a;line-height:1.35}
.rg-step span{display:block;font-size:.86rem;color:#475569;margin-top:.25rem;line-height:1.55}

/* 4 — du carreau a la facture */
.rg-flow{display:grid;grid-template-columns:repeat(5,1fr);gap:.6rem;counter-reset:fx}
.rg-node{border:1px solid #e2e8f0;border-top:3px solid #00B1F5;border-radius:12px;
 padding:.9rem .8rem;background:#fff;position:relative}
.rg-node{counter-increment:fx}
.rg-node b{display:block;font-size:.85rem;color:#0f172a}
.rg-node b::before{content:counter(fx);display:inline-grid;place-items:center;width:20px;
 height:20px;margin-right:.45rem;border-radius:50%;background:#e0f2fe;color:#046C93;
 font-size:.68rem;font-weight:800;vertical-align:1px}
.rg-node:nth-child(2) b::before,.rg-node:nth-child(5) b::before{background:#fee2e2;color:#b91c1c}
.rg-node+.rg-node::before{content:"";position:absolute;left:-.6rem;top:50%;width:.6rem;
 height:1px;background:#cbd5e1}
.rg-node+.rg-node::after{content:"";position:absolute;left:-.42rem;top:50%;width:5px;height:5px;
 border-top:1px solid #94a3b8;border-right:1px solid #94a3b8;
 transform:translateY(-50%) rotate(45deg)}
.rg-lg{display:flex;align-items:center;gap:.45rem;font-size:.74rem;color:#64748b;
 margin:.8rem 0 0 !important}
.rg-lg i{width:14px;height:14px;border-radius:4px;background:#fef7f7;border:1px solid #fecaca;
 border-top:3px solid #EF4444;flex:0 0 auto}
.rg-node span{display:block;font-size:.76rem;color:#475569;margin-top:.3rem;line-height:1.5}
.rg-node:nth-child(2),.rg-node:nth-child(5){border-top-color:#EF4444;background:#fef7f7}

/* 5 — l'ecart de poids */
.rg-calc{border:1px solid #e2e8f0;border-radius:16px;background:#fff;overflow:hidden}
.rg-in{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem;padding:1.1rem}
.rg-fld label{display:block;font-size:.76rem;font-weight:600;color:#475569;
 margin:0 0 .3rem !important}
.rg-fld input{width:100%;font:inherit;font-size:16px;padding:.55rem .7rem;
 border:1px solid #cbd5e1;border-radius:10px;background:#fff;color:#0f172a;
 font-variant-numeric:tabular-nums}
.rg-fld input:focus-visible{outline:2px solid #00B1F5;outline-offset:1px;border-color:#00B1F5}
.rg-fld input::-webkit-outer-spin-button,.rg-fld input::-webkit-inner-spin-button{
 -webkit-appearance:none;margin:0}
.rg-out{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#e2e8f0;
 border-top:1px solid #e2e8f0}
.rg-out div{background:#f8fafc;padding:1rem 1.1rem}
.rg-out b{display:block;font-size:1.5rem;font-weight:800;color:#0f172a;
 font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.rg-out .perte{background:#fef7f7;box-shadow:inset 3px 0 0 #b91c1c}
.rg-out .perte b{color:#b91c1c}
.rg-out div:first-child{box-shadow:inset 3px 0 0 #16DB7F}
.rg-out span{display:block;font-size:.76rem;color:#64748b;margin-top:.2rem}

@media(max-width:760px){
 .rg-nums{grid-template-columns:repeat(2,1fr)}
 .rg-out{grid-template-columns:1fr}
 .rg-out b{font-size:clamp(1.35rem,6vw,1.5rem)}
 .rg-scale{padding:0 .8rem}
 .rg-node+.rg-node::before{left:50%;top:-.6rem;width:1px;height:.6rem}
 .rg-node+.rg-node::after{left:50%;top:-.32rem;transform:translateX(-50%) rotate(135deg)}
 .rg-flow{grid-template-columns:1fr}
 .rg-in{grid-template-columns:1fr}
 .rg-scale,.rg-row{grid-template-columns:1fr}
 .rg-lab{padding:.6rem .8rem .2rem}
 .rg-track{margin:0 .8rem .55rem}
 .rg-scale>span:first-child{display:none}
 .rg-ticks{height:22px}
}
""") + "</style>"


# --------------------------------------------------------------- 1. chiffres
def chiffres():
    cases = "".join(
        '<div class="rg-num"><b data-n="%s">%s</b><i>%s</i><span>%s</span></div>'
        % (v, v, u, l) for v, u, l in C.CHIFFRES)
    return ('<figure class="rg" id="rg-chiffres">'
            '<figcaption class="rg-h"><p class="rg-k">Le marché en chiffres</p>'
            '<p class="rg-s">Source : site officiel du marché, 2024</p>'
            '<p class="rg-t">Rungis, premier marché de produits frais au monde</p>'
            '</figcaption><div class="rg-nums">' + cases + '</div></figure>')


# --------------------------------------------------------------- 2. journee
def journee():
    DEB, FIN = 2.0, 20.0
    span = FIN - DEB
    ticks = "".join('<u style="left:%.2f%%">%dh</u>' % ((h - DEB) / span * 100, h)
                    for h in (2, 5, 8, 11, 14, 17, 20))
    lignes = ""
    for nom, jours, d, f, coul in C.HORAIRES:
        g = (d - DEB) / span * 100
        w = (f - d) / span * 100
        lab = "%s → %s" % (("%dh30" % int(d)) if d % 1 else "%dh" % d,
                           ("%dh30" % int(f)) if f % 1 else "%dh" % f)
        lignes += ('<div class="rg-row"><div class="rg-lab"><b>%s</b><span>%s</span></div>'
                   '<div class="rg-track"><span class="rg-band" '
                   'style="left:%.2f%%;width:%.2f%%;background:%s">%s</span></div></div>'
                   % (nom, jours, g, w, coul, lab))
    return ('<figure class="rg" id="rg-journee">'
            '<figcaption class="rg-h"><p class="rg-k">La journée de Rungis</p>'
            '<p class="rg-s">Horaires relevés le 11 septembre 2026</p>'
            '<p class="rg-t">Onze secteurs, onze horaires différents</p></figcaption>'
            '<div class="rg-day"><div class="rg-scale"><span>Secteur</span>'
            '<span class="rg-ticks">' + ticks + '</span></div>' + lignes +
            '<p class="rg-src">Bleu soutenu : la marée et les fruits et légumes, les deux '
            'secteurs qui encadrent la journée. Bleu clair : les autres produits frais. '
            'Gris : fleurs, plantes, accessoires et services. '
            'Source : ' + C.SOURCE + '.</p></div></figure>')


# --------------------------------------------------------------- 3. la carte
def carte():
    etapes = "".join('<div class="rg-step"><div><b>%s</b><span>%s</span></div></div>'
                     % (t, d) for t, d in C.CARTE)
    return ('<figure class="rg" id="rg-carte">'
            '<figcaption class="rg-h"><p class="rg-k">Accès professionnel</p>'
            '<p class="rg-t">Obtenir sa carte d\'acheteur, en quatre temps</p></figcaption>'
            '<div class="rg-steps">' + etapes + '</div></figure>')


# --------------------------------------------------------------- 4. le flux
def flux():
    n = "".join('<div class="rg-node"><b>%s</b><span>%s</span></div>' % (t, d)
                for t, d in C.FLUX)
    return ('<figure class="rg" id="rg-flux">'
            '<figcaption class="rg-h"><p class="rg-k">Du carreau à la facture</p>'
            '<p class="rg-t">Les deux étapes où la marge se perd</p></figcaption>'
            '<div class="rg-flow">' + n + '</div>'
            '<p class="rg-lg"><i></i>Les deux étapes où la marge se perd</p></figure>')


# --------------------------------------------------------------- 5. l'ecart
def ecart():
    return ('<figure class="rg" id="rg-ecart">'
            '<figcaption class="rg-h"><p class="rg-k">Calcul</p>'
            '<p class="rg-s">Modifiez les trois valeurs</p>'
            '<p class="rg-t">Ce que coûte l\'écart entre le kilo acheté et le kilo facturé'
            '</p></figcaption>'
            '<div class="rg-calc"><div class="rg-in">'
            '<div class="rg-fld"><label for="rg-kg">Kilos achetés par jour</label>'
            '<input type="number" inputmode="decimal" id="rg-kg" value="1200" min="0" step="10"></div>'
            '<div class="rg-fld"><label for="rg-ec">Écart de poids constaté (%)</label>'
            '<input type="number" inputmode="decimal" id="rg-ec" value="1.5" min="0" max="20" step="0.1"></div>'
            '<div class="rg-fld"><label for="rg-pr">Prix de vente au kilo (€)</label>'
            '<input type="number" inputmode="decimal" id="rg-pr" value="4.20" min="0" step="0.1"></div>'
            '</div><div class="rg-out"><div><b id="rg-r1">75,60 €</b>'
            '<span>de marchandise non facturée par jour</span></div>'
            '<div class="perte"><b id="rg-r2">19 656 €</b>'
            '<span>sur une année de 260 jours ouvrés</span></div></div>'
            '<p class="rg-src">Les valeurs de départ sont un exemple, pas une moyenne de '
            'marché : remplacez-les par les vôtres. Le calcul est '
            'kilos × écart × prix de vente.</p></div></figure>')


JS = """<script>
/* Les deux seules choses que le JS ajoute : le compteur des chiffres cles et
   le calcul de l'ecart. Sans lui, les valeurs de depart restent affichees et
   justes — rien ne disparait. */
(function () {
  var kg = document.getElementById('rg-kg');
  var ec = document.getElementById('rg-ec');
  var pr = document.getElementById('rg-pr');
  var r1 = document.getElementById('rg-r1');
  var r2 = document.getElementById('rg-r2');
  if (kg && ec && pr && r1 && r2) {
    var eur = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR',
      maximumFractionDigits: 2 });
    var eur0 = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR',
      maximumFractionDigits: 0 });
    var calc = function () {
      var j = (+kg.value || 0) * ((+ec.value || 0) / 100) * (+pr.value || 0);
      r1.textContent = eur.format(j);
      r2.textContent = eur0.format(j * 260);
    };
    [kg, ec, pr].forEach(function (i) { i.addEventListener('input', calc); });
    calc();
  }

  var cases = document.querySelectorAll('#rg-chiffres .rg-num b');
  if (!cases.length || !('IntersectionObserver' in window)) { return; }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) { return; }
      io.unobserve(e.target);
      var fin = e.target.dataset.n;
      var num = parseFloat(fin.replace(/\\s/g, '').replace(',', '.'));
      if (isNaN(num)) { return; }
      var dec = (fin.indexOf(',') > -1) ? 2 : 0;
      var t0 = null;
      var pas = function (t) {
        if (!t0) { t0 = t; }
        var p = Math.min((t - t0) / 900, 1);
        var v = num * (1 - Math.pow(1 - p, 3));
        e.target.textContent = v.toLocaleString('fr-FR', {
          minimumFractionDigits: dec, maximumFractionDigits: dec });
        if (p < 1) { requestAnimationFrame(pas); } else { e.target.textContent = fin; }
      };
      requestAnimationFrame(pas);
    });
  }, { threshold: 0.4 });
  Array.prototype.forEach.call(cases, function (c) { io.observe(c); });
})();
</script>"""
