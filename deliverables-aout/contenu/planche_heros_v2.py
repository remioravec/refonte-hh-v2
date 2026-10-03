#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Planche des heros metier — etat REEL du site, relu page par page.

Pourquoi une v2 : la premiere planche etait faite de captures d'ecran prises
par un service tiers. Elle montrait donc aussi les defauts du gabarit, dont
celui qui rendait le titre illisible — le <h1> et le chapo n'avaient aucune
classe et heritaient du noir du corps de page au lieu du blanc prevu.

Ici on reconstruit chaque hero a partir de ses elements reels, lus par l'API :
la photo de fond, le badge, le H1 et le chapo de la page. Les classes du hero
sont posees comme elles devraient l'etre. On voit donc l'image de chaque page
metier, et ce que le hero donne une fois le defaut corrige.

Les cinq pages protegees sont affichees et signalees ; rien n'y est ecrit.

Usage :  python3 planche_heros_v2.py
"""

import base64
import html
import io as _io
import os
import re
import subprocess
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
CACHE = os.path.join(S, "heros")
SORTIE = os.path.join(S, "planche-heros-v2.html")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

PAGES = [
 ("/agroalimentaire/", 1726, "Agroalimentaire", "page mère"),
 ("/agroalimentaire/boulanger/", 3309, "Boulanger", ""),
 ("/agroalimentaire/brasseur/", 10896, "Brasseur", ""),
 ("/agroalimentaire/charcutier/", 2818, "Charcutier", ""),
 ("/agroalimentaire/chocolatier/", 10894, "Chocolatier", ""),
 ("/agroalimentaire/conserverie/", 10933, "Conserverie", ""),
 ("/agroalimentaire/fromager/", 10867, "Fromager", ""),
 ("/agroalimentaire/glacier/", 10895, "Glacier", ""),
 ("/agroalimentaire/industrie-laitiere/", 5470, "Industrie laitière", ""),
 ("/agroalimentaire/maraicher/", 2824, "Fruits et légumes", ""),
 ("/agroalimentaire/patissier/", 10865, "Pâtissier", ""),
 ("/agroalimentaire/plats-cuisines-industriels/", 5477, "Plats cuisinés", ""),
 ("/agroalimentaire/poissonnier/", 10868, "Poissonnier", ""),
 ("/agroalimentaire/torrefacteur/", 10935, "Torréfacteur", ""),
 ("/agroalimentaire/traiteur/", 2839, "Traiteur", ""),
 ("/agroalimentaire/viande/", 11332, "Viande", ""),
 ("/negoce/", 5957, "Négoce", "page porteuse"),
 ("/migration-as400/", 11162, "Migration AS/400", ""),
]


def _texte(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x or "")).strip()


def lire(pid):
    """Photo de fond, badge, H1 et chapo, tels qu'ils sont en ligne."""
    c = w.get_raw("pages", pid)["content"]["raw"]
    i = c.find('<section class="hero-section')
    if i < 0:
        return None
    j = c.find("</section>", i)
    h = c[i:j]
    img = re.search(r"url\('([^']+)'\)", h)
    badge = re.search(r'<div class="hero-badge">(.*?)</div>', h, re.S)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    p = re.search(r"</h1>\s*<p[^>]*>(.*?)</p>", h, re.S)
    return {"img": img.group(1) if img else None,
            "badge": _texte(badge.group(1)) if badge else "",
            "h1": _texte(h1.group(1)) if h1 else "",
            "chapo": _texte(p.group(1)) if p else ""}


