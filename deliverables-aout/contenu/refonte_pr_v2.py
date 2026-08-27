#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REFONTE 100 % du corps de /blog/calculer-le-prix-de-revient-en-boulangerie/ (post 3430).
Cible « logiciel prix de revient ». Doctrine NavBoost du skill operationnel-contenu.

CE QUI JUSTIFIE CHAQUE MODULE (releve SERP du 27/08/2026, France) :
  Otami (abs 2) 1299 mots · INBP (abs 4) 531 mots · Celge (abs 7) 3360 mots
  => AUCUN des trois n'a de tableau, de calculateur ni de FAQ depliable.
  Catalogue : « les 5 alignent des paragraphes, aucun outil -> 5. Calculateur ».
  Requete a variable (prix) -> calculateur, sans exception.
  PAA present -> 8. FAQ, questions mot pour mot.
  AI Overview au rang absolu 1 -> 1. Reponse encadree + 2. Chiffre date, renforces.
  Page > 5 H2 -> 3. Sommaire ancre.
  Concurrents sans tableau -> 4. Tableau TRIABLE (la ou les leurs n'existent pas).

Les 6 regles de construction sont respectees : aucune dependance externe, le module
fonctionne sans JavaScript (valeurs par defaut deja calculees dans le HTML), aucun
contenu injecte au clic, <button>/<label>/aria-expanded, aucun decalage de mise en
page, donnees reelles sourcees.

DRY par defaut ; --live pour pousser.
"""
import sys, re, json, importlib.util

_s = importlib.util.spec_from_file_location("d", "refonte_pr_v2_data.py")
D = importlib.util.module_from_spec(_s); _s.loader.exec_module(D)
import wp_common as w

PID = 3430
TITLE = "Logiciel Prix de Revient • Simulateur Gratuit & Comparatif 2026"
H1 = "Le simulateur de prix de revient, et les logiciels qui l’automatisent"

# ---------- calcul de reference, fait en Python pour que le HTML servi soit deja juste ----------
d = D.DEFAUTS
_mat = d["matieres"] / (1 - d["perte"] / 100)
_mo = d["temps"] / 60 * d["taux"]
_tot = _mat + _mo + d["fixes"]
_unit = _tot / d["quantite"]
REF = {"mat": round(_mat, 2), "mo": round(_mo, 2), "tot": round(_tot, 2),
       "unit": round(_unit, 3),
       "p30": round(_unit / (1 - .30), 2), "p50": round(_unit / (1 - .50), 2),
       "p70": round(_unit / (1 - .70), 2)}

CSS = """
<style id="hh-pri">
#hh-page .pri{--acc:#0090c8;--acc-d:#00658c;--ink:#0f172a;--ink2:#475569;--ink3:#7c8794;
--line:#e2e8f0;--wash:#f7f9fb;--ok:#15803d;--no:#b45309;
font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:var(--ink2);
font-size:16.5px;line-height:1.68}
#hh-page .pri *{box-sizing:border-box}
#hh-page .pri h2{font-size:clamp(1.35rem,2.5vw,1.85rem);line-height:1.22;font-weight:800;
color:var(--ink);letter-spacing:-.012em;margin:2.6rem 0 .7rem;scroll-margin-top:100px}
#hh-page .pri h2:first-child{margin-top:0}
#hh-page .pri h3{font-size:1.06rem;font-weight:700;color:var(--ink);margin:1.7rem 0 .45rem}
#hh-page .pri p{margin:0 0 1rem}
#hh-page .pri strong{color:var(--ink);font-weight:600}
#hh-page .pri a{color:var(--acc-d);font-weight:500}

/* 1 · reponse encadree */
#hh-page .pri .rep{border:1px solid #cfe3ee;border-left:4px solid var(--acc);background:#f4fafd;
padding:22px 24px;border-radius:4px;margin:0 0 16px}
#hh-page .pri .rep .lbl{display:block;font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;
font-weight:800;color:var(--acc);margin-bottom:.6rem}
#hh-page .pri .rep p{font-size:1.08rem;line-height:1.6;color:var(--ink);margin:0}
#hh-page .pri .rep p+p{margin-top:.7rem;font-size:1rem;color:var(--ink2)}

