#!/usr/bin/env python3
"""
Lot A — create /migration-as400/ : dedicated OFFER page (not a redirect).
Self-contained (clone metier chrome 2818): migration-audit hero + project
steps + data-recovery guarantees + AS/400 end-of-life RISK table + a dedicated
AUDIT FORM (FormSubmit.co, no JS dependency) + migration FAQ (real drawer).

Cannibalisation guard: targets "migration/remplacer AS400", NEVER "erp as400"
(that query stays on /blog/erp-as400/).

DRY by default; --live to create.
"""
import sys, re, json
import wp_common as w

SRC = 2818
PARENT = 0
SLUG = "migration-as400"
TITLE = "Migration AS/400 : audit gratuit & reprise de données garantie"
SELF = "https://www.helloharel.com/migration-as400/"

HERO = (
    '<section class="hero-section" style="background:linear-gradient(rgba(0,50,80,0.62),rgba(0,100,160,0.64)),'
    "url('https://www.helloharel.com/wp-content/uploads/2025/07/Logiciel-de-gestion-des-achats-3.png') "
    'center/cover no-repeat;">\n'
    '    <div class="container"><div class="hero-grid"><div class="hero-text">\n'
    '        <div class="hero-badge"><span class="dot"></span>Migration AS/400</div>\n'
    '        <h1 class="hero-title" style="color:#fff">Remplacez votre <span class="accent" style="color:#60a5fa">AS/400</span> sans perdre une donnée</h1>\n'
    '        <p class="hero-description">Audit de migration gratuit vers un ERP SaaS moderne : reprise de vos données '
    'garantie, déroulé de projet étape par étape, zéro rupture d\'exploitation. Pour les industriels agroalimentaires sur IBM iSeries en fin de vie.</p>\n'
    '        <div class="hero-ctas">\n'
    '            <a href="#audit" class="hero-cta-primary" style="background:#22C55E !important;border-color:#22C55E !important;color:#fff !important;">Demander mon audit gratuit</a>\n'
    '            <a href="#projet" class="hero-cta-secondary" style="color:#fff !important;border-color:#fff !important;">Voir le déroulé</a>\n'
    '        </div>\n'
    '        <p class="hero-cta-sub">Réponse sous 24 h · sans engagement · éditeur français.</p>\n'
    '    </div><div class="hero-image-spacer"></div></div></div>\n'
    '</section>\n'
)

def step(n, t, d):
    return (f'<div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px 18px">'
            f'<div style="width:34px;height:34px;border-radius:50%;background:#00B1F5;color:#fff;font-weight:800;'
            f'display:flex;align-items:center;justify-content:center;margin:0 0 10px">{n}</div>'
            f'<b style="display:block;color:#0f172a;margin:0 0 4px">{t}</b>'
            f'<p style="margin:0;color:#64748b;font-size:.9rem;line-height:1.5">{d}</p></div>')

def guar(t):
    return ('<li style="display:flex;gap:.6rem;align-items:flex-start;color:#0f172a;font-weight:600;margin:0 0 .7rem">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="#00B1F5" stroke-width="2.6" style="width:22px;height:22px;flex:0 0 22px">'
            '<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg><span>' + t + '</span></li>')

RISKS = [
    ("Matériel &amp; OS en fin de support", "Pannes sans pièces, failles de sécurité non corrigées."),
    ("Compétences RPG rares", "Dépendance à quelques experts, maintenance de plus en plus chère."),
    ("Pas de mobilité ni de cloud", "Accès local uniquement — ni télétravail, ni multi-sites."),
    ("Intégrations limitées", "Difficile de brancher e-commerce, EDI, outils modernes."),
    ("Coûts qui grimpent", "Licences et maintenance en hausse pour une valeur qui baisse."),
]

