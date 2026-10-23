# -*- coding: utf-8 -*-
"""Recette de la maquette : ce qui casse, ce qui deborde, ce qui ne se lit pas."""
import json
from playwright.sync_api import sync_playwright

F = ("file:///tmp/claude-0/-home-user-refonte-hh-v2/"
     "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/maquette-agro.html")

JS = r"""
() => {
  const out = {};
  const vis = e => { const s = getComputedStyle(e);
    return e.offsetParent !== null && s.visibility !== 'hidden' && s.opacity !== '0'; };

  // identifiants en double
  const ids = {};
  document.querySelectorAll('[id]').forEach(e => { ids[e.id] = (ids[e.id]||0)+1; });
  out.idsDoubles = Object.entries(ids).filter(([,n]) => n>1).map(([k,n]) => k+' x'+n);

  // titres
  out.h1 = [...document.querySelectorAll('h1')].map(e=>e.textContent.trim().slice(0,70));
  const niveaux = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis)
     .map(e=>+e.tagName[1]);
  out.sautsDeNiveau = niveaux.map((n,i)=> i && n-niveaux[i-1]>1
     ? 'h'+niveaux[i-1]+' -> h'+n : null).filter(Boolean);

  // images sans alternative
  out.imgSansAlt = [...document.querySelectorAll('img')]
     .filter(e=>!e.hasAttribute('alt')).map(e=>(e.getAttribute('src')||'').slice(0,50));

  // liens sans intitule accessible
  out.liensMuets = [...document.querySelectorAll('a')].filter(a => vis(a) &&
      !a.textContent.trim() && !a.getAttribute('aria-label') && !a.querySelector('img[alt]:not([alt=""])'))
     .map(a=>(a.getAttribute('href')||'').slice(0,60));

  // liens vides ou #
  out.liensMorts = [...new Set([...document.querySelectorAll('a')]
     .map(a=>a.getAttribute('href')).filter(h=>!h || h==='#' || h==='javascript:void(0)'))];

  // texte ecrete : un bloc dont le contenu deborde sans pouvoir defiler
  out.texteEcrete = [...document.querySelectorAll('#hh-page p,#hh-page h1,#hh-page h2,#hh-page h3,#hh-page li,#hh-page span,#hh-page label')]
     .filter(e => vis(e) && e.scrollWidth > e.clientWidth + 2
             && getComputedStyle(e).overflowX === 'hidden')
     .slice(0,14).map(e => e.tagName+'.'+(e.className||'').toString().split(' ')[0]
             +' : '+e.textContent.trim().slice(0,44));

  // debordement horizontal de la page
  out.largeurDoc = document.documentElement.scrollWidth;
  out.largeurVue = window.innerWidth;
  out.coupables = [...document.querySelectorAll('#hh-page *')]
     .filter(e => { const r = e.getBoundingClientRect();
       return vis(e) && (r.right > window.innerWidth + 2 || r.left < -2); })
     .slice(0,12).map(e => e.tagName+'.'+(e.className||'').toString().split(' ')[0]
             +' ['+Math.round(e.getBoundingClientRect().left)+'→'
             +Math.round(e.getBoundingClientRect().right)+']');

  // cibles tactiles trop petites
  out.ciblesPetites = [...document.querySelectorAll('#hh-page a,#hh-page button,#hh-page label,#hh-page input')]
     .filter(e => { const r = e.getBoundingClientRect();
       return vis(e) && r.width>0 && (r.height < 32 || r.width < 24); })
     .slice(0,12).map(e => e.tagName+'.'+(e.className||'').toString().split(' ')[0]
             +' '+Math.round(e.getBoundingClientRect().width)+'x'
             +Math.round(e.getBoundingClientRect().height)
             +' « '+e.textContent.trim().slice(0,26)+' »');

  // sections et modules attendus
  out.sections = [...document.querySelectorAll('#hh-page section')]
     .map(s => (s.className||'').split(' ')[0]);
  out.modules = {
     onglets: document.querySelectorAll('#fonctionnalites .hhf-bar label').length,
     panneauxVisibles: [...document.querySelectorAll('#fonctionnalites .hhf-panels>.hhf-row')].filter(vis).length,
     quiz: !!document.querySelector('.hh2-quiz'),
     simulateur: !!document.querySelector('.hh2-roi'),
     guide: !!document.querySelector('#guide-erp-agroalimentaire'),
     faq: document.querySelectorAll('.hh2-faq-section details, .hh2-faq-section .faq-item').length,
     metiers: document.querySelectorAll('.metiers-section a').length,
  };
  return out;
}
"""

resultats = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    for nom, vp in (("bureau 1280", {"width": 1280, "height": 900}),
                    ("tablette 768", {"width": 768, "height": 1024}),
                    ("mobile 390", {"width": 390, "height": 844})):
        pg = b.new_page(viewport=vp)
        erreurs = []
        pg.on("console", lambda m: erreurs.append(m.type + " : " + m.text[:110])
              if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: erreurs.append("exception : " + str(e)[:140]))
        pg.goto(F)
        pg.wait_for_timeout(2600)
        r = pg.evaluate(JS)
        r["console"] = erreurs[:10]
        resultats[nom] = r
        pg.close()
    b.close()

for nom, r in resultats.items():
    print("=" * 64)
    print(nom, " — document", r["largeurDoc"], "px pour une vue de", r["largeurVue"], "px")
    for cle in ("console", "idsDoubles", "sautsDeNiveau", "imgSansAlt", "liensMuets",
                "liensMorts", "texteEcrete", "coupables", "ciblesPetites"):
        v = r.get(cle) or []
        if v:
            print("  %s (%d) :" % (cle, len(v)))
            for x in v[:10]:
                print("     -", x)
    print("  h1 :", r["h1"])
    print("  modules :", json.dumps(r["modules"], ensure_ascii=False))
print("\nsections :", resultats["bureau 1280"]["sections"])
