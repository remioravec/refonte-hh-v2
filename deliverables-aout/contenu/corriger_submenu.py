#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le sous-menu mobile etait plafonne : seize metiers dans le code, huit a l'ecran.

MESURE DU 17/09/2026, sous Chromium a 390 px, sur la page en ligne :
  Fonctionnalites ... 416 px de haut, 8 liens sur 8 visibles ;
  Industries ....... 951 px de haut, plafonnes a 500, 8 liens sur 16 visibles.

La cause : .mobile-submenu.open { max-height: 500px !important } avec
overflow:hidden. Le plafond suffisait pour l'ancien menu a sept metiers ; il
ne suffit plus a seize. Les liens sont bien dans le document — donc le
controle precedent, qui comptait dans le code, ne voyait rien. Il ne comptait
pas la bonne chose.

CORRECTIF — le plafond passe a 1200 px, soit 951 px mesures plus une marge.
Une seule declaration change, dans la feuille inline de chaque contenu. La
transition est conservee.

Usage :  python3 corriger_submenu.py            (essai a blanc)
         python3 corriger_submenu.py --live     (ecriture)
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402

LIVE = "--live" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"

AVANT = ".mobile-submenu.open,\n.mobile-submenu.open {\n  max-height: 500px !important;\n}"
MOTIF = re.compile(r'(\.mobile-submenu\.open,\s*\.mobile-submenu\.open\s*\{\s*max-height:\s*)'
                   r'(\d+)px(\s*!important;\s*\})')
PLANCHER = 1200


def main():
    inv = json.load(open(os.path.join(S, "inventaire-menu.json")))
    cibles = [x for x in inv if x["nav"] and x["mobile"] and not x["elementor"]]
    print("%d contenus · mode %s\n" % (len(cibles), "ECRITURE" if LIVE else "essai a blanc"))

    faits, refus, deja = 0, [], []
    for x in cibles:
        kind, pid = x["kind"], x["id"]
        url = x["link"].replace("https://www.helloharel.com", "")
        try:
            p = w.get_raw(kind, pid)
            c = p["content"]["raw"]
            el = (p.get("meta", {}).get("_elementor_data") or "").strip()
            if el not in ("", "[]", "[ ]", "null"):
                raise ValueError("contenu Elementor")
            m = MOTIF.search(c)
            if not m:
                raise ValueError("regle .mobile-submenu.open introuvable")
            if len(MOTIF.findall(c)) != 1:
                raise ValueError("regle trouvee %d fois" % len(MOTIF.findall(c)))
            actuel = int(m.group(2))
            if actuel >= PLANCHER:
                deja.append((kind, pid, url, actuel))
                continue
            n = c[:m.start()] + m.group(1) + "%dpx" % PLANCHER + m.group(3) + c[m.end():]
            if abs(len(n) - len(c)) > 3:
                raise ValueError("delta inattendu : %d octets" % (len(n) - len(c)))
            if n.count("<h1") != c.count("<h1") or n.count("<section") != c.count("<section"):
                raise ValueError("empreinte modifiee")
        except Exception as e:
            refus.append((kind, pid, url, str(e)))
            continue

        if LIVE:
            w.api("%s/%d" % (kind, pid), "POST", {"content": n})
            c2 = w.get_raw(kind, pid)["content"]["raw"]
            if "max-height: 1200px !important" not in c2:
                refus.append((kind, pid, url, "RELECTURE : plafond absent en base"))
                continue
        faits += 1
        if faits % 25 == 0:
            print("   %d / %d" % (faits, len(cibles)), flush=True)

    print("\n%s : %d contenus" % ("corriges" if LIVE else "prets", faits))
    print("deja au-dessus du plancher : %d" % len(deja))
    for k, i, u, v in deja:
        print("   . %-6s %-6s %-44s deja a %d px" % (k, i, u[:44], v))
    for k, i, u, e in refus:
        print("   ! %-6s %-6s %-44s %s" % (k, i, u[:44], e))


if __name__ == "__main__":
    main()
