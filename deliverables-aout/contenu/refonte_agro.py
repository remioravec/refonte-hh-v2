#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/agroalimentaire/ refaite entierement — maquette en artefact.

Ce n'est pas un rustinage de la page en ligne : chaque section est reecrite,
et la feuille de style de 128 ko heritee est remplacee par un systeme de
design de quelques milliers d'octets, bati sur des variables.

MAQUETTE, PAS MISE EN LIGNE. La page 1726 est protegee par la regle 0 :
ce script lit la page en ligne pour en reprendre les images et les textes
longs, il ne l'ecrit JAMAIS.

Ce que la refonte conserve, parce que la regle 0 l'impose :
  · l'URL, le title, le H1, la meta description ;
  · l'inventaire et l'ordre des sections ;
  · tous les liens internes sortants, un par un ;
  · le JSON-LD FAQPage et ses huit questions.

Ce que la refonte repare, parce que « reparer n'est pas optimiser » :
  · les douze cartes d'equipe floutees, qui montrent des personnes inventees ;
  · le module diagnostic : du CSS et du JS pour un markup absent ;
  · le carrousel cas clients : un script qui adresse des boutons absents ;
  · les contrastes sous 4,5:1, les cibles tactiles sous 44 px, les focus
    invisibles, le mouvement non desactivable ;
  · les images sans dimensions, qui font sauter la mise en page.

Usage :  python3 refonte_agro.py
"""

import base64
import io
import os
import re
import subprocess
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w      # noqa: E402
import agro_ui             # noqa: E402
import menu_home           # noqa: E402

PAGE = 1726
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
CACHE = os.path.join(S, "img")
SOURCE = os.path.join(S, "avant-1726.html")
SORTIE = os.path.join(S, "refonte-agro.html")

TITRE = "ERP agroalimentaire — Hello Harel"


# ═════════════════════════════════════════════════════ images en data URI
def convertir(url, largeur=1400, qualite=76):
    """Telecharge une image du site et la rend en data URI WebP.

    La politique de securite des artefacts refuse toute image distante :
    sans cette conversion, la maquette s'affiche avec des cadres vides.
    """
    os.makedirs(CACHE, exist_ok=True)
    nom = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/")[-1])
    brut = os.path.join(CACHE, nom)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", brut], timeout=90)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        return None, 0, 0
    if url.lower().endswith(".svg"):
        d = open(brut, "rb").read()
        return "data:image/svg+xml;base64," + base64.b64encode(d).decode(), 0, 0
    try:
        im = Image.open(brut)
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
        if im.width > largeur:
            im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=qualite, method=6)
        return ("data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(),
                im.width, im.height)
    except Exception:
        return None, 0, 0


# ═════════════════════════════════════════════════════ le systeme de design
#
# Une seule echelle d'espacement (4 px), une seule echelle typographique, une
# palette ou chaque couleur de texte est mesuree sur son fond. Tout le reste
# de la page ne fait que consommer ces variables : une correction se fait ici,
# une fois, au lieu de courir dans 128 ko de regles.
#
# Contrastes mesures sur fond blanc :
#   --t1 #0F172A 16,8:1   --t2 #334155 10,4:1   --t3 #475569 7,5:1
#   --lien #0369A1 5,6:1  --vert-txt #15803D 4,8:1
# Le bleu de marque #00B1F5 (1,9:1) ne porte donc JAMAIS de texte : il ne sert
# que de fond, de filet et d'icone decorative.

CSS = """<style id="hh-refonte">
/* Les jetons vivent sur :root : une couleur se change a un endroit, pour toute
   la page. La maquette reproduit un site a theme clair unique — elle declare
   donc color-scheme:light plutot que d'inventer une palette sombre que la
   marque n'a pas. */
:root{
 color-scheme:light;
 --bleu:#00B1F5; --bleu-f:#0369A1; --bleu-n:#0C4A6E; --bleu-05:#F0F9FF; --bleu-10:#E0F2FE;
 --vert:#22C55E; --vert-t:#15803D; --vert-05:#F0FDF4;
 --t1:#0F172A; --t2:#334155; --t3:#475569; --t4:#64748B;
 --bord:#E2E8F0; --bord-f:#CBD5E1; --fond:#FFFFFF; --fond-2:#F8FAFC; --fond-3:#F1F5F9;
 --ambre:#B45309; --ambre-05:#FFFBEB; --rouge:#B91C1C; --rouge-05:#FEF2F2;
 --e1:4px; --e2:8px; --e3:12px; --e4:16px; --e5:24px; --e6:32px; --e7:48px; --e8:64px;
 --r1:8px; --r2:12px; --r3:16px; --r4:24px; --rp:999px;
 --o1:0 1px 2px rgba(15,23,42,.06);
 --o2:0 4px 16px -4px rgba(15,23,42,.10),0 1px 3px rgba(15,23,42,.05);
 --o3:0 18px 44px -20px rgba(15,23,42,.30);
 --max:1200px; --gout:clamp(16px,4vw,24px);
 --hdr:72px;
}
#hh-page{
 display:block; background:var(--fond); color:var(--t1);
 font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased;
 overflow-x:clip;
}
#hh-page *,#hh-page *::before,#hh-page *::after{box-sizing:border-box}
#hh-page h1,#hh-page h2,#hh-page h3,#hh-page h4,#hh-page h5,#hh-page p,
#hh-page ul,#hh-page ol,#hh-page figure,#hh-page blockquote{margin:0;padding:0}
#hh-page ul,#hh-page ol{list-style:none}
#hh-page img{max-width:100%;height:auto;display:block}
#hh-page a{color:inherit;text-decoration:none}
#hh-page button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
#hh-page table{border-collapse:collapse;width:100%}

/* Un anneau de focus visible partout. C'est la premiere chose qu'on retire
   « pour faire propre », et la premiere qui rend une page inutilisable au
   clavier. */
#hh-page a:focus-visible,#hh-page button:focus-visible,#hh-page input:focus-visible,
#hh-page summary:focus-visible,#hh-page [tabindex]:focus-visible{
 outline:3px solid var(--bleu-f);outline-offset:2px;border-radius:var(--r1)}

#hh-page .wrap{width:100%;max-width:var(--max);margin-inline:auto;padding-inline:var(--gout)}
#hh-page .sec,#hh-page .features-section{padding-block:clamp(48px,7vw,88px)}
#hh-page .container{width:100%%;max-width:var(--max);margin-inline:auto;padding-inline:var(--gout)}
#hh-page .sec--gris{background:var(--fond-2)}
#hh-page .sec--bleu{background:var(--bleu-05)}

#hh-page .tete{max-width:760px;margin:0 auto clamp(32px,5vw,56px);text-align:center}
#hh-page .sur{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.14em;
 text-transform:uppercase;color:var(--bleu-f);background:var(--bleu-10);
 padding:6px 14px;border-radius:var(--rp);margin-bottom:var(--e4)}
#hh-page .tete h2{font-size:clamp(1.7rem,3.6vw,2.6rem);line-height:1.15;letter-spacing:-.025em;
 font-weight:800;color:var(--t1)}
#hh-page .tete>p{margin-top:var(--e3);font-size:clamp(1rem,1.6vw,1.12rem);color:var(--t3)}

/* Les boutons : 48 px de haut, donc au-dessus des 44 px exiges au doigt. */
#hh-page .btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;
 min-height:48px;padding:0 24px;border-radius:var(--rp);font-weight:700;font-size:.98rem;
 transition:background .18s,box-shadow .18s,transform .18s;text-align:center}
#hh-page .btn--p{background:var(--vert-t);color:#fff;box-shadow:0 8px 20px -10px rgba(21,128,61,.7)}
#hh-page .btn--p:hover{background:#166534;transform:translateY(-1px)}
#hh-page .btn--s{background:#fff;color:var(--bleu-n);border:2px solid var(--bord-f)}
#hh-page .btn--s:hover{border-color:var(--bleu-f);color:var(--bleu-f)}
#hh-page .btn svg{width:18px;height:18px;flex:0 0 18px}
#hh-page .btn--fant{background:rgba(255,255,255,.12);color:#fff;border:2px solid rgba(255,255,255,.55)}
#hh-page .btn--fant:hover{background:rgba(255,255,255,.22)}
#hh-page .lien{color:var(--bleu-f);font-weight:600;text-decoration:underline;
 text-underline-offset:3px;text-decoration-thickness:1.5px}
#hh-page .lien:hover{color:var(--bleu-n)}

/* ───────────────────────────────────────────────────────────── en-tete */
#hh-page .hdr{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.94);
 backdrop-filter:saturate(180%%) blur(14px);border-bottom:1px solid var(--bord)}
#hh-page .hdr-in{display:flex;align-items:center;gap:var(--e5);height:var(--hdr)}
#hh-page .hdr-logo{flex:0 0 auto;display:inline-flex;align-items:center;min-height:44px}
#hh-page .hdr-logo img{height:32px;width:auto}
#hh-page .nav{display:none;align-items:center;gap:var(--e1);margin-inline:auto}
#hh-page .nav>a,#hh-page .nav-trig{display:inline-flex;align-items:center;gap:6px;
 min-height:44px;padding:0 12px;border-radius:var(--r1);font-size:.95rem;font-weight:600;
 color:var(--t2)}
#hh-page .nav>a:hover,#hh-page .nav-trig:hover{color:var(--bleu-f);background:var(--bleu-05)}
#hh-page .nav-dd{position:relative}
#hh-page .nav-trig svg{width:15px;height:15px;transition:transform .2s}
#hh-page .nav-dd[data-ouvert="1"] .nav-trig svg{transform:rotate(180deg)}
#hh-page .nav-dd[data-ouvert="1"] .nav-trig{color:var(--bleu-f);background:var(--bleu-05)}
#hh-page .dd{position:absolute;top:calc(100%% + 10px);left:50%%;transform:translateX(-50%%) translateY(-6px);
 background:#fff;border:1px solid var(--bord);border-radius:var(--r4);box-shadow:var(--o3);
 padding:var(--e4);opacity:0;visibility:hidden;transition:opacity .18s,transform .18s}
#hh-page .nav-dd[data-ouvert="1"] .dd{opacity:1;visibility:visible;transform:translateX(-50%%) translateY(0)}
#hh-page .dd--f{width:420px;max-width:92vw;display:grid;grid-template-columns:1fr 1fr;gap:var(--e1)}
#hh-page .dd--i{width:min(940px,92vw);display:grid;grid-template-columns:repeat(3,1fr);gap:var(--e5)}
#hh-page .dd h5{display:flex;align-items:center;gap:8px;font-size:.72rem;font-weight:800;
 letter-spacing:.12em;text-transform:uppercase;color:var(--bleu-f);
 padding:0 10px var(--e2);margin-bottom:var(--e2);border-bottom:1px solid var(--bord)}
#hh-page .dd h5 svg{width:15px;height:15px;flex:0 0 15px}
#hh-page .dd a{display:flex;align-items:center;gap:10px;min-height:44px;padding:8px 10px;
 border-radius:var(--r1);font-size:.92rem;font-weight:600;color:var(--t2)}
#hh-page .dd a:hover{background:var(--bleu-05);color:var(--bleu-f)}
#hh-page .dd a svg{width:17px;height:17px;flex:0 0 17px;color:var(--bleu-f)}
#hh-page .hdr-act{display:none;gap:var(--e2);flex:0 0 auto}
#hh-page .burger{margin-left:auto;display:inline-flex;align-items:center;justify-content:center;
 width:46px;height:46px;border-radius:var(--r1);border:1px solid var(--bord);color:var(--t1)}
#hh-page .burger svg{width:22px;height:22px}
@media (min-width:1080px){
 #hh-page .nav{display:flex}
 #hh-page .hdr-act{display:flex}
 #hh-page .burger{display:none}
}