/* 2 · chiffre date */
#hh-page .pri .fait{display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:start;
background:var(--wash);border:1px solid var(--line);border-radius:4px;padding:18px 22px;margin:0 0 30px}
#hh-page .pri .fait .n{font-size:2.1rem;font-weight:800;color:var(--acc);line-height:1;
font-variant-numeric:tabular-nums}
#hh-page .pri .fait p{margin:0;font-size:.95rem;line-height:1.6}
#hh-page .pri .fait .src{display:block;margin-top:6px;font-size:.8rem;color:var(--ink3)}

/* 5 · calculateur */
#hh-page .pri .calc{border:1px solid var(--line);border-radius:6px;overflow:hidden;margin:0 0 32px;
background:#fff;box-shadow:0 1px 3px rgba(15,23,42,.05)}
#hh-page .pri .calc-h{background:var(--ink);color:#fff;padding:18px 24px}
#hh-page .pri .calc-h b{display:block;font-size:1.12rem;font-weight:700;letter-spacing:-.01em}
#hh-page .pri .calc-h span{font-size:.86rem;color:rgba(255,255,255,.66)}
#hh-page .pri .calc-b{display:grid;grid-template-columns:1fr 1fr;gap:0}
#hh-page .pri .fields{padding:22px 24px;display:grid;grid-template-columns:1fr 1fr;gap:14px 16px;
border-right:1px solid var(--line)}
#hh-page .pri .f label{display:block;font-size:.8rem;font-weight:600;color:var(--ink2);margin-bottom:5px}
#hh-page .pri .f input{width:100%;padding:9px 11px;border:1px solid var(--line);border-radius:4px;
font-size:.98rem;font-family:inherit;color:var(--ink);background:#fff;
font-variant-numeric:tabular-nums;-moz-appearance:textfield}
#hh-page .pri .f input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#hh-page .pri .out{padding:22px 24px;background:var(--wash)}
#hh-page .pri .out .big{font-size:2.4rem;font-weight:800;color:var(--ink);line-height:1;
font-variant-numeric:tabular-nums;letter-spacing:-.02em}
#hh-page .pri .out .big small{font-size:1rem;font-weight:600;color:var(--ink3)}
#hh-page .pri .out .lg{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;
color:var(--ink3);font-weight:700;margin-bottom:8px}
#hh-page .pri .det{margin:16px 0 0;border-top:1px solid var(--line);padding-top:14px}
#hh-page .pri .det div{display:flex;justify-content:space-between;gap:12px;font-size:.9rem;padding:5px 0}
#hh-page .pri .det span:last-child{font-variant-numeric:tabular-nums;font-weight:600;color:var(--ink)}
#hh-page .pri .pv{margin-top:16px;border-top:1px solid var(--line);padding-top:14px}
#hh-page .pri .pv .lg{margin-bottom:10px}
#hh-page .pri .pvg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
#hh-page .pri .pvg div{background:#fff;border:1px solid var(--line);border-radius:4px;padding:10px;text-align:center}
#hh-page .pri .pvg b{display:block;font-size:1.12rem;color:var(--ink);font-variant-numeric:tabular-nums}
#hh-page .pri .pvg span{font-size:.74rem;color:var(--ink3)}
#hh-page .pri .calc-f{padding:12px 24px;border-top:1px solid var(--line);font-size:.82rem;color:var(--ink3)}

/* 3 · sommaire */
#hh-page .pri .som{border:1px solid var(--line);border-radius:6px;padding:20px 24px;margin:0 0 34px;background:#fff}
#hh-page .pri .som p{font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;font-weight:800;
color:var(--ink3);margin:0 0 12px}
#hh-page .pri .som ol{margin:0;padding-left:1.15rem;columns:2;column-gap:28px}
#hh-page .pri .som li{margin:0 0 .5rem;break-inside:avoid}
#hh-page .pri .som a{color:var(--ink);font-weight:500;text-decoration:none;border-bottom:1px solid transparent}
#hh-page .pri .som a:hover{border-bottom-color:var(--acc);color:var(--acc-d)}

