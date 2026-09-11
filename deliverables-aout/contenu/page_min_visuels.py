# -*- coding: utf-8 -*-
"""
Un visuel par H2, pour la page MIN. Six H2, six visuels :

  H2 1  tableau triable des 17 MIN     module interactif, au-dessus du 2e ecran
  H2 2  infographie « process »        du carreau a la facture, 5 etapes
  H2 3  photo                          la pesee
  H2 4  infographie « chronologie »    la vie d'un lot a DLC courte
  H2 5  photo                          le stock entre trois endroits
  H2 6  ecran du logiciel              reproduit en HTML, pas une capture

Aucune dependance externe. Tout reste lisible SANS JavaScript : le tableau est
complet et deja trie dans le document, le JS n'ajoute que le tri au clic et le
filtre par region. Aucun contenu injecte au clic, aucun decalage de mise en page.

Portee doublee sous #hh-page et sans : les blocs peuvent atterrir hors du
conteneur du site.
"""

import base64
import os

import page_min_contenu as C
import blog_min_contenu as M     # la liste des 17 MIN, source unique
import agro_ui as UI             # les briques du kit d'ecrans
import min_data as M2

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"


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
    for bloc in css.split("}"):
        if "{" not in bloc:
            out.append(bloc)
            continue
        sel, corps = bloc.split("{", 1)
        out.append(_double(sel) + "{" + corps + "}")
    return "".join(out)


def _sc(css):
    """Double la portee, y compris a l'interieur des @media."""
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


