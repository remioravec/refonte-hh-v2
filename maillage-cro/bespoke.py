#!/usr/bin/env python3
"""
Bespoke, high-value interactive tools + custom inter-H2 visuals for 10 flagship
articles. Each tool is genuinely useful for the article's micro-intention and
ships with a live visual (waterfall / gauge / comparison / simulator). Everything
is self-contained, scoped under .hha-tpl, vanilla JS in an IIFE, unique ids.

API:
  has(slug) -> bool
  tool(slug) -> str | None         top-of-article interactive tool
  visuals_for(slug) -> [(keywords, html)]   inter-H2 visuals matched by H2 text
"""

# ----------------------------------------------------------------------------
# 1) ROI ERP
ROI = r"""
<section class="hha-tool" data-tool="b-roi"><div class="hha-tool-h">
<span class="hha-tool-badge">Calculateur ROI</span>
<h3>Calculez le ROI réel de votre ERP</h3>
<p>Temps gagné, économies et retour sur investissement, en direct.</p></div>
<div class="hha-tool-b">
<div class="hha-tg">
<div class="hha-fld"><label>Nombre d'utilisateurs</label><input type="number" id="ro_u" value="10" min="1"></div>
<div class="hha-fld"><label>Heures perdues / sem. (saisie, Excel)</label><input type="number" id="ro_h" value="4" min="0"></div>
<div class="hha-fld"><label>Coût horaire chargé (€)</label><input type="number" id="ro_c" value="28" min="0"></div>
<div class="hha-fld"><label>Gain de productivité visé (%)</label><input type="number" id="ro_g" value="35" min="0" max="100"></div>
<div class="hha-fld"><label>Coût annuel de l'ERP (€)</label><input type="number" id="ro_l" value="6000" min="0"></div>
<div class="hha-fld"><label>Erreurs évitées / an (€)</label><input type="number" id="ro_e" value="3000" min="0"></div>
</div>
<div class="hha-out">
<div class="l">Gain net annuel estimé</div><div class="v" id="ro_net">—</div>
<div class="hb-cmp" style="margin-top:12px">
<div class="hb-card"><div class="big" id="ro_save" style="color:#02587F">—</div><div class="lbl">Économies / an</div></div>
<div class="hb-card win"><div class="big" id="ro_pay">—</div><div class="lbl">Retour sur invest.</div></div>
</div>
<p class="n" id="ro_note"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div>
<script>(function(){
function f(){var u=+ro_u.value||0,h=+ro_h.value||0,c=+ro_c.value||0,g=(+ro_g.value||0)/100,l=+ro_l.value||0,e=+ro_e.value||0;
var save=u*h*52*c*g+e;var net=save-l;
document.getElementById('ro_save').textContent=Math.round(save).toLocaleString('fr-FR')+' €';
document.getElementById('ro_net').textContent=Math.round(net).toLocaleString('fr-FR')+' € / an';
var pay=save>0?(l/save*12):0;
document.getElementById('ro_pay').textContent=l<=0?'immédiat':(pay<12?pay.toFixed(1)+' mois':(pay/12).toFixed(1)+' ans');
document.getElementById('ro_note').textContent='Soit '+(u*h*g).toFixed(1)+" h récupérées/semaine, plus "+Math.round(e).toLocaleString('fr-FR')+" € d'erreurs évitées.";}
['ro_u','ro_h','ro_c','ro_g','ro_l','ro_e'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();
})();</script></section>"""

