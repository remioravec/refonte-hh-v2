#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La FAQ des trois pages passe en accordeon simple.

Aujourd'hui : six cartes qui appellent openFaqDrawer(n), et un tiroir pose
plus bas dans la page avec les six reponses. Sur telephone, un panneau du
tiroir se retrouve rendu en ligne — c'est la « petite image dans le vide »
signalee le 22/09.

Apres : six <details> natifs. On clique, ca se deplie. Pas de tiroir, pas de
superposition, pas de JavaScript — donc plus rien a casser. Le balisage
FAQPage est ajoute au passage : les questions deviennent eligibles aux
resultats enrichis, ce que les cartes ne permettaient pas.

Les questions et les reponses sont celles du tiroir, mot pour mot. Les
libelles des cartes en differaient legerement ; ce sont les paires du tiroir
qui font foi, puisque ce sont elles qui portent les reponses.

Usage :  python3 faq_accordeon.py            (blanc)
         python3 faq_accordeon.py --poser    (ecrit)
"""

import json
import os
import re
import sys
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w         # noqa: E402
import scroll_sticky as SY    # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "faq-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

CSS = """<style id="hh-faq-accordeon">
#hh-page .fa2,.fa2{max-width:860px !important;margin:0 auto !important;
 display:grid !important;gap:.85rem !important}
#hh-page .fa2 details,.fa2 details{background:#fff !important;
 border:1px solid #e2e8f0 !important;border-radius:18px !important;overflow:hidden;
 transition:border-color .2s ease,box-shadow .2s ease}
#hh-page .fa2 details[open],.fa2 details[open]{border-color:#7DD3FC !important;
 box-shadow:0 14px 34px -26px rgba(15,23,42,.65) !important}
#hh-page .fa2 summary,.fa2 summary{display:flex !important;align-items:center !important;
 justify-content:space-between !important;gap:1.25rem !important;min-height:64px !important;
 padding:1.2rem 1.5rem !important;cursor:pointer !important;list-style:none !important;
 font-size:1.04rem !important;font-weight:700 !important;color:#0f172a !important;
 line-height:1.4 !important;transition:background .18s ease}
#hh-page .fa2 summary:hover,.fa2 summary:hover{background:#F8FAFC !important}
#hh-page .fa2 summary::-webkit-details-marker,.fa2 summary::-webkit-details-marker{display:none}
/* le chevron, dans sa pastille : une cible visible, pas un trait perdu */
#hh-page .fa2 summary::after,.fa2 summary::after{content:"";flex:0 0 30px;width:30px;
 height:30px;border-radius:50%;background:#F0F9FF;
 background-image:linear-gradient(45deg,transparent 47%,#0369A1 47%,#0369A1 53%,transparent 53%),
  linear-gradient(-45deg,transparent 47%,#0369A1 47%,#0369A1 53%,transparent 53%);
 background-size:9px 9px,9px 9px;background-position:calc(50% - 3px) calc(50% + 1px),
  calc(50% + 3px) calc(50% + 1px);background-repeat:no-repeat;
 transition:transform .22s ease,background-color .22s ease}
#hh-page .fa2 details[open] summary::after,.fa2 details[open] summary::after{
 transform:rotate(180deg);background-color:#E0F2FE}
/* la reponse : une respiration franche, et un filet qui la detache */
#hh-page .fa2 .fa2-r,.fa2 .fa2-r{padding:1.3rem 1.5rem 1.55rem !important;
 border-top:1px solid #EEF2F7 !important;color:#475569 !important;
 font-size:1rem !important;line-height:1.78 !important}
#hh-page .fa2 .fa2-r p,.fa2 .fa2-r p{margin:0 0 1rem !important}
#hh-page .fa2 .fa2-r>div>*:last-child,.fa2 .fa2-r>div>*:last-child{margin-bottom:0 !important}
#hh-page .fa2 .fa2-r ul,.fa2 .fa2-r ul{margin:0 0 1rem !important;padding:0 !important;
 list-style:none !important}
#hh-page .fa2 .fa2-r li,.fa2 .fa2-r li{position:relative !important;
 padding-left:1.5rem !important;margin:0 0 .75rem !important;line-height:1.72 !important}
#hh-page .fa2 .fa2-r li:last-child,.fa2 .fa2-r li:last-child{margin-bottom:0 !important}
#hh-page .fa2 .fa2-r li::before,.fa2 .fa2-r li::before{content:"";position:absolute;
 left:.3rem;top:.72em;width:7px;height:7px;border-radius:50%;background:#00B1F5}
#hh-page .fa2 .fa2-r strong,.fa2 .fa2-r strong{color:#0f172a !important;font-weight:650 !important}
#hh-page .fa2-pied,.fa2-pied{max-width:860px !important;margin:1.6rem auto 0 !important;
 text-align:center !important}
#hh-page .fa2-cta,.fa2-cta{display:inline-flex !important;align-items:center !important;
 gap:.5rem !important;padding:.9rem 1.8rem !important;border-radius:999px !important;
 background:#0369A1 !important;color:#fff !important;font-weight:700 !important;
 font-size:.98rem !important;text-decoration:none !important;
 box-shadow:0 10px 24px -14px rgba(3,105,161,.9) !important}
