#!/usr/bin/env python3
"""
Assemble CRO previews + the per-article CRO plan (DRY-RUN, no WP writes).

For each blog article we know (from inventory.json) its title and H2 outline.
This builds:
  - maillage-cro/preview/<slug>.html : a standalone, browser-openable preview
    showing the top-of-article interactive tool, an inter-H2 visual for each H2,
    and the multi-level CTA ladder — styled exactly as it will render live.
  - maillage-cro/CRO-PLAN.md : mapping of every blog slug -> tool id, #visuals,
    CTA targets, so the plan can be reviewed before applying to production.

Usage:
  python3 cro_article.py                 # full plan + previews for SAMPLES
  python3 cro_article.py <slug> [<slug>] # also build previews for these slugs
"""

import os
import sys
import json

import cro_tools as T
import clusters as C

HERE = os.path.dirname(__file__)
INV = os.path.join(HERE, "inventory.json")
PREVIEW_DIR = os.path.join(HERE, "preview")

SAMPLES = ["roi-erp", "calcul-stock-de-securite", "cout-de-revient", "fifo-fefo-lifo",
           "conformite-haccp"]


def cta_targets_for(slug):
    """Pick CTA-ladder destinations using the article's cluster (reasonable surfer)."""
    primary, _ = C.cluster_of(slug)
    evaluator = "/comparatifs/"
    explorer = "/blog/"
    if primary and C.CLUSTERS[primary]["up"]:
        explorer = C.CLUSTERS[primary]["up"][0]  # the daughter hub of the cluster
    return explorer, evaluator, "/tarifs/", "/contact/"


def build_preview(item):
    slug = C.slug_of(item["path"])
    title = item.get("title") or slug
    h2s = item.get("h2") or ["Section"]
    tool = T.interactive_tool(slug, title)
    ladder = T.cta_ladder(*cta_targets_for(slug))
    h2_blocks = "\n".join(
        f'<h2 style="font-family:Inter;max-width:680px;margin:2rem auto 0;color:#0f172a">{h}</h2>'
        f'<p style="font-family:Inter;max-width:680px;margin:.5rem auto;color:#475569">'
        f'[…contenu éditorial de la section…]</p>\n{T.inter_h2_visual(i, h)}'
        for i, h in enumerate(h2s)
    )
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Preview CRO — {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>body{{background:#eef3f8;margin:0;padding:2rem 1rem}}h1{{font-family:Inter;max-width:680px;margin:0 auto 1rem;color:#0f172a}}
.note{{font-family:Inter;max-width:680px;margin:0 auto 1.5rem;color:#64748b;font-size:.85rem;background:#fff;border-radius:10px;padding:.75rem 1rem}}</style>
</head><body>
<h1>{title}</h1>
<div class="note">Preview DRY-RUN — outil interactif (haut d'article), visuel inter-H2, échelle de CTA. Aucune écriture WordPress.</div>
{tool}
{h2_blocks}
{ladder}
</body></html>"""


def main():
    data = json.load(open(INV))
    by_path = {x["path"]: x for x in data["items"]}
    posts = [x for x in data["items"] if x["kind"] == "post" and x["path"].startswith("/blog/")]

    os.makedirs(PREVIEW_DIR, exist_ok=True)

    # CRO plan for ALL blog articles
    lines = ["# Template CRO article — Plan DRY-RUN", "",
             "Chaque article (page petite-fille L3) reçoit : un **outil interactif** en haut "
             "(selon la micro-intention), un **visuel HTML/CSS inter-H2** entre chaque section, "
             "et une **échelle de CTA** multi-niveaux.", "",
             "| Article | Outil interactif | Visuels inter-H2 | Échelle CTA (explore→prêt) |",
             "|---|---|---|---|"]
    tool_counts = {}
    for x in sorted(posts, key=lambda z: z["path"]):
        slug = C.slug_of(x["path"])
        tid = T.tool_for(slug)
        tool_counts[tid] = tool_counts.get(tid, 0) + 1
        nvis = len(x.get("h2") or [])
        ex, ev, cv, dc = cta_targets_for(slug)
        lines.append(f"| {x['path']} | `{tid}` | {nvis} | {ex} → {ev} → {cv} → {dc} |")
    lines += ["", "## Répartition des outils", ""]
    for tid, n in sorted(tool_counts.items(), key=lambda z: -z[1]):
        lines.append(f"- `{tid}` : {n} articles")
    open(os.path.join(HERE, "CRO-PLAN.md"), "w").write("\n".join(lines))

    # Previews
    targets = SAMPLES + sys.argv[1:]
    built = []
    for slug in dict.fromkeys(targets):
        item = by_path.get(f"/blog/{slug}/")
        if not item:
            print(f"  skip (unknown slug): {slug}")
            continue
        html = build_preview(item)
        out = os.path.join(PREVIEW_DIR, f"{slug}.html")
        open(out, "w").write(html)
        built.append(out)
    print(f"CRO-PLAN.md written for {len(posts)} articles.")
    print("Previews built:")
    for b in built:
        print("  -", b)


if __name__ == "__main__":
    main()
