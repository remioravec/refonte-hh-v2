#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maquette de /agroalimentaire/ : la page telle qu'elle est en ligne, avec la
section bento des fonctionnalites remplacee par les ecrans en flat design, et
une section guide ajoutee en bas de page.

MAQUETTE, PAS MISE EN LIGNE. /agroalimentaire/ est page 1726, protegee par la
regle 0 : ce script lit son contenu, il ne l'ecrit jamais.

L'artefact doit vivre sans le site : la politique de securite des artefacts
bloque toute image et toute feuille de style distante. Les images sont donc
converties en WebP et integrees en data URI, et la seule ressource externe
conservee est la police, servie par Google Fonts — le seul hote autorise.

Usage :  python3 maquette_agro.py
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
import wp_common as w   # noqa: E402
import agro_ui          # noqa: E402
import agro_ebook       # noqa: E402

PAGE = 1726
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
CACHE = os.path.join(S, "img")
SORTIE = os.path.join(S, "maquette-agro.html")
SITE = "https://www.helloharel.com"

POLICE = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
          'family=Urbanist:wght@400;500;600;700;800;900&display=swap">')

# Le site anime ses blocs a l'apparition. Dans une maquette, tout doit etre
# lisible a l'arret : on neutralise l'etat masque plutot que de parier sur le JS.
REPOS = """<style id="hh-maquette-repos">
#hh-page .scroll-reveal,#hh-page .metier-slide{opacity:1 !important;transform:none !important}
html{scroll-behavior:smooth}
body{background:#fff}
</style>"""


def convertir(url, largeur=1400):
    """Telecharge une image du site et la rend en data URI WebP."""
    os.makedirs(CACHE, exist_ok=True)
    nom = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/")[-1])
    brut = os.path.join(CACHE, nom)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", brut], timeout=90)
    if not os.path.exists(brut) or os.path.getsize(brut) < 200:
        return None
    if url.lower().endswith(".svg"):
        d = open(brut, "rb").read()
        return "data:image/svg+xml;base64," + base64.b64encode(d).decode()
    try:
        im = Image.open(brut)
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
        if im.width > largeur:
            im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=76, method=6)
        return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None


SVG_FA = {
    'fas fa-star': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
                   'style="width:1em;height:1em;display:inline-block;vertical-align:-.125em">'
                   '<path d="M12 2l2.9 6.26 6.85.78-5.09 4.64 1.4 6.74L12 17.1l-6.06 3.32 '
                   '1.4-6.74L2.25 9.04l6.85-.78z"/></svg>',
    'fab fa-linkedin-in': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
                   'style="width:1em;height:1em;display:inline-block;vertical-align:-.125em">'
                   '<path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zm7 0h3.8'
                   'v1.7h.05c.53-.95 1.83-1.95 3.77-1.95 4.03 0 4.78 2.5 4.78 5.76V21h-4v-5.6c0'
                   '-1.34-.03-3.06-1.9-3.06-1.9 0-2.2 1.45-2.2 2.96V21h-4z"/></svg>',
    'fab fa-google': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
                   'style="width:1em;height:1em;display:inline-block;vertical-align:-.125em">'
                   '<path d="M12 11v3.2h5.3a4.6 4.6 0 01-4.5 3.4 5.1 5.1 0 110-10.2c1.3 0 2.5.5'
                   ' 3.4 1.3l2.3-2.3A8.4 8.4 0 1012 20.5c4.8 0 8.2-3.4 8.2-8.2 0-.5 0-.9-.1-1.3z"'
                   '/></svg>',
    'fas fa-quote-left': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
                       'style="width:1em;height:1em;display:inline-block;vertical-align:-.125em">'
                       '<path d="M9.6 5.6A7.5 7.5 0 003 12.8V18a1 1 0 001 1h5.2a1 1 0 001-1v-5.2a1 '
                       '1 0 00-1-1H6.1c.2-1.9 1.5-3.4 3.5-3.9zM20.1 5.6a7.5 7.5 0 00-6.6 7.2V18a1 1 '
                       '0 001 1h5.2a1 1 0 001-1v-5.2a1 1 0 00-1-1h-3.1c.2-1.9 1.5-3.4 3.5-3.9z"/>'
                       '</svg>',
    'fab fa-youtube': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
                   'style="width:1em;height:1em;display:inline-block;vertical-align:-.125em">'
                   '<path d="M22 12s0-3.2-.4-4.7a2.5 2.5 0 00-1.8-1.8C18.3 5 12 5 12 5s-6.3 0-7.8'
                   '.5a2.5 2.5 0 00-1.8 1.8C2 8.8 2 12 2 12s0 3.2.4 4.7c.2.9.9 1.6 1.8 1.8 1.5.5'
                   ' 7.8.5 7.8.5s6.3 0 7.8-.5a2.5 2.5 0 001.8-1.8c.4-1.5.4-4.7.4-4.7zM10 15.2V8.8'
                   'l5.2 3.2z"/></svg>',
}



