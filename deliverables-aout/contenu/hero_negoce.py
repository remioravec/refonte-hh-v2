#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nouvelle photo de hero pour /negoce/ — la page de negoce alimentaire.

Photo choisie par le client : un commerçant disposant des salades dans une
cagette, au rayon fruits et legumes d'une epicerie. Retrouvee sur Pexels,
reference 8476596, Kampus Production, serie tournee au Portugal.

Pourquoi /negoce/ et non /agroalimentaire/negoce-alimentaire/ : les deux pages
ont ete unifiees le 11/09/2026. L'ancienne URL est en 301 vers /negoce/, et sa
page est en brouillon. Le negoce alimentaire, aujourd'hui, c'est la page 5957.

La page 5957 n'est pas dans les cinq pages protegees.

Usage :  python3 hero_negoce.py            (essai a blanc)
         python3 hero_negoce.py --live     (ecriture)
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
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402

LIVE = "--live" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

PAGE = 5957
URL = "/negoce/"
PEXELS = 8476596
NOM = "erp-negoce-alimentaire-epicerie-cagettes-salades"
ALT = ("Commerçant disposant des salades dans une cagette au rayon fruits et légumes "
       "d'une épicerie")


def preparer():
    """Telecharge, recadre en 16/9 a 1920x1080, WebP sous 200 ko."""
    os.makedirs(S + "/px", exist_ok=True)
    brut = "%s/px/src-%d.jpg" % (S, PEXELS)
    if not os.path.exists(brut) or os.path.getsize(brut) < 20000:
        r = subprocess.run(
            ["curl", "-sL", "-A", "Mozilla/5.0", "-w", "%{http_code}",
             "https://images.pexels.com/photos/%d/pexels-photo-%d.jpeg"
             "?auto=compress&cs=tinysrgb&w=2400" % (PEXELS, PEXELS), "-o", brut],
            capture_output=True, text=True)
        if r.stdout.strip() != "200":
            raise SystemExit("ARRET — telechargement Pexels : HTTP %s" % r.stdout.strip())
    im = Image.open(brut).convert("RGB")
    L, H = 1920, 1080
    r = max(L / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x0, y0 = (im.width - L) // 2, (im.height - H) // 2
    im = im.crop((x0, y0, x0 + L, y0 + H))
    f = "%s/%s.webp" % (S, NOM)
    for q in (80, 74, 68, 62, 56):
        im.save(f, "WEBP", quality=q, method=6)
        ko = os.path.getsize(f) // 1024
        if ko <= 195:
            break
    return f, ko, q


def televerser(chemin):
    req = urllib.request.Request(
        "%s/wp-json/wp/v2/media" % w.SITE, data=open(chemin, "rb").read(), method="POST",
        headers={"Authorization": w._auth_header(), "Content-Type": "image/webp",
                 "Content-Disposition": 'attachment; filename="%s.webp"' % NOM})
    with urllib.request.urlopen(req, timeout=300, context=w._CTX) as r:
        m = json.loads(r.read().decode())
    w.api("media/%d" % m["id"], "POST", {"alt_text": ALT, "caption": "Photo Pexels"})
    return m


def main():
    if PAGE in PROTEGEES:
        raise SystemExit("ARRET — page protegee")

    p = w.get_raw("pages", PAGE)
    c = p["content"]["raw"]
    # « _elementor_data » vaut « [] » sur les pages canvas autonomes : c'est une
    # liste VIDE, pas un contenu Elementor. La regle interdit d'ecrire dans le
    # post_content d'une page reellement construite avec Elementor.
    el = (p.get("meta", {}).get("_elementor_data") or "").strip()
    if el not in ("", "[]", "[ ]", "null"):
        raise SystemExit("ARRET — la page porte des donnees Elementor (%d octets)" % len(el))

    m = re.search(r"(<section class=\"hero-section\"[^>]*url\(')([^']+)('\))", c)
    if not m:
        raise SystemExit("ARRET — fond du hero introuvable sur %d" % PAGE)
    avant = m.group(2)
    print("page %d %s" % (PAGE, URL))
    print("  hero actuel : %s" % avant.split("/")[-1])

    f, ko, q = preparer()
    print("  nouvelle photo : %s (1920x1080, %d ko, qualite %d)" % (os.path.basename(f), ko, q))

    if not LIVE:
        print("\nessai a blanc — rien n'est ecrit. Relancer avec --live.")
        return

    sauve = "%s/backup-hero-%d.html" % (S, PAGE)
    open(sauve, "w", encoding="utf-8").write(c)
    print("  sauvegarde : %s" % sauve)

    md = televerser(f)
    print("  media %d : %s" % (md["id"], md["source_url"]))

    neuf = c[:m.start(2)] + md["source_url"] + c[m.end(2):]
    if neuf == c or md["source_url"] not in neuf:
        raise SystemExit("ARRET — le remplacement n'a pas pris")
    w.api("pages/%d" % PAGE, "POST", {"content": neuf})

    # relecture : on verifie ce qui est REELLEMENT en base, pas ce qu'on a envoye
    c2 = w.get_raw("pages", PAGE)["content"]["raw"]
    m2 = re.search(r"<section class=\"hero-section\"[^>]*url\('([^']+)'\)", c2)
    ok = m2 and m2.group(1) == md["source_url"]
    print("  relecture : %s" % ("hero en place" if ok else "ECHEC — %s" % (m2 and m2.group(1))))
    if len(c2) < len(c) - 200:
        print("  ! la page a maigri de %d octets, a verifier" % (len(c) - len(c2)))
    for u in (md["source_url"], "https://www.helloharel.com" + URL):
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-I", u],
                           capture_output=True, text=True)
        print("  %s -> HTTP %s" % (u.split("/")[-1] or URL, r.stdout.strip()))


if __name__ == "__main__":
    main()
