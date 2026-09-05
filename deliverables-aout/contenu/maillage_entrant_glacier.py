#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maillage entrant vers /agroalimentaire/glacier/.

Une page sans lien entrant editorial n'existe pas : le carrousel « Nos secteurs
d'expertise » pointe deja vers Glacier depuis 20 pages, mais c'est de la
navigation, pas du maillage. On pose ici deux ancres editoriales exactes depuis
les deux pages thematiquement les plus proches, dans leur ligne « A approfondir »
existante — donc sans ajouter de bloc etranger au gabarit.

Regle 2 : ancre exacte, expression contigue, jamais neutre.
Regle 0 : aucune des deux pages n'est protegee.

Usage :  python3 maillage_entrant_glacier.py [--live]
"""
import os
import re
import sys

sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import wp_common as w

LIVE = "--live" in sys.argv
LIEN = '<a href="/agroalimentaire/glacier/">ERP glacier</a>'

# page : (id, fin de phrase actuelle, fin de phrase visee)
CIBLES = {
    "patissier": (10865,
                  '<a href="/agroalimentaire/boulanger/">ERP boulangerie</a>.',
                  '<a href="/agroalimentaire/boulanger/">ERP boulangerie</a>, ' + LIEN + '.'),
    "industrie-laitiere": (5470,
                           '<a href="/agroalimentaire/fromager/">ERP fromager</a>.',
                           '<a href="/agroalimentaire/fromager/">ERP fromager</a>, ' + LIEN + '.'),
}


def main():
    for nom, (pid, avant, apres) in CIBLES.items():
        c = w.get_raw("pages", pid)["content"]["raw"]
        if '/agroalimentaire/glacier/">ERP glacier' in c:
            print("  %-20s deja fait" % nom)
            continue
        if avant not in c:
            print("  %-20s ATTENDU INTROUVABLE : %r" % (nom, avant[:60]))
            continue
        neuf = c.replace(avant, apres, 1)
        n = len(re.findall(r'href="/agroalimentaire/glacier/"', neuf)) - \
            len(re.findall(r'href="/agroalimentaire/glacier/"', c))
        if n != 1:
            print("  %-20s ecart inattendu (%d liens ajoutes)" % (nom, n))
            continue
        if neuf.count("<div") != c.count("<div") or neuf.count("</div>") != c.count("</div>"):
            print("  %-20s desequilibre des div, abandon" % nom)
            continue
        if LIVE:
            w.update_content("pages", pid, neuf, live=True)
            print("  %-20s ancre « ERP glacier » posee (page %d)" % (nom, pid))
        else:
            print("  %-20s pret : +1 ancre « ERP glacier » (page %d)" % (nom, pid))


if __name__ == "__main__":
    main()
