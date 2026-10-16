#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deux defauts reperes a l'oeil sur un article, mesures sur le parc entier.

1. DES ACCENTS MANQUANTS DANS LES TITRES. « tracabilite », « integree »,
   « reduire » : du francais sans accents, en H2, visible par le lecteur.
   On cherche les mots qui devraient en porter un.

2. DES « CAS CONCRETS » CHIFFRES. « reduire ses pertes DLC de 60 % » est
   une promesse de resultat. Si le cas n'est pas reel et sourcable, c'est
   une allegation. On releve ou ils sont et ce qu'ils avancent.
"""
import os, re, sys
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp_common as w, ns_api      # noqa: E402

# des mots frequents du domaine qui portent un accent en francais
SANS_ACCENT = ["tracabilite", "integree", "integre", "reduire", "reduit",
               "reglementaire", "peremption", "perimee", "securite", "qualite",
               "conformite", "reception", "etiquetage", "etiquette", "prefere",
               "operationnel", "realise", "derniere", "matiere", "cout",
               "prevision", "reference", "gere", "generale", "specifique"]
CHIFFRE = re.compile(r"(?:de|jusqu'à|jusqu'a|\+|\-)?\s?\d{1,3}\s?%")


def main():
    arts, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/posts?per_page=100&page=%d&status=publish&_fields=id,link" % p)
        if not lot:
            break
        arts += lot
        if len(lot) < 100:
            break
        p += 1

    acc_pages, cas_pages = [], []
    for a in sorted(arts, key=lambda x: x["link"]):
        c = w.get_raw("posts", a["id"])["content"]["raw"]
        u = a["link"].replace("https://www.helloharel.com", "")
        titres = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
                  for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", c, re.S)]
        fautifs = []
        for t in titres:
            bas = t.lower()
            for mot in SANS_ACCENT:
                if re.search(r"\b%s\b" % mot, bas):
                    fautifs.append((t, mot))
                    break
        if fautifs:
            acc_pages.append((u, fautifs))
        # les cas concrets chiffres
        cas = [t for t in titres if re.search(r"cas (concret|client|pratique)", t, re.I)]
        pct = CHIFFRE.findall(re.sub(r"<[^>]+>", " ", c))
        if cas:
            cas_pages.append((u, cas, sorted(set(pct))[:6]))

    print("=== 1. accents manquants dans les titres ===")
    print("%d article(s) sur %d\n" % (len(acc_pages), len(arts)))
    for u, f in acc_pages[:16]:
        print("   %-50s %s" % (u[:50], " · ".join("« %s »" % t[:46] for t, _ in f[:2])))
    if len(acc_pages) > 16:
        print("   … et %d autres" % (len(acc_pages) - 16))

    print("\n=== 2. « cas concret » et pourcentages ===")
    print("%d article(s) avec un titre de cas\n" % len(cas_pages))
    for u, cas, pct in cas_pages[:16]:
        print("   %-46s %-40s %s" % (u[:46], cas[0][:40], ", ".join(pct)))
    if len(cas_pages) > 16:
        print("   … et %d autres" % (len(cas_pages) - 16))


if __name__ == "__main__":
    main()
