#!/usr/bin/env python3
"""
Correctif du carrousel « Nos secteurs d'expertise » — 45 pages.
Trois defauts cumules, tous constates le 18/08 :
  1. ancre <a> imbriquee dans la carte <a class="metier-slide"> -> HTML invalide,
     le navigateur ferme la carte prematurement et la mise en page explose ;
  2. .metier-slide en scroll-reveal (opacity:0) : les cartes hors ecran d'un
     carrousel horizontal ne declenchent jamais l'IntersectionObserver -> invisibles ;
  3. boutons .carousel-prev / .carousel-next absents du HTML alors que le CSS ET
     le JS (metiersCarousel) les referencent -> carrousel non navigable.

REGLE 0 — sur les 5 pages protegees on n'applique QUE les deux reparations de
defaut (1 et 2). L'ajout des boutons est une modification de structure : exclu.
DRY par defaut ; --live pour appliquer.
"""
import sys, re
import wp_common as w

PROTEGEES = {"agroalimentaire", "traiteur", "charcutier",
             "plats-cuisines-industriels", "migration-as400"}

STYLE_FIX = ('<style id="hh-carousel-fix">'
             '#hh-page .metiers-carousel .metier-slide,'
             '#hh-page .metiers-carousel .metier-slide.scroll-reveal,'
             '.metiers-carousel .metier-slide,'
             '.metiers-carousel .metier-slide.scroll-reveal'
             '{opacity:1 !important;transform:none !important}</style>\n')

CHEV_L = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
          'width="20" height="20" aria-hidden="true"><path stroke-linecap="round" '
          'stroke-linejoin="round" d="M15 6l-6 6 6 6"/></svg>')
CHEV_R = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
          'width="20" height="20" aria-hidden="true"><path stroke-linecap="round" '
          'stroke-linejoin="round" d="M9 6l6 6-6 6"/></svg>')
BOUTONS = ('<button type="button" class="carousel-arrow carousel-prev" '
           'aria-label="Voir les métiers précédents">%s</button>\n                '
           '<button type="button" class="carousel-arrow carousel-next" '
           'aria-label="Voir les métiers suivants">%s</button>\n                ') % (CHEV_L, CHEV_R)

ANCRE_IMBRIQUEE = re.compile(
    r'<a href="[^"]+"\s+style="color:#00B1F5[^"]*"\s*>(.*?)</a>', re.S)


def corriger(c, slug):
    """Retourne (contenu, actions[])."""
    actions = []
    i = c.find('<section class="metiers-section"')
    if i < 0:
        return c, actions
    j = c.find('</section>', i)
    seg = c[i:j]

    # 1 · ancre imbriquee dans une carte
    seg2, n = ANCRE_IMBRIQUEE.subn(r'\1', seg)
    if n:
        actions.append("ancre imbriquee retiree x%d" % n)
    seg = seg2

    # 3 · boutons de navigation (hors pages protegees)
    anchor = '<div class="metiers-carousel" id="metiersCarousel">'
    if anchor in seg and 'carousel-prev' not in seg:
        if slug in PROTEGEES:
            actions.append("boutons NON ajoutes (regle 0)")
        else:
            seg = seg.replace(anchor, BOUTONS + anchor, 1)
            actions.append("boutons prev/next ajoutes")

    c = c[:i] + seg + c[j:]

    # 2 · fix d'opacite (CSS pur, autorise partout)
    if 'hh-carousel-fix' not in c:
        c = STYLE_FIX + c
        actions.append("fix opacite ajoute")
    return c, actions


def main():
    live = "--live" in sys.argv
    pages = w.api("pages?per_page=100&context=edit&_fields=id,slug,content")
    total = touchees = 0
    for p in sorted(pages, key=lambda x: x["slug"]):
        c = (p.get("content") or {}).get("raw", "") or ""
        if '<section class="metiers-section"' not in c or 'metier-slide' not in c:
            continue
        total += 1
        c2, actions = corriger(c, p["slug"])
        if not actions or c2 == c:
            continue
        touchees += 1
        tag = " [PROTEGEE]" if p["slug"] in PROTEGEES else ""
        print("  %-36s %s%s" % (p["slug"][:36], " | ".join(actions), tag))
        if live:
            w.update_content("pages", p["id"], c2, live=True)
    print("\npages avec carrousel : %d | modifiees : %d" % (total, touchees))
    if not live:
        print("DRY-RUN — ajouter --live")


if __name__ == "__main__":
    main()