@media (max-width:640px){
 #hh-page .fa2 summary,.fa2 summary{font-size:.98rem !important;
  padding:1rem 1.1rem !important;gap:.8rem !important}
 #hh-page .fa2 summary::after,.fa2 summary::after{flex:0 0 26px;width:26px;height:26px}
 #hh-page .fa2 .fa2-r,.fa2 .fa2-r{padding:1.1rem 1.1rem 1.25rem !important;
  font-size:.97rem !important}}
</style>"""


def lire(contenu):
    """Rend (bornes, entete, paires, pied) — questions et reponses du tiroir."""
    i = contenu.find('<section class="faq-section"')
    if i < 0:
        raise SystemExit("ARRET — section FAQ introuvable")
    j = contenu.find("</section>", i) + len("</section>")
    ent = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="faq-cards-grid")',
                    contenu[i:j], re.S)
    if not ent:
        raise SystemExit("ARRET — en-tete de FAQ introuvable")

    k = contenu.find('id="faqDrawerOverlay"')
    if k < 0:
        raise SystemExit("ARRET — tiroir introuvable")
    k = contenu.rfind("<div", 0, k)
    fin = contenu.find("<script", k)
    tiroir = contenu[k:fin]

    paires = []
    for m in re.finditer(r'<div class="faq-drawer-panel"[^>]*>', tiroir):
        bout = SY.bloc_ferme(tiroir, m.start())
        pan = tiroir[m.end():bout - len("</div>")]
        q = re.search(r"<h3>(.*?)</h3>", pan, re.S)
        r = re.search(r'<div class="faq-drawer-content">(.*)</div>\s*$', pan, re.S)
        if not q or not r:
            raise SystemExit("ARRET — panneau de tiroir incomplet")
        paires.append((re.sub(r"<[^>]+>", "", q.group(1)).strip(), r.group(1).strip()))
    if not paires:
        raise SystemExit("ARRET — aucune reponse dans le tiroir")
    # Le pied du tiroir porte un lien vers /contact/ : il suit l'accordeon.
    pied = re.search(r'<div class="faq-drawer-footer">\s*(<a\b.*?</a>)', tiroir, re.S)
    return (i, j, k, fin), ent.group(0), paires, (pied.group(1) if pied else "")


def section(entete, paires, pied=""):
    det = ""
    for n, (q, r) in enumerate(paires):
        det += ('<details%s itemscope itemprop="mainEntity" '
                'itemtype="https://schema.org/Question">'
                '<summary itemprop="name">%s</summary>'
                '<div class="fa2-r" itemscope itemprop="acceptedAnswer" '
                'itemtype="https://schema.org/Answer"><div itemprop="text">%s</div></div>'
                '</details>' % (" open" if n == 0 else "", q, r))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer",
                            "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()}}
        for q, r in paires]}
    return (CSS + '<section class="faq-section" id="faq" itemscope '
            'itemtype="https://schema.org/FAQPage"><div class="container">'
            + entete + '<div class="fa2">%s</div>' % det
            + (('<p class="fa2-pied">%s</p>' % re.sub(r'class="[^"]*"', 'class="fa2-cta"', pied))
               if pied else "") + '</div>' 
            + '<script type="application/ld+json">%s</script></section>'
            % json.dumps(ld, ensure_ascii=False))


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        (i, j, k, fin), entete, paires, pied = lire(c)
        if not (j <= k):
            raise SystemExit("ARRET — le tiroir n'est pas apres la section sur %s" % url)

        # On retire d'abord le tiroir (plus loin dans la chaine), puis la
        # section : dans cet ordre, les bornes de la section restent valides.
        neuf = c[:k] + c[fin:]
        neuf = neuf[:i] + section(entete, paires, pied) + neuf[j:]

        # Le script du tiroir n'a plus de cible : il part avec lui.
        for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", neuf, re.S))[::-1]:
            if "openFaqDrawer" in m.group(1) or "faqDrawerOverlay" in m.group(1):
                neuf = neuf[:m.start()] + neuf[m.end():]

        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        reste = [x for x in ("faqDrawerOverlay", "faq-drawer", "openFaqDrawer", "faq-card")
                 if x in corps(neuf)]
        if reste:
            raise SystemExit("ARRET — il reste %s dans le corps sur %s" % (reste, url))
        av = re.findall(r'href="([^"]+)"', corps(c))
        ap = re.findall(r'href="([^"]+)"', corps(neuf))
        if sorted(av) != sorted(ap):
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s : %s"
                             % (url, list(set(av) - set(ap))[:3]))

        print("%-42s %d questions · %+d ko · balisage FAQPage ajoute"
              % (url, len(paires), (len(neuf) - len(c)) // 1024))
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
    time.sleep(4)
    for cle, (page, url) in SY.PAGES.items():
        req = urllib.request.Request("https://www.helloharel.com" + url,
                                     headers={"User-Agent": "Mozilla/5.0"})
        h = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
        det, cartes = h.count("<details"), h.count('class="faq-card"')
        ld = h.count('"@type": "FAQPage"') + h.count('"@type":"FAQPage"')
        ok = det >= 6 and cartes == 0 and "faqDrawerOverlay" not in h and ld >= 1
        print("   %-42s %s  %d accordeons · %d cartes restantes · tiroir %s · FAQPage %d"
              % (url, "OK " if ok else "KO ", det, cartes,
                 "absent" if "faqDrawerOverlay" not in h else "PRESENT", ld))


if __name__ == "__main__":
    main()
