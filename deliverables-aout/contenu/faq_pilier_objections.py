#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rallonger la FAQ du pilier — par des objections, pas des definitions.

Les huit questions en place expliquent : qu'est-ce qu'un ERP, comment
fonctionne la tracabilite, quelle difference entre DLC et DLUO. Aucune ne
repond a ce qu'un dirigeant dit vraiment avant de signer : « on a deja un
logiciel », « mes gars ne sont pas informaticiens », « et si vous fermez ».

Les huit ajoutees sont de ce registre. Elles reprennent le composant
existant — hh2-faq-item, bouton, microdonnees Question/Answer — donc le
balisage structure s'etend tout seul, sans JSON-LD a maintenir a cote.

Aucune ne contient de chiffre de performance sans source : les reponses
en place en portent deja, et deux d'entre elles se contredisent d'une
page a l'autre sur la duree de deploiement. On n'en rajoute pas.
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

PID = 1726
URL = "/agroalimentaire/"
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/faq-pilier-avant")

OBJECTIONS = [
 ("Nous avons déjà un logiciel, faut-il vraiment tout reprendre ?",
  "<p>Non, et c'est rarement ce qui se passe. La plupart des entreprises "
  "gardent leur comptabilité et remplacent d'abord la gestion commerciale "
  "et la production — c'est là que le métier se joue, et c'est là que les "
  "outils généralistes atteignent leur limite.</p>"
  "<p>Le reste se branche : les écritures partent vers votre logiciel "
  "comptable, les commandes arrivent de vos clients par EDI, les pesées "
  "remontent de vos balances. Vous ne repartez pas d'une feuille blanche, "
  "vous remplacez la pièce qui coince.</p>"),

 ("Mes équipes ne sont pas informaticiennes. Vont-elles suivre ?",
  "<p>C'est l'objection la plus fréquente, et elle est légitime : un "
  "opérateur en atelier porte des gants, travaille dans le froid, et n'a "
  "pas le temps de chercher un menu.</p>"
  "<p>Ce qui change la donne n'est pas la formation, c'est le nombre de "
  "gestes. En production, la saisie se réduit à scanner un lot et à poser "
  "un poids. Les écrans de l'atelier ne montrent que ce que l'atelier doit "
  "voir. La complexité reste au bureau, là où elle a un sens.</p>"),

 ("Excel nous suffit depuis des années. Qu'est-ce qui change vraiment ?",
  "<p>Excel tient très bien tant qu'une seule personne écrit dedans et que "
  "la donnée ne se périme pas. L'agroalimentaire casse les deux "
  "hypothèses.</p><ul>"
  "<li><strong>Le lot.</strong> Retrouver où est parti un lot suspect "
  "demande de croiser des fichiers à la main, un jour où personne n'a le "
  "temps.</li>"
  "<li><strong>La date.</strong> Un classeur ne prévient pas qu'une DLC "
  "approche ; il faut penser à regarder.</li>"
  "<li><strong>Le poids variable.</strong> Une ligne de commande en pièces "
  "et une facture au kilo ne se réconcilient pas par une formule.</li>"
  "<li><strong>Le prix de revient.</strong> Il est juste le jour où on le "
  "calcule, et faux dès que les cours bougent.</li></ul>"
  "<p>Le jour où l'un de ces quatre points vous coûte une nuit de travail, "
  "vous avez la réponse.</p>"),

 ("Que paie-t-on exactement, au-delà de l'abonnement ?",
  "<p>Trois postes, et il faut les regarder ensemble :</p><ul>"
  "<li><strong>L'abonnement</strong>, fonction du nombre d'utilisateurs et "
  "des modules ouverts. Il couvre l'hébergement, les sauvegardes et les "
  "mises à jour — il n'y a pas de version à racheter.</li>"
  "<li><strong>La mise en route</strong>, facturée une fois : cadrage, "
  "reprise de vos données, paramétrage de vos recettes et de vos tarifs, "
  "formation.</li>"
  "<li><strong>Les interfaces</strong>, quand il faut parler à une balance, "
  "à une étiqueteuse, à un automate ou à la plateforme EDI d'une "
  "enseigne.</li></ul>"
  "<p>Ce qui n'est pas dans le devis ne se facture pas en cours de route. "
  "Demandez le détail des trois postes avant de comparer deux offres : "
  "c'est le seul moyen de comparer la même chose.</p>"),

 ("Et si vous fermez ? Que deviennent nos données ?",
  "<p>Elles sont à vous, et elles sortent. À tout moment, vous exportez "
  "l'intégralité de vos articles, clients, fournisseurs, tarifs, stocks, "
  "mouvements de lots et pièces commerciales dans des formats ouverts, "
  "lisibles sans notre logiciel.</p>"
  "<p>C'est aussi une obligation pratique : la traçabilité doit rester "
  "consultable pendant toute la durée de conservation de vos archives, "
  "quel que soit l'outil que vous utiliserez d'ici là. Posez la question à "
  "tout éditeur que vous consultez, et demandez à voir l'export réel — pas "
  "la clause du contrat.</p>"),

 ("Notre activité est très particulière. Un logiciel du marché peut-il la gérer ?",
  "<p>La bonne question n'est pas « est-ce que ça gère mon cas », mais "
  "« est-ce que ça se paramètre ou est-ce que ça se développe ».</p>"
  "<p>Un rendement de cuisson qui varie selon le calibre, une consigne de "
  "palette, un tarif au cours du jour, une recette à trois niveaux avec "
  "des freintes à chaque étage : ce sont des situations courantes du "
  "secteur, déjà prévues, qui se règlent en paramétrage. Ce qui relève "
  "vraiment du sur-mesure est rare — et on vous le dit avant, pas "
  "après.</p>"),

 ("Qui nous accompagne une fois le logiciel démarré ?",
  "<p>Un interlocuteur qui connaît l'agroalimentaire, pas un centre "
  "d'appels qui lit une fiche. La différence se voit le jour où vous "
  "appelez parce qu'un lot bloque un départ de camion : il faut quelqu'un "
  "qui comprenne l'urgence sans qu'on la lui explique.</p>"
  "<p>Le démarrage est assisté, puis le suivi continue : ajustement de "
  "paramétrage, formation des nouveaux arrivants, ouverture d'un module "
  "quand l'activité l'exige.</p>"),

 ("Sommes-nous trop petits pour un ERP ?",
  "<p>Ce n'est pas une affaire de taille mais de nombre de croisements à "
  "tenir en tête. Une dizaine de personnes, deux cents références, des "
  "lots, des dates et deux enseignes à livrer : c'est déjà plus que ce "
  "qu'un tableur et une mémoire peuvent porter sans erreur.</p>"
  "<p>À l'inverse, une activité à quelques références stables, sans lot ni "
  "date courte, n'en a pas besoin. Le déclencheur, en général, est un de "
  "ces trois moments : un audit qui demande une traçabilité qu'on ne sait "
  "pas produire, une enseigne qui impose l'EDI, ou une marge qui se dégrade "
  "sans qu'on sache dire où.</p>"),
]