FORM = (
    '<section id="audit" style="background:linear-gradient(135deg,#0090c8,#00B1F5);padding:clamp(40px,6vw,64px) 0">'
    '<div class="container" style="max-width:760px">'
    '<div style="background:#fff;border-radius:20px;box-shadow:0 20px 48px rgba(2,32,54,.22);padding:clamp(24px,4vw,40px)">'
    '<h2 style="margin:0 0 .4rem;color:#0f172a;font-size:clamp(1.4rem,3vw,1.9rem)">Demandez votre audit de migration gratuit</h2>'
    '<p style="margin:0 0 1.4rem;color:#475569">On analyse votre AS/400 actuel et on vous remet un plan de migration chiffré. Réponse sous 24 h.</p>'
    '<form action="https://formsubmit.co/administration@remi-oravec.fr" method="POST" '
    'style="display:grid;gap:12px">'
    '<input type="hidden" name="_subject" value="Demande d\'audit de migration AS/400 — HelloHarel.com">'
    '<input type="hidden" name="_cc" value="timothy.jollivet@harelsystems.com">'
    '<input type="hidden" name="_captcha" value="false">'
    '<input type="hidden" name="_template" value="table">'
    '<input type="hidden" name="_next" value="https://www.helloharel.com/migration-as400/?envoye=1">'
    '<input type="text" name="_honey" style="display:none">'
    '<input name="Nom" required placeholder="Nom et prénom *" style="padding:13px 15px;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem">'
    '<input type="email" name="Email" required placeholder="Email professionnel *" style="padding:13px 15px;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem">'
    '<input name="Entreprise" placeholder="Entreprise" style="padding:13px 15px;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem">'
    '<input name="AS400 actuel" placeholder="Votre AS/400 actuel (éditeur, ancienneté)" style="padding:13px 15px;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem">'
    '<input name="Nombre d utilisateurs" placeholder="Nombre d\'utilisateurs" style="padding:13px 15px;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem">'
    '<textarea name="Message" rows="3" placeholder="Votre contexte, votre échéance…" style="padding:13px 15px;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem;resize:vertical"></textarea>'
    '<button type="submit" style="background:#22C55E;color:#fff;font-weight:800;border:0;padding:15px;border-radius:12px;font-size:1.05rem;cursor:pointer">Demander mon audit de migration gratuit →</button>'
    '<p style="margin:.3rem 0 0;color:#94a3b8;font-size:.82rem;text-align:center">Sans engagement · vos données ne sont jamais revendues.</p>'
    '</form></div></div></section>\n'
)

def features():
    steps = "".join([
        step(1, "Audit de l'existant", "Cartographie de vos données AS/400, flux et éditions."),
        step(2, "Reprise des données", "Articles, tiers, stocks, historiques — contrôlés et validés."),
        step(3, "Paramétrage métier", "Configuration sur votre process agroalimentaire."),
        step(4, "Tests &amp; formation", "Jeux d'essais et montée en compétence des équipes."),
        step(5, "Bascule accompagnée", "Mise en production progressive, sans arrêt d'activité."),
    ])
    risk_rows = "".join(
        f'<tr><td style="padding:11px 13px;border-bottom:1px solid #e5e7eb;font-weight:700;color:#0f172a">{r}</td>'
        f'<td style="padding:11px 13px;border-bottom:1px solid #e5e7eb;color:#475569">{c}</td></tr>'
        for r, c in RISKS)
    return (
        '<section class="features-section" id="projet">\n<div class="container">\n'
        '<div class="section-header"><p class="overline">Migration AS/400</p>\n'
        '<h2>Votre migration, étape par étape</h2>\n'
        '<p>Un déroulé cadré, des garanties écrites, zéro rupture d\'exploitation.</p></div>\n'
        '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:0 0 2.4rem">' + steps + '</div>\n'
        '<style>@media(max-width:900px){#projet [style*="repeat(5"]{grid-template-columns:1fr 1fr !important}}</style>'
        # guarantees + risk table, two columns
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start">'
        '<div><h3 style="margin:0 0 1rem;color:#0f172a">Nos garanties de reprise</h3><ul style="list-style:none;padding:0;margin:0">'
        + guar("Reprise de vos données historiques garantie") + guar("Sauvegarde et réversibilité avant bascule")
        + guar("Un chef de projet dédié, éditeur français") + guar("Traçabilité, DLC et facturation intégrées")
        + '</ul></div>'
        '<div><h3 style="margin:0 0 1rem;color:#0f172a">Les risques d\'un AS/400 en fin de vie</h3>'
        '<div style="overflow-x:auto;border:1px solid #e5e7eb;border-radius:14px"><table style="border-collapse:collapse;width:100%">'
        '<thead><tr><th style="padding:11px 13px;text-align:left;background:#f1f5f9;color:#475569;font-size:.72rem;text-transform:uppercase">Risque</th>'
        '<th style="padding:11px 13px;text-align:left;background:#f1f5f9;color:#475569;font-size:.72rem;text-transform:uppercase">Conséquence</th></tr></thead>'
        '<tbody>' + risk_rows + '</tbody></table></div></div>'
        '</div>\n'
        '<style>@media(max-width:900px){#projet [style*="1fr 1fr"]{grid-template-columns:1fr !important}}</style>'
        '</div>\n</section>\n' + FORM
    )

