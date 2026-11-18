#!/usr/bin/env python3
"""
Create /comparatifs/meilleur-erp-charcuterie-salaison/ — comparatif page.

Zero-bug strategy: clone the fully-validated metier chrome (page 2818),
replace hero + features(→ static comparison table, NO JS) + FAQ (real drawer
structure), keep generic brand sections. Competitors from live SERP
(DataForSEO, France): VIF, Infologic Copilote, Akanea, CSB-System, Sage, Kardol.

DRY prints lengths + integrity checks. --live creates the page.
"""
import sys, re, json
import wp_common as w

SRC = 2818
PARENT = 7920            # /comparatifs/
SLUG = "meilleur-erp-charcuterie-salaison"
TITLE = "Meilleur ERP charcuterie & salaison : comparatif 2026"
SELF_URL = "https://www.helloharel.com/comparatifs/meilleur-erp-charcuterie-salaison/"

HERO = (
    '<section class="hero-section" style="background:linear-gradient(rgba(0,50,80,0.6),rgba(0,100,160,0.62)),'
    "url('https://www.helloharel.com/wp-content/uploads/2025/07/Logiciel-de-gestion-des-achats-3.png') "
    'center/cover no-repeat;">\n'
    '    <div class="container"><div class="hero-grid"><div class="hero-text">\n'
    '        <div class="hero-badge"><span class="dot"></span>Comparatif 2026</div>\n'
    '        <h1 class="hero-title" style="color:#fff">Meilleur ERP <span class="accent" style="color:#60a5fa">charcuterie &amp; salaison</span> : le comparatif 2026</h1>\n'
    '        <p class="hero-description">7 logiciels ERP passés au crible pour les charcutiers-salaisonniers : '
    'traçabilité de la viande, rendement matière, poids variable et coût de revient. Comparez, puis choisissez en connaissance de cause.</p>\n'
    '        <div class="hero-ctas">\n'
    '            <a href="/contact/" class="hero-cta-primary" style="background:#22C55E !important;border-color:#22C55E !important;color:#fff !important;">Demander une démo</a>\n'
    '            <a href="#comparatif" class="hero-cta-secondary" style="color:#fff !important;border-color:#fff !important;">Voir le comparatif</a>\n'
    '        </div>\n'
    '        <p class="hero-cta-sub">Méthodo : SERP France + fonctionnalités métier vérifiées.</p>\n'
    '    </div><div class="hero-image-spacer"></div></div></div>\n'
    '</section>\n'
)

# rows: name, cible, deploiement, traca_viande, rendement, prix, avis, highlight
ROWS = [
    ("Hello Harel", "TPE, PME & PMI artisanales et industrielles", "SaaS (cloud), déploiement rapide",
     "Complète : lots, DLC, rappel en secondes", "Désassemblage carcasse, poids variable, rendement matière",
     "€ — accessible, dès ~99 €/mois", "5/5 (31 avis)", True),
    ("VIF", "PME & ETI industrielles", "On-premise / cloud, projet long",
     "Complète", "Oui, orienté industrie", "€€€ — élevé", "3,5/5", False),
    ("Infologic Copilote", "PME & ETI", "On-premise",
     "Complète", "Oui", "€€€ — élevé", "—", False),
    ("Akanea (Konnect'AGRO Viandes)", "Filière viande & produits carnés", "SaaS / on-premise",
     "Oui, spécialisée viande", "Oui (découpe, carné)", "€€ — moyen/élevé", "4,2/5", False),
    ("CSB-System", "Grandes industries de la viande", "On-premise, lourd",
     "Très forte (référence viande)", "Oui", "€€€ — élevé", "—", False),
    ("Sage X3", "Généraliste multi-secteurs", "On-premise / cloud",
     "Module, non spécialisé viande", "Limité (pas dédié charcuterie)", "€€€ — élevé", "4,2/5", False),
    ("Kardol", "PME agro (SAP Business One)", "Cloud / on-premise",
     "Oui", "Partiel", "€€ — moyen", "4/5", False),
]

def cell(t):
    return f'<td style="padding:11px 13px;border-bottom:1px solid #e5e7eb;font-size:.92rem;color:#334155;vertical-align:top">{t}</td>'

