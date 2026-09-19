#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/negoce/marches-interet-national/rungis/ — la premiere fille du silo MIN.

4.1 BRIEF
=========
REQUETES VISEES — 3 200 recherches par mois sur le coeur du marche :
  min de rungis 1 600 · min rungis 1 600 · carte acheteur rungis 170 ·
  grossiste rungis 210 · min de rungis plan 70 · min rungis prix 50
Contexte, hors cible directe : marche de rungis 5 400, rungis marche 4 400.

ANTI-CANNIBALISATION — verdict MODERE, arbitre en trois etages :
  · /blog/min/ ................................ la definition d'un MIN, TOFU
  · /negoce/marches-interet-national/ .......... les dix-sept, la comparaison
  · cette page ................................. Rungis seul, pour qui y travaille
Chaque etage lie le precedent. Aucun ne reprend le title d'un autre.

SERP « min de rungis » RELEVEE LE 11/09/2026 — dix positions, ZERO editeur de
logiciel : site officiel, questions posees, cours FranceAgriMer, Wikipedia,
cinquante offres d'emploi Indeed, Facebook, MyRungis, YouTube, videos courtes,
fiche Google avec 656 avis. Recherches associees : recrutement, prix, plan,
histoire, restaurant.

VERIFIE LE 11/09/2026 SUR 3 428 URL DE SITEMAPS CONCURRENTS — personne n'a de
page par MIN. Les trois approximations les plus proches : trois pages « MIN
Carreau » generiques par filiere chez Groupe Bellon, un communique et une
entree de glossaire chez Akanea, un temoignage client situe a Rungis chez
Isatech. Le champ est libre.

ANGLE TRANCHE — la premiere place est hors de portee : le site officiel
l'occupe et la fiche Google prend le premier ecran. Ce qui est atteignable,
c'est la reponse que PERSONNE ne donne — les horaires reels secteur par
secteur, ce que Rungis pese face aux seize autres, et ce que le carreau impose
a la gestion de celui qui y travaille.

PROMESSE — Rungis pour celui qui y achete : quand chaque secteur ouvre, ce que
le marche pese, comment on y entre, et ce que ca change dans la gestion.

MODULE NAVBOOST — la frise horaire des onze secteurs, au-dessus du 2e ecran.
Aucune SERP ne la donne sous forme lisible.

SIGNAL GA4 DECLARE — interaction avec la frise et avec la fiche comparative.

MAQUETTE. Rien n'est ecrit sur WordPress.

