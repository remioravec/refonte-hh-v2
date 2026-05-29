#!/usr/bin/env python3
"""
Uniform, conflict-free article template for helloharel.com blog posts.

Goal: every article has the SAME look — same typography, spacing, no overflow.
Layout:  Hero (breadcrumb + H1 + author bio)
         2 columns: LEFT = article content, RIGHT = sticky TOC + CTA (+ "À lire aussi")
         Footer

Conflict-free by construction:
  - REPLACES content.raw entirely with a self-contained block (no merge with the
    old per-article CSS/JS that was breaking the render).
  - Unique CSS namespace `hha-` (distinct from the existing `hh-` classes).
  - Every selector scoped under `.hha-root`; no global `*` rules leak out.
  - Critical layout props use !important to win over theme CSS.
  - Images/tables/long words bounded -> no horizontal overflow ("débordement").
  - Pure CSS sticky sidebar; no JavaScript.

Content is extracted from the existing page:
  - <h1> title, .article-author (name/role/avatar), and the editorial prose
    inside <main class="article-content"> (which already holds clean <h2 id="s-N">
    sections). The old marketing hero / FAQ / CTA banners are dropped.

Usage:
  python3 template.py                      # DRY-RUN all -> preview-tpl/<slug>.html
  python3 template.py --slugs a b          # restrict
  python3 template.py --live --slugs a     # WRITE pilot
  python3 template.py --live               # WRITE all (after approval)
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
MAIN_OPEN = re.compile(r'<main class="article-content"[^>]*>', re.I)

CLUSTER_LABEL = {
    "stock": "Gestion de stock", "couts": "Coût de revient", "tracabilite": "Traçabilité",
    "fabrication": "Production", "facturation": "Facturation", "traiteur": "ERP traiteur",
    "viande": "ERP viande", "maraicher": "Fruits & légumes", "boulanger": "ERP boulangerie",
    "negoce": "Négoce", "erp_techno": "ERP agroalimentaire", "comparatifs": "Comparatif ERP",
    "integrateur": "Intégration ERP",
}


def txt(s):
    return html.unescape(TAGS.sub("", s)).strip()


def extract(raw):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = txt(m.group(1)) if m else ""

    name = role = avatar = ""
    am = re.search(r'<div class="article-author">(.*?)</div>\s*</div>', raw, re.S)
    block = am.group(1) if am else ""
    mn = re.search(r'article-author-name">(.*?)<', block)
    mr = re.search(r'article-author-role">(.*?)<', block)
    mv = re.search(r'<img[^>]+src="([^"]+)"', block)
    name = txt(mn.group(1)) if mn else "Hello Harel"
    role = txt(mr.group(1)) if mr else "Expert ERP agroalimentaire"
    avatar = mv.group(1) if mv else ""

    mo = MAIN_OPEN.search(raw)
    if not mo:
        return None
    body = raw[mo.end():]
    end = re.search(r"</main>|<footer", body, re.I)
    body = body[:end.start()] if end else body
    body = body.strip()

    # Ensure each H2 has an id so the TOC can anchor to it
    toc = []
    counter = [0]

    def ensure_id(match):
        tag = match.group(0)
        inner = match.group(1)
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
    return {"title": title, "name": name, "role": role, "avatar": avatar,
            "body": body, "toc": toc}


def css():
    return """
