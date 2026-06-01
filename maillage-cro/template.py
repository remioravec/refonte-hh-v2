#!/usr/bin/env python3
"""
Uniform article template for helloharel.com — same look on 100% of posts.

Design reproduces the reference (dark hero + author bio, reading progress bar,
"Mode Lecture Rapide", 2 columns: article left / sticky TOC + demo CTA right,
share buttons, toast) BUT:

  - The site header (menu) and footer stay VISIBLE — no chrome hiding.
  - NO Tailwind/CDN dependency. All styles are self-contained, scoped under
    `.hha-tpl`, so there is zero conflict with the theme or other plugins, and
    nothing leaks out (no global selectors).
  - Native CSS grid for the 2-column layout (reliable; collapses on mobile).
  - Images/tables/long words bounded => no horizontal overflow.

The existing article content is extracted (title, author, prose, H2 -> TOC) and
injected into the prose body. extract() reads both the original markup
(<main class="article-content">) and a previously templated page
(<main class="hha-content"> / Tailwind variant), and strips HH-CRO leftovers,
so the script is safe to re-run.

Usage:
  python3 template.py                  # DRY-RUN all -> preview-tpl/<slug>.html
  python3 template.py --slugs a b      # restrict
  python3 template.py --live --slugs a # WRITE pilot
  python3 template.py --live           # WRITE all
"""

import os
import re
import sys
import json
import html
import datetime

import wp_common as wp
import clusters as C
import widgets as W
import bespoke as B
from cro_article import cta_targets_for

HERE = os.path.dirname(__file__)
INV = json.load(open(os.path.join(HERE, "inventory.json")))
ITEMS = {x["path"]: x for x in INV["items"]}
PLAN = json.load(open(os.path.join(HERE, "maillage-plan.json")))["plan"]

# Live URL status map (from the last full crawl) to never ship a link to a 404.
try:
    LIVE_STATUS = json.load(open(os.path.join(HERE, "crawl.json")))["status"]
except Exception:
    LIVE_STATUS = {}


def _asset(name):
    return open(os.path.join(HERE, "assets", name), encoding="utf-8").read()


# Verbatim site chrome captured from the HOME page (so header/footer are EXACTLY
# the same as the home) + the ORIGINAL article hero ("hero d'avant").
HOME_HEADER = _asset("home_header.html")
HOME_MOBILEMENU = _asset("home_mobilemenu.html")
HOME_FOOTER = _asset("home_footer.html")
HOME_CSS = _asset("home_header.css")          # scoped to #hh-page (+ harmless body rules)
HERO_CSS = _asset("article_hero.css")         # scoped to #hh-page
NAV_JS = _asset("home_nav.js")

TAGS = re.compile(r"<[^>]+>")
MAIN_OPEN = re.compile(r'<main class="(?:article-content|hha-content)"[^>]*>', re.I)
ARTICLE_OPEN = re.compile(r'<article[^>]*id="article-content"[^>]*>', re.I)
STRIP_HHCRO = re.compile(r"\s*<!-- HH-CRO:START -->.*?<!-- HH-CRO:END -->", re.S)
MONTHS = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
          "août", "septembre", "octobre", "novembre", "décembre"]

# Authors resolved reliably by WordPress user id (the article HTML only carries
# the default gravatar, so we never trust the markup for the photo).
AUTHOR_BY_ID = {
    2: {"name": "Timothy Jollivet",
        "role": "Président de Hello Harel · Expert ERP agroalimentaire depuis 2014",
        "photo": "https://www.helloharel.com/wp-content/uploads/2024/10/Timothy-Jolliver-President-de-Hello-Harel.jpeg"},
    5: {"name": "Rémi Oravec", "role": "Hello Harel · ERP agroalimentaire", "photo": ""},
    6: {"name": "Maxime Corteel", "role": "Hello Harel · ERP agroalimentaire", "photo": ""},
}
DEFAULT_AUTHOR = AUTHOR_BY_ID[2]

# Footer (Elementor footer isn't rendered on single posts by the theme, so we
# ship a faithful one inside the template; the site header stays visible).
FOOTER_NAV = [
    ("Accueil", "/"), ("ERP agroalimentaire", "/agroalimentaire/"),
    ("Fonctionnalités", "/fonctionnalites/"), ("Négoce", "/negoce/"),
    ("Comparatifs", "/comparatifs/"), ("Blog", "/blog/"),
    ("Tarifs", "/tarifs/"), ("Qui sommes-nous", "/qui-sommes-nous/"),
    ("Contact", "/contact/"),
]
FOOTER_LEGAL = [
    ("Mentions légales", "/mentions-legales/"), ("CGU", "/cgu/"),
    ("Politique de confidentialité", "/politique-de-confidentialite/"),
]
# Site nav (the theme builds the real menu in JS and does not render it on single
# posts, so we ship a faithful sticky header here so the menu is always visible).
HEADER_NAV = [
    ("ERP Agroalimentaire", "/agroalimentaire/"), ("Fonctionnalités", "/fonctionnalites/"),
    ("Négoce", "/negoce/"), ("Comparatifs", "/comparatifs/"), ("Blog", "/blog/"),
    ("Tarifs", "/tarifs/"),
]

CLUSTER_LABEL = {
    "stock": "Gestion de stock", "couts": "Coût de revient", "tracabilite": "Traçabilité & qualité",
    "fabrication": "Production", "facturation": "Facturation", "traiteur": "ERP traiteur",
    "viande": "ERP viande", "maraicher": "Fruits & légumes", "boulanger": "ERP boulangerie",
    "negoce": "Négoce & distribution", "erp_techno": "ERP agroalimentaire",
    "comparatifs": "Comparatif ERP", "integrateur": "Intégration ERP",
}

# Minimal inline SVG icons (no external icon lib).
ICON = {
    "zap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3m0 12v3M5.6 5.6l2.1 2.1m8.6 8.6l2.1 2.1M3 12h3m12 0h3M5.6 18.4l2.1-2.1m8.6-8.6l2.1-2.1"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>',
    "chev": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:12px;height:12px"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>',
    "clock": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
}


def txt(s):
    return html.unescape(TAGS.sub("", s)).strip()