def vignette(url, largeur=760):
    """Telecharge la photo du hero et la reduit, pour tenir dans un artefact."""
    if not url:
        return None, "aucune photo de fond"
    nom = url.split("/")[-1]
    brut = os.path.join(CACHE, nom)
    if not os.path.exists(brut) or os.path.getsize(brut) < 4000:
        r = subprocess.run(["curl", "-sSL", "-A", "Mozilla/5.0", url, "-o", brut,
                            "-w", "%{http_code}"], capture_output=True, text=True)
        if r.stdout.strip() != "200":
            return None, "HTTP %s sur %s" % (r.stdout.strip(), nom)
    try:
        im = Image.open(brut).convert("RGB")
    except Exception as e:
        return None, "illisible : %s" % e
    r = largeur / im.width
    im = im.resize((largeur, round(im.height * r)), Image.LANCZOS)
    b = _io.BytesIO()
    for q in (72, 64, 56, 48):
        b = _io.BytesIO()
        im.save(b, "WEBP", quality=q, method=6)
        if b.tell() <= 90_000:
            break
    return ("data:image/webp;base64," + base64.b64encode(b.getvalue()).decode(), nom)


CSS = """<style>
:root{--pap:#F4F6F4;--surf:#fff;--enc:#161A17;--enc2:#4C544E;--enc3:#7E8781;
 --trait:#DDE2DD;--bleu:#046C93;--rouge:#B3261E}
*{box-sizing:border-box}
body{margin:0;background:var(--pap);color:var(--enc);
 font:16px/1.55 'Archivo',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:2.5rem 1rem 5rem}
header.t{border-bottom:2px solid var(--enc);padding-bottom:1.2rem;margin-bottom:2.2rem}
header.t p.k{margin:0 0 .5rem;font-size:.72rem;font-weight:600;letter-spacing:.16em;
 text-transform:uppercase;color:var(--bleu)}
header.t h1{margin:0 0 .6rem;font-size:clamp(1.6rem,4vw,2.4rem);line-height:1.15;
 letter-spacing:-.02em}
header.t p.s{margin:0;color:var(--enc2);max-width:62ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:1.6rem}
.card{background:var(--surf);border:1px solid var(--trait);border-radius:16px;
 overflow:hidden;box-shadow:0 1px 3px rgba(16,24,40,.08);display:flex;flex-direction:column}
.hero{position:relative;aspect-ratio:16/9;overflow:hidden;display:block;text-decoration:none}
.hero img{width:100%;height:100%;object-fit:cover;display:block}
.hero .voile{position:absolute;inset:0;
 background:linear-gradient(rgba(0,50,80,.55),rgba(0,100,160,.6))}
.hero .txt{position:absolute;inset:0;padding:1rem 1.1rem;display:flex;
 flex-direction:column;justify-content:center;gap:.45rem}
.hero .bdg{align-self:flex-start;font-size:.62rem;font-weight:600;letter-spacing:.04em;
 color:#fff;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28);
 border-radius:99px;padding:.22rem .6rem;backdrop-filter:blur(4px)}
.hero .h{margin:0;color:#fff;font-size:1.05rem;line-height:1.2;font-weight:800;
 letter-spacing:-.01em;text-shadow:0 1px 12px rgba(0,0,0,.28)}
.hero .c{margin:0;color:rgba(255,255,255,.86);font-size:.74rem;line-height:1.45;
 display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.meta{padding:.85rem 1.1rem 1rem;border-top:1px solid var(--trait);flex:1}
.meta h2{margin:0 0 .25rem;font-size:1rem;letter-spacing:-.01em}
.meta .u{margin:0 0 .45rem;font-size:.76rem;color:var(--enc2);word-break:break-all}
.meta .f{margin:0;font:.68rem/1.45 'IBM Plex Mono',ui-monospace,monospace;color:var(--enc3);
 word-break:break-all}
.tag{display:inline-block;font-size:.62rem;font-weight:700;letter-spacing:.05em;
 text-transform:uppercase;border-radius:99px;padding:.15rem .5rem;margin-left:.35rem;
 vertical-align:.1em}
.tag.p{background:#FDECEA;color:var(--rouge)}
.tag.d{background:#FEF6E6;color:#8A5A00}
.note{margin:2.4rem 0 0;padding:1rem 1.2rem;background:#fff;border:1px solid var(--trait);
 border-radius:14px;color:var(--enc2);font-size:.88rem}
.note b{color:var(--enc)}
@media(max-width:520px){.wrap{padding:1.5rem .9rem 3rem}.grid{grid-template-columns:1fr}}
</style>"""


