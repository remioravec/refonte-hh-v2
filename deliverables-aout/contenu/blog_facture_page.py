#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4.2 — Article « mentions obligatoires d'une facture », sur le gabarit blog.

Gabarit : le billet « cout de revient » (post 7766), celui que le client a
valide comme LE gabarit du blog. Le module hha-tool du gabarit disparait :
les six visuels vivent entre les Hn.

MAQUETTE. Rien n'est ecrit sur WordPress.

Usage :  python3 blog_facture_page.py
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                   # noqa: E402
import blog_facture_contenu as C        # noqa: E402
import blog_facture_visuels as G        # noqa: E402
import agro_ui as UI                    # noqa: E402
from maquette_agro import convertir, POLICE, REPOS, SVG_FA, nettoyer, controler  # noqa: E402

GABARIT = 7766
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "blog-facture.html")

PLAN = [
    ("liste", "Les 23 mentions obligatoires, une par une"),
    ("nouvelles", "Les quatre nouvelles mentions de la facture électronique"),
    ("calendrier", "Ce qui s'applique déjà, et ce qui arrive"),
    ("formats", "Factur-X, UBL, CII : lequel choisir"),
    ("sanctions", "Ce que coûte une mention manquante"),
    ("logiciel", "Ce que ça change dans votre logiciel"),
    ("faq", "Les questions qu'on nous pose"),
]

LIENS = ["/fonctionnalites/facturation/", "/blog/factur-x-e-facturation-logiciel/",
         "/fonctionnalites/facturation-automatique-bon-livraison/", "/blog/bon-de-livraison/",
         "/blog/bon-de-commande/", "/conformite-loi-anti-fraude-tva/",
         "/negoce/tarifs-reporting-edi/"]


