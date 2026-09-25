#!/usr/bin/env python3
"""
Phase 2+3 scraper — SERBOTEL (serbotel.com) exhibitor directory.
The public directory exposes, per exhibitor: name, sector, address/city,
contact, email (HTML-entity-encoded mailto), phone, website. We parse the
alphabetical pages /exposants/abcd/<letter> and emit a clean CSV row each.

Compliance: public professional B2B directory; we log source_url + date,
classify generic vs nominative email, and tag ICP relevance. No JS, polite rate.

Run: python3 scrape_serbotel.py
Out: serbotel-exposants.csv
"""
import re, csv, time, ssl, html, urllib.request, datetime, string

BASE = "https://www.serbotel.com"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; HelloHarel-Prospection/1.0)"
TODAY = datetime.date.today().isoformat()

GENERIC = ("contact", "info", "infos", "commercial", "accueil", "hello", "bonjour",
           "direction", "rh", "compta", "comptabilite", "sav", "contact1", "service",
           "communication", "marketing", "administration", "secretariat", "vente", "ventes")

# ICP relevance: sectors where the exhibitor IS a food producer/processor/wholesaler
ICP_HI = ("AGROALIMENTAIRE", "CHARCUTERIE", "BOULANGERIE", "PATISSERIE", "FROMAGE",
          "LAITIER", "TRAITEUR", "VIANDE", "POISSON", "MAREE", "FRUITS", "LEGUMES",
          "BOISSON", "VIN", "BIERE", "EPICERIE", "SNACKING", "PRODUITS ALIMENTAIRES",
          "PRODUITS SUCRES", "VIENNOISERIE", "GLACE", "CHOCOLAT", "MATIERES PREMIERES",
          "CONSERVE", "PLATS", "SURGELES", "CREMERIE", "BRASSERIE", "DISTILLERIE")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if attempt == 2:
                return ""
            time.sleep(2 * (attempt + 1))


def decode_mailto(block):
    m = re.search(r"href='(&#[0-9]+;(?:&#[0-9]+;)*)'", block)  # entity-encoded mailto
    if not m:
        m = re.search(r'href="(mailto:[^"]+)"', block)
        if not m:
            return ""
        raw = m.group(1)
    else:
        raw = html.unescape(m.group(1))
    raw = raw.replace("mailto:", "").strip()
    em = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
    return em.group(0).lower() if em else ""


def classify(email):
    if not email:
        return ""
    local = email.split("@")[0]
    return "generique" if any(local == g or local.startswith(g) for g in GENERIC) else "nominatif"


def icp(sector):
    s = sector.upper()
    return "Haute" if any(k in s for k in ICP_HI) else "Faible/à qualifier"


def parse_page(html_str, url):
    rows = []
    # split into blocks by the exhibitor heading
    parts = re.split(r'<h5><a href="(/exposants/fiche/\d+)">', html_str)
    # parts: [pre, href1, block1, href2, block2, ...]
    for i in range(1, len(parts), 2):
        href = parts[i]
        block = parts[i + 1]
        name_m = re.match(r'\s*(.*?)</a></h5>', block, re.S)
        name = html.unescape(re.sub(r'<[^>]+>', '', name_m.group(1)).strip()) if name_m else ""
        if not name:
            continue
        sec_m = re.search(r'<p class="bold">(.*?)</p>', block, re.S)
        sector = html.unescape(re.sub(r'\s+', ' ', sec_m.group(1)).strip()) if sec_m else ""
        city, dept = "", ""
        addr = re.search(r'(\d{5})\s+([A-ZÀ-Ÿ' + r"'\- ]+?)(?:\s+CEDEX)?\s*,?\s*France", block)
        if addr:
            cp = addr.group(1); dept = cp[:2]
            city = html.unescape(addr.group(2).strip().title())
        person = ""
        pm = re.search(r"<p class='dotted'>\s*([A-ZÀ-Ÿ][^<\n]+?)\s*<br", block)
        if pm and "@" not in pm.group(1):
            person = html.unescape(pm.group(1).strip())
        phone = ""
        ph = re.search(r'T[ée]l\s*:\s*([0-9 .]{8,})', block)
        if ph:
            phone = ph.group(1).strip()
        web = ""
        wm = re.search(r'href="(https?://(?!www\.serbotel|serbotel\.)[^"]+)"', block)
        if wm:
            web = wm.group(1).strip()
        email = decode_mailto(block)
        rows.append({
            "salon": "Serbotel", "edition_annee": "2025", "entreprise": name,
            "secteur_metier": sector, "site_web": web, "email": email,
            "type_email": classify(email), "nom_contact": person, "fonction": "",
            "ville": city, "departement": dept, "telephone": phone,
            "source_url": url, "date_collecte": TODAY,
            "statut_validation": "valide" if email else "sans_email",
            "segment_ICP": icp(sector),
        })
    return rows


def main():
    letters = list(string.ascii_lowercase)
    all_rows = []
    for L in letters:
        url = f"{BASE}/exposants/abcd/{L}"
        page = fetch(url)
        if not page:
            print(f"  {L}: fetch failed"); continue
        rows = parse_page(page, url)
        all_rows += rows
        print(f"  {L}: {len(rows)} exposants")
        time.sleep(0.5)
    # dedupe by (entreprise, email)
    seen, dedup = set(), []
    for r in all_rows:
        k = (r["entreprise"].lower(), r["email"])
        if k in seen:
            continue
        seen.add(k); dedup.append(r)
    cols = ["salon", "edition_annee", "entreprise", "secteur_metier", "site_web", "email",
            "type_email", "nom_contact", "fonction", "ville", "departement", "telephone",
            "source_url", "date_collecte", "statut_validation", "segment_ICP"]
    with open("serbotel-exposants.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";"); w.writeheader(); w.writerows(dedup)
    with_email = sum(1 for r in dedup if r["email"])
    gen = sum(1 for r in dedup if r["type_email"] == "generique")
    hi = sum(1 for r in dedup if r["segment_ICP"] == "Haute")
    print(f"\nTOTAL exposants: {len(dedup)} | avec email: {with_email} "
          f"(génériques {gen} / nominatifs {with_email - gen}) | ICP Haute: {hi}")


if __name__ == "__main__":
    main()