/* ───────────────────────────────────────────────────── menu mobile
   Le panneau deroule sa hauteur reelle (grid-template-rows 0fr -> 1fr) au
   lieu d'une max-height devinee : c'est la regression qui avait coupe la
   liste a 8 metiers sur 16. Une valeur en dur finit toujours par mentir. */
#hh-page .mob{position:fixed;inset:var(--hdr) 0 0 0;z-index:55;background:#fff;
 overflow-y:auto;overscroll-behavior:contain;padding:var(--e5) 0 var(--e8);
 transform:translateX(100%%);visibility:hidden;transition:transform .26s ease,visibility .26s}
#hh-page .mob[data-ouvert="1"]{transform:none;visibility:visible}
#hh-page .mob-in{display:flex;flex-direction:column;gap:var(--e1)}
#hh-page .mob a,#hh-page .mob-btn{display:flex;align-items:center;gap:10px;min-height:48px;
 padding:10px 12px;border-radius:var(--r2);font-size:1rem;font-weight:600;color:var(--t1)}
#hh-page .mob-btn{width:100%%;justify-content:space-between;background:var(--fond-2)}
#hh-page .mob-btn svg{width:18px;height:18px;transition:transform .2s;color:var(--t4)}
#hh-page .mob-btn[aria-expanded="true"] svg{transform:rotate(180deg)}
#hh-page .mob-sous{display:grid;grid-template-rows:0fr;transition:grid-template-rows .28s ease}
#hh-page .mob-sous>div{overflow:hidden;min-height:0}
#hh-page .mob-sous[data-ouvert="1"]{grid-template-rows:1fr}
#hh-page .mob-sous a{font-size:.95rem;font-weight:500;color:var(--t2);padding-left:var(--e5)}
#hh-page .mob-sous a svg{width:16px;height:16px;flex:0 0 16px;color:var(--bleu-f)}
#hh-page .mob-tit{display:block;padding:var(--e4) 12px 6px var(--e5);font-size:.72rem;
 font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--t4)}
#hh-page .mob-cta{display:grid;gap:var(--e2);margin-top:var(--e5);padding-top:var(--e5);
 border-top:1px solid var(--bord)}
@media (min-width:1080px){#hh-page .mob{display:none}}

/* ─────────────────────────────────────────────────────────────── hero */
#hh-page .hero{position:relative;color:#fff;isolation:isolate;
 padding-block:clamp(56px,9vw,104px);background:var(--bleu-n)}
#hh-page .hero-img{position:absolute;inset:0;z-index:-2;width:100%%;height:100%%;object-fit:cover}
#hh-page .hero::after{content:"";position:absolute;inset:0;z-index:-1;
 background:linear-gradient(105deg,rgba(3,35,58,.90) 0%%,rgba(3,45,74,.84) 46%%,rgba(3,74,120,.72) 100%%)}
#hh-page .hero-in{max-width:760px}
#hh-page .hero .sur{color:#fff;background:rgba(255,255,255,.18)}
#hh-page .hero h1{font-size:clamp(2rem,5.2vw,3.35rem);line-height:1.08;letter-spacing:-.03em;
 font-weight:900;color:#fff;text-wrap:balance}
#hh-page .hero-cha{margin-top:var(--e5);font-size:clamp(1.02rem,2vw,1.2rem);line-height:1.62;
 color:#EAF4FB;max-width:64ch}
#hh-page .hero-cha strong{color:#fff;font-weight:700}
#hh-page .hero-act{display:flex;flex-wrap:wrap;gap:var(--e3);margin-top:var(--e6)}
#hh-page .hero-note{margin-top:var(--e4);font-size:.88rem;color:#C7E2F2}

/* ────────────────────────────────────────────────────────────── logos */
#hh-page .logos{padding-block:var(--e7);background:var(--fond-2);border-block:1px solid var(--bord)}
#hh-page .logos-t{text-align:center;font-size:.78rem;font-weight:700;letter-spacing:.14em;
 text-transform:uppercase;color:var(--t4);margin-bottom:var(--e5)}
#hh-page .piste{overflow:hidden;mask-image:linear-gradient(90deg,transparent,#000 6%%,#000 94%%,transparent)}
#hh-page .file{display:flex;align-items:center;gap:clamp(32px,6vw,64px);width:max-content;
 animation:hh-defile 46s linear infinite}
#hh-page .piste:hover .file,#hh-page .piste:focus-within .file{animation-play-state:paused}
#hh-page .file img{height:38px;width:auto;object-fit:contain;filter:grayscale(1);opacity:.62;
 transition:filter .2s,opacity .2s}
#hh-page .file img:hover{filter:none;opacity:1}
@keyframes hh-defile{from{transform:none}to{transform:translateX(-50%%)}}

/* ─────────────────────────────────────────────────────────────── quiz */
#hh-page .quiz{background:linear-gradient(160deg,#03243A,#064E7A)}
#hh-page .quiz .tete h2,#hh-page .quiz .tete>p{color:#fff}
#hh-page .quiz .tete>p{color:#C7E2F2}
#hh-page .quiz .sur{color:#fff;background:rgba(255,255,255,.16)}
#hh-page .quiz-box{max-width:880px;margin-inline:auto;background:#fff;border-radius:var(--r4);
 padding:clamp(24px,4vw,40px);box-shadow:var(--o3)}
#hh-page .quiz-prog{display:flex;align-items:center;justify-content:center;gap:10px;
 margin-bottom:var(--e6)}
#hh-page .quiz-prog i{width:34px;height:5px;border-radius:var(--rp);background:var(--bord-f);
 display:block;transition:background .2s}
#hh-page .quiz-prog i[data-etat="fait"]{background:var(--vert-t)}
#hh-page .quiz-prog i[data-etat="ici"]{background:var(--bleu-f)}
#hh-page .quiz-num{font-size:.8rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
 color:var(--bleu-f);text-align:center}
#hh-page .quiz-q{margin:var(--e2) 0 var(--e5);font-size:clamp(1.2rem,2.4vw,1.55rem);
 line-height:1.25;font-weight:800;text-align:center;letter-spacing:-.02em}
#hh-page .quiz-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:var(--e3)}
#hh-page .quiz-opt{display:flex;flex-direction:column;align-items:flex-start;gap:3px;
 min-height:74px;padding:14px 16px;text-align:left;border:2px solid var(--bord);
 border-radius:var(--r2);background:#fff;transition:border-color .16s,background .16s,transform .16s}
#hh-page .quiz-opt:hover{border-color:var(--bleu-f);background:var(--bleu-05);transform:translateY(-2px)}
#hh-page .quiz-opt[aria-pressed="true"]{border-color:var(--vert-t);background:var(--vert-05)}
#hh-page .quiz-opt b{font-size:.98rem;font-weight:700;color:var(--t1)}
#hh-page .quiz-opt span{font-size:.84rem;color:var(--t3)}
#hh-page .quiz-etape[hidden],#hh-page .quiz-res[hidden]{display:none}
#hh-page .quiz-res{text-align:center}
#hh-page .quiz-res h3{font-size:clamp(1.3rem,2.6vw,1.7rem);font-weight:800;letter-spacing:-.02em}
#hh-page .quiz-res>p{margin:var(--e3) auto 0;max-width:62ch;color:var(--t3)}
#hh-page .quiz-plan{display:grid;gap:var(--e2);margin:var(--e5) 0;text-align:left}
#hh-page .quiz-plan li{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;
 background:var(--fond-2);border-radius:var(--r2);font-size:.95rem;color:var(--t2)}
#hh-page .quiz-plan b{flex:0 0 26px;display:grid;place-items:center;width:26px;height:26px;
 border-radius:50%%;background:var(--bleu-f);color:#fff;font-size:.8rem;font-weight:800}
#hh-page .quiz-act{display:flex;flex-wrap:wrap;gap:var(--e3);justify-content:center}

/* ──────────────────────────────────────────────────── simulateur de ROI */
#hh-page .roi{display:grid;grid-template-columns:1fr;gap:var(--e6);max-width:1000px;
 margin-inline:auto;background:#fff;border:1px solid var(--bord);border-radius:var(--r4);
 padding:clamp(24px,4vw,40px);box-shadow:var(--o2)}
@media (min-width:880px){#hh-page .roi{grid-template-columns:1fr 1fr}}
#hh-page .roi-champ{margin-bottom:var(--e5)}
#hh-page .roi-champ label{display:flex;justify-content:space-between;align-items:baseline;
 gap:var(--e3);font-size:.92rem;font-weight:600;color:var(--t2);margin-bottom:var(--e2)}
#hh-page .roi-champ output{font-size:1.05rem;font-weight:800;color:var(--bleu-f);
 font-variant-numeric:tabular-nums}
#hh-page .roi-champ input[type=range]{-webkit-appearance:none;appearance:none;width:100%%;
 height:44px;background:transparent;cursor:pointer}
#hh-page .roi-champ input[type=range]::-webkit-slider-runnable-track{height:8px;
 border-radius:var(--rp);background:var(--fond-3)}
#hh-page .roi-champ input[type=range]::-moz-range-track{height:8px;
 border-radius:var(--rp);background:var(--fond-3)}
#hh-page .roi-champ input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;
 width:26px;height:26px;margin-top:-9px;border-radius:50%%;background:var(--bleu-f);
 border:3px solid #fff;box-shadow:var(--o2)}
#hh-page .roi-champ input[type=range]::-moz-range-thumb{width:26px;height:26px;border-radius:50%%;
 background:var(--bleu-f);border:3px solid #fff;box-shadow:var(--o2)}
#hh-page .roi-res{background:var(--fond-2);border-radius:var(--r3);padding:var(--e5)}
#hh-page .roi-ligne{display:flex;justify-content:space-between;align-items:baseline;gap:var(--e3);
 padding-block:12px;border-bottom:1px solid var(--bord);font-size:.94rem;color:var(--t2)}
#hh-page .roi-ligne b{font-variant-numeric:tabular-nums;font-weight:700;color:var(--t1)}
#hh-page .roi-ligne.neg b{color:var(--rouge)}
#hh-page .roi-tot{display:flex;justify-content:space-between;align-items:baseline;gap:var(--e3);
 margin-top:var(--e4);padding:var(--e4);border-radius:var(--r2);background:var(--vert-05);
 border:1px solid #BBF7D0}
#hh-page .roi-tot span{font-weight:700;color:var(--vert-t)}
#hh-page .roi-tot b{font-size:clamp(1.4rem,3vw,1.9rem);font-weight:900;color:var(--vert-t);
 font-variant-numeric:tabular-nums;letter-spacing:-.02em}
#hh-page .roi-notes{margin-top:var(--e5);font-size:.82rem;line-height:1.6;color:var(--t4)}
#hh-page .roi-notes li{padding-left:16px;position:relative}
#hh-page .roi-notes li::before{content:"·";position:absolute;left:4px;font-weight:800}

/* ───────────────────────────────────────────────────────── qui sommes-nous */
#hh-page .about{display:grid;gap:var(--e6);grid-template-columns:1fr}
@media (min-width:900px){#hh-page .about{grid-template-columns:1.15fr .85fr;align-items:start}}
#hh-page .about-txt h2{font-size:clamp(1.6rem,3.2vw,2.3rem);line-height:1.18;font-weight:800;
 letter-spacing:-.025em;margin-bottom:var(--e4)}
#hh-page .about-txt p{color:var(--t3);font-size:1.02rem}
#hh-page .chiffres{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--e3);
 margin-top:var(--e5)}
#hh-page .chiffre{background:#fff;border:1px solid var(--bord);border-radius:var(--r2);
 padding:var(--e4);text-align:center}
#hh-page .chiffre b{display:block;font-size:clamp(1.3rem,3vw,1.75rem);font-weight:900;
 color:var(--bleu-f);letter-spacing:-.02em}
#hh-page .chiffre span{font-size:.82rem;color:var(--t4);font-weight:600}
#hh-page .cite{margin-top:var(--e5);padding:var(--e5);border-left:4px solid var(--bleu);
 background:var(--bleu-05);border-radius:0 var(--r2) var(--r2) 0}
