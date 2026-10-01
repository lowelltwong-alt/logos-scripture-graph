#!/usr/bin/env python3
"""A6 containment, measured three ways, because the first way was too strict to mean anything.

WHAT THE FIRST COMPARISON DID AND WHY ITS NUMBER WAS MISLEADING. It compared the arm's run text to the boss's
run text exactly, and reported that 66 of the arm's 96 runs were "NOT in" the boss's 170. But the two sweeps
name run EXTENTS independently: the arm's "you will know that i" and a boss run "you will know that i am yahweh"
on the same row are the SAME SITE at different extents. A strict text comparison counts that as a miss, so 66 is
an artifact of the comparison and not a measurement of the worklist's coverage.

So containment is measured three ways and all three are reported:
  1. EXACT   - identical normalised run text on the same row. The strictest, and the least meaningful.
  2. OVERLAP - the same row, and one run's word sequence contains the other's. This is the SITE question, and it
               is the one that decides whether the worklist covers what the arm found.
  3. ROW     - the same row appears in both. The weakest; reported only to bound the others.

A number without its comparison rule is not a measurement. That is why all three are here rather than the one
that flatters the worklist.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
ARM = EZ / "tools" / "check_web_quotes.py"

boss = json.loads((EZ / "ezek_boss_audit.v1.json").read_text(encoding="utf-8"))
att = boss["a6_measured_attachment"]
rows_in_file = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]


def norm(s):
    return " ".join(re.sub(r"[^\w\s']", " ", str(s).lower()).split())


boss_runs = {}
for rid, runs in att["by_row"].items():
    for r in runs:
        boss_runs.setdefault(rid, []).append(norm(r.get("run", "")))

res = subprocess.run([sys.executable, str(ARM), str(ROWS)], capture_output=True, text=True,
                     cwd=str(ARM.parent), encoding="utf-8", errors="replace")
arm_json = json.loads(res.stdout)
arm_runs = {}
for h in arm_json["flags"]:
    m = re.match(r"\[(\d+)\]", str(h.get("path", "")))
    if not m:
        continue
    rid = rows_in_file[int(m.group(1))]["decision_id"]
    arm_runs.setdefault(rid, set()).add(norm(h.get("quote") or ""))

n_arm = sum(len(v) for v in arm_runs.values())
exact_miss, overlap_miss, row_miss = [], [], []
for rid, runs in arm_runs.items():
    b = boss_runs.get(rid, [])
    for r in runs:
        if r not in b:
            exact_miss.append((rid, r))
        if not any(r in x or x in r for x in b):
            overlap_miss.append((rid, r))
        if not b:
            row_miss.append((rid, r))

report = {
    "schema": "ezek_a6_union_check.v2",
    "order": ("#e13 R3: the A6 worklist is the corrected arm's output UNIONED with every peer's hand-named run, "
              "filtered by A6-b. The arm is a union MEMBER, not an alternative to the boss's sweep."),
    "why_v2_exists": ("v1 compared run TEXT exactly and reported 66 of 96 arm runs 'NOT in' the boss "
                      "attachment. The two sweeps name run EXTENTS independently, so the same site at a "
                      "different extent counted as a miss. 66 measured the comparison rule, not the worklist."),
    "sets": {"boss_attachment_runs": att["runs_not_delimited_and_referenced"],
             "boss_attachment_rows": att["rows"],
             "arm_runs": n_arm, "arm_rows": len(arm_runs),
             "arm_member_sha256": hashlib.sha256(ARM.read_bytes()).hexdigest()},
    "containment_three_ways": {
        "1_EXACT_identical_run_text": {
            "arm_runs_not_matched": len(exact_miss),
            "meaning": "the strictest and least meaningful: an extent difference counts as a miss"},
        "2_OVERLAP_one_run_contains_the_other_on_the_same_row": {
            "arm_runs_not_matched": len(overlap_miss),
            "meaning": ("THE SITE QUESTION, and the one that decides coverage. An arm run with no overlapping "
                        "boss run on its row is a site the worklist does not carry."),
            "the_residue": [{"row": r, "run": t[:80]} for r, t in sorted(overlap_miss)]},
        "3_ROW_the_row_appears_in_both": {
            "arm_runs_on_rows_the_boss_never_names": len(row_miss),
            "rows": sorted({r for r, _ in row_miss}),
            "meaning": "the weakest bound; a row the boss's sweep never reached at all"},
    },
    "verdict": None,
    "tier": "MEASURED on both sides over the pinned rows; the comparison rules are stated in full",
}
if not overlap_miss:
    report["verdict"] = ("COVERED. Every run the arm names overlaps a run the boss attachment already carries, "
                         "so the worklist's A6 class is at least as large as R3's first union member requires. "
                         "Extent differences remain and are the author's business at the row, since A6 asks for "
                         "the delimiter and the reference, not for a canonical extent.")
else:
    report["verdict"] = ("INCOMPLETE. %d run sites the arm names have no overlapping run in the worklist's A6 "
                         "class, on %d rows. R3 makes the arm a union MEMBER, so each must be ADDED to the "
                         "worklist or dismissed with a stated reason. The worklist is not yet R3's union."
                         % (len(overlap_miss), len({r for r, _ in overlap_miss})))

(HERE / "a6_union_check.v2.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                             encoding="utf-8", newline="\n")
out = dict(report)
out["containment_three_ways"] = json.loads(json.dumps(report["containment_three_ways"]))
res2 = out["containment_three_ways"]["2_OVERLAP_one_run_contains_the_other_on_the_same_row"]
res2["the_residue"] = res2["the_residue"][:12] + (["... %d more" % (len(overlap_miss) - 12)]
                                                  if len(overlap_miss) > 12 else [])
print(json.dumps(out, ensure_ascii=False, indent=1))
