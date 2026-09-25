#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La page pilier /agroalimentaire/ rejoint le gabarit.

Elle portait dix-huit sections contre neuf ailleurs, et trois cent onze
kilo-octets — la plus lourde du site. On retire ce qui n'appartient pas
au gabarit, et rien d'autre. La FAQ n'est pas touchee : elle garde ses
huit reponses, son balisage et son composant. Elle sera rallongee
ensuite, dans la meme forme.

Ce qui part, et pourquoi :

  hh2-quiz           un questionnaire de vingt-quatre kilo-octets. Les
  hh2-roi            calculateurs et simulateurs ont ete retires de
                     toutes les pages metiers ; celle-ci en gardait deux.
  hh2-compare  ×2    le gabarit n'a pas de comparatif. Le second annonce
                     « un deploiement 5× plus rapide, un TCO 3× inferieur »
                     sans source — une promesse chiffree qu'on ne tient pas.
  hh2-cas-clients    quatre entreprises nommees, avec adresse, effectif,
                     chiffre d'affaires et resultats au dixieme de point.
                     Rien ne les sourcent. On ne laisse pas ca en ligne
                     sans verification.
  hh2-trust-section  des citations de presse qui doublent la bande de
                     logos posee juste au-dessus.
  hh-demo-cta        un appel a l'action au milieu de la page, quand le
                     gabarit en pose un a la fin.

Ce qui reste et qui n'est pas au gabarit : le bloc « Pour approfondir ».
Il tient en sept cent cinquante octets et porte deux liens internes vers
des pages que rien d'autre ne cite. Le retirer creerait deux orphelines.

