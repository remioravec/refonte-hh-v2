#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/tarifs/ — un IIFE JavaScript a été collé À L'INTÉRIEUR du bloc
<script type="application/ld+json">. Deux défauts en un :

  1. le bloc ld+json n'est plus du JSON valide (« Extra data », caractère 4679),
     donc Google ignore TOUT le balisage de la page : LocalBusiness, Product,
     Offer, BreadcrumbList ;
  2. le script, lui, ne s'exécute jamais — un navigateur n'exécute pas un
     type="application/ld+json". Les puces du carrousel de tarifs sont donc
     mortes depuis leur mise en ligne.

Correction : on sépare les deux en deux balises, et on ajoute au script la
garde qui lui manquait (il lisait .offsetWidth sur un .pricing-card supposé
présent). Aucune ligne de comportement n'est ajoutée.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

PID = 608
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-tarifs')
GARDE = ("  var dots = document.querySelectorAll('.pricing-dot');\n"
         "  if (!grid || !dots.length) return;\n")
GARDE_NEUVE = ("  var dots = document.querySelectorAll('.pricing-dot');\n"
               "  if (!grid || !dots.length) return;\n"
               "  if (!grid.querySelector('.pricing-card')) return;\n")


def main(ecrire=False):
    os.makedirs(SAUVE, exist_ok=True)
    d = n.call(f'wp/v2/pages/{PID}?context=edit&_fields=id,content,meta')
    if d['meta'].get('_elementor_data') not in ('', '[]', None):
        raise RuntimeError('elementor non vide')
    c = d['content']['raw']
    open(os.path.join(SAUVE, 'tarifs.html'), 'w').write(c)

    m = re.search(r'(?is)(<script[^>]*ld\+json[^>]*>)(.*?)(</script>)', c)
    if not m:
        raise RuntimeError('pas de bloc ld+json')
    brut = m.group(2)
    dec = json.JSONDecoder()
    obj, fin = dec.raw_decode(brut.lstrip())
    decalage = len(brut) - len(brut.lstrip())
    schema = brut[:decalage + fin]
    reste = brut[decalage + fin:]
    js = reste.strip()
    if not js.startswith('(function'):
        raise RuntimeError('ce qui suit le JSON n\'est pas le script attendu : '
                           + repr(js[:60]))
    json.loads(schema)                                   # relecture
    assert GARDE in js, 'la garde attendue est introuvable dans le script'
    js = js.replace(GARDE, GARDE_NEUVE)
    assert not re.search(r'&(?!(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);)', js), 'un & nu dans le script'

    neuf = (c[:m.start()]
            + m.group(1) + schema + m.group(3) + '\n'
            + '<script>\n' + js + '\n</script>'
            + c[m.end():])

    # Contrôles
    for b in re.finditer(r'(?is)<script[^>]*ld\+json[^>]*>(.*?)</script>', neuf):
        json.loads(b.group(1))
    assert neuf.count('<script') == c.count('<script') + 1
    assert len(neuf) < 275_000

    print(f'ld+json : {len(brut)} o -> {len(schema)} o de JSON valide '
          f'+ {len(js)} o de script sorti dans sa propre balise')
    print(f'contenu : {len(c)} -> {len(neuf)} o')
    print('entités du schéma :',
          [e.get('@type') for e in (obj.get('@graph') or [obj])])
    if ecrire:
        n.call(f'wp/v2/pages/{PID}', 'POST', {'content': neuf})
        print('écrit.')


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
