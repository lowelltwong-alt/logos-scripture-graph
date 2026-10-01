#!/usr/bin/env python3
"""REPAIR-2 step 2: apply the landed Fable adjudication through the guarded harness. Simulate by default.

Edits are GENERATED from the landed proposal, never hand-written: a prose field becomes a `set` carrying the live
value as expected_before; a refs list becomes one `append_ref` per new entry carrying the live list as expected_before.
The harness appends at the END, so the build REFUSES unless each proposed list is exactly the live list followed by
the new entries - an interleaved entry would otherwise be silently reordered.

After a real apply, the post-image is compared FIELD BY FIELD to the proposal, and the step's receipt is appended to
the author sweep receipts beside step 1's.

usage: python apply_step2.py            (simulate)
       python apply_step2.py --apply
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HARNESS_DIR = EZ / "repair2" / "session_910cbe15" / "ezek_aw"
sys.path.insert(0, str(HARNESS_DIR))
import guarded_apply as GA                                                     # noqa: E402

HERE = Path(__file__).resolve().parent
PROPOSAL = HERE / "adjudication_a1" / "proposal.json"
PROPOSAL_SHA = "dfbeab44f318802339037a424fcf43484b75595910f55d6431a121a88a9c414f"
PRE = "1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425"
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
REFS = "boundary_evidence_refs"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

if sha(PROPOSAL) != PROPOSAL_SHA:
    raise SystemExit("REFUSED: the landed proposal's digest moved")
if Path(GA.ROWS) != EZ / "repair" / "rows_v7_cwo24.jsonl":
    raise SystemExit("REFUSED: the harness points at a different rows file: %s" % GA.ROWS)
prop = json.loads(PROPOSAL.read_text(encoding="utf-8"))
live = {r["decision_id"]: r for r in GA.load_rows()}

edits, refused = [], []
for rid, fields in sorted(prop.items()):
    if rid not in live:
        refused.append((rid, "no such row"))
        continue
    for f, v in fields.items():
        if f in PROSE:
            if v == live[rid].get(f):
                continue
            edits.append({"row_id": rid, "field": f, "op": "set", "expected_before": live[rid].get(f), "value": v,
                          "sweep": "repair2_step2_grounds"})
        elif f == REFS:
            old = list(live[rid].get(REFS) or [])
            if list(v[:len(old)]) != old:
                refused.append((rid, "the proposed refs list is not the live list followed by new entries - an "
                                     "append-at-end apply would reorder it"))
                continue
            for e in v[len(old):]:
                edits.append({"row_id": rid, "field": REFS, "op": "append_ref", "expected_before": old, "value": e,
                              "sweep": "repair2_step2_grounds"})
        else:
            refused.append((rid, "field %s is not one step 2 may write" % f))
if refused:
    raise SystemExit("REFUSED before simulation: %r" % refused)

summary = {"edits": len(edits), "set": sum(1 for e in edits if e["op"] == "set"),
           "append_ref": sum(1 for e in edits if e["op"] == "append_ref"),
           "rows": len({e["row_id"] for e in edits})}
sim = GA.simulate_plan([("repair2_step2_grounds", edits)], PRE)
print(json.dumps({"plan": summary, "simulation_ok": sim["ok"], "final_if_applied": sim.get("final_digest_if_applied")},
                 indent=1))
if not sim["ok"]:
    raise SystemExit("REFUSED at simulation")
if "--apply" not in sys.argv:
    raise SystemExit(0)

rec = GA.apply_edits(edits, PRE, "repair2_step2_grounds", ordered_count=len(edits), apply=True)
post = {r["decision_id"]: r for r in GA.load_rows()}
mismatch = []
for rid, fields in prop.items():
    for f, v in fields.items():
        if post[rid].get(f) != v:
            mismatch.append((rid, f))
untouched_changed = [rid for rid in live if rid not in prop and live[rid] != post[rid]]
if mismatch or untouched_changed:
    raise SystemExit("POSTCHECK FAILED - fields differing from the proposal %r; rows changed that the proposal did not "
                     "name %r. The harness keeps its pre-image backup for rollback." % (mismatch, untouched_changed))
rec.update({"batch": "REPAIR-2 step 2: grounds, from the Fable adjudication of two blind author lanes",
            "proposal": {"file": "Ezek/repair2/step2_reconciliation/adjudication_a1/proposal.json", "sha256": PROPOSAL_SHA},
            "attempt": "ezek_repair2_step2_adjudication_a1#e1", "plan": summary,
            "postcheck": "every proposed field equals the post-image; no row outside the proposal changed",
            "closes_the_step1_obligation": ("the nine rows whose grades moved at step 1 now state the ground for the "
                                            "grade they carry, as #e15 ordered"),
            "recorded_at": datetime.now(timezone.utc).isoformat()})
with (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec.get(k) for k in ("sweep", "e18_parity_digits", "rows_touched", "preimage_sha256",
                                          "postimage_sha256_measured_from_disk", "postcheck")}, indent=1))
