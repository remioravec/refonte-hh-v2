#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cinq pages /fonctionnalites/ servaient le balisage des sections « métiers » et
« équipe » SANS la feuille de style qui va avec.

CE QUE ÇA DONNAIT SUR MOBILE. Les SVG inline n'avaient plus de taille : la
flèche d'une carte métier et le logo LinkedIn d'un membre d'équipe
s'affichaient en pleine largeur d'écran. Les cartes perdaient leur grille :
« Timothy » et « Gérant » se suivaient sur la même ligne, sans espace, et le
rail ne défilait pas.

CE QUI MANQUAIT, mesuré en comparant le markup au CSS servi : les classes
.eq-c, .eq-rail, .eq-av, .eq-plus et .mt-v sont utilisées par le balisage et
absentes de toutes les balises <style> de la page. Les 36 autres pages du même
gabarit les ont. Ces cinq-là n'ont que le bloc de base, qui date d'avant la
refonte du rail d'équipe et du carrousel métiers.

CORRECTION : les trois blocs <style> manquants sont recopiés depuis
/agroalimentaire/boulanger/, à l'octet près, et posés au même endroit que
chez elle — les deux blocs du carrousel juste avant <section
class="metiers-section">, le bloc du rail d'équipe juste avant <section
class="team-section">.

GARDE-FOUS : sauvegarde avant écriture, refus si _elementor_data n'est pas
vide, refus si une page porte déjà l'un des sélecteurs, refus si un ancrage
est introuvable, et contrôle qu'aucune page ne dépasse le plafond de rendu.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

MODELE = 3309          # /agroalimentaire/boulanger/
CIBLES = [7905, 7909, 7910, 7911, 7912]
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-css-fonctions')
PLAFOND = 275_000

SELECTEURS = ('.eq-c', '.eq-rail', '.eq-av', '.eq-plus', '.mt-v')


def blocs_style(contenu):
    return [(m.start(), m.end(), m.group(0), m.group(1))
            for m in re.finditer(r'(?is)<style[^>]*>(.*?)</style>', contenu)]


def prelever(contenu):
    """Les blocs <style> du modèle qui portent les sélecteurs manquants."""
    metiers, equipe = [], []
    for deb, fin, entier, css in blocs_style(contenu):
        if len(css) > 20000:
            continue                      # le gros bloc de base, déjà présent partout
        if any(s in css for s in ('.eq-c', '.eq-rail', '.eq-av', '.eq-plus')):
            equipe.append((deb, entier))
        elif '.mt-v' in css or 'hh-metiers-sobre' in entier:
            metiers.append((deb, entier))
    metiers = [e for _, e in sorted(metiers)]
    equipe = [e for _, e in sorted(equipe)]
    if not metiers or not equipe:
        raise RuntimeError('blocs du modèle introuvables : '
                           f'{len(metiers)} métiers, {len(equipe)} équipe')
    return metiers, equipe


def main(ecrire=False):
    os.makedirs(SAUVE, exist_ok=True)
    modele = n.call(f'wp/v2/pages/{MODELE}?context=edit&_fields=content')['content']['raw']
    metiers, equipe = prelever(modele)
    print(f'modèle {MODELE} : {len(metiers)} bloc(s) carrousel '
          f'({sum(len(x) for x in metiers)} o), '
          f'{len(equipe)} bloc(s) équipe ({sum(len(x) for x in equipe)} o)')

    for pid in CIBLES:
        d = n.call(f'wp/v2/pages/{pid}?context=edit&_fields=id,link,content,meta')
        if d['meta'].get('_elementor_data') not in ('', '[]', None):
            print(f'  IGNORÉE (elementor non vide) {pid}')
            continue
        c = d['content']['raw']
        css = ' '.join(x[3] for x in blocs_style(c))
        deja = [s for s in SELECTEURS if s in css]
        if deja:
            print(f'  IGNORÉE ({pid}) : porte déjà {deja}')
            continue
        open(os.path.join(SAUVE, f'pages-{pid}.html'), 'w').write(c)

        a_eq = c.find('<section class="team-section"')
        a_me = c.find('<section class="metiers-section"')
        if a_eq < 0 or a_me < 0:
            raise RuntimeError(f'{pid} : ancrage introuvable '
                               f'(team {a_eq}, metiers {a_me})')
        # on insère de la fin vers le début pour ne pas décaler les positions
        c2 = c[:a_eq] + ''.join(equipe) + c[a_eq:]
        c2 = c2[:a_me] + ''.join(metiers) + c2[a_me:]

        css2 = ' '.join(x[3] for x in blocs_style(c2))
        manque = [s for s in SELECTEURS if s not in css2]
        assert not manque, f'{pid} : encore absents {manque}'
        assert len(c2) < PLAFOND, f'{pid} : {len(c2)} o au-dessus du plafond'
        assert c2.count('<section') == c.count('<section')
        assert c2.count('<style') == c.count('<style') + len(metiers) + len(equipe)
        print(f'  pages/{pid} {len(c):7} -> {len(c2):7}  {d["link"]}')
        if ecrire:
            n.call(f'wp/v2/pages/{pid}', 'POST', {'content': c2})


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
