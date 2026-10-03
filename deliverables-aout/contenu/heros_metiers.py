#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Photos de hero des pages metier — une scene de metier par page.

Constat du 05/09/2026 : cinq pages partageaient la meme photo (boulanger,
brasseur, chocolatier, patissier, torrefacteur), trois en partageaient une autre,
et deux autres encore une troisieme. Un torrefacteur voyait donc la meme image
qu'un brasseur. C'est ce que le client resume par « le client ne se reconnait
pas ».

Chaque page recoit desormais une scene de son metier, dans le registre demande :
un professionnel au travail, ou un marche de gros.

Regle 0 : les cinq pages protegees ne sont pas touchees. La photo de
/agroalimentaire/ — deux professionnels sur une cagette de tomates — est
REUTILISEE sur /agroalimentaire/maraicher/, comme demande, sans que la page
protegee soit modifiee.

Usage :  python3 heros_metiers.py            (essai a blanc)
         python3 heros_metiers.py --live     (ecriture)
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import wp_common as w

LIVE = "--live" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
BASE = "https://www.helloharel.com/wp-content/uploads/2026/08/"

PROTEGEES = {1726, 2818, 2839, 5477, 11162}   # Regle 0 — jamais modifiees

# page, id, photo Pexels, nom de fichier, alternative textuelle
PLAN = [
 (2824,  "/agroalimentaire/maraicher/",           None,
  "Screenshot-2026-02-14-08.34.42",
  "Deux professionnels contrôlent une cagette de tomates dans un entrepôt de fruits et légumes"),
 (3309,  "/agroalimentaire/boulanger/",           7447289,
  "erp-boulanger-fournil-professionnel",
  "Boulanger sortant une plaque de pains devant les échelles d'un fournil"),
 (10865, "/agroalimentaire/patissier/",           5964573,
  "erp-patissier-laboratoire-poche",
  "Pâtissier garnissant des éclairs à la poche dans un laboratoire"),
 (10894, "/agroalimentaire/chocolatier/",         28146801,
  "erp-chocolatier-atelier-moulage",
  "Chocolatier pesant une garniture au-dessus d'un moule dans son atelier"),
 (10935, "/agroalimentaire/torrefacteur/",        4816504,
  "erp-torrefacteur-tambour-torrefaction",
  "Torréfacteur surveillant la cuisson devant son tambour de torréfaction"),
 (10896, "/agroalimentaire/brasseur/",            5532995,
  "erp-brasseur-cuves-fermentation",
  "Brasseur relevant ses paramètres devant les cuves de fermentation"),
 (10867, "/agroalimentaire/fromager/",            33313085,
  "erp-fromager-cave-affinage-meules",
  "Meules de fromage en cours d'affinage sur les planches d'une cave"),
 (5470,  "/agroalimentaire/industrie-laitiere/",  5953759,
  "erp-industrie-laitiere-atelier-fabrication",
  "Opératrice pesant des moules à fromage dans un atelier de fabrication laitière"),
 (10868, "/agroalimentaire/poissonnier/",         16435443,
  "erp-poissonnier-etal-maree-gros",
  "Étal de poissons entiers disposés sur glace sur un marché de gros"),
 (11332, "/agroalimentaire/viande/",              16276492,
  "erp-viande-atelier-decoupe",
  "Atelier de boucherie avec pièces suspendues et poste de découpe"),
 (10933, "/agroalimentaire/conserverie/",         10040011,
  "erp-conserverie-ligne-conditionnement",
  "Opératrices en tenue sur une ligne de conditionnement de bocaux"),
 (10934, "/agroalimentaire/negoce-alimentaire/",  16276469,
  "erp-negoce-alimentaire-marche-de-gros",
  "Déchargement de cagettes depuis un camion sur un marché de gros au petit matin"),
 (5957,  "/negoce/",                              1797428,
  "erp-negoce-entrepot-allees-preparation",
  "Deux opérateurs manœuvrant un chariot dans les allées d'un entrepôt"),
]


