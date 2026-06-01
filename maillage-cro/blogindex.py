#!/usr/bin/env python3
"""
/blog/ index (WP page id 141) rebuilt with the SITE'S OWN charte: native
.blog-section / .blog-grid / .blog-card classes (CSS already shipped via the home
stylesheet). Featured image when available, else the brand gradient placeholder
(#005F88→#3b82f6) with a faint icon — exactly like the rest of the site. Clean
first-paragraph excerpts, author + reading time, category, live search + category
filter + load-more. Home header/footer chrome.

Usage:
  python3 blogindex.py          # DRY-RUN -> preview-tpl/blog.html
  python3 blogindex.py --live   # write WP page 141 (with backup)
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
PER_PAGE = 12

CAT = {
    "stock": ("Gestion de stock", "M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"),
    "couts": ("Coûts & marges", "M12 8c-1.7 0-3 .9-3 2s1.3 2 3 2 3 .9 3 2-1.3 2-3 2m0-8V7m0 9v1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"),
    "tracabilite": ("Traçabilité & qualité", "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
    "fabrication": ("Production", "M11 4a2 2 0 114 0v1a2 2 0 01-2 2H9a2 2 0 01-2-2V4zM3 8h18M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8"),
    "facturation": ("Facturation", "M9 7h6m-6 4h6m-6 4h4M5 3h14a2 2 0 012 2v16l-3-2-3 2-3-2-3 2-3-2V5a2 2 0 012-2z"),
    "traiteur": ("ERP traiteur", "M3 3h18v4H3zM6 7v14M18 7v14M6 12h12"),
    "viande": ("ERP viande", "M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"),
    "maraicher": ("Fruits & légumes", "M12 2C8 6 6 9 6 13a6 6 0 0012 0c0-4-2-7-6-11z"),
    "boulanger": ("Boulangerie", "M4 11h16v3a4 4 0 01-4 4H8a4 4 0 01-4-4v-3zM6 11V8a6 6 0 0112 0v3"),
    "negoce": ("Négoce & distribution", "M3 9l9-6 9 6v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"),
    "erp_techno": ("ERP agroalimentaire", "M9 3v18M3 9h18M3 15h18M15 3v18"),
    "comparatifs": ("Comparatif ERP", "M9 17V9m6 8V5M5 21h14"),
    "integrateur": ("Intégration ERP", "M13 10V3L4 14h7v7l9-11h-7z"),
}
DEFAULT_CAT = ("Ressources ERP", "M4 19.5A2.5 2.5 0 016.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z")


def _raw_by_slug():
    out = {}
    for f in glob.glob(os.path.join(HERE, "backup-live-20260529-223414", "post_*.json")) + \
             glob.glob(os.path.join(HERE, "backup-live-20260529-223301", "post_*.json")):
        m = re.search(r"post_\d+_(.+)\.before\.json$", os.path.basename(f))
        if m and m.group(1) not in out:
            out[m.group(1)] = json.load(open(f)).get("content", {}).get("raw", "")
    return out


def build():
    data = json.load(open(os.path.join(HERE, "blogdata.json")))["posts"]
    raw_by_slug = _raw_by_slug()
    data.sort(key=lambda p: p["date"], reverse=True)

    cards, present, seen = [], [], set()
    for p in data:
        slug = p["slug"]
        primary, _ = C.cluster_of(slug)
        label, icon = CAT.get(primary, DEFAULT_CAT)
        if primary and primary not in seen:
            seen.add(primary)
            present.append((primary, label))
        title = html.escape(p["title"])
        d = T.extract(raw_by_slug.get(slug, "")) if raw_by_slug.get(slug) else None
        exc = ""
        reading = 5
        if d:
            for mm in re.finditer(r"<p[^>]*>(.*?)</p>", d["body"], re.S):
                t = T.txt(mm.group(1))
                if len(t) > 60:
                    exc = (t[:150].rsplit(" ", 1)[0] + "…") if len(t) > 150 else t
                    break
            reading = max(2, round(len(re.findall(r"[A-Za-zÀ-ÿ0-9]+", T.txt(d["body"]))) / 200))
        exc = html.escape(exc or "Conseils et bonnes pratiques pour l'ERP agroalimentaire.")
        date_fr = T.fr_date(p["date"])
        if p["img"]:
            img = (f'<div class="blog-card-img" style="background-image:url(\'{p["img"]}\')!important;'
                   f'background-size:cover!important;background-position:center!important"></div>')
        else:
            img = (f'<div class="blog-card-img"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">'
                   f'<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="{icon}"/></svg></div>')
        cards.append(
            f'<a class="blog-card" href="{p["link"]}" data-cat="{primary or "autre"}" '
            f'data-search="{html.escape((p["title"]+" "+label).lower())}">{img}'
            f'<div class="blog-card-body">'
            f'<span class="blog-card-date">{html.escape(label)} · {date_fr}</span>'
            f'<h3 class="blog-card-title">{title}</h3>'
            f'<p class="blog-card-excerpt">{exc}</p>'
            f'<div class="blog-card-author"><span class="blog-card-avatar">TJ</span>'
            f'<span><span class="blog-card-author-name">Timothy Jollivet</span>'
            f'<span class="blog-card-read-time">{reading} min de lecture</span></span></div>'
            f'</div></a>')

    pills = ['<button class="bgx-pill on" data-f="all">Tout</button>'] + [
        f'<button class="bgx-pill" data-f="{pr}">{html.escape(lbl)}</button>' for pr, lbl in present]
    return cards, "".join(pills)


# Minimal charte-aligned CSS: only hero + tools + load-more (cards/grid come from
# the site's own .blog-section/.blog-grid/.blog-card).
CSS = """
<style id="bgx-css">
#hh-page .bgx-hero{background:linear-gradient(135deg,#005F88 0%,#0a3d5c 60%,#0f172a 100%);color:#fff;
padding:128px 20px 56px;text-align:center;position:relative;overflow:hidden}
#hh-page .bgx-hero::after{content:"";position:absolute;top:-120px;right:-80px;width:460px;height:460px;
background:radial-gradient(circle,rgba(0,177,245,.25),transparent 70%);pointer-events:none}
#hh-page .bgx-hero h1{color:#fff!important;font-size:clamp(2rem,4.4vw,3rem);font-weight:800;margin:0 0 14px;letter-spacing:-.01em;position:relative}
#hh-page .bgx-hero p{color:#cbd5e1!important;font-size:1.05rem;max-width:62ch;margin:0 auto;position:relative}
#hh-page .blog-section .container{max-width:1180px;margin:0 auto;padding:0 20px}
#hh-page .bgx-tools{display:flex;gap:14px;flex-wrap:wrap;align-items:center;justify-content:space-between;
margin:-28px auto 30px;max-width:1180px;background:#fff;border:1px solid #e2e8f0;border-radius:16px;
padding:16px 18px;box-shadow:0 12px 34px rgba(13,43,68,.10);position:relative;z-index:3}
#hh-page .bgx-search{flex:1 1 240px;display:flex;align-items:center;gap:8px;border:1px solid #e2e8f0;border-radius:11px;padding:10px 12px}
#hh-page .bgx-search input{border:none;outline:none;width:100%;font-size:.95rem;font-family:inherit}
#hh-page .bgx-search svg{width:18px;height:18px;color:#94a3b8;flex:0 0 18px}
#hh-page .bgx-pills{display:flex;gap:8px;flex-wrap:wrap}
#hh-page .bgx-pill{border:1px solid #e2e8f0;background:#fff;border-radius:999px;padding:8px 14px;font-size:.82rem;
font-weight:600;color:#334155;cursor:pointer;font-family:inherit}
#hh-page .bgx-pill.on{background:#00B1F5;color:#fff;border-color:#00B1F5}
#hh-page .blog-card{text-decoration:none!important;color:inherit!important}
#hh-page .blog-card-title{text-decoration:none!important}
/* the home rule .blog-card{display:flex!important} beats inline display:none, so
   hide via a higher-specificity class instead of style.display */
