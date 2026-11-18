/**
 * Attribution premiere partie des formulaires (remplace le tracker Lovable).
 * Remplit les cinq champs caches que la chaine serveur transmet au CRM :
 * te_source, te_medium, te_campaign, te_landing, workspace_id.
 * Difference avec l'ancien tracker : AUCUN envoi navigateur. Pas de sendBeacon,
 * pas d'appel cross-domaine, donc pas le defaut CORS de l'incident du 23/10.
 * Le CRM continue d'etre alimente par le relai serveur du snippet 6, lui seul.
 */
add_action( 'wp_footer', 'hh_attribution_premiere_partie', 5 );

function hh_attribution_premiere_partie() {
    if ( is_admin() || is_feed() ) { return; }
    // Le relai serveur (snippet 6) remet de toute facon l'espace de travail s'il arrive vide.
    $ws = defined( 'HH_CRM_WORKSPACE' ) ? esc_js( HH_CRM_WORKSPACE ) : '';
    ?>
<script>
(function(){
  var CLE='hh_attribution', WS='<?php echo $ws; ?>';
  function premierContact(){
    try{ var g=localStorage.getItem(CLE); if(g){ return JSON.parse(g); } }catch(e){}
    var p=new URLSearchParams(location.search), r=document.referrer||'';
    var d={source:'direct',medium:'(none)',campaign:'(none)',landing:location.origin+location.pathname};
    if(p.get('gclid')){ d.landing=location.origin+location.pathname+'?gclid='+p.get('gclid'); }
    if(p.get('utm_source')){
      d.source=p.get('utm_source'); d.medium=p.get('utm_medium')||'cpc'; d.campaign=p.get('utm_campaign')||'(none)';
    } else if(p.get('gclid')){
      d.source='google'; d.medium='cpc';
    } else if(r && r.indexOf(location.hostname)<0){
      var h=''; try{ h=new URL(r).hostname; }catch(e){ h=''; }
      if(/(^|\.)google\./.test(h)){ d.source='google'; d.medium='organic'; }
      else if(/(^|\.)(bing|yahoo|duckduckgo|ecosia|qwant)\./.test(h)){ d.source=h.replace(/^www\./,''); d.medium='organic'; }
      else if(/(^|\.)(facebook|linkedin|twitter|x|instagram|youtube)\./.test(h)){ d.source=h.replace(/^www\./,''); d.medium='social'; }
      else if(h){ d.source=h.replace(/^www\./,''); d.medium='referral'; }
    }
    try{ localStorage.setItem(CLE, JSON.stringify(d)); }catch(e){}
    return d;
  }
  var d=premierContact();
  var champs={te_source:d.source,te_medium:d.medium,te_campaign:d.campaign,te_landing:d.landing,workspace_id:WS};
  function remplir(){
    var forms=document.querySelectorAll('form');
    for(var i=0;i<forms.length;i++){
      for(var k in champs){
        if(!champs[k]) continue;
        var el=forms[i].querySelector('#form-field-'+k)||forms[i].querySelector('input[name="'+k+'"]');
        if(el && el.value!==champs[k]){ el.value=champs[k]; el.setAttribute('value',champs[k]); }
      }
    }
  }
  remplir();
  if(window.MutationObserver && document.body){
    var t=null;
    new MutationObserver(function(){ clearTimeout(t); t=setTimeout(remplir,120); })
      .observe(document.body,{childList:true,subtree:true});
  }
})();
</script>
    <?php
}
