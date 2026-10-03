#!/usr/bin/env python3
"""
Phase 3 — Email harvester (générique, SANS API, SANS invention).
Pour chaque exposant ayant un site web, on visite son site, on ouvre les pages
mentions légales / contact / CGV, et on extrait le ou les emails RÉELLEMENT
présents sur la page. On préfère un email générique sur le même domaine que le
site. La page exacte où l'email a été trouvé est journalisée (email_site_source).
Si aucun email n'est trouvé : champ vide (aucune fabrication).

Entrée : un <salon>-exposants.csv (doit contenir 'entreprise' et 'site_web').
Sortie : le même fichier enrichi (colonnes email_site, email_site_source,
         email_origine ; 'email' = meilleur email retenu).

Usage:
  python3 enrich_emails.py serbotel-exposants.csv [--limit N] [--icp] [--only-empty]
"""
import sys, re, csv, ssl, time, html, urllib.request, urllib.parse, datetime

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; HelloHarel-Prospection/1.0; +contact)"
TODAY = datetime.date.today().isoformat()

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
GENERIC = ("contact", "info", "infos", "commercial", "accueil", "hello", "bonjour",
           "direction", "rh", "compta", "comptabilite", "sav", "service", "vente",
           "ventes", "communication", "marketing", "administration", "secretariat",
           "commande", "commandes", "client", "clients")
# domaines / extensions à exclure (faux positifs, trackers, assets)
BAD_DOM = ("wixpress.com", "sentry.io", "example.com", "example.org", "domain.com",
           "email.com", "your-domain", "wix.com", "squarespace.com", "godaddy.com",
           "schema.org", "w3.org", "googleapis.com", "gstatic.com", "cloudflare",
           "jsdelivr.net", "sentry-next", "wordpress.org", "gravatar.com", "/")
BAD_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".css", ".js", ".json", ".xml", ".bmp")
HINT = re.compile(r"mention|legal|l[ée]gal|cgv|cgu|contact|nous-?contacter|qui-?sommes|"
                  r"a-?propos|about|impressum|coordonn", re.I)
GUESS = ["/mentions-legales/", "/mentions-legales", "/contact/", "/contact",
         "/nous-contacter/", "/cgv/", "/qui-sommes-nous/", "/mentions-legales.html",
         "/contact.html", "/legal/", "/mentions/"]


def norm_url(u):
    u = (u or "").strip()
    if not u:
        return ""
    if not u.startswith("http"):
        u = "https://" + u
    return u


def host(u):
    try:
        return urllib.parse.urlparse(u).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def fetch(url, timeout=22):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr"})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                ct = r.headers.get("Content-Type", "")
                if "html" not in ct and "text" not in ct and ct:
                    return "", r.geturl()
                raw = r.read(900000)
                enc = "utf-8"
                m = re.search(r'charset=["\']?([\w\-]+)', ct)
                if m:
                    enc = m.group(1)
                return raw.decode(enc, "replace"), r.geturl()
        except Exception:
            if attempt == 0:
                time.sleep(1.5)
                continue
            return "", url


def extract_emails(page):
    found = set()
    # mailto (souvent entity-encodé)
    for m in re.finditer(r'href=["\']?((?:&#\d+;)+|mailto:[^"\'>\s]+)', page):
        raw = html.unescape(m.group(1)).replace("mailto:", "")
        raw = urllib.parse.unquote(raw).split("?")[0]
        for e in EMAIL_RE.findall(raw):
            found.add(e.lower())
    # texte brut (après unescape des entités)
    txt = html.unescape(page)
    for e in EMAIL_RE.findall(txt):
        found.add(e.lower())
    # nettoyage
    out = []
    for e in found:
        dom = e.split("@")[1]
        if any(b in dom for b in BAD_DOM):
            continue
        if any(e.endswith(ext) for ext in BAD_EXT):
            continue
        if len(e) > 80 or e.count("@") != 1:
            continue
        out.append(e)
    return out