def remplacer_video(c):
    """Une <iframe> YouTube est bloquee dans un artefact : elle rend un cadre vide.

    On la remplace par la vignette de la video, integree, cliquable vers
    YouTube. La maquette montre ce que la page montre, sans faire croire a un
    lecteur qui ne demarrera pas.
    """
    faits = []
    for m in list(re.finditer(
            r'<iframe[^>]+src="https?://www\.youtube\.com/embed/([\w-]+)"[^>]*>\s*</iframe>',
            c))[::-1]:
        vid = m.group(1)
        vignette = convertir("https://img.youtube.com/vi/%s/maxresdefault.jpg" % vid, 1280)
        if not vignette:
            continue
        bloc = (
            '<a class="hh-video" href="https://www.youtube.com/watch?v=%s" target="_blank" '
            'rel="noopener" aria-label="Voir la vidéo de présentation Hello Harel sur YouTube" '
            'style="position:relative;display:block;line-height:0;border-radius:inherit;'
            'overflow:hidden">'
            '<img src="%s" alt="Vignette de la vidéo de présentation Hello Harel" '
            'style="width:100%%;height:100%%;object-fit:cover;display:block">'
            '<span style="position:absolute;inset:0;display:flex;align-items:center;'
            'justify-content:center;background:rgba(4,38,58,.28)">'
            '<span style="width:68px;height:68px;border-radius:50%%;background:#fff;'
            'display:flex;align-items:center;justify-content:center;'
            'box-shadow:0 10px 26px -10px rgba(0,0,0,.7)">'
            '<svg viewBox="0 0 24 24" width="26" height="26" fill="#00B1F5" '
            'aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></span></a>'
            % (vid, vignette))
        c = c[:m.start()] + bloc + c[m.end():]
        faits.append("video YouTube remplacee par sa vignette cliquable (%s)" % vid)
    return c, faits



def _jumeler(c, tag, remplacant):
    """Duplique chaque regle CSS qui vise <tag> pour viser aussi le remplacant.

    Permet de changer un niveau de titre sans perdre sa mise en forme : on
    ajoute des regles, on n'en retire aucune.
    """
    n = 0
    for m in list(re.finditer(r"<style[^>]*>(.*?)</style>", c, re.S))[::-1]:
        css, sup = m.group(1), []
        for r in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
            sel = r.group(1)
            if re.search(r"\b%s\b" % tag, sel):
                sup.append(re.sub(r"\b%s\b" % tag, remplacant, sel).strip()
                           + "{" + r.group(2) + "}")
                n += 1
        if sup:
            c = c[:m.end(1)] + "".join(sup) + c[m.end(1):]
    return c, n


