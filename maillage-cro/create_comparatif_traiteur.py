#!/usr/bin/env python3
"""
Create /comparatifs/meilleur-erp-traiteur/ — comparatif traiteur.
Same zero-bug method as the charcuterie comparatif (clone metier chrome 2818,
replace hero + features(static table, no JS) + FAQ (real drawer), fix
breadcrumb). Competitors from live DataForSEO SERP (France).
DRY by default; --live to create.
"""
import sys, re, json
import wp_common as w

SRC = 2818
PARENT = 7920
SLUG = "meilleur-erp-traiteur"
TITLE = "Meilleur logiciel & ERP traiteur : comparatif 2026"
SELF_URL = "https://www.helloharel.com/comparatifs/meilleur-erp-traiteur/"

HERO = (
    '<section class="hero-section" style="background:linear-gradient(rgba(0,50,80,0.6),rgba(0,100,160,0.62)),'
    "url('https://www.helloharel.com/wp-content/uploads/2025/07/Logiciel-de-gestion-des-achats-3.png') "
    'center/cover no-repeat;">\n'
    '    <div class="container"><div class="hero-grid"><div class="hero-text">\n'
    '        <div class="hero-badge"><span class="dot"></span>Comparatif 2026</div>\n'
    '        <h1 class="hero-title" style="color:#fff">Meilleur logiciel &amp; ERP <span class="accent" style="color:#60a5fa">traiteur</span> : le comparatif 2026</h1>\n'
    '        <p class="hero-description">7 solutions passées au crible pour les traiteurs et organisateurs de réceptions : '
    'devis événementiel, fiches techniques, coût de revient, production et traçabilité. Comparez avant de choisir.</p>\n'
    '        <div class="hero-ctas">\n'
    '            <a href="/contact/" class="hero-cta-primary" style="background:#22C55E !important;border-color:#22C55E !important;color:#fff !important;">Demander une démo</a>\n'
    '            <a href="#comparatif" class="hero-cta-secondary" style="color:#fff !important;border-color:#fff !important;">Voir le comparatif</a>\n'
    '        </div>\n'
    '        <p class="hero-cta-sub">Méthodo : SERP France + fonctionnalités métier vérifiées.</p>\n'
    '    </div><div class="hero-image-spacer"></div></div></div>\n'
    '</section>\n'
)

ROWS = [
    ("Hello Harel", "Traiteurs & centres de production, PME/PMI", "SaaS (cloud)",
     "Devis, dossiers, planning", "Complète : recettes, coût de revient au gramme, traçabilité, DLC",
     "€ — accessible", "5/5 (31 avis)", True),
    ("Sextan", "Traiteurs & organisateurs de réceptions", "SaaS",
     "Fort (CRM réception, événementiel)", "Oui (production, logistique)", "€€ — moyen/élevé", "—", False),
    ("MOBICHEF", "Traiteurs & réceptions (TPE/PME)", "Windows/Mac + web",
     "Devis & factures personnalisés, planning", "Coût de revient", "€€ — moyen", "—", False),
    ("Servolution (Commertra)", "Traiteurs événementiels", "ERP",
     "Devis événementiel, Factur-X 2026", "Fiches techniques recettes", "€€ — moyen", "—", False),
    ("Chef Traiteur", "Traiteurs (PGI/ERP)", "ERP",
     "Gestion des prestations", "Oui", "€€ — moyen", "—", False),
    ("Traiteur Digital", "Auto-entrepreneurs & TPE", "SaaS",
     "Devis & factures", "Limité", "€ — faible", "—", False),
    ("Kolirys", "TPE traiteur", "SaaS",
     "Devis & factures", "Limité", "€ — faible", "—", False),
]

def cell(t):
    return f'<td style="padding:11px 13px;border-bottom:1px solid #e5e7eb;font-size:.92rem;color:#334155;vertical-align:top">{t}</td>'

