#!/usr/bin/env python3
"""
Contact page (id 661) — clear the fixed 72px header so the CRO heading/form
no longer sits UNDER the sticky menu ("ne grignote pas le menu").

The theme's fixed header (.site-header position:fixed; .header-inner height:72px)
is out of flow; the original hero used padding-top:160px to clear it. After the
hero was removed for the CRO redesign, the slim .contact-heading only had
padding-top:1.4rem, so it hid behind the menu. This adds a proper top offset
(fixed-element-offset UX rule) on desktop + mobile, keeps the form above the
fold, and keeps the mobile form-first order.

DRY-RUN by default. Run live:
    export WP_USER="administration@remi-oravec.fr"
    export WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"
    python3 fix_contact_header_offset.py --live
"""
import sys
import wp_common as w

PAGE_ID = 661

OLD = (
    '<style id="cro-contact-fix">'
    '#hh-page .contact-section{padding-top:1rem !important;}'
    '#hh-page .contact-grid{align-items:start !important;}'
    '@media(max-width:900px){'
    '#hh-page .contact-grid{display:flex !important;flex-direction:column !important;}'
    '#hh-page .contact-form{order:-1 !important;}'
    '#hh-page .contact-info{order:2 !important;}}'
    '</style>'
)

# Adds the header offset to the FIRST content block (.contact-heading) so it
# clears the 72px fixed header + breathing room, on desktop and mobile.
NEW = (
    '<style id="cro-contact-fix">'
    '#hh-page .contact-heading{padding-top:calc(72px + 1.6rem) !important;'
    'padding-bottom:.4rem !important;}'
    '#hh-page .contact-section{padding-top:.5rem !important;}'
    '#hh-page .contact-grid{align-items:start !important;}'
    '@media(max-width:900px){'
    '#hh-page .contact-heading{padding-top:calc(66px + 1rem) !important;}'
    '#hh-page .contact-grid{display:flex !important;flex-direction:column !important;}'
    '#hh-page .contact-form{order:-1 !important;}'
    '#hh-page .contact-info{order:2 !important;}}'
    '</style>'
)


def main():
    live = "--live" in sys.argv
    page = w.get_raw("pages", PAGE_ID)
    content = page["content"]["raw"]

    if OLD not in content:
        # Fallback: locate the style block by id and replace whatever is inside.
        import re
        m = re.search(r'<style id="cro-contact-fix">.*?</style>', content, re.S)
        if not m:
            raise SystemExit("cro-contact-fix style block not found — inspect page 661 manually.")
        content = content[: m.start()] + NEW + content[m.end():]
        print("Replaced style block via regex fallback.")
    else:
        content = content.replace(OLD, NEW)
        print("Replaced style block via exact match.")

    res = w.update_content("pages", PAGE_ID, content, live=live)
    print("LIVE" if live else "DRY-RUN", "->", {k: res.get(k) for k in ("id", "dry_run", "new_len")} if isinstance(res, dict) else res)


if __name__ == "__main__":
    main()