# 2) ERP AS400 — TCO 5 ans
TCO = r"""
<section class="hha-tool" data-tool="b-tco"><div class="hha-tool-h">
<span class="hha-tool-badge">Comparateur TCO 5 ans</span>
<h3>AS/400 vs ERP SaaS : le coût réel sur 5 ans</h3>
<p>Comparez le coût total de possession et trouvez le point de bascule.</p></div>
<div class="hha-tool-b">
<div class="hha-tg">
<div class="hha-fld"><label>AS/400 — maintenance + licences / an (€)</label><input type="number" id="tc_a" value="22000" min="0"></div>
<div class="hha-fld"><label>AS/400 — serveur & infogérance / an (€)</label><input type="number" id="tc_s" value="8000" min="0"></div>
<div class="hha-fld"><label>ERP SaaS — abonnement / an (€)</label><input type="number" id="tc_c" value="12000" min="0"></div>
<div class="hha-fld"><label>ERP SaaS — coût de migration (one-shot €)</label><input type="number" id="tc_m" value="9000" min="0"></div>
</div>
<div class="hha-out"><div class="l">Coût cumulé sur 5 ans</div>
<div class="hb-cmp" style="margin-top:10px">
<div class="hb-card"><div class="lbl">AS/400</div><div class="big" id="tc_oa" style="color:#64748b">—</div></div>
<div class="hb-card win"><div class="lbl">ERP SaaS</div><div class="big" id="tc_oc">—</div></div>
</div>
<p class="n" id="tc_note"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div>
<script>(function(){
function f(){var a=+tc_a.value||0,s=+tc_s.value||0,c=+tc_c.value||0,m=+tc_m.value||0;
var as=(a+s)*5, sa=c*5+m;
document.getElementById('tc_oa').textContent=Math.round(as).toLocaleString('fr-FR')+' €';
document.getElementById('tc_oc').textContent=Math.round(sa).toLocaleString('fr-FR')+' €';
var diff=as-sa, per=(a+s)-c;
var be=per>0?(m/per):0;
document.getElementById('tc_note').textContent=(diff>0?('Économie de '+Math.round(diff).toLocaleString('fr-FR')+' € sur 5 ans. '):'Surcoût de '+Math.round(-diff).toLocaleString('fr-FR')+' € sur 5 ans. ')+(per>0?('Point de bascule : '+be.toFixed(1)+' an(s).'):'');}
['tc_a','tc_s','tc_c','tc_m'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();
})();</script></section>"""

# 3) Coût de revient — waterfall
COST = r"""
<section class="hha-tool" data-tool="b-cost"><div class="hha-tool-h">
<span class="hha-tool-badge">Calculateur de coût de revient</span>
<h3>Votre coût de revient réel, décomposé</h3>
<p>Matières, main d'œuvre, charges et freinte : visualisez où part votre prix.</p></div>
<div class="hha-tool-b">
<div class="hha-tg">
<div class="hha-fld"><label>Coût matières (€)</label><input type="number" id="co_m" value="3.20" step="0.01" min="0"></div>
<div class="hha-fld"><label>Main d'œuvre (€)</label><input type="number" id="co_l" value="1.10" step="0.01" min="0"></div>
<div class="hha-fld"><label>Charges / frais (€)</label><input type="number" id="co_o" value="0.70" step="0.01" min="0"></div>
<div class="hha-fld"><label>Freinte / pertes (%)</label><input type="number" id="co_f" value="6" min="0" max="100"></div>
<div class="hha-fld"><label>Marge visée (%)</label><input type="number" id="co_g" value="30" min="0" max="95"></div>
</div>
<div class="hha-out">
<div class="l">Décomposition du prix de vente</div>
<div class="hb-water" id="co_water" style="margin:10px 0"></div>
<div class="v" id="co_pv">—</div><p class="n" id="co_n"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div></div>
<script>(function(){
var C=['#02587F','#38bdf8','#f59e0b','#ef4444','#22c55e'];
function row(lab,val,pct,color){return '<div class="hb-wrow"><span class="lab">'+lab+'</span>'+
'<div class="hb-wtrack"><div class="hb-wseg" style="width:'+Math.min(100,pct)+'%;background:'+color+'"></div></div>'+
'<span class="val">'+val.toFixed(2)+' €</span></div>';}
function f(){var m=+co_m.value||0,l=+co_l.value||0,o=+co_o.value||0,fr=(+co_f.value||0)/100,g=(+co_g.value||0)/100;
var cr=(m+l+o)/(1-fr);var fre=cr-(m+l+o);var pv=g<1?cr/(1-g):cr;var marge=pv-cr;
document.getElementById('co_pv').textContent='Prix de vente conseillé : '+pv.toFixed(2)+' €';
var T=pv||1;
document.getElementById('co_water').innerHTML=
row('Matières',m,m/T*100,C[0])+row('Main d\'œuvre',l,l/T*100,C[1])+
row('Charges',o,o/T*100,C[2])+row('Freinte',fre,fre/T*100,C[3])+row('Marge',marge,marge/T*100,C[4]);
document.getElementById('co_n').textContent='Coût de revient '+cr.toFixed(2)+' € (freinte incluse) pour '+(g*100).toFixed(0)+'% de marge.';}
['co_m','co_l','co_o','co_f','co_g'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();
})();</script></section>"""

