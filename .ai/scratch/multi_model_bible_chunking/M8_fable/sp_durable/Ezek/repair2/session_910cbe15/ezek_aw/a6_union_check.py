#!/usr/bin/env python3
"""Is the A6 worklist at least the union #e13 R3 orders? Measured, not assumed.

R3 sets the A6 worklist as "the arm's output UNIONED with every peer's hand-named run ... filtered by A6-b".
Worklist v2's 170 A6 items come from the BOSS AUDIT's a6_measured_attachment, which is the boss's own
independent measurement over the same corrected predicate - a THIRD measurement, not the arm's 98 and not the
peers' hand-named runs. So the worklist's basis needs the same containment test the A4 union got: if the boss's
170 contains the arm's runs, the worklist is at least as large as R3 requires; if not, the residue is named.

This is the same question that went wrong once already in this book. A worklist whose basis is "a measurement
that looked bigger" is not a worklist whose basis is the ORDER.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
ARM = EZ / "tools" / "check_web_quotes.py"

boss = json.loads((EZ / "ezek_boss_audit.v1.json").read_text(encoding="utf-8"))
att = boss["a6_measured_attachment"]
boss_by_row = att["by_row"]


def norm(s):
    """Compare runs on their word sequence, not on incidental spacing or case."""
    return " ".join(str(s).lower().split())


boss_set = {(rid, norm(r.get("run", ""))) for rid, runs in boss_by_row.items() for r in runs}

# ---- the arm, run now over the pinned rows
res = subprocess.run([sys.executable, str(ARM), str(ROWS)], capture_output=True, text=True,
                     cwd=str(ARM.parent), encoding="utf-8", errors="replace")
arm_json = None
try:
    arm_json = json.loads(res.stdout)
except Exception:
    pass

report = {
    "schema": "ezek_a6_union_check.v1",
    "order": ("#e13 R3: the A6 worklist is the corrected arm's output UNIONED with every peer's hand-named run, "
              "filtered by A6-b (formula renderings exempt when the row names the device)"),
    "worklist_basis_used": ("the boss audit's a6_measured_attachment - 170 runs on 86 rows, the boss's own "
                            "MEASURED sweep with the corrected predicate (5+ consecutive words identical to "
                            "the WEB after punctuation stripping, on the continuation-joined 1273-verse parse)"),
    "boss_attachment": {"runs": att["runs_not_delimited_and_referenced"], "rows": att["rows"],
                        "tier": att["tier"]},
    "arm_rerun": {"exit": res.returncode, "parsed": arm_json is not None,
                  "member_sha256": hashlib.sha256(ARM.read_bytes()).hexdigest()},
}

if arm_json is not None:
    # the arm's shape: find its hit list whatever the key is called, and report what was read
    keys = list(arm_json.keys())
    report["arm_rerun"]["top_level_keys"] = keys
    # MEASURED SHAPE: the arm's records are {file, path, quote, words, ref, issue}. The run text is under
    # "quote", not "run", and the ROW is identified by the PATH INDEX ("[1].boundary_rationale") rather than by
    # decision_id. My first extractor looked for a key containing "run", found none, and was about to record
    # containment as UNAVAILABLE - which would have been UNAVAILABLE-where-MEASURABLE, the defect class the
    # boss audit named, with the list sitting in plain view under "flags".
    hits = arm_json.get("flags")
    report["arm_rerun"]["hit_key"] = "flags"
    report["arm_rerun"]["record_shape"] = sorted(hits[0].keys()) if hits else None
    rows_in_file = [__import__("json").loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines()
                    if l.strip()]
    import re as _re
    arm_set = set()
    unmapped = 0
    for h in hits or []:
        m = _re.match(r"\[(\d+)\]", str(h.get("path", "")))
        if not m:
            unmapped += 1
            continue
        i = int(m.group(1))
        rid = rows_in_file[i]["decision_id"] if 0 <= i < len(rows_in_file) else "?"
        arm_set.add((rid, norm(h.get("quote") or "")))
    report["arm_rerun"]["records_whose_row_could_not_be_mapped"] = unmapped
    if True:
        missing = sorted(arm_set - boss_set)
        report["containment_MEASURED"] = {
            "arm_runs": len(arm_set),
            "arm_rows": len({r for r, _ in arm_set}),
            "arm_runs_contained_in_the_boss_attachment": len(arm_set) - len(missing),
            "arm_runs_NOT_in_the_boss_attachment": len(missing),
            "the_residue": [{"row": r, "run": t[:70]} for r, t in missing[:40]],
            "verdict": ("the boss attachment CONTAINS the arm's output, so the worklist is at least as large as "
                        "R3's first union member requires"
                        if not missing else
                        "the arm names %d runs the boss attachment does not; each must be added to the worklist "
                        "or dismissed with a reason, because R3 makes the arm a union MEMBER and not an "
                        "alternative" % len(missing)),
        }
else:
    report["arm_rerun"]["stderr_tail"] = (res.stderr or "")[-600:]
    report["containment_MEASURED"] = ("UNAVAILABLE - the arm's output could not be parsed as JSON, so "
                                      "containment was not measured. This is UNAVAILABLE-where-MEASURABLE "
                                      "unless the parse failure is itself reported and fixed.")

(HERE / "a6_union_check.v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                             encoding="utf-8", newline="\n")
print(json.dumps(report, ensure_ascii=False, indent=1)[:3500])
