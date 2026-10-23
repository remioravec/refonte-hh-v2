#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deux blocs de reassurance sur les trois pages metier.

1. Sous le Hero : une rangee d'avatars, les etoiles Google et le nombre de
   clients. Les avatars sont des silhouettes neutres, marquees aria-hidden —
   les memes que sous « plus d'une vingtaine de membres » dans la section
   equipe. Elles disent une quantite, elles ne pretendent identifier
   personne. La note et le nombre d'avis sont repris mot pour mot de la
   section des avis de la page : on ne rehausse rien au passage.

2. En bas a droite : Maxence, sa photo de la mediatheque, et un lien vers le
   formulaire. Refermable, et l'etat tient le temps de la visite — un
   visiteur qui l'ecarte ne le revoit pas a chaque page.

Usage :  python3 hero_maxence.py            (blanc)
         python3 hero_maxence.py --poser    (ecrit)
"""

import os
import re
import sys
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w          # noqa: E402
import scroll_sticky as SY     # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "hero-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}


def FRAIS():
    """Une URL unique par controle : le cache du site sert sinon la
    version d'avant la pose, et le controle annonce un echec faux."""
    import random
    return "?hh=%d" % random.randrange(10 ** 9)


def lire_page(url):
    """La page servie, en entier.

    Le transfert est parfois coupe en route : on a deja lu 170 ko d'une page
    qui en fait 364, et le controle a annonce un echec qui n'existait pas.
    On redemande tant que la page ne se termine pas.
    """
    import time
    for essai in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(
                "https://www.helloharel.com" + url + FRAIS(),
                headers={"User-Agent": "Mozilla/5.0"}),
                timeout=90).read().decode("utf-8", "replace")
            if "</html>" in h:
                return h
        except Exception:
            pass
        time.sleep(2 * (essai + 1))
    raise SystemExit("ARRET — page %s illisible en entier apres 4 essais" % url)

PHOTO_MAXENCE = "https://www.helloharel.com/wp-content/uploads/2026/08/Maxence-150x150-1.webp"

# Pas de formatage par % ici : la chaine EST pleine de %, et melanger les
# deux, c'est le piege dans lequel on tombe a chaque fois. On remplace un
# jeton, et une garde refuse toute chaine ou il subsisterait.
SILHOUETTE = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'"
              " viewBox='0 0 100 100'%3E"
              "%3Crect width='100' height='100' rx='50' fill='hsl({t},42%,88%)'/%3E"
              "%3Ccircle cx='50' cy='38' r='16' fill='hsl({t},38%,68%)'/%3E"
              "%3Cellipse cx='50' cy='84' rx='25' ry='21' fill='hsl({t},38%,68%)'/%3E"
              "%3C/svg%3E")


def silhouette(teinte):
    u = SILHOUETTE.replace("{t}", str(teinte))
    if "{t}" in u:
        raise SystemExit("ARRET — jeton non remplace dans la silhouette")
    return u

ETOILE = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M12 2l2.9 6.26 6.85.78-5.09 4.64 1.4 6.74L12 17.1l-6.06 3.32 1.4-6.74'
          'L2.25 9.04l6.85-.78z"/></svg>')

