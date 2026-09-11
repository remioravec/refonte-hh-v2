# -*- coding: utf-8 -*-
"""
Un visuel par H2, pour l'article des mentions obligatoires. Six H2, six visuels :

  H2 1  checklist cochable des 23 mentions   module interactif, au-dessus du 2e ecran
  H2 2  versus — 15 mentions hier, 19 demain
  H2 3  chronologie du calendrier, en vigueur et a venir
  H2 4  les trois formats acceptes
  H2 5  chiffres cles des sanctions
  H2 6  l'ecran du logiciel

Regles tenues : aucune dependance externe, aucun contenu injecte au clic,
aucun decalage de mise en page, et TOUT reste lisible sans JavaScript — les
vingt-trois lignes de la checklist sont dans le document, le JS n'ajoute que
le compteur. Les donnees sont sourcees et datees, jamais decoratives.
"""

import blog_facture_contenu as C


def _double(sel):
    out = []
    for x in sel.split(","):
        x = x.strip()
        if x:
            out.append("#hh-page " + x)
            out.append(x)
    return ", ".join(out)


def _regles(css):
    out = []
    for b in css.split("}"):
        if "{" not in b:
            out.append(b)
            continue
        s, c = b.split("{", 1)
        out.append(_double(s) + "{" + c + "}")
    return "".join(out)


def _sc(css):
    import re
    out, i = [], 0
    for m in re.finditer(r"@media[^{]*\{", css):
        out.append(_regles(css[i:m.start()]))
        prof, j = 1, m.end()
        while j < len(css) and prof:
            prof += 1 if css[j] == "{" else (-1 if css[j] == "}" else 0)
            j += 1
        out.append(m.group(0) + _regles(css[m.end():j - 1]) + "}")
        i = j
    out.append(_regles(css[i:]))
    return "".join(out)


