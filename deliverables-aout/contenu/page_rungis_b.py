#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIN de Rungis — page fille, VERSION B « modele Bellon ».

D'OU VIENT CE GABARIT
=====================
Le client a fourni le code source de
https://groupe-bellon.fr/gasc-m-i-n-carreau-produits-carnes/ — la page de leur
offre pour les grossistes de carreau. Sa mecanique, relevee le 12/09/2026 :

  H2 d'introduction + schema d'ensemble
  puis UN module a onglets — treize onglets, un par module fonctionnel —
  chaque onglet : titre, paragraphe, liste a puces, capture 1024x576.

Toute la page tient dans ce module. C'est une page de COUVERTURE
FONCTIONNELLE : elle ne raconte pas le marche, elle montre le logiciel.

CE QUE CETTE VERSION B REPREND
------------------------------
La mecanique entiere : introduction + schema, puis le module a onglets comme
coeur de page, un onglet par module fonctionnel, avec sa capture.

CE QU'ELLE CORRIGE — le detail est documente dans rungis_modules.py :
  · 13 onglets -> 7, dans l'ordre de la journee reelle du carreau ;
  · onglets nommes par le geste du grossiste, pas par le nom du module
    (mesure du 11/09/2026 : 8 des 9 termes metier de Bellon sont sous le seuil
    de mesure de Google Ads, < 10 recherches / mois) ;
  · zero JavaScript : boutons radio + labels, rien n'est injecte au clic ;
  · captures en HTML/CSS et non en JPG : du texte reel, lisible par un moteur
    et par un lecteur d'ecran, redimensionnable sur mobile.

CE QU'ELLE AJOUTE, ET QUE BELLON N'A PAS
----------------------------------------
Une page 100 %% fonctionnelle ne se cherche pas. La SERP « min de rungis »,
relevee le 11/09/2026, est informationnelle : site officiel, questions posees,
cours FranceAgriMer, Wikipedia, cinquante offres d'emploi, fiche Google a 656
avis. Aucun editeur de logiciel dans les dix.

On garde donc DEUX ancrages editoriaux que personne ne publie lisiblement, et
qui sont ce par quoi la page peut entrer :
  · la frise des horaires, secteur par secteur ;
  · Rungis rapporte aux seize autres MIN, en tonnage et en densite.
C'est la difference entre la page de Bellon — qui ne rank sur rien — et
celle-ci.

REQUETES — « min de rungis » 1 600 / mois, « min rungis » 1 600,
« grossiste rungis » 210, « carte acheteur rungis » 170, « min rungis prix » 50.
Source : planificateur Google Ads, France, moyenne 12 mois arretee en juillet
2026, relevee le 11/09/2026.

MAQUETTE. Rien n'est ecrit sur WordPress.