def qualite(c):
    """Les correctifs releves par l'agent qualite, poses pour TOUTES les pages.

    Ils sont ici et non dans une rustine de fin de fichier : ce sont des
    defauts du gabarit du site, pas de la page produite.
    """
    faits = []

    # --- 1. Le pied de page passe SOUS le bouton flottant en mobile : trois
    #        liens legaux etaient inaccessibles.
    # --- 2. La barre d'onglets de l'ecran reproduit coupait « Producti » et
    #        masquait l'onglet actif sous 560 px.
    # --- 3. Le triangle de l'onglet actif etait ecrete par l'overflow du
    #        conteneur : remplace par un soulignement.
    # --- 4. Contrastes sous 4,5:1 sur les surtitres, les liens de carte, les
    #        sources d'avis et les deux appels a l'action du hero.
    # --- 5. Trente-six cibles tactiles sous 24 px dans le pied de page.
    # --- 6. En-tete transparent quand le menu mobile est ouvert.
    # --- 7. Aucun indice de defilement sur les tableaux des ecrans.
    c += ('<style id="hh-qualite">'
          '@media(max-width:1023px){#hh-page > footer{padding-bottom:8rem !important}}'
          '@media(max-width:560px){'
          '#hh-page .hhf .ui-nav span{display:none !important}'
          '#hh-page .hhf .ui-nav span.on{display:flex !important}}'
          '#hh-page .hhf .ui-nav span.on::after{left:0 !important;right:0 !important;'
          'bottom:0 !important;width:auto !important;height:2px !important;'
          'background:#fff !important;border:0 !important;transform:none !important}'
          '#hh-page .section-header .overline,#hh-page .card-link{color:#046C93 !important}'
          '#hh-page .section-label,#hh-page .review-source,'
          '#hh-page .testimonial-card cite{color:#64748B !important}'
          '#hh-page .hero-cta-sub{color:rgba(255,255,255,.92) !important;'
          'text-shadow:0 1px 3px rgba(0,0,0,.55) !important}'
          '#hh-page .hero-cta-primary,#hh-page .btn-demo-header{background:#15803D !important}'
          '#hh-page .hero-cta-secondary{background:transparent !important;'
          'border:2px solid #fff !important;color:#fff !important}'
          '#hh-page > footer a{display:inline-block !important;padding-block:5px !important;'
          'min-height:24px !important}'
          '#hh-page .card-link{padding-block:2px !important;min-height:24px !important}'
          'body.menu-open #hh-page .site-header{background:#0f172a !important;'
          'box-shadow:none !important}'
          '#hh-page .hhf .ui-tw{background:linear-gradient(90deg,#fff 30%,rgba(255,255,255,0)),'
          'linear-gradient(270deg,#fff 30%,rgba(255,255,255,0)) 100% 0,'
          'linear-gradient(90deg,rgba(15,23,42,.12),rgba(15,23,42,0)) 100% 0 !important;'
          'background-repeat:no-repeat !important;'
          'background-size:24px 100%,24px 100%,12px 100% !important;'
          'background-attachment:local,local,scroll !important}'
          '</style>')
    faits.append("pied de page degage du bouton flottant, contrastes, cibles tactiles")

    # --- 8. Le bouton du menu mobile etait deref sans garde : si l'id
    #        disparait, l'exception coupe le reveal et le carrousel.
    av = "document.getElementById('hamburgerBtn').addEventListener('click',"
    if av in c:
        c = c.replace(av, "(document.getElementById('hamburgerBtn')||{addEventListener:"
                          "function(){}}).addEventListener('click',")
        faits.append("bouton du menu mobile protege")

    # --- 9. Code mort : le tiroir de FAQ du gabarit n'est appele nulle part,
    #        et son contenu n'a rien a voir avec la page.
    if "openFaqDrawer(" not in re.sub(r"function openFaqDrawer[^)]*\)", "", c):
        for motif in (r'<div class="faq-drawer-overlay".*?</div>',
                      r'<div class="faq-drawer".*?</div>\s*</div>'):
            c2 = re.sub(motif, "", c, flags=re.S)
            if c2 != c:
                c = c2
        c2 = re.sub(r'<script>\s*var faqData=.*?</script>', "", c, flags=re.S)
        if c2 != c:
            c, _ = c2, faits.append("tiroir de FAQ inutilise retire")

    # --- 10. Sauts de niveau de titre : un h2 suivi d'un h4. On duplique
    #         d'abord les regles CSS pour que h3 herite de la mise en forme,
    #         PUIS on change la balise. L'inverse casserait l'affichage.
    c, n = _jumeler(c, "h4", "h3")
    for cls in ("team-section", "reviews-section"):
        i = c.find('<section class="%s"' % cls)
        if i < 0:
            continue
        j = c.find("</section>", i)
        z = c[i:j]
        if "<h4" in z:
            c = c[:i] + z.replace("<h4", "<h3").replace("</h4>", "</h3>") + c[j:]
    i = c.find("<footer")
    if i > 0:
        j = c.find("</footer>", i)
        z = c[i:j]
        if "<h4" in z:
            c = c[:i] + z.replace("<h4", "<h3").replace("</h4>", "</h3>") + c[j:]
    if n:
        faits.append("h4 ramenes en h3 (%d regles CSS jumelees)" % n)

    # --- 11. Le mega-menu ouvrait des h5 AVANT le h1 de la page. Ce sont des
    #         intertitres visuels, pas des niveaux de plan.
    c, n5 = _jumeler(c, "h5", ".mega-col-title")
    i = c.find('<header class="site-header"')
    if i > 0:
        j = c.find("</header>", i)
        z = c[i:j]
        if "<h5" in z:
            c = (c[:i] + z.replace("<h5", '<p class="mega-col-title"').replace("</h5>", "</p>")
                 + c[j:])
            faits.append("h5 du mega-menu passes en intertitres (%d regles jumelees)" % n5)

    return c, faits


