#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les cartes metier ne gardent que la photo, le nom et une fleche.

La description et la ligne « Gestion marée et criée → » partent : sur une
carte qui porte deja une photo parlante, elles ajoutent de la lecture sans
ajouter d'information. Reste le nom du metier et une fleche, qui dit que
ca se clique.

Effet de bord a connaitre : ces deux elements etaient DANS le lien. L'ancre
de chaque carte se reduit donc au nom du metier. C'est une ancre exacte et
contigue, ce que la regle 2 demande — mais c'est une modification du
maillage, pas seulement de la mise en page.

Usage :  python3 metiers_sobre.py            (blanc)
         python3 metiers_sobre.py --poser    (ecrit)
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
SAUV = os.path.join(S, "metiers-sobre-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def FRAIS():
    import random
    return "?hh=%d" % random.randrange(10 ** 9)


def lire_page(url):
    """La page servie, en entier.

    Le transfert est parfois coupe en route : on a deja lu 170 ko d'une page
    qui en fait 364, et le controle a annonce un echec qui n'existait pas.
    On redemande tant que la page ne se termine pas.
    """
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
    raise SystemExit("ARRET — page %s illisible en entier apres 4 essais" % url)


FLECHE = ('<svg class="mt-f" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" '
          'aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg>')

CSS = """<style id="hh-metiers-sobre">
#hh-page .metier-slide,.metier-slide{padding:0 !important;overflow:hidden !important;
 display:flex !important;flex-direction:column !important}
/* nom et fleche sur une seule ligne : la carte tient en deux regards */
#hh-page .metier-slide h3,.metier-slide h3{display:flex !important;
 align-items:center !important;justify-content:space-between !important;
 gap:.75rem !important;margin:0 !important;padding:.95rem 1.15rem 1.05rem !important;
 font-size:1.08rem !important;line-height:1.3 !important}
#hh-page .mt-f,.mt-f{width:19px;height:19px;flex:0 0 19px;color:#0369A1;
 transition:transform .22s ease}
#hh-page .metier-slide:hover .mt-f,.metier-slide:hover .mt-f{
 transform:translateX(3px) !important}
@media (max-width:900px){
 #hh-page .metier-slide h3,.metier-slide h3{font-size:1.12rem !important;
  padding:1rem 1.15rem 1.1rem !important}}
@media (prefers-reduced-motion:reduce){
 #hh-page .mt-f,.mt-f{transition:none !important}
 #hh-page .metier-slide:hover .mt-f,.metier-slide:hover .mt-f{
  transform:none !important}}
</style>"""


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        i = c.find('<section class="metiers-section"')
        if i < 0:
            raise SystemExit("ARRET — section metiers introuvable sur %s" % url)
        j = c.find("</section>", i) + len("</section>")
        sec = c[i:j]
        if 'class="mt-v"' not in sec:
            raise SystemExit("ARRET — %s ne porte pas encore les photos" % url)
        if 'class="mt-f"' in sec:
            raise SystemExit("ARRET — %s porte deja les cartes sobres" % url)

        cartes = re.findall(r'(<a href="[^"]+" class="metier-slide[^"]*">)(.*?)(</a>)', sec, re.S)
        if not cartes:
            raise SystemExit("ARRET — aucune carte metier sur %s" % url)

        neuve, noms, retires = sec, [], 0
        for ouvre, corps, ferme in cartes:
            nom = re.search(r"<h3>([^<]+)</h3>", corps)
            if not nom:
                raise SystemExit("ARRET — carte sans nom sur %s" % url)
            visuel = re.search(r'<span class="mt-v">.*?</span>', corps, re.S)
            if not visuel:
                raise SystemExit("ARRET — carte sans photo sur %s" % url)
            retires += len(re.findall(r"<p>", corps)) \
                + len(re.findall(r'class="discover-link"', corps))
            noms.append(nom.group(1).strip())
            sobre = (visuel.group(0)
                     + "<h3><span>%s</span>%s</h3>" % (nom.group(1).strip(), FLECHE))
            neuve = neuve.replace(ouvre + corps + ferme, ouvre + sobre + ferme, 1)

        neuve = CSS + neuve
        neuf = c[:i] + neuve + c[j:]

        # Les cartes, les photos et les destinations restent. Le contenu du
        # lien change — c'est demande — mais aucun lien ne disparait.
        if len(re.findall(r'class="metier-slide', neuve)) != len(cartes):
            raise SystemExit("ARRET — carte perdue sur %s" % url)
        if neuve.count('class="mt-v"') != len(cartes):
            raise SystemExit("ARRET — photo perdue sur %s" % url)
        if len(re.findall(r"<h3>", neuve)) != len(cartes):
            raise SystemExit("ARRET — titre perdu sur %s" % url)
        if "discover-link" in neuve:
            raise SystemExit("ARRET — une ligne « decouvrir » survit sur %s" % url)
        corps_seul = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        if sorted(re.findall(r'href="([^"]+)"', corps_seul(c))) != \
           sorted(re.findall(r'href="([^"]+)"', corps_seul(neuf))):
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s" % url)

        print("%-42s %d cartes · %d elements retires · %+d octets"
              % (url, len(cartes), retires, len(neuf) - len(c)))
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
        v = len(re.findall(r'<span class="mt-v">', h))
        f = len(re.findall(r'<svg class="mt-f"', h))
        d = h.count("discover-link")
        ok = v >= 8 and f >= 8 and d == 0
        print("   %-42s %s  %d photos · %d fleches · %d lignes « decouvrir » restantes"
              % (url, "OK " if ok else "KO ", v, f, d))


if __name__ == "__main__":
    main()
