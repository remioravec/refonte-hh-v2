#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roadmap contenu — semaine du 19/10/2026, avec la boucle complete.

Trois mises a jour : /fonctionnalites/logistique/, /planification-production-erp/
et /vente/.

LA BOUCLE, dans l'ordre demande :

1. PAGE GENERANT DES DEMOS. Mesure sur la base d'attribution, 64 demandes
   depuis le 01/07/2026 : l'accueil en porte 29, /negoce/ 8, /agroalimentaire/
   5, puis des articles de blog. AUCUNE page /fonctionnalites/ n'en a jamais
   porte une seule. Les trois pages de la semaine appartiennent donc a la
   famille qui ne convertit pas : on ne se contente pas de les reecrire, on
   leur ajoute l'etage qui manque et on les branche sur les pages qui, elles,
   convertissent.

2. REQUETES SECONDAIRES. Search Console, 17/07 au 12/10, page par page. Ce
   sont elles qui dictent les sections ajoutees, pas une idee de plan.
     logistique    : prestataire logistique connecte erp (55 impressions),
                     wms agroalimentaire, reception marchandises,
                     suivi livraisons transporteurs, produits frais
     planification : devis logiciel d'ordonnancement (60), outil
                     d'ordonnancement et de planification (40), logiciel
                     ordonnancement atelier (36), planification fabrication
                     alimentaire (24), temps reel, CBN
     vente         : negoce fruits et legumes, crm agroalimentaire,
                     gestion des ventes agroalimentaire

3. CARTOGRAPHIE DE LA DEMANDE. Chaque bloc MOFU repond a une sous-intention
   reellement mesuree, avec le volume d'impressions en regard. Rien n'est
   ajoute qui ne soit adosse a une ligne de la Search Console.

4. SECTIONS MOFU ET BOFU. MOFU : le visiteur compare, on lui donne le cas
   d'usage qui est le sien. BOFU : il choisit, on lui donne ce qui fait
   varier le prix, ce qu'il verra en demo, et le lien vers les pages qui
   convertissent.

DEUX ENSEIGNEMENTS A REMONTER
  - /fonctionnalites/vente/ est en position 1 sur « hello harel connexion »
    (26 impressions) et « helloharel » (44). Des clients qui cherchent leur
    espace de connexion atterrissent sur une page commerciale. C'est un
    defaut d'experience autant qu'un signal gache.
  - /fonctionnalites/planification-production-erp/ vise « planification »
    alors que la demande dit « ordonnancement » : 36 + 40 + 60 impressions
    sur des formulations en ordonnancement, contre quelques unites en
    planification. Le H1 porte deja les deux, le MOFU creuse le second.

GARDE-FOUS
  - sauvegarde avant ecriture ;
  - refus si _elementor_data n'est pas vide ;
  - refus si un « & » nu entre dans un <script> ;
  - refus si le contenu depasse le plafond de rendu ;
  - un seul H1, points d'insertion uniques.

Usage :  python3 maj_semaine_19_octobre.py            (blanc)
         python3 maj_semaine_19_octobre.py --ecrire
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

PLAFOND = 275_000
SAUVE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avant-sem42")

LARGE = set("mwMW—…")
MOYEN = set("ABCDEFGHJKLNOPQRSTUVXYZabcdeghknopqsuvxyz0123456789")


def px(t):
    return round(sum(11.0 if c in LARGE else (8.0 if c in MOYEN else 5.5)
                     for c in t))


# --------------------------------------------------------------------------
# Lecture equilibree
# --------------------------------------------------------------------------

