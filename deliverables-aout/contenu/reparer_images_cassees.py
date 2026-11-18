#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cinq images cassées sur quatre pages — trouvées en faisant T14.

Trois fichiers référencés dans le contenu répondent 404 :

    timothy-jollivet-hello-harel.jpg        3 pages  — l'avatar de la signature
    Logiciel-Gestion-des-stocks.png         1 page
    Page-Daccueil-Hello-Harel-1024x548.png  1 page

L'avatar est le plus coûteux : il est appelé par la signature de
/fonctionnalites/facturation-automatique-bon-livraison/ et des DEUX pages
comparatives. Les trois pages affichaient une image cassée sous le nom de
l'auteur, là où le lecteur cherche la preuve d'expertise.

Réparations :
  - l'avatar pointe vers le fichier WebP de Timothy déjà présent dans la
    médiathèque ;
  - « Logiciel Gestion des stocks » pointe vers la capture de gestion de
    stock convertie en WebP par T14 — même sujet, même alt ;
  - la capture de page d'accueil est RETIRÉE avec sa <figure> : aucune image
    équivalente en médiathèque, et une figure vide dans un article sur la
    variation de stock n'apporte rien.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

SITE = 'https://www.helloharel.com'
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-cassees')
AVATAR = SITE + '/wp-content/uploads/2026/08/Timothy-Jolliver-President-de-Hello-Harel-150x150-1.webp'


def figure_autour(c, i):
    """Bornes de la <figure> qui contient la position i, par comptage équilibré."""
    debut = c.rfind('<figure', 0, i)
    if debut < 0:
        return None
    p = 0
    for t in re.finditer(r'<figure\b|</figure>', c[debut:]):
        p += 1 if t.group(0) != '</figure>' else -1
        if p == 0:
            fin = debut + t.end()
            return (debut, fin) if debut < i < fin else None
    return None


def main(ecrire=False):
    os.makedirs(SAUVE, exist_ok=True)
    table = json.load(open('/tmp/t/table-webp.json'))
    stocks = next((v for k, v in table.items()
                   if 'Hello-Harel-Gestion-des-stocks' in k), None)
    if not stocks:
        raise RuntimeError('le WebP de Hello-Harel-Gestion-des-stocks est introuvable '
                           'dans la table de conversion')
    print('avatar  ->', AVATAR)
    print('stocks  ->', stocks)

    remplacements = [
        (re.compile(r'(?:' + re.escape(SITE) + r')?/wp-content/uploads/2025/03/'
                    r'timothy-jollivet-hello-harel\.jpg'), AVATAR),
        (re.compile(r'(?:' + re.escape(SITE) + r')?/wp-content/uploads/2024/02/'
                    r'Logiciel-Gestion-des-stocks\.png'), stocks),
    ]
    A_RETIRER = re.compile(r'(?:' + re.escape(SITE) + r')?/wp-content/uploads/2024/06/'
                           r'Page-Daccueil-Hello-Harel(?:-\d+x\d+)?\.png')

    cibles = {('pages', 7905), ('pages', 7921), ('pages', 7922), ('posts', 2955)}
    for base, pid in sorted(cibles):
        d = n.call(f'wp/v2/{base}/{pid}?context=edit&_fields=id,link,content,meta')
        if d['meta'].get('_elementor_data') not in ('', '[]', None):
            print(f'  IGNORÉE (elementor non vide) {base}/{pid}')
            continue
        c = d['content']['raw']
        open(os.path.join(SAUVE, f'{base}-{pid}.html'), 'w').write(c)
        c2 = c
        for rx, neuf in remplacements:
            c2 = rx.sub(neuf, c2)
        # la figure cassée, retirée en entier
        while True:
            m = A_RETIRER.search(c2)
            if not m:
                break
            b = figure_autour(c2, m.start())
            if not b:
                # pas dans une <figure> : on retire juste la balise <img>
                i = c2.rfind('<img', 0, m.start())
                j = c2.find('>', m.end())
                if i < 0 or j < 0:
                    raise RuntimeError('référence cassée hors <img>, à voir à la main')
                c2 = c2[:i] + c2[j + 1:]
                continue
            c2 = c2[:b[0]] + c2[b[1]:]
        if c2 == c:
            print(f'  rien à faire  {base}/{pid}')
            continue
        assert len(c2) <= len(c) + 500
        assert not A_RETIRER.search(c2)
        print(f'  {base}/{pid:6} {len(c):7} -> {len(c2):7}  {d["link"]}')
        if ecrire:
            n.call(f'wp/v2/{base}/{pid}', 'POST', {'content': c2})
    print('\nfini')


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