.elementor-location-header,.elementor-location-footer,[data-elementor-type="header"],
[data-elementor-type="footer"],body>header,#masthead,#site-header,#colophon,.site-header,
.site-footer,.ast-above-header-wrap,.ast-below-header-wrap,header#header,.main-navigation{display:none!important}
.hha-root{--blue:#00B1F5;--green:#22C55E;--ink:#0f172a;--muted:#64748b;
font-family:'Inter',system-ui,-apple-system,sans-serif;color:#1f2937;line-height:1.7;
max-width:1180px;margin:0 auto;padding:0 20px 64px}
.hha-root *{box-sizing:border-box}
.hha-root img{max-width:100%!important;height:auto}
.hha-hero{padding:32px 0 24px;border-bottom:1px solid #eef2f7;margin-bottom:32px}
.hha-bc{font-size:.8rem;color:var(--muted);margin:0 0 12px}
.hha-bc a{color:var(--muted);text-decoration:none}
.hha-bc a:hover{color:var(--blue)}
.hha-hero h1{font-size:clamp(1.6rem,3.4vw,2.35rem);line-height:1.22;color:var(--ink);
font-weight:800;margin:0 0 20px;overflow-wrap:anywhere}
.hha-author{display:flex;align-items:center;gap:12px}
.hha-author img{width:48px;height:48px;border-radius:50%;flex:0 0 48px;object-fit:cover}
.hha-author .n{font-weight:700;color:var(--ink);display:block;font-size:.95rem;line-height:1.2}
.hha-author .r{color:var(--muted);font-size:.82rem}
.hha-wrap{display:grid!important;grid-template-columns:minmax(0,1fr) 320px;gap:48px;align-items:start}
.hha-content{min-width:0;overflow-wrap:anywhere}
.hha-content>section{margin:0}
.hha-content h2{font-size:1.5rem;font-weight:800;color:var(--ink);margin:2.4rem 0 1rem;
line-height:1.3;scroll-margin-top:24px}
.hha-content h3{font-size:1.18rem;font-weight:700;color:var(--ink);margin:1.8rem 0 .7rem}
.hha-content p{margin:0 0 1.1rem;font-size:1.02rem}
.hha-content ul,.hha-content ol{margin:0 0 1.2rem;padding-left:1.3rem}
.hha-content li{margin:.4rem 0}
.hha-content a{color:var(--blue);text-decoration:underline;text-underline-offset:2px;overflow-wrap:anywhere}
.hha-content img{border-radius:10px;margin:1rem 0}
.hha-content figure{margin:1.2rem 0;max-width:100%}
.hha-content figure.wp-block-table,.hha-content .wp-block-table{display:block;overflow-x:auto}
.hha-content table{width:100%;border-collapse:collapse;font-size:.92rem}
.hha-content th,.hha-content td{border:1px solid #e2e8f0;padding:.55rem .7rem;text-align:left;vertical-align:top}
.hha-content blockquote{margin:1.2rem 0;padding:.6rem 1rem;border-left:4px solid var(--blue);
background:#f8fbff;color:#334155;border-radius:0 8px 8px 0}
.hha-content pre{overflow-x:auto;background:#0f172a;color:#e2e8f0;padding:1rem;border-radius:10px}
.hha-side{position:sticky;top:24px;display:flex;flex-direction:column;gap:18px}
.hha-card{border:1px solid #e2e8f0;border-radius:14px;padding:18px;background:#fff}
.hha-card .t{font-size:.76rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:0 0 12px}
.hha-toc nav{display:flex;flex-direction:column;gap:8px;max-height:60vh;overflow-y:auto}
.hha-toc a{color:#334155;text-decoration:none;font-size:.9rem;line-height:1.35;
border-left:2px solid #e2e8f0;padding-left:10px}
.hha-toc a:hover{color:var(--blue);border-color:var(--blue)}
.hha-cta{background:linear-gradient(160deg,#f8fbff,#eef7ff);border-color:#cfe9fb}
.hha-cta p{margin:0 0 12px;font-weight:700;color:var(--ink)}
.hha-btn{display:block;text-align:center;background:linear-gradient(135deg,var(--green),#16a34a);
color:#fff!important;padding:.72rem 1rem;border-radius:10px;font-weight:700;text-decoration:none;margin-bottom:8px}
.hha-btn.sec{background:#fff;color:var(--blue)!important;border:1px solid var(--blue)}
.hha-aux ul{list-style:none;margin:0;padding:0}
.hha-aux li{margin:.55rem 0}
.hha-aux a{color:var(--blue);text-decoration:none;font-size:.9rem;font-weight:600}
.hha-footer{margin-top:56px;padding-top:24px;border-top:1px solid #eef2f7;color:var(--muted);
font-size:.85rem;display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;justify-content:center}
.hha-footer a{color:var(--muted);text-decoration:none}
.hha-footer a:hover{color:var(--blue)}
@media(max-width:900px){.hha-wrap{grid-template-columns:1fr!important}.hha-side{position:static}}
"""


FOOTER_LINKS = [("Accueil", "/"), ("Blog", "/blog/"), ("ERP agroalimentaire", "/agroalimentaire/"),
                ("Fonctionnalités", "/fonctionnalites/"), ("Tarifs", "/tarifs/"), ("Contact", "/contact/"),
                ("Mentions légales", "/mentions-legales/"), ("Confidentialité", "/politique-de-confidentialite/")]


def render(slug, data):
    title = html.escape(data["title"])
    toc = "".join(f'<a href="#{hid}">{html.escape(t)}</a>' for hid, t in data["toc"])
    av = (f'<img src="{data["avatar"]}" alt="{html.escape(data["name"])}" loading="lazy">'
          if data["avatar"] else "")

    explorer, evaluator, convinced, decision = cta_targets_for(slug)
    primary, _ = C.cluster_of(slug)
    sec_label = CLUSTER_LABEL.get(primary, "Découvrir Hello Harel")

    plan = PLAN.get(f"/blog/{slug}/", {})
    lat = [l for l in plan.get("new_links", []) if l["type"] == "lateral"][:3]
    aux = ""
    if lat:
        lis = "".join(f'<li><a href="{l["target"]}">{html.escape(l["anchor"])}</a></li>' for l in lat)
        aux = f'<div class="hha-card hha-aux"><p class="t">À lire aussi</p><ul>{lis}</ul></div>'

    foot = "".join(f'<a href="{h}">{html.escape(n)}</a>' for n, h in FOOTER_LINKS)

    inner = f"""<style>{css()}</style>
<div class="hha-root">
  <header class="hha-hero">
    <p class="hha-bc"><a href="/">Accueil</a> › <a href="/blog/">Blog</a> › {title}</p>
    <h1>{title}</h1>
    <div class="hha-author">{av}<span><span class="n">{html.escape(data['name'])}</span>
      <span class="r">{html.escape(data['role'])}</span></span></div>
  </header>
  <div class="hha-wrap">
    <main class="hha-content">
{data['body']}
    </main>
    <aside class="hha-side">
      <div class="hha-card hha-toc"><p class="t">Sommaire</p><nav>{toc}</nav></div>
      <div class="hha-card hha-cta">
        <p>Prêt à voir Hello Harel en action ?</p>
        <a class="hha-btn" href="{decision}">Demander une démo</a>
        <a class="hha-btn sec" href="{explorer}">{html.escape(sec_label)}</a>
      </div>
      {aux}
    </aside>
  </div>
  <footer class="hha-footer">{foot}</footer>
</div>"""
    return f"<!-- wp:html -->\n{inner}\n<!-- /wp:html -->"


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
        if not data or not data["body"] or not data["title"]:
            print(f"  SKIP {slug}: extraction failed")
            log.append({"slug": slug, "status": "skip"})
            continue
        new_raw = render(slug, data)
        # Guards
        if "hha-root" not in new_raw or "<h1" not in new_raw or len(data["body"]) < 200:
            print(f"  SKIP {slug}: guard failed (body {len(data['body'])})")
            log.append({"slug": slug, "status": "skip-guard"})
            continue
        if live:
            json.dump(full, open(os.path.join(bdir, f"post_{x['id']}_{slug}.before.json"), "w"),
                      ensure_ascii=False)
            wp.update_content("posts", x["id"], new_raw, live=True)
            print(f"  WROTE {slug}: h2={len(data['toc'])} body={len(data['body'])}")
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
