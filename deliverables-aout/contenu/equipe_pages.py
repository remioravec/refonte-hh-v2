#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La section equipe des trois pages metier : carrousel de cartes, et fin des
douze personnes inventees.

Sur ces pages, la section affiche quinze cartes. Trois sont de vraies
personnes, avec leur photo, leur poste et leur LinkedIn. Les douze autres
sont floutees et portent des noms et des postes fabriques — « M. D.,
Developpeur Full-Stack », « S. L., Consultante ERP ». On ne presente pas
des gens qui n'existent pas.

Elles laissent la place a ce qui avait ete valide sur /agroalimentaire/ :
les trois vraies personnes dans un rail qui se fait glisser, et en dessous
une rangee de silhouettes neutres qui dit une quantite, sans nom ni poste
et marquee aria-hidden.

La phrase de pied passe de « une equipe de 15 personnes » a « plus d'une
vingtaine de membres » — le libelle retenu sur /agroalimentaire/.

Usage :  python3 equipe_pages.py            (blanc)
         python3 equipe_pages.py --poser    (ecrit)
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
import remanier_agro as RA     # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "equipe-avant")
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


def lire(sec):
    """Rend ([(photo, alt, prenom, poste, lien)], nb de cartes fabriquees)."""
    vrais, faux = [], 0
    for m in re.finditer(r'<div class="team-card[^"]*"[^>]*>', sec):
        bloc = sec[m.start():RA.div_complet(sec, m.start())]
        if "blur(" in bloc or "data:image/svg" in bloc:
            faux += 1
            continue
        img = re.search(r'src="([^"]+)"', bloc)
        alt = re.search(r'alt="([^"]*)"', bloc)
        nom = re.search(r"<h4>([^<]+)</h4>", bloc)
        pos = re.search(r"<p>([^<]+)</p>", bloc)
        lien = re.search(r'<a href="([^"]+)"', bloc)
        if not (img and nom and pos and lien):
            raise SystemExit("ARRET — carte reelle incomplete")
        vrais.append((img.group(1), alt.group(1) if alt else nom.group(1),
                      nom.group(1).strip(), pos.group(1).strip(), lien.group(1)))
    return vrais, faux


def section(entete, vrais):
    cartes = ""
    for photo, alt, prenom, poste, lien in vrais:
        cartes += ('<li><div class="eq-c">'
                   '<img src="%s" alt="%s" width="118" height="118" loading="lazy">'
                   '<b>%s</b><span>%s</span>'
                   '<a href="%s" target="_blank" rel="noopener">%sLinkedIn</a>'
                   '</div></li>' % (photo, alt, prenom, poste, lien, RA.LINKEDIN))
    av = "".join('<li><img src="%s" alt="" width="34" height="34" loading="lazy"></li>'
                 % RA.AVATAR for _ in range(RA.AVATARS))
    fl = ('<button class="eq-fl eq-fl--%s" type="button" aria-label="%s" data-eq="%s">'
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M%s"/></svg></button>')
    # Le script du rail : aucun « et » commercial, WordPress les transforme en
    # entites et le script cesse de s'executer. Lecon du 22/09.
    js = ('<script id="hh-equipe-js">'
          '(function(){var eq=document.querySelector(".eq");if(!eq)return;'
          'var r=eq.querySelector(".eq-rail");if(!r)return;'
          'var fl=Array.prototype.slice.call(eq.querySelectorAll(".eq-fl"));'
          'function etat(){'
          'eq.setAttribute("data-deborde",r.scrollWidth>r.clientWidth+4?"1":"0");'
          'var p=fl[0],n=fl[1];'
          'if(p)p.disabled=r.scrollLeft<=2;'
          'if(n)n.disabled=r.scrollLeft>=r.scrollWidth-r.clientWidth-2}'
          'fl.forEach(function(b){b.addEventListener("click",function(){'
          'var li=r.querySelector("li");var pas=li?li.offsetWidth:280;'
          'r.scrollBy({left:(+b.getAttribute("data-eq"))*(pas+20),behavior:"smooth"})})});'
          'r.addEventListener("scroll",etat);'
          'window.addEventListener("resize",etat);etat()})();'
          '</script>')
    return (RA.CSS_EQUIPE
            + '<section class="team-section"><div class="container">'
            + entete
            + '<div class="eq" data-deborde="0">'
            + fl % ("p", "Membre précédent", "-1", "15 19l-7-7 7-7")
            + '<ul class="eq-rail">%s</ul>' % cartes
            + fl % ("n", "Membre suivant", "1", "9 5l7 7-7 7")
            + '<div class="eq-plus"><ul class="eq-av" aria-hidden="true">%s</ul>' % av
            + '<p class="eq-txt">… et <b>plus d\'une vingtaine de membres</b> '
              'à votre service.</p></div>'
              '</div></div></section>' + js)


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        i = c.find('<section class="team-section"')
        if i < 0:
            raise SystemExit("ARRET — section equipe introuvable sur %s" % url)
        j = c.find("</section>", i) + len("</section>")
        sec = c[i:j]
        if 'class="eq-rail"' in sec:
            raise SystemExit("ARRET — %s porte deja le carrousel" % url)

        ent = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="team-grid")',
                        sec, re.S)
        if not ent:
            raise SystemExit("ARRET — en-tete de l'equipe introuvable sur %s" % url)
        vrais, faux = lire(sec)
        if len(vrais) != 3:
            raise SystemExit("ARRET — %d personne(s) reelle(s) sur %s" % (len(vrais), url))

        neuve = section(ent.group(0), vrais)
        neuf = c[:i] + neuve + c[j:]

        # Les trois LinkedIn doivent survivre ; ceux des cartes fabriquees
        # n'existent pas, il n'y a donc rien d'autre a perdre ici.
        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        av = sorted(re.findall(r'href="([^"]+)"', corps(c)))
        ap = sorted(re.findall(r'href="([^"]+)"', corps(neuf)))
        if av != ap:
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s : %s"
                             % (url, sorted(set(av) - set(ap))[:4]))
        for mot in ("blur(", "Développeur Full-Stack", "Consultante ERP",
                    "15 personnes"):
            if mot in neuve:
                raise SystemExit("ARRET — %r survit sur %s" % (mot, url))
        if neuve.count("eq-c") < 3:
            raise SystemExit("ARRET — carte reelle perdue sur %s" % url)

        print("%-42s 3 personnes en carrousel · %d cartes fabriquees retirees · %+d ko"
              % (url, faux, (len(neuf) - len(c)) // 1024))
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
    attendu = re.sub(r"^<script[^>]*>|</script>$", "",
                     re.search(r'<script id="hh-equipe-js">.*?</script>',
                               section("<div class=\"section-header\"></div>",
                                       [("a", "b", "c", "d", "e")] * 3), re.S).group(0))
    attendu = re.sub(r"^<script[^>]*>|</script>$", "", attendu)
    for cle, (page, url) in SY.PAGES.items():
        h = lire_page(url)
        m = re.search(r'<script id="hh-equipe-js">(.*?)</script>', h, re.S)
        intact = bool(m) and "&#" not in m.group(1)
        cartes = h.count('class="eq-c"')
        ok = cartes == 3 and "blur(1px)" not in h and intact
        print("   %-42s %s  %d cartes · floutees %s · script %s"
              % (url, "OK " if ok else "KO ", cartes,
                 "aucune" if "blur(1px)" not in h else "PRESENTES",
                 "intact" if intact else "ABIME"))


if __name__ == "__main__":
    main()