def article():
    p = []
    a = p.append

    a('<p class="hha-lead">Une facture entre professionnels doit porter '
      '<strong>dix-neuf mentions obligatoires</strong>, auxquelles la facturation '
      'électronique en ajoute <strong>quatre</strong>. L\'oubli se paie '
      '<strong>15 € par mention manquante</strong>. Si votre '
      '<a href="/fonctionnalites/facturation/">logiciel de facturation</a> ne les porte pas '
      'toutes, la liste ci-dessous vous dit lesquelles il vous manque.</p>')

    a('<h2 id="liste">Les 23 mentions obligatoires, une par une</h2>')
    a('<p>La liste vient du Code de commerce et du Code général des impôts. Elle vaut pour '
      'une facture entre professionnels ; une facture à un particulier obéit à des règles '
      'plus légères. Cochez ce que votre facture porte déjà.</p>')
    a(G.checklist())
    a('<p>Deux pièges reviennent souvent. Le <strong>numéro unique</strong> doit suivre une '
      'séquence chronologique continue : un trou dans la numérotation est la première chose '
      'qu\'un contrôle regarde. Et les <strong>conditions d\'escompte</strong> doivent '
      'figurer même quand il n\'y en a pas — on écrit alors « escompte pour paiement '
      'anticipé : néant », l\'absence de mention étant elle-même une omission.</p>')

    a('<h2 id="nouvelles">Les quatre nouvelles mentions de la facture électronique</h2>')
    a('<p>La réforme de la facturation électronique ne change pas seulement le support : elle '
      'ajoute quatre mentions au contenu de la facture.</p>')
    a(G.versus())
    a('<p>Deux d\'entre elles concernent directement le négoce. Le <strong>SIREN du '
      'client</strong> devient la clé d\'acheminement : sans lui, la facture ne trouve pas '
      'son destinataire sur la plateforme. Et l\'<strong>adresse de livraison</strong> doit '
      'être portée dès qu\'elle diffère de l\'adresse de facturation — pour un grossiste qui '
      'livre plusieurs points de vente sous une seule enseigne, c\'est la règle, pas '
      'l\'exception. C\'est le lien direct entre la facture et le '
      '<a href="/blog/bon-de-livraison/">bon de livraison</a>.</p>')

    a('<h2 id="calendrier">Ce qui s\'applique déjà, et ce qui arrive</h2>')
    a('<p>Le calendrier est souvent présenté comme une échéance future. Il ne l\'est plus '
      'entièrement : une partie est en vigueur depuis le 1ᵉʳ septembre 2026.</p>')
    a(G.calendrier())
    a('<p>Autrement dit : <strong>vous devez déjà être capable de recevoir une facture '
      'électronique</strong>, quelle que soit la taille de votre entreprise. C\'est la partie '
      'que l\'on oublie, parce que l\'attention se porte sur l\'émission — dont l\'échéance, '
      'pour une PME, est au 1ᵉʳ septembre 2027. Le détail du format et de la mise en œuvre '
      'est traité dans notre guide '
      '<a href="/blog/factur-x-e-facturation-logiciel/">Factur-X</a>.</p>')

    a('<h2 id="formats">Factur-X, UBL, CII : lequel choisir</h2>')
    a('<p>Trois formats sont reconnus. Ils ne se valent pas du point de vue de celui qui lit '
      'la facture.</p>')
    a(G.formats())
    a('<p>Factur-X est le seul des trois qu\'un humain peut lire sans outil : c\'est un PDF '
      'normal, avec le XML embarqué dedans. Les deux autres sont des fichiers XML purs, '
      'destinés aux échanges automatisés — le terrain de l\'<a href="/negoce/tarifs-reporting-edi/">'
      'EDI</a>. Pour une PME qui envoie des factures à des clients de tailles très '
      'différentes, Factur-X évite d\'avoir à expliquer au client comment ouvrir le fichier.</p>')

    a('<h2 id="sanctions">Ce que coûte une mention manquante</h2>')
    a('<p>L\'amende ne se compte pas par facture mais <strong>par mention</strong>. Sur un '
      'lot de factures qui partagent le même défaut de paramétrage, l\'addition monte vite.</p>')
    a(G.sanctions())
    a('<p>Le plafond de 25 % du montant facturé protège sur une facture isolée, pas sur un '
      'exercice entier. Et l\'obligation de facturer, elle, relève d\'un autre registre : '
      'jusqu\'à 375 000 € pour une personne morale, doublés en cas de récidive dans les deux '
      'ans. C\'est le même sujet que la <a href="/conformite-loi-anti-fraude-tva/">conformité '
      'à la loi anti-fraude TVA</a> : ce qui est contrôlé, c\'est le paramétrage du logiciel, '
      'pas la bonne foi de celui qui édite.</p>')

    a('<h2 id="logiciel">Ce que ça change dans votre logiciel</h2>')
    a('<p>Toutes ces mentions ont un point commun : aucune ne se saisit à la main facture par '
      'facture. Elles se paramètrent une fois et se reportent automatiquement — le SIREN du '
      'client dans sa fiche, l\'adresse de livraison dans le point de livraison, la catégorie '
      'de l\'opération dans la ligne de commande.</p>')
    a('<figure class="fa2" id="fa-ecran">'
      '<figcaption class="fa2-h"><p class="fa2-k">Dans le logiciel</p>'
      '<p class="fa2-t">La facture se construit depuis la commande, pas l\'inverse</p>'
      '</figcaption><div class="hhf">' + UI.ecran_cout() + '</div></figure>')
    a('<p>C\'est le rôle de la '
      '<a href="/fonctionnalites/facturation-automatique-bon-livraison/">facturation '
      'automatique depuis le bon de livraison</a> : la facture reprend le '
      '<a href="/blog/bon-de-commande/">bon de commande</a>, les quantités réellement '
      'livrées et les mentions rattachées au client. Ce qui n\'est pas ressaisi ne peut pas '
      'être oublié.</p>')

    a('<h2 id="faq">Les questions qu\'on nous pose</h2>')
    # L'accordeon EST le visuel de ce H2 : il est donc enveloppe comme les autres.
    a('<figure class="fa2" id="fa-faq">'
      + "".join('<details class="minq"><summary>%s</summary><div><p>%s</p></div></details>'
                % (q, r) for q, r in C.FAQ)
      + '</figure>')

    return "".join(p)


