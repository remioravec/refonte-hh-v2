#!/usr/bin/env python3
"""
Apply maillage + CRO to live blog articles — IDEMPOTENT, gated by --live.

Injection happens ONLY inside <main class="article-content"> ... </main>, the
clean editorial region (verified present on 99/99 posts). The marketing hero,
header and footer are never touched.

Per article, between the markers <!-- HH-CRO:START --> / <!-- HH-CRO:END -->:
  - TOP   : interactive tool (by micro-intention) + "En bref" up-links box
  - inline: an HTML/CSS visual before each section heading <h2 id="s-...">
  - END   : "Sur le même sujet" lateral links + multi-level CTA ladder

Idempotent: existing HH-CRO blocks are stripped before re-injecting, so the
script can be re-run safely. Before any write, the pre-change object is saved to
backup-live-<ts>/ (full restore point) and structural guards are checked.

Usage:
  python3 apply.py                      # DRY-RUN, all posts -> preview-apply/
  python3 apply.py --slugs a b c        # restrict to these slugs
  python3 apply.py --live               # WRITE to production (all planned posts)
  python3 apply.py --live --slugs a b   # WRITE only these (pilot)
"""

import os
import re
import sys
import json
import time
import datetime

import wp_common as wp
import cro_tools as T
import clusters as C
from cro_article import cta_targets_for

HERE = os.path.dirname(__file__)
INV = json.load(open(os.path.join(HERE, "inventory.json")))
ITEMS = {x["path"]: x for x in INV["items"]}
PLAN = json.load(open(os.path.join(HERE, "maillage-plan.json")))["plan"]

MAIN_RE = re.compile(r'<main class="article-content"[^>]*>', re.I)
SEC_H2_RE = re.compile(r'<h2\b[^>]*\bid="s-', re.I)
STRIP_RE = re.compile(r'\s*<!-- HH-CRO:START -->.*?<!-- HH-CRO:END -->', re.S)
HHBLUE = T.BRAND


def wrap(html):
    return f"\n<!-- HH-CRO:START -->\n{html}\n<!-- HH-CRO:END -->\n"


def join_links(links):
    parts = [f'<a href="{l["target"]}">{l["anchor"]}</a>' for l in links]
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " et " + parts[-1]


def enbref_box(up_links):
    if not up_links:
        return ""
    return (f'<p class="hh-enbref" style="font-family:\'Inter\',sans-serif;max-width:680px;'
            f'margin:1rem auto;padding:.9rem 1.1rem;background:{HHBLUE}0d;border-left:4px solid '
            f'{HHBLUE};border-radius:10px;color:#334155;font-size:.95rem">'
            f'<strong style="color:#0f172a">L\'essentiel —</strong> pour aller plus vite : '
            f'{join_links(up_links)}.</p>')


def related_box(lateral_links):
    if not lateral_links:
        return ""
    lis = "".join(f'<li style="margin:.3rem 0"><a href="{l["target"]}" '
                  f'style="color:{HHBLUE};font-weight:600">{l["anchor"]}</a></li>'
                  for l in lateral_links)
    return (f'<aside class="hh-related" style="font-family:\'Inter\',sans-serif;max-width:680px;'
            f'margin:2rem auto;padding:1.1rem 1.3rem;background:#f8fbff;border:1px solid #e2e8f0;'
            f'border-radius:14px">'
            f'<p style="margin:0 0 .5rem;font-weight:800;color:#0f172a;font-size:1.05rem">Sur le même sujet</p>'
            f'<ul style="margin:0;padding-left:1.1rem">{lis}</ul></aside>')