/* 4 · tableau triable */
#hh-page .pri .tbw{border:1px solid var(--line);border-radius:6px;overflow:hidden;margin:14px 0 10px;background:#fff}
#hh-page .pri .tbc{display:flex;flex-wrap:wrap;gap:8px;padding:14px 18px;border-bottom:1px solid var(--line);
align-items:center}
#hh-page .pri .tbc b{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink3);margin-right:4px}
#hh-page .pri .chip{font:inherit;font-size:.85rem;font-weight:600;padding:6px 14px;border:1px solid var(--line);
background:#fff;color:var(--ink2);border-radius:999px;cursor:pointer}
#hh-page .pri .chip[aria-pressed="true"]{background:var(--ink);color:#fff;border-color:var(--ink)}
#hh-page .pri .scroll{overflow-x:auto}
#hh-page .pri table{width:100%;border-collapse:collapse;font-size:.93rem;min-width:660px}
#hh-page .pri thead th{background:var(--wash);text-align:left;padding:11px 16px;font-size:.74rem;
letter-spacing:.07em;text-transform:uppercase;color:var(--ink3);font-weight:700;border-bottom:1px solid var(--line);
white-space:nowrap}
#hh-page .pri thead th button{font:inherit;background:none;border:0;padding:0;color:inherit;cursor:pointer;
display:inline-flex;align-items:center;gap:5px;letter-spacing:inherit;text-transform:inherit}
#hh-page .pri thead th button:after{content:"\\2195";opacity:.4;font-size:.9em}
#hh-page .pri thead th[aria-sort="ascending"] button:after{content:"\\2191";opacity:1;color:var(--acc)}
#hh-page .pri thead th[aria-sort="descending"] button:after{content:"\\2193";opacity:1;color:var(--acc)}
#hh-page .pri tbody td{padding:12px 16px;border-bottom:1px solid var(--line);vertical-align:top}
#hh-page .pri tbody tr:last-child td{border-bottom:none}
#hh-page .pri tbody td:first-child{color:var(--ink);font-weight:600;white-space:nowrap}
#hh-page .pri .y{color:var(--ok);font-weight:700}
#hh-page .pri .n{color:var(--no);font-weight:700}
#hh-page .pri .cap{font-size:.83rem;color:var(--ink3);line-height:1.6;margin:.4rem 0 0}

/* seuil */
#hh-page .pri .seuil{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px 0 8px}
#hh-page .pri .seuil div{border:1px solid var(--line);border-top:3px solid var(--acc);border-radius:4px;padding:18px 20px;background:#fff}
#hh-page .pri .seuil b{display:block;color:var(--ink);font-size:1rem;margin-bottom:.35rem}
#hh-page .pri .seuil p{font-size:.92rem;margin:0}

/* exemple */
#hh-page .pri .ex{border:1px solid var(--line);border-radius:6px;overflow:hidden;margin:16px 0 8px;background:#fff}
#hh-page .pri .ex table{min-width:0}
#hh-page .pri .ex tbody td:last-child{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;color:var(--ink)}
#hh-page .pri .ex tr.t td{background:var(--ink);color:#fff;font-weight:700;border:none}
#hh-page .pri .ex tr.t td:last-child{color:#fff}

/* suite */
#hh-page .pri .next{border-top:1px solid var(--line);margin-top:2.4rem;padding-top:1.4rem}
#hh-page .pri .next a{display:block;padding:14px 0;border-bottom:1px solid var(--line);color:var(--ink);
text-decoration:none;font-weight:600}
#hh-page .pri .next a:hover{color:var(--acc-d)}
#hh-page .pri .next a span{display:block;font-weight:400;font-size:.9rem;color:var(--ink3);margin-top:2px}

