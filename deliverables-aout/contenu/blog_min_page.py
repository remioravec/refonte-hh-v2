#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rendu de /blog/min/ sur le gabarit blog valide du site.

Le gabarit de reference est celui du billet « cout de revient » (post 7766),
celui que le client a valide comme LE gabarit du blog :
  article-hero → hha-toc → hha-tool → hha-art → faq-section.

Ce script prend ce billet comme coquille — en-tete, CSS, pied de page,
sommaire flottant, tiroir de FAQ — et n'en remplace que le contenu. La page
produite est donc, au pixel pres, ce que le site rendrait.

MAQUETTE. Le post 5274 n'est pas ecrit : le rendu est publie en artefact pour
validation.

Usage :  python3 blog_min_page.py
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import blog_min_contenu as C     # noqa: E402
from maquette_agro import convertir, POLICE, REPOS, SVG_FA, nettoyer, controler  # noqa: E402

GABARIT = 7766
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "blog-min.html")

PLAN = [
    ("definition", "Qu'est-ce qu'un marché d'intérêt national ?"),
    ("liste", "Les 17 MIN de France, marché par marché"),
    ("acheter", "Qui peut acheter dans un MIN, et comment"),
    ("prix", "Ce qu'on y achète, et comment le prix se fixe"),
    ("declasses", "Les cinq MIN déclassés depuis 1978"),
    ("gerer", "Gérer une activité de gros sur un marché"),
    ("faq", "Les questions qu'on nous pose"),
]


# ------------------------------------------------------------------- module
def module():
    """Tableau triable et filtrable des 17 MIN.

    Regle du module : il fonctionne SANS JavaScript. Les dix-sept lignes sont
    dans le document, deja triees par volume decroissant. Le JS n'ajoute que
    le tri au clic et le filtre par region — il n'injecte aucun contenu.
    """
    regions = []
    for _, _, reg, _, _ in C.MIN:
        if reg not in regions:
            regions.append(reg)
    boutons = "".join(
        '<button type="button" class="minf" data-reg="%s">%s</button>' % (r, r)
        for r in regions)

    lignes = ""
    for nom, commune, reg, vol, site in sorted(
            C.MIN, key=lambda x: (-(x[3] or 0), x[0])):
        lien = ('<a href="%s" target="_blank" rel="noopener nofollow">site officiel</a>' % site
                if site else '<span class="minv">—</span>')
        lignes += ('<tr data-reg="%s"><th scope="row">%s</th><td>%s</td><td>%s</td>'
                   '<td class="minn" data-v="%d">%s</td><td>%s</td></tr>'
                   % (reg, nom, commune, reg, vol or 0,
                      ("%s /&nbsp;mois" % format(vol, ",d").replace(",", " ")) if vol
                      else '<span class="minv">non mesuré</span>', lien))

    return ('<section class="hha-tool" id="liste-min">'
            '<div class="hha-tool-h"><span class="hha-tool-badge">Tableau interactif</span>'
            '<h3>Les 17 marchés d\'intérêt national</h3>'
            '<p>Triez par volume ou par nom, filtrez par région.</p></div>'
            '<div class="hha-tool-b">'
            '<div class="minbar"><button type="button" class="minf on" data-reg="">'
            'Toutes les régions</button>' + boutons + '</div>'
            '<div class="mintw"><table class="mintab">'
            '<caption class="minv">Dix-sept marchés en activité au 11 septembre 2026. '
            'Volumes : Google Ads, France, moyenne 12 mois arrêtée en juillet 2026.</caption>'
            '<thead><tr>'
            '<th scope="col"><button type="button" class="mins" data-k="0">Marché</button></th>'
            '<th scope="col">Commune</th>'
            '<th scope="col">Région</th>'
            '<th scope="col"><button type="button" class="mins on" data-k="3">'
            'Recherches par mois</button></th>'
            '<th scope="col">Site</th>'
            '</tr></thead><tbody>' + lignes + '</tbody></table></div>'
            '<p class="minv" id="mincount">17 marchés affichés.</p>'
            '</div></section>')