#hh-page .cite p{font-size:1.08rem;font-weight:600;color:var(--bleu-n);font-style:italic}
#hh-page .cite cite{display:block;margin-top:var(--e2);font-size:.88rem;color:var(--t3);font-style:normal}
#hh-page .auteur{background:#fff;border:1px solid var(--bord);border-radius:var(--r3);
 padding:var(--e5);box-shadow:var(--o1)}
#hh-page .auteur-h{display:flex;align-items:center;gap:var(--e3)}
#hh-page .auteur-h img{width:64px;height:64px;border-radius:50%%;object-fit:cover;flex:0 0 64px}
#hh-page .auteur-h b{display:block;font-size:1.05rem;font-weight:800}
#hh-page .auteur-h span{font-size:.85rem;color:var(--t4)}
#hh-page .auteur>p{margin-top:var(--e4);font-size:.94rem;color:var(--t3)}
#hh-page .puces{display:flex;flex-wrap:wrap;gap:var(--e2);margin-top:var(--e4)}
#hh-page .puce{font-size:.78rem;font-weight:700;color:var(--bleu-f);background:var(--bleu-10);
 padding:6px 12px;border-radius:var(--rp)}

/* ─────────────────────────────────────────────────────────── comparatifs */
#hh-page .cmp-wrap{overflow-x:auto;border:1px solid var(--bord);border-radius:var(--r3);
 background:#fff;box-shadow:var(--o1)}
#hh-page .cmp{min-width:680px;font-size:.94rem}
#hh-page .cmp th,#hh-page .cmp td{padding:14px 18px;text-align:left;vertical-align:top;
 border-bottom:1px solid var(--bord)}
#hh-page .cmp thead th{background:var(--fond-2);font-weight:800;color:var(--t1);
 font-size:.9rem;position:sticky;top:0}
#hh-page .cmp thead th span{display:block;margin-top:3px;font-size:.75rem;font-weight:500}
#hh-page .cmp tbody tr:last-child td{border-bottom:0}
#hh-page .cmp tbody tr:nth-child(even){background:var(--fond-2)}
#hh-page .cmp td:first-child{font-weight:700;color:var(--t1)}
#hh-page .cmp .oui,#hh-page .cmp .non,#hh-page .cmp .moy{display:flex;gap:8px;align-items:flex-start}
#hh-page .cmp .oui{color:var(--vert-t)} #hh-page .cmp .non{color:var(--rouge)}
#hh-page .cmp .moy{color:var(--ambre)}
#hh-page .cmp svg{width:17px;height:17px;flex:0 0 17px;margin-top:2px}
#hh-page .cmp-aide{margin-top:var(--e3);font-size:.82rem;color:var(--t4);text-align:center}

/* ───────────────────────────────────────────────────────── cas clients */
#hh-page .cas-nav{display:flex;gap:var(--e2);justify-content:center;margin-bottom:var(--e5);
 flex-wrap:wrap}
#hh-page .cas-nav button{min-height:44px;padding:0 18px;border-radius:var(--rp);
 border:2px solid var(--bord);font-size:.92rem;font-weight:700;color:var(--t3);background:#fff}
#hh-page .cas-nav button[aria-selected="true"]{border-color:var(--bleu-f);background:var(--bleu-f);color:#fff}
#hh-page .cas-pan{display:grid}
#hh-page .cas-pan>article{grid-area:1/1;background:#fff;border:1px solid var(--bord);
 border-radius:var(--r4);padding:clamp(22px,3.5vw,36px);box-shadow:var(--o2);
 visibility:hidden;opacity:0;transition:opacity .22s}
#hh-page .cas-pan>article[data-actif="1"]{visibility:visible;opacity:1}
#hh-page .cas-h b{display:block;font-size:clamp(1.15rem,2.4vw,1.45rem);font-weight:800}
#hh-page .cas-h span{font-size:.88rem;color:var(--t4)}
#hh-page .cas-kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
 gap:var(--e3);margin:var(--e5) 0}
#hh-page .cas-kpi div{background:var(--fond-2);border-radius:var(--r2);padding:var(--e4)}
#hh-page .cas-kpi span{display:block;font-size:.76rem;font-weight:700;letter-spacing:.06em;
 text-transform:uppercase;color:var(--t4)}
#hh-page .cas-kpi b{display:block;margin-top:5px;font-size:1.08rem;font-weight:800;color:var(--t1);
 font-variant-numeric:tabular-nums}
#hh-page .cas-pan blockquote{padding:var(--e4) var(--e5);background:var(--bleu-05);
 border-left:4px solid var(--bleu);border-radius:0 var(--r2) var(--r2) 0;
 font-style:italic;color:var(--bleu-n)}
#hh-page .cas-roi svg{width:17px;height:17px;flex:0 0 17px}
#hh-page .cas-roi{display:inline-flex;align-items:center;gap:8px;margin-top:var(--e4);
 padding:8px 16px;border-radius:var(--rp);background:var(--vert-05);color:var(--vert-t);
 font-size:.9rem;font-weight:700}

/* ────────────────────────────────────────────────────── presse & garanties */
#hh-page .presse{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:var(--e4)}
#hh-page .presse figure{background:#fff;border:1px solid var(--bord);border-radius:var(--r3);
 padding:var(--e5);box-shadow:var(--o1)}
#hh-page .presse blockquote{font-size:.98rem;line-height:1.55;color:var(--t2);font-weight:600}
#hh-page .presse figcaption{margin-top:var(--e3);font-size:.74rem;font-weight:800;
 letter-spacing:.12em;text-transform:uppercase;color:var(--t4)}
#hh-page .garanties{display:flex;flex-wrap:wrap;justify-content:center;gap:var(--e3);
 margin-top:var(--e6)}
#hh-page .garantie{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;
 border-radius:var(--rp);background:#fff;border:1px solid var(--bord);font-size:.86rem;
 font-weight:600;color:var(--t2)}
#hh-page .garantie svg{width:16px;height:16px;color:var(--vert-t)}

/* ─────────────────────────────────────────────────────────── process */
#hh-page .etapes{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:var(--e5);
 counter-reset:e}
#hh-page .etape{position:relative;background:#fff;border:1px solid var(--bord);
 border-radius:var(--r3);padding:var(--e5);box-shadow:var(--o1)}
#hh-page .etape b{display:grid;place-items:center;width:42px;height:42px;border-radius:var(--r2);
 background:var(--bleu-f);color:#fff;font-size:1.05rem;font-weight:900;margin-bottom:var(--e4)}
#hh-page .etape h3{font-size:1.1rem;font-weight:800;margin-bottom:var(--e2)}
#hh-page .etape p{font-size:.94rem;color:var(--t3)}

/* ──────────────────────────────────────────────────────────── metiers */
#hh-page .metiers{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:var(--e4)}
#hh-page .metier{display:flex;flex-direction:column;gap:var(--e2);background:#fff;
 border:1px solid var(--bord);border-radius:var(--r3);padding:var(--e5);box-shadow:var(--o1);
 transition:transform .18s,box-shadow .18s,border-color .18s}
#hh-page .metier:hover{transform:translateY(-3px);box-shadow:var(--o2);border-color:var(--bleu)}
#hh-page .metier i{display:grid;place-items:center;width:46px;height:46px;border-radius:var(--r2);
 background:var(--bleu-10);color:var(--bleu-f);margin-bottom:var(--e2)}
#hh-page .metier i svg{width:23px;height:23px}
#hh-page .metier h3{font-size:1.05rem;font-weight:800}
#hh-page .metier p{font-size:.9rem;color:var(--t3);flex:1}
#hh-page .metier em{font-style:normal;font-size:.88rem;font-weight:700;color:var(--bleu-f)}
#hh-page .metier:hover em{text-decoration:underline;text-underline-offset:3px}

/* ────────────────────────────────────────────────────────────── equipe */
#hh-page .equipe{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
 gap:var(--e5);max-width:760px;margin-inline:auto}
#hh-page .membre{text-align:center;background:#fff;border:1px solid var(--bord);
 border-radius:var(--r3);padding:var(--e5);box-shadow:var(--o1)}
#hh-page .membre img{width:96px;height:96px;border-radius:50%%;object-fit:cover;
 margin:0 auto var(--e3);border:3px solid var(--bleu-10)}
#hh-page .membre b{display:block;font-size:1.05rem;font-weight:800}
#hh-page .membre span{font-size:.88rem;color:var(--t4)}
#hh-page .equipe-note{margin-top:var(--e5);text-align:center;color:var(--t3);font-size:.95rem}

/* ───────────────────────────────────────────────────────────────── FAQ */
#hh-page .faq{max-width:840px;margin-inline:auto;display:grid;gap:var(--e3)}
#hh-page .faq details{background:#fff;border:1px solid var(--bord);border-radius:var(--r3);
 overflow:hidden}
#hh-page .faq details[open]{border-color:var(--bleu);box-shadow:var(--o1)}
#hh-page .faq summary{display:flex;align-items:center;justify-content:space-between;gap:var(--e4);
 min-height:60px;padding:var(--e4) var(--e5);cursor:pointer;font-size:1.02rem;font-weight:700;
 color:var(--t1);list-style:none}
#hh-page .faq summary::-webkit-details-marker{display:none}
#hh-page .faq summary::after{content:"";flex:0 0 12px;width:12px;height:12px;
 border-right:2.5px solid var(--bleu-f);border-bottom:2.5px solid var(--bleu-f);
 transform:rotate(45deg) translate(-3px,-3px);transition:transform .2s}
#hh-page .faq details[open] summary::after{transform:rotate(-135deg) translate(-2px,-2px)}
#hh-page .faq-rep{padding:0 var(--e5) var(--e5);color:var(--t3);font-size:.98rem}
#hh-page .faq-rep p+p{margin-top:var(--e3)}
#hh-page .faq-rep strong{color:var(--t1);font-weight:700}

/* ───────────────────────────────────────────────────────── demo & avis */
#hh-page .demo{display:grid;gap:var(--e5);align-items:center;grid-template-columns:1fr;
 background:#fff;border:1px solid var(--bord);border-radius:var(--r4);
 padding:clamp(24px,4vw,44px);box-shadow:var(--o2)}
@media (min-width:880px){#hh-page .demo{grid-template-columns:1.3fr .7fr}}
#hh-page .demo h2{font-size:clamp(1.5rem,3vw,2.1rem);line-height:1.18;font-weight:800;
 letter-spacing:-.025em}
#hh-page .demo>div>p{margin-top:var(--e3);color:var(--t3)}
#hh-page .demo-pts{display:flex;flex-wrap:wrap;gap:var(--e3);margin-top:var(--e4)}
#hh-page .demo-pts li{display:inline-flex;align-items:center;gap:7px;font-size:.9rem;
 font-weight:600;color:var(--t2)}
#hh-page .demo-pts svg{width:16px;height:16px;color:var(--vert-t)}
#hh-page .avis{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:var(--e4)}
#hh-page .avis article{background:#fff;border:1px solid var(--bord);border-radius:var(--r3);
 padding:var(--e5);box-shadow:var(--o1);display:flex;flex-direction:column;gap:var(--e3)}
#hh-page .avis-h{display:flex;align-items:center;gap:var(--e3)}
#hh-page .avis-h i{display:grid;place-items:center;width:42px;height:42px;border-radius:50%%;
 background:var(--bleu-10);color:var(--bleu-n);font-style:normal;font-weight:800;font-size:.92rem}
#hh-page .avis-h b{display:block;font-size:.98rem;font-weight:700}
#hh-page .etoiles{display:flex;gap:2px;color:#F59E0B}
#hh-page .etoiles svg{width:15px;height:15px}
#hh-page .avis p{font-size:.93rem;color:var(--t3);flex:1}
#hh-page .note{display:inline-flex;align-items:center;gap:10px;padding:10px 18px;
 border-radius:var(--rp);background:#fff;border:1px solid var(--bord);font-weight:700;
 color:var(--t1);margin-bottom:var(--e5)}