def fr_date(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.split("T")[0])
        return f"{d.day} {MONTHS[d.month]} {d.year}"
    except Exception:
        return ""


def initials(name):
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    if not parts:
        return "HH"
    return (parts[0][:2] if len(parts) == 1 else parts[0][0] + parts[-1][0]).upper()


# Markers that signal the END of editorial prose inside the original <main>:
# the legacy per-article CTA blocks / share / related boxes. Everything from the
# first occurrence onward is dropped (we ship our own footer + CTA + related).
TAIL_MARKERS = [
    r'<div[^>]*class="[^"]*hh-cta-final', r'<div[^>]*class="[^"]*hh-cta',
    r'<div[^>]*class="[^"]*hh-related', r'<section[^>]*class="[^"]*hh-related',
    r'<div[^>]*class="[^"]*hh-share', r'<div[^>]*class="[^"]*hh-author',
    r'<div[^>]*class="[^"]*blog-cta', r'<div[^>]*class="[^"]*post-cta',
    r'<div[^>]*class="[^"]*hh-newsletter',
]


# Dead/redirect links that must never ship in the prose (keeps SEO clean).
LINK_FIXES = {
    "/demo/": "/contact/", "/roi-calculator/": "/blog/roi-erp/",
    "/formation/": "/contact/", "/solutions/": "/agroalimentaire/",
    "/demonstration/": "/contact/", "/fonctionnalites/comptabilite/": "/fonctionnalites/facturation/",
    "/negoce/stocks-multi-dépôts/": "/negoce/stocks-multi-depots/",
    # comparatif slugs are blog posts -> prepend /blog/
    "/alternatives-sage-agroalimentaire/": "/blog/alternatives-sage-agroalimentaire/",
    "/alternatives-odoo-agroalimentaire/": "/blog/alternatives-odoo-agroalimentaire/",
    "/alternatives-silog-agroalimentaire/": "/blog/alternatives-silog-agroalimentaire/",
    "/alternatives-divalto-agroalimentaire/": "/blog/alternatives-divalto-agroalimentaire/",
    "/alternatives-cegid-distribution-alimentaire/": "/blog/alternatives-cegid-distribution-alimentaire/",
    "/alternatives-copilote-traiteur/": "/blog/alternatives-copilote-traiteur/",
    # non-existent feature pages -> closest real module/page
    "/fonctionnalites/business-intelligence/": "/fonctionnalites/",
    "/fonctionnalites/commande-fournisseur/": "/fonctionnalites/achat/",
    "/fonctionnalites/gestion-commerciale/": "/fonctionnalites/vente/",
    "/fonctionnalites/haccp/": "/blog/conformite-haccp/",
    "/fonctionnalites/tarifs/": "/tarifs/",
    "/fonctionnalites/traçabilite/": "/fonctionnalites/gestion-de-stock/",
    "/fonctionnalites/tracabilite/": "/fonctionnalites/gestion-de-stock/",
    "/les-meilleurs-logiciels-de-prise-de-commande-en-2024/": "/blog/bon-de-commande/",
    # Post 5910 front-404 (server permalink issue) — route inbound links to a
    # live, relevant page until permalinks are flushed in WP admin.
    "/blog/logiciel-maree-mareyeur/": "/negoce/",
}


def _balance_tags(body, tag):
    """Remove unmatched </tag> closers (which would break our wrappers) and
    append any missing closers for tags left open. Order-aware via a depth walk."""
    token = re.compile(rf"<{tag}\b[^>]*>|</{tag}>", re.I)
    out, depth, last = [], 0, 0
    for m in token.finditer(body):
        out.append(body[last:m.start()])
        tok = m.group(0)
        if tok.lower().startswith(f"</{tag}"):
            if depth == 0:
                pass  # drop this unmatched closer
            else:
                depth -= 1
                out.append(tok)
        else:
            depth += 1
            out.append(tok)
        last = m.end()
    out.append(body[last:])
    res = "".join(out)
    if depth > 0:
        res += f"\n</{tag}>" * depth
    return res


def clean_body(body):
    """Truncate trailing legacy CTA/share blocks and balance stray tags so the
    extracted prose can't corrupt the template grid."""
    # Cut trailing legacy CTA/share blocks FIRST (before unwrapping), then unwrap
    # every <div>/<section> layout container (keep inner content). The article
    # prose then becomes pure semantic flow (h2/h3/p/ul/table/blockquote/img),
    # which cannot escape or break our grid — the key to a stable, identical
    # rendering on every post.
    cut = len(body)
    for pat in TAIL_MARKERS:
        m = re.search(pat, body, re.I)
        if m and m.start() < cut:
            cut = m.start()
    body = body[:cut].rstrip()
    # Some articles have a FULL nested HTML document pasted inside the content
    # (<!DOCTYPE><html><head>…</head><body>…). Strip the scaffolding and drop the
    # <head> entirely (its CSS/meta must not leak); keep everything else as prose.
    body = re.sub(r"<!DOCTYPE[^>]*>", "", body, flags=re.I)
    body = re.sub(r"<head\b[^>]*>.*?</head>", "", body, flags=re.I | re.S)
    body = re.sub(r"</?(?:html|head|body|meta|title|link)\b[^>]*>", "", body, flags=re.I)
    # Strip embedded forms / interactive widgets pasted into the prose (we ship
    # our own CTA); they must not capture leads or break layout.
    body = re.sub(r"<form\b.*?</form>", "", body, flags=re.I | re.S)
    body = re.sub(r"<(?:button|input|select|textarea)\b[^>]*>(?:.*?</(?:button|select|textarea)>)?",
                  "", body, flags=re.I | re.S)
    # Unwrap ALL layout containers: remove every <div>/<section> open & close tag
    # (keep inner content). Leaves pure semantic prose that can't break the grid.
    body = re.sub(r"</?(?:div|section|main|article)\b[^>]*>", "", body, flags=re.I)
    # Also drop empty figures left behind and collapse blank lines.
    body = re.sub(r"<figure[^>]*>\s*</figure>", "", body, flags=re.I)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    # Rewrite dead/redirect links — both relative and absolute forms, with any
    # trailing querystring (e.g. /demo/?from=...).
    for dead, good in LINK_FIXES.items():
        for prefix in ('', 'https://www.helloharel.com', 'http://www.helloharel.com', 'https://helloharel.com'):
            body = re.sub(r'href="' + re.escape(prefix + dead) + r'[^"]*"', f'href="{good}"', body)
    return body.strip()


