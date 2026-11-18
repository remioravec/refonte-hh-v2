#!/usr/bin/env python3
"""
Maillage interne engine (DRY-RUN planner).

Reads inventory.json and produces, per blog article, a set of NEW contextual
internal links to add, following the reasonable-surfer cocon model:

  budget   = clamp(words/180, 5, 11) total contextual links per article
  UP links = cluster daughter (L2) then mother (L1), placed "top", anchor first
  LATERAL  = forward ring to cluster siblings (i -> i+1, i+2), placed "body"
  diversify= anchors from GSC-seeded pools, unused + non-cannibal (anchors.py)
  idempotent: never re-propose a target already linked contextually from a post

Outputs (committed, no secrets):
  maillage-cro/maillage-plan.json   machine-readable plan
  maillage-cro/MAILLAGE-DRY-RUN.md  human review report + global audits

No content is written to WordPress here. Apply step is a separate, gated script.
"""

import os
import json
import collections

import anchors
import clusters as C

HERE = os.path.dirname(__file__)
INV = os.path.join(HERE, "inventory.json")


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


import re as _re

def descriptive_anchor(target_item):
    """Craft a clean, natural lateral anchor from a sibling article's title.

    Title tags carry marketing suffixes separated by •/·/|/– — keep only the
    first, meaningful segment (e.g. "Alternative Cegid • ERP Agro • PME" ->
    "Alternative Cegid"). Title case is kept (acronyms like FIFO stay intact).
    """
    t = (target_item.get("title") or "").strip()
    t = _re.split(r"\s*[•·|–—]\s*|\s+-\s+", t)[0].strip()
    t = _re.sub(r"\s+", " ", t)
    if not t:
        t = C.slug_of(target_item["path"]).replace("-", " ").capitalize()
    return t


