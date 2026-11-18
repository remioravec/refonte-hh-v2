#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trois pages rejoignent le gabarit : negoce, traiteur, plats cuisines.

La Regle 0 couvrait les deux dernieres ; elle a ete levee a la demande.
Restent protegees /agroalimentaire/charcutier/ et /migration-as400/.

Le travail se fait en deux temps, et l'ordre n'est pas negociable. Ce
script retire d'abord ce qui n'appartient pas au gabarit, puis le
deployeur transforme les sections restantes — il exige que leur nombre
ne bouge pas pendant son passage, donc il ne peut pas retirer lui-meme.

Ce qui part :
  hnb-section     sur /negoce/, treize kilo-octets. Attention : c'est le
                  meilleur bloc de la page — une reponse en une phrase et
                  un tableau de delais de paiement sources sur le Code de
                  commerce. Il est sauvegarde entier, et son contenu
                  merite d'etre reloge plutot que perdu.
  hh-serp-boost   un pave de texte sans lien, sous le gabarit.
  container       le bloc « Pour approfondir ».

Ce qui reste intact : la FAQ, que le deployeur convertira de son tiroir
JavaScript en accordeons HTML — c'est ce qui repare au passage les
resumes casses des cartes, « L'ERP, peut-il, calculer ».

Usage :  python3 gabarit_trois.py           (blanc)
         python3 gabarit_trois.py --poser   (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import pilier_gabarit as P       # noqa: E402
import alleger_css as A          # noqa: E402
import nap_pied as NAP           # noqa: E402

PAGES = [(5957, "/negoce/", ("hnb-section", "hh-serp-boost", "container")),
         (2839, "/agroalimentaire/traiteur/", ("container",)),
         (5477, "/agroalimentaire/plats-cuisines-industriels/",
          ("hh-serp-boost", "container"))]
GABARIT = ["hero-section", "logos-section", "features-section",
           "about-card-section", "process-section", "metiers-section",
           "team-section", "faq-section", "reviews-section"]
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/trois-avant")


def traiter(pid, url, a_retirer, poser):
    d = w.get_raw("pages", pid)
    el = (d.get("meta") or {}).get("_elementor_data")
    if el not in (None, "", "[]"):
        raise SystemExit("ARRET — _elementor_data non vide sur %s" % url)
    c = d["content"]["raw"]
    depart = c
    notes = []
    sauves = {}

    for nom in a_retirer:
        n = 0
        while True:
            m = re.search(r'<section class="[^"]*\b%s\b[^"]*"' % re.escape(nom), c)
            if not m:
                break
            fin = P.bornes(c, m.start())
            if fin is None:
                raise SystemExit("ARRET — <section %s> non fermee" % nom)
            bloc = c[m.start():fin]
            if D.solde(bloc) != 0:
                raise SystemExit("ARRET — %s : %d <div> non clos"
                                 % (nom, D.solde(bloc)))
            sauves.setdefault(nom, []).append(bloc)
            c = c[:m.start()] + c[fin:]
            n += 1
        if n:
            notes.append("%s ×%d" % (nom, n))

    c = P.vider_les_orphelins(c, notes)
    c, nr, gr = A.alleger(c, mini=0)
    if nr:
        notes.append("%d regle(s) CSS morte(s), %d o" % (nr, gr))

    if 'class="hh-nap"' not in c:
        m = re.search(r'(<div class="footer-brand">.*?)(</div>\s*<div class="footer-col">)',
                      c, re.S)
        if not m:
            raise SystemExit("ARRET — pied introuvable, NAP non pose sur %s" % url)
        c = c[:m.end(1)] + NAP.BLOC + c[m.end(1):]
        if '<style id="hh-nap">' not in c:
            k = c.rfind("</footer>") + len("</footer>")
            c = c[:k] + NAP.CSS + c[k:]
        notes.append("NAP pose")

    # ── controles ────────────────────────────────────────────────────────
    ordre = [m.group(1).split()[0] for m in re.finditer(r'<section class="([^"]+)"', c)]
    manque = [x for x in GABARIT if x not in ordre]
    rang = [GABARIT.index(x) for x in ordre if x in GABARIT]
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    if manque:
        raise SystemExit("ARRET — section(s) du gabarit perdue(s) : %s" % manque)
    if rang != sorted(rang):
        raise SystemExit("ARRET — l'ordre du gabarit est rompu : %s" % ordre)
    hors = [x for x in ordre if x not in GABARIT and x != "cta-banner"]
    if hors:
        raise SystemExit("ARRET — section(s) hors gabarit restante(s) : %s" % hors)
    if c.count('onclick="openFaqDrawer') != depart.count('onclick="openFaqDrawer'):
        raise SystemExit("ARRET — la FAQ a bouge")
    if len(c) > D.PLAFOND:
        raise SystemExit("ARRET — %d o, au-dela du seuil de rendu" % len(c))
    perdus = sorted(set(D.liens(depart)) - set(D.liens(c)))
    attendus = set()
    for blocs in sauves.values():
        for b in blocs:
            attendus |= set(re.findall(r'href="([^"]+)"', b))
    if set(perdus) - attendus:
        raise SystemExit("ARRET — lien(s) perdu(s) en trop : %s"
                         % sorted(set(perdus) - attendus)[:3])

    print("%-46s %d -> %d o (%+d) · %d sections"
          % (url[:46], len(depart), len(c), len(c) - len(depart),
             c.count("<section class=")))
    print("   %s" % " · ".join(notes))
    if perdus:
        print("   liens partis : %s"
              % [x.replace("https://www.helloharel.com", "") for x in perdus])
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
             encoding="utf-8").write(depart)
        for nom, blocs in sauves.items():
            open(os.path.join(SAUV, "%d-%s.html" % (pid, nom)), "w",
                 encoding="utf-8").write("\n\n".join(blocs))
        w.update_content("pages", pid, c, live=True)
        print("   pose.")


def main():
    poser = "--poser" in sys.argv
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    for pid, url, a_retirer in PAGES:
        try:
            traiter(pid, url, a_retirer, poser)
        except SystemExit as e:
            print("%-46s %s" % (url[:46], e))
        print()
    if not poser:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