# 4) Boulangerie — recette
BAKE = r"""
<section class="hha-tool" data-tool="b-bake"><div class="hha-tool-h">
<span class="hha-tool-badge">Simulateur boulangerie</span>
<h3>Prix de revient d'une fournée</h3>
<p>De la farine au prix de vente conseillé, par pièce.</p></div>
<div class="hha-tool-b">
<div class="hha-tg">
<div class="hha-fld"><label>Farine (€ / kg)</label><input type="number" id="bk_ff" value="0.85" step="0.01" min="0"></div>
<div class="hha-fld"><label>Farine par fournée (kg)</label><input type="number" id="bk_fk" value="10" step="0.1" min="0"></div>
<div class="hha-fld"><label>Autres ingrédients (€)</label><input type="number" id="bk_i" value="6" step="0.1" min="0"></div>
<div class="hha-fld"><label>Énergie (four) (€)</label><input type="number" id="bk_e" value="3.5" step="0.1" min="0"></div>
<div class="hha-fld"><label>Main d'œuvre (€)</label><input type="number" id="bk_l" value="12" step="0.5" min="0"></div>
<div class="hha-fld"><label>Pièces par fournée</label><input type="number" id="bk_n" value="80" min="1"></div>
</div>
<div class="hha-out">
<div class="hb-cmp">
<div class="hb-card"><div class="lbl">Coût / pièce</div><div class="big" id="bk_cu" style="color:#02587F">—</div></div>
<div class="hb-card win"><div class="lbl">Prix conseillé (×3)</div><div class="big" id="bk_pv">—</div></div>
</div>
<p class="n" id="bk_n2"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div></div>
<script>(function(){
function f(){var ff=+bk_ff.value||0,fk=+bk_fk.value||0,i=+bk_i.value||0,e=+bk_e.value||0,l=+bk_l.value||0,n=+bk_n.value||1;
var tot=ff*fk+i+e+l;var cu=tot/n;var pv=cu*3;
document.getElementById('bk_cu').textContent=cu.toFixed(3)+' €';
document.getElementById('bk_pv').textContent=pv.toFixed(2)+' €';
document.getElementById('bk_n2').textContent='Coût total de la fournée : '+tot.toFixed(2)+' € pour '+n+' pièces (coefficient ×3 = marge ~67%).';}
['bk_ff','bk_fk','bk_i','bk_e','bk_l','bk_n'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();
})();</script></section>"""

# 5) Stock de sécurité — 3 méthodes
SAFETY = r"""
<section class="hha-tool" data-tool="b-safety"><div class="hha-tool-h">
<span class="hha-tool-badge">Calculateur de stock de sécurité</span>
<h3>Stock de sécurité & point de commande</h3>
<p>Trois méthodes, un résultat actionnable instantané.</p></div>
<div class="hha-tool-b">
<div class="hb-pills" id="ss_pills">
<span class="hb-pill on" data-m="0">Max − Moyenne</span>
<span class="hb-pill" data-m="1">Niveau de service</span>
<span class="hb-pill" data-m="2">Statistique (loi normale)</span></div>
<div class="hha-tg">
<div class="hha-fld"><label>Conso. moyenne / jour</label><input type="number" id="ss_d" value="120" min="0"></div>
<div class="hha-fld"><label>Délai fournisseur (jours)</label><input type="number" id="ss_l" value="5" min="0"></div>
<div class="hha-fld m0"><label>Conso. max / jour</label><input type="number" id="ss_dm" value="180" min="0"></div>
<div class="hha-fld m0"><label>Délai max (jours)</label><input type="number" id="ss_lm" value="8" min="0"></div>
<div class="hha-fld m1 m2" style="display:none"><label>Écart-type conso./jour</label><input type="number" id="ss_sd" value="25" min="0"></div>
<div class="hha-fld m1 m2" style="display:none"><label>Niveau de service (%)</label><input type="number" id="ss_sl" value="95" min="50" max="99"></div>
</div>
<div class="hha-out"><div class="l">Stock de sécurité</div><div class="v" id="ss_o">—</div>
<p class="n" id="ss_n"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div></div>
<script>(function(){
var mode=0;var Z={90:1.28,95:1.65,97:1.88,98:2.05,99:2.33};
function zfor(p){var keys=Object.keys(Z).map(Number);var best=keys[0];keys.forEach(function(k){if(Math.abs(k-p)<Math.abs(best-p))best=k;});return Z[best];}
function show(){document.querySelectorAll('.m0,.m1,.m2').forEach(function(e){e.style.display='none';});
document.querySelectorAll('.m'+mode).forEach(function(e){e.style.display='';});}
function f(){var d=+ss_d.value||0,l=+ss_l.value||0,ss=0,note='';
if(mode===0){var dm=+ss_dm.value||0,lm=+ss_lm.value||0;ss=(dm*lm)-(d*l);note='Méthode max − moyenne : (conso max × délai max) − (conso moy × délai moy).';}
else{var sd=+ss_sd.value||0,sl=+ss_sl.value||95,z=zfor(sl);ss=z*sd*Math.sqrt(l);note='Méthode loi normale : Z('+sl+'%)='+z+' × écart-type × √délai.';}
if(ss<0)ss=0;document.getElementById('ss_o').textContent=Math.round(ss).toLocaleString('fr-FR')+' unités';
document.getElementById('ss_n').textContent=note+' Point de commande conseillé : '+Math.round(d*l+ss).toLocaleString('fr-FR')+' unités.';}
document.querySelectorAll('#ss_pills .hb-pill').forEach(function(p){p.addEventListener('click',function(){
document.querySelectorAll('#ss_pills .hb-pill').forEach(function(x){x.classList.remove('on')});p.classList.add('on');
mode=+p.dataset.m;show();f();});});
['ss_d','ss_l','ss_dm','ss_lm','ss_sd','ss_sl'].forEach(function(i){var el=document.getElementById(i);if(el)el.addEventListener('input',f)});
show();f();
})();</script></section>"""

