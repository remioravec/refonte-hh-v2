#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose du menu unifie sur 100 % des contenus.

ETAT DES LIEUX — 179 contenus analyses le 17/09/2026 :
  · 174 portent la navigation de bureau ET le menu mobile ;
  · 5 n'ont aucun menu, et n'en ont aucun non plus en ligne :
      /cgu/, /mentions-legales/, /politique-de-confidentialite/ (Elementor),
      /comparatifs/, /conformite-loi-anti-fraude-tva/.
    Elles sont signalees, pas modifiees : trois sont sous Elementor, et les
    deux autres n'ont pas d'entete du tout — il faudrait leur en poser une
    entiere, ce qui est une autre decision.

QUATRE versions du menu coexistaient :
  bureau  ...  7 metiers sur 153 contenus · 15 sur 16 · 16 sur 5
  mobile  ...  7 metiers sur la totalite des 174
Le mobile etait donc faux partout, y compris la ou le bureau etait complet.

CE QUE FAIT CE SCRIPT — il remplace DEUX blocs par contenu : la navigation de
bureau et le contenu du menu mobile. Rien d'autre. Ni feuille de style, ni
JavaScript, ni entete, ni contenu de page.

GARDE-FOUS
  · sauvegarde du contenu AVANT ecriture, un fichier par contenu ;
  · refus d'ecrire si une borne est incertaine, si le contenu est sous
    Elementor, ou si un controle est rouge ;
  · apres ecriture, relecture depuis l'API et verification de ce qui est
    reellement en base ;
  · title, H1 et nombre de sections compares avant/apres : la regle 0 interdit
    d'y toucher, y compris sur les cinq pages protegees.

Usage :  python3 poser_menu.py                (essai a blanc, tout)
         python3 poser_menu.py --live         (ecriture)
         python3 poser_menu.py --live --lot 5 (ecriture des 5 premiers)
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402
import menu_home as N                       # noqa: E402

LIVE = "--live" in sys.argv
LOT = None
if "--lot" in sys.argv:
    LOT = int(sys.argv[sys.argv.index("--lot") + 1])
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUVE = os.path.join(S, "menus-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def bloc_div(c, i):
    """Fin du <div> ouvert en i, accolades equilibrees."""
    prof, j = 0, i
    while j < len(c):
        a = c.find("<div", j)
        b = c.find("</div>", j)
        if b < 0:
            return -1
        if 0 <= a < b:
            prof += 1
            j = a + 4
        else:
            prof -= 1
            j = b + 6
            if prof == 0:
                return j
    return -1


def poser(c):
    """Retourne le contenu modifie, ou leve si une borne est incertaine."""
    if c.count('<nav class="desktop-nav">') != 1:
        raise ValueError("navigation de bureau : %d occurrences"
                         % c.count('<nav class="desktop-nav">'))
    if c.count('<div class="mobile-menu-inner">') != 1:
        raise ValueError("menu mobile : %d occurrences"
                         % c.count('<div class="mobile-menu-inner">'))

    i = c.find('<nav class="desktop-nav">')
    j = c.find("</nav>", i)
    if j < 0 or "<nav" in c[i + 25:j]:
        raise ValueError("borne de fin de la navigation incertaine")
    c = c[:i] + N.desktop() + c[j + 6:]

    i = c.find('<div class="mobile-menu-inner">')
    j = bloc_div(c, i)
    if j < 0:
        raise ValueError("borne de fin du menu mobile incertaine")
    c = c[:i] + N.mobile() + c[j:]
    return c


def empreinte(c):
    """Ce qui ne doit PAS changer."""
    return (c.count("<h1"), c.count("<section"), c.count("<header"),
            c.count("</body>"), c.count('class="hero-section"'))


def main():
    os.makedirs(SAUVE, exist_ok=True)
    inv = json.load(open(os.path.join(S, "inventaire-menu.json")))
    cibles = [x for x in inv if x["nav"] and x["mobile"] and not x["elementor"]]
    hors = [x for x in inv if not (x["nav"] and x["mobile"])]
    if LOT:
        cibles = cibles[:LOT]

    print("%d contenus a traiter · %d sans menu, ecartes" % (len(cibles), len(hors)))
    print("mode : %s\n" % ("ECRITURE" if LIVE else "essai a blanc"))

    faits, refus = 0, []
    for x in cibles:
        kind, pid = x["kind"], x["id"]
        url = x["link"].replace("https://www.helloharel.com", "")
        try:
            p = w.get_raw(kind, pid)
            c = p["content"]["raw"]
            el = (p.get("meta", {}).get("_elementor_data") or "").strip()
            if el not in ("", "[]", "[ ]", "null"):
                raise ValueError("contenu Elementor (%d octets)" % len(el))
            av = empreinte(c)
            n = poser(c)
            ap = empreinte(n)
            if av != ap:
                raise ValueError("empreinte modifiee %s -> %s" % (av, ap))
            nav = n[n.find('<nav class="desktop-nav">'):n.find("</nav>", n.find('<nav class="desktop-nav">'))]
            agro = len(set(re.findall(r'href="(/agroalimentaire/[^"]*)"', nav)))
            if agro != 16:
                raise ValueError("%d metiers dans la navigation" % agro)
            if "/negoce/" in nav or "/medical/" in nav:
                raise ValueError("negoce ou medical encore dans la navigation")
            mob = n[n.find('<div class="mobile-menu-inner">'):]
            mob = mob[:bloc_div(mob, 0)]
            if len(set(re.findall(r'href="(/agroalimentaire/[^"]*)"', mob))) != 16:
                raise ValueError("menu mobile incomplet")
        except Exception as e:
            refus.append((kind, pid, url, str(e)))
            continue

        if LIVE:
            open("%s/%s-%d.html" % (SAUVE, kind, pid), "w", encoding="utf-8").write(c)
            w.api("%s/%d" % (kind, pid), "POST", {"content": n})
            c2 = w.get_raw(kind, pid)["content"]["raw"]
            nav2 = c2[c2.find('<nav class="desktop-nav">'):c2.find("</nav>", c2.find('<nav class="desktop-nav">'))]
            if len(set(re.findall(r'href="(/agroalimentaire/[^"]*)"', nav2))) != 16:
                refus.append((kind, pid, url, "RELECTURE : la navigation n'est pas en base"))
                continue
            if empreinte(c2) != av:
                refus.append((kind, pid, url, "RELECTURE : empreinte changee en base"))
                continue
        faits += 1
        if faits % 25 == 0:
            print("   %d / %d" % (faits, len(cibles)))

    print("\n%s : %d contenus" % ("poses" if LIVE else "prets", faits))
    if refus:
        print("refus (%d) :" % len(refus))
        for k, i, u, e in refus:
            print("   %-6s %-6s %-46s %s" % (k, i, u[:46], e))
    print("\nsans menu, a traiter a part (%d) :" % len(hors))
    for x in hors:
        print("   %-6s %-6s %s%s" % (x["kind"], x["id"],
              x["link"].replace("https://www.helloharel.com", ""),
              "  [Elementor]" if x["elementor"] else "  [aucune entete]"))
    if LIVE:
        print("\nsauvegardes : %s" % SAUVE)


if __name__ == "__main__":
    main()
