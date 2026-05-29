#!/usr/bin/env python3
"""
CRO building blocks for Hello Harel blog articles (granddaughter / L3 pages).

Three pieces, all returned as self-contained HTML+CSS+JS strings that drop into
the existing `content.raw` model (same design tokens as the FAQ drawer:
Inter font, brand blue #00B1F5, success green #22C55E):

  1) interactive_tool(slug)  -> a calculator/selector matched to the article's
     MICRO-INTENTION, placed at the TOP of the article (above the fold).
  2) inter_h2_visual(i, h2)  -> an illustrative HTML/CSS/SVG figure inserted
     BETWEEN each pair of H2 sections.
  3) cta_ladder(slug, ...)   -> a multi-level CTA block (reasonable-surfer /
     Hormozi value-equation: explorateur -> évaluateur -> convaincu -> décisionnaire).

TOOL_REGISTRY maps every blog slug to a tool id so each article gets a relevant
top-of-page interactive widget. Slugs not listed fall back to "diagnostic".
"""

BRAND = "#00B1F5"
GREEN = "#22C55E"

# ---- Micro-intention -> tool mapping -------------------------------------
TOOL_REGISTRY = {
    # ROI / decision
    "roi-erp": "roi", "erp-pme": "roi", "erp-saas": "roi", "erp-saas-cloud": "roi",
    "erp-cloud-saas-vs-on-premise": "roi", "migration-erp-agroalimentaire": "roi",
    "erp-as400": "roi", "erp-agroalimentaire": "roi",
    # Safety stock / replenishment
    "calcul-stock-de-securite": "safety_stock", "alerte-stock-securite": "safety_stock",
    "reapprovisionnement-stocks": "safety_stock", "gestion-des-inventaires": "safety_stock",
    "optimisation-entrepot": "safety_stock", "maitriser-la-gestion-des-stocks": "safety_stock",
    "gestion-stock-multi-entrepots": "safety_stock",
    # Cost / margin
    "cout-de-revient": "cost", "calcul-du-cout-achat": "cost", "cout-prix-au-kilo": "cost",
    "couts-de-production": "cost", "cout-marginal": "cost", "calcul-du-prix-moyen": "cost",
    "calculer-le-prix-de-revient-en-boulangerie": "cost", "calcul-cout-de-revient-logiciel": "cost",
    "calcul-freinte-charcuterie-logiciel": "cost", "logiciel-calcul-cout-de-revient-traiteur": "cost",
    "prix-dachat-definition": "cost", "difference-prix-dachat-et-prix-de-revient": "cost",
    # FEFO / rotation
    "fifo-fefo-lifo": "fefo", "dlc-ddm-dluo": "fefo", "alerte-date-peremption": "fefo",
    "tracabilite-lot-dlc-logiciel": "fefo", "logiciel-tracabilite-dlc-traiteur": "fefo",
}


def tool_for(slug):
    return TOOL_REGISTRY.get(slug, "diagnostic")


# ---- 1) Interactive tools -------------------------------------------------
def _shell(tool_id, title, intro, body_html, js):
    return f"""<!-- HH-CRO:tool:{tool_id} -->
<section class="hh-tool" data-tool="{tool_id}">
  <div class="hh-tool-head">
    <span class="hh-tool-badge">Outil interactif</span>
    <h2 class="hh-tool-title">{title}</h2>
    <p class="hh-tool-intro">{intro}</p>
  </div>
  <div class="hh-tool-body">{body_html}</div>
</section>
<style>
.hh-tool{{font-family:'Inter',sans-serif;max-width:760px;margin:1.5rem auto 2.5rem;background:linear-gradient(180deg,#f8fbff,#fff);
border:1px solid #e2e8f0;border-radius:18px;box-shadow:0 10px 30px rgba(0,60,120,.07);overflow:hidden}}
.hh-tool-head{{padding:1.5rem 1.75rem .5rem}}
.hh-tool-badge{{display:inline-block;background:{BRAND}1a;color:{BRAND};font-weight:700;font-size:.72rem;
letter-spacing:.05em;text-transform:uppercase;padding:.3rem .7rem;border-radius:999px}}
.hh-tool-title{{font-size:1.3rem;font-weight:800;color:#0f172a;margin:.6rem 0 .3rem}}
.hh-tool-intro{{color:#475569;font-size:.95rem;margin:0}}
.hh-tool-body{{padding:1.25rem 1.75rem 1.75rem}}
.hh-field{{margin-bottom:.9rem}}
.hh-field label{{display:block;font-size:.82rem;font-weight:600;color:#334155;margin-bottom:.3rem}}
.hh-field input,.hh-field select{{width:100%;padding:.6rem .75rem;border:1px solid #cbd5e1;border-radius:10px;font-size:.95rem;box-sizing:border-box}}
.hh-grid{{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}}
.hh-result{{margin-top:1rem;padding:1rem 1.25rem;background:{BRAND}0d;border:1px solid {BRAND}33;border-radius:12px}}
.hh-result .big{{font-size:1.8rem;font-weight:800;color:{BRAND};line-height:1.1}}
.hh-result .lbl{{font-size:.8rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:.04em}}
.hh-tool .hh-cta{{display:inline-block;margin-top:1rem;background:linear-gradient(135deg,{GREEN},#16a34a);color:#fff;
padding:.7rem 1.5rem;border-radius:10px;font-weight:700;text-decoration:none;font-size:.92rem}}
@media(max-width:600px){{.hh-grid{{grid-template-columns:1fr}}}}
</style>
<script>(function(){{{js}}})();</script>
"""