def extract(raw):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = txt(m.group(1)) if m else ""

    # Editorial body: prefer the original <main>, else a prior templated <article>
    mo = MAIN_OPEN.search(raw)
    if mo:
        body = raw[mo.end():]
        end = re.search(r"</main>|<footer", body, re.I)
        body = body[:end.start()] if end else body
    else:
        ao = ARTICLE_OPEN.search(raw)
        if not ao:
            return None
        body = raw[ao.end():]
        end = re.search(r"</article>", body, re.I)
        body = body[:end.start()] if end else body
    body = STRIP_HHCRO.sub("", body).strip()
    # Remove literal {{ }} artifacts left by an earlier buggy templating pass
    # (legitimate ERP article text never contains double braces).
    body = body.replace("{{", "").replace("}}", "")
    body = clean_body(body)

    toc = []
    counter = [0]

    def ensure_id(match):
        tag, inner = match.group(0), match.group(1)
        mid = re.search(r'id="([^"]+)"', tag)
        if mid:
            hid = mid.group(1)
        else:
            hid = f"hha-s{counter[0]}"
            tag = tag[:3] + f' id="{hid}"' + tag[3:]
        counter[0] += 1
        toc.append((hid, txt(inner)))
        return tag

    body = re.sub(r"<h2[^>]*>(.*?)</h2>", ensure_id, body, flags=re.S)
    return {"title": title, "body": body, "toc": toc}