def main():
    os.makedirs(CACHE, exist_ok=True)
    cartes, pb, fichiers = [], [], {}
    for url, pid, nom, mention in PAGES:
        d = lire(pid)
        if not d:
            pb.append("%s : hero introuvable" % url)
            continue
        uri, fichier = vignette(d["img"])
        if not uri:
            pb.append("%s : %s" % (url, fichier))
        fichiers.setdefault(fichier, []).append(nom)
        tags = ""
        if pid in PROTEGEES:
            tags += '<span class="tag p">protégée</span>'
        if mention:
            tags += '<span class="tag d">%s</span>' % mention
        visuel = ('<img src="%s" alt="Photo de hero de la page %s" loading="lazy">' % (uri, nom)
                  if uri else '<div style="background:#DDE2DD;width:100%;height:100%"></div>')
        cartes.append(
            '<article class="card">'
            '<a class="hero" href="https://www.helloharel.com%s" target="_blank" rel="noopener">'
            '%s<span class="voile"></span><span class="txt">'
            '%s<span class="h">%s</span><span class="c">%s</span></span></a>'
            '<div class="meta"><h2>%s%s</h2><p class="u">%s · ID %d</p>'
            '<p class="f">%s</p></div></article>'
            % (url, visuel,
               ('<span class="bdg">%s</span>' % html.escape(d["badge"])) if d["badge"] else "",
               html.escape(d["h1"]), html.escape(d["chapo"][:150]),
               nom, tags, url, pid, html.escape(fichier or "—")))

    # Un partage est VOULU : la page mere /agroalimentaire/ et la page fruits et
    # legumes montrent la meme scene de cagettes de tomates, a la demande du
    # client. Tous les autres partages sont des defauts.
    VOULU = {("Agroalimentaire", "Fruits et légumes")}
    doublons = {f: v for f, v in fichiers.items() if f and len(v) > 1}
    defauts = {f: v for f, v in doublons.items() if tuple(v) not in VOULU}
    lignes = []
    if not defauts:
        lignes.append("Chaque métier porte sa propre scène. Aucune image n'est "
                      "partagée par accident.")
    for f, v in defauts.items():
        lignes.append("<b>%s</b> sert de fond à %s. Les deux pages sont protégées : "
                      "la photo ne peut être remplacée qu'avec votre feu vert."
                      % (f, " et ".join(v)))
    for f, v in doublons.items():
        if tuple(v) in VOULU:
            lignes.append("<b>%s</b> est volontairement partagée par %s."
                          % (f, " et ".join(v)))
    note = "<br>".join(lignes)

    corps = ('<title>Héros des pages métier</title>' + CSS
             + '<div class="wrap"><header class="t"><p class="k">Hello Harel · '
               'relevé du 12 septembre 2026</p>'
               '<h1>Les héros des pages métier</h1>'
               '<p class="s">La photo, le badge, le titre et le chapô de chaque page, lus en '
               'direct sur le site. Le titre s\'affiche ici en blanc, comme il devrait '
               'l\'être : en ligne, le H1 et le chapô n\'ont aucune classe et héritent du noir '
               'du corps de page, ce qui les rend illisibles sur la photo. Le correctif est '
               'dans les maquettes.</p></header>'
             + '<div class="grid">' + "".join(cartes) + '</div>'
             + '<p class="note">%s</p>' % note
             + '<p class="note">Les cinq pages marquées <b>protégée</b> ne reçoivent aucune '
               'modification : ni URL, ni gabarit, ni titre, ni structure.</p>'
             + '</div>')
    open(SORTIE, "w", encoding="utf-8").write(corps)
    print("ecrit : %s (%d ko, %d pages)" % (SORTIE, len(corps) // 1024, len(cartes)))
    for x in pb:
        print("   !", x)
    if doublons:
        print("   ! images partagees :", doublons)
    if not pb and not doublons:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
