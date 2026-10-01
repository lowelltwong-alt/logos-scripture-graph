#!/usr/bin/env python3
"""Apply the planned grade moves (#e16, as superseded by #e17 and settled by the section-7 and T-3 checks) through the
guarded harness's set_confidence operation - the same path REPAIR-2 step 1 used. apply_proposal.py refuses 'confidence'
by design, so grades never ride in a prose proposal.

Refuses unless: the live rows are the named pre-image; every move's expected_before is the live grade; every value is on
the four-value scale; the simulation is clean; and, with --expect-final, the post-image equals the digest the suite was
run on. Appends the harness receipt to the sweep receipts file.

usage: python apply_grade_moves.py --pre <rows sha> [--expect-final <sha>] [--apply]
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "repair2" / "session_910cbe15" / "ezek_aw"))
import guarded_apply as GA                                                     # noqa: E402

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
arg = lambda n: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else None      # noqa: E731
PRE = arg("--pre")
plan = json.loads((HERE / "mechanical" / "plan.json").read_text(encoding="utf-8"))
rows = {r["decision_id"]: r for r in GA.load_rows()}
if sha(GA.ROWS) != PRE:
    raise SystemExit("REFUSED: live rows %s are not the named pre-image %s" % (sha(GA.ROWS), PRE))
edits = []
for g in plan["grade_moves"]:
    cur = rows[g["row"]].get("confidence")
    if cur != g["from"]:
        raise SystemExit("REFUSED: %s live grade %r is not the move's from %r" % (g["row"], cur, g["from"]))
    edits.append({"row_id": g["row"], "field": "confidence", "op": "set_confidence", "expected_before": cur, "value": g["to"],
                  "sweep": "confidence", "why": "grade move: %s" % str(g.get("ground"))[:200]})
sim = GA.simulate_plan([("confidence", edits)], PRE)
print(json.dumps({"edits": len(edits), "simulation": {k: sim[k] for k in sim if k in ("ok", "final_sha256", "problems")} if isinstance(sim, dict) else str(sim)[:300]}, indent=1))
if "--apply" not in sys.argv:
    raise SystemExit(0)
rec = GA.apply_edits(edits, PRE, "repair2_final_grade_moves_e16_e17", ordered_count=len(edits), apply=True)
post = sha(GA.ROWS)
if arg("--expect-final") and post != arg("--expect-final"):
    raise SystemExit("POSTCHECK FAILED: post-image %s is not the suite-tested candidate %s (the harness receipt records the write)" % (post, arg("--expect-final")))
with (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec.get(k) for k in ("sweep", "e18_parity_digits", "rows_touched", "preimage_sha256", "postimage_sha256_measured_from_disk")}, indent=1))
