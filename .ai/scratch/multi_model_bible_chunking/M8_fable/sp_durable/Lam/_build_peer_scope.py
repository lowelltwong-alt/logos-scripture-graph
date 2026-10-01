#!/usr/bin/env python3
"""Build the r3-scoped peer round plan for Lamentations (orchestrator, deterministic; the Jer peer_scope.json shape):
challenged rows (any challenge in either primary packet, with sources + severities), a supported-row sample (every
Nth supported row in canonical order from index K), peers = contiguous cluster groups (CLUSTERS_PER_PEER), attempt
splits of <=8 challenged rows per attempt id (follow-on attempts for the deferred rows), outputs reviews/peer_NN.json
(+ _rN follow-ons). Every packet is read by exact name from review_clusters.json; sha256 per packet recorded.
Usage: _build_peer_scope.py [--clusters-per-peer 2] [--sample-every 10] [--sample-from 4]"""
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
A = sys.argv[1:]
CPP = int(A[A.index("--clusters-per-peer") + 1]) if "--clusters-per-peer" in A else 2
EVERY = int(A[A.index("--sample-every") + 1]) if "--sample-every" in A else 10
FROM = int(A[A.index("--sample-from") + 1]) if "--sample-from" in A else 4
clusters = json.loads((HERE / "review_clusters.json").read_text(encoding="utf-8"))["clusters"]
rows = [json.loads(l) for l in (HERE / "draft_rows_combined.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
order = [r["writer_decision_id"] for r in rows]
challenged, supported, shas = {}, [], {}
for c in clusters:
    for role in ("LF", "OL"):
        f = HERE / "reviews" / f"rev_{role}_{c['id']}.json"; assert f.is_file(), f"missing {f}"
        shas[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
        pk = json.loads(f.read_text(encoding="utf-8-sig"))
        for it in pk["items"]:
            if it.get("verdict") == "challenge":
                e = challenged.setdefault(it["row_id"], {"cluster": c["id"], "sources": [], "severities": []})
                if role not in e["sources"]: e["sources"].append(role)
                if it.get("severity") and it["severity"] not in e["severities"]: e["severities"].append(it["severity"])
supported = [r for r in order if r not in challenged]
sample = supported[FROM::EVERY]
peers, n = [], 0
for i in range(0, len(clusters), CPP):
    grp = clusters[i:i + CPP]; n += 1; pid = f"peer_{n:02d}"
    ch_rows = [r for c in grp for r in c["row_ids"] if r in challenged]
    smp = [r for c in grp for r in c["row_ids"] if r in sample]
    splits, k = [], 0
    while k < len(ch_rows) or not splits:
        chunk = ch_rows[k:k + 8]; k += 8
        splits.append({"attempt_id": f"lam_{pid}_a{len(splits) + 1}", "r1_row_ids": chunk, "deferred_row_ids": ch_rows[k:]})
    peers.append({"peer_id": pid, "clusters": [c["id"] for c in grp], "packet_files": [f"rev_{role}_{c['id']}.json" for c in grp for role in ("LF", "OL")],
                  "challenged_row_count": len(ch_rows), "attempt_splits": splits, "sample_row_ids": smp, "output": f"reviews/{pid}.json",
                  "followon_outputs": [f"reviews/{pid}_r{j + 2}.json" for j in range(len(splits) - 1)]})
out = {"schema": "lam_peer_scope.v1", "totals": {"rows": len(rows), "challenged_rows": len(challenged), "supported_rows": len(supported), "sample_rows": len(sample), "peers": len(peers), "total_attempts": sum(len(p["attempt_splits"]) for p in peers)},
       "sample_rule": f"supported rows in canonical corpus order, every {EVERY}th from index {FROM}", "challenged": {r: challenged[r] for r in order if r in challenged}, "sample": sample, "peers": peers, "packet_sha256": shas}
(HERE / "peer_scope.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8"); print(json.dumps({"totals": out["totals"], "peers": [(p["peer_id"], p["clusters"], p["challenged_row_count"], len(p["attempt_splits"])) for p in peers]}, indent=1))
