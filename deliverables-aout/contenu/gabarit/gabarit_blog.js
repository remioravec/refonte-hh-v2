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