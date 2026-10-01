"""Build per-agent author work-order files from peer_work_orders.json + boss_isa_r1.json.

Deterministic. Writes SP/Isa/author/orders_aNN.json and a plan summary to stdout.
Run from SP/Isa.
"""
import json, collections, sys

PEER = json.load(open("peer_work_orders.json", encoding="utf-8"))
BOSS = json.load(open("reviews/boss_isa_r1.json", encoding="utf-8"))
ROWS = [json.loads(l) for l in open("draft_rows_combined.jsonl", encoding="utf-8")]
ROW_BY_ID = {r["writer_decision_id"]: r for r in ROWS}

# --- boss row map (rows -> binding B-ids), from the ledger's consequence.rows ---
boss_rows = collections.defaultdict(list)
for ruling in BOSS["rulings"]:
    for row in ruling["consequence"]["rows"]:
        rid = row.split()[0].split("(")[0].strip()
        if rid.startswith("P") and "-" in rid:
            boss_rows[rid].append(ruling["id"])

RETIRES = {"P15-003": "B-3", "P09-004": "B-5"}
MERGE_SURVIVORS = {"P15-002": "B-3", "P09-003": "B-5"}
RESPANS = {"P10-005": "B-2", "P10-006": "B-2"}
B6_ROWS = {r for r, bs in boss_rows.items() if "B-6" in bs}

# --- collect peer orders per row ---
orders_by_row = {}
for cat in ("boundary_proposals", "ordinary_cures"):
    for o in PEER[cat]:
        o = dict(o)
        o["category"] = cat
        orders_by_row[o["row_id"]] = o
assert len(orders_by_row) == 200, len(orders_by_row)

# --- union with boss rows; synthesize orders for boss-only rows ---
all_rows = set(orders_by_row) | set(boss_rows)
synthetic = sorted(set(boss_rows) - set(orders_by_row))
for rid in synthetic:
    orders_by_row[rid] = {
        "row_id": rid, "category": "boss_only", "source": "boss",
        "ruling": "boss_consequence",
        "remedy": "No separate peer remedy. Execute the boss consequence.spec items that name this row (see boss_refs).",
    }
for rid, o in orders_by_row.items():
    o["boss_refs"] = sorted(boss_rows.get(rid, []))
    o["op"] = "retire" if rid in RETIRES else "replace"

# --- allowed-fields hints ---
PROSE = ["boundary_rationale", "device_notes", "strongest_rejected_alternative",
         "observed_substrate_signals", "boundary_evidence_refs"]
for rid, o in orders_by_row.items():
    if o["op"] == "retire":
        o["allowed_fields"] = []
        continue
    allowed = list(PROSE)
    if rid in B6_ROWS or rid in MERGE_SURVIVORS or rid in RESPANS:
        allowed += ["confidence", "frontier_flag_considered"]
    if rid in MERGE_SURVIVORS or rid in RESPANS:
        allowed += ["span"]
    if "confidence" in (o.get("remedy") or "").lower():
        if "confidence" not in allowed:
            allowed += ["confidence", "frontier_flag_considered"]
    o["allowed_fields"] = allowed

# --- agent grouping (adjacent-part pairing; boss-heavy parts solo) ---
GROUPS = [
    ("a01", ["P01"]), ("a02", ["P02"]), ("a03", ["P03"]), ("a04", ["P04", "P06"]),
    ("a05", ["P05"]), ("a06", ["P07"]), ("a07", ["P08", "P09"]), ("a08", ["P10"]),
    ("a09", ["P11"]), ("a10", ["P12", "P13"]), ("a11", ["P14"]), ("a12", ["P15"]),
    ("a13", ["P16"]), ("a14", ["P17", "P18"]),
]
covered = set()
plan = []
for aid, parts in GROUPS:
    rids = sorted(r for r in all_rows if r[:3] in parts)
    covered |= set(rids)
    # attempts of <=8 rows
    attempts = [rids[i:i + 8] for i in range(0, len(rids), 8)]
    payload = {
        "schema": "isa_author_orders.v1", "agent": aid, "parts": parts,
        "attempts": [
            {"attempt_id": f"author_isa_{aid}_r{i+1}", "rows": chunk,
             "output": f"author/author_{aid}.jsonl" if i == 0 else f"author/author_{aid}_r{i+1}.jsonl"}
            for i, chunk in enumerate(attempts)
        ],
        "orders": {rid: orders_by_row[rid] for rid in rids},
    }
    with open(f"author/orders_{aid}.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    n_boss = sum(1 for r in rids if orders_by_row[r]["boss_refs"])
    plan.append((aid, "+".join(parts), len(rids), len(attempts), n_boss))

missing = all_rows - covered
assert not missing, missing
print("agent  parts    rows attempts boss-bound")
for aid, parts, n, na, nb in plan:
    print(f"{aid}   {parts:8} {n:4} {na:8} {nb:10}")
print(f"TOTAL rows={len(all_rows)} (peer-remedied 200 + boss-only {len(synthetic)}: {synthetic})")
print(f"retires={sorted(RETIRES)} merge_survivors={sorted(MERGE_SURVIVORS)} respans={sorted(RESPANS)}")
print(f"B6 class rows={sorted(B6_ROWS)}")
missing_ids = [r for r in all_rows if r not in ROW_BY_ID]
print("rows not in corpus:", missing_ids or "NONE")
