#!/usr/bin/env python3
r"""Deterministic builder for the OW-2 item-2 (and item-3) Fable-5-high
adjudication slices.

Extracts the routing queue from every VERIFIED audit packet of the item-2 lane
(reviews/ow2i2_<Book>_NN.json, 29 slices) and, when present, the item-3 lane
(reviews/ow2p38_NN.json, 5 slices) using EXACTLY the lane verifiers' rule —
every medium/high finding + every finding whose REQUIRED boolean span_change is
true (no pattern fallback in these lanes) — joins each item with its full
finding body, the trigger that put the row in scope (item-2 rows), and the
row's audit-slice context (shipped row + neighbors), groups by row (a row's
items never split), keeps slices BOOK-PURE (one toolkit per adjudicator), and
packs rows in frame order into slices of <= 8 items per attempt.
Assertions pin the queue size against the verifiers' full-run counts passed on
the command line (--expect-i2 N [--expect-p38 M]); a mismatch is surfaced,
never substituted.

2026-09-05 (orchestrator-owned edit, recorded in CYCLE_STATE): (a) rows are
packed LANE-FIRST (every item-2 row before every item-3 row, frame order inside
each lane) so the item-2 slices already adjudicated stay byte-identical when the
item-3 queue is appended; (b) NO-CLOBBER GUARD — an existing slice file whose
content would change is never overwritten: the run aborts with the slice named
(a delivered packet always matches the slice it was launched from).
Usage: _build_i2adj_slices.py --expect-i2 N [--expect-p38 M]
"""
import argparse
import glob
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_ITEMS = 8
BOOK_ORDER = ["Ps", "Job", "Prov", "Eccl", "Song"]
LANE_RANK = {"i2": 0, "p38": 1}

ap = argparse.ArgumentParser()
ap.add_argument("--expect-i2", type=int, required=True)
ap.add_argument("--expect-p38", type=int, default=None)
ns = ap.parse_args()


def grounds_text(g):
    if isinstance(g, list):
        return " | ".join(str(x).strip() for x in g)
    return g


def slice_batches(prefix):
    out = []
    for p in sorted(glob.glob(str(HERE / "slices" / f"slice_{prefix}_*.json"))):
        m = re.match(rf"slice_({prefix}_.+)\.json$", Path(p).name)
        out.append(m.group(1))
    return out


# --- gather context + queue, per source lane
context = {}          # key -> {book, audit_batch, source_lane, triggers, ...}
row_order = []        # (lane_rank, book_index, chunk_index, key)
row_items = {}
sev_hist = {"low": 0, "medium": 0, "high": 0}
per_lane = {"i2": 0, "p38": 0}
span_items = []
for lane, prefix in (("i2", "i2"), ("p38", "p38")):
    for b in slice_batches(prefix):
        sl = json.load(open(HERE / "slices" / f"slice_{b}.json", encoding="utf-8"))
        pk_path = HERE / sl["output_file"]
        if not pk_path.is_file():
            if lane == "p38":
                continue
            raise SystemExit(f"missing verified packet {sl['output_file']} — audit incomplete, do not build")
        pk = json.load(open(pk_path, encoding="utf-8"))
        book = sl["book"]
        by_row = {it["row_id"]: it for it in sl["items"]}
        for r in pk["rows"]:
            rid = r["row_id"]
            ctx_item = by_row[rid]
            key = f"{lane}:{rid}"
            k = 0
            for f in r.get("findings") or []:
                sev = f["severity"]
                explicit = f.get("span_change")
                assert isinstance(explicit, bool), f"{b} {rid}: span_change not boolean (verifier should have failed)"
                if sev not in ("medium", "high") and not explicit:
                    continue
                k += 1
                item = {"item_id": f"{rid}#{k}" if lane == "i2" else f"{rid}#p38-{k}",
                        "source_lane": lane, "audit_batch": b, "book": book, "row_id": rid,
                        "severity": sev, "class": f.get("class"), "claim": f.get("claim"),
                        "grounds": grounds_text(f.get("grounds")), "span_change": explicit,
                        "proposed_change": f.get("proposed_change")}
                if key not in row_items:
                    row_items[key] = []
                    row_order.append((LANE_RANK[lane], BOOK_ORDER.index(book),
                                      ctx_item["shipped_row"]["chunk_index_in_book"], key))
                    context[key] = {"book": book, "audit_batch": b, "source_lane": lane,
                                    "triggers": ctx_item.get("triggers"),
                                    "trigger_dispositions": r.get("triggers"),
                                    "shipped_row": ctx_item["shipped_row"],
                                    "prev_row": ctx_item.get("prev_row"), "next_row": ctx_item.get("next_row")}
                row_items[key].append(item)
                sev_hist[sev] += 1
                per_lane[lane] += 1
                if explicit:
                    span_items.append(item["item_id"])

