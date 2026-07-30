#!/usr/bin/env python3
"""
Turn the #1-ranking AS/400 article (post 4283, /blog/erp-as400/) into an
OFFER page by injecting a conversion band right after the hero. Purely
additive, inline-styled, idempotent (marker id). No Elementor touched.

DRY-RUN by default. Live: python3 as400_offer.py --live
"""
import sys, re
import wp_common as w

POST_ID = 4283
MARK = "hh-as400-offer"
CHK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
       'style="width:20px;height:20px;flex:0 0 20px"><path stroke-linecap="round" '
       'stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>')

def step(n, t, d):
    return (f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px 18px">'
            f'<div style="font-family:Inter,sans-serif;font-weight:800;color:#00B1F5;font-size:.85rem">ÉTAPE {n}</div>'
            f'<div style="font-weight:700;margin:.25rem 0 .3rem;color:#0f172a">{t}</div>'
            f'<p style="margin:0;color:#475569;font-size:.92rem;line-height:1.55">{d}</p></div>')

def bullet(t):
    return (f'<li style="display:flex;align-items:flex-start;gap:.55rem;color:#0f172a;'
            f'font-weight:600;font-size:1rem">{CHK}<span>{t}</span></li>')

BLOCK = (
    f'<section class="{MARK}" id="{MARK}" style="background:linear-gradient(135deg,#0090c8,#00B1F5);'
    'padding:44px 0;margin:0;">'
    f'<style>@media(max-width:760px){{'
    f'#{MARK} .as400-steps{{grid-template-columns:1fr !important;}}'
    f'#{MARK} .as400-bullets{{grid-template-columns:1fr !important;}}'
    f'#{MARK} .as400-in{{padding:0 18px !important;}}'
    f'#{MARK} h2{{font-size:1.4rem !important;}}'
    f'#{MARK} .as400-cta{{display:block !important;text-align:center !important;}}'
    f'}}</style>'
    '<div class="as400-in" style="max-width:1040px;margin:0 auto;padding:0 22px;font-family:Inter,-apple-system,sans-serif">'
    '<span style="display:inline-block;background:rgba(255,255,255,.18);color:#fff;font-weight:700;'
    'font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;padding:.35rem .8rem;border-radius:999px">'
    'Offre migration AS/400</span>'
    '<h2 style="color:#fff;font-size:clamp(1.5rem,3.2vw,2.1rem);line-height:1.2;font-weight:800;margin:.7rem 0 .5rem">'
    'Remplacez votre AS/400 (IBM iSeries) sans perdre une donnée</h2>'
    '<p style="color:rgba(255,255,255,.92);font-size:1.08rem;line-height:1.6;max-width:680px;margin:0 0 1.3rem">'
    'Hello Harel migre votre gestion agroalimentaire d\'un AS/400 vieillissant vers un ERP SaaS moderne : '
    'reprise de vos données garantie, accompagnement dédié, zéro rupture d\'exploitation.</p>'
    '<div class="as400-bullets" style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem 2rem;max-width:760px;margin:0 0 1.6rem;'
    'list-style:none">'
    f'<ul style="margin:0;padding:0;display:grid;gap:.6rem;list-style:none">{bullet("Reprise des données historiques garantie")}{bullet("Accès web, mobile et multi-sites (SaaS)")}</ul>'
    f'<ul style="margin:0;padding:0;display:grid;gap:.6rem;list-style:none">{bullet("Un chef de projet dédié, éditeur français")}{bullet("Traçabilité, DLC et facturation intégrées")}</ul>'
    '</div>'
    '<div class="as400-steps" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 1.6rem">'
    + step(1, "Audit de l\'existant", "Cartographie de vos données AS/400, de vos flux et de vos éditions.")
    + step(2, "Reprise des données", "Migration des articles, tiers, stocks et historiques, contrôlée et validée.")
    + step(3, "Paramétrage métier", "Configuration sur votre process agroalimentaire et formation des équipes.")
    + step(4, "Bascule accompagnée", "Mise en production progressive, sans arrêt de votre activité.")
    + '</div>'
    '<a href="/contact/" class="as400-cta" style="display:inline-block;background:#fff;color:#0090c8;font-weight:800;'
    'padding:13px 26px;border-radius:12px;text-decoration:none;font-size:1rem">Demander une démonstration gratuite →</a>'
    '</div></section>\n'
)

def main():
    live = "--live" in sys.argv
    c = w.get_raw("posts", POST_ID)["content"]["raw"]
    c = re.sub(r'<section class="%s".*?</section>\n?' % MARK, "", c, flags=re.S)
    # insert right after the article-hero closing tag
    m = re.search(r'<section class="article-hero".*?</section>', c, re.S)
    if not m:
        raise SystemExit("article-hero not found")
    c2 = c[:m.end()] + "\n" + BLOCK + c[m.end():]
    res = w.update_content("posts", POST_ID, c2, live=live)
    print(("LIVE" if live else "DRY-RUN"), "offer injected; +", len(BLOCK), "new len", len(c2))

if __name__ == "__main__":
    main()