CSS = "<style id=\"hh-min-page\">" + _sc("""
.mn{margin:3.2rem 0 !important}
.mn-h{display:flex;align-items:baseline;flex-wrap:wrap;column-gap:.75rem;row-gap:.35rem;
 margin:0 0 1.1rem !important}
.mn-k{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:#046C93;background:#e6f7fe;padding:.25rem .6rem;
 border-radius:99px;margin:0 !important}
.mn-s{position:relative;padding-left:.75rem;font-size:.78rem;color:#64748b;margin:0 !important}
.mn-s::before{content:"";position:absolute;left:0;top:.35em;width:1px;height:1em;background:#cbd5e1}
.mn-t{flex:1 1 100%;font-size:1.3rem;line-height:1.3;font-weight:700;color:#0f172a;
 letter-spacing:-.018em;margin:.45rem 0 0 !important}

/* --- photo --- */
.mn-ph{margin:0 !important;border-radius:18px;overflow:hidden;border:1px solid #e2e8f0;
 background:#f1f5f9;line-height:0}
.mn-ph img{width:100%;height:auto;display:block;aspect-ratio:16/10;object-fit:cover}
.mn-cap{font-size:.78rem;color:#64748b;padding:.75rem .95rem;background:#f8fafc;
 border-top:1px solid #e2e8f0;line-height:1.5;margin:0 !important}

/* --- tableau des 17 MIN --- */
.mn-bar{display:flex;flex-wrap:wrap;gap:.45rem;margin:0 0 1rem !important}
.mn-f{font:inherit;font-size:.82rem;font-weight:600;padding:.42rem .85rem;border:1px solid #d7dde3;
 background:#fff;color:#475569;border-radius:999px;cursor:pointer}
.mn-f:hover{border-color:#00B1F5;color:#0f172a}
.mn-f.on{background:#00B1F5;border-color:#00B1F5;color:#fff}
.mn-f:focus-visible{outline:2px solid #0f172a;outline-offset:2px}
.mn-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid #e2e8f0;
 border-radius:16px;background:#fff}
.mn-tab{width:100%;border-collapse:collapse;font-size:.88rem;margin:0 !important}
.mn-tab caption{caption-side:bottom;text-align:left;padding:.75rem .95rem;font-size:.76rem;
 line-height:1.5;color:#64748b;border-top:1px solid #eef2f6}
.mn-tab th,.mn-tab td{padding:.62rem .95rem;text-align:left;border-bottom:1px solid #eef2f6}
.mn-tab thead th{background:#f8fafc;font-weight:600;color:#0f172a;white-space:nowrap}
.mn-tab tbody th{font-weight:600;color:#0f172a}
.mn-tab tbody tr:nth-child(even) th,.mn-tab tbody tr:nth-child(even) td{background:#fbfcfd}
.mn-tab tbody tr:last-child th,.mn-tab tbody tr:last-child td{border-bottom:0}
.mn-n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.mn-s2{font:inherit;font-weight:600;color:#0f172a;background:none;border:0;padding:0;
 cursor:pointer;display:inline-flex;align-items:center;gap:.3rem}
.mn-s2::after{content:"↕";font-size:.78em;color:#94a3b8}
.mn-s2.on::after{content:"↓";color:#00B1F5}
.mn-s2:focus-visible{outline:2px solid #0f172a;outline-offset:2px}
.mn-mut{color:#64748b}
.mn-cnt{margin:.8rem 0 0 !important;font-size:.82rem;color:#64748b}

/* --- process : du carreau a la facture --- */
.mn-flow{display:grid;grid-template-columns:repeat(5,1fr);gap:.6rem;counter-reset:fx}
.mn-node{position:relative;counter-increment:fx;border:1px solid #e2e8f0;border-top:3px solid #00B1F5;
 border-radius:12px;padding:.9rem .8rem;background:#fff}
.mn-node:nth-child(2),.mn-node:nth-child(5){border-top-color:#EF4444;background:#fef7f7}
.mn-node b{display:block;font-size:.85rem;color:#0f172a}
.mn-node b::before{content:counter(fx);display:inline-grid;place-items:center;width:20px;height:20px;
 margin-right:.45rem;border-radius:50%;background:#e0f2fe;color:#046C93;font-size:.68rem;
 font-weight:800;vertical-align:1px}
.mn-node:nth-child(2) b::before,.mn-node:nth-child(5) b::before{background:#fee2e2;color:#b91c1c}
.mn-node span{display:block;font-size:.76rem;color:#475569;margin-top:.3rem;line-height:1.5}
.mn-node+.mn-node::before{content:"";position:absolute;left:-.6rem;top:50%;width:.6rem;height:1px;
 background:#cbd5e1}
.mn-node+.mn-node::after{content:"";position:absolute;left:-.42rem;top:50%;width:5px;height:5px;
 border-top:1px solid #94a3b8;border-right:1px solid #94a3b8;transform:translateY(-50%) rotate(45deg)}
.mn-lg{display:flex;align-items:center;gap:.45rem;font-size:.74rem;color:#64748b;
 margin:.8rem 0 0 !important}
.mn-lg i{width:14px;height:14px;border-radius:4px;background:#fef7f7;border:1px solid #fecaca;
 border-top:3px solid #EF4444;flex:0 0 auto}

/* --- les trois contraintes --- */
.mn-tri{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem;margin:0 0 1.2rem !important}
.mn-c{border:1px solid #e2e8f0;border-radius:14px;padding:1rem 1.1rem;background:#fff}
.mn-c b{display:block;font-size:.95rem;color:#0f172a}
.mn-c span{display:block;font-size:.82rem;color:#475569;margin-top:.35rem;line-height:1.5}
.mn-c em{display:block;font-style:normal;font-size:.8rem;color:#b91c1c;font-weight:600;
 margin-top:.5rem;padding-top:.5rem;border-top:1px dashed #fecaca}

/* --- densites --- */
.mn-dens{border:1px solid #e2e8f0;border-radius:16px;background:#fff;overflow:hidden;
 padding:.5rem 0 0}
.mn-dr{display:grid;grid-template-columns:150px 1fr 78px;align-items:center;gap:.7rem;
 padding:.4rem 1rem}
.mn-dn{font-size:.82rem;font-weight:600;color:#0f172a;min-width:0;overflow:hidden;
 text-overflow:ellipsis;white-space:nowrap}
.mn-dt{display:block;height:12px;border-radius:99px;background:#f1f5f9;overflow:hidden}
.mn-dt i{display:block;height:100%;border-radius:99px;
 background:linear-gradient(90deg,#00B1F5,#0079b8)}
.mn-dv{font-size:.8rem;font-weight:700;color:#0f172a;text-align:right;
 font-variant-numeric:tabular-nums}
.mn-dens .mn-cap{margin-top:.5rem !important}

/* --- chronologie du lot --- */
.mn-tl{border:1px solid #e2e8f0;border-radius:16px;background:#fff;overflow:hidden}
.mn-step{display:grid;grid-template-columns:64px 1fr;gap:0;border-bottom:1px solid #f1f5f9;
 position:relative}
.mn-step:last-child{border-bottom:0}
.mn-j{display:grid;place-items:center;background:#f8fafc;border-right:1px solid #eef2f6;
 font-size:.8rem;font-weight:800;color:#046C93;font-variant-numeric:tabular-nums}
.mn-step:last-child .mn-j{background:#fef7f7;color:#b91c1c}
.mn-d{padding:.85rem 1.1rem}
.mn-d b{display:block;font-size:.92rem;color:#0f172a}
.mn-d span{display:block;font-size:.82rem;color:#475569;margin-top:.2rem;line-height:1.5}

@media(max-width:760px){
 .mn-flow{grid-template-columns:1fr}
 .mn-tri{grid-template-columns:1fr}
 .mn-node+.mn-node::before{left:50%;top:-.6rem;width:1px;height:.6rem}
 .mn-node+.mn-node::after{left:50%;top:-.32rem;transform:translateX(-50%) rotate(135deg)}
 .mn-tab{font-size:.8rem}
 .mn-tab th,.mn-tab td{padding:.5rem .6rem}
 .mn-dr{grid-template-columns:1fr 62px;row-gap:.2rem}
 .mn-dn{grid-column:1 / -1}
}
""") + "</style>"


