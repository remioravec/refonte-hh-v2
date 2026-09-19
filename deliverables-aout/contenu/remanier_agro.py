#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/agroalimentaire/ remaniee : les douze demandes du 18/09, appliquees au code
source de la page 1726.

   1. le quiz interactif est retire ;
   2. le simulateur de ROI est retire ;
   3. « Qui sommes-nous » reprend la section des pages soeurs, video comprise ;
   4. « Ce qu'un ERP generaliste ne sait pas faire » est retire ;
   5. « Un deploiement 5x plus rapide » est retire ;
   6. « Des resultats concrets » devient un mur de logos clients, trois colonnes ;
   7. la bande presse est retiree ;
   8. la FAQ reprend le composant des pages soeurs ;
   9. « Une equipe humaine » : deja identique aux soeurs, rien a faire ;
  10. l'appel a l'action « demo personnalisee » est retire ;
  11. les avis passent en carrousel continu, deux colonnes ;
  12. « Pour approfondir » est retire ;
  13. une section guide est ajoutee tout en bas, sous la banniere d'appel a
      l'action : une couverture de livre blanc batie sur la photo du hero, un
      sommaire de cinq chapitres et un bouton vers le hub /comparatifs/.

Aucune donnee n'est inventee. Les logos sont ceux de la mediatheque, nommes
d'apres ce qu'on lit dessus ; les questions et reponses de la FAQ sont celles
de la page ; les quatre avis sont ceux de la page.

MAQUETTE, PAS MISE EN LIGNE. La page 1726 est protegee par la regle 0 :
ce script lit la page, il ne l'ecrit jamais.

Usage :  python3 remanier_agro.py
"""

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w      # noqa: E402
import maquette_agro as M  # noqa: E402  (SVG_FA, remplacer_video)
import refonte_agro as R   # noqa: E402  (convertir, qui rend aussi les dimensions)
import agro_ebook          # noqa: E402  (la section guide)

PAGE = 1726
SOEUR = 10867                      # /agroalimentaire/fromager/, page soeur de reference
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "remanie-agro.html")
UP = "https://www.helloharel.com/wp-content/uploads/"

POLICE = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
          'family=Inter:wght@300;400;500;600;700;800;900&display=swap">')

REPOS = """<style id="hh-repos">
#hh-page .scroll-reveal,#hh-page .metier-slide{opacity:1 !important;transform:none !important}
body{margin:0;background:#fff}
</style>"""


# ══════════════════════════════════════════════════════ le mur de logos
#
# Les noms ne viennent PAS des attributs alt de la page : ceux-ci sont
# decales d'un cran (l'image de Storia e Sapori porte « Maison Alena »,
# celle de Maison Alena porte le nom suivant, et ainsi de suite). Chaque
# logo est donc nomme d'apres ce qu'on lit dessus, planche a l'appui.
# Les doublons sont ecartes : Corseprim, Les Primeurs et Jacob existaient
# chacun en deux fichiers.
LOGOS = [
    ("2026/08/Logo_Pro-inter_Magasins_Orientaux.webp", "Pro-Inter, supermarché oriental"),
    ("2026/08/1.webp", "E.Leclerc"),
    ("2026/08/2-300x240-1.webp", "Label’Frite"),
    ("2026/08/4-300x240-1.webp", "VDB, Vergers de Boulogne"),
    ("2026/08/5-300x240-1.webp", "Agri Distribution"),
    ("2026/01/Capture-decran-2026-01-13-a-14.56.24.png", "Storia e Sapori"),
    ("2026/01/Capture-decran-2026-01-13-a-14.57.18.png", "Ottanta Pasta"),
    ("2026/01/Capture-decran-2026-01-13-a-14.58.40.png", "Maison Aléna"),
    ("2026/01/Capture-decran-2026-01-13-a-15.00.01.png", "Chrono Primeurs"),
    ("2026/01/Capture-decran-2026-01-13-a-15.01.39.png", "Karine & Jeff"),
    ("2026/01/Capture-decran-2026-01-13-a-15.03.06.png", "Chef Cheffe !"),
    ("2026/01/Capture-decran-2026-01-13-a-15.04.34.png", "Savary"),
    ("2026/01/Capture-decran-2026-01-13-a-15.06.38.png", "Ciao Gusto"),
    ("2026/01/Capture-decran-2026-01-13-a-15.07.48.png", "Eatmotion"),
    ("2026/01/Capture-decran-2026-01-13-a-15.08.48.png", "Poujauran"),
    ("2026/01/Capture-decran-2026-01-13-a-15.10.42.png", "Koré"),
    ("2026/01/Capture-decran-2026-01-13-a-15.12.46.png", "HPS"),
    ("2026/01/Capture-decran-2026-01-13-a-15.14.24.png", "Les Primeurs d’Issy à Rungis"),
    ("2026/01/Capture-decran-2026-01-13-a-15.16.50.png", "Jacob, Halles de Versailles"),
    ("2026/01/Capture-decran-2026-01-13-a-15.21.09.png", "Corseprim"),
    ("2025/05/logo-beaugrain.png", "Beaugrain"),
    ("2025/05/logo-biosain.png", "Maison Bio Sain"),
    ("2025/05/logo-herbes-champenoises.jpeg", "Les Herbes Champenoises"),
    ("2025/05/logo-primeur-mondial.png", "Primeur Mondial"),
    ("2025/05/logo-toncarton.png", "Ton Carton"),
]

CSS_MUR = """<style id="hh-mur-logos">
/* Quatre logos de front, et ils coulissent — comme la bande du haut de page.
   La largeur d'une vignette se calcule sur la piste, pas sur la fenetre :
   dans une rangee en width:max-content, un pourcentage n'a aucun sens et
   laisserait depasser une cinquieme vignette. */
#hh-page .mur-section,.mur-section{padding:clamp(40px,6vw,72px) 0 !important;
 background:#f8fafc !important}
#hh-page .mur,.mur{--piste:1100px;--jour:14px;
 max-width:var(--piste) !important;margin:0 auto !important;
 display:grid !important;gap:var(--jour) !important;padding:0 !important;
 list-style:none !important;overflow:hidden !important;
 -webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);
 mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