# 6) Stock moyen + rotation
AVG = r"""
<section class="hha-tool" data-tool="b-avg"><div class="hha-tool-h">
<span class="hha-tool-badge">Calculateur de stock moyen</span>
<h3>Stock moyen & taux de rotation</h3>
<p>Mesurez la performance de votre stock en quelques secondes.</p></div>
<div class="hha-tool-b">
<div class="hha-tg">
<div class="hha-fld"><label>Stock initial (unités)</label><input type="number" id="av_i" value="400" min="0"></div>
<div class="hha-fld"><label>Stock final (unités)</label><input type="number" id="av_f" value="200" min="0"></div>
<div class="hha-fld"><label>Consommation sur la période</label><input type="number" id="av_c" value="3600" min="0"></div>
<div class="hha-fld"><label>Durée de la période (jours)</label><input type="number" id="av_d" value="365" min="1"></div>
</div>
<div class="hha-out">
<div class="hb-cmp">
<div class="hb-card"><div class="lbl">Stock moyen</div><div class="big" id="av_m" style="color:#02587F">—</div></div>
<div class="hb-card win"><div class="lbl">Rotations / période</div><div class="big" id="av_r">—</div></div>
</div>
<p class="n" id="av_n"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div></div>
<script>(function(){
function f(){var i=+av_i.value||0,fi=+av_f.value||0,c=+av_c.value||0,d=+av_d.value||1;
var m=(i+fi)/2;var rot=m>0?c/m:0;var couv=rot>0?d/rot:0;
document.getElementById('av_m').textContent=Math.round(m).toLocaleString('fr-FR');
document.getElementById('av_r').textContent=rot.toFixed(1);
document.getElementById('av_n').textContent='Couverture moyenne : '+couv.toFixed(0)+' jours de stock. Plus la rotation est élevée, moins votre trésorerie dort.';}
['av_i','av_f','av_c','av_d'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();
})();</script></section>"""

# 7) Réapprovisionnement — point de commande + EOQ (Wilson)
REORDER = r"""
<section class="hha-tool" data-tool="b-reorder"><div class="hha-tool-h">
<span class="hha-tool-badge">Calculateur de réapprovisionnement</span>
<h3>Point de commande & quantité économique</h3>
<p>Quand commander, et combien : la formule de Wilson appliquée.</p></div>
<div class="hha-tool-b">
<div class="hha-tg">
<div class="hha-fld"><label>Demande annuelle (unités)</label><input type="number" id="re_d" value="36000" min="0"></div>
<div class="hha-fld"><label>Délai fournisseur (jours)</label><input type="number" id="re_l" value="5" min="0"></div>
<div class="hha-fld"><label>Stock de sécurité (unités)</label><input type="number" id="re_s" value="300" min="0"></div>
<div class="hha-fld"><label>Coût d'une commande (€)</label><input type="number" id="re_c" value="60" min="0"></div>
<div class="hha-fld"><label>Coût de stockage / unité / an (€)</label><input type="number" id="re_h" value="2.5" step="0.1" min="0.01"></div>
</div>
<div class="hha-out">
<div class="hb-cmp">
<div class="hb-card"><div class="lbl">Point de commande</div><div class="big" id="re_rop" style="color:#02587F">—</div></div>
<div class="hb-card win"><div class="lbl">Quantité éco. (EOQ)</div><div class="big" id="re_eoq">—</div></div>
</div>
<p class="n" id="re_n"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div></div>
<script>(function(){
function f(){var D=+re_d.value||0,l=+re_l.value||0,ss=+re_s.value||0,k=+re_c.value||0,h=+re_h.value||0.01;
var daily=D/365;var rop=daily*l+ss;var eoq=Math.sqrt(2*D*k/h);
document.getElementById('re_rop').textContent=Math.round(rop).toLocaleString('fr-FR');
document.getElementById('re_eoq').textContent=Math.round(eoq).toLocaleString('fr-FR');
var nb=eoq>0?D/eoq:0;
document.getElementById('re_n').textContent='Commandez quand le stock atteint '+Math.round(rop).toLocaleString('fr-FR')+' unités, par lots de ~'+Math.round(eoq).toLocaleString('fr-FR')+' unités, soit ~'+nb.toFixed(0)+' commandes/an.';}
['re_d','re_l','re_s','re_c','re_h'].forEach(function(i){document.getElementById(i).addEventListener('input',f)});f();
})();</script></section>"""

