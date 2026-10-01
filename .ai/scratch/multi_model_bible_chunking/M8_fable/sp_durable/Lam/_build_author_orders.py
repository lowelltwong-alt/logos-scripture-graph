#!/usr/bin/env python3
"""Deterministic author-order builder — Lam repair wave (m8-mesh-r3 + OW-1; the Jer _build_author_orders.py shape with
the hand lists replaced by author_overrides.json). Consumes remedy_docket.v1.json + every VERIFIED boss ledger
(reviews/boss_lam_bN.json) and emits author/orders_aNN.json per agent + author_orders_summary.json. Order composition per
row: docket entry verbatim (peer remedy = the work order) where one exists; every boss ruling whose consequence.rows
names the row, embedded VERBATIM (boss-over-peer); op hint replace | retire | new_row. author_overrides.json (written by
the orchestrator after reading the boss ledgers): {"retires": {row: ruling_id}, "new_rows": {row: ruling_id},
"no_edit": {row: reason}, "agents": [["a01", ["P01"]], ...]}. Corpus-wide orders are NOT folded per row (E-18).
Usage: _build_author_orders.py"""
import glob, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; OUT = HERE / "author"
d = json.load(open(HERE / "remedy_docket.v1.json", encoding="utf-8")); dk = d["docket"]
rows = [json.loads(l) for l in open(HERE / "draft_rows_combined.jsonl", encoding="utf-8") if l.strip()]; by_id = {r["decision_id"]: r for r in rows}
ov = json.load(open(HERE / "author_overrides.json", encoding="utf-8")) if (HERE / "author_overrides.json").exists() else {}
RETIRES = ov.get("retires", {}); NEW_ROWS = ov.get("new_rows", {}); NO_EDIT = ov.get("no_edit", {})
boss = {}
for f in sorted(glob.glob(str(HERE / "reviews" / "boss_lam_b[0-9].json"))):
    doc = json.load(open(f, encoding="utf-8-sig"))
    for r in doc["rulings"]: boss[r["id"]] = r
row_rulings = {}
for bid, r in boss.items():
    for rid in (r.get("consequence") or {}).get("rows") or []:
        if rid.startswith("corpus_wide") or rid == "record": continue
        row_rulings.setdefault(rid, []).append(bid)
refuted = {rid for rid, e in dk.items() if e["ruling"] == "refute"}
touched = (set(dk) - refuted) | set(row_rulings) | set(NEW_ROWS); touched -= set(NO_EDIT)
entries = {}
for rid in sorted(touched):
    if rid in NEW_ROWS:
        entries[rid] = {"row_id": rid, "op": "new_row", "authored_from": NEW_ROWS[rid], "boss_rulings": {NEW_ROWS[rid]: boss[NEW_ROWS[rid]]}, "note": "author the row IN FULL per the boss spec; 22-field schema; decision_id exactly as given; chunk_index_in_book 0"}; continue
    e = {"row_id": rid, "op": "retire" if rid in RETIRES else "replace"}
    if rid in dk and dk[rid]["ruling"] != "refute": e["docket"] = dk[rid]
    if rid in row_rulings: e["boss_rulings"] = {bid: boss[bid] for bid in sorted(row_rulings[rid])}
    if rid in RETIRES: e["note"] = f"retire per {RETIRES[rid]}; surviving orders re-point per that spec"
    assert rid in by_id, f"{rid} not in corpus"; e["current_row"] = by_id[rid]; entries[rid] = e
def part_of(rid): return rid.split("-")[0].rstrip("b")
parts = {}
for rid in entries: parts.setdefault(part_of(rid), []).append(rid)
for p in parts: parts[p].sort()
AGENTS = ov.get("agents") or [[f"a{i + 1:02d}", [p]] for i, p in enumerate(sorted(parts))]
assigned = [p for _, ps in AGENTS for p in ps]; assert sorted(assigned) == sorted(parts.keys()), f"part split mismatch: {sorted(set(parts) - set(assigned))} unassigned / {sorted(set(assigned) - set(parts))} empty"
OUT.mkdir(exist_ok=True)
summary = {"schema": "lam_author_orders.v1", "orders_total": len(entries), "replace": sum(1 for e in entries.values() if e["op"] == "replace"), "retire": sum(1 for e in entries.values() if e["op"] == "retire"), "new_row": sum(1 for e in entries.values() if e["op"] == "new_row"), "excluded_no_edit": NO_EDIT, "refuted_stand": sorted(refuted), "agents": {}}
for aid, ps in AGENTS:
    ids = [rid for p in ps for rid in parts.get(p, [])]; attempts = [ids[i:i + 8] for i in range(0, len(ids), 8)]
    doc = {"schema": "lam_author_orders_slice.v1", "agent": aid, "parts": ps, "row_ids": ids, "attempts": attempts, "attempt_ids": [f"lam_auth_{aid}_a{n + 1}" for n in range(len(attempts))], "output_file": f"author/author_{aid}.jsonl", "orders": {rid: entries[rid] for rid in ids}}
    json.dump(doc, open(OUT / f"orders_{aid}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    summary["agents"][aid] = {"parts": ps, "rows": len(ids), "attempts": len(attempts), "output_file": doc["output_file"]}
json.dump(summary, open(HERE / "author_orders_summary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
