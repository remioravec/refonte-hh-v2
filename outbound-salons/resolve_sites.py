#!/usr/bin/env python3
"""
Phase 2bis — Résolution nom -> site officiel (pour les salons qui ne donnent que
le nom, ex. Medfel), via une recherche web GRATUITE et scriptable
(DuckDuckGo HTML — pas d'API tierce payante). Puis harvest de l'email sur le site
trouvé (enrich_emails.harvest). Aucune invention : si pas de site fiable ou pas
d'email, champs laissés vides.

Usage:
  python3 resolve_sites.py <salon>-exposants.csv [--limit N]
"""
import sys, re, csv, ssl, time, html, urllib.request, urllib.parse, datetime
from enrich_emails import harvest  # réutilise le harvester email

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; HelloHarel-Prospection/1.0)"
TODAY = datetime.date.today().isoformat()

# domaines à NE jamais prendre comme "site officiel" (annuaires, réseaux, presse)
BLOCK = ("facebook.", "linkedin.", "instagram.", "twitter.", "x.com", "youtube.",
         "wikipedia.", "societe.com", "pappers.", "infogreffe.", "verif.com",
         "pagesjaunes.", "europages.", "kompass.", "medfel.", "salon", "francetv",
         "lefigaro", "ouest-france", "usinenouvelle", "agro-media", "tripadvisor",
         "amazon.", "leboncoin", "indeed.", "glassdoor", "bing.", "google.",
         "duckduckgo", "yelp.", "mappy.", "118", "annuaire")


def ddg(query):
    u = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    try:
        h = urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")
    except Exception:
        return []
    links = re.findall(r'class="result__a"[^>]*href="([^"]+)"', h)
    if not links:
        links = re.findall(r'href="(https?://[^"]*uddg=[^"]+)"', h)
    out = []
    for l in links[:8]:
        m = re.search(r'uddg=([^&]+)', l)
        out.append(urllib.parse.unquote(m.group(1)) if m else l)
    return out


def tokens(name):
    return [t for t in re.split(r'[^a-z0-9]+', name.lower()) if len(t) > 2]


def resolve(name):
    """Return a best-guess official site URL or ''."""
    res = ddg(f"{name} site officiel")
    toks = tokens(name)
    cand = []
    for url in res:
        dom = urllib.parse.urlparse(url).netloc.lower().replace("www.", "")
        if not dom or any(b in dom for b in BLOCK):
            continue
        cand.append((url, dom))
    if not cand:
        return ""
    # prefer a domain sharing a token with the company name
    for url, dom in cand:
        d0 = dom.split(".")[0]
        if any(t in d0 or d0 in t for t in toks):
            return url
    return cand[0][0]  # else first acceptable organic result


def main():
    if len(sys.argv) < 2:
        print("usage: resolve_sites.py <salon>-exposants.csv [--limit N]"); return
    path = sys.argv[1]
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter=";"))
    todo = [r for r in rows if not r.get("site_web") and not r.get("email")]
    if limit:
        todo = todo[:limit]
    print(f"à résoudre : {len(todo)}")
    site_hits = mail_hits = 0
    for i, r in enumerate(todo, 1):
        site = resolve(r["entreprise"])
        if site:
            r["site_web"] = site; site_hits += 1
            e, t, src = harvest(site)
            if e:
                r["email"] = e; r["type_email"] = t; r["email_site"] = e
                r["email_site_source"] = src; r["email_origine"] = "site"
                r["source_url"] = src; r["date_collecte"] = TODAY
                r["statut_validation"] = "valide"; mail_hits += 1
        time.sleep(1.0)  # politesse moteur de recherche
        if i % 10 == 0:
            print(f"  {i}/{len(todo)} — sites {site_hits} / emails {mail_hits}")
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";"); w.writeheader(); w.writerows(rows)
    print(f"\nTerminé : sites trouvés {site_hits}/{len(todo)} | emails {mail_hits}/{len(todo)} -> {path}")


if __name__ == "__main__":
    main()
