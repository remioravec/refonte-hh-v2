#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le site ne parle plus que d'agroalimentaire.

Partent : la page « Devenir integrateur », les deux articles
« integrateur ERP » + ville, et les six pages intelligence artificielle.
Aucune ne se positionne sur quoi que ce soit, aucune ne recoit de lien
externe — la suppression ne coute rien.

Le medical reste en ligne, mais sort du pied de page.

L'ordre compte. On enleve d'abord les liens, on supprime ensuite : sinon
le pied de page pointe vers des pages disparues pendant tout le temps de
la bascule.

Usage :  python3 epurer_hors_agro.py              (blanc)
         python3 epurer_hors_agro.py --poser      (nettoie les liens)
         python3 epurer_hors_agro.py --corbeille  (met les 9 a la corbeille)
"""

import os
import re
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import ns_api                    # noqa: E402
import deployer_gabarit as D     # noqa: E402

MORTES = {
    "/integrateurs/": ("pages", 5950),
    "/erp-ia/": ("pages", 5951),
    "/intelligence-artificielle/": ("pages", 5952),
    "/ia-analyse-predictive/": ("pages", 5953),
    "/ia-automatisation-comptable/": ("pages", 5954),
    "/ia-assistant-commercial/": ("pages", 5955),
    "/ia-optimisation-stocks/": ("pages", 5956),
    "/blog/integrateur-erp-lyon/": ("posts", 5585),
    "/blog/integrateur-erp-paris/": ("posts", 5582),
}
# Le pied de page perd le medical et tout ce qui n'est pas agroalimentaire.
# Le negoce reste : c'est du commerce de denrees, pas un autre metier.
PIED = ("/medical/", "/medical/dispositifs-medicaux/", "/medical/laboratoires/",
        "/erp-ia/", "/intelligence-artificielle/", "/integrateurs/")
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/epure-avant")
PLAFOND = 275_000


def _bloc(c, i, balise):
    """Du <balise ...> ouvrant en i jusqu'a sa fermeture, imbrications
    comprises. Une expression paresseuse s'arrete au premier </balise>
    venu, qui n'est pas forcement le bon."""
    prof, fin = 0, None
    for m in re.finditer(r"<(/?)%s\b" % balise, c[i:]):
        prof += 1 if not m.group(1) else -1
        if prof == 0:
            fin = i + c[i:].find(">", m.end()) + 1
            break
    return fin


def retirer_li(c, href, notes):
    """L'entree de liste du pied qui porte ce lien.

    On ne decoupe pas la page en « avant le pied » et « apres le pied » :
    certaines pages posent un encart apres le <footer>, et un lien
    /medical/ y vit aussi, hors de toute liste. On vise donc la forme
    exacte de l'entree — <li><a href="...">libelle</a></li> — qui
    n'existe que dans les colonnes du pied."""
    motif = (r'<li\b[^>]*>\s*<a [^>]*href="(?:https://www\.helloharel\.com)?'
             + re.escape(href) + r'"[^>]*>(?:(?!</a>).)*?</a>\s*</li>')
    c, n = re.subn(motif, "", c, flags=re.S)
    if n:
        notes.append("%s ×%d" % (href, n))
    return c


def retirer_carte_blog(c, href, notes):
    """La vignette de l'article dans l'index du blog."""
    m = re.search(r'<a class="blog-card" href="(?:https://www\.helloharel\.com)?'
                  r'%s"' % re.escape(href), c)
    if not m:
        return c
    fin = _bloc(c, m.start(), "a")
    if fin is None:
        raise SystemExit("ARRET — vignette non fermee : %s" % href)
    c = c[:m.start()] + c[fin:]
    notes.append("vignette %s" % href)
    return c


def retirer_ancre(c, href, notes):
    """L'ancre entiere, pas seulement son adresse : un libelle « Voir
    l'analyse predictive IA → » sans destination ne sert personne."""
    n = 0
    while True:
        m = re.search(r'<a [^>]*href="(?:https://www\.helloharel\.com)?%s"'
                      % re.escape(href), c)
        if not m:
            break
        fin = _bloc(c, m.start(), "a")
        if fin is None:
            raise SystemExit("ARRET — ancre non fermee : %s" % href)
        c = c[:m.start()] + c[fin:]
        n += 1
    if n:
        notes.append("ancre %s ×%d" % (href, n))
    return c