def table():
    head = ''.join(f'<th style="padding:11px 13px;text-align:left;background:#f1f5f9;color:#475569;'
                   f'font-size:.72rem;text-transform:uppercase;letter-spacing:.03em;white-space:nowrap;'
                   f'border-bottom:2px solid #e2e8f0">{h}</th>'
                   for h in ["Solution", "Cible", "Déploiement", "Devis / événementiel", "Production / coût de revient", "Prix", "Avis"])
    body = ""
    for name, cib, dep, ev, pr, px, av, hi in ROWS:
        bg = 'background:#ecfeff;' if hi else ''
        nm = (f'<td style="padding:11px 13px;border-bottom:1px solid #e5e7eb;font-weight:800;'
              f'color:{"#0090c8" if hi else "#0f172a"};{bg}white-space:nowrap">{name}{" ⭐" if hi else ""}</td>')
        body += f'<tr style="{bg}">' + nm + cell(cib) + cell(dep) + cell(ev) + cell(pr) + cell(px) + cell(av) + '</tr>'
    return (f'<div style="overflow-x:auto;border:1px solid #e5e7eb;border-radius:16px;margin:0 0 1.4rem">'
            f'<table style="border-collapse:collapse;width:100%;min-width:820px"><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')

VERDICTS = [
    ("Hello Harel — le meilleur choix pour les traiteurs qui produisent",
     "Au-delà du devis, Hello Harel gère la <b>production</b> : recettes et sous-recettes, <b>coût de revient au gramme</b>, "
     "traçabilité, DLC et multi-sites. Idéal pour un traiteur avec un vrai centre de production ou plusieurs boutiques. Noté 5/5."),
    ("Sextan, MOBICHEF, Servolution, Chef Traiteur — spécialistes traiteur/événementiel",
     "Très bons sur le <b>CRM réception et le devis événementiel</b> (BEO, planning, dossiers). Sextan est le leader dédié. "
     "Moins orientés production industrielle / coût matière fin que Hello Harel."),
    ("Traiteur Digital, Kolirys — pour auto-entrepreneurs & TPE",
     "Parfaits pour <b>démarrer</b> (devis, factures, clients) à petit budget, mais sans dimension production ni coût de revient détaillé "
     "quand l'activité grandit."),
]

def features():
    verd = "".join(
        f'<div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px 18px;margin:0 0 12px">'
        f'<h3 style="margin:0 0 .3rem;font-size:1.05rem;color:#0f172a">{t}</h3>'
        f'<p style="margin:0;color:#475569;line-height:1.6;font-size:.95rem">{d}</p></div>'
        for t, d in VERDICTS)
    return (
        '<section class="features-section" id="comparatif">\n<div class="container">\n'
        '<div class="section-header"><p class="overline">Comparatif logiciel &amp; ERP traiteur</p>\n'
        '<h2>Top 7 des logiciels &amp; ERP traiteur en 2026</h2>\n'
        '<p>Cible, déploiement, devis événementiel, production &amp; coût de revient, prix — côte à côte.</p></div>\n'
        + table()
        + '<div style="max-width:900px;margin:0 auto">' + verd + '</div>\n'
        + '<p style="text-align:center;margin:1.4rem 0 0"><a href="/contact/" class="hero-cta-primary" '
          'style="display:inline-block;background:#00B1F5;color:#fff;font-weight:800;padding:13px 26px;'
          'border-radius:12px;text-decoration:none">Voir Hello Harel en démo →</a></p>\n'
        '</div>\n</section>\n'
    )

FAQ_QA = [
    ("Quel est le meilleur logiciel pour un traiteur ?", "Meilleur, logiciel, traiteur",
     "Pour un traiteur qui produit (centre de production, plusieurs boutiques), Hello Harel offre le meilleur rapport complet/prix : devis, recettes, coût de revient au gramme, traçabilité et DLC. Sextan, MOBICHEF et Servolution sont d'excellents spécialistes du devis événementiel ; Traiteur Digital et Kolirys conviennent aux auto-entrepreneurs."),
    ("Différence entre un ERP traiteur et un simple logiciel de devis ?", "Différence, ERP, devis",
     "Un logiciel de devis gère la commande client (devis, facture, BEO). Un ERP traiteur y ajoute la production : recettes, fiches techniques, coût de revient, achats, stocks, traçabilité et DLC — indispensable dès que vous fabriquez en volume."),
    ("Le logiciel calcule-t-il le coût de revient et les fiches techniques ?", "Coût de revient, fiches techniques",
     "Oui : Hello Harel calcule le coût de revient au gramme par recette et par prestation, à partir des matières, des rendements et des sous-recettes, avec fiches techniques et marge par produit."),
    ("Gère-t-il les devis événementiels et le planning des prestations ?", "Devis, événementiel, planning",
     "Oui : devis par prestation, dossiers clients, planning de production et de livraison. L'événementiel (nombre de couverts, dressage, logistique) est piloté sans ressaisie de la commande à la facture."),
    ("Combien coûte un logiciel traiteur ?", "Combien, coûte, prix",
     "Les outils de devis pour TPE démarrent à quelques dizaines d'euros par mois. Un ERP traiteur complet en SaaS comme Hello Harel reste accessible (dès quelques dizaines d'euros/utilisateur) sans le coût d'un ERP d'ETI."),
    ("SaaS (cloud) ou logiciel installé pour un traiteur ?", "SaaS, cloud, installé",
     "Le SaaS se déploie vite, se met à jour seul et s'accède partout (cuisine, événement, bureau) — idéal pour un traiteur mobile. L'installé reste réservé aux structures avec une informatique dédiée."),
]