def table():
    head = ''.join(f'<th style="padding:11px 13px;text-align:left;background:#f1f5f9;color:#475569;'
                   f'font-size:.72rem;text-transform:uppercase;letter-spacing:.03em;white-space:nowrap;'
                   f'border-bottom:2px solid #e2e8f0">{h}</th>'
                   for h in ["ERP", "Cible", "Déploiement", "Traçabilité viande", "Rendement / découpe", "Prix", "Avis"])
    body = ""
    for name, cib, dep, tr, rd, px, av, hi in ROWS:
        bg = 'background:#ecfeff;' if hi else ''
        nm = (f'<td style="padding:11px 13px;border-bottom:1px solid #e5e7eb;font-weight:800;'
              f'color:{"#0090c8" if hi else "#0f172a"};{bg}white-space:nowrap">'
              f'{name}{" ⭐" if hi else ""}</td>')
        body += f'<tr style="{bg}">' + nm + cell(cib) + cell(dep) + cell(tr) + cell(rd) + cell(px) + cell(av) + '</tr>'
    return (f'<div style="overflow-x:auto;border:1px solid #e5e7eb;border-radius:16px;margin:0 0 1.4rem">'
            f'<table style="border-collapse:collapse;width:100%;min-width:820px"><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')

VERDICTS = [
    ("Hello Harel — meilleur choix TPE/PME artisanales & PMI",
     "L'ERP SaaS le plus agile et le plus accessible : rendement matière, poids variable, désassemblage carcasse, "
     "traçabilité et coût de revient, déployé vite et sans gros projet. Noté 5/5. Idéal si vous voulez un outil métier "
     "sans la lourdeur d'un ERP d'ETI."),
    ("VIF, Infologic Copilote, CSB-System — pour les grandes industries",
     "Solutions puissantes et éprouvées pour les ETI et grands groupes viande, mais projets longs et budgets élevés. "
     "Surdimensionnées pour une charcuterie artisanale ou une PME en croissance."),
    ("Akanea, Sage, Kardol — spécialiste viande ou généralistes",
     "Akanea est solide sur la filière carnée ; Sage et Kardol sont généralistes et demandent du paramétrage pour "
     "coller aux spécificités charcuterie-salaison (rendements, DLC courtes, étiquetage INCO)."),
]

def features():
    verd = "".join(
        f'<div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px 18px;margin:0 0 12px">'
        f'<h3 style="margin:0 0 .3rem;font-size:1.05rem;color:#0f172a">{t}</h3>'
        f'<p style="margin:0;color:#475569;line-height:1.6;font-size:.95rem">{d}</p></div>'
        for t, d in VERDICTS)
    return (
        '<section class="features-section" id="comparatif">\n<div class="container">\n'
        '<div class="section-header"><p class="overline">Comparatif ERP charcuterie &amp; salaison</p>\n'
        '<h2>Top 7 des ERP charcuterie &amp; salaison en 2026</h2>\n'
        '<p>Cible, déploiement, traçabilité viande, rendement matière et prix — comparés côte à côte.</p></div>\n'
        + table()
        + '<div style="max-width:900px;margin:0 auto">' + verd + '</div>\n'
        + '<p style="text-align:center;margin:1.4rem 0 0"><a href="/contact/" class="hero-cta-primary" '
          'style="display:inline-block;background:#00B1F5;color:#fff;font-weight:800;padding:13px 26px;'
          'border-radius:12px;text-decoration:none">Voir Hello Harel en démo →</a></p>\n'
        '</div>\n</section>\n'
    )