def nettoyer(c):
    """Ce qui ne peut pas vivre dans un artefact : scripts tiers, liens absolus."""
    c = re.sub(r'<script[^>]+src="https?://(?!www\.helloharel\.com)[^"]+"[^>]*></script>', "", c)
    return c.replace('href="https://www.helloharel.com/', 'href="/')


def reparer(c):
    """Defauts releves en recette, presents AUSSI sur la page en ligne.

    Ils sont corriges dans la maquette et signales au client, jamais corriges
    en douce sur le site.
    """
    faits = []
    # le carrousel des cas clients appelle addEventListener sur deux fleches
    # qui n'ont jamais ete posees dans le markup : l'exception coupait le
    # script juste avant les clics sur les puces.
    for quoi in ("prev", "next"):
        av = "  %s.addEventListener('click'" % quoi
        ap = "  if (%s) %s.addEventListener('click'" % (quoi, quoi)
        if av in c:
            c = c.replace(av, ap)
            faits.append("carrousel des cas clients : %s protege" % quoi)

    LIB = {"linkedin.com/in/timothy": "Timothy Jollivet sur LinkedIn",
           "linkedin.com/in/nicolas": "Nicolas de Cerner sur LinkedIn",
           "linkedin.com/in/maxence": "Maxence Flavigny sur LinkedIn",
           "linkedin.com/company": "Hello Harel sur LinkedIn",
           "youtube.com/@HelloHarel": "Hello Harel sur YouTube"}
    for motif, lib in LIB.items():
        for m in list(re.finditer(r'<a href="([^"]*%s[^"]*)"' % re.escape(motif), c)):
            if "aria-label" not in c[m.start():m.start() + 220]:
                c = c[:m.end()] + ' aria-label="%s"' % lib + c[m.end():]
                faits.append("intitule accessible : %s" % lib)
                break

    # sur certaines pages le conteneur #hh-page se ferme trop tot : les avis
    # et le pied de page tombent en dehors, donc hors de son overflow-x: clip,
    # et le document defile lateralement de 40 px a toutes les largeurs. La
    # cause est un </div> mal place dans le markup ; le symptome se coupe en
    # une ligne, et la cause est signalee au client.
    faits.append("defilement horizontal coupe au niveau de <html>")

    # les puces du carrousel mesuraient 10 px, sous le minimum tactile.
    # La pastille garde sa taille, c'est la zone de clic qui grandit.
    c += ('<style id="hh-recette">'
          'html{overflow-x:clip}'
          '#hh-page .hh2-cas-clients__dot{position:relative}'
          '#hh-page .hh2-cas-clients__dot::after{content:"";position:absolute;'
          'left:50%;top:50%;transform:translate(-50%,-50%);width:24px;height:24px}'
          '</style>')
    faits.append("puces du carrousel : zone de clic portee a 24 px")

    c, g = gabarit(c)
    faits += g
    c, q = qualite(c)
    faits += q
    return c, faits


