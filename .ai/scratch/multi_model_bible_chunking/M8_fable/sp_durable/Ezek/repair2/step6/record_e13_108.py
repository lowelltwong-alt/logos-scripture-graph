#!/usr/bin/env python3
"""Queue E13-108: REPAIR-2 step 6 landed; the routed measured defects owed in a final remediation batch."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
before = Q.read_bytes()
if any(json.loads(l).get("id") == "E13-108" for l in before.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E13-108 already recorded")
if sha(EZ / "repair" / "rows_v7_cwo24.jsonl") != "097799dcebed1c4e2fdf5a5cdb40c2547309570902c4059d32fc44ced64dbf3f":
    raise SystemExit("REFUSED: rows are not at the step-6 post-image")
A = EZ / "author" / "repair2_step6"
routed = {h: json.loads((A / ("h%d_adjudication" % h) / "adjudication.json").read_text(encoding="utf-8")).get("routed") for h in (1, 2)}
delta = json.loads((EZ / "repair2" / "step6" / "suite_delta_after_6.json").read_text(encoding="utf-8"))
e = {
    "id": "E13-108", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
    "status": "DONE for step 6; the routed measured defects are OWED in a final remediation batch after step 7 and #e16",
    "headline": ("REPAIR-2 STEP 6 LANDED: the transport batch (#e15 Q8: 4+4 released items, 7 A16 weighings, 37:2's "
                 "disclosure, 5 onset drivers, 2 stale '20' figures), 26 routed step-5 repairs and 35 register items; four "
                 "blind Opus lanes and two Fable adjudications; 71 edits on 46 rows, rows a2e51d68 -> 097799dc; register "
                 "GREEN book-wide (43 -> 0), web_quotes 13 -> 11, triage 751 -> 715, no hard member gained a flag. The "
                 "lanes and adjudicators MEASURED further defects outside the orders and routed each with its exact repair."),
    "orchestrator_checks": ["every deliverable digest matches the agent's report",
                            "gate v5 (step-6 worklist) re-run by the orchestrator on each lane, each adjudication and the merge: all ALL_CLEAN, hard GREEN",
                            "the merge's gate candidate equals the harness's planned post-image (097799dc)",
                            "apply 71/71, protected fields unchanged, no row outside the proposal changed",
                            "suite delta against the post-member-fix report: %s" % delta.get("verdict")],
    "adjudications": {"h1": "39 discharged, 2 no-defect; 1 field from A, 23 from B, 6 reconciled, 5 identical, 1 left live; 15 routed",
                      "h2": "43 discharged; 8 from A, 19 from B, 2 reconciled, 7 identical; P11-009's strongest rival decided on measurement (the 46.20/46.21 transport seam); 14 routed"},
    "routed": routed,
    "lesson_candidates": [
        "a lane declined a routed wording ('no intra-verse position is sourceable from this witness') as false for the witness as a whole; routed repairs are re-measured, never transcribed",
        "the half-1 adjudicator hand-typed Hebrew as escape sequences in a draft and corrupted two accents; read-back caught it before any gate run (LOW)",
        "both step-6 half-2 lanes re-ranked P11-009's rival independently; the adjudicator decided it on measurement, not on the agreement",
    ],
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
after = Q.read_bytes()
assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
print("E13-108 appended; queue rows:", sum(1 for l in after.decode("utf-8").splitlines() if l.strip()))
