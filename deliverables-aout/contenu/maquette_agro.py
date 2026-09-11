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
    if html.count("<section") != html.count("</section>"):
        pb.append("sections non refermees")
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
            protege = re.search(r"if\s*\(\s*!?\s*%s\s*[)&]" % re.escape(var), t) \
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