# 8) FIFO/FEFO/LIFO — simulateur de rotation
ROT = r"""
<section class="hha-tool" data-tool="b-rot"><div class="hha-tool-h">
<span class="hha-tool-badge">Simulateur de rotation</span>
<h3>Quel lot sort en premier ?</h3>
<p>Choisissez la méthode : le lot prélevé est mis en évidence.</p></div>
<div class="hha-tool-b">
<div class="hb-pills" id="rt_pills">
<span class="hb-pill on" data-m="FIFO">FIFO</span>
<span class="hb-pill" data-m="FEFO">FEFO</span>
<span class="hb-pill" data-m="LIFO">LIFO</span></div>
<div class="hb-lots" id="rt_lots">
<div class="hb-lot" data-in="2026-01-10" data-dlc="2026-04-20"><div class="n">Lot A</div><div class="d">Entré 10/01<br>DLC 20/04</div><div class="tag">Sort en premier</div></div>
<div class="hb-lot" data-in="2026-02-05" data-dlc="2026-03-15"><div class="n">Lot B</div><div class="d">Entré 05/02<br>DLC 15/03</div><div class="tag">Sort en premier</div></div>
<div class="hb-lot" data-in="2026-02-28" data-dlc="2026-06-30"><div class="n">Lot C</div><div class="d">Entré 28/02<br>DLC 30/06</div><div class="tag">Sort en premier</div></div>
</div>
<p class="n" id="rt_n" style="margin-top:12px"></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></section>
<script>(function(){
var mode='FIFO';var lots=[].slice.call(document.querySelectorAll('#rt_lots .hb-lot'));
var msg={FIFO:'FIFO : le premier entré sort en premier (rotation par ancienneté d\'entrée).',
FEFO:'FEFO : le premier périmé sort en premier — indispensable sur DLC courtes.',
LIFO:'LIFO : le dernier entré sort en premier (logique comptable, rarement physique en agro).'};
function pick(){var idx=0;
if(mode==='FIFO'){var min=lots[0].dataset.in;lots.forEach(function(e,i){if(e.dataset.in<min){min=e.dataset.in;idx=i;}});}
else if(mode==='FEFO'){var md=lots[0].dataset.dlc;lots.forEach(function(e,i){if(e.dataset.dlc<md){md=e.dataset.dlc;idx=i;}});}
else{var mx=lots[0].dataset.in;lots.forEach(function(e,i){if(e.dataset.in>mx){mx=e.dataset.in;idx=i;}});}
lots.forEach(function(e){e.classList.remove('first')});lots[idx].classList.add('first');
document.getElementById('rt_n').textContent=msg[mode];}
document.querySelectorAll('#rt_pills .hb-pill').forEach(function(p){p.addEventListener('click',function(){
document.querySelectorAll('#rt_pills .hb-pill').forEach(function(x){x.classList.remove('on')});p.classList.add('on');mode=p.dataset.m;pick();});});
pick();
})();</script>"""

