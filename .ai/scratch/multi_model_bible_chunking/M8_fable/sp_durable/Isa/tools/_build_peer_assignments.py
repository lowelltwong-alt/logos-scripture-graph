"""Build the deterministic Isaiah peer-wave assignment table (m8-mesh-r3).

Scope per the 2026-08-26 owner rulings + the session-3 cursor:
  - ALL rows challenged by >=1 primary role (202 rows), grouped by cluster;
  - a ~10% deterministic sample of the 23 both-supported rows: every 10th of
    the sorted list -> P01-009, P10-010, P18-003;
  - one peer per ~2 clusters => 15 peers (p01..p14 = 2 clusters each in
    canonical order, p15 = c29);
  - <=8 rulings per attempt id: r1 stops at 8 in canonical order and defers
    the remainder (deferred_row_ids) to a follow-on attempt peer_isa_pNN_r2
    (output peer_NN_r2.json) — the Song c05_PEER_r2 precedent.

Run from SP/Isa/tools. Writes ../peer_assignments.json. Deterministic.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SP_ISA = os.path.dirname(HERE)

with open(os.path.join(SP_ISA, "peer_scope_table.json"), encoding="utf-8") as f:
    scope = json.load(f)
with open(os.path.join(SP_ISA, "review_clusters.json"), encoding="utf-8") as f:
    rc = json.load(f)

tab = scope["table"]
clusters = {c["id"]: c for c in rc["clusters"]}
cluster_ids = sorted(clusters, key=lambda x: int(x[1:]))
assert len(cluster_ids) == 29

# challenged rows per cluster, canonical (row-id) order
challenged = {cid: [] for cid in cluster_ids}
supported_both = []
for rid in sorted(tab):
    e = tab[rid]
    lf, ol = e["LF"]["verdict"], e["OL"]["verdict"]
    src = None
    if lf == "challenge" and ol == "challenge":
        src = "both"
    elif lf == "challenge":
        src = "LF"
    elif ol == "challenge":
        src = "OL"
    if src:
        challenged[e["cluster"]].append({"row_id": rid, "source": src})
    if lf == "support" and ol == "support":
        supported_both.append(rid)

sb = sorted(supported_both)
sample = [sb[i] for i in range(0, len(sb), 10)]  # deterministic ~10%

peers = []
for i in range(15):
    nn = f"{i + 1:02d}"
    cl = cluster_ids[2 * i:2 * i + 2]  # p15 gets just c29
    rows = []
    for cid in cl:
        rows.extend(challenged[cid])
    sample_rows = [r for r in sample if tab[r]["cluster"] in cl]
    r1 = [r["row_id"] for r in rows[:8]]
    deferred = [r["row_id"] for r in rows[8:]]
    peers.append({
        "peer": nn,
        "attempt_id_r1": f"peer_isa_p{nn}_r1",
        "attempt_id_r2": f"peer_isa_p{nn}_r2" if deferred else None,
        "clusters": cl,
        "spans": {cid: clusters[cid]["span"] for cid in cl},
        "packets": [f"{cid}_{role}.json" for cid in cl for role in ("LF", "OL")],
        "challenged_rows": rows,
        "n_challenged": len(rows),
        "r1_row_ids": r1,
        "expected_deferred_row_ids": deferred,
        "supported_sample_row_ids": sample_rows,
        "output_r1": f"peer_{nn}.json",
        "output_r2": f"peer_{nn}_r2.json" if deferred else None,
    })

out = {
    "schema": "isa_peer_assignments.v1",
    "scope_rule": "challenged_any + deterministic 10pct of supported_both (every 10th sorted)",
    "peer_model": "claude-opus-5",
    "total_challenged_rows": sum(p["n_challenged"] for p in peers),
    "supported_sample": sample,
    "peers": peers,
}
dst = os.path.join(SP_ISA, "peer_assignments.json")
with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote", dst)
print("total challenged:", out["total_challenged_rows"], "sample:", sample)
for p in peers:
    print(p["peer"], p["clusters"], "challenged", p["n_challenged"],
          "r1", len(p["r1_row_ids"]), "deferred", len(p["expected_deferred_row_ids"]),
          "sample", p["supported_sample_row_ids"])
