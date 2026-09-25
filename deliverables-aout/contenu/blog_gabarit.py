#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le gabarit d'article : ce qu'on change, et ce qu'on ne touche pas.

CE QU'ON NE TOUCHE PAS. La structure des articles est deja homogene sur
les 103 : entete, fil d'ariane, sommaire, corps, cartes laterales,
partage. Et le simulateur reste — decision de Remi du 22/09 : sur une
requete de blog, il repond a l'intention de recherche.

CE QU'ON CHANGE.

1. LA FAUSSE FAQ. La section « Les reponses a vos questions » contient
   deux cartes de rendez-vous, pas des questions. Pire, le balisage
   FAQPage declare a Google « Voyez Hello Harel sur vos donnees » comme
   une question. Elle devient une vraie FAQ en accordeons, avec des
   reponses dans le HTML, et le balisage porte enfin de vraies questions.

2. LES DEUX CARTES DE RENDEZ-VOUS ne disparaissent pas : elles passent
   dans un bloc qui dit son nom, avec leurs liens de suivi intacts.

3. LES ACCENTS des titres. « tracabilite », « cout », « integree » en H2 :
   du francais sans accents, lu par le visiteur.

LES QUESTIONS SONT TIREES DE L'ARTICLE. Chacune trouve sa reponse dans le
corps du texte ou dans un texte reglementaire public. On n'ajoute aucun
chiffre, aucune promesse de resultat, aucun cas client.
"""

import re

# ── les accents manquants, releves dans les titres du parc ────────────────
ACCENTS = [
    ("tracabilite", "traçabilité"), ("Tracabilite", "Traçabilité"),
    ("integree", "intégrée"), ("integre", "intégré"), ("Integree", "Intégrée"),
    ("reglementaire", "réglementaire"), ("Reglementaire", "Réglementaire"),
    ("reduire", "réduire"), ("Reduire", "Réduire"),
    ("reception", "réception"), ("Reception", "Réception"),
    ("parametrables", "paramétrables"), ("parametrable", "paramétrable"),
    ("etiquetage", "étiquetage"), ("Etiquetage", "Étiquetage"),
    ("conformite", "conformité"), ("Conformite", "Conformité"),
    ("cout", "coût"), ("Cout", "Coût"),
    ("resultats", "résultats"), ("Resultats", "Résultats"),
    ("apres", "après"), ("Apres", "Après"),
    ("securite", "sécurité"), ("Securite", "Sécurité"),
    ("qualite", "qualité"), ("Qualite", "Qualité"),
    ("peremption", "péremption"), ("Peremption", "Péremption"),
    ("reference", "référence"), ("Reference", "Référence"),
    ("matiere", "matière"), ("Matiere", "Matière"),
    ("derniere", "dernière"), ("Derniere", "Dernière"),
    ("specifique", "spécifique"), ("Specifique", "Spécifique"),
    ("operationnel", "opérationnel"), ("Operationnel", "Opérationnel"),
    ("televente", "télévente"), ("Televente", "Télévente"),
    ("previsible", "prévisible"), ("Previsible", "Prévisible"),
    ("eleve", "élevé"), ("Eleve", "Élevé"),
    ("opacite", "opacité"), ("Opacite", "Opacité"),
    ("limitee", "limitée"), ("Limitee", "Limitée"),
    ("visibilite", "visibilité"), ("Visibilite", "Visibilité"),
    ("eclatee", "éclatée"), ("Eclatee", "Éclatée"),
    ("sanitaires", "sanitaires"),
    ("Definition", "Définition"), ("definition", "définition"),
    ("realise", "réalisé"), ("Realise", "Réalisé"),
    ("scenario", "scénario"), ("Scenario", "Scénario"),
    ("decouvrir", "découvrir"), ("Decouvrir", "Découvrir"),
    ("maitriser", "maîtriser"), ("Maitriser", "Maîtriser"),
    ("benefices", "bénéfices"), ("Benefices", "Bénéfices"),
    ("donnees", "données"), ("Donnees", "Données"),
    ("deploiement", "déploiement"), ("Deploiement", "Déploiement"),
    ("possibilite", "possibilité"), ("Possibilite", "Possibilité"),
    ("coeur", "cœur"), ("Coeur", "Cœur"),
]


def accentuer_titres(c):
    """Corrige les titres seulement — jamais le corps, ou un mot sans
    accent peut etre volontaire (un nom propre, une URL, du code)."""
    n = [0]

    def rep(m):
        ouvre, texte, ferme = m.group(1), m.group(2), m.group(3)
        avant = texte
        for faux, vrai in ACCENTS:
            texte = re.sub(r"\b%s\b" % faux, vrai, texte)
        if texte != avant:
            n[0] += 1
        return ouvre + texte + ferme

    c = re.sub(r"(<h[1-4][^>]*>)(.*?)(</h[1-4]>)", rep, c, flags=re.S)
    return c, n[0]


def bloc_faq(entete, paires, css):
    """La FAQ en accordeons, plus son balisage."""
    import json
    det = ""
    for q, r in paires:
        det += ('<details itemscope itemprop="mainEntity" '
                'itemtype="https://schema.org/Question">'
                '<summary itemprop="name">%s</summary>'
                '<div class="fa2-r" itemscope itemprop="acceptedAnswer" '
                'itemtype="https://schema.org/Answer"><div itemprop="text">%s</div></div>'
                '</details>' % (q, r))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer",
                            "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()}}
        for q, r in paires]}
    return (css + '<section class="faq-section" itemscope '
            'itemtype="https://schema.org/FAQPage"><div class="container">'
            + entete + '<div class="fa2">%s</div></div>' % det
            + '<script type="application/ld+json">%s</script></section>'
            % json.dumps(ld, ensure_ascii=False))


CSS_CTA = """<style id="hh-blog-cta">
.hhb-cta{max-width:860px;margin:2.2rem auto 0 !important;display:grid !important;
 grid-template-columns:repeat(auto-fit,minmax(260px,1fr)) !important;
 gap:1rem !important;padding:0 !important;list-style:none !important}
