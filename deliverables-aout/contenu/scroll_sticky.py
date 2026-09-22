#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La section fonctionnalites en defilement colle (« scrollytelling »).

Au lieu de cinq onglets qu'il faut penser a cliquer, la colonne de gauche
defile avec le texte et la colonne de droite reste collee : l'ecran du
logiciel change tout seul au fur et a mesure de la descente.

Le contenu n'est PAS reecrit : titres, chapos, puces, liens de maillage et
ecrans sont extraits du module a onglets deja en place sur la page. Seule
la mise en scene change.

Trois garde-fous, parce qu'un effet colle casse vite :
  · sur telephone, pas de colle du tout — chaque ecran suit son texte. Deux
    colonnes collees dans 390 px ne tiennent pas, et un panneau colle qui
    recouvre le texte est pire que pas d'effet ;
  · sans JavaScript, les cinq ecrans restent empiles et lisibles ;
  · si le visiteur demande moins de mouvement, le fondu disparait et
    l'ecran change d'un coup.

MAQUETTE. Ce module ne s'ecrit nulle part : il rend un artefact.

Usage :  python3 scroll_sticky.py            (torrefacteur)
         python3 scroll_sticky.py brasseur
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w        # noqa: E402
import maquette_agro as M    # noqa: E402  (SVG_FA, convertir)
import contenu_sticky as C   # noqa: E402  (titres, puces, avis reels)

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SITE = "https://www.helloharel.com"

PAGES = {
    "torrefacteur": (10935, "/agroalimentaire/torrefacteur/"),
    "brasseur":     (10896, "/agroalimentaire/brasseur/"),
    "chocolatier":  (10894, "/agroalimentaire/chocolatier/"),
}

POLICE = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
          'family=Inter:wght@300;400;500;600;700;800;900&display=swap">')

REPOS = """<style id="hh-repos">
#hh-page .scroll-reveal,#hh-page .metier-slide{opacity:1 !important;transform:none !important}
body{margin:0;background:#fff}
</style>"""


# ═══════════════════════════════════════════════════ lecture du module actuel
def bloc_ferme(t, i, tag="div"):
    """Fin de la balise ouverte en i, en comptant les ouvertures."""
    n, k = 0, i
    for m in re.finditer(r"<%s\b[^>]*>|</%s\s*>" % (tag, tag), t[i:]):
        k = i + m.end()
        n += 1 if not m.group(0).startswith("</") else -1
        if n == 0:
            return k
    raise SystemExit("ARRET — <%s> non referme" % tag)


def extraire_sticky(contenu):
    """Meme sortie, depuis le module de defilement deja pose.

    Une fois la section convertie, il n'y a plus d'onglets a lire : les
    ecrans vivent dans .sy-ecrans et le lien de maillage dans .sy-t.
    """
    i = contenu.find('<section class="features-section"')
    j = contenu.find("</section>", i) + len("</section>")
    sec = contenu[i:j]
    ent = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="sy )', sec, re.S)
    if not ent:
        raise SystemExit("ARRET — en-tete introuvable dans le module de defilement")
    ecrans = []
    for m in re.finditer(r'<li data-actif="[01]" aria-hidden="(?:true|false)">', sec):
        fin = bloc_ferme(sec, m.start(), "li")
        ecrans.append(sec[m.end():fin - len("</li>")])
    liens = re.findall(r'(<a class="hhf-lien".*?</a>)', sec, re.S)
    if not ecrans:
        raise SystemExit("ARRET — aucun ecran dans le module de defilement")
    return ent.group(0), ecrans, liens


