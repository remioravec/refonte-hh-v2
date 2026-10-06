#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose la section fonctionnalites en defilement colle sur les trois pages.

Torrefacteur (10935), brasseur (10896), chocolatier (10894). Aucune n'est
protegee par la regle 0 — le script refuse de demarrer si l'une d'elles y
figurait.

Le markup vient de scroll_sticky.section(), nourri par le module a onglets
deja en place sur chaque page : titres, chapos, puces, liens de maillage et
ecrans sont repris tels quels. Seule la mise en scene change.

Ce qu'on ne touche pas : la feuille de style d'agro_ui, qui vit AVANT la
section et que le nouveau module continue d'utiliser via la classe .hhf.

Usage :  python3 poser_sticky.py            (blanc)
         python3 poser_sticky.py --poser    (ecrit)
"""

import os
import re
import sys
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w         # noqa: E402
import scroll_sticky as SY    # noqa: E402
import contenu_sticky as C    # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "sticky-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def FRAIS():
    """Une URL unique par controle : le cache du site sert sinon la
    version d'avant la pose, et le controle annonce un echec faux."""
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


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]

        # La feuille et le script du module vivent AVANT et APRES la section.
        # Remplacer la seule section les laisserait en place : une regle
        # supprimee d'une version a l'autre continuerait de s'appliquer depuis
        # l'ancienne feuille, et l'ancien script tournerait en meme temps que
        # le neuf. On les retire donc tous, avant de poser la version du jour.
        # Les premieres versions du script n'avaient pas d'identifiant : on
        # les reconnait a ce qu'elles pilotent, pas a leur etiquette.
        avant = c
        for motif in (r'<style id="hh-scrollytelling">.*?</style>',
                      r'<script(?![^>]*\ssrc)[^>]*>(?:(?!</script>).)*?'
                      r'querySelectorAll\("\.sy-ecrans'
                      r'(?:(?!</script>).)*?</script>'):
            c = re.sub(motif, "", c, flags=re.S)
        vieux = len(re.findall(r'<style id="hh-scrollytelling">', avant)) \
            + len(re.findall(r'querySelectorAll\("\.sy-ecrans', avant))

        i = c.find('<section class="features-section"')
        j = c.find("</section>", i) + len("</section>")
        if i < 0 or j <= i:
            raise SystemExit("ARRET — section introuvable sur %s" % url)
        if "<section" in c[i + 10:j]:
            raise SystemExit("ARRET — section imbriquee sur %s" % url)
        if 'class="sy-ecrans"' in c:
            entete, ecrans, liens = SY.extraire_sticky(c)
        elif 'class="hhf-bar"' in c[i:j]:
            entete, blocs = SY.extraire(c)
            ecrans = [b[2] for b in blocs]
            liens = [m for b in blocs
                     for m in re.findall(r'(<a class="hhf-lien".*?</a>)', b[1], re.S)]
        else:
            raise SystemExit("ARRET — %s ne porte aucun module connu" % url)

        neuf = c[:i] + SY.section(entete, ecrans, liens, C.CONTENU[cle]) + c[j:]

        # La feuille et le script du module vivent AVANT et APRES la section :
        # remplacer la seule section les laisserait en double, et une regle
        # supprimee d'une version a l'autre continuerait de s'appliquer depuis
        # l'ancienne feuille. On retire donc les anciens exemplaires, en
        # gardant le dernier — celui qu'on vient de poser.

        # Les seuls liens autorises a disparaitre sont ceux de la section
        # elle-meme, retires a la demande le 22/09. Tout autre lien qui
        # manque arrete la pose : c'est le maillage du reste de la page.
        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        attendus = re.findall(r'href="([^"]+)"', " ".join(liens))
        av = re.findall(r'href="([^"]+)"', corps(c))
        ap = re.findall(r'href="([^"]+)"', corps(neuf))
        reste = list(av)
        for x in attendus:
            if x in reste:
                reste.remove(x)
        if sorted(reste) != sorted(ap):
            perdus = [x for x in reste if reste.count(x) > ap.count(x)]
            raise SystemExit("ARRET — lien(s) perdu(s) hors section sur %s : %s"
                             % (url, sorted(set(perdus))[:4]))
        # Les ecrans non plus. Le module les porte DEUX fois : une dans la
        # colonne collee de l'ordinateur, une sous chaque texte pour le
        # telephone, ou le titre doit arriver avant son tableau de bord. Un
        # seul des deux jeux s'affiche a la fois.
        ap_ui = corps(neuf).count('class="ui"')
        if ap_ui != len(ecrans):
            raise SystemExit("ARRET — %d etapes extraites, %d ecrans en sortie "
                             "(attendu %d) sur %s"
                             % (len(ecrans), ap_ui, len(ecrans), url))

        for motif, quoi in ((r'<style id="hh-scrollytelling">', "feuille"),
                            (r'querySelectorAll\("\.sy-ecrans', "script")):
            n = len(re.findall(motif, neuf))
            if n != 1:
                raise SystemExit("ARRET — %d %s(s) du module sur %s" % (n, quoi, url))

        avis = neuf.count('class="sy-avis"')
        print("%-42s %d etapes · %d lien(s) de section retire(s) · %d liens "
              "restants · %d avis · %+d ko"
              % (url, len(ecrans), len(attendus), len(ap), avis,
                 (len(neuf) - len(avant)) // 1024))

        if not poser:
            continue
        open(os.path.join(SAUV, "avant-%d.html" % page), "w", encoding="utf-8").write(avant)
        w.update_content("pages", page, neuf, live=True)
        print("   pose (sauvegarde : sticky-avant/avant-%d.html)" % page)

    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")
        return

    print("\n--- verification en ligne ---")
    import time
    time.sleep(6)
    # Le script SERVI, et non celui qu'on croit avoir pose. WordPress reecrit
    # le contenu a l'enregistrement : il a transforme les « et » commerciaux
    # du script en entites HTML, ce qui l'a rendu inexecutable sur les trois
    # pages — bureau compris — sans qu'aucun controle ne s'en apercoive. Tous
    # portaient sur un apercu construit localement, qui ne passe jamais par
    # WordPress. Desormais on compare octet pour octet ce que le site sert.
    attendu = re.sub(r"^<script[^>]*>|</script>$", "", SY.JS.strip())
    for cle, (page, url) in SY.PAGES.items():
        h = lire_page(url)
        # Le rendu lache au-dela d'environ 280 ko de contenu : le site sert
        # alors un document complet, en-tete et pied compris, mais vide de
        # ses sections. Constate le 22/09 en ajoutant 18 ko. On compte donc
        # les sections servies, pas seulement la notre.
        sect = h.count('<section class=')
        pas = h.count('class="sy-pas"')
        ecr = len(re.findall(r'<li data-actif="[01]" aria-hidden=', h))
        onglets = h.count('class="hhf-bar"')
        hhf = 'class="sy hhf"' in h
        m = re.search(r'<script id="hh-scrollytelling-js">(.*?)</script>', h, re.S)
        servi = m.group(1) if m else ""
        intact = bool(m) and servi == attendu
        detail = "intact"
        if not m:
            detail = "ABSENT"
        elif not intact:
            detail = "ABIME"
            for e in ("&#038;", "&#8217;", "&#8221;", "&#8211;", "&gt;", "&lt;", "&amp;"):
                if e in servi:
                    detail = "ABIME (%s dedans)" % e
                    break
            else:
                detail = "ABIME (%d octets servis, %d attendus)" % (len(servi), len(attendu))
        ok = (pas == 1 and ecr >= 5 and onglets == 0 and hhf and intact
              and sect >= 8)
        print("   %-42s %s  %d sections servies · %d pas · %d ecrans · "
              ".hhf %s · script %s"
              % (url, "OK " if ok else "KO ", sect, pas, ecr,
                 "oui" if hhf else "NON", detail))


if __name__ == "__main__":
    main()
