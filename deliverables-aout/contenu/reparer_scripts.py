#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Huit pages fonctionnalites ont perdu leur script de comportement.

Le balisage est intact — le bouton du menu, les fleches du carrousel, les
sections a reveler sont tous la. C'est le script qui les anime qui a
disparu. Consequence, dans l'ordre de gravite :

  * « Qui sommes-nous » et « Succes guide par des experts » sont
    invisibles. La feuille de style pose .scroll-reveal a opacity 0 et
    attend qu'un observateur ajoute la classe .revealed. Sans le script,
    elle n'arrive jamais : seize elements restent transparents.
  * le bouton du menu mobile ne repond pas ;
  * les fleches du carrousel metiers ne repondent pas ;
  * l'en-tete ne prend jamais son etat « defile ».

Soixante-trois pages portent ce meme script, a deux lignes vides pres. On
repose exactement celui-la, au meme endroit : juste avant la section des
avis. On ne reecrit rien.

Verification : la page est rendue avant et apres, et on mesure l'opacite
reelle des elements. Un script pose qui ne revele pas serait un echec
silencieux.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

CIBLES = ("/fonctionnalites/achat/", "/fonctionnalites/crm/",
          "/fonctionnalites/fabrication/", "/fonctionnalites/facturation/",
          "/fonctionnalites/gestion-de-stock/", "/fonctionnalites/import-export/",
          "/fonctionnalites/logistique/", "/fonctionnalites/vente/")
DONNEUSE = "/agroalimentaire/industrie-laitiere/"   # une des 39 pages saines
ANCRE = '<section class="reviews-section">'
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/scripts-avant")
PLAFOND = 275_000

MESURE = r"""
from playwright.sync_api import sync_playwright
import json, sys
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.goto("file://" + sys.argv[1])
    pg.wait_for_timeout(1200)
    # L'observateur ne declenche que si l'element entre vraiment dans le
    # champ. Un saut jusqu'au bas de page ne suffit pas : on amene chaque
    # element au centre, un par un.
    o = {}
    for s in ("about-two-col", "timeline-step"):
        e = pg.query_selector_all("." + s)
        vals = []
        for x in e:
            x.evaluate("el=>el.scrollIntoView({block:'center'})")
            pg.wait_for_timeout(700)
            vals.append(x.evaluate("el=>getComputedStyle(el).opacity"))
        o[s] = vals
    print(json.dumps(o))
    pg.close(); b.close()
"""


def script_canonique():
    pid = dict((u, p) for p, u in D.cibles())[DONNEUSE]
    c = w.get_raw("pages", pid)["content"]["raw"]
    for m in re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S):
        if "revealed" in m.group(1) and "hamburgerBtn" in m.group(1):
            s = m.group(0)
            if "&" in s:
                raise SystemExit("ARRET — le script contient une esperluette ; "
                                 "WordPress la transformerait en entite")
            return s
    raise SystemExit("ARRET — script introuvable sur la page donneuse")


def servie(url):
    for essai in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(
                "https://www.helloharel.com" + url + "?v=%d" % time.time(),
                headers={"User-Agent": "Mozilla/5.0"}), timeout=120
            ).read().decode("utf-8", "replace")
            if "</html>" in h:
                return h
        except Exception:                      # noqa: BLE001
            pass
        time.sleep(2 * (essai + 1))
    return None


def opacites(url):
    """Ce que le navigateur affiche vraiment."""
    h = servie(url)
    if h is None:
        return None
    f = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                    encoding="utf-8")
    f.write(h)
    f.close()
    g = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                    encoding="utf-8")
    g.write(MESURE)
    g.close()
    r = subprocess.run([sys.executable, g.name, f.name],
                       capture_output=True, text=True, timeout=180)
    os.unlink(f.name)
    os.unlink(g.name)
    if r.returncode != 0:
        return None
    # La sortie peut porter un avertissement du navigateur avant le resultat.
    for ligne in reversed(r.stdout.strip().splitlines()):
        try:
            d = json.loads(ligne)
        except ValueError:
            continue
        if isinstance(d, dict):
            return d
    return None


def visible(o):
    if not o:
        return None
    tout = o.get("about-two-col", []) + o.get("timeline-step", [])
    return tout and all(float(x) > 0.9 for x in tout)


def main():
    poser = "--poser" in sys.argv
    cib = dict((u, p) for p, u in D.cibles())
    sc = script_canonique()
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)")
    print("script canonique : %d o, present sur 63 pages\n" % len(sc))

    for url in CIBLES:
        pid = cib[url]
        c = w.get_raw("pages", pid)["content"]["raw"]
        depart = c

        # « revealed » apparait aussi dans la feuille de style : on cherche
        # le script, pas le mot.
        if any("revealed" in m.group(1) for m in re.finditer(
                r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S)):
            print("%-42s le script est deja la — rien a faire" % url[:42])
            continue
        i = c.find(ANCRE)
        if i < 0:
            print("%-42s ancre introuvable — a revoir a la main" % url[:42])
            continue
        c = c[:i] + sc + " " + c[i:]

        if D.solde(c) != D.solde(depart):
            raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
        perdus = [x for x in D.liens(depart) if x not in D.liens(c)]
        if perdus:
            raise SystemExit("ARRET — lien(s) perdu(s) : %s" % perdus[:3])
        # On compte dans le balisage seul : le script pose contient lui-meme
        # les mots « scroll-reveal » et « metiersCarousel ».
        av, ap = D.sans_code(depart), D.sans_code(c)
        for motif in (r'<section class="[^"]+"', r"<details", r'id="hamburgerBtn"',
                      r'id="metiersCarousel"', r"scroll-reveal"):
            if len(re.findall(motif, ap)) != len(re.findall(motif, av)):
                raise SystemExit("ARRET — %s bouge sur %s" % (motif, url))
        if len(c) > PLAFOND:
            raise SystemExit("ARRET — %d o sur %s, au-dela du plafond"
                             % (len(c), url))

        avant = visible(opacites(url)) if poser else None
        print("%-42s %d -> %d o (+%d)%s"
              % (url[:42], len(depart), len(c), len(c) - len(depart),
                 "" if avant is None else
                 ("  · avant : %s" % ("visible" if avant else "INVISIBLE"))))

        if poser:
            os.makedirs(SAUV, exist_ok=True)
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(depart)
            w.update_content("pages", pid, c, live=True)
            time.sleep(3)
            apres = visible(opacites(url))
            if apres is None:
                print("   rendu illisible — a verifier a la main")
            elif apres:
                print("   apres : les sections s'affichent")
            else:
                print("   ALERTE — toujours invisible apres la pose")
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