def extraire(contenu):
    """Rend (entete, [(court, txt, ecran)]) depuis le module a onglets."""
    i = contenu.find('<section class="features-section"')
    if i < 0:
        raise SystemExit("ARRET — section des fonctionnalites introuvable")
    j = contenu.find("</section>", i) + len("</section>")
    sec = contenu[i:j]

    ent = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="hhf">)',
                    sec, re.S)
    if not ent:
        raise SystemExit("ARRET — en-tete de section introuvable")

    courts = re.findall(r'<label for="hhf-o\d+"><b>\d+</b>([^<]+)</label>', sec)
    blocs = []
    for m in re.finditer(r'<div class="hhf-row">', sec):
        row = sec[m.start():bloc_ferme(sec, m.start())]
        t = re.search(r'<div class="hhf-txt">', row)
        s = re.search(r'<div class="hhf-shot">', row)
        if not t or not s:
            raise SystemExit("ARRET — panneau incomplet")
        txt = row[t.start():bloc_ferme(row, t.start())]
        shot = row[s.start():bloc_ferme(row, s.start())]
        # le chapo « 01 Fonctionnalite » appartient a l'ancien gabarit
        txt = re.sub(r'<p class="hhf-num">.*?</p>', "", txt, flags=re.S)
        inner = txt[txt.find(">") + 1:txt.rfind("</div>")]
        ecran = shot[shot.find(">") + 1:shot.rfind("</div>")]
        blocs.append((inner, ecran))
    if len(blocs) != len(courts) or not blocs:
        raise SystemExit("ARRET — %d panneaux pour %d onglets" % (len(blocs), len(courts)))
    return ent.group(0), [(courts[k], a, b) for k, (a, b) in enumerate(blocs)]