def preparer(pid, nom):
    """Telecharge, recadre en 16/9 et convertit en WebP sous 200 ko."""
    brut = f"{S}/px/src-{pid}.jpg"
    if not os.path.exists(brut) or os.path.getsize(brut) < 5000:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0",
                        f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg"
                        f"?auto=compress&cs=tinysrgb&w=2400", "-o", brut], check=True)
    im = Image.open(brut).convert("RGB")
    L, H = 1920, 1080
    r = max(L / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x0, y0 = (im.width - L) // 2, (im.height - H) // 2
    im = im.crop((x0, y0, x0 + L, y0 + H))
    f = f"{S}/{nom}.webp"
    for q in (80, 74, 68, 62, 56):
        im.save(f, "WEBP", quality=q, method=6)
        ko = os.path.getsize(f) // 1024
        if ko <= 195:
            break
    return f, ko, q


def televerser(chemin, nom, alt):
    req = urllib.request.Request(
        f"{w.SITE}/wp-json/wp/v2/media", data=open(chemin, "rb").read(), method="POST",
        headers={"Authorization": w._auth_header(), "Content-Type": "image/webp",
                 "Content-Disposition": f'attachment; filename="{nom}.webp"'})
    with urllib.request.urlopen(req, timeout=300, context=w._CTX) as r:
        m = json.loads(r.read().decode())
    w.api(f"media/{m['id']}", "POST", {"alt_text": alt, "caption": "Photo Pexels"})
    return m


def main():
    rapport, pb = [], []
    for page, url, pexels, nom, alt in PLAN:
        if page in PROTEGEES:
            pb.append("REFUS — page protegee : %s" % url)
            continue

        c = w.get_raw("pages", page)["content"]["raw"]
        m = re.search(r'(<section class="hero-section"[^>]*url\(\')([^\']+)(\'\))', c)
        if not m:
            pb.append("%s : hero introuvable" % url)
            continue
        ancienne = m.group(2)

        if pexels is None:
            # reutilisation d'un media deja en ligne
            neuve = BASE + nom + ".webp"
            info = "réutilisée"
        else:
            f, ko, q = preparer(pexels, nom)
            if LIVE:
                md = televerser(f, nom, alt)
                neuve = md["source_url"]
            else:
                neuve = BASE + nom + ".webp"
            info = "%d ko, q=%d" % (ko, q)

        if ancienne == neuve:
            rapport.append("%-42s inchangée" % url)
            continue

        # On substitue DANS la balise du hero et nulle part ailleurs : la meme URL
        # peut figurer ailleurs dans la page, par exemple dans les donnees
        # structurees, ou elle n'a rien a faire ici.
        neuf = c[:m.start(2)] + neuve + c[m.end(2):]
        if len(neuf) - len(c) != len(neuve) - len(ancienne):
            pb.append("%s : la substitution a touche autre chose que l'URL" % url)
            continue
        if neuf.count(neuve) - c.count(neuve) != 1:
            pb.append("%s : la nouvelle URL n'a pas ete posee une fois exactement" % url)
            continue
        reste = c.count(ancienne) - 1
        if reste:
            pb.append("%s : l'ancienne image reste citee %d fois ailleurs dans la page"
                      % (url, reste))

        if LIVE:
            w.update_content("pages", page, neuf, live=True)
        rapport.append("%-42s %-46s %s" % (url, nom, info))

    print("%-42s %-46s %s" % ("PAGE", "NOUVELLE IMAGE", "POIDS"))
    print("-" * 118)
    for l in rapport:
        print(l)
    print("\n%d pages traitees | %d point(s) de vigilance" % (len(rapport), len(pb)))
    for p in pb:
        print("   !", p)
    if not LIVE:
        print("\nessai a blanc — rien n'a ete ecrit sur le site")


if __name__ == "__main__":
    main()