# Styles: home chrome CSS (verbatim, scoped to #hh-page) + original hero CSS +
# our own content/grid/TOC/CTA CSS (scoped to .hha-tpl). No global selectors.
CSS = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style id="hha-home-css">""" + HOME_CSS + """</style>
<style id="hha-hero-css">""" + HERO_CSS + """</style>
<style id="hha-tpl-css">
.hha-tpl{--ink:#0D2B44;--blue:#02587F;--sky:#38bdf8;--muted:#64748b;--line:#e2e8f0;--bg:#F8FAFC;
font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1f2937;
line-height:1.7;-webkit-font-smoothing:antialiased}
.hha-tpl *,.hha-tpl *::before,.hha-tpl *::after{box-sizing:border-box}
.hha-progress{position:fixed;top:0;left:0;height:4px;width:0;z-index:10000;
background:linear-gradient(90deg,var(--blue),var(--sky));transition:width .1s}
.hha-shell{max-width:1180px;margin:0 auto;padding:36px 20px 64px;position:relative;z-index:2;background:var(--bg)}
.hha-grid{display:grid;grid-template-columns:1fr;gap:28px;align-items:start}
.hha-card{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:0 6px 24px rgba(13,43,68,.06)}
.hha-main{min-width:0;padding:26px}
.hha-skim{display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--bg);
border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:26px}
.hha-skim-l{display:flex;align-items:center;gap:12px}
.hha-skim-ic{width:38px;height:38px;flex:0 0 38px;border-radius:10px;background:#EBF5FA;color:var(--blue);
display:flex;align-items:center;justify-content:center}.hha-skim-ic svg{width:20px;height:20px}
.hha-skim h4{margin:0;font-size:.9rem;font-weight:700;color:#0f172a}
.hha-skim p{margin:2px 0 0;font-size:.78rem;color:var(--muted)}
.hha-switch{position:relative;width:46px;height:26px;flex:0 0 46px;border:none;border-radius:999px;
background:#cbd5e1;cursor:pointer;transition:background .2s}
.hha-switch[aria-checked="true"]{background:var(--blue)}
.hha-switch span{position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;
box-shadow:0 1px 3px rgba(0,0,0,.2);transition:transform .2s}
.hha-switch[aria-checked="true"] span{transform:translateX(20px)}
/* article typography (uniform across all posts) */
.hha-art{overflow-wrap:anywhere}
.hha-art>section{margin:0 0 1.5rem}
.hha-art h2{font-size:1.5rem;font-weight:800;color:var(--ink);line-height:1.35;margin:3.2rem 0 1.3rem;
scroll-margin-top:90px;display:flex;gap:10px;align-items:flex-start}
.hha-art h2::before{content:"";flex:0 0 6px;width:6px;height:1.4em;border-radius:999px;background:var(--blue);margin-top:.05em}
.hha-art h3{font-size:1.18rem;font-weight:700;color:var(--ink);margin:2.2rem 0 .8rem}
.hha-art p{margin:0 0 1.35rem;font-size:1.02rem;line-height:1.8}
.hha-art ul,.hha-art ol{margin:1rem 0 1.6rem;padding-left:1.4rem}
.hha-art li{margin:.6rem 0;line-height:1.7;padding-left:.2rem}.hha-art li::marker{color:var(--blue)}
.hha-art a{color:var(--blue);text-decoration:underline;text-underline-offset:2px;overflow-wrap:anywhere}
.hha-art img{max-width:100%!important;height:auto;border-radius:12px;margin:1rem 0}
.hha-art figure{margin:1.2rem 0;max-width:100%}
.hha-art figure.wp-block-table,.hha-art .wp-block-table{display:block;overflow-x:auto}
.hha-art table{width:100%;border-collapse:collapse;font-size:.92rem;margin:.4rem 0}
.hha-art th,.hha-art td{border:1px solid var(--line);padding:.6rem .7rem;text-align:left;vertical-align:top}
.hha-art thead th{background:var(--ink);color:#fff;font-weight:600}
.hha-art blockquote{margin:1.2rem 0;padding:.7rem 1.1rem;border-left:4px solid var(--blue);
background:#f1f8fc;color:#334155;border-radius:0 10px 10px 0}
.hha-art pre{overflow-x:auto;background:#0f172a;color:#e2e8f0;padding:1rem;border-radius:12px}
.hha-inline-links{background:#f1f8fc;border:1px solid #cfe9fb;border-left:4px solid var(--blue);
border-radius:0 10px 10px 0;padding:.7rem 1rem;font-size:.95rem;margin:1.2rem 0}
.hha-inline-links strong{color:var(--ink)}
.hha-inline-links a{color:var(--blue);font-weight:600}
.hha-ctab{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;
margin:3rem 0;padding:22px 26px;border-radius:18px;
background:radial-gradient(120% 160% at 0% 0%,#f4f9ff 0%,#fff 60%);
border:1px solid #d6e8f6;border-left:5px solid var(--blue);color:var(--ink);
box-shadow:0 10px 30px rgba(13,43,68,.07)}
.hha-ctab-txt{display:flex;flex-direction:column;gap:4px;min-width:0}
.hha-ctab-txt strong{font-size:1.1rem;font-weight:800;color:var(--ink)}
.hha-ctab-txt span{font-size:.88rem;color:var(--muted)}
.hha-ctab-btn{flex:0 0 auto;background-color:#16a34a;background-image:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;
font-weight:700;text-decoration:none;padding:13px 24px;border-radius:12px;white-space:nowrap;
box-shadow:0 10px 22px rgba(34,197,94,.28);transition:transform .15s ease,box-shadow .15s ease}
.hha-ctab-btn:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(34,197,94,.36)}
@media(max-width:560px){.hha-ctab{flex-direction:column;align-items:stretch;text-align:center}.hha-ctab-btn{text-align:center}}
/* Re-assert link styles: the home CSS sets `#hh-page a{color:inherit!important;
   text-decoration:none!important}`, so we override it with equal id-specificity. */
#hh-page .hha-art a{color:var(--blue)!important;text-decoration:underline!important;text-underline-offset:2px}
#hh-page .hha-inline-links a{color:var(--blue)!important;text-decoration:none!important;font-weight:600}
#hh-page .hha-toc a{color:#475569!important}
#hh-page .hha-toc a.active{color:var(--ink)!important}
#hh-page .hha-aux a{color:var(--blue)!important}
#hh-page .hha-cta .sec{color:var(--blue)!important}
#hh-page .hha-art a.hha-ctab-btn,#hh-page .hha-ctab a.hha-ctab-btn{color:#fff!important;text-decoration:none!important}
#hh-page .hha-share a,#hh-page .hha-share button{text-decoration:none!important}
#hh-page .hha-share a.tw,#hh-page .hha-share a.li{color:#fff!important}
.skimming-active .hha-art p{color:#94a3b8}
.skimming-active .hha-art strong{background:rgba(2,88,127,.14);color:var(--blue);font-weight:600;padding:0 4px;border-radius:4px}
.hha-share{margin-top:30px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;
background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:12px 18px}
.hha-share span.lbl{font-size:.85rem;font-weight:600;color:#475569}
.hha-share .btns{display:flex;gap:8px;align-items:center}
.hha-share a,.hha-share button{display:inline-flex;align-items:center;gap:6px;font-size:.78rem;font-weight:600;
text-decoration:none;border-radius:8px;padding:7px 12px;cursor:pointer;border:1px solid var(--line);background:#fff;color:#334155}
.hha-share a.tw{background:#0ea5e9;color:#fff;border-color:transparent}
.hha-share a.li{background:#1d4ed8;color:#fff;border-color:transparent}
.hha-share svg{width:14px;height:14px}
.hha-aside{display:flex;flex-direction:column;gap:20px}
.hha-side-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 6px 24px rgba(13,43,68,.06)}
.hha-side-h{font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);
margin:0 0 14px;display:flex;align-items:center;gap:8px}.hha-side-h svg{width:16px;height:16px;color:var(--blue)}
.hha-toc{display:flex;flex-direction:column;gap:4px;max-height:62vh;overflow-y:auto}
.hha-toc a{font-size:.88rem;line-height:1.35;color:#475569;text-decoration:none;padding:8px 12px;border-radius:8px;
border-left:2px solid transparent}
.hha-toc a:hover{color:var(--ink);background:var(--bg)}
.hha-toc a.active{color:var(--ink);background:var(--bg);border-left-color:var(--blue);font-weight:600}
/* CTA — light version */
.hha-cta{background:#fff;color:var(--ink);border:1px solid var(--line);
border-radius:18px;padding:22px;position:relative;overflow:hidden;box-shadow:0 6px 24px rgba(13,43,68,.06)}
.hha-cta::after{content:"";position:absolute;top:-50px;right:-50px;width:140px;height:140px;
background:radial-gradient(circle,rgba(2,88,127,.10),transparent 70%)}
.hha-cta-ic{width:46px;height:46px;border-radius:12px;background:var(--mykonosLight,#EBF5FA);color:var(--blue);
display:flex;align-items:center;justify-content:center;margin-bottom:14px;position:relative}.hha-cta-ic svg{width:24px;height:24px}
.hha-cta h3{margin:0 0 8px;font-size:1.2rem;font-weight:800;line-height:1.3;position:relative;color:var(--ink)}
.hha-cta p{margin:0 0 16px;font-size:.82rem;color:var(--muted);position:relative}
#hh-page .hha-btn{display:flex;align-items:center;justify-content:center;gap:8px;background-color:#16a34a!important;background-image:linear-gradient(135deg,#22c55e,#16a34a)!important;
color:#fff!important;font-weight:700;font-size:.95rem;padding:14px 18px;border-radius:12px;text-decoration:none!important;position:relative;
box-shadow:0 10px 22px rgba(34,197,94,.3);transition:transform .15s ease,box-shadow .15s ease}
#hh-page .hha-btn:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(34,197,94,.4)}.hha-btn svg{width:16px;height:16px}
.hha-cta .sec{display:block;text-align:center;color:var(--blue);font-size:.78rem;text-decoration:none;margin-top:10px;position:relative;font-weight:600}
.hha-cta .fine{margin:10px 0 0;font-size:.66rem;color:#94a3b8;text-align:center;position:relative}
/* Inter-H2 schema figures — airy, premium, lots of breathing room */
.hha-fig{margin:3.75rem 0;border:1px solid #e8eef5;border-radius:20px;
background:radial-gradient(120% 140% at 0% 0%,#f4f9ff 0%,#fff 55%);
padding:30px 32px;box-shadow:0 14px 40px rgba(13,43,68,.07)}
.hha-fig-cap{font-size:1.12rem;font-weight:800;color:var(--ink);margin:0;display:flex;align-items:center;gap:11px;line-height:1.35}
.hha-fig-cap svg{width:18px;height:18px;color:#fff;flex:0 0 34px;height:34px;width:34px;padding:8px;border-radius:10px;
background:linear-gradient(135deg,var(--blue),var(--sky));box-shadow:0 6px 14px rgba(2,88,127,.25)}
.hha-fig-sub{margin:10px 0 26px;font-size:.92rem;color:var(--muted);line-height:1.6;max-width:60ch}
.hha-fig-body{margin-top:6px}
.hha-flow{display:flex;align-items:stretch;gap:14px;flex-wrap:wrap}
.hha-flow-step{flex:1 1 0;min-width:120px;background:#fff;border:1px solid #e8eef5;border-radius:14px;
padding:18px 14px;text-align:center;box-shadow:0 4px 14px rgba(13,43,68,.05)}
.hha-flow-step b{display:block;font-size:1.05rem;color:var(--blue);margin-bottom:5px;line-height:1.2}
.hha-flow-step span{font-size:.78rem;color:var(--muted);line-height:1.4}
.hha-flow-arrow{display:flex;align-items:center;color:#b8c6d6}.hha-flow-arrow svg{width:22px;height:22px}
.hha-bars{display:flex;flex-direction:column;gap:18px}
.hha-bar-row{display:flex;align-items:center;gap:16px;font-size:.9rem;color:var(--ink)}
.hha-bar-row .lab{flex:0 0 170px;color:#334155;font-weight:600}
.hha-bar-track{flex:1;height:20px;background:#eef3f8;border-radius:999px;overflow:hidden}
.hha-bar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--blue),var(--sky));
box-shadow:inset 0 -2px 4px rgba(0,0,0,.08);transition:width .6s ease}
.hha-bar-val{flex:0 0 48px;text-align:right;font-weight:800;color:var(--ink)}
.hha-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px}
.hha-kpi{background:#fff;border:1px solid #e8eef5;border-radius:16px;padding:22px 14px;text-align:center;box-shadow:0 4px 14px rgba(13,43,68,.05)}
.hha-kpi .v{font-size:1.85rem;font-weight:800;color:var(--blue);line-height:1;letter-spacing:-.02em}
.hha-kpi .l{font-size:.78rem;color:var(--muted);margin-top:8px;line-height:1.35}
.hha-cycle{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}
.hha-cycle-node{background:#fff;color:var(--blue);border:1px solid #cfe3f2;border-radius:999px;
padding:12px 20px;font-size:.88rem;font-weight:700;box-shadow:0 3px 10px rgba(2,88,127,.08)}
@media(max-width:560px){.hha-fig{padding:22px 18px;margin:2.8rem 0}.hha-bar-row{gap:10px}.hha-bar-row .lab{flex:0 0 105px;font-size:.82rem}.hha-flow{gap:10px}}
/* Top interactive tool (light) */
.hha-tool{border:1px solid var(--line);border-radius:16px;background:linear-gradient(180deg,#f8fbff,#fff);
margin:0 0 26px;overflow:hidden;box-shadow:0 6px 20px rgba(13,43,68,.05)}
.hha-tool-h{padding:16px 18px 8px}
.hha-tool-badge{display:inline-block;background:var(--mykonosLight,#EBF5FA);color:var(--blue);font-weight:700;
font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;padding:4px 10px;border-radius:999px}
.hha-tool-h h3{margin:.5rem 0 .2rem;font-size:1.12rem;font-weight:800;color:var(--ink)}
.hha-tool-h p{margin:0;color:var(--muted);font-size:.85rem}
.hha-tool-b{padding:14px 18px 18px}
.hha-tg{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.hha-fld label{display:block;font-size:.78rem;font-weight:600;color:#334155;margin-bottom:4px}
.hha-fld input,.hha-fld select{width:100%;padding:9px 10px;border:1px solid #cbd5e1;border-radius:9px;font-size:.9rem}
.hha-out{margin-top:12px;padding:12px 14px;background:var(--mykonosLight,#EBF5FA);border:1px solid #cfe9fb;border-radius:11px}
.hha-out .v{font-size:1.5rem;font-weight:800;color:var(--blue);line-height:1.1}
.hha-out .l{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;font-weight:600}
.hha-out .n{margin:.3rem 0 0;font-size:.8rem;color:#475569}
#hh-page .hha-tool .hha-tbtn{display:inline-flex!important;align-items:center;gap:8px;margin-top:14px;
background-color:#16a34a!important;background-image:linear-gradient(135deg,#22c55e,#16a34a)!important;color:#fff!important;padding:13px 24px;border-radius:12px;
font-weight:700;text-decoration:none!important;font-size:.92rem;box-shadow:0 10px 22px rgba(34,197,94,.28);
transition:transform .15s ease,box-shadow .15s ease;letter-spacing:.01em}
#hh-page .hha-tool .hha-tbtn:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(34,197,94,.36)}
.hha-chk{display:flex;gap:8px;align-items:center;font-size:.86rem;color:#334155;margin:5px 0}
.hha-chk input{width:auto}
@media(max-width:560px){.hha-tg{grid-template-columns:1fr}}
/* Bespoke (hb-) visual primitives for the 10 flagship articles */
.hb-water{display:flex;flex-direction:column;gap:8px}
.hb-wrow{display:flex;align-items:center;gap:10px;font-size:.85rem}
.hb-wrow .lab{flex:0 0 150px;color:#334155}
.hb-wtrack{flex:1;height:18px;background:#eef2f7;border-radius:6px;overflow:hidden;display:flex}
.hb-wseg{height:100%}
.hb-wrow .val{flex:0 0 70px;text-align:right;font-weight:700;color:var(--ink)}
.hb-cmp{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.hb-card{border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center;background:#fff}
.hb-card .big{font-size:1.5rem;font-weight:800;line-height:1.1}
.hb-card .lbl{font-size:.74rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-top:4px}
.hb-card.win{border-color:var(--green);background:#f0fdf4}.hb-card.win .big{color:#16a34a}
.hb-gauge{height:14px;border-radius:999px;background:linear-gradient(90deg,#22c55e,#f59e0b,#ef4444);position:relative;margin:10px 0 6px}
.hb-gauge .mk{position:absolute;top:-5px;width:3px;height:24px;background:#0f172a;border-radius:2px;transition:left .3s}
.hb-gscale{display:flex;justify-content:space-between;font-size:.7rem;color:var(--muted)}
.hb-lots{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.hb-lot{border:1px solid var(--line);border-radius:12px;padding:12px;background:#fff;text-align:center;transition:all .25s}
.hb-lot.first{border-color:var(--blue);background:var(--mykonosLight,#EBF5FA);box-shadow:0 6px 18px rgba(2,88,127,.18);transform:translateY(-3px)}
.hb-lot .n{font-weight:700;color:var(--ink);font-size:.85rem}.hb-lot .d{font-size:.72rem;color:var(--muted);margin-top:3px}
.hb-lot .tag{display:none;margin-top:8px;font-size:.68rem;font-weight:700;color:#fff;background:var(--blue);border-radius:999px;padding:3px 8px}
.hb-lot.first .tag{display:inline-block}
.hb-pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.hb-pill{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 14px;font-size:.82rem;font-weight:600;color:#334155;cursor:pointer}
.hb-pill.on{background:var(--blue);color:#fff;border-color:var(--blue)}
.hb-spark{display:flex;align-items:flex-end;gap:4px;height:60px}
.hb-spark span{flex:1;background:linear-gradient(180deg,var(--sky),var(--blue));border-radius:3px 3px 0 0;min-height:4px}
.hb-badge{display:inline-block;font-weight:800;border-radius:10px;padding:6px 14px;font-size:1rem}
@media(max-width:560px){.hb-cmp{grid-template-columns:1fr}.hb-lots{grid-template-columns:1fr}.hb-wrow .lab{flex:0 0 110px}}
.hha-aux nav{display:flex;flex-direction:column;gap:2px}
.hha-aux a{font-size:.88rem;font-weight:600;color:var(--blue);text-decoration:none;padding:7px 10px;border-radius:8px}
.hha-aux a:hover{background:#EBF5FA}
.hha-toast{position:fixed;bottom:24px;right:24px;background:#0f172a;color:#fff;font-size:.85rem;border-radius:12px;
padding:12px 16px;box-shadow:0 12px 30px rgba(0,0,0,.25);transform:translateY(120px);opacity:0;
transition:all .3s;z-index:9999}.hha-toast.show{transform:translateY(0);opacity:1}
.hha-foot{background:#0D2B44;color:#cbd5e1;margin-top:48px}
.hha-foot-in{max-width:1180px;margin:0 auto;padding:40px 20px 28px}
.hha-foot-brand{font-weight:800;color:#fff;font-size:1.15rem;letter-spacing:-.01em}
.hha-foot-tag{color:#94a3b8;font-size:.85rem;margin:6px 0 20px;max-width:46ch}
.hha-foot-nav{display:flex;flex-wrap:wrap;gap:10px 22px;padding-bottom:20px;border-bottom:1px solid #1e3147}
.hha-foot-nav a{color:#cbd5e1;text-decoration:none;font-size:.9rem}.hha-foot-nav a:hover{color:#fff}
.hha-foot-bot{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;justify-content:space-between;padding-top:18px}
.hha-foot-legal{display:flex;flex-wrap:wrap;gap:8px 16px}
.hha-foot-legal a{color:#94a3b8;text-decoration:none;font-size:.8rem}.hha-foot-legal a:hover{color:#fff}
.hha-foot-cp{color:#64748b;font-size:.78rem}
/* DOM order is: TOC, main, extras(CTA+related).
   MOBILE (single column) => TOC above content, CTA after content. */
.hha-toc-card{margin-bottom:0}
.hha-extras{display:flex;flex-direction:column;gap:20px}
@media(min-width:1024px){
.hha-grid{grid-template-columns:minmax(0,1fr) 340px;gap:32px}
.hha-main{grid-column:1;grid-row:1 / span 2;padding:36px}
.hha-toc-card{grid-column:2;grid-row:1;position:sticky;top:24px}
.hha-extras{grid-column:2;grid-row:2;position:sticky;top:24px}
}
</style>"""

JS = """
<script>
(function(){
var bar=document.getElementById('hha-progress');
var sections=Array.prototype.slice.call(document.querySelectorAll('.hha-art [id]'));
var links=Array.prototype.slice.call(document.querySelectorAll('.hha-toc a'));
function onScroll(){
  var st=window.pageYOffset||document.documentElement.scrollTop;
  var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;
  if(bar)bar.style.width=(h>0?(st/h*100):0)+'%';
  var idx=-1;
  for(var i=0;i<sections.length;i++){if(st+150>=sections[i].offsetTop)idx=i;}
  links.forEach(function(l){l.classList.remove('active');});
  if(idx>=0){if(links[idx])links[idx].classList.add('active');}
}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
var sw=document.getElementById('hha-skim');
if(sw)sw.addEventListener('click',function(){
  var a=document.body.classList.toggle('skimming-active');
  sw.setAttribute('aria-checked',a?'true':'false');
  toast(a?'Mode Lecture Rapide activé':'Mode Lecture Rapide désactivé');
});
var toastEl=document.getElementById('hha-toast');
function toast(m){if(!toastEl)return;toastEl.textContent=m;toastEl.classList.add('show');
  setTimeout(function(){toastEl.classList.remove('show');},2600);}
var cp=document.getElementById('hha-copy');
if(cp)cp.addEventListener('click',function(){
  var done=function(){toast('Lien copié !');};
  if(navigator.clipboard){navigator.clipboard.writeText(location.href).then(done,done);}else{done();}
});
// FAQ accordions: only if the imported content uses .faq-btn / .faq-content
document.querySelectorAll('.hha-art .faq-btn').forEach(function(b){b.addEventListener('click',function(){
  var c=b.nextElementSibling;if(!c)return;
  if(c.style.maxHeight){c.style.maxHeight=null;}else{c.style.maxHeight=c.scrollHeight+'px';}
});});
})();
</script>"""


def inject_mesh(slug, body_html):
    """Weave the planned CONTEXTUAL internal links (diversified anchors, from
    maillage-plan.json) into the prose so they survive every rebuild. Up-links
    (money pages) go in a box after the 1st paragraph; lateral links mid-article.
    All targets are validated against the live status map if available."""
    plan = PLAN.get(f"/blog/{slug}/")
    if not plan:
        return body_html
    up = [l for l in plan["new_links"] if l["type"] == "up"]
    lat = [l for l in plan["new_links"] if l["type"] == "lateral"]
    if not up and not lat:
        return body_html

    def good(t):
        st = LIVE_STATUS.get(t)
        return st is None or st == 200  # keep if unknown or 200; drop known-404

    up = [l for l in up if good(l["target"])][:3]
    lat = [l for l in lat if good(l["target"])][:3]

    def links(ls):
        return ", ".join(f'<a href="{l["target"]}">{html.escape(l["anchor"])}</a>' for l in ls)

    inserted = body_html
    # Up-links box after the first closing </p>
    if up:
        box = (f'<p class="hha-inline-links"><strong>À découvrir :</strong> {links(up)}.</p>')
        m = re.search(r"</p>", inserted, re.I)
        if m:
            inserted = inserted[:m.end()] + box + inserted[m.end():]
        else:
            inserted = box + inserted
    # Lateral links box before the last third (after a mid <h2> if present)
    if lat:
        box = (f'<p class="hha-inline-links"><strong>Sur le même thème :</strong> {links(lat)}.</p>')
        h2s = list(re.finditer(r"<h2[^>]*>", inserted, re.I))
        if len(h2s) >= 2:
            pos = h2s[len(h2s) // 2].start()
            inserted = inserted[:pos] + box + inserted[pos:]
        else:
            inserted += box
    return inserted


CTA_BANNER = (
    '<aside class="hha-ctab"><div class="hha-ctab-txt">'
    '<strong>Envie de voir Hello Harel sur vos données ?</strong>'
    '<span>Démonstration personnalisée, sans engagement — réponse sous 24&nbsp;h.</span></div>'
    '<a class="hha-ctab-btn" href="/contact/">Demander une démo</a></aside>')


def inject_cta_banner(body_html):
    """Insert ONE demo CTA banner before a mid-article H2 (after ~45% of the H2s).
    100% of CTAs point to /contact/ (demo request)."""
    h2s = list(re.finditer(r"<h2[^>]*>", body_html, re.I))
    if len(h2s) < 4:
        return body_html
    pos = h2s[int(len(h2s) * 0.55)].start()
    return body_html[:pos] + CTA_BANNER + body_html[pos:]


def render(slug, data, date_iso, author_id):
    title = html.escape(data["title"])
    primary, _ = C.cluster_of(slug)
    cat = html.escape(CLUSTER_LABEL.get(primary, "ERP agroalimentaire"))
    bc = html.escape((data["title"][:46] + "…") if len(data["title"]) > 47 else data["title"])
    explorer, _ev, _cv, decision = cta_targets_for(slug)
    date_fr = fr_date(date_iso)

    author = AUTHOR_BY_ID.get(author_id, DEFAULT_AUTHOR)
    a_name, a_role, a_photo = author["name"], author["role"], author["photo"]
    if a_photo:
        av = f'<img src="{a_photo}" alt="{html.escape(a_name)}" loading="lazy">'
    else:
        av = initials(a_name)

    toc = "\n".join(f'<a href="#{hid}">{html.escape(t)}</a>' for hid, t in data["toc"]) or \
        '<span style="font-size:.85rem;color:#94a3b8">—</span>'

    aux = ""
    lat = [l for l in PLAN.get(f"/blog/{slug}/", {}).get("new_links", []) if l["type"] == "lateral"][:3]
    if lat:
        items = "".join(f'<a href="{l["target"]}">{html.escape(l["anchor"])}</a>' for l in lat)
        aux = (f'<div class="hha-side-card hha-aux"><p class="hha-side-h">{ICON["book"]} À lire aussi</p>'
               f'<nav>{items}</nav></div>')

    # Visuals before pertinent H2s. Flagship articles (bespoke) use hand-crafted
    # visuals matched to their real H2 wording; others use the generic library.
    bvis = B.visuals_for(slug)
    state = {"n": 0, "placed": 0, "last": -9, "used": set()}

    def _ins(m):
        i = state["n"]
        state["n"] += 1
        h2txt = txt(re.sub(r"<[^>]+>", " ", m.group(1)))
        if i == 0 or state["placed"] >= 3 or (i - state["last"]) < 1:
            return m.group(0)
        fig = None
        if bvis:
            kl = h2txt.lower()
            for j, (kws, html_) in enumerate(bvis):
                if j in state["used"]:
                    continue
                if any(kw in kl for kw in kws):
                    fig = html_
                    state["used"].add(j)
                    break
        else:
            fig = W.schema_for(h2txt)
        if not fig:
            return m.group(0)
        state["placed"] += 1
        state["last"] = i
        return fig + m.group(0)

    body_html = re.sub(r"<h2[^>]*>(.*?)</h2>", _ins, data["body"], flags=re.S)
    body_html = inject_mesh(slug, body_html)
    body_html = inject_cta_banner(body_html)
    top = B.tool(slug) or W.top_tool(slug, data["title"])

    # Reading time from word count (~200 wpm).
    words = len(re.findall(r"[A-Za-zÀ-ÿ0-9]+", re.sub(r"<[^>]+>", " ", data["body"])))
    reading = max(1, round(words / 200))

    # Author avatar for the ORIGINAL hero (real photo, else initials chip).
    if a_photo:
        hero_av = f'<img src="{a_photo}" alt="{html.escape(a_name)}" loading="lazy">'
    else:
        hero_av = (f'<span style="display:flex;width:100%;height:100%;align-items:center;'
                   f'justify-content:center;background:#1e293b;color:#fff;font-weight:700">{initials(a_name)}</span>')

    hero = f"""<section class="article-hero">
    <div class="article-hero-inner">
        <div class="article-breadcrumb">
            <a href="/">Accueil</a><span class="bc-sep">{ICON["chev"]}</span><a href="/blog/">Blog</a><span class="bc-sep">{ICON["chev"]}</span><span style="color:rgba(255,255,255,0.5)">{bc}</span>
        </div>
        <div class="article-hero-meta">
            <span class="article-cat">{cat}</span>
            {f'<span class="article-date">{date_fr}</span>' if date_fr else ''}
            <span class="article-reading-time">{ICON["clock"]}<span>{reading} min de lecture</span></span>
        </div>
        <h1>{title}</h1>
        <div class="article-author">
            <div class="article-author-avatar">{hero_av}</div>
            <div class="article-author-info">
                <span class="article-author-name">{html.escape(a_name)}</span>
                <span class="article-author-role">{html.escape(a_role)}</span>
            </div>
        </div>
    </div>
</section>"""

    body = f"""<!-- wp:html -->
{CSS}
<div id="hh-page" class="hha-tpl">
<div class="hha-progress" id="hha-progress"></div>
{HOME_HEADER}
{HOME_MOBILEMENU}
{hero}
<div class="hha-shell">
  <div class="hha-grid">
    <div class="hha-side-card hha-toc-card">
      <p class="hha-side-h">{ICON["list"]} Sommaire de l'article</p>
      <nav class="hha-toc">{toc}</nav>
    </div>
    <div class="hha-card hha-main">
      {top}
      <div class="hha-skim">
        <div class="hha-skim-l"><span class="hha-skim-ic">{ICON["zap"]}</span>
          <div><h4>Mode Lecture Rapide</h4><p>Surlignez l'essentiel pour un survol efficace</p></div></div>
        <button class="hha-switch" id="hha-skim" role="switch" aria-checked="false"><span></span></button>
      </div>
      <article class="hha-art" id="article-content">
{body_html}
      </article>
      <div class="hha-share">
        <span class="lbl">Partager cet article</span>
        <div class="btns">
          <button id="hha-copy">{ICON["link"]} Copier le lien</button>
          <a class="tw" href="https://twitter.com/intent/tweet" target="_blank" rel="noopener">Twitter</a>
          <a class="li" href="https://www.linkedin.com/sharing/share-offsite/" target="_blank" rel="noopener">LinkedIn</a>
        </div>
      </div>
    </div>
    <div class="hha-extras">
      <div class="hha-cta">
        <div class="hha-cta-ic">{ICON["spark"]}</div>
        <h3>Révolutionnez votre gestion agroalimentaire</h3>
        <p>Traçabilité, coûts de revient, production et commandes : tout dans un ERP cloud spécialisé.</p>
        <a class="hha-btn" href="/contact/">Demander une démo {ICON["arrow"]}</a>
        <a class="sec" href="/contact/">Parler à un expert agroalimentaire →</a>
        <p class="fine">Présentation personnalisée en visioconférence sous 48h.</p>
      </div>
      {aux}
    </div>
  </div>
</div>
<div class="hha-toast" id="hha-toast"></div>
{HOME_FOOTER}
</div>
<script>{NAV_JS}</script>
{JS}
<!-- /wp:html -->"""
    return body


def load_backup_sources(dirs):
    """Map slug -> original post object from backup folders (first wins)."""
    import glob
    src = {}
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(HERE, d, "post_*.json"))):
            m = re.search(r"post_\d+_(.+)\.before\.json$", os.path.basename(f))
            if m and m.group(1) not in src:
                src[m.group(1)] = json.load(open(f))
    return src


def main():
    live = "--live" in sys.argv
    slugs = None
    if "--slugs" in sys.argv:
        i = sys.argv.index("--slugs")
        slugs = [s for s in sys.argv[i + 1:] if not s.startswith("--")]

    # Re-template from pristine originals rather than the (possibly already
    # templated/thinned) live content: --source-backup DIR1[,DIR2]
    src_backups = {}
    if "--source-backup" in sys.argv:
        i = sys.argv.index("--source-backup")
        dirs = sys.argv[i + 1].split(",")
        src_backups = load_backup_sources(dirs)
        print(f"Source backups loaded: {len(src_backups)} articles from {dirs}")

    posts = [x for x in INV["items"] if x["kind"] == "post" and x["path"].startswith("/blog/")]
    if slugs:
        posts = [x for x in posts if C.slug_of(x["path"]) in slugs]

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bdir = os.path.join(HERE, f"backup-tpl-{ts}")
    pdir = os.path.join(HERE, "preview-tpl")
    os.makedirs(bdir if live else pdir, exist_ok=True)

    log = []
    print(f"Mode: {'LIVE WRITE' if live else 'DRY-RUN'} | posts: {len(posts)}")
    for x in posts:
        slug = C.slug_of(x["path"])
        # Prefer pristine original content from backup; fall back to live.
        src = src_backups.get(slug)
        full = wp.get_raw("posts", x["id"])  # always get fresh author/date
        if src:
            raw = (src.get("content") or {}).get("raw", "") or ""  # pristine content
        else:
            raw = (full.get("content") or {}).get("raw", "") or ""
        data = extract(raw)
        if not data or not data["body"] or not data["title"] or len(data["body"]) < 200:
            print(f"  SKIP {slug}: extraction failed")
            log.append({"slug": slug, "status": "skip"})
            continue
        new_raw = render(slug, data, full.get("date", ""), full.get("author"))
        if "hha-tpl" not in new_raw or "<h1" not in new_raw:
            print(f"  SKIP {slug}: guard failed")
            log.append({"slug": slug, "status": "skip-guard"})
            continue
        if live:
            json.dump(full, open(os.path.join(bdir, f"post_{x['id']}_{slug}.before.json"), "w"), ensure_ascii=False)
            wp.update_content("posts", x["id"], new_raw, live=True)
            print(f"  WROTE {slug}: h2={len(data['toc'])}")
            log.append({"slug": slug, "status": "wrote", "h2": len(data["toc"])})
        else:
            open(os.path.join(pdir, f"{slug}.html"), "w").write(new_raw)
            print(f"  dry  {slug}: h2={len(data['toc'])} body={len(data['body'])}")
            log.append({"slug": slug, "status": "dry", "h2": len(data["toc"])})

    json.dump({"mode": "live" if live else "dry", "items": log},
              open(os.path.join(HERE, f"template-log-{ts}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"\nLog: template-log-{ts}.json" + (f" | backups: backup-tpl-{ts}/" if live else ""))


if __name__ == "__main__":
    main()