def _bloc(c, ouvrant, balise="div"):
    """Retourne (debut, fin) du bloc ouvert par `ouvrant`, accolades equilibrees."""
    i = c.find(ouvrant)
    if i < 0:
        return None
    prof, j = 0, i
    o, f = "<%s" % balise, "</%s>" % balise
    while j < len(c):
        a = c.find(o, j)
        b = c.find(f, j)
        if b < 0:
            return None
        if 0 <= a < b:
            prof += 1
            j = a + len(o)
        else:
            prof -= 1
            j = b + len(f)
            if prof == 0:
                return i, j
    return None


def gabarit(c):
    """Defauts du GABARIT, releves par l'agent de controle UX le 12/09/2026.

    Ils viennent de la page modele, donc ils sont sur toutes les pages du site.
    Corriges ici dans la maquette, signales au client, jamais touches en ligne.
    """
    faits = []

    # 1. Le H1 et le chapo du hero n'ont aucune classe : ils heritent du
    #    #hh-page{color:#101828} au lieu des .hero-title / .hero-description
    #    qui existent et valent #fff. Mesure sur la photo : 2,88:1 pour le H1
    #    (seuil 3), 2,83:1 pour le chapo (seuil 4,5).
    i = c.find('<section class="hero-section')
    if i > 0:
        j = c.find("</section>", i)
        h = c[i:j]
        n = h
        if "<h1>" in n:
            n = n.replace("<h1>", '<h1 class="hero-title">', 1)
        k = n.find("</h1>")
        if k > 0 and "<p>" in n[k:]:
            m = n.index("<p>", k)
            n = n[:m] + '<p class="hero-description">' + n[m + 3:]
        if n != h:
            c = c[:i] + n + c[j:]
            faits.append("hero : classes .hero-title et .hero-description posees")

    # 2. Les douze cartes d'equipe floutees. Un mur de portraits illisibles
    #    marques opacity .45 et filter:blur : la page annonce quinze personnes
    #    et en montre trois. On garde les trois reelles.
    n = 0
    while True:
        b = _bloc(c, '<div class="team-card scroll-reveal" style="opacity:0.45;')
        if not b:
            break
        c = c[:b[0]] + c[b[1]:]
        n += 1
    if n:
        faits.append("equipe : %d cartes floutees retirees" % n)

    # 3. Les accents manquants du carrousel des metiers. Sur une page
    #    francophone, c'est le signal « genere » le plus visible.
    ACC = {"Stocks Multi-Depots": "Stocks multi-dépôts",
           "Tracabilite par lots": "Traçabilité par lots",
           "inter-depots": "inter-dépôts",
           "conformite reglementaire": "conformité réglementaire",
           "EDI integre": "EDI intégré",
           "negociation tarifaire": "négociation tarifaire",
           "temps reel": "temps réel"}
    n = 0
    for a, b in ACC.items():
        if ">" + a in c or " " + a in c:
            n += c.count(a)
            c = c.replace(a, b)
    if n:
        faits.append("carrousel des metiers : %d libelles reaccentues" % n)

    # 4. Le nom et la fonction colles dans le temoignage.
    if "<strong>Julien Benguigui</strong>Co-fondateur" in c:
        c = c.replace("<strong>Julien Benguigui</strong>Co-fondateur",
                      "<strong>Julien Benguigui</strong> — Co-fondateur")
        faits.append("temoignage : separateur entre le nom et la fonction")

    # 5. Doublon : « Ils nous font confiance » en petit sous le hero ET en H2
    #    de la section des avis.
    if c.count("Ils nous font confiance") > 1:
        i = c.find('<section class="reviews-section')
        if i < 0:
            i = c.find('<section class="testimonial-section')
        if i > 0:
            j = c.find("Ils nous font confiance", i)
            if j > 0:
                c = c[:j] + "Ce qu'en disent nos clients" + c[j + len("Ils nous font confiance"):]
                faits.append("doublon « Ils nous font confiance » leve")

    # 6. Tout le reste passe par la feuille : specificite, contraste, rayons.
    c += """<style id="hh-gabarit">
/* rythme de l'article : .hha-art h2 etait battu par #hh-page h2{margin:0} */
#hh-page .hha-art h2{margin:3.2rem 0 1.2rem !important;font-size:1.75rem !important;line-height:1.25 !important}
#hh-page .hha-art h3{margin:2.4rem 0 .8rem !important}
#hh-page .hha-art p{margin:0 0 1.25rem !important}
#hh-page .hha-art ul,#hh-page .hha-art ol{margin:1.1rem 0 1.7rem !important;padding-left:1.4rem !important}
#hh-page .hha-art li{margin:.55rem 0 !important}
/* le bouton flottant couvrait le contenu au centre de l'ecran */
#hh-page .sticky-cta,.sticky-cta{left:auto !important;right:1.5rem !important;transform:none !important}
#hh-page .sticky-cta a,.sticky-cta a{color:#06283D !important}
@media(max-width:700px){#hh-page .sticky-cta,.sticky-cta{right:.75rem !important;bottom:.75rem !important}}
/* un seul bleu de texte, un seul bleu de fond porteur de blanc */
#hh-page .overline,#hh-page .card-link,#hh-page .section-label{color:#046C93 !important}
#hh-page .timeline-circle,#hh-page .review-avatar{background:#0079B8 !important}
/* les liens de carte etaient a des hauteurs differentes selon la longueur du texte */
#hh-page .metier-slide{display:flex !important;flex-direction:column !important}
#hh-page .metier-slide .card-link{margin-top:auto !important}
/* deux niveaux de carte, un seul rayon, une seule bordure */
#hh-page .metier-slide,#hh-page .timeline-card,#hh-page .team-card,
#hh-page .about-card,#hh-page .review-card{border-radius:16px !important;
 border:1px solid #E2E8F0 !important;box-shadow:0 1px 3px rgba(16,24,40,.08) !important}
/* les fleches du carrousel mordaient sur la premiere carte, et disparaissaient en mobile */
#hh-page .carousel-prev{left:-20px !important}
#hh-page .carousel-next{right:-20px !important}
@media(max-width:1023px){#hh-page .carousel-arrow{display:none !important}}
/* le tableau des ecrans se coupait sans le dire : on degrade le bord droit */
@media(max-width:560px){#hh-page .hhf .ui-tw{-webkit-mask-image:linear-gradient(to right,#000 calc(100% - 26px),transparent);
 mask-image:linear-gradient(to right,#000 calc(100% - 26px),transparent)}}
</style>"""
    faits.append("gabarit : rythme, contraste, rayons et debordements corriges en feuille")
    return c, faits