def _tete(kicker, titre, source=None):
    s = '<p class="mn-s">%s</p>' % source if source else ''
    return ('<figcaption class="mn-h"><p class="mn-k">%s</p>%s<p class="mn-t">%s</p></figcaption>'
            % (kicker, s, titre))


def photo(cle, kicker, titre, legende):
    nom, alt = C.PHOTOS[cle]
    f = os.path.join(S, nom)
    if not os.path.exists(f):
        raise SystemExit("ARRET — photo absente : %s" % f)
    uri = "data:image/webp;base64," + base64.b64encode(open(f, "rb").read()).decode()
    return ('<figure class="mn">' + _tete(kicker, titre) +
            '<div class="mn-ph"><img src="%s" alt="%s" loading="lazy" decoding="async" '
            'width="1280" height="800"><p class="mn-cap">%s</p></div></figure>'
            % (uri, alt, legende))


def tableau():
    regions = []
    for _, _, reg, _, _ in M.MIN:
        if reg not in regions:
            regions.append(reg)
    boutons = "".join('<button type="button" class="mn-f" data-reg="%s">%s</button>' % (r, r)
                      for r in regions)
    lignes = ""
    for nom, commune, reg, vol, site in sorted(M.MIN, key=lambda x: (-(x[3] or 0), x[0])):
        lien = ('<a href="%s" target="_blank" rel="noopener nofollow">site officiel</a>' % site
                if site else '<span class="mn-mut">—</span>')
        lignes += ('<tr data-reg="%s"><th scope="row">%s</th><td>%s</td><td>%s</td>'
                   '<td class="mn-n" data-v="%d">%s</td><td>%s</td></tr>'
                   % (reg, nom, commune, reg, vol or 0,
                      ("%s /&nbsp;mois" % format(vol, ",d").replace(",", " ")) if vol
                      else '<span class="mn-mut">non mesuré</span>', lien))
    return ('<figure class="mn" id="mn-liste">'
            + _tete("Les 17 marchés", "Trouvez le vôtre, et sa commune réelle",
                    "Triez, filtrez par région")
            + '<div class="mn-bar"><button type="button" class="mn-f on" data-reg="">'
              'Toutes les régions</button>' + boutons + '</div>'
            '<div class="mn-tw"><table class="mn-tab">'
            '<caption>Dix-sept marchés en activité au 11 septembre 2026. '
            'Recherches mensuelles : Google Ads, France, moyenne 12 mois arrêtée en '
            'juillet 2026.</caption><thead><tr>'
            '<th scope="col"><button type="button" class="mn-s2" data-k="0">Marché</button></th>'
            '<th scope="col">Commune</th><th scope="col">Région</th>'
            '<th scope="col"><button type="button" class="mn-s2 on" data-k="3">'
            'Recherches par mois</button></th><th scope="col">Site</th>'
            '</tr></thead><tbody>' + lignes + '</tbody></table></div>'
            '<p class="mn-cnt" id="mn-cnt">17 marchés affichés.</p></figure>')


