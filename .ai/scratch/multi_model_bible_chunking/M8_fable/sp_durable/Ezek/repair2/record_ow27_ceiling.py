#!/usr/bin/env python3
"""OW-27: the owner's 2026-09-23 answer at the OW-22 line - follow the recommendations, and raise Ezekiel's ceiling 20%.

Same carrier mechanism as OW-22 (record_ow22_ceiling.py): SP/campaign/_guarded_json_patch.py with the whole-file digest
and exact expected-before values; dry run, then apply; postcheck. Unlike OW-22, the ledger and close-gate appends are
made under an exclusive lock with the expected-before digest pinned and a post-write check (E-44: append, never edit).
The JSONL ledger surface stopped being written after E-43 (E-51), so the directive goes to the live MD ledger only.
--dry prints the plan and writes nothing.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SP = M8 / "sp_durable"
CAR = SP / "campaign" / "budget_ceilings.v1.json"
TOOL = SP / "campaign" / "_guarded_json_patch.py"
GUARD = SP / "campaign" / "_inflight_pin_guard.py"
LM, G = M8 / "ERROR_PATTERN_LEDGER.v1.md", M8 / "CAMPAIGN_CLOSE_GATE.v1.md"
NOW = datetime.now(timezone.utc).isoformat()
DRY = "--dry" in sys.argv
OLD, NEW = 72000000, 86400000                      # 72,000,000 x 1.20
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
env = dict(os.environ, PYTHONUTF8="1")

OWNER_VERBATIM = "lets follow your recomendations and also up the budet for this by 20 percent"
BROUGHT = ("Both OW-26 lanes landed not_fit. Measured LOWER_BOUND 70,938,658 against the 72,000,000 hard line, headroom "
           "UPPER_BOUND 1,061,342, so a same-shape re-check pair (576,419-855,552 per lane, measured) did not fit. The "
           "orchestrator offered scope cuts only: (a) a delta fix round, (b) hold Ezekiel open, (c) the owner rules on the "
           "residuals. It recommended (b) for now: first re-measure the census from the transcripts' usage fields (a "
           "script, no model lanes), because the headroom is an upper bound over a total that may already be past the "
           "line; only if the re-measure confirms room, (a) with a hard cap on each lane.")

g = subprocess.run([sys.executable, "-B", str(GUARD), "--book", "Ezek", "--target", "campaign/budget_ceilings.v1.json",
                    "--target", "../ERROR_PATTERN_LEDGER.v1.md", "--target", "../CAMPAIGN_CLOSE_GATE.v1.md"],
                   cwd=str(SP), capture_output=True, text=True, encoding="utf-8", env=env)
go = json.loads(g.stdout)
if go["verdict"] != "CLEAR" or go["in_flight"]:
    raise SystemExit("REFUSED by pin guard: %s in_flight=%s" % (go["verdict"], go["in_flight"]))

# ---- 1. carrier, through the guarded patch
car_b = CAR.read_bytes()
car = json.loads(car_b.decode("utf-8"))
before_books = car["books"]
if before_books["Ezek"]["ceiling"] != OLD:
    raise SystemExit("REFUSED: Ezekiel's ceiling is %r, not the expected 72,000,000" % before_books["Ezek"]["ceiling"])
new_books = copy.deepcopy(before_books)
old = new_books["Ezek"]
new_books["Ezek"] = {
    "ceiling": NEW,
    "effective_from": "2026-09-23",
    "owner_answer": ("OW-27: the owner wrote '%s' when the orchestrator brought Ezekiel to the OW-22 line with scope cuts "
                     "only; 72,000,000 x 1.20" % OWNER_VERBATIM),
    "hard_line": ("the orchestrator requests no further raise; a forecast above this is brought as a scope cut. The OW-27 "
                  "raise was the owner's own offer, not a request, so the OW-22 commitment stands"),
    "counted_as": old["counted_as"],
    "superseded": [{"ceiling": old["ceiling"], "answer_date": old["effective_from"],
                    "note": old["owner_answer"] + " (held as a hard line until OW-27)"}] + old["superseded"],
}
plan = {"target": str(CAR), "expect_file_sha256": sha(car_b),
        "edits": [{"key": "books", "expect_before": before_books, "set": new_books,
                   "why": "OW-27: owner raised Ezekiel's ceiling 20%, from 72,000,000 to 86,400,000, on 2026-09-23"},
                  {"key": "updated_at", "expect_before": car.get("updated_at", "__ABSENT__"), "set": NOW,
                   "why": "OW-27 carrier update"}],
        "receipt": str(SP / "Ezek" / "repair2" / "_ow27_ceiling_patch_receipt.json")}
pp = Path(__file__).resolve().parent / "_ow27_plan.json"

# ---- 2. ledger directive and 3. close-gate addendum (text fixed before any write)
LEDGER_ADD = "\n".join([
    "", "## OWNER DIRECTIVE OW-27 (2026-09-23) - EZEKIEL'S CEILING RAISED 20% TO 86,400,000; THE RECOMMENDATIONS FOLLOWED", "",
    "**What the orchestrator brought (summary).** %s" % BROUGHT, "",
    "**Owner answer (verbatim):** \"%s\"" % OWNER_VERBATIM, "",
    "**Decides.** (1) Ezekiel's subagent-token ceiling is 86,400,000 (was 72,000,000); Daniel's 25,000,000 is unchanged. "
    "The owner said \"this\" and \"20 percent\"; the orchestrator reads it as Ezekiel's per-book ceiling x 1.20 (INFERRED: "
    "the ceiling is per book and the question was Ezekiel's). (2) The recommendation is followed in order: re-measure the "
    "census from the transcripts' usage fields first, with no model lanes; then, only if the re-measure confirms room, "
    "the delta fix round (a) with a hard cap on each lane, forecast from measured actuals with a growth allowance.",
    "",
    "**The orchestrator's reading, not the owner's words (INFERRED).** The owner named no adjudicator for the P03-001 "
    "severity split. The fix round grounds or re-grades P03-001 whichever severity holds, so the split does not have to "
    "be settled first; the delta re-check lanes judge the result. If a lane still splits on it, the question goes back "
    "to the owner.", "",
    "**What it does NOT change.** The OW-22 commitment: no raise is requested, and a forecast above 86,400,000 is brought "
    "as a scope cut. OW-26's merged-verdict shape and its transcript audit OWED, NOT MET. OW-19: two blind lanes at the "
    "floor, and the orchestrator never grades its own items. OW-25: every role on claude-opus-5-5. OW-11: closing, "
    "`_close_book.py --close`, the `--acf` choice, publication and campaign-log appends remain the owner's act. OW-9: stop "
    "at the book boundary. The prevention-skill question put to the owner is still unanswered.", "",
    "**Basis:** measured LOWER_BOUND 70,938,658 (receipts, merged lanes at usage-field spend); headroom was UPPER_BOUND "
    "1,061,342 against 72,000,000 and becomes UPPER_BOUND 15,461,342 against 86,400,000, before the re-measure. "
    "**Carrier:** budget_ceilings.v1.json via the guarded patch, sha256 {CARRIER}.", ""])
GATE_ADD = "\n".join([
    "", "## Addendum 2026-09-23 - OW-27 (Ezekiel ceiling 86,400,000)", "",
    "- The close packet states Ezekiel's spend against 86,400,000, read from SP/campaign/budget_ceilings.v1.json.",
    "- Spend is measured from the executions' usage fields (E-54), not the completion notification's figure; the census "
    "is re-measured before any further launch, and a forecast above the ceiling is brought as a named scope cut.", ""])


def locked_append(path, text, before):
    add = text.encode("utf-8")
    after = before + (b"" if before.endswith(b"\n") else b"\n") + add
    lock = path.with_suffix(path.suffix + ".lock")
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        if path.read_bytes() != before:
            raise SystemExit("REFUSED: %s changed under the lock" % path.name)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(after)
        os.replace(tmp, path)
        now = path.read_bytes()
        if sha(now) != sha(after) or not now.startswith(before):
            path.write_bytes(before)
            raise SystemExit("ROLLED BACK: %s post-write check failed" % path.name)
    finally:
        os.close(fd)
        lock.unlink()
    return sha(before), sha(after)


lm_b, g_b = LM.read_bytes(), G.read_bytes()
if b"OW-27" in lm_b or b"OW-27" in g_b:
    raise SystemExit("REFUSED: OW-27 already present in the ledger or the close gate")
if "C-2" in LEDGER_ADD or "C-3" in LEDGER_ADD:
    raise SystemExit("REFUSED: a DAD marker number appears in the directive text (E-52)")

pp.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
dry = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp)], capture_output=True, text=True,
                     encoding="utf-8", env=env)
d = json.loads(dry.stdout[dry.stdout.find("{"):])
if d.get("status") != "DRY_RUN" or sorted(d.get("keys_addressed", [])) != ["books", "updated_at"]:
    raise SystemExit("REFUSED at dry run: %s" % dry.stdout[-600:])
print(json.dumps({"dry_run": d.get("status"), "keys": d.get("keys_addressed"), "ceiling": [OLD, NEW],
                  "ledger_before": sha(lm_b)[:16], "gate_before": sha(g_b)[:16], "ledger_add_lines": LEDGER_ADD.count("\n")},
                 indent=1))
if DRY:
    pp.unlink()
    raise SystemExit(0)

app = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp), "--apply"], capture_output=True, text=True,
                     encoding="utf-8", env=env)
a = json.loads(app.stdout[app.stdout.find("{"):])
if a.get("status") != "APPLIED":
    raise SystemExit("REFUSED at apply: %s" % app.stdout[-600:])
check = json.loads(CAR.read_text(encoding="utf-8"))["books"]
if check["Ezek"]["ceiling"] != NEW or check["Dan"] != before_books["Dan"]:
    raise SystemExit("POSTCHECK FAILED on the carrier")
car_after = sha(CAR.read_bytes())
lm = locked_append(LM, LEDGER_ADD.replace("{CARRIER}", car_after), lm_b)
gt = locked_append(G, GATE_ADD, g_b)
print(json.dumps({"carrier_sha256": car_after, "ezek_ceiling": NEW, "ledger_sha256": lm, "gate_sha256": gt}, indent=1))
