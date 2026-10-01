#!/usr/bin/env python3
"""Repair the five sentences my register substitution broke. Grammar only - no claim changes.

WHOSE DEFECT. Mine. My register repair replaced internal labels with descriptive phrases by regex and did not
check the result read as English. The remediation agent found five sentences and declined to touch them, because
they were outside its mandate - correctly, and it flagged them rather than silently fixing prose it was not
asked to write.

Each substitution below is the grammatical consequence of one of mine:
  * "pmarks" -> "the section-mark record" inside "the pinned pmarks" gave "the pinned the section-mark record".
  * "MARKS-3D" -> "the mark-disclosure duty" at a sentence start left it lowercase.
  * "the strategy" -> "the division plan" AND "§7" -> "the division plan's held question" in one clause gave
    "the division the division plan holds at the division plan's held question".
  * the same §7 substitution gave "a scene seam the division plan's held question names by verse".
  * "under the MARKS-3D direction convention" -> "reading each section mark as standing on the verse it
    follows" dropped the clause boundary, so two clauses ran together.

NO CLAIM CHANGES. Every fix restores the sentence the author wrote, with the internal label still gone. The
register check is re-run afterwards to prove the repair did not reintroduce what it removed.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarded_apply as GA                                                     # noqa: E402

HERE = Path(__file__).resolve().parent
EZ = GA.EZ
PRE = "1d9f071dbe0d7dc90511bae47839605ab1b0b400c646a8a4407a8368c1382518"

FIXES = [
    ("P02-009", "strongest_rejected_alternative",
     "Read off the pinned the section-mark record,",
     "Read off the pinned section-mark record,",
     "my substitution produced a doubled article"),
    ("P01-013", "device_notes",
     "not capped. the mark-disclosure duty, MEASURED from",
     "not capped. The mark-disclosure duty, MEASURED from",
     "my substitution left a sentence beginning in lower case"),
    ("P01-009", "strongest_rejected_alternative",
     "the division the division plan holds at the division plan's held question for this chapter",
     "the division the division plan holds for this chapter",
     "two of my substitutions collided in one clause and repeated the phrase"),
    ("P02-003", "strongest_rejected_alternative",
     "a scene seam the division plan's held question names by verse",
     "a scene seam the division plan names by verse",
     "my section-number substitution read as the subject of the clause"),
    ("P09-002", "strongest_rejected_alternative",
     "reading each section mark as standing on the verse it follows no samekh or pe falls",
     "reading each section mark as standing on the verse it follows, no samekh or pe falls",
     "my substitution dropped the clause boundary and ran two clauses together"),
]

rows = {r["decision_id"]: r for r in GA.load_rows()}
edits, missing = [], []
for rid, field, old, new, why in FIXES:
    v = rows[rid].get(field)
    if not isinstance(v, str) or v.count(old) != 1:
        missing.append({"row": rid, "field": field, "anchor": old[:60],
                        "occurrences": (v.count(old) if isinstance(v, str) else "field is not a string")})
        continue
    edits.append({"row_id": rid, "field": field, "op": "set", "expected_before": v,
                  "value": v.replace(old, new, 1), "sweep": "vocab", "why": why})

print(json.dumps({"fixes_ordered": len(FIXES), "anchored": len(edits), "anchor_failures": missing}, indent=1))
if missing:
    raise SystemExit("REFUSED: an anchor did not occur exactly once; nothing applied")

sim = GA.simulate_plan([("grammar", edits)], PRE)
print(json.dumps({"simulation_ok": sim["ok"], "final": sim.get("final_digest_if_applied")}, indent=1))
if not sim["ok"]:
    raise SystemExit("REFUSED")
if "--apply" not in sys.argv:
    print("\n(simulation only; pass --apply)")
    raise SystemExit(0)

RECEIPTS = EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl"
rec = GA.apply_edits(edits, PRE, "author_wave_grammar_repair", ordered_count=len(edits), apply=True)
rec["what_this_was"] = ("grammar repair of five sentences my own register substitution broke. No claim "
                        "changed; the internal labels stay removed. Found by the remediation agent, which "
                        "flagged them rather than rewriting prose outside its mandate.")
rec["whose_defect"] = "the orchestrator's"
with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

# prove the repair did not reintroduce what the register sweep removed
r = subprocess.run([sys.executable, str(EZ / "tools" / "check_register.py"), str(GA.ROWS)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
reg = json.loads(r.stdout)
print(json.dumps({"sweep": rec["sweep"], "parity": rec["e18_parity_digits"],
                  "rows_touched": rec["rows_touched"],
                  "postimage": rec["postimage_sha256_measured_from_disk"],
                  "register_after_the_repair": {"flag_count": reg.get("flag_count"),
                                                "status": reg.get("status")}}, indent=1))
