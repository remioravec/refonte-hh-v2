#!/usr/bin/env python3
"""
Restore blog articles from a backup-live-<ts>/ folder created by apply.py.

Each *.before.json holds the FULL pre-change post object (content.raw + meta).
This re-PUTs the original content, undoing the maillage + CRO injection.

Usage:
  python3 restore.py backup-live-20260529-223414            # DRY-RUN (lists)
  python3 restore.py backup-live-20260529-223414 --live      # actually restore
  python3 restore.py backup-live-... --live --slugs roi-erp  # restore some
"""

import os
import sys
import glob
import json

import wp_common as wp


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    bdir = sys.argv[1]
    live = "--live" in sys.argv
    slugs = None
    if "--slugs" in sys.argv:
        i = sys.argv.index("--slugs")
        slugs = [s for s in sys.argv[i + 1:] if not s.startswith("--")]

    files = sorted(glob.glob(os.path.join(bdir, "post_*.before.json")))
    print(f"Mode: {'LIVE RESTORE' if live else 'DRY-RUN'} | backups: {len(files)}")
    for f in files:
        obj = json.load(open(f))
        slug = obj["slug"]
        if slugs and slug not in slugs:
            continue
        raw = (obj.get("content") or {}).get("raw", "")
        if not raw:
            print(f"  SKIP {slug}: empty backup")
            continue
        if live:
            wp.update_content("posts", obj["id"], raw, live=True)
            print(f"  RESTORED {slug} (id {obj['id']})")
        else:
            print(f"  would restore {slug} (id {obj['id']}, {len(raw)} chars)")


if __name__ == "__main__":
    main()
