#!/usr/bin/env python3
"""
Conflict-free inter-H2 schemas + top micro-intention tools for the article
template. All markup uses the .hha-* classes already defined in template.CSS
(light theme), inline SVG only (no external libs), vanilla JS namespaced per id.

Two public helpers:
  schema_for(index, h2_text) -> small HTML figure illustrating the section
  top_tool(slug, title)      -> interactive widget matched to the micro-intention
"""

import re
import html

ARROW = ('<span class="hha-flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/>'
         '<polyline points="12 5 19 12 12 19"/></svg></span>')
IC = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
      'stroke-linejoin="round"><path d="M9 19V6l12-3v13M9 19a3 3 0 11-6 0 3 3 0 016 0zm12-3a3 3 0 11-6 0 3 3 0 016 0z"/></svg>')


def _kw(h2):
    return h2.lower()


def schema_for(index, h2_text):
    """Pick a schema type from the H2 wording; rotate styles otherwise."""
    k = _kw(h2_text)
    cap = html.escape(h2_text.strip()[:70])
    head = f'<p class="hha-fig-cap">{IC} {cap}</p>'

    def fig(inner):
        return f'<figure class="hha-fig" aria-hidden="true">{head}{inner}</figure>'

    # process / steps
    if any(w in k for w in ["étape", "etape", "process", "comment", "méthode", "methode", "déploiement", "deploiement", "migrer", "migration"]):
        steps = [("1", "Analyse"), ("2", "Paramétrage"), ("3", "Déploiement"), ("4", "Suivi")]
        cells = ARROW.join(f'<div class="hha-flow-step"><b>{n}</b><span>{l}</span></div>' for n, l in steps)
        return fig(f'<div class="hha-flow">{cells}</div>')
    # comparison / vs / alternative
    if any(w in k for w in ["vs", "comparat", "alternativ", "différence", "difference", "choisir", "meilleur"]):
        rows = [("Solution spécialisée", 88), ("ERP généraliste", 55), ("Tableur / Excel", 28)]
        bars = "".join(
            f'<div class="hha-bar-row"><span class="lab">{l}</span>'
            f'<div class="hha-bar-track"><div class="hha-bar-fill" style="width:{p}%"></div></div>'
            f'<b style="flex:0 0 38px;text-align:right">{p}%</b></div>' for l, p in rows)
        return fig(f'<div class="hha-bars">{bars}</div>')
    # KPI / chiffres / ROI / coût
    if any(w in k for w in ["roi", "kpi", "coût", "cout", "marge", "rentab", "gain", "chiffre", "résultat", "resultat", "prix"]):
        kpis = [("-35%", "temps de saisie"), ("+12%", "marge nette"), ("x3", "vitesse d'inventaire"), ("0", "ressaisie")]
        cells = "".join(f'<div class="hha-kpi"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in kpis)
        return fig(f'<div class="hha-kpis">{cells}</div>')
    # traceability / cycle / stock rotation
    if any(w in k for w in ["traçab", "tracab", "lot", "fefo", "fifo", "rotation", "stock", "inventaire", "cycle", "flux"]):
        nodes = ["Réception", "Lot + DLC", "Stockage FEFO", "Préparation", "Expédition"]
        cells = ARROW.join(f'<span class="hha-cycle-node">{n}</span>' for n in nodes)
        return fig(f'<div class="hha-cycle">{cells}</div>')
    # default: rotate between bars and kpis so every section has a visual
    if index % 2 == 0:
        rows = [("Avant Hello Harel", 40), ("Avec Hello Harel", 90)]
        bars = "".join(
            f'<div class="hha-bar-row"><span class="lab">{l}</span>'
            f'<div class="hha-bar-track"><div class="hha-bar-fill" style="width:{p}%"></div></div>'
            f'<b style="flex:0 0 38px;text-align:right">{p}%</b></div>' for l, p in rows)
        return fig(f'<div class="hha-bars">{bars}</div>')
    nodes = ["Données", "Automatisation", "Contrôle", "Décision"]
    cells = ARROW.join(f'<span class="hha-cycle-node">{n}</span>' for n in nodes)
    return fig(f'<div class="hha-cycle">{cells}</div>')


# ---- Top micro-intention tools (light theme) ----
TOOLS = {
    "roi": ["roi-erp", "erp-pme", "erp-saas", "erp-saas-cloud", "erp-cloud-saas-vs-on-premise",
            "erp-as400", "erp-agroalimentaire", "migration-erp-agroalimentaire"],
    "stock": ["calcul-stock-de-securite", "alerte-stock-securite", "reapprovisionnement-stocks",
              "gestion-des-inventaires", "optimisation-entrepot", "maitriser-la-gestion-des-stocks",
              "gestion-stock-multi-entrepots"],
    "cost": ["cout-de-revient", "calcul-du-cout-achat", "cout-prix-au-kilo", "couts-de-production",
             "cout-marginal", "calcul-du-prix-moyen", "calculer-le-prix-de-revient-en-boulangerie",
             "calcul-cout-de-revient-logiciel", "calcul-freinte-charcuterie-logiciel",
             "logiciel-calcul-cout-de-revient-traiteur", "prix-dachat-definition",
             "difference-prix-dachat-et-prix-de-revient"],
    "fefo": ["fifo-fefo-lifo", "dlc-ddm-dluo", "alerte-date-peremption", "tracabilite-lot-dlc-logiciel",
             "logiciel-tracabilite-dlc-traiteur"],
    "margin": ["erp-grossiste-distributeur", "logiciel-grossiste-alimentaire", "erp-boissons",
               "logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises", "logiciel-maree-mareyeur",
               "logiciel-televente-alimentaire", "min", "logiciel-prix-du-jour-fruits-legumes",
               "logiciel-gestion-calibre-fruits-legumes"],
    "compare": ["alternative-akanea-erp", "alternative-archipelia", "alternative-cegid", "alternative-sage-erp",
                "alternative-vif-erp", "alternatives-cegid-distribution-alimentaire", "alternatives-copilote-traiteur",
                "alternatives-divalto-agroalimentaire", "alternatives-odoo-agroalimentaire",
                "alternatives-sage-agroalimentaire", "alternatives-silog-agroalimentaire", "hello-harel-vs-divalto",
                "hello-harel-vs-odoo", "hello-harel-vs-sage", "hello-harel-vs-silog", "meilleurs-erp-import-export",
                "meilleurs-erp-boulangerie", "meilleurs-erp-maraichers-fruits-legumes",
                "meilleurs-erp-gestion-approvisionnements"],
}
SLUG_TOOL = {s: t for t, ss in TOOLS.items() for s in ss}


def tool_id(slug):
    return SLUG_TOOL.get(slug, "diagnostic")


def _wrap(uid, badge, title, intro, body, js):
    return (f'<section class="hha-tool" data-tool="{uid}">'
            f'<div class="hha-tool-h"><span class="hha-tool-badge">{badge}</span>'
            f'<h3>{title}</h3><p>{intro}</p></div>'
            f'<div class="hha-tool-b">{body}</div></section>'
            f'<script>(function(){{{js}}})();</script>')


def top_tool(slug, title=""):
    t = tool_id(slug)
    return _BUILD.get(t, _diag)(slug)


def _roi(slug):
    body = ('<div class="hha-tg">'
            '<div class="hha-fld"><label>Utilisateurs</label><input type="number" id="r_u" value="10" min="1"></div>'
            '<div class="hha-fld"><label>Heures perdues/sem.</label><input type="number" id="r_h" value="4" min="0"></div>'
            '<div class="hha-fld"><label>Coût horaire (€)</label><input type="number" id="r_c" value="28" min="0"></div>'
            '<div class="hha-fld"><label>Gain visé (%)</label><input type="number" id="r_g" value="35" min="0" max="100"></div>'
            '</div><div class="hha-out"><div class="l">Économies annuelles estimées</div>'
            '<div class="v" id="r_o">—</div><p class="n" id="r_n"></p>'
            '<a class="hha-tbtn" href="/contact/">Chiffrer mon ROI →</a></div>')
    js = ("function f(){var u=+r_u.value||0,h=+r_h.value||0,c=+r_c.value||0,g=(+r_g.value||0)/100;"
          "var s=u*h*52*c*g;document.getElementById('r_o').textContent=s.toLocaleString('fr-FR',{maximumFractionDigits:0})+' € / an';"
          "document.getElementById('r_n').textContent='Soit '+(u*h*g).toFixed(1)+' h récupérées/semaine.';}"
          "['r_u','r_h','r_c','r_g'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();")
    return _wrap("roi", "Outil interactif", "Calculez le ROI de votre ERP",
                 "Estimez les économies en supprimant ressaisies et Excel.", body, js)


def _stock(slug):
    body = ('<div class="hha-tg">'
            '<div class="hha-fld"><label>Conso. moy./jour</label><input type="number" id="s_d" value="120" min="0"></div>'
            '<div class="hha-fld"><label>Délai fournisseur (j)</label><input type="number" id="s_l" value="5" min="0"></div>'
            '<div class="hha-fld"><label>Conso. max/jour</label><input type="number" id="s_dm" value="180" min="0"></div>'
            '<div class="hha-fld"><label>Délai max (j)</label><input type="number" id="s_lm" value="8" min="0"></div>'
            '</div><div class="hha-out"><div class="l">Stock de sécurité conseillé</div>'
            '<div class="v" id="s_o">—</div><p class="n" id="s_n"></p>'
            '<a class="hha-tbtn" href="/fonctionnalites/gestion-de-stock/">Automatiser dans l\'ERP →</a></div>')
    js = ("function f(){var d=+s_d.value||0,l=+s_l.value||0,dm=+s_dm.value||0,lm=+s_lm.value||0;var ss=(dm*lm)-(d*l);if(ss<0)ss=0;"
          "document.getElementById('s_o').textContent=ss.toLocaleString('fr-FR')+' unités';"
          "document.getElementById('s_n').textContent='Point de commande : '+((d*l)+ss).toLocaleString('fr-FR')+' unités.';}"
          "['s_d','s_l','s_dm','s_lm'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();")
    return _wrap("stock", "Outil interactif", "Calculez votre stock de sécurité",
                 "Évitez ruptures et sur-stockage : stock de sécurité + point de commande.", body, js)


def _cost(slug):
    body = ('<div class="hha-tg">'
            '<div class="hha-fld"><label>Matières (€)</label><input type="number" id="c_m" value="3.20" step="0.01"></div>'
            '<div class="hha-fld"><label>Main d\'œuvre (€)</label><input type="number" id="c_l" value="1.10" step="0.01"></div>'
            '<div class="hha-fld"><label>Charges (€)</label><input type="number" id="c_o" value="0.70" step="0.01"></div>'
            '<div class="hha-fld"><label>Freinte (%)</label><input type="number" id="c_f" value="6" min="0" max="100"></div>'
            '<div class="hha-fld"><label>Marge visée (%)</label><input type="number" id="c_g" value="30" min="0" max="100"></div>'
            '</div><div class="hha-out"><div class="l">Coût de revient → Prix de vente</div>'
            '<div class="v" id="c_oo">—</div><p class="n" id="c_n"></p>'
            '<a class="hha-tbtn" href="/fonctionnalites/fabrication/">Fiabiliser mes coûts →</a></div>')
    js = ("function f(){var m=+c_m.value||0,l=+c_l.value||0,o=+c_o.value||0,fr=(+c_f.value||0)/100,g=(+c_g.value||0)/100;"
          "var cr=(m+l+o)/(1-fr);var pv=g<1?cr/(1-g):cr;"
          "document.getElementById('c_oo').textContent=cr.toFixed(2)+' € → '+pv.toFixed(2)+' €';"
          "document.getElementById('c_n').textContent='Freinte incluse ; prix pour '+(g*100).toFixed(0)+'% de marge.';}"
          "['c_m','c_l','c_o','c_f','c_g'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();")
    return _wrap("cost", "Outil interactif", "Calculez votre coût de revient réel",
                 "Intégrez freinte et charges pour protéger votre marge.", body, js)


def _fefo(slug):
    body = ('<div class="hha-fld"><label>Type de produit</label><select id="fe_t">'
            '<option value="dlc">Frais à DLC courte</option><option value="ddm">DDM (épicerie, surgelé)</option>'
            '<option value="lot">Matière première stockable</option></select></div>'
            '<div class="hha-fld" style="margin-top:8px"><label>Forte saisonnalité / promos ?</label>'
            '<select id="fe_s"><option value="non">Non</option><option value="oui">Oui</option></select></div>'
            '<div class="hha-out"><div class="l">Méthode de rotation conseillée</div>'
            '<div class="v" id="fe_o">—</div><p class="n" id="fe_n"></p>'
            '<a class="hha-tbtn" href="/fonctionnalites/gestion-de-stock/">Appliquer le FEFO →</a></div>')
    js = ("function f(){var t=fe_t.value,s=fe_s.value,m,n;"
          "if(t==='dlc'){m='FEFO';n='Premier périmé, premier sorti : impératif sur DLC courtes.';}"
          "else if(t==='ddm'){m=(s==='oui')?'FEFO':'FIFO';n='FIFO suffit hors promos ; FEFO si pics de dates.';}"
          "else{m='FIFO';n='Rotation par ancienneté ; LIFO seulement en logique comptable.';}"
          "document.getElementById('fe_o').textContent=m;document.getElementById('fe_n').textContent=n;}"
          "['fe_t','fe_s'].forEach(function(i){document.getElementById(i).addEventListener('change',f)});f();")
    return _wrap("fefo", "Outil interactif", "Quelle méthode de rotation ?",
                 "FIFO, FEFO ou LIFO : 2 questions pour trancher.", body, js)


def _margin(slug):
    body = ('<div class="hha-tg">'
            '<div class="hha-fld"><label>Prix d\'achat HT (€)</label><input type="number" id="m_a" value="1.80" step="0.01"></div>'
            '<div class="hha-fld"><label>Coefficient</label><input type="number" id="m_k" value="1.35" step="0.01" min="1"></div>'
            '<div class="hha-fld"><label>Remise (%)</label><input type="number" id="m_r" value="5" min="0" max="100"></div>'
            '<div class="hha-fld"><label>Volume</label><input type="number" id="m_v" value="500" min="0"></div>'
            '</div><div class="hha-out"><div class="l">Prix de vente → Marge sur volume</div>'
            '<div class="v" id="m_o">—</div><p class="n" id="m_n"></p>'
            '<a class="hha-tbtn" href="/negoce/">Piloter mes marges →</a></div>')
    js = ("function f(){var a=+m_a.value||0,k=+m_k.value||0,r=(+m_r.value||0)/100,v=+m_v.value||0;"
          "var pv=a*k*(1-r),mu=pv-a,tx=pv?mu/pv*100:0;"
          "document.getElementById('m_o').textContent=pv.toFixed(2)+' € → '+(mu*v).toLocaleString('fr-FR',{maximumFractionDigits:0})+' €';"
          "document.getElementById('m_n').textContent='Marge unitaire '+mu.toFixed(2)+' € ('+tx.toFixed(0)+'%).';}"
          "['m_a','m_k','m_r','m_v'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();")
    return _wrap("margin", "Outil interactif", "Calculez votre marge en négoce",
                 "Prix d'achat, coefficient, remise : marge sur volume.", body, js)


def _compare(slug):
    body = ('<p style="margin:.1rem 0 .6rem;color:#475569;font-size:.84rem">Cochez vos besoins :</p>'
            '<label class="hha-chk"><input type="checkbox" checked> Traçabilité lot & DLC</label>'
            '<label class="hha-chk"><input type="checkbox" checked> Poids variable & rendements</label>'
            '<label class="hha-chk"><input type="checkbox"> Conformité HACCP / INCO</label>'
            '<label class="hha-chk"><input type="checkbox" checked> Déploiement rapide SaaS</label>'
            '<label class="hha-chk"><input type="checkbox"> Multi-dépôts & télévente</label>'
            '<label class="hha-chk"><input type="checkbox"> Coût de revient réel</label>'
            '<div class="hha-out"><div class="l">Adéquation Hello Harel</div>'
            '<div class="v" id="cmp_o">—</div><p class="n" id="cmp_n"></p>'
            '<a class="hha-tbtn" href="/comparatifs/">Voir le comparatif →</a></div>')
    js = ("var box=document.currentScript.previousElementSibling;"
          "function f(){var cb=box.querySelectorAll('.hha-chk input'),n=0;cb.forEach(function(c){if(c.checked)n++});"
          "var t=cb.length,p=Math.round(n/t*100);"
          "document.getElementById('cmp_o').textContent=p+'%';"
          "document.getElementById('cmp_n').textContent='Hello Harel couvre '+n+'/'+t+' de vos besoins agro sélectionnés.';}"
          "box.addEventListener('change',f);f();")
    return _wrap("compare", "Outil interactif", "Hello Harel est-il fait pour vous ?",
                 "Sélectionnez vos priorités, mesurez l'adéquation.", body, js)


def _diag(slug):
    body = ('<div class="hha-fld"><label>Où en êtes-vous ?</label><select id="dg_s">'
            '<option value="0">Je découvre le sujet</option><option value="1">Je compare des solutions</option>'
            '<option value="2">Je veux déployer</option></select></div>'
            '<div class="hha-out"><div class="l">Étape conseillée</div>'
            '<div class="v" id="dg_o" style="font-size:1.05rem">—</div>'
            '<a class="hha-tbtn" id="dg_c" href="/contact/">Continuer →</a></div>')
    js = ("var M=[['Lisez ce guide puis explorez nos ressources.','/blog/','Voir le blog →'],"
          "['Comparez Hello Harel au marché.','/comparatifs/','Voir le comparatif →'],"
          "['Réservez une démonstration.','/contact/','Demander une démo →']];"
          "function f(){var i=+dg_s.value;document.getElementById('dg_o').textContent=M[i][0];"
          "var c=document.getElementById('dg_c');c.href=M[i][1];c.textContent=M[i][2];}"
          "document.getElementById('dg_s').addEventListener('change',f);f();")
    return _wrap("diagnostic", "Outil interactif", "Par où commencer ?",
                 "Un mini-diagnostic pour vous orienter.", body, js)


_BUILD = {"roi": _roi, "stock": _stock, "cost": _cost, "fefo": _fefo,
          "margin": _margin, "compare": _compare, "diagnostic": _diag}
