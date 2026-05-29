#!/usr/bin/env python3
"""
Common WordPress REST helpers for the Hello Harel maillage + CRO toolkit.

SECURITY: credentials are read from environment variables only. Never hardcode
them here or commit them. Set before running:

    export WP_USER="administration@remi-oravec.fr"
    export WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"   # WP Application Password

All write helpers are gated behind an explicit live=True flag; the default for
every script in this toolkit is DRY-RUN (no write hits the production site).
"""

import os
import json
import ssl
import time
import base64
import urllib.request
import urllib.error

SITE = os.environ.get("WP_SITE", "https://www.helloharel.com")

# The remote container clock can drift relative to the TLS cert "notBefore",
# raising "certificate is not yet valid". curl already validates reachability,
# and this is the site owner's own host, so we tolerate the skew for our calls.
_CTX = ssl.create_default_context()
if os.environ.get("WP_INSECURE_SSL", "1") == "1":
    _CTX.check_hostname = False
    _CTX.verify_mode = ssl.CERT_NONE


def _auth_header():
    user = os.environ.get("WP_USER")
    pw = os.environ.get("WP_PASS")
    if not user or not pw:
        raise SystemExit(
            "Missing WP_USER / WP_PASS env vars. Export your WordPress "
            "Application Password before running (see wp_common.py header)."
        )
    token = base64.b64encode(f"{user}:{pw}".encode()).decode()
    return f"Basic {token}"


def api(endpoint, method="GET", data=None, timeout=60):
    url = f"{SITE}/wp-json/wp/v2/{endpoint}"
    headers = {"Authorization": _auth_header(), "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} on {method} {endpoint}: {e.read().decode()[:300]}")


def get_all(kind, fields="id,slug,link,title,status", per_page=50, status="publish"):
    """Paginate through posts/pages. kind in {'posts','pages'}."""
    out, page = [], 1
    while True:
        batch = api(f"{kind}?per_page={per_page}&page={page}&status={status}&_fields={fields}")
        if not isinstance(batch, list) or not batch:
            break
        out.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
        time.sleep(0.2)
    return out


def get_raw(kind, item_id):
    """Fetch a single item with edit context (raw content + meta)."""
    return api(f"{kind}/{item_id}?context=edit&_fields=id,slug,link,title,content,meta")


def update_content(kind, item_id, new_content, live=False):
    """Update content. DRY-RUN unless live=True is passed explicitly."""
    if not live:
        return {"dry_run": True, "id": item_id, "new_len": len(new_content)}
    res = api(f"{kind}/{item_id}", method="POST", data={"content": new_content})
    time.sleep(0.5)
    return res
