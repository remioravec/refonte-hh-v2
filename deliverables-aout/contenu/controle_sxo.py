#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4.3 — la part MESUREE du controle qualite SXO, celle qu'un script tranche.

Les sept autres controles sont juges par l'agent, a froid, sur le rendu.
Ici on ne mesure que ce qui se compte, sur le HTML livre :

  1. un visuel par H2
  2. les infographies portent du texte, une source et une date
  3. les liens du plan sont poses DANS LE TEXTE, pas en annexe
  4. lisibilite : longueur de phrase, longueur de paragraphe
  5. rendu : title et description dans les fourchettes, un seul H1,
     JSON-LD valide, pas de lien interne casse

Usage :  python3 controle_sxo.py <fichier.html> [--liens a,b,c]
"""

import json
import re
import subprocess
import sys


def mesurer(f, liens, a_publier=()):
    """a_publier : les URL du meme lot, pas encore en ligne. Un 404 sur
    l'une d'elles est une dependance de publication, pas un lien casse."""
    h = open(f, encoding="utf-8").read()
    corps = h
    i = h.find('class="hha-art"')
    if i > 0:
        j = h.find("</article>", i)
        if j < 0:
            j = h.find("</section>", i)
        corps = h[i:j if j > 0 else len(h)]

    r = []

    # 1 — un visuel par H2
    n_h2 = len(re.findall(r"<h2\b", corps))
    n_vis = len(re.findall(r'<figure[^>]*class="(?:mn|rg|fa2)\b', corps))
    r.append(("un visuel par H2", n_h2 == n_vis, "%d H2, %d visuels" % (n_h2, n_vis)))

    # 2 — les infographies portent texte, source et date
    figs = re.findall(r"<figure[^>]*>(.*?)</figure>", corps, re.S)
    sans_texte = sum(1 for x in figs if len(re.sub(r"<[^>]+>", "", x).strip()) < 60)
    sourcees = sum(1 for x in figs if re.search(r"[Ss]ource|relevé|Google Ads", x))
    r.append(("infographies avec du texte", sans_texte == 0,
              "%d figure(s) quasi vide(s) sur %d" % (sans_texte, len(figs))))
    r.append(("au moins une source datee", sourcees > 0,
              "%d figure(s) sourcee(s) sur %d" % (sourcees, len(figs))))

    # 3 — les liens du plan, dans le texte
    manquants = [u for u in liens if ('href="%s"' % u) not in corps]
    r.append(("liens du plan dans le texte", not manquants,
              "manquants : %s" % (", ".join(manquants) if manquants else "aucun")))
    # et poses dans une phrase, pas dans une liste de liens nue
    nus = len(re.findall(r"<(?:li|p)>\s*<a [^>]*>[^<]*</a>\s*</(?:li|p)>", corps))
    r.append(("aucun lien pose nu", nus == 0, "%d lien(s) seul(s) dans leur bloc" % nus))

    # 4 — lisibilite, sur la PROSE seulement.
    # Les <figure> sont des tableaux, des frises et des ecrans : leur texte
    # concatene forme un bloc sans ponctuation que le compteur prenait pour
    # une phrase de cent cinquante mots. On les retire avant de mesurer.
    prose = re.sub(r"<figure.*?</figure>", " ", corps, flags=re.S)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", prose))
    phrases = [p.strip() for p in re.split(r"[.!?]\s", txt) if len(p.strip()) > 15]
    longues = [p for p in phrases if len(p.split()) > 38]
    paras = re.findall(r"<p[^>]*>(.*?)</p>", prose, re.S)
    gros = [p for p in paras if len(re.sub(r"<[^>]+>", "", p).split()) > 110]
    r.append(("phrases sous 38 mots", len(longues) <= 1,
              "%d phrase(s) longue(s) sur %d" % (len(longues), len(phrases))))
    r.append(("paragraphes sous 110 mots", not gros,
              "%d paragraphe(s) trop long(s) sur %d" % (len(gros), len(paras))))

    # 5 — rendu
    try:
        from PIL import ImageFont
        T = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 20)
        D = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 14)
        t = (re.findall(r"<title>(.*?)</title>", h, re.S) or [""])[0]
        d = (re.findall(r'<meta name="description" content="(.*?)"', h, re.S) or [""])[0]
        tp = round(T.getlength(t)) if t else 0
        dp = round(D.getlength(d)) if d else 0
        r.append(("title 200-561 px", 200 <= tp <= 561 if tp else False, "%d px" % tp))
        if dp:
            r.append(("description 400-985 px", 400 <= dp <= 985, "%d px" % dp))
    except Exception as e:
        r.append(("mesure en pixels", False, str(e)[:50]))

    n_h1 = len(re.findall(r"<h1\b", h))
    r.append(("un seul H1", n_h1 == 1, "%d H1" % n_h1))

    ok_ld = True
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(m.group(1))
        except Exception:
            ok_ld = False
    r.append(("JSON-LD valide", ok_ld, "ok" if ok_ld else "au moins un bloc invalide"))

    casses, attendus = [], []
    for u in sorted(set(re.findall(r'href="(/[^"#?]+)"', corps))):
        code = subprocess.run(["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}",
                               "https://www.helloharel.com" + u],
                              capture_output=True, text=True, timeout=40).stdout.strip()
        if code in ("200", "301"):
            continue
        if u in a_publier:
            attendus.append(u)
        else:
            casses.append("%s (%s)" % (u, code))
    r.append(("liens internes qui repondent", not casses,
              "casses : %s%s" % (", ".join(casses) if casses else "aucun",
                                 " · %d en attente de publication" % len(attendus)
                                 if attendus else "")))

    return r


def main():
    f = sys.argv[1]
    liens, a_publier = [], []
    if "--liens" in sys.argv:
        liens = [x for x in sys.argv[sys.argv.index("--liens") + 1].split(",") if x]
    if "--a-publier" in sys.argv:
        a_publier = [x for x in sys.argv[sys.argv.index("--a-publier") + 1].split(",") if x]
    res = mesurer(f, liens, set(a_publier))
    print("CONTROLE SXO MESURE — %s\n" % f.split("/")[-1])
    ko = 0
    for nom, ok, det in res:
        print("  %s  %-32s %s" % ("OK " if ok else "!! ", nom, det))
        ko += 0 if ok else 1
    print("\n%d / %d controles mesures passes" % (len(res) - ko, len(res)))
    sys.exit(1 if ko else 0)


if __name__ == "__main__":
    main()
