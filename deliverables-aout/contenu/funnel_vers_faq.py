#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les sections MOFU et BOFU repassent dans la FAQ.

Demande du 15/10/2026 : ne pas garder deux sections autonomes au milieu de la
page, mais verser leur contenu dans l'accordeon de questions deja en place.

Ce que fait le script, page par page :
  1. retire les deux sections .hhf-wrap posees le matin meme ;
  2. retire leur feuille de style, devenue sans objet ;
  3. ajoute leur contenu a la FAQ, reformule en questions, au format
     <details> de la page ;
  4. reconstruit le FAQPage JSON-LD sur la FAQ complete, en remplacant celui
     qui existe — jamais en l'ajoutant une seconde fois.

GARDE-FOUS
  - sauvegarde avant ecriture ;
  - refus si _elementor_data n'est pas vide ;
  - refus si un « & » nu entre dans un <script> ;
  - refus s'il reste une section .hhf-wrap ou plus d'un bloc FAQPage ;
  - le contenu doit avoir diminue.

Usage :  python3 funnel_vers_faq.py            (blanc)
         python3 funnel_vers_faq.py --ecrire
"""

import html
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import ns_api as n                                        # noqa: E402

SAUVE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avant-funnel-faq")


# --------------------------------------------------------------------------
# Lecture equilibree
# --------------------------------------------------------------------------

def bornes_section(c, classe, depart=0):
    m = re.search(r'<section[^>]*class="[^"]*' + re.escape(classe)
                  + r'[^"]*"[^>]*>', c[depart:])
    if not m:
        return None
    i, p = depart + m.start(), 0
    for t in re.finditer(r"<section\b|</section>", c[i:]):
        p += 1 if t.group(0) != "</section>" else -1
        if p == 0:
            return (i, i + t.end())
    return None


def details(bloc):
    out = []
    for m in re.finditer(r"<details\b[^>]*>", bloc):
        i, p, d = m.start(), 0, None
        for t in re.finditer(r"<details\b|</details>", bloc[i:]):
            p += 1 if t.group(0) != "</details>" else -1
            if p == 0:
                d = bloc[i:i + t.end()]
                break
        if d is None:
            continue
        q = re.search(r"(?is)<summary[^>]*>(.*?)</summary>", d)
        if not q:
            continue
        out.append((html.unescape(re.sub(r"<[^>]+>", "", q.group(1))).strip(),
                    re.sub(r"(?is)</details>\s*$", "", d[q.end():])))
    return out


def texte(h):
    h = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", h)
    h = re.sub(r"(?is)</(p|li|h[1-6]|div)>", " ", h)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h))).strip()


def resume(h, maxi=320):
    t = re.sub(r"\s+", " ", texte(h).replace("&", " et ")).strip()
    if len(t) > maxi:
        coupe = t[:maxi]
        for sep in (". ", " : ", "; "):
            j = coupe.rfind(sep)
            if j > 140:
                t = coupe[:j + 1].strip()
                break
        else:
            t = coupe.rsplit(" ", 1)[0].rstrip(",;") + "."
    if t and t[-1] not in ".!?…":
        t += "."
    return t


def sans_amp_nu_dans_scripts(c):
    for m in re.finditer(r"(?is)<script\b[^>]*>(.*?)</script>", c):
        corps = m.group(1)
        for a in re.finditer(r"&", corps):
            if not re.match(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);",
                            corps[a.start():a.start() + 10]):
                return False
    return True


# --------------------------------------------------------------------------
# Les questions, reformulees depuis les cartes MOFU et les etapes BOFU
# --------------------------------------------------------------------------
P = "<p>%s</p>"

QUESTIONS = {
    4791: [
        ("Faut-il un WMS, ou l'ERP suffit-il&nbsp;?",
         P % "Un WMS gère l'entrepôt : emplacements, vagues de picking, "
             "réapprovisionnement de zone. Un ERP agroalimentaire gère le lot et "
             "la DLC. Tant que vos volumes tiennent sur un entrepôt et que la "
             "contrainte dominante est la date limite, l'ERP évite une deuxième "
             "base de données et une passerelle à maintenir."
         + P % "Au-delà, le module logistique se branche sur un WMS existant "
               "plutôt que de le remplacer."),
        ("Que faut-il saisir à la réception des marchandises&nbsp;?",
         P % "C'est là que tout se joue : si le lot fournisseur et la DLC "
             "n'entrent pas à la réception, ils n'existeront nulle part ensuite. "
             "Pesée à l'entrée, écart entre commandé et reçu, contrôle à "
             "réception, blocage qualité."
         + P % "Le stock se valorise sur le poids réellement reçu, pas sur le "
               "poids commandé."),
        ("Comment suivre les livraisons et les transporteurs&nbsp;?",
         P % "Statut d'expédition, preuve de livraison, écart de température le "
             "cas échéant, et retour de l'information dans la fiche client. Quand "
             "le transport est sous-traité, c'est l'échange de fichiers avec le "
             "transporteur qui porte le suivi."),
        ("Peut-on travailler avec un prestataire logistique&nbsp;?",
         P % "Oui. Un prestataire connecté reçoit les ordres de préparation et "
             "renvoie les confirmations : vous gardez la maîtrise du stock "
             "théorique, il gère le physique. L'enjeu est le format d'échange et "
             "la fréquence de synchronisation, pas l'outil."),
        ("Produits frais et restauration collective : quelles contraintes&nbsp;?",
         P % "Rotation FEFO imposée au picking, commandes à J-1, points de "
             "livraison multiples, et un cadencier par client. Les contraintes de "
             "la restauration collective ne sont pas celles d'un entrepôt sec."),
        ("Que montre la démonstration&nbsp;?",
         P % "On part d'une de vos réceptions et on la suit jusqu'au bon de "
             "livraison. Pas de jeu de données de démonstration : vos références, "
             "vos lots, vos clients."),
        ("Qu'est-ce qui fait varier le prix&nbsp;?",
         P % "Le nombre d'utilisateurs simultanés et la reprise de l'existant, "
             "rarement la liste des fonctions. Le détail est sur la page "
             "<a href=\"/tarifs/\">tarifs</a>."),
        ("Par où commencer&nbsp;?",
         P % "Par le métier avant le module. Si vous êtes grossiste ou "
             "distributeur, commencez par <a href=\"/negoce/\">l'ERP pour le "
             "négoce</a>. Si vous transformez, par "
             "<a href=\"/agroalimentaire/\">l'ERP agroalimentaire</a>. Le module "
             "logistique s'y rattache."),
    ],
    7910: [
        ("Quelle différence entre planification et ordonnancement&nbsp;?",
         P % "La planification décide quoi produire et en quelle quantité, sur "
             "des semaines. L'ordonnancement décide dans quel ordre et sur quelle "
             "ligne, sur des heures. Un outil qui ne fait que le premier vous "
             "laisse l'atelier à gérer au tableau blanc."),
        ("Comment fonctionne l'ordonnancement d'atelier&nbsp;?",
         P % "Il séquence les ordres de fabrication sur chaque ligne en tenant "
             "compte des changements de série, des nettoyages entre allergènes et "
             "des capacités réelles. En agroalimentaire, le temps de nettoyage est "
             "une contrainte de séquence, pas une perte."),
        ("Peut-on suivre la production en temps réel&nbsp;?",
         P % "Oui : quantité déclarée, écart au théorique, aléa signalé pendant "
             "que l'ordre tourne. Sans retour d'atelier, un planning est un vœu."),
        ("Et pour la fabrication alimentaire ou une cuisine centrale&nbsp;?",
         P % "Planifier une production alimentaire, c'est planifier des dates "
             "limites. Un ordre lancé trop tôt consomme de la durée de vie. "
             "Cuisines centrales et ateliers traiteur partagent cette contrainte "
             "avec l'industrie, à une autre échelle."),
        ("Comment obtenir un devis d'ordonnancement&nbsp;?",
         P % "Ce qui est chiffré, c'est le nombre de lignes et de postes : un "
             "atelier à trois lignes et un site à quinze ne se paramètrent pas "
             "pareil. Nomenclatures, gammes et calendriers se reprennent de "
             "l'existant. La grille est sur la page "
             "<a href=\"/tarifs/\">tarifs</a>, et vous pouvez "
             "<a href=\"/contact/\">nous décrire votre atelier</a> : nombre de "
             "lignes, de références et d'équipes suffit pour commencer."),
        ("Que montre la démonstration&nbsp;?",
         P % "Votre semaine la plus chargée. On prend une semaine réelle, avec "
             "ses aléas, et on la rejoue dans l'outil. C'est le seul test qui dit "
             "quelque chose."),
        ("Par quoi commencer avant l'ordonnancement&nbsp;?",
         P % "Si les nomenclatures et les rendements ne sont pas encore tenus, "
             "commencez par <a href=\"/fonctionnalites/fabrication/\">le logiciel "
             "de fabrication agroalimentaire</a> : l'ordonnancement s'appuie "
             "dessus."),
    ],
    4767: [
        ("Comment gérer le négoce de fruits et légumes&nbsp;?",
         P % "Prix qui bougent dans la journée, marchandise périssable, achat et "
             "vente dans le même geste : la vente se pilote à la marge sur le lot, "
             "pas sur une fiche article figée. Le détail est sur "
             "<a href=\"/negoce/\">l'ERP pour le négoce alimentaire</a>."),
        ("Faut-il un CRM ou une gestion commerciale&nbsp;?",
         P % "Un CRM suit la relation, une gestion commerciale sort les pièces. "
             "En agroalimentaire les deux se touchent : pendant l'appel, le "
             "commercial a besoin du cadencier, des impayés et du stock "
             "disponible. Voir <a href=\"/fonctionnalites/crm/\">le CRM "
             "agroalimentaire</a>."),
        ("Comment fonctionne la télévente avec un cadencier&nbsp;?",
         P % "Reprendre la commande précédente, proposer les manquants, repérer "
             "les ruptures avant d'appeler. Un cadencier bien tenu fait plus pour "
             "le panier moyen qu'un argumentaire."),
        ("Comment passe-t-on du devis à la préparation&nbsp;?",
         P % "Le devis devient commande, la commande devient bon de préparation, "
             "puis bon de livraison au poids pesé. Le chemin complet est décrit "
             "sur <a href=\"/fonctionnalites/logiciel-devis-commande-bon-livraison/\">"
             "logiciel devis, commande et bon de livraison</a>."),
        ("Où se connecter à son espace client&nbsp;?",
         P % "Cette page présente le module de vente, elle n'est pas l'accès à "
             "votre compte. Pour vous connecter à votre ERP, utilisez le lien "
             "transmis par votre intégrateur ou "
             "<a href=\"/contact/\">demandez-le-nous</a>."),
        ("Par où commencer si j'achète pour revendre&nbsp;?",
         P % "Par <a href=\"/negoce/\">la page négoce</a> : marge au lot, prix "
             "d'achat qui bouge, poids variable. C'est la page qui correspond à "
             "ce métier."),
        ("Et si je transforme ma marchandise&nbsp;?",
         P % "Commencez par <a href=\"/agroalimentaire/\">l'ERP "
             "agroalimentaire</a> : quand la vente est la sortie d'un atelier, "
             "elle s'y rattache, pas l'inverse."),
        ("Combien coûte le module de vente&nbsp;?",
         P % "Au poste, pas au module. Le nombre de commerciaux simultanés pèse "
             "davantage que le nombre de fonctions activées. La grille est sur la "
             "page <a href=\"/tarifs/\">tarifs</a>."),
    ],
}

NOMS = {4791: "logistique", 7910: "planification-production-erp", 4767: "vente"}


# --------------------------------------------------------------------------

def retirer_funnel(c):
    """Retire les deux sections .hhf-wrap et leur feuille de style."""
    k = 0
    while True:
        b = bornes_section(c, "hhf-wrap")
        if not b:
            break
        c = c[:b[0]] + c[b[1]:]
        k += 1
    c = re.sub(r'(?is)<style id="hh-funnel-css">.*?</style>\s*', "", c)
    return c, k


def ajouter_questions(c, questions):
    b = bornes_section(c, "faq-section")
    if not b:
        raise RuntimeError("faq-section introuvable")
    bloc = c[b[0]:b[1]]
    dern = None
    for m in re.finditer(r"</details>", bloc):
        dern = m
    if dern is None:
        raise RuntimeError("aucun <details> dans la FAQ")
    ouvr = re.findall(r"<details\b[^>]*>", bloc)[-1]
    summ = re.findall(r"<summary\b[^>]*>", bloc)[-1]
    ajout = ""
    for q, r in questions:
        if q.replace("&nbsp;", " ") in bloc or q in bloc:
            continue
        ajout += ouvr + summ + q + "</summary>" + r + "</details>"
    if not ajout:
        return c, 0
    pos = b[0] + dern.end()
    return c[:pos] + ajout + c[pos:], len(questions)


def refaire_faq_jsonld(c):
    """Remplace le FAQPage existant par un bloc reconstruit sur la FAQ complete."""
    c = re.sub(r'(?is)\s*<script type="application/ld\+json">(?=[^<]*FAQPage)'
               r'.*?</script>\s*', "\n", c)
    b = bornes_section(c, "faq-section")
    qs = details(c[b[0]:b[1]])
    if len(qs) < 3:
        raise RuntimeError("moins de 3 questions dans la FAQ")
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question",
                            "name": html.unescape(q).replace("\xa0", " "),
                            "acceptedAnswer": {"@type": "Answer",
                                               "text": resume(r)}}
                           for q, r in qs]}
    return (c + '\n<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False) + "</script>\n"), len(qs)


def main(poser=False):
    os.makedirs(SAUVE, exist_ok=True)
    print("mode :", "ECRITURE REELLE" if poser else "blanc (aucune écriture)", "\n")
    for pid, questions in QUESTIONS.items():
        d = n.call("wp/v2/pages/%d?context=edit&_fields=id,content,meta" % pid)
        if d["meta"].get("_elementor_data") not in ("", "[]", None):
            raise RuntimeError("%d : _elementor_data non vide" % pid)
        c = d["content"]["raw"]
        open(os.path.join(SAUVE, "%d.html" % pid), "w").write(c)
        avant = len(c)
        c, k = retirer_funnel(c)
        c, nq = ajouter_questions(c, questions)
        c, total = refaire_faq_jsonld(c)
        assert "hhf-wrap" not in c, "%d : une section funnel subsiste" % pid
        assert c.count('"FAQPage"') == 1, \
            "%d : %d blocs FAQPage" % (pid, c.count('"FAQPage"'))
        assert c.count("<h1") == 1, "%d : nombre de H1 anormal" % pid
        assert sans_amp_nu_dans_scripts(c), "%d : un & nu dans un <script>" % pid
        assert len(c) < avant, "%d : le contenu a grossi" % pid
        print("  %-30s %d section(s) retirée(s) · %d questions ajoutées · "
              "FAQ à %d questions · %+d o"
              % (NOMS[pid], k, nq, total, len(c) - avant))
        if poser:
            n.call("wp/v2/pages/%d" % pid, "POST", {"content": c})


if __name__ == "__main__":
    main(poser="--ecrire" in sys.argv)
