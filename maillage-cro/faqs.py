#!/usr/bin/env python3
"""
Rebuild article FAQ sections in the EXACT home style: a card grid that opens a
drawer overlay (same markup/classes/JS as the home, whose CSS is already shipped
via HOME_CSS). Also emits FAQPage JSON-LD for SEO.

Public:
  rebuild(region_html, h2_id) -> (cards_section_html, drawer_and_js_html) | (None,None)
    region_html : the HTML between the FAQ <h2> and the next <h2> (article prose)
    h2_id       : id of the original FAQ <h2> (kept on the new section for the TOC)
"""

import re
import json
import html as _html

# Rotating card icons (home style).
ICONS = [
    'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
    'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6',
    'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
    'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.656-1.79 3-4 3-.197 0-.391-.007-.58-.021M12 17h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'M13 10V3L4 14h7v7l9-11h-7z',
]
TAGS = re.compile(r"<[^>]+>")
ARROW = ('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" '
         'stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>')


def _text(s):
    return re.sub(r"\s+", " ", _html.unescape(TAGS.sub(" ", s))).strip()


def _clean_answer(h):
    # keep inline tags/lists, drop wrappers/scripts/onclick, decode entities
    h = re.sub(r"<script\b.*?</script>", "", h, flags=re.I | re.S)
    h = re.sub(r"\son\w+=\"[^\"]*\"", "", h, flags=re.I)
    h = re.sub(r'</?div[^>]*>', "", h, flags=re.I)
    h = _html.unescape(h)
    return re.sub(r"\s+", " ", h).strip()


def parse(region):
    """Return list of (question, answer_html). Handles the 3 FAQ patterns seen."""
    qa = []
    # Pattern B: .faq-item with .faq-question / .faq-answer
    items = re.findall(r'<div class="faq-question"[^>]*>(.*?)</div>\s*'
                       r'<div class="faq-answer"[^>]*>(.*?)</div>', region, re.S)
    if items:
        for q, a in items:
            qt = _text(q)
            ah = _clean_answer(a)
            if qt and ah:
                qa.append((qt, ah))
        if qa:
            return qa
    # Pattern A: <p><strong>Q?</strong><br>A</p>
    for m in re.finditer(r'<p>\s*<strong>(.*?)</strong>\s*(?:<br\s*/?>)?(.*?)</p>', region, re.S):
        qt = _text(m.group(1))
        ah = _clean_answer(m.group(2))
        if qt and ah and ("?" in qt or len(qt) < 120):
            qa.append((qt, "<p>" + ah + "</p>"))
    if qa:
        return qa
    # Pattern C: <h3>Q</h3> ... up to next h3
    h3 = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', region, re.S))
    for i, m in enumerate(h3):
        qt = _text(m.group(1))
        end = h3[i + 1].start() if i + 1 < len(h3) else len(region)
        ah = _clean_answer(region[m.end():end])
        if qt and ah:
            qa.append((qt, ah))
    return qa


def build(qa, h2_id):
    if len(qa) < 2:
        return None, None
    qa = qa[:8]
    idattr = f' id="{h2_id}"' if h2_id else ""

    cards = []
    data = []
    for i, (q, a) in enumerate(qa):
        icon = ICONS[i % len(ICONS)]
        meta = _text(a)[:48].rstrip()
        if len(_text(a)) > 48:
            meta += "…"
        cards.append(
            f'<div class="faq-card" onclick="openFaqDrawer({i})"><div class="faq-card-inner">'
            f'<div class="faq-card-emoji"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">'
            f'<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="{icon}"/></svg></div>'
            f'<span class="faq-card-question">{_html.escape(q)}</span>'
            f'<span class="faq-card-meta">{_html.escape(meta)}</span></div>'
            f'<div class="faq-card-arrow">{ARROW}</div></div>')
        data.append({"title": q, "html": a})

    section = (
        f'<section class="faq-section"><div class="container"><div class="section-header">'
        f'<p class="overline">FAQ</p><h2{idattr}>Les réponses à vos questions</h2>'
        f'<p>Tout ce qu\'il faut savoir, en un coup d\'œil.</p></div>'
        f'<div class="faq-cards-grid">{"".join(cards)}</div></div></section>')

    faqdata = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": _text(a)}}
                                        for q, a in qa]}, ensure_ascii=False)

    drawer = (
        '<div class="faq-drawer-overlay" id="faqOverlay" onclick="closeFaqDrawer()"></div>'
        '<div class="faq-drawer" id="faqDrawer"><button class="faq-drawer-close" onclick="closeFaqDrawer()" aria-label="Fermer">'
        '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'
        '</button><div class="faq-drawer-content" id="faqDrawerContent"></div></div>'
        f'<script>var faqData={faqdata};'
        'function openFaqDrawer(i){var d=faqData[i];document.getElementById("faqDrawerContent").innerHTML="<h2>"+d.title+"</h2>"+d.html;'
        'document.getElementById("faqOverlay").classList.add("open");document.getElementById("faqDrawer").classList.add("open");document.body.style.overflow="hidden";}'
        'function closeFaqDrawer(){document.getElementById("faqOverlay").classList.remove("open");document.getElementById("faqDrawer").classList.remove("open");document.body.style.overflow="";}'
        'document.addEventListener("keydown",function(e){if(e.key==="Escape")closeFaqDrawer();});</script>'
        f'<script type="application/ld+json">{schema}</script>')

    return section, drawer
