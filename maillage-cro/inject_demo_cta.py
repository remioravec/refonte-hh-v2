#!/usr/bin/env python3
"""
Invitation démo — premium, on-brand CTA band injected on the high-commercial
pages (agroalimentaire hub, charcutier, comparatif maraîchers).
Additive, idempotent (marker), responsive, SVG icons (no emoji).
Inserted before <section class="faq-section"> on metier pages; before the FAQ
or reviews on the blog article.

DRY by default; --live to apply.
"""
import sys, re
import wp_common as w

MARK = "hh-demo-cta"

def chip(svg, label):
    return (f'<span class="hh-demo-chip">{svg}<span>{label}</span></span>')

CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M12 7v5l3 2"/></svg>'
SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z"/><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4"/></svg>'
USER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path stroke-linecap="round" d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" style="width:18px;height:18px"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>'

def band(headline, subline):
    return (
        f'<section class="{MARK}" id="{MARK}" style="background:#f8fafc;padding:clamp(40px,6vw,68px) 0">'
        f'<style>'
        f'#{MARK} .hh-demo-wrap{{max-width:1080px;margin:0 auto;padding:0 22px;'
        'font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif}'
        f'#{MARK} .hh-demo-card{{position:relative;overflow:hidden;background:linear-gradient(135deg,#0090c8 0%,#00B1F5 100%);'
        'border-radius:28px;box-shadow:0 24px 60px rgba(0,120,180,.28);padding:clamp(28px,4vw,48px);'
        'display:grid;grid-template-columns:1.35fr .85fr;gap:32px;align-items:center;color:#fff}'
        f'#{MARK} .hh-demo-card::after{{content:"";position:absolute;right:-80px;top:-80px;width:280px;height:280px;'
        'background:radial-gradient(circle,rgba(255,255,255,.16),transparent 70%);pointer-events:none}'
        f'#{MARK} .hh-demo-eyebrow{{display:inline-block;background:rgba(255,255,255,.18);color:#fff;font-weight:700;'
        'font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;padding:.4rem .85rem;border-radius:999px}'
        f'#{MARK} h2{{color:#fff !important;font-size:clamp(1.5rem,3vw,2.15rem);line-height:1.18;font-weight:800;margin:.9rem 0 .55rem}}'
        f'#{MARK} .hh-demo-sub1{{color:rgba(255,255,255,.94);font-size:1.05rem;line-height:1.6;margin:0 0 1.2rem;max-width:520px}}'
        f'#{MARK} .hh-demo-chips{{display:flex;flex-wrap:wrap;gap:10px}}'
        f'#{MARK} .hh-demo-chip{{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.14);'
        'border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:6px 13px;font-size:.86rem;font-weight:600}'
        f'#{MARK} .hh-demo-chip svg{{width:16px;height:16px;flex:0 0 16px}}'
        f'#{MARK} .hh-demo-action{{display:flex;flex-direction:column;align-items:stretch;gap:10px}}'
        f'#{MARK} .hh-demo-btn{{display:inline-flex;align-items:center;justify-content:center;gap:9px;background:#fff;color:#0090c8 !important;'
        'font-weight:800;font-size:1.08rem;padding:16px 26px;border-radius:14px;text-decoration:none;'
        'box-shadow:0 10px 24px rgba(2,32,54,.18);transition:transform .15s ease,box-shadow .15s ease}'
        f'#{MARK} .hh-demo-btn:hover{{transform:translateY(-2px);box-shadow:0 16px 32px rgba(2,32,54,.24);color:#0090c8 !important}}'
        f'#{MARK} .hh-demo-note{{text-align:center;color:rgba(255,255,255,.9);font-size:.86rem}}'
        f'@media(max-width:820px){{#{MARK} .hh-demo-card{{grid-template-columns:1fr;gap:22px}}'
        f'#{MARK} .hh-demo-sub1{{max-width:none}}}}'
        f'</style>'
        '<div class="hh-demo-wrap"><div class="hh-demo-card">'
        '<div class="hh-demo-text">'
        '<span class="hh-demo-eyebrow">Démo gratuite &amp; personnalisée</span>'
        f'<h2>{headline}</h2>'
        f'<p class="hh-demo-sub1">{subline}</p>'
        '<div class="hh-demo-chips">'
        + chip(CLOCK, "30 minutes") + chip(SHIELD, "Sans engagement") + chip(USER, "Un expert de votre secteur")
        + '</div>'
        '</div>'
        '<div class="hh-demo-action">'
        f'<a class="hh-demo-btn" href="/contact/">Réserver ma démo {ARROW}</a>'
        '<span class="hh-demo-note">Réponse sous 24 h ouvrées</span>'
        '</div>'
        '</div></div></section>\n'
    )

TARGETS = {
    1726: ("pages", "Voyez l'ERP agroalimentaire en action sur votre métier",
           "Une démonstration adaptée à votre production — traçabilité, coût de revient, DLC — et à votre secteur précis. Pas une visite générique."),
    2818: ("pages", "Voyez Hello Harel sur votre atelier de charcuterie",
           "Rendement matière, poids variable, traçabilité viande, coût de revient : on vous montre l'ERP sur vos cas concrets, en 30 minutes."),
    None: (None, None, None),  # placeholder
}

def inject(pid, kind, headline, subline, live):
    c = w.get_raw(kind, pid)["content"]["raw"]
    c = re.sub(r'<section class="%s".*?</section>\n?' % MARK, "", c, flags=re.S)
    b = band(headline, subline)
    for anchor in ('<section class="faq-section"', '<section class="reviews-section"',
                   '<section class="cta-banner"'):
        if anchor in c:
            c2 = c.replace(anchor, b + anchor, 1)
            break
    else:
        # blog fallback: before the last closing or the footer marker
        m = re.search(r'<section class="article-cta"|<div class="hh-blog-share"|</article>', c)
        if m:
            c2 = c[:m.start()] + b + c[m.start():]
        else:
            c2 = c + b
    res = w.update_content(kind, pid, c2, live=live)
    print(f"[{pid}] {kind} — demo band {'INJECTED' if live else 'DRY'} (+{len(b)})")

def main():
    live = "--live" in sys.argv
    # metier pages
    inject(1726, "pages", "Voyez l'ERP agroalimentaire en action sur votre métier",
           "Une démonstration adaptée à votre production — traçabilité, coût de revient, DLC — et à votre secteur précis. Pas une visite générique.", live)
    inject(2818, "pages", "Voyez Hello Harel sur votre atelier de charcuterie",
           "Rendement matière, poids variable, traçabilité de la viande, coût de revient : l'ERP démontré sur vos cas concrets, en 30 minutes.", live)
    # blog comparatif maraîchers
    r = w.api("posts?slug=meilleurs-erp-maraichers-fruits-legumes&_fields=id")
    if r:
        inject(r[0]["id"], "posts", "Le bon ERP fruits &amp; légumes, démontré en 30 minutes",
               "Agréage, prix au cours du jour, poids variable, traçabilité : voyez comment Hello Harel pilote votre négoce de fruits et légumes.", live)
    else:
        print("maraichers post not found")

if __name__ == "__main__":
    main()
