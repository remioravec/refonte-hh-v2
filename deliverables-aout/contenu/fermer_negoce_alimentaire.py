#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fermeture de /agroalimentaire/negoce-alimentaire/ apres unification sur /negoce/.

  1. 301 de l'ancienne URL vers /negoce/ (snippet 8, deja en place)
  2. la redirection /erp-grossiste/ qui pointait sur l'ancienne URL est retargetee
     pour ne pas creer de chaine 301 -> 301
  3. l'ancienne page passe en brouillon : elle sort du sitemap
  4. le title fige du snippet 12 est retire pour 10934, pose pour 5957
  5. les liens internes qui pointaient sur l'ancienne URL sont retargetes,
     SAUF sur les cinq pages protegees (regle 0), qui sont listees pour arbitrage

Usage :  python3 fermer_negoce_alimentaire.py            (essai a blanc)
         python3 fermer_negoce_alimentaire.py --live     (ecriture)
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import wp_common as w   # noqa: E402
import ns_api          # noqa: E402

LIVE = "--live" in sys.argv
ANCIENNE = "/agroalimentaire/negoce-alimentaire/"
NOUVELLE = "/negoce/"
SOURCE = 10934
PORTEUSE = 5957
PROTEGEES = {1726, 2818, 2839, 5477, 11162}
TITLE = "ERP Négoce Alimentaire • Poids Réel, DLC, Marge Grossiste"


def maj_snippet(sid, avant, apres, libelle):
    s = ns_api.call("code-snippets/v1/snippets/%d" % sid)
    code = s["code"]
    if avant not in code:
        print("   ! %s : motif introuvable dans le snippet %d" % (libelle, sid))
        return None
    neuf = code.replace(avant, apres)
    print("   · %s" % libelle)
    if LIVE:
        s["code"] = neuf
        ns_api.call("code-snippets/v1/snippets/%d" % sid, "POST", s)
    return neuf


def main():
    print("1. redirections (snippet 8)")
    maj_snippet(8,
                '"/erp-grossiste/" => "%s",' % ANCIENNE,
                '"/erp-grossiste/" => "%s",\n            "%s" => "%s",'
                % (NOUVELLE, ANCIENNE.rstrip("/") + "/", NOUVELLE),
                "301 de l'ancienne URL + /erp-grossiste/ retargete sans chaine")

    print("\n2. title fige (snippet 12)")
    maj_snippet(12,
                "\t\t10934 => 'ERP Négoce Alimentaire • Poids Réel, DLC et Marge Grossiste',\n",
                "",
                "entree 10934 retiree (la page est fermee)")
    maj_snippet(12,
                "\t\t5957  => 'ERP Négoce • Achats, Stocks, Ventes et Tarifs',",
                "\t\t5957  => '%s'," % TITLE,
                "title de /negoce/ aligne sur la page unifiee")

    print("\n3. liens internes entrants")
    inv = json.load(open("/tmp/claude-0/-home-user-refonte-hh-v2/"
                         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/inventaire.json"))
    touches, differes = [], []
    for pt, pid, lien in inv:
        if pid in (SOURCE,):
            continue
        c = w.get_raw(pt, pid)["content"]["raw"]
        n = len(re.findall(r'href="(?:https://www\.helloharel\.com)?%s"' % ANCIENNE, c))
        if not n:
            continue
        if pid in PROTEGEES:
            differes.append((pid, lien, n))
            continue
        neuf = re.sub(r'href="(?:https://www\.helloharel\.com)?%s"' % ANCIENNE,
                      'href="%s"' % NOUVELLE, c)
        touches.append((pt, pid, lien, n))
        if LIVE:
            w.update_content(pt, pid, neuf, live=True)

    for pt, pid, lien, n in touches:
        print("   · %-6s %-2d %s" % (pid, n, lien))
    print("   %d contenus retargetes" % len(touches))
    if differes:
        print("\n   REGLE 0 — non touchees, a arbitrer :")
        for pid, lien, n in differes:
            print("     %-6s %-2d %s" % (pid, n, lien))

    print("\n4. ancienne page en brouillon")
    if LIVE:
        w.api("pages/%d" % SOURCE, "POST", {"status": "draft"})
        print("   · page %d passee en brouillon" % SOURCE)
    else:
        print("   · (essai a blanc)")

    if not LIVE:
        print("\nESSAI A BLANC — rien n'a ete ecrit.")


if __name__ == "__main__":
    main()