assert per_lane["i2"] == ns.expect_i2, f"i2 queue {per_lane['i2']} != verifier {ns.expect_i2}"
if ns.expect_p38 is not None:
    assert per_lane["p38"] == ns.expect_p38, f"p38 queue {per_lane['p38']} != verifier {ns.expect_p38}"
for key, its in row_items.items():
    assert len(its) <= MAX_ITEMS, f"{key} carries {len(its)} items > {MAX_ITEMS}"

# --- pack: lane-first, book-pure, rows whole, frame order, <= 8 items per slice
row_order.sort()
groups = []
cur, cur_n, cur_book, cur_lane = [], 0, None, None
for lr, bi, ci, key in row_order:
    book = context[key]["book"]
    n = len(row_items[key])
    if cur and (cur_n + n > MAX_ITEMS or book != cur_book or lr != cur_lane):
        groups.append((cur_book, cur))
        cur, cur_n = [], 0
    cur.append(key)
    cur_n += n
    cur_book = book
    cur_lane = lr
if cur:
    groups.append((cur_book, cur))

slice_report = []
counters = {}
pending = []
for book, keys in groups:
    counters[book] = counters.get(book, 0) + 1
    name = f"i2adj_{book}_{counters[book]:02d}"
    doc = {"schema": "m8_ow2_i2adj_slice.v1", "batch": name, "book": book,
           "attempt_id": f"ow2i2adj_{book}_{counters[book]:02d}_a1",
           "output_file": f"reviews/ow2i2adj_{book}_{counters[book]:02d}.json",
           "item_ids": [it["item_id"] for key in keys for it in row_items[key]],
           "rows": [{"row_id": key.split(":", 1)[1], "source_lane": context[key]["source_lane"],
                     "audit_batch": context[key]["audit_batch"], "queue_items": row_items[key],
                     "context": {kk: vv for kk, vv in context[key].items() if kk not in ("audit_batch", "source_lane")}}
                    for key in keys]}
    new_bytes = json.dumps(doc, ensure_ascii=False, indent=1).encode("utf-8")
    out = HERE / "slices" / f"slice_{name}.json"
    pending.append((name, book, keys, doc, out, new_bytes))

# no-clobber guard: every existing slice must be byte-identical to what would be written
clobber = [str(out.name) for name, book, keys, doc, out, nb in pending if out.exists() and out.read_bytes() != nb]
if clobber:
    raise SystemExit(f"REFUSING to overwrite existing slices with different content (delivered packets depend on them): {clobber}")
for name, book, keys, doc, out, nb in pending:
    state = "unchanged" if out.exists() else "written"
    if state == "written":
        out.write_bytes(nb)
    slice_report.append({"slice": name, "book": book, "rows": len(keys), "items": len(doc["item_ids"]),
                         "bytes": out.stat().st_size, "sha256": hashlib.sha256(out.read_bytes()).hexdigest()[:16],
                         "state": state,
                         "lanes": sorted({context[k]["source_lane"] for k in keys})})

total = sum(s["items"] for s in slice_report)
assert total == per_lane["i2"] + per_lane["p38"]
print(json.dumps({"queue_total": total, "per_lane": per_lane, "severity": sev_hist,
                  "distinct_rows": len(row_order), "genuine_span_items": span_items,
                  "slices": slice_report,
                  "per_book_slices": {b: sum(1 for s in slice_report if s["book"] == b) for b in BOOK_ORDER}},
                 ensure_ascii=False, indent=1))