# ═══════════════════════════════════════════════════════════════ le module
CSS = """<style id="hh-scrollytelling">
#hh-page .sy,.sy{--haut:104px;position:relative;
 margin:clamp(1.5rem,4vw,3.25rem) auto 0 !important;
 padding:clamp(1.25rem,3vw,2.5rem) clamp(0px,2vw,1.75rem) !important;
 max-width:1140px}
#hh-page .sy-grille,.sy-grille{display:grid !important;
 grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);
 gap:clamp(1.25rem,2.4vw,2.25rem) !important;align-items:start !important;
 margin:0 !important}

/* ── colonne de gauche : les etapes, qui defilent normalement ───────────── */
#hh-page .sy-pas,.sy-pas{margin:0 !important;padding:0 !important;list-style:none !important}
#hh-page .sy-pas>li,.sy-pas>li{margin:0 !important;padding:0 !important;
 min-height:70vh;display:flex !important;flex-direction:column !important;
 justify-content:center !important}
#hh-page .sy-pas>li:last-child,.sy-pas>li:last-child{min-height:50vh}
#hh-page .sy-t,.sy-t{opacity:.34;transition:opacity .45s ease}
#hh-page .sy-pas>li[data-actif="1"] .sy-t,.sy-pas>li[data-actif="1"] .sy-t{opacity:1}
#hh-page .sy-n,.sy-n{display:inline-flex !important;align-items:center;gap:.6rem;
 font-size:.74rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
 color:#0369A1;margin:0 0 1rem !important}
#hh-page .sy-n b,.sy-n b{display:grid;place-items:center;width:28px;height:28px;
 border-radius:9px;background:#E0F2FE;color:#075985;font-size:.8rem;letter-spacing:0}
#hh-page .sy-t h2,.sy-t h2{font-size:clamp(1.4rem,2.7vw,1.95rem) !important;line-height:1.16;
 color:#0f172a;font-weight:800;letter-spacing:-.025em;margin:0 0 .9rem !important}
#hh-page .sy-t>p,.sy-t>p{color:#475569;font-size:1.04rem;line-height:1.7;
 margin:0 0 1.35rem !important;max-width:46ch}
#hh-page .sy-t .hhf-pts,.sy-t .hhf-pts{list-style:none;padding:0;margin:0 !important;
 display:flex;flex-direction:column;gap:.72rem}
#hh-page .sy-t .hhf-pts li,.sy-t .hhf-pts li{display:flex;gap:.65rem;align-items:flex-start;
 color:#334155;font-size:.97rem;line-height:1.5;margin:0 !important}
#hh-page .sy-t .hhf-pts li svg,.sy-t .hhf-pts li svg{width:19px;height:19px;flex:0 0 19px;
 margin-top:2px;color:#16DB7F}
#hh-page .sy-t .hhf-lien,.sy-t .hhf-lien{margin-top:1.35rem !important}
/* L'avis : une vraie citation Google, posee sous les puces de la
   fonctionnalite dont elle parle. Les etapes sans avis correspondant n'en
   portent pas — on n'en fabrique pas pour remplir. */
#hh-page .sy-avis,.sy-avis{display:flex !important;gap:.85rem !important;
 align-items:flex-start !important;margin:1.5rem 0 0 !important;
 padding:.95rem 1.1rem !important;background:#F0F9FF !important;
 border:1px solid #E0F2FE !important;border-left:3px solid #00B1F5 !important;
 border-radius:0 12px 12px 0 !important;max-width:46ch}
#hh-page .sy-avis i,.sy-avis i{display:grid !important;place-items:center !important;
 width:36px !important;height:36px !important;flex:0 0 36px !important;
 border-radius:50% !important;background:#0369A1 !important;color:#fff !important;
 font-style:normal !important;font-weight:700 !important;font-size:.78rem !important}
#hh-page .sy-avis p,.sy-avis p{margin:0 !important;font-size:.9rem !important;
 line-height:1.5 !important;color:#0f172a !important;font-style:italic !important}
#hh-page .sy-avis b,.sy-avis b{display:block !important;margin-top:.3rem !important;
 font-style:normal !important;font-size:.76rem !important;font-weight:600 !important;
 color:#64748b !important}
#hh-page .sy-avis svg,.sy-avis svg{width:12px;height:12px;color:#F59E0B;
 vertical-align:-1px;margin-right:1px}

/* ── colonne de droite : l'ecran, colle ─────────────────────────────────── */
#hh-page .sy-colle,.sy-colle{position:sticky;top:var(--haut);
 height:calc(100vh - var(--haut) - 5rem);display:grid !important;align-content:center;
 justify-items:center}
#hh-page .sy-ecrans,.sy-ecrans{display:grid !important;margin:0 !important;padding:0 !important;
 list-style:none !important;width:100% !important}
/* Les cinq ecrans occupent LA MEME cellule : aucun saut de mise en page
   quand on passe de l'un a l'autre, quelle que soit leur hauteur. */
#hh-page .sy-ecrans>li,.sy-ecrans>li{grid-area:1/1;margin:0 !important;padding:0 !important;
 opacity:0;transform:translateY(14px) scale(.985);pointer-events:none;
 transition:opacity .5s ease,transform .5s ease}
#hh-page .sy-ecrans>li[data-actif="1"],.sy-ecrans>li[data-actif="1"]{opacity:1;
 transform:none;pointer-events:auto}
#hh-page .sy-ecrans>li,.sy-ecrans>li{overflow:hidden}
#hh-page .sy-ecrans .ui,.sy-ecrans .ui{width:720px !important;
 transform:scale(var(--k,1)) translateX(var(--dx,0px));
 transform-origin:top left;transition:transform .3s ease}


/* -- telephone : un carrousel de cartes, l'ecran d'abord ----------------- */
/* Ce qu'on vient voir sur un telephone, c'est le tableau de bord. Il passe
   donc AU-DESSUS du texte, en pleine largeur de carte, entier — plus de
   glissement horizontal pour en voir la moitie. Les quatre puces longues
   cedent la place a trois pastilles : meme information, moins de lecture.
   Le DOM ne change pas : ni H2 ni avis dupliques, seule la mise en page. */
@media (max-width:900px){
 #hh-page .sy-grille,.sy-grille{grid-template-columns:minmax(0,1fr) !important}
 #hh-page .sy-colle,.sy-colle{display:none !important}

 /* le rail deborde le conteneur : les cartes prennent toute la largeur
    de l'ecran, et la suivante depasse juste assez pour se laisser deviner */
 #hh-page .sy-pas,.sy-pas{display:flex !important;gap:.85rem !important;
  overflow-x:auto !important;-webkit-overflow-scrolling:touch;
  scroll-snap-type:x mandatory;scrollbar-width:none;
  width:100vw !important;margin-left:calc(50% - 50vw) !important;
  margin-right:calc(50% - 50vw) !important;
  padding:.4rem 8vw 1rem !important;min-width:0 !important}
 #hh-page .sy-pas::-webkit-scrollbar,.sy-pas::-webkit-scrollbar{display:none}
 #hh-page .sy-pas>li,.sy-pas>li{flex:0 0 84vw !important;max-width:420px !important;
  min-width:0 !important;scroll-snap-align:center;min-height:0 !important;
  margin:0 !important;padding:0 !important;background:#fff !important;
  border:1px solid #e2e8f0 !important;border-radius:20px !important;
  overflow:hidden !important;
  box-shadow:0 14px 32px -24px rgba(15,23,42,.6) !important}
 #hh-page .sy-t,.sy-t{opacity:1 !important;display:flex !important;
  flex-direction:column !important;padding:0 1.05rem 1.15rem !important}

 /* le tableau de bord, en tete de carte et en entier */
 #hh-page .sy-mob,.sy-mob{display:block !important;order:-1 !important;position:relative;
  margin:0 -1.05rem 1rem !important;padding:12px !important;
  box-sizing:border-box !important;
  background:#F8FAFC !important;border-bottom:1px solid #e2e8f0 !important}
 #hh-page .sy-cadre,.sy-cadre{overflow:hidden !important;contain:paint}
 /* 480px est la largeur plancher : en dessous, une colonne du tableau se
    replie. On garde donc cette mise en page et on la reduit — jamais on ne
    la comprime. */
 #hh-page .sy-mob .ui,.sy-mob .ui{width:480px !important;min-width:480px !important;
  transform:scale(var(--km,1)) !important;transform-origin:top left !important}
 /* agrandi : on rend sa taille reelle a l'ecran, et on le fait glisser */
 #hh-page .sy-mob[data-grand="1"] .sy-cadre,.sy-mob[data-grand="1"] .sy-cadre{
  overflow-x:auto !important;-webkit-overflow-scrolling:touch;
  height:auto !important;max-height:62vh}
 #hh-page .sy-mob[data-grand="1"] .ui,.sy-mob[data-grand="1"] .ui{
  transform:none !important}
 #hh-page .sy-loupe,.sy-loupe{position:absolute !important;right:14px !important;
  bottom:14px !important;z-index:2;display:inline-flex !important;
  align-items:center !important;gap:.32rem !important;
  padding:.42rem .74rem !important;margin:0 !important;
  border:1px solid #CBD5E1 !important;border-radius:999px !important;
  background:rgba(255,255,255,.95) !important;color:#0C4A6E !important;
  font-size:.74rem !important;font-weight:700 !important;line-height:1 !important;
  cursor:pointer !important;box-shadow:0 4px 12px -6px rgba(15,23,42,.5) !important}
 #hh-page .sy-loupe svg,.sy-loupe svg{width:14px;height:14px;flex:0 0 14px}

 #hh-page .sy-n,.sy-n{margin:.95rem 0 .5rem !important}
 #hh-page .sy-t h2,.sy-t h2{font-size:1.16rem !important;line-height:1.3 !important;
  margin:0 !important}
 #hh-page .sy-t>p,.sy-t>p{font-size:.95rem !important;margin:.6rem 0 0 !important}
 #hh-page .sy-t .hhf-pts,.sy-t .hhf-pts{display:none !important}
 #hh-page .sy-ch,.sy-ch{display:flex !important}
 #hh-page .sy-t .hhf-lien,.sy-t .hhf-lien{margin-top:1rem !important}
 #hh-page .sy-avis,.sy-avis{margin-top:1rem !important}
 #hh-page .sy-pts,.sy-pts{display:flex !important}
}
#hh-page .sy-mob,.sy-mob{display:none}

/* pastilles courtes : telephone seulement */
#hh-page .sy-ch,.sy-ch{display:none;flex-wrap:wrap;gap:.4rem;list-style:none;
 padding:0 !important;margin:.75rem 0 0 !important}
#hh-page .sy-ch li,.sy-ch li{display:inline-flex !important;align-items:center;
 gap:.34rem;margin:0 !important;padding:.34rem .62rem !important;
 border-radius:999px !important;background:#F0F9FF !important;
 border:1px solid #BAE6FD !important;color:#075985 !important;
 font-size:.78rem !important;font-weight:600 !important;line-height:1.2 !important}
#hh-page .sy-ch li svg,.sy-ch li svg{width:13px;height:13px;flex:0 0 13px;
 color:#0369A1 !important}

/* reperes du carrousel */
#hh-page .sy-pts,.sy-pts{display:none;justify-content:center;gap:.4rem;
 margin:.1rem 0 0 !important}
#hh-page .sy-pts i,.sy-pts i{width:7px;height:7px;border-radius:50%;
 background:#CBD5E1;transition:width .25s ease,background .25s ease}
#hh-page .sy-pts i[data-actif="1"],.sy-pts i[data-actif="1"]{width:20px;
 border-radius:999px;background:#0369A1}

/* ── sans JavaScript, tout reste lisible ────────────────────────────────── */
#hh-page .sy:not([data-js="1"]) .sy-ecrans>li,.sy:not([data-js="1"]) .sy-ecrans>li{
 opacity:1;transform:none;position:relative;grid-area:auto;margin-bottom:1.5rem !important}
#hh-page .sy:not([data-js="1"]) .sy-colle,.sy:not([data-js="1"]) .sy-colle{
 position:static;height:auto}
#hh-page .sy:not([data-js="1"]) .sy-t,.sy:not([data-js="1"]) .sy-t{opacity:1}

@media (prefers-reduced-motion:reduce){
 #hh-page .sy-ecrans>li,.sy-ecrans>li,#hh-page .sy-t,.sy-t{transition:none !important}
 #hh-page .sy-ecrans>li,.sy-ecrans>li{transform:none !important}
}
</style>"""

