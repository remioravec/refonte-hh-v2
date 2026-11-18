#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4.2 — Montage de la page MIN sur le gabarit des PAGES.

Gabarit de reference : /negoce/tracabilite-lots/ (page 6077), une fille de
/negoce/ — donc exactement l'etage ou cette page doit vivre.
Sections conservees : hero, logos, about, process, metiers, equipe, temoignage,
avis, banniere. Seules la features-section et la FAQ sont remplacees.

Un visuel par H2, six H2. Lien mere dans les 100 premiers mots.

MAQUETTE. Rien n'est ecrit sur WordPress.

Usage :  python3 page_min.py
"""

import base64
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                # noqa: E402
import page_min_contenu as C         # noqa: E402
import page_min_visuels as V         # noqa: E402
import min_fiches as F               # noqa: E402
import min_data as D                 # noqa: E402
import agro_ui as UI                 # noqa: E402
from maquette_agro import convertir, POLICE, REPOS, SVG_FA, nettoyer, reparer, controler  # noqa: E402

GABARIT = 6077
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "page-min.html")


def corps():
    p = []
    a = p.append

    # H2 1 — le tableau, module interactif au-dessus du 2e ecran.
    # Lien mere dans les 100 premiers mots.
    t = D.totaux()
    a('<h2 id="liste">Les 17 MIN de France, marché par marché</h2>')
    a('<p>Un <a href="/blog/min/">marché d\'intérêt national</a> est un marché de gros au '
      'statut public, réservé aux professionnels. Il y en a dix-sept en France, ils traitent '
      '<strong>%s tonnes par an sur %.0f hectares</strong>, et si vous travaillez sur l\'un '
      'd\'eux, votre gestion en subit les règles : c\'est précisément ce qu\'un '
      '<a href="/negoce/">ERP négoce alimentaire</a> prend en charge. Commençons par la '
      'carte.</p>' % (format(t["tonnage"], ",d").replace(",", " "), t["surface"]))
    a('<figure class="mn" id="mn-fiches">'
      '<figcaption class="mn-h"><p class="mn-k">Les 17 marchés</p>'
      '<p class="mn-s">Superficie et tonnage : fédération des marchés de gros de France</p>'
      '<p class="mn-t">Une fiche par marché, cliquez pour le détail</p></figcaption>'
      + F.toutes() + '</figure>')
    a('<p>La commune ne suit pas toujours le nom : le MIN de Nantes est à Rezé, celui de Lyon '
      'à Corbas, et Rungis est à cheval sur Rungis et Chevilly-Larue. '
      '<span class="hha-src">Source : %s.</span></p>' % C.SOURCE)

    # H2 2 — ce que revele la comparaison : la donnee proprietaire
    a('<h2 id="comparaison">Ce que révèle la comparaison des dix-sept</h2>')
    a('<p>Mis sur la même grille, les marchés ne se ressemblent pas. '
      '<strong>Rungis pèse %d %% du tonnage</strong> à lui seul. Mais rapporté à la surface, '
      'ce n\'est pas le plus dense : Rungis traite %s tonnes par hectare quand Lyon-Corbas en '
      'traite %s, soit <strong>trois fois plus sur douze hectares</strong>. La densité va de '
      '%s à %s tonnes par hectare d\'un marché à l\'autre.</p>'
      % (round(1862000 / t["tonnage"] * 100),
         format(round(1862000 / 234), ",d").replace(",", " "),
         format(round(305000 / 12), ",d").replace(",", " "),
         format(round(86000 / 25.5), ",d").replace(",", " "),
         format(round(305000 / 12), ",d").replace(",", " ")))
    a(V.densites())
    a('<p>Cette densité n\'est pas une curiosité : elle décrit la pression sur les quais. Plus '
      'un marché est dense, moins la marchandise y stationne, et plus l\'écart entre le stock '
      'théorique et le stock réel se creuse vite. C\'est le premier argument pour tenir ses '
      '<a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a> en temps réel plutôt '
      'qu\'à l\'inventaire.</p>')
    a('<p class="hha-src">Superficie et tonnage : %s, relevés le %s. Quinze marchés sur '
      'dix-sept publient les deux. Trois valeurs publiées nous paraissent douteuses et sont '
      'signalées sur leur fiche plutôt que recopiées.</p>'
      % (D.SOURCES["federation"][0], D.RELEVE))

    # H2 3 — les contraintes + le flux
    a('<h2 id="carreau">Ce que le carreau impose à votre gestion</h2>')
    a('<p>Travailler sur un marché d\'intérêt national, ce n\'est pas acheter autrement : '
      'c\'est acheter dans des conditions que votre logiciel doit savoir encaisser. Trois '
      'contraintes reviennent sur les dix-sept marchés.</p>')
    a(V.contraintes())

    # H2 3 — la pesee, photo
    a('<h2 id="poids">Facturer le poids réellement pesé</h2>')
    a('<p>C\'est l\'écart le plus banal et le plus coûteux. Un colis annoncé à 10 kg en pèse '
      '9,7. Si la facture part sur le poids commandé, les 300 grammes sont offerts — à chaque '
      'ligne, à chaque jour. Un outil de facturation généraliste facture ce qui a été '
      'commandé ; sur un carreau, il faut facturer ce qui a été pesé.</p>')
    a(V.photo("pesee", "Sur le terrain", "La pesée entre dans la ligne de commande",
              "La balance renseigne directement la ligne : le poids réel remonte dans la "
              "commande, puis dans le bon de livraison, puis dans la facture. Sans ressaisie."))
    a('<p>Ce mécanisme suppose que la chaîne complète porte le poids, de l\'arrivage à la '
      'facture. C\'est le rôle des <a href="/negoce/achats-approvisionnements/">achats et '
      'approvisionnements</a> en amont, et des '
      '<a href="/negoce/ventes-devis-commandes/">ventes, devis et commandes</a> en aval.</p>')

    # H2 4 — la DLC, chronologie
    a('<h2 id="dlc">Suivre la DLC du lot, pas la date du produit</h2>')
    a('<p>Sur un MIN, les dates sont courtes. Un lot de marée arrivé à 2 h peut périmer trois '
      'jours plus tard. La date qui compte n\'est pas celle de la référence produit, mais '
      'celle du lot précis que vous avez chargé.</p>')
    a(V.chronologie())
    a('<p>La conséquence opérationnelle est le prélèvement : il faut sortir en premier ce qui '
      'périme en premier, ce que seule une '
      '<a href="/negoce/tracabilite-lots/">traçabilité des lots</a> au niveau du lot permet.</p>')

    # H2 5 — le stock, photo
    a('<h2 id="stock">Réconcilier le carreau, la chambre froide et le camion</h2>')
    a('<p>À un instant donné, votre marchandise est à trois endroits : encore sur le carreau, '
      'déjà en chambre froide, ou chargée dans un camion en tournée. Un stock tenu sur un '
      'seul emplacement ne décrit jamais la réalité, et l\'écart se découvre à l\'inventaire.</p>')
    a(V.photo("stock", "Sur le terrain", "Le stock vit sur plusieurs emplacements",
              "Entre la réception, la chambre froide et le chargement, la même palette change "
              "trois fois d'endroit dans la matinée. Le stock doit suivre, pas être reconstitué."))
    a('<p>C\'est exactement ce que couvre la gestion des '
      '<a href="/negoce/stocks-multi-depots/">stocks multi-dépôts</a>, et ce qui permet de '
      'répercuter un mouvement de prix sur la gamme via les '
      '<a href="/negoce/tarifs-reporting-edi/">tarifs, reporting et EDI</a>.</p>')

    # H2 6 — l'ecran
    a('<h2 id="logiciel">Ce que ça donne dans Hello Harel</h2>')
    a('<p>Les trois contraintes se règlent sur le même écran : ce qui périme le plus tôt sort '
      'en premier, le poids réel remonte dans la ligne, et le stock reste juste quel que soit '
      'l\'emplacement.</p>')
    a(V.ecran())
    a('<p>Les grossistes en <a href="/agroalimentaire/maraicher/">fruits et légumes</a> et les '
      'professionnels de la <a href="/agroalimentaire/poissonnier/">poissonnerie</a> sont les '
      'premiers concernés : ce sont eux qui subissent à la fois le poids variable, la DLC '
      'courte et le prix du jour.</p>')

    return "".join(p)


def faq():
    q = "".join('<details class="minq"><summary>%s</summary><div><p>%s</p></div></details>'
                % (a, b) for a, b in C.FAQ)
    return ('<section class="faq-section"><div class="container">'
            '<div class="section-header"><p class="overline">FAQ</p>'
            '<h2>Questions sur les marchés d\'intérêt national</h2></div>'
            '<div class="hha-art">' + q + '</div></div></section>')


FAQ_CSS = """<style id="hh-min-faq">
#hh-page .minq,.minq{border:1px solid #e2e8f0;border-radius:14px;margin:0 auto .7rem !important;
 background:#fff;overflow:hidden;max-width:820px}