def item(n, question, reponse):
    return (
        '<div class="hh2-faq-item" itemscope itemprop="mainEntity" '
        'itemtype="https://schema.org/Question">'
        '<button class="hh2-faq-question" aria-expanded="false" '
        'aria-controls="hh2-faq-a%d">'
        '<span itemprop="name">%s</span>'
        '<span class="hh2-faq-icon"><svg xmlns="http://www.w3.org/2000/svg" '
        'fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M19.5 8.25l-7.5 7.5-7.5-7.5"/></svg></span>'
        '</button>'
        '<div class="hh2-faq-answer-wrapper" id="hh2-faq-a%d" itemscope '
        'itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">'
        '<div class="hh2-faq-answer" itemprop="text">%s</div></div></div>'
        % (n, question, n, reponse))


def main():
    poser = "--poser" in sys.argv
    c = w.get_raw("pages", PID)["content"]["raw"]
    depart = c

    for q, r in OBJECTIONS:
        if "&" in q + r:
            raise SystemExit("ARRET — une esperluette nue : WordPress la "
                             "transformerait en entite")

    i = c.find('<div class="hh2-faq-list">')
    if i < 0:
        raise SystemExit("ARRET — liste de FAQ introuvable")
    fin = c.find('</div>', c.rfind('</div>', 0, c.find('<div class="section-footer"', i))) \
        if False else None
    # La fin de la liste : le dernier </div> avant la fermeture de la section.
    j = c.find('<section', i + 10)
    sec_fin = c.find('</section>', i)
    dernier = c.rfind('</div>', i, sec_fin)
    if dernier < 0:
        raise SystemExit("ARRET — fin de liste introuvable")

    n0 = len(re.findall(r'<div class="hh2-faq-item"', c))
    ajout = "".join(item(n0 + k + 1, q, r) for k, (q, r) in enumerate(OBJECTIONS))
    c = c[:dernier] + ajout + c[dernier:]

    # ── controles ────────────────────────────────────────────────────────
    n1 = len(re.findall(r'<div class="hh2-faq-item"', c))
    if n1 != n0 + len(OBJECTIONS):
        raise SystemExit("ARRET — %d questions au lieu de %d" % (n1, n0 + len(OBJECTIONS)))
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    if D.liens(c) != D.liens(depart):
        raise SystemExit("ARRET — les liens bougent")
    if c.count("<section class=") != depart.count("<section class="):
        raise SystemExit("ARRET — le nombre de sections bouge")
    for nom in ("Question", "Answer"):
        a = len(re.findall(r'schema.org/%s"' % nom, depart))
        b = len(re.findall(r'schema.org/%s"' % nom, c))
        if b != a + len(OBJECTIONS):
            raise SystemExit("ARRET — balisage %s : %d -> %d" % (nom, a, b))
    ids = re.findall(r'aria-controls="([^"]+)"', c)
    if len(ids) != len(set(ids)):
        raise SystemExit("ARRET — identifiants d'accordeon en double")
    if len(c) > D.PLAFOND:
        raise SystemExit("ARRET — %d o, au-dela du seuil de rendu" % len(c))

    print("%s  %d -> %d o" % (URL, len(depart), len(c)))
    print("   FAQ : %d -> %d questions" % (n0, n1))
    for q, _ in OBJECTIONS:
        print("      + %s" % q)
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % PID), "w",
             encoding="utf-8").write(depart)
        w.update_content("pages", PID, c, live=True)
        print("\n   pose.")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