CSS = """<style id="hha-min">
#hh-page .minbar{display:flex;flex-wrap:wrap;gap:.45rem;margin:0 0 1rem !important}
#hh-page .minf{font:inherit;font-size:.82rem;font-weight:600;padding:.42rem .85rem;
 border:1px solid #d7dde3;background:#fff;color:#475569;border-radius:999px;cursor:pointer}
#hh-page .minf:hover{border-color:#00B1F5;color:#0f172a}
#hh-page .minf.on{background:#00B1F5;border-color:#00B1F5;color:#fff}
#hh-page .minf:focus-visible{outline:2px solid #0f172a;outline-offset:2px}
#hh-page .mintw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid #e2e8f0;
 border-radius:14px;background:#fff}
#hh-page .mintab{width:100%;border-collapse:collapse;font-size:.88rem;margin:0 !important}
#hh-page .mintab caption{caption-side:bottom;text-align:left;padding:.7rem .9rem;
 font-size:.76rem;line-height:1.5;border-top:1px solid #eef2f6}
#hh-page .mintab th,#hh-page .mintab td{padding:.6rem .9rem;text-align:left;
 border-bottom:1px solid #eef2f6;vertical-align:middle}
#hh-page .mintab thead th{background:#f8fafc;font-weight:600;color:#0f172a;white-space:nowrap;
 position:sticky;top:0}
#hh-page .mintab tbody th{font-weight:600;color:#0f172a}
#hh-page .mintab tbody tr:last-child th,#hh-page .mintab tbody tr:last-child td{border-bottom:0}
#hh-page .mintab tbody tr:nth-child(even) th,#hh-page .mintab tbody tr:nth-child(even) td{background:#fbfcfd}
#hh-page .minn{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
#hh-page .mins{font:inherit;font-weight:600;color:#0f172a;background:none;border:0;padding:0;
 cursor:pointer;display:inline-flex;align-items:center;gap:.3rem}
#hh-page .mins::after{content:"↕";font-size:.78em;color:#94a3b8}
#hh-page .mins.on::after{content:"↓";color:#00B1F5}
#hh-page .mins:focus-visible{outline:2px solid #0f172a;outline-offset:2px}
#hh-page .minv{color:#64748b}
#hh-page #mincount{margin:.8rem 0 0 !important;font-size:.82rem}
#hh-page .hha-art .minq{border:1px solid #e2e8f0;border-radius:14px;margin:0 0 .7rem !important;
 background:#fff;overflow:hidden}
#hh-page .hha-art .minq summary{cursor:pointer;padding:1rem 1.15rem;font-weight:600;
 color:#0f172a;list-style:none;display:flex;justify-content:space-between;gap:1rem;align-items:center}
#hh-page .hha-art .minq summary::-webkit-details-marker{display:none}
#hh-page .hha-art .minq summary::after{content:"+";color:#00B1F5;font-size:1.25rem;font-weight:400;flex:0 0 auto}
#hh-page .hha-art .minq[open] summary::after{content:"−"}
#hh-page .hha-art .minq summary:focus-visible{outline:2px solid #0f172a;outline-offset:-2px}
#hh-page .hha-art .minq div{padding:0 1.15rem 1.1rem}
#hh-page .hha-art .minq div p{margin:0 !important}
@media(max-width:640px){#hh-page .mintab{font-size:.8rem}
 #hh-page .mintab th,#hh-page .mintab td{padding:.5rem .6rem}}
</style>"""