Usage :  python3 page_rungis.py
"""

import base64
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                      # noqa: E402
import min_data as D                       # noqa: E402
import page_min_contenu as PC              # noqa: E402
import page_min_visuels as V               # noqa: E402
import blog_rungis_contenu as R            # noqa: E402
import blog_rungis_infographies as G       # noqa: E402
import agro_ui as UI                       # noqa: E402
from maquette_agro import convertir, POLICE, REPOS, SVG_FA, nettoyer, reparer, controler  # noqa: E402

GABARIT = 6077
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "page-rungis.html")

TITLE = "MIN de Rungis : Horaires par Secteur, Accès et Chiffres"      # px verifie au montage
DESC = ("Le MIN de Rungis pour les professionnels : horaires réels secteur par secteur, "
        "carte d'acheteur, chiffres du marché et ce que le carreau impose à la gestion.")
H1 = "MIN de Rungis : les horaires, l'accès, et ce que le carreau impose"
CHAPO = ("234 hectares, 1 226 entreprises, 1,86 million de tonnes par an. Voici Rungis vu "
         "du côté de celui qui y achète : quand chaque secteur ouvre, comment on y entre, "
         "et ce que le marché change dans la gestion d'un grossiste.")

MERE = "/negoce/marches-interet-national/"
LIENS = [MERE, "/negoce/", "/blog/min/", "/negoce/tracabilite-lots/",
         "/negoce/stocks-multi-depots/", "/negoce/achats-approvisionnements/",
         "/agroalimentaire/maraicher/", "/agroalimentaire/poissonnier/"]


def comparatif():
    """Rungis face aux seize autres — la donnee que le site officiel ne donne pas."""
    d = sorted(D.avec_donnees(), key=lambda m: -m[5])[:8]
    maxi = d[0][5]
    lignes = ""
    for m in d:
        est = m[0] == "rungis"
        lignes += ('<div class="mn-dr"><span class="mn-dn"%s>%s</span>'
                   '<span class="mn-dt"><i style="width:%.1f%%%s"></i></span>'
                   '<span class="mn-dv">%s</span></div>'
                   % (' style="color:#046C93;font-weight:800"' if est else '', m[1],
                      m[5] / maxi * 100,
                      ';background:linear-gradient(90deg,#00B1F5,#0079b8)' if est
                      else ';background:#cbd5e1',
                      format(round(m[5] / 1000), ",d").replace(",", " ") + " kt"))
    t = D.totaux()
    return ('<figure class="mn" id="rg-cmp">'
            '<figcaption class="mn-h"><p class="mn-k">Face aux seize autres</p>'
            '<p class="mn-s">Tonnage annuel, huit premiers marchés</p>'
            '<p class="mn-t">Rungis pèse %d %% du tonnage des MIN français</p></figcaption>'
            '<div class="mn-dens">' % round(1862000 / t["tonnage"] * 100)
            + lignes
            + '<p class="mn-cap">Mais pas le plus dense : 7 957 tonnes par hectare, contre '
              '25 417 à Lyon-Corbas sur douze hectares. Source : fédération des marchés de '
              'gros de France, relevé le 11 septembre 2026.</p></div></figure>')


def corps():
    p = []
    a = p.append

    # H2 1 — les chiffres. Lien mere dans les 100 premiers mots.
    a('<h2 id="chiffres">Le MIN de Rungis en chiffres</h2>')
    a('<p>Rungis est le plus grand des <a href="%s">dix-sept marchés d\'intérêt national</a> '
      'français, et se présente comme le premier marché de produits frais au monde. Si vous y '
      'travaillez, les règles du carreau s\'imposent à votre gestion : c\'est ce qu\'un '
      '<a href="/negoce/">ERP négoce alimentaire</a> prend en charge.</p>' % MERE)
    a(G.chiffres())
    a('<p>Le marché a ouvert en 1969, en remplacement des halles de Paris, et s\'étend à '
      'cheval sur les communes de Rungis et de Chevilly-Larue, dans le Val-de-Marne. Son '
      'statut n\'est pas commercial mais public : un '
      '<a href="/blog/min/">marché d\'intérêt national</a> est un service public de gestion '
      'de marché au sens des articles L761-1 à L761-11 du Code de commerce. '
      '<span class="hha-src">Source : %s.</span></p>' % R.SOURCE)

    # H2 2 — la frise, module au-dessus du 2e ecran
    a('<h2 id="horaires">Les horaires, secteur par secteur</h2>')
    a('<p>Il n\'y a pas un horaire de Rungis, il y en a onze. C\'est le point que personne ne '
      'publie lisiblement, et c\'est celui qui structure la journée d\'un acheteur.</p>')
    a(G.journee())
    a('<p>Un restaurateur qui prend du poisson et des légumes entre à 2 h et ressort après '
      '6 h. Un charcutier qui ne fait que la boucherie arrive à 3 h. Et le samedi, la '
      'boucherie est fermée quand la marée et la volaille tournent. C\'est ce décalage qui '
      'fait qu\'une commande partie du marché à 7 h doit être préparée, chargée et livrée '
      'avant l\'ouverture des clients.</p>')

    # H2 3 — le comparatif, donnee proprietaire
    a('<h2 id="poids">Ce que Rungis pèse face aux seize autres</h2>')
    a('<p>Le chiffre d\'affaires et la surface sont publiés partout. Le tonnage rapporté aux '
      'autres marchés, non — il se calcule.</p>')
    a(comparatif())
    a('<p>Autrement dit : Rungis écrase le réseau en volume, mais un carreau y est moins dense '
      'qu\'ailleurs. La marchandise y stationne plus longtemps, ce qui change la façon de '
      'tenir ses <a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a> par rapport à '
      'un marché comme Lyon-Corbas.</p>')

    # H2 4 — l'acces
    a('<h2 id="acces">Entrer à Rungis : la carte d\'acheteur</h2>')
    a('<p>L\'accès est réservé aux professionnels. Commerçants de détail, métiers de bouche, '
      'restaurateurs, traiteurs, collectivités et grossistes entrent sur présentation d\'une '
      'carte d\'acheteur. Un particulier n\'y fait pas ses courses ; il peut visiter, quand le '
      'marché organise des visites.</p>')
    a(G.carte())

    # H2 5 — le carreau et la gestion
    a('<h2 id="gestion">Ce que le carreau de Rungis impose à la gestion</h2>')
    a('<p>Le prix bouge dans la matinée, selon l\'arrivage et ce qu\'il reste. FranceAgriMer '
      'publie chaque jour les <a href="https://rnm.franceagrimer.fr/prix?M0123:MARCHE" '
      'target="_blank" rel="noopener">cours des grossistes relevés sur le MIN de Rungis</a> : '
      'c\'est la référence publique avant de négocier. Et entre le lot acheté et la facture '
      'envoyée, la marchandise traverse cinq étapes dont deux font disparaître de la marge.</p>')
    a(V.photo("pesee", "Sur le terrain", "Le poids réel remonte dans la ligne de commande",
              "On achète au kilo pesé, on facture au colis annoncé. Un colis annoncé à 10 kg "
              "qui en pèse 9,7 : l'écart est offert à chaque ligne, à chaque jour."))
    a('<p>Trois mécanismes répondent aux trois contraintes du carreau. La pesée entre dans la '
      'ligne de commande, et la facture suit le poids réel — c\'est le sujet des '
      '<a href="/negoce/achats-approvisionnements/">achats et approvisionnements</a>. La '
      '<a href="/negoce/tracabilite-lots/">traçabilité des lots</a> suit le lot et sa DLC, '
      'pas la référence produit, ce qui permet de prélever au plus près de la date. Et le '
      'stock reste juste entre le carreau, la chambre froide et le camion.</p>')

    # H2 6 — l'ecran
    a('<h2 id="logiciel">Ce que ça donne dans Hello Harel</h2>')
    a('<p>Les trois contraintes se règlent sur le même écran. Ce qui périme le plus tôt sort '
      'en premier, le poids réel remonte dans la ligne, et le stock reste juste quel que soit '
      'l\'emplacement.</p>')
    a(V.ecran())
    a('<p>Les grossistes en <a href="/agroalimentaire/maraicher/">fruits et légumes</a> et les '
      'professionnels de la <a href="/agroalimentaire/poissonnier/">poissonnerie</a> sont les '
      'premiers concernés à Rungis. Ce sont les deux secteurs qui ouvrent le plus tôt, et les '
      'seuls à subir à la fois le poids variable, la DLC courte et le prix du jour.</p>')

    return "".join(p)


FAQ = [
    ("C'est quoi le MIN de Rungis ?",
     "Le MIN de Rungis est le marché d'intérêt national qui approvisionne l'Île-de-France en "
     "produits frais. <strong>234 hectares</strong>, <strong>1 226 entreprises</strong>, "
     "<strong>12 000 salariés</strong> et <strong>12,02 milliards d'euros</strong> de chiffre "
     "d'affaires en 2024. Il a ouvert en 1969, en remplacement des halles de Paris."),
    ("À quelle heure ouvre le MIN de Rungis ?",
     "Cela dépend du secteur. La marée ouvre à <strong>2 h</strong>, la boucherie et la "
     "volaille à <strong>3 h</strong>, les fleurs coupées à <strong>4 h</strong>, les produits "
     "laitiers et la gastronomie à <strong>5 h</strong>, les fruits et légumes à "
     "<strong>5 h 30</strong>. Les jours varient aussi : la marée et la volaille fonctionnent "
     "du mardi au samedi, la boucherie du lundi au vendredi."),
    ("Qui peut acheter au MIN de Rungis ?",
     "Uniquement les professionnels, sur présentation d'une carte d'acheteur délivrée contre "
     "un justificatif d'activité. Les particuliers n'y achètent pas, sauf lors des visites "
     "organisées par le marché."),
    ("Quel logiciel pour un grossiste de Rungis ?",
     "Il faut un outil qui facture au poids réellement pesé et non au poids commandé, qui "
     "suive la DLC du lot et non la date du produit, et qui réconcilie un stock éclaté entre "
     "le carreau, la chambre froide et le camion. C'est ce que couvre un ERP de négoce "
     "alimentaire, et ce qu'un logiciel de facturation généraliste ne sait pas faire."),
]


def faq_section():
    q = "".join('<details class="minq"><summary>%s</summary><div><p>%s</p></div></details>'
                % (a, b) for a, b in FAQ)
    return ('<section class="faq-section"><div class="container">'
            '<div class="section-header"><p class="overline">FAQ</p>'
            '<h2>Questions sur le MIN de Rungis</h2></div>'
            '<div class="hha-art">' + q + '</div></div></section>')


def remplacer_section(c, cls, neuf):
    i = c.find('<section class="%s"' % cls)
    if i < 0:
        raise SystemExit("ARRET — section %s introuvable" % cls)
    j = c.find("</section>", i)
    if j < 0 or "<section" in c[i + 10:j]:
        raise SystemExit("ARRET — borne de fin incertaine sur %s" % cls)
    return c[:i] + neuf + c[j + len("</section>"):]


def main():
    c = w.get_raw("pages", GABARIT)["content"]["raw"]
    print("gabarit %d lu : %d octets" % (GABARIT, len(c)))

    nom, alt = PC.PHOTOS["hero"]
    f = os.path.join(S, nom)
    uri = "data:image/webp;base64," + base64.b64encode(open(f, "rb").read()).decode()
    m = re.search(r"(<section class=\"hero-section\"[^>]*url\(')([^']+)('\))", c)
    if not m:
        raise SystemExit("ARRET — fond du hero introuvable")
    c = c[:m.start(2)] + uri + c[m.end(2):]

    c = re.sub(r"<h1[^>]*>.*?</h1>", lambda _: "<h1>" + H1 + "</h1>", c, count=1, flags=re.S)
    i = c.find("</h1>")
    j = c.find("</p>", i)
    k = c.find("<p", i)
    if 0 < k < j:
        c = c[:k] + "<p>" + CHAPO + c[j:]
    c = c.replace('<div class="hero-badge"><span class="dot"></span>ERP Négoce — Traçabilité</div>',
                  '<div class="hero-badge"><span class="dot"></span>ERP Négoce — MIN de Rungis</div>')
    print("hero pose")

    contenu = corps()
    bloc = ('<section class="features-section" id="rungis"><div class="container">'
            + V.CSS + G.CSS + PC_FAQ_CSS + UI.CSS
            + '<div class="hha-art" style="max-width:820px;margin:0 auto">'
            + contenu + '</div></div></section>')
    c = remplacer_section(c, "features-section", bloc)
    print("corps pose : %d octets, %d H2, %d visuels"
          % (len(contenu), contenu.count("<h2"),
             contenu.count('<figure class="mn"') + contenu.count('<figure class="rg"')))

    c = remplacer_section(c, "faq-section", faq_section())
    c = c.replace("</body>", G.JS + "</body>") if "</body>" in c else c + G.JS

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
    c = re.sub(r"<link[^>]+cdnjs\.cloudflare\.com[^>]*>", "", c)
    c, _ = reparer(c)
    c = nettoyer(c)
    print("images integrees : %d" % ok)

    html = ("<title>%s</title>\n" % TITLE) + POLICE + "\n" + REPOS + "\n" + c
    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\necrit : %s (%d ko)" % (SORTIE, len(html) // 1024))

    pb = controler(html)
    for u in LIENS:
        if ('href="%s"' % u) not in contenu:
            pb.append("lien du plan absent du texte : %s" % u)
    nv = contenu.count('<figure class="mn"') + contenu.count('<figure class="rg"')
    if contenu.count("<h2") != nv:
        pb.append("un visuel par H2 non respecte : %d H2, %d visuels"
                  % (contenu.count("<h2"), nv))
    from PIL import ImageFont
    T = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 20)
    Dp = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 14)
    tp, dp = round(T.getlength(TITLE)), round(Dp.getlength(DESC))
    print("title %d px | description %d px" % (tp, dp))
    if not 200 <= tp <= 561:
        pb.append("title hors fourchette : %d px" % tp)
    if not 400 <= dp <= 985:
        pb.append("description hors fourchette : %d px" % dp)
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


PC_FAQ_CSS = """<style id="hh-rungis-faq">
#hh-page .minq,.minq{border:1px solid #e2e8f0;border-radius:14px;margin:0 auto .7rem !important;
 background:#fff;overflow:hidden;max-width:820px}
#hh-page .minq summary,.minq summary{cursor:pointer;padding:1rem 1.15rem;font-weight:600;
 color:#0f172a;list-style:none;display:flex;justify-content:space-between;gap:1rem;align-items:center}
#hh-page .minq summary::-webkit-details-marker{display:none}
#hh-page .minq summary::after,.minq summary::after{content:"+";color:#00B1F5;font-size:1.25rem;
 font-weight:400;flex:0 0 auto}
#hh-page .minq[open] summary::after,.minq[open] summary::after{content:"−"}
#hh-page .minq summary:focus-visible{outline:2px solid #0f172a;outline-offset:-2px}
#hh-page .minq div,.minq div{padding:0 1.15rem 1.1rem}
#hh-page .minq div p,.minq div p{margin:0 !important;color:#475569;line-height:1.65}
#hh-page .hha-src,.hha-src{font-size:.82rem;color:#64748b}
</style>"""


if __name__ == "__main__":
    main()
