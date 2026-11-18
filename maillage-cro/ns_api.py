#!/usr/bin/env python3
"""Appel REST sur un namespace arbitraire (code-snippets/v1, rankmath/v1, ...)."""
import json, urllib.request, urllib.error
import wp_common as w

def call(path, method="GET", data=None, timeout=90):
    url = f"{w.SITE}/wp-json/{path}"
    headers = {"Authorization": w._auth_header(), "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=w._CTX) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} on {method} {path}: {e.read().decode()[:500]}")