CSS = "<style id=\"hh-fac\">" + _sc("""
.fa2{margin:3.2rem 0 !important}
.fa2-h{display:flex;align-items:baseline;flex-wrap:wrap;column-gap:.75rem;row-gap:.35rem;
 margin:0 0 1.1rem !important}
.fa2-k{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:#046C93;background:#e6f7fe;padding:.25rem .6rem;
 border-radius:99px;margin:0 !important}
.fa2-s{position:relative;padding-left:.75rem;font-size:.78rem;color:#64748b;margin:0 !important}
.fa2-s::before{content:"";position:absolute;left:0;top:.35em;width:1px;height:1em;background:#cbd5e1}
.fa2-t{flex:1 1 100%;font-size:1.3rem;line-height:1.3;font-weight:700;color:#0f172a;
 letter-spacing:-.018em;margin:.45rem 0 0 !important}
.fa2-src{font-size:.76rem;color:#64748b;padding:.75rem .95rem;background:#f8fafc;
 border-top:1px solid #eef2f6;line-height:1.5;margin:0 !important}

/* 1 — checklist */
.ck{border:1px solid #e2e8f0;border-radius:16px;background:#fff;overflow:hidden}
.ck-bar{display:flex;align-items:center;gap:.85rem;padding:.9rem 1.1rem;background:#f8fafc;
 border-bottom:1px solid #eef2f6;flex-wrap:wrap}
.ck-cnt{font-size:.92rem;font-weight:700;color:#0f172a;font-variant-numeric:tabular-nums;
 white-space:nowrap}
.ck-prog{flex:1;min-width:120px;height:9px;border-radius:99px;background:#e2e8f0;overflow:hidden}
.ck-prog i{display:block;height:100%;width:0;border-radius:99px;background:#16DB7F;
 transition:width .25s ease}
.ck-rst{font:inherit;font-size:.78rem;font-weight:600;color:#475569;background:#fff;
 border:1px solid #d7dde3;border-radius:99px;padding:.35rem .8rem;cursor:pointer}
.ck-rst:hover{border-color:#00B1F5;color:#0f172a}
.ck-rst:focus-visible{outline:2px solid #0f172a;outline-offset:2px}
.ck-g{font-size:.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;
 color:#64748b;background:#f1f5f9;padding:.45rem 1.1rem;margin:0 !important}
.ck-i{display:flex;align-items:flex-start;gap:.8rem;padding:.7rem 1.1rem;
 border-bottom:1px solid #f1f5f9;cursor:pointer}
.ck-i:last-of-type{border-bottom:0}
.ck-i input{appearance:none;-webkit-appearance:none;width:20px;height:20px;flex:0 0 20px;
 margin:2px 0 0;border:2px solid #cbd5e1;border-radius:6px;background:#fff;cursor:pointer;
 display:grid;place-items:center}
.ck-i input:checked{background:#16DB7F;border-color:#16DB7F}
.ck-i input:checked::after{content:"";width:10px;height:6px;border-left:2px solid #fff;
 border-bottom:2px solid #fff;transform:rotate(-45deg) translate(1px,-1px)}
.ck-i input:focus-visible{outline:2px solid #0f172a;outline-offset:2px}
.ck-i b{display:block;font-size:.92rem;font-weight:600;color:#0f172a;line-height:1.35}
.ck-i span{display:block;font-size:.82rem;color:#64748b;margin-top:.15rem;line-height:1.5}
.ck-i.neuf b::after{content:"nouveau";margin-left:.5rem;font-size:.62rem;font-weight:800;
 letter-spacing:.06em;text-transform:uppercase;color:#96650E;background:#fef6e6;
 padding:.12rem .45rem;border-radius:99px;vertical-align:2px}
.ck-i input:checked~div b{color:#64748b;text-decoration:line-through}

/* 2 — versus */
.vs{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:stretch}
.vs-c{border:1px solid #e2e8f0;border-radius:16px;padding:1.1rem 1.2rem;background:#fff}
.vs-c.apres{border-color:#16DB7F;background:#f3fdf8}
.vs-c em{display:block;font-style:normal;font-size:.72rem;font-weight:800;letter-spacing:.08em;
 text-transform:uppercase;color:#64748b}
.vs-c.apres em{color:#0b7a47}
.vs-c b{display:block;font-size:2.3rem;font-weight:800;color:#0f172a;line-height:1.05;
 margin-top:.3rem;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.vs-c span{display:block;font-size:.84rem;color:#475569;margin-top:.35rem;line-height:1.5}
.vs-a{display:grid;place-items:center;font-size:1.5rem;color:#94a3b8}
.vs-l{list-style:none;padding:0;margin:1rem 0 0 !important;display:grid;gap:.55rem}
.vs-l li{display:flex;gap:.6rem;font-size:.86rem;color:#334155;line-height:1.45;padding:0}
.vs-l li::before{content:"+";color:#16DB7F;font-weight:800;flex:0 0 auto}

/* 3 — calendrier */
.cal{border:1px solid #e2e8f0;border-radius:16px;background:#fff;overflow:hidden}
.cal-r{display:grid;grid-template-columns:150px 1fr;border-bottom:1px solid #f1f5f9}
.cal-r:last-child{border-bottom:0}
.cal-d{display:flex;flex-direction:column;justify-content:center;gap:.3rem;padding:.95rem 1.1rem;
 background:#f8fafc;border-right:1px solid #eef2f6}
.cal-d b{font-size:.88rem;font-weight:800;color:#0f172a;font-variant-numeric:tabular-nums}
.cal-p{display:inline-block;font-size:.62rem;font-weight:800;letter-spacing:.06em;
 text-transform:uppercase;padding:.15rem .5rem;border-radius:99px;width:max-content}
.cal-p.on{background:#e9fbf2;color:#0b7a47}
.cal-p.off{background:#f1f5f9;color:#64748b}
.cal-b{padding:.95rem 1.1rem}
.cal-b b{display:block;font-size:.95rem;color:#0f172a}
.cal-b span{display:block;font-size:.86rem;color:#475569;margin-top:.25rem;line-height:1.55}

/* 4 — formats */
.fmt{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem}
.fmt-c{border:1px solid #e2e8f0;border-top:3px solid #00B1F5;border-radius:14px;
 padding:1rem 1.1rem;background:#fff}
.fmt-c:first-child{border-top-color:#16DB7F;background:#f8fefb}
.fmt-c b{display:block;font-size:1.02rem;font-weight:700;color:#0f172a}
.fmt-c em{display:block;font-style:normal;font-size:.74rem;font-weight:700;color:#046C93;
 margin-top:.2rem}
.fmt-c span{display:block;font-size:.84rem;color:#475569;margin-top:.45rem;line-height:1.5}

/* 5 — sanctions */
.snc{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:#e2e8f0;
 border:1px solid #e2e8f0;border-radius:16px;overflow:hidden}
.snc-c{background:#fff;padding:1.15rem 1.2rem}
.snc-c b{display:block;font-size:1.9rem;font-weight:800;color:#b91c1c;line-height:1;
 letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.snc-c em{display:block;font-style:normal;font-size:.84rem;font-weight:700;color:#0f172a;
 margin-top:.35rem}
.snc-c span{display:block;font-size:.8rem;color:#64748b;margin-top:.2rem;line-height:1.5}

@media(max-width:760px){
 .vs{grid-template-columns:1fr}
 .vs-a{transform:rotate(90deg)}
 .fmt{grid-template-columns:1fr}
 .snc{grid-template-columns:1fr}
 .cal-r{grid-template-columns:1fr}
 .cal-d{border-right:0;border-bottom:1px solid #eef2f6;flex-direction:row;align-items:center;
  gap:.6rem}
}
""") + "</style>"


def _tete(k, t, s=None):
    return ('<figcaption class="fa2-h"><p class="fa2-k">%s</p>%s<p class="fa2-t">%s</p>'
            '</figcaption>' % (k, ('<p class="fa2-s">%s</p>' % s) if s else '', t))