FAQ_QA = [
    ("Combien de temps dure une migration depuis un AS/400 ?", "Combien, temps, migration",
     "Selon la taille et la complexité, comptez de quelques semaines à quelques mois. L'audit gratuit donne un calendrier précis dès le départ, avec une bascule progressive pour ne jamais arrêter votre activité."),
    ("Est-ce que je récupère toutes mes données AS/400 ?", "Récupère, données",
     "Oui : la reprise des articles, tiers, stocks et historiques est garantie et contrôlée avant la bascule. Une sauvegarde complète et la réversibilité sont assurées."),
    ("Faut-il tout arrêter pendant la migration ?", "Arrêter, exploitation",
     "Non. La bascule est progressive et accompagnée, sans rupture d'exploitation : vous continuez à produire pendant le projet."),
    ("Combien coûte une migration AS/400 vers un ERP SaaS ?", "Combien, coûte, prix",
     "L'audit est gratuit et chiffre le projet. L'ERP SaaS Hello Harel reste accessible (abonnement mensuel), sans le lourd investissement initial d'un ERP d'ETI."),
    ("Pourquoi quitter un AS/400 qui fonctionne encore ?", "Pourquoi, quitter",
     "Matériel et OS en fin de support, compétences RPG rares, pas de mobilité ni de cloud, intégrations limitées et coûts croissants : le risque augmente chaque année. Migrer sécurise votre exploitation et ouvre le web, l'EDI et le multi-sites."),
    ("Vous accompagnez la formation des équipes ?", "Formation, équipes",
     "Oui : tests, jeux d'essais et formation sont intégrés au déroulé, avec un chef de projet dédié jusqu'à la mise en production."),
]

def faq(src_raw):
    a = src_raw.find('<section class="faq-section"'); b = src_raw.find('<section class="reviews-section"')
    span = src_raw[a:b]
    span = re.sub(r'(<p class="overline">)[^<]*(</p>)', r'\1FAQ Migration AS/400\2', span, count=1)
    span = re.sub(r'(<section class="faq-section"[^>]*>.*?<h2>).*?(</h2>)',
                  r'\1Vos questions sur la migration AS/400\2', span, count=1, flags=re.S)
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
    c = c.replace("https://www.helloharel.com/agroalimentaire/charcutier/", SELF)
    c = re.sub(r'"name"\s*:\s*"(ERP )?Charcutier"', '"name": "Migration AS/400"', c)
    checks = {"faqDrawerOverlay": c.count("faqDrawerOverlay"), "panels": c.count('faq-drawer-panel"'),
              "form": c.count('formsubmit.co'), "charcutier": c.lower().count("charcutier"), "erp as400 in H1": 'erp as400' in c.lower().split('</h1>')[0].lower()}
    print("Assembled", len(c), "| checks", checks)
    if not live:
        print("DRY-RUN"); return
    res = w.api("pages", method="POST", data={"slug": SLUG, "title": TITLE, "content": c,
                "status": "publish", "parent": PARENT, "template": "elementor_canvas"})
    print("CREATED id", res.get("id"), res.get("link"))

if __name__ == "__main__":
    main()
