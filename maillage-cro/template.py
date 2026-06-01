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
from cro_article import cta_targets_for

HERE = os.path.dirname(__file__)
INV = json.load(open(os.path.join(HERE, "inventory.json")))
ITEMS = {x["path"]: x for x in INV["items"]}
PLAN = json.load(open(os.path.join(HERE, "maillage-plan.json")))["plan"]

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
    r'<div[^>]*class="[^"]*hh-newsletter', r'<form\b',
]


# Dead/redirect links that must never ship in the prose (keeps SEO clean).
LINK_FIXES = {
    "/demo/": "/contact/", "/roi-calculator/": "/blog/roi-erp/",
    "/formation/": "/contact/", "/solutions/": "/agroalimentaire/",
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
    # Unwrap ALL layout containers: remove every <div>/<section> open & close tag
    # (keep inner content). Leaves pure semantic prose that can't break the grid.
    body = re.sub(r"</?(?:div|section|main|article)\b[^>]*>", "", body, flags=re.I)
    # Also drop empty figures left behind and collapse blank lines.
    body = re.sub(r"<figure[^>]*>\s*</figure>", "", body, flags=re.I)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    # Rewrite dead/redirect links (handle querystrings: /demo/?from=...).
    for dead, good in LINK_FIXES.items():
        body = re.sub(r'href="' + re.escape(dead) + r'[^"]*"', f'href="{good}"', body)
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


# Self-contained, scoped styles. No global selectors -> no conflict, no chrome hiding.
CSS = """
<style id="hha-tpl-css">
.hha-tpl{--ink:#0D2B44;--blue:#02587F;--sky:#38bdf8;--muted:#64748b;--line:#e2e8f0;--bg:#F8FAFC;
font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1f2937;
background:var(--bg);line-height:1.7;-webkit-font-smoothing:antialiased}
.hha-tpl *,.hha-tpl *::before,.hha-tpl *::after{box-sizing:border-box}
.hha-tpl a{color:var(--blue)}
.hha-progress{position:fixed;top:0;left:0;height:4px;width:0;z-index:10000;
background:linear-gradient(90deg,var(--blue),var(--sky));transition:width .1s}
.hha-nav{position:sticky;top:0;z-index:9000;background:rgba(255,255,255,.96);
backdrop-filter:saturate(180%) blur(8px);border-bottom:1px solid var(--line)}
.hha-nav-in{max-width:1180px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:18px}
.hha-logo{font-weight:800;color:var(--ink);font-size:1.15rem;text-decoration:none;letter-spacing:-.01em;flex:0 0 auto}
.hha-logo span{color:var(--blue)}
.hha-nav-links{display:none;gap:20px;margin-left:8px}
.hha-nav-links a{color:#334155;text-decoration:none;font-size:.92rem;font-weight:500}
.hha-nav-links a:hover{color:var(--blue)}
.hha-nav-cta{margin-left:auto;background:linear-gradient(135deg,var(--blue),#0284c7);color:#fff;
text-decoration:none;font-weight:700;font-size:.85rem;padding:9px 16px;border-radius:10px;white-space:nowrap}
.hha-nav-cta:hover{filter:brightness(1.08)}
@media(min-width:900px){.hha-nav-links{display:flex}}
.hha-hero{position:relative;overflow:hidden;background:linear-gradient(180deg,#0D2B44,#0b2238 60%,#0f172a);
color:#fff;padding:48px 20px 96px;text-align:center;border-bottom:1px solid #1e293b}
.hha-hero::after{content:"";position:absolute;top:-120px;right:-80px;width:420px;height:420px;
background:radial-gradient(circle,rgba(2,88,127,.35),transparent 70%);pointer-events:none}
.hha-hero-in{max-width:880px;margin:0 auto;position:relative;z-index:1}
.hha-bc{font-size:.8rem;color:#94a3b8;margin:0 0 18px}
.hha-bc a{color:#94a3b8;text-decoration:none}.hha-bc a:hover{color:#fff}.hha-bc .sep{color:#475569;margin:0 8px}
.hha-cat{display:inline-flex;align-items:center;gap:6px;font-size:.72rem;font-weight:600;text-transform:uppercase;
letter-spacing:.06em;color:var(--sky);background:rgba(15,23,42,.6);border:1px solid #334155;
padding:6px 12px;border-radius:999px;margin-bottom:22px}
.hha-cat svg{width:14px;height:14px}
.hha-hero h1{font-size:clamp(1.7rem,3.4vw,2.8rem);line-height:1.18;font-weight:800;letter-spacing:-.01em;
margin:0 auto 26px;max-width:18ch;overflow-wrap:anywhere}
.hha-bio{display:flex;gap:14px;align-items:center;text-align:left;max-width:520px;margin:0 auto;
background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:16px 18px}
.hha-bio-av{flex:0 0 52px;width:52px;height:52px;border-radius:50%;overflow:hidden;border:2px solid #fff;
display:flex;align-items:center;justify-content:center;background:#1e293b;color:#fff;font-weight:700;font-size:1.05rem}
.hha-bio-av img{width:100%;height:100%;object-fit:cover}
.hha-bio-name{font-weight:700;color:#fff;font-size:.95rem}
.hha-bio-meta{color:#94a3b8;font-size:.78rem;margin-left:6px}
.hha-bio-role{color:var(--sky);font-size:.8rem;font-weight:500;margin-top:2px}
.hha-shell{max-width:1180px;margin:-60px auto 0;padding:0 20px 64px;position:relative;z-index:2}
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
.hha-art>section{margin:0 0 8px}
.hha-art h2{font-size:1.5rem;font-weight:800;color:var(--ink);line-height:1.3;margin:2.2rem 0 1rem;
scroll-margin-top:90px;display:flex;gap:10px;align-items:flex-start}
.hha-art h2::before{content:"";flex:0 0 6px;width:6px;height:1.4em;border-radius:999px;background:var(--blue);margin-top:.05em}
.hha-art h3{font-size:1.18rem;font-weight:700;color:var(--ink);margin:1.6rem 0 .6rem}
.hha-art p{margin:0 0 1.1rem;font-size:1.02rem}
.hha-art ul,.hha-art ol{margin:0 0 1.2rem;padding-left:1.3rem}
.hha-art li{margin:.4rem 0}.hha-art li::marker{color:var(--blue)}
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
.hha-cta{background:linear-gradient(155deg,#0D2B44,#0f172a);color:#fff;border:1px solid #1e293b;
border-radius:18px;padding:22px;position:relative;overflow:hidden}
.hha-cta::after{content:"";position:absolute;top:-50px;right:-50px;width:140px;height:140px;
background:radial-gradient(circle,rgba(2,88,127,.4),transparent 70%)}
.hha-cta-ic{width:46px;height:46px;border-radius:12px;background:rgba(2,88,127,.2);color:var(--sky);
display:flex;align-items:center;justify-content:center;margin-bottom:14px;position:relative}.hha-cta-ic svg{width:24px;height:24px}
.hha-cta h3{margin:0 0 8px;font-size:1.2rem;font-weight:800;line-height:1.3;position:relative}
.hha-cta p{margin:0 0 16px;font-size:.82rem;color:#cbd5e1;position:relative}
.hha-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,var(--blue),#0284c7);
color:#fff;font-weight:700;font-size:.9rem;padding:12px 16px;border-radius:12px;text-decoration:none;position:relative;
box-shadow:0 8px 20px rgba(2,88,127,.3)}.hha-btn:hover{filter:brightness(1.08)}.hha-btn svg{width:16px;height:16px}
.hha-cta .sec{display:block;text-align:center;color:var(--sky);font-size:.78rem;text-decoration:none;margin-top:10px;position:relative}
.hha-cta .fine{margin:10px 0 0;font-size:.66rem;color:#94a3b8;text-align:center;position:relative}
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
@media(min-width:1024px){
.hha-grid{grid-template-columns:minmax(0,1fr) 340px;gap:32px}
.hha-aside{position:sticky;top:24px}
.hha-main{padding:36px}
}
</style>"""

JS = """
<script>
(function(){
var root=document.currentScript&&document.currentScript.closest?document.currentScript.parentNode:document;
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
  if(idx>=0&&links[idx])links[idx].classList.add('active');
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

    meta = f'<span class="hha-bio-meta">• Publié le {date_fr}</span>' if date_fr else ""
    nav_links = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in HEADER_NAV)
    foot_nav = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in FOOTER_NAV)
    foot_legal = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in FOOTER_LEGAL)
    year = datetime.datetime.now().year

    body = f"""<!-- wp:html -->
{CSS}
<div class="hha-tpl">
<div class="hha-progress" id="hha-progress"></div>
<nav class="hha-nav">
  <div class="hha-nav-in">
    <a class="hha-logo" href="/">Hello <span>Harel</span></a>
    <div class="hha-nav-links">{nav_links}</div>
    <a class="hha-nav-cta" href="/contact/">Demander une démo</a>
  </div>
</nav>
<header class="hha-hero">
  <div class="hha-hero-in">
    <nav class="hha-bc"><a href="/">Accueil</a><span class="sep">/</span><a href="/blog/">Blog</a><span class="sep">/</span>{bc}</nav>
    <span class="hha-cat">{ICON["tag"]} {cat}</span>
    <h1>{title}</h1>
    <div class="hha-bio">
      <div class="hha-bio-av">{av}</div>
      <div class="hha-bio-txt">
        <div><span class="hha-bio-name">{html.escape(a_name)}</span>{meta}</div>
        <div class="hha-bio-role">{html.escape(a_role)}</div>
      </div>
    </div>
  </div>
</header>
<div class="hha-shell">
  <div class="hha-grid">
    <div class="hha-card hha-main">
      <div class="hha-skim">
        <div class="hha-skim-l"><span class="hha-skim-ic">{ICON["zap"]}</span>
          <div><h4>Mode Lecture Rapide</h4><p>Surlignez l'essentiel pour un survol efficace</p></div></div>
        <button class="hha-switch" id="hha-skim" role="switch" aria-checked="false"><span></span></button>
      </div>
      <article class="hha-art" id="article-content">
{data['body']}
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
    <aside class="hha-aside">
      <div class="hha-side-card">
        <p class="hha-side-h">{ICON["list"]} Sommaire de l'article</p>
        <nav class="hha-toc">{toc}</nav>
      </div>
      <div class="hha-cta">
        <div class="hha-cta-ic">{ICON["spark"]}</div>
        <h3>Révolutionnez votre gestion agroalimentaire</h3>
        <p>Traçabilité, coûts de revient, production et commandes : tout dans un ERP cloud spécialisé.</p>
        <a class="hha-btn" href="{decision}">Demander une démo {ICON["arrow"]}</a>
        <a class="sec" href="{explorer}">Découvrir la solution →</a>
        <p class="fine">Présentation personnalisée en visioconférence sous 48h.</p>
      </div>
      {aux}
    </aside>
  </div>
</div>
<div class="hha-toast" id="hha-toast"></div>
<footer class="hha-foot">
  <div class="hha-foot-in">
    <div class="hha-foot-brand">Hello Harel</div>
    <p class="hha-foot-tag">L'ERP cloud spécialisé pour l'agroalimentaire : traçabilité, production, coûts de revient, négoce et conformité.</p>
    <nav class="hha-foot-nav">{foot_nav}</nav>
    <div class="hha-foot-bot">
      <div class="hha-foot-legal">{foot_legal}</div>
      <div class="hha-foot-cp">© {year} Hello Harel — Tous droits réservés.</div>
    </div>
  </div>
</footer>
</div>
{JS}
<!-- /wp:html -->"""
    return body


def main():
    live = "--live" in sys.argv
    slugs = None
    if "--slugs" in sys.argv:
        i = sys.argv.index("--slugs")
        slugs = [s for s in sys.argv[i + 1:] if not s.startswith("--")]

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
        full = wp.get_raw("posts", x["id"])
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
