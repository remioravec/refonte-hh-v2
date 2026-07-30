#!/usr/bin/env python3
"""
Create /fonctionnalites/tracabilite-alimentaire/ (feature/money page for
"logiciel traçabilité alimentaire", currently captured at pos ~30 by the hub).

Method: clone the metier template chrome (page 2818, self-contained HTML) and
splice in authored traçabilité content for the 3 metier-specific regions
(hero, features bento, FAQ). Generic brand sections (logos, about, process,
metiers, team, reviews) are kept as-is. Breadcrumb JSON-LD self-URL fixed.
No Elementor is touched.

DRY (default) prints lengths only. --live creates the page.
"""
import sys, re
import wp_common as w

SRC = 2818
PARENT = 4728
SLUG = "tracabilite-alimentaire"
TITLE = "Logiciel de traçabilité alimentaire"

ICON = ('<div class="tilted-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">'
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
        'd="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div>')

def chk(t):
    return ('<li><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
            'd="M5 13l4 4L19 7"/></svg>' + t + '</li>')

def card(title, desc, items, span2=False):
    lis = "".join(chk(x) for x in items)
    cls = "bento-card span-2 scroll-reveal" if span2 else "bento-card scroll-reveal"
    return (f'<div class="{cls}">{ICON}<h3>{title}</h3><p>{desc}</p>'
            f'<ul class="check-list">{lis}</ul></div>')

HERO = (
    '<section class="hero-section" style="background:linear-gradient(rgba(0,50,80,0.55),rgba(0,100,160,0.6)),'
    "url('https://www.helloharel.com/wp-content/uploads/2025/07/Logiciel-de-gestion-des-achats-3.png') "
    'center/cover no-repeat;">\n'
    '    <div class="container"><div class="hero-grid"><div class="hero-text">\n'
    '        <div class="hero-badge"><span class="dot"></span>Traçabilité alimentaire</div>\n'
    '        <h1 class="hero-title" style="color:#fff">Le logiciel de <span class="accent" style="color:#60a5fa">traçabilité alimentaire</span> de vos lots</h1>\n'
    '        <p class="hero-description">Traçabilité ascendante et descendante, gestion des lots, DLC/DDM et FEFO, '
    'étiquetage INCO et rappel de lot en quelques secondes. L\'ERP agroalimentaire qui sécurise vos audits HACCP et le Paquet Hygiène.</p>\n'
    '        <div class="hero-ctas">\n'
    '            <a href="/contact/" class="hero-cta-primary" style="background:#22C55E !important;border-color:#22C55E !important;color:#fff !important;">Demander une démo</a>\n'
    '            <a href="/contact/" class="hero-cta-secondary" style="color:#fff !important;border-color:#fff !important;">Essayez</a>\n'
    '        </div>\n'
    '        <p class="hero-cta-sub">Sans engagement. Déploiement clé en main.</p>\n'
    '    </div><div class="hero-image-spacer"></div></div></div>\n'
    '</section>\n'
)

FEATURES = (
    '<section class="features-section" id="fonctionnalites">\n<div class="container">\n'
    '<div class="section-header"><p class="overline">Logiciel de traçabilité alimentaire</p>\n'
    '<h2>Une traçabilité complète, du lot fournisseur au client livré</h2>\n'
    '<p>Traçabilité ascendante et descendante, lots, DLC/DDM, FEFO, rappel et étiquetage INCO</p></div>\n'
    '<div class="bento-grid">\n'
    + card("Traçabilité ascendante et descendante",
           "Remontez d'un produit fini à chaque lot de matière première, et redescendez d'un lot vers tous les produits et clients concernés. Traçabilité quantitative et qualitative sur toute la chaîne.",
           ["Généalogie complète des lots", "Traçabilité au n° de lot et à la DLC", "Historique conservé pour vos audits"], span2=True)
    + card("Gestion des lots et des DLC/DDM",
           "Chaque réception, fabrication et expédition est rattachée à un lot daté, avec DLC/DDM et rotation FEFO pour limiter les pertes.",
           ["FEFO (First Expired, First Out)", "Alertes sur les dates courtes"])
    + card("Rappel de lot en quelques secondes",
           "En cas d'alerte sanitaire, identifiez instantanément les produits finis et les clients à rappeler, et éditez le dossier de retrait-rappel prêt pour la DGCCRF.",
           ["Blocage immédiat des lots concernés", "Liste des clients à rappeler", "Dossier de retrait-rappel"])
    + card("Étiquetage INCO et conformité HACCP",
           "Éditez des étiquettes conformes INCO (allergènes, valeurs nutritionnelles, estampille) et documentez vos contrôles pour le Paquet Hygiène et vos certifications (IFS, BRC).",
           ["Étiquettes INCO automatiques", "Plans de contrôle et non-conformités", "Prêt pour audits IFS / BRC"], span2=True)
    + '</div>\n</div>\n</section>\n'
)

