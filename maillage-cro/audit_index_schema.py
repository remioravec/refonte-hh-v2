#!/usr/bin/env python3
"""
Site-wide indexation + structured-data (Schema.org) crawl for helloharel.com.

For every URL (union of the XML sitemaps and the known inventory), capture:
  - HTTP status + final URL (redirect target)
  - <link rel=canonical>  (self-referencing or cross?)
  - <meta name=robots>    (index/noindex, follow/nofollow)
  - all JSON-LD @type values (server-rendered by Rank Math)
  - whether the URL is present in the XML sitemap (indexation coverage)

Public HTTP only (no auth, no JS) — Rank Math emits JSON-LD server-side.
Output -> audit-indexation.json
"""
import json, re, ssl, time, urllib.request, urllib.error, gzip, io

SITE = "https://www.helloharel.com"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; HelloHarel-SEO-Audit/1.0)"


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
        return r.status, r.geturl(), raw.decode("utf-8", "replace")


def sitemap_urls():
    urls = set()
    idx_status, _, idx = fetch(f"{SITE}/sitemap_index.xml")
    for sm in re.findall(r"<loc>([^<]+)</loc>", idx):
        try:
            _, _, body = fetch(sm)
            for loc in re.findall(r"<loc>([^<]+)</loc>", body):
                urls.add(loc.strip())
        except Exception as e:
            print("sitemap fetch fail", sm, e)
    return urls


def path_of(url):
    p = re.sub(r"^https?://[^/]+", "", url)
    return p or "/"


def ld_types(htmlstr):
    types = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', htmlstr, re.S | re.I):
        block = m.group(1)
        types += re.findall(r'"@type"\s*:\s*"([^"]+)"', block)
        # arrays of types: "@type":["A","B"]
        for arr in re.findall(r'"@type"\s*:\s*\[([^\]]+)\]', block):
            types += re.findall(r'"([^"]+)"', arr)
    return types


def main():
    sm = sitemap_urls()
    sm_paths = {path_of(u) for u in sm}
    print(f"sitemap URLs: {len(sm)}")

    inv = json.load(open("inventory.json"))
    inv_paths = {it["path"] for it in inv["items"]}
    kind_of = {it["path"]: it["kind"] for it in inv["items"]}

    all_paths = sorted(sm_paths | inv_paths)
    print(f"crawling {len(all_paths)} unique paths")

    out = {}
    for i, p in enumerate(all_paths, 1):
        url = SITE + p
        rec = {"kind": kind_of.get(p, "page"), "in_sitemap": p in sm_paths,
               "in_inventory": p in inv_paths}
        try:
            st, final, body = fetch(url)
            rec["status"] = st
            rec["redirected"] = (path_of(final) != p)
            rec["final"] = path_of(final)
            c = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', body, re.I)
            rec["canonical"] = c.group(1) if c else None
            rec["canonical_self"] = bool(c and path_of(c.group(1)) == p)
            rb = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)', body, re.I)
            rec["robots"] = rb.group(1) if rb else None
            rec["noindex"] = bool(rb and "noindex" in rb.group(1).lower())
            t = ld_types(body)
            rec["schema_types"] = sorted(set(t))
            rec["schema_count"] = len(t)
        except urllib.error.HTTPError as e:
            rec["status"] = e.code; rec["error"] = "http"
        except Exception as e:
            rec["status"] = 0; rec["error"] = str(e)[:80]
        out[p] = rec
        if i % 20 == 0:
            print(f"  {i}/{len(all_paths)}")
        time.sleep(0.25)

    json.dump({"site": SITE, "sitemap_count": len(sm), "crawled": len(out),
               "sitemap_paths": sorted(sm_paths), "pages": out},
              open("audit-indexation.json", "w"), ensure_ascii=False, indent=1)
    print("WROTE audit-indexation.json")


if __name__ == "__main__":
    main()
