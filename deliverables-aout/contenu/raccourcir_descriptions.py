#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T11 — 88 meta descriptions dépassent 985 px, donc Google les coupe.

Le relevé montre un motif, pas 88 cas particuliers : la quasi-totalité se
termine par une signature de marque — « Guide par Hello Harel, éditeur
spécialisé agroalimentaire depuis 2014. », « Analyse experte par Hello Harel,
éditeur spécialisé. » — qui pèse 50 à 70 caractères. C'est exactement ce qui
dépasse, et c'est la partie la moins utile dans une SERP : la marque est déjà
dans le title et dans l'URL affichée.

La règle appliquée, dans cet ordre, jusqu'à passer sous 985 px :
  1. la signature de marque finale est remplacée par une forme courte
     (« Par Hello Harel. ») ;
  2. si ça ne suffit pas, elle est retirée ;
  3. si ça ne suffit toujours pas, la dernière phrase informative est retirée ;
  4. si on tombe sous 400 px, on remet « Démo gratuite. ».

Aucune description n'est coupée au milieu d'une phrase, et aucune n'est
réécrite à l'aveugle : le script sort l'avant/après des 88 pour relecture.
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

HAUT, BAS = 985, 400
LARGE = set("mwMW—…")
SIGNATURE = re.compile(r'(?i)\b(guide|analyse|comparatif|conseils?|m[ée]thode)?\s*'
                       r'[^.]*\bhello harel\b[^.]*\.$')
COURTE = 'Par Hello Harel.'


def px(s):
    return round(sum(11.0 if c in LARGE else (8.0 if c.isalnum() else 5.5) for c in s))


def phrases(d):
    """Découpe en phrases sur « . » suivi d'une majuscule ou de la fin."""
    out, cour = [], ''
    for i, c in enumerate(d):
        cour += c
        if c == '.' and (i + 1 >= len(d) or d[i + 1] == ' '):
            out.append(cour.strip())
            cour = ''
    if cour.strip():
        out.append(cour.strip())
    return out


def raccourcir(d):
    d = re.sub(r'\s+', ' ', html.unescape(d)).strip()
    if px(d) <= HAUT:
        return d, 'déjà conforme'
    ph = phrases(d)
    # 1. signature remplacée par une forme courte
    if ph and 'hello harel' in ph[-1].lower():
        essai = ' '.join(ph[:-1] + [COURTE])
        if px(essai) <= HAUT and px(essai) >= BAS:
            return essai, 'signature raccourcie'
        # 2. signature retirée
        essai = ' '.join(ph[:-1])
        if BAS <= px(essai) <= HAUT:
            return essai, 'signature retirée'
        if px(essai) < BAS:
            essai2 = essai + ' Démo gratuite.'
            if BAS <= px(essai2) <= HAUT:
                return essai2, 'signature remplacée par le CTA'
        ph = ph[:-1]
        # 3. la signature a sauté et ça ne suffit pas : on retire la dernière
        # phrase informative, tant qu'il reste de la matière.
        while len(ph) > 1 and px(' '.join(ph)) > HAUT:
            ph = ph[:-1]
        essai = ' '.join(ph)
        if BAS <= px(essai) <= HAUT:
            return essai, 'signature et dernière phrase retirées'
        return essai, 'À RÉÉCRIRE À LA MAIN'
    # Pas de signature de marque : retirer une phrase entière ferait perdre un
    # argument. Ces cas se réécrivent à la main, pas au chalumeau.
    return d, 'À RÉÉCRIRE À LA MAIN'


def resoudre(url):
    seg = [x for x in url.strip('/').split('/') if x]
    slug = seg[-1] if seg else ''
    for base in ('posts', 'pages'):
        d = n.call(f'wp/v2/{base}?slug={slug}&_fields=id,link')
        for p in d:
            if p['link'].replace('https://www.helloharel.com', '').rstrip('/') == url.rstrip('/'):
                return base, p['id']
        if d:
            return base, d[0]['id']
    raise RuntimeError('introuvable : ' + url)


def main(ecrire=False):
    src = json.load(open('/tmp/t/desc88.json'))
    reste, faits = [], 0
    for p in src:
        neuf, pourquoi = raccourcir(p['desc'])
        print(f"{p['px']:5} -> {px(neuf):4}  {pourquoi:36} {p['url']}")
        print(f"       - {p['desc']}")
        print(f"       + {neuf}")
        if 'À RÉÉCRIRE' in pourquoi:
            reste.append(p['url'])
            continue
        if not (BAS <= px(neuf) <= HAUT):
            reste.append(p['url'])
            continue
        if ecrire:
            base, pid = resoudre(p['url'])
            n.call('rankmath/v1/updateMeta', 'POST', {
                'objectID': pid, 'objectType': 'post',
                'meta': {'rank_math_description': neuf}})
        faits += 1
    print()
    print(f'{faits} descriptions ramenées entre {BAS} et {HAUT} px, '
          f'{len(reste)} à réécrire à la main')
    for u in reste:
        print('   ', u)


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
