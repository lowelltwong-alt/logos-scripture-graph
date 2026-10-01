#!/usr/bin/env python3
"""Phase 2 step 1 (orchestrator, deterministic): build the pre-primaries review
cluster plan (full dual-blind LF sonnet + OL opus per cluster, owner-ruled Q2)
and the per-row declared-FP flag digest (the writer-report queues riding into
review for pressure-testing). Isa lineage shape: contiguous book-order clusters
of 8 with a 7-row tail; <=8 decisions per attempt id binds size.

276 rows -> 35 clusters: c01..c31 x 8 rows + c32..c35 x 7 rows = 248 + 28.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS_FILE = HERE / "draft_rows_combined.jsonl"
REPORT_FILE = HERE / "draft_rows_combined.jsonl.validator_report.json"

rows = [json.loads(l) for l in ROWS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
assert len(rows) == 276, f"expected 276 rows, got {len(rows)}"
# order + renumbering assertions (assembly renumbered 1..276)
for i, r in enumerate(rows, 1):
    assert r["chunk_index_in_book"] == i, f"row {i} carries chunk_index_in_book {r['chunk_index_in_book']}"
    assert re.fullmatch(r"P\d{2}-\d{3}", r["writer_decision_id"]), r["writer_decision_id"]
ids = [r["writer_decision_id"] for r in rows]
assert len(set(ids)) == 276, "duplicate writer_decision_id"

SIZES = [8] * 31 + [7] * 4
assert sum(SIZES) == 276

clusters = []
pos = 0
for n, size in enumerate(SIZES, 1):
    chunk = rows[pos:pos + size]
    pos += size
    span_start = chunk[0]["span"].split("-")[0]
    span_end = chunk[-1]["span"].split("-")[1]
    parts = []
    for r in chunk:
        if r["writer_part"] not in parts:
            parts.append(r["writer_part"])
    clusters.append({
        "id": f"c{n:02d}",
        "row_ids": [r["writer_decision_id"] for r in chunk],
        "span": f"{span_start}-{span_end}",
        "parts": parts,
    })
assert pos == 276

out = {
    "built": "pre-primaries cluster plan (full dual-blind LF sonnet + OL opus per cluster, owner-ruled)",
    "rows_total": 276,
    "clusters_total": len(clusters),
    "sizes": "31 x 8 + 4 x 7",
    "clusters": clusters,
}
(HERE / "review_clusters.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- declared-FP flag digest (queues from the writer-gate FLAGS members) ----
rep = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
row_id_by_index = {r["chunk_index_in_book"]: r["writer_decision_id"] for r in rows}
span_by_row = {r["writer_decision_id"]: r["span"] for r in rows}

def find_row_id(entry):
    """Resolve a flag entry to a writer_decision_id via any id-ish key."""
    if isinstance(entry, dict):
        # checker "path" fields carry a 0-based row index into the JSONL: "[176].boundary_rationale"
        path = entry.get("path")
        if isinstance(path, str):
            m = re.match(r"\[(\d+)\]", path)
            if m:
                idx = int(m.group(1)) + 1  # 0-based file line -> 1-based chunk_index_in_book
                if idx in row_id_by_index:
                    return row_id_by_index[idx]
        for k in ("writer_decision_id", "decision_id", "row_id", "row"):
            v = entry.get(k)
            if isinstance(v, str) and re.fullmatch(r"P\d{2}-\d{3}", v):
                return v
            if isinstance(v, int) and v in row_id_by_index:
                return row_id_by_index[v]
        for v in entry.values():
            if isinstance(v, str):
                m = re.search(r"\bP\d{2}-\d{3}\b", v)
                if m and m.group(0) in span_by_row:
                    return m.group(0)
    elif isinstance(entry, str):
        m = re.search(r"\bP\d{2}-\d{3}\b", entry)
        if m and m.group(0) in span_by_row:
            return m.group(0)
    return None

SOURCES = [
    ("web_quotes", ["flags", "neighbor_only_warns"]),
    ("refs_mirror", ["flags", "orphan_ref_warns"]),
    ("mark_symmetry", ["flags", "warns"]),
    ("universals", ["flags"]),
    ("register", ["flags"]),
    ("citation_sweep", ["prose_dual_warns", "kq_web_quote_warns"]),
]
by_row = {}
unresolved = []
total = 0
for member, keys in SOURCES:
    for key in keys:
        for entry in rep.get(member, {}).get(key, []) or []:
            total += 1
            rid = find_row_id(entry)
            item = {"member": member, "kind": key, "flag": entry}
            if rid:
                by_row.setdefault(rid, []).append(item)
            else:
                unresolved.append(item)

digest = {
    "built": "declared-FP queues from the writer-gate FLAGS members over draft_rows_combined.jsonl "
             "(writer-dispositioned, NOT orchestrator-accepted; primaries pressure-test the dispositions)",
    "total_flags": total,
    "rows_with_flags": len(by_row),
    "unresolved_count": len(unresolved),
    "by_row": {rid: by_row[rid] for rid in sorted(by_row)},
    "unresolved": unresolved,
}
(HERE / "flags_by_row.json").write_text(json.dumps(digest, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- verification census ----
cluster_rows = sum(len(c["row_ids"]) for c in clusters)
flagged_in_clusters = sum(1 for rid in by_row if rid in span_by_row)
print(json.dumps({
    "clusters_total": len(clusters),
    "cluster_rows": cluster_rows,
    "sizes_ok": all(len(c["row_ids"]) <= 8 for c in clusters),
    "spans_first_last": [clusters[0]["span"], clusters[-1]["span"]],
    "flags_total": total,
    "rows_with_flags": len(by_row),
    "unresolved": len(unresolved),
    "flagged_rows_resolve_to_corpus": flagged_in_clusters == len(by_row),
}, indent=1))
