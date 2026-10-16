#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T13 — une seule entité notée par page.

MESURE CORRIGÉE DU 01/10/2026. Le relevé initial annonçait « Organization ×10,
AggregateRating ×10 sur 133 pages ». C'était un comptage à plat des
« "@type":"..." » dans le source, et il est faux : sur une page comparative,
l'ItemList porte légitimement un SoftwareApplication et un AggregateRating par
concurrent, et chaque Article porte légitimement son publisher.

Le défaut réel, mesuré entité par entité : **33 pages** déclarent la note de
Hello Harel plus d'une fois, sur des entités que rien ne relie.

    source                                              pages
    extrait Elementor 4143 « Shcema » (global, head)     172   SoftwareApplication + note
    bloc LocalBusiness dans le contenu                    26   + note
    ligne « Hello Harel » de l'ItemList comparatif          2   + note
    @graph Organization#organization des pages /negoce/     5   + note

Correction :
  1. l'extrait global reçoit @id = <site>/#software et renvoie son creator
     vers <site>/#organization — il devient LA fiche logiciel du site ;
  2. toute entité Hello Harel de type SoftwareApplication reçoit ce même @id,
     ce qui la fusionne avec la précédente au lieu de la dupliquer ;
  3. la note est retirée des entités LocalBusiness et Organization. Google
     ignore de toute façon les avis auto-déclarés sur ces deux types ; c'est
     leur présence en double qui rend la fiche notée ambiguë.

La note reste donc déclarée une fois et une seule, sur le type qui la rend
éligible aux résultats enrichis.

