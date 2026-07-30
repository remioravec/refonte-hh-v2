#!/usr/bin/env python3
"""
AS/400 offer module (post 4283, /blog/erp-as400/) — v2, ergonomic.

v1 was a full-bleed cyan band glued to the hero (a redundant "second hero",
dense, uneven spacing). v2 is a CONTAINED, breathable offer card: clear
hierarchy (eyebrow > headline > one subline > benefits > divider > numbered
4-step stepper > single pill CTA), consistent 8px spacing rhythm, responsive.
Additive + idempotent (marker id). No Elementor touched.

DRY-RUN by default. Live: python3 as400_offer.py --live
"""
import sys, re
import wp_common as w

POST_ID = 4283
MARK = "hh-as400-offer"


def benefit(t):
    return ('<div class="a4-benefit"><span class="ic">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6">'
            '<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'
            f'</span><span>{t}</span></div>')


def step(n, t, d):
    return f'<div class="a4-step"><div class="n">{n}</div><b>{t}</b><p>{d}</p></div>'


CSS = (
    '<style>'
    f'#{MARK} *{{box-sizing:border-box}}'
    f'#{MARK} .a4-card{{max-width:1080px;margin:0 auto;background:#fff;border:1px solid #e2e8f0;'
    'border-radius:24px;box-shadow:0 12px 34px rgba(2,32,54,.07);padding:clamp(26px,4vw,52px);'
    'font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif}'
    f'#{MARK} .a4-eyebrow{{display:inline-block;background:rgba(0,177,245,.1);color:#0090c8;'
    'font-weight:700;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;padding:.4rem .85rem;border-radius:999px}'
    f'#{MARK} h2{{color:#0f172a !important;font-size:clamp(1.5rem,3vw,2.05rem);line-height:1.15;font-weight:800;margin:1rem 0 .6rem}}'
    f'#{MARK} .a4-sub{{color:#475569;font-size:1.05rem;line-height:1.6;max-width:640px;margin:0}}'
    f'#{MARK} .a4-benefits{{display:grid;grid-template-columns:1fr 1fr;gap:16px 32px;margin:30px 0 0}}'
    f'#{MARK} .a4-benefit{{display:flex;align-items:flex-start;gap:12px;color:#0f172a;font-weight:600;font-size:1rem;line-height:1.45}}'
    f'#{MARK} .a4-benefit .ic{{flex:0 0 26px;width:26px;height:26px;border-radius:8px;background:rgba(0,177,245,.12);'
    'display:flex;align-items:center;justify-content:center;color:#0090c8;margin-top:1px}'
    f'#{MARK} .a4-benefit svg{{width:16px;height:16px}}'
    f'#{MARK} .a4-div{{height:1px;background:#eef2f6;margin:34px 0}}'
    f'#{MARK} .a4-steplabel{{font-size:.75rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#94a3b8;margin:0 0 18px}}'
    f'#{MARK} .a4-steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}}'
    f'#{MARK} .a4-step .n{{width:34px;height:34px;border-radius:50%;background:#00B1F5;color:#fff;font-weight:800;'
    'display:flex;align-items:center;justify-content:center;font-size:.95rem;margin:0 0 12px}'
    f'#{MARK} .a4-step b{{display:block;color:#0f172a;font-size:1rem;margin:0 0 5px;font-weight:700}}'
    f'#{MARK} .a4-step p{{margin:0;color:#64748b;font-size:.9rem;line-height:1.5}}'
    f'#{MARK} .a4-cta{{display:inline-flex;align-items:center;gap:8px;background:#00B1F5;color:#fff !important;font-weight:700;'
    'padding:14px 28px;border-radius:999px;text-decoration:none;font-size:1rem;margin:34px 0 0;'
    'box-shadow:0 8px 20px rgba(0,177,245,.28);transition:background .2s}'
    f'#{MARK} .a4-cta:hover{{background:#0090c8;color:#fff !important}}'
    '@media(max-width:760px){'
    f'#{MARK} .a4-benefits{{grid-template-columns:1fr;gap:14px}}'
    f'#{MARK} .a4-steps{{grid-template-columns:1fr;gap:18px}}'
    f'#{MARK} .a4-cta{{display:flex;justify-content:center;width:100%}}'
    '}'
    '</style>'
)

BLOCK = (
    f'<section class="{MARK}" id="{MARK}" style="background:#f8fafc;padding:clamp(40px,6vw,64px) 0;">'
    + CSS +
    '<div class="a4-card">'
    '<span class="a4-eyebrow">Offre migration AS/400</span>'
    '<h2>Remplacez votre AS/400 sans perdre une donnée</h2>'
    '<p class="a4-sub">On migre votre gestion agroalimentaire d\'un AS/400 (IBM iSeries) vieillissant vers '
    'un ERP SaaS moderne — reprise des données garantie, accompagnement dédié, zéro rupture d\'exploitation.</p>'
    '<div class="a4-benefits">'
    + benefit("Reprise des données historiques garantie")
    + benefit("Un chef de projet dédié, éditeur français")
    + benefit("Accès web, mobile et multi-sites (SaaS)")
    + benefit("Traçabilité, DLC et facturation intégrées")
    + '</div>'
    '<div class="a4-div"></div>'
    '<p class="a4-steplabel">La migration en 4 étapes</p>'
    '<div class="a4-steps">'
    + step(1, "Audit de l'existant", "Cartographie de vos données, flux et éditions AS/400.")
    + step(2, "Reprise des données", "Articles, tiers, stocks et historiques, contrôlés et validés.")
    + step(3, "Paramétrage métier", "Configuration sur votre process et formation des équipes.")
    + step(4, "Bascule accompagnée", "Mise en production progressive, sans arrêt d'activité.")
    + '</div>'
    '<a href="/contact/" class="a4-cta">Demander une démonstration gratuite →</a>'
    '</div>'
    '</section>\n'
)


def main():
    live = "--live" in sys.argv
    c = w.get_raw("posts", POST_ID)["content"]["raw"]
    c = re.sub(r'<section class="%s".*?</section>\n?' % MARK, "", c, flags=re.S)
    m = re.search(r'<section class="article-hero".*?</section>', c, re.S)
    if not m:
        raise SystemExit("article-hero not found")
    c2 = c[:m.end()] + "\n" + BLOCK + c[m.end():]
    res = w.update_content("posts", POST_ID, c2, live=live)
    print(("LIVE" if live else "DRY-RUN"), "offer v2 injected; block", len(BLOCK), "new len", len(c2))


if __name__ == "__main__":
    main()