Usage :  python3 pilier_gabarit.py           (blanc)
         python3 pilier_gabarit.py --poser   (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import alleger_css as A          # noqa: E402
import nap_pied as NAP           # noqa: E402

PID = 1726
URL = "/agroalimentaire/"
A_RETIRER = ("hh2-quiz", "hh2-roi", "hh2-compare", "hh2-cas-clients",
             "hh2-trust-section", "hh-demo-cta")
GABARIT = ["hero-section", "logos-section", "features-section",
           "about-card-section", "process-section", "metiers-section",
           "team-section", "hh2-faq-section", "reviews-section", "cta-banner"]
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/pilier-avant")


def bornes(c, i):
    """Une <section> de son ouverture a sa fermeture, imbrications comprises.

    Une expression paresseuse s'arrete au premier </section> venu. Les
    sections du site en contiennent — on a deja mange un </div> comme ca."""
    prof = 0
    for m in re.finditer(r"<(/?)section\b", c[i:]):
        prof += 1 if not m.group(1) else -1
        if prof == 0:
            return i + c[i:].find(">", m.end()) + 1
    return None



def sans_code(c):
    return re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", c, flags=re.S)


def vider_les_orphelins(c, notes):
    """Les feuilles et les scripts des sections retirees.

    Une section qui part laisse derriere elle sa feuille de style et son
    script, ranges ailleurs dans la page. Vingt-sept kilo-octets qui ne
    peignent plus rien et n'animent plus rien.

    La regle est mesuree, pas devinee : un bloc ne s'en va que si AUCUNE
    des classes ou des identifiants qu'il vise n'existe encore dans le
    balisage. La grande feuille commune vise des centaines de classes
    toujours presentes — elle ne bouge pas."""
    marquage = sans_code(c)
    partis = 0
    for m in list(re.finditer(r"<(style|script)([^>]*)>(.*?)</\1>", c, re.S))[::-1]:
        if "id=" in m.group(2) or "src=" in m.group(2) or "ld+json" in m.group(2):
            continue
        corps = m.group(3)
        # TOUTES les classes visees, pas seulement celles prefixees « hh- ».
        # La premiere version ne regardait que ce prefixe : une feuille de
        # quatre-vingt-dix-huit kilo-octets, dont deux classes seulement le
        # portaient, se retrouvait declaree morte en entier — le hero, la
        # FAQ et les cartes seraient partis avec elle.
        vises = set(re.findall(r"\.([a-zA-Z][\w-]+)", corps))
        vises |= set(re.findall(r"#([a-zA-Z][\w-]+)", corps)) - A.ENVELOPPES
        vises |= set(re.findall(r"getElementById\(['\"]([\w-]+)", corps))
        vises |= set(re.findall(r"querySelector(?:All)?\(['\"][.#]([\w-]+)", corps))
        if not vises:
            continue
        if any(re.search(r'(?:class="[^"]*\b%s\b|id="%s")' % (re.escape(v), re.escape(v)),
                         marquage) for v in vises):
            continue
        notes.append("%s orphelin %d o (%s)"
                     % (m.group(1), len(m.group(0)), ", ".join(sorted(vises)[:3])))
        c = c[:m.start()] + c[m.end():]
        partis += len(m.group(0))
    if partis:
        notes.append("%d o de code mort" % partis)
    return c


def main():
    poser = "--poser" in sys.argv
    d = w.get_raw("pages", PID)
    el = (d.get("meta") or {}).get("_elementor_data")
    if el not in (None, "", "[]"):
        raise SystemExit("ARRET — _elementor_data non vide")
    c = d["content"]["raw"]
    depart = c
    notes = []

    for nom in A_RETIRER:
        n = 0
        while True:
            # La classe peut etre accompagnee : <section class="hh2-compare
            # hh2-compare--alt">. On vise le mot, pas la chaine entiere.
            m = re.search(r'<section class="[^"]*\b%s\b[^"]*"' % re.escape(nom), c)
            if not m:
                break
            fin = bornes(c, m.start())
            if fin is None:
                raise SystemExit("ARRET — <section %s> non fermee" % nom)
            bloc = c[m.start():fin]
            if D.solde(bloc) != 0:
                raise SystemExit("ARRET — %s : %d <div> non clos"
                                 % (nom, D.solde(bloc)))
            c = c[:m.start()] + c[fin:]
            n += 1
        if n:
            notes.append("%s ×%d" % (nom, n))

    c = vider_les_orphelins(c, notes)

    # Le seul numero de telephone de la page vivait dans l'appel a l'action
    # qu'on vient de retirer. La Regle 0 avait aussi tenu cette page a
    # l'ecart du NAP pose sur soixante-neuf autres. Elle le recoit.
    if 'class="hh-nap"' not in c:
        m = re.search(r'(<div class="footer-brand">.*?)(</div>\s*<div class="footer-col">)',
                      c, re.S)
        if not m:
            raise SystemExit("ARRET — pied de page introuvable, NAP non pose")
        c = c[:m.end(1)] + NAP.BLOC + c[m.end(1):]
        if '<style id="hh-nap">' not in c:
            c = c[:c.rfind("</footer>") + len("</footer>")] + NAP.CSS \
                + c[c.rfind("</footer>") + len("</footer>"):]
        notes.append("NAP pose au pied (nom, adresse, telephone)")

    ordre = [m.group(1).split()[0] for m in re.finditer(r'<section class="([^"]+)"', c)]
    rang = [GABARIT.index(x) for x in ordre if x in GABARIT]

    # ── controles ────────────────────────────────────────────────────────
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    if [x for x in GABARIT if x not in ordre]:
        raise SystemExit("ARRET — section(s) du gabarit perdue(s) : %s"
                         % [x for x in GABARIT if x not in ordre])
    if rang != sorted(rang):
        raise SystemExit("ARRET — l'ordre du gabarit est rompu : %s" % ordre)
    # On compte les questions dans le balisage : « hh2-faq-item » apparait
    # aussi dans la feuille de style.
    nq = lambda t: len(re.findall(r'<div class="hh2-faq-item"', sans_code(t)))
    if nq(c) != nq(depart):
        raise SystemExit("ARRET — la FAQ a bouge (%d -> %d questions)"
                         % (nq(depart), nq(c)))
    if len(re.findall(r'"@type": ?"Question"', c)) \
            != len(re.findall(r'"@type": ?"Question"', depart)):
        raise SystemExit("ARRET — le balisage de la FAQ a bouge")
    if len(c) > D.PLAFOND:
        raise SystemExit("ARRET — %d o, au-dela du seuil de rendu" % len(c))
    partis = sorted(set(D.liens(depart)) - set(D.liens(c)))
    if "06 18 06 00 18" not in c or 'href="tel:' not in c:
        raise SystemExit("ARRET — la page n'a plus de telephone")

    print("%s  %d -> %d o (%+d)" % (URL, len(depart), len(c), len(c) - len(depart)))
    print("   retire : %s" % " · ".join(notes))
    print("   sections : %d -> %d  %s" % (depart.count("<section class="),
                                          c.count("<section class="), ordre))
    print("   FAQ : %d questions, intactes" % nq(c))
    print("   liens partis avec les sections retirees (%d) :" % len(partis))
    for x in partis:
        print("      %s" % x)
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % PID), "w",
             encoding="utf-8").write(depart)
        w.update_content("pages", PID, c, live=True)
        print("\n   pose.")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
