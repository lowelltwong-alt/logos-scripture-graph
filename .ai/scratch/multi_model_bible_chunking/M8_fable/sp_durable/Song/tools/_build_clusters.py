#!/usr/bin/env python3
"""Orchestrator: deterministic review-cluster plan for the FULL dual-blind
mesh (owner-ruled: no scoping) — all 41 rows, canonical order, clusters of
<=8, BALANCED (41 straight-sliced by 8 would leave a 1-row tail cluster and
waste a primary pair; balanced sizes 7,7,7,7,7,6 keep every cluster a real
review unit). Writes SP/Song/review_clusters.json (distinct from the
reserved review_scope.json name of the unarmed atomic-isolation tool)."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (SPBOOK / "draft_rows_combined.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
n = len(rows)
n_clusters = (n + 7) // 8
base = n // n_clusters
rem = n % n_clusters
sizes = [base + 1 if i < rem else base for i in range(n_clusters)]
assert sum(sizes) == n and max(sizes) <= 8

clusters = []
pos = 0
for i, size in enumerate(sizes):
    chunk = rows[pos:pos + size]
    pos += size
    clusters.append({
        "id": f"c{i + 1:02d}",
        "row_ids": [r["writer_decision_id"] for r in chunk],
        "span_range": f"{chunk[0]['span'].split('-')[0]}-{chunk[-1]['span'].split('-')[1]}",
        "unit_types": sorted({r["unit_type"] for r in chunk}),
    })
out = {
    "built": "Phase 2 assembly, full dual-blind mesh (owner-ruled 2026-08-25; no scoping; balanced <=8 clusters)",
    "corpus": "draft_rows_combined.jsonl",
    "rows_total": n,
    "clusters": clusters,
}
(SPBOOK / "review_clusters.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"rows": n, "clusters": len(clusters), "sizes": sizes,
                  "plan": [{c['id']: f"{c['row_ids'][0]}..{c['row_ids'][-1]} ({c['span_range']})"} for c in clusters]},
                 ensure_ascii=False, indent=1))