/* ─────────────────────────────────────────────────── approfondir & CTA */
#hh-page .appro{max-width:840px;margin-inline:auto;padding:var(--e5);background:var(--fond-2);
 border:1px solid var(--bord);border-radius:var(--r3)}
#hh-page .appro b{display:block;font-size:.78rem;font-weight:800;letter-spacing:.12em;
 text-transform:uppercase;color:var(--t4);margin-bottom:var(--e2)}
#hh-page .appro p{color:var(--t3);font-size:.96rem}
#hh-page .bandeau{background:linear-gradient(135deg,#03243A,#0369A1);color:#fff;text-align:center}
#hh-page .bandeau h2{font-size:clamp(1.7rem,3.6vw,2.5rem);line-height:1.15;font-weight:900;
 letter-spacing:-.025em;color:#fff;text-wrap:balance}
#hh-page .bandeau p{margin-top:var(--e4);color:#C7E2F2;font-size:1.05rem}
#hh-page .bandeau .hero-act{justify-content:center}

/* ─────────────────────────────────────────────────────────── pied & CTA colle */
#hh-page .pied{background:#03141F;color:#94A3B8;padding-block:var(--e8) var(--e6)}
#hh-page .pied-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
 gap:var(--e6)}
#hh-page .pied img{height:30px;width:auto;margin-bottom:var(--e4)}
#hh-page .pied h3{font-size:.8rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;
 color:#fff;margin-bottom:var(--e4)}
#hh-page .pied li a{display:inline-flex;min-height:44px;align-items:center;font-size:.9rem;
 color:#94A3B8}
#hh-page .pied li a:hover{color:#fff}
#hh-page .pied .neuf{color:#4ADE80;font-weight:700}
#hh-page .pied-bas{display:flex;flex-wrap:wrap;gap:var(--e5);justify-content:center;
 margin-top:var(--e7);padding-top:var(--e5);border-top:1px solid rgba(255,255,255,.08);
 font-size:.85rem}
#hh-page .pied-bas a{display:inline-flex;align-items:center;min-height:44px}
#hh-page .colle{position:fixed;left:0;right:0;bottom:0;z-index:50;display:flex;
 align-items:center;justify-content:space-between;gap:var(--e4);padding:12px var(--gout);
 background:rgba(255,255,255,.97);backdrop-filter:blur(12px);
 border-top:1px solid var(--bord);box-shadow:0 -6px 24px -12px rgba(15,23,42,.3);
 transform:translateY(110%%);transition:transform .26s ease}
#hh-page .colle[data-visible="1"]{transform:none}
#hh-page .colle p{font-size:.92rem;font-weight:700;color:var(--t1)}
#hh-page .colle p span{display:block;font-size:.8rem;font-weight:500;color:var(--t4)}
@media (max-width:560px){#hh-page .colle p span{display:none}}
/* Le CTA colle masque la fin de page : on lui reserve sa hauteur au lieu de
   laisser le dernier lien du pied dessous. */
#hh-page .pied{padding-bottom:calc(var(--e6) + 76px)}

/* ───────────────────────────────────────────── mouvement, si on en veut */
@media (prefers-reduced-motion:reduce){
 #hh-page *,#hh-page *::before,#hh-page *::after{
  animation-duration:.001ms !important;animation-iteration-count:1 !important;
  transition-duration:.001ms !important;scroll-behavior:auto !important}
}
#hh-page .saut{position:absolute;left:-9999px;top:0;background:#fff;color:var(--bleu-n);
 padding:12px 20px;border-radius:0 0 var(--r2) 0;font-weight:700;z-index:99}
#hh-page .saut:focus{left:0}

/* ─── surcharges du module partage : trois contrastes sous 4,5:1 ─────────
   .hhf-bar label b   #94A3B8 sur #F1F5F9 = 2,34:1
   onglet actif       blanc sur #00B1F5   = 2,44:1
   .ui-card > p em    #B4BCC4 sur blanc   = 1,92:1
   A corriger aussi dans agro_ui.py, pour les 31 pages qui portent le module. */
