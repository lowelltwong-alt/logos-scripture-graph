#!/usr/bin/env python3
"""Orchestrator Tier-0: compile the author-wave work-order manifest from all
peer rulings and boss attempts (run ONCE after the final boss attempt).

Walks SP/Prov/reviews/peer_*.json and boss_prov_r*.json, extracts:
  - every upheld/refined peer ruling's remedy (with cluster, row, severity,
    grounds pointer);
  - every boss consequence (adopt_change / disclosure_cure) with its spec;
  - deferred-but-ruled follow-on files included automatically (peer_*_r2).
Groups orders by writer part (from the row id prefix) and tags class-sweep
orders (S-1/S-2/engagement/E-1) by remedy-text heuristics for batch planning.
Output: ../author/work_orders.json (+ a per-part/class summary to stdout).
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
REVIEWS = SPBOOK / "reviews"
OUT_DIR = SPBOOK / "author"
OUT_DIR.mkdir(exist_ok=True)

CLASS_PATTERNS = [
    ("S1_el_citation", re.compile(r"אֶל|el.?citation|divine.name.*(?:preposition|אל)", re.I)),
    ("S2_quote_convention", re.compile(r"curly|straight.*quote|quote.*convention|web: ref", re.I)),
    ("HEB_engagement", re.compile(r"hebrew.?engagement|transliterat|skeleton.tier.*(?:label|unlabel)|no quoted hebrew|quote the original", re.I)),
    ("E1_stale_figure", re.compile(r"stale|17.*(?:figure|count)|5.of.17", re.I)),
]


def classify(text: str) -> str:
    for name, pat in CLASS_PATTERNS:
        if pat.search(text):
            return name
    return "row_specific"


def main() -> int:
    orders = []
    for f in sorted(glob.glob(str(REVIEWS / "peer_*.json"))):
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        for r in data.get("rulings", []):
            ruling = (r.get("ruling") or "").lower()
            if ruling not in ("uphold", "refine"):
                continue
            remedy = r.get("remedy")
            if not remedy or remedy in ("null", "n/a"):
                continue
            row = r.get("row_id", "?")
            orders.append({
                "source": Path(f).name,
                "kind": "peer_remedy",
                "cluster": r.get("cluster"),
                "row_id": row,
                "part": row.split("-")[0].lower() if "-" in row else "?",
                "severity": r.get("severity_final") or r.get("severity"),
                "ruling": ruling,
                "remedy": remedy,
                "class": classify(json.dumps(r, ensure_ascii=False)),
            })
    for f in sorted(glob.glob(str(REVIEWS / "boss_prov_r*.json"))):
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        for r in data.get("rulings", []):
            c = r.get("consequence", {})
            kind = c.get("kind")
            if kind in ("no_action", "owner_escalation") or not kind:
                continue
            rows = c.get("rows", [])
            orders.append({
                "source": Path(f).name,
                "kind": f"boss_{kind}",
                "ruling_id": r.get("id"),
                "rows": rows,
                "part": rows[0].split("-")[0].lower() if rows else "?",
                "severity": r.get("severity"),
                "remedy": c.get("spec"),
                "class": "boss_order",
            })
    manifest = {
        "built": "post-boss-r4, orchestrator Tier-0",
        "order_count": len(orders),
        "orders": orders,
    }
    (OUT_DIR / "work_orders.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    by_class = {}
    by_part = {}
    for o in orders:
        by_class[o["class"]] = by_class.get(o["class"], 0) + 1
        by_part[o["part"]] = by_part.get(o["part"], 0) + 1
    print(json.dumps({"orders": len(orders), "by_class": by_class,
                      "by_part": dict(sorted(by_part.items()))}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
