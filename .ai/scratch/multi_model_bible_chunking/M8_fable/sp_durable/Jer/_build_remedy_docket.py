#!/usr/bin/env python3
"""Deterministic remedy consolidation for the Jer r3 peer round (orchestrator-run).

Builds remedy_docket.v1.json from peer_scope.json + all 35 verified peer packets:
per-row docket (uphold/refine remedies as author-wave work orders, grounds carried
verbatim because peer new-findings ride inside them), refuted list, escalations,
sample-lane defects, corpus-wide-order candidates (E-18 law: scope markers scanned
mechanically; the orchestrator adjudicates the explicit list, and CWO-1 from the
writer-wave census is seeded unconditionally), and per-packet sha256 integrity.

Assertions pin: every scope-challenged row ruled exactly once; vocabulary; remedy
present on every uphold/refine; canonical corpus ordering in the docket."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCOPE = json.loads((HERE / "peer_scope.json").read_text(encoding="utf-8"))

CWO_MARKERS = ("book-wide", "bookwide", "whole-book", "corpus", "all rows",
               "every row", "across the book", "across all", "book level",
               "book-level", "all 276")

CWO1 = {
    "id": "CWO-1",
    "origin": "writer-wave census (ngram7 book-level RED), carried per E-18 law until executed",
    "order": ("book-wide variation-order pass over the mandated disclosure boilerplate "
              "(the 23 ngram7 grams >=10 rows; 4+ distinct formulations per disclosure "
              "class, pooled pre-check) - assign at author wave; verify by ngram7 re-run "
              "over the revised corpus"),
    "status": "pending_author_wave",
}

rows_order = []          # canonical row order from scope iteration
docket = {}              # row_id -> list of ruling entries
refuted = []
escalations = []
sample_defects = []
cwo_candidates = []
packet_hashes = {}
tally = {"uphold": 0, "refine": 0, "refute": 0, "escalate": 0}

challenged = SCOPE["challenged"]

for peer in SCOPE["peers"]:
    pid = peer["peer_id"]
    for i, split in enumerate(peer["attempt_splits"]):
        fname = peer["output"] if i == 0 else peer["followon_outputs"][i - 1]
        path = HERE / fname
        raw = path.read_bytes()
        packet_hashes[fname] = hashlib.sha256(raw).hexdigest()
        pk = json.loads(raw.decode("utf-8"))
        assert pk["attempt_id"] == split["attempt_id"], fname
        rulings = pk["rulings"]
        ruled_ids = [r["row_id"] for r in rulings]
        assert ruled_ids == split["r1_row_ids"], f"{fname}: ruling order != scope split"
        for r in rulings:
            rid = r["row_id"]
            assert rid in challenged, f"{fname}: {rid} not a challenged row"
            assert rid not in docket, f"{rid} ruled twice"
            assert r["ruling"] in ("uphold", "refine", "refute", "escalate"), rid
            tally[r["ruling"]] += 1
            if r["ruling"] in ("uphold", "refine"):
                assert r.get("remedy"), f"{rid}: {r['ruling']} without remedy"
            entry = {
                "cluster": r.get("cluster"),
                "peer_file": fname,
                "attempt_id": pk["attempt_id"],
                "source": r.get("source"),
                "ruling": r["ruling"],
                "severity_final": r.get("severity_final"),
                "challenge_claim": r.get("challenge_claim"),
                "grounds": r.get("grounds"),
                "remedy": r.get("remedy"),
            }
            docket[rid] = entry
            rows_order.append(rid)
            if r["ruling"] == "refute":
                refuted.append({"row_id": rid, "peer_file": fname,
                                "grounds": r.get("grounds")})
            if r["ruling"] == "escalate":
                escalations.append({"row_id": rid, "peer_file": fname,
                                    "grounds": r.get("grounds")})
            blob = " ".join(str(r.get(k) or "") for k in
                            ("remedy", "grounds")).lower()
            hits = [m for m in CWO_MARKERS if m in blob]
            if hits and r["ruling"] in ("uphold", "refine"):
                cwo_candidates.append({"row_id": rid, "peer_file": fname,
                                       "markers": hits,
                                       "remedy": r.get("remedy")})
        for s in pk.get("supported_sample") or []:
            if s.get("result") == "defect_found":
                sample_defects.append({"row_id": s["row_id"], "peer_file": fname,
                                       "notes": s.get("notes")})

assert set(docket) == set(challenged), (
    f"coverage mismatch: {len(docket)} ruled vs {len(challenged)} challenged; "
    f"missing {sorted(set(challenged) - set(docket))[:5]} "
    f"extra {sorted(set(docket) - set(challenged))[:5]}")
assert len(rows_order) == len(challenged) == 216
assert sum(tally.values()) == 216

def rowkey(rid):
    part, num = rid.split("-")
    return (int(part[1:]), int(num))

ordered = sorted(docket, key=rowkey)

out = {
    "schema": "jer_remedy_docket.v1",
    "built_from": "peer_scope.json + 35 verified peer packets (18 a1 + 17 a2)",
    "totals": {"rulings": 216, **tally,
               "work_orders": tally["uphold"] + tally["refine"],
               "refuted": len(refuted), "escalations": len(escalations),
               "sample_defects": len(sample_defects),
               "cwo_candidates": len(cwo_candidates)},
    "corpus_wide_orders": [CWO1],
    "cwo_candidates_for_orchestrator_adjudication": cwo_candidates,
    "docket": {rid: docket[rid] for rid in ordered},
    "refuted": refuted,
    "escalations": escalations,
    "sample_lane_defects": sample_defects,
    "packet_sha256": packet_hashes,
}
(HERE / "remedy_docket.v1.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"docket": "BUILT", "totals": out["totals"],
                  "cwo_candidates": [(c["row_id"], c["markers"]) for c in cwo_candidates],
                  "sample_defects": [d["row_id"] for d in sample_defects],
                  "refuted": [r["row_id"] for r in refuted]}, indent=1))