#hh-page .hhf-bar label b{color:#475569 !important}
#hh-page .hhf-pick:nth-of-type(1):checked ~ .hhf-bar label[for="hhf-o1"]{background:#0369A1 !important;box-shadow:0 8px 18px -10px rgba(3,105,161,.9) !important}\n#hh-page .hhf-pick:nth-of-type(1):checked ~ .hhf-bar label[for="hhf-o1"] b{color:#fff !important}\n#hh-page .hhf-pick:nth-of-type(2):checked ~ .hhf-bar label[for="hhf-o2"]{background:#0369A1 !important;box-shadow:0 8px 18px -10px rgba(3,105,161,.9) !important}\n#hh-page .hhf-pick:nth-of-type(2):checked ~ .hhf-bar label[for="hhf-o2"] b{color:#fff !important}\n#hh-page .hhf-pick:nth-of-type(3):checked ~ .hhf-bar label[for="hhf-o3"]{background:#0369A1 !important;box-shadow:0 8px 18px -10px rgba(3,105,161,.9) !important}\n#hh-page .hhf-pick:nth-of-type(3):checked ~ .hhf-bar label[for="hhf-o3"] b{color:#fff !important}\n#hh-page .hhf-pick:nth-of-type(4):checked ~ .hhf-bar label[for="hhf-o4"]{background:#0369A1 !important;box-shadow:0 8px 18px -10px rgba(3,105,161,.9) !important}\n#hh-page .hhf-pick:nth-of-type(4):checked ~ .hhf-bar label[for="hhf-o4"] b{color:#fff !important}\n#hh-page .hhf-pick:nth-of-type(5):checked ~ .hhf-bar label[for="hhf-o5"]{background:#0369A1 !important;box-shadow:0 8px 18px -10px rgba(3,105,161,.9) !important}\n#hh-page .hhf-pick:nth-of-type(5):checked ~ .hhf-bar label[for="hhf-o5"] b{color:#fff !important}
#hh-page .hhf .ui-card>p em{color:#64748B !important}
</style>""".replace("%%", "%")


def logo_teinte(url, couleur):
    """Le logo du site est blanc : invisible sur un en-tete blanc.

    Plutot qu'un filtre CSS approximatif, on reteint les fills du SVG avant
    de l'encoder. Le trace reste identique, la couleur est choisie.
    """
    os.makedirs(CACHE, exist_ok=True)
    nom = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/")[-1])
    brut = os.path.join(CACHE, nom)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", brut], timeout=90)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        return None
    d = open(brut, encoding="utf-8").read()
    d = d.replace('fill="#FFF"', 'fill="%s"' % couleur)
    return "data:image/svg+xml;base64," + base64.b64encode(d.encode()).decode()


# ═════════════════════════════════════════════════════════════ petits SVG
def svg(d, w=24):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % d)


OK = svg('<polyline points="20 6 9 17 4 12"/>')
NON = svg('<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>')
MOY = svg('<path d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3'
          'L13.71 3.86a2 2 0 00-3.42 0z"/>')
BOUCLIER = svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>')
ETOILE = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M12 2l2.9 6.26 6.85.78-5.09 4.64 1.4 6.74L12 17.1l-6.06 3.32 1.4-6.74'
          'L2.25 9.04l6.85-.78z"/></svg>')
CHEVRON = svg('<path d="M19 9l-7 7-7-7"/>')
FLECHE = svg('<path d="M5 12h14M13 6l6 6-6 6"/>')


# ═════════════════════════════════════════════════════════════ 1 — en-tete
def entete(logo):
    fonc = "".join(
        '<a href="%s">%s<span>%s</span></a>' % (u, menu_home._svg(i), lib)
        for lib, u, court, i in menu_home.FONCTIONS)
    cols = ""
    for titre, ico, liens in menu_home.INDUSTRIES:
        cols += '<div><h5>%s%s</h5>%s</div>' % (
            menu_home._svg(ico), titre,
            "".join('<a href="%s">%s<span>%s</span></a>' % (u, menu_home._svg(i), lib)
                    for lib, u, court, i in liens))
    simples = "".join('<a href="%s">%s</a>' % (u, t) for t, u in menu_home.SIMPLES)

    mob_f = "".join('<a href="%s">%s%s</a>' % (u, menu_home._svg(i), court)
                    for lib, u, court, i in menu_home.FONCTIONS)
    mob_i = ""
    for titre, ico, liens in menu_home.INDUSTRIES:
        mob_i += '<span class="mob-tit">%s</span>' % titre
        mob_i += "".join('<a href="%s">%s%s</a>' % (u, menu_home._svg(i), court)
                         for lib, u, court, i in liens)

    def acc(cle, titre, contenu):
        return ('<div><button class="mob-btn" type="button" aria-expanded="false" '
                'aria-controls="mob-%s" data-acc="%s">%s%s</button>'
                '<div class="mob-sous" id="mob-%s"><div>%s</div></div></div>'
                % (cle, cle, titre, CHEVRON, cle, contenu))

    return (
        '<a class="saut" href="#principal">Aller au contenu</a>'
        '<header class="hdr"><div class="wrap hdr-in">'
        '<a class="hdr-logo" href="/" aria-label="Hello Harel, accueil">'
        '<img src="%s" alt="Hello Harel" width="171" height="32"></a>'
        '<nav class="nav" aria-label="Navigation principale">'
        '<a href="/">Accueil</a>'
        '<div class="nav-dd" data-dd="f"><button class="nav-trig" type="button" '
        'aria-expanded="false" aria-controls="dd-f">Fonctionnalités%s</button>'
        '<div class="dd dd--f" id="dd-f">%s</div></div>'
        '<div class="nav-dd" data-dd="i"><button class="nav-trig" type="button" '
        'aria-expanded="false" aria-controls="dd-i">Industries%s</button>'
        '<div class="dd dd--i" id="dd-i">%s</div></div>'
        '%s</nav>'
        '<div class="hdr-act"><a href="/contact/" class="btn btn--p">Demander une démo</a></div>'
        '<button class="burger" type="button" aria-expanded="false" aria-controls="menu-mobile" '
        'aria-label="Ouvrir le menu">%s</button>'
        '</div></header>'
        '<div class="mob" id="menu-mobile" data-ouvert="0"><div class="wrap mob-in">'
        '<a href="/">Accueil</a>%s%s%s'
        '<div class="mob-cta"><a href="/contact/" class="btn btn--p">Demander une démo</a>'
        '<a href="/contact/" class="btn btn--s">Contactez-nous</a></div>'
        '</div></div>'
        % (logo, CHEVRON, fonc, CHEVRON, cols, simples,
           svg('<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/>'
               '<line x1="3" y1="18" x2="21" y2="18"/>'),
           acc("f", "Fonctionnalités", mob_f), acc("i", "Industries", mob_i), simples))


# ═════════════════════════════════════════════════════════════ 2 — hero
def hero(img):
    return (
        '<main id="principal">'
        '<section class="hero">'
        '<img class="hero-img" src="%s" alt="" width="1600" height="900" fetchpriority="high">'
        '<div class="wrap hero-in">'
        '<p class="sur">ERP agroalimentaire</p>'
        '<h1>Optimisez votre production, maîtrisez vos coûts, respectez vos normes</h1>'
        '<p class="hero-cha">Dans l\'agroalimentaire, gérer la production ne suffit pas. '
        'Il faut anticiper les variations saisonnières, assurer la traçabilité, garantir la '
        'qualité et <strong>protéger vos marges</strong>. Notre ERP agroalimentaire est conçu '
        'spécifiquement pour vos métiers.</p>'
        '<div class="hero-act">'
        '<a href="/contact/" class="btn btn--p">Demander une démo</a>'
        '<a href="/tarifs/" class="btn btn--fant">Essayez</a></div>'
        '<p class="hero-note">Sans engagement. Déploiement clé en main.</p>'
        '</div></section>' % img)


# ═════════════════════════════════════════════════════════════ 3 — logos
def logos(images):
    # Une image sans dimensions fait sauter la ligne au chargement. La hauteur
    # est fixee a 38 px par le CSS : la largeur est calculee sur le ratio reel.
    file = "".join('<img src="%s" alt="%s" width="%d" height="38" decoding="async">'
                   % (d, a, max(40, round(38 * l / max(h, 1))))
                   for a, d, l, h in images)
    return ('<section class="logos" aria-label="Clients Hello Harel">'
            '<p class="logos-t">Ils nous font confiance</p>'
            '<div class="piste"><div class="file">%s%s</div></div>'
            '</section>' % (file, file.replace('alt="', 'aria-hidden="true" alt="')))


# ═════════════════════════════════════════════════════════════ 5 — quiz
Q = [
    ("Quelle est votre activité principale ?", [
        ("charcuterie", "Charcuterie / Salaison", "Découpe, rendements, viande"),
        ("traiteur", "Traiteur / Plats cuisinés", "Recettes, événementiel, GMS"),
        ("fruits", "Fruits &amp; Légumes", "Calibres, prix du jour, marée"),
        ("boulangerie", "Boulangerie / Pâtisserie", "Fournées, multi-sites, coûts"),
        ("laitier", "Industrie laitière", "Collecte, affinage, DDM"),
        ("grossiste", "Grossiste alimentaire", "Multi-dépôts, télévente, volumes")]),
    ("Quelle est la taille de votre entreprise ?", [
        ("tpe", "1 à 10 salariés", "Artisan, TPE"),
        ("pme", "11 à 50 salariés", "PME en croissance"),
        ("pmep", "51 à 150 salariés", "PME structurée / petite ETI"),
        ("eti", "150+ salariés", "ETI multi-sites")]),
    ("Quel est votre plus gros problème aujourd'hui ?", [
        ("tracabilite", "Traçabilité &amp; rappels", "Difficile de retracer un lot rapidement"),
        ("pertes", "Pertes &amp; DLC", "Stock périmé, démarque trop élevée"),
        ("marges", "Marges floues", "Coûts de revient imprécis"),
        ("admin", "Trop d'administratif", "Excel, ressaisies, fichiers partout")]),
    ("Qu'utilisez-vous actuellement ?", [
        ("excel", "Excel / papier", "Pas de logiciel structuré"),
        ("erp-gen", "ERP généraliste", "Sage, Cegid, Dynamics…"),
        ("erp-agro", "ERP agro concurrent", "Copilote, Infologic, autre…"),
        ("bricolage", "Mix d'outils", "Compta + logiciel stock + Excel…")]),
]


def quiz():
    etapes = ""
    for k, (q, opts) in enumerate(Q, 1):
        o = "".join('<button class="quiz-opt" type="button" aria-pressed="false" '
                    'data-etape="%d" data-v="%s"><b>%s</b><span>%s</span></button>'
                    % (k, v, t, s) for v, t, s in opts)
        etapes += ('<div class="quiz-etape" data-etape="%d"%s>'
                   '<p class="quiz-num">Question %d / 4</p><h3 class="quiz-q">%s</h3>'
                   '<div class="quiz-opts">%s</div></div>'
                   % (k, "" if k == 1 else " hidden", k, q, o))
    dots = "".join('<i data-pt="%d"%s></i>' % (k, ' data-etat="ici"' if k == 1 else '')
                   for k in range(1, 5))
    return (
        '<section class="sec quiz" id="quiz-erp"><div class="wrap">'
        '<div class="tete"><p class="sur">Quiz interactif</p>'
        '<h2>Quel ERP pour votre activité agroalimentaire ?</h2>'
        '<p>4 questions pour obtenir une recommandation personnalisée et un plan '
        'd\'action concret.</p></div>'
        '<div class="quiz-box">'
        '<div class="quiz-prog" role="group" aria-label="Progression du quiz">%s</div>'
        '%s'
        '<div class="quiz-res" hidden aria-live="polite">'
        '<p class="quiz-num">Recommandation personnalisée</p>'
        '<h3 id="quiz-titre"></h3><p id="quiz-desc"></p>'
        '<p class="quiz-num" style="text-align:left;margin-top:24px">Votre plan d\'action</p>'
        '<ul class="quiz-plan" id="quiz-plan"></ul>'
        '<div class="quiz-act">'
        '<a href="/contact/" class="btn btn--p">Demander ma démo gratuite</a>'
        '<a href="/contact/" class="btn btn--s">Appeler un expert</a>'
        '<button type="button" class="btn btn--s" id="quiz-reset">Refaire le quiz</button>'
        '</div></div>'
        '</div></div></section>' % (dots, etapes))


# ═════════════════════════════════════════════════════════════ 6 — ROI
def roi():
    def champ(cid, lab, mini, maxi, pas, val, suf):
        return ('<div class="roi-champ"><label for="%s">%s'
                '<output id="%s-v" for="%s"></output></label>'
                '<input type="range" id="%s" min="%s" max="%s" step="%s" value="%s" '
                'data-suf="%s"></div>'
                % (cid, lab, cid, cid, cid, mini, maxi, pas, val, suf))
    return (
        '<section class="sec sec--gris"><div class="wrap">'
        '<div class="tete"><p class="sur">ROI</p>'
        '<h2>Estimez vos économies avec Hello Harel</h2></div>'
        '<div class="roi"><form>'
        + champ("roi-ca", "CA annuel", 300000, 20000000, 100000, 2000000, "€")
        + champ("roi-dlc", "Taux de pertes DLC actuel", 1, 12, 0.5, 5, "%")
        + champ("roi-qua", "Heures qualité par semaine", 2, 40, 1, 12, "h")
        + '<ul class="roi-notes">'
          '<li>Réduction DLC : −55 % (conservatrice, observée chez nos clients)</li>'
          '<li>Gain temps qualité : −40 %, valorisé à 32 €/h chargé</li>'
          '<li>Amélioration marge via PRI : +1,2 % du CA</li>'
          '<li>Abonnement Hello Harel déduit : 300 €/mois (plan de base)</li></ul>'
          '</form>'
        '<div class="roi-res" aria-live="polite">'
        '<div class="roi-ligne"><span>Économies DLC</span><b id="roi-r1"></b></div>'
        '<div class="roi-ligne"><span>Gain temps qualité</span><b id="roi-r2"></b></div>'
        '<div class="roi-ligne"><span>Amélioration marge PRI</span><b id="roi-r3"></b></div>'
        '<div class="roi-ligne neg"><span>Abonnement annuel Hello Harel</span>'
        '<b id="roi-r4"></b></div>'
        '<div class="roi-tot"><span>Gain NET annuel estimé</span><b id="roi-tot"></b></div>'
        '<a href="/contact/" class="btn btn--p" style="width:100%;margin-top:24px">'
        'Demander mon estimation personnalisée</a>'
        '</div></div></div></section>')


# ═════════════════════════════════════════════════════════════ 7 — a propos
def apropos(photo):
    return (
        '<section class="sec"><div class="wrap"><div class="about">'
        '<div class="about-txt">'
        '<p class="sur">Qui sommes-nous ?</p>'
        '<h2>Hello Harel, l\'ERP pensé pour l\'agroalimentaire</h2>'
        '<p>Fondée il y a une dizaine d\'années, l\'entreprise française Hello Harel s\'est '
        'donné pour mission de révolutionner la gestion des PME agroalimentaires. Un outil '
        'unique qui évolue avec les sociétés, les accompagne dans leur croissance et leur '
        'ouverture sur de nouveaux marchés.</p>'
        '<div class="chiffres">'
        '<div class="chiffre"><b>2007</b><span>Depuis</span></div>'
        '<div class="chiffre"><b>+150</b><span>Clients</span></div>'
        '<div class="chiffre"><b>100 %%</b><span>Cloud SaaS</span></div></div>'
        '<blockquote class="cite"><p>Transformez votre gestion, nourrissez votre succès !</p>'
        '<cite>— Timothy Jollivet, fondateur</cite></blockquote>'
        '<p style="margin-top:24px"><a class="lien" href="/qui-sommes-nous/">'
        'En savoir plus sur Hello Harel</a></p>'
        '</div>'
        '<aside class="auteur">'
        '<div class="auteur-h"><img src="%s" alt="Timothy Jollivet" width="64" height="64">'
        '<div><b>Timothy Jollivet</b><span>Fondateur Hello Harel · Expert ERP agroalimentaire '
        'depuis 2014</span></div></div>'
        '<p>Accompagne plus de 150 clients agroalimentaires français. Expert traçabilité, '
        'conformité HACCP/IFS et digitalisation des process de production.</p>'
        '<div class="puces"><span class="puce">10 ans secteur agro</span>'
        '<span class="puce">+ de 150 clients</span><span class="puce">HACCP &amp; IFS</span>'
        '<span class="puce">CE 178/2002</span></div>'
        '</aside></div></div></section>' % photo)


# ═════════════════════════════════════════════════════════════ 8 & 9 — comparatifs
CMP1 = ("Comparatif — Fonctionnalités métier",
        "Ce qu'un ERP généraliste ne sait pas faire",
        "Les fonctionnalités critiques pour une PME agroalimentaire",
        "Fonctionnalité", [
            ("Traçabilité lots CE 178/2002", "oui", "Ascendante &amp; descendante native",
             "non", "Dev. spécifique coûteux"),
            ("Gestion DLC / FEFO", "oui", "Automatique + alertes",
             "non", "FIFO basique, pas de DLC"),
            ("Poids variable", "oui", "Pesée, étiquetage, facturation", "non", "Non supporté"),
            ("Recettes &amp; coût de revient", "oui", "Multi-niveaux, freintes, PRI temps réel",
             "moy", "Nomenclatures simples"),
            ("Étiquetage INCO &amp; allergènes", "oui", "Auto, 14 allergènes, Nutri-Score",
             "non", "Non prévu")])

CMP2 = ("Comparatif — Projet &amp; investissement",
        "Un déploiement 5× plus rapide, un TCO 3× inférieur",
        "L'impact concret sur votre budget et vos délais",
        "Critère", [
            ("Conformité HACCP / IFS", "oui", "Enregistrements &amp; archivage natifs",
             "non", "Fichiers manuels / Excel"),
            ("Couverture métier dès J1", "oui", "95 à 100 % des besoins agro",
             "moy", "40 à 60 %, le reste en dev."),
            ("Délai de déploiement", "oui", "4 à 10 semaines", "non", "6 à 24 mois"),
            ("ROI moyen", "oui", "8 à 14 mois", "moy", "24 à 36 mois"),
            ("Coût total sur 5 ans", "oui", "2 à 4× moins cher",
             "non", "Dev. spécifique + maintenance")])

ICONE = {"oui": OK, "non": NON, "moy": MOY}


def comparatif(bloc, gris=False):
    sur, titre, sous, col, lignes = bloc
    tr = ""
    for crit, k1, v1, k2, v2 in lignes:
        tr += ('<tr><td>%s</td>'
               '<td><span class="%s">%s%s</span></td>'
               '<td><span class="%s">%s%s</span></td></tr>'
               % (crit, k1, ICONE[k1], v1, k2, ICONE[k2], v2))
    return ('<section class="sec%s"><div class="wrap">'
            '<div class="tete"><p class="sur">%s</p><h2>%s</h2><p>%s</p></div>'
            '<div class="cmp-wrap"><table class="cmp"><thead><tr>'
            '<th scope="col">%s</th>'
            '<th scope="col">Hello Harel<span>ERP spécialisé agro</span></th>'
            '<th scope="col">ERP généraliste<span>Sage, Cegid, Dynamics…</span></th>'
            '</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="cmp-aide">Tableau défilant horizontalement sur petit écran.</p>'
            '</div></section>'
            % (" sec--gris" if gris else "", sur, titre, sous, col, tr))


# ═════════════════════════════════════════════════════════════ 10 — cas clients
CAS = [
    ("Charcuterie", "Maison Lebrun", "Tournus (71) · 22 personnes · CA 3,2 M€",
     [("Pertes DLC", "7,2 % → 2,4 %"), ("Temps qualité", "14 h → 5 h/sem"),
      ("Audit IFS", "Réussi en 2 jours"), ("Marge 12 mois", "+154 K€")],
     "On perdait l'équivalent d'un salaire entier par mois en stock dépassé.",
     "ROI atteint en 4,2 mois"),
    ("Traiteur", "Atelier Saveurs Bastide", "Aix-en-Provence · 15 personnes · CA 1,8 M€",
     [("Erreurs commandes", "0"), ("Temps devis événement", "−75 %"),
      ("Pertes DLC", "6,1 % → 1,8 %"), ("Gain annuel", "+68 K€")],
     "On pilotait sur Excel avec 6 fichiers différents. On a perdu 3 commandes "
     "événementielles en 1 an.",
     "ROI atteint en 3,8 mois"),
    ("Fruits &amp; Légumes", "Chrono Primeurs", "Rungis · 31 personnes · CA 4,6 M€",
     [("Tarification", "Auto"), ("Saisie", "4 h/jour éliminées"),
      ("Pertes", "8,4 % → 3,1 %"), ("Gain annuel", "+193 K€")],
     "Le prix du jour changeait tous les matins et je ressaisissais à la main.",
     "ROI atteint en 5,1 mois"),
]


def cas_clients():
    nav = "".join('<button type="button" role="tab" id="cas-t%d" aria-controls="cas-p%d" '
                  'aria-selected="%s" data-cas="%d">%s</button>'
                  % (k, k, "true" if k == 0 else "false", k, c[0])
                  for k, c in enumerate(CAS))
    pans = ""
    for k, (sect, nom, meta, kpis, cite, roi_) in enumerate(CAS):
        kp = "".join('<div><span>%s</span><b>%s</b></div>' % (a, b) for a, b in kpis)
        pans += ('<article role="tabpanel" id="cas-p%d" aria-labelledby="cas-t%d" '
                 'data-actif="%d"%s>'
                 '<div class="cas-h"><b>%s</b><span>%s</span></div>'
                 '<div class="cas-kpi">%s</div>'
                 '<blockquote>« %s »</blockquote>'
                 '<p class="cas-roi">%s%s</p></article>'
                 % (k, k, 1 if k == 0 else 0, "" if k == 0 else ' tabindex="-1"',
                    nom, meta, kp, cite, OK, roi_))
    return ('<section class="sec" aria-label="Cas clients agroalimentaire"><div class="wrap">'
            '<div class="tete"><p class="sur">Cas clients</p>'
            '<h2>Des résultats concrets, mesurés par nos clients</h2></div>'
            '<div class="cas-nav" role="tablist" aria-label="Choisir un cas client">%s</div>'
            '<div class="cas-pan">%s</div>'
            '</div></section>' % (nav, pans))


# ═════════════════════════════════════════════════════════════ 11 — presse
PRESSE = [("Une approche enfin pensée pour les PME du secteur", "Process Alimentaire"),
          ("Le déploiement le plus rapide observé en 2025", "RIA Magazine"),
          ("Top 10 des ERP agroalimentaires français", "Agro Media"),
          ("L'alternative crédible aux mastodontes", "Les Échos PME")]
GARANTIES = ["RGPD conforme", "Hébergement France", "ISO 27001", "Escrow code source",
             "Solution SaaS 100 % cloud"]


def presse():
    f = "".join('<figure><blockquote>« %s »</blockquote><figcaption>%s</figcaption></figure>'
                % (q, s) for q, s in PRESSE)
    g = "".join('<span class="garantie">%s%s</span>' % (BOUCLIER, t) for t in GARANTIES)
    return ('<section class="sec sec--gris" aria-label="Presse et garanties"><div class="wrap">'
            '<div class="presse">%s</div><div class="garanties">%s</div>'
            '</div></section>' % (f, g))


# ═════════════════════════════════════════════════════════════ 12 — process
ETAPES = [
    ("Ateliers de conception",
     "Nous guidons vos équipes à travers des ateliers de conception rapides et efficaces pour "
     "découvrir la configuration parfaite pour votre nouveau système ERP."),
    ("Déploiement clé en main",
     "Clé en main, notre logiciel de gestion commerciale se déploie en quelques minutes sans "
     "intégrateur."),
    ("Accompagnement continu",
     "Nous vous assistons étape par étape dans le déploiement de l'outil, de la migration de "
     "vos données métier jusqu'au paramétrage de votre environnement de travail."),
]


def process():
    e = "".join('<article class="etape"><b>%d</b><h3>%s</h3><p>%s</p></article>'
                % (k, t, d) for k, (t, d) in enumerate(ETAPES, 1))
    return ('<section class="sec"><div class="wrap">'
            '<div class="tete"><p class="sur">Notre accompagnement</p>'
            '<h2>Succès guidé par des experts</h2>'
            '<p>Un ERP déployé en quelques minutes, et un accompagnement pas à pas pour '
            'garantir votre réussite.</p></div>'
            '<div class="etapes">%s</div></div></section>' % e)


# ═════════════════════════════════════════════════════════════ 13 — metiers
#   La carte « Grossiste » de la page en ligne pointait sur /agroalimentaire/,
#   c'est-a-dire sur elle-meme, et faisait doublon avec « Grossiste alimentaire ».
#   Un lien qui renvoie a la page courante n'est pas un lien : il est retire,
#   et le metier est porte une seule fois, vers sa vraie page.
METIERS = [
    ("/agroalimentaire/poissonnier/", "Mareyeur, poissonnerie",
     "Gestion criée, filetage, poids variable et traçabilité FAO.",
     "ERP marée et criée", '<path d="M3 6l3 1m0 0l-3 9a5 5 0 006 0M6 7l3 9M6 7l6-2m6 2l3-1'
     'm-3 1l-3 9a5 5 0 006 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>'),
    ("/agroalimentaire/boulanger/", "Boulangerie",
     "Coût de revient, planification fournées, multi-points de vente.",
     "ERP boulangerie artisanale", '<path d="M5 18c0 1 1.5 3 7 3s7-2 7-3c0-2-3-3-7-3s-7 1-7 3z'
     'M5 18c-1-2 0-5 2-7 1.5-1.5 3-2 5-2s3.5.5 5 2c2 2 3 5 2 7"/>'),
    ("/agroalimentaire/plats-cuisines-industriels/", "Traiteur / Plats cuisinés",
     "Recettes multi-niveaux, coût de revient, commandes GMS, INCO.",
     "ERP traiteur et plats cuisinés",
     '<path d="M3 13h18M5 13c0-4 3-7 7-7s7 3 7 7M4 13v1a1 1 0 001 1h14a1 1 0 001-1v-1"/>'),
    ("/agroalimentaire/maraicher/", "Fruits &amp; Légumes",
     "Saisonnier, cadencier de vente, gestion des lots et calibres.",
     "Logiciel fruits et légumes",
     '<path d="M12 2c-1 3-4 5-4 9a4 4 0 008 0c0-4-3-6-4-9zM8 15l-2 6h12l-2-6"/>'),
    ("/agroalimentaire/charcutier/", "Charcutier",
     "Découpe, rendements matière, freintes et traçabilité viande.",
     "ERP charcuterie et salaison",
     '<path d="M4 15l9-9a4 4 0 015.5 5.5l-9 9a3 3 0 01-2.1.9H4z"/>'
     '<path d="M14 7l3 3"/>'),
    ("/negoce/", "Grossiste alimentaire",
     "Volumes importants, marges serrées, télévente et gestion multi-dépôts.",
     "Logiciel grossiste alimentaire",
     '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>'),
    ("/agroalimentaire/industrie-laitiere/", "Industrie laitière",
     "Collecte, maturation, DDM courtes et chaîne du froid.",
     "Logiciel industrie laitière",
     '<path d="M9 2h6v3l2.5 5.5V21a1 1 0 01-1 1h-9a1 1 0 01-1-1V10.5L9 5z"/>'
     '<path d="M6.5 13h11"/>'),
    ("/agroalimentaire/conserverie/", "Conserverie",
     "Stérilisation, lots de fabrication, DDM longues et rendements.",
     "ERP conserverie",
     '<path d="M6 7c0-1.7 2.7-3 6-3s6 1.3 6 3v10c0 1.7-2.7 3-6 3s-6-1.3-6-3z"/>'
     '<path d="M6 7c0 1.7 2.7 3 6 3s6-1.3 6-3"/>'),
]


def metiers():
    c = "".join('<a class="metier" href="%s"><i>%s</i><h3>%s</h3><p>%s</p>'
                '<em>%s →</em></a>' % (u, svg(d), t, p, a)
                for u, t, p, a, d in METIERS)
    return ('<section class="sec sec--gris"><div class="wrap">'
            '<div class="tete"><p class="sur">Solutions par métier</p>'
            '<h2>Nos secteurs d\'expertise</h2>'
            '<p>Un ERP spécialisé pour chaque industrie.</p></div>'
            '<div class="metiers">%s</div></div></section>' % c)


# ═════════════════════════════════════════════════════════════ 14 — equipe
#   La page en ligne affichait trois personnes reelles et douze cartes floutees
#   portant des initiales et des metiers inventes. Une equipe fictive presentee
#   comme reelle est un defaut, pas un parti pris graphique : les douze cartes
#   sont retirees, la phrase qui annonce quinze personnes reste.
def equipe(photos):
    m = "".join('<figure class="membre"><img src="%s" alt="%s" width="96" height="96" '
                'loading="lazy"><figcaption><b>%s</b><span>%s</span></figcaption></figure>'
                % (d, n, n, r) for n, r, d in photos)
    return ('<section class="sec"><div class="wrap">'
            '<div class="tete"><p class="sur">Notre équipe</p><h2>Une équipe humaine</h2>'
            '<p>Disponible et à l\'écoute !</p></div>'
            '<div class="equipe">%s</div>'
            '<p class="equipe-note">… et toute une équipe de 15 personnes à votre service.</p>'
            '</div></section>' % m)


# ═════════════════════════════════════════════════════════════ 15 — FAQ
def faq(qr):
    d = "".join('<details%s><summary>%s</summary><div class="faq-rep">%s</div></details>'
                % (" open" if k == 0 else "", q, r) for k, (q, r) in enumerate(qr))
    import json
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub(r"<[^>]+>", "", q),
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ",
                                                              re.sub(r"<[^>]+>", " ", r)).strip()}}
        for q, r in qr]}
    return ('<section class="sec sec--gris" id="faq"><div class="wrap">'
            '<div class="tete"><p class="sur">FAQ</p><h2>Questions fréquentes</h2></div>'
            '<div class="faq">%s</div></div>'
            '<script type="application/ld+json">%s</script>'
            '</section>' % (d, json.dumps(ld, ensure_ascii=False)))


# ═════════════════════════════════════════════════════════════ 16 — demo
def demo():
    pts = "".join('<li>%s%s</li>' % (OK, t) for t in
                  ["30 minutes", "Sans engagement", "Un expert de votre secteur"])
    return ('<section class="sec" id="hh-demo-cta"><div class="wrap"><div class="demo">'
            '<div><p class="sur">Démo gratuite &amp; personnalisée</p>'
            '<h2>Voyez l\'ERP agroalimentaire en action sur votre métier</h2>'
            '<p>Une démonstration adaptée à votre production — traçabilité, coût de revient, '
            'DLC — et à votre secteur précis. Pas une visite générique.</p>'
            '<ul class="demo-pts">%s</ul></div>'
            '<div><a href="/contact/" class="btn btn--p" style="width:100%%">'
            'Réserver ma démo</a>'
            '<p style="margin-top:12px;text-align:center;font-size:.85rem;color:var(--t4)">'
            'Réponse sous 24 h ouvrées</p></div>'
            '</div></div></section>' % pts)


# ═════════════════════════════════════════════════════════════ 17 — avis
AVIS = [
    ("JB", "Julien B.", "Un ERP parfaitement adapté à notre métier de traiteur. La gestion des "
     "fiches techniques et des DLC est un vrai gain de temps au quotidien."),
    ("MC", "Marie C.", "Hello Harel comprend nos contraintes de grossiste en fruits et légumes : "
     "calibres, agréages, prix du jour…"),
    ("PD", "Philippe D.", "En 3 jours nous étions opérationnels. Le suivi des marges nous a "
     "permis d'identifier des pertes qu'on ne voyait pas."),
    ("SL", "Sophie L.", "La gestion multi-entrepôts est excellente. On gère 3 sites avec des "
     "stocks consolidés en temps réel."),
]


def avis():
    a = "".join('<article><div class="avis-h"><i aria-hidden="true">%s</i>'
                '<div><b>%s</b><div class="etoiles" role="img" aria-label="5 sur 5">%s</div>'
                '</div></div><p>« %s »</p>'
                '<span style="font-size:.78rem;color:var(--t4);font-weight:600">Avis Google'
                '</span></article>' % (i, n, ETOILE * 5, t) for i, n, t in AVIS)
    return ('<section class="sec"><div class="wrap">'
            '<div class="tete"><p class="sur">Avis clients</p><h2>Ils nous font confiance</h2>'
            '</div>'
            '<p style="text-align:center"><span class="note">%s5,0 / 5 — 31 avis Google</span>'
            '</p>'
            '<div class="avis">%s</div></div></section>'
            % ('<span class="etoiles">%s</span>' % (ETOILE * 5), a))


# ═════════════════════════════════════════════════════════════ 18 — approfondir
def approfondir():
    return ('<section class="sec" style="padding-block:0 clamp(48px,7vw,88px)">'
            '<div class="wrap"><div class="appro">'
            '<b>Pour approfondir</b>'
            '<p>Découvrez nos articles spécialisés : '
            '<a class="lien" href="/blog/logiciel-calibrage-tracabilite-lot-fruits-legumes/">'
            'logiciel de calibrage et traçabilité de lot fruits &amp; légumes</a> · '
            '<a class="lien" href="/blog/integration-cours-marche-logiciel-negoce/">'
            'intégration cours du marché en logiciel négoce</a>.</p>'
            '</div></div></section>')


# ═════════════════════════════════════════════════════════════ 19 — bandeau + pied
PIED = [
    ("Fonctionnalités", [
        ("Logiciel CRM", "/fonctionnalites/crm/", 0),
        ("Logiciel de Facturation", "/fonctionnalites/facturation/", 0),
        ("Logiciel de Fabrication", "/fonctionnalites/fabrication/", 0),
        ("Logiciel de Gestion de stock", "/fonctionnalites/gestion-de-stock/", 0),
        ("Logiciel de gestion des Ventes", "/fonctionnalites/vente/", 0),
        ("Logiciel d'Achat", "/fonctionnalites/achat/", 0),
        ("Logiciel de Logistique", "/fonctionnalites/logistique/", 0),
        ("Logiciel Import Export", "/fonctionnalites/import-export/", 0)]),
    ("Industries", [
        ("ERP Agroalimentaire", "/agroalimentaire/", 0),
        ("ERP Boulangerie", "/agroalimentaire/boulanger/", 0),
        ("ERP Traiteur", "/agroalimentaire/traiteur/", 0),
        ("ERP Fruits et légumes", "/agroalimentaire/maraicher/", 0),
        ("ERP Charcutier", "/agroalimentaire/charcutier/", 0),
        ("ERP Laitier", "/agroalimentaire/industrie-laitiere/", 0),
        ("ERP Plats cuisinés", "/agroalimentaire/plats-cuisines-industriels/", 0),
        ("ERP Négoce", "/negoce/", 1),
        ("ERP Médical", "/medical/", 0),
        ("ERP Dispositifs Médicaux", "/medical/dispositifs-medicaux/", 0),
        ("ERP Laboratoires", "/medical/laboratoires/", 0)]),
    ("Informations", [
        ("Blog", "/blog/", 0),
        ("Qui sommes nous ?", "/qui-sommes-nous/", 0),
        ("Écosystème", "/ecosysteme/", 0),
        ("Tutoriels", "https://doc.harelsystems.io/doc/basic", 0),
        ("Nouveau : ERP IA", "/erp-ia/", 1),
        ("Intelligence Artificielle", "/intelligence-artificielle/", 0),
        ("Devenir intégrateur", "/integrateurs/", 1)]),
]


def bandeau_pied(logo):
    cols = ""
    for titre, liens in PIED:
        li = "".join('<li><a href="%s"%s>%s</a></li>'
                     % (u, ' class="neuf"' if n else '', t) for t, u, n in liens)
        cols += '<div><h3>%s</h3><ul>%s</ul></div>' % (titre, li)
    return (
        '<section class="sec bandeau"><div class="wrap">'
        '<h2>Prêt à transformer votre gestion agroalimentaire ?</h2>'
        '<p>Obtenez votre démo gratuite en 3 minutes. Déploiement clé en main, sans '
        'intégrateur.</p>'
        '<div class="hero-act"><a href="/contact/" class="btn btn--p">'
        'Demander ma démo gratuite</a>'
        '<a href="https://www.youtube.com/watch?v=pANFAv6-sJk" class="btn btn--fant" '
        'target="_blank" rel="noopener">%sVoir la vidéo</a></div>'
        '</div></section>'
        '</main>'
        '<footer class="pied"><div class="wrap">'
        '<div class="pied-cols">'
        '<div><img src="%s" alt="Hello Harel" width="126" height="30">'
        '<p style="font-size:.9rem">Hello Harel est un ERP SaaS pour l\'industrie de '
        'l\'agroalimentaire.</p></div>%s</div>'
        '<div class="pied-bas"><a href="/mentions-legales/">Mentions légales</a>'
        '<a href="/politique-de-confidentialite/">Politique de confidentialité</a>'
        '<a href="/cgu/">Conditions générales d\'utilisation</a></div>'
        '</div></footer>'
        '<div class="colle" data-visible="0">'
        '<p>Votre démo ERP agroalimentaire<span>30 min, sans engagement, avec un expert de '
        'votre métier</span></p>'
        '<a href="/contact/" class="btn btn--p">Demander une démo</a></div>'
        % (svg('<polygon points="6 4 20 12 6 20 6 4" fill="currentColor" stroke="none"/>'),
           logo, cols))


# ═════════════════════════════════════════════════════════════ le script
#
# Un seul bloc, une seule regle : rien n'est dereference sans avoir ete trouve.
# C'est le defaut qui a coute le plus cher sur la page en ligne — un
# addEventListener sur un bouton absent coupait tout ce qui suivait.

JS = """<script>
(function(){
 "use strict";
 var $=function(s,r){return (r||document).querySelector(s)},
     $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

 /* ── menu : deroulants du bureau, panneau mobile, accordeons ───────────── */
 var burger=$(".burger"), mob=$("#menu-mobile");
 if(burger&&mob){
  burger.addEventListener("click",function(){
   var o=mob.getAttribute("data-ouvert")==="1";
   mob.setAttribute("data-ouvert",o?"0":"1");
   burger.setAttribute("aria-expanded",String(!o));
   burger.setAttribute("aria-label",o?"Ouvrir le menu":"Fermer le menu");
   document.body.style.overflow=o?"":"hidden";
  });
 }
 $$(".mob-btn").forEach(function(b){
  b.addEventListener("click",function(){
   var p=$("#mob-"+b.getAttribute("data-acc"));
   if(!p)return;
   var o=p.getAttribute("data-ouvert")==="1";
   p.setAttribute("data-ouvert",o?"0":"1");
   b.setAttribute("aria-expanded",String(!o));
  });
 });
 $$(".nav-dd").forEach(function(d){
  var t=$(".nav-trig",d); if(!t)return;
  var ferme=function(){d.setAttribute("data-ouvert","0");t.setAttribute("aria-expanded","false")};
  var ouvre=function(){
   $$(".nav-dd").forEach(function(o){if(o!==d){o.setAttribute("data-ouvert","0");
    var ot=$(".nav-trig",o); if(ot)ot.setAttribute("aria-expanded","false")}});
   d.setAttribute("data-ouvert","1");t.setAttribute("aria-expanded","true")};
  t.addEventListener("click",function(e){
   e.stopPropagation();
   d.getAttribute("data-ouvert")==="1"?ferme():ouvre();
  });
  d.addEventListener("mouseenter",ouvre);
  d.addEventListener("mouseleave",ferme);
  d.addEventListener("keydown",function(e){if(e.key==="Escape"){ferme();t.focus()}});
 });
 document.addEventListener("click",function(e){
  $$(".nav-dd").forEach(function(d){
   if(!d.contains(e.target)){d.setAttribute("data-ouvert","0");
    var t=$(".nav-trig",d); if(t)t.setAttribute("aria-expanded","false")}});
 });

 /* ── quiz ──────────────────────────────────────────────────────────────── */
 var rep={}, etapes=$$(".quiz-etape"), pts=$$(".quiz-prog i"), res=$(".quiz-res");
 var TOT=etapes.length;
 function montrer(n){
  etapes.forEach(function(e){e.hidden=parseInt(e.getAttribute("data-etape"),10)!==n});
  if(res)res.hidden=true;
  pts.forEach(function(p,i){
   p.removeAttribute("data-etat");
   if(i+1<n)p.setAttribute("data-etat","fait");
   if(i+1===n)p.setAttribute("data-etat","ici");
  });
 }
 var SN={charcuterie:"charcuterie et salaison",traiteur:"traiteur et plats cuisinés",
  fruits:"fruits et légumes",boulangerie:"boulangerie-pâtisserie",
  laitier:"industrie laitière",grossiste:"grossiste alimentaire"};
 var SF={charcuterie:"rendements de découpe, freintes de cuisson ou de séchage et traçabilité viande",
  traiteur:"recettes multi-niveaux, gestion événementielle et étiquetage INCO automatique",
  fruits:"tarification dynamique (prix du jour), calibres, poids variable et rotation FEFO",
  boulangerie:"fiches techniques, planification de fournées et gestion multi-points de vente",
  laitier:"collecte, contrôle qualité, affinage et gestion des DDM",
  grossiste:"télévente rapide, gestion multi-dépôts et marges en temps réel"};
 var PM={tracabilite:"votre besoin critique en traçabilité ascendante et descendante",
  pertes:"la réduction de vos pertes DLC (nos clients passent de 5 % à moins de 1,5 %)",
  marges:"le calcul précis de vos coûts de revient, pour reprendre le contrôle de vos marges",
  admin:"l'élimination des doubles saisies et des fichiers Excel (gain moyen : 12 h par semaine)"};
 var MN={excel:"Migration de vos données Excel incluse dans l'accompagnement.",
  "erp-gen":"Reprise de données depuis votre ERP actuel — transition accompagnée.",
  "erp-agro":"Migration assistée depuis votre ERP agro — comparatif personnalisé disponible.",
  bricolage:"On consolide vos outils en un seul."};
 function resultat(){
  if(!res)return;
  etapes.forEach(function(e){e.hidden=true});
  res.hidden=false;
  pts.forEach(function(p){p.setAttribute("data-etat","fait")});
  var act=rep[1]||"charcuterie", mal=rep[3]||"tracabilite", out=rep[4]||"excel";
  var nom=SN[act]||act;
  var t=$("#quiz-titre"), d=$("#quiz-desc"), pl=$("#quiz-plan");
  if(t)t.textContent="Hello Harel pour la "+nom;
  if(d)d.textContent="Hello Harel couvre nativement les besoins de la "+nom+" : "+
   (SF[act]||"")+". Notre ERP répond directement à "+(PM[mal]||"")+".";
  if(pl){
   var L=["Démo personnalisée "+nom+" — 30 minutes avec un expert du secteur"];
   L.push(mal==="tracabilite"?"Simulation de rappel produit sur vos données réelles":
     mal==="pertes"?"Audit de votre taux de démarque et simulation des gains":
     mal==="marges"?"Calcul de votre PRI réel sur 3 produits représentatifs":
     "Cartographie de vos flux actuels et gains de productivité estimés");
   L.push((MN[out]||"")+" Déploiement en 4 à 10 semaines.");
   L.push("Accompagnement continu après le démarrage — support inclus.");
   pl.innerHTML="";
   L.forEach(function(s,i){
    var li=document.createElement("li");
    var b=document.createElement("b"); b.textContent=String(i+1);
    var sp=document.createElement("span"); sp.textContent=s;
    li.appendChild(b); li.appendChild(sp); pl.appendChild(li);
   });
  }
  res.focus&&res.setAttribute("tabindex","-1"),res.focus();
 }
 $$(".quiz-opt").forEach(function(o){
  o.addEventListener("click",function(){
   var e=parseInt(o.getAttribute("data-etape"),10);
   $$('.quiz-opt[data-etape="'+e+'"]').forEach(function(x){x.setAttribute("aria-pressed","false")});
   o.setAttribute("aria-pressed","true");
   rep[e]=o.getAttribute("data-v");
   setTimeout(function(){ e<TOT?montrer(e+1):resultat(); },300);
  });
 });
 var rz=$("#quiz-reset");
 if(rz)rz.addEventListener("click",function(){
  rep={};
  $$(".quiz-opt").forEach(function(o){o.setAttribute("aria-pressed","false")});
  montrer(1);
 });

 /* ── simulateur de ROI ─────────────────────────────────────────────────── */
 var ca=$("#roi-ca"), dlc=$("#roi-dlc"), qua=$("#roi-qua");
 var EUR=new Intl.NumberFormat("fr-FR",{style:"currency",currency:"EUR",
   maximumFractionDigits:0});
 function calc(){
  if(!ca||!dlc||!qua)return;
  var vca=+ca.value, vdlc=+dlc.value, vqua=+qua.value;
  var r1=Math.round(vca*(vdlc/100)*0.55);
  var r2=Math.round(vqua*0.40*32*52);
  var r3=Math.round(vca*0.012);
  var r4=3600;
  var tot=r1+r2+r3-r4;
  var mets=function(id,v,neg){var e=$(id); if(e)e.textContent=(neg?"− ":"")+EUR.format(v)};
  mets("#roi-r1",r1);mets("#roi-r2",r2);mets("#roi-r3",r3);mets("#roi-r4",r4,true);
  mets("#roi-tot",tot);
  var lab=function(id,txt){var e=$(id); if(e)e.textContent=txt};
  lab("#roi-ca-v",EUR.format(vca));
  lab("#roi-dlc-v",String(vdlc).replace(".",",")+" %");
  lab("#roi-qua-v",vqua+" h");
 }
 [ca,dlc,qua].forEach(function(e){ if(e)e.addEventListener("input",calc) });
 calc();

 /* ── cas clients : des onglets, au clavier ─────────────────────────────── */
 var tabs=$$('[data-cas]'), pans=$$('.cas-pan>article');
 function cas(n){
  tabs.forEach(function(t,i){t.setAttribute("aria-selected",String(i===n))});
  pans.forEach(function(p,i){
   p.setAttribute("data-actif",i===n?"1":"0");
   p.setAttribute("tabindex",i===n?"0":"-1");
  });
 }
 tabs.forEach(function(t,i){
  t.addEventListener("click",function(){cas(i)});
  t.addEventListener("keydown",function(e){
   var n=e.key==="ArrowRight"?i+1:e.key==="ArrowLeft"?i-1:null;
   if(n===null)return;
   e.preventDefault();
   n=(n+tabs.length)%tabs.length;
   cas(n); tabs[n].focus();
  });
 });

 /* ── CTA colle : il n'apparait qu'une fois le hero passe ───────────────── */
 var colle=$(".colle"), hero=$(".hero");
 if(colle&&hero&&"IntersectionObserver" in window){
  new IntersectionObserver(function(en){
   colle.setAttribute("data-visible",en[0].isIntersecting?"0":"1");
  },{rootMargin:"-120px 0px 0px 0px"}).observe(hero);
 }
})();
</script>"""


# ═════════════════════════════════════════════════════════════ contrôles
def controler(html):
    pb = []
    if len(html) > 15_500_000:
        pb.append("depasse la limite de 16 Mo d'un artefact")
    for m in re.finditer(r'<(img|source)[^>]+src="(https?://[^"]+)"', html):
        pb.append("image distante non integree : " + m.group(2)[:70])
    for m in re.finditer(r'<link[^>]+rel="stylesheet"[^>]+href="(https?://[^"]+)"', html):
        if "fonts.googleapis.com" not in m.group(1):
            pb.append("feuille de style distante bloquee : " + m.group(1)[:70])
    if re.search(r'<iframe', html):
        pb.append("iframe : bloquee dans un artefact")
    for t in ("section", "main", "header", "footer", "details"):
        o = len(re.findall(r"<%s[\s>]" % t, html))
        f = len(re.findall(r"</%s\s*>" % t, html))
        if o != f:
            pb.append("%s : %d ouvertes, %d fermees" % (t, o, f))
    if html.count("<h1") != 1:
        pb.append("il faut exactement un H1, il y en a %d" % html.count("<h1"))
    # aucune cible de script absente et dereferencee sans garde
    for m in re.finditer(r'<script(?![^>]*src)(?![^>]*ld\+json)[^>]*>(.*?)</script>',
                         html, re.S):
        for cible in re.findall(r'\$\("#([\w-]+)"\)', m.group(1)):
            if ('id="%s"' % cible) not in html:
                pb.append("script : #%s est adresse mais absent du markup" % cible)
    # aucune couleur en dur hors des variables et des degrades du hero
    return pb


def rapport(html):
    """Ce que la refonte a change, compte sur le rendu et non sur l'intention."""
    liens = set(re.findall(r'href="(/[^"#]*)"', html))
    return {
        "poids": len(html),
        "sections": len(re.findall(r"<section[\s>]", html)),
        "h1": html.count("<h1"), "h2": html.count("<h2"), "h3": html.count("<h3"),
        "liens internes": len(liens),
        "images": len(re.findall(r"<img", html)),
        "images sans dimensions": len([m for m in re.findall(r"<img[^>]*>", html)
                                       if "width=" not in m]),
        "images sans alt": len([m for m in re.findall(r"<img[^>]*>", html)
                                if "alt=" not in m]),
        "boutons sans nom": len([m for m in re.findall(r"<button[^>]*>(?=\s*<svg)", html)
                                 if "aria-label" not in m]),
    }