def controler(html):
    pb = []
    if len(html) > 15_500_000:
        pb.append("depasse la limite de 16 Mo d'un artefact")
    for m in re.finditer(r'<(img|source)[^>]+src="(https?://[^"]+)"', html):
        pb.append("image distante non integree : " + m.group(2)[:70])
    for m in re.finditer(r'<iframe[^>]+src="(https?://[^"]+)"', html):
        pb.append("iframe distante, bloquee dans un artefact : " + m.group(1)[:70])
    for m in re.finditer(r'<link[^>]+rel="stylesheet"[^>]+href="(https?://[^"]+)"', html):
        if "fonts.googleapis.com" not in m.group(1):
            pb.append("feuille de style distante bloquee : " + m.group(1)[:70])
    if re.search(r'<i class="fa[sbr]? ', html):
        pb.append("il reste une icone Font Awesome sans police")
    # « <section » en simple sous-chaine attrape « i<sections.length » dans un
    # script : on exige une vraie balise.
    ouvertes = len(re.findall(r"<section[\s>]", html))
    fermees = len(re.findall(r"</section\s*>", html))
    if ouvertes != fermees:
        pb.append("sections non refermees : %d ouvertes, %d fermees" % (ouvertes, fermees))
    # Un script qui s'adresse a un element absent leve une exception et coupe
    # tout ce qui le suit dans le meme bloc. C'est le defaut le plus couteux
    # et le plus silencieux d'une page assemblee a la main.
    # Une cible absente n'est pas forcement un bug : le script peut la
    # proteger par un if. Ce qui casse, c'est le dereferencement NON protege :
    # l'exception coupe tout ce qui suit dans le meme bloc.
    for m in re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.S):
        t = m.group(1)
        for var, quoi, cible in re.findall(
                r"(?:var|let|const)\s+(\w+)\s*=\s*document\."
                r"(getElementById|querySelector)\(\s*['\"]([^'\"]+)", t):
            present = (('id="%s"' % cible) in html) if quoi == "getElementById" else (
                cible.lstrip(".#") in html)
            if present:
                continue
            # La variable peut etre testee n'importe ou dans une condition, pas
            # seulement juste apres le if : « if (a && b && r2) » protege r2.
            protege = any(re.search(r"\b%s\b" % re.escape(var), cond)
                          for cond in re.findall(r"if\s*\(([^)]*)\)", t)) \
                or re.search(r"%s\s*&&" % re.escape(var), t)
            usage = re.search(r"\b%s\s*\." % re.escape(var), t)
            if usage and not protege:
                pb.append("script : %s (%s) est absent et dereference sans garde"
                          % (cible, var))

    return pb