Usage :  python3 page_rungis_b.py
"""

import base64
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                      # noqa: E402
import page_min_contenu as PC              # noqa: E402
import page_min_visuels as V               # noqa: E402
import blog_rungis_contenu as R            # noqa: E402
import blog_rungis_infographies as G       # noqa: E402
import agro_ui as UI                       # noqa: E402
import rungis_modules as MOD               # noqa: E402
import page_rungis as A                    # noqa: E402
from maquette_agro import convertir, POLICE, REPOS, SVG_FA, nettoyer, reparer, controler  # noqa: E402

GABARIT = 6077
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "page-rungis-b.html")

TITLE = "MIN de Rungis : le Logiciel du Carreau, Module par Module"
DESC = ("Le MIN de Rungis vu du carreau : les sept étapes de la journée d'un grossiste, "
        "l'écran de chacune, les horaires par secteur et ce que le marché pèse.")
H1 = "MIN de Rungis : la journée d'un grossiste, et le logiciel qui la tient"
CHAPO = ("Sur le carreau, la marge se perd à deux endroits : le poids qu'on ne repèse pas et "
         "la date qu'on ne suit pas. Voici les sept étapes de la journée d'un grossiste de "
         "Rungis, et l'écran qui répond à chacune.")

MERE = "/negoce/marches-interet-national/"
LIENS = [MERE, "/negoce/", "/blog/min/", "/negoce/tracabilite-lots/",
         "/negoce/stocks-multi-depots/", "/negoce/achats-approvisionnements/",
         "/agroalimentaire/maraicher/", "/agroalimentaire/poissonnier/"]


def corps():
    p = []
    a = p.append

    # ------------------------------------------------ H2 1 : intro + schema
    # Chez Bellon : un H2 d'introduction et un schema d'ensemble. Meme geste,
    # mais le schema porte une donnee et pas un dessin d'architecture.
    a('<h2 id="carreau">Ce que le carreau de Rungis impose à un grossiste</h2>')
    a('<p>Rungis est le plus grand des <a href="%s">dix-sept marchés d\'intérêt national</a> '
      'français. Pour celui qui y achète, le marché n\'est pas un décor : il impose trois '
      'contraintes que la gestion doit absorber le jour même. Le poids réel n\'est pas le '
      'poids annoncé, la date limite appartient au lot et non au produit, et le prix du '
      'carreau bouge dans la matinée. C\'est ce que prend en charge un '
      '<a href="/negoce/">ERP de négoce alimentaire</a>.</p>' % MERE)
    a(V.contraintes())
    a('<p>Le statut du marché n\'est pas commercial mais public : un '
      '<a href="/blog/min/">marché d\'intérêt national</a> est un service public de gestion '
      'de marché au sens des articles L761-1 à L761-11 du Code de commerce. Les prix, eux, '
      'sont publics aussi : FranceAgriMer publie chaque jour les '
      '<a href="https://rnm.franceagrimer.fr/prix?M0123:MARCHE" target="_blank" '
      'rel="noopener">cours des grossistes relevés sur le MIN de Rungis</a>. '
      '<span class="hha-src">Source : %s.</span></p>' % R.SOURCE)

    # ------------------------------- H2 2 : le coeur, le module a onglets
    a('<h2 id="modules">Les sept étapes de la journée, et l\'écran de chacune</h2>')
    a('<p>Une journée de carreau se lit dans l\'ordre : on achète, on pèse, on suit le lot, '
      'on prépare, on livre, on facture, on mesure. Chaque étape a son écran. Choisissez la '
      'vôtre — les sept sont dans la page, aucune n\'attend un clic pour exister.</p>')
    a(MOD.section())
    a('<p>Les grossistes en <a href="/agroalimentaire/maraicher/">fruits et légumes</a> et les '
      'professionnels de la <a href="/agroalimentaire/poissonnier/">poissonnerie</a> sont les '
      'premiers concernés : ce sont les deux secteurs qui ouvrent le plus tôt à Rungis, et les '
      'seuls à subir en même temps le poids variable, la DLC courte et le prix du jour.</p>')

    # ------------------- H2 3 : l'ancrage editorial 1, la frise des horaires
    a('<h2 id="horaires">Les horaires de Rungis, secteur par secteur</h2>')
    a('<p>Il n\'y a pas un horaire de Rungis, il y en a onze. C\'est ce qui décide de l\'heure '
      'à laquelle une commande peut partir, donc de l\'heure à laquelle elle doit être '
      'préparée.</p>')
    a(G.journee())
    a('<p>Un restaurateur qui prend du poisson et des légumes entre à 2 h et ressort après '
      '6 h. Le samedi, la boucherie est fermée quand la marée et la volaille tournent. Une '
      'commande partie du marché à 7 h doit être préparée, chargée et livrée avant l\'ouverture '
      'des clients : c\'est ce décalage que les étapes « Préparer » et « Livrer » ci-dessus '
      'absorbent.</p>')

    # ------------------ H2 4 : l'ancrage editorial 2, la donnee proprietaire
    a('<h2 id="poids">Ce que Rungis pèse face aux seize autres marchés</h2>')
    a('<p>Le chiffre d\'affaires et la surface du marché sont publiés partout. Le tonnage '
      'rapporté aux seize autres MIN, non : il se calcule.</p>')
    a(A.comparatif())
    a('<p>Rungis écrase le réseau en volume, mais un carreau y est moins dense qu\'ailleurs : '
      'la marchandise y stationne plus longtemps. C\'est ce qui rend le suivi des '
      '<a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a> et de la '
      '<a href="/negoce/tracabilite-lots/">traçabilité des lots</a> plus sensible ici que sur '
      'un marché comme Lyon-Corbas, et ce qui fait de l\'étape '
      '<a href="/negoce/achats-approvisionnements/">achats et approvisionnements</a> le point '
      'où la marge se gagne.</p>')

    return "".join(p)


FAQ = [
    ("Quel logiciel pour un grossiste du MIN de Rungis ?",
     "Il faut un outil qui facture au poids réellement pesé et non au poids commandé, qui "
     "suive la <strong>DLC du lot</strong> et non la date du produit, et qui réconcilie un "
     "stock éclaté entre le carreau, la chambre froide et le camion. C'est ce que couvre un "
     "ERP de négoce alimentaire, et ce qu'un logiciel de facturation généraliste ne sait pas "
     "faire."),
    ("À quelle heure ouvre le MIN de Rungis ?",
     "Cela dépend du secteur. La marée ouvre à <strong>2 h</strong>, la boucherie et la "
     "volaille à <strong>3 h</strong>, les fleurs coupées à <strong>4 h</strong>, les produits "
     "laitiers et la gastronomie à <strong>5 h</strong>, les fruits et légumes à "
     "<strong>5 h 30</strong>. La marée et la volaille fonctionnent du mardi au samedi, la "
     "boucherie du lundi au vendredi."),
    ("Comment gérer l'écart entre le poids annoncé et le poids pesé ?",
     "En le constatant à quai, pas en fin de mois. Un colis annoncé à 10 kg qui en pèse "
     "<strong>9,7 kg</strong> représente <strong>3 %</strong> offerts sur chaque ligne. "
     "L'agréage enregistre les deux poids sur la même ligne de réception et ouvre la "
     "réclamation fournisseur tant qu'elle est recevable."),
    ("Qui peut acheter au MIN de Rungis ?",
     "Uniquement les professionnels, sur présentation d'une <strong>carte d'acheteur</strong> "
     "délivrée contre un justificatif d'activité : commerçants de détail, métiers de bouche, "
     "restaurateurs, traiteurs, collectivités et grossistes. Les particuliers n'y achètent "
     "pas, sauf lors des visites organisées par le marché."),
    ("Que pèse le MIN de Rungis face aux autres marchés d'intérêt national ?",
     "<strong>1,86 million de tonnes</strong> par an, soit <strong>43 %</strong> du tonnage "
     "des dix-sept MIN français, sur <strong>234 hectares</strong>. Mais pas le plus dense : "
     "<strong>7 957 tonnes par hectare</strong>, contre <strong>25 417</strong> à Lyon-Corbas. "
     "Relevé le 11 septembre 2026."),
]


def faq_section():
    q = "".join('<details class="minq"><summary>%s</summary><div><p>%s</p></div></details>'
                % (a, b) for a, b in FAQ)
    return ('<section class="faq-section"><div class="container">'
            '<div class="section-header"><p class="overline">FAQ</p>'
            '<h2>Questions sur le MIN de Rungis et sa gestion</h2></div>'
            '<div class="hha-art">' + q + '</div></div></section>')


def main():
    c = w.get_raw("pages", GABARIT)["content"]["raw"]
    print("gabarit %d lu : %d octets" % (GABARIT, len(c)))

    nom, _ = PC.PHOTOS["hero"]
    f = os.path.join(S, nom)
    if not os.path.exists(f):
        raise SystemExit("ARRET — photo de hero absente : %s" % f)
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
    print("hero pose")

    contenu = corps()
    bloc = ('<section class="features-section" id="rungis"><div class="container">'
            + V.CSS + G.CSS + A.PC_FAQ_CSS + UI.CSS + MOD.CSS
            + '<div class="hha-art" style="max-width:860px;margin:0 auto">'
            + contenu + '</div></div></section>')
    c = A.remplacer_section(c, "features-section", bloc)
    nv = contenu.count('<figure class="mn"') + contenu.count('<figure class="rg"')
    print("corps pose : %d octets, %d H2, %d H3, %d visuels"
          % (len(contenu), contenu.count("<h2"), contenu.count("<h3"), nv))

    c = A.remplacer_section(c, "faq-section", faq_section())
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
    if contenu.count("<h2") != nv:
        pb.append("un visuel par H2 non respecte : %d H2, %d visuels"
                  % (contenu.count("<h2"), nv))
    if contenu.count("<h3") != len(MOD.MODULES):
        pb.append("H3 attendus : %d, trouves %d" % (len(MOD.MODULES), contenu.count("<h3")))
    if html.count('name="mnm-onglet"') != len(MOD.MODULES):
        pb.append("onglets perdus au montage")
    if "<script" in MOD.section():
        pb.append("le module a onglets embarque du JavaScript")

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


if __name__ == "__main__":
    main()
