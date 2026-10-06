#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ce que le visiteur recoit reellement sur les cent trois articles.

On ne lit pas la base : on lit la page servie. Une page peut etre juste en
base et rendue vide, et un script juste en base peut etre servi casse —
WordPress a deja transforme deux esperluettes en entites et rendu le
defilement inerte sur trois pages.
"""

import os
import re
import sys
import time
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import ns_api                    # noqa: E402
import blog_faq_cachee as FC     # noqa: E402
import deployer_blog as DB       # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/blog-parc-avant")


def lire_page(url):
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


def main():
    arts, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/posts?per_page=100&page=%d&status=publish"
                          "&_fields=id,link" % p)
        if not lot:
            break
        arts += lot
        if len(lot) < 100:
            break
        p += 1

    print("%-52s %4s %3s %3s %3s  %s"
          % ("url", "ko", "FAQ", "img", "ld", "etat"))
    print("-" * 132)
    bons = 0
    for a in sorted(arts, key=lambda x: x["link"]):
        url = a["link"].replace("https://www.helloharel.com", "")
        av = os.path.join(SAUV, "avant-%d.html" % a["id"])
        attendu = 0
        if os.path.exists(av) and url not in DB.REFERENCE:
            q, _, _ = FC.extraire(open(av, encoding="utf-8").read())
            attendu = len(q)
        h = lire_page(url)
        if h and re.search(r'<link rel="canonical" href="([^"]+)"', h) \
                and re.search(r'<link rel="canonical" href="([^"]+)"', h).group(1) \
                .replace("https://www.helloharel.com", "") != url:
            vers = re.search(r'<link rel="canonical" href="([^"]+)"', h).group(1)
            print("%-52s %4d   —   —   —  REDIRIGE vers %s"
                  % (url[:52], len(h) // 1024,
                     vers.replace("https://www.helloharel.com", "")))
            continue
        if h is None:
            print("%-52s    ?   ?   ?   ?  page illisible en entier" % url[:52])
            continue
        maux = []
        i = h.find('<article class="hha-art"')
        j = h.find('<section class="hhb-acc"')
        if j < 0:
            j = h.rfind("<footer")
        corps = h[i:j] if i >= 0 else ""
        nq = h.count("<details")
        nimg = len(re.findall(r'<figure class="hhb-img">', h))
        nld = len(re.findall(r'"@type": ?"FAQPage"', h))

        if i < 0 and url not in DB.REFERENCE:
            maux.append("corps d'article non servi")
        elif corps and len(corps) < 3000:
            maux.append("corps servi quasi vide (%d o)" % len(corps))
        if attendu and nq < attendu:
            maux.append("%d question(s) servies pour %d attendues" % (nq, attendu))
        if nld > 1:
            maux.append("%d balisages FAQPage" % nld)
        if nq and not nld:
            maux.append("FAQ servie sans balisage")
        if "var faqData" in h:
            maux.append("le tiroir JavaScript est toujours la")
        if "hhb-acc" not in h and url not in DB.REFERENCE:
            maux.append("appel a l'action absent")
        if "&#038;&#038;" in h:
            maux.append("esperluettes transformees en entites")
        if not maux:
            bons += 1
        print("%-52s %4d %3d %3d %3d  %s"
              % (url[:52], len(h) // 1024, nq, nimg, nld,
                 " · ".join(maux) if maux else "servi conforme"))
    print("\n%d article(s) sur %d servis conformes" % (bons, len(arts)))


if __name__ == "__main__":
    main()
