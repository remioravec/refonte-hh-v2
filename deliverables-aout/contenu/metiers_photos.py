#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les cartes metier passent de l'icone a la photo du metier.

Chaque carte recoit la photo du Hero de LA PAGE QU'ELLE OUVRE. C'est le
seul choix honnête : la carte montre ce que le visiteur va trouver en
cliquant, et l'image n'est pas choisie a part de sa destination.

Le carrousel n'est pas refait — il existe deja, avec son aimantation et ses
fleches. On agrandit seulement les cartes sur telephone pour que la photo
porte, et on pose l'image en tete de carte, au-dessus du nom du metier.

Usage :  python3 metiers_photos.py            (blanc)
         python3 metiers_photos.py --poser    (ecrit)
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
SAUV = os.path.join(S, "metiers-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def FRAIS():
    import random
    return "?hh=%d" % random.randrange(10 ** 9)


CSS = """<style id="hh-metiers-photos">
#hh-page .metier-slide,.metier-slide{padding:0 !important;overflow:hidden !important;
 display:flex !important;flex-direction:column !important}
#hh-page .mt-v,.mt-v{display:block !important;position:relative;width:100% !important;
 aspect-ratio:16/10;margin:0 !important;overflow:hidden !important;background:#E2E8F0}
#hh-page .mt-v img,.mt-v img{display:block !important;width:100% !important;
 height:100% !important;margin:0 !important;object-fit:cover !important;
 border-radius:0 !important;transition:transform .35s ease}
#hh-page .metier-slide:hover .mt-v img,.metier-slide:hover .mt-v img{
 transform:scale(1.04) !important}
/* un voile en bas de la photo : le nom qui suit s'y raccroche visuellement */
#hh-page .mt-v::after,.mt-v::after{content:"";position:absolute;inset:auto 0 0 0;
 height:38%;background:linear-gradient(transparent,rgba(15,23,42,.28))}
#hh-page .metier-slide h3,.metier-slide h3{margin:1rem 1.15rem .45rem !important}
#hh-page .metier-slide p,.metier-slide p{margin:0 1.15rem .9rem !important}
#hh-page .metier-slide .discover-link,.metier-slide .discover-link{
 margin:auto 1.15rem 1.15rem !important}
@media (max-width:900px){
 /* La photo est ce qu'on vient voir : la carte s'elargit pour la porter. */
 #hh-page .metiers-carousel>.metier-slide,.metiers-carousel>.metier-slide{
  flex:0 0 min(78vw,320px) !important;width:min(78vw,320px) !important}
 #hh-page .mt-v,.mt-v{aspect-ratio:3/2}
 #hh-page .metier-slide h3,.metier-slide h3{font-size:1.15rem !important}}
@media (prefers-reduced-motion:reduce){
 #hh-page .mt-v img,.mt-v img{transition:none !important}
 #hh-page .metier-slide:hover .mt-v img,.metier-slide:hover .mt-v img{
  transform:none !important}}
</style>"""


def hero_de(url, cache={}):
    """La photo du Hero de la page ciblee, ou None."""
    if url in cache:
        return cache[url]
    try:
        h = urllib.request.urlopen(urllib.request.Request(
            "https://www.helloharel.com" + url,
            headers={"User-Agent": "Mozilla/5.0"}), timeout=45).read().decode("utf-8", "replace")
    except Exception:
        cache[url] = None
        return None
    i = h.find('<section class="hero-section"')
    m = re.search(r"url\(['\"]?([^'\")]+)", h[i:h.find(">", i)]) if i >= 0 else None
    cache[url] = m.group(1) if m else None
    return cache[url]


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
        if 'class="mt-v"' in sec:
            raise SystemExit("ARRET — %s porte deja les photos" % url)

        cartes = re.findall(r'<a href="([^"]+)" class="metier-slide[^"]*">(.*?)</a>', sec, re.S)
        if not cartes:
            raise SystemExit("ARRET — aucune carte metier sur %s" % url)

        neuve, poses, sans = sec, 0, []
        for cible, corps in cartes:
            img = hero_de(cible)
            nom = re.search(r"<h3>([^<]+)</h3>", corps)
            nom = nom.group(1).strip() if nom else cible
            if not img:
                sans.append(nom)
                continue
            bloc = re.search(r'<div class="tilted-icon">.*?</div>\s*(?=<h3>)', corps, re.S)
            if not bloc:
                sans.append(nom + " (icone introuvable)")
                continue
            visuel = ('<span class="mt-v"><img src="%s" alt="" aria-hidden="true" '
                      'loading="lazy" decoding="async"></span>' % img)
            neuve = neuve.replace(corps, corps.replace(bloc.group(0), visuel), 1)
            poses += 1

        if poses < 6:
            raise SystemExit("ARRET — seulement %d photo(s) posee(s) sur %s" % (poses, url))
        neuve = CSS + neuve
        neuf = c[:i] + neuve + c[j:]

        # Ni carte ni lien ne doit disparaitre, et aucune icone ne doit rester.
        corps_seul = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        if len(re.findall(r'class="metier-slide', neuve)) != len(cartes):
            raise SystemExit("ARRET — %d cartes au lieu de %d sur %s"
                             % (len(re.findall(r'class="metier-slide', neuve)), len(cartes), url))
        if sorted(re.findall(r'href="([^"]+)"', corps_seul(c))) != \
           sorted(re.findall(r'href="([^"]+)"', corps_seul(neuf))):
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s" % url)
        if len(re.findall(r"<h3>", neuve)) != len(re.findall(r"<h3>", sec)):
            raise SystemExit("ARRET — un titre de carte a disparu sur %s" % url)
        if neuve.count('class="mt-v"') != poses:
            raise SystemExit("ARRET — %d visuels pour %d photos sur %s"
                             % (neuve.count('class="mt-v"'), poses, url))

        print("%-42s %d/%d cartes en photo%s · %+d octets"
              % (url, poses, len(cartes),
                 (" · sans photo : " + ", ".join(sans)) if sans else "",
                 len(neuf) - len(c)))
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
        h = urllib.request.urlopen(urllib.request.Request(
            "https://www.helloharel.com" + url + FRAIS(),
            headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")
        v = len(re.findall(r'<span class="mt-v">', h))
        ic = len(re.findall(r'<a href="[^"]+" class="metier-slide[^"]*">\s*'
                            r'<div class="tilted-icon">', h))
        ok = v >= 6 and ic == 0
        print("   %-42s %s  %d photos · %d icones restantes"
              % (url, "OK " if ok else "KO ", v, ic))


if __name__ == "__main__":
    main()