GARDE-FOUS
  - sauvegarde de chaque contenu avant écriture ;
  - refus si _elementor_data n'est pas vide ;
  - les blocs sont relus par json.loads avant et après : un bloc illisible
    n'est jamais réécrit, il est signalé ;
  - tout « & » du JSON ressort en \\u0026, jamais nu (WordPress le changerait
    en &#038; et casserait le bloc).
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

SITE = 'https://www.helloharel.com'
ID_LOGICIEL = SITE + '/#software'
ID_SOCIETE = SITE + '/#organization'
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-balisage')
PLAFOND = 275_000

SANS_NOTE = {'LocalBusiness', 'Organization', 'Corporation'}


def est_soi(e):
    n_ = e.get('name') or e.get('legalName') or ''
    return isinstance(n_, str) and 'hello harel' in n_.lower()


def type_de(e):
    t = e.get('@type')
    return t[0] if isinstance(t, list) and t else t


def transformer(d, journal):
    """Parcours récursif : retire la note des fiches société, pose l'@id logiciel."""
    if isinstance(d, list):
        return [transformer(x, journal) for x in d]
    if not isinstance(d, dict):
        return d
    t = type_de(d)
    if isinstance(t, str) and est_soi(d):
        if t in SANS_NOTE and isinstance(d.get('aggregateRating'), dict):
            d.pop('aggregateRating')
            journal.append('note retirée de ' + t)
        if t == 'SoftwareApplication':
            # On ne fusionne que ce qui est fusionnable. La ligne « Hello Harel »
            # des pages comparatives porte une note EDITORIALE (4,7 sur 1 avis,
            # notre propre score de comparatif) : lui donner le meme @id que la
            # fiche logiciel creerait un noeud a deux notes contradictoires,
            # pire que le doublon. Elle est donc laissee telle quelle et le
            # sujet remonte en decision dans la roadmap.
            r = d.get('aggregateRating')
            editoriale = isinstance(r, dict) and (
                str(r.get('ratingValue')) not in ('5', '5.0')
                or str(r.get('reviewCount') or r.get('ratingCount')) != '31')
            if editoriale:
                journal.append('note éditoriale laissée telle quelle sur '
                               + str(d.get('name')) + ' : '
                               + str(r.get('ratingValue')) + '/'
                               + str(r.get('reviewCount') or r.get('ratingCount')))
            elif d.get('@id') != ID_LOGICIEL:
                d['@id'] = ID_LOGICIEL
                journal.append('@id logiciel posé sur SoftwareApplication')
    return {k: transformer(v, journal) for k, v in d.items()}


def sans_amp_nu(s):
    return s.replace('&', '\\u0026')


def reecrire_blocs(contenu, journal):
    """Réécrit chaque <script application/ld+json> transformé. Laisse les illisibles."""
    out, pos = [], 0
    for m in re.finditer(r'(?is)(<script[^>]*ld\+json[^>]*>)(.*?)(</script>)', contenu):
        out.append(contenu[pos:m.start()])
        brut = m.group(2)
        try:
            d = json.loads(brut)
        except Exception as e:
            journal.append('BLOC ILLISIBLE laissé tel quel : ' + str(e)[:60])
            out.append(m.group(0))
            pos = m.end()
            continue
        avant = json.dumps(d, ensure_ascii=False, sort_keys=True)
        j2 = []
        d = transformer(d, j2)
        apres = json.dumps(d, ensure_ascii=False, sort_keys=True)
        if avant == apres:
            journal.extend(x for x in j2 if 'éditoriale' in x)
            out.append(m.group(0))
        else:
            journal.extend(j2)
            txt = sans_amp_nu(json.dumps(d, ensure_ascii=False))
            json.loads(txt)                       # relecture obligatoire
            out.append(m.group(1) + txt + m.group(3))
        pos = m.end()
    out.append(contenu[pos:])
    return ''.join(out)


# --------------------------------------------------------------------------

def resoudre(url):
    """URL servie -> (type REST, id). Essaie les pages puis les articles."""
    slug = [x for x in url.strip('/').split('/') if x]
    slug = slug[-1] if slug else ''
    if not slug:
        d = n.call('wp/v2/pages?per_page=100&_fields=id,link')
        for p in d:
            if p['link'].rstrip('/') == SITE:
                return 'pages', p['id']
        raise RuntimeError('accueil introuvable')
    for base in ('pages', 'posts'):
        d = n.call(f'wp/v2/{base}?slug={slug}&_fields=id,link')
        for p in d:
            if p['link'].replace(SITE, '').rstrip('/') == url.rstrip('/'):
                return base, p['id']
        if d:
            return base, d[0]['id']
    raise RuntimeError('introuvable : ' + url)


def extrait_global(ecrire):
    d = n.call('wp/v2/elementor_snippet/4143?context=edit&_fields=id,meta')
    code = d['meta'].get('_elementor_code', '')
    open(os.path.join(SAUVE, 'elementor-4143.txt'), 'w').write(code)
    m = re.search(r'(?is)(<script[^>]*ld\+json[^>]*>)(.*?)(</script>)', code)
    if not m:
        raise RuntimeError('4143 : pas de bloc ld+json')
    j = json.loads(m.group(2))
    j['@id'] = ID_LOGICIEL
    if isinstance(j.get('creator'), dict):
        j['creator'] = {'@id': ID_SOCIETE, '@type': 'Organization',
                        'name': j['creator'].get('name', 'Harel Systems SAS'),
                        'url': SITE, 'address': j['creator'].get('address')}
    if isinstance(j.get('aggregateRating'), dict):
        j['aggregateRating'] = {'@type': 'AggregateRating', 'ratingValue': '5',
                                'reviewCount': '31', 'bestRating': '5',
                                'worstRating': '1'}
    txt = sans_amp_nu(json.dumps(j, ensure_ascii=False, indent=2))
    json.loads(txt)
    neuf = code[:m.start()] + m.group(1) + '\n' + txt + '\n' + m.group(3) + code[m.end():]
    if ecrire:
        n.call('wp/v2/elementor_snippet/4143', 'POST',
               {'meta': {'_elementor_code': neuf}})
    return len(code), len(neuf)


def main(urls, ecrire=False):
    os.makedirs(SAUVE, exist_ok=True)
    a, b = extrait_global(ecrire)
    print(f'extrait Elementor 4143 « Shcema » : {a} -> {b} o')
    print()
    for u in urls:
        base, pid = resoudre(u)
        d = n.call(f'wp/v2/{base}/{pid}?context=edit&_fields=id,content,meta')
        if d['meta'].get('_elementor_data') not in ('', '[]', None):
            print(f'  IGNORÉE (elementor non vide) {u}')
            continue
        c = d['content']['raw']
        open(os.path.join(SAUVE, f'{base}-{pid}.html'), 'w').write(c)
        journal = []
        c2 = reecrire_blocs(c, journal)
        if c2 == c:
            if journal:
                print(f'  inchangée          {u}')
                for x in journal:
                    print('        ·', x)
            else:
                print(f'  rien à faire       {u}')
            continue
        # Deux pages comparatives vivent deja au-dessus du plafond et rendent
        # correctement. On ne les refuse pas, on interdit simplement qu'elles
        # grossissent.
        assert len(c2) < max(PLAFOND, len(c)), (
            f'{u} : {len(c)} -> {len(c2)} o, la page grossit au-dela du plafond')
        if ecrire:
            n.call(f'wp/v2/{base}/{pid}', 'POST', {'content': c2})
        print(f'  {base[:4]} {pid:6} {len(c):7} -> {len(c2):7}  {u}')
        for x in journal:
            print('        ·', x)


if __name__ == '__main__':
    cibles = json.load(open('/tmp/t/balisage.json'))
    urls = [x['url'] for x in cibles if x.get('note_soi', 0) > 1]
    main(urls, ecrire='--ecrire' in sys.argv)