# 9) DLC/DDM — classifieur + jauge
EXPIRY = r"""
<section class="hha-tool" data-tool="b-exp"><div class="hha-tool-h">
<span class="hha-tool-badge">Assistant DLC / DDM</span>
<h3>Quelle date, quelle action ?</h3>
<p>Identifiez le type de date et l'action à mener selon les jours restants.</p></div>
<div class="hha-tool-b">
<div class="hha-tg">
<div class="hha-fld"><label>Type de produit</label><select id="ex_t">
<option value="dlc">Frais périssable (viande, traiteur, lait…)</option>
<option value="ddm">Stable (épicerie, surgelé, conserve…)</option></select></div>
<div class="hha-fld"><label>Jours avant la date</label><input type="number" id="ex_j" value="4" min="-5"></div>
</div>
<div class="hha-out">
<div class="l">Type de date</div><div class="v" id="ex_type">—</div>
<div class="hb-gauge"><span class="mk" id="ex_mk" style="left:50%"></span></div>
<div class="hb-gscale"><span>Critique</span><span>Surveiller</span><span>OK</span></div>
<p class="n"><span class="hb-badge" id="ex_badge">—</span> <span id="ex_act"></span></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div></section>
<script>(function(){
function f(){var t=ex_t.value,j=+ex_j.value;
document.getElementById('ex_type').textContent=(t==='dlc')?'DLC — Date Limite de Consommation':'DDM — Date de Durabilité Minimale';
var pct=Math.max(0,Math.min(100,(j+2)/12*100));document.getElementById('ex_mk').style.left=pct+'%';
var b=document.getElementById('ex_badge'),a=document.getElementById('ex_act');
function set(txt,bg,col,msg){b.textContent=txt;b.style.background=bg;b.style.color=col;a.textContent=msg;}
if(t==='dlc'){
 if(j<0){set('RETIRER','#fee2e2','#b91c1c','DLC dépassée : retrait immédiat de la vente (obligation sanitaire).');}
 else if(j<=2){set('PROMO','#fef3c7','#92400e','DLC proche : appliquer une démarque / promotion anti-gaspillage.');}
 else{set('OK','#dcfce7','#166534','Vente normale ; appliquer le FEFO en stock.');}
}else{
 if(j<0){set('VENDABLE','#fef3c7','#92400e','DDM dépassée : produit encore commercialisable (qualité, pas sécurité).');}
 else{set('OK','#dcfce7','#166534','Rotation standard ; surveiller pour limiter la casse.');}
}}
['ex_t','ex_j'].forEach(function(i){document.getElementById(i).addEventListener('input',f);document.getElementById(i).addEventListener('change',f)});f();
})();</script>"""

# 10) ERP PME — score d'adéquation
FIT = r"""
<section class="hha-tool" data-tool="b-fit"><div class="hha-tool-h">
<span class="hha-tool-badge">Test d'adéquation ERP PME</span>
<h3>Votre PME est-elle prête pour un ERP ?</h3>
<p>Cochez votre réalité : obtenez un score et la prochaine étape.</p></div>
<div class="hha-tool-b" id="fit_b">
<label class="hha-chk"><input type="checkbox" data-w="20"> Vous gérez encore vos stocks/commandes sous Excel</label>
<label class="hha-chk"><input type="checkbox" data-w="15"> Les ressaisies entre outils vous font perdre du temps</label>
<label class="hha-chk"><input type="checkbox" data-w="20"> Vous avez des obligations de traçabilité / DLC</label>
<label class="hha-chk"><input type="checkbox" data-w="15"> Plusieurs personnes saisissent les mêmes données</label>
<label class="hha-chk"><input type="checkbox" data-w="15"> Vous manquez de visibilité sur vos marges en temps réel</label>
<label class="hha-chk"><input type="checkbox" data-w="15"> Vous prévoyez de croître / d'ouvrir un site</label>
<div class="hha-out"><div class="l">Score d'adéquation</div><div class="v" id="fit_s">0 / 100</div>
<div class="hb-gauge"><span class="mk" id="fit_mk" style="left:0%"></span></div>
<p class="n"><span class="hb-badge" id="fit_badge">—</span> <span id="fit_msg"></span></p>
<a class="hha-tbtn" href="/contact/">Demander une démo →</a></div></div></section>
<script>(function(){
var box=document.getElementById('fit_b');
function f(){var s=0;box.querySelectorAll('input').forEach(function(c){if(c.checked)s+=+c.dataset.w;});
if(s>100)s=100;document.getElementById('fit_s').textContent=s+' / 100';
document.getElementById('fit_mk').style.left=s+'%';
var b=document.getElementById('fit_badge'),m=document.getElementById('fit_msg');
if(s>=60){b.textContent='PRÊT';b.style.background='#dcfce7';b.style.color='#166534';m.textContent="Un ERP métier vous ferait gagner du temps et de la marge dès maintenant.";}
else if(s>=30){b.textContent='À ÉTUDIER';b.style.background='#fef3c7';b.style.color='#92400e';m.textContent="Certains irritants justifient déjà un ERP ; cadrons le besoin ensemble.";}
else{b.textContent='PAS ENCORE';b.style.background='#e2e8f0';b.style.color='#334155';m.textContent="Vos process tiennent ; revoyez la question à la prochaine étape de croissance.";}}
box.addEventListener('change',f);f();
})();</script>"""

