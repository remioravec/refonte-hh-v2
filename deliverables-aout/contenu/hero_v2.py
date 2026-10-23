#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le Hero des trois pages metier : badge revu, description en liste.

1. Le badge de reassurance perd ses silhouettes au profit de la marque
   Google — une seule, pas trois : trois marques identiques empilees se
   lisent comme un defaut d'affichage, pas comme une rangee de clients.
   Sa mise en page telephone est refaite : une rangee compacte qui tient sur
   la largeur, au lieu d'un pave qui se coupait en deux.

2. La phrase sous le H1 devient une liste a puces. AUCUN mot n'est ajoute ni
   retire : on remonte la phrase d'amorce devant, et l'enumeration qu'elle
   contenait deja devient la liste. Un controle compare les deux versions
   mot pour mot avant d'ecrire — ce texte porte les mots-cles de la page.

Usage :  python3 hero_v2.py            (blanc)
         python3 hero_v2.py --poser    (ecrit)
"""

import os
import re
import sys
import unicodedata
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w          # noqa: E402
import scroll_sticky as SY     # noqa: E402
import avatars as AV           # noqa: E402
import hero_maxence as HM      # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "hero-v2-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def FRAIS():
    import random
    return "?hh=%d" % random.randrange(10 ** 9)


def lire_page(url):
    """La page servie, en entier.

    Le transfert est parfois coupe en route : on a deja lu 170 ko d'une page
    qui en fait 364, et le controle a annonce un echec qui n'existait pas.
    On redemande tant que la page ne se termine pas.
    """
    import time
    for essai in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(
                "https://www.helloharel.com" + url + FRAIS(),
                headers={"User-Agent": "Mozilla/5.0"}),
                timeout=90).read().decode("utf-8", "replace")
            if "</html>" in h:
                return h
        except Exception:
            pass
        time.sleep(2 * (essai + 1))
    raise SystemExit("ARRET — page %s illisible en entier apres 4 essais" % url)


COCHE = ('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
         '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.6" '
         'd="M5 13l4 4L19 7"/></svg>')

# Amorce + enumeration, decoupees a la main dans la phrase existante.
# Les mots sont ceux de la page, dans le meme ordre pour l'amorce, et
# l'enumeration reprend la liste que la phrase contenait deja.
LISTES = {
    "torrefacteur": (
        "Torréfaction artisanale de café : du café vert au paquet, notre ERP pilote",
        ["lots", "profils de torréfaction", "coût de revient", "DLC/DDM",
         "conditionnement", "traçabilité des origines"]),
    "brasseur": (
        "L'ERP qui transforme votre brasserie en production maîtrisée",
        ["brassins", "matières (malt, houblon)", "fermentation",
         "conditionnement", "traçabilité"]),
    "chocolatier": (
        "L'ERP qui sécurise vos marges et votre qualité, de la fève à la ballotine",
        ["tempérage", "coût matière au gramme", "moulage", "DLC",
         "étiquetage INCO"]),
}

CSS = """<style id="hh-hero-v2">
/* ── la description en liste ─────────────────────────────────────────── */
#hh-page .hh-hl,.hh-hl{display:flex !important;flex-wrap:wrap !important;
 gap:.45rem !important;list-style:none !important;
 margin:.9rem 0 1.6rem !important;padding:0 !important}
#hh-page .hh-hl li,.hh-hl li{display:inline-flex !important;align-items:center !important;
 gap:.36rem !important;margin:0 !important;padding:.34rem .72rem !important;
 background:rgba(2,32,51,.55) !important;
 border:1px solid rgba(255,255,255,.28) !important;border-radius:999px !important;
 color:#fff !important;font-size:.88rem !important;font-weight:600 !important;
 line-height:1.25 !important;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
#hh-page .hh-hl li svg,.hh-hl li svg{width:14px;height:14px;flex:0 0 14px;
 color:#4ADE80 !important}

/* ── le badge de reassurance ─────────────────────────────────────────── */
#hh-page .hh-conf,.hh-conf{display:inline-flex !important;align-items:center !important;
 gap:.75rem !important;flex-wrap:nowrap !important;margin:1.35rem 0 0 !important;
 padding:.6rem 1.1rem .6rem .65rem !important;width:auto !important;
 max-width:100% !important;box-sizing:border-box !important;
 background:rgba(2,32,51,.66) !important;
 border:1px solid rgba(255,255,255,.22) !important;border-radius:999px !important;
 -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
