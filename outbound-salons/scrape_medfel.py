#!/usr/bin/env python3
"""
Phase 2 — MEDFEL (medfel.com) exhibitor list via the site's OWN public WP REST
feed (flux interne autorisé) : custom post type 'exposant'.
Medfel n'expose PAS les sites/emails (JS + meta protégée) — on récupère donc la
LISTE des exposants (nom + page détail) ; l'email sera ajouté ensuite via
l'étape nom→site. Aucune API tierce.

Run: python3 scrape_medfel.py
Out: medfel-exposants.csv
"""
import json, csv, ssl, time, html, urllib.request, datetime

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; HelloHarel-Prospection/1.0)"
TODAY = datetime.date.today().isoformat()
BASE = "https://www.medfel.com/wp-json/wp/v2/exposant"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for a in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception:
            if a == 2:
                return []
            time.sleep(2)


def main():
    rows, page = [], 1
    while True:
        data = fetch_json(f"{BASE}?per_page=100&page={page}&_fields=id,slug,link,title")
        if not isinstance(data, list) or not data:
            break
        for e in data:
            name = html.unescape((e.get("title") or {}).get("rendered", "")).strip()
            if not name:
                continue
            rows.append({
                "salon": "Medfel", "edition_annee": "2026", "entreprise": name,
                "secteur_metier": "Fruits & légumes / négoce (Medfel)", "site_web": "",
                "email": "", "type_email": "", "email_origine": "", "email_annuaire": "",
                "email_site": "", "email_site_source": "", "nom_contact": "", "fonction": "",
                "ville": "", "departement": "", "telephone": "",
                "source_url": e.get("link", ""), "date_collecte": TODAY,
                "statut_validation": "a_enrichir", "segment_ICP": "Haute",
            })
        print(f"  page {page}: {len(data)} exposants")
        if len(data) < 100:
            break
        page += 1
        time.sleep(0.4)
    cols = ["salon", "edition_annee", "entreprise", "secteur_metier", "site_web", "email",
            "type_email", "email_origine", "email_annuaire", "email_site", "email_site_source",
            "nom_contact", "fonction", "ville", "departement", "telephone",
            "source_url", "date_collecte", "statut_validation", "segment_ICP"]
    with open("medfel-exposants.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";"); w.writeheader(); w.writerows(rows)
    print(f"\nTOTAL Medfel: {len(rows)} exposants (liste) -> medfel-exposants.csv "
          f"(emails à enrichir via nom→site)")


if __name__ == "__main__":
    main()