JS = """<script>
/* Tri et filtre du tableau des MIN. Le tableau est deja complet et trie dans
   le document : sans ce script, il reste lisible et exact. */
(function () {
  var tab = document.querySelector('.mintab');
  if (!tab) { return; }
  var corps = tab.tBodies[0];
  var cpt = document.getElementById('mincount');
  var lignes = Array.prototype.slice.call(corps.rows);
  var sens = {};

  function compter() {
    var n = lignes.filter(function (l) { return !l.hidden; }).length;
    if (cpt) { cpt.textContent = n + (n > 1 ? ' marchés affichés.' : ' marché affiché.'); }
  }

  Array.prototype.forEach.call(document.querySelectorAll('.minf'), function (b) {
    b.addEventListener('click', function () {
      var reg = b.dataset.reg;
      Array.prototype.forEach.call(document.querySelectorAll('.minf'), function (o) {
        o.classList.toggle('on', o === b);
      });
      lignes.forEach(function (l) { l.hidden = !!reg && l.dataset.reg !== reg; });
      compter();
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('.mins'), function (b) {
    b.addEventListener('click', function () {
      var k = +b.dataset.k;
      /* premier clic : A→Z sur le nom, du plus grand au plus petit sur le
         volume. C'est l'ordre que le lecteur attend dans les deux cas. */
      sens[k] = (k in sens) ? !sens[k] : false;
      Array.prototype.forEach.call(document.querySelectorAll('.mins'), function (o) {
        o.classList.toggle('on', o === b);
      });
      lignes.slice().sort(function (a, c) {
        var x, y;
        if (k === 3) { x = +a.cells[3].dataset.v; y = +c.cells[3].dataset.v; }
        else { x = a.cells[0].textContent; y = c.cells[0].textContent; }
        var d = (k === 3) ? y - x : String(x).localeCompare(String(y), 'fr');
        return sens[k] ? -d : d;
      }).forEach(function (l) { corps.appendChild(l); });
    });
  });
})();
</script>"""