#hh-page .mur-b,.mur-b{display:flex !important;gap:var(--jour) !important;
 width:max-content !important;margin:0 !important;padding:0 !important;
 list-style:none !important;animation:hh-mur 42s linear infinite}
/* Une rangee sur deux part dans l'autre sens : le mur respire au lieu de
   defiler d'un bloc. */
#hh-page .mur-b--rev,.mur-b--rev{animation-name:hh-mur-rev;animation-duration:50s}
#hh-page .mur:hover .mur-b,.mur:hover .mur-b,
#hh-page .mur:focus-within .mur-b,.mur:focus-within .mur-b{animation-play-state:paused}
#hh-page .mur-b>li,.mur-b>li{margin:0 !important;padding:0 !important;
 flex:0 0 calc((var(--piste) - 3 * var(--jour)) / 4)}
#hh-page .mur-b figure,.mur-b figure{display:grid !important;place-items:center !important;
 height:72px !important;margin:0 !important;padding:10px 14px !important;
 background:#fff !important;border:1px solid #e2e8f0 !important;
 border-radius:12px !important;transition:border-color .18s,box-shadow .18s !important}
#hh-page .mur-b figure:hover,.mur-b figure:hover{border-color:#00B1F5 !important;
 box-shadow:0 8px 18px -14px rgba(15,23,42,.5) !important}
#hh-page .mur-b img,.mur-b img{max-width:100% !important;width:auto !important;
 object-fit:contain !important;
 opacity:.88 !important;transition:opacity .18s !important}
#hh-page .mur-b figure:hover img,.mur-b figure:hover img{opacity:1 !important}
/* La piste est doublee : on la decale d'exactement une moitie, gouttiere
   comprise, pour que la boucle se referme sans saut. */