def tool_roi():
    body = """
    <div class="hh-grid">
      <div class="hh-field"><label>Nombre d'utilisateurs</label><input type="number" id="roi_u" value="10" min="1"></div>
      <div class="hh-field"><label>Heures perdues / sem. (saisie, Excel, ressaisie)</label><input type="number" id="roi_h" value="4" min="0"></div>
      <div class="hh-field"><label>Coût horaire chargé (€)</label><input type="number" id="roi_c" value="28" min="0"></div>
      <div class="hh-field"><label>Gain de productivité visé (%)</label><input type="number" id="roi_g" value="35" min="0" max="100"></div>
    </div>
    <div class="hh-result">
      <div class="lbl">Économies annuelles estimées</div>
      <div class="big" id="roi_out">—</div>
      <p style="margin:.4rem 0 0;color:#475569;font-size:.85rem" id="roi_note"></p>
      <a class="hh-cta" href="/contact/">Chiffrer mon ROI avec un expert →</a>
    </div>"""
    js = """
    function f(){var u=+document.getElementById('roi_u').value||0,h=+document.getElementById('roi_h').value||0,
    c=+document.getElementById('roi_c').value||0,g=(+document.getElementById('roi_g').value||0)/100;
    var save=u*h*52*c*g;
    document.getElementById('roi_out').textContent=save.toLocaleString('fr-FR',{maximumFractionDigits:0})+' € / an';
    document.getElementById('roi_note').textContent='Soit '+(u*h*g).toFixed(1)+' h récupérées par semaine sur l\\'ensemble de l\\'équipe.';}
    ['roi_u','roi_h','roi_c','roi_g'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();"""
    return _shell("roi", "Calculez le ROI de votre ERP",
                  "Estimez en 10 secondes les économies réalisables en supprimant les ressaisies et le travail sous Excel.",
                  body, js)


def tool_safety_stock():
    body = """
    <div class="hh-grid">
      <div class="hh-field"><label>Conso. moyenne / jour</label><input type="number" id="ss_d" value="120" min="0"></div>
      <div class="hh-field"><label>Délai fournisseur (jours)</label><input type="number" id="ss_l" value="5" min="0"></div>
      <div class="hh-field"><label>Conso. max / jour (pic)</label><input type="number" id="ss_dm" value="180" min="0"></div>
      <div class="hh-field"><label>Délai max (jours)</label><input type="number" id="ss_lm" value="8" min="0"></div>
    </div>
    <div class="hh-result">
      <div class="lbl">Stock de sécurité recommandé</div>
      <div class="big" id="ss_out">—</div>
      <p style="margin:.4rem 0 0;color:#475569;font-size:.85rem" id="ss_note"></p>
      <a class="hh-cta" href="/fonctionnalites/gestion-de-stock/">Automatiser ce calcul dans l'ERP →</a>
    </div>"""
    js = """
    function f(){var d=+document.getElementById('ss_d').value||0,l=+document.getElementById('ss_l').value||0,
    dm=+document.getElementById('ss_dm').value||0,lm=+document.getElementById('ss_lm').value||0;
    var ss=(dm*lm)-(d*l); if(ss<0)ss=0;
    document.getElementById('ss_out').textContent=ss.toLocaleString('fr-FR',{maximumFractionDigits:0})+' unités';
    document.getElementById('ss_note').textContent='Point de commande conseillé : '+((d*l)+ss).toLocaleString('fr-FR')+' unités (méthode max−moyenne).';}
    ['ss_d','ss_l','ss_dm','ss_lm'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();"""
    return _shell("safety_stock", "Calculez votre stock de sécurité",
                  "Évitez la rupture comme le sur-stockage : obtenez votre stock de sécurité et votre point de commande.",
                  body, js)


