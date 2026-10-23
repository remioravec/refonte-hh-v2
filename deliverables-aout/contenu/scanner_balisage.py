#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T13 — mesure correcte du balisage structure.

Le relevé du 01/10 comptait « Organization ×10, AggregateRating ×10 » sur les
pages comparatifs. C'était un comptage à plat de "@type":"..." dans le source,
et c'est faux : sur une page comparative, l'ItemList porte légitimement un
SoftwareApplication et un AggregateRating PAR CONCURRENT, et chaque Article
porte légitimement son publisher Organization.

Ce script mesure ce qui compte vraiment :
  - combien d'entités de PREMIER NIVEAU par type (un @graph compte ses membres) ;
  - combien de fois la note de Hello Harel lui-même est déclarée sur la page ;
  - combien d'entités décrivent l'entreprise sans @id pour les relier.
"""
import json, re, ssl, sys
import urllib.request as ur
from concurrent.futures import ThreadPoolExecutor

CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
SITE = "https://www.helloharel.com"
SOI = ("hello harel",)
ENTREPRISE = {"Organization", "LocalBusiness", "Corporation", "SoftwareApplication"}


def premier_niveau(d):
    """Entités de premier niveau d'un bloc ld+json (en dépliant @graph et les listes)."""
    if isinstance(d, list):
        out = []
        for x in d:
            out += premier_niveau(x)
        return out
    if not isinstance(d, dict):
        return []
    if "@graph" in d:
        return premier_niveau(d["@graph"])
    return [d]


def parcourir(d, chemin=()):
    if isinstance(d, dict):
        yield chemin, d
        for k, v in d.items():
            yield from parcourir(v, chemin + (k,))
    elif isinstance(d, list):
        for x in d:
            yield from parcourir(x, chemin)


def soi(e):
    n = e.get("name") or e.get("legalName") or ""
    if isinstance(n, str) and any(s in n.lower() for s in SOI):
        return True
    u = e.get("url") or e.get("@id") or ""
    return isinstance(u, str) and "helloharel.com" in u and not e.get("name")


def analyser(url):
    try:
        h = ur.urlopen(SITE + url, timeout=120, context=CTX).read().decode("utf-8", "replace")
    except Exception as e:
        return dict(url=url, erreur=str(e)[:80])
    blocs, invalides = [], 0
    for m in re.finditer(r'(?is)<script[^>]*ld\+json[^>]*>(.*?)</script>', h):
        try:
            blocs.append(json.loads(m.group(1)))
        except Exception:
            invalides += 1
    types, entreprises_soi, sans_id = {}, 0, 0
    # On compte des NOEUDS notes distincts, pas des occurrences : deux entites
    # qui portent le meme @id sont un seul noeud pour Google.
    notes = set()
    for b in blocs:
        for e in premier_niveau(b):
            t = e.get("@type")
            t = t[0] if isinstance(t, list) and t else t
            if isinstance(t, str):
                types[t] = types.get(t, 0) + 1
    for b in blocs:
        for _, e in parcourir(b):
            t = e.get("@type")
            t = t[0] if isinstance(t, list) and t else t
            if not isinstance(t, str):
                continue
            if t in ENTREPRISE and soi(e):
                entreprises_soi += 1
                if "@id" not in e:
                    sans_id += 1
                r = e.get("aggregateRating")
                if isinstance(r, dict):
                    notes.add((e.get("@id") or ('sans-id:' + t),
                               str(r.get("ratingValue")),
                               str(r.get("reviewCount") or r.get("ratingCount"))))
    return dict(url=url, blocs=len(blocs), invalides=invalides, types=types,
                note_soi=len(notes), notes=sorted(notes),
                entreprises_soi=entreprises_soi, sans_id=sans_id)


if __name__ == "__main__":
    import os
    src = sys.argv[1] if len(sys.argv) > 1 else \
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', '..', 'deliverables-octobre', 'crawl-2026-10-01.json')
    urls = [p["url"] for p in json.load(open(src)) if p.get("code") == 200]
    with ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(analyser, urls))
    json.dump(res, open('/tmp/t/balisage.json', 'w'), ensure_ascii=False)
    err = [r for r in res if r.get('erreur')]
    print(len(res), 'URL analysées,', len(err), 'en erreur')
    inv = [r for r in res if r.get('invalides')]
    print('pages avec un bloc ld+json illisible :', len(inv))
    print('\nNote de Hello Harel déclarée plus d\'une fois sur la page :')
    for r in sorted((r for r in res if r.get('note_soi', 0) > 1),
                    key=lambda r: -r['note_soi']):
        print(f"  {r['note_soi']} noeuds notes  {r['url']}")
        for x in r['notes']:
            print('       ', x)
    print('\nEntités « entreprise » Hello Harel sans @id, par page (top 15) :')
    for r in sorted((r for r in res if r.get('sans_id', 0) > 1),
                    key=lambda r: -r['sans_id'])[:15]:
        print(f"  {r['sans_id']}  {r['url']}")
    print('\nTypes de premier niveau dupliqués sur une même page (top 20) :')
    dup = []
    for r in res:
        for t, k in (r.get('types') or {}).items():
            if k > 1 and t not in ('ListItem', 'Question'):
                dup.append((k, t, r['url']))
    for k, t, u in sorted(dup, reverse=True)[:20]:
        print(f'  {k}x {t:22} {u}')
