#!/usr/bin/env python3
"""
Uniform Tailwind article template for helloharel.com — same look on 100% of posts.

Reproduces the reference design (dark hero + author bio, 2 columns with the
article on the left and a sticky TOC + demo CTA on the right, reading progress
bar, "Mode Lecture Rapide", share buttons, toast) and injects the EXISTING
article content into the prose body.

Conflict-free by construction:
  - REPLACES content.raw entirely (no merge with old per-article CSS/JS).
  - The theme header/footer are hidden (nuclear reset) so only this template shows.
  - Tailwind Play CDN (+ typography plugin) styles the page; the article keeps the
    `prose` class for uniform typography. `min-w-0` + scrollable tables + bounded
    images => no horizontal overflow.
  - Existing content is read from <main class="article-content"> (original posts)
    OR <main class="hha-content"> (already-templated posts); HH-CRO leftovers are
    stripped. So it is safe to re-run.

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
STRIP_HHCRO = re.compile(r"\s*<!-- HH-CRO:START -->.*?<!-- HH-CRO:END -->", re.S)
MONTHS = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
          "août", "septembre", "octobre", "novembre", "décembre"]

CLUSTER_LABEL = {
    "stock": "Gestion de stock", "couts": "Coût de revient", "tracabilite": "Traçabilité & qualité",
    "fabrication": "Production", "facturation": "Facturation", "traiteur": "ERP traiteur",
    "viande": "ERP viande", "maraicher": "Fruits & légumes", "boulanger": "ERP boulangerie",
    "negoce": "Négoce & distribution", "erp_techno": "ERP agroalimentaire",
    "comparatifs": "Comparatif ERP", "integrateur": "Intégration ERP",
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
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def extract(raw):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = txt(m.group(1)) if m else ""

    block = ""
    am = re.search(r'<div class="article-author">(.*?)</div>\s*</div>', raw, re.S)
    if am:
        block = am.group(1)
        name = re.search(r'article-author-name">(.*?)<', block)
        role = re.search(r'article-author-role">(.*?)<', block)
    else:
        am = re.search(r'<div class="hha-author">(.*?)</div>\s*</div>', raw, re.S)
        block = am.group(1) if am else ""
        name = re.search(r'class="n">(.*?)<', block)
        role = re.search(r'class="r">(.*?)<', block)
    mv = re.search(r'<img[^>]+src="([^"]+)"', block) if block else None
    name = txt(name.group(1)) if name else "Hello Harel"
    role = txt(role.group(1)) if role else "Expert ERP agroalimentaire"
    avatar = mv.group(1) if mv else ""
    if avatar and ("d=mp" in avatar or "d=blank" in avatar):
        avatar = ""  # default gravatar -> use initials instead

    mo = MAIN_OPEN.search(raw)
    if not mo:
        return None
    body = raw[mo.end():]
    end = re.search(r"</main>|<footer", body, re.I)
    body = (body[:end.start()] if end else body)
    body = STRIP_HHCRO.sub("", body).strip()

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
    return {"title": title, "name": name, "role": role, "avatar": avatar, "body": body, "toc": toc}


HEAD = """<script src="https://cdn.tailwindcss.com?plugins=typography"></script>
<script>
tailwind.config={theme:{extend:{colors:{
crowBlackBlue:'#0D2B44',mykonosBlue:'#02587F',mykonosLight:'#EBF5FA',harelLight:'#F8FAFC',harelGray:'#64748B'},
fontFamily:{sans:['Inter','sans-serif']}}}};
</script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://unpkg.com/lucide@latest"></script>
<style>
.elementor-location-header,.elementor-location-footer,[data-elementor-type="header"],
[data-elementor-type="footer"],body>header,#masthead,#site-header,#colophon,.site-header,
.site-footer,.ast-above-header-wrap,.ast-below-header-wrap,header#header,.main-navigation{display:none!important}
.hha-tpl{font-family:'Inter',sans-serif;background:#F8FAFC}
.hha-tpl .prose{max-width:none}
.hha-tpl .prose img{max-width:100%!important;height:auto;border-radius:.75rem}
.hha-tpl .prose figure{overflow-x:auto}
.hha-tpl .prose table{display:block;overflow-x:auto;white-space:normal}
.hha-tpl #article-content{overflow-wrap:anywhere}
.skimming-active #article-content p{color:#94a3b8;transition:color .3s}
.skimming-active #article-content strong{background:rgba(2,88,127,.15);color:#02587F;font-weight:600;padding:0 4px;border-radius:4px}
</style>"""


def render(slug, data, date_iso):
    title = html.escape(data["title"])
    primary, _ = C.cluster_of(slug)
    tag = html.escape(CLUSTER_LABEL.get(primary, "ERP agroalimentaire"))
    bc_short = html.escape((data["title"][:42] + "…") if len(data["title"]) > 43 else data["title"])
    explorer, _ev, _cv, decision = cta_targets_for(slug)
    date_fr = fr_date(date_iso)

    if data["avatar"]:
        avatar_html = (f'<div class="relative w-full h-full rounded-full overflow-hidden border-2 border-white">'
                       f'<img src="{data["avatar"]}" alt="{html.escape(data["name"])}" class="w-full h-full object-cover"></div>')
    else:
        avatar_html = (f'<div class="relative w-full h-full rounded-full bg-slate-800 flex items-center '
                       f'justify-center text-white font-bold border-2 border-white text-lg">{initials(data["name"])}</div>')

    toc_links = "\n".join(
        f'<a href="#{hid}" class="toc-link block px-3 py-2.5 text-sm rounded-lg text-slate-600 '
        f'hover:bg-slate-50 hover:text-crowBlackBlue font-medium border-l-2 border-transparent transition-all">'
        f'{html.escape(t)}</a>' for hid, t in data["toc"]) or \
        '<p class="text-sm text-slate-400 px-3">—</p>'

    aux = ""
    lat = [l for l in PLAN.get(f"/blog/{slug}/", {}).get("new_links", []) if l["type"] == "lateral"][:3]
    if lat:
        items = "".join(
            f'<a href="{l["target"]}" class="block px-3 py-2 text-sm rounded-lg text-mykonosBlue '
            f'hover:bg-mykonosLight font-medium transition-colors">{html.escape(l["anchor"])}</a>' for l in lat)
        aux = (f'<div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">'
               f'<h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center">'
               f'<i data-lucide="book-open" class="w-4 h-4 mr-2 text-mykonosBlue"></i> À lire aussi</h3>'
               f'<nav class="space-y-1">{items}</nav></div>')

    inner = f"""{HEAD}
<div class="hha-tpl text-slate-800 antialiased">
<div id="progress-bar" class="fixed top-0 left-0 h-1.5 bg-gradient-to-r from-mykonosBlue to-sky-400 z-50 transition-all duration-100" style="width:0%"></div>

<section class="relative bg-gradient-to-b from-crowBlackBlue via-crowBlackBlue to-slate-900 text-white pt-16 pb-28 overflow-hidden border-b border-slate-800">
  <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-mykonosBlue/15 via-transparent to-transparent"></div>
  <div class="absolute -bottom-48 left-1/3 w-96 h-96 bg-mykonosBlue/10 rounded-full blur-3xl"></div>
  <div class="max-w-4xl mx-auto px-4 relative z-10 text-center">
    <nav class="flex justify-center items-center space-x-2 text-xs text-slate-400 mb-6 font-medium">
      <a href="/" class="hover:text-white transition-colors">Accueil</a><span class="text-slate-600">/</span>
      <a href="/blog/" class="hover:text-white transition-colors">Blog</a><span class="text-slate-600">/</span>
      <span class="text-slate-300">{bc_short}</span>
    </nav>
    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-slate-800/80 text-mykonosBlue border border-slate-700/60 mb-6 uppercase tracking-wider">
      <i data-lucide="layers" class="w-3.5 h-3.5 mr-1.5 text-sky-400"></i> {tag}</span>
    <h1 class="text-3xl md:text-5xl lg:text-6xl font-black tracking-tight leading-tight mb-8">{title}</h1>
    <div class="flex flex-col sm:flex-row items-center sm:items-start gap-4 mt-8 p-5 bg-white/5 rounded-2xl border border-white/10 max-w-xl mx-auto text-left backdrop-blur-sm">
      <div class="relative w-14 h-14 flex-shrink-0">
        <div class="absolute inset-0 bg-gradient-to-tr from-mykonosBlue to-sky-400 rounded-full animate-pulse opacity-50"></div>
        {avatar_html}
      </div>
      <div>
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-sm font-bold text-white">{html.escape(data['name'])}</span>
          <span class="text-slate-400 text-xs">•</span>
          <span class="text-xs text-slate-300">Publié le {date_fr}</span></div>
        <p class="text-xs text-sky-300 font-medium">{html.escape(data['role'])}</p>
      </div>
    </div>
  </div>
</section>

<div class="max-w-7xl mx-auto px-4 -mt-10 pb-24 relative z-20">
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
    <main class="lg:col-span-8 min-w-0 bg-white p-6 md:p-10 rounded-2xl border border-slate-200 shadow-sm">
      <div class="flex items-center justify-between bg-slate-50 border border-slate-200 rounded-xl p-4 mb-8">
        <div class="flex items-center space-x-3">
          <span class="p-2 bg-mykonosLight rounded-lg text-mykonosBlue"><i data-lucide="zap" class="w-5 h-5"></i></span>
          <div><h4 class="text-sm font-bold text-slate-800">Mode Lecture Rapide</h4>
          <p class="text-xs text-slate-500">Surlignez l'essentiel pour un survol efficace</p></div>
        </div>
        <button id="btn-skimming" class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-slate-200 transition-colors duration-200 focus:outline-none" role="switch" aria-checked="false">
          <span aria-hidden="true" class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow transition duration-200 translate-x-0" id="skimming-toggle"></span>
        </button>
      </div>
      <article class="prose prose-slate lg:prose-lg max-w-none" id="article-content">
{data['body']}
      </article>
      <div class="mt-12 flex flex-wrap items-center justify-between gap-4 py-4 px-6 bg-slate-50 border border-slate-100 rounded-xl">
        <span class="text-sm font-semibold text-slate-600">Partager cet article :</span>
        <div class="flex items-center space-x-3">
          <button id="btn-copy-link" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors">
            <i data-lucide="link" class="w-3.5 h-3.5"></i><span>Copier le lien</span></button>
          <a href="https://twitter.com/intent/tweet" target="_blank" rel="noopener" class="p-2 rounded-lg bg-sky-500 text-white hover:bg-sky-600 transition-colors"><i data-lucide="twitter" class="w-3.5 h-3.5"></i></a>
          <a href="https://www.linkedin.com/sharing/share-offsite/" target="_blank" rel="noopener" class="p-2 rounded-lg bg-blue-700 text-white hover:bg-blue-800 transition-colors"><i data-lucide="linkedin" class="w-3.5 h-3.5"></i></a>
        </div>
      </div>
    </main>
    <aside class="col-span-1 lg:col-span-4 space-y-6 lg:sticky lg:top-8 self-start">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center">
          <i data-lucide="list-ordered" class="w-4 h-4 mr-2 text-mykonosBlue"></i> Sommaire de l'article</h3>
        <nav class="space-y-1" id="toc-container">{toc_links}</nav>
      </div>
      <div class="relative bg-gradient-to-br from-crowBlackBlue to-slate-900 text-white p-6 rounded-2xl border border-slate-800 shadow-lg overflow-hidden">
        <div class="absolute -top-16 -right-16 w-32 h-32 bg-mykonosBlue/20 rounded-full blur-2xl"></div>
        <div class="relative z-10 space-y-4">
          <div class="w-12 h-12 rounded-xl bg-mykonosBlue/15 flex items-center justify-center text-sky-400"><i data-lucide="sparkles" class="w-6 h-6"></i></div>
          <h3 class="font-extrabold text-xl leading-snug">Révolutionnez votre gestion agroalimentaire</h3>
          <p class="text-xs text-slate-300 leading-relaxed">Traçabilité, coûts de revient, production et commandes : tout dans un ERP cloud spécialisé.</p>
          <a href="{decision}" class="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-gradient-to-r from-mykonosBlue to-sky-600 text-white font-bold text-sm hover:from-sky-600 hover:to-mykonosBlue active:scale-95 transition-all shadow-lg shadow-mykonosBlue/20">
            <span>Demander une démo</span><i data-lucide="arrow-right" class="w-4 h-4"></i></a>
          <a href="{explorer}" class="block text-center text-xs text-sky-300 hover:text-white transition-colors">Découvrir la solution →</a>
          <p class="text-[10px] text-center text-slate-400">Présentation personnalisée en visioconférence sous 48h.</p>
        </div>
      </div>
      {aux}
    </aside>
  </div>
</div>

<div id="toast" class="fixed bottom-6 right-6 px-4 py-3 bg-slate-900 text-white text-sm rounded-xl shadow-xl flex items-center space-x-2.5 transform translate-y-24 opacity-0 transition-all duration-300 z-50">
  <span class="p-1 bg-sky-500/20 text-sky-400 rounded-lg"><i data-lucide="check" class="w-4 h-4"></i></span>
  <span id="toast-message">Lien copié !</span></div>

<script>
(function(){{
if(window.lucide)lucide.createIcons();
var bar=document.getElementById('progress-bar');
var sections=document.querySelectorAll('#article-content section, #article-content h2');
var tocLinks=document.querySelectorAll('.toc-link');
function onScroll(){{
  var st=document.documentElement.scrollTop||document.body.scrollTop;
  var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;
  bar.style.width=(h>0?(st/h*100):0)+'%';
  var idx=-1;
  for(var i=0;i<sections.length;i++){{if(window.scrollY+140>=sections[i].offsetTop)idx=i;}}
  tocLinks.forEach(function(l){{l.classList.remove('border-mykonosBlue','text-crowBlackBlue','bg-slate-50');}});
  if(idx>=0&&tocLinks[idx])tocLinks[idx].classList.add('border-mykonosBlue','text-crowBlackBlue','bg-slate-50');
}}
window.addEventListener('scroll',onScroll);onScroll();
var sb=document.getElementById('btn-skimming'),stg=document.getElementById('skimming-toggle');
sb.addEventListener('click',function(){{
  var a=document.body.classList.toggle('skimming-active');sb.setAttribute('aria-checked',a);
  if(a){{stg.classList.add('translate-x-5');stg.classList.remove('translate-x-0');sb.classList.add('bg-mykonosBlue');sb.classList.remove('bg-slate-200');showToast('Mode Lecture Rapide activé');}}
  else{{stg.classList.remove('translate-x-5');stg.classList.add('translate-x-0');sb.classList.remove('bg-mykonosBlue');sb.classList.add('bg-slate-200');showToast('Mode Lecture Rapide désactivé');}}
}});
document.querySelectorAll('.faq-btn').forEach(function(btn){{btn.addEventListener('click',function(){{
  var c=btn.nextElementSibling,ch=btn.querySelector('svg');
  if(c.style.maxHeight){{c.style.maxHeight=null;if(ch)ch.classList.remove('rotate-180');}}
  else{{c.style.maxHeight=c.scrollHeight+'px';if(ch)ch.classList.add('rotate-180');}}
}});}});
var toast=document.getElementById('toast'),tm=document.getElementById('toast-message');
function showToast(m){{tm.innerText=m;toast.classList.remove('translate-y-24','opacity-0');toast.classList.add('translate-y-0','opacity-100');
  setTimeout(function(){{toast.classList.add('translate-y-24','opacity-0');toast.classList.remove('translate-y-0','opacity-100');}},3000);}}
var cp=document.getElementById('btn-copy-link');
if(cp)cp.addEventListener('click',function(){{(navigator.clipboard?navigator.clipboard.writeText(location.href):Promise.reject()).then(function(){{showToast('Lien copié !');}},function(){{showToast('Lien copié !');}});}});
}})();
</script>
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
        if not data or not data["body"] or not data["title"] or len(data["body"]) < 200:
            print(f"  SKIP {slug}: extraction failed")
            log.append({"slug": slug, "status": "skip"})
            continue
        new_raw = render(slug, data, full.get("date", ""))
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