def checklist():
    lignes, groupe = [], None
    n = 0
    for g, lib, det in C.MENTIONS:
        if g != groupe:
            groupe = g
            lignes.append('<p class="ck-g">%s</p>' % g)
        n += 1
        lignes.append('<label class="ck-i"><input type="checkbox" class="ck-b2"><div><b>%s</b>%s'
                      '</div></label>'
                      % (lib, ('<span>%s</span>' % det) if det else ''))
    lignes.append('<p class="ck-g">Avec la facturation électronique</p>')
    for lib, det in C.NOUVELLES:
        n += 1
        lignes.append('<label class="ck-i neuf"><input type="checkbox" class="ck-b2">'
                      '<div><b>%s</b><span>%s</span></div></label>' % (lib, det))
    return ('<figure class="fa2" id="fa-check">'
            + _tete("Checklist", "Les %d mentions, une par une" % n,
                    "Cochez ce que porte déjà votre facture")
            + '<div class="ck"><div class="ck-bar">'
              '<span class="ck-cnt" id="ck-cnt">0 / %d</span>'
              '<span class="ck-prog"><i id="ck-prog"></i></span>'
              '<button type="button" class="ck-rst" id="ck-rst">Tout décocher</button>'
              '</div>' % n
            + "".join(lignes)
            + '<p class="fa2-src">Sources : %s ; %s. Relevé le %s.</p></div></figure>'
              % (C.SOURCES["sp_mentions"][0], C.SOURCES["loi"][0], C.RELEVE))


def versus():
    plus = "".join("<li>%s</li>" % t for t, _ in C.NOUVELLES)
    av = len(C.MENTIONS)
    ap = av + len(C.NOUVELLES)
    return ('<figure class="fa2" id="fa-vs">'
            + _tete("Ce qui change", "Quatre mentions de plus, et pas des moindres")
            + '<div class="vs">'
              '<div class="vs-c"><em>Jusqu\'à la réforme</em><b>%d</b>'
              '<span>mentions obligatoires sur une facture entre professionnels.</span></div>'
              '<div class="vs-a">→</div>'
              '<div class="vs-c apres"><em>Avec la facture électronique</em><b>%d</b>'
              '<span>Les quatre ajoutées :</span><ul class="vs-l">%s</ul></div>'
              '</div></figure>' % (av, ap, plus))


def calendrier():
    r = ""
    for date, quoi, det, envig in C.CALENDRIER:
        r += ('<div class="cal-r"><div class="cal-d"><b>%s</b>'
              '<span class="cal-p %s">%s</span></div>'
              '<div class="cal-b"><b>%s</b><span>%s</span></div></div>'
              % (date, "on" if envig else "off",
                 "en vigueur" if envig else "à venir", quoi, det))
    return ('<figure class="fa2" id="fa-cal">'
            + _tete("Calendrier", "Ce qui s'applique déjà, et ce qui arrive",
                    "Arrêté au %s" % C.RELEVE)
            + '<div class="cal">' + r + '</div></figure>')


def formats():
    c = "".join('<div class="fmt-c"><b>%s</b><em>%s</em><span>%s</span></div>' % f
                for f in C.FORMATS)
    return ('<figure class="fa2" id="fa-fmt">'
            + _tete("Les formats", "Trois formats acceptés, un seul se lit à l'œil")
            + '<div class="fmt">' + c + '</div></figure>')


def sanctions():
    c = "".join('<div class="snc-c"><b>%s</b><em>%s</em><span>%s</span></div>' % s
                for s in C.SANCTIONS)
    return ('<figure class="fa2" id="fa-snc">'
            + _tete("Ce que coûte un oubli", "L'amende se compte par mention, pas par facture",
                    "Source : %s" % C.SOURCES["sp_sanctions"][0])
            + '<div class="snc">' + c + '</div></figure>')


JS = """<script>
/* La checklist : le JS n'ajoute que le compteur. Les vingt-trois lignes sont
   dans le document et restent lisibles et cochables sans lui. */
(function () {
  var cases = document.querySelectorAll('.ck-b2');
  var cnt = document.getElementById('ck-cnt');
  var prog = document.getElementById('ck-prog');
  var rst = document.getElementById('ck-rst');
  if (!cases.length || !cnt || !prog) { return; }
  var total = cases.length;
  function maj() {
    var n = 0;
    Array.prototype.forEach.call(cases, function (c) { if (c.checked) { n++; } });
    cnt.textContent = n + ' / ' + total;
    prog.style.width = (n / total * 100) + '%';
  }
  Array.prototype.forEach.call(cases, function (c) { c.addEventListener('change', maj); });
  if (rst) {
    rst.addEventListener('click', function () {
      Array.prototype.forEach.call(cases, function (c) { c.checked = false; });
      maj();
    });
  }
  maj();
})();
</script>"""
