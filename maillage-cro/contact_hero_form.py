#!/usr/bin/env python3
"""
Contact page (id 661) — bring the HERO back, but keep the form above the fold.

Layout: a real hero band with a 2-column grid — hero copy (eyebrow, H1,
subtitle, reassurance) on the left, the existing contact FORM on the right.
Desktop: both above the fold, form clearly visible. Mobile: the grid stacks
and the form is ordered FIRST so it stays above the fold (the user's standing
requirement). The header offset (fixed 72px menu) is respected.

The form block is lifted out of the old .contact-grid and placed inside the
hero; the remaining .contact-info becomes a coordinates strip below.

DRY-RUN by default. Live: python3 contact_hero_form.py --live
"""
import sys
import re
import wp_common as w

PAGE_ID = 661
CHK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4">'
       '<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>')

CSS = (
    '<style id="cro-contact-fix">'
    '#hh-page .contact-hero{background:linear-gradient(135deg,#0090c8,#00B1F5);'
    'padding:calc(72px + 2.1rem) 0 2.3rem;}'
    '#hh-page .contact-hero .container{max-width:1140px;margin:0 auto;padding:0 22px;}'
    '#hh-page .contact-hero-grid{display:grid;grid-template-columns:1.02fr 1fr;gap:38px;align-items:start;}'
    '#hh-page .contact-hero-copy{color:#fff;}'
    '#hh-page .contact-hero-copy .eyebrow{display:inline-block;background:rgba(255,255,255,.16);'
    'color:#fff;font-weight:700;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;'
    'padding:.35rem .8rem;border-radius:999px;}'
    '#hh-page .contact-hero-copy h1{color:#fff;font-size:clamp(1.7rem,3.4vw,2.5rem);line-height:1.15;'
    'font-weight:800;margin:.85rem 0 .6rem;}'
    '#hh-page .contact-hero-copy .sub{color:rgba(255,255,255,.92);font-size:1.08rem;line-height:1.6;'
    'margin:0 0 1.15rem;max-width:470px;}'
    '#hh-page .contact-hero-copy ul{list-style:none;padding:0;margin:0;display:grid;gap:.6rem;}'
    '#hh-page .contact-hero-copy li{color:#fff;font-weight:600;display:flex;align-items:center;'
    'gap:.55rem;font-size:.99rem;}'
    '#hh-page .contact-hero-copy li svg{width:20px;height:20px;flex:0 0 20px;color:#fff;}'
    '#hh-page .contact-hero .contact-form{background:#fff;border-radius:16px;'
    'box-shadow:0 22px 48px rgba(2,32,54,.24);padding:24px 22px;margin:0;}'
    '#hh-page .contact-hero .contact-form h3{margin-top:0;}'
    '#hh-page .contact-section{padding:2.4rem 0;}'
    '#hh-page .contact-section .contact-grid{grid-template-columns:1fr;}'
    '@media(max-width:900px){'
    '#hh-page .contact-hero{padding:calc(66px + 1.2rem) 0 1.5rem;}'
    '#hh-page .contact-hero-grid{grid-template-columns:1fr;gap:18px;}'
    '#hh-page .contact-hero .contact-form{order:-1;}'          # form first on mobile
    '#hh-page .contact-hero-copy .sub{max-width:none;}'
    '}'
    '</style>'
)


def hero(form_html):
    return (
        '<!-- HERO 2-col : copy + formulaire (au-dessus de la ligne de flottaison) -->\n'
        '<section class="contact-hero">\n'
        '  <div class="container">\n'
        '    <div class="contact-hero-grid">\n'
        '      <div class="contact-hero-copy">\n'
        '        <span class="eyebrow">Démo gratuite · ERP agroalimentaire</span>\n'
        '        <h1>Demandez votre démonstration gratuite</h1>\n'
        '        <p class="sub">Découvrez en 30 minutes comment Hello Harel pilote votre '
        'traçabilité, vos coûts de revient et votre facturation — adapté à votre métier.</p>\n'
        '        <ul>\n'
        f'          <li>{CHK}Réponse sous 24 h ouvrées</li>\n'
        f'          <li>{CHK}Sans engagement, sans carte bancaire</li>\n'
        f'          <li>{CHK}Un expert dédié à votre secteur agroalimentaire</li>\n'
        '        </ul>\n'
        '      </div>\n'
        f'      {form_html.strip()}\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n'
    )


def main():
    live = "--live" in sys.argv
    c = w.get_raw("pages", PAGE_ID)["content"]["raw"]

    if 'contact-hero-grid' in c:
        print("Hero already present — aborting to avoid double transform.")
        return

    if c.count('<div class="contact-form">') != 1 or c.count('<div class="contact-info">') != 1:
        raise SystemExit("Unexpected contact-form/contact-info count — inspect manually.")

    # 1) Lift the form div out of the grid.
    head, tmp = c.split('<div class="contact-form">', 1)
    form_body, after_info = tmp.split('<div class="contact-info">', 1)
    form_html = '<div class="contact-form">' + form_body  # includes closing </div> of the form
    c = head + '<div class="contact-info">' + after_info

    # 2) Remove the old slim heading section.
    c = re.sub(r'<!-- HERO[^>]*-->\s*<section class="contact-heading".*?</section>\s*', "", c, flags=re.S)
    c = re.sub(r'<section class="contact-heading".*?</section>\s*', "", c, flags=re.S)

    # 3) Swap the CSS control block.
    c = re.sub(r'<style id="cro-contact-fix">.*?</style>', CSS, c, flags=re.S)

    # 4) Insert the hero (with the form) before the contact-section.
    anchor = '<section class="contact-section">'
    if anchor not in c:
        raise SystemExit("contact-section anchor missing.")
    c = c.replace(anchor, hero(form_html) + anchor, 1)

    res = w.update_content("pages", PAGE_ID, c, live=live)
    print(("LIVE" if live else "DRY-RUN"),
          "form lifted into hero; new len", len(c))


if __name__ == "__main__":
    main()