def tool_cost():
    body = """
    <div class="hh-grid">
      <div class="hh-field"><label>Coût matières (€)</label><input type="number" id="co_m" value="3.20" step="0.01" min="0"></div>
      <div class="hh-field"><label>Main d'œuvre (€)</label><input type="number" id="co_l" value="1.10" step="0.01" min="0"></div>
      <div class="hh-field"><label>Frais / charges (€)</label><input type="number" id="co_o" value="0.70" step="0.01" min="0"></div>
      <div class="hh-field"><label>Freinte / pertes (%)</label><input type="number" id="co_f" value="6" min="0" max="100"></div>
      <div class="hh-field"><label>Marge visée (%)</label><input type="number" id="co_mg" value="30" min="0" max="100"></div>
    </div>
    <div class="hh-result">
      <div class="lbl">Coût de revient / Prix de vente conseillé</div>
      <div class="big" id="co_out">—</div>
      <p style="margin:.4rem 0 0;color:#475569;font-size:.85rem" id="co_note"></p>
      <a class="hh-cta" href="/fonctionnalites/fabrication/">Fiabiliser mes coûts de revient →</a>
    </div>"""
    js = """
    function f(){var m=+document.getElementById('co_m').value||0,l=+document.getElementById('co_l').value||0,
    o=+document.getElementById('co_o').value||0,fr=(+document.getElementById('co_f').value||0)/100,
    mg=(+document.getElementById('co_mg').value||0)/100;
    var cr=(m+l+o)/(1-fr); var pv=mg<1?cr/(1-mg):cr;
    document.getElementById('co_out').textContent=cr.toFixed(2)+' € → '+pv.toFixed(2)+' €';
    document.getElementById('co_note').textContent='Coût de revient '+cr.toFixed(2)+' € (freinte incluse), prix de vente pour '+(mg*100).toFixed(0)+' % de marge : '+pv.toFixed(2)+' €.';}
    ['co_m','co_l','co_o','co_f','co_mg'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();"""
    return _shell("cost", "Calculez votre coût de revient réel",
                  "Intégrez la freinte et les charges pour fixer un prix de vente qui protège vraiment votre marge.",
                  body, js)


def tool_fefo():
    body = """
    <div class="hh-field"><label>Type de produit</label>
      <select id="fe_t">
        <option value="dlc">Produit frais à DLC courte</option>
        <option value="ddm">Produit à DDM (épicerie, surgelé)</option>
        <option value="lot">Matière première stockable</option>
      </select></div>
    <div class="hh-field"><label>Forte saisonnalité / promotions ?</label>
      <select id="fe_s"><option value="non">Non</option><option value="oui">Oui</option></select></div>
    <div class="hh-result">
      <div class="lbl">Méthode de rotation conseillée</div>
      <div class="big" id="fe_out">—</div>
      <p style="margin:.4rem 0 0;color:#475569;font-size:.85rem" id="fe_note"></p>
      <a class="hh-cta" href="/fonctionnalites/gestion-de-stock/">Appliquer le FEFO automatiquement →</a>
    </div>"""
    js = """
    function f(){var t=document.getElementById('fe_t').value,s=document.getElementById('fe_s').value,m,n;
    if(t==='dlc'){m='FEFO';n='Premier périmé, premier sorti : impératif sur les DLC courtes pour limiter la casse.';}
    else if(t==='ddm'){m=(s==='oui')?'FEFO':'FIFO';n='FIFO suffit hors promotions ; basculez en FEFO si les pics créent des écarts de dates.';}
    else{m='FIFO';n='Rotation par ancienneté ; le LIFO ne se justifie qu\\'en logique comptable, pas physique en agro.';}
    document.getElementById('fe_out').textContent=m;document.getElementById('fe_note').textContent=n;}
    ['fe_t','fe_s'].forEach(function(i){document.getElementById(i).addEventListener('change',f)});f();"""
    return _shell("fefo", "Quelle méthode de rotation pour vos stocks ?",
                  "FIFO, FEFO ou LIFO ? Répondez à 2 questions pour connaître la méthode adaptée à vos produits.",
                  body, js)


