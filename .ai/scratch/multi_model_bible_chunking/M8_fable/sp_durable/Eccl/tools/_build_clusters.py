#!/usr/bin/env python3
"""Orchestrator: deterministic review-cluster plan for the FULL dual-blind
mesh (owner-ruled: no scoping) — all 85 rows, canonical order, clusters of
<=8. Writes SP/Eccl/review_clusters.json (distinct from the reserved
review_scope.json name of the unarmed atomic-isolation tool)."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (SPBOOK / "draft_rows_combined.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
clusters = []
for i in range(0, len(rows), 8):
    chunk = rows[i:i + 8]
    clusters.append({
        "id": f"c{i // 8 + 1:02d}",
        "row_ids": [r["writer_decision_id"] for r in chunk],
        "span_range": f"{chunk[0]['span'].split('-')[0]}-{chunk[-1]['span'].split('-')[1]}",
        "unit_types": sorted({r["unit_type"] for r in chunk}),
    })
out = {
    "built": "Phase 2 assembly, full dual-blind mesh (owner-ruled 2026-08-19; no scoping)",
    "corpus": "draft_rows_combined.jsonl",
    "rows_total": len(rows),
    "clusters": clusters,
}
(SPBOOK / "review_clusters.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"rows": len(rows), "clusters": len(clusters),
                  "plan": [{c['id']: f"{c['row_ids'][0]}..{c['row_ids'][-1]} ({c['span_range']})"} for c in clusters]},
                 ensure_ascii=False, indent=1))
