#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les cinq pages de fonctionnalites specialisees recoivent les sections qui
leur manquent, et perdent la feuille de style de l'outil retire.

Ces pages — facturation automatique, consigne, rendement matiere,
devis-commande, planification — n'ont jamais eu a-propos, process, metiers,
equipe ni avis. Elles s'arretaient a : hero · logos · fonctionnalites · faq.

Les cinq sections manquantes sont copiees depuis une page soeur conforme.
Elles sont identiques d'une page a l'autre — meme presentation de
l'editeur, meme parcours en trois etapes, memes huit cartes metier, meme
equipe, memes avis Google. Rien n'y est propre a un metier, donc rien n'est
invente en les reprenant.

La feuille de l'outil interactif (.roi-block et ses voisines) est restee
apres le retrait de la section : elle part aussi.

Usage :  python3 completer_specialisees.py            (blanc)
         python3 completer_specialisees.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/completer-avant")
DONNEUSE = 4798          # /fonctionnalites/achat/ — conforme
CIBLES = [(7905, "/fonctionnalites/facturation-automatique-bon-livraison/"),
          (7912, "/fonctionnalites/gestion-consigne-bouteille-logiciel/"),
          (7909, "/fonctionnalites/gestion-rendement-matiere-logiciel/"),
          (7911, "/fonctionnalites/logiciel-devis-commande-bon-livraison/"),
          (7910, "/fonctionnalites/planification-production-erp/")]
AVANT_FAQ = ["about-card-section", "process-section", "metiers-section", "team-section"]
APRES_FAQ = ["reviews-section"]


def extraire(c, classe):
    i = c.find('<section class="%s"' % classe)
    if i < 0:
        raise SystemExit("ARRET — %s absente de la page donneuse" % classe)
    j = c.find("</section>", i) + len("</section>")
    if "<section" in c[i + 10:j]:
        raise SystemExit("ARRET — %s imbriquee chez la donneuse" % classe)
    return c[i:j]


def feuilles_outil(c):
    """Les <style> qui ne servent plus qu'a l'outil retire."""
    out = []
    for m in re.finditer(r"<style[^>]*>.*?</style>", c, re.S):
        t = m.group(0)
        if ".roi-block" in t or "roi-tool" in t or "midcta-banner" in t:
            # une feuille qui ne sert qu'a ca : plus aucune de ses classes
            # n'est employee dans le corps
            cls = set(re.findall(r"\.([a-z][a-z0-9-]{3,})", t))
            corps = D.sans_code(c)
            vivantes = [x for x in cls if 'class="' in corps and x in corps]
            if not vivantes:
                out.append((m.start(), m.end(), len(t)))
    return out


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    don = w.get_raw("pages", DONNEUSE)["content"]["raw"]
    morceaux = {x: extraire(don, x) for x in AVANT_FAQ + APRES_FAQ}
    print("donneuse : /fonctionnalites/achat/ — %s\n"
          % ", ".join("%s %d o" % (k.replace("-section", ""), len(v))
                      for k, v in morceaux.items()))

    for pid, url in CIBLES:
        c = w.get_raw("pages", pid)["content"]["raw"]
        depart = c
        ajoutees, ajout_liens = [], []

        i = c.find('<section class="faq-section"')
        if i < 0:
            raise SystemExit("ARRET — pas de FAQ sur %s" % url)
        bloc = ""
        for x in AVANT_FAQ:
            if ('<section class="%s"' % x) in c:
                continue
            bloc += morceaux[x]
            ajoutees.append(x.replace("-section", ""))
            ajout_liens += re.findall(r'href="([^"]+)"', D.sans_code(morceaux[x]))
        c = c[:i] + bloc + c[i:]

        j = c.find("</section>", c.find('<section class="faq-section"')) + len("</section>")
        bloc = ""
        for x in APRES_FAQ:
            if ('<section class="%s"' % x) in c:
                continue
            bloc += morceaux[x]
            ajoutees.append(x.replace("-section", ""))
            ajout_liens += re.findall(r'href="([^"]+)"', D.sans_code(morceaux[x]))
        c = c[:j] + bloc + c[j:]

        # la feuille de l'outil retire
        retire = 0
        for a, b, n in feuilles_outil(c)[::-1]:
            c = c[:a] + c[b:]
            retire += n

        if D.solde(c) != D.solde(depart):
            raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
        attendu = sorted(D.liens(depart) + ajout_liens)
        if attendu != D.liens(c):
            manque = sorted(set(attendu) - set(D.liens(c)))
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s : %s" % (url, manque[:3]))
        ordre = [m.group(1).split()[0] for m in re.finditer(r'<section class="([^"]+)"', c)]
        ref = ["hero-section", "logos-section", "features-section", "about-card-section",
               "process-section", "metiers-section", "team-section", "faq-section",
               "reviews-section"]
        suite = [x for x in ordre if x in ref]
        if suite != ref:
            raise SystemExit("ARRET — ordre obtenu sur %s : %s" % (url, suite))
        if len(c) > 275_000:
            raise SystemExit("ARRET — %d ko, au-dela du seuil de rendu sur %s"
                             % (len(c) // 1024, url))

        print("%-52s %3d -> %3d ko · ajout : %s · feuille de l'outil : %d o"
              % (url[:52], len(depart) // 1024, len(c) // 1024,
                 ", ".join(ajoutees) or "rien", retire))
        if poser:
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(depart)
            w.update_content("pages", pid, c, live=True)
            print("%-52s   pose" % "")
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
