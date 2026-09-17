#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cree les trois landings de septembre, sur le gabarit des fiches metier.

GABARIT — clone de /agroalimentaire/fromager/ (10867), non protegee et deja
convertie au module a onglets. On ne recopie pas un gabarit de memoire : on
part de la page reelle et on remplace cinq blocs.

CE QUI EST REMPLACE — la photo et le texte du hero, le module a onglets avec
ses cinq ecrans, la FAQ, et le titre de la page. Tout le reste du gabarit
(logos, about, process, metiers, equipe, avis) est conserve tel quel.

Les pages sont creees en BROUILLON. Rien n'est publie sans relecture.

Usage :  python3 creer_landings.py            (essai a blanc)
         python3 creer_landings.py --live     (creation en brouillon)
"""

import base64
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402
import agro_ui as UI                        # noqa: E402
import bento_toggles as BT                  # noqa: E402
import landings_sept as L                   # noqa: E402

LIVE = "--live" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
MODELE = 10867                              # /agroalimentaire/fromager/
PARENT = 1726                               # /agroalimentaire/


def televerser(chemin, nom, alt):
    import urllib.request
    req = urllib.request.Request(
        "%s/wp-json/wp/v2/media" % w.SITE, data=open(chemin, "rb").read(), method="POST",
        headers={"Authorization": w._auth_header(), "Content-Type": "image/webp",
                 "Content-Disposition": 'attachment; filename="%s.webp"' % nom})
    with urllib.request.urlopen(req, timeout=300, context=w._CTX) as r:
        m = json.loads(r.read().decode())
    w.api("media/%d" % m["id"], "POST", {"alt_text": alt, "caption": "Photo Pexels"})
    return m["source_url"]


def remplacer_section(c, cls, neuf):
    i = c.find('<section class="%s"' % cls)
    if i < 0:
        raise ValueError("section %s introuvable" % cls)
    j = c.find("</section>", i)
    if j < 0 or "<section" in c[i + 10:j]:
        raise ValueError("borne de fin incertaine sur %s" % cls)
    return c[:i] + neuf + c[j + len("</section>"):]


def hero(v, photo_url):
    return (
        '<section class="hero-section" style="background:linear-gradient('
        'rgba(0,50,80,0.55),rgba(0,100,160,0.6)),url(\'%s\') center/cover no-repeat;">'
        '<div class="container"><div class="hero-grid"><div class="hero-text">'
        '<div class="hero-badge"><span class="dot"></span>%s</div>'
        '<h1 class="hero-title" style="color:#fff">%s '
        '<span class="accent" style="color:#60a5fa">%s</span></h1>'
        '<p class="hero-description">%s</p>'
        '<div class="hero-ctas">'
        '<a href="/contact/" class="hero-cta-primary" style="background:#22C55E !important;'
        'border-color:#22C55E !important;color:#fff !important;">Demander une démo</a>'
        '<a href="/contact/" class="hero-cta-secondary" style="color:#fff !important;'
        'border-color:#fff !important;">Essayez</a></div>'
        '<p class="hero-cta-sub">Sans engagement. Déploiement clé en main.</p>'
        '</div><div class="hero-image-spacer"></div></div></div></section>'
        % (photo_url, v["badge"], v["h1"], v["h1_accent"], v["chapo"]))


ANCRES = {
 "/negoce/": "ERP négoce alimentaire",
 "/negoce/tracabilite-lots/": "traçabilité des lots",
 "/negoce/achats-approvisionnements/": "achats et approvisionnements",
 "/negoce/stocks-multi-depots/": "stocks multi-dépôts",
 "/agroalimentaire/": "ERP agroalimentaire",
 "/agroalimentaire/maraicher/": "ERP maraîcher",
 "/agroalimentaire/poissonnier/": "ERP poissonnerie",
 "/fonctionnalites/gestion-de-stock/": "gestion des stocks",
 "/fonctionnalites/fabrication/": "gestion de la fabrication",
 "/fonctionnalites/facturation/": "gestion de la facturation",
 "/tarifs/": "nos tarifs",
}


def module(cle, v):
    """Le module a onglets, avec les liens du plan poses en pied de panneau."""
    entete = ('<div class="section-header"><p class="overline">%s</p><h2>%s</h2>'
              '<p>%s</p></div>' % (v["overline"], v["h2"], v["sous_titre"]))
    # un lien par panneau, dans l'ordre du plan ; le reste va sur le dernier.
    liens = list(v["liens"])
    par_panneau = [[] for _ in v["fonctions"]]
    for k, u in enumerate(liens):
        par_panneau[min(k, len(par_panneau) - 1)].append(u)
    blocs, courts = [], []
    for k, (((titre, chapo, puces), nom)) in enumerate(zip(v["fonctions"], L.ECRANS[cle])):
        lien = "".join('<a class="hhf-lien" href="%s">%s →</a>'
                       % (u, ANCRES.get(u, u.strip("/").split("/")[-1].replace("-", " ")))
                       for u in par_panneau[k])
        blocs.append((titre, chapo, puces, BT.ECRANS[nom][0], lien))
        courts.append(BT.court(titre))
    return UI.section(entete, blocs, courts)


def faq(v):
    q = "".join('<details class="minq"><summary>%s</summary><div><p>%s</p></div></details>'
                % (a, b) for a, b in v["faq"])
    return ('<section class="faq-section"><div class="container">'
            '<div class="section-header"><p class="overline">FAQ</p>'
            '<h2>Questions fréquentes</h2></div>'
            '<div class="hha-art">' + q + '</div></div></section>')


FAQ_CSS = """<style id="hh-landing-faq">
#hh-page .minq,.minq{border:1px solid #e2e8f0;border-radius:14px;margin:0 auto .7rem !important;
 background:#fff;overflow:hidden;max-width:860px}
