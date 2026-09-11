#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deux maquettes de /agroalimentaire/traiteur/, pour comparaison :

  A — la page telle qu'elle est en ligne aujourd'hui, rien change
  B — la meme, avec les fonctionnalites en onglets et leurs ecrans du
      logiciel, plus la section guide vers le comparatif traiteur

MAQUETTES, PAS MISE EN LIGNE. La page 2818 est protegee par la regle 0 :
ce script la lit, il ne l'ecrit jamais.

La version B reprend les CINQ MEMES fonctionnalites que la page porte deja —
planning d'evenements, achats et stocks evenementiels, cout et marge par
evenement, tracabilite et HACCP, devis et fiches techniques. Seule la forme
change : un module a onglets et un ecran du logiciel par fonctionnalite.

Usage :  python3 maquette_traiteur.py
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import base64                 # noqa: E402
import wp_common as w        # noqa: E402
import agro_ebook            # noqa: E402
import traiteur_ui           # noqa: E402
from maquette_agro import (convertir, POLICE, REPOS, SVG_FA,  # noqa: E402
                           nettoyer, reparer, controler, remplacer_video)

PAGE = 2839   # /agroalimentaire/traiteur/ — 2818 est le charcutier
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"

# La photo de hero de la page traiteur est celle d'une autre page : le fichier
# s'appelle ERP-logiciel-pour-les-grossistes-en-lait.webp et montre un homme en
# costume dans un entrepot de casiers de lait. Signale au client le 11/09.
# La version B la remplace par une brigade qui dresse en serie des assiettes
# identiques sur le passe — la production evenementielle, pas la logistique.
# Photo Pexels 15671274, recadree en 1920x1080, WebP 133 ko.
PHOTO = os.path.join(S, "erp-traiteur-dressage-assiettes-serie.webp")


def hero_traiteur(c):
    """Remplace le fond de la section hero. Version B seulement."""
    m = re.search(r"(<section class=\"hero-section\"[^>]*url\(')([^']+)('\))", c)
    if not m:
        raise SystemExit("ARRET — fond de la section hero introuvable")
    if not os.path.exists(PHOTO):
        raise SystemExit("ARRET — photo de hero absente : %s" % PHOTO)
    uri = ("data:image/webp;base64,"
           + base64.b64encode(open(PHOTO, "rb").read()).decode())
    return c[:m.start(2)] + uri + c[m.end(2):], m.group(2).split("/")[-1]


ENTETE = ('<div class="section-header">'
          '<p class="overline">ERP Traiteur</p>'
          '<h2>L\'ERP conçu pour les traiteurs</h2>'
          '<p>Événements, fiches techniques, coûts et conformité</p>'
          '</div>')

GUIDE_TITRE = "Comment choisir un ERP traiteur"
GUIDE_HUB = "/comparatifs/meilleur-erp-traiteur/"
GUIDE_CHAPO = ("Cinq questions décident du choix, et aucune ne porte sur le nombre de "
               "fonctionnalités. Chaque chapitre répond à l'une d'elles, puis le comparatif "
               "des ERP traiteur vous donne le classement.")
GUIDE_CHAPITRES = [
    ("Le coût au couvert : ce qu'un logiciel de caisse ne calcule pas",
     "/blog/logiciel-calcul-cout-de-revient-traiteur/"),
    ("Allergènes et DLC : le test qui élimine la moitié des candidats",
     "/blog/logiciel-tracabilite-dlc-traiteur/"),
    ("La facture d'événement, du devis au solde",
     "/blog/facture-traiteur/"),
    ("Ce que coûte vraiment un ERP, au-delà des licences",
     "/blog/roi-erp/"),
    ("Cloud ou serveur : la question à trancher avant de comparer",
     "/blog/erp-cloud-saas-vs-on-premise/"),
]


def assembler(c, version):
    """version 'A' : on ne touche a rien. version 'B' : onglets et guide."""
    if version == "B":
        i = c.find('<section class="features-section"')
        j = c.find('</section>', i)
        if i < 0 or j < 0:
            raise SystemExit("ARRET — section des fonctionnalites introuvable")
        j += len('</section>')
        if '<section' in c[i + 10:j]:
            raise SystemExit("ARRET — section imbriquee, la borne de fin est fausse")
        c = c[:i] + traiteur_ui.section(ENTETE) + c[j:]

        c, ancienne = hero_traiteur(c)
        print("   · photo de hero remplacee (avant : %s)" % ancienne)

        k = c.rfind('<section class="cta-banner"')
        if k < 0:
            k = c.rfind('</div>')
        c = c[:k] + agro_ebook.section(GUIDE_TITRE, GUIDE_CHAPITRES, GUIDE_HUB, GUIDE_CHAPO) + c[k:]

    # les deux versions subissent le meme traitement d'artefact, sinon la
    # comparaison porterait sur le traitement et non sur la page
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
    c, _ = reparer(c)
    c, _ = remplacer_video(c)
    c = nettoyer(c)

    titre = ("ERP traiteur — version %s" % version)
    return ("<title>%s</title>\n" % titre) + POLICE + "\n" + REPOS + "\n" + c, ok


def main():
    brut = w.get_raw("pages", PAGE)["content"]["raw"]
    print("page %d lue : %d octets" % (PAGE, len(brut)))

    for version in ("A", "B"):
        html, ok = assembler(brut, version)
        f = os.path.join(S, "traiteur-%s.html" % version)
        open(f, "w", encoding="utf-8").write(html)
        pb = controler(html)
        print("\nversion %s : %d ko, %d images integrees" % (version, len(html) // 1024, ok))
        for x in pb:
            print("   !", x)
        if not pb:
            print("   controles : tout est vert")


if __name__ == "__main__":
    main()
