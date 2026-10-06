#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Artefacts d'apercu des trois brouillons, lisibles sans connexion."""
import os, re, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro"); sys.path.insert(0, ICI)
import wp_common as w
from maquette_agro import (convertir, POLICE, REPOS, SVG_FA, nettoyer, reparer,
                           controler, remplacer_video)
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
for pid, cle, titre in ((11955, "fruits-et-legumes", "ERP Fruits et Légumes"),
                        (11957, "produits-de-la-mer", "ERP Produits de la Mer"),
                        (11959, "pme-en-croissance", "ERP PME Agroalimentaire")):
    c = w.api("pages/%d?context=edit" % pid)["content"]["raw"]
    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    ok = 0
    for u in sorted(urls):
        d = convertir(u)
        if d:
            c = c.replace(u, d); ok += 1
    for cls, svg in SVG_FA.items():
        c = c.replace('<i class="%s"></i>' % cls, svg)
    c = re.sub(r"<link[^>]+cdnjs\.cloudflare\.com[^>]*>", "", c)
    c, _ = remplacer_video(c)
    c, _ = reparer(c)
    c = nettoyer(c)
    # reparer() retire le tiroir de FAQ du gabarit mais laisse son script :
    # dans l'artefact seulement, pas sur la page. On garde donc le script,
    # mais on le protege, sinon l'apercu leve une exception que la vraie page
    # n'a pas.
    if 'id="faqDrawerOverlay"' not in c:
        c = c.replace("document.getElementById('faqDrawerOverlay').addEventListener(",
                      "(document.getElementById('faqDrawerOverlay')||"
                      "{addEventListener:function(){}}).addEventListener(")
    html = ("<title>%s — brouillon</title>\n" % titre) + POLICE + "\n" + REPOS + "\n" + c
    f = "%s/apercu-%s.html" % (S, cle)
    open(f, "w", encoding="utf-8").write(html)
    pb = controler(html)
    print("%-20s %4d ko · %d images · %d onglets %s"
          % (cle, len(html) // 1024, ok, html.count('name="hhf-onglet"'),
             "· " + " ".join(pb) if pb else "· controles verts"))
