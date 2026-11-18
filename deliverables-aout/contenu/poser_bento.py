#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose du module a onglets a la place du bento, sur les pages fonctionnalites
et les fiches metier.

TRENTE ET UNE PAGES visees, relevees le 17/09/2026 : seize fiches metier
agroalimentaires et quinze pages fonctionnalites. Le bento y est uniforme :
une section, cinq cartes, un titre et un texte par carte, souvent un lien de
maillage.

CE QUI EST REPRIS ET NON REECRIT — le titre, le texte et les puces de chaque
carte sortent de la page et reposent tels quels dans les onglets. On ne change
pas ce que la page dit.

LES LIENS DE MAILLAGE — comptes avant et apres. La conversion est refusee s'il
en manque un seul : les perdre couterait du maillage interne sur trente et une
pages.

REGLE 0 — quatre des fiches metier sont protegees : /agroalimentaire/,
charcutier, traiteur et plats-cuisines-industriels. Remplacer la section des
fonctionnalites est une modification de structure. Elles sont preparees et
controlees, mais PAS ecrites : il faut un feu vert explicite, comme pour le
champ telephone de /migration-as400/.

Usage :  python3 poser_bento.py                (essai a blanc)
         python3 poser_bento.py --live         (ecriture, hors pages protegees)
         python3 poser_bento.py --live --protegees   (y compris les protegees)
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402
import bento_toggles as B                   # noqa: E402

LIVE = "--live" in sys.argv
AVEC_PROTEGEES = "--protegees" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUVE = os.path.join(S, "bento-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def empreinte(c):
    return (c.count("<h1"), c.count("<header"), c.count("<section"),
            c.count('class="hero-section"'), c.count("</body>"))


def main():
    os.makedirs(SAUVE, exist_ok=True)
    inv = json.load(open(os.path.join(S, "inventaire-bento.json")))
    cibles = [x for x in inv if x["features_section"]]
    print("%d pages visees · mode %s%s\n"
          % (len(cibles), "ECRITURE" if LIVE else "essai a blanc",
             ", protegees incluses" if AVEC_PROTEGEES else ""))

    faits, refus, gardees = 0, [], []
    for x in cibles:
        pid, url = x["id"], x["url"]
        try:
            p = w.get_raw("pages", pid)
            c = p["content"]["raw"]
            el = (p.get("meta", {}).get("_elementor_data") or "").strip()
            if el not in ("", "[]", "[ ]", "null"):
                raise ValueError("contenu Elementor")
            av = empreinte(c)
            liens_av = len(set(re.findall(r'href="(/[^"]*)"', c)))
            n, ecrans = B.convertir(c)
            if empreinte(n) != av:
                raise ValueError("empreinte %s -> %s" % (av, empreinte(n)))
            liens_ap = len(set(re.findall(r'href="(/[^"]*)"', n)))
            if liens_ap < liens_av:
                raise ValueError("%d liens internes perdus" % (liens_av - liens_ap))
            if n.count('name="hhf-onglet"') < 4:
                raise ValueError("module a onglets incomplet")
            if "bento-card" in n[n.find('<section class="features-section"'):
                                 n.find("</section>", n.find('<section class="features-section"'))]:
                raise ValueError("le bento subsiste")
        except Exception as e:
            refus.append((pid, url, str(e)))
            continue

        if pid in PROTEGEES and not AVEC_PROTEGEES:
            gardees.append((pid, url, len(ecrans)))
            continue

        if LIVE:
            open("%s/%d.html" % (SAUVE, pid), "w", encoding="utf-8").write(c)
            w.api("pages/%d" % pid, "POST", {"content": n})
            c2 = w.get_raw("pages", pid)["content"]["raw"]
            if 'name="hhf-onglet"' not in c2 or empreinte(c2) != av:
                refus.append((pid, url, "RELECTURE : la pose n'est pas en base"))
                continue
        faits += 1
        print("   %-46s %d onglets · %s" % (url[:46], n.count('class="hhf-pick"'),
                                            ", ".join(ecrans)), flush=True)

    print("\n%s : %d pages" % ("posees" if LIVE else "pretes", faits))
    if gardees:
        print("\npages protegees, pretes mais NON ecrites (%d) :" % len(gardees))
        for i, u, _ in gardees:
            print("   . %-6s %s" % (i, u))
    if refus:
        print("\nrefus (%d) :" % len(refus))
        for i, u, e in refus:
            print("   ! %-6s %-44s %s" % (i, u[:44], e))


if __name__ == "__main__":
    main()
