#!/usr/bin/env python3
"""OW-2 item 3 frame builder — the deferred 38-row Proverbs Opus OL review.

DURABLE PROVENANCE (sp_durable/Prov/freeze/CYCLE_STATE.md §OWNER MESH RULINGS
2026-08-18 ruling 2 + CYCLE_STATE_CLOSE.md §OWNER ITEMS PENDING 1 +
deliverables/Prov_completion.json scoped_mesh_disclosure.ol_primaries_model):
the OL primaries ran on SONNET under the owner-approved hybrid fallback (opus
saturated, 5/5 launches killed); the owner deferred an OPUS OL spot-wave over
"the highest-stakes clusters (all 38 proverb_cluster rows + the crux zones)" to
restore cross-model decorrelation. Owner denominator: 38.

EXACT SET DERIVATION (at launch, from the shipped corpus, never from prose):
every shipped Prov row whose unit_type == "proverb_cluster". The count is
asserted EXACTLY against the owner denominator; a mismatch is SURFACED, never
substituted. The phrase "+ the crux zones" has NO enumerated durable row set
(the close record names none; the strategy's crux sites — 30:1 massa +
Ithiel-Ucal, the 22:20 shalishim K/Q, 31:1 massa, the 22:17 in-verse seam —
are chapter facts, not a ruled row list): that gap is SURFACED in the frame
for the owner and NOT folded into the 38. Pins: the shipped Prov corpus hash,
the durable Prov completion receipt, the durable close record.
Run from SP/OW2_audit.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SHIPPED = M8 / "book_chunks" / "Prov" / "chunks.jsonl"
COMPLETION = M8 / "sp_durable" / "Prov" / "deliverables" / "Prov_completion.json"
CLOSE = M8 / "sp_durable" / "Prov" / "freeze" / "CYCLE_STATE_CLOSE.md"
CYCLE = M8 / "sp_durable" / "Prov" / "freeze" / "CYCLE_STATE.md"
OWNER_DENOMINATOR = 38
MAX_ROWS = 8


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


rows = [json.loads(l) for l in SHIPPED.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
by_idx = {r["chunk_index_in_book"]: r for r in rows}
clusters = [r for r in rows if r.get("unit_type") == "proverb_cluster"]
completion = json.load(open(COMPLETION, encoding="utf-8"))
close_text = CLOSE.read_text(encoding="utf-8")
cycle_text = CYCLE.read_text(encoding="utf-8")
provenance_lines = [l.strip() for l in (close_text + "\n" + cycle_text).splitlines()
                    if "proverb_cluster" in l and ("crux" in l or "38" in l)]

report = {
    "schema": "m8_ow2_prov38_frame.v1", "built": "2026-09-03",
    "authorization": "owner directive OW-2 item 2 (2026-08-31): 'Complete the deferred 38-row Proverbs Opus review' under the OW-2D sequencing ruling (audit first)",
    "owner_denominator": OWNER_DENOMINATOR,
    "derivation_rule": "every shipped Prov row with unit_type == proverb_cluster (book_chunks/Prov/chunks.jsonl)",
    "derived_size": len(clusters),
    "denominator_match": len(clusters) == OWNER_DENOMINATOR,
    "completion_receipt_unit_type_count": completion["unit_type_distribution"].get("proverb_cluster"),
    "completion_receipt_ol_model": completion["scoped_mesh_disclosure"]["ol_primaries_model"],
    "durable_provenance_lines": provenance_lines,
    "crux_zones_gap_surfaced": ("the durable record's phrase '+ the crux zones' names no enumerated row set; the 38 are the "
                                "proverb_cluster rows EXACTLY; crux-site rows (30:1 massa/Ithiel-Ucal, 22:20 shalishim K/Q, "
                                "31:1 massa, the 22:17 in-verse seam) are NOT folded in — owner decision needed if they "
                                "are to be added as a separately-denominated set"),
    "pinned": {"book_chunks/Prov/chunks.jsonl": sha(SHIPPED),
               "sp_durable/Prov/deliverables/Prov_completion.json": sha(COMPLETION),
               "sp_durable/Prov/freeze/CYCLE_STATE_CLOSE.md": sha(CLOSE),
               "sp_durable/Prov/freeze/CYCLE_STATE.md": sha(CYCLE)},
    "row_ids": [r["decision_id"] for r in clusters],
}
if not report["denominator_match"] or completion["unit_type_distribution"].get("proverb_cluster") != OWNER_DENOMINATOR:
    report["status"] = "MISMATCH_SURFACED_DO_NOT_LAUNCH"
    (HERE / "frame_prov38.v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({k: report[k] for k in ("derived_size", "denominator_match", "status")}, indent=1))
    raise SystemExit(1)

n = len(clusters)
k = -(-n // MAX_ROWS)
base, extra = divmod(n, k)
sizes = [base + 1 if i < extra else base for i in range(k)]
slices = []
pos = 0
(HERE / "slices").mkdir(exist_ok=True)
for i, sz in enumerate(sizes, 1):
    chunk = clusters[pos:pos + sz]
    pos += sz
    name = f"p38_{i:02d}"
    items = []
    for row in chunk:
        idx = row["chunk_index_in_book"]
        item = {"row_id": row["decision_id"], "shipped_row": row}
        if idx - 1 in by_idx:
            item["prev_row"] = by_idx[idx - 1]
        if idx + 1 in by_idx:
            item["next_row"] = by_idx[idx + 1]
        items.append(item)
    doc = {"schema": "m8_ow2_p38_slice.v1", "batch": name, "book": "Prov",
           "attempt_id": f"ow2p38_{i:02d}_a1", "output_file": f"reviews/ow2p38_{i:02d}.json",
           "row_ids": [r["decision_id"] for r in chunk], "items": items}
    out = HERE / "slices" / f"slice_{name}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    slices.append({"slice": name, "rows": len(chunk), "sha256": sha(out)})
report["slices"] = slices
report["status"] = "READY"
(HERE / "frame_prov38.v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"status": "READY", "derived_size": n, "denominator_match": True,
                  "slices": [s["rows"] for s in slices], "provenance_lines": len(provenance_lines)}, indent=1))