JS = """<script id="hh-scrollytelling-js">
(function(){
 var sy=document.querySelector(".sy"); if(!sy) return;
 var pas=Array.prototype.slice.call(sy.querySelectorAll(".sy-pas>li"));
 var ecr=Array.prototype.slice.call(sy.querySelectorAll(".sy-ecrans>li"));
 if(!pas.length||pas.length!==ecr.length) return;
 sy.setAttribute("data-js","1");
 var courant=-1;
 function poser(n){
  if(n===courant) return;
  courant=n;
  pas.forEach(function(p,i){p.setAttribute("data-actif",i===n?"1":"0")});
  ecr.forEach(function(e,i){
   e.setAttribute("data-actif",i===n?"1":"0");
   e.setAttribute("aria-hidden",i===n?"false":"true");
  });
 }
 poser(0);
 /* L'ecran le plus charge depasse la hauteur du panneau colle. On mesure sa
    hauteur naturelle et on le reduit juste ce qu'il faut — jamais au-dela
    de 1, on n'agrandit pas une capture. */
 var LARGE=720;   /* la largeur ou les tableaux de l'ecran tiennent sans se replier */
 function ajuster(){
  var colle=sy.querySelector(".sy-colle"); if(!colle) return;
  var dh=colle.clientHeight, dw=colle.clientWidth;
  if(!dh||!dw) return;
  ecr.forEach(function(li){
   var ui=li.querySelector(".ui"); if(!ui) return;
   var h=ui.offsetHeight; if(!h) return;
   var k=Math.min(1, dw/LARGE, (dh-12)/h);
   ui.style.setProperty("--k", k.toFixed(4));
   /* recentrage : l'origine est en haut a gauche, on rattrape a la main */
   ui.style.setProperty("--dx", ((dw-LARGE*k)/2/k).toFixed(1)+"px");
   li.style.height = Math.round(h*k)+"px";
  });
 }
 /* Sur telephone, le meme ecran remplit la largeur de la carte. On le
    reduit depuis sa largeur de reference (480px) jusqu'a la carte : la
    mise en page interne ne se replie pas, et le tableau de bord se voit
    en entier, sans glissement horizontal. */
 var MOB=480;
 var mobs=Array.prototype.slice.call(sy.querySelectorAll(".sy-mob"));
 function ajusterMob(){
  var hauteurs=[];
  mobs.forEach(function(m){
   var cad=m.querySelector(".sy-cadre"), ui=m.querySelector(".ui");
   if(!cad||!ui) return;
   if(!m.offsetParent){ui.style.removeProperty("--km");cad.style.height="";return}
   if(m.getAttribute("data-grand")==="1"){cad.style.height="";return}
   var w=cad.clientWidth; if(w<=0) return;
   var k=Math.min(1,w/MOB);
   ui.style.setProperty("--km",k.toFixed(4));
   /* offsetHeight : la hauteur de mise en page, avant la reduction */
   hauteurs.push(Math.round(ui.offsetHeight*k));
  });
  /* Toutes les cartes montrent leur ecran sur la meme hauteur : le texte
     demarre au meme endroit d'une carte a l'autre, et le carrousel ne
     sautille pas quand on le fait defiler. */
  if(!hauteurs.length) return;
  var H=Math.max.apply(null,hauteurs);
  mobs.forEach(function(m){
   var cad=m.querySelector(".sy-cadre"); if(!cad) return;
   if(m.getAttribute("data-grand")==="1"){cad.style.height="";return}
   cad.style.height=H+"px";
  });
 }
 /* « Agrandir » : l'ecran reprend sa taille reelle et se fait glisser. On
    ne peut pas tout rendre lisible dans 330px de large — on rend donc la
    vue d'ensemble par defaut, et le detail a la demande. */
 Array.prototype.forEach.call(sy.querySelectorAll(".sy-loupe"),function(b){
  b.addEventListener("click",function(){
   var m=b.parentNode, grand=m.getAttribute("data-grand")==="1";
   m.setAttribute("data-grand",grand?"0":"1");
   b.setAttribute("aria-expanded",grand?"false":"true");
   var t=b.querySelector("span"); if(t) t.textContent=grand?"Agrandir":"Réduire";
   ajusterMob();
  });
 });
 /* Les reperes suivent la carte la plus proche du centre du carrousel. */
 var rail=sy.querySelector(".sy-pas"), pts=sy.querySelector(".sy-pts");
 function reperer(){
  if(!rail||!pts||!pts.offsetParent) return;
  var mid=rail.getBoundingClientRect().left+rail.clientWidth/2, best=0, d=1e9;
  pas.forEach(function(p,i){
   var r=p.getBoundingClientRect(), e=Math.abs((r.left+r.right)/2-mid);
   if(e<d){d=e;best=i}
  });
  Array.prototype.forEach.call(pts.children,function(c,i){
   c.setAttribute("data-actif",i===best?"1":"0");
  });
 }
 if(rail) rail.addEventListener("scroll",function(){
  window.requestAnimationFrame(reperer);
 },{passive:true});
 function tout(){ajuster();ajusterMob();reperer()}
 tout();
 window.addEventListener("resize",tout);
 /* Les captures se mettent en place apres les polices : on remesure. */
 window.addEventListener("load",tout);
 if(document.fonts&&document.fonts.ready) document.fonts.ready.then(tout);
 /* Le pas actif est celui dont le milieu est le plus proche du milieu de
    l'ecran : c'est ce que l'oeil lit, et ca ne depend pas d'un seuil. */
 var attente=false;
 function mesurer(){
  attente=false;
  var mid=window.innerHeight/2, best=0, d=1e9;
  pas.forEach(function(p,i){
   var r=p.getBoundingClientRect();
   var e=Math.abs((r.top+r.bottom)/2-mid);
   if(e<d){d=e;best=i}
  });
  poser(best);
 }
 window.addEventListener("scroll",function(){
  if(attente) return; attente=true; window.requestAnimationFrame(mesurer);
 },{passive:true});
 window.addEventListener("resize",mesurer);
 mesurer();
})();
</script>"""


