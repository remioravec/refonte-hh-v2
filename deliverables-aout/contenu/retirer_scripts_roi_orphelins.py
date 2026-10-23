#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les scripts de l'outil ROI retire en septembre sont restes dans quatre pages.

En septembre, completer_specialisees.py a retire de cinq pages
/fonctionnalites/ la section de l'outil ROI et sa feuille de style. Le
<script> qui pilotait l'outil, lui, est reste. Mesure du 06/10/2026 sur les
pages servies : aucune ne contient plus l'element que ces scripts cherchent
(id="roiI1" pour quatre d'entre elles, la grille .roi-block pour la cinquieme).
Ils sortent donc immediatement, mais ils pesent et — surtout — ils portent des
« & » nus a l'interieur d'un <script>. WordPress les transforme en &#038; au
prochain enregistrement du contenu : toute ecriture future sur ces pages
casserait la chaine de requete qu'ils construisent. 7911 a ete nettoyee le
06/10 en meme temps que sa mise a jour de contenu ; restent les quatre autres.

Ce n'est pas une optimisation, c'est une reparation : on retire du code mort
qui est aussi un piege d'ecriture.

ACCEPTATION : plus aucun « & » nu dans un <script> sur ces quatre pages, et
aucune difference visible sur le rendu servi.

Usage :  python3 retirer_scripts_roi_orphelins.py            (blanc)
         python3 retirer_scripts_roi_orphelins.py --ecrire
"""

import json
import os
import re
import sys

sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import ns_api as n                                        # noqa: E402

SAUVE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avant-roi")

# (id, url, la marque qui identifie le script, l'element qu'il cherche)
CIBLES = [
    (7905, "/fonctionnalites/facturation-automatique-bon-livraison/",
     "roi-calculator-facturation-bl", None),
    (7909, "/fonctionnalites/gestion-rendement-matiere-logiciel/",
     'getElementById("roiI1")', 'id="roiI1"'),
    (7910, "/fonctionnalites/planification-production-erp/",
     'getElementById("roiI1")', 'id="roiI1"'),
    (7912, "/fonctionnalites/gestion-consigne-bouteille-logiciel/",
     'getElementById("roiI1")', 'id="roiI1"'),
]


def amp_nus(bloc):
    return [a.start() for a in re.finditer(r"&", bloc)
            if not re.match(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);",
                            bloc[a.start():a.start() + 10])]


def echapper_ld_json(c):
    """Ecrit \\u0026 les « & » litteraux des blocs ld+json."""
    morceaux, total = [], 0
    for m in re.finditer(r"(?is)<script\b([^>]*ld\+json[^>]*)>(.*?)</script>", c):
        corps, nus = m.group(2), amp_nus(m.group(2))
        if not nus:
            continue
        for i in sorted(nus, reverse=True):
            corps = corps[:i] + "\\u0026" + corps[i + 1:]
        json.loads(corps)
        morceaux.append((m.start(), m.end(),
                         "<script" + m.group(1) + ">" + corps + "</script>"))
        total += len(nus)
    for a, b, neuf in sorted(morceaux, reverse=True):
        c = c[:a] + neuf + c[b:]
    return c, total


def corps_sans_code(c):
    c = re.sub(r"(?is)<script\b.*?</script>", "", c)
    return re.sub(r"(?is)<style\b.*?</style>", "", c)


def main(poser=False):
    os.makedirs(SAUVE, exist_ok=True)
    print("mode :", "ECRITURE REELLE" if poser else "blanc (aucune écriture)", "\n")
    for pid, url, marque, element in CIBLES:
        d = n.call("wp/v2/pages/%d?context=edit&_fields=id,content,meta" % pid)
        if d["meta"].get("_elementor_data") not in ("", "[]", None):
            raise RuntimeError("%d : _elementor_data non vide" % pid)
        c = d["content"]["raw"]
        open(os.path.join(SAUVE, "%d.html" % pid), "w").write(c)
        avant = len(c)

        # l'element pilote doit etre absent du corps : sinon le script sert
        if element is not None and element in c:
            raise RuntimeError("%d : %s existe encore, le script n'est PAS mort"
                               % (pid, element))
        if element is None and "roi-block" in corps_sans_code(c):
            raise RuntimeError("%d : la grille .roi-block existe encore" % pid)

        vise = [m for m in re.finditer(r"(?is)<script\b[^>]*>(.*?)</script>", c)
                if marque in m.group(1)]
        if len(vise) != 1:
            raise RuntimeError("%d : %d script(s) portant « %s »"
                               % (pid, len(vise), marque))
        m = vise[0]
        print("  %-6d %-58s script de %5d o, %d « & » nus"
              % (pid, url[:58], len(m.group(0)), len(amp_nus(m.group(1)))))
        c = c[:m.start()] + c[m.end():]

        # plus aucun « & » nu dans un <script> apres retrait
        # les « & » qui restent sont des litteraux de ld+json (« Fondateur &
        # CEO ») : on les ecrit \\u0026, l'echappement JSON, qui survit a
        # l'enregistrement. Le bloc doit rester du JSON valide.
        c, echappes = echapper_ld_json(c)
        restants = sum(len(amp_nus(x.group(1)))
                       for x in re.finditer(r"(?is)<script\b[^>]*>(.*?)</script>", c))
        print("         après : %d o, %d « & » échappés en ld+json, %d nus restants"
              % (len(c), echappes, restants))
        assert restants == 0, "%d : il reste des « & » nus" % pid
        assert c.count("<h1") == 1, "%d : nombre de H1 anormal" % pid
        assert len(c) < avant, "%d : le contenu a grossi" % pid
        if poser:
            n.call("wp/v2/pages/%d" % pid, "POST", {"content": c})


if __name__ == "__main__":
    main(poser="--ecrire" in sys.argv)