BTOOL = {
    "roi-erp": ROI, "erp-as400": TCO, "cout-de-revient": COST,
    "calculer-le-prix-de-revient-en-boulangerie": BAKE, "calcul-stock-de-securite": SAFETY,
    "calcul-stock-moyen": AVG, "reapprovisionnement-stocks": REORDER,
    "fifo-fefo-lifo": ROT, "dlc-ddm-dluo": EXPIRY, "erp-pme": FIT,
}


# ---- Bespoke inter-H2 visuals (matched to each article's real H2 keywords) ----
def _fig(title, sub, inner):
    import html as _h
    return (f'<figure class="hha-fig" role="group">'
            f'<figcaption class="hha-fig-cap">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/></svg>'
            f'<span>{_h.escape(title)}</span></figcaption>'
            f'<p class="hha-fig-sub">{_h.escape(sub)}</p><div class="hha-fig-body">{inner}</div></figure>')


def _bars(rows):
    return '<div class="hha-bars">' + "".join(
        f'<div class="hha-bar-row"><span class="lab">{l}</span><div class="hha-bar-track">'
        f'<div class="hha-bar-fill" style="width:{p}%"></div></div><b class="hha-bar-val">{p}%</b></div>'
        for l, p in rows) + '</div>'


def _flow(items):
    arrow = ('<span class="hha-flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/>'
             '<polyline points="12 5 19 12 12 19"/></svg></span>')
    return '<div class="hha-flow">' + arrow.join(
        f'<div class="hha-flow-step"><b>{a}</b><span>{b}</span></div>' for a, b in items) + '</div>'


