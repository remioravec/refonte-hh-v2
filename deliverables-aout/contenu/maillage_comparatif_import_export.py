#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liens entrants vers /blog/meilleurs-erp-import-export/.

Mesure du 06/10/2026, sur le contenu en base, hors menu et pied de page :

  /fonctionnalites/import-export/                     517 liens entrants
      dont 502 sur trois ancres repetees 167 a 168 fois chacune
  /fonctionnalites/logiciel-devis-commande-bon-livraison/   164 liens entrants
      tous avec la meme ancre, « Logiciel Devis Commande BL »
  /blog/meilleurs-erp-import-export/                    3 liens entrants

La troisieme est pourtant la page qui RANKE sur cette famille de requetes :
position 8,4 sur « logiciel import export » (226 impressions sur 90 jours) et
9,7 sur « logiciel gestion commerciale import export » (134 impressions).
Les deux autres recoivent des centaines de liens d'un bloc de gabarit, a
ancre unique — exactement ce que la regle 2 interdit.

On ne reecrit pas 500 liens de gabarit ici : c'est le ticket T20. On pose
trois liens editoriaux, contigus, a ancres differentes, dans des phrases qui
parlent deja du sujet. Le quatrieme a ete pose le meme jour depuis
/fonctionnalites/import-export/, avec l'ancre « logiciel de gestion
commerciale import export ».

ACCEPTATION : la page passe de 3 a 6 liens entrants, portes par 4 ancres
distinctes, et aucune page hote ne perd de lien existant.

Usage :  python3 maillage_comparatif_import_export.py            (blanc)
         python3 maillage_comparatif_import_export.py --ecrire
"""

import os
import re
import sys

sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import ns_api as n                                        # noqa: E402

CIBLE = "/blog/meilleurs-erp-import-export/"
SAUVE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avant-maillage")

# (id, type, url, texte a trouver tel quel, phrase ajoutee a sa suite)
POSES = [
    (6074, "pages", "/negoce/achats-approvisionnements/",
     "Intégrez les frais de transport, droits de douane, commissions et "
     "calculez le PMP réel de chaque référence. Marge nette fiable.",
     " Notre <a href=\"%s\">comparatif des logiciels import export</a> "
     "détaille ce calcul, éditeur par éditeur." % CIBLE),

    (5966, "pages", "/implantation-maurice/",
     "Gérez vos activités en zone franche avec un ERP qui intègre la gestion "
     "multi-devises, les règles douanières et la fiscalité mauricienne.",
     " Le choix d'un <a href=\"%s\">logiciel import export</a> se joue "
     "d'abord sur ces trois points." % CIBLE),

    (5269, "posts", "/blog/erp-grossiste-distributeur/",
     "rattrape ces trois-là par développement spécifique.</p>",
     None),      # insertion en fin de paragraphe, voir ci-dessous
]

# Pour 5269, le paragraphe hote est long : on ajoute la phrase juste avant sa
# fermeture, donc a la fin du paragraphe, et non au milieu.
PARA_5269 = (
    " Les distributeurs qui achètent hors Union européenne y ajoutent le "
    "calcul des frais d'approche : c'est le critère que compare notre dossier "
    "sur l'<a href=\"%s\">ERP import export pour le négoce alimentaire</a>."
    % CIBLE)


def fin_du_paragraphe(c, depart):
    """Position de la fermeture du <p> qui contient `depart`."""
    i = c.rfind("<p>", 0, depart)
    j = c.find("</p>", depart)
    if i < 0 or j < 0 or "<p>" in c[depart:j]:
        raise RuntimeError("paragraphe hôte introuvable ou imbriqué")
    return j


def main(poser=False):
    os.makedirs(SAUVE, exist_ok=True)
    print("mode :", "ECRITURE REELLE" if poser else "blanc (aucune écriture)", "\n")
    for pid, kind, url, trouve, phrase in POSES:
        d = n.call("wp/v2/%s/%d?context=edit&_fields=id,content,meta"
                   % (kind, pid))
        if str(d["meta"].get("_elementor_data")) not in ("[]", "", "None"):
            raise RuntimeError("%d : _elementor_data non vide" % pid)
        c = d["content"]["raw"]
        open(os.path.join(SAUVE, "%d.html" % pid), "w").write(c)
        avant, liens_avant = len(c), c.count('<a ')
        if CIBLE in c:
            print("  %-6d %-52s déjà lié, on passe" % (pid, url[:52]))
            continue
        if c.count(trouve) != 1:
            raise RuntimeError("%d : %d occurrence(s) du texte hôte"
                               % (pid, c.count(trouve)))
        if phrase is None:                       # 5269 : fin de paragraphe
            # le meme texte figure aussi dans le FAQPage JSON-LD de la page :
            # on vise la fermeture </p>, qui n'existe que dans le HTML.
            j = c.index(trouve) + len(trouve) - len("</p>")
            c = c[:j] + PARA_5269 + c[j:]
            ancre = "ERP import export pour le négoce alimentaire"
        else:
            i = c.index(trouve) + len(trouve)
            c = c[:i] + phrase + c[i:]
            ancre = re.search(r">([^<]+)</a>", phrase).group(1)
        assert c.count(CIBLE) == 1, "%d : lien posé %d fois" % (pid, c.count(CIBLE))
        assert c.count('<a ') == liens_avant + 1, \
            "%d : le compte de liens a bougé de plus de un" % pid
        assert c.count("<h1") <= 1, "%d : nombre de H1 anormal" % pid
        print("  %-6d %-52s +%d o   ancre « %s »"
              % (pid, url[:52], len(c) - avant, ancre))
        if poser:
            n.call("wp/v2/%s/%d" % (kind, pid), "POST", {"content": c})


if __name__ == "__main__":
    main(poser="--ecrire" in sys.argv)
