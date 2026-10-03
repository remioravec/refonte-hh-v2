#!/usr/bin/env python3
"""
Site-wide CODE audit — fetch every published page & post and run static checks
for the classes of "small bugs on many pages":

  JS-REF     document.getElementById('X')./querySelector('#X'). where #X is
             absent in the HTML  -> runtime TypeError that can halt scripts
  DUP-ID     the same id="..." used more than once  -> JS/CSS/anchor breakage
  MIXED      http:// sub-resource on an https page   -> mixed-content/blocked
  IMG-NOSRC  <img> with empty/missing src
  IMG-ALT    <img> without alt (a11y)
  TAG-BAL    <section>/<div> open vs close mismatch  -> layout/structure bug
  MULTI-H1   more than one <h1>                       -> SEO/structure
  BAD-LINK   href="#" / href="" / javascript:void     -> dead controls
  DBL-SLASH  href/src with accidental // in path

Read-only. Outputs a per-URL issue list + aggregate summary.
"""
import re, json, subprocess, concurrent.futures as cf
import wp_common as w

def all_urls():
    urls = []
    for kind in ("pages", "posts"):
        for it in w.get_all(kind, fields="id,link,slug"):
            urls.append((kind, it["id"], it["link"]))
    return urls

def fetch(url):
    try:
        return subprocess.run(["curl", "-s", "-m", "30", url], capture_output=True, text=True, timeout=35).stdout
    except Exception:
        return ""

# --- individual checks -------------------------------------------------------
def check(html):
    issues = []
    ids = re.findall(r'\sid="([^"]+)"', html)
    idset = set(ids)

    # JS-REF: getElementById('X'). / querySelector('#X').  with immediate use
    for m in re.finditer(r"getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\.", html):
        if m.group(1) not in idset:
            issues.append(("JS-REF", f"getElementById('{m.group(1)}') used but #id absent"))
    for m in re.finditer(r"querySelector\(\s*['\"]#([A-Za-z][\w-]*)['\"]\s*\)\s*\.", html):
        if m.group(1) not in idset:
            issues.append(("JS-REF", f"querySelector('#{m.group(1)}') used but #id absent"))

    # DUP-ID
    seen, dup = set(), set()
    for i in ids:
        (dup if i in seen else seen).add(i)
    for d in sorted(dup):
        issues.append(("DUP-ID", f'id="{d}" appears {ids.count(d)}x'))

    # MIXED content (ignore xmlns / schema / w3.org namespaces)
    for m in re.finditer(r'(?:src|href)="(http://[^"]+)"', html):
        u = m.group(1)
        if not any(s in u for s in ("w3.org", "schema.org", "purl.org", "ogp.me", "gmpg.org", "xmlns")):
            issues.append(("MIXED", u[:80]))

    # IMG issues
    for m in re.finditer(r'<img\b[^>]*>', html):
        tag = m.group(0)
        if not re.search(r'\ssrc="[^"]+"', tag):
            issues.append(("IMG-NOSRC", tag[:70]))
        if not re.search(r'\salt=', tag):
            issues.append(("IMG-ALT", tag[:70]))

    # TAG balance for section (div is too noisy across full theme)
    for tag in ("section",):
        o = len(re.findall(r'<%s\b' % tag, html)); c = len(re.findall(r'</%s>' % tag, html))
        if o != c:
            issues.append(("TAG-BAL", f"<{tag}> {o} open / {c} close"))

    # MULTI-H1
    h1 = len(re.findall(r'<h1\b', html))
    if h1 > 1:
        issues.append(("MULTI-H1", f"{h1} <h1>"))

    # BAD-LINK
    bad = len(re.findall(r'href="(#|javascript:void\(0\)?|)"', html))
    if bad:
        issues.append(("BAD-LINK", f'{bad} href="#"/empty/js-void'))

    # DBL-SLASH in path (not protocol)
    for m in re.finditer(r'(?:src|href)="https://[^"]+?[^:]//[^"]*"', html):
        issues.append(("DBL-SLASH", m.group(0)[:80]))

    return issues

def main():
    urls = all_urls()
    print("scanning", len(urls), "urls")
    results = {}
    def work(item):
        kind, pid, url = item
        return (url, check(fetch(url)))
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for url, iss in ex.map(work, urls):
            if iss:
                results[url] = iss
    # aggregate
    agg = {}
    for url, iss in results.items():
        for t, _ in iss:
            agg[t] = agg.get(t, 0) + 1
    out = {"scanned": len(urls), "pages_with_issues": len(results), "by_type": agg, "detail": {}}
    for url, iss in results.items():
        short = url.replace("https://www.helloharel.com", "")
        out["detail"][short] = [f"{t}: {m}" for t, m in iss]
    open("/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/code_audit.json", "w").write(json.dumps(out, ensure_ascii=False, indent=1))
    print("BY TYPE:", json.dumps(agg))
    print("pages with issues:", len(results), "/", len(urls))

if __name__ == "__main__":
    main()
