#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dix pages d'implantation servaient un title fautif.

Trouvé en vérifiant T11/T12. Trois défauts cumulés :
  - les noms de région sont mal écrits : « Auvergne Rhone Alpes », « Ile De
    France », « Nouvelle Aquitaine », « Reunion », « Hauts De France » —
    ni accents ni traits d'union ;
  - « Implantation Belgique » ne correspond à aucune requête : le title ne
    porte pas l'expression que quelqu'un taperait (Règle 1) ;
  - /implantations/ servait un title de 186 px, sous le plancher de 200 px.

Seuls les titles sont touchés ici. Les DESCRIPTIONS de ces dix pages restent
quasi identiques entre elles — même phrase, seul le nom de la région change —
et ce n'est pas un problème de balise : ces pages locales sont minces, elles
se corrigent par du contenu local réel, pas par dix variantes de la même
phrase. Le sujet part en ligne de roadmap contenu.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

LARGE = set("mwMW—…")
px = lambda s: round(sum(11.0 if c in LARGE else (8.0 if c.isalnum() else 5.5) for c in s))

T = {
 '/implantations/':                     "ERP agroalimentaire • Nos implantations en France",
 '/implantation-ile-de-france/':        "ERP agroalimentaire en Île-de-France",
 '/implantation-hauts-de-france/':      "ERP agroalimentaire en Hauts-de-France",
 '/implantation-bretagne/':             "ERP agroalimentaire en Bretagne",
 '/implantation-nouvelle-aquitaine/':   "ERP agroalimentaire en Nouvelle-Aquitaine",
 '/implantation-occitanie/':            "ERP agroalimentaire en Occitanie",
 '/implantation-auvergne-rhone-alpes/': "ERP agroalimentaire en Auvergne-Rhône-Alpes",
 '/implantation-belgique/':             "ERP agroalimentaire en Belgique",
 '/implantation-maurice/':              "ERP agroalimentaire à Maurice",
 '/implantation-reunion/':              "ERP agroalimentaire à La Réunion",
}


def resoudre(url):
    slug = [x for x in url.strip('/').split('/') if x][-1]
    for base in ('pages', 'posts'):
        d = n.call(f'wp/v2/{base}?slug={slug}&_fields=id,link')
        for p in d:
            if p['link'].replace('https://www.helloharel.com', '').rstrip('/') == url.rstrip('/'):
                return base, p['id']
        if d:
            return base, d[0]['id']
    raise RuntimeError(url)


def main(ecrire=False):
    for u, t in T.items():
        p = px(t)
        hors = '' if 200 <= p <= 561 else '  <-- HORS BORNES'
        print(f'{p:4} px{hors}  {u:42} {t}')
        if hors:
            continue
        if ecrire:
            base, pid = resoudre(u)
            n.call('rankmath/v1/updateMeta', 'POST', {
                'objectID': pid, 'objectType': 'post',
                'meta': {'rank_math_title': t}})


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
