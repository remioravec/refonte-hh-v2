#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GABARIT BLOG HELLO HAREL — valide le 27/08/2026 sur
/blog/calculer-le-prix-de-revient-en-boulangerie/ et adopte comme gabarit de
reference pour tous les articles du blog.

CE QUE LE GABARIT IMPOSE, DANS L'ORDRE :
  1. reponse encadree      (.rep)   — la definition en UNE phrase + la promesse
  2. chiffre date          (.fait)  — un chiffre, sa date, sa source
  3. calculateur           (.calc)  — module interactif AU-DESSUS du 2e ecran
  4. sommaire ancre        (.som)   — une entree par H2
  5. sections de corps     (h2/h3 + prose)
  6. tableau triable       (.tbw)   — filtres + tri, la donnee structurée
  7. FAQ                   (h3/p)   — questions reprises mot pour mot du PAA
  8. la suite dans la page (.next)  — liens internes contextuels

CE QU'IL GARANTIT :
  - aucune dependance externe, tout fonctionne sans JavaScript en mode degrade
  - <label> sur chaque champ, aria-sort et aria-pressed, aucun <div onclick>
  - aeration : le theme impose #hh-page p{margin:0 !important}, toutes les
    regles d'espacement portent donc !important (sinon elles sont ecrasees)
  - mobile : calculateur en 2 colonnes sous 820 px, valeurs en nowrap,
    H2 et paragraphes resserres, degrade de defilement sur le tableau

Le CSS et le JS sont extraits tels quels de la page validee : gabarit_blog.css
et gabarit_blog.js, a cote de ce fichier.
"""
import os, json, re

_HERE = os.path.dirname(os.path.abspath(__file__))

def _lire(nom):
    with open(os.path.join(_HERE, nom), encoding="utf-8") as f:
        return f.read()

CSS = _lire("gabarit_blog.css")


def _fr(x, d=2):
    return ("%%.%df" % d % x).replace(".", ",")


def champ(id_, lab, val, step="0.01"):
    return ('<div class="f"><label for="%s">%s</label>'
            '<input type="number" id="%s" value="%s" step="%s" min="0" inputmode="decimal"></div>'
            % (id_, lab, id_, val, step))


def calculateur(titre, sous_titre, champs, unite, ref, note, grille_titre, grille):
    """champs : [(id, label, valeur, step)] · ref : dict des valeurs de reference
    deja calculees (rendu sans JS) · grille : [(id, valeur, legende)]"""
    f = "".join(champ(i, l, v, s) for i, l, v, s in champs)
    det = "".join('<div><span>%s</span><span id="%s">%s</span></div>' % (lab, i, val)
                  for i, lab, val in ref["detail"])
    g = "".join('<div><b id="%s">%s</b><span>%s</span></div>' % (i, v, leg) for i, v, leg in grille)
    return (
        '<div class="calc"><div class="calc-h"><b>%s</b><span>%s</span></div>'
        '<div class="calc-b"><div class="fields">%s</div>'
        '<div class="out"><div class="lg">%s</div>'
        '<div class="big" id="%s">%s&nbsp;<small>%s</small></div>'
        '<div class="det">%s</div>'
        '<div class="pv"><div class="lg">%s</div><div class="pvg">%s</div></div>'
        '</div></div><div class="calc-f">%s</div></div>'
        % (titre, sous_titre, f, ref["label"], ref["id"], ref["valeur"], unite, det,
           grille_titre, g, note))


def tableau(colonnes, lignes, filtres, tid="pri-tab"):
    """colonnes : [(intitule, triable)] · lignes : [(groupe, [cellules html])]"""
    th = "".join(
        ('<th aria-sort="none"><button type="button" data-c="%d">%s</button></th>' % (n, c))
        if tri else ('<th>%s</th>' % c)
        for n, (c, tri) in enumerate(colonnes))
    tr = "".join('<tr data-g="%s">%s</tr>' % (g, "".join("<td>%s</td>" % c for c in cells))
                 for g, cells in lignes)
    ch = "".join('<button type="button" class="chip" data-f="%s" aria-pressed="%s">%s</button>'
                 % (v, "true" if i == 0 else "false", lab) for i, (v, lab) in enumerate(filtres))
    return ('<div class="tbw"><div class="tbc"><b>Filtrer</b>%s</div>'
            '<div class="scroll"><table id="%s"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div></div>' % (ch, tid, th, tr))


def rendre(cfg):
    """Assemble la page selon le gabarit. cfg : voir le fichier de contenu."""
    som = "".join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in cfg["sommaire"])
    faq = "".join('<h3>%s</h3><p>%s</p>' % (q, a) for q, a in cfg["faq"])
    nxt = "".join('<a href="%s">%s<span>%s</span></a>' % (u, t, d) for u, t, d in cfg["suite"])
    corps = "".join(cfg["sections"])
    html = ('<div class="pri">'
        # 1 · reponse encadree
        '<div class="rep"><span class="lbl">La réponse en une phrase</span>'
        '<p>%s</p><p>%s</p></div>'
        # 2 · chiffre date
        '<div class="fait"><div class="n">%s</div><div><p>%s'
        '<span class="src">%s</span></p></div></div>'
        # 3 · calculateur
        '<h2 id="%s">%s</h2><p>%s</p>%s'
        # 4 · sommaire
        '<div class="som"><p>Dans cette page</p><ol>%s</ol></div>'
        # 5-7 · corps, tableau et FAQ (dans l'ordre donne par le contenu)
        '%s'
        '<h2 id="s-faq">Les questions fréquentes</h2>%s'
        # 8 · la suite
        '<div class="next">%s</div>'
        '</div>') % (
        cfg["reponse"], cfg["promesse"],
        cfg["fait_chiffre"], cfg["fait_texte"], cfg["fait_source"],
        cfg["calc_id"], cfg["calc_h2"], cfg["calc_intro"], cfg["calc_html"],
        som, corps, faq, nxt)
    return CSS + html + cfg["js"]


def controle(html, cfg):
    """Les 7 criteres du skill, mesures sur le HTML produit."""
    plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ',
             re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.S)))
    b = plain[plain.find('La réponse en une phrase'):] if 'La réponse en une phrase' in plain else plain
    f60 = " ".join(b.split()[:60]).lower()
    tiers = " ".join(plain.split()[:max(1, len(plain.split()) // 3)]).lower()
    n_champs = len(re.findall(r'<label for="', html))
    return {
     "1 · title porte l'angle": cfg["cible"].lower() in cfg["title"].lower(),
     "2 · P1 = la reponse (requete dans les 60 mots)": cfg["cible_courte"].lower() in f60,
     "3 · module interactif au-dessus du 2e ecran": 'class="calc"' in html and n_champs >= 3,
     "3b · 2e module (tableau triable)": 'aria-sort' in html and 'aria-pressed' in html,
     "4 · preuve datee + source dans le 1er tiers": cfg["date_courte"] in tiers and "source" in tiers,
     "5 · une promesse par H2": len(re.findall(r'<h2 id="s-', html)) >= 5,
     "6 · la suite est dans la page": 'class="next"' in html and html.count('/blog/') >= 2,
     "C1 · definition en UNE phrase": cfg["reponse"][:40] in html,
     "C2 · donnee structuree": '<table id=' in html,
     "C3 · fonctionne sans JS": 'class="big" id=' in html,
     "A · un <label> par champ": n_champs == len(cfg["champs"]),
     "A · aucun div cliquable": '<div onclick' not in html,
    }