# 6 Q&A (must stay 6 = number of cards/panels the drawer JS expects).
FAQ_QA = [
    ("Qu'est-ce qu'un logiciel de traçabilité alimentaire ?", "Comment, traçabilité, logiciel",
     "Un logiciel de traçabilité alimentaire enregistre, pour chaque lot, son origine, sa transformation et sa destination. Il permet de retrouver instantanément d'où vient un produit (traçabilité ascendante) et où il est parti (traçabilité descendante) — une obligation du Paquet Hygiène et le cœur de la méthode HACCP."),
    ("Comment gérer un rappel de lot avec Hello Harel ?", "Comment, rappel, lot",
     "À partir d'un lot suspect, Hello Harel identifie en quelques secondes tous les produits finis qui le contiennent et tous les clients livrés. Vous bloquez les lots concernés, éditez la liste des clients à contacter et générez le dossier de retrait-rappel prêt pour la DGCCRF."),
    ("Le logiciel gère-t-il les DLC, DDM et la méthode FEFO ?", "DLC, DDM, FEFO",
     "Oui. Chaque lot porte sa DLC ou sa DDM ; la logique FEFO (First Expired, First Out) impose de sortir en priorité les lots les plus proches de la péremption, ce qui réduit les pertes et sécurise vos expéditions."),
    ("La traçabilité couvre-t-elle l'étiquetage INCO et les allergènes ?", "Étiquetage, INCO, allergènes",
     "Oui. Les étiquettes reprennent automatiquement les mentions INCO (allergènes en gras, valeurs nutritionnelles, estampille sanitaire) à partir des recettes et des lots, sans ressaisie et sans risque d'erreur."),
    ("Est-ce adapté aux audits IFS, BRC et au Paquet Hygiène ?", "Audits, IFS, BRC",
     "L'historique complet des lots, des contrôles et des non-conformités est conservé et exportable, ce qui accélère les audits IFS et BRC et prouve votre conformité au Paquet Hygiène."),
    ("Quelle différence entre traçabilité ascendante et descendante ?", "Ascendante, descendante, différence",
     "La traçabilité ascendante remonte d'un produit fini vers ses matières premières et fournisseurs ; la descendante part d'un lot de matière pour retrouver tous les produits et clients concernés. Hello Harel couvre les deux sens, condition d'un rappel efficace."),
]

def faq(src_raw):
    """Rebuild the FAQ from the template's real drawer structure (cards + overlay
    + 6 panels + JSON-LD) so the page's global drawer JS keeps working."""
    import re, json
    a = src_raw.find('<section class="faq-section"')
    b = src_raw.find('<section class="reviews-section"')
    span = src_raw[a:b]

    # section-header labels
    span = re.sub(r'(<p class="overline">)[^<]*(</p>)', r'\1FAQ Traçabilité\2', span, count=1)
    span = re.sub(r'(<section class="faq-section"[^>]*>.*?<h2>).*?(</h2>)',
                  r'\1Les réponses à vos questions sur la traçabilité alimentaire\2', span, count=1, flags=re.S)

    # Replace the 6 card questions + meta, positionally.
    qi = [0]
    def repl_card(m):
        i = qi[0]; qi[0] += 1
        q, meta, _ = FAQ_QA[i]
        return (f'<span class="faq-card-question">{q}</span>\n'
                f'                    <span class="faq-card-meta">{meta}</span>')
    span = re.sub(r'<span class="faq-card-question">.*?</span>\s*<span class="faq-card-meta">.*?</span>',
                  repl_card, span, flags=re.S)

    # Replace the 6 panels (h3 + faq-drawer-content), positionally.
    pi = [0]
    def repl_panel(m):
        i = pi[0]; pi[0] += 1
        q, _, ans = FAQ_QA[i]
        return (f'{m.group(1)}<h3>{q}</h3>\n            '
                f'<div class="faq-drawer-content"><p>{ans}</p></div>')
    span = re.sub(r'(<div class="faq-drawer-panel"[^>]*>\s*)<h3>.*?</h3>\s*'
                  r'<div class="faq-drawer-content">.*?</div>',
                  repl_panel, span, flags=re.S)

    # Rebuild the JSON-LD to match.
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": ans}}
                         for q, _, ans in FAQ_QA]}
    span = re.sub(r'<script type="application/ld\+json">\s*\{.*?"FAQPage".*?\}\s*</script>',
                  '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
                  span, count=1, flags=re.S)
    return span

def span(c, cls_from, cls_to):
    a = c.find('<section class="%s"' % cls_from)
    b = c.find('<section class="%s"' % cls_to)
    if a < 0 or b < 0 or b <= a:
        raise SystemExit(f"span not found {cls_from}->{cls_to}")
    return a, b

TARGET_ID = 10968  # existing page to update (avoid creating a duplicate)

def main():
    live = "--live" in sys.argv
    src = w.get_raw("pages", SRC)["content"]["raw"]
    c = src

    # Replace FAQ first (largest span) then features then hero — back to front keeps offsets valid.
    a, b = span(c, "faq-section", "reviews-section"); c = c[:a] + faq(src) + c[b:]
    a, b = span(c, "features-section", "about-card-section"); c = c[:a] + FEATURES + c[b:]
    a, b = span(c, "hero-section", "logos-section"); c = c[:a] + HERO + c[b:]

    # Fix breadcrumb JSON-LD self-URL + label.
    c = c.replace("https://www.helloharel.com/agroalimentaire/charcutier/",
                  "https://www.helloharel.com/fonctionnalites/tracabilite-alimentaire/")
    c = re.sub(r'"name"\s*:\s*"(ERP )?Charcutier"', '"name": "Logiciel de traçabilité alimentaire"', c)

    # Sanity: drawer integrity (page JS needs matching cards/panels + overlay).
    checks = {
        "faqDrawerOverlay": c.count("faqDrawerOverlay"),
        "faq-drawer-panel": c.count('faq-drawer-panel"') + c.count("faq-drawer-panel "),
        "faq-card onclick": c.count("openFaqDrawer("),
        "residual charcutier": c.lower().count("charcutier"),
    }
    print("Assembled length:", len(c), "| checks:", checks)
    if not live:
        print("DRY-RUN — pass --live to update page", TARGET_ID)
        return
    res = w.update_content("pages", TARGET_ID, c, live=True)
    print("UPDATED id", TARGET_ID, "->", res.get("id") if isinstance(res, dict) else res)

if __name__ == "__main__":
    main()
