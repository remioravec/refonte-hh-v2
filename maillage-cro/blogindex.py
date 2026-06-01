#!/usr/bin/env python3
"""
Rebuild the /blog/ index page (WP page id 141) with a clean, modern card grid.

Fixes the broken thumbnails (the old page shipped background-image:url('+fi+')
literally) and the polluted auto-excerpts (they captured the nav menu). Each card
gets: the featured image if any, otherwise a premium branded placeholder
(category gradient + icon); a clean first-paragraph excerpt; category tag; author
+ date + reading time. Same home header/footer chrome as the articles. Includes a
vanilla-JS search + category filter and a "load more".

Usage:
  python3 blogindex.py            # DRY-RUN -> preview-tpl/blog.html
  python3 blogindex.py --live     # write WP page 141 (with backup)
"""

import os
import re
import sys
import json
import glob
import html
import datetime

import wp_common as wp
import clusters as C
import template as T

HERE = os.path.dirname(__file__)
BLOG_PAGE_ID = 141
PER_PAGE = 12  # cards shown before "load more"

# Category -> (label, gradient colors, inline SVG icon path)
CAT = {
    "stock": ("Gestion de stock", "#0ea5e9,#0369a1", "M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"),
    "couts": ("Coûts & marges", "#f59e0b,#b45309", "M12 8c-1.7 0-3 .9-3 2s1.3 2 3 2 3 .9 3 2-1.3 2-3 2m0-8V7m0 9v1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"),
    "tracabilite": ("Traçabilité & qualité", "#22c55e,#15803d", "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
    "fabrication": ("Production", "#6366f1,#4338ca", "M11 4a2 2 0 114 0v1a2 2 0 01-2 2H9a2 2 0 01-2-2V4zM3 8h18M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8"),
    "facturation": ("Facturation", "#02587f,#0d2b44", "M9 7h6m-6 4h6m-6 4h4M5 3h14a2 2 0 012 2v16l-3-2-3 2-3-2-3 2-3-2V5a2 2 0 012-2z"),
    "traiteur": ("ERP traiteur", "#ec4899,#9d174d", "M3 3h18v4H3zM6 7v14M18 7v14M6 12h12"),
    "viande": ("ERP viande", "#ef4444,#991b1b", "M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"),
    "maraicher": ("Fruits & légumes", "#16a34a,#166534", "M12 2C8 6 6 9 6 13a6 6 0 0012 0c0-4-2-7-6-11z"),
    "boulanger": ("Boulangerie", "#d97706,#92400e", "M4 11h16v3a4 4 0 01-4 4H8a4 4 0 01-4-4v-3zM6 11V8a6 6 0 0112 0v3"),
    "negoce": ("Négoce & distribution", "#0891b2,#155e75", "M3 9l9-6 9 6v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"),
    "erp_techno": ("ERP agroalimentaire", "#02587f,#38bdf8", "M9 3v18M3 9h18M3 15h18M15 3v18"),
    "comparatifs": ("Comparatif ERP", "#7c3aed,#5b21b6", "M9 17V9m6 8V5M5 21h14"),
    "integrateur": ("Intégration ERP", "#0d9488,#115e59", "M13 10V3L4 14h7v7l9-11h-7z"),
}
DEFAULT_CAT = ("Ressources ERP", "#02587f,#0d2b44", "M4 19.5A2.5 2.5 0 016.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z")


def excerpt_for(slug, raw_by_slug):
    raw = raw_by_slug.get(slug)
    if not raw:
        return ""
    data = T.extract(raw)
    if not data:
        return ""
    # first real paragraph of the prose
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", data["body"], re.S):
        t = T.txt(m.group(1))
        if len(t) > 60:
            return (t[:155].rsplit(" ", 1)[0] + "…") if len(t) > 155 else t
    return ""


def reading_for(slug, raw_by_slug):
    raw = raw_by_slug.get(slug)
    if not raw:
        return 5
    d = T.extract(raw)
    if not d:
        return 5
    w = len(re.findall(r"[A-Za-zÀ-ÿ0-9]+", T.txt(d["body"])))
    return max(2, round(w / 200))


def build():
    data = json.load(open(os.path.join(HERE, "blogdata.json")))["posts"]
    # raw content by slug from backups for clean excerpts
    raw_by_slug = {}
    for f in glob.glob(os.path.join(HERE, "backup-live-20260529-223414", "post_*.json")) + \
             glob.glob(os.path.join(HERE, "backup-live-20260529-223301", "post_*.json")):
        m = re.search(r"post_\d+_(.+)\.before\.json$", os.path.basename(f))
        if m and m.group(1) not in raw_by_slug:
            raw_by_slug[m.group(1)] = json.load(open(f)).get("content", {}).get("raw", "")

    # newest first
    data.sort(key=lambda p: p["date"], reverse=True)

    cards = []
    for p in data:
        slug = p["slug"]
        primary, _ = C.cluster_of(slug)
        label, grad, icon = CAT.get(primary, DEFAULT_CAT)
        title = html.escape(p["title"])
        exc = html.escape(excerpt_for(slug, raw_by_slug) or "Découvrez nos conseils et bonnes pratiques pour l'ERP agroalimentaire.")
        date_fr = T.fr_date(p["date"])
        reading = reading_for(slug, raw_by_slug)
        link = p["link"]
        if p["img"]:
            thumb = (f'<div class="bgx-thumb" style="background-image:url(\'{p["img"]}\')">'
                     f'<span class="bgx-cat">{html.escape(label)}</span></div>')
        else:
            thumb = (f'<div class="bgx-thumb bgx-ph" style="background:linear-gradient(135deg,{grad})">'
                     f'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" '
                     f'stroke-linejoin="round" opacity="0.9"><path d="{icon}"/></svg>'
                     f'<span class="bgx-cat">{html.escape(label)}</span></div>')
        cards.append(
            f'<a class="bgx-card" href="{link}" data-cat="{primary or "autre"}" '
            f'data-search="{html.escape((p["title"]+" "+label).lower())}">'
            f'{thumb}<div class="bgx-body"><h3>{title}</h3><p>{exc}</p>'
            f'<div class="bgx-meta"><span class="bgx-av">TJ</span>'
            f'<span>Timothy Jollivet · {date_fr} · {reading} min</span></div></div></a>')

    # category filter pills (only clusters present)
    present = []
    seen = set()
    for p in data:
        pr, _ = C.cluster_of(p["slug"])
        if pr and pr not in seen:
            seen.add(pr)
            present.append((pr, CAT.get(pr, DEFAULT_CAT)[0]))
    pills = ['<button class="bgx-pill on" data-f="all">Tout</button>'] + [
        f'<button class="bgx-pill" data-f="{pr}">{html.escape(lbl)}</button>' for pr, lbl in present]

    return cards, "".join(pills)


CSS = """
<style id="bgx-css">
#hh-page .bgx-wrap{max-width:1180px;margin:0 auto;padding:0 20px 72px}
#hh-page .bgx-hero{background:linear-gradient(135deg,#0D2B44,#0a3d5c 60%,#0f172a);color:#fff;
padding:120px 20px 64px;text-align:center;position:relative;overflow:hidden}
#hh-page .bgx-hero::after{content:"";position:absolute;top:-120px;right:-80px;width:460px;height:460px;
background:radial-gradient(circle,rgba(2,88,127,.35),transparent 70%);pointer-events:none}
#hh-page .bgx-hero h1{font-size:clamp(2rem,4.4vw,3rem);font-weight:800;margin:0 0 14px;letter-spacing:-.01em}
#hh-page .bgx-hero p{color:#cbd5e1;font-size:1.05rem;max-width:60ch;margin:0 auto}
#hh-page .bgx-tools{display:flex;gap:14px;flex-wrap:wrap;align-items:center;justify-content:space-between;
margin:-32px auto 28px;max-width:1180px;background:#fff;border:1px solid #e8eef5;border-radius:16px;
padding:16px 18px;box-shadow:0 12px 34px rgba(13,43,68,.10);position:relative;z-index:3}
#hh-page .bgx-search{flex:1 1 240px;display:flex;align-items:center;gap:8px;border:1px solid #e2e8f0;border-radius:11px;padding:9px 12px}
#hh-page .bgx-search input{border:none;outline:none;width:100%;font-size:.95rem;font-family:inherit}
#hh-page .bgx-search svg{width:18px;height:18px;color:#94a3b8;flex:0 0 18px}
#hh-page .bgx-pills{display:flex;gap:8px;flex-wrap:wrap}
#hh-page .bgx-pill{border:1px solid #e2e8f0;background:#fff;border-radius:999px;padding:8px 14px;font-size:.82rem;
font-weight:600;color:#334155;cursor:pointer;font-family:inherit}
#hh-page .bgx-pill.on{background:#02587f;color:#fff;border-color:#02587f}
#hh-page .bgx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:26px}
#hh-page .bgx-card{display:flex;flex-direction:column;background:#fff;border:1px solid #e8eef5;border-radius:18px;
overflow:hidden;text-decoration:none!important;color:inherit!important;box-shadow:0 6px 22px rgba(13,43,68,.06);
transition:transform .18s ease,box-shadow .18s ease}
#hh-page .bgx-card:hover{transform:translateY(-5px);box-shadow:0 18px 40px rgba(13,43,68,.13)}
#hh-page .bgx-thumb{position:relative;height:172px;background-size:cover;background-position:center;
display:flex;align-items:flex-end;padding:12px}
#hh-page .bgx-thumb.bgx-ph{align-items:center;justify-content:center}
#hh-page .bgx-thumb.bgx-ph svg{width:54px;height:54px;position:absolute;opacity:.9}
#hh-page .bgx-cat{position:relative;background:rgba(255,255,255,.92);color:#0d2b44;font-size:.7rem;font-weight:700;
text-transform:uppercase;letter-spacing:.04em;padding:5px 10px;border-radius:999px}
#hh-page .bgx-thumb.bgx-ph .bgx-cat{position:absolute;bottom:12px;left:12px}
#hh-page .bgx-body{padding:18px 18px 20px;display:flex;flex-direction:column;flex:1}
#hh-page .bgx-body h3{font-size:1.08rem;font-weight:800;color:#0d2b44;line-height:1.35;margin:0 0 8px}
#hh-page .bgx-body p{font-size:.9rem;color:#64748b;line-height:1.6;margin:0 0 16px;flex:1}
#hh-page .bgx-meta{display:flex;align-items:center;gap:10px;font-size:.78rem;color:#94a3b8}
#hh-page .bgx-av{width:30px;height:30px;flex:0 0 30px;border-radius:50%;background:linear-gradient(135deg,#02587f,#38bdf8);
color:#fff;display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:700}
#hh-page .bgx-more{display:block;margin:36px auto 0;background-color:#16a34a;background-image:linear-gradient(135deg,#22c55e,#16a34a);
color:#fff!important;border:none;font-weight:700;font-size:.95rem;padding:14px 28px;border-radius:12px;cursor:pointer;
box-shadow:0 10px 24px rgba(34,197,94,.28);font-family:inherit}
#hh-page .bgx-more:hover{transform:translateY(-2px)}
#hh-page .bgx-empty{text-align:center;color:#94a3b8;padding:40px;display:none}
@media(max-width:560px){#hh-page .bgx-hero{padding:100px 18px 52px}#hh-page .bgx-tools{flex-direction:column;align-items:stretch}}
</style>"""


def render():
    cards, pills = build()
    per = PER_PAGE
    cards_html = "\n".join(cards)
    js = ("""<script>(function(){
var grid=document.getElementById('bgxGrid'),cards=[].slice.call(grid.querySelectorAll('.bgx-card'));
var per=%d,shown=per,flt='all',q='';
function apply(){var n=0;cards.forEach(function(c){var ok=(flt==='all'||c.dataset.cat===flt)&&(q===''||c.dataset.search.indexOf(q)>-1);
c.dataset.match=ok?'1':'0';});
var matched=cards.filter(function(c){return c.dataset.match==='1';});
cards.forEach(function(c){c.style.display='none';});
matched.slice(0,shown).forEach(function(c){c.style.display='';});
document.getElementById('bgxMore').style.display=matched.length>shown?'block':'none';
document.getElementById('bgxEmpty').style.display=matched.length===0?'block':'none';}
document.getElementById('bgxSearch').addEventListener('input',function(e){q=e.target.value.toLowerCase().trim();shown=per;apply();});
[].slice.call(document.querySelectorAll('.bgx-pill')).forEach(function(b){b.addEventListener('click',function(){
document.querySelectorAll('.bgx-pill').forEach(function(x){x.classList.remove('on');});b.classList.add('on');flt=b.dataset.f;shown=per;apply();});});
document.getElementById('bgxMore').addEventListener('click',function(){shown+=per;apply();});
apply();})();</script>""" % per)

    inner = f"""<!-- wp:html -->
{T.CSS}{CSS}
<div id="hh-page" class="hha-tpl">
{T.HOME_HEADER}
{T.HOME_MOBILEMENU}
<header class="bgx-hero"><h1>Ressources &amp; actualités ERP</h1>
<p>Guides, comparatifs et conseils pour piloter votre entreprise agroalimentaire avec un ERP métier.</p></header>
<div class="bgx-wrap">
  <div class="bgx-tools">
    <div class="bgx-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input id="bgxSearch" type="search" placeholder="Rechercher un article, un thème…"></div>
    <div class="bgx-pills">{pills}</div>
  </div>
  <div class="bgx-grid" id="bgxGrid">
{cards_html}
  </div>
  <p class="bgx-empty" id="bgxEmpty">Aucun article ne correspond à votre recherche.</p>
  <button class="bgx-more" id="bgxMore">Charger plus d'articles</button>
</div>
{T.HOME_FOOTER}
</div>
<script>{T.NAV_JS}</script>
{js}
<!-- /wp:html -->"""
    return inner


def main():
    live = "--live" in sys.argv
    htmlout = render()
    if live:
        full = wp.api(f"pages/{BLOG_PAGE_ID}?context=edit&_fields=id,slug,content")
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        bdir = os.path.join(HERE, f"backup-tpl-{ts}")
        os.makedirs(bdir, exist_ok=True)
        json.dump(full, open(os.path.join(bdir, f"page_{BLOG_PAGE_ID}_blog.before.json"), "w"), ensure_ascii=False)
        wp.update_content("pages", BLOG_PAGE_ID, htmlout, live=True)
        print(f"WROTE /blog/ (page {BLOG_PAGE_ID}); backup backup-tpl-{ts}/")
    else:
        os.makedirs(os.path.join(HERE, "preview-tpl"), exist_ok=True)
        open(os.path.join(HERE, "preview-tpl", "blog.html"), "w").write(htmlout)
        print("dry-run -> preview-tpl/blog.html (len %d)" % len(htmlout))


if __name__ == "__main__":
    main()
