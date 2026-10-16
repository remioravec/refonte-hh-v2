#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Article « MIN de Rungis », monte sur le gabarit blog valide du site.

Le gabarit de reference reste le billet « cout de revient » (post 7766) :
article-hero → sommaire → hha-art → FAQ. Ce script en prend la coquille et
n'en remplace que le contenu.

Le module hha-tool du gabarit est retire : les cinq infographies vivent ENTRE
les Hn, ce qui est la demande. Le script du calculateur de cout part avec lui.

MAQUETTE. Rien n'est ecrit sur WordPress.

Usage :  python3 blog_rungis_page.py
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                     # noqa: E402
import blog_rungis_contenu as C           # noqa: E402
import blog_rungis_infographies as G      # noqa: E402
from maquette_agro import convertir, POLICE, REPOS, SVG_FA, nettoyer, controler  # noqa: E402

GABARIT = 7766
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "blog-rungis.html")

PLAN = [
    ("cest-quoi", "Le MIN de Rungis, en une phrase"),
    ("horaires", "Les horaires, secteur par secteur"),
    ("acces", "Qui peut acheter, et comment entrer"),
    ("prix", "Comment le prix se fixe sur le carreau"),
    ("marge", "Où la marge se perd entre le carreau et la facture"),
    ("gestion", "Ce qu'un ERP de négoce change sur un carreau"),
    ("faq", "Les questions qu'on nous pose"),
]


def article():
    p = []
    a = p.append

    # P1 — la reponse, requete exacte dans les 60 premiers mots, fait date et source
    a('<p class="hha-lead">Le <strong>MIN de Rungis</strong> est le marché d\'intérêt national '
      'qui approvisionne l\'Île-de-France en produits frais. Il est réservé aux professionnels, '
      'et chaque secteur y ouvre à une heure différente : <strong>2 h pour la marée, '
      '5 h 30 pour les fruits et légumes</strong>. Voici comment il fonctionne quand on y '
      'achète pour travailler.</p>')

    a('<h2 id="cest-quoi">Le MIN de Rungis, en une phrase</h2>')
    a(G.chiffres())
    a('<p>Ouvert en 1969 en remplacement des halles de Paris, le marché s\'étend sur '
      '<strong>234 hectares</strong> à cheval sur les communes de Rungis et de '
      'Chevilly-Larue. Il accueille <strong>1 226 entreprises</strong> et '
      '<strong>12 000 salariés</strong>, pour un chiffre d\'affaires de '
      '<strong>12,02 milliards d\'euros en 2024</strong>. '
      '<span class="hha-src">Source : %s.</span></p>' % C.SOURCE)
    a('<p>Son statut n\'est pas commercial mais public : un '
      '<a href="/blog/min/">marché d\'intérêt national</a> est un service public de gestion de '
      'marché au sens des articles L761-1 à L761-11 du Code de commerce. Ce sont ces textes '
      'qui justifient l\'enceinte close, le contrôle à l\'entrée et la réservation aux '
      'professionnels.</p>')

    a('<h2 id="horaires">Les horaires, secteur par secteur</h2>')
    a('<p>C\'est le point que personne ne publie lisiblement, et c\'est celui qui structure '
      'la journée d\'un acheteur. Il n\'y a pas un horaire de Rungis, il y en a onze.</p>')
    a(G.journee())
    a('<p>La conséquence est concrète : un restaurateur qui prend du poisson et des légumes '
      'entre à 2 h et ressort après 6 h. Un charcutier qui ne fait que la boucherie arrive à '
      '3 h. Et le samedi, la boucherie est fermée quand la marée et la volaille tournent. '
      'C\'est ce décalage qui fait qu\'une commande partie du marché à 7 h doit être préparée, '
      'chargée et livrée avant l\'ouverture des clients.</p>')

    a('<h2 id="acces">Qui peut acheter, et comment entrer</h2>')
    a('<p>L\'accès est réservé aux professionnels : commerçants de détail, métiers de bouche, '
      'restaurateurs, traiteurs, collectivités et grossistes. Un particulier n\'y fait pas ses '
      'courses — il peut en revanche visiter, quand le marché organise des visites.</p>')
    a(G.carte())

    a('<h2 id="prix">Comment le prix se fixe sur le carreau</h2>')
    a('<p>Le prix n\'est pas affiché une fois pour toutes le matin : il bouge avec l\'arrivage '
      'et avec ce qu\'il reste à écouler. FranceAgriMer publie chaque jour les '
      '<a href="https://rnm.franceagrimer.fr/prix?M0123:MARCHE" target="_blank" '
      'rel="noopener">cours des grossistes relevés sur le MIN de Rungis</a> : c\'est la '
      'référence publique du secteur, et le premier réflexe avant de négocier.</p>')
    a('<p>Pour celui qui revend, cette volatilité impose de répercuter le '
      '<a href="/blog/logiciel-prix-du-jour-fruits-legumes/">cours du jour des fruits et '
      'légumes</a> sur son propre tarif. Sans quoi la hausse du matin est encaissée par le '
      'client et payée par la marge.</p>')

    a('<h2 id="marge">Où la marge se perd entre le carreau et la facture</h2>')
    a('<p>Entre le lot acheté sur le carreau et la facture envoyée au client, la marchandise '
      'traverse cinq étapes. Deux d\'entre elles font disparaître de la marge sans que '
      'personne ne s\'en aperçoive.</p>')
    a(G.flux())
    a('<p>Le premier trou est le <strong>poids</strong>. On achète un colis annoncé à 10 kg, '
      'il en pèse 9,7. Si la facture part sur le poids commandé, l\'écart est offert. Le '
      'second est la <strong>date</strong> : les DLC sont courtes, parfois trois jours, et un '
      'lot prélevé au mauvais ordre finit en perte.</p>')
    a(G.ecart())
    a('<p>Ce calcul n\'est pas une projection commerciale : c\'est une multiplication. '
      'Remplacez les trois valeurs par les vôtres, le résultat est le vôtre.</p>')

    a('<h2 id="gestion">Ce qu\'un ERP de négoce change sur un carreau</h2>')
    a('<p>Un logiciel de facturation classique facture ce qui a été commandé. Sur un marché de '
      'gros, ça ne suffit pas : il faut facturer ce qui a été <em>pesé</em>. C\'est la '
      'différence entre un outil généraliste et un '
      '<a href="/negoce/">ERP négoce alimentaire</a>, conçu pour le poids variable.</p>')
    a('<p>Trois mécanismes changent la donne au quotidien. La pesée entre dans la ligne de '
      'commande, et la facture suit le poids réel. La '
      '<a href="/negoce/tracabilite-lots/">traçabilité des lots</a> suit le lot et sa DLC, pas '
      'seulement la référence produit, ce qui permet le prélèvement au plus près de la date. '
      'Et la gestion des <a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a> '
      'réconcilie ce qui est sur le carreau, en chambre froide et déjà chargé dans le camion.</p>')
    a('<p>C\'est le quotidien des grossistes et distributeurs alimentaires que nous '
      'accompagnons, à Rungis comme sur les autres marchés d\'intérêt national.</p>')

    a('<h2 id="faq">Les questions qu\'on nous pose</h2>')
    for q, r in C.FAQ:
        a('<details class="minq"><summary>%s</summary><div><p>%s</p></div></details>' % (q, r))

    return "".join(p)


