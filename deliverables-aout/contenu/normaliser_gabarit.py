#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ramene toutes les pages metier et fonctionnalites au meme gabarit.

LE GABARIT DE REFERENCE, celui des trois pages validees :
  hero · logos · fonctionnalites · a-propos · process · metiers · equipe ·
  faq · avis   (+ cta-banner quand la page en porte un)

CE QUI PART :
  · les blocs « maj d'aout » (hh-maj-aout-*), un par page sur six pages ;
  · hh-demo-cta, le rappel de demo ;
  · glnb-section sur la page glacier ;
  · les sections .features-section surnumeraires : l'outil interactif
    (« Calculez votre charge atelier ») et le « Voir aussi ». La premiere
    .features-section, celle du defilement, est evidemment gardee ;
  · les <section class="container"> qui ne portent qu'un rappel de demo.

CE QUI RESTE, et pourquoi :
  · les <section class="container"> qui listent des sources externes
    (AFNOR, INRS, FranceAgriMer, ANSES, service-public) : ce sont des
    references, pas un bloc decoratif. Les retirer appauvrirait la page.

Chaque lien qui disparait est nomme, et le script dit s'il subsiste
ailleurs sur la page ou s'il devient orphelin.

Usage :  python3 normaliser_gabarit.py                (blanc)
         python3 normaliser_gabarit.py --poser        (ecrit)
         python3 normaliser_gabarit.py --page 3309    (une seule)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/normalise-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

GARDE = {"hero-section", "logos-section", "about-card-section", "process-section",
         "metiers-section", "team-section", "faq-section", "reviews-section",
         "cta-banner"}
SOURCES = ("afnor.org", "inrs.fr", "franceagrimer.fr", "service-public.fr", "anses.fr")


def sections(c):
    """[(debut, fin, classe)] pour chaque <section> de premier niveau."""
    out = []
    for m in re.finditer(r'<section class="([^"]+)"[^>]*>', c):
        j = c.find("</section>", m.start()) + len("</section>")
        out.append((m.start(), j, m.group(1).split()[0]))
    return out


def a_retirer(c):
    """Rend [(debut, fin, classe, motif)] des sections hors gabarit."""
    secs = sections(c)
    vues_features = 0
    out = []
    for i, j, cl in secs:
        bloc = c[i:j]
        if cl == "features-section":
            vues_features += 1
            if vues_features == 1:
                continue                      # le defilement : on le garde
            ov = re.search(r'class="overline"[^>]*>([^<]+)<', bloc)
            out.append((i, j, cl, "features surnumeraire — %s"
                        % (ov.group(1).strip() if ov else "sans intitule")))
            continue
        if cl in GARDE:
            continue
        if cl == "container":
            if any(x in bloc for x in SOURCES) or 'id="sources"' in bloc:
                continue          # sources officielles : elles restent
            if "Pour approfondir" in bloc:
                out.append((i, j, cl, "« Pour approfondir » — deja ecarte le 22/09"))
            elif "midcta" in bloc:
                out.append((i, j, cl, "rappel de demo en milieu de page"))
            else:
                out.append((i, j, cl, "container hors gabarit"))
            continue
        out.append((i, j, cl, "hors gabarit"))
    return out


def main():
    poser = "--poser" in sys.argv
    une = int(sys.argv[sys.argv.index("--page") + 1]) if "--page" in sys.argv else None
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    pages = D.cibles() + [(10935, "/agroalimentaire/torrefacteur/"),
                          (10896, "/agroalimentaire/brasseur/"),
                          (10894, "/agroalimentaire/chocolatier/")]
    orphelins_total = {}
    for pid, url in sorted(pages, key=lambda t: t[1]):
        if une and pid != une:
            continue
        if pid in PROTEGEES:
            continue
        c = w.get_raw("pages", pid)["content"]["raw"]
        cibles_ = a_retirer(c)
        if not cibles_:
            continue
        depart = c
        partis = []
        for i, j, cl, motif in sorted(cibles_, reverse=True):
            partis += re.findall(r'href="([^"]+)"', D.sans_code(c[i:j]))
            c = c[:i] + c[j:]
        if D.solde(c) != D.solde(depart):
            print("%-46s REFUSEE — le solde des <div> bouge" % url[:46])
            continue
        restants = D.liens(c)
        reste = D.liens(depart)
        for x in partis:
            if x in reste:
                reste.remove(x)
        if reste != restants:
            print("%-46s REFUSEE — lien(s) perdu(s) hors des sections visees" % url[:46])
            continue
        orph = [x for x in dict.fromkeys(partis) if x not in restants]
        for x in orph:
            orphelins_total.setdefault(x, []).append(url)

        print("%-46s %3d -> %3d ko · %d section(s) retiree(s)"
              % (url[:46], len(depart) // 1024, len(c) // 1024, len(cibles_)))
        for i, j, cl, motif in cibles_:
            print("        %-28s %5d o · %s" % (cl[:28], j - i, motif))
        if orph:
            print("        liens sans autre source sur la page : %s" % ", ".join(orph))
        if poser:
            open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
                 encoding="utf-8").write(depart)
            w.update_content("pages", pid, c, live=True)
            print("        pose")

    if orphelins_total:
        print("\n=== liens qui perdent leur source sur la page ===")
        for u, ou in sorted(orphelins_total.items()):
            print("   %-58s depuis %s" % (u[:58], ", ".join(x[:26] for x in ou)))
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
