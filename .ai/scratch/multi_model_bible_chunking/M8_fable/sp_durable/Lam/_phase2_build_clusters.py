#!/usr/bin/env python3
"""Phase 2 step 1 (orchestrator, deterministic; the Jer _phase2_build_clusters.py lineage sized to Lamentations): build
the pre-primaries review cluster plan (full dual-blind LF sonnet + OL opus per cluster) and the per-row declared-FP flag
digest (the writer-report queues riding into review for pressure-testing). Contiguous book-order clusters of <=8 rows;
the row total is READ from draft_rows_combined.jsonl (never assumed); cluster sizes are the most even split into
ceil(N/8) clusters (every cluster 7 or 8 rows when N >= 14). Rows never straddle a poem seam by construction of the
writer parts; clusters may span parts (recorded). Outputs: review_clusters.json + flags_by_row.json."""
import json, math, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS_FILE = HERE / "draft_rows_combined.jsonl"
REPORT_FILE = HERE / "draft_rows_combined.jsonl.validator_report.json"

rows = [json.loads(l) for l in ROWS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
N = len(rows); assert N >= 8, f"unexpectedly few rows: {N}"
for i, r in enumerate(rows, 1):
    assert r["chunk_index_in_book"] == i, f"row {i} carries chunk_index_in_book {r['chunk_index_in_book']}"
    assert re.fullmatch(r"P\d{2}-\d{3}", r["writer_decision_id"]), r["writer_decision_id"]
    assert r["book"] == "Lam" and re.fullmatch(r"Lam\.\d+\.\d+-Lam\.\d+\.\d+", r["span"]), r["span"]
ids = [r["writer_decision_id"] for r in rows]
assert len(set(ids)) == N, "duplicate writer_decision_id"
k = math.ceil(N / 8); base, extra = divmod(N, k)
SIZES = [base + 1] * extra + [base] * (k - extra)
assert sum(SIZES) == N and max(SIZES) <= 8

clusters, pos = [], 0
for n, size in enumerate(SIZES, 1):
    chunk = rows[pos:pos + size]; pos += size
    parts = []
    for r in chunk:
        if r["writer_part"] not in parts: parts.append(r["writer_part"])
    clusters.append({"id": f"c{n:02d}", "row_ids": [r["writer_decision_id"] for r in chunk], "span": f"{chunk[0]['span'].split('-')[0]}-{chunk[-1]['span'].split('-')[1]}", "parts": parts})
assert pos == N
out = {"built": "pre-primaries cluster plan (full dual-blind LF sonnet + OL opus per cluster; Lam, m8-mesh-r3)", "rows_total": N, "clusters_total": len(clusters),
       "sizes": " + ".join(f"{SIZES.count(s)} x {s}" for s in sorted(set(SIZES), reverse=True)), "clusters": clusters}
(HERE / "review_clusters.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

rep = json.loads(REPORT_FILE.read_text(encoding="utf-8-sig"))
row_id_by_index = {r["chunk_index_in_book"]: r["writer_decision_id"] for r in rows}
span_by_row = {r["writer_decision_id"]: r["span"] for r in rows}
def find_row_id(entry):
    if isinstance(entry, dict):
        path = entry.get("path")
        if isinstance(path, str):
            m = re.match(r"\[(\d+)\]", path)
            if m:
                idx = int(m.group(1)) + 1
                if idx in row_id_by_index: return row_id_by_index[idx]
        for kk in ("writer_decision_id", "decision_id", "row_id", "row"):
            v = entry.get(kk)
            if isinstance(v, str) and re.fullmatch(r"P\d{2}-\d{3}", v): return v
            if isinstance(v, int) and v in row_id_by_index: return row_id_by_index[v]
        for v in entry.values():
            if isinstance(v, str):
                m = re.search(r"\bP\d{2}-\d{3}\b", v)
                if m and m.group(0) in span_by_row: return m.group(0)
    elif isinstance(entry, str):
        m = re.search(r"\bP\d{2}-\d{3}\b", entry)
        if m and m.group(0) in span_by_row: return m.group(0)
    return None
SOURCES = [("web_quotes", ["flags", "neighbor_only_warns"]), ("refs_mirror", ["flags", "orphan_ref_warns"]), ("mark_symmetry", ["flags", "warns"]),
           ("universals", ["flags"]), ("register", ["flags"]), ("citation_sweep", ["prose_dual_warns", "kq_web_quote_warns"])]
by_row, unresolved, total = {}, [], 0
for member, keys in SOURCES:
    for key in keys:
        for entry in rep.get(member, {}).get(key, []) or []:
            total += 1; rid = find_row_id(entry); item = {"member": member, "kind": key, "flag": entry}
            if rid: by_row.setdefault(rid, []).append(item)
            else: unresolved.append(item)
digest = {"built": "declared-FP queues from the writer-gate FLAGS members over draft_rows_combined.jsonl (writer-dispositioned, NOT orchestrator-accepted; primaries pressure-test the dispositions)",
          "total_flags": total, "rows_with_flags": len(by_row), "unresolved_count": len(unresolved), "by_row": {rid: by_row[rid] for rid in sorted(by_row)}, "unresolved": unresolved}
(HERE / "flags_by_row.json").write_text(json.dumps(digest, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"rows_total": N, "clusters_total": len(clusters), "sizes": out["sizes"], "cluster_rows": sum(len(c["row_ids"]) for c in clusters), "sizes_ok": all(len(c["row_ids"]) <= 8 for c in clusters),
                  "spans_first_last": [clusters[0]["span"], clusters[-1]["span"]], "flags_total": total, "rows_with_flags": len(by_row), "unresolved": len(unresolved)}, indent=1))