def article():
    p = []
    a = p.append

    a('<p class="hha-lead">Un <strong>marché d\'intérêt national</strong> est un marché de gros '
      'auquel les pouvoirs publics ont accordé un statut particulier. La France en compte '
      '<strong>dix-sept en activité</strong>. Leur régime est fixé par les '
      '<a href="https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000005634379/'
      'LEGISCTA000006146141/" target="_blank" rel="noopener">articles L761-1 à L761-11 du Code '
      'de commerce</a>, qui en font des services publics de gestion de marché, réservés aux '
      'professionnels.</p>')

    a('<h2 id="definition">Qu\'est-ce qu\'un marché d\'intérêt national ?</h2>')
    a('<p>Le texte est explicite : les marchés d\'intérêt national sont « des services publics '
      'de gestion de marchés offrant à des grossistes et à des producteurs des services de '
      'gestion collective ». Concrètement, une enceinte close où l\'on trouve au même endroit '
      'des quais, des chambres froides, un contrôle sanitaire, la sécurité et le traitement des '
      'déchets — mutualisés entre des entreprises qui, seules, ne les financeraient pas.</p>')
    a('<p>Le premier réseau naît en 1953. Rungis, le plus connu, ouvre en 1969 et remplace les '
      'halles de Paris. Depuis, cinq marchés ont été déclassés et le réseau s\'est stabilisé à '
      'dix-sept. <span class="hha-src">Source : %s.</span></p>' % C.SOURCE_LOI)

    a('<h2 id="liste">Les 17 MIN de France, marché par marché</h2>')
    a('<p>Voici les dix-sept, avec leur commune réelle — qui n\'est pas toujours celle du nom : '
      'le MIN de Nantes est à Rezé, celui de Lyon à Corbas, et Rungis est à cheval sur Rungis '
      'et Chevilly-Larue. La dernière colonne donne le nombre de recherches mensuelles sur '
      '« min de <em>ville</em> » : c\'est une mesure de notoriété, pas d\'activité.</p>')

    a('<h2 id="acheter">Qui peut acheter dans un MIN, et comment</h2>')
    a('<p>L\'accès est réservé aux professionnels. Commerçants de détail, métiers de bouche, '
      'restaurateurs, traiteurs, collectivités et grossistes entrent sur présentation d\'une '
      'carte d\'acheteur, délivrée contre un justificatif d\'activité — un extrait Kbis, le plus '
      'souvent. Un particulier n\'y fait pas ses courses ; il peut en revanche visiter, quand le '
      'marché organise des visites.</p>')
    a('<p>Les horaires sont ceux du gros : l\'essentiel des transactions se fait entre deux et '
      'sept heures du matin, pour que la marchandise soit en rayon à l\'ouverture. C\'est ce '
      'décalage qui structure toute l\'organisation d\'un grossiste — la préparation de commande, '
      'le chargement, la tournée.</p>')

    a('<h2 id="prix">Ce qu\'on y achète, et comment le prix se fixe</h2>')
    a('<p>Fruits et légumes d\'abord, puis marée, viandes, produits laitiers, horticulture. Le '
      'prix n\'est pas affiché une fois pour toutes : il bouge dans la matinée, selon l\'arrivage '
      'et ce qu\'il reste. FranceAgriMer publie chaque jour les '
      '<a href="https://rnm.franceagrimer.fr/" target="_blank" rel="noopener">cours des '
      'grossistes</a> relevés sur les principaux marchés — c\'est la référence publique du '
      'secteur.</p>')
    a('<p>Pour un grossiste, cette volatilité a une conséquence directe : le tarif client doit '
      'suivre le <a href="/blog/logiciel-prix-du-jour-fruits-legumes/">cours du jour des fruits '
      'et légumes</a>, sans quoi la marge se fait manger entre l\'achat du matin et la facture '
      'du soir. C\'est le sujet central de la gestion en '
      '<a href="/agroalimentaire/maraicher/">fruits et légumes</a>.</p>')

    a('<h2 id="declasses">Les cinq MIN déclassés depuis 1978</h2>')
    a('<p>Le statut de MIN n\'est pas acquis : il se perd quand l\'activité ne le justifie plus. '
      'Cinq marchés l\'ont perdu.</p>')
    a('<ul>' + "".join('<li><strong>%s</strong> — déclassé en %d</li>' % (n, an)
                       for n, an in C.DECLASSES) + '</ul>')
    a('<p>Le plus récent, Lille, est sorti du réseau en 2019. Lyon, lui, n\'a pas disparu : '
      'Perrache a été déclassé en 2006, et l\'activité a été reprise à Corbas.</p>')

    a('<h2 id="gerer">Gérer une activité de gros sur un marché</h2>')
    a('<p>Travailler sur un carreau impose trois contraintes que les outils généralistes gèrent '
      'mal. Le poids : on achète au kilo et on facture au colis, et l\'écart entre le poids '
      'commandé et le poids réellement pesé se paie. La date : les DLC sont courtes, parfois '
      'trois jours, et la <a href="/negoce/tracabilite-lots/">traçabilité des lots</a> doit '
      'suivre le lot, pas le produit. Le lieu : la marchandise vit sur plusieurs emplacements, '
      'ce qui suppose une gestion des '
      '<a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a>.</p>')
    a('<p>C\'est exactement ce que couvre un <a href="/negoce/">ERP négoce alimentaire</a>, et '
      'ce qui le distingue d\'un logiciel de facturation.</p>')

    a('<h2 id="faq">Les questions qu\'on nous pose</h2>')
    for q, r in C.FAQ:
        a('<details class="minq"><summary>%s</summary><div><p>%s</p></div></details>' % (q, r))

    return "".join(p)


# ------------------------------------------------------------------- montage
def remplacer(c, deb_motif, fin_motif, neuf, quoi):
    i = c.find(deb_motif)
    if i < 0:
        raise SystemExit("ARRET — %s : debut introuvable" % quoi)
    j = c.find(fin_motif, i)
    if j < 0:
        raise SystemExit("ARRET — %s : fin introuvable" % quoi)
    return c[:i] + neuf + c[j + len(fin_motif):]


