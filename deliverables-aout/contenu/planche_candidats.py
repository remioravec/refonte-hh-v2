#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page metier par page metier : le hero actuel, et trois ou quatre remplacants.

Comment les candidats ont ete choisis — a l'oeil, pas par un score. Pour
chacun des dix-sept metiers, quatre requetes Pexels orientees production ont
sorti une quinzaine de photos ; les quinze ont ete montees en planche contact
et REGARDEES une par une. Ce qui a fait le tri :
  · un vrai lieu de travail, pas un decor de studio ni une cuisine de maison ;
  · un geste de metier lisible — le fournier qui enfourne, la main dans le bac
    de refroidissement du torrefacteur, le tranchage du caille, le dressage en
    serie, la palette qu'on tire dans l'allee ;
  · un decor credible en Europe, aux codes du metier ;
  · format paysage, au moins 1600 px de large.

On ne trie pas les personnes sur leur couleur de peau. On trie le lieu, le
geste et la credibilite de la scene ; le choix final revient au client.

Licence : Pexels, utilisation commerciale libre, sans attribution obligatoire.
Le photographe est cite malgre tout, et chaque vignette renvoie a sa page.

Usage :  python3 planche_candidats.py
"""

import base64
import html
import io as _io
import json
import os
import subprocess
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
CACHE_HERO = os.path.join(S, "heros")
CACHE_PX = os.path.join(S, "heros2/src")
SORTIE = os.path.join(S, "candidats-heros.html")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

# (url, id de page, libelle, [candidats Pexels], note eventuelle)
PLAN = [
 ("/agroalimentaire/", 1726, "Agroalimentaire — page mère",
  [2889093, 32578355, 11679687, 8877381], ""),
 ("/agroalimentaire/boulanger/", 3309, "Boulanger",
  [36445171, 36445354, 36445548, 30918892], ""),
 ("/agroalimentaire/brasseur/", 10896, "Brasseur",
  [5532998, 5532995, 5532988, 1267348], ""),
 ("/agroalimentaire/charcutier/", 2818, "Charcutier",
  [7163993, 29346647, 18882519, 30557313], ""),
 ("/agroalimentaire/chocolatier/", 10894, "Chocolatier",
  [6035326, 6035334, 6035990, 29188957], ""),
 ("/agroalimentaire/conserverie/", 10933, "Conserverie",
  [5532660, 5532719, 5532711, 5532675],
  "Pexels n'a pas de scène de conserverie avec un opérateur : les quatre "
  "propositions sont des vues de ligne. À défaut, une photo de terrain serait "
  "à commander."),
 ("/agroalimentaire/fromager/", 10867, "Fromager",
  [8287391, 5953721, 9424540, 8287395], ""),
 ("/agroalimentaire/glacier/", 10895, "Glacier",
  [4916466, 449730, 20732658, 1028432],
  "Le fonds est pauvre : l'essentiel des photos de glace sont des cornets en "
  "studio. Les quatre retenues sont ce qui se rapproche le plus d'un labo."),
 ("/agroalimentaire/industrie-laitiere/", 5470, "Industrie laitière",
  [5953801, 5953805, 5953794, 5953685], ""),
 ("/agroalimentaire/maraicher/", 2824, "Fruits et légumes",
  [8475178, 11678431, 34936950, 12519455], ""),
 ("/agroalimentaire/patissier/", 10865, "Pâtissier",
  [33393555, 5908284, 20194906, 19498989], ""),
 ("/agroalimentaire/plats-cuisines-industriels/", 5477, "Plats cuisinés",
  [29226707, 7124346, 17318176, 5531288], ""),
 ("/agroalimentaire/poissonnier/", 10868, "Poissonnier",
  [8352778, 30811293, 8352350, 21813752], ""),
 ("/agroalimentaire/torrefacteur/", 10935, "Torréfacteur",
  [4820817, 4820732, 4820655, 7176000], ""),
 ("/agroalimentaire/traiteur/", 2839, "Traiteur",
  [15671274, 2977515, 15671410, 2696064], ""),
 ("/agroalimentaire/viande/", 11332, "Viande",
  [7163987, 7163988, 7163991, 7163990], ""),
 ("/negoce/", 5957, "Négoce alimentaire",
  [4487382, 4487365, 4481531, 4483861],
  "La photo posée le 16/09 à votre demande — l'épicier et ses cagettes — est "
  "celle qui est en place ci-contre. Les quatre propositions sont des "
  "alternatives entrepôt, si vous voulez un registre plus négoce."),
]


def _uri(im, q=62, maxi=95_000):
    b = _io.BytesIO()
    for qq in (q, 54, 46, 38):
        b = _io.BytesIO()
        im.save(b, "WEBP", quality=qq, method=6)
        if b.tell() <= maxi:
            break
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()


def hero(pid):
    c = w.get_raw("pages", pid)["content"]["raw"]
    import re
    m = re.search(r'<section class="hero-section"[^>]*url\(\'([^\']+)\'\)', c)
    if not m:
        return None, "hero introuvable"
    u = m.group(1)
    nom = u.split("/")[-1]
    f = os.path.join(CACHE_HERO, nom)
    if not os.path.exists(f) or os.path.getsize(f) < 4000:
        subprocess.run(["curl", "-sSL", "-A", "Mozilla/5.0", u, "-o", f], capture_output=True)
    try:
        im = Image.open(f).convert("RGB")
    except Exception:
        return None, nom
    r = 460 / im.width
    return _uri(im.resize((460, round(im.height * r)), Image.LANCZOS)), nom


META = {}
for f in os.listdir(os.path.join(S, "heros2/planches")):
    if f.endswith(".json"):
        for e in json.load(open(os.path.join(S, "heros2/planches", f))):
            META[e["id"]] = e


def candidat(pid):
    f = os.path.join(CACHE_PX, "%d.jpg" % pid)
    if not os.path.exists(f) or os.path.getsize(f) < 4000:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0",
                        "https://images.pexels.com/photos/%d/pexels-photo-%d.jpeg"
                        "?auto=compress&cs=tinysrgb&w=1000" % (pid, pid), "-o", f],
                       capture_output=True)
    try:
        im = Image.open(f).convert("RGB")
    except Exception:
        return None
    r = 460 / im.width
    e = META.get(pid, {})
    return {"uri": _uri(im.resize((460, round(im.height * r)), Image.LANCZOS)),
            "id": pid, "ph": e.get("ph", "Pexels"),
            "url": e.get("url", "https://www.pexels.com/photo/%d/" % pid),
            "dim": "%s × %s" % (e.get("w", "?"), e.get("h", "?")),
            "alt": e.get("alt", "")}


CSS = """<style>
:root{--pap:#F4F6F4;--surf:#fff;--enc:#161A17;--enc2:#4C544E;--enc3:#7E8781;
 --trait:#DDE2DD;--bleu:#046C93;--rouge:#B3261E;--vert:#0F7A45}
*{box-sizing:border-box}
body{margin:0;background:var(--pap);color:var(--enc);
 font:16px/1.55 'Archivo',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:2.5rem 1rem 5rem}
header.t{border-bottom:2px solid var(--enc);padding-bottom:1.3rem;margin-bottom:1.6rem}
header.t p.k{margin:0 0 .5rem;font-size:.72rem;font-weight:600;letter-spacing:.16em;
 text-transform:uppercase;color:var(--bleu)}
header.t h1{margin:0 0 .7rem;font-size:clamp(1.6rem,4vw,2.4rem);line-height:1.15;
 letter-spacing:-.02em}
header.t p.s{margin:0 0 .5rem;color:var(--enc2);max-width:74ch}
.methode{background:#fff;border:1px solid var(--trait);border-radius:14px;
 padding:1.1rem 1.3rem;margin:0 0 2.4rem;color:var(--enc2);font-size:.92rem}
.methode b{color:var(--enc)}
.methode ul{margin:.6rem 0 0;padding-left:1.1rem}
.methode li{margin:.25rem 0}
section.m{background:#fff;border:1px solid var(--trait);border-radius:16px;
 padding:1.3rem;margin:0 0 1.5rem;box-shadow:0 1px 3px rgba(16,24,40,.06)}
.tete{display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap;margin:0 0 1rem}
.tete h2{margin:0;font-size:1.15rem;letter-spacing:-.01em}
.tete .u{font-size:.8rem;color:var(--enc2);word-break:break-all}
.tag{font-size:.62rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
 border-radius:99px;padding:.15rem .55rem;background:#FDECEA;color:var(--rouge)}
.rangee{display:grid;grid-template-columns:1.25fr 3fr;gap:1.3rem;align-items:start}
.act .cadre{border:2px solid var(--enc);border-radius:12px;overflow:hidden}
.cands{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem}
figure{margin:0}
.cadre{border:1px solid var(--trait);border-radius:10px;overflow:hidden;background:#EDEFEC}
.cadre img{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}
figcaption{margin:.4rem 0 0;font-size:.72rem;line-height:1.4;color:var(--enc2)}
figcaption .lab{display:block;font-weight:700;color:var(--enc);font-size:.7rem;
 letter-spacing:.06em;text-transform:uppercase;margin-bottom:.15rem}
figcaption a{color:var(--bleu)}
.lab.act{color:var(--rouge)}
.note{margin:1rem 0 0;padding:.75rem .9rem;background:#FEF6E6;border-radius:10px;
 color:#8A5A00;font-size:.84rem;line-height:1.5}
footer.f{margin-top:2.5rem;padding:1.1rem 1.3rem;background:#fff;border:1px solid var(--trait);
 border-radius:14px;color:var(--enc2);font-size:.88rem}
@media(max-width:1000px){.rangee{grid-template-columns:1fr}.cands{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.wrap{padding:1.5rem .9rem 3rem}.cands{grid-template-columns:1fr}}
</style>"""


def main():
    os.makedirs(CACHE_HERO, exist_ok=True)
    os.makedirs(CACHE_PX, exist_ok=True)
    blocs, pb = [], []
    for url, pid, libelle, cands, note in PLAN:
        uri, nom = hero(pid)
        if not uri:
            pb.append("%s : hero illisible (%s)" % (url, nom))
        vign = ""
        for c in cands:
            d = candidat(c)
            if not d:
                pb.append("%s : candidat %d illisible" % (url, c))
                continue
            vign += ('<figure><div class="cadre"><img src="%s" alt="%s" loading="lazy">'
                     '</div><figcaption><span class="lab">Pexels %d</span>%s · %s<br>'
                     '<a href="%s" target="_blank" rel="noopener">voir sur Pexels</a>'
                     '</figcaption></figure>'
                     % (d["uri"], html.escape(d["alt"] or "Proposition %d" % c),
                        d["id"], html.escape(d["ph"]), d["dim"], d["url"]))
        blocs.append(
            '<section class="m"><div class="tete"><h2>%s</h2>'
            '<span class="u">%s</span>%s</div>'
            '<div class="rangee"><div class="act"><figure>'
            '<div class="cadre">%s</div>'
            '<figcaption><span class="lab act">En place aujourd\'hui</span>%s</figcaption>'
            '</figure></div>'
            '<div class="cands">%s</div></div>%s</section>'
            % (libelle, url,
               '<span class="tag">protégée</span>' if pid in PROTEGEES else '',
               ('<img src="%s" alt="Hero actuel de la page %s">' % (uri, libelle))
               if uri else '<div style="aspect-ratio:16/9"></div>',
               html.escape(nom), vign,
               ('<p class="note">%s</p>' % note) if note else ''))

    doc = ('<title>Héros métier — actuel et propositions</title>' + CSS
           + '<div class="wrap"><header class="t">'
             '<p class="k">Hello Harel · 17 septembre 2026</p>'
             '<h1>Les héros des pages métier : l\'actuel, et quoi mettre à la place</h1>'
             '<p class="s">Pour chaque page métier, la photo de hero en place aujourd\'hui, '
             'lue en direct sur le site, et quatre remplaçantes libres de droit.</p>'
             '</header>'
           + '<div class="methode"><b>Comment les candidates ont été choisies.</b> '
             'Quatre requêtes Pexels orientées production par métier, une quinzaine de '
             'photos remontées, montées en planche contact et regardées une par une. '
             'Ce qui a fait le tri :'
             '<ul><li>un vrai lieu de travail, pas un décor de studio ni une cuisine '
             'de maison ;</li>'
             '<li>un geste de métier lisible — le fournier qui enfourne, la main dans le '
             'bac de refroidissement du torréfacteur, le tranchage du caillé, le dressage '
             'en série, la palette qu\'on tire dans l\'allée ;</li>'
             '<li>un décor crédible en Europe, aux codes du métier ;</li>'
             '<li>format paysage, au moins 1600 px de large.</li></ul>'
             '<p style="margin:.7rem 0 0">Je n\'ai pas trié les personnes sur leur couleur '
             'de peau : le tri porte sur le lieu, le geste et la crédibilité de la scène. '
             'Le choix final vous revient — dites-moi les numéros Pexels retenus et je les '
             'pose, recadrées en 1920 × 1080, avec leur alternative textuelle.</p></div>'
           + "".join(blocs)
           + '<footer class="f"><b>Licence.</b> Toutes les propositions viennent de Pexels : '
             'utilisation commerciale libre, sans attribution obligatoire. Le photographe est '
             'cité quand même, et chaque vignette renvoie à sa page d\'origine. '
             '<b>Pages protégées.</b> Cinq pages portent la mention : aucune photo n\'y sera '
             'remplacée sans votre feu vert explicite.</footer>'
             '</div>')
    open(SORTIE, "w", encoding="utf-8").write(doc)
    print("ecrit : %s (%d ko, %d metiers, %d vignettes)"
          % (SORTIE, len(doc) // 1024, len(PLAN), doc.count("<figure>")))
    for x in pb:
        print("   !", x)
    if len(doc) > 15_500_000:
        print("   ! depasse la limite d'un artefact")
    if not pb:
        print("controles : tout est vert")


if __name__ == "__main__":
    main()