#hh-page .hh-conf-g,.hh-conf-g{width:38px !important;height:38px !important;
 flex:0 0 38px !important}
#hh-page .hh-conf-d,.hh-conf-d{display:grid !important;gap:.1rem !important;min-width:0}
#hh-page .hh-conf-e,.hh-conf-e{display:flex !important;align-items:center !important;
 gap:.22rem !important;flex-wrap:wrap !important;margin:0 !important;color:#fff !important;
 font-size:.86rem !important;font-weight:700 !important;line-height:1.25 !important}
#hh-page .hh-conf-e svg,.hh-conf-e svg{width:13px;height:13px;color:#FBBF24;flex:none}
#hh-page .hh-conf-e b,.hh-conf-e b{margin-left:.3rem !important;font-weight:700 !important;
 color:#fff !important}
#hh-page .hh-conf-c,.hh-conf-c{margin:0 !important;color:rgba(255,255,255,.92) !important;
 font-size:.8rem !important;font-weight:600 !important;line-height:1.25 !important}
/* Sur telephone le badge reste UNE rangee : la marque, puis la note et le
   nombre de clients l'un sous l'autre. C'est la version a deux rangees qui
   se coupait en deux et donnait l'impression d'un bloc casse. */
@media (max-width:560px){
 #hh-page .hh-conf,.hh-conf{gap:.6rem !important;
  padding:.55rem .95rem .55rem .55rem !important}
 #hh-page .hh-conf-g,.hh-conf-g{width:34px !important;height:34px !important;
  flex:0 0 34px !important}
 #hh-page .hh-conf-e,.hh-conf-e{font-size:.8rem !important;gap:.18rem !important}
 #hh-page .hh-conf-e svg,.hh-conf-e svg{width:11px;height:11px}
 #hh-page .hh-conf-e b,.hh-conf-e b{margin-left:.22rem !important}
 #hh-page .hh-conf-c,.hh-conf-c{font-size:.75rem !important}
 #hh-page .hh-hl li,.hh-hl li{font-size:.82rem !important;
  padding:.3rem .62rem !important}
 /* Le texte du Hero est centre sur telephone : les puces le suivent,
    sinon la colonne part de travers. */
 #hh-page .hh-hl,.hh-hl{gap:.38rem !important;justify-content:center !important;
  margin:.85rem 0 1.35rem !important}
 #hh-page .hh-conf,.hh-conf{margin-top:1.15rem !important}}
</style>"""

ETOILE = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M12 2l2.9 6.26 6.85.78-5.09 4.64 1.4 6.74L12 17.1l-6.06 3.32 1.4-6.74'
          'L2.25 9.04l6.85-.78z"/></svg>')


def css_maxence():
    """La part « Maxence » de la feuille d'origine, sans les regles du badge."""
    i = HM.CSS.find("/* \u2500\u2500 Maxence")
    if i < 0:
        raise SystemExit("ARRET — bloc Maxence introuvable dans la feuille d'origine")
    return '<style id="hh-reassurance">\n' + HM.CSS[i:]


def mots(t):
    """Les mots d'un texte, sans balise, sans accent, sans ponctuation."""
    t = re.sub(r"<[^>]+>", " ", t)
    t = unicodedata.normalize("NFD", t)
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn").lower()
    return sorted(x for x in re.split(r"[^a-z0-9]+", t) if x)


def liste(cle):
    amorce, items = LISTES[cle]
    lis = "".join("<li>%s%s</li>" % (COCHE, x) for x in items)
    return ('<p class="hero-description">%s :</p><ul class="hh-hl">%s</ul>'
            % (amorce, lis))


