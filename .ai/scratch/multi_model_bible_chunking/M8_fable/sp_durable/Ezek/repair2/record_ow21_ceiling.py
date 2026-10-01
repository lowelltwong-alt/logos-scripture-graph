#!/usr/bin/env python3
"""OW-21: the owner's 2026-09-16 answer raising Ezekiel's ceiling to 65,000,000 - carrier first, then ledger and gate.

Carrier through SP/campaign/_guarded_json_patch.py (one top-level key addressed with its exact expected-before value
and the whole-file digest; dry run printed, then applied). Ledger MD and JSONL and the close-gate addendum in the same
step (OW-11-n control u). CYCLE_STATE and the resume prompt's budget line follow at the next durability checkpoint.
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

QUESTION = ("Ezekiel's real spend is ~45.5M of its 55M ceiling (10 attempts had no receipts, now recovered), and "
            "finishing Ezekiel is projected at ~12.6M more (~58M total, an estimate). OW-15 requires your check-in "
            "before a launch that would cross the ceiling. How should I proceed?")
ANSWER = "Raise ceiling to 65M (Recommended)"
OPTION_TEXT = ("Record the new ceiling in budget_ceilings.v1.json via the guarded patch, then continue Ezekiel's close "
               "with full quality: every step keeps two blind lanes plus Fable adjudication, the second review and the "
               "final checks. Leaves ~7M margin over the projection.")

car = json.loads(CAR.read_text(encoding="utf-8"))
before_books = car["books"]
if before_books["Ezek"]["ceiling"] != 55000000:
    raise SystemExit("REFUSED: Ezekiel's ceiling is not the expected 55,000,000")
new_books = copy.deepcopy(before_books)
old = new_books["Ezek"]
new_books["Ezek"] = {
    "ceiling": 65000000,
    "effective_from": "2026-09-16",
    "owner_answer": "OW-21: the owner selected '%s' in answer to the orchestrator's OW-15 check-in" % ANSWER,
    "counted_as": old["counted_as"],
    "superseded": [{"ceiling": old["ceiling"], "answer_date": old["effective_from"],
                    "note": old["owner_answer"]}] + old["superseded"],
}
plan = {"target": str(CAR), "expect_file_sha256": sha(CAR),
        "edits": [{"key": "books", "expect_before": before_books, "set": new_books,
                   "why": "OW-21: owner raised Ezekiel's ceiling from 55,000,000 to 65,000,000 on 2026-09-16"},
                  {"key": "updated_at", "expect_before": car.get("updated_at", "__ABSENT__"), "set": NOW,
                   "why": "OW-21 carrier update"}],
        "receipt": str(SP / "Ezek" / "repair2" / "_ow21_ceiling_patch_receipt.json")}
pp = Path(__file__).resolve().parent / "_ow21_plan.json"
pp.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
env = dict(os.environ, PYTHONUTF8="1")
dry = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp)], capture_output=True, text=True,
                     encoding="utf-8", env=env)
d = json.loads(dry.stdout[dry.stdout.find("{"):])
if d.get("status") != "DRY_RUN" or sorted(d.get("keys_addressed", [])) != ["books", "updated_at"]:
    raise SystemExit("REFUSED at dry run: %s" % dry.stdout[-600:])
app = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp), "--apply"], capture_output=True, text=True,
                     encoding="utf-8", env=env)
a = json.loads(app.stdout[app.stdout.find("{"):])
if a.get("status") != "APPLIED":
    raise SystemExit("REFUSED at apply: %s" % app.stdout[-600:])
check = json.loads(CAR.read_text(encoding="utf-8"))["books"]
if check["Ezek"]["ceiling"] != 65000000 or check["Dan"] != before_books["Dan"]:
    raise SystemExit("POSTCHECK FAILED")

LJ, LM, G = M8 / "error_pattern_ledger.v1.jsonl", M8 / "ERROR_PATTERN_LEDGER.v1.md", M8 / "CAMPAIGN_CLOSE_GATE.v1.md"
row = {"id": "OW-21", "kind": "owner_directive", "date": "2026-09-16",
       "question_verbatim": QUESTION, "answer_selected_verbatim": ANSWER, "option_text_verbatim": OPTION_TEXT,
       "decides": "Ezekiel's subagent-token ceiling is 65,000,000 (was 55,000,000); Daniel's 25,000,000 is unchanged",
       "does_not_change": ["the pre-crossing owner check-in (OW-15 c) - it now binds at 65,000,000",
                           "OW-16: budget is a limit, not a driver",
                           "the per-session soft cap and pre-8M check-in stay REPLACED for Ezekiel and Daniel (OW-15 d)"],
       "basis": ("census LOWER BOUND 45,479,215 after recovering ten unreceipted attempts and four UNAVAILABLE figures "
                 "(E13-101, E-38); remaining close PROJECTED at about 12,600,000 (INFERRED)"),
       "carriers": {"budget_ceilings.v1.json": {"sha256_after": sha(CAR), "patch_receipt": plan["receipt"]},
                    "ledger": "this row and the MD addendum", "close_gate": "addendum 2026-09-16 OW-21",
                    "cycle_state_and_resume_prompt": "at the next durability checkpoint"}}
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(["", "## OW-21 - OWNER DIRECTIVE (2026-09-16): Ezekiel's ceiling raised to 65,000,000", "",
                        "**Question (verbatim):** \"%s\"" % QUESTION, "",
                        "**Answer selected (verbatim):** \"%s\" - option text: \"%s\"" % (ANSWER, OPTION_TEXT), "",
                        "**Decides:** Ezekiel 65,000,000 (was 55,000,000); Daniel's 25,000,000 unchanged. **Does not "
                        "change:** the pre-crossing check-in now binds at 65M; OW-16 stands; the per-session soft cap "
                        "and pre-8M check-in stay replaced for Ezekiel and Daniel. **Basis:** census lower bound "
                        "45,479,215 (E13-101, E-38); remaining close projected at about 12.6M (INFERRED). **Carrier:** "
                        "budget_ceilings.v1.json via the guarded patch, sha256 %s." % sha(CAR), ""]))
with G.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(["", "## Addendum 2026-09-16 - OW-21 (Ezekiel ceiling 65,000,000)", "",
                        "- The close packet states Ezekiel's spend against 65,000,000, read from "
                        "SP/campaign/budget_ceilings.v1.json; the owner check-in before a crossing launch binds there.",
                        "- The census is reconciled against the runtime notification log before the close packet's "
                        "budget statement (E-38).", ""]))
print(json.dumps({"carrier_sha256": sha(CAR), "ezek_ceiling": 65000000, "ledger_rows":
                  sum(1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip())}, indent=1))