@media(max-width:820px){
 #hh-page .pri .calc-b,#hh-page .pri .fields,#hh-page .pri .seuil{grid-template-columns:1fr}
 #hh-page .pri .fields{border-right:0;border-bottom:1px solid var(--line)}
 #hh-page .pri .som ol{columns:1}
}
@media(prefers-reduced-motion:reduce){#hh-page .pri *{transition:none!important}}
</style>
"""

def champ(id_, lab, val, step="0.01", unit=""):
    return ('<div class="f"><label for="%s">%s</label>'
            '<input type="number" id="%s" value="%s" step="%s" min="0" inputmode="decimal"></div>'
            % (id_, lab, id_, val, step))

def build_body():
    s = D.SOLUTIONS
    rows = "".join(
        '<tr data-g="%d"><td>%s</td><td>%s</td><td class="%s">%s</td><td class="%s">%s</td><td>%s</td></tr>'
        % (g, nom, typ, "y" if g else "n", "Oui" if g else "Non",
           "y" if maj else "n", "Oui" if maj else "Non", qui)
        for nom, typ, g, qui, maj in s)

    faq_items = "".join(
        '<h3>%s</h3><p>%s</p>' % (q, a) for q, a in D.FAQ)

    som = [("s-calcul", "Le calculateur"), ("s-formule", "La formule, et ce qu’on oublie"),
           ("s-comparatif", "Les solutions du marché, comparées"),
           ("s-seuil", "Simulateur, logiciel ou ERP : le seuil"),
           ("s-exemple", "Un exemple chiffré, de bout en bout"),
           ("s-erreurs", "Les quatre erreurs qui faussent tout"),
           ("s-faq", "Les questions fréquentes")]
    som_html = "".join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in som)

    html = ('<div class="pri">'

# 1 · REPONSE ENCADREE
'<div class="rep"><span class="lbl">La réponse en une phrase</span>'
'<p><strong>Un logiciel de prix de revient calcule automatiquement ce que vous coûte une '
'recette ou un produit fini</strong> — matières, freinte, main-d’œuvre, énergie et frais fixes '
'compris — puis met ce coût à jour dès qu’un prix d’achat bouge, ce qu’un tableur ne fait pas.</p>'
'<p>Testez le calcul tout de suite ci-dessous, gratuitement et sans inscription, puis comparez '
'les solutions du marché.</p></div>'

# 2 · CHIFFRE DATE
'<div class="fait"><div class="n">6/10</div><div>'
'<p>Sur les dix premiers résultats Google pour « logiciel prix de revient », <strong>six sont des '
'logiciels payants</strong>, deux seulement proposent une version gratuite et deux sont des '
'comparateurs. L’offre réellement gratuite se limite en pratique aux simulateurs en ligne et aux '
'modèles de tableur.'
'<span class="src">Source : relevé de la SERP française, 27 août 2026.</span></p></div></div>'

# 5 · LE CALCULATEUR
'<h2 id="s-calcul">Calculez votre prix de revient</h2>'
'<p>Renseignez votre recette : le coût de revient unitaire et le prix de vente conseillé se '
'recalculent à chaque frappe. Aucune donnée n’est envoyée ni enregistrée.</p>'
'<div class="calc"><div class="calc-h"><b>Calculateur de prix de revient</b>'
'<span>Matières, freinte, main-d’œuvre et frais fixes</span></div>'
'<div class="calc-b"><div class="fields">'
+ champ("pri-mat", "Coût des matières (€)", "%.2f" % d["matieres"])
+ champ("pri-qte", "Quantité produite", d["quantite"], "1")
+ champ("pri-perte", "Freinte / pertes (%%)", d["perte"], "0.5")
+ champ("pri-tps", "Temps de production (min)", d["temps"], "1")
+ champ("pri-taux", "Coût horaire chargé (€/h)", "%.2f" % d["taux"])
+ champ("pri-fixes", "Frais fixes imputés (€)", "%.2f" % d["fixes"])
+ '</div><div class="out">'
'<div class="lg">Coût de revient unitaire</div>'
'<div class="big" id="pri-unit">%(unit)s&nbsp;<small>€ / pièce</small></div>'
'<div class="det">'
'<div><span>Matières, freinte comprise</span><span id="pri-o-mat">%(mat)s €</span></div>'
'<div><span>Main-d’œuvre</span><span id="pri-o-mo">%(mo)s €</span></div>'
'<div><span>Frais fixes</span><span id="pri-o-fix">%(fix)s €</span></div>'
'<div><span>Coût total de la fournée</span><span id="pri-o-tot">%(tot)s €</span></div>'
'</div>'
'<div class="pv"><div class="lg">Prix de vente conseillé</div><div class="pvg">'
'<div><b id="pri-p30">%(p30)s €</b><span>marge 30 %%</span></div>'
'<div><b id="pri-p50">%(p50)s €</b><span>marge 50 %%</span></div>'
'<div><b id="pri-p70">%(p70)s €</b><span>marge 70 %%</span></div>'
'</div></div></div></div>'
'<div class="calc-f">Les valeurs affichées sont un exemple modifiable. Sans JavaScript, '
'le calcul de référence reste lisible ci-dessus.</div></div>'

# 3 · SOMMAIRE
'<div class="som"><p>Dans cette page</p><ol>%(som)s</ol></div>'

# FORMULE
'<h2 id="s-formule">La formule, et ce que tout le monde oublie</h2>'
'<p><strong>Prix de revient = matières consommées + freinte + main-d’œuvre + énergie + '
'quote-part de frais fixes</strong>, le tout divisé par la quantité <em>réellement</em> produite.</p>'
'<p>Le poste qu’on oublie, c’est la <strong>freinte</strong>. À la cuisson, un kilo de pâte crue ne '
'donne pas un kilo de produit fini : l’eau s’évapore. Si vous divisez votre coût matière par le '
'poids engagé plutôt que par le poids sorti, votre coût au kilo est faux — toujours dans le même '
'sens, toujours à votre désavantage. C’est exactement ce que corrige le champ « freinte » du '
'calculateur ci-dessus.</p>'
'<p>Le deuxième oubli fréquent est la <strong>main-d’œuvre du dirigeant</strong>. Tout temps passé '
'à produire entre dans le coût, quel que soit le statut de la personne. Ne pas le compter donne une '
'marge qui n’existe que sur le papier.</p>'

# 4 · TABLEAU TRIABLE
'<h2 id="s-comparatif">Les solutions du marché, comparées</h2>'
'<p>Aucune des pages qui se positionnent sur cette recherche ne propose de tableau comparatif. '
'Voici les solutions relevées sur la première page de résultats, triables et filtrables.</p>'
'<div class="tbw"><div class="tbc"><b>Filtrer</b>'
'<button type="button" class="chip" data-f="all" aria-pressed="true">Toutes</button>'
'<button type="button" class="chip" data-f="1" aria-pressed="false">Gratuites</button>'
'<button type="button" class="chip" data-f="0" aria-pressed="false">Payantes</button></div>'
'<div class="scroll"><table id="pri-tab">'
'<thead><tr>'
'<th aria-sort="none"><button type="button" data-c="0">Solution</button></th>'
'<th aria-sort="none"><button type="button" data-c="1">Type</button></th>'
'<th aria-sort="none"><button type="button" data-c="2">Gratuit</button></th>'
'<th aria-sort="none"><button type="button" data-c="3">Mise à jour auto</button></th>'
'<th>Pensé pour</th>'
'</tr></thead><tbody>%(rows)s</tbody></table></div></div>'
'<p class="cap">Relevé sur la première page de résultats Google France pour « logiciel prix de '
'revient », le 27 août 2026. « Mise à jour auto » signifie que le coût se recalcule seul quand un '
'prix d’achat change, sans ressaisie.</p>'

# SEUIL
'<h2 id="s-seuil">Simulateur, logiciel dédié ou ERP : où est votre seuil</h2>'
'<p>Le partage ne se fait pas sur le prix de l’outil mais sur la <strong>fréquence de mise à '
'jour</strong>. Un tableur et un simulateur donnent une photo ; un logiciel donne un film. Si vos '
'prix d’achat bougent plusieurs fois par trimestre, la photo est périmée avant d’être imprimée.</p>'
'<div class="seuil">'
'<div><b>Moins de 30 références</b><p>Prix d’achat stables, mise à jour annuelle : le simulateur '
'ci-dessus ou un tableur suffisent. Inutile de payer pour davantage.</p></div>'
'<div><b>30 à 150 références</b><p>Fiches recettes à conserver d’une saison à l’autre : un logiciel '
'dédié au coût de revient devient rentable, surtout s’il gère les déclinaisons.</p></div>'
'<div><b>Plus de 150 références</b><p>Ou des tarifs qui bougent chaque trimestre : il faut que le '
'coût se recalcule à chaque facture fournisseur — c’est le rôle d’un ERP.</p></div>'
'</div>'
'<p>Le calcul de rentabilité tient en une multiplication : <strong>nombre de références × nombre de '
'changements de prix par an</strong>. Cinquante références et des tarifs trimestriels, cela fait '
'deux cents mises à jour par an. À cinq minutes l’une, c’est plus de seize heures de ressaisie — '
'sans compter l’écart de marge sur les fiches qu’on n’a pas eu le temps de corriger. Le détail du '
'mécanisme est dans notre guide sur le <a href="/blog/calcul-cout-de-revient-logiciel/">calcul du '
'coût de revient par un logiciel</a>.</p>'

# EXEMPLE
'<h2 id="s-exemple">Un exemple chiffré, de bout en bout</h2>'
'<p>Une fournée de 100 pièces, avec les valeurs par défaut du calculateur.</p>'
'<div class="ex"><div class="scroll"><table><tbody>'
'<tr><td>Matières premières engagées</td><td>%(matb)s €</td></tr>'
'<tr><td>Freinte de %(perte)s %% — matière réellement nécessaire</td><td>%(mat)s €</td></tr>'
'<tr><td>Main-d’œuvre : %(tps)s min à %(taux)s €/h</td><td>%(mo)s €</td></tr>'
'<tr><td>Frais fixes imputés</td><td>%(fix)s €</td></tr>'
'<tr class="t"><td>Coût total de la fournée</td><td>%(tot)s €</td></tr>'
'<tr class="t"><td>Coût de revient unitaire (100 pièces)</td><td>%(unit)s €</td></tr>'
'</tbody></table></div></div>'
'<p class="cap">Sans la freinte, le coût matière serait resté à %(matb)s € et le coût unitaire '
'sous-évalué : c’est l’écart qui sépare une marge affichée d’une marge réelle.</p>'

# ERREURS
'<h2 id="s-erreurs">Les quatre erreurs qui faussent le calcul</h2>'
'<h3>1. Diviser par la quantité engagée au lieu de la quantité sortie</h3>'
'<p>C’est la freinte, encore. Elle se mesure une fois, sur une production réelle, puis se '
'paramètre par recette.</p>'
'<h3>2. Oublier le temps de production du dirigeant</h3>'
'<p>Tout temps passé à fabriquer entre dans le coût. Le statut de la personne ne change rien à '
'l’économie de l’atelier.</p>'
'<h3>3. Travailler sur des prix d’achat périmés</h3>'
'<p>C’est le défaut structurel du tableur : il calcule juste, sur des données fausses. Une fiche '
'recette non mise à jour depuis six mois donne une marge qui n’existe plus.</p>'
'<h3>4. Confondre marge et coefficient</h3>'
'<p>Une marge de 50 %% ne s’obtient pas en multipliant par 1,5 mais en divisant par 0,5 — soit un '
'coefficient de 2. Le calculateur ci-dessus applique la division, comme le fait un logiciel.</p>'

# FAQ (le module 8 vit dans la faq-section du gabarit ; ici les reponses longues indexables)
'<h2 id="s-faq">Les questions fréquentes</h2>'
'%(faq)s'

# LA SUITE EST DANS LA PAGE
'<div class="next">'
'<a href="/blog/calcul-cout-de-revient-logiciel/">Comment un logiciel calcule le coût de revient en temps réel'
'<span>Le mécanisme, les nomenclatures et les fiches recettes — le guide complet.</span></a>'
'<a href="/blog/cout-prix-au-kilo/">Calculer un prix au kilo'
'<span>La conversion et les pièges, avec son propre calculateur.</span></a>'
'<a href="/blog/difference-prix-dachat-et-prix-de-revient/">Prix d’achat ou prix de revient&nbsp;?'
'<span>La différence, avec un exemple chiffré.</span></a>'
'</div>'

'</div>') % {
 "unit": ("%.3f" % REF["unit"]).replace(".", ","),
 "mat": ("%.2f" % REF["mat"]).replace(".", ","),
 "mo": ("%.2f" % REF["mo"]).replace(".", ","),
 "fix": ("%.2f" % d["fixes"]).replace(".", ","),
 "tot": ("%.2f" % REF["tot"]).replace(".", ","),
 "matb": ("%.2f" % d["matieres"]).replace(".", ","),
 "perte": d["perte"], "tps": d["temps"],
 "taux": ("%.2f" % d["taux"]).replace(".", ","),
 "p30": ("%.2f" % REF["p30"]).replace(".", ","),
 "p50": ("%.2f" % REF["p50"]).replace(".", ","),
 "p70": ("%.2f" % REF["p70"]).replace(".", ","),
 "som": som_html, "rows": rows, "faq": faq_items,
}
    return CSS + html + JS

JS = """
<script>
(function(){
  var ids=['pri-mat','pri-qte','pri-perte','pri-tps','pri-taux','pri-fixes'];
  var el={}; for(var i=0;i<ids.length;i++){el[ids[i]]=document.getElementById(ids[i]);}
  if(!el['pri-mat']) return;
  function f(n,d){return n.toLocaleString('fr-FR',{minimumFractionDigits:d,maximumFractionDigits:d});}
  function set(id,v){var e=document.getElementById(id); if(e) e.innerHTML=v;}
  function calc(){
    var mat=parseFloat(el['pri-mat'].value)||0,
        qte=parseFloat(el['pri-qte'].value)||1,
        per=parseFloat(el['pri-perte'].value)||0,
        tps=parseFloat(el['pri-tps'].value)||0,
        tx =parseFloat(el['pri-taux'].value)||0,
        fx =parseFloat(el['pri-fixes'].value)||0;
    if(qte<=0) qte=1; if(per>=100) per=99;
    var matN=mat/(1-per/100), mo=tps/60*tx, tot=matN+mo+fx, u=tot/qte;
    set('pri-o-mat',f(matN,2)+' €'); set('pri-o-mo',f(mo,2)+' €');
    set('pri-o-fix',f(fx,2)+' €');   set('pri-o-tot',f(tot,2)+' €');
    set('pri-unit',f(u,3)+'&nbsp;<small>€ / pièce</small>');
    set('pri-p30',f(u/0.70,2)+' €'); set('pri-p50',f(u/0.50,2)+' €'); set('pri-p70',f(u/0.30,2)+' €');
  }
  for(var k in el){ if(el[k]){ el[k].addEventListener('input',calc); } }
  calc();

  var tab=document.getElementById('pri-tab'); if(!tab) return;
  var tb=tab.querySelector('tbody');
  tab.querySelectorAll('thead th button').forEach(function(b){
    b.addEventListener('click',function(){
      var c=+b.dataset.c, th=b.parentNode;
      var asc=th.getAttribute('aria-sort')!=='ascending';
      tab.querySelectorAll('thead th').forEach(function(x){x.setAttribute('aria-sort','none');});
      th.setAttribute('aria-sort',asc?'ascending':'descending');
      var rows=[].slice.call(tb.querySelectorAll('tr'));
      rows.sort(function(x,y){
        var a=x.children[c].textContent.trim().toLowerCase(),
            d2=y.children[c].textContent.trim().toLowerCase();
        return (a<d2?-1:a>d2?1:0)*(asc?1:-1);
      });
      rows.forEach(function(r){tb.appendChild(r);});
    });
  });
  document.querySelectorAll('.pri .chip').forEach(function(c){
    c.addEventListener('click',function(){
      document.querySelectorAll('.pri .chip').forEach(function(x){x.setAttribute('aria-pressed','false');});
      c.setAttribute('aria-pressed','true');
      var v=c.dataset.f;
      tb.querySelectorAll('tr').forEach(function(r){
        r.style.display=(v==='all'||r.dataset.g===v)?'':'none';
      });
    });
  });
})();
</script>
"""


def replace_body(c, new_inner):
    """Remplace en bloc la tranche <div class="hha-card hha-main"> ... jusqu'a la
    faq-section. La tranche d'origine est equilibree (49 div ouvrants / 49 fermants),
    on la remplace par un conteneur 1/1 : la balance globale est preservee."""
    open_tag = '<div class="hha-card hha-main">'
    i = c.find(open_tag)
    j = c.find('<section class="faq-section"')
    if i < 0 or j < 0 or j <= i:
        raise SystemExit("bornes du corps introuvables")
    import re as _re
    sl = c[i:j]
    o, f = len(_re.findall(r'<div[\s>]', sl)), len(_re.findall(r'</div>', sl))
    if o != f:
        raise SystemExit("tranche desequilibree (%d/%d) — abandon" % (o, f))
    # hha-main enveloppe aussi la FAQ dans ce gabarit : on ne le referme pas ici
    neuf = open_tag + "\n" + new_inner + "\n\n"
    return c[:i] + neuf + c[j:], len(sl)


def controle(c):
    plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', c, flags=re.S)))
    b = plain[plain.find('La réponse en une phrase'):] if 'La réponse en une phrase' in plain else plain
    f60 = " ".join(b.split()[:60]).lower()
    tiers = " ".join(plain.split()[:max(1, len(plain.split()) // 3)]).lower()
    return {
     "1 · title porte l'angle": "logiciel prix de revient" in TITLE.lower(),
     "2 · P1 = la reponse (requete dans les 60 mots)": "prix de revient" in f60,
     "3 · module interactif au-dessus du 2e ecran": 'class="calc"' in c and c.count('<input') >= 6,
     "3b · 2e module (tableau triable)": 'id="pri-tab"' in c and 'aria-sort' in c,
     "4 · preuve datee + source dans le 1er tiers": "27 août 2026" in tiers and "source" in tiers,
     "5 · une promesse par H2": len(re.findall(r'<h2 id="s-', c)) >= 6,
     "6 · la suite est dans la page": 'class="next"' in c and c.count('/blog/') >= 3,
     "C1 · definition en UNE phrase": "Un logiciel de prix de revient calcule automatiquement" in c,
     "C2 · donnee structuree": 'id="pri-tab"' in c,
     "C3 · fonctionne sans JS": '<div class="big" id="pri-unit">' in c and '€ / pièce' in c,
     "A · labels sur tous les champs": c.count('<label for="pri-') == 6,
     "A · boutons, pas de div cliquable": '<div onclick' not in c,
    }


def main():
    live = "--live" in sys.argv
    c0 = w.get_raw('posts', PID)['content']['raw']
    body = build_body()
    c, removed = replace_body(c0, body)
    mots = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', c, flags=re.S)).split())
    print("corps remplace : %d car. retires, %d poses" % (removed, len(body)))
    print("page %d -> %d car. | mots %d | tableaux %d -> %d"
          % (len(c0), len(c), mots, len(re.findall(r'<table', c0)), len(re.findall(r'<table', c))))
    for tag in ('div', 'section', 'table', 'tbody', 'thead', 'tr', 'td', 'button', 'label'):
        o = len(re.findall(r'<%s[\s>]' % tag, c)); f = len(re.findall(r'</%s>' % tag, c))
        if o != f: print("  !! DESEQUILIBRE <%s> %d/%d" % (tag, o, f))
    print("\n=== controle ===")
    ok = True
    for k, v in controle(c).items():
        print("  [%s] %s" % ("OK " if v else "NON", k))
        if not v: ok = False
    print("\n  VERDICT :", "livrable" if ok else "BLOQUE")
    if not live: print("\nDRY-RUN — ajouter --live"); return
    if not ok: print("refus de pousser"); return
    w.update_content('posts', PID, c, live=True)
    print("\nPOUSSE — post %d" % PID)


if __name__ == "__main__":
    main()
