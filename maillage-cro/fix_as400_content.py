#!/usr/bin/env python3
"""
Readability/UX cleanup of the AS/400 article body (post 4283).

Fixes the real "rognage" (clipping) and spacing bugs seen on screen:
 1. Callouts: 5 conflicting blockquote rules + a decorative ::before quote
    glyph absolutely positioned ON TOP of the text. -> one clean callout
    style, quote glyph removed, consistent padding/margins.
 2. Emojis used as icons in the text (🔹×15, 🔔×3, 💡) -> removed (H2s keep
    their clean CSS bar marker; lists keep their <ul> bullets).
 3. Dated cartoon banner (Appel-a-Laction.png) -> removed (redundant with the
    new offer card, off-charter).

Corrective CSS is prepended (additive), content edits are surgical.
Idempotent. DRY-RUN by default; --live to apply.
"""
import sys, re
import wp_common as w

POST_ID = 4283
MARK = "hh-art-fix"

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
    '.hha-art figure,.hha-art img{margin:2.2rem 0 !important}'
    '</style>'
)


def main():
    live = "--live" in sys.argv
    c = w.get_raw("posts", POST_ID)["content"]["raw"]
    before = len(c)

    # 1. Drop previous corrective style (idempotent).
    c = re.sub(r'<style id="%s">.*?</style>' % MARK, "", c, flags=re.S)

    # 2. Remove emoji icons (with any trailing whitespace/nbsp).
    for e in ("🔹", "🔔", "💡"):
        c = re.sub(re.escape(e) + r"[  ]*", "", c)

    # 3. Remove the dated cartoon banner (figure wrapping Appel-a-Laction.png),
    #    and an immediately-preceding separator if present.
    c = re.sub(r'(<hr[^>]*wp-block-separator[^>]*/?>\s*)?<figure[^>]*>(?:(?!</figure>).)*?Appel-a-Laction(?:(?!</figure>).)*?</figure>',
               "", c, flags=re.S)

    # 4. Prepend corrective CSS.
    c = CSS + "\n" + c

    emojis_left = sum(c.count(e) for e in ("🔹", "🔔", "💡"))
    banner_left = c.count("Appel-a-Laction")
    print(f"len {before} -> {len(c)} | emojis left {emojis_left} | banner left {banner_left}")
    res = w.update_content("posts", POST_ID, c, live=live)
    print("LIVE" if live else "DRY-RUN", "done")


if __name__ == "__main__":
    main()
