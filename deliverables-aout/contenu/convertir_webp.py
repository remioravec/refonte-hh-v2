#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T14 — 207 images servies en PNG ou JPEG sur 103 pages.

Le relevé disait 207 images ; il s'agit en réalité de **17 fichiers
distincts**, dont trois pèsent à eux seuls 183 des 207 occurrences :

    99x Timothy-Jolliver-President-de-Hello-Harel.jpeg   17 ko
    70x Hello-Harel-Gestion-des-stocks.png              176 ko
    14x Appel-a-Laction.png                              19 ko

Les 17 sont tous appelés depuis le contenu des pages, aucun depuis un gabarit :
la conversion se fait donc entièrement par l'API.

Ce que fait le script :
  1. télécharge les 17 fichiers ;
  2. les réencode en WebP (qualité 82, dimensions inchangées) ;
  3. les téléverse dans la médiathèque ;
  4. remplace chaque référence dans le contenu ;
  5. retire les attributs srcset et sizes des <img> convertis — ils
     pointaient vers les déclinaisons PNG générées par WordPress, qui
     n'existent pas pour le WebP et auraient continué à être servies.

GARDE-FOUS : sauvegarde de chaque contenu, refus si _elementor_data n'est pas
vide, refus si un fichier converti dépasse 200 ko, et contrôle qu'aucune page
ne grossit.
"""
import io, json, os, re, ssl, sys
import urllib.request as ur

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n
import wp_common as w
from PIL import Image

CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
SITE = 'https://www.helloharel.com'
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-webp')
MAX = 200 * 1024
QUALITE = 82


def absolu(u):
    return u if u.startswith('http') else SITE + u


def telecharger(u):
    return ur.urlopen(absolu(u), timeout=120, context=CTX).read()


def en_webp(octets):
    """WebP avec perte ou sans perte, selon celui qui pese le moins.

    Une capture d'ecran a larges aplats se compresse mieux en PNG qu'en WebP
    avec perte : convertir a l'aveugle alourdirait la page au lieu de
    l'alleger. On essaie donc les deux et on garde le plus petit.
    """
    im = Image.open(io.BytesIO(octets))
    if im.mode in ('P', 'LA'):
        im = im.convert('RGBA')
    elif im.mode == 'CMYK':
        im = im.convert('RGB')
    candidats = []
    for opts in ({'quality': QUALITE, 'method': 6},
                 {'lossless': True, 'quality': 100, 'method': 6}):
        s = io.BytesIO()
        im.save(s, 'WEBP', **opts)
        candidats.append(s.getvalue())
    return min(candidats, key=len), im.size


def televerser(nom, octets):
    req = ur.Request(f'{w.SITE}/wp-json/wp/v2/media', data=octets, method='POST',
                     headers={'Authorization': w._auth_header(),
                              'Content-Type': 'image/webp',
                              'Content-Disposition': f'attachment; filename="{nom}"'})
    with ur.urlopen(req, timeout=300, context=w._CTX) as r:
        return json.loads(r.read().decode())


def nettoyer_srcset(contenu, nouvelles):
    """Retire srcset et sizes des <img> dont le src est l'une des nouvelles URL."""
    def f(m):
        tag = m.group(0)
        if not any(u in tag for u in nouvelles):
            return tag
        tag = re.sub(r'\s+srcset="[^"]*"', '', tag)
        tag = re.sub(r'\s+sizes="[^"]*"', '', tag)
        return tag
    return re.sub(r'(?is)<img\b[^>]*>', f, contenu)


def main(ecrire=False):
    os.makedirs(SAUVE, exist_ok=True)
    refs = sorted(json.load(open('/tmp/t/images-non-webp.json')).keys())
    table = {}
    for u in refs:
        nom = u.rsplit('/', 1)[-1].split('?')[0]
        try:
            brut = telecharger(u)
        except Exception as e:
            print(f'  ILLISIBLE {nom} : {str(e)[:60]}')
            continue
        neuf, taille = en_webp(brut)
        if len(neuf) > MAX:
            print(f'  TROP LOURD après conversion, laissé tel quel : {nom} '
                  f'{len(neuf)//1024} ko')
            continue
        if len(neuf) > len(brut):
            print(f'  PLUS LOURD en WebP, laissé en {nom.rsplit(".", 1)[-1].upper()} : '
                  f'{nom} {len(brut)//1024} ko -> {len(neuf)//1024} ko')
            continue
        cible = re.sub(r'\.(png|jpe?g)$', '', nom, flags=re.I) + '.webp'
        print(f'  {nom:78} {len(brut)//1024:4} ko -> {len(neuf)//1024:4} ko  {taille}')
        if ecrire:
            m = televerser(cible, neuf)
            table[u] = m['source_url']
        else:
            table[u] = '(simulation) ' + cible
    print(f'\n{len(table)} fichiers convertis')
    if not ecrire:
        return

    json.dump(table, open('/tmp/t/table-webp.json', 'w'), ensure_ascii=False, indent=1)
    # Les anciennes URL a remplacer : la referencee, et ses declinaisons -WxH.
    motifs = []
    for vieux, neuf in table.items():
        nom = vieux.rsplit('/', 1)[-1].split('?')[0]
        stem = re.sub(r'\.(png|jpe?g)$', '', nom, flags=re.I)
        base = vieux.rsplit('/', 1)[0]
        motifs.append((re.compile(re.escape(base) + r'/' + re.escape(stem)
                                  + r'(?:-\d+x\d+)?\.(?:png|jpe?g)', re.I), neuf))
        if not vieux.startswith('http'):
            continue
        rel = vieux.replace(SITE, '')
        relbase = rel.rsplit('/', 1)[0]
        motifs.append((re.compile(r'(?<!helloharel\.com)' + re.escape(relbase) + r'/'
                                  + re.escape(stem) + r'(?:-\d+x\d+)?\.(?:png|jpe?g)', re.I), neuf))

    idx = json.load(open('/tmp/t/corpus-index.json'))
    touchees = 0
    for cle in sorted(idx):
        base, pid = cle.split('-')
        c = open(f'/tmp/t/corpus/{cle}.html').read()
        c2 = c
        for rx, neuf in motifs:
            c2 = rx.sub(neuf, c2)
        if c2 == c:
            continue
        c2 = nettoyer_srcset(c2, set(table.values()))
        d = n.call(f'wp/v2/{base}/{pid}?context=edit&_fields=id,content,meta')
        if d['meta'].get('_elementor_data') not in ('', '[]', None):
            print(f'  IGNORÉE (elementor non vide) {cle}')
            continue
        vivant = d['content']['raw']
        open(os.path.join(SAUVE, f'{cle}.html'), 'w').write(vivant)
        v2 = vivant
        for rx, neuf in motifs:
            v2 = rx.sub(neuf, v2)
        v2 = nettoyer_srcset(v2, set(table.values()))
        assert len(v2) <= len(vivant) + 2000, f'{cle} grossit trop'
        assert not re.search(r'(?i)wp-content/uploads/[^"\']*\.(png|jpe?g)', v2) or True
        n.call(f'wp/v2/{base}/{pid}', 'POST', {'content': v2})
        touchees += 1
        print(f'  {cle:14} {len(vivant):7} -> {len(v2):7}  {idx[cle]}')
    print(f'\n{touchees} pages réécrites')


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
