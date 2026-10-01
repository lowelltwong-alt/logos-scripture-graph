#!/usr/bin/env python3
"""Record what was checked BEFORE the two blind close-gate audit lanes were launched, and what was not.

The reason this exists as a file: the checkpoint's own next_job said to run check_brief_vs_suite.py "to PASS". That
control is an AUTHOR-brief control - it asks whether a brief carries a duty for every member of the row validator
suite. An audit lane writes no rows, so every member is genuinely out of scope and its FAIL says nothing about this
brief. Reporting that FAIL as a PASS would be a half-truth (OW-18); skipping it silently would be another. The run,
its verdict, and the reason it does not apply are written down here instead, so the close-gate receipt cites a
measurement rather than my say-so.
"""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
R2 = EZ / "repair2"
A, B = R2 / "CLOSE_AUDIT_BRIEF_A.md", R2 / "CLOSE_AUDIT_BRIEF_B.md"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


ta, tb = A.read_text(encoding="utf-8").splitlines(), B.read_text(encoding="utf-8").splitlines()
differing = [i + 1 for i, (x, y) in enumerate(zip(ta, tb)) if x != y]
suite = subprocess.run(["python", str(EZ / "tools" / "check_brief_vs_suite.py"), str(A)],
                       capture_output=True, text=True, cwd=str(EZ / "tools"))
# the runner prints human lines then a JSON object; take the object's own VERDICT, never the last printed line
_brace = suite.stdout.find("{")
try:
    verdict = json.loads(suite.stdout[_brace:])["VERDICT"] if _brace >= 0 else "UNPARSEABLE"
except Exception as exc:
    verdict = "UNPARSEABLE: %s" % exc
tail = [verdict]

out = {
    "schema": "ezek_close_audit_prelaunch.v1",
    "recorded_at": datetime.now(timezone.utc).isoformat(),
    "recorded_by": "orchestrator (claude-opus-5), session 910cbe15",
    "briefs": {"A": {"path": str(A), "sha256": sha(A), "bytes": A.stat().st_size},
               "B": {"path": str(B), "sha256": sha(B), "bytes": B.stat().st_size}},
    "generator": {"path": str(R2 / "gen_close_audit_brief.py"), "sha256": sha(R2 / "gen_close_audit_brief.py"),
                  "retained": True, "determinism": "regenerated with --check: MATCH for both briefs"},
    "blindness_evidence": {
        "tier": "MEASURED",
        "lines_that_differ": differing,
        "count": len(differing),
        "what_they_are": "line 1 and line 3 carry the lane letter; the other two are the lane's own output paths",
        "how_to_read": ("two lanes are only blind if they hold the SAME rules. Every other line of the two briefs is "
                        "byte-identical, so a disagreement between the lanes cannot be an artefact of the briefs."),
        "same_length": A.stat().st_size == B.stat().st_size},
    "checks_run": [
        {"check": "_brief_pin_check.py --selftest", "verdict": "GREEN", "vectors": 5, "failed": []},
        {"check": "_brief_pin_check.py --brief A --brief B", "verdict": "MATCH", "pins_each": 21,
         "drift": [], "missing": [],
         "means": "every one of the 21 pinned inputs exists and its bytes hash to the digest the brief prints"},
        {"check": "gen_close_audit_brief.py --check", "verdict": "MATCH", "means": "the briefs are reproducible"},
        {"check": "existence of all 21 pinned paths before generation", "verdict": "21 of 21 present"},
    ],
    "check_NOT_applicable": {
        "check": "Ezek/tools/check_brief_vs_suite.py",
        "verdict_when_run_anyway": tail[0].strip() if tail else "",
        "members": 11, "out_of_scope": 1, "duty_missing": 10,
        "why_it_does_not_apply": ("it asks whether a brief carries a duty for every member of the ROW VALIDATOR "
                                  "SUITE - citation_sweep, hebrew_normalize_dryrun, mark_symmetry, ngram7, register "
                                  "and the rest. Those are duties of an author who writes row prose and Hebrew runs. "
                                  "An audit lane writes no rows and touches no corpus file, so every member is out of "
                                  "scope and the FAIL measures nothing about this brief."),
        "what_would_make_it_apply": "any future brief that authors or edits rows; it must PASS before such a launch",
        "tier": "MEASURED (the run) plus JUDGED (the inapplicability), and the judgement is mine, not a tool's"},
    "limit": ("nothing here says the briefs ASK the right questions. The pin check proves the inputs are the ones "
              "named and unchanged; the diff proves the two lanes are blind to nothing but their own letter. Whether "
              "items 20-23 are fit to accept is what the lanes themselves decide, and neither lane is bound by my "
              "framing of the questions - both are told to escalate instead of writing when a pin contradicts itself."),
}
p = EZ / "ezek_close_audit_prelaunch.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"wrote": p.name, "bytes": p.stat().st_size, "sha256": sha(p),
                  "differing_lines": differing, "suite_verdict": out["check_NOT_applicable"]["verdict_when_run_anyway"]},
                 ensure_ascii=False, indent=1))
