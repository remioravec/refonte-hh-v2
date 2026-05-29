#!/usr/bin/env python3
"""
Build a compact, ground-truth inventory of helloharel.com (read-only).

Outputs:
  - /tmp/wp_cache/<kind>_<id>.html   raw content cache (NOT committed)
  - maillage-cro/inventory.json      compact structure (committed, no secrets)

Per item we record: id, kind, slug, url, title, word count, list of H2 texts,
and every internal <a> (target path + anchor text). This is the substrate the
maillage engine and the CRO enhancer both read.
"""

import os
import re
import json
import html
import time

import wp_common as wp

CACHE = "/tmp/wp_cache"
OUT = os.path.join(os.path.dirname(__file__), "inventory.json")

TAG_RE = re.compile(r"<[^>]+>")
H2_RE = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.I | re.S)
A_RE = re.compile(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)
P_RE = re.compile(r"<p\b[^>]*>(.*?)</p>", re.I | re.S)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ0-9]+")


def strip_code(raw):
    """Remove inline <script>/<style> blocks so they don't pollute analysis."""
    return SCRIPT_STYLE_RE.sub(" ", raw)


def strip_tags(s):
    return html.unescape(TAG_RE.sub(" ", s)).strip()


def normalize_path(href):
    """Return an internal site path or None for external/anchor/mailto links."""
    href = href.strip()
    if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
        return None
    for prefix in ("https://www.helloharel.com", "https://helloharel.com",
                   "http://www.helloharel.com", "http://helloharel.com"):
        if href.startswith(prefix):
            href = href[len(prefix):] or "/"
            break
    else:
        if href.startswith("http"):
            return None  # external
    if not href.startswith("/"):
        return None
    href = href.split("#")[0].split("?")[0]
    if not href.endswith("/") and "." not in href.rsplit("/", 1)[-1]:
        href += "/"
    return href


def analyze(raw):
    clean = strip_code(raw)  # drop inline CSS/JS
    words = len(WORD_RE.findall(strip_tags(clean)))
    h2s = [strip_tags(m) for m in H2_RE.findall(clean)]

    # Contextual links = those living inside editorial <p> paragraphs.
    contextual_pairs = set()
    for para in P_RE.findall(clean):
        for href, inner in A_RE.findall(para):
            p = normalize_path(href)
            if p:
                contextual_pairs.add((p, strip_tags(inner)))

    links = []
    for href, inner in A_RE.findall(clean):
        path = normalize_path(href)
        if path is None:
            continue
        anchor = strip_tags(inner)
        links.append({
            "path": path,
            "anchor": anchor,
            "ctx": (path, anchor) in contextual_pairs,  # editorial vs boilerplate
        })
    return words, h2s, links


def main():
    os.makedirs(CACHE, exist_ok=True)
    inventory = []
    for kind in ("pages", "posts"):
        items = wp.get_all(kind, fields="id,slug,link,title")
        print(f"{kind}: {len(items)} items")
        for it in items:
            full = wp.get_raw(kind, it["id"])
            raw = (full.get("content") or {}).get("raw", "") or ""
            with open(os.path.join(CACHE, f"{kind}_{it['id']}.html"), "w") as f:
                f.write(raw)
            words, h2s, links = analyze(raw)
            path = normalize_path(it.get("link", "")) or "/" + it["slug"] + "/"
            inventory.append({
                "id": it["id"],
                "kind": kind[:-1],  # page / post
                "slug": it["slug"],
                "path": path,
                "title": strip_tags((it.get("title") or {}).get("rendered", "")),
                "words": words,
                "h2": h2s,
                "internal_links": links,
                "raw_len": len(raw),
            })
            time.sleep(0.15)

    # Build inbound link graph + anchor map per target
    by_path = {x["path"]: x for x in inventory}
    inbound = {x["path"]: [] for x in inventory}
    for x in inventory:
        for lk in x["internal_links"]:
            if lk["path"] in inbound:
                inbound[lk["path"]].append(
                    {"from": x["path"], "anchor": lk["anchor"], "ctx": lk["ctx"]})
    for x in inventory:
        links = inbound.get(x["path"], [])
        ctx = [l for l in links if l["ctx"]]
        x["inbound_count"] = len(links)
        x["inbound_ctx_count"] = len(ctx)
        x["inbound_ctx_anchors"] = sorted({l["anchor"] for l in ctx if l["anchor"]})

    with open(OUT, "w") as f:
        json.dump({"site": wp.SITE, "count": len(inventory), "items": inventory},
                  f, ensure_ascii=False, indent=1)
    print(f"\nWrote {OUT} ({len(inventory)} items)")
    orphans = [x for x in inventory if x["kind"] == "post" and x["inbound_ctx_count"] == 0]
    print(f"Posts with 0 CONTEXTUAL inbound links (real orphans): {len(orphans)}")


if __name__ == "__main__":
    main()