def badge(note):
    return ('<div class="hh-conf">'
            '<i class="hh-tete hh-tete-g hh-conf-g" aria-hidden="true"></i>'
            '<div class="hh-conf-d">'
            '<p class="hh-conf-e">%s<b>%s</b></p>'
            '<p class="hh-conf-c">Plus de 100 clients nous font confiance</p>'
            '</div></div>' % (ETOILE * 5, note))


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        neuf = c

        # 1. la description devient une liste, sans perdre un mot
        m = re.search(r'<p class="hero-description">(.*?)</p>', neuf, re.S)
        if not m:
            raise SystemExit("ARRET — description du Hero introuvable sur %s" % url)
        # Seule la conjonction de l'enumeration a le droit de disparaitre :
        # « conditionnement ET tracabilite » devient deux puces, la
        # coordination est portee par la liste elle-meme. Tout le reste doit
        # se retrouver a l'identique — ce texte porte les mots-cles.
        LIBRE = {"et"}
        avant_mots = [x for x in mots(m.group(1)) if x not in LIBRE]
        neuve = liste(cle)
        apres_mots = [x for x in mots(neuve) if x not in LIBRE]
        if apres_mots != avant_mots:
            manque = [x for x in avant_mots if x not in apres_mots]
            ajout = [x for x in apres_mots if x not in avant_mots]
            raise SystemExit("ARRET — le texte du Hero a change sur %s\n"
                             "   disparus : %s\n   ajoutes  : %s"
                             % (url, manque, ajout))
        neuf = neuf[:m.start()] + neuve + neuf[m.end():]

        # 2. le badge : la marque Google a la place des silhouettes
        b = re.search(r'<div class="hh-conf">.*?</div>\s*</div>\s*</div>', neuf, re.S)
        if not b:
            raise SystemExit("ARRET — badge introuvable sur %s" % url)
        note = re.search(r'class="rating-text">([^<]+)<', c).group(1).strip()
        neuf = neuf[:b.start()] + badge(note) + neuf[b.end():]

        # 3. la feuille de la premiere version portait le badge ET Maxence.
        #    Le badge est refait ici ; on ne garde de l'ancienne que la part
        #    de Maxence, sinon ses regles d'hier continuent de s'appliquer.
        if '<style id="hh-hero-v2">' in neuf:
            neuf = re.sub(r'<style id="hh-hero-v2">.*?</style>', CSS, neuf, flags=re.S)
            neuf = re.sub(r'<style id="hh-reassurance">.*?</style>', css_maxence(),
                          neuf, flags=re.S)
        else:
            neuf = re.sub(r'<style id="hh-reassurance">.*?</style>',
                          CSS + css_maxence(), neuf, flags=re.S)

        if neuf.count('class="hh-conf"') != 1 or neuf.count('class="hh-hl"') != 1:
            raise SystemExit("ARRET — bloc en double sur %s" % url)
        # Le controle porte sur le Hero SEUL : la section equipe utilise la
        # meme silhouette pour ses cartes floutees, et elle n'est pas le
        # sujet ici.
        hd = neuf.find('<section class="hero-section"')
        hero = neuf[hd:neuf.find("</section>", hd)]
        if "hh-conf-t" in hero or "data:image/svg+xml" in hero:
            raise SystemExit("ARRET — il reste une silhouette dans le Hero de %s" % url)
        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        if sorted(re.findall(r'href="([^"]+)"', corps(c))) != \
           sorted(re.findall(r'href="([^"]+)"', corps(neuf))):
            raise SystemExit("ARRET — lien(s) perdu(s) sur %s" % url)
        if corps(neuf).count("<h1") != corps(c).count("<h1"):
            raise SystemExit("ARRET — le H1 a bouge sur %s" % url)

        print("%-42s %d puces · badge a la marque Google · %+d octets"
              % (url, len(LISTES[cle][1]), len(neuf) - len(c)))
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
    time.sleep(5)
    for cle, (page, url) in SY.PAGES.items():
        h = lire_page(url)
        p = len(re.findall(r'<ul class="hh-hl">', h))
        g = h.count('"hh-tete hh-tete-g hh-conf-g"')
        ok = p == 1 and g == 1 and "hh-conf-t" not in h
        print("   %-42s %s  liste %d · marque %d · silhouettes %s"
              % (url, "OK " if ok else "KO ", p, g,
                 "aucune" if "hh-conf-t" not in h else "PRESENTES"))


if __name__ == "__main__":
    main()
