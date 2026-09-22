#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L'etat du parc d'articles, avant toute proposition de gabarit.

On releve ce qui existe : combien d'articles, quelles structures
coexistent, ce qui manque et ce qui traine. On ne propose rien ici.
"""
import os, re, sys
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp_common as w, ns_api      # noqa: E402

MARQUES = [
    ("chapo", r'class="[^"]*(?:chapo|lead|intro)[^"]*"'),
    ("sommaire", r'class="[^"]*(?:toc|sommaire)[^"]*"|id="sommaire"'),
    ("FAQ", r"<details|faq-section|faqData"),
    ("CTA", r"cta-banner|hh-demo-cta|demander-une-demo|/contact/"),
    ("image a la une", r"wp-post-image|featured"),
    ("tableau", r"<table"),
    ("encadre", r'class="[^"]*(?:encadre|callout|note|reponse)[^"]*"'),
    ("sources", r'id="sources"|eeat-sources'),
    ("auteur", r'rel="author"|class="[^"]*auteur[^"]*"'),
    ("maj", r"Mis à jour|Mise à jour|derniere mise a jour"),
    ("calculateur", r"roi-block|calculateur|simulateur"),
    ("carte orpheline", r'<div class="bento-card'),
    ("JS inline", r"<script(?![^>]*src)"),
]


def main():
    arts, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/posts?per_page=100&page=%d&status=publish"
                          "&_fields=id,link,title,date,modified" % p)
        if not lot:
            break
        arts += lot
        if len(lot) < 100:
            break
        p += 1
    print("%d article(s) publie(s)\n" % len(arts))
    print("%-6s %-52s %5s %4s %4s  %s" % ("id", "url", "ko", "h2", "mots", "marques"))
    print("-" * 132)
    stats = {n: 0 for n, _ in MARQUES}
    lignes = []
    for a in sorted(arts, key=lambda x: x["link"]):
        c = w.get_raw("posts", a["id"])["content"]["raw"]
        u = a["link"].replace("https://www.helloharel.com", "")
        corps = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", c, flags=re.S)
        mots = len(re.sub(r"<[^>]+>", " ", corps).split())
        h2 = len(re.findall(r"<h2", corps))
        trouve = []
        for nom, motif in MARQUES:
            if re.search(motif, c, re.I):
                trouve.append(nom)
                stats[nom] += 1
        lignes.append((u, a["id"], len(c), h2, mots, trouve))
        print("%-6d %-52s %5d %4d %4d  %s"
              % (a["id"], u[:52], len(c) // 1024, h2, mots, ", ".join(trouve)))
    print("\n=== presence des marques sur %d articles ===" % len(arts))
    for n, _ in MARQUES:
        print("   %-18s %3d article(s)  (%d%%)"
              % (n, stats[n], round(100 * stats[n] / max(1, len(arts)))))
    tailles = sorted(x[2] for x in lignes)
    mots = sorted(x[4] for x in lignes)
    print("\ntaille : de %d a %d ko (median %d)"
          % (tailles[0] // 1024, tailles[-1] // 1024, tailles[len(tailles) // 2] // 1024))
    print("mots   : de %d a %d (median %d)" % (mots[0], mots[-1], mots[len(mots) // 2]))


if __name__ == "__main__":
    main()