CSS = """<style id="hh-reassurance">
/* ── le bandeau sous le Hero ─────────────────────────────────────────── */
#hh-page .hh-conf,.hh-conf{display:flex !important;align-items:center !important;
 gap:.85rem !important;flex-wrap:wrap !important;margin:1.35rem 0 0 !important;
 padding:.7rem 1.05rem .7rem .8rem !important;width:fit-content !important;
 /* Fond SOMBRE et non clair : la photo du Hero change d'une page a
    l'autre, et sur une image claire un voile blanc faisait tomber le texte
    a 2,4:1. Un voile sombre a 66 % tient 9,1:1 dans le pire cas — une photo
    entierement blanche — et le jaune des etoiles 5,5:1. */
 background:rgba(2,32,51,.66) !important;
 border:1px solid rgba(255,255,255,.22) !important;border-radius:999px !important;
 -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
#hh-page .hh-conf-t,.hh-conf-t{display:flex !important;align-items:center !important;
 margin:0 !important;padding:0 !important;list-style:none !important}
#hh-page .hh-conf-t li,.hh-conf-t li{margin:0 0 0 -12px !important;padding:0 !important}
#hh-page .hh-conf-t li:first-child,.hh-conf-t li:first-child{margin-left:0 !important}
#hh-page .hh-conf-t img,.hh-conf-t img{display:block !important;width:36px !important;
 height:36px !important;border-radius:50% !important;margin:0 !important;
 border:2px solid rgba(255,255,255,.92) !important;background:#E0F2FE !important}
#hh-page .hh-conf-d,.hh-conf-d{display:grid !important;gap:.1rem !important}
#hh-page .hh-conf-e,.hh-conf-e{display:flex !important;align-items:center !important;
 gap:.3rem !important;margin:0 !important;color:#fff !important;
 font-size:.86rem !important;font-weight:700 !important;line-height:1.2 !important}
#hh-page .hh-conf-e svg,.hh-conf-e svg{width:14px;height:14px;color:#FBBF24;flex:none}
#hh-page .hh-conf-e b,.hh-conf-e b{margin-left:.25rem !important;font-weight:700 !important;
 color:#fff !important}
#hh-page .hh-conf-c,.hh-conf-c{margin:0 !important;color:rgba(255,255,255,.92) !important;
 font-size:.82rem !important;font-weight:600 !important;line-height:1.2 !important}
@media (max-width:560px){
 #hh-page .hh-conf,.hh-conf{width:100% !important;box-sizing:border-box !important;
  gap:.7rem !important}
 #hh-page .hh-conf-t img,.hh-conf-t img{width:32px !important;height:32px !important}}

/* ── Maxence, en bas a droite ────────────────────────────────────────── */
#hh-page .hh-max,.hh-max{position:fixed !important;right:18px !important;
 bottom:18px !important;z-index:60;display:flex !important;align-items:center !important;
 gap:.7rem !important;margin:0 !important;padding:.5rem 1.1rem .5rem .5rem !important;
 max-width:calc(100vw - 36px);box-sizing:border-box !important;
 background:#fff !important;border:1px solid #e2e8f0 !important;
 border-radius:999px !important;text-decoration:none !important;
 box-shadow:0 16px 38px -18px rgba(15,23,42,.55) !important;
 transition:transform .18s ease,box-shadow .18s ease !important}
#hh-page .hh-max:hover,.hh-max:hover{transform:translateY(-2px) !important;
 box-shadow:0 22px 46px -20px rgba(15,23,42,.6) !important}
#hh-page .hh-max img,.hh-max img{display:block !important;width:46px !important;
 height:46px !important;border-radius:50% !important;object-fit:cover !important;
 margin:0 !important;flex:none !important;border:2px solid #E0F2FE !important}
#hh-page .hh-max span,.hh-max span{display:block !important;color:#0f172a !important;
 font-size:.92rem !important;font-weight:700 !important;line-height:1.25 !important}
#hh-page .hh-max small,.hh-max small{display:block !important;color:#64748b !important;
 font-size:.78rem !important;font-weight:600 !important;line-height:1.25 !important}
#hh-page .hh-max-x,.hh-max-x{position:fixed !important;z-index:61;
 right:12px !important;bottom:74px !important;
 display:grid !important;place-items:center !important;
 width:26px !important;height:26px !important;padding:0 !important;margin:0 !important;
 border:1px solid #e2e8f0 !important;border-radius:50% !important;
 background:#fff !important;color:#475569 !important;font-size:15px !important;
 line-height:1 !important;cursor:pointer !important;
 box-shadow:0 6px 16px -8px rgba(15,23,42,.5) !important}
#hh-page .hh-max[hidden],.hh-max[hidden],
#hh-page .hh-max-x[hidden],.hh-max-x[hidden]{display:none !important}
@media (max-width:560px){
 #hh-page .hh-max,.hh-max{right:12px !important;bottom:12px !important;
  padding:.4rem .9rem .4rem .4rem !important;gap:.55rem !important}
 #hh-page .hh-max img,.hh-max img{width:40px !important;height:40px !important}
 #hh-page .hh-max span,.hh-max span{font-size:.85rem !important}
 #hh-page .hh-max small,.hh-max small{display:none !important}
 #hh-page .hh-max-x,.hh-max-x{bottom:62px !important;right:8px !important}}
@media (prefers-reduced-motion:reduce){
 #hh-page .hh-max,.hh-max{transition:none !important}}
</style>"""

JS = """<script id="hh-max-js">
(function(){
 var a=document.querySelector(".hh-max"), x=document.querySelector(".hh-max-x");
 if(!a||!x) return;
 /* Ecarte une fois, ecarte pour la visite : sessionStorage et non
    localStorage — on n'impose pas un choix au retour du visiteur. */
 var CLE="hh-max-ecarte";
 try{ if(sessionStorage.getItem(CLE)==="1"){a.hidden=true;x.hidden=true;return} }catch(e){}
 x.addEventListener("click",function(){
  a.hidden=true; x.hidden=true;
  try{ sessionStorage.setItem(CLE,"1") }catch(e){}
 });
})();
</script>"""


