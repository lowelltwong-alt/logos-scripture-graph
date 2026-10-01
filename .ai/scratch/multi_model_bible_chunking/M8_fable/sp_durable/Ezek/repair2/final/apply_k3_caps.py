#!/usr/bin/env python3
"""Apply the #e17 K3 grade CAPS through the guarded harness's set_confidence operation (the same path step 1 and the
#e16/#e17 grade moves used). Plan: Ezek/repair2/final/k3_caps_plan.v1.json.

Refuses unless: the live rows are the named pre-image; every capped row's live grade is still the grade the plan
measured; every target is medium_low; the plan's own inputs still hash to what it recorded; and, with --expect-final,
the post-image equals a digest the caller pinned in advance. A row an adjudicator measured as NOT named in the plan is
excluded by --exclude and the exclusion is recorded in the receipt.

usage: python apply_k3_caps.py --pre <rows sha> [--exclude P01-012,...] [--expect-final <sha>] [--apply]
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
EXCLUDE = set((arg("--exclude") or "").split(",")) - {""}
plan = json.loads((HERE / "k3_caps_plan.v1.json").read_text(encoding="utf-8"))
if plan["section7_check_sha256"] != sha(EZ / "repair2" / "e16" / "section7_check.v1.json"):
    raise SystemExit("REFUSED: the section-7 check moved since the caps were planned; re-plan")
if plan["ruling_e17_sha256"] != sha(EZ / "author" / "e17" / "ruling_e17.json"):
    raise SystemExit("REFUSED: #e17 moved since the caps were planned; re-plan")
if sha(GA.ROWS) != PRE:
    raise SystemExit("REFUSED: live rows %s are not the named pre-image %s" % (sha(GA.ROWS), PRE))
rows = {r["decision_id"]: r for r in GA.load_rows()}
edits, skipped = [], []
for c in plan["caps"]:
    rid = c["row"]
    if rid in EXCLUDE:
        skipped.append({"row": rid, "why": "an adjudicator measured that the plan does not name this span or region"})
        continue
    cur = rows[rid].get("confidence")
    if cur != c["from"]:
        raise SystemExit("REFUSED: %s live grade %r is not the planned %r" % (rid, cur, c["from"]))
    if c["to"] != "medium_low":
        raise SystemExit("REFUSED: %s cap target %r is not medium_low" % (rid, c["to"]))
    edits.append({"row_id": rid, "field": "confidence", "op": "set_confidence", "expected_before": cur, "value": "medium_low",
                  "sweep": "confidence", "why": "K3 cap: the plan names this span or region as an open question (%s)" % str(c.get("why_named"))[:160]})
sim = GA.simulate_plan([("confidence", edits)], PRE)
print(json.dumps({"caps": len(edits), "skipped": skipped, "simulation_ok": sim.get("ok") if isinstance(sim, dict) else str(sim)[:200]}, indent=1))
if "--apply" not in sys.argv:
    raise SystemExit(0)
rec = GA.apply_edits(edits, PRE, "repair2_final_k3_grade_caps", ordered_count=len(edits), apply=True)
rec["k3_excluded"] = skipped
post = sha(GA.ROWS)
if arg("--expect-final") and post != arg("--expect-final"):
    raise SystemExit("POSTCHECK FAILED: post-image %s is not the pinned %s (the harness receipt records the write)" % (post, arg("--expect-final")))
with (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec.get(k) for k in ("sweep", "e18_parity_digits", "rows_touched", "preimage_sha256", "postimage_sha256_measured_from_disk")}, indent=1))