FAQ_CSS = """<style id="hh-rungis-faq">
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

    # le module du gabarit disparait : les infographies vivent entre les Hn
    i = c.find('<section class="hha-tool"')
    j = c.find('</section>', i)
    if i < 0 or j < 0:
        raise SystemExit("ARRET — module du gabarit introuvable")
    c = c[:i] + c[j + len('</section>'):]
    print("module du gabarit retire")

    i = c.find('<article class="hha-art"')
    j = c.find('<section class="faq-section">', i)
    if i < 0 or j < 0:
        raise SystemExit("ARRET — corps de l'article introuvable")
    corps = article()
    c = (c[:i] + '<article class="hha-art">' + G.CSS + FAQ_CSS + corps + G.JS + c[j:])
    print("corps pose : %d octets, %d infographies, %d Hn"
          % (len(corps), corps.count('<figure class="rg"'), corps.count('<h2')))

    # le script du calculateur du gabarit lit ses champs en variables globales
    for m in list(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.S))[::-1]:
        if "c_m.value" in m.group(1) or "c_f.value" in m.group(1):
            c = c[:m.start()] + c[m.end():]
            print("script du calculateur du gabarit retire")

    c = re.sub(r'(<span style="color:rgba\(255,255,255,0\.5\)">)[^<]*(</span>)',
               lambda m: m.group(1) + C.H1 + m.group(2), c, count=1)
    c = re.sub(r'(<span class="article-cat">)[^<]*(</span>)',
               lambda m: m.group(1) + "Négoce alimentaire" + m.group(2), c, count=1)
    c = re.sub(r'(<span class="article-date">)[^<]*(</span>)',
               lambda m: m.group(1) + "11 septembre 2026" + m.group(2), c, count=1)
    c = re.sub(r'(<span>)\d+ min de lecture(</span>)',
               lambda m: m.group(1) + "8 min de lecture" + m.group(2), c, count=1)
    c = re.sub(r'<h1>.*?</h1>', lambda _: '<h1>' + C.H1 + '</h1>', c, count=1, flags=re.S)
    c = c.replace('href="/demo/?from=', 'href="/contact/?from=')
    c = c.replace('blog-calcul-cout-de-revient-logiciel-final', 'blog-min-rungis')
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
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
