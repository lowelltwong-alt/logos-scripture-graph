#!/usr/bin/env python3
"""OW-22: the owner's 2026-09-16 answer raising Ezekiel's ceiling to 72,000,000 - carrier first, then ledger and gate.

Same mechanism as OW-21 (record_ow21_ceiling.py): SP/campaign/_guarded_json_patch.py with the whole-file digest and
exact expected-before values; dry run, then apply; postcheck; ledger MD and JSONL and the close-gate addendum.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SP = M8 / "sp_durable"
CAR = SP / "campaign" / "budget_ceilings.v1.json"
TOOL = SP / "campaign" / "_guarded_json_patch.py"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

QUESTION = ("Ezekiel's measured subagent spend is 53.9M of its 65M ceiling (receipts, lower bound). The rest of the close "
            "projects to about 66M total (estimate, \u00b13M): step-7 re-read now running ~4.2M, #e16 ~0.7M, a final "
            "remediation batch ~3M, the second Fable review ~1.5M, the scholar-record audit ~1M, the final check ~1.5M. "
            "OW-21 requires your check-in before a launch that would cross 65M. How should I proceed?")
ANSWER = "Raise ceiling to 72M (Recommended)"
OPTION_TEXT = ("Record 72,000,000 in budget_ceilings.v1.json via the guarded patch and finish Ezekiel at full quality: two "
               "blind lanes plus Fable adjudication on every remaining step. Leaves ~6M margin over the projection; "
               "Daniel's 25M unchanged.")
FOLLOW_UP = ("The owner then asked how complete Ezekiel is and said they are tired of the token budget being missed. The "
             "orchestrator answered about 80 percent by tokens and about 75 percent by remaining steps (estimates), named "
             "the three causes of the repeated misses (an undercounted census base, each step surfacing new owed work, and "
             "lanes doubled for OW-19 before re-projecting), and committed: 72,000,000 is a hard line with no further raise "
             "requested; the forecast is re-made from measured per-step actuals after step 7 and after #e16; a forecast "
             "above 72,000,000 is brought to the owner as a specific scope cut, not a raise.")

car = json.loads(CAR.read_text(encoding="utf-8"))
before_books = car["books"]
if before_books["Ezek"]["ceiling"] != 65000000:
    raise SystemExit("REFUSED: Ezekiel's ceiling is not the expected 65,000,000")
new_books = copy.deepcopy(before_books)
old = new_books["Ezek"]
new_books["Ezek"] = {
    "ceiling": 72000000,
    "effective_from": "2026-09-16",
    "owner_answer": "OW-22: the owner selected '%s' in answer to the orchestrator's OW-21 check-in" % ANSWER,
    "hard_line": "the orchestrator committed to request no further raise; a forecast above this is brought as a scope cut",
    "counted_as": old["counted_as"],
    "superseded": [{"ceiling": old["ceiling"], "answer_date": old["effective_from"], "note": old["owner_answer"]}] + old["superseded"],
}
plan = {"target": str(CAR), "expect_file_sha256": sha(CAR),
        "edits": [{"key": "books", "expect_before": before_books, "set": new_books,
                   "why": "OW-22: owner raised Ezekiel's ceiling from 65,000,000 to 72,000,000 on 2026-09-16"},
                  {"key": "updated_at", "expect_before": car.get("updated_at", "__ABSENT__"), "set": NOW, "why": "OW-22 carrier update"}],
        "receipt": str(SP / "Ezek" / "repair2" / "_ow22_ceiling_patch_receipt.json")}
pp = Path(__file__).resolve().parent / "_ow22_plan.json"
pp.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
env = dict(os.environ, PYTHONUTF8="1")
dry = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp)], capture_output=True, text=True, encoding="utf-8", env=env)
d = json.loads(dry.stdout[dry.stdout.find("{"):])
if d.get("status") != "DRY_RUN" or sorted(d.get("keys_addressed", [])) != ["books", "updated_at"]:
    raise SystemExit("REFUSED at dry run: %s" % dry.stdout[-600:])
app = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp), "--apply"], capture_output=True, text=True, encoding="utf-8", env=env)
a = json.loads(app.stdout[app.stdout.find("{"):])
if a.get("status") != "APPLIED":
    raise SystemExit("REFUSED at apply: %s" % app.stdout[-600:])
check = json.loads(CAR.read_text(encoding="utf-8"))["books"]
if check["Ezek"]["ceiling"] != 72000000 or check["Dan"] != before_books["Dan"]:
    raise SystemExit("POSTCHECK FAILED")

LJ, LM, G = M8 / "error_pattern_ledger.v1.jsonl", M8 / "ERROR_PATTERN_LEDGER.v1.md", M8 / "CAMPAIGN_CLOSE_GATE.v1.md"
if any(json.loads(l).get("id") == "OW-22" for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: OW-22 already in the ledger (the carrier was patched; ledger not appended twice)")
row = {"id": "OW-22", "kind": "owner_directive", "date": "2026-09-16",
       "question_verbatim": QUESTION, "answer_selected_verbatim": ANSWER, "option_text_verbatim": OPTION_TEXT,
       "owner_follow_up_and_orchestrator_commitment": FOLLOW_UP,
       "decides": "Ezekiel's subagent-token ceiling is 72,000,000 (was 65,000,000); Daniel's 25,000,000 is unchanged",
       "does_not_change": ["the pre-crossing owner check-in - it now binds at 72,000,000", "OW-16: budget is a limit, not a driver",
                           "the per-session soft cap and pre-8M check-in stay REPLACED for Ezekiel and Daniel"],
       "basis": "measured lower bound 53,916,504 before the step-7 launch; remaining close projected at about 12M (INFERRED)",
       "carriers": {"budget_ceilings.v1.json": {"sha256_after": sha(CAR), "patch_receipt": plan["receipt"]},
                    "ledger": "this row and the MD addendum", "close_gate": "addendum 2026-09-16 OW-22",
                    "cycle_state_and_resume_prompt": "at the next durability checkpoint"}}
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(["", "## OW-22 - OWNER DIRECTIVE (2026-09-16): Ezekiel's ceiling raised to 72,000,000, held as a hard line", "",
                        "**Question (verbatim):** \"%s\"" % QUESTION, "",
                        "**Answer selected (verbatim):** \"%s\" - option text: \"%s\"" % (ANSWER, OPTION_TEXT), "",
                        "**Owner follow-up and the orchestrator's commitment.** %s" % FOLLOW_UP, "",
                        "**Decides:** Ezekiel 72,000,000 (was 65,000,000); Daniel's 25,000,000 unchanged. **Basis:** measured "
                        "lower bound 53,916,504 before the step-7 launch; remaining close projected at about 12M (INFERRED). "
                        "**Carrier:** budget_ceilings.v1.json via the guarded patch, sha256 %s." % sha(CAR), ""]))
with G.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(["", "## Addendum 2026-09-16 - OW-22 (Ezekiel ceiling 72,000,000, a hard line)", "",
                        "- The close packet states Ezekiel's spend against 72,000,000, read from SP/campaign/budget_ceilings.v1.json.",
                        "- The forecast is re-made from measured per-step actuals after step 7 and after #e16; a forecast above the "
                        "ceiling is brought to the owner as a named scope cut, never as a further raise.", ""]))
print(json.dumps({"carrier_sha256": sha(CAR), "ezek_ceiling": 72000000,
                  "ledger_rows": sum(1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip())}, indent=1))