def main():
    c = w.get_raw("posts", GABARIT)["content"]["raw"]
    print("gabarit %d lu : %d octets" % (GABARIT, len(c)))

    # 1 — le sommaire, aux deux endroits ou il apparait
    toc = '<nav class="hha-toc">' + "".join(
        '<a href="#%s">%s</a>' % (i, t) for i, t in PLAN) + '</nav>'
    n = len(re.findall(r'<nav class="hha-toc">.*?</nav>', c, re.S))
    c = re.sub(r'<nav class="hha-toc">.*?</nav>', lambda _: toc, c, flags=re.S)
    print("sommaire remplace : %d occurrence(s)" % n)

    # 2 — le module
    c = remplacer(c, '<section class="hha-tool"', '</section>', CSS + module(), "module")
    print("module pose : tableau des 17 MIN")

    # 3 — le corps
    c = remplacer(c, '<article class="hha-art"',
                  '<section class="faq-section">',
                  '<article class="hha-art">' + article() + JS
                  + '<section class="faq-section">', "corps")
    print("corps remplace : %d octets" % len(article()))

    # 4 — l'en-tete
    c = re.sub(r'(<span style="color:rgba\(255,255,255,0\.5\)">)[^<]*(</span>)',
               lambda m: m.group(1) + C.H1 + m.group(2), c, count=1)
    c = re.sub(r'(<span class="article-cat">)[^<]*(</span>)',
               lambda m: m.group(1) + "Négoce alimentaire" + m.group(2), c, count=1)
    c = re.sub(r'(<span class="article-date">)[^<]*(</span>)',
               lambda m: m.group(1) + "11 septembre 2026" + m.group(2), c, count=1)
    c = re.sub(r'(<span>)\d+ min de lecture(</span>)',
               lambda m: m.group(1) + "7 min de lecture" + m.group(2), c, count=1)
    c = re.sub(r'<h1>.*?</h1>', lambda _: '<h1>' + C.H1 + '</h1>', c, count=1, flags=re.S)
    print("en-tete pose")

    # 5 — le script du calculateur de cout part avec le module qu'il pilotait.
    #     Il lit ses champs en variables globales (c_m.value), sans passer par
    #     getElementById : sans eux il levait une exception au chargement, ce
    #     qui coupait tout ce qui suivait dans le meme bloc.
    for m in list(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.S))[::-1]:
        if "c_m.value" in m.group(1) or "c_f.value" in m.group(1):
            c = c[:m.start()] + c[m.end():]
            print("script du calculateur retire")

    # 6 — la redirection /demo/ vers /contact/ etait une chaine 301
    c = c.replace('href="/demo/?from=', 'href="/contact/?from=')
    c = c.replace('blog-calcul-cout-de-revient-logiciel-final', 'blog-min')

    # 7 — traitement d'artefact
    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    urls |= set(re.findall(r"url\(&#039;(https?://[^&]+\.(?:png|jpe?g|webp|svg|gif))&#039;\)", c))
    ok = 0
    for u in sorted(urls):
        d = convertir(u)
        if d:
            c = c.replace(u, d)
            ok += 1
    for cls, svg in SVG_FA.items():
        c = c.replace('<i class="%s"></i>' % cls, svg)
    c = re.sub(r'<link[^>]+cdnjs\.cloudflare\.com[^>]*>', "", c)
    c = nettoyer(c)
    c += '<style id="hh-recette">html{overflow-x:clip}</style>'
    print("images integrees : %d" % ok)

    html = ("<title>%s</title>\n" % C.TITLE) + POLICE + "\n" + REPOS + "\n" + c
    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\necrit : %s (%d ko)" % (SORTIE, len(html) // 1024))

    pb = controler(html)
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