def nettoyer(url, c, notes):
    depart = c
    for href in PIED:
        c = retirer_li(c, href, notes)
    if url == "/blog/":
        for href in ("/blog/integrateur-erp-lyon/", "/blog/integrateur-erp-paris/"):
            c = retirer_carte_blog(c, href, notes)
        m = re.search(r'<button class="bgx-pill" data-f="integrateur">.*?</button>',
                      c, re.S)
        if m:
            c = c[:m.start()] + c[m.end():]
            notes.append("filtre « Integration ERP »")
    if url not in MORTES:
        for href in MORTES:
            if re.search(r'href="(?:https://www\.helloharel\.com)?%s"'
                         % re.escape(href), c):
                c = retirer_ancre(c, href, notes)

    if not notes:
        return depart
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge sur %s" % url)
    # Les pages supprimees ne doivent plus etre citees nulle part. Le
    # medical, lui, reste en ligne : il sort du pied, pas du site — ses
    # pages continuent de se citer entre elles.
    for href in MORTES:
        if re.search(r'href="(?:https://www\.helloharel\.com)?%s"'
                     % re.escape(href), c):
            raise SystemExit("ARRET — il reste un lien vers %s sur %s" % (href, url))
    for col in re.findall(r'<div class="footer-col">.*?</div>', c, re.S):
        for href in PIED:
            if re.search(r'href="(?:https://www\.helloharel\.com)?%s"'
                         % re.escape(href), col):
                raise SystemExit("ARRET — %s est encore dans le pied de %s"
                                 % (href, url))
    partis = set(D.liens(depart)) - set(D.liens(c))
    attendus = set()
    for x in list(MORTES) + list(PIED):
        attendus |= {x, "https://www.helloharel.com" + x}
    if partis - attendus:
        raise SystemExit("ARRET — lien(s) perdu(s) en trop sur %s : %s"
                         % (url, sorted(partis - attendus)[:3]))
    for motif in (r'<section class="[^"]+"', r"<details"):
        if len(re.findall(motif, c)) != len(re.findall(motif, depart)):
            raise SystemExit("ARRET — %s bouge sur %s" % (motif, url))
    # Le plafond interdit de faire grossir une page au-dela du seuil de
    # rendu. Une page deja au-dessus qui retrecit ne pose pas ce probleme.
    if len(c) > PLAFOND and len(c) >= len(depart):
        raise SystemExit("ARRET — %d o sur %s, au-dela du seuil de rendu"
                         % (len(c), url))
    return c


def inventaire():
    out = []
    for t in ("pages", "posts"):
        p = 1
        while True:
            lot = ns_api.call("wp/v2/%s?per_page=100&page=%d&status=publish"
                              "&_fields=id,link" % (t, p))
            if not lot:
                break
            out += [(t, x["id"],
                     x["link"].replace("https://www.helloharel.com", "") or "/")
                    for x in lot]
            if len(lot) < 100:
                break
            p += 1
    return sorted(out, key=lambda z: z[2])


def main():
    poser = "--poser" in sys.argv
    corbeille = "--corbeille" in sys.argv

    if corbeille:
        print("=== mise a la corbeille ===")
        for url, (t, pid) in MORTES.items():
            c = w.get_raw(t, pid)["content"]["raw"]
            os.makedirs(SAUV, exist_ok=True)
            open(os.path.join(SAUV, "supprimee-%d.html" % pid), "w",
                 encoding="utf-8").write(c)
            ns_api.call("wp/v2/%s/%d" % (t, pid), method="DELETE")
            print("  %-34s corbeille (%d o sauvegardes)" % (url, len(c)))
        return

    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    n = 0
    for t, pid, url in inventaire():
        if url in MORTES:
            continue          # elles partent a la corbeille, inutile de les coiffer
        c = w.get_raw(t, pid)["content"]["raw"]
        notes = []
        c2 = nettoyer(url, c, notes)
        if not notes:
            continue
        n += 1
        print("%-52s %d -> %d o · %s" % (url[:52], len(c), len(c2),
                                         " · ".join(notes[:4])
                                         + (" …" if len(notes) > 4 else "")))
        if poser:
            os.makedirs(SAUV, exist_ok=True)
            open(os.path.join(SAUV, "avant-%s-%d.html" % (t, pid)), "w",
                 encoding="utf-8").write(c)
            w.update_content(t, pid, c2, live=True)
            time.sleep(0.2)
    print("\n%d page(s) nettoyee(s)" % n)
    if not poser:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
