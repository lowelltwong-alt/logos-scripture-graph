#!/usr/bin/env python3
"""Deterministic builder for the OW-2 item-1 Fable-5-high adjudication slices.

Extracts the routing queue (every medium/high finding + every span-flagged
finding) from the 20 verified audit packets using EXACTLY the _ow2lf_verify.py
rule, joins each item with its full finding body and the row's audit-slice
context (shipped row + neighbor), groups by row (a row's items never split),
and packs rows in frame order into slices of <= 8 items per attempt.
Assertions pin the queue size against the verifier's full-run count (146).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_QUEUE = 146  # _ow2lf_verify.py full-run routing_queue_size, 2026-09-01
MAX_ITEMS = 8

# copied VERBATIM from _ow2lf_verify.py — the two rules must never diverge
SPAN_PAT = re.compile(
    r"respan|re-span|new span|span set|merge|merging|split|absorb|"
    r"boundary (?:change|move|relocat)|move the seam|retire", re.I)

# reconciled-by-reading pattern over-matches (wave A1 census, CYCLE_STATE
# 2026-08-31): the agent summaries were right; these are NOT span proposals.
RECONCILED_OVER_MATCHES = {("b02", "P01-010"), ("b04", "P03-010")}
OVER_MATCH_NOTE = (
    "orchestrator reconciliation (wave A1 census, 2026-08-31): the span "
    "pattern-detector over-matched this finding's proposed_change prose; the "
    "auditor's own summary declared it a non-span item and reading confirmed "
    "that. Treat as a severity item only, NOT a span proposal.")

batches = ["b%02d" % n for n in range(1, 21)]

# row context from the audit slices, keyed by row id
context = {}
for b in batches:
    sl = json.load(open(HERE / "slices" / f"slice_{b}.json", encoding="utf-8"))
    for it in sl["items"]:
        assert it["row_id"] not in context, f"duplicate row context {it['row_id']}"
        context[it["row_id"]] = {"audit_batch": b, **it}

# queue extraction in packet (frame) order, grouped by row
row_order = []
row_items = {}
sev_hist = {"low": 0, "medium": 0, "high": 0}
span_items = []
per_wave = {"A1": 0, "A2": 0}
for b in batches:
    pk = json.load(open(HERE / "reviews" / f"ow2lf_{b}.json", encoding="utf-8"))
    for r in pk["rows"]:
        rid = r["row_id"]
        k = 0
        for f in r.get("findings") or []:
            sev = f["severity"]
            sc = f.get("proposed_change")
            explicit = f.get("span_change")
            pattern_derived = not isinstance(explicit, bool)
            is_span = (bool(explicit) if isinstance(explicit, bool)
                       else bool(sc) and bool(SPAN_PAT.search(str(sc))))
            if sev not in ("medium", "high") and not is_span:
                continue
            k += 1
            item = {"item_id": f"{rid}#{k}", "audit_batch": b, "row_id": rid,
                    "severity": sev, "class": f.get("class"),
                    "claim": f.get("claim"), "grounds": f.get("grounds"),
                    "span_change": is_span,
                    "proposed_change": sc}
            if is_span and pattern_derived and (b, rid) in RECONCILED_OVER_MATCHES:
                item["span_change"] = False
                item["reconciliation_note"] = OVER_MATCH_NOTE
            if rid not in row_items:
                row_items[rid] = []
                row_order.append(rid)
            row_items[rid].append(item)
            sev_hist[sev] += 1
            per_wave["A1" if b <= "b10" else "A2"] += 1
            if item["span_change"]:
                span_items.append(item["item_id"])

total = sum(len(v) for v in row_items.values())
assert total == EXPECTED_QUEUE, f"queue {total} != verifier {EXPECTED_QUEUE}"
for rid, its in row_items.items():
    assert len(its) <= MAX_ITEMS, f"{rid} carries {len(its)} items > {MAX_ITEMS}"
    assert rid in context, f"no audit-slice context for {rid}"

# pack rows whole, frame order, <= 8 items per slice
groups = []
cur, cur_n = [], 0
for rid in row_order:
    n = len(row_items[rid])
    if cur and cur_n + n > MAX_ITEMS:
        groups.append(cur)
        cur, cur_n = [], 0
    cur.append(rid)
    cur_n += n
if cur:
    groups.append(cur)

slice_report = []
for i, rids in enumerate(groups, 1):
    name = f"adj{i:02d}"
    doc = {
        "schema": "m8_ow2_adj_slice.v1",
        "batch": name,
        "attempt_id": f"ow2adj_{i:02d}_a1",
        "output_file": f"reviews/ow2adj_{i:02d}.json",
        "item_ids": [it["item_id"] for rid in rids for it in row_items[rid]],
        "rows": [{"row_id": rid,
                  "audit_batch": context[rid]["audit_batch"],
                  "queue_items": row_items[rid],
                  "context": {kk: vv for kk, vv in context[rid].items()
                              if kk not in ("audit_batch",)}}
                 for rid in rids],
    }
    out = HERE / "slices" / f"slice_{name}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                   encoding="utf-8", newline="\n")
    slice_report.append({"slice": name, "rows": len(rids),
                         "items": len(doc["item_ids"]),
                         "bytes": out.stat().st_size})

assert sum(s["items"] for s in slice_report) == EXPECTED_QUEUE
print(json.dumps({"queue_total": total, "per_wave": per_wave,
                  "severity": sev_hist, "distinct_rows": len(row_order),
                  "genuine_span_items": span_items,
                  "reconciled_over_matches": sorted(
                      f"{b}:{r}" for b, r in RECONCILED_OVER_MATCHES),
                  "slices": slice_report}, ensure_ascii=False, indent=1))
