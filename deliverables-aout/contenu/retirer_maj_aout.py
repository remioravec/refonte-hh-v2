#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retire la section posee entre l'equipe et la FAQ.

Elle n'existe que sur la page brasseur : « ERP brasseur : brassins,
consignes et tracabilite des matieres », quatre cartes, 1223 px de haut.
Son propos recoupe desormais celui de la section fonctionnalites, qui dit
la meme chose avec les ecrans a l'appui.

Ce qu'elle emporte est liste avant l'ecriture : un H2, quatre H3 et ses
liens. Le script dit lesquels de ces liens subsistent ailleurs sur la page
et lesquels disparaissent vraiment — c'est la seule chose qui ne se
rattrape pas toute seule.

Usage :  python3 retirer_maj_aout.py            (blanc)
         python3 retirer_maj_aout.py --poser    (ecrit)
"""

import os
import re
import sys
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w          # noqa: E402
import scroll_sticky as SY     # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "maj-aout-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}
CIBLE = "hh-maj-aout-brasseur"


def FRAIS():
    import random
    return "?hh=%d" % random.randrange(10 ** 9)


def lire_page(url):
    import time
    for essai in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(
                "https://www.helloharel.com" + url + FRAIS(),
                headers={"User-Agent": "Mozilla/5.0"}),
                timeout=90).read().decode("utf-8", "replace")
            if "</html>" in h:
                return h
        except Exception:
            pass
        time.sleep(2 * (essai + 1))
    raise SystemExit("ARRET — page %s illisible en entier" % url)


def solde(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", lambda m: " " * len(m.group(0)), t, flags=re.S)
    return len(re.findall(r"<div\b", t)) - len(re.findall(r"</div>", t))


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        i = c.find('<section class="%s"' % CIBLE)
        if i < 0:
            print("%-42s rien entre l'equipe et la FAQ" % url)
            continue
        j = c.find("</section>", i) + len("</section>")
        sec = c[i:j]
        if "<section" in sec[10:]:
            raise SystemExit("ARRET — section imbriquee sur %s" % url)

        # la section doit bien se trouver entre l'equipe et la FAQ
        te = c.find('<section class="team-section"')
        fa = c.find('<section class="faq-section"')
        if not (te < i < fa):
            raise SystemExit("ARRET — la section n'est pas entre l'equipe et la FAQ sur %s" % url)

        neuf = c[:i] + c[j:]
        if solde(neuf) != solde(c):
            raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)

        sans_code = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        liens = re.findall(r'href="([^"]+)"', sans_code(sec))
        restants = re.findall(r'href="([^"]+)"', sans_code(neuf))
        perdus = [x for x in dict.fromkeys(liens) if x not in restants]
        gardes = [x for x in dict.fromkeys(liens) if x in restants]
        titres = re.findall(r"<h([23])[^>]*>(.*?)</h\1>", sans_code(sec), re.S)

        print("%-42s -%d ko · %d titre(s) retire(s) · %d section(s) restantes"
              % (url, len(sec) // 1024, len(titres), neuf.count("<section class=")))
        for n, t in titres:
            print("      H%s  %s" % (n, re.sub(r"<[^>]+>", "", t).strip()[:62]))
        print("      liens conserves ailleurs : %s" % (", ".join(gardes) or "aucun"))
        print("      LIENS PERDUS             : %s" % (", ".join(perdus) or "aucun"))

        if not poser:
            continue
        open(os.path.join(SAUV, "avant-%d.html" % page), "w", encoding="utf-8").write(c)
        w.update_content("pages", page, neuf, live=True)
        print("   pose")

    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")
        return
    print("\n--- verification en ligne ---")
    import time
    time.sleep(6)
    for cle, (page, url) in SY.PAGES.items():
        h = lire_page(url)
        reste = h.count('<section class="%s"' % CIBLE)
        sect = h.count("<section class=")
        ok = reste == 0 and sect >= 8
        print("   %-42s %s  %d sections · section visee %s"
              % (url, "OK " if ok else "KO ", sect,
                 "absente" if reste == 0 else "PRESENTE"))


if __name__ == "__main__":
    main()
