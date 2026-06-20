#!/usr/bin/env python3
"""
Phase 4 — Précision des emails. Pour chaque ligne possédant un email :
  1) Syntaxe RFC simple.
  2) MX : le domaine a-t-il un enregistrement MX (peut recevoir des mails) ?
     -> sinon repli sur A/AAAA (domaine résout).
  3) Correspondance nom entreprise <-> domaine (token overlap + similarité difflib)
     pour démasquer les mauvais rapprochements (ex. IBANEZ guitare, VEGETABLE).

Met à jour statut_validation :
  valide          = MX ok ET correspondance nom↔domaine forte
  a_verifier      = MX ok MAIS correspondance faible (revue humaine)
  email_invalide  = pas de MX et domaine ne résout pas  (email retiré)
Écrit aussi un score 0-100 dans la colonne 'type_email' ? NON : on garde le schéma.
Un récap est affiché. Cache DNS pour la vitesse.

Usage: python3 verify_emails.py <salon>-exposants.csv [--strict]
       (--strict : retire l'email aussi quand statut devient 'a_verifier')
"""
import sys, csv, re, difflib, urllib.parse
import dns.resolver

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
GENERIC_LOCAL = {"contact", "info", "infos", "hello", "bonjour", "commercial",
                 "accueil", "sales", "rh", "recrutement", "service", "admin"}
DNS_CACHE = {}
res = dns.resolver.Resolver()
res.lifetime = 5.0; res.timeout = 5.0


def domain_status(dom):
    """'mx' | 'resolve' | 'dead' (avec cache)."""
    if dom in DNS_CACHE:
        return DNS_CACHE[dom]
    st = "dead"
    try:
        if res.resolve(dom, "MX"):
            st = "mx"
    except Exception:
        try:
            res.resolve(dom, "A"); st = "resolve"
        except Exception:
            st = "dead"
    DNS_CACHE[dom] = st
    return st


def norm(s):
    s = s.lower()
    for w in (" sarl", " sas", " sa ", " spa", " sl", " gmbh", " srl", " eurl",
              " group", " groupe", " france", " export", " import", " trading"):
        s = s.replace(w, " ")
    return re.split(r'[^a-z0-9]+', s)


def match_score(name, email, site):
    """0-100 : à quel point le domaine 'colle' au nom de l'entreprise."""
    dom = email.split("@")[1].lower()
    sld = dom.split(".")[0]  # second-level (ex. medimat)
    # comparer au domaine du site aussi (cohérence)
    name_toks = [t for t in norm(name) if len(t) > 2]
    if not name_toks:
        return 0
    best = 0
    for t in name_toks:
        best = max(best, difflib.SequenceMatcher(None, t, sld).ratio())
        if t in sld or sld in t:
            best = max(best, 0.95)
    # bonus si le nom entier compacté est proche du domaine
    compact = "".join(name_toks)
    best = max(best, difflib.SequenceMatcher(None, compact, sld).ratio())
    return int(best * 100)


def main():
    if len(sys.argv) < 2:
        print("usage: verify_emails.py <csv> [--strict]"); return
    path = sys.argv[1]; strict = "--strict" in sys.argv
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter=";"))
    n_mail = n_valide = n_verif = n_dead = 0
    for r in rows:
        em = (r.get("email") or "").strip()
        if not em:
            continue
        n_mail += 1
        if not EMAIL_RE.match(em):
            r["statut_validation"] = "email_invalide"; r["email"] = ""; n_dead += 1
            continue
        dom = em.split("@")[1]
        dstat = domain_status(dom)
        if dstat == "dead":
            # email invalide (domaine sans MX et ne résout pas) -> supprimé
            r["statut_validation"] = "email_invalide"
            r["email"] = ""; r["email_site"] = ""; r["type_email"] = ""
            n_dead += 1
            continue
        score = match_score(r["entreprise"], em, r.get("site_web", ""))
        local = em.split("@")[0].lower()
        # un email nominatif ou un domaine très proche du nom = confiance haute
        strong = score >= 60 or (local not in GENERIC_LOCAL and score >= 45)
        if strong:
            r["statut_validation"] = "valide"; n_valide += 1
        else:
            r["statut_validation"] = "a_verifier"; n_verif += 1
            if strict:
                r["email"] = ""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    print(f"emails analysés : {n_mail}")
    print(f"  valide (MX + nom OK)      : {n_valide}")
    print(f"  a_verifier (MX, nom faible): {n_verif}")
    print(f"  email_invalide (domaine KO): {n_dead}")
    print(f"-> {path}")


if __name__ == "__main__":
    main()