def transform(raw, slug, title):
    """Return (new_raw, stats) or (None, reason) if guards fail."""
    raw = STRIP_RE.sub("", raw)  # idempotent: remove prior HH-CRO blocks

    m = MAIN_RE.search(raw)
    if not m:
        return None, "no <main class=article-content>"
    inner_start = m.end()
    close = re.search(r'</main>', raw[inner_start:], re.I)
    region_end = inner_start + close.start() if close else None
    if region_end is None:
        f = re.search(r'<footer', raw[inner_start:], re.I)
        if not f:
            return None, "no </main> or <footer>"
        region_end = inner_start + f.start()

    plan = PLAN.get(f"/blog/{slug}/", {})
    new_links = plan.get("new_links", [])
    up = [l for l in new_links if l["type"] == "up"]
    lat = [l for l in new_links if l["type"] == "lateral"]

    tool = T.interactive_tool(slug, title)
    ladder = T.cta_ladder(*cta_targets_for(slug))
    top_block = wrap(tool + enbref_box(up))
    end_block = wrap(related_box(lat) + ladder)

    # Section headings within the editorial region
    sec_positions = [inner_start + mm.start()
                     for mm in SEC_H2_RE.finditer(raw[inner_start:region_end])]

    # Backward insertion to keep indices valid: end -> visuals -> top
    out = raw[:region_end] + end_block + raw[region_end:]
    for i in range(len(sec_positions) - 1, -1, -1):
        pos = sec_positions[i]
        vis = wrap(T.inter_h2_visual(i, ITEMS.get(f"/blog/{slug}/", {}).get("h2", ["Section"])[i]
                                     if i < len(ITEMS.get(f"/blog/{slug}/", {}).get("h2", [])) else "Section"))
        out = out[:pos] + vis + out[pos:]
    out = out[:inner_start] + top_block + out[inner_start:]

    # Structural guards — never push a broken page
    for token, label in [(MAIN_RE, "main"), (re.compile(r'<footer', re.I), "footer"),
                         (re.compile(r'<h1', re.I), "h1")]:
        if len(token.findall(out)) != len(token.findall(raw)):
            return None, f"guard failed: {label} count changed"
    if out.count("<!-- HH-CRO:START -->") != out.count("<!-- HH-CRO:END -->"):
        return None, "guard failed: unbalanced HH-CRO markers"
    if len(out) < len(raw):
        return None, "guard failed: output shorter than input"

    return out, {"tool": T.tool_for(slug), "visuals": len(sec_positions),
                 "up": len(up), "lateral": len(lat), "delta": len(out) - len(raw)}


def strip_only(raw):
    """Remove all HH-CRO blocks; return (new_raw, removed_count) or (None, reason)."""
    new = STRIP_RE.sub("", raw)
    for token, label in [(MAIN_RE, "main"), (re.compile(r'<footer', re.I), "footer"),
                         (re.compile(r'<h1', re.I), "h1")]:
        if len(token.findall(new)) != len(token.findall(raw)):
            return None, f"guard failed: {label}"
    return new, raw.count("<!-- HH-CRO:START -->")


def main():
    live = "--live" in sys.argv
    strip = "--strip" in sys.argv
    slugs = None
    if "--slugs" in sys.argv:
        i = sys.argv.index("--slugs")
        slugs = [s for s in sys.argv[i + 1:] if not s.startswith("--")]

    posts = [x for x in INV["items"] if x["kind"] == "post" and x["path"].startswith("/blog/")]
    if slugs:
        posts = [x for x in posts if C.slug_of(x["path"]) in slugs]

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bdir = os.path.join(HERE, f"backup-live-{ts}")
    pdir = os.path.join(HERE, "preview-apply")
    os.makedirs(bdir if live else pdir, exist_ok=True)

    log = []
    mode = ("STRIP " if strip else "") + ("LIVE WRITE" if live else "DRY-RUN")
    print(f"Mode: {mode} | posts: {len(posts)}")
    for x in posts:
        slug = C.slug_of(x["path"])
        title = x.get("title") or slug
        # Always work from FRESH content at apply time
        full = wp.get_raw("posts", x["id"])
        raw = (full.get("content") or {}).get("raw", "") or ""
        if strip:
            new_raw, info = strip_only(raw)
            if new_raw is None:
                print(f"  SKIP {slug}: {info}"); log.append({"slug": slug, "status": "skip", "reason": info}); continue
            if info == 0:
                log.append({"slug": slug, "status": "noop"}); continue
            if live:
                wp.update_content("posts", x["id"], new_raw, live=True)
                print(f"  STRIPPED {slug}: -{info} blocks")
                log.append({"slug": slug, "status": "stripped", "blocks": info})
            else:
                print(f"  dry strip {slug}: -{info} blocks")
                log.append({"slug": slug, "status": "dry-strip", "blocks": info})
            continue
        new_raw, stats = transform(raw, slug, title)
        if new_raw is None:
            print(f"  SKIP {slug}: {stats}")
            log.append({"slug": slug, "status": "skip", "reason": stats})
            continue
        if live:
            # save restore point BEFORE writing
            json.dump(full, open(os.path.join(bdir, f"post_{x['id']}_{slug}.before.json"), "w"),
                      ensure_ascii=False)
            wp.update_content("posts", x["id"], new_raw, live=True)
            print(f"  WROTE {slug}: {stats}")
            log.append({"slug": slug, "status": "wrote", **stats})
        else:
            open(os.path.join(pdir, f"{slug}.html"), "w").write(new_raw)
            print(f"  dry  {slug}: {stats}")
            log.append({"slug": slug, "status": "dry", **stats})

    logname = f"apply-log-{ts}.json"
    json.dump({"mode": "live" if live else "dry", "count": len(log), "items": log},
              open(os.path.join(HERE, logname), "w"), ensure_ascii=False, indent=1)
    print(f"\nLog: maillage-cro/{logname}")
    if live:
        print(f"Restore points: maillage-cro/backup-live-{ts}/")


if __name__ == "__main__":
    main()