def tool_diagnostic(slug, title):
    body = f"""
    <div class="hh-field"><label>Où en êtes-vous sur « {title} » ?</label>
      <select id="dg_s">
        <option value="0">Je découvre le sujet</option>
        <option value="1">Je compare des solutions</option>
        <option value="2">Je veux mettre en place une solution</option>
      </select></div>
    <div class="hh-result">
      <div class="lbl">Prochaine étape recommandée</div>
      <div class="big" id="dg_out" style="font-size:1.15rem">—</div>
      <a class="hh-cta" id="dg_cta" href="/contact/">Continuer →</a>
    </div>"""
    js = """
    var map=[['Lisez ce guide en entier, puis explorez nos ressources liées.','/blog/','Voir les ressources →'],
    ['Comparez Hello Harel aux solutions du marché.','/comparatifs/','Voir le comparatif →'],
    ['Réservez une démonstration personnalisée.','/contact/','Demander une démo →']];
    function f(){var i=+document.getElementById('dg_s').value;document.getElementById('dg_out').textContent=map[i][0];
    var c=document.getElementById('dg_cta');c.href=map[i][1];c.textContent=map[i][2];}
    document.getElementById('dg_s').addEventListener('change',f);f();"""
    return _shell("diagnostic", "Par où commencer ?",
                  "Un mini-diagnostic pour vous orienter vers la ressource la plus utile selon votre situation.",
                  body, js)


def interactive_tool(slug, title=""):
    tid = tool_for(slug)
    return {"roi": tool_roi, "safety_stock": tool_safety_stock, "cost": tool_cost,
            "fefo": tool_fefo}.get(tid, lambda: tool_diagnostic(slug, title))()


# ---- 2) Inter-H2 illustrative visual -------------------------------------
def inter_h2_visual(index, h2_text):
    """A lightweight, on-brand HTML/CSS figure to break up the wall of text."""
    palette = [BRAND, GREEN, "#6366f1", "#f59e0b", "#ec4899"]
    color = palette[index % len(palette)]
    pct = [62, 78, 45, 88, 70][index % 5]
    return f"""<!-- HH-CRO:visual:{index} -->
<figure class="hh-visual" aria-hidden="true">
  <div class="hh-visual-bar"><span style="width:{pct}%;background:{color}"></span></div>
  <figcaption>{h2_text}</figcaption>
  <style>
  .hh-visual{{font-family:'Inter',sans-serif;max-width:680px;margin:1.5rem auto;padding:1.1rem 1.25rem;
  background:#fff;border:1px solid #eef2f7;border-left:4px solid {color};border-radius:12px;box-shadow:0 4px 16px rgba(0,40,80,.05)}}
  .hh-visual-bar{{height:10px;background:#eef2f7;border-radius:999px;overflow:hidden;margin-bottom:.6rem}}
  .hh-visual-bar span{{display:block;height:100%;border-radius:999px;transition:width .8s ease}}
  .hh-visual figcaption{{font-size:.85rem;color:#64748b;font-weight:600}}
  </style>
</figure>"""


# ---- 3) Multi-level CTA ladder (reasonable surfer / Hormozi) --------------
def cta_ladder(explorer_link="/blog/", evaluator_link="/comparatifs/",
               convinced_link="/tarifs/", decision_link="/contact/"):
    return f"""<!-- HH-CRO:cta-ladder -->
<section class="hh-ctal">
  <h2 class="hh-ctal-title">Selon votre niveau d'avancement</h2>
  <div class="hh-ctal-grid">
    <a class="hh-ctal-card lvl1" href="{explorer_link}"><span>J'explore</span><b>Ressources & guides liés</b></a>
    <a class="hh-ctal-card lvl2" href="{evaluator_link}"><span>Je compare</span><b>Comparatif des ERP</b></a>
    <a class="hh-ctal-card lvl3" href="{convinced_link}"><span>Je me décide</span><b>Voir les tarifs</b></a>
    <a class="hh-ctal-card lvl4" href="{decision_link}"><span>Je suis prêt</span><b>Demander une démo</b></a>
  </div>
  <style>
  .hh-ctal{{font-family:'Inter',sans-serif;max-width:880px;margin:2.5rem auto}}
  .hh-ctal-title{{font-size:1.15rem;font-weight:800;color:#0f172a;text-align:center;margin-bottom:1rem}}
  .hh-ctal-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem}}
  .hh-ctal-card{{display:flex;flex-direction:column;gap:.25rem;padding:1rem;border-radius:14px;text-decoration:none;
  border:1px solid #e2e8f0;background:#fff;transition:transform .2s,box-shadow .2s}}
  .hh-ctal-card:hover{{transform:translateY(-3px);box-shadow:0 12px 26px rgba(0,40,80,.12)}}
  .hh-ctal-card span{{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#94a3b8}}
  .hh-ctal-card b{{font-size:.95rem;color:#0f172a}}
  .hh-ctal-card.lvl4{{background:linear-gradient(135deg,{GREEN},#16a34a);border-color:transparent}}
  .hh-ctal-card.lvl4 span{{color:#dcfce7}} .hh-ctal-card.lvl4 b{{color:#fff}}
  .hh-ctal-card.lvl3{{border-color:{BRAND}55}}
  @media(max-width:760px){{.hh-ctal-grid{{grid-template-columns:1fr 1fr}}}}
  </style>
</section>"""
