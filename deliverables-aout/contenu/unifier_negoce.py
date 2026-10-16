#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unification des deux pages meres du negoce.

CONSTAT : deux pages se disputaient la meme intention.
  /negoce/                                 (5957)  — gabarit generique, title « ERP Negoce »,
                                                     942 liens internes entrants, ancre « ERP Negoce »
  /agroalimentaire/negoce-alimentaire/     (10934) — contenu metier refondu en septembre
                                                     (poids pese, DLC, echeance legale, calculateur),
                                                     24 liens entrants seulement

DECISION DU CLIENT : une seule page, a l'URL /negoce/, exclusivement alimentaire.

CE QUE FAIT CE SCRIPT
  1. sauvegarde les deux pages
  2. porte le contenu de 10934 sur 5957, avec :
       - les auto-references retargetees sur /negoce/
       - un fil d'Ariane a deux niveaux, coherent avec une URL de premier niveau
       - la photo de hero de /negoce/ conservee (entrepot) et non celle de 10934
         (marche de gros asiatique, signalee au client le 11/09)
  3. pose le title et la meta description de la page unifiee
  4. redirige 10934 en 301 vers /negoce/ et le sort du sitemap

Regle 0 : aucune des cinq pages protegees n'est modifiee ici.

Usage :  python3 unifier_negoce.py            (essai a blanc)
         python3 unifier_negoce.py --live     (ecriture)
"""

import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import wp_common as w   # noqa: E402
import ns_api           # noqa: E402

LIVE = "--live" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"

PORTEUSE = 5957     # /negoce/            — celle qu'on garde
SOURCE = 10934      # /agroalimentaire/negoce-alimentaire/ — celle qu'on fond dedans
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

ANCIENNE = "/agroalimentaire/negoce-alimentaire/"
NOUVELLE = "/negoce/"

TITLE = "ERP Négoce Alimentaire • Poids Réel, DLC, Marge Grossiste"          # 544 px
DESC = ("L'ERP négoce alimentaire qui facture au poids réellement pesé, applique la DLC "
        "du lot et l'échéance légale du produit. Calculateur de marge réelle.")          # 913 px

FIL = ('<script type="application/ld+json">{"@context": "https://schema.org", '
       '"@type": "BreadcrumbList", "itemListElement": ['
       '{"@type": "ListItem", "position": 1, "name": "Accueil", '
       '"item": "https://www.helloharel.com/"}, '
       '{"@type": "ListItem", "position": 2, "name": "Négoce alimentaire", '
       '"item": "https://www.helloharel.com/negoce/"}]}</script>')


def hero_de(contenu):
    """Renvoie l'URL de fond de la section hero."""
    m = re.search(r'(<section class="hero-section"[^>]*url\(\')([^\']+)(\'\))', contenu)
    return m.group(2) if m else None


def transformer(base, photo):
    """Adapte le contenu de 10934 pour qu'il vive a l'URL /negoce/."""
    journal = []

    n = base.count(ANCIENNE)
    base = base.replace(ANCIENNE, NOUVELLE)
    journal.append("auto-references retargetees sur /negoce/ : %d" % n)

    bloc = re.search(r'<script type="application/ld\+json">\{[^<]*?BreadcrumbList.*?</script>',
                     base, re.S)
    if not bloc:
        raise SystemExit("ARRET — BreadcrumbList introuvable dans la source")
    base = base[:bloc.start()] + FIL + base[bloc.end():]
    journal.append("fil d'Ariane ramene a deux niveaux (Accueil > Négoce alimentaire)")

    actuelle = hero_de(base)
    if photo and actuelle and actuelle != photo:
        base = base.replace(actuelle, photo)
        journal.append("photo de hero conservee : %s" % photo.split("/")[-1])

    return base, journal


def controles(neuf):
    """Verifications bloquantes avant ecriture."""
    pb = []

    if ANCIENNE in neuf:
        pb.append("il reste %d reference(s) a l'ancienne URL" % neuf.count(ANCIENNE))

    h1 = re.findall(r"<h1[^>]*>", neuf)
    if len(h1) != 1:
        pb.append("%d balises h1 (il en faut exactement une)" % len(h1))

    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', neuf, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            pb.append("JSON-LD invalide : %s" % e)

    if neuf.count("<section") != neuf.count("</section>"):
        pb.append("sections non refermees")

    corps = re.sub(r"<header.*?</header>", "", neuf, flags=re.S)
    corps = re.sub(r"<footer.*?</footer>", "", corps, flags=re.S)
    # le menu mobile vit apres le <header>, dans #hh-page : c'est de la navigation
    j = corps.find('<div class="mobile-menu"')
    if j >= 0:
        k = corps.find('<section class="hero-section"', j)
        if k < 0:
            raise SystemExit("ARRET — impossible de borner le menu mobile")
        corps = corps[:j] + corps[k:]
    if re.search(r"[Ii]mport[- ]?[Ee]xport", corps):
        pb.append("mention import-export dans le corps de page")

    vus = set()
    for href in sorted(set(re.findall(r'href="(/[^"#?]+)"', neuf))):
        if href in vus:
            continue
        vus.add(href)
        code = subprocess.run(
            ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}",
             "https://www.helloharel.com" + href],
            capture_output=True, text=True, timeout=45).stdout.strip()
        if code not in ("200", "301"):
            pb.append("lien interne en %s : %s" % (code, href))
        elif code == "301" and href != ANCIENNE:
            pb.append("lien interne en 301 (chaine) : %s" % href)

    return pb


def main():
    porteuse = w.get_raw("pages", PORTEUSE)
    source = w.get_raw("pages", SOURCE)

    for pid, p in ((PORTEUSE, porteuse), (SOURCE, source)):
        f = os.path.join(ICI, "backup-unification-%d.html" % pid)
        open(f, "w", encoding="utf-8").write(p["content"]["raw"])
        print("sauvegarde  %s  (%d octets)" % (os.path.basename(f), len(p["content"]["raw"])))

    if PORTEUSE in PROTEGEES or SOURCE in PROTEGEES:
        raise SystemExit("ARRET — page protegee (regle 0)")

    photo = hero_de(porteuse["content"]["raw"])
    neuf, journal = transformer(source["content"]["raw"], photo)

    print()
    for l in journal:
        print("  ·", l)

    print("\ncontroles…")
    pb = controles(neuf)
    if pb:
        print("\nBLOCAGE :")
        for x in pb:
            print("   !", x)
        raise SystemExit(1)
    print("  tout est vert")

    print("\n%d octets -> %d octets" % (len(porteuse["content"]["raw"]), len(neuf)))

    if not LIVE:
        open(os.path.join(S, "negoce-unifie.html"), "w", encoding="utf-8").write(neuf)
        print("\nESSAI A BLANC — rien n'a ete ecrit. Rendu dans %s/negoce-unifie.html" % S)
        return

    w.update_content("pages", PORTEUSE, neuf, live=True)
    print("\npage %d mise a jour" % PORTEUSE)

    ns_api.call("rankmath/v1/updateMeta", "POST", {
        "objectID": PORTEUSE, "objectType": "post",
        "meta": {"rank_math_title": TITLE, "rank_math_description": DESC},
    })
    print("title et description poses")


if __name__ == "__main__":
    main()