def _kpis(items):
    return '<div class="hha-kpis">' + "".join(
        f'<div class="hha-kpi"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in items) + '</div>'


BVIS = {
    "roi-erp": [
        (["bénéfices", "benefices", "mesurés", "mesures", "concrètement"],
         _fig("Bénéfices mesurables d'un ERP", "Les 4 postes où le ROI se matérialise le plus vite.",
              _kpis([("−35%", "temps de saisie"), ("+12%", "marge nette"), ("×3", "vitesse d'inventaire"), ("−50%", "ruptures")]))),
        (["coût total", "cout total", "tco"],
         _fig("Composantes du coût total (TCO)", "Au-delà de la licence : intégration, formation, maintenance.",
              _bars([("Abonnement / licence", 45), ("Intégration & reprise", 25), ("Formation", 15), ("Maintenance", 15)]))),
    ],
    "erp-as400": [
        (["étapes pour migrer", "etapes pour migrer", "migrer"],
         _fig("Migration AS/400 → SaaS", "Un parcours en 5 étapes pour sécuriser la bascule.",
              _flow([("1", "Audit existant"), ("2", "Reprise données"), ("3", "Paramétrage"), ("4", "Tests"), ("5", "Go-live")]))),
        (["avantages", "long terme"],
         _fig("Ce que gagne une PME en passant au SaaS", "Comparatif synthétique AS/400 vs ERP cloud.",
              _bars([("Accessibilité & mobilité", 92), ("Mises à jour automatiques", 88), ("Coût maîtrisé (OpEx)", 80), ("Sécurité & sauvegardes", 85)]))),
    ],
    "cout-de-revient": [
        (["formule"],
         _fig("La formule du coût de revient", "Coût d'achat + coûts de production + coûts de distribution.",
              _flow([("Achat", "matières"), ("+ Production", "MO, énergie"), ("+ Distribution", "logistique"), ("= Revient", "total")]))),
        (["maximiser", "bénéfice", "benefice"],
         _fig("Du coût de revient au prix de vente", "Décomposition type d'un prix agroalimentaire.",
              _bars([("Matières premières", 55), ("Main d'œuvre", 22), ("Charges & freinte", 13), ("Marge nette", 10)]))),
    ],
    "calculer-le-prix-de-revient-en-boulangerie": [
        (["étude de cas", "etude de cas", "exemple"],
         _fig("Cas type : une baguette tradition", "Où part le prix d'une pièce vendue 1,20 €.",
              _bars([("Farine & ingrédients", 38), ("Énergie (four)", 17), ("Main d'œuvre", 30), ("Marge", 15)]))),
        (["optimiser"],
         _fig("3 leviers pour protéger sa marge", "Les postes à piloter en priorité.",
              _kpis([("−10%", "pertes / freinte"), ("+1 tournée", "four optimisé"), ("Prix", "réindexé matières")]))),
    ],
    "calcul-stock-de-securite": [
        (["importance"],
         _fig("Le stock de sécurité, amortisseur de l'aléa", "Il absorbe les pics de demande et les retards fournisseurs.",
              _flow([("Demande", "qui varie"), ("+ Délai", "qui glisse"), ("= Risque", "de rupture"), ("Tampon", "= stock sécu")]))),
        (["facteurs", "influençant", "influencant"],
         _fig("Ce qui fait monter le stock de sécurité", "Plus ces facteurs sont élevés, plus le tampon doit l'être.",
              _bars([("Variabilité de la demande", 80), ("Variabilité du délai", 70), ("Niveau de service visé", 90), ("Criticité produit", 60)]))),
    ],
    "calcul-stock-moyen": [
        (["formule"],
         _fig("La formule du stock moyen", "(Stock initial + stock final) ÷ 2, puis rotation.",
              _flow([("Stock initial", "début"), ("+ Stock final", "fin"), ("÷ 2", "= moyen"), ("Conso ÷ moyen", "= rotation")]))),
        (["automatiser", "outils"],
         _fig("Ce qu'un ERP automatise", "Du relevé manuel au pilotage en temps réel.",
              _kpis([("Temps réel", "valorisation"), ("Auto", "alertes seuil"), ("0", "ressaisie")]))),
    ],
    "reapprovisionnement-stocks": [
        (["méthodes", "methodes"],
         _fig("Les méthodes de réapprovisionnement", "Choisir selon la régularité de la demande.",
              _bars([("Point de commande", 85), ("Recomplètement périodique", 70), ("Calendaire (date fixe)", 55), ("À la commande (juste-à-temps)", 65)]))),
        (["calculer", "optimal"],
         _fig("Du besoin au lot optimal", "Point de commande + quantité économique (Wilson).",
              _flow([("Demande/jour", "× délai"), ("+ Stock sécu", "= seuil"), ("EOQ", "quantité éco"), ("Commande", "auto")]))),
    ],
    "fifo-fefo-lifo": [
        (["différences", "differences"],
         _fig("FIFO, FEFO, LIFO : quelle logique ?", "Le critère de sortie change tout en agroalimentaire.",
              _bars([("FEFO — par DLC (agro frais)", 95), ("FIFO — par ancienneté", 75), ("LIFO — comptable seulement", 30)]))),
        (["cas d'usage", "cas d usage", "agroalimentaire"],
         _fig("Quel produit, quelle méthode ?", "Recommandation par typologie de produit.",
              _flow([("Frais DLC", "→ FEFO"), ("Épicerie DDM", "→ FIFO"), ("Matière stockable", "→ FIFO")]))),
    ],
    "dlc-ddm-dluo": [
        (["stratégiques", "strategiques", "professionnels"],
         _fig("Pourquoi piloter ses dates", "L'impact direct sur la casse et la conformité.",
              _kpis([("−50%", "casse / gaspillage"), ("100%", "conformité retrait"), ("FEFO", "appliqué auto")]))),
        (["hello harel", "piloter"],
         _fig("Le pilotage DLC/DDM dans l'ERP", "De l'alerte au retrait, sans tableur.",
              _flow([("Saisie lot", "+ date"), ("Alerte", "J-x"), ("Démarque", "ou retrait"), ("Traçabilité", "complète")]))),
    ],
    "erp-pme": [
        (["pourquoi"],
         _fig("Pourquoi une PME passe à l'ERP", "Les irritants qui déclenchent le projet.",
              _bars([("Fin des ressaisies Excel", 88), ("Visibilité marges temps réel", 82), ("Traçabilité & conformité", 78), ("Croissance / multi-site", 70)]))),
        (["cloud ou on-premise", "cloud ou on premise"],
         _fig("Cloud (SaaS) ou On-Premise ?", "Pour une PME, le SaaS l'emporte le plus souvent.",
              _bars([("ERP SaaS (cloud)", 90), ("ERP On-Premise", 50)]))),
    ],
}


def has(slug):
    return slug in BTOOL or slug in BVIS


def tool(slug):
    return BTOOL.get(slug)


def visuals_for(slug):
    return BVIS.get(slug, [])