#hh-page .minq summary,.minq summary{cursor:pointer;padding:1rem 1.15rem;font-weight:600;
 color:#0f172a;list-style:none;display:flex;justify-content:space-between;gap:1rem;
 align-items:center}
#hh-page .minq summary::-webkit-details-marker{display:none}
#hh-page .minq summary::after,.minq summary::after{content:"+";color:#00B1F5;font-size:1.25rem;
 font-weight:400;flex:0 0 auto}
#hh-page .minq[open] summary::after,.minq[open] summary::after{content:"−"}
#hh-page .minq summary:focus-visible{outline:2px solid #0f172a;outline-offset:-2px}
#hh-page .minq div,.minq div{padding:0 1.15rem 1.1rem}
#hh-page .minq div p,.minq div p{margin:0 !important;color:#475569;line-height:1.65}
#hh-page .hha-src,.hha-src{font-size:.82rem;color:#64748b}
</style>"""


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

    # --- la photo de hero
    nom, alt = C.PHOTOS["hero"]
    f = os.path.join(S, nom)
    if not os.path.exists(f):
        raise SystemExit("ARRET — photo de hero absente")
    uri = "data:image/webp;base64," + base64.b64encode(open(f, "rb").read()).decode()
    m = re.search(r"(<section class=\"hero-section\"[^>]*url\(')([^']+)('\))", c)
    if not m:
        raise SystemExit("ARRET — fond du hero introuvable")
    c = c[:m.start(2)] + uri + c[m.end(2):]
    print("photo de hero posee (avant : %s)" % m.group(2).split("/")[-1])

    # --- hero : H1, chapo, fil d'Ariane
    c = re.sub(r"<h1[^>]*>.*?</h1>", lambda _: "<h1>" + C.H1 + "</h1>", c, count=1, flags=re.S)
    i = c.find("</h1>")
    j = c.find("</p>", i)
    if j > 0:
        k = c.find("<p", i)
        if 0 < k < j:
            c = c[:k] + "<p>" + C.CHAPO + c[j:]
    print("hero pose")

    # --- le corps remplace la features-section
    contenu = corps()
    bloc = ('<section class="features-section" id="min"><div class="container">'
            + V.CSS + F.CSS + FAQ_CSS + UI.CSS
            + '<div class="hha-art" style="max-width:820px;margin:0 auto">'
            + contenu + '</div></div></section>')
    c = remplacer_section(c, "features-section", bloc)
    print("corps pose : %d octets, %d H2, %d visuels"
          % (len(contenu), contenu.count("<h2"), contenu.count('<figure class="mn"')))

    # --- la FAQ du gabarit prend nos questions
    c = remplacer_section(c, "faq-section", faq())
    print("FAQ posee : %d questions" % len(C.FAQ))

    c = c.replace("</body>", V.JS + "</body>") if "</body>" in c else c + V.JS

    # --- traitement d'artefact
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

    html = ("<title>%s</title>\n" % C.TITLE) + POLICE + "\n" + REPOS + "\n" + c
    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\necrit : %s (%d ko)" % (SORTIE, len(html) // 1024))

    pb = controler(html)
    # maillage : chaque lien du plan doit etre dans le texte
    PLAN = ["/negoce/", "/blog/min/", "/negoce/achats-approvisionnements/",
            "/negoce/ventes-devis-commandes/", "/negoce/stocks-multi-depots/",
            "/negoce/tracabilite-lots/", "/negoce/tarifs-reporting-edi/",
            "/agroalimentaire/maraicher/", "/agroalimentaire/poissonnier/"]
    for u in PLAN:
        if ('href="%s"' % u) not in contenu:
            pb.append("lien du plan absent du texte : %s" % u)
    if contenu.count("<h2") != contenu.count('<figure class="mn"'):
        pb.append("un visuel par H2 non respecte : %d H2, %d visuels"
                  % (contenu.count("<h2"), contenu.count('<figure class="mn"')))
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