def main():
    c = w.get_raw("pages", PAGE)["content"]["raw"]
    print("page %d lue : %d octets" % (PAGE, len(c)))

    # 1 — la section bento devient les ecrans.
    #     La borne de fin est le </section> qui ferme le bloc, PAS le <section>
    #     suivant : entre les deux vivent des blocs <style> qui appartiennent a
    #     la section d'apres. Couper au <section> suivant emportait la feuille
    #     de style du quiz, dont les deux boutons d'appel a l'action.
    i = c.find('<section class="features-section"')
    j = c.find('</section>', i)
    if i < 0 or j < 0:
        raise SystemExit("ARRET — section des fonctionnalites introuvable")
    j += len('</section>')
    if '<section' in c[i + 10:j]:
        raise SystemExit("ARRET — section imbriquee, la borne de fin est fausse")
    ancienne = c[i:j]
    entete = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="bento-grid")',
                       ancienne, re.S)
    if not entete:
        raise SystemExit("ARRET — en-tete de section introuvable")
    c = c[:i] + agro_ui.section(entete.group(0)) + c[j:]
    print("bento remplace : %d octets -> %d octets" % (len(ancienne), len(agro_ui.section(entete.group(0)))))

    # 2 — le simulateur de ROI est retire : apres le quiz, on enchaine
    #     directement sur « a propos ». Son bloc de style dedie part avec lui.
    i = c.find('<section class="hh2-roi"')
    if i < 0:
        raise SystemExit("ARRET — section du simulateur introuvable")
    j = c.find('</section>', i)
    if j < 0 or '<section' in c[i + 10:j]:
        raise SystemExit("ARRET — borne de fin du simulateur incertaine")
    c = c[:i] + c[j + len('</section>'):]

    # Le calculateur a son <script> POSE APRES son </section> : sans ses
    # curseurs il levait une exception au chargement, ce qui coupait la suite
    # du fichier. On le retire avec la section qu'il pilote.
    for m in list(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.S))[::-1]:
        if "sliderCA" in m.group(1) or "resDLC" in m.group(1):
            c = c[:m.start()] + c[m.end():]
    for m in list(re.finditer(r'<style[^>]*>(.*?)</style>', c, re.S))[::-1]:
        sel = set(re.findall(r'\.([a-zA-Z][\w-]+)', m.group(1)))
        if sel and all(x.startswith("hh2-roi") for x in sel):
            c = c[:m.start()] + c[m.end():]
    # Les regles CSS du simulateur survivent dans la grande feuille commune :
    # sans markup pour les porter, elles sont inertes. Ce qui compte, c'est
    # qu'il ne reste aucune trace dans le corps de la page.
    hors_css = re.sub(r'<style[^>]*>.*?</style>', "", c, flags=re.S)
    reste = len(re.findall(r'hh2-roi', hors_css))
    print("simulateur de ROI retire (%d reference(s) dans le corps)" % reste)
    if reste:
        raise SystemExit("ARRET — il reste des references au simulateur dans le corps")

    # 3 — le guide, juste avant la banniere finale
    k = c.rfind('<section class="cta-banner"')
    if k < 0:
        k = c.rfind('</div>')
    c = c[:k] + agro_ebook.section(
        couverture=agro_ebook.en_data_uri(
            os.path.join(S, "couverture-agroalimentaire.webp"))) + c[k:]
    print("section guide inseree")

    # 4 — les images, integrees
    urls = set(re.findall(r'(?:src|data-src)="(https?://[^"]+\.(?:png|jpe?g|webp|svg|gif))"', c))
    urls |= set(re.findall(r"url\('?(https?://[^)']+\.(?:png|jpe?g|webp|svg|gif))'?\)", c))
    urls |= set(re.findall(r"url\(&#039;(https?://[^&]+\.(?:png|jpe?g|webp|svg|gif))&#039;\)", c))
    ok = ko = 0
    for u in sorted(urls):
        d = convertir(u)
        if d:
            c = c.replace(u, d)
            ok += 1
        else:
            ko += 1
            print("   ! image non recuperee :", u[:90])
    print("images integrees : %d (%d en echec)" % (ok, ko))

    # 5 — Font Awesome est servi par un CDN que la politique de securite des
    #     artefacts refuse pour les feuilles de style. Les 34 icones sont donc
    #     remplacees par des SVG en ligne, qui ne dependent de personne.
    n = 0
    for cls, svg in SVG_FA.items():
        for balise in ('<i class="%s"></i>' % cls, '<i class="%s"/>' % cls):
            n += c.count(balise)
            c = c.replace(balise, svg)
    c = re.sub(r'<link[^>]+cdnjs\.cloudflare\.com[^>]*>', "", c)
    print("icones Font Awesome remplacees par des SVG : %d" % n)

    # 6 — defauts releves en recette, corriges ici et signales au client
    c, corrections = reparer(c)
    c, faits = remplacer_video(c)
    corrections += faits
    for x in corrections:
        print("   ·", x)

    # 7 — ce qui ne peut pas vivre dans un artefact
    c = nettoyer(c)

    html = ("<title>ERP agroalimentaire — maquette</title>\n" + POLICE + "\n" + REPOS + "\n" + c)
    open(SORTIE, "w", encoding="utf-8").write(html)
    print("\necrit : %s  (%d ko)" % (SORTIE, len(html) // 1024))

    pb = controler(html)
    for x in pb:
        print("   !", x)
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
