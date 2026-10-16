#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T16 — /comparatifs/ servait deux H1.

Le premier vient du gabarit du thème : <h1 class="entry-title"> qui imprime le
titre du post. Ce titre était « Comparatifs ERP Agroalimentaire • Par Métier •
2026 ☁️ » — un title de SERP, pas un H1. Le second était dans le contenu.

Correction :
  - le titre du post redevient un titre de page (« Comparatifs ERP
    agroalimentaire par métier »), ce qui donne un H1 propre et un fil
    d'Ariane lisible. Le title de SERP, lui, vit dans Rank Math et ne bouge
    pas ;
  - le H1 du contenu devient un H2 ;
  - le hub ne listait que 3 des 4 comparatifs publiés. Les 4 y sont, ancres en
    exact match, aucune ancre neutre.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

PID = 7920
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-hub')
TITRE = 'Comparatifs ERP agroalimentaire par métier'
RM_TITLE = 'Comparatifs ERP agroalimentaire • Par métier • 2026'
RM_DESC = ('Comparatifs ERP agroalimentaire par métier : négoce, charcuterie, '
           'traiteur, facturation grossiste. Édition 2026.')

CONTENU = '''<!-- wp:html -->
<div style="max-width:900px;margin:4rem auto;padding:2rem;font-family:Inter,sans-serif">
<h2 style="font-size:2rem;color:#0f172a;margin-bottom:1rem">Nos comparatifs ERP, filière par filière</h2>
<p style="font-size:1.1rem;color:#64748b;line-height:1.6;margin-bottom:2rem">Quatre comparatifs, un par segment, mis à jour pour 2026. Chacun confronte les éditeurs sur les points qui décident en agroalimentaire : poids variable, DLC et traçabilité par lot, prix de revient réel, reprise des données.</p>
<ul style="list-style:none;padding:0;font-size:1.05rem;line-height:2.1">
<li>→ <a href="/comparatifs/meilleur-erp-negoce-distribution-alimentaire-2026/" style="color:#16a34a;text-decoration:none;font-weight:600">Meilleur ERP négoce et distribution alimentaire 2026</a></li>
<li>→ <a href="/comparatifs/meilleur-logiciel-facturation-grossiste-negoce-2026/" style="color:#16a34a;text-decoration:none;font-weight:600">Meilleur logiciel de facturation grossiste et négoce 2026</a></li>
<li>→ <a href="/comparatifs/meilleur-erp-charcuterie-salaison/" style="color:#16a34a;text-decoration:none;font-weight:600">Meilleur ERP charcuterie et salaison</a></li>
<li>→ <a href="/comparatifs/meilleur-erp-traiteur/" style="color:#16a34a;text-decoration:none;font-weight:600">Meilleur ERP traiteur</a></li>
</ul>
</div>
<!-- /wp:html -->'''


def main(ecrire=False):
    os.makedirs(SAUVE, exist_ok=True)
    d = n.call(f'wp/v2/pages/{PID}?context=edit&_fields=id,title,content,meta')
    if d['meta'].get('_elementor_data') not in ('', '[]', None):
        raise RuntimeError('elementor non vide')
    open(os.path.join(SAUVE, 'comparatifs.html'), 'w').write(
        d['title']['raw'] + '\n\n' + d['content']['raw'])
    assert '<h1' not in CONTENU and CONTENU.count('<h2') == 1
    assert not re.search(r'&(?!(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);)', CONTENU)
    print('titre  :', repr(d['title']['raw']), '->', repr(TITRE))
    print('contenu:', len(d['content']['raw']), '->', len(CONTENU), 'o')
    print('liens  :', len(re.findall(r'href="(/comparatifs/[^"]+)"', CONTENU)))
    if ecrire:
        n.call(f'wp/v2/pages/{PID}', 'POST', {'title': TITRE, 'content': CONTENU})
        n.call('rankmath/v1/updateMeta', 'POST', {
            'objectID': PID, 'objectType': 'post',
            'meta': {'rank_math_title': RM_TITLE, 'rank_math_description': RM_DESC}})
        print('écrit.')


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
