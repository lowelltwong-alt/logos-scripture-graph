#!/usr/bin/env python3
"""OW-28: the owner's 2026-09-23 answer to the E-55 unit question - the old count, budgets no longer gate, Fable at the end.

Same mechanism as record_ow27_ceiling.py: the carrier through SP/campaign/_guarded_json_patch.py with the whole-file
digest and exact expected-before values (dry run, apply, postcheck); the ledger directive and the close-gate addendum as
locked appends with the before-digest pinned and a post-write check (E-44: append, never edit). --dry writes nothing.
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
CAR_PIN = "54843bbc419c0fb00bf5858767fbf2a29022231229610a40ea77242dc99a48f1"
NOW = datetime.now(timezone.utc).isoformat()
DRY = "--dry" in sys.argv
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
env = dict(os.environ, PYTHONUTF8="1")

OWNER_VERBATIM = ("use the old count. also lets jest get thes books done dont worry about budgets or fable. i will likly "
                  "have fable at teh very end of all these books being chunged review each books lease confident chuns and "
                  "review yoru notes for them becasue its job is to make the hardest decisions. so dont worry about budget "
                  "worry about token effieiency and quality aand alctual projgess with the goal being ot move through thee "
                  "books and having the notuon that fable will review each of these at the end")
UNIT = ("notification unit (the owner's 'old count'): each execution's completion-notification figure, which equals the "
        "last request's context; E-55 measured the spend unit (input + cache_creation + output per unique message id) at "
        "about 1.66x it. Spend-unit figures are still measured and reported, for efficiency, not against the ceiling")
RULE = ("OW-28 (2026-09-23): ceilings are TRACKED, NOT ENFORCED. The orchestrator reports each book's spend against its "
        "ceiling in the notification unit at every landing and close, and keeps lanes lean for token efficiency, but a "
        "forecast or spend above a ceiling no longer stops a launch or needs a check-in. Released by the owner: 'dont worry "
        "about budgets'")

g = subprocess.run([sys.executable, "-B", str(GUARD), "--book", "Ezek", "--target", "campaign/budget_ceilings.v1.json",
                    "--target", "../ERROR_PATTERN_LEDGER.v1.md", "--target", "../CAMPAIGN_CLOSE_GATE.v1.md"],
                   cwd=str(SP), capture_output=True, text=True, encoding="utf-8", env=env)
go = json.loads(g.stdout)
if go["verdict"] != "CLEAR" or go["in_flight"]:
    raise SystemExit("REFUSED by pin guard: %s in_flight=%s" % (go["verdict"], go["in_flight"]))

# ---- 1. carrier, through the guarded patch
car_b = CAR.read_bytes()
if sha(car_b) != CAR_PIN:
    raise SystemExit("REFUSED: the carrier is not the pinned one (%s)" % sha(car_b))
car = json.loads(car_b.decode("utf-8"))
before_books, before_rule = car["books"], car["rule"]
new_books = copy.deepcopy(before_books)
ez = new_books["Ezek"]
if "unit" in ez or "unit" in new_books["Dan"]:
    raise SystemExit("REFUSED: a unit is already recorded")
old_hard = ez["hard_line"]
ez["unit"] = UNIT
ez["hard_line"] = "released by OW-28 (2026-09-23): tracked, not enforced; see the carrier's rule"
ez["hard_line_superseded"] = [{"text": old_hard, "held_from": "2026-09-23 (OW-27)", "released_by": "OW-28"}]
new_books["Dan"]["unit"] = UNIT + " (INFERRED for Daniel: the owner answered for Ezekiel's ceiling)"
plan = {"target": str(CAR), "expect_file_sha256": sha(car_b),
        "edits": [{"key": "books", "expect_before": before_books, "set": new_books,
                   "why": "OW-28: the ceiling's unit is the notification unit; Ezekiel's hard line released"},
                  {"key": "rule", "expect_before": before_rule, "set": RULE,
                   "why": "OW-28: budgets no longer gate launches; tracked and reported only"},
                  {"key": "updated_at", "expect_before": car.get("updated_at", "__ABSENT__"), "set": NOW,
                   "why": "OW-28 carrier update"}],
        "receipt": str(SP / "Ezek" / "repair2" / "_ow28_directive_patch_receipt.json")}
pp = Path(__file__).resolve().parent / "_ow28_plan.json"

# ---- 2. ledger directive and 3. close-gate addendum (text fixed before any write)
LEDGER_ADD = "\n".join([
    "", "## OWNER DIRECTIVE OW-28 (2026-09-23) - THE OLD COUNT; BUDGETS TRACKED, NOT GATING; FABLE REVIEWS EVERY BOOK AT THE END", "",
    "**What the orchestrator brought (summary).** E-55: census v4 measured Ezekiel at 70,938,658 in the notification "
    "unit (the completion-notification figure the ceilings were set in) and at LOWER_BOUND 118,001,439 in the spend unit "
    "(input + cache_creation + output per unique message id), 31,601,439 over 86,400,000 in that unit. The owner was "
    "asked which unit the ceiling is in; no launch until answered.", "",
    "**Owner answer (verbatim):** \"%s\"" % OWNER_VERBATIM, "",
    "**Decides.** (1) The ceilings are in the notification unit (\"the old count\"): Ezekiel stands at 70,938,658 "
    "against 86,400,000, headroom UPPER_BOUND 15,461,342. Spend-unit figures are still measured and reported, for "
    "efficiency. (2) Budgets no longer gate progress: the carrier's rule becomes tracked-not-enforced, and the "
    "check-in-before-crossing rule and Ezekiel's OW-22/OW-27 hard line are released. Token efficiency stays a goal: lean "
    "lanes, delta re-checks, spend measured at every landing. (3) Fable is no longer awaited per book. At the very end of "
    "the campaign Fable reviews, for each book, its least-confident chunks and the orchestrator's notes on them, and "
    "makes the hardest decisions. (4) The goal is actual progress through the books, with quality.", "",
    "**The orchestrator's reading, not the owner's words (INFERRED).** (a) Each book's close carries a deferred-Fable "
    "review packet: every row graded low or medium_low, its sidecar and low_confidence_register entry, and the "
    "orchestrator's notes (lane splits, reservations, open questions, residuals judged non-blocking). (b) A close gate "
    "that requires a Fable model (the Lam L60 gate; a final checker equal to claude-fable-5-1) is recorded DEFERRED to "
    "that end review, never MET. (c) \"the old count\" is read as the unit for every book's ceiling, Daniel included.", "",
    "**What it does NOT change.** OW-11: closing, `_close_book.py --close`, the `--acf` choice, publication and "
    "campaign-log appends remain the owner's act. OW-9: stop at the book boundary. OW-19: two blind lanes at the floor, "
    "and the orchestrator never grades its own items. OW-25: every role on claude-opus-5-5. OW-26: the transcript audit "
    "stays OWED, NOT MET. E-54/E-55 measurement stays: spend is measured from usage fields, and both units are named. "
    "The prevention-skill question put to the owner is still unanswered.", "",
    "**Carrier:** budget_ceilings.v1.json via the guarded patch, sha256 {CARRIER}.", ""])
GATE_ADD = "\n".join([
    "", "## Addendum 2026-09-23 - OW-28 (old count; budgets tracked; Fable at the end)", "",
    "- Each close packet states the book's spend in the notification unit against its ceiling, and the spend-unit "
    "measurement beside it. A spend above the ceiling is reported, not a blocking gate.",
    "- A gate that requires a Fable model is recorded DEFERRED to the campaign-end Fable review, never MET.",
    "- Each close carries a deferred-Fable review packet: every low and medium_low row, its sidecar and "
    "low_confidence_register entry, and the orchestrator's notes on lane splits, reservations and open questions.", ""])


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
if b"OW-28" in lm_b or b"OW-28" in g_b:
    raise SystemExit("REFUSED: OW-28 already present in the ledger or the close gate")
for t in (LEDGER_ADD, GATE_ADD, RULE, UNIT):
    if "C-2" in t or "C-3" in t:
        raise SystemExit("REFUSED: a DAD marker number appears in the text (E-52)")

pp.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
dry = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp)], capture_output=True, text=True,
                     encoding="utf-8", env=env)
d = json.loads(dry.stdout[dry.stdout.find("{"):])
if d.get("status") != "DRY_RUN" or sorted(d.get("keys_addressed", [])) != ["books", "rule", "updated_at"]:
    raise SystemExit("REFUSED at dry run: %s" % dry.stdout[-600:])
print(json.dumps({"dry_run": d.get("status"), "keys": d.get("keys_addressed"), "ledger_before": sha(lm_b)[:16],
                  "gate_before": sha(g_b)[:16], "ledger_add_lines": LEDGER_ADD.count("\n")}, indent=1))
if DRY:
    pp.unlink()
    raise SystemExit(0)

app = subprocess.run([sys.executable, "-B", str(TOOL), "--plan", str(pp), "--apply"], capture_output=True, text=True,
                     encoding="utf-8", env=env)
a = json.loads(app.stdout[app.stdout.find("{"):])
if a.get("status") != "APPLIED":
    raise SystemExit("REFUSED at apply: %s" % app.stdout[-600:])
check = json.loads(CAR.read_text(encoding="utf-8"))
if (check["rule"] != RULE or check["books"]["Ezek"]["ceiling"] != 86400000 or check["books"]["Ezek"]["unit"] != UNIT
        or check["books"]["Dan"]["ceiling"] != 25000000):
    raise SystemExit("POSTCHECK FAILED on the carrier")
car_after = sha(CAR.read_bytes())
lm = locked_append(LM, LEDGER_ADD.replace("{CARRIER}", car_after), lm_b)
gt = locked_append(G, GATE_ADD, g_b)
print(json.dumps({"carrier_sha256": car_after, "ledger_sha256": lm, "gate_sha256": gt}, indent=1))