FAQ_CSS = """<style id="hh-fac-faq">
#hh-page .hha-art .minq,.hha-art .minq{border:1px solid #e2e8f0;border-radius:14px;
 margin:0 0 .7rem !important;background:#fff;overflow:hidden}
#hh-page .hha-art .minq summary,.hha-art .minq summary{cursor:pointer;padding:1rem 1.15rem;
 font-weight:600;color:#0f172a;list-style:none;display:flex;justify-content:space-between;
 gap:1rem;align-items:center}
#hh-page .hha-art .minq summary::-webkit-details-marker{display:none}
#hh-page .hha-art .minq summary::after,.hha-art .minq summary::after{content:"+";color:#00B1F5;
 font-size:1.25rem;font-weight:400;flex:0 0 auto}
#hh-page .hha-art .minq[open] summary::after,.hha-art .minq[open] summary::after{content:"−"}
#hh-page .hha-art .minq summary:focus-visible{outline:2px solid #0f172a;outline-offset:-2px}
#hh-page .hha-art .minq div,.hha-art .minq div{padding:0 1.15rem 1.1rem}
#hh-page .hha-art .minq div p,.hha-art .minq div p{margin:0 !important}
</style>"""


def main():
    c = w.get_raw("posts", GABARIT)["content"]["raw"]
    print("gabarit %d lu : %d octets" % (GABARIT, len(c)))

    toc = '<nav class="hha-toc">' + "".join(
        '<a href="#%s">%s</a>' % (i, t) for i, t in PLAN) + '</nav>'
    n = len(re.findall(r'<nav class="hha-toc">.*?</nav>', c, re.S))
    c = re.sub(r'<nav class="hha-toc">.*?</nav>', lambda _: toc, c, flags=re.S)
    print("sommaire remplace : %d occurrence(s)" % n)

    i = c.find('<section class="hha-tool"')
    j = c.find('</section>', i)
    if i < 0 or j < 0:
        raise SystemExit("ARRET — module du gabarit introuvable")
    c = c[:i] + c[j + len('</section>'):]
    print("module du gabarit retire")

    i = c.find('<article class="hha-art"')
    j = c.find('<section class="faq-section">', i)
    if i < 0 or j < 0:
        raise SystemExit("ARRET — corps introuvable")
    corps = article()
    c = c[:i] + '<article class="hha-art">' + G.CSS + FAQ_CSS + UI.CSS + corps + G.JS + c[j:]
    print("corps pose : %d octets, %d H2, %d visuels"
          % (len(corps), corps.count("<h2"), corps.count('<figure class="fa2"')))

    for m in list(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.S))[::-1]:
        if "c_m.value" in m.group(1) or "c_f.value" in m.group(1):
            c = c[:m.start()] + c[m.end():]
            print("script du calculateur du gabarit retire")

    c = re.sub(r'(<span style="color:rgba\(255,255,255,0\.5\)">)[^<]*(</span>)',
               lambda m: m.group(1) + C.H1 + m.group(2), c, count=1)
    c = re.sub(r'(<span class="article-cat">)[^<]*(</span>)',
               lambda m: m.group(1) + "Facturation" + m.group(2), c, count=1)
    c = re.sub(r'(<span class="article-date">)[^<]*(</span>)',
               lambda m: m.group(1) + "11 septembre 2026" + m.group(2), c, count=1)
    c = re.sub(r'(<span>)\d+ min de lecture(</span>)',
               lambda m: m.group(1) + "9 min de lecture" + m.group(2), c, count=1)
    c = re.sub(r'<h1>.*?</h1>', lambda _: '<h1>' + C.H1 + '</h1>', c, count=1, flags=re.S)
    c = c.replace('href="/demo/?from=', 'href="/contact/?from=')
    c = c.replace('blog-calcul-cout-de-revient-logiciel-final', 'blog-mentions-obligatoires-facture')
    print("en-tete pose")

    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
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
    for u in LIENS:
        if ('href="%s"' % u) not in corps:
            pb.append("lien du plan absent du texte : %s" % u)
    if corps.count("<h2") != corps.count('<figure class="fa2"'):
        pb.append("un visuel par H2 non respecte : %d H2, %d visuels"
                  % (corps.count("<h2"), corps.count('<figure class="fa2"')))
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
