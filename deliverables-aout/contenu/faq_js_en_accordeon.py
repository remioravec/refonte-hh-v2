#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les FAQ dont les reponses vivaient dans un tableau JavaScript passent en
accordeons dans le HTML.

Sur sept pages, les questions etaient des cartes cliquables et les reponses
un tableau `faqData` injecte dans un tiroir au clic. Deux consequences :
un moteur de recherche ne voyait AUCUNE reponse, et sur l'accueil un
fragment de ce code — « '+d.title+' » — se retrouvait rendu en H2 au milieu
de la page.

Les reponses sont donc sorties du script et ecrites dans la page, en
<details> natifs, comme sur les autres pages. Le texte n'est pas retouche :
il est deplace.

Le tableau est lu par node, qui sait evaluer un litteral JavaScript la ou
une expression reguliere se tromperait sur les apostrophes.

Usage :  python3 faq_js_en_accordeon.py            (blanc)
         python3 faq_js_en_accordeon.py --poser    (ecrit)
"""

import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import faq_accordeon as FA       # noqa: E402
import remanier_agro as RA       # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "faqjs-avant")
CIBLES = [(2, "/"), (4728, "/fonctionnalites/"),
          (7905, "/fonctionnalites/facturation-automatique-bon-livraison/"),
          (7912, "/fonctionnalites/gestion-consigne-bouteille-logiciel/"),
          (7909, "/fonctionnalites/gestion-rendement-matiere-logiciel/"),
          (7911, "/fonctionnalites/logiciel-devis-commande-bon-livraison/"),
          (7910, "/fonctionnalites/planification-production-erp/")]


def lire_faqdata(c):
    m = re.search(r"var faqData\s*=\s*(\[.*?\]);", c, re.S)
    if not m:
        raise SystemExit("ARRET — faqData introuvable")
    f = os.path.join(S, "faqdata.js")
    open(f, "w", encoding="utf-8").write(
        "const faqData = %s;\nprocess.stdout.write(JSON.stringify(faqData));" % m.group(1))
    r = subprocess.run(["node", f], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ARRET — node ne lit pas faqData : %s" % r.stderr.strip()[:120])
    return m.start(), m.end(), json.loads(r.stdout)


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for pid, url in CIBLES:
        c = w.get_raw("pages", pid)["content"]["raw"]
        depart = c
        a, b, data = lire_faqdata(c)
        paires = []
        for d in data:
            t = re.sub(r"<[^>]+>", "", d.get("title", "")).strip()
            h = d.get("html", "").strip()
            if not t or not h:
                raise SystemExit("ARRET — entree incomplete sur %s" % url)
            paires.append((t, h))

        # l'en-tete de la section reste, la grille de cartes s'en va
        i = c.find('<section class="faq-section"')
        j = c.find("</section>", i) + len("</section>")
        sec = c[i:j]
        ent = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="faq-cards-grid")',
                        sec, re.S)
        if not ent:
            raise SystemExit("ARRET — en-tete de FAQ introuvable sur %s" % url)
        pied = re.search(r'<div class="faq-drawer-footer">\s*(<a\b.*?</a>)', c, re.S)
        neuve = FA.section(ent.group(0), paires, pied.group(1) if pied else "")
        neuve = re.sub(r'\sitem(?:scope|prop|type)(?:="[^"]*")?', "", neuve)
        neuve = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*?'
                       r'FAQPage(?:(?!</script>).)*?</script>', "", neuve, flags=re.S)
        neuve = neuve.replace("<details open ", "<details ").replace("<details open>", "<details>")
        c = c[:i] + neuve + c[j:]

        # Le tiroir et son script n'ont plus d'objet. On le retire par
        # comptage de balises et non par expression reguliere : un .*? sur
        # du HTML imbrique coupe au premier </div> venu et desequilibre la
        # page — constate ici avec un solde a -3.
        for ident in ('id="faqOverlay"', 'id="faqDrawer"'):
            k = c.find(ident)
            while k >= 0:
                d = c.rfind("<div", 0, k)
                if d < 0:
                    break
                fin = RA.div_complet(c, d)
                bloc = c[d:fin]
                if D.solde(bloc) != 0:
                    raise SystemExit("ARRET — bloc de tiroir non clos sur %s" % url)
                c = c[:d] + c[fin:]
                k = c.find(ident)
        for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S))[::-1]:
            if "faqData" in m.group(1) or "openFaqDrawer" in m.group(1):
                c = c[:m.start()] + c[m.end():]

        corps = D.sans_code(c)
        for x in ("faq-card", "openFaqDrawer", "faqDrawerContent", "'+d.title+'"):
            if x in corps:
                raise SystemExit("ARRET — %r survit dans le corps sur %s" % (x, url))
        if D.solde(c) != D.solde(depart):
            raise SystemExit("ARRET — le solde des <div> bouge sur %s (%+d -> %+d)"
                             % (url, D.solde(depart), D.solde(c)))
        if c.count("<details") != len(paires):
            raise SystemExit("ARRET — %d accordeons pour %d reponses sur %s"
                             % (c.count("<details"), len(paires), url))
        # le texte des reponses entre dans la page : des liens y apparaissent
        nouveaux = [x for x in D.liens(c) if x not in D.liens(depart)]
        perdus = [x for x in D.liens(depart) if x not in D.liens(c)]
        if perdus:
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s : %s" % (url, perdus[:3]))
        if len(c) > 275_000:
            raise SystemExit("ARRET — %d ko sur %s" % (len(c) // 1024, url))

        print("%-52s %3d -> %3d ko · %2d reponses sorties du script%s"
              % (url[:52], len(depart) // 1024, len(c) // 1024, len(paires),
                 (" · %d lien(s) rendus visibles" % len(set(nouveaux))) if nouveaux else ""))
        if poser:
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(depart)
            w.update_content("pages", pid, c, live=True)
            print("%-52s   pose" % "")
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
