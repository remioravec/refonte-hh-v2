#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La signature d'auteur recoit la vraie photo de Timothy, centree.

Jusqu'ici la signature affichait un avatar genere par ui-avatars.com : deux
initiales blanches sur fond vert, servies par un tiers. Deux defauts. Le
premier est editorial — une page qui revendique l'experience d'un fondateur
et montre un monogramme ne prouve rien. Le second est technique : l'image
venait d'un domaine externe, donc une requete de plus, hors de notre
controle, et sans dimensions declarees.

La mediatheque contenait deja une photo de Timothy (200x200, plan large en
exterieur). Elle est recadree sur la tete et les epaules — fenetre de 44 %
centree a 52 % / 30 % — remontee a 192 px pour rester nette en ecran dense,
et televersee en WebP (7 ko).

La signature passe en colonne centree : portrait de 72 px au-dessus, nom et
dates en dessous, le bloc lui-meme centre dans sa colonne. Les dimensions
sont declarees sur l'image, donc aucun decalage de mise en page au
chargement.

ACCEPTATION : plus aucun appel a ui-avatars.com sur le site, la photo repond
en 200, les dimensions sont declarees, et le rendu ne deborde pas a 390 px.

Usage :  python3 photo_timothy_byline.py            (blanc)
         python3 photo_timothy_byline.py --ecrire
"""

import json
import os
import re
import sys

sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
import ns_api as n                                        # noqa: E402

SAUVE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avant-photo")
LISTE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/bylines.json")

PHOTO = ("https://www.helloharel.com/wp-content/uploads/2026/10/"
         "timothy-jollivet-fondateur-hello-harel.webp")

IMG = ('<img loading="lazy" decoding="async" width="72" height="72" src="'
       + PHOTO + '" alt="Timothy Jollivet, fondateur de Hello Harel">')

# Chaque regle est doublee en #hh-page : le theme prefixe les siennes de cet
# identifiant, et sans le doublon c'est lui qui gagne.
CSS = """<style id="hh-byline-css">
.eeat-byline{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.75rem;margin:1.5rem auto;padding:1.25rem 1.25rem 1.1rem;max-width:30rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
#hh-page .eeat-byline{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.75rem;margin:1.5rem auto;padding:1.25rem 1.25rem 1.1rem;max-width:30rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
.eeat-byline img,#hh-page .eeat-byline img{width:72px;height:72px;border-radius:50%;border:2px solid #16DB7F;object-fit:cover;display:block;margin:0 auto;flex:0 0 auto}
.eeat-byline-author,#hh-page .eeat-byline-author{color:#fff;font-size:.9375rem;line-height:1.5}
.eeat-byline-author strong,#hh-page .eeat-byline-author strong{color:#16DB7F;display:block;font-size:1.0625rem;margin-bottom:.15rem}
.eeat-byline-meta,#hh-page .eeat-byline-meta{color:rgba(255,255,255,.85);font-size:.8125rem;display:flex;flex-wrap:wrap;gap:.35rem .9rem;margin-top:.55rem;justify-content:center}
.eeat-byline-meta span,#hh-page .eeat-byline-meta span{display:inline-flex;align-items:center;gap:.35rem}
</style>
"""


def remplacer_image(c):
    """L'avatar genere cede la place au portrait, dans la signature seule."""
    m = re.search(r'(?is)(<div class="eeat-byline">\s*)<img\b[^>]*ui-avatars\.com[^>]*>',
                  c)
    if not m:
        return c, 0
    return c[:m.start()] + m.group(1) + IMG + c[m.end():], 1


def remplacer_css(c):
    """Remplace la feuille nommee, ou l'insere quand la page n'en a pas.

    Sept des treize pages tiennent leurs regles de signature dans un gros
    <style> sans identifiant, de 100 ko et plus, qu'on ne reecrit pas. On y
    ajoute donc la feuille nommee : chacune de ses regles est doublee en
    #hh-page, specificite qui l'emporte sur les .eeat-byline nus du bloc
    d'origine, quel que soit l'ordre des deux blocs dans la page.
    """
    m = re.search(r'(?is)<style id="hh-byline-css">.*?</style>\s*', c)
    if m:
        return c[:m.start()] + CSS + c[m.end():], 1
    i = c.find('<div class="eeat-byline">')
    if i < 0:
        return c, 0
    return c[:i] + CSS + c[i:], 2


def main(poser=False):
    os.makedirs(SAUVE, exist_ok=True)
    print("mode :", "ECRITURE REELLE" if poser else "blanc (aucune écriture)", "\n")
    cibles = [x for x in json.load(open(LISTE)) if x[3] or x[4]]
    print("%d page(s) portant la signature\n" % len(cibles))
    tot_img = tot_css = 0
    for kind, pid, url, nb_by, nb_ui in cibles:
        d = n.call("wp/v2/%s/%d?context=edit&_fields=id,content,meta" % (kind, pid))
        if str(d["meta"].get("_elementor_data")) not in ("[]", "", "None"):
            raise RuntimeError("%d : _elementor_data non vide" % pid)
        c = d["content"]["raw"]
        open(os.path.join(SAUVE, "%d.html" % pid), "w").write(c)
        avant = len(c)
        c, ki = remplacer_image(c)
        c, kc = remplacer_css(c)
        if not ki and not kc:
            print("  %-6d %-56s rien à changer" % (pid, url[:56]))
            continue
        assert "ui-avatars.com" not in c, "%d : un avatar généré subsiste" % pid
        assert c.count('class="eeat-byline"') == nb_by, \
            "%d : le nombre de signatures a bougé" % pid
        assert c.count("<h1") <= 1, "%d : nombre de H1 anormal" % pid
        assert c.count('<style id="hh-byline-css">') == 1, \
            "%d : %d feuille(s) nommée(s)" % (pid, c.count('<style id="hh-byline-css">'))
        tot_img += ki
        tot_css += 1 if kc else 0
        print("  %-6d %-56s image %s · feuille %s · %+d o"
              % (pid, url[:56], "oui" if ki else "—",
                 {0: "—", 1: "remplacée", 2: "ajoutée"}[kc], len(c) - avant))
        if poser:
            n.call("wp/v2/%s/%d" % (kind, pid), "POST", {"content": c})
    print("\n%d image(s) remplacée(s), %d feuille(s) de style remise(s)"
          % (tot_img, tot_css))


if __name__ == "__main__":
    main(poser="--ecrire" in sys.argv)
