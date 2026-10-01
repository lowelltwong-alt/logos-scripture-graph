#!/usr/bin/env python3
"""Orchestrator: deterministic review-cluster plan for the Isa primaries
(full dual-blind per the gate ruling): canonical order, BALANCED sizes <=8
(the Song deviation from straight 8-slices, avoiding tiny tail clusters),
grouped into part-batches for the multi-session schedule."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (SPBOOK / "draft_rows_combined.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
ids = [r["decision_id"] for r in rows]
spans = {r["decision_id"]: r["span"] for r in rows}

N = len(ids)
n_clusters = (N + 7) // 8                    # 29 for 225
base = N // n_clusters                        # 7
extra = N - base * n_clusters                 # clusters getting base+1
clusters = []
i = 0
for c in range(n_clusters):
    size = base + (1 if c < extra else 0)
    chunk = ids[i:i + size]
    i += size
    clusters.append({
        "id": f"c{c + 1:02d}",
        "row_ids": chunk,
        "span": f"{spans[chunk[0]].split('-')[0]}-{spans[chunk[-1]].split('-')[1]}",
        "parts": sorted({x.split('-')[0] for x in chunk}),
    })
assert i == N and all(len(c["row_ids"]) <= 8 for c in clusters)

# session batches for the multi-session primaries schedule (gate ruling):
# grouped by the seven part-architecture divisions, cluster-aligned
out = {
    "built": "pre-primaries cluster plan (full dual-blind LF sonnet + OL opus per cluster, owner-ruled)",
    "rows_total": N, "clusters_total": n_clusters,
    "sizes": f"{extra} x {base + 1} + {n_clusters - extra} x {base}",
    "clusters": clusters,
}
(SPBOOK / "review_clusters.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"rows": N, "clusters": n_clusters,
                  "sizes": out["sizes"],
                  "first": clusters[0], "last": clusters[-1]}, ensure_ascii=False, indent=1))
