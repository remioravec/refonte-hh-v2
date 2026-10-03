#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rend visibles les questions que le blog cachait dans son JavaScript.

Cent une des cent trois pages du blog portent un tableau « faqData ».
Il contient trois natures de choses, melangees :

  * de vraies questions, avec de vraies reponses, ecrites a la main —
    cinquante-quatre articles en ont, deux cent cinquante au total. Elles
    n'etaient injectees dans la page qu'au clic : aucun moteur ne les a
    jamais lues.
  * un bloc de sources officielles, sur huit articles — des liens vers
    EUR-Lex, la DGCCRF, l'ANSES. Egalement invisible.
  * deux cartes de rendez-vous, presentees comme des questions, y compris
    dans le balisage FAQPage envoye a Google. Celles-la n'ont rien a faire
    dans une FAQ : elles deviennent l'appel a l'action.

Ce module ne redige rien. Il deplace : du JavaScript vers le HTML.
"""

import json
import re

VIDES = {"br", "hr", "img", "input", "meta", "link", "source", "col"}
CTA = re.compile(r'href="(?:/demo/|/contact/)')
SOURCES = re.compile(r"sources?\b|pour aller plus loin", re.I)


def assainir(h):
    """Un fragment ecrit a la main ferme parfois des balises qu'il n'a pas
    ouvertes. On retire ces orphelines et on ferme ce qui reste ouvert."""
    pile, sortie, pos = [], [], 0
    for m in re.finditer(r"<(/?)([a-zA-Z0-9]+)([^>]*?)(/?)>", h):
        fermant, nom, auto = m.group(1), m.group(2).lower(), m.group(4)
        sortie.append(h[pos:m.start()])
        pos = m.end()
        if nom in VIDES or auto:
            sortie.append(m.group(0))
            continue
        if not fermant:
            pile.append(nom)
            sortie.append(m.group(0))
        elif nom in pile:
            while pile and pile.pop() != nom:
                sortie.append("</x>")          # jamais atteint en pratique
            sortie.append(m.group(0))
        # une fermante sans ouvrante est simplement abandonnee
    sortie.append(h[pos:])
    for nom in reversed(pile):
        sortie.append("</%s>" % nom)
    return re.sub(r"\s+", " ", "".join(sortie)).strip()



def en_paragraphes(h):
    """Cent quarante-huit reponses sont du texte nu : sans balise de bloc,
    la respiration entre les phrases n'existe pas. On les remet en
    paragraphes, en coupant la ou l'auteur avait mis un saut de ligne."""
    if re.search(r"<(p|ul|ol|table|div)\b", h, re.I):
        return h
    morceaux = [x.strip() for x in re.split(r"<br\s*/?>", h, flags=re.I)]
    morceaux = [x for x in morceaux if re.sub(r"<[^>]+>", "", x).strip()]
    return "".join("<p>%s</p>" % x for x in morceaux) or h


def _titre(t):
    """« 3. Sage X3 est puissant ? » devient « Sage X3 est puissant ? »."""
    return re.sub(r"^\s*\d+[.)]\s*", "", t).strip()


def extraire(contenu):
    """(questions, sources, liens de rendez-vous) — ou ([], [], None)."""
    m = re.search(r"var faqData\s*=\s*(\[.*?\]);", contenu, re.S)
    if not m:
        return [], [], None
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return [], [], None
    questions, sources, liens = [], [], []
    for e in data:
        titre, html = e.get("title", ""), e.get("html", "")
        if CTA.search(html):
            liens += [x for x in re.findall(r'href="([^"]+)"', html)
                      if x.startswith(("/demo/", "/contact/"))]
        elif SOURCES.search(titre):
            sources.append((_titre(titre), assainir(html)))
        elif titre:
            questions.append((_titre(titre), en_paragraphes(assainir(html))))
    return questions, sources, (liens[:2] if len(liens) >= 2 else None)


CSS_SRC = """<style id="hh-blog-sources">
.hhb-src,#hh-page .hhb-src{max-width:860px;margin:2rem auto 0 !important;
 padding:1.4rem 1.6rem !important;background:#F8FAFC !important;
 border:1px solid #E2E8F0 !important;border-left:4px solid #0369A1 !important;
 border-radius:14px !important}
.hhb-src>b,#hh-page .hhb-src>b{display:block !important;color:#0f172a !important;
 font-size:1.02rem !important;font-weight:800 !important;margin-bottom:.7rem !important}
.hhb-src ul,#hh-page .hhb-src ul{margin:0 !important;padding:0 !important;
 list-style:none !important}
.hhb-src li,#hh-page .hhb-src li{margin:0 0 .6rem !important;padding-left:1.1rem !important;
 position:relative !important;line-height:1.6 !important;font-size:.95rem !important}
.hhb-src li:before,#hh-page .hhb-src li:before{content:'';position:absolute;left:0;
 top:.62em;width:5px;height:5px;border-radius:50%;background:#0369A1}
.hhb-src a,#hh-page .hhb-src a{color:#0369A1 !important;text-decoration:none !important;
 font-weight:600 !important}
.hhb-src a:hover,#hh-page .hhb-src a:hover{text-decoration:underline !important}
.hhb-src .src-domain,#hh-page .hhb-src .src-domain{display:block !important;
 color:#64748b !important;font-weight:400 !important;font-size:.85rem !important}
@media(max-width:640px){.hhb-src,#hh-page .hhb-src{margin:1.6rem 16px 0 !important;
 padding:1.15rem 1.2rem !important}}
</style>"""


def bloc_sources(sources):
    """Le bloc de references, rendu lisible et crawlable."""
    if not sources:
        return ""
    corps = "".join('<div class="hhb-src"><b>%s</b>%s</div>' % (t, h)
                    for t, h in sources)
    return CSS_SRC + corps


ENTETE = ('<div class="section-header"><p class="overline">FAQ</p>'
          '<h2 id="faq">Les réponses à vos questions</h2>'
          '<p>%s</p></div>')

CHAPEAUX = [
    (r"co[uû]t|prix|marge|revient|tarif", "Calcul, marge et prix de revient."),
    (r"stock|inventaire|entrep[oô]t|r[ée]approvision", "Stock, inventaire et réapprovisionnement."),
    (r"tra[cç]abilit|lot|dlc|ddm|dluo|rappel", "Traçabilité, lots et dates limites."),
    (r"erp|logiciel|migration|saas|cloud|as/?400", "Choix, coût et mise en place d'un ERP."),
    (r"haccp|conformit|r[ée]glement|norme|qualit", "Conformité, contrôles et réglementation."),
    (r"facture|facturation|devis|commande|livraison", "Documents de vente et facturation."),
    (r"edi|gms|p[ée]nalit|grande surface", "Échanges avec la grande distribution."),
]


def chapeau(titre_article):
    for motif, texte in CHAPEAUX:
        if re.search(motif, titre_article, re.I):
            return texte
    return "Ce que les lecteurs de cet article demandent le plus souvent."