def bandeau(note):
    """note : le texte de la note, repris tel quel de la section des avis."""
    tetes = "".join(
        '<li><img src="%s" width="36" height="36" alt="" aria-hidden="true"'
        ' loading="lazy" decoding="async"></li>' % silhouette(t)
        for t in (202, 152, 28))
    return ('<div class="hh-conf">'
            '<ul class="hh-conf-t">%s</ul>'
            '<div class="hh-conf-d">'
            '<p class="hh-conf-e">%s<b>%s</b></p>'
            '<p class="hh-conf-c">Plus de 100 clients nous font confiance</p>'
            '</div></div>' % (tetes, ETOILE * 5, note))


def widget():
    return ('<a class="hh-max" href="/contact/" '
            'aria-label="Une question ? Contactez Maxence, responsable commercial">'
            '<img src="%s" width="46" height="46" alt="" aria-hidden="true" '
            'loading="lazy" decoding="async">'
            '<span>Une question ? Contactez-moi'
            '<small>Maxence · Resp. commercial</small></span></a>'
            '<button class="hh-max-x" type="button" '
            'aria-label="Masquer le message de Maxence">&times;</button>' % PHOTO_MAXENCE)


def main():
    poser = "--poser" in sys.argv
    os.makedirs(SAUV, exist_ok=True)
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")

    for cle, (page, url) in SY.PAGES.items():
        if page in PROTEGEES:
            raise SystemExit("ARRET — page %d protegee par la regle 0" % page)
        c = w.get_raw("pages", page)["content"]["raw"]
        if 'class="hh-conf"' in c or 'class="hh-max"' in c:
            raise SystemExit("ARRET — %s porte deja les blocs" % url)

        note = re.search(r'class="rating-text">([^<]+)<', c)
        if not note:
            raise SystemExit("ARRET — note des avis introuvable sur %s" % url)
        note = note.group(1).strip()

        # 1. le bandeau, juste apres la mention sous les boutons du Hero
        m = re.search(r'<p class="hero-cta-sub">.*?</p>', c, re.S)
        if not m:
            raise SystemExit("ARRET — pied du Hero introuvable sur %s" % url)
        h = c.find('<section class="hero-section"')
        hf = c.find("</section>", h)
        if not (h < m.start() < hf):
            raise SystemExit("ARRET — le point d'insertion sort du Hero sur %s" % url)
        neuf = c[:m.end()] + bandeau(note) + c[m.end():]

        # 2. Maxence, a la toute fin du contenu
        neuf = neuf + CSS + widget() + JS

        corps = lambda t: re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)
        av = re.findall(r'href="([^"]+)"', corps(c))
        ap = re.findall(r'href="([^"]+)"', corps(neuf))
        if sorted(av) != sorted(x for x in ap if x != "/contact/") and \
           ap.count("/contact/") != av.count("/contact/") + 1:
            raise SystemExit("ARRET — le maillage a bouge autrement que par le widget sur %s"
                             % url)
        if neuf.count('class="hh-conf"') != 1 or neuf.count('class="hh-max"') != 1:
            raise SystemExit("ARRET — bloc en double sur %s" % url)
        if corps(neuf).count("<h1") != corps(c).count("<h1"):
            raise SystemExit("ARRET — le H1 a bouge sur %s" % url)

        print("%-42s bandeau « %s » · Maxence · %+d ko"
              % (url, note, (len(neuf) - len(c)) // 1024))
        if not poser:
            continue
        open(os.path.join(SAUV, "avant-%d.html" % page), "w", encoding="utf-8").write(c)
        w.update_content("pages", page, neuf, live=True)
        print("   pose")

    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")
        return
    print("\n--- verification en ligne ---")
    import time
    time.sleep(5)
    for cle, (page, url) in SY.PAGES.items():
        h = lire_page(url)
        ok = h.count('class="hh-conf"') == 1 and h.count('class="hh-max"') == 1
        print("   %-42s %s  bandeau %d · Maxence %d · bouton %d"
              % (url, "OK " if ok else "KO ", h.count('class="hh-conf"'),
                 h.count('class="hh-max"'), h.count('class="hh-max-x"')))


if __name__ == "__main__":
    main()
