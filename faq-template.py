#!/usr/bin/env python3
"""
Generates FAQ drawer HTML, JS, CSS and JSON-LD schema for Hello Harel pages.
Injects the FAQ content into WordPress pages via REST API.
"""

import json
import re
import urllib.request
import base64
import time

SITE = "https://www.helloharel.com"
USER = "administration@remi-oravec.fr"
PASS = "I9xb KzTA qqPR Altw YquG hNoI"
AUTH = base64.b64encode(f"{USER}:{PASS}".encode()).decode()


def api_get(endpoint):
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/{endpoint}",
        headers={"Authorization": f"Basic {AUTH}"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def api_post(endpoint, data):
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/{endpoint}",
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def convert_links(text):
    """Convert [LINK:/path/]anchor[/LINK] to real HTML links."""
    return re.sub(
        r'\[LINK:(/[^\]]+)\](.*?)\[/LINK\]',
        r'<a href="\1" style="color:#00B1F5;font-weight:600;text-decoration:underline;">\2</a>',
        text
    )


def generate_faq_cards_html(questions):
    """Generate FAQ card grid HTML."""
    icons = [
        '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.656-1.79 3-4 3-.197 0-.391-.007-.58-.021M12 17h.01"/></svg>',
        '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>',
        '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
        '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>',
        '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
        '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>',
    ]
    arrow = '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>'

    cards = []
    for i, faq in enumerate(questions):
        q = faq['q']
        # Generate a short meta from the question keywords
        meta_words = [w for w in q.split() if len(w) > 4][:3]
        meta = ', '.join(meta_words) if meta_words else ''
        icon = icons[i % len(icons)]

        cards.append(f'''            <div class="faq-card" onclick="openFaqDrawer({i})">
                <div class="faq-card-inner">
                    <div class="faq-card-emoji">{icon}</div>
                    <span class="faq-card-question">{q}</span>
                    <span class="faq-card-meta">{meta}</span>
                </div>
                <div class="faq-card-arrow">{arrow}</div>
            </div>''')

    return '\n'.join(cards)


def generate_drawer_html(questions):
    """Generate the FAQ drawer overlay with all answers."""
    panels = []
    for i, faq in enumerate(questions):
        answer = convert_links(faq['a'])
        panels.append(f'''        <div class="faq-drawer-panel" data-faq="{i}" style="display:none">
            <h3>{faq['q']}</h3>
            <div class="faq-drawer-content">{answer}</div>
        </div>''')

    return f'''<div class="faq-drawer-overlay" id="faqDrawerOverlay" style="display:none">
    <div class="faq-drawer">
        <div class="faq-drawer-header">
            <button class="faq-drawer-close" onclick="closeFaqDrawer()" aria-label="Fermer"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg></button>
            <div class="faq-drawer-nav">
                <button class="faq-drawer-prev" onclick="navFaqDrawer(-1)"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button>
                <span class="faq-drawer-counter" id="faqDrawerCounter">1/{len(questions)}</span>
                <button class="faq-drawer-next" onclick="navFaqDrawer(1)"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button>
            </div>
        </div>
        <div class="faq-drawer-body" id="faqDrawerBody">
{chr(10).join(panels)}
        </div>
        <div class="faq-drawer-footer">
            <a href="/contact/" class="faq-drawer-cta">Une question ? Contactez-nous</a>
        </div>
    </div>
</div>'''


def generate_drawer_js(num_questions):
    """Generate JS for the FAQ drawer."""
    return f'''
var currentFaq = 0;
var totalFaqs = {num_questions};
function openFaqDrawer(idx) {{
    currentFaq = idx;
    var overlay = document.getElementById('faqDrawerOverlay');
    overlay.classList.remove('closing');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    showFaqPanel(idx);
}}
function closeFaqDrawer() {{
    var overlay = document.getElementById('faqDrawerOverlay');
    overlay.classList.add('closing');
    overlay.classList.remove('open');
    setTimeout(function() {{
        overlay.classList.remove('closing');
        document.body.style.overflow = '';
    }}, 250);
}}
function navFaqDrawer(dir) {{
    currentFaq = (currentFaq + dir + totalFaqs) % totalFaqs;
    showFaqPanel(currentFaq);
}}
function showFaqPanel(idx) {{
    var panels = document.querySelectorAll('.faq-drawer-panel');
    panels.forEach(function(p) {{ p.style.display = 'none'; }});
    panels[idx].style.display = 'block';
    document.getElementById('faqDrawerCounter').textContent = (idx + 1) + '/' + totalFaqs;
}}
document.getElementById('faqDrawerOverlay').addEventListener('click', function(e) {{
    if (e.target === this) closeFaqDrawer();
}});
document.addEventListener('keydown', function(e) {{
    var overlay = document.getElementById('faqDrawerOverlay');
    if (overlay.classList.contains('open')) {{
        if (e.key === 'Escape') closeFaqDrawer();
        if (e.key === 'ArrowRight') navFaqDrawer(1);
        if (e.key === 'ArrowLeft') navFaqDrawer(-1);
    }}
}});
'''


def generate_drawer_css():
    """Generate CSS for the FAQ drawer overlay."""
    return """
/* ====== FAQ DRAWER OVERLAY ====== */
@keyframes faqOverlayIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes faqOverlayOut {
  from { opacity: 1; }
  to { opacity: 0; }
}
@keyframes faqDrawerIn {
  from { opacity: 0; transform: translateY(30px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes faqDrawerOut {
  from { opacity: 1; transform: translateY(0) scale(1); }
  to { opacity: 0; transform: translateY(30px) scale(0.96); }
}
.faq-drawer-overlay {
  position: fixed !important; top: 0 !important; left: 0 !important;
  width: 100% !important; height: 100% !important;
  background: rgba(0,20,40,0.55) !important; backdrop-filter: blur(6px) !important;
  -webkit-backdrop-filter: blur(6px) !important;
  z-index: 200000 !important; display: none !important;
  align-items: center !important; justify-content: center !important;
}
.faq-drawer-overlay.open {
  display: flex !important;
  animation: faqOverlayIn 0.3s ease-out !important;
}
.faq-drawer-overlay.closing {
  display: flex !important;
  animation: faqOverlayOut 0.25s ease-in forwards !important;
}
.faq-drawer {
  background: #fff !important; border-radius: 20px !important;
  width: 90% !important; max-width: 700px !important; max-height: 85vh !important;
  display: flex !important; flex-direction: column !important;
  box-shadow: 0 25px 60px rgba(0,0,0,0.25), 0 0 0 1px rgba(0,0,0,0.05) !important;
  overflow: hidden !important;
  animation: faqDrawerIn 0.35s cubic-bezier(0.16,1,0.3,1) !important;
}
.faq-drawer-overlay.closing .faq-drawer {
  animation: faqDrawerOut 0.25s ease-in forwards !important;
}

/* ---- Header ---- */
.faq-drawer-header {
  display: flex !important; justify-content: space-between !important;
  align-items: center !important; padding: 1rem 1.5rem !important;
  border-bottom: 1px solid #f1f5f9 !important;
  background: #fafbfc !important;
}
.faq-drawer-close {
  display: flex !important; align-items: center !important; justify-content: center !important;
  width: 36px !important; height: 36px !important;
  background: #f1f5f9 !important; border: none !important;
  border-radius: 10px !important; cursor: pointer !important;
  color: #64748b !important; font-size: 1.35rem !important;
  line-height: 1 !important; transition: all 0.2s ease !important;
}
.faq-drawer-close:hover {
  background: #e2e8f0 !important; color: #0f172a !important;
  transform: scale(1.05) !important;
}
.faq-drawer-close svg {
  width: 18px !important; height: 18px !important;
  color: #64748b !important; stroke: #64748b !important;
  fill: none !important; flex-shrink: 0 !important;
}
.faq-drawer-close:hover svg {
  color: #0f172a !important; stroke: #0f172a !important;
}
.faq-drawer-nav {
  display: flex !important; align-items: center !important; gap: 0.5rem !important;
}
.faq-drawer-prev, .faq-drawer-next {
  background: #f1f5f9 !important; border: none !important;
  border-radius: 10px !important; width: 36px !important; height: 36px !important;
  display: flex !important; align-items: center !important; justify-content: center !important;
  cursor: pointer !important; transition: all 0.2s ease !important;
  color: #64748b !important;
}
.faq-drawer-prev:hover, .faq-drawer-next:hover {
  background: #e2e8f0 !important; color: #0f172a !important;
  transform: scale(1.05) !important;
}
.faq-drawer-prev svg, .faq-drawer-next svg {
  width: 16px !important; height: 16px !important;
  color: #64748b !important; stroke: #64748b !important;
  fill: none !important; flex-shrink: 0 !important;
}
.faq-drawer-prev:hover svg, .faq-drawer-next:hover svg {
  color: #0f172a !important; stroke: #0f172a !important;
}
.faq-drawer-counter {
  font-size: 0.8rem !important; color: #94a3b8 !important;
  font-weight: 600 !important; min-width: 2.5rem !important;
  text-align: center !important; letter-spacing: 0.025em !important;
}

/* ---- Body ---- */
.faq-drawer-body {
  flex: 1 !important; overflow-y: auto !important;
  padding: 2rem 2.25rem !important;
  scroll-behavior: smooth !important;
}
.faq-drawer-body::-webkit-scrollbar { width: 5px !important; }
.faq-drawer-body::-webkit-scrollbar-track { background: transparent !important; }
.faq-drawer-body::-webkit-scrollbar-thumb { background: #e2e8f0 !important; border-radius: 10px !important; }
.faq-drawer-body::-webkit-scrollbar-thumb:hover { background: #cbd5e1 !important; }

/* ---- Panel content ---- */
.faq-drawer-panel {
  animation: faqPanelIn 0.3s ease-out !important;
}
@keyframes faqPanelIn {
  from { opacity: 0; transform: translateX(12px); }
  to { opacity: 1; transform: translateX(0); }
}
.faq-drawer-panel h3 {
  font-size: 1.3rem !important; color: #0f172a !important;
  margin: 0 0 1.5rem 0 !important; font-weight: 800 !important;
  line-height: 1.4 !important; letter-spacing: -0.01em !important;
  padding-bottom: 1rem !important;
  border-bottom: 2px solid #f1f5f9 !important;
}
.faq-drawer-content {
  font-size: 0.95rem !important;
}
.faq-drawer-content p {
  margin: 0 0 1rem 0 !important; line-height: 1.75 !important;
  color: #475569 !important; font-size: 0.95rem !important;
}
.faq-drawer-content strong {
  color: #0f172a !important; font-weight: 700 !important;
}
.faq-drawer-content ul {
  padding-left: 0 !important; margin: 0 0 1.25rem 0 !important;
  list-style: none !important;
}
.faq-drawer-content li {
  margin-bottom: 0.625rem !important; line-height: 1.65 !important;
  color: #475569 !important; font-size: 0.95rem !important;
  padding-left: 1.5rem !important; position: relative !important;
}
.faq-drawer-content li::before {
  content: '' !important; position: absolute !important;
  left: 0 !important; top: 0.55em !important;
  width: 6px !important; height: 6px !important;
  border-radius: 50% !important; background: #00B1F5 !important;
}
.faq-drawer-content a {
  color: #00B1F5 !important; font-weight: 600 !important;
  text-decoration: none !important;
  border-bottom: 1px solid transparent !important;
  transition: border-color 0.2s !important;
}
.faq-drawer-content a:hover {
  border-bottom-color: #00B1F5 !important;
}

/* ---- Footer ---- */
.faq-drawer-footer {
  padding: 1rem 1.5rem !important;
  border-top: 1px solid #f1f5f9 !important;
  text-align: center !important; background: #fafbfc !important;
}
.faq-drawer-cta {
  display: inline-block !important; background: linear-gradient(135deg, #22C55E, #16a34a) !important;
  color: #fff !important; padding: 0.7rem 1.75rem !important;
  border-radius: 10px !important; font-weight: 700 !important;
  text-decoration: none !important; font-size: 0.9rem !important;
  transition: transform 0.2s, box-shadow 0.2s !important;
  box-shadow: 0 2px 8px rgba(34,197,94,0.25) !important;
}
.faq-drawer-cta:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(34,197,94,0.35) !important;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .faq-drawer {
    width: 100% !important; max-width: 100% !important;
    max-height: 100vh !important; height: 100% !important;
    border-radius: 0 !important;
  }
  .faq-drawer-body { padding: 1.5rem !important; }
  .faq-drawer-panel h3 { font-size: 1.15rem !important; }
}
"""


def generate_faq_schema(questions, page_url):
    """Generate FAQ JSON-LD schema."""
    items = []
    for faq in questions:
        # Strip HTML from answer for schema
        answer_text = re.sub(r'<[^>]+>', '', convert_links(faq['a'])).strip()
        answer_text = re.sub(r'\s+', ' ', answer_text)
        items.append({
            "@type": "Question",
            "name": faq['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer_text
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }

    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'


def inject_faq(slug, page_id, title, subtitle, description, questions):
    """Inject complete FAQ section into a WordPress page."""
    print(f"\n  Processing {slug}...")

    full = api_get(f"pages/{page_id}?context=edit&_fields=id,content")
    raw = full.get('content', {}).get('raw', '')

    # Find and replace existing FAQ section
    style_end_pos = raw.rfind('</style>')
    html_part = raw[style_end_pos:]

    if 'faq-section' in html_part:
        faq_start = html_part.index('faq-section')
        faq_start = html_part.rfind('<section', 0, faq_start)
        faq_end = html_part.index('</section>', faq_start) + len('</section>')
        old_faq = html_part[faq_start:faq_end]
    else:
        old_faq = None

    # Clean up any existing drawer overlays (from previous runs)
    while 'faq-drawer-overlay' in raw[raw.rfind('</style>'):]:
        html_after = raw[raw.rfind('</style>'):]
        ov_pos = html_after.index('faq-drawer-overlay')
        ov_div = html_after.rfind('<div', 0, ov_pos)
        abs_start = raw.rfind('</style>') + ov_div
        # Track div depth to find end
        depth, pos = 0, abs_start
        end = None
        while pos < len(raw):
            if raw[pos:pos+4] == '<div':
                depth += 1
                pos = raw.index('>', pos) + 1
            elif raw[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end = pos + 6
                    break
                pos += 6
            else:
                pos += 1
        if end:
            raw = raw[:abs_start] + raw[end:]
            print(f"    Cleaned old drawer overlay")
        else:
            break
    # Clean up old FAQ JSON-LD schemas
    raw = re.sub(
        r'\s*<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"FAQPage".*?</script>',
        '', raw, flags=re.DOTALL
    )

    # Build new FAQ section
    cards_html = generate_faq_cards_html(questions)
    drawer_html = generate_drawer_html(questions)
    faq_schema = generate_faq_schema(questions, f"{SITE}/{slug}/")

    new_faq = f'''<section class="faq-section">
    <div class="container">
        <div class="section-header">
            <p class="overline">{subtitle}</p>
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        <div class="faq-cards-grid">
{cards_html}
        </div>
    </div>
</section>

{drawer_html}

{faq_schema}'''

    # Replace or inject
    if old_faq:
        new_raw = raw.replace(old_faq, new_faq)
        print(f"    Replaced existing FAQ section")
    else:
        # Insert before the CTA banner or footer
        if 'cta-banner' in html_part:
            insert_before = '<section class="cta-banner"'
            insert_pos = raw.index(insert_before)
            new_raw = raw[:insert_pos] + new_faq + '\n\n' + raw[insert_pos:]
        else:
            # Insert before footer
            insert_pos = raw.index('<footer>')
            new_raw = raw[:insert_pos] + new_faq + '\n\n' + raw[insert_pos:]
        print(f"    Injected new FAQ section")

    # Add drawer CSS if not present
    if 'faq-drawer-overlay' not in raw:
        style_end = new_raw.index('</style>')
        new_raw = new_raw[:style_end] + generate_drawer_css() + '\n' + new_raw[style_end:]
        print(f"    Added drawer CSS")

    # Add drawer JS if not present
    if 'openFaqDrawer' not in new_raw or 'showFaqPanel' not in new_raw:
        # Find the last script or add a new one
        last_script = new_raw.rfind('</script>')
        js = generate_drawer_js(len(questions))
        new_raw = new_raw[:last_script] + '\n' + js + '\n' + new_raw[last_script:]
        print(f"    Added drawer JS")

    result = api_post(f"pages/{page_id}", {"content": new_raw})
    print(f"    Updated (ID: {result['id']}, +{len(new_raw)-len(raw)} chars)")
    return True


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 faq-template.py <faq-data.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        faq_data = json.load(f)

    # Get all page IDs
    all_pages = api_get("pages?per_page=100&_fields=id,slug")
    slug_to_id = {p['slug']: p['id'] for p in all_pages}

    # Page metadata
    PAGE_META = {
        "charcutier": ("Les reponses a vos questions metier", "FAQ Charcutier", "Maitrisez votre tracabilite et vos rendements."),
        "maraicher": ("Les reponses a vos questions metier", "FAQ Maraicher", "Gerez le poids variable et la saisonnalite."),
        "traiteur": ("Les reponses a vos questions metier", "FAQ Traiteur", "Pilotez vos evenements et votre production."),
        "boulanger": ("Les reponses a vos questions metier", "FAQ Boulangerie", "Calculez vos couts et planifiez vos fournees."),
        "industrie-laitiere": ("Les reponses a vos questions metier", "FAQ Industrie Laitiere", "Gerez la collecte, la maturation et la chaine du froid."),
        "plats-cuisines-industriels": ("Les reponses a vos questions metier", "FAQ Plats Cuisines", "Maitrisez vos recettes et la conformite INCO."),
        "agroalimentaire": ("Les reponses a vos questions", "FAQ ERP Agroalimentaire", "Tout savoir sur l'ERP specialise pour l'agroalimentaire."),
        "crm": ("Les reponses a vos questions", "FAQ CRM", "Optimisez votre relation client B2B."),
        "facturation": ("Les reponses a vos questions", "FAQ Facturation", "Automatisez et securisez votre facturation."),
        "vente": ("Les reponses a vos questions", "FAQ Gestion Commerciale", "Accelerez vos ventes et devis."),
        "gestion-de-stock": ("Les reponses a vos questions", "FAQ Gestion de Stock", "Maitrisez vos stocks en temps reel."),
        "fabrication": ("Les reponses a vos questions", "FAQ Fabrication", "Pilotez votre production agroalimentaire."),
        "logistique": ("Les reponses a vos questions", "FAQ Logistique", "Optimisez vos tournees et expeditions."),
        "achat": ("Les reponses a vos questions", "FAQ Achats", "Maitrisez vos approvisionnements."),
        "import-export": ("Les reponses a vos questions", "FAQ Import-Export", "Gerez vos echanges internationaux."),
    }

    total = 0
    for slug, questions_data in faq_data.items():
        page_id = slug_to_id.get(slug)
        if not page_id:
            print(f"  SKIP: {slug} not found")
            continue

        questions = questions_data.get('questions', [])
        if not questions:
            print(f"  SKIP: {slug} no questions")
            continue

        meta = PAGE_META.get(slug, ("FAQ", f"FAQ {slug.title()}", ""))
        title, subtitle, desc = meta

        try:
            inject_faq(slug, page_id, title, subtitle, desc, questions)
            total += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  ERROR on {slug}: {e}")

    print(f"\n{'='*50}")
    print(f"Total: {total} pages updated with FAQ content")