def faq(src_raw):
    a = src_raw.find('<section class="faq-section"'); b = src_raw.find('<section class="reviews-section"')
    span = src_raw[a:b]
    span = re.sub(r'(<p class="overline">)[^<]*(</p>)', r'\1FAQ Comparatif\2', span, count=1)
    span = re.sub(r'(<section class="faq-section"[^>]*>.*?<h2>).*?(</h2>)',
                  r'\1Questions fréquentes sur le choix d\'un logiciel traiteur\2', span, count=1, flags=re.S)
    qi = [0]
    def rc(m):
        i = qi[0]; qi[0] += 1; q, meta, _ = FAQ_QA[i]
        return f'<span class="faq-card-question">{q}</span>\n                    <span class="faq-card-meta">{meta}</span>'
    span = re.sub(r'<span class="faq-card-question">.*?</span>\s*<span class="faq-card-meta">.*?</span>', rc, span, flags=re.S)
    pi = [0]
    def rp(m):
        i = pi[0]; pi[0] += 1; q, _, ans = FAQ_QA[i]
        return f'{m.group(1)}<h3>{q}</h3>\n            <div class="faq-drawer-content"><p>{ans}</p></div>'
    span = re.sub(r'(<div class="faq-drawer-panel"[^>]*>\s*)<h3>.*?</h3>\s*<div class="faq-drawer-content">.*?</div>',
                  rp, span, flags=re.S)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, _, ans in FAQ_QA]}
    span = re.sub(r'<script type="application/ld\+json">\s*\{.*?"FAQPage".*?\}\s*</script>',
                  '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>', span, count=1, flags=re.S)
    return span

def span_between(c, f, t):
    a = c.find('<section class="%s"' % f); b = c.find('<section class="%s"' % t)
    if a < 0 or b < 0 or b <= a: raise SystemExit(f"span {f}->{t} not found")
    return a, b

def main():
    live = "--live" in sys.argv
    src = w.get_raw("pages", SRC)["content"]["raw"]
    c = src
    a, b = span_between(c, "faq-section", "reviews-section"); c = c[:a] + faq(src) + c[b:]
    a, b = span_between(c, "features-section", "about-card-section"); c = c[:a] + features() + c[b:]
    a, b = span_between(c, "hero-section", "logos-section"); c = c[:a] + HERO + c[b:]
    c = c.replace("https://www.helloharel.com/agroalimentaire/charcutier/", SELF_URL)
    c = re.sub(r'"name"\s*:\s*"(ERP )?Charcutier"', '"name": "Comparatif logiciel & ERP traiteur"', c)
    checks = {"faqDrawerOverlay": c.count("faqDrawerOverlay"), "faq-drawer-panel": c.count('faq-drawer-panel"'),
              "openFaqDrawer(": c.count("openFaqDrawer("), "rows": c.count('</tr>'), "charcutier": c.lower().count("charcutier")}
    print("Assembled", len(c), "| checks", checks)
    if not live:
        print("DRY-RUN"); return
    res = w.api("pages", method="POST", data={"slug": SLUG, "title": TITLE, "content": c,
                "status": "publish", "parent": PARENT, "template": "elementor_canvas"})
    print("CREATED id", res.get("id"), res.get("link"))

if __name__ == "__main__":
    main()