def bornes_section(c, classe):
    m = re.search(r'<section[^>]*class="[^"]*' + re.escape(classe)
                  + r'[^"]*"[^>]*>', c)
    if not m:
        return None
    i, p = m.start(), 0
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
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", h)
    t = re.sub(r"(?is)</(p|li|h[1-6]|div)>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip()


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
# Signature
# --------------------------------------------------------------------------
BYLINE_CSS = """<style id="hh-byline-css">
.eeat-byline{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.75rem;margin:1.5rem auto;padding:1.25rem 1.25rem 1.1rem;max-width:30rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
#hh-page .eeat-byline{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.75rem;margin:1.5rem auto;padding:1.25rem 1.25rem 1.1rem;max-width:30rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
.eeat-byline img,#hh-page .eeat-byline img{width:72px;height:72px;border-radius:50%;border:2px solid #16DB7F;object-fit:cover;display:block;margin:0 auto;flex:0 0 auto}
.eeat-byline-author,#hh-page .eeat-byline-author{color:#fff;font-size:.9375rem;line-height:1.5}
.eeat-byline-author strong,#hh-page .eeat-byline-author strong{color:#16DB7F;display:block;font-size:1.0625rem;margin-bottom:.15rem}
.eeat-byline-meta,#hh-page .eeat-byline-meta{color:rgba(255,255,255,.85);font-size:.8125rem;display:flex;flex-wrap:wrap;gap:.35rem .9rem;margin-top:.55rem;justify-content:center}
.eeat-byline-meta span,#hh-page .eeat-byline-meta span{display:inline-flex;align-items:center;gap:.35rem}
</style>
"""

BYLINE = """<div class="eeat-byline">
<img loading="lazy" decoding="async" width="72" height="72" src="https://www.helloharel.com/wp-content/uploads/2026/10/timothy-jollivet-fondateur-hello-harel.webp" alt="Timothy Jollivet, fondateur de Hello Harel">
<div class="eeat-byline-author"><strong>Timothy Jollivet</strong>Fondateur de Hello Harel, éditeur d'ERP agroalimentaire
<div class="eeat-byline-meta"><span>Publié le 1er avril 2026</span><span>Mis à jour le 15 octobre 2026</span><span>{LECTURE} min de lecture</span></div>
</div></div>"""


# --------------------------------------------------------------------------
# Feuille des sections MOFU et BOFU — chaque regle doublee en #hh-page
# --------------------------------------------------------------------------
FUNNEL_CSS = """<style id="hh-funnel-css">
.hhf-wrap,#hh-page .hhf-wrap{background:#0b1b2b;padding:3.5rem 0}
.hhf-wrap .container,#hh-page .hhf-wrap .container{max-width:1180px;margin:0 auto;padding:0 1rem}
.hhf-h,#hh-page .hhf-h{margin:0 0 1.75rem;text-align:center}
.hhf-h p.hhf-over,#hh-page .hhf-h p.hhf-over{color:#16DB7F;text-transform:uppercase;letter-spacing:.08em;font-size:.8125rem;font-weight:700;margin:0 0 .5rem}
.hhf-h h2,#hh-page .hhf-h h2{color:#fff;font-size:1.75rem;line-height:1.3;margin:0 0 .6rem}
.hhf-h p.hhf-sub,#hh-page .hhf-h p.hhf-sub{color:rgba(255,255,255,.8);font-size:1rem;margin:0 auto;max-width:46rem;line-height:1.6}
.hhf-grid,#hh-page .hhf-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(20rem,1fr));gap:1.25rem}
.hhf-card,#hh-page .hhf-card{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:16px;padding:1.4rem 1.4rem 1.25rem}
.hhf-card h3,#hh-page .hhf-card h3{color:#16DB7F;font-size:1.0625rem;margin:0 0 .6rem;line-height:1.35}
.hhf-card p,#hh-page .hhf-card p{color:rgba(255,255,255,.88);font-size:.9375rem;line-height:1.65;margin:0 0 .6rem}
.hhf-card p:last-child,#hh-page .hhf-card p:last-child{margin-bottom:0}
.hhf-card a,#hh-page .hhf-card a{color:#8fd8ff;text-decoration:underline;text-underline-offset:3px}
.hhf-bofu,#hh-page .hhf-bofu{background:#0e2438}
.hhf-steps,#hh-page .hhf-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1.25rem;margin:0 0 1.5rem}
.hhf-step,#hh-page .hhf-step{background:#fff;border-radius:16px;padding:1.4rem;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.hhf-step b,#hh-page .hhf-step b{display:block;color:#16DB7F;font-size:.78125rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 .5rem}
.hhf-step h3,#hh-page .hhf-step h3{margin:0 0 .5rem;font-size:1.0625rem;color:#0b1b2b}
.hhf-step p,#hh-page .hhf-step p{margin:0;color:#334155;font-size:.9375rem;line-height:1.6}
.hhf-step a,#hh-page .hhf-step a{color:#0369A1;text-decoration:underline;text-underline-offset:3px}
.hhf-note,#hh-page .hhf-note{color:rgba(255,255,255,.72);font-size:.84375rem;line-height:1.6;margin:1.25rem 0 0;text-align:center}
.hhf-note a,#hh-page .hhf-note a{color:#8fd8ff;text-decoration:underline}
</style>
"""


def bloc_mofu(over, titre, sous, cartes):
    c = "".join(
        '<div class="hhf-card"><h3>%s</h3>%s</div>'
        % (t, "".join("<p>%s</p>" % p for p in ps)) for t, ps in cartes)
    return ('<section class="hhf-wrap"><div class="container">'
            '<div class="hhf-h"><p class="hhf-over">%s</p><h2>%s</h2>'
            '<p class="hhf-sub">%s</p></div>'
            '<div class="hhf-grid">%s</div></div></section>'
            % (over, titre, sous, c))


def bloc_bofu(titre, sous, etapes, note):
    e = "".join(
        '<div class="hhf-step"><b>%s</b><h3>%s</h3><p>%s</p></div>'
        % (b, t, p) for b, t, p in etapes)
    return ('<section class="hhf-wrap hhf-bofu"><div class="container">'
            '<div class="hhf-h"><p class="hhf-over">Passer à l\'étape suivante</p>'
            '<h2>%s</h2><p class="hhf-sub">%s</p></div>'
            '<div class="hhf-steps">%s</div>'
            '<p class="hhf-note">%s</p></div></section>'
            % (titre, sous, e, note))


# --------------------------------------------------------------------------
# Les trois pages
# --------------------------------------------------------------------------
PAGES = {}

PAGES["logistique"] = dict(
    pid=4791, lecture=7, refondre=True,
    badge="Logiciel de logistique agroalimentaire",
    h1=("Le logiciel de logistique agroalimentaire qui ",
        "sait ce qu'il y a dans chaque palette"),
    accroche="Un logiciel de logistique agroalimentaire pilote la réception, "
             "le stockage par emplacement, la préparation et l'expédition sans "
             "perdre le lot de vue. Chaque palette garde son numéro de lot et sa "
             "DLC, de la porte du quai au bon de livraison du client.",
    title="Logiciel de logistique agroalimentaire • Quais, lots et tournées",
    desc="Logiciel de logistique agroalimentaire : réception, emplacements, "
         "préparation au lot, expédition et suivi transporteur. Démo gratuite.",
    mofu=("Cartographie de la demande",
          "Votre logistique, selon ce que vous cherchez vraiment",
          "Les cinq entrées ci-dessous sont les sous-intentions réellement "
          "mesurées sur cette page dans la Search Console entre le 17 juillet "
          "et le 12 octobre 2026. Chacune appelle une réponse différente.",
          [("Un WMS, ou l'ERP suffit&nbsp;?",
            ["Un WMS gère l'entrepôt&nbsp;: emplacements, vagues de picking, "
             "réapprovisionnement de zone. Un ERP agroalimentaire gère le lot et "
             "la DLC. Tant que vos volumes tiennent sur un entrepôt et que la "
             "contrainte dominante est la date limite, l'ERP évite une deuxième "
             "base de données et une passerelle à maintenir.",
             "Au-delà, le module logistique se branche sur un WMS existant plutôt "
             "que de le remplacer."]),
           ("La réception des marchandises",
            ["C'est là que tout se joue&nbsp;: si le lot fournisseur et la DLC "
             "n'entrent pas à la réception, ils n'existeront nulle part ensuite. "
             "Pesée à l'entrée, écart entre commandé et reçu, contrôle à "
             "réception, blocage qualité.",
             "Le stock se valorise sur le poids réellement reçu, pas sur le poids "
             "commandé."]),
           ("Le suivi des livraisons et des transporteurs",
            ["Statut d'expédition, preuve de livraison, écart de température le "
             "cas échéant, et retour de l'information dans la fiche client. "
             "Quand le transport est sous-traité, c'est l'échange de fichiers "
             "avec le transporteur qui porte le suivi."]),
           ("Travailler avec un prestataire logistique",
            ["C'est la sous-intention la plus demandée sur cette page. Un "
             "prestataire connecté reçoit les ordres de préparation et renvoie "
             "les confirmations&nbsp;: vous gardez la maîtrise du stock "
             "théorique, il gère le physique. L'enjeu est le format d'échange et "
             "la fréquence de synchronisation, pas l'outil."]),
           ("Produits frais et restauration collective",
            ["Rotation FEFO imposée au picking, commandes à J-1, points de "
             "livraison multiples, et un cadencier par client. Les contraintes de "
             "la restauration collective ne sont pas celles d'un entrepôt sec."])]),
    bofu=("Ce qu'il faut regarder avant de choisir",
          "Trois choses décident, et aucune n'est la liste de fonctionnalités.",
          [("Ce qu'on vous montre",
            "Une démo sur vos propres flux",
            "On part d'une de vos réceptions et on la suit jusqu'au bon de "
            "livraison. Pas de jeu de données de démonstration&nbsp;: vos "
            "références, vos lots, vos clients."),
           ("Ce qui fait varier le prix",
            "Le nombre de postes, pas le nombre de modules",
            "Le détail est sur la page <a href=\"/tarifs/\">tarifs</a>. Ce qui "
            "pèse, c'est le nombre d'utilisateurs simultanés et la reprise de "
            "l'existant, rarement la liste des fonctions."),
           ("Par où on commence",
            "Le métier avant le module",
            "Si vous êtes grossiste ou distributeur, commencez par "
            "<a href=\"/negoce/\">l'ERP pour le négoce</a>. Si vous "
            "transformez, par <a href=\"/agroalimentaire/\">l'ERP "
            "agroalimentaire</a>. Le module logistique s'y rattache.")],
          "Une question précise plutôt qu'une démo&nbsp;? "
          "<a href=\"/contact/\">Écrivez-nous</a>, on répond sans rendez-vous."),
)

PAGES["planification-production-erp"] = dict(
    pid=7910, lecture=8, refondre=False,
    title="Logiciel de planification de production • Ordonnancement d'atelier",
    desc="Logiciel de planification de production et d'ordonnancement d'atelier : "
         "calcul des besoins nets, charge par poste, suivi temps réel.",
    mofu=("Cartographie de la demande",
          "Planification ou ordonnancement&nbsp;? Ce que vous cherchez n'est pas toujours ce que vous nommez",
          "Sur cette page, la Search Console enregistre trois fois plus "
          "d'impressions sur des formulations en « ordonnancement » que sur "
          "« planification », entre le 17 juillet et le 12 octobre 2026. Les "
          "deux mots ne désignent pourtant pas le même travail.",
          [("La différence, en une phrase",
            ["La planification décide <em>quoi</em> produire et <em>en quelle "
             "quantité</em>, sur des semaines. L'ordonnancement décide <em>dans "
             "quel ordre</em> et <em>sur quelle ligne</em>, sur des heures. Un "
             "outil qui ne fait que le premier vous laisse l'atelier à gérer au "
             "tableau blanc."]),
           ("L'ordonnancement d'atelier",
            ["Séquencer les ordres de fabrication sur chaque ligne en tenant "
             "compte des changements de série, des nettoyages entre allergènes "
             "et des capacités réelles. En agroalimentaire, le temps de "
             "nettoyage est une contrainte de séquence, pas une perte."]),
           ("Le calcul des besoins nets",
            ["À partir des commandes fermes et des prévisions, le CBN remonte "
             "les nomenclatures et sort ce qu'il faut acheter et produire, "
             "quand. C'est lui qui évite d'acheter trop tôt un ingrédient "
             "périssable."]),
           ("Le suivi en temps réel",
            ["Savoir où en est un ordre pendant qu'il tourne&nbsp;: quantité "
             "déclarée, écart au théorique, aléa signalé. Sans retour d'atelier, "
             "un planning est un vœu."]),
           ("La fabrication alimentaire, et la cuisine centrale",
            ["Planifier une production alimentaire, c'est planifier des dates "
             "limites. Un ordre lancé trop tôt consomme de la durée de vie. "
             "Cuisines centrales et ateliers traiteur partagent cette contrainte "
             "avec l'industrie, à une autre échelle."])]),
    bofu=("Un devis d'ordonnancement, concrètement",
          "C'est la demande la plus fréquente sur cette page. Voici ce qui la "
          "détermine, avant même qu'on se parle.",
          [("Ce qui est chiffré",
            "Le nombre de lignes et de postes",
            "Un atelier à trois lignes et un site à quinze ne se paramètrent pas "
            "pareil. Le reste — nomenclatures, gammes, calendriers — se reprend "
            "de l'existant. La grille est sur la page "
            "<a href=\"/tarifs/\">tarifs</a>."),
           ("Ce qu'on vous montre",
            "Votre semaine la plus chargée",
            "On prend une semaine réelle, avec ses aléas, et on la rejoue dans "
            "l'outil. C'est le seul test qui dit quelque chose."),
           ("L'étape d'avant",
            "La fabrication, puis l'ordonnancement",
            "Si les nomenclatures et les rendements ne sont pas encore tenus, "
            "commencez par <a href=\"/fonctionnalites/fabrication/\">le logiciel "
            "de fabrication agroalimentaire</a>&nbsp;: l'ordonnancement s'appuie "
            "dessus.")],
          "Pour un chiffrage, <a href=\"/contact/\">décrivez-nous votre atelier</a> "
          "— nombre de lignes, de références et d'équipes suffit pour commencer."),
)

PAGES["vente"] = dict(
    pid=4767, lecture=7, refondre=True,
    badge="Logiciel de vente agroalimentaire",
    h1=("Le logiciel de vente agroalimentaire qui ",
        "facture le poids réellement expédié"),
    accroche="Un logiciel de vente agroalimentaire tient le cadencier du client, "
             "ses tarifs négociés et ses contrats, puis facture le poids pesé à "
             "l'expédition. Le commercial voit le stock disponible au lot près "
             "pendant qu'il prend la commande.",
    title="Logiciel de vente agroalimentaire • Cadencier, tarifs, poids réel",
    desc="Logiciel de vente agroalimentaire : cadencier de télévente, tarifs "
         "négociés par client, facturation au poids expédié. Démo gratuite.",
    mofu=("Cartographie de la demande",
          "Ce que « vente » recouvre, selon votre activité",
          "Les entrées ci-dessous correspondent aux requêtes réellement "
          "enregistrées sur cette page entre le 17 juillet et le 12 octobre "
          "2026. Elles ne parlent pas toutes du même métier.",
          [("Le négoce de fruits et légumes",
            ["Prix qui bougent dans la journée, marchandise périssable, achat et "
             "vente dans le même geste. La vente se pilote à la marge sur le lot, "
             "pas sur une fiche article figée. Le détail est sur "
             "<a href=\"/negoce/\">l'ERP pour le négoce alimentaire</a>."]),
           ("Le CRM, ou la gestion commerciale&nbsp;?",
            ["Un CRM suit la relation. Une gestion commerciale sort les pièces. "
             "En agroalimentaire les deux se touchent&nbsp;: pendant l'appel, le "
             "commercial a besoin du cadencier, des impayés et du stock "
             "disponible. Voir <a href=\"/fonctionnalites/crm/\">le CRM "
             "agroalimentaire</a>."]),
           ("La télévente et le cadencier",
            ["Reprendre la commande précédente, proposer les manquants, repérer "
             "les ruptures avant d'appeler. Un cadencier bien tenu fait plus pour "
             "le panier moyen qu'un argumentaire."]),
           ("Du devis à la préparation",
            ["Le devis devient commande, la commande devient bon de préparation, "
             "puis bon de livraison au poids pesé. Le chemin complet est décrit "
             "sur <a href=\"/fonctionnalites/logiciel-devis-commande-bon-livraison/\">"
             "logiciel devis, commande et bon de livraison</a>."]),
           ("Vous cherchiez votre espace client&nbsp;?",
            ["Cette page est une présentation du module de vente, pas l'accès à "
             "votre compte. Pour vous connecter à votre ERP, utilisez le lien "
             "transmis par votre intégrateur ou "
             "<a href=\"/contact/\">demandez-le-nous</a>."])]),
    bofu=("Par où commencer, selon votre métier",
          "La page qui vous servira ensuite n'est pas la même selon ce que vous "
          "vendez.",
          [("Si vous achetez pour revendre",
            "L'ERP pour le négoce",
            "Marge au lot, prix d'achat qui bouge, poids variable&nbsp;: "
            "<a href=\"/negoce/\">la page négoce</a> est faite pour ça, et c'est "
            "celle qui génère le plus de demandes après l'accueil."),
           ("Si vous transformez",
            "L'ERP agroalimentaire",
            "Quand la vente est la sortie d'un atelier, commencez par "
            "<a href=\"/agroalimentaire/\">l'ERP agroalimentaire</a>&nbsp;: la "
            "vente s'y rattache, pas l'inverse."),
           ("Ce que coûte le module",
            "Au poste, pas au module",
            "La grille est sur la page <a href=\"/tarifs/\">tarifs</a>. Le "
            "nombre de commerciaux simultanés pèse davantage que le nombre de "
            "fonctions activées.")],
          "Vous voulez voir votre propre cadencier dans l'outil&nbsp;? "
          "<a href=\"/contact/\">Demandez une démo</a>, on part de vos données."),
)


# --------------------------------------------------------------------------
# Transformations
# --------------------------------------------------------------------------

def remplacer_h1(c, debut, accent):
    m = re.search(r'(?is)(<h1[^>]*class="[^"]*hero-title[^"]*"[^>]*>)(.*?)(</h1>)', c)
    if not m:
        raise RuntimeError("h1.hero-title introuvable")
    coul = re.search(r'class="accent"[^>]*style="color:([^";]+)', m.group(2))
    coul = coul.group(1) if coul else "#60a5fa"
    return (c[:m.start()] + m.group(1) + debut
            + '<span class="accent" style="color:' + coul + '">' + accent
            + "</span>" + m.group(3) + c[m.end():])


def remplacer_accroche(c, t):
    m = re.search(r'(?is)(<p class="hero-description">)(.*?)(</p>)', c)
    if not m:
        raise RuntimeError("p.hero-description introuvable")
    return c[:m.start()] + m.group(1) + t + m.group(3) + c[m.end():]


def remplacer_badge(c, badge):
    m = re.search(r'(?is)(<div class="hero-badge">\s*<span class="dot"></span>)(.*?)(</div>)', c)
    if not m:
        raise RuntimeError("div.hero-badge introuvable")
    return c[:m.start()] + m.group(1) + badge + m.group(3) + c[m.end():]


def poser_byline(c, lecture):
    if "eeat-byline" in c:
        return c
    m = re.search(r'(?is)<p class="hero-cta-sub">.*?</p>', c)
    if not m:
        raise RuntimeError("p.hero-cta-sub introuvable")
    c = c[:m.end()] + BYLINE.replace("{LECTURE}", str(lecture)) + c[m.end():]
    s = re.search(r'<section[^>]*class="[^"]*hero-section', c)
    return c[:s.start()] + BYLINE_CSS + c[s.start():]


def poser_funnel(c, mofu, bofu):
    """MOFU et BOFU entre les fonctionnalites et la carte « a propos »."""
    cle = '<section class="about-card-section"'
    if c.count(cle) != 1:
        raise RuntimeError("point d'insertion ambigu : %d about-card-section"
                           % c.count(cle))
    i = c.index(cle)
    bloc = bloc_mofu(*mofu) + bloc_bofu(*bofu)
    if "hh-funnel-css" not in c:
        s = re.search(r'<section[^>]*class="[^"]*hero-section', c)
        c = c[:s.start()] + FUNNEL_CSS + c[s.start():]
        i = c.index(cle)
    return c[:i] + bloc + c[i:]


def faq_jsonld(c):
    b = bornes_section(c, "faq-section")
    if not b:
        raise RuntimeError("faq-section introuvable")
    qs = details(c[b[0]:b[1]])
    if len(qs) < 3:
        raise RuntimeError("moins de 3 questions dans la FAQ")
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer",
                                               "text": resume(r)}}
                           for q, r in qs]}
    return ('\n<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False) + "</script>\n")


def lire(pid):
    d = n.call("wp/v2/pages/%d?context=edit&_fields=id,slug,link,content,meta" % pid)
    if d["meta"].get("_elementor_data") not in ("", "[]", None):
        raise RuntimeError("%d : _elementor_data non vide" % pid)
    return d


def rankmath(pid, title, desc):
    n.call("rankmath/v1/updateMeta", "POST",
           {"objectID": pid, "objectType": "post",
            "meta": {"rank_math_title": title, "rank_math_description": desc}})


def main(poser=False):
    os.makedirs(SAUVE, exist_ok=True)
    print("mode :", "ECRITURE REELLE" if poser else "blanc (aucune écriture)", "\n")
    rapport = []
    for slug, p in PAGES.items():
        d = lire(p["pid"])
        c = d["content"]["raw"]
        open(os.path.join(SAUVE, "%d.html" % p["pid"]), "w").write(c)
        avant = len(c)
        notes = []
        if p["refondre"]:
            c = remplacer_badge(c, p["badge"])
            c = remplacer_h1(c, p["h1"][0], p["h1"][1])
            c = remplacer_accroche(c, p["accroche"])
            c = poser_byline(c, p["lecture"])
            notes.append("hero refondu + signature")
        c = poser_funnel(c, p["mofu"], p["bofu"])
        notes.append("MOFU + BOFU")
        if "FAQPage" not in c:
            c = c + faq_jsonld(c)
            notes.append("FAQPage posé")
        assert len(c) < max(PLAFOND, avant), "%s : %d o au-dessus du plafond" % (slug, len(c))
        assert sans_amp_nu_dans_scripts(c), "%s : un & nu dans un <script>" % slug
        assert c.count("<h1") == 1, "%s : %d H1" % (slug, c.count("<h1"))
        assert c.count("hhf-wrap") >= 2, "%s : les 2 sections ne sont pas posées" % slug
        if poser:
            n.call("wp/v2/pages/%d" % p["pid"], "POST", {"content": c})
            rankmath(p["pid"], p["title"], p["desc"])
        rapport.append((slug, avant, len(c), px(p["title"]), px(p["desc"]),
                        " · ".join(notes)))

    print("%-30s %9s %9s %8s %8s  %s"
          % ("page", "avant", "après", "title", "desc", "ce qui est posé"))
    for s, a, b, t, de, nt in rapport:
        al = "" if (200 <= t <= 561 and 400 <= de <= 985) else "  <-- HORS BORNES"
        print("%-30s %9d %9d %6d px %6d px  %s%s" % (s, a, b, t, de, nt, al))


if __name__ == "__main__":
    main(poser="--ecrire" in sys.argv)