FAQ_QA = [
    ("Quel est le meilleur ERP pour la charcuterie et la salaison ?", "Meilleur, ERP, charcuterie",
     "Pour une TPE, une PME artisanale ou une PMI, Hello Harel offre le meilleur rapport agilité/prix : SaaS, rendement matière, poids variable, traçabilité et coût de revient, sans la lourdeur d'un ERP d'ETI. VIF, Infologic Copilote et CSB-System s'adressent surtout aux grandes industries de la viande."),
    ("Quelle différence entre un ERP généraliste et un ERP charcuterie-salaison ?", "Différence, ERP, généraliste",
     "Un ERP charcuterie-salaison gère nativement les spécificités du métier : désassemblage de carcasse, rendement matière, poids variable, DLC courtes, recettes et coût de revient, étiquetage INCO. Un ERP généraliste (Sage, Kardol) demande beaucoup de paramétrage pour approcher ces fonctions."),
    ("Un ERP charcuterie gère-t-il le rendement matière et le poids variable ?", "Rendement, poids variable",
     "Oui : c'est un critère décisif. Hello Harel calcule les rendements par recette et par découpe, gère le poids variable de la réception à la facturation, et remonte le coût de revient au centime."),
    ("Combien coûte un ERP charcuterie-salaison ?", "Combien, coûte, prix",
     "Les ERP d'ETI (VIF, Infologic, CSB) représentent des projets à plusieurs dizaines de milliers d'euros. Une solution SaaS comme Hello Harel démarre à quelques dizaines d'euros par mois et par utilisateur, sans gros investissement initial."),
    ("ERP SaaS ou on-premise pour une charcuterie ?", "SaaS, on-premise",
     "Le SaaS (cloud) évite l'installation serveur, se déploie vite, se met à jour automatiquement et s'accède partout — idéal pour une charcuterie ou une PME. L'on-premise reste choisi par les grands groupes ayant une DSI dédiée."),
    ("Comment assurer la traçabilité de la viande et les rappels de lot ?", "Traçabilité, viande, rappel",
     "Un bon ERP trace chaque lot de l'agréage au client (ascendante et descendante). En cas d'alerte, vous identifiez en secondes les produits et clients concernés et éditez le dossier de retrait-rappel — natif chez Hello Harel."),
]

def faq(src_raw):
    a = src_raw.find('<section class="faq-section"'); b = src_raw.find('<section class="reviews-section"')
    span = src_raw[a:b]
    span = re.sub(r'(<p class="overline">)[^<]*(</p>)', r'\1FAQ Comparatif\2', span, count=1)
    span = re.sub(r'(<section class="faq-section"[^>]*>.*?<h2>).*?(</h2>)',
                  r'\1Questions fréquentes sur le choix d\'un ERP charcuterie &amp; salaison\2', span, count=1, flags=re.S)
    qi = [0]
    def rc(m):
        i = qi[0]; qi[0] += 1; q, meta, _ = FAQ_QA[i]
        return (f'<span class="faq-card-question">{q}</span>\n'
                f'                    <span class="faq-card-meta">{meta}</span>')
    span = re.sub(r'<span class="faq-card-question">.*?</span>\s*<span class="faq-card-meta">.*?</span>', rc, span, flags=re.S)
    pi = [0]
    def rp(m):
        i = pi[0]; pi[0] += 1; q, _, ans = FAQ_QA[i]
        return f'{m.group(1)}<h3>{q}</h3>\n            <div class="faq-drawer-content"><p>{ans}</p></div>'
    span = re.sub(r'(<div class="faq-drawer-panel"[^>]*>\s*)<h3>.*?</h3>\s*<div class="faq-drawer-content">.*?</div>',
                  rp, span, flags=re.S)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
                         for q, _, ans in FAQ_QA]}
    span = re.sub(r'<script type="application/ld\+json">\s*\{.*?"FAQPage".*?\}\s*</script>',
                  '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
                  span, count=1, flags=re.S)
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
    # breadcrumb self-URL + label
    c = c.replace("https://www.helloharel.com/agroalimentaire/charcutier/", SELF_URL)
    c = re.sub(r'"name"\s*:\s*"(ERP )?Charcutier"', '"name": "Comparatif ERP charcuterie & salaison"', c)

    checks = {"faqDrawerOverlay": c.count("faqDrawerOverlay"),
              "faq-drawer-panel": c.count('faq-drawer-panel"'),
              "openFaqDrawer(": c.count("openFaqDrawer("),
              "comparison table rows": c.count('</tr>'),
              "residual charcutier": c.lower().count("charcutier")}
    print("Assembled:", len(c), "| checks:", checks)
    if not live:
        print("DRY-RUN — pass --live to create."); return
    res = w.api("pages", method="POST", data={
        "slug": SLUG, "title": TITLE, "content": c, "status": "publish",
        "parent": PARENT, "template": "elementor_canvas"})
    print("CREATED id", res.get("id"), res.get("link"))

if __name__ == "__main__":
    main()