def contraintes():
    c = "".join('<div class="mn-c"><b>%s</b><span>%s</span><em>%s</em></div>' % t
                for t in C.CONTRAINTES)
    n = "".join('<div class="mn-node"><b>%s</b><span>%s</span></div>' % t for t in C.FLUX)
    return ('<figure class="mn" id="mn-flux">'
            + _tete("Du carreau à la facture", "Les deux étapes où la marge se perd")
            + '<div class="mn-tri">' + c + '</div>'
            + '<div class="mn-flow">' + n + '</div>'
            '<p class="mn-lg"><i></i>Les deux étapes où la marge se perd</p></figure>')


def densites():
    """Barres de densite : le tonnage rapporte a la surface, marche par marche.

    C'est le chiffre que personne ne publie — il se calcule, il ne se recopie pas.
    """
    d = sorted(M2.avec_donnees(), key=lambda m: -(m[5] / m[4]))
    maxi = d[0][5] / d[0][4]
    lignes = ""
    for m in d:
        v = m[5] / m[4]
        lignes += ('<div class="mn-dr"><span class="mn-dn">%s</span>'
                   '<span class="mn-dt"><i style="width:%.1f%%"></i></span>'
                   '<span class="mn-dv">%s</span></div>'
                   % (m[1], v / maxi * 100, format(round(v), ",d").replace(",", " ")))
    return ('<figure class="mn" id="mn-dens">'
            + _tete("Tonnes par hectare", "La densité va du simple au sept fois plus",
                    "Calculé sur les 15 marchés qui publient les deux chiffres")
            + '<div class="mn-dens">' + lignes
            + '<p class="mn-cap">Tonnage annuel rapporté à la superficie. '
              'Source des deux données : fédération des marchés de gros de France, '
              'relevé le 11 septembre 2026.</p></div></figure>')


def chronologie():
    e = "".join('<div class="mn-step"><span class="mn-j">%s</span>'
                '<div class="mn-d"><b>%s</b><span>%s</span></div></div>' % t for t in C.DLC)
    return ('<figure class="mn" id="mn-dlc">'
            + _tete("Chronologie", "La vie d'un lot à DLC courte, en trois jours")
            + '<div class="mn-tl">' + e + '</div></figure>')


def ecran():
    UI_ = UI.ecran_dlc()
    return ('<figure class="mn" id="mn-ecran">'
            + _tete("Dans le logiciel", "Ce que vous voyez le matin, avant de charger")
            + '<div class="hhf">' + UI_ + '</div></figure>')


JS = """<script>
/* Tri et filtre du tableau des MIN. Le tableau est deja complet et trie dans le
   document : sans ce script il reste lisible et exact. */
(function () {
  var tab = document.querySelector('.mn-tab');
  if (!tab) { return; }
  var corps = tab.tBodies[0];
  var cnt = document.getElementById('mn-cnt');
  var lignes = Array.prototype.slice.call(corps.rows);
  var sens = {};

  function compter() {
    var n = lignes.filter(function (l) { return !l.hidden; }).length;
    if (cnt) { cnt.textContent = n + (n > 1 ? ' marchés affichés.' : ' marché affiché.'); }
  }

  Array.prototype.forEach.call(document.querySelectorAll('.mn-f'), function (b) {
    b.addEventListener('click', function () {
      var reg = b.dataset.reg;
      Array.prototype.forEach.call(document.querySelectorAll('.mn-f'), function (o) {
        o.classList.toggle('on', o === b);
      });
      lignes.forEach(function (l) { l.hidden = !!reg && l.dataset.reg !== reg; });
      compter();
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('.mn-s2'), function (b) {
    b.addEventListener('click', function () {
      var k = +b.dataset.k;
      sens[k] = (k in sens) ? !sens[k] : false;
      Array.prototype.forEach.call(document.querySelectorAll('.mn-s2'), function (o) {
        o.classList.toggle('on', o === b);
      });
      lignes.slice().sort(function (a, c) {
        var d;
        if (k === 3) { d = (+c.cells[3].dataset.v) - (+a.cells[3].dataset.v); }
        else { d = String(a.cells[0].textContent).localeCompare(c.cells[0].textContent, 'fr'); }
        return sens[k] ? -d : d;
      }).forEach(function (l) { corps.appendChild(l); });
    });
  });
})();
</script>"""
