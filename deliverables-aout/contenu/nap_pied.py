#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le NAP dans le pied de page, sur toutes les pages du site.

NAP : Name, Address, Phone. Aujourd'hui le pied de page n'en porte AUCUN —
ni raison sociale, ni adresse, ni telephone. L'adresse n'apparait que sur
trois pages (contact, CGU, mentions legales) et le telephone sur dix.
Pour un moteur, l'etablissement n'est identifie nulle part ailleurs que
dans le balisage.

LES VALEURS POSEES sont celles des mentions legales de la societe, pas des
valeurs choisies : raison sociale, adresse, telephone, TVA et SIREN y
figurent deja. Le SIREN est deduit du numero de TVA intracommunautaire
(les neuf derniers chiffres), ce qui est une regle de calcul, pas une
invention.

CE QUI N'EST PAS POSE : l'adresse electronique. Le site en affiche deux —
contact@helloharel.com sur onze pages, support@helloharel.com dans les
mentions legales et dans le balisage. Choisir l'une reviendrait a trancher
a la place de l'entreprise ; l'ecart est signale, pas arbitre.

Les cinq pages de la regle 0 sont exclues : y ajouter un bloc touche a leur
structure, et la regle ne l'autorise que pour reparer un defaut.

Usage :  python3 nap_pied.py            (blanc)
         python3 nap_pied.py --poser    (ecrit)
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

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/nap-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

RAISON = "Harel Systems SAS"
RUE = "6 avenue de Rueil"
CP_VILLE = "92420 Vaucresson"
PAYS = "France"
TEL_AFFICHE = "06 18 06 00 18"
TEL_LIEN = "+33618060018"
TVA = "FR87799992102"
SIREN = TVA[2:].lstrip("0")[:9] if False else "799992102"

CSS = """<style id="hh-nap">
#hh-page .hh-nap,.hh-nap,footer .hh-nap{margin:1rem 0 0 !important;
 padding-top:.9rem !important;border-top:1px solid rgba(255,255,255,.12) !important;
 font-size:.82rem !important;line-height:1.65 !important;
 color:rgba(255,255,255,.72) !important;font-style:normal !important}
footer .hh-nap b,.hh-nap b{display:block !important;color:#fff !important;
 font-weight:700 !important;font-size:.88rem !important;margin-bottom:.15rem !important}
footer .hh-nap a,.hh-nap a{color:#fff !important;text-decoration:none !important;
 font-weight:600 !important}
footer .hh-nap a:hover,.hh-nap a:hover{text-decoration:underline !important}
footer .hh-nap span,.hh-nap span{display:block !important}
footer .hh-nap .hh-nap-id,.hh-nap .hh-nap-id{margin-top:.45rem !important;
 font-size:.74rem !important;color:rgba(255,255,255,.5) !important}
</style>"""

BLOC = ('<address class="hh-nap">'
        '<b>%s</b>'
        '<span>%s</span><span>%s, %s</span>'
        '<span>Tél. <a href="tel:%s">%s</a></span>'
        '<span class="hh-nap-id">SIREN %s · TVA %s</span>'
        '</address>' % (RAISON, RUE, CP_VILLE, PAYS, TEL_LIEN, TEL_AFFICHE, SIREN, TVA))


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    print("NAP pose :", RAISON, "·", RUE, CP_VILLE, "·", TEL_AFFICHE,
          "· SIREN", SIREN, "· TVA", TVA, "\n")

    pages, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/pages?per_page=100&page=%d&status=publish&_fields=id,link" % p)
        if not lot:
            break
        pages += lot
        if len(lot) < 100:
            break
        p += 1

    faits = exclus = sans = deja = 0
    sans_liste = []
    for x in sorted(pages, key=lambda t: t["link"]):
        pid = x["id"]
        url = x["link"].replace("https://www.helloharel.com", "") or "/"
        if pid in PROTEGEES:
            exclus += 1
            continue
        c = w.get_raw("pages", pid)["content"]["raw"]
        if 'class="hh-nap"' in c:
            deja += 1
            continue
        m = re.search(r'(<div class="footer-brand">.*?)(</div>\s*<div class="footer-col">)',
                      c, re.S)
        if not m:
            # Ces pages n'embarquent pas de pied : elles utilisent celui du
            # theme, hors de portee du contenu. Elles sont listees pour que
            # le NAP y soit pose par ailleurs.
            sans += 1
            sans_liste.append(url)
            continue
        neuf = c[:m.end(1)] + BLOC + c[m.end(1):]
        if '<style id="hh-nap">' not in neuf:
            neuf += CSS
        if D.solde(neuf) != D.solde(c):
            print("%-44s REFUSEE — le solde des <div> bouge" % url[:44])
            continue
        # Le bloc ajoute UN lien tel: ; plusieurs pages en portaient deja un.
        # On en retire donc exactement une occurrence, pas toutes.
        av, ap = D.liens(c), list(D.liens(neuf))
        if ("tel:" + TEL_LIEN) in ap:
            ap.remove("tel:" + TEL_LIEN)
        if sorted(av) != sorted(ap):
            manque = sorted(set(av) - set(ap))
            print("%-44s REFUSEE — lien(s) perdu(s) %s" % (url[:44], manque[:2]))
            continue
        faits += 1
        if poser:
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(c)
            w.update_content("pages", pid, neuf, live=True)
    print("%d page(s) traitees · %d deja faites · %d exclues (regle 0)"
          % (faits, deja, exclus))
    if sans_liste:
        print("\n%d page(s) au pied du theme, a traiter autrement :" % len(sans_liste))
        for u in sans_liste:
            print("   %s" % u)
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
