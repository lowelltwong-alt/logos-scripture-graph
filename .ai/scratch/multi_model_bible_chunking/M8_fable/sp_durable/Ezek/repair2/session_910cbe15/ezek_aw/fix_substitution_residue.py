#!/usr/bin/env python3
"""Fix the rest of my substitution damage, found by auditing my own edit instead of waiting to be told.

I fixed five broken sentences an agent named. A reviewer then found a sixth, worse than any of them. Auditing
every field my substitution touched found eleven artifacts across five rows, of which these six are genuine
damage and the rest are grammatical.

TWO OF THEM ALSO CARRY A SEPARATE DEFECT the spot reviewer flagged independently: a STRATEGY LINE NUMBER in
shipped prose. The register rule bars citing the division plan by locus, and my substitution had left "line 351"
and "line 408" stranded where a section symbol used to govern them. So these fixes remove the line numbers as
well as repairing the grammar - the claim is unchanged, and the plan is still named as the source.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarded_apply as GA                                                     # noqa: E402

EZ = GA.EZ
PRE = "16898b85f62df8c40d153b79c6aa7f5032e2d48a038a3a74807cd4c823e432ae"

FIXES = [
    ("P01-008", "strongest_rejected_alternative",
     "the question the division plan holds at the division plan's held question for chs 4-7",
     "the question the division plan holds for chs 4-7",
     "two of my substitutions collided; the same collision I fixed at P01-009 and missed here"),
    ("P02-020", "strongest_rejected_alternative",
     "against the pinned the device census",
     "against the pinned device census",
     "doubled determiner"),
    ("P06-009", "boundary_rationale",
     "unit at the division plan the division plan's held question, line 351, and restates for this region in "
     "the division plan's",
     "unit in the division plan, and restates for this region in the division plan's",
     "a replacement repeated adjacently, plus a stranded line number the register rule bars"),
    ("P06-009", "strongest_rejected_alternative",
     "a rule the pinned strategy states at the division plan the division plan's held question, line 351, so "
     "it is sourced",
     "a rule the pinned division plan states, so it is sourced",
     "the same doubling, plus a stranded line number; 'the pinned strategy' also survived my own table"),
    ("P07-001", "strongest_rejected_alternative",
     "EXTRACTED from the division plan line 408 inside its flagged chs 25-32 region",
     "EXTRACTED from the division plan inside its flagged chs 25-32 region",
     "a strategy line number in shipped prose, which the register rule bars"),
]

rows = {r["decision_id"]: r for r in GA.load_rows()}
edits, missing = [], []
for rid, field, old, new, why in FIXES:
    v = rows[rid].get(field)
    if not isinstance(v, str) or v.count(old) != 1:
        missing.append({"row": rid, "field": field, "anchor": old[:70],
                        "occurrences": v.count(old) if isinstance(v, str) else "not a string"})
        continue
    edits.append({"row_id": rid, "field": field, "op": "set", "expected_before": v,
                  "value": v.replace(old, new, 1), "sweep": "vocab", "why": why})

print(json.dumps({"ordered": len(FIXES), "anchored": len(edits), "anchor_failures": missing}, indent=1))
if missing:
    raise SystemExit("REFUSED: an anchor did not occur exactly once")

sim = GA.simulate_plan([("residue", edits)], PRE)
print(json.dumps({"simulation_ok": sim["ok"], "final": sim.get("final_digest_if_applied")}, indent=1))
if not sim["ok"]:
    raise SystemExit("REFUSED")
if "--apply" not in sys.argv:
    print("\n(simulation only; pass --apply)")
    raise SystemExit(0)

rec = GA.apply_edits(edits, PRE, "author_wave_substitution_residue", ordered_count=len(edits), apply=True)
rec["what_this_was"] = ("the rest of my register substitution's damage, found by auditing every field the "
                        "substitution touched rather than fixing only what agents named. Two fixes also remove "
                        "a strategy line number from shipped prose, which the register rule bars and which my "
                        "substitution had stranded.")
rec["whose_defect"] = "the orchestrator's, twice: the substitution, and then a repair scoped to what I was told"
with (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

# re-audit: the detector must now find nothing genuine, and register must still be green
aud = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "audit_my_substitution.py")],
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
reg = subprocess.run([sys.executable, str(EZ / "tools" / "check_register.py"), str(GA.ROWS)],
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
print(json.dumps({"sweep": rec["sweep"], "parity": rec["e18_parity_digits"],
                  "rows_touched": rec["rows_touched"],
                  "postimage": rec["postimage_sha256_measured_from_disk"],
                  "register_after": json.loads(reg.stdout).get("status"),
                  "register_flags": json.loads(reg.stdout).get("flag_count")}, indent=1))
print()
print("RE-AUDIT:")
print(aud.stdout[:1400])
