/**
 * Pont de consentement CookieYes -> marqueur Oravec (Le Fil).
 * CookieYes n'emet aucun signal Google Consent Mode sur ce site : sans ce pont, le marqueur
 * reste en mode exempte et ne rapporte jamais la provenance d'un lead.
 * Ce qu'il fait, et rien d'autre :
 *   - lit le cookie « cookieyes-consent » deja pose par CookieYes (aucun cookie nouveau) ;
 *   - avant que le marqueur ne demarre, pose window.filConsentement = {mesure, regies} ;
 *   - relaie chaque reponse du visiteur, par l'evenement « cookieyes_consent_update » ET par
 *     une relecture du cookie toutes les 1,5 s pendant 10 minutes (meme veille que celle que
 *     le marqueur applique aux autres bandeaux : l'evenement seul s'est revele intermittent).
 * Correspondance : categorie analytics -> mesure, categorie advertisement -> regies.
 * Tant que le visiteur n'a pas repondu, rien n'est pose : le marqueur reste en mode exempte.
 * Ne touche ni GA4, ni le formulaire, ni CookieYes lui-meme. Desactiver ce snippet suffit a le retirer.
 */
add_action( 'wp_head', 'hh_pont_consentement_fil', 1 );

function hh_pont_consentement_fil() {
    if ( is_admin() || is_feed() ) { return; }
    ?>
<script>
(function(){
  var dernier = null;
  function etat(){
    var m=/(?:^|;\s*)cookieyes-consent=([^;]+)/.exec(document.cookie);
    if(!m) return null;
    var p={};
    decodeURIComponent(m[1]).split(',').forEach(function(x){
      var i=x.indexOf(':'); if(i>0){ p[x.slice(0,i).trim()]=x.slice(i+1).trim(); }
    });
    if(p.action!=='yes' && p.consent!=='yes' && p.consent!=='no') return null;
    var mesure=p.analytics==='yes';
    return { mesure:mesure, regies:mesure && p.advertisement==='yes' };
  }
  function relayer(){
    var c=etat(); if(!c) return;
    var cle=(c.mesure?'m':'')+(c.regies?'r':'');
    if(cle===dernier) return;
    dernier=cle;
    window.filConsentement=c;
    try{
      if(window.fil && typeof window.fil.consentement==='function'){ window.fil.consentement(c); return; }
      document.dispatchEvent(new CustomEvent('fil:consentement',{detail:c}));
    }catch(err){}
  }
  relayer();
  document.addEventListener('cookieyes_consent_update', relayer);
  document.addEventListener('DOMContentLoaded', relayer);
  var tours=0;
  var veille=setInterval(function(){ relayer(); if(++tours>400) clearInterval(veille); },1500);
})();
</script>
    <?php
}
