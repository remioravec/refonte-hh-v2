#!/usr/bin/env python3
"""
Site-wide UX/readability pass — applies the fixes validated on /blog/erp-as400/
to every post & page that contains the affected elements.

Applied (idempotent, additive):
 - Callouts: kill the overlapping ::before quote glyph, one clean blockquote
   style, consistent padding/margins (fixes the 'rognage').
 - Vertical rhythm: normalize p / h2 / h3 / ul / li / img / figure margins.
 - Infographic figures (.hha-fig): restore generous 4.5rem margin.
 - Mobile: FAQ drawer 540px -> 100% ; CookieYes banner width clamp.
 - Emoji-as-icons removed (🔹 🔔 💡).

Deliberately NOT applied site-wide: the dated banner removal (elsewhere it is
the article's only mid-content CTA) and the AS/400 offer band (page-specific).

Only writes items whose content actually changes. DRY-RUN by default.
    python3 apply_site_ux.py            # dry-run, prints scope
    python3 apply_site_ux.py --live     # apply
    python3 apply_site_ux.py --live --pages-only / --posts-only
"""
import sys, re, time
import wp_common as w

MARK = "hh-ux-fix"
EMOJIS = ("🔹", "🔔", "💡")

CSS = (
    f'<style id="{MARK}">'
    '.hha-art blockquote,#hh-page .hha-art blockquote{position:relative !important;'
    'border-left:4px solid #00B1F5 !important;background:#f0f9ff !important;'
    'padding:1.15rem 1.4rem !important;margin:2.2rem 0 !important;'
    'border-radius:0 12px 12px 0 !important;color:#334155 !important;'
    'font-style:normal !important;box-shadow:none !important;overflow:visible !important}'
    '.hha-art blockquote::before,#hh-page .hha-art blockquote::before{content:none !important;display:none !important}'
    '.hha-art blockquote p,#hh-page .hha-art blockquote p{margin:0 !important;padding-left:0 !important;line-height:1.75 !important}'
    '.hha-art blockquote p+p{margin-top:.6rem !important}'
    '.hha-art p{margin:0 0 1.4rem !important;line-height:1.8 !important}'
    '.hha-art h2{margin:3.2rem 0 1.2rem !important}'
    '.hha-art h3{margin:2.4rem 0 .8rem !important}'
    '.hha-art ul,.hha-art ol{margin:1.1rem 0 1.7rem !important}'
    '.hha-art li{margin:.55rem 0 !important;line-height:1.7 !important}'
    '.hha-art img{margin:2.2rem 0 !important}'
    '.hha-art figure{margin:2.6rem 0 !important}'
    '.hha-art figure.hha-fig,.hha-art .hha-fig{margin:4.5rem 0 !important}'
    '@media(max-width:600px){'
    '.faq-drawer{width:100% !important;max-width:100% !important}'
    '.cky-consent-container{width:calc(100% - 16px) !important;max-width:100% !important;left:8px !important;right:8px !important}'
    '}'
    '</style>'
)


def transform(raw):
    c = raw
    # Drop any prior corrective markers (idempotent; also supersedes hh-art-fix).
    c = re.sub(r'<style id="hh-art-fix">.*?</style>\s*', "", c, flags=re.S)
    c = re.sub(r'<style id="%s">.*?</style>\s*' % MARK, "", c, flags=re.S)
    # Remove emoji-as-icons.
    for e in EMOJIS:
        c = re.sub(re.escape(e) + r"[  ]*", "", c)
    # Inject corrective CSS only where a targeted element exists.
    has_target = any(t in c for t in ('<blockquote', 'faq-drawer', 'hha-fig', 'hha-art'))
    if has_target:
        c = CSS + "\n" + c
    return c


def run(kind, live):
    items = w.get_all(kind, fields="id,slug", per_page=100)
    changed, skipped, errors = [], 0, []
    for it in items:
        pid = it["id"]
        try:
            raw = w.get_raw(kind, pid)["content"]["raw"]
        except Exception as e:
            errors.append((pid, str(e)[:80])); continue
        new = transform(raw)
        if new == raw:
            skipped += 1; continue
        if live:
            try:
                w.update_content(kind, pid, new, live=True); time.sleep(0.15)
            except Exception as e:
                errors.append((pid, str(e)[:80])); continue
        changed.append(it["slug"])
    return changed, skipped, errors


def main():
    live = "--live" in sys.argv
    do_posts = "--pages-only" not in sys.argv
    do_pages = "--posts-only" not in sys.argv
    total_changed = 0
    for kind, go in (("posts", do_posts), ("pages", do_pages)):
        if not go:
            continue
        changed, skipped, errors = run(kind, live)
        total_changed += len(changed)
        print(f"[{kind}] {'APPLIED' if live else 'WOULD CHANGE'} {len(changed)} | unchanged {skipped} | errors {len(errors)}")
        for e in errors[:8]:
            print("   ERR", e)
    print(("LIVE" if live else "DRY-RUN"), "total changed", total_changed)


if __name__ == "__main__":
    main()
