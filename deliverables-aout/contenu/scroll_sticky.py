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
#hh-page .sy-t h3,.sy-t h3{font-size:clamp(1.45rem,2.9vw,2.1rem) !important;line-height:1.14;
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

/* ── le rail de progression ─────────────────────────────────────────────── */
#hh-page .sy-rail,.sy-rail{position:absolute;left:-14px;top:0;bottom:0;width:3px;
 background:#e2e8f0;border-radius:2px}
#hh-page .sy-jauge,.sy-jauge{position:absolute;inset:0 0 auto 0;height:0;background:#00B1F5;
 border-radius:2px;transition:height .25s ease}
@media (max-width:1240px){#hh-page .sy-rail,.sy-rail{display:none}}

/* ── telephone : on retire la colle, chaque ecran suit son texte ────────── */
@media (max-width:900px){
 #hh-page .sy-grille,.sy-grille{grid-template-columns:minmax(0,1fr) !important}
 #hh-page .sy-pas,.sy-pas,#hh-page .sy-pas>li,.sy-pas>li{min-width:0 !important}
 #hh-page .sy-mob,.sy-mob{overflow-x:auto !important;-webkit-overflow-scrolling:touch}
 #hh-page .sy-mob .ui,.sy-mob .ui{min-width:520px !important}
 #hh-page .sy-colle,.sy-colle{display:none !important}
 #hh-page .sy-pas>li,.sy-pas>li{min-height:0 !important;display:block !important;
  padding-bottom:3rem !important}
 #hh-page .sy-t,.sy-t{opacity:1 !important}
 #hh-page .sy-mob,.sy-mob{display:block !important;margin-top:1.75rem !important}
}
#hh-page .sy-mob,.sy-mob{display:none}

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

JS = """<script>
(function(){
 var sy=document.querySelector(".sy"); if(!sy) return;
 var pas=Array.prototype.slice.call(sy.querySelectorAll(".sy-pas>li"));
 var ecr=Array.prototype.slice.call(sy.querySelectorAll(".sy-ecrans>li"));
 var jauge=sy.querySelector(".sy-jauge");
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
  if(jauge) jauge.style.height=((n+1)/pas.length*100)+"%";
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
 ajuster();
 window.addEventListener("resize",ajuster);
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


def section(entete, blocs):
    pas, ecrans = "", ""
    for k, (court, txt, ecran) in enumerate(blocs, 1):
        pas += ('<li data-actif="%s"><div class="sy-t">'
                '<p class="sy-n"><b>%02d</b>%s</p>%s'
                '<div class="sy-mob">%s</div></div></li>'
                % ("1" if k == 1 else "0", k, court, txt, ecran))
        ecrans += ('<li data-actif="%s" aria-hidden="%s">%s</li>'
                   % ("1" if k == 1 else "0", "false" if k == 1 else "true", ecran))
    return (CSS
            + '<section class="features-section" id="fonctionnalites"><div class="container">'
            + entete
            + '<div class="sy hhf"><div class="sy-rail"><i class="sy-jauge"></i></div>'
              '<div class="sy-grille">'
              '<ul class="sy-pas">%s</ul>'
              '<div class="sy-colle"><ul class="sy-ecrans">%s</ul></div>'
              '</div></div>'
              '</div></section>' % (pas, ecrans)
            + JS)


def main():
    cle = sys.argv[1] if len(sys.argv) > 1 else "torrefacteur"
    if cle not in PAGES:
        raise SystemExit("ARRET — page inconnue : %s" % cle)
    page, url = PAGES[cle]
    c = w.get_raw("pages", page)["content"]["raw"]
    print("page %d (%s) : %d octets" % (page, url, len(c)))

    entete, blocs = extraire(c)
    print("extrait : %d fonctionnalites — %s" % (len(blocs), ", ".join(b[0] for b in blocs)))

    i = c.find('<section class="features-section"')
    j = c.find("</section>", i) + len("</section>")
    c = c[:i] + section(entete, blocs) + c[j:]

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
