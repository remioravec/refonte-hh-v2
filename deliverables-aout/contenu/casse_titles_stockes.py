#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T12, premier temps — les 13 titles dont la CASSE EST FAUSSE EN BASE.

Sur les 39 titles servis en casse anglaise, 26 sont corrects en base : c'est
le réglage Rank Math « Capitalize Titles » qui les capitalise à la sortie, et
il se décoche en un clic (voir la roadmap). Les 13 ci-dessous, en revanche,
sont stockés capitalisés : décocher le réglage ne les corrigerait pas. Ils
sont réécrits ici, à l'identique au mot près, seule la casse change.

/migration-as400/ n'y figure pas : son stocké est correct, et son rendu est
figé par l'extrait « Casse française des titles » (Règle 0).
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

LARGE = set("mwMW—…")
px = lambda s: round(sum(11.0 if c in LARGE else (8.0 if c.isalnum() else 5.5) for c in s))

# id -> (champ, nouveau title). « rm » = rank_math_title, « post » = titre du post.
T = {
    2:     ('rm',   "ERP agroalimentaire • Agile et sur-mesure • 200+ PME"),
    10865: ('rm',   "Logiciel et ERP pâtisserie • Prix de revient et marge"),
    7766:  ('rm',   "Calcul coût de revient • Logiciel agroalimentaire • Guide"),
    8112:  ('rm',   "Calcul freinte charcuterie • Perte de séchage • Logiciel"),
    5287:  ('rm',   "ERP pour PME • Simple et rentable • Guide complet 2026"),
    7944:  ('rm',   "Logiciel coût de revient traiteur • Marge par plat"),
    7769:  ('rm',   "Remplacer Excel en agroalimentaire • Migration ERP"),
    7761:  ('rm',   "Traçabilité lot et DLC • Logiciel de suivi • Guide 2026"),
    7911:  ('rm',   "Logiciel devis, commande et bon de livraison • ERP"),
    7910:  ('rm',   "Planification de production ERP • CBN et ordonnancement"),
    5969:  ('post', "Implantation Hauts-de-France"),
    5968:  ('post', "Implantation Île-de-France"),
    608:   ('rm',   "Tarifs ERP agro • Transparent et sans engagement • 99 €"),
}


def main(ecrire=False):
    for pid, (champ, titre) in T.items():
        p = px(titre)
        hors = '' if 200 <= p <= 561 else '  <-- HORS BORNES'
        print(f'{pid:6} {champ:5} {p:4} px{hors}  {titre}')
        if hors:
            continue
        if not ecrire:
            continue
        if champ == 'rm':
            n.call('rankmath/v1/updateMeta', 'POST', {
                'objectID': pid, 'objectType': 'post',
                'meta': {'rank_math_title': titre}})
        else:
            base = 'pages'
            n.call(f'wp/v2/{base}/{pid}', 'POST', {'title': titre})
    print(f'\n{len(T)} titles traités')


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