ETOILE = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M12 2l2.9 6.26 6.85.78-5.09 4.64 1.4 6.74L12 17.1l-6.06 3.32 1.4-6.74'
          'L2.25 9.04l6.85-.78z"/></svg>')

LOUPE = ('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
         '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" '
         'd="M21 21l-4.3-4.3M11 19a8 8 0 100-16 8 8 0 000 16zM11 8v6M8 11h6"/></svg>')

COCHE = ('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
         '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" '
         'd="M5 13l4 4L19 7"/></svg>')


def bloc_avis(cle):
    """Un avis Google reel, ou rien. On n'en fabrique pas pour remplir."""
    if not cle or cle not in C.AVIS:
        return ""
    nom, ini, texte = C.AVIS[cle]
    return ('<div class="sy-avis"><i aria-hidden="true">%s</i>'
            '<p>« %s »<b>%s%s · avis Google</b></p></div>'
            % (ini, texte, ETOILE * 5, nom))


def section(entete, ecrans, liens, contenu):
    """contenu : [(titre H2, [puces], cle d'avis)] — un par ecran."""
    if len(ecrans) != len(contenu):
        raise SystemExit("ARRET — %d ecrans pour %d blocs de contenu"
                         % (len(ecrans), len(contenu)))
    pas, col = "", ""
    for k, (ecran, (h2, puces, avis, courtes)) in enumerate(zip(ecrans, contenu), 1):
        pts = "".join("<li>%s%s</li>" % (COCHE, x) for x in puces)
        # Sur telephone, les puces longues cedent la place aux pastilles.
        pst = "".join("<li>%s%s</li>" % (COCHE, x) for x in courtes)
        # les liens de maillage sont distribues dans l'ordre, un par etape
        lien = liens[k - 1] if k - 1 < len(liens) else ""
        txt = ('<h2>%s</h2><ul class="hhf-pts">%s</ul>'
               '<ul class="sy-ch">%s</ul>%s%s'
               % (h2, pts, pst, lien, bloc_avis(avis)))
        pas += ('<li data-actif="%s"><div class="sy-t">'
                '<p class="sy-n"><b>%02d</b>Fonctionnalité</p>%s'
                '<div class="sy-mob"><div class="sy-cadre">%s</div>'
                '<button class="sy-loupe" type="button" aria-expanded="false">'
                '%s<span>Agrandir</span></button></div></div></li>'
                % ("1" if k == 1 else "0", k, txt, ecran, LOUPE))
        col += ('<li data-actif="%s" aria-hidden="%s">%s</li>'
                % ("1" if k == 1 else "0", "false" if k == 1 else "true", ecran))
    ecrans, pas_ = col, pas
    pas = pas_
    # Les reperes du carrousel telephone : un par carte, caches au bureau.
    points = ('<div class="sy-pts" aria-hidden="true">%s</div>'
              % "".join('<i data-actif="%s"></i>' % ("1" if n == 0 else "0")
                        for n in range(len(contenu))))
    return (CSS
            + '<section class="features-section" id="fonctionnalites"><div class="container">'
            + entete
            + '<div class="sy hhf"><div class="sy-grille">'
              '<ul class="sy-pas">%s</ul>'
              '<div class="sy-colle"><ul class="sy-ecrans">%s</ul></div>'
              '</div>%s</div>'
              '</div></section>' % (pas, ecrans, points)
            + JS)


