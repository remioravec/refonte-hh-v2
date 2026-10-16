#!/usr/bin/env python3
"""
Add BreadcrumbList JSON-LD to EVERY blog article that still lacks it (audit:
0/99 articles had a breadcrumb schema). Safe, minimal: we DON'T re-render the
page — we inject a single <script type="application/ld+json"> right after the
<div id="hh-page" class="hha-tpl"> wrapper of the existing live content.
Idempotent: skips any post already carrying a BreadcrumbList.

Run:
  python3 breadcrumb_all.py            # DRY-RUN (report only)
  python3 breadcrumb_all.py --live     # inject + update
"""
import sys, re, json, html
import wp_common as wp


def all_posts():
    out, pg = [], 1
    while True:
        try:
            b = wp.api(f"posts?per_page=50&page={pg}&status=publish&_fields=id,slug")
        except RuntimeError as e:
            if "invalid_page_number" in str(e):
                break
            raise
        if not isinstance(b, list) or not b:
            break
        out += b
        if len(b) < 50:
            break
        pg += 1
    return out


def bc_script(slug, title):
    return ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil",
             "item": "https://www.helloharel.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog",
             "item": "https://www.helloharel.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": title,
             "item": f"https://www.helloharel.com/blog/{slug}/"},
        ]}, ensure_ascii=False) + "</script>")


def main():
    live = "--live" in sys.argv
    posts = all_posts()
    print(f"published posts: {len(posts)}")
    need, skipped, done, failed = [], 0, [], []
    for p in posts:
        full = wp.get_raw("posts", p["id"])
        content = (full.get("content") or {}).get("raw", "") or ""
        if "BreadcrumbList" in content:
            skipped += 1
            continue
        title = html.unescape(re.sub(r"<[^>]+>", "", (full.get("title") or {}).get("raw", "") or p["slug"])).strip()
        script = bc_script(p["slug"], title)
        m = re.search(r'<div id="hh-page" class="hha-tpl">', content)
        if m:
            new = content[:m.end()] + "\n" + script + content[m.end():]
        else:
            new = "<!-- wp:html -->\n" + script + "\n<!-- /wp:html -->\n" + content
        need.append(p["slug"])
        if live:
            try:
                wp.api(f"posts/{p['id']}", method="POST", data={"content": new})
                done.append(p["slug"])
            except Exception as e:
                failed.append((p["slug"], str(e)[:80]))
    print(f"already had breadcrumb: {skipped}")
    print(f"needed injection: {len(need)}")
    if live:
        print(f"injected OK: {len(done)} | failed: {len(failed)}")
        for s, e in failed:
            print("   FAIL", s, e)
    else:
        for s in need:
            print("   need:", s)


if __name__ == "__main__":
    main()
