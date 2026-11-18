#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le defilement colle des fonctionnalites, pose sur /negoce/.

Le deployeur ne savait pas quoi faire de cette page : il attend le module
a onglets et n'a trouve qu'une grille de cartes. Il l'a dit et n'a rien
touche — « module inconnu, laissee ». C'est le bon reflexe, mais la page
reste alors sans le module central du gabarit.

On convertit donc a la main, en reprenant ce qui existe :
  * les cinq cartes de la page donnent les titres et les puces. On ne
    reecrit rien ;
  * les ecrans viennent de la bibliotheque deja posee sur les autres
    pages — ce sont des reproductions d'interface en HTML, pas des
    images. Chacun est choisi pour la fonctionnalite qu'il montre, et
    aucun n'est utilise deux fois ici.

Les liens des cartes disparaissent avec elles : la section raconte le
produit, elle n'envoie pas ailleurs — decision du 22/09. On verifie que
chacun est cite ailleurs avant de le laisser partir.
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import ns_api                    # noqa: E402
import deployer_gabarit as D     # noqa: E402
import pilier_gabarit as P       # noqa: E402
import scroll_sticky as SY       # noqa: E402
import verifier_metiers as V     # noqa: E402

PID, URL = 5957, "/negoce/"
# Fonctionnalite de la page -> ecran de la bibliotheque, et page d'ou il vient.
ECRANS = [("Achats", "Contrôle à réception", 10868),      # /poissonnier/
          ("Stocks", "Stock consolidé", 3309),            # /boulanger/
          ("Tarifs", "Marge", 11955),                     # /fruits-et-legumes/
          ("Commandes", "Flux EDI", 2824),                # /maraicher/
          ("Traçabilité", "Traçabilité", 3309)]           # /boulanger/
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/negoce-avant")


def bibliotheque():
    """Un ecran par libelle, pris sur les pages qui le portent deja."""
    out = {}
    for _, lab, source in ECRANS:
        c = w.get_raw("pages", source)["content"]["raw"]
        _, ecrans, _ = SY.extraire_sticky(c)
        for e in ecrans:
            # Le libelle s'arrete a « de Hello Harel », pas aux deux-points :
            # sinon on capture « Contrôle a reception de Hello Harel ».
            m = re.search(r'aria-label="Reproduction de l.{1,3}écran (.+?) de Hello Harel',
                          e)
            if m and m.group(1).strip() == lab:
                out[lab] = e
                break
    manquants = [lab for _, lab, _ in ECRANS if lab not in out]
    if manquants:
        raise SystemExit("ARRET — ecran(s) introuvable(s) : %s" % manquants)
    return out


def cartes(sec):
    """Titre, puces et lien de chaque carte, dans l'ordre de la page."""
    out = []
    for m in re.finditer(r'<div class="bento-card[^"]*"', sec):
        fin = P.bornes(sec, m.start()) if False else None
        # les cartes ne s'imbriquent pas : on ferme sur le <div> equilibre
        prof, fin = 0, None
        for mm in re.finditer(r"<(/?)div\b", sec[m.start():]):
            prof += 1 if not mm.group(1) else -1
            if prof == 0:
                fin = m.start() + mm.end() + 1
                break
        if fin is None:
            raise SystemExit("ARRET — carte non fermee")
        bloc = sec[m.start():fin]
        h3 = re.search(r"<h3>(.*?)</h3>", bloc, re.S)
        if not h3:
            continue
        puces = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
                 for x in re.findall(r"<li>(.*?)</li>", bloc, re.S)]
        if not puces:
            # Quatre cartes sur cinq n'ont pas de liste, juste un paragraphe.
            # On le coupe a la phrase : ce sont les mots de la page, pas les
            # notres. Le gabarit s'adapte, le contenu ne s'invente pas.
            p = re.search(r"<p>(.*?)</p>", bloc, re.S)
            if p:
                txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", p.group(1))).strip()
                puces = [x.strip() + "." for x in txt.rstrip(".").split(". ")
                         if len(x.strip()) > 18]
        liens = re.findall(r'href="([^"]+)"', bloc)
        out.append((re.sub(r"<[^>]+>", "", h3.group(1)).strip(),
                    [x for x in puces if x], liens))
    return out