#hh-page .minq summary,.minq summary{cursor:pointer;padding:1rem 1.15rem;font-weight:600;
 color:#0f172a;list-style:none;display:flex;justify-content:space-between;gap:1rem;align-items:center}
#hh-page .minq summary::-webkit-details-marker{display:none}
#hh-page .minq summary::after,.minq summary::after{content:"+";color:#0079B8;font-size:1.25rem;
 font-weight:400;flex:0 0 auto}
#hh-page .minq[open] summary::after,.minq[open] summary::after{content:"−"}
#hh-page .minq summary:focus-visible{outline:2px solid #0f172a;outline-offset:-2px}
#hh-page .minq div,.minq div{padding:0 1.15rem 1.1rem}
#hh-page .minq div p,.minq div p{margin:0 !important;color:#475569;line-height:1.65}
#hh-page .minq a,.minq a{color:#046C93;text-decoration:underline}
</style>"""


def main():
    base = w.get_raw("pages", MODELE)["content"]["raw"]
    print("modele %d lu : %d octets\n" % (MODELE, len(base)))
    pb = []
    for cle, v in L.PAGES.items():
        pid, nom, alt = v["photo"]
        f = "%s/%s.webp" % (S, nom)
        if not os.path.exists(f):
            pb.append("%s : photo absente" % cle); continue

        url_photo = "https://www.helloharel.com/PHOTO-%s.webp" % nom
        if LIVE:
            url_photo = televerser(f, nom, alt)

        c = base
        c = remplacer_section(c, "hero-section", hero(v, url_photo))
        c = remplacer_section(c, "features-section", module(cle, v))
        c = remplacer_section(c, "faq-section", faq(v))
        # la section de maj propre au fromager n'a rien a faire ici
        i = c.find('<section class="hh-maj-aout-fromager"')
        if i >= 0:
            j = c.find("</section>", i)
            c = c[:i] + c[j + 10:]
        if "hh-landing-faq" not in c:
            c += FAQ_CSS

        # ---- controles
        # ATTENTION — ce controle porte sur le CONTENU, pas sur la page rendue.
        # Il ne voit pas ce que le theme ajoute autour : c'est exactement ce qui
        # a laisse passer le second H1. Le controle qui compte est celui de la
        # page en ligne.
        d = []
        if c.count("<h1") != 1:
            d.append("%d H1" % c.count("<h1"))
        if c.count('name="hhf-onglet"') != 5:
            d.append("%d onglets" % c.count('name="hhf-onglet"'))
        if c.count('class="hhf-shot"') != 5:
            d.append("%d ecrans" % c.count('class="hhf-shot"'))
        for u in v["liens"]:
            if ('href="%s"' % u) not in c:
                d.append("lien du plan absent : %s" % u)
        i0 = c.find('<section class="hero-section"')
        i1 = c.find("</section>", c.find('<section class="features-section"'))
        zone = c[i0:i1].lower() if i0 >= 0 and i1 > i0 else ""
        if "fromag" in zone:
            d.append("le mot fromager subsiste dans le hero ou le module")
        if d:
            pb.append("%s : %s" % (cle, " · ".join(d)))
            print("  ! %-20s %s" % (cle, " · ".join(d)))
            continue

        print("  · %-20s %d octets · 5 onglets · %d FAQ · photo %s"
              % (cle, len(c), len(v["faq"]), "en ligne" if LIVE else "(à téléverser)"))
        open("%s/landing-%s.html" % (S, cle), "w", encoding="utf-8").write(c)

        if LIVE:
            # le gabarit « elementor_canvas » est ce qui retire l'habillage du
            # theme. Sans lui, WordPress ajoute son propre <h1 class="entry-title">
            # au-dessus du contenu : la page sort avec DEUX H1.
            r = w.api("pages", "POST", {
                "title": v["titre_page"], "slug": cle, "parent": PARENT,
                "template": "elementor_canvas",
                "status": "draft", "content": c})
            print("      creee en brouillon : id %d — %s" % (r["id"], r["link"]))

    if pb:
        print("\nrefus :")
        for x in pb:
            print("   !", x)
    elif not LIVE:
        print("\nessai a blanc : les trois pages sont pretes. Relancer avec --live.")


if __name__ == "__main__":
    main()
