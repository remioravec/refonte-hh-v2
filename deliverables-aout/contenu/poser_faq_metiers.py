#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose les reponses de FAQ reecrites sur les cinq pages concernees.

Les QUESTIONS ne bougent pas : elles etaient deja celles du metier, c'est
l'interieur qui parlait d'autre chose. Seules les reponses sont remplacees,
une a une, appariees par leur question.

Le controle refuse d'ecrire si :
  · une question a change ou manque a l'appel ;
  · un mot d'un autre metier survit dans la section ;
  · un lien disparait ailleurs que dans les anciennes reponses ;
  · le solde des <div> bouge, ou une section disparait.

Usage :  python3 poser_faq_metiers.py            (blanc)
         python3 poser_faq_metiers.py --poser    (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import faq_metiers as FM         # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/faqmetiers-avant")


def txt(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    pb = FM.controler()
    if pb:
        raise SystemExit("ARRET — le contenu ne passe pas son propre controle : %s" % pb[:2])

    for pid, (nom, reponses) in FM.PAGES.items():
        c = w.get_raw("pages", pid)["content"]["raw"]
        depart = c
        i = c.find('<section class="faq-section"')
        j = c.find("</section>", i) + len("</section>")
        sec = c[i:j]
        attendues = {q: r for q, r in reponses}

        blocs = list(re.finditer(
            r'(<details[^>]*><summary[^>]*>)(.*?)(</summary><div class="fa2-r"[^>]*>)'
            r'(.*?)(</div></details>)', sec, re.S))
        if len(blocs) != len(reponses):
            raise SystemExit("ARRET — %d accordeons pour %d reponses sur %s"
                             % (len(blocs), len(reponses), nom))

        neuve, remplacees, anciens_liens = sec, 0, []
        for m in blocs[::-1]:
            q = txt(m.group(2))
            if q not in attendues:
                raise SystemExit("ARRET — question inconnue sur %s : « %s »" % (nom, q[:60]))
            anciens_liens += re.findall(r'href="([^"]+)"', m.group(4))
            interieur = '<div itemprop="text">%s</div>' % attendues[q] \
                if 'itemprop="text"' in m.group(4) else attendues[q]
            neuve = neuve[:m.start()] + m.group(1) + m.group(2) + m.group(3) \
                + interieur + m.group(5) + neuve[m.end():]
            remplacees += 1

        # aucun mot d'un autre metier ne doit survivre dans la section
        plat = FM.sans_accent(txt(neuve))
        restants = [x for x in FM.INTRUS[nom] if FM.sans_accent(x) in plat]
        if restants:
            raise SystemExit("ARRET — %s survit dans la section de %s" % (restants, nom))

        neuf = c[:i] + neuve + c[j:]
        if D.solde(neuf) != D.solde(depart):
            raise SystemExit("ARRET — le solde des <div> bouge sur %s" % nom)
        if neuf.count("<section class=") != depart.count("<section class="):
            raise SystemExit("ARRET — une section a bouge sur %s" % nom)
        if neuf.count("<details") != depart.count("<details"):
            raise SystemExit("ARRET — un accordeon a disparu sur %s" % nom)
        # Les liens des anciennes reponses ont le droit de partir, ceux des
        # nouvelles d'arriver. Tout le reste doit se retrouver a l'identique,
        # multiplicite comprise — un simple ensemble ne le verrait pas.
        import collections
        nouveaux_liens = []
        for q, r in reponses:
            nouveaux_liens += re.findall(r'href="([^"]+)"', r)
        attendu = collections.Counter(D.liens(depart))
        attendu.subtract(collections.Counter(anciens_liens))
        attendu.update(collections.Counter(nouveaux_liens))
        obtenu = collections.Counter(D.liens(neuf))
        if attendu != obtenu:
            ecart = (attendu - obtenu) or (obtenu - attendu)
            raise SystemExit("ARRET — le maillage bouge autrement que prevu sur %s : %s"
                             % (nom, ecart.most_common(3)))
        perdus = sorted({x for x in anciens_liens if x not in D.liens(neuf)})

        print("%-14s %d reponses reecrites · %+d ko%s"
              % (nom, remplacees, (len(neuf) - len(depart)) // 1024,
                 (" · lien(s) des anciennes reponses : " + ", ".join(perdus))
                 if perdus else ""))
        if poser:
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(depart)
            w.update_content("pages", pid, neuf, live=True)
            print("%-14s   pose" % "")
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