def is_generic(e):
    loc = e.split("@")[0]
    return any(loc == g or loc.startswith(g + ".") or loc.startswith(g) for g in GENERIC)


def pick_best(emails, site_host):
    """Prefer same-domain + generic. Return (email, 'generique'|'nominatif')."""
    if not emails:
        return "", ""
    same = [e for e in emails if site_host and site_host in e.split("@")[1]]
    pool = same or emails
    gen = [e for e in pool if is_generic(e)]
    if gen:
        return sorted(gen, key=len)[0], "generique"
    return sorted(pool, key=len)[0], "nominatif"


def harvest(site):
    """Visit a site + its legal/contact pages, return (email, type, source_url)."""
    url = norm_url(site)
    if not url:
        return "", "", ""
    h = host(url)
    home, final = fetch(url)
    if not home:
        return "", "", ""
    base = final or url
    # candidate pages from homepage links
    cands = []
    for m in re.finditer(r'href=["\']([^"\'#]+)["\']', home):
        href = m.group(1)
        if HINT.search(href) or HINT.search(home[max(0, m.start()-120):m.start()]):
            full = urllib.parse.urljoin(base, href)
            if host(full) == h and full not in cands:
                cands.append(full)
    for g in GUESS:
        full = urllib.parse.urljoin(base, g)
        if full not in cands:
            cands.append(full)
    # search homepage first, then candidates (legal/contact pages prioritaires)
    pages = [(base, home)]
    for c in cands[:6]:
        pg, _ = fetch(c)
        if pg:
            pages.append((c, pg))
        time.sleep(0.2)
    # prefer emails from legal/contact pages
    best = ("", "", "")
    for src, pg in sorted(pages, key=lambda x: 0 if HINT.search(x[0]) else 1):
        em = extract_emails(pg)
        e, t = pick_best(em, h)
        if e:
            # generic same-domain is ideal -> return immediately
            if t == "generique":
                return e, t, src
            if not best[0]:
                best = (e, t, src)
    return best


def main():
    if len(sys.argv) < 2:
        print("usage: enrich_emails.py <salon>-exposants.csv [--limit N] [--icp] [--only-empty]")
        return
    path = sys.argv[1]
    limit = int(sys.argv[sys.argv.index("--limit")+1]) if "--limit" in sys.argv else None
    icp_only = "--icp" in sys.argv
    only_empty = "--only-empty" in sys.argv
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter=";"))
    for r in rows:
        r.setdefault("email_annuaire", r.get("email", ""))
        r.setdefault("email_site", "")
        r.setdefault("email_site_source", "")
        r.setdefault("email_origine", "annuaire" if r.get("email") else "")

    todo = [r for r in rows if norm_url(r.get("site_web"))]
    if icp_only:
        todo = [r for r in todo if r.get("segment_ICP") == "Haute"]
    if only_empty:
        todo = [r for r in todo if not r.get("email")]
    if limit:
        todo = todo[:limit]
    print(f"sites à visiter : {len(todo)} / {len(rows)}")

    hit = 0
    for i, r in enumerate(todo, 1):
        e, t, src = harvest(r["site_web"])
        if e:
            r["email_site"] = e
            r["email_site_source"] = src
            hit += 1
            # On NE remplace PAS un email d'annuaire vérifié : le site comble les
            # trous (et sert de source primaire pour les salons sans annuaire-email).
            if not r.get("email_annuaire"):
                r["email"] = e
                r["type_email"] = t
                r["email_origine"] = "site"
                r["source_url"] = src
                r["date_collecte"] = TODAY
                r["statut_validation"] = "valide"
        if i % 20 == 0:
            print(f"  {i}/{len(todo)} — emails site trouvés: {hit}")
        time.sleep(0.3)

    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
        w.writeheader(); w.writerows(rows)
    print(f"\nTerminé. Emails récupérés via site : {hit}/{len(todo)}  -> {path}")


if __name__ == "__main__":
    main()
