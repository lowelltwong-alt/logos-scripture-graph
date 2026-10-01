#!/usr/bin/env python3
"""Deterministic author-order builder — Jer repair wave (m8-mesh-r3 + OW-1).

Consumes remedy_docket.v1.json + the four VERIFIED boss ledgers and emits
author/orders_aNN.json per agent plus author_orders_summary.json.

Order composition per row:
- docket entry verbatim (peer remedy = the work order), where one exists;
- every boss ruling whose consequence.rows names the row, embedded VERBATIM
  (boss-over-peer: its spec controls; supersessions/survivals are stated
  inside the spec text);
- op hint: replace | retire | new_row.
Rows the boss enumerated as NO-EDIT (P02-016, P03-009) are excluded with a
recorded reason. The corpus-wide orders CWO-1..CWO-8 + the boss-ordered
zone-coordinate sweep (B1-6 arm, CWO-9) are NOT folded per-row (E-18);
they execute as their own wave slice. B4-6's six enumerated key-drops ride
per-row (a completed deterministic enumeration, the Isa B-6 pattern).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "author"

d = json.load(open(HERE / "remedy_docket.v1.json", encoding="utf-8"))
dk = d["docket"]
rows = [json.loads(l) for l in open(HERE / "draft_rows_combined.jsonl", encoding="utf-8")]
by_id = {r["decision_id"]: r for r in rows}
assert len(rows) == 276

boss = {}
for a in ("b1", "b2", "b3", "b4"):
    doc = json.load(open(HERE / "reviews" / f"boss_jer_{a}.json", encoding="utf-8"))
    for r in doc["rulings"]:
        boss[r["id"]] = r

# boss consequence index: row -> [ruling ids]
row_rulings = {}
for bid, r in boss.items():
    for rid in r["consequence"].get("rows") or []:
        if rid.startswith("corpus_wide"):
            continue
        row_rulings.setdefault(rid, []).append(bid)

RETIRES = {"P14-008": "B3-5", "P06-012": "B2-5"}
NEW_ROWS = {"P02-017b": "B1-4"}
NO_EDIT = {"P02-016": "B1-4 rules NO EDIT REQUIRED (prose anchors forward to Jer.6.6, unchanged)",
           "P03-009": "B1-6 rules NO span edit and NO seam edit (front corroboration + K/Q disclosure unchanged and still true)"}

# every row that needs an author touch
touched = set(dk.keys()) - {"P13-006"}          # refuted row: stands, no order
touched |= set(row_rulings.keys())
touched |= set(NEW_ROWS.keys())
touched -= set(NO_EDIT.keys())

entries = {}
for rid in sorted(touched):
    if rid in NEW_ROWS:
        entries[rid] = {"row_id": rid, "op": "new_row",
                        "authored_from": NEW_ROWS[rid],
                        "boss_rulings": {NEW_ROWS[rid]: boss[NEW_ROWS[rid]]},
                        "note": "author the row IN FULL per the boss spec; 22-field schema; decision_id exactly as given"}
        continue
    op = "retire" if rid in RETIRES else "replace"
    e = {"row_id": rid, "op": op}
    if rid in dk and dk[rid]["ruling"] != "refute":
        e["docket"] = dk[rid]
    if rid in row_rulings:
        e["boss_rulings"] = {bid: boss[bid] for bid in sorted(row_rulings[rid])}
    if rid in RETIRES:
        e["note"] = f"retire per {RETIRES[rid]}; surviving orders re-point per that spec"
    assert rid in by_id or rid in NEW_ROWS, f"{rid} not in corpus"
    if rid in by_id:
        e["current_row"] = by_id[rid]
    entries[rid] = e

# sample-lane defect P06-009 must carry B2-7's order even if unchallenged
assert "P06-009" in entries and "B2-7" in entries["P06-009"].get("boss_rulings", {}), \
    "B2-7 ratified order must ride on P06-009"

# agent split: part-grouped, <=8 rows per attempt, ~11-20 rows per agent
def part_of(rid):
    return rid.split("-")[0].replace("b", "")  # P02-017b -> P02

parts = {}
for rid in entries:
    parts.setdefault(part_of(rid), []).append(rid)
for p in parts:
    parts[p].sort()

AGENTS = [
    ("a01", ["P01"]), ("a02", ["P02"]), ("a03", ["P03", "P16"]),
    ("a04", ["P04"]), ("a05", ["P05"]), ("a06", ["P06"]),
    ("a07", ["P07", "P08"]), ("a08", ["P09", "P12"]), ("a09", ["P10"]),
    ("a10", ["P11"]), ("a11", ["P13", "P14"]), ("a12", ["P15"]),
    ("a13", ["P17"]), ("a14", ["P18"]), ("a15", ["P19", "P20"]),
]
assigned = [p for _, ps in AGENTS for p in ps]
assert sorted(assigned) == sorted(parts.keys()), \
    f"part split mismatch: {sorted(set(parts) - set(assigned))} unassigned / {sorted(set(assigned) - set(parts))} empty"

OUT.mkdir(exist_ok=True)
summary = {"schema": "jer_author_orders.v1", "orders_total": len(entries),
           "replace": sum(1 for e in entries.values() if e["op"] == "replace"),
           "retire": sum(1 for e in entries.values() if e["op"] == "retire"),
           "new_row": sum(1 for e in entries.values() if e["op"] == "new_row"),
           "excluded_no_edit": NO_EDIT, "agents": {}}
for aid, ps in AGENTS:
    ids = [rid for p in ps for rid in parts[p]]
    attempts = [ids[i:i + 8] for i in range(0, len(ids), 8)]
    doc = {"schema": "jer_author_orders_slice.v1", "agent": aid, "parts": ps,
           "row_ids": ids, "attempts": attempts,
           "attempt_ids": [f"jer_auth_{aid}_a{n+1}" for n in range(len(attempts))],
           "output_file": f"author/author_{aid}.jsonl",
           "orders": {rid: entries[rid] for rid in ids}}
    json.dump(doc, open(OUT / f"orders_{aid}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    summary["agents"][aid] = {"parts": ps, "rows": len(ids),
                              "attempts": len(attempts),
                              "output_file": doc["output_file"]}
json.dump(summary, open(HERE / "author_orders_summary.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