.hhb-cta li{margin:0 !important}
.hhb-cta a{display:block !important;height:100% !important;
 padding:1.25rem 1.4rem !important;background:#fff !important;
 border:1px solid #e2e8f0 !important;border-radius:16px !important;
 text-decoration:none !important;transition:border-color .18s,box-shadow .18s}
.hhb-cta a:hover{border-color:#7DD3FC !important;
 box-shadow:0 14px 32px -26px rgba(15,23,42,.6) !important}
.hhb-cta b{display:block !important;color:#0f172a !important;font-size:1.02rem !important;
 font-weight:700 !important;margin-bottom:.3rem !important}
.hhb-cta span{display:block !important;color:#475569 !important;font-size:.92rem !important;
 line-height:1.6 !important}
.hhb-cta em{display:inline-block !important;margin-top:.6rem !important;
 color:#0369A1 !important;font-style:normal !important;font-weight:700 !important;
 font-size:.9rem !important}
.hhb-cta-t{max-width:860px;margin:2.4rem auto .2rem !important;
 font-size:1.3rem !important;font-weight:800 !important;color:#0f172a !important}
</style>"""


def bloc_cta(cartes):
    """cartes : [(titre, texte, libelle du lien, href)]

    La carte n'est PAS un lien. Un soulignement se transmet du lien a tout
    ce qu'il contient, et un descendant ne peut pas l'annuler : l'ancienne
    version soulignait le titre, le texte et le bouton. Seul le bouton est
    donc un lien, et la carte est un simple conteneur.
    """
    # Le second bouton est marque dans le balisage et non deduit de sa
    # position : un selecteur par rang se fait battre trop facilement.
    li = "".join('<li><div class="hhb-c"><b>%s</b><span>%s</span>'
                 '<a class="hhb-b%s" href="%s">%s →</a></div></li>'
                 % (t, d, ("" if k == 0 else " hhb-b2"), h, lib)
                 for k, (t, d, lib, h) in enumerate(cartes))
    return (CSS_CTA + '<h2 class="hhb-cta-t">Passer à la suite</h2>'
            '<ul class="hhb-cta">%s</ul>' % li)


# ══════════════════════════════════════════════════════ l'article temoin
#
# Six questions, toutes tirees du corps de l'article : le cadre
# reglementaire, la difference entre les trois dates, FEFO contre FIFO, le
# plan de rappel, l'etiquetage et la limite du tableur. Aucun chiffre de
# resultat, aucun cas client.

TEMOIN = [
 ("Quelle est la différence entre DLC, DDM et DLUO ?",
  "<p>Les trois dates ne disent pas la même chose, et ne se gèrent pas de la "
  "même façon en stock.</p><ul>"
  "<li><strong>La DLC</strong> — date limite de consommation, « à consommer "
  "jusqu'au ». Elle concerne les denrées très périssables. Au-delà, le produit "
  "ne doit plus être commercialisé ni consommé.</li>"
  "<li><strong>La DDM</strong> — date de durabilité minimale, « à consommer de "
  "préférence avant ». Elle porte sur des produits stables. Après cette date, "
  "le produit peut perdre en qualité sans devenir dangereux.</li>"
  "<li><strong>La DLUO</strong> — ancienne appellation de la DDM, encore "
  "présente sur des documents et dans des habitudes de langage.</li></ul>"
  "<p>La conséquence pratique est simple : une DLC impose une rotation stricte "
  "et une alerte courte, une DDM tolère un horizon plus long. Un stock qui "
  "mélange les deux sans les distinguer se pilote mal.</p>"),

 ("Que dit le règlement CE 178/2002 sur la traçabilité ?",
  "<p>Ce règlement européen pose le principe de la traçabilité à toutes les "
  "étapes de la chaîne alimentaire. Ce qu'il impose en pratique :</p><ul>"
  "<li><strong>Savoir d'où vient chaque produit</strong> : identifier les "
  "fournisseurs des denrées et des ingrédients entrés dans l'entreprise.</li>"
  "<li><strong>Savoir où il est parti</strong> : identifier les entreprises "
  "auxquelles les produits ont été livrés.</li>"
  "<li><strong>Pouvoir le démontrer</strong> : disposer de systèmes et de "
  "procédures permettant de mettre cette information à disposition des "
  "autorités qui la demandent.</li>"
  "<li><strong>Retirer ce qui doit l'être</strong> : engager un retrait ou un "
  "rappel lorsqu'une denrée est jugée non conforme.</li></ul>"
  "<p>C'est ce qu'on appelle la règle « un pas en avant, un pas en arrière ». "
  "Elle ne demande pas un logiciel, elle demande une chaîne d'information "
  "complète et disponible.</p>"),

 ("FEFO ou FIFO : quelle méthode choisir pour des produits périssables ?",
  "<p>Les deux méthodes règlent l'ordre dans lequel on sort les stocks, mais "
  "elles ne répondent pas à la même question.</p><ul>"
  "<li><strong>FIFO</strong> — premier entré, premier sorti. On sert dans "
  "l'ordre d'arrivée. Pertinent quand la date de péremption suit l'ordre des "
  "réceptions, ce qui n'est pas toujours le cas.</li>"
  "<li><strong>FEFO</strong> — premier périmé, premier sorti. On sert dans "
  "l'ordre des dates limites, quelle que soit la date d'entrée.</li></ul>"
  "<p>Pour une denrée périssable, le FEFO est la seule méthode cohérente : un "
  "lot reçu ce matin avec une DLC courte doit partir avant un lot reçu la "
  "semaine dernière avec une DLC longue. Appliquer le FIFO dans ce cas revient "
  "à fabriquer de la perte.</p>"),

 ("Que doit contenir un plan de rappel produit ?",
  "<p>Un rappel se prépare avant d'en avoir besoin. Les éléments à pouvoir "
  "produire rapidement :</p><ul>"
  "<li><strong>L'identification du lot</strong> : numéro, date de fabrication, "
  "quantité produite et quantité encore en stock.</li>"
  "<li><strong>La traçabilité amont</strong> : les matières premières et les "
  "fournisseurs concernés par ce lot.</li>"
  "<li><strong>La traçabilité aval</strong> : la liste des clients livrés, les "
  "quantités et les bons de livraison correspondants.</li>"
  "<li><strong>Les enregistrements</strong> : contrôles, températures et "
  "non-conformités rattachés au lot.</li>"
  "<li><strong>Les destinataires à prévenir</strong> : clients, autorités "
  "compétentes et, selon les cas, consommateurs.</li></ul>"
  "<p>La différence entre un rappel ciblé et un rappel de gamme entière tient "
  "à un seul point : la capacité à dire précisément qui a reçu quoi.</p>"),

 ("Quelles mentions l'étiquetage INCO impose-t-il ?",
  "<p>Le règlement INCO fixe les informations obligatoires sur les denrées "
  "préemballées. Les principales :</p><ul>"
  "<li><strong>La dénomination de la denrée</strong> et la liste des "
  "ingrédients, par ordre décroissant de poids.</li>"
  "<li><strong>Les allergènes</strong>, mis en évidence dans la liste des "
  "ingrédients — en gras, en majuscules ou par un autre contraste.</li>"
  "<li><strong>La date</strong> : DLC ou DDM selon la nature du produit, et "
  "les conditions de conservation qui vont avec.</li>"
  "<li><strong>La quantité nette</strong> et, le cas échéant, le poids net "
  "égoutté.</li>"
  "<li><strong>La déclaration nutritionnelle</strong> et l'identification de "
  "l'exploitant responsable.</li></ul>"
  "<p>Le point qui coûte cher n'est pas la liste : c'est de la tenir à jour "
  "quand une recette change ou qu'un fournisseur est remplacé.</p>"),

 ("Un tableur suffit-il pour suivre les lots et les DLC ?",
  "<p>Un tableur tient tant que le nombre de lots reste petit. Il cède sur "
  "trois points, et toujours au mauvais moment.</p><ul>"
  "<li><strong>Le lien entre les lots</strong> : un tableur ne relie pas un "
  "bon de livraison à un lot de matière première. Le jour d'un rappel, cette "
  "chaîne se reconstitue à la main.</li>"
  "<li><strong>L'alerte</strong> : une date limite ne se surveille pas toute "
  "seule dans une grille. Il faut penser à l'ouvrir.</li>"
  "<li><strong>Le temps réel</strong> : le stock d'un tableur est celui de la "
  "dernière saisie, pas celui de la dernière sortie.</li></ul>"
  "<p>Le tableur garde sa place pour une analyse ponctuelle. Il ne tient pas "
  "un stock qui bouge tous les jours et dont chaque lot porte une date.</p>"),
]
