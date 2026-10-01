#!/usr/bin/env python3
"""OW-2 item 1 frame builder — the Isaiah LF-SUPPORT audit frame, 155/155.

Derives the frame from the durable Isa LF primary packets (verdict=support),
maps the two boss-retired rows onto their absorbing successors, verifies
every audit target exists in the SHIPPED corpus, asserts the owner
denominator (155) EXACTLY (a mismatch is SURFACED, never substituted), pins
input hashes (OW-2 item 6), and emits the frame + 8-row audit slices.
Run from SP\OW2_audit.
"""
import glob
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP_ISA = HERE.parent / "Isa"
SHIPPED = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking"
               r"\M8_fable\book_chunks\Isa\chunks.jsonl")

# boss-adopted retirements (Isa B-3 / B-5): retired id -> absorbing survivor
RETIRE_MAP = {"P09-004": "P09-003", "P15-003": "P15-002"}
OWNER_DENOMINATOR = 155


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


support = set()
packet_hashes = {}
packets = sorted(glob.glob(str(SP_ISA / "reviews" / "c*_LF.json")))
assert packets, "no LF packets found"
for f in packets:
    p = Path(f)
    packet_hashes[p.name] = sha(p)
    pkt = json.load(open(f, encoding="utf-8"))
    items = pkt.get("items") or pkt.get("reviews") or pkt.get("rows") or []
    if isinstance(items, dict):
        items = [dict(v, row_id=k) for k, v in items.items()]
    for it in items:
        rid = (it.get("row_id") or it.get("writer_decision_id")
               or it.get("decision_id"))
        verdict = (it.get("verdict") or it.get("ruling") or "").lower()
        if rid and verdict == "support":
            support.add(rid)

frame_raw = sorted(support)
shipped_rows = [json.loads(l) for l in
                SHIPPED.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
by_id = {r.get("writer_decision_id") or r.get("decision_id"): r
         for r in shipped_rows}
by_idx = {r["chunk_index_in_book"]: r for r in shipped_rows}

targets = []
mappings = []
missing = []
for rid in frame_raw:
    if rid in by_id:
        targets.append(rid)
    elif rid in RETIRE_MAP and RETIRE_MAP[rid] in by_id:
        mappings.append({"frame_id": rid, "audited_as": RETIRE_MAP[rid],
                         "reason": "boss-adopted retirement; span absorbed"})
        targets.append(RETIRE_MAP[rid])
    else:
        missing.append(rid)

targets_unique = sorted(set(targets))
report = {"schema": "m8_ow2_isa_lf_frame.v1", "built": "2026-08-31",
          "frame_raw_size": len(frame_raw),
          "owner_denominator": OWNER_DENOMINATOR,
          "denominator_match": len(frame_raw) == OWNER_DENOMINATOR,
          "audit_targets_unique": len(targets_unique),
          "retirement_mappings": mappings, "missing_unmapped": missing,
          "pinned": {"book_chunks/Isa/chunks.jsonl": sha(SHIPPED),
                     "lf_packets": packet_hashes},
          "row_ids": targets_unique}
if len(frame_raw) != OWNER_DENOMINATOR or missing:
    report["status"] = "MISMATCH_SURFACED_DO_NOT_LAUNCH"
    json.dump(report, open(HERE / "frame_isa_lf.v1.json", "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: report[k] for k in
                      ("frame_raw_size", "denominator_match",
                       "audit_targets_unique", "missing_unmapped", "status")},
                     indent=1))
    raise SystemExit(1)

report["status"] = "READY"
json.dump(report, open(HERE / "frame_isa_lf.v1.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 8-row slices over the AUDIT TARGETS in id order
slices = [targets_unique[i:i + 8] for i in range(0, len(targets_unique), 8)]
for n, ids in enumerate(slices, 1):
    items = []
    for rid in ids:
        row = by_id[rid]
        idx = row["chunk_index_in_book"]
        item = {"row_id": rid, "shipped_row": row}
        if idx - 1 in by_idx:
            item["prev_row"] = by_idx[idx - 1]
        if idx + 1 in by_idx:
            item["next_row"] = by_idx[idx + 1]
        fm = [m for m in mappings if m["audited_as"] == rid]
        if fm:
            item["frame_mapping_note"] = fm
        items.append(item)
    doc = {"schema": "m8_ow2_lf_slice.v1", "batch": f"b{n:02d}",
           "attempt_id": f"ow2lf_b{n:02d}_a1",
           "output_file": f"reviews/ow2lf_b{n:02d}.json",
           "row_ids": ids, "items": items}
    (HERE / "slices").mkdir(exist_ok=True)
    json.dump(doc, open(HERE / "slices" / f"slice_b{n:02d}.json", "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
(HERE / "reviews").mkdir(exist_ok=True)
print(json.dumps({"frame_raw_size": len(frame_raw),
                  "audit_targets_unique": len(targets_unique),
                  "mappings": mappings, "slices": len(slices),
                  "last_slice_rows": len(slices[-1]),
                  "status": "READY"}, indent=1))