def main():
    data = json.load(open(INV))
    items = data["items"]
    by_path = {x["path"]: x for x in items}
    pick_anchor = anchors.build_selector(items)

    plan = {}
    posts = [x for x in items if x["kind"] == "post" and x["path"].startswith("/blog/")]

    # Stable ordering inside each cluster = the members[] order in clusters.py
    cluster_present = {
        name: [s for s in cfg["members"] if f"/blog/{s}/" in by_path]
        for name, cfg in C.CLUSTERS.items()
    }

    # Per-article state shared across passes
    state = {}
    for x in posts:
        existing = {l["path"] for l in x["internal_links"] if l["ctx"]}
        budget = clamp(x["words"] // 180, 5, 11)
        state[x["path"]] = {"targets": set(existing), "room": budget - len(existing),
                            "budget": budget, "existing_n": len(existing), "proposals": []}

    # ---- PASS 1: cocon up-links + lateral ring ----
    for x in posts:
        slug = C.slug_of(x["path"])
        primary, allc = C.cluster_of(slug)
        st = state[x["path"]]
        existing_ctx_targets = st["targets"]
        proposals = st["proposals"]

        if primary and st["room"] > 0:
            room = st["room"]
            up = C.CLUSTERS[primary]["up"]
            mother = C.MOTHER.get(primary)
            up_targets = list(dict.fromkeys(up + ([mother] if mother else [])))

            # 1) UP links (top zone) — strategic anchor first
            for tgt in up_targets:
                if room <= 0:
                    break
                if tgt not in by_path or tgt in existing_ctx_targets:
                    continue
                a = pick_anchor(tgt)
                if not a:
                    continue
                proposals.append({"target": tgt, "anchor": a, "zone": "top",
                                   "type": "up", "reason": f"cocon: {slug} → {primary} (montant)"})
                existing_ctx_targets.add(tgt)
                room -= 1

            # 2) LATERAL forward ring to siblings (body zone)
            ring = cluster_present[primary]
            if slug in ring and len(ring) > 1:
                i = ring.index(slug)
                for step in (1, 2, 3):
                    if room <= 0:
                        break
                    sib_slug = ring[(i + step) % len(ring)]
                    if sib_slug == slug:
                        continue
                    tgt = f"/blog/{sib_slug}/"
                    if tgt in existing_ctx_targets or tgt not in by_path:
                        continue
                    # A lateral anchor is derived from the TARGET's title, so it
                    # maps to exactly one target — multiple sources reusing it is
                    # fine (not cannibalization, which is one anchor -> many targets).
                    a = descriptive_anchor(by_path[tgt])
                    proposals.append({"target": tgt, "anchor": a, "zone": "body",
                                      "type": "lateral", "reason": f"anneau {primary}: maillage latéral"})
                    existing_ctx_targets.add(tgt)
                    room -= 1
            st["room"] = room

    # ---- PASS 2: demand balancing for starved money pages ----
    # Current distinct ctx anchors per money page (live) + anchors added in pass 1.
    distinct_now = {m: set(by_path.get(m, {}).get("inbound_ctx_anchors", [])) for m in C.MONEY_AFFINITY}
    for st in state.values():
        for lk in st["proposals"]:
            if lk["target"] in distinct_now:
                distinct_now[lk["target"]].add(lk["anchor"])

    for money_page, keywords in C.MONEY_AFFINITY.items():
        if money_page not in by_path:
            continue
        # Candidate source articles: keyword match, has room, not already linking.
        cands = []
        for x in posts:
            st = state[x["path"]]
            if st["room"] <= 0 or money_page in st["targets"]:
                continue
            hay = (C.slug_of(x["path"]) + " " + (x["title"] or "")).lower()
            score = sum(1 for kw in keywords if kw in hay)
            if score:
                cands.append((score, x["words"], x["path"]))
        cands.sort(key=lambda z: (-z[0], -z[1]))  # best keyword fit, longest first
        for _score, _w, src in cands:
            if len(distinct_now[money_page]) >= C.MONEY_ANCHOR_FLOOR:
                break
            st = state[src]
            a = pick_anchor(money_page)
            if not a:
                break  # pool exhausted for this target
            st["proposals"].append({"target": money_page, "anchor": a, "zone": "top",
                                    "type": "up", "reason": "équilibrage: page money sous le plancher d'ancres"})
            st["targets"].add(money_page)
            st["room"] -= 1
            distinct_now[money_page].add(a)

    # ---- Assemble plan ----
    for x in posts:
        st = state[x["path"]]
        if st["proposals"]:
            slug = C.slug_of(x["path"])
            primary, _ = C.cluster_of(slug)
            plan[x["path"]] = {
                "title": x["title"], "words": x["words"], "cluster": primary,
                "existing_ctx_links": st["existing_n"], "budget": st["budget"],
                "new_links": st["proposals"],
            }

    json.dump({"site": data["site"], "articles_planned": len(plan), "plan": plan},
              open(os.path.join(HERE, "maillage-plan.json"), "w"),
              ensure_ascii=False, indent=1)

    write_report(items, by_path, plan)
    print(f"Planned new links for {len(plan)} articles.")
    total = sum(len(p["new_links"]) for p in plan.values())
    print(f"Total NEW contextual links proposed: {total}")


def write_report(items, by_path, plan):
    # Projected inbound (contextual) per money page after applying the plan
    money = list(anchors.POOLS.keys())
    projected = collections.defaultdict(lambda: {"add": 0, "anchors": set()})
    for src, p in plan.items():
        for lk in p["new_links"]:
            if lk["target"] in money:
                projected[lk["target"]]["add"] += 1
                projected[lk["target"]]["anchors"].add(lk["anchor"])

    # Cannibalization audit on the PLAN (must be zero by construction)
    anchor_targets = collections.defaultdict(set)
    for p in plan.values():
        for lk in p["new_links"]:
            anchor_targets[lk["anchor"].strip().lower()].add(lk["target"])
    canni = {a: sorted(t) for a, t in anchor_targets.items() if len(t) > 1}

    lines = ["# Maillage interne — Plan DRY-RUN", "",
             "Généré par `maillage.py` à partir de `inventory.json` (données live).",
             "Aucune écriture n'a été faite sur WordPress. Étape d'application séparée et validée.", "",
             "## Synthèse", "",
             f"- Articles concernés : **{len(plan)}**",
             f"- Liens contextuels NOUVEAUX proposés : **{sum(len(p['new_links']) for p in plan.values())}**",
             f"- Cannibalisation d'ancres dans le plan : **{len(canni)}** (objectif : 0)", "",
             "## Pages money — liens contextuels entrants projetés (ajouts)", "",
             "| Page money | ctx entrants actuels | ancres distinctes actuelles | + liens (plan) | + ancres distinctes |",
             "|---|---|---|---|---|"]
    for m in money:
        cur = by_path.get(m, {})
        lines.append(f"| {m} | {cur.get('inbound_ctx_count', 0)} | "
                     f"{len(cur.get('inbound_ctx_anchors', []))} | "
                     f"+{projected[m]['add']} | +{len(projected[m]['anchors'])} |")

    if canni:
        lines += ["", "## ⚠️ Ancres cannibales détectées", ""]
        for a, t in canni.items():
            lines.append(f"- `{a}` → {', '.join(t)}")

    lines += ["", "## Détail par article", ""]
    for src in sorted(plan):
        p = plan[src]
        lines.append(f"### {src}")
        lines.append(f"_{p['title']}_ — cluster **{p['cluster']}** · {p['words']} mots · "
                     f"{p['existing_ctx_links']} liens ctx existants · budget {p['budget']}")
        lines.append("")
        lines.append("| zone | type | ancre | → cible |")
        lines.append("|---|---|---|---|")
        for lk in p["new_links"]:
            lines.append(f"| {lk['zone']} | {lk['type']} | {lk['anchor']} | {lk['target']} |")
        lines.append("")

    open(os.path.join(HERE, "MAILLAGE-DRY-RUN.md"), "w").write("\n".join(lines))


if __name__ == "__main__":
    main()
