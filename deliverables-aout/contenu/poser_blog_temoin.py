#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose le gabarit sur l'article temoin, pour validation avant deploiement.

Article : /blog/tracabilite-lot-dlc-logiciel/ — le plus fourni du parc.

Le simulateur reste en place : decision de Remi. Sur une requete de blog,
il repond a l'intention de recherche.

Usage :  python3 poser_blog_temoin.py            (blanc)
         python3 poser_blog_temoin.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import faq_accordeon as FA       # noqa: E402
import blog_gabarit as BG        # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/blog-avant")
ARTICLE = 7761
URL = "/blog/tracabilite-lot-dlc-logiciel/"


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    c = w.get_raw("posts", ARTICLE)["content"]["raw"]
    depart = c

    # ── 1. les deux cartes de rendez-vous, recuperees avant tout ──────────
    cartes = []
    i = c.find('<section class="faq-section"')
    j = c.find("</section>", i) + len("</section>")
    sec = c[i:j]
    m = re.search(r"var faqData\s*=\s*(\[.*?\]);", c, re.S)
    if not m:
        raise SystemExit("ARRET — faqData introuvable")
    for t, d in re.findall(
            r'\{"title":\s*"([^"]+)",\s*"html":\s*"(.*?)"\}', m.group(1), re.S):
        lien = re.search(r'href=\\"([^\\"]+)\\"', d)
        lib = re.search(r'>([^<]+)<\\/a>', d)
        txt = re.sub(r"<[^>]+>", " ", d.replace("\\/", "/")).strip()
        txt = re.sub(r"\s+", " ", txt)
        if lib:
            txt = txt.replace(lib.group(1), "").strip()
        cartes.append((t, txt, (lib.group(1) if lib else "En savoir plus").replace(" →", ""),
                       lien.group(1).replace("\\/", "/") if lien else "/contact/"))
    if len(cartes) != 2:
        raise SystemExit("ARRET — %d carte(s) de rendez-vous au lieu de 2" % len(cartes))

    # ── 2. la vraie FAQ prend la place de la fausse ───────────────────────
    entete = ('<div class="section-header"><p class="overline">FAQ</p>'
              '<h2 id="faq">Les réponses à vos questions</h2>'
              '<p>Traçabilité, dates limites et rappel produit.</p></div>')
    c = c[:i] + BG.bloc_faq(entete, BG.TEMOIN, FA.CSS) + BG.bloc_cta(cartes) + c[j:]

    # ── 3. le tiroir et son script n'ont plus d'objet ─────────────────────
    for ident in ('id="faqOverlay"', 'id="faqDrawer"'):
        k = c.find(ident)
        while k >= 0:
            import remanier_agro as RA
            d0 = c.rfind("<div", 0, k)
            fin = RA.div_complet(c, d0)
            if D.solde(c[d0:fin]) != 0:
                raise SystemExit("ARRET — bloc de tiroir non clos")
            c = c[:d0] + c[fin:]
            k = c.find(ident)
    for mm in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S))[::-1]:
        if "faqData" in mm.group(1) or "openFaqDrawer" in mm.group(1):
            c = c[:mm.start()] + c[mm.end():]
    # l'ancien balisage declarait les deux rendez-vous comme des questions
    avant_ld = len(re.findall(r'"@type": "FAQPage"', depart))
    c = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*?'
               r'Voyez Hello Harel(?:(?!</script>).)*?</script>', "", c, flags=re.S)

    # ── 4. les accents des titres ─────────────────────────────────────────
    c, n_acc = BG.accentuer_titres(c)

    # ── controles ─────────────────────────────────────────────────────────
    corps = D.sans_code(c)
    for x in ("faq-card", "openFaqDrawer", "faqDrawerContent"):
        if x in corps:
            raise SystemExit("ARRET — %r survit dans le corps" % x)
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    if c.count("<details") != len(BG.TEMOIN):
        raise SystemExit("ARRET — %d accordeons pour %d questions"
                         % (c.count("<details"), len(BG.TEMOIN)))
    if "hha-tool" not in c:
        raise SystemExit("ARRET — le simulateur a disparu")
    perdus = [x for x in D.liens(depart) if x not in D.liens(c)]
    if perdus:
        raise SystemExit("ARRET — lien(s) perdu(s) : %s" % perdus[:3])
    ld = len(re.findall(r'"@type": "FAQPage"', c))

    print("%-46s %d -> %d ko" % (URL, len(depart) // 1024, len(c) // 1024))
    print("   %d questions reelles, reponses dans le HTML" % len(BG.TEMOIN))
    print("   2 cartes de rendez-vous deplacees : %s" % ", ".join(x[3] for x in cartes))
    print("   %d titre(s) reaccentue(s)" % n_acc)
    print("   balisage FAQPage : %d -> %d (les rendez-vous n'y sont plus declares "
          "comme des questions)" % (avant_ld, ld))
    print("   simulateur : conserve")
    if poser:
        open(os.path.join(SAUV, "avant-%d.html" % ARTICLE), "w",
             encoding="utf-8").write(depart)
        w.update_content("posts", ARTICLE, c, live=True)
        print("\n   pose")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
