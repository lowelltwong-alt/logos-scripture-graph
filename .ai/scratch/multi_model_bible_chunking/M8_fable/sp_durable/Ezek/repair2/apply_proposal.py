#!/usr/bin/env python3
"""Apply a LANDED adjudication proposal through the guarded harness. Simulate by default. Step-agnostic.

Edits are GENERATED from the proposal: every changed field becomes a `set` carrying the live value as expected_before
(prose strings, full refs lists and signals alike), so an edit whose target moved since the proposal was written is
refused by the harness. The proposal's digest and the rows' preimage are pinned on the command line. After a real
apply the post-image is compared FIELD BY FIELD to the proposal and every row the proposal does not name must be
byte-identical; the receipt is appended to the author sweep receipts.

usage: python apply_proposal.py --proposal <path> --proposal-sha <hex> --pre <rows sha> --sweep <name> [--apply]
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
sys.path.insert(0, str(EZ / "repair2" / "session_910cbe15" / "ezek_aw"))
import guarded_apply as GA                                                     # noqa: E402

ALLOWED = {"boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess",
           "boundary_evidence_refs", "observed_substrate_signals"}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

ap = argparse.ArgumentParser()
ap.add_argument("--proposal", required=True)
ap.add_argument("--proposal-sha", required=True)
ap.add_argument("--pre", required=True)
ap.add_argument("--sweep", required=True)
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()
if sha(a.proposal) != a.proposal_sha:
    raise SystemExit("REFUSED: the proposal's digest is not the pinned one")
if Path(GA.ROWS) != EZ / "repair" / "rows_v7_cwo24.jsonl":
    raise SystemExit("REFUSED: the harness points at another rows file")
prop = json.loads(Path(a.proposal).read_text(encoding="utf-8"))
live = {r["decision_id"]: r for r in GA.load_rows()}
edits, refused = [], []
for rid, fields in sorted(prop.items()):
    if rid not in live:
        refused.append((rid, "no such row"))
        continue
    for f, v in fields.items():
        if f not in ALLOWED:
            refused.append((rid, "field %s is not writable here" % f))
        elif v != live[rid].get(f):
            edits.append({"row_id": rid, "field": f, "op": "set", "expected_before": live[rid].get(f), "value": v,
                          "sweep": a.sweep})
if refused:
    raise SystemExit("REFUSED: %r" % refused)
summary = {"edits": len(edits), "rows": len({e["row_id"] for e in edits}),
           "by_field": {f: sum(1 for e in edits if e["field"] == f) for f in sorted({e["field"] for e in edits})}}
sim = GA.simulate_plan([(a.sweep, edits)], a.pre)
print(json.dumps({"plan": summary, "simulation_ok": sim["ok"], "final_if_applied": sim.get("final_digest_if_applied")},
                 indent=1))
if not sim["ok"] or not a.apply:
    raise SystemExit(0 if sim["ok"] else 1)
rec = GA.apply_edits(edits, a.pre, a.sweep, ordered_count=len(edits), apply=True)
post = {r["decision_id"]: r for r in GA.load_rows()}
mismatch = [(rid, f) for rid, fs in prop.items() for f, v in fs.items() if post[rid].get(f) != v]
moved = [rid for rid in live if rid not in prop and live[rid] != post[rid]]
if mismatch or moved:
    raise SystemExit("POSTCHECK FAILED - differing %r; rows outside the proposal changed %r (the harness keeps its "
                     "pre-image backup)" % (mismatch, moved))
rec.update({"proposal": {"file": str(a.proposal), "sha256": a.proposal_sha}, "plan": summary,
            "postcheck": "every proposed field equals the post-image; no row outside the proposal changed",
            "recorded_at": datetime.now(timezone.utc).isoformat()})
with (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec.get(k) for k in ("sweep", "e18_parity_digits", "rows_touched", "preimage_sha256",
                                          "postimage_sha256_measured_from_disk", "postcheck")}, indent=1))