def main():
    cle = sys.argv[1] if len(sys.argv) > 1 else "torrefacteur"
    if cle not in PAGES:
        raise SystemExit("ARRET — page inconnue : %s" % cle)
    page, url = PAGES[cle]
    c = w.get_raw("pages", page)["content"]["raw"]
    print("page %d (%s) : %d octets" % (page, url, len(c)))

    if 'class="sy-ecrans"' in c:
        entete, ecrans, liens = extraire_sticky(c)
    else:
        entete, blocs = extraire(c)
        ecrans = [b[2] for b in blocs]
        liens = [m for b in blocs
                 for m in re.findall(r'(<a class="hhf-lien".*?</a>)', b[1], re.S)]
    print("extrait : %d ecrans, %d lien(s) de maillage" % (len(ecrans), len(liens)))

    i = c.find('<section class="features-section"')
    j = c.find("</section>", i) + len("</section>")
    c = c[:i] + section(entete, ecrans, liens, C.CONTENU[cle]) + c[j:]

    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    n = 0
    for u in sorted(urls):
        d = M.convertir(u)
        if d:
            c = c.replace(u, d)
            n += 1
    rel = set(re.findall(r'(?:src|data-src)="(/wp-content/[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    for u in sorted(rel):
        d = M.convertir(SITE + u)
        if d:
            c = c.replace('"%s"' % u, '"%s"' % d)
            n += 1
    print("images integrees : %d" % n)

    c, faits = M.remplacer_video(c)
    for f in faits:
        print("  ", f)

    k = 0
    for cls, svg in M.SVG_FA.items():
        for b in ('<i class="%s"></i>' % cls, '<i class="%s"/>' % cls):
            k += c.count(b)
            c = c.replace(b, svg)
    c = re.sub(r'<link[^>]+cdnjs\.cloudflare\.com[^>]*>', "", c)
    print("icones Font Awesome remplacees : %d" % k)

    html = ('<!doctype html><html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Fonctionnalités en défilement — %s</title>' % cle.capitalize()
            + POLICE + REPOS + '</head><body>' + c + '</body></html>')
    sortie = os.path.join(S, "sticky-%s.html" % cle)
    open(sortie, "w", encoding="utf-8").write(html)
    print("\necrit : %s (%d ko)" % (sortie, len(html) // 1024))

    pb = []
    for m in re.finditer(r'<(img|source)[^>]+src="((?:https?:)?/[^"]*)"', html):
        pb.append("image non integree : " + m.group(2)[:60])
    if re.search(r"<iframe", html):
        pb.append("iframe : bloquee dans un artefact")
    for t in ("section", "div", "ul", "li"):
        o, f = len(re.findall(r"<%s[\s>]" % t, html)), len(re.findall(r"</%s\s*>" % t, html))
        if o != f:
            pb.append("%s : %d ouvertes, %d fermees" % (t, o, f))
    if html.count("<h1") != 1:
        pb.append("il faut un seul H1, il y en a %d" % html.count("<h1"))
    if html.count('class="sy-pas"') != 1 or html.count('class="sy-ecrans"') != 1:
        pb.append("le module n'est pas pose une seule fois")
    # sans l'ancetre .hhf, la feuille des ecrans ne s'applique pas
    if 'class="sy hhf"' not in html:
        pb.append("le conteneur a perdu la classe .hhf : les ecrans sortiraient nus")
    print("controles :", "tout est vert" if not pb else pb)


if __name__ == "__main__":
    main()