def cite_ailleurs(cible):
    n = 0
    for t in ("pages", "posts"):
        p = 1
        while True:
            lot = ns_api.call("wp/v2/%s?per_page=100&page=%d&status=publish"
                              "&_fields=id,link" % (t, p))
            if not lot:
                break
            for x in lot:
                if x["id"] == PID:
                    continue
                c = w.get_raw(t, x["id"])["content"]["raw"]
                if re.search(r'href="(?:https://www\.helloharel\.com)?%s"'
                             % re.escape(cible),
                             re.sub(r"<(style|script)[^>]*>.*?</\1>", "", c, flags=re.S)):
                    n += 1
            if len(lot) < 100:
                break
            p += 1
    return n


def main():
    poser = "--poser" in sys.argv
    c = w.get_raw("pages", PID)["content"]["raw"]
    depart = c
    i = c.find('<section class="features-section"')
    if i < 0:
        raise SystemExit("ARRET — section des fonctionnalites introuvable")
    fin = P.bornes(c, i)
    sec = c[i:fin]
    if 'class="sy-ecrans"' in sec:
        raise SystemExit("ARRET — le defilement est deja pose")

    ent = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="bento-grid">)',
                    sec, re.S)
    if not ent:
        raise SystemExit("ARRET — en-tete de section introuvable")
    lot = cartes(sec)
    if len(lot) != len(ECRANS):
        raise SystemExit("ARRET — %d carte(s) pour %d ecran(s) prevus"
                         % (len(lot), len(ECRANS)))

    bib = bibliotheque()
    contenu = [(titre, puces, None, []) for titre, puces, _ in lot]
    ecrans = [bib[lab] for _, lab, _ in ECRANS]
    c = c[:i] + SY.section(ent.group(0), ecrans, [], contenu) + c[fin:]

    # ── controles ────────────────────────────────────────────────────────
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    partis = sorted(set(D.liens(depart)) - set(D.liens(c)))
    attendus = {x for _, _, ls in lot for x in ls}
    if set(partis) - attendus:
        raise SystemExit("ARRET — lien(s) perdu(s) en trop : %s"
                         % sorted(set(partis) - attendus)[:3])
    if c.count("<section class=") != depart.count("<section class="):
        raise SystemExit("ARRET — le nombre de sections bouge")
    # « data-actif » figure sur les etapes ET sur les ecrans : le compter
    # a plat donne le double. On compte les <li> de premier niveau.
    n_pas = V.enfants_li(c, "sy-pas")
    n_ecr = V.enfants_li(c, "sy-ecrans")
    if n_pas != len(ECRANS) or n_ecr != len(ECRANS):
        raise SystemExit("ARRET — %s etape(s) et %s ecran(s) au lieu de %d"
                         % (n_pas, n_ecr, len(ECRANS)))
    if len(c) > D.PLAFOND:
        raise SystemExit("ARRET — %d o, au-dela du seuil de rendu" % len(c))

    print("%s  %d -> %d o" % (URL, len(depart), len(c)))
    for (titre, puces, _), (_, lab, src) in zip(lot, ECRANS):
        print("   %-34s %d puce(s)  ecran « %s »" % (titre[:34], len(puces), lab))
    print("\n   liens de cartes qui partent :")
    for x in partis:
        u = x.replace("https://www.helloharel.com", "")
        n = cite_ailleurs(u)
        print("      %-44s %s" % (u[:44],
                                  "cite sur %d autre(s) page(s)" % n if n
                                  else "ORPHELINE — a reloger"))
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % PID), "w",
             encoding="utf-8").write(depart)
        w.update_content("pages", PID, c, live=True)
        print("\n   pose.")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
