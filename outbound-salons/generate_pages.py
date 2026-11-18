#!/usr/bin/env python3
"""
Génère les pages perso prospect (et les emails de la séquence) en remplaçant les
variables {{...}} par les données de la base. Démo : génère un échantillon.

Usage:
  python3 generate_pages.py [--limit N] [--salon Serbotel]
Sortie:
  pages-perso/<entreprise>.html   (1 page par prospect avec email valide)
"""
import csv, glob, os, re, sys, html

TEMPLATE = "page-perso-prospect.html"
LIEN_DEMO = "https://www.helloharel.com/demo"   # à remplacer par votre lien RDV
PRENOM_COMMERCIAL = "Rémi"

def first_name(full):
    return full.strip().split()[0] if full and full.strip() else ""

def fill(tpl, row):
    secteur = row.get("secteur_metier", "") or "agroalimentaires"
    secteur = re.sub(r"\s*\(.*?\)", "", secteur).strip().lower()  # enlève "(Medfel)" etc.
    vals = {
        "prenom": first_name(row.get("nom_contact", "")) or "Bonjour",
        "nom_entreprise": row.get("entreprise", "").strip(),
        "secteur_metier": secteur or "agroalimentaires",
        "ville": (row.get("ville") or "").strip() or "votre région",
        "salon": row.get("salon", "").strip(),
        "lien_demo": LIEN_DEMO,
        "prenom_commercial": PRENOM_COMMERCIAL,
    }
    out = tpl
    for k, v in vals.items():
        out = out.replace("{{%s}}" % k, html.escape(v, quote=True))
    return out

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "prospect"

def main():
    limit = int(sys.argv[sys.argv.index("--limit")+1]) if "--limit" in sys.argv else 10
    salon = sys.argv[sys.argv.index("--salon")+1] if "--salon" in sys.argv else None
    tpl = open(TEMPLATE, encoding="utf-8").read()
    rows = []
    for p in glob.glob("*-exposants.csv"):
        for r in csv.DictReader(open(p, encoding="utf-8"), delimiter=";"):
            if r.get("email") and r.get("statut_validation") == "valide":
                if not salon or r.get("salon") == salon:
                    rows.append(r)
    os.makedirs("pages-perso", exist_ok=True)
    n = 0
    for r in rows[:limit]:
        open(f"pages-perso/{slug(r['entreprise'])}.html", "w", encoding="utf-8").write(fill(tpl, r))
        n += 1
    print(f"{n} pages générées dans pages-perso/ (sur {len(rows)} prospects valides)")

if __name__ == "__main__":
    main()