#hh-page .blog-grid > .blog-card.bgx-hide{display:none!important}
#hh-page .bgx-more{display:block;margin:40px auto 0;background-color:#00B1F5;color:#fff!important;border:none;
font-weight:700;font-size:.95rem;padding:14px 30px;border-radius:12px;cursor:pointer;font-family:inherit;
box-shadow:0 10px 24px rgba(0,177,245,.28)}
#hh-page .bgx-more:hover{transform:translateY(-2px);background-color:#0096cf}
#hh-page .bgx-empty{text-align:center;color:#94a3b8;padding:40px;display:none}
/* the home ships #hh-page .blog-grid{...3 cols !important}; its responsive rule is only
   .blog-grid (lower specificity) so it never wins under #hh-page -> re-assert scoped */
@media(max-width:1024px){#hh-page .blog-grid{grid-template-columns:repeat(2,1fr)!important}}
@media(max-width:640px){#hh-page .blog-grid{grid-template-columns:1fr!important}}
@media(max-width:560px){#hh-page .bgx-hero{padding:104px 18px 44px}#hh-page .bgx-tools{flex-direction:column;align-items:stretch}}
</style>"""


def render():
    cards, pills = build()
    cards_html = "\n".join(cards)
    js = ("""<script>(function(){
var grid=document.getElementById('bgxGrid'),cards=[].slice.call(grid.querySelectorAll('.blog-card'));
var per=%d,shown=per,flt='all',q='';
function apply(){cards.forEach(function(c){c.dataset.match=((flt==='all'||c.dataset.cat===flt)&&(q===''||c.dataset.search.indexOf(q)>-1))?'1':'0';});
var matched=cards.filter(function(c){return c.dataset.match==='1';});
cards.forEach(function(c){c.classList.add('bgx-hide');});matched.slice(0,shown).forEach(function(c){c.classList.remove('bgx-hide');});
document.getElementById('bgxMore').style.display=matched.length>shown?'block':'none';
document.getElementById('bgxEmpty').style.display=matched.length===0?'block':'none';}
document.getElementById('bgxSearch').addEventListener('input',function(e){q=e.target.value.toLowerCase().trim();shown=per;apply();});
[].slice.call(document.querySelectorAll('.bgx-pill')).forEach(function(b){b.addEventListener('click',function(){
document.querySelectorAll('.bgx-pill').forEach(function(x){x.classList.remove('on');});b.classList.add('on');flt=b.dataset.f;shown=per;apply();});});
document.getElementById('bgxMore').addEventListener('click',function(){shown+=per;apply();});apply();})();</script>""" % PER_PAGE)

    return f"""<!-- wp:html -->
{T.CSS}{CSS}
<div id="hh-page" class="hha-tpl">
{T.HOME_HEADER}
{T.HOME_MOBILEMENU}
<header class="bgx-hero"><h1>Ressources &amp; actualités ERP</h1>
<p>Guides, comparatifs et conseils pour piloter votre entreprise agroalimentaire avec un ERP métier.</p></header>
<section class="blog-section"><div class="container">
  <div class="bgx-tools">
    <div class="bgx-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input id="bgxSearch" type="search" placeholder="Rechercher un article, un thème…"></div>
    <div class="bgx-pills">{pills}</div>
  </div>
  <div class="blog-grid" id="bgxGrid">
{cards_html}
  </div>
  <p class="bgx-empty" id="bgxEmpty">Aucun article ne correspond à votre recherche.</p>
  <button class="bgx-more" id="bgxMore">Charger plus d'articles</button>
</div></section>
{T.HOME_FOOTER}
</div>
<script>{T.NAV_JS}</script>
{js}
<!-- /wp:html -->"""


def main():
    live = "--live" in sys.argv
    out = render()
    if live:
        full = wp.api(f"pages/{BLOG_PAGE_ID}?context=edit&_fields=id,slug,content")
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        bdir = os.path.join(HERE, f"backup-tpl-{ts}")
        os.makedirs(bdir, exist_ok=True)
        json.dump(full, open(os.path.join(bdir, f"page_{BLOG_PAGE_ID}_blog.before.json"), "w"), ensure_ascii=False)
        wp.update_content("pages", BLOG_PAGE_ID, out, live=True)
        print(f"WROTE /blog/ (page {BLOG_PAGE_ID}); backup backup-tpl-{ts}/")
    else:
        os.makedirs(os.path.join(HERE, "preview-tpl"), exist_ok=True)
        open(os.path.join(HERE, "preview-tpl", "blog.html"), "w").write(out)
        print("dry-run -> preview-tpl/blog.html (len %d)" % len(out))


if __name__ == "__main__":
    main()