@keyframes hh-mur{from{transform:none}to{transform:translateX(calc(-50% - var(--jour)/2))}}
@keyframes hh-mur-rev{from{transform:translateX(calc(-50% - var(--jour)/2))}to{transform:none}}
@media (max-width:1180px){#hh-page .mur,.mur{--piste:calc(100vw - 3rem)}}
@media (max-width:700px){
 #hh-page .mur-b>li,.mur-b>li{flex:0 0 calc((var(--piste) - 2 * var(--jour)) / 3)}
 #hh-page .mur-b figure,.mur-b figure{height:60px !important;padding:8px 10px !important}
 #hh-page .mur-b img,.mur-b img{max-height:34px !important}}
@media (prefers-reduced-motion:reduce){
 #hh-page .mur-b,.mur-b{animation:none !important}
 #hh-page .mur,.mur{overflow-x:auto !important;
  -webkit-mask-image:none;mask-image:none}}
</style>"""


def logo_net(url, largeur=260, qualite=82):
    """Le logo, debarrasse de la marge vide que son fichier porte.

    Plusieurs fichiers de la mediatheque sont des captures : le logo occupe le
    tiers de l'image, le reste est du blanc. A surface egale, ces logos-la
    paraissent trois fois plus petits que les autres. On rogne donc la bordure
    unie — transparente ou quasi blanche — avant de mesurer.
    """
    import base64
    import io
    import subprocess
    from PIL import Image, ImageChops

    os.makedirs(R.CACHE, exist_ok=True)
    nom = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/")[-1])
    brut = os.path.join(R.CACHE, nom)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", brut], timeout=90)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        return None, 0, 0
    try:
        im = Image.open(brut)
        im = im.convert("RGBA")
        # Un pixel compte comme vide s'il est transparent OU tres clair.
        alpha = im.getchannel("A")
        gris = im.convert("L").point(lambda v: 0 if v > 244 else 255)
        masque = ImageChops.lighter(gris, alpha.point(lambda v: 0 if v < 12 else 255)
                                    .point(lambda v: 255 - v))
        boite = ImageChops.lighter(gris, alpha.point(lambda v: 255 if v > 12 else 0)
                                   .point(lambda v: 0)).getbbox() or masque.getbbox()
        boite = masque.getbbox()
        if boite:
            # une marge de 2 px evite de raboter un trait qui touche le bord
            x0, y0, x1, y1 = boite
            im = im.crop((max(0, x0 - 2), max(0, y0 - 2),
                          min(im.width, x1 + 2), min(im.height, y1 + 2)))
        fond = Image.new("RGB", im.size, (255, 255, 255))
        fond.paste(im, mask=im.getchannel("A"))
        im = fond
        if im.width > largeur:
            im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=qualite, method=6)
        return ("data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(),
                im.width, im.height)
    except Exception:
        return R.convertir(url, largeur, qualite)


RANGEES = 3      # trois bandes qui coulissent, pas une grille figee
SURFACE = 3400   # px carres vises par logo, format reduit
MINI, MAXI = 26, 48


def hauteur_egale(lg, ht):
    """La hauteur qui donne a ce logo la meme surface qu'aux autres."""
    if not lg or not ht:
        return 36
    return int(max(MINI, min(MAXI, round((SURFACE * ht / lg) ** 0.5))))


def mur_logos(images):
    """images : [(data URI, nom, largeur, hauteur)]

    Pas de legende : le logo se reconnait, le nom sous le logo alourdit le mur
    et double la hauteur de chaque vignette. Le nom reste dans l'alt, donc
    lisible par un lecteur d'ecran.
    """
    paquets = [images[k::RANGEES] for k in range(RANGEES)]
    bandes = ""
    for n, paquet in enumerate(paquets):
        if not paquet:
            continue
        vign = ""
        for d, nom, lg, ht in paquet:
            h = hauteur_egale(lg, ht)
            w = max(20, round(h * lg / max(ht, 1)))
            vign += ('<li><figure><img src="%s" alt="Logo %s" width="%d" height="%d" '
                     'style="height:%dpx !important;width:auto !important" '
                     'decoding="async"></figure></li>'
                     % (d, nom, w, h, h))
        # La bande est doublee a l'identique : c'est ce qui rend la boucle
        # continue. La copie est masquee aux lecteurs d'ecran.
        cache = vign.replace("<li>", '<li aria-hidden="true">')
        bandes += ('<ul class="mur-b%s">%s%s</ul>'
                   % (" mur-b--rev" if n % 2 else "", vign, cache))
    return (CSS_MUR +
            '<section class="mur-section"><div class="container">'
            '<div class="section-header">'
            '<p class="overline">Nos clients</p>'
            '<h2>Des PME agroalimentaires de tous les métiers</h2>'
            '<p>Charcutiers, primeurs, traiteurs, grossistes, pastiers, torréfacteurs — '
            'quelques-uns des clients Hello Harel.</p></div>'
            '<div class="mur">%s</div>'
            '</div></section>' % bandes)



# ══════════════════════════════════════════════════════ les avis en carrousel
CSS_AVIS = """<style id="hh-avis-carrousel">
/* Deux colonnes se decident sur la largeur de la piste, pas sur celle de la
   fenetre : la piste est bornee, et chaque carte vaut la moitie de la piste
   moins la gouttiere. Deux cartes entieres, jamais un bout de troisieme. */
#hh-page .avis-piste,.avis-piste{--piste:1152px;--jour:1.5rem;
 max-width:var(--piste) !important;margin:0 auto !important;
 overflow:hidden !important;padding:.5rem 0 1rem !important;
 -webkit-mask-image:linear-gradient(90deg,transparent,#000 4%,#000 96%,transparent);
 mask-image:linear-gradient(90deg,transparent,#000 4%,#000 96%,transparent)}
#hh-page .avis-file,.avis-file{display:flex !important;gap:var(--jour) !important;
 width:max-content !important;margin:0 !important;padding:0 !important;list-style:none !important;
 animation:hh-avis 52s linear infinite}
#hh-page .avis-piste:hover .avis-file,.avis-piste:hover .avis-file,
#hh-page .avis-piste:focus-within .avis-file,.avis-piste:focus-within .avis-file{
 animation-play-state:paused}
#hh-page .avis-file>li,.avis-file>li{margin:0 !important;padding:0 !important;
 flex:0 0 calc((var(--piste) - var(--jour))/2)}
#hh-page .avis-file .review-card,.avis-file .review-card{height:100% !important;
 margin:0 !important}
/* La piste est doublee : on la decale d'exactement une moitie, gouttiere
   comprise, pour que la boucle se referme sans saut. */
@keyframes hh-avis{from{transform:none}to{transform:translateX(calc(-50% - var(--jour)/2))}}
@media (max-width:1240px){
 #hh-page .avis-piste,.avis-piste{--piste:calc(100vw - 4rem)}}
@media (max-width:760px){
 #hh-page .avis-piste,.avis-piste{--piste:calc(100vw - 3rem);--jour:1rem}
 #hh-page .avis-file>li,.avis-file>li{flex:0 0 var(--piste)}}
@media (prefers-reduced-motion:reduce){
 #hh-page .avis-file,.avis-file{animation:none !important}
 #hh-page .avis-piste,.avis-piste{overflow-x:auto !important;
  -webkit-mask-image:none;mask-image:none}}
</style>"""


def avis_carrousel(cartes):
    """cartes : la liste des .review-card d'origine, telles quelles."""
    file = "".join("<li>%s</li>" % c for c in cartes)
    # La piste est doublee : c'est ce qui rend la boucle continue, sans saut.
    cache = "".join('<li aria-hidden="true">%s</li>' % c for c in cartes)
    return (CSS_AVIS +
            '<div class="avis-piste"><ul class="avis-file">%s%s</ul></div>' % (file, cache))


# ══════════════════════════════════════════════════════ la FAQ des soeurs
ICONES = [
    'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.656-1.79 3-4 3-.197 0-.391-.007'
    '-.58-.021M12 17h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 '
    '12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052'
    '-.382-3.016z',
    'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
    'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 '
    '01.293.707V19a2 2 0 01-2 2z',
    'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1'
    'M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'M13 10V3L4 14h7v7l9-11h-7z',
    'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
    'M12 9v2m0 4h.01M5 19h14a2 2 0 001.84-2.75L13.74 4a2 2 0 00-3.5 0L3.2 16.25A2 2 0 005 19z',
]
METAS = ["Définition, périmètre, métiers", "Spécialisé, généraliste, TCO",
         "Charcutier, primeur, traiteur", "HACCP, INCO, CE 178/2002",
         "ROI, pertes, productivité", "Cadrage, reprise, formation",
         "DLC, DDM, FEFO", "Rappel, lot, ascendante"]


def faq_soeur(qr):
    """qr : [(question, reponse HTML)] — celles de la page, mot pour mot."""
    cartes, panneaux, ld = [], [], []
    for k, (q, r) in enumerate(qr):
        cartes.append(
            '<div class="faq-card" role="button" tabindex="0" onclick="openFaqDrawer(%d)" '
            'onkeydown="if(event.key===\'Enter\'||event.key===\' \'){event.preventDefault();'
            'openFaqDrawer(%d)}">'
            '<div class="faq-card-inner">'
            '<div class="faq-card-emoji"><svg fill="none" stroke="currentColor" '
            'viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" '
            'stroke-width="2" d="%s"/></svg></div>'
            '<span class="faq-card-question">%s</span>'
            '<span class="faq-card-meta">%s</span></div>'
            '<div class="faq-card-arrow"><svg fill="none" stroke="currentColor" '
            'viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" '
            'stroke-width="2" d="M9 5l7 7-7 7"/></svg></div></div>'
            % (k, k, ICONES[k % len(ICONES)], q, METAS[k % len(METAS)]))
        panneaux.append(
            '<div class="faq-drawer-panel" data-faq="%d" style="display:none" '
            'itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">'
            '<h3 itemprop="name">%s</h3>'
            '<div class="faq-drawer-content" itemscope itemprop="acceptedAnswer" '
            'itemtype="https://schema.org/Answer"><div itemprop="text">%s</div></div></div>'
            % (k, q, r))
        ld.append(q)

    return (
        '<section class="faq-section" id="faq" itemscope '
        'itemtype="https://schema.org/FAQPage"><div class="container">'
        '<div class="section-header">'
        '<p class="overline">FAQ ERP agroalimentaire</p>'
        '<h2>Les réponses à vos questions métier</h2>'
        '<p>Traçabilité, DLC, coût de revient, conformité : ce qu\'un ERP agroalimentaire '
        'doit savoir faire.</p></div>'
        '<div class="faq-cards-grid">%s</div></div>'
        '<div class="faq-drawer-overlay" id="faqDrawerOverlay" style="display:none">'
        '<div class="faq-drawer"><div class="faq-drawer-header">'
        '<button class="faq-drawer-close" onclick="closeFaqDrawer()" aria-label="Fermer">'
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg></button>'
        '<div class="faq-drawer-nav">'
        '<button class="faq-drawer-prev" onclick="navFaqDrawer(-1)" '
        'aria-label="Question précédente"><svg fill="none" stroke="currentColor" '
        'viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" '
        'stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button>'
        '<span class="faq-drawer-counter" id="faqDrawerCounter">1/%d</span>'
        '<button class="faq-drawer-next" onclick="navFaqDrawer(1)" '
        'aria-label="Question suivante"><svg fill="none" stroke="currentColor" '
        'viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" '
        'stroke-width="2" d="M9 5l7 7-7 7"/></svg></button>'
        '</div></div>'
        '<div class="faq-drawer-body" id="faqDrawerBody">%s</div>'
        '</div></div>'
        '</section>'
        '<script>'
        'var currentFaq=0,totalFaqs=%d;'
        'function openFaqDrawer(i){var o=document.getElementById("faqDrawerOverlay");'
        'if(!o)return;currentFaq=i;o.style.display="block";o.classList.remove("closing");'
        'o.classList.add("open");document.body.style.overflow="hidden";showFaqPanel(i)}'
        'function closeFaqDrawer(){var o=document.getElementById("faqDrawerOverlay");'
        'if(!o)return;o.classList.add("closing");o.classList.remove("open");'
        'setTimeout(function(){o.classList.remove("closing");o.style.display="none";'
        'document.body.style.overflow=""},250)}'
        'function navFaqDrawer(d){currentFaq=(currentFaq+d+totalFaqs)%%totalFaqs;'
        'showFaqPanel(currentFaq)}'
        'function showFaqPanel(i){var p=document.querySelectorAll(".faq-drawer-panel");'
        'if(!p.length)return;p.forEach(function(x){x.style.display="none"});'
        'if(p[i])p[i].style.display="block";'
        'var c=document.getElementById("faqDrawerCounter");'
        'if(c)c.textContent=(i+1)+"/"+totalFaqs}'
        '(function(){var o=document.getElementById("faqDrawerOverlay");if(!o)return;'
        'o.addEventListener("click",function(e){if(e.target===this)closeFaqDrawer()});'
        'document.addEventListener("keydown",function(e){'
        'if(!o.classList.contains("open"))return;'
        'if(e.key==="Escape")closeFaqDrawer();'
        'if(e.key==="ArrowRight")navFaqDrawer(1);'
        'if(e.key==="ArrowLeft")navFaqDrawer(-1)})})();'
        '</script>'
        % ("".join(cartes), len(qr), "".join(panneaux), len(qr)))


# ══════════════════════════════════════════════════════ outils de decoupe
def div_complet(c, i):
    """Renvoie la fin du <div> ouvert en i, en comptant ouvertures et fermetures."""
    n, k = 0, i
    for m in re.finditer(r"<div\b[^>]*>|</div\s*>", c[i:]):
        k = i + m.end()
        n += 1 if m.group(0).startswith("<div") else -1
        if n == 0:
            return k
    raise SystemExit("ARRET — <div> non referme")


def section(c, ouvrant):
    """Renvoie (debut, fin) de la section, bornes sur son </section> propre."""
    i = c.find(ouvrant)
    if i < 0:
        return None
    j = c.find("</section>", i)
    if j < 0:
        return None
    j += len("</section>")
    if "<section" in c[i + 10:j]:
        raise SystemExit("ARRET — section imbriquee : " + ouvrant[:50])
    return i, j


def retirer(c, ouvrant, quoi, prefixes=()):
    """Retire une section, puis les <style> et <script> qui ne servaient qu'elle."""
    b = section(c, ouvrant)
    if not b:
        raise SystemExit("ARRET — introuvable : " + quoi)
    i, j = b
    c = c[:i] + c[j:]
    n = 0
    for pref in prefixes:
        for m in list(re.finditer(r"<style[^>]*>(.*?)</style>", c, re.S))[::-1]:
            sel = set(re.findall(r"\.([a-zA-Z][\w-]+)", m.group(1)))
            if sel and all(x.startswith(pref) for x in sel):
                c = c[:m.start()] + c[m.end():]
                n += 1
    # Rien ne doit subsister dans le corps ; le CSS orphelin reste inerte.
    hors = re.sub(r"<(style|script)[^>]*>.*?</\1>", "", c, flags=re.S)
    reste = [p for p in prefixes if p in hors]
    if reste:
        raise SystemExit("ARRET — %s laisse des traces dans le corps : %s" % (quoi, reste))
    print("   · %-46s retiree (%d bloc(s) de style)" % (quoi, n))
    return c


def main():
    c = w.get_raw("pages", PAGE)["content"]["raw"]
    src = c
    print("page %d lue : %d octets\n" % (PAGE, len(c)))

    # ─── 1 & 2 — le quiz et le simulateur
    c = retirer(c, '<section class="hh2-quiz"', "1. quiz interactif", ("hh2-quiz",))
    for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S))[::-1]:
        if "qResTitle" in m.group(1) or "diagData" in m.group(1):
            c = c[:m.start()] + c[m.end():]
    c = retirer(c, '<section class="hh2-roi"', "2. simulateur de ROI", ("hh2-roi",))
    for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S))[::-1]:
        if "sliderCA" in m.group(1) or "resDLC" in m.group(1):
            c = c[:m.start()] + c[m.end():]

    # ─── 3 — « Qui sommes-nous » reprend la section des soeurs
    s = w.get_raw("pages", SOEUR)["content"]["raw"]
    bs = section(s, '<section class="about-card-section"')
    ba = section(c, '<section class="about-card-section"')
    if not bs or not ba:
        raise SystemExit("ARRET — section « qui sommes-nous » introuvable")
    c = c[:ba[0]] + s[bs[0]:bs[1]] + c[ba[1]:]
    print("   · 3. « Qui sommes-nous » reprise de la page %d (video comprise)" % SOEUR)

    # ─── 4 & 5 — les deux comparatifs
    c = retirer(c, '<section class="hh2-compare hh2-compare--alt"',
                "5. « Un déploiement 5x plus rapide »")
    c = retirer(c, '<section class="hh2-compare"',
                "4. « Ce qu'un ERP généraliste ne sait pas faire »", ("hh2-compare",))

    # ─── 6 — les cas clients deviennent le mur de logos
    b = section(c, '<section class="hh2-cas-clients"')
    if not b:
        raise SystemExit("ARRET — section des cas clients introuvable")
    images = []
    for rel, nom in LOGOS:
        d, lg, ht = logo_net(UP + rel)
        if d:
            images.append((d, nom, lg, ht))
        else:
            print("     ! logo non recupere :", rel)
    c = c[:b[0]] + mur_logos(images) + c[b[1]:]
    for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S))[::-1]:
        if "casTrack" in m.group(1) or "hh2-cas" in m.group(1) or "casClients" in m.group(1):
            c = c[:m.start()] + c[m.end():]
    print("   · 6. cas clients → mur de %d logos, quatre de front, en défilement" % len(images))

    # ─── 7 — la bande presse
    c = retirer(c, '<section class="hh2-trust-section"', "7. bande presse et garanties",
                ("hh2-trust",))

    # ─── 8 — la FAQ des soeurs, avec les questions de la page
    b = section(c, '<section class="hh2-faq-section"')
    if not b:
        raise SystemExit("ARRET — FAQ introuvable")
    bloc = c[b[0]:b[1]]
    qs = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
          for _, x in re.findall(r'<(h3|span|button)[^>]*itemprop="name"[^>]*>(.*?)</\1>',
                                 bloc, re.S)]
    rs = [re.sub(r"\s+", " ", x).strip() for x in
          re.findall(r'itemprop="text"[^>]*>(.*?)(?=</div>\s*</div>\s*</div>)', bloc, re.S)]
    if len(qs) != 8 or len(rs) != 8:
        raise SystemExit("ARRET — FAQ incomplete : %d questions, %d reponses" % (len(qs), len(rs)))
    c = c[:b[0]] + faq_soeur(list(zip(qs, rs))) + c[b[1]:]
    print("   · 8. FAQ → composant des pages sœurs, %d questions reprises" % len(qs))

    # ─── 9 — l'equipe : deja identique aux soeurs
    ea = section(c, '<section class="team-section"')
    es = section(s, '<section class="team-section"')
    pareil = ea and es and c[ea[0]:ea[1]] == s[es[0]:es[1]]
    print("   · 9. « Une équipe humaine » %s"
          % ("déjà identique aux sœurs, inchangée" if pareil else "DIFFÈRE des sœurs"))

    # ─── 10 — l'appel a l'action de bas de page
    c = retirer(c, '<section class="hh-demo-cta"', "10. CTA « démo personnalisée »",
                ("hh-demo",))

    # ─── 11 — les avis en carrousel continu, deux colonnes
    b = section(c, '<section class="reviews-section"')
    if not b:
        raise SystemExit("ARRET — section des avis introuvable")
    bloc = c[b[0]:b[1]]
    cartes = []
    for m in re.finditer(r'<div class="review-card">', bloc):
        cartes.append(bloc[m.start():div_complet(bloc, m.start())])
    if len(cartes) != 4:
        raise SystemExit("ARRET — %d carte(s) d'avis au lieu de 4" % len(cartes))
    grille = re.search(r'<div class="reviews-grid">.*?(?=</div>\s*</section>)', bloc, re.S)
    if not grille:
        raise SystemExit("ARRET — grille des avis introuvable")
    c = c[:b[0]] + bloc.replace(grille.group(0), avis_carrousel(cartes)) + c[b[1]:]
    print("   · 11. avis → carrousel continu, %d cartes, deux colonnes" % len(cartes))

    # ─── 12 — « Pour approfondir »
    b = section(c, '<section class="container" style="padding:1.5rem 0 2rem')
    if not b:
        raise SystemExit("ARRET — « Pour approfondir » introuvable")
    c = c[:b[0]] + c[b[1]:]
    print("   · 12. « Pour approfondir »                      retirée")

    # ─── 13 — la section guide, tout en bas, sous la banniere d'appel a l'action
    #
    # La couverture reprend la photo du hero : c'est elle que le lecteur
    # reconnait avant de lire le titre. Le voile sombre du gabarit monte du bas,
    # le titre reste donc lisible sur cette photo comme sur une autre.
    # Le cadrage a ete choisi sur le rendu, cinq essais compares : au centre,
    # le recadrage 3/4 d'une photo paysage coupait le visage.
    HERO = "2026/08/Screenshot-2026-02-14-08.34.42.webp"
    couv, _, _ = R.convertir(UP + HERO, 900, 74)
    if not couv:
        raise SystemExit("ARRET — photo du hero introuvable pour la couverture")
    i = c.find("<footer")
    if i < 0:
        raise SystemExit("ARRET — pied de page introuvable")
    if c.rfind('<section class="cta-banner"') > i:
        raise SystemExit("ARRET — la bannière d'appel à l'action n'est pas avant le pied")
    c = c[:i] + agro_ebook.section(
        titre="Comment bien choisir son ERP agroalimentaire",
        couverture=couv, cadrage="center 25%") + c[i:]
    liens = re.findall(r'href="([^"]+)"', agro_ebook.section(titre="x", couverture=None))
    print("   · 13. section guide ajoutée sous la bannière (%d liens, hub %s)"
          % (len(liens), agro_ebook.HUB))

    # ─── ce qu'impose l'artefact, et rien d'autre
    print()
    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    urls |= set(re.findall(r"url\(&#039;(https?://[^&]+\.(?:png|jpe?g|webp|svg|gif))&#039;\)", c))
    ok = 0
    for u in sorted(urls):
        d, _, _ = R.convertir(u)
        if d:
            c = c.replace(u, d)
            ok += 1
    rel = set(re.findall(r'(?:src|data-src)="(/wp-content/[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    for u in sorted(rel):
        d, _, _ = R.convertir("https://www.helloharel.com" + u)
        if d:
            c = c.replace('"%s"' % u, '"%s"' % d)
            ok += 1
    print("images intégrées : %d" % ok)

    c, faits = M.remplacer_video(c)
    for f in faits:
        print("  ", f)

    n = 0
    for cls, svg in M.SVG_FA.items():
        for balise in ('<i class="%s"></i>' % cls, '<i class="%s"/>' % cls):
            n += c.count(balise)
            c = c.replace(balise, svg)
    c = re.sub(r'<link[^>]+cdnjs\.cloudflare\.com[^>]*>', "", c)
    print("icônes Font Awesome remplacées par des SVG : %d" % n)

    html = ('<!doctype html><html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>ERP Agroalimentaire • Spécialiste PME • Depuis 2014 ☁️</title>'
            + POLICE + REPOS + '</head><body>' + c + '</body></html>')
    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\nécrit : %s  (%d ko)\n" % (SORTIE, len(html) // 1024))

    # ─── contrôles
    pb = []
    for m in re.finditer(r'<(img|source)[^>]+src="((?:https?:)?/[^"]*)"', html):
        pb.append("image non intégrée : " + m.group(2)[:70])
    if re.search(r"<iframe", html):
        pb.append("iframe : bloquée dans un artefact")
    if re.search(r'<i class="fa[sbr]? ', html):
        pb.append("il reste une icône Font Awesome sans police")
    for t in ("section", "details"):
        o, f = len(re.findall(r"<%s[\s>]" % t, html)), len(re.findall(r"</%s\s*>" % t, html))
        if o != f:
            pb.append("%s : %d ouvertes, %d fermées" % (t, o, f))
    if html.count("<h1") != 1:
        pb.append("il faut un seul H1, il y en a %d" % html.count("<h1"))
    ig, ib, ip = (html.find('id="guide-erp-agroalimentaire"'),
                  html.rfind('<section class="cta-banner"'), html.find("<footer"))
    if ig < 0:
        pb.append("la section guide est absente")
    elif not (ib < ig < ip):
        pb.append("la section guide n'est pas entre la bannière et le pied de page")
    for parti in ("hh2-quiz", "hh2-roi", "hh2-compare", "hh2-trust", "hh-demo-cta",
                  "hh2-cas-clients", "Pour approfondir"):
        corps = re.sub(r"<(style|script)[^>]*>.*?</\1>", "", html, flags=re.S)
        if parti in corps:
            pb.append("%s survit dans le corps" % parti)

    corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
    print("   sections   avant %2d   après %2d"
          % (len(re.findall(r"<section[\s>]", corps(src))),
             len(re.findall(r"<section[\s>]", corps(html)))))
    print("   H2         avant %2d   après %2d"
          % (len(re.findall(r"<h2[\s>]", corps(src))),
             len(re.findall(r"<h2[\s>]", corps(html)))))
    print("   liens      avant %2d   après %2d"
          % (len(re.findall(r'href="', corps(src))),
             len(re.findall(r'href="', corps(html)))))
    print()
    for x in pb:
        print("   !", x)
    print("contrôles : %s" % ("tout est vert" if not pb else "%d écart(s)" % len(pb)))


if __name__ == "__main__":
    main()
