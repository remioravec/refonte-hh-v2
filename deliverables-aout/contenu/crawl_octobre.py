#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le crawl qui alimente les tickets techniques d'octobre.

On releve ce que la roadmap technique a historiquement traite — titles et
descriptions hors gabarit, canoniques, indexabilite, sitemap, poids,
images, balisage en double — plus ce que les mois precedents ont laisse
derriere eux. Un ticket ne se redige pas sur une impression : chaque
ligne sortie ici est mesuree sur la page servie.
"""

import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import ns_api                    # noqa: E402

SORTIE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
          "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/crawl-octobre.json")
# Largeur en pixels d'un title Google : approximation par la largeur des
# caracteres, celle utilisee pour le tableau de balisage.
LARGE = set("mwMW—…")
MOYEN = set("ABCDEFGHJKLNOPQRSTUVXYZabcdeghknopqsuvxyz0123456789")


def px(t):
    n = 0.0
    for c in t:
        n += 11.0 if c in LARGE else (8.0 if c in MOYEN else 5.5)
    return round(n)


def lire(url, essais=3):
    for k in range(essais):
        try:
            r = urllib.request.urlopen(urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (crawl Hello Harel)"}),
                timeout=90)
            h = r.read().decode("utf-8", "replace")
            if "</html>" in h:
                return r.status, h
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception:                      # noqa: BLE001
            time.sleep(2 * (k + 1))
    return None, ""


def balise(h, nom):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % nom, h, re.I)
    return m.group(1) if m else ""


def examiner(t, pid, url):
    plein = "https://www.helloharel.com" + url
    code, h = lire(plein)
    if not h:
        return {"url": url, "type": t, "code": code, "erreur": "illisible"}
    titre = re.search(r"<title>(.*?)</title>", h, re.S)
    titre = re.sub(r"\s+", " ", titre.group(1)).strip() if titre else ""
    desc = balise(h, "description")
    rob = balise(h, "robots")
    can = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    can = can.group(1).replace("https://www.helloharel.com", "") if can else ""
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    corps = h[h.find('<div id="hh-page"'):h.rfind("<footer")]
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', h)
    return {
        "url": url, "type": t, "code": code, "poids": len(h),
        "title": titre, "title_px": px(titre),
        "desc": desc, "desc_px": px(desc),
        "desc_css": bool(re.search(r"[{}]", desc)),
        "robots": rob, "canonical": can, "canonique_ok": (can in ("", url)),
        "h1": [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip() for x in h1],
        "sections": len(re.findall(r'<section class="[^"]+"', corps)),
        "images": len(imgs),
        "img_non_webp": sum(1 for x in imgs if re.search(r"\.(png|jpe?g)(\?|$)", x, re.I)),
        "ld_json": len(re.findall(r'<script type="application/ld\+json">', h)),
        "organization": len(re.findall(r'"@type": ?"Organization"', h)),
        "website": len(re.findall(r'"@type": ?"WebSite"', h)),
        "aggregate": len(re.findall(r'"@type": ?"AggregateRating"', h)),
        "faqpage": len(re.findall(r'"@type": ?"FAQPage"', h)),
        "entites": len(re.findall(r"&#0?38;", h)),
    }


def inventaire():
    out = []
    for t in ("pages", "posts"):
        p = 1
        while True:
            try:
                lot = ns_api.call("wp/v2/%s?per_page=100&page=%d&status=publish"
                                  "&_fields=id,link" % (t, p))
            except RuntimeError as e:
                if "invalid_page_number" in str(e):
                    break
                raise
            if not lot:
                break
            out += [(t, x["id"],
                     x["link"].replace("https://www.helloharel.com", "") or "/")
                    for x in lot]
            if len(lot) < 100:
                break
            p += 1
    return sorted(out, key=lambda z: z[2])


def main():
    cibles = inventaire()
    print("%d URL a crawler" % len(cibles))
    res = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for k, r in enumerate(ex.map(lambda z: examiner(*z), cibles), 1):
            res.append(r)
            if k % 25 == 0:
                print("   %d/%d" % (k, len(cibles)))
    json.dump(res, open(SORTIE, "w"), ensure_ascii=False)
    print("ecrit :", SORTIE)


if __name__ == "__main__":
    main()