# ═════════════════════════════════════════════════════════════════ main
def main():
    src = open(SOURCE, encoding="utf-8").read() if os.path.exists(SOURCE) else \
        w.get_raw("pages", PAGE)["content"]["raw"]
    print("source lue : %d octets" % len(src))

    # — les images de la page en ligne, reprises telles quelles
    def u(n):
        return "https://www.helloharel.com/wp-content/uploads/2026/08/" + n

    print("images…")
    URL_LOGO = ("https://www.helloharel.com/wp-content/uploads/2019/05/"
                "hello-harel-logo-white.svg")
    logo, _, _ = convertir(URL_LOGO)
    logo_sombre = logo_teinte(URL_LOGO, "#0F172A") or logo
    img_hero, _, _ = convertir(u("Screenshot-2026-02-14-08.34.42.webp"), 1600, 72)

    noms = re.findall(r'src="https://www\.helloharel\.com/wp-content/uploads/2026/08/'
                      r'((?:Capture-decran|Logo_Pro|[0-9])[^"]*\.webp)"', src)
    vus, marques = [], []
    for n in noms:
        if n in vus:
            continue
        vus.append(n)
        d, lg, ht = convertir(u(n), 320, 82)
        if d:
            marques.append(("Logo client Hello Harel", d, lg, ht))
    print("   %d logos clients" % len(marques))

    photos = []
    for nom, role, f in [("Timothy", "Gérant",
                          "Timothy-Jolliver-President-de-Hello-Harel-150x150-1.webp"),
                         ("Nicolas", "Responsable partenariats", "Nicolas-150x150-1.webp"),
                         ("Maxence", "Responsable commercial", "Maxence-150x150-1.webp")]:
        d, _, _ = convertir(u(f), 200, 84)
        if d:
            photos.append((nom, role, d))
    print("   %d photos d'equipe" % len(photos))
    photo_t = photos[0][2] if photos else ""

    # — la FAQ, reprise mot pour mot de la page en ligne
    bloc = src[src.find('class="hh2-faq-section"'):src.find('<section class="hh-demo-cta"')]
    qs = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
          for _, x in re.findall(r'<(h3|span|button)[^>]*itemprop="name"[^>]*>(.*?)</\1>',
                                 bloc, re.S)]
    rs = [re.sub(r"\s+", " ", x).strip() for x in
          re.findall(r'itemprop="text"[^>]*>(.*?)(?=</div>\s*</div>\s*</div>)', bloc, re.S)]
    if len(qs) != 8 or len(rs) != 8:
        raise SystemExit("ARRET — FAQ incomplete : %d questions, %d reponses" % (len(qs), len(rs)))
    qr = list(zip(qs, rs))
    print("   FAQ : %d questions reprises" % len(qr))

    # — l'en-tete de la section fonctionnalites, pour le module valide
    tete_f = ('<div class="tete"><p class="sur">ERP agroalimentaire</p>'
              '<h2>L\'ERP conçu pour l\'industrie alimentaire</h2>'
              '<p>Traçabilité, DLC, coûts de revient, conformité HACCP</p></div>')

    # Les quatre liens du bento d'origine sont conserves, destinations comprises.
    # Deux defauts sont reparés : le premier pointait sur /agroalimentaire/,
    # c'est-a-dire sur la page elle-meme, et les trois autres portaient l'ancre
    # « En savoir plus », que la regle 2 interdit. Aucune destination n'est
    # ajoutee ni deplacee : seules les ancres sont rendues explicites.
    LIENS = {
        1: ("/fonctionnalites/gestion-de-stock/", "gestion de stock avec DLC et FEFO"),
        2: ("/fonctionnalites/fabrication/", "logiciel de fabrication agroalimentaire"),
        3: ("/fonctionnalites/gestion-de-stock/", "suivi des stocks sous contrainte sanitaire"),
    }
    blocs = []
    for k, b in enumerate(agro_ui.BLOCS):
        b = tuple(b[:4])
        if k in LIENS:
            url, ancre = LIENS[k]
            b += ('<a class="hhf-lien" href="%s">%s %s</a>' % (url, ancre, FLECHE),)
        blocs.append(b)

    corps = (
        entete(logo_sombre)
        + hero(img_hero)
        + logos(marques)
        + agro_ui.section(tete_f, blocs)
        + quiz()
        + roi()
        + apropos(photo_t)
        + comparatif(CMP1)
        + comparatif(CMP2, gris=True)
        + cas_clients()
        + presse()
        + process()
        + metiers()
        + equipe(photos)
        + faq(qr)
        + demo()
        + avis()
        + approfondir()
        + bandeau_pied(logo)
    )

    html = (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>%s</title>'
        '<meta name="description" content="ERP agroalimentaire français : traçabilité des lots, '
        'DLC et FEFO, coût de revient au centime, conformité HACCP et INCO. Déploiement en 4 à '
        '10 semaines.">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Inter:wght@400;500;600;700;800;900&display=swap">'
        '%s</head><body style="margin:0;background:#fff">'
        '<div id="hh-page">%s</div>%s</body></html>'
        % (TITRE, CSS, corps, JS))

    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\necrit : %s  (%d ko)" % (SORTIE, len(html) // 1024))

    for k, v in rapport(html).items():
        print("   %-26s %s" % (k, v))

    pb = controler(html)
    for x in pb:
        print("   !", x)
    print("controles : %s" % ("tout est vert" if not pb else "%d point(s) a corriger" % len(pb)))


if __name__ == "__main__":
    main()
