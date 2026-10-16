#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Combien de reponses de FAQ sont invisibles pour un moteur, sur le blog."""
import os, re, sys
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp_common as w, ns_api      # noqa: E402

arts, p = [], 1
while True:
    lot = ns_api.call("wp/v2/posts?per_page=100&page=%d&status=publish&_fields=id,link" % p)
    if not lot:
        break
    arts += lot
    if len(lot) < 100:
        break
    p += 1

tot_q = tot_js = 0
avec_details = avec_js = avec_outil = avec_fragment = 0
sans_faq = []
for a in arts:
    c = w.get_raw("posts", a["id"])["content"]["raw"]
    u = a["link"].replace("https://www.helloharel.com", "")
    cartes = len(re.findall(r'class="faq-card"', c))
    det = c.count("<details")
    js = "faqData" in c
    if det:
        avec_details += 1
    if js:
        avec_js += 1
        m = re.search(r"var faqData\s*=\s*(\[.*?\]);", c, re.S)
        n = len(re.findall(r"\{\s*title\s*:", m.group(1))) if m else 0
        tot_js += n
        tot_q += n
    elif det:
        tot_q += det
    else:
        sans_faq.append(u)
    if re.search(r"hha-tool", c):
        avec_outil += 1
    if "'+d.title+'" in c or '"+d.title+"' in c:
        avec_fragment += 1

print("%d articles" % len(arts))
print("   FAQ en <details> (lisible)        : %d" % avec_details)
print("   FAQ en JavaScript (invisible)     : %d" % avec_js)
print("   sans FAQ                          : %d" % len(sans_faq))
print("   outil interactif hha-tool         : %d" % avec_outil)
print("   fragment de script rendu en titre : %d" % avec_fragment)
print("\n%d questions au total, dont %d dont la reponse n'est PAS dans le HTML"
      % (tot_q, tot_js))
if sans_faq:
    print("\nsans FAQ :", ", ".join(sans_faq[:6]))
