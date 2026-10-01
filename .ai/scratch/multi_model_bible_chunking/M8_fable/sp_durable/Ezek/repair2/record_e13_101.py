#!/usr/bin/env python3
"""Queue E13-101 and ledger E-38: unreceipted attempts recovered, census restated, and the budget consequence."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
pos = json.loads((EZ / "ezek_ow15_position.v2.json").read_text(encoding="utf-8"))
c = pos["census"]

PROJECTION = {
    "tier": "INFERRED - per-type maxima MEASURED from this book's receipts, counts of launches ASSUMED from #e15's sequence",
    "per_type_maxima_measured": {"fable_ruling_or_audit": 847447, "opus_author_lane": 386948, "spot_lane": 414422},
    "lines": {"step 2 adjudication (in flight)": 850000,
              "steps 3-6: two blind lanes plus a Fable adjudication each": 5100000,
              "step 7: spot re-read at full coverage, 3 lanes": 1250000,
              "#e16": 500000, "OW-6b(b) second Fable review": 850000, "OW-17 scholar-record Fable audit": 850000,
              "OW-6 two-stage Fable final check": 1700000, "fix-up rounds after findings": 1500000},
}
PROJECTION["total"] = sum(PROJECTION["lines"].values())

q = {
    "id": "E13-101", "opened_at": NOW, "severity": "HIGH", "tier": "MEASURED",
    "headline": ("TEN ATTEMPTS HAD NO RECEIPT AND FOUR RECEIPTS DECLARED UNAVAILABLE A FIGURE THE RUNTIME HAD REPORTED - "
                 "recovered from the session transcript. Ezekiel's census moves from 39,426,659 to %s, headroom at most "
                 "%s, and the remaining close is PROJECTED (INFERRED) at about %s - so an OW-15 owner check-in is owed "
                 "before the launch that would cross 55,000,000." % (format(c["LOWER_BOUND"], ","),
                                                                     format(pos["headroom"]["UPPER_BOUND"], ","),
                                                                     format(PROJECTION["total"], ","))),
    "raised_by": "orchestrator (claude-opus-5)", "status": "RECORDED - owner check-in owed before the crossing launch",
    "blocks_close": True,
    "recovered": {
        "unreceipted_attempts": {"author-wave lanes 01-06": 2020709, "remediation batch": 298238,
                                 "spot lanes 1-3": 1157822, "total": 3476769,
                                 "receipts": ["Ezek/author/ezek_author_wave_attempt_receipts.jsonl",
                                              "Ezek/author/ezek_remediation_attempt_receipts.jsonl",
                                              "Ezek/reviews/spot/ezek_spot_attempt_receipts.jsonl"]},
        "unavailable_that_was_available": {"#e12": 502905, "#e13": 365746, "#e14": 221050, "boss audit": 847447,
                                           "total": 1937148, "as": "appended amendments"},
        "source": "the runtime's completion notifications preserved in the session transcript (75 agents, 21,891,417 tokens)",
        "tiers": "figures MEASURED (runtime-reported); attribution to attempts INFERRED - these launches recorded no agent id and no attempt id",
    },
    "census_v2": {"file": "Ezek/ezek_ow15_position.v2.json", "sha256": sha(EZ / "ezek_ow15_position.v2.json"),
                  "LOWER_BOUND": c["LOWER_BOUND"], "headroom_UPPER_BOUND": pos["headroom"]["UPPER_BOUND"],
                  "measured_in_full": c["measured_in_full"], "partial": c["measured_only_in_part"],
                  "declared_unmeasured": c["unmeasured_declared"], "undeclared": c["unmeasured_UNDECLARED"]},
    "projection_to_close": PROJECTION,
    "consequence": ("OW-15 (c): the owner is checked in with before any launch that would cross the ceiling. The "
                    "projection says the close crosses it, so the check-in is raised NOW rather than at the crossing "
                    "launch, and no launch that would cross is made without it. OW-16 stands: budget is a limit, not a "
                    "driver - no lane is dropped and no review narrowed to stay under it."),
    "defects_of_mine_in_this_recovery": [
        "E13-95 said Ezekiel's budget column carried '0 undeclared blanks'. That was true of the receipts that EXIST and "
        "silent about attempts that produced none - ten of them, 3,476,769 tokens.",
        "I paired author lanes 01 and 04 to their digests by the order of a SORTED printout and wrote digest PREFIXES "
        "into sha256 fields; the pairing proved right by luck, and full digests were appended by amendment from the "
        "queue's explicit mapping and the files on disk.",
        "my census v2 first dropped v1's resolution of UNAVAILABLE-declaring amendments and reported two declared "
        "attempts as undeclared; restored before the figure was recorded.",
    ],
    "other_carried_obligations": [
        "the transcript map (SP/Ezek/_transcript_map.ezek.json) has no entry after the primaries for the peer round, boss "
        "audit, rulings #e12-#e15, the author wave, the spot wave or the remediation batch; their agent ids are now in "
        "the late receipts and the amendments and can be mapped through the guarded patch tool",
        "the resume prompt's BUDGET line still states 39,426,659 and its OPERATIONAL LAWS sentence still calls the pre-8M "
        "check-in LIVE for Ezekiel; both are corrected at the next durability checkpoint",
    ],
}
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(q, ensure_ascii=False) + "\n")

LJ, LM = M8 / "error_pattern_ledger.v1.jsonl", M8 / "ERROR_PATTERN_LEDGER.v1.md"
row = {
    "id": "E-38", "kind": "error_pattern", "date": "2026-09-16",
    "headline": "a census over records cannot see work that produced no record - ten attempts and 3.5M tokens were invisible to it",
    "severity": "high",
    "severity_basis": ("no over-spend happened, but the budget position was understated by 6,052,556 tokens (15%%) at the "
                       "moment the remaining close was being planned; the projection now crosses the ceiling, which the "
                       "understated figure hid"),
    "instance": ("the author-wave lanes, the remediation batch and the spot lanes landed and were applied without attempt "
                 "receipts; four receipts declared UNAVAILABLE a token figure the runtime had reported. The census summed "
                 "receipt rows, and a 'zero undeclared blanks' report was true only of the rows that existed."),
    "cure": [
        "reconcile the receipt census against the runtime's own notification log at every book close and before every "
        "budget statement - the notification log is the denominator, the receipts are the record",
        "a landing is not complete until its attempt receipt exists; the landing script refuses to apply a deliverable "
        "that has no receipt",
        "a 'no blanks' claim names its denominator: blanks among the receipts that exist, never blanks in the work done",
    ],
    "tier": "MEASURED - the notifications, the receipts and the census were all read from disk",
    "provenance": {"book": "Ezek", "found_by": "orchestrator (claude-opus-5)", "found_at": NOW, "queue": "E13-101"},
}
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join([
        "", "## E-38 - a census over records cannot see work that produced no record", "",
        "**Instance.** Ten attempts - the six author-wave lanes, the remediation batch and the three spot lanes - landed "
        "and were applied with no attempt receipt, and four receipts declared UNAVAILABLE a token figure the runtime had "
        "in fact reported. The OW-15 census summed receipt rows, so 3,476,769 tokens were invisible and 1,937,148 more "
        "were recorded as unknown. A report of \"zero undeclared blanks\" was true of the receipts that existed and "
        "silent about the attempts that produced none. Recovered from the runtime's completion notifications in the "
        "session transcript: the census moved from 39,426,659 to 45,479,215, and the remaining close is now projected "
        "to cross the ceiling - which the understated figure had hidden.", "",
        "**Cure.** (1) Reconcile the receipt census against the runtime notification log at every book close and before "
        "every budget statement: the log is the denominator, the receipts are the record. (2) A landing is not complete "
        "until its attempt receipt exists; the landing refuses to apply a deliverable without one. (3) A \"no blanks\" "
        "claim names its denominator.", ""]))
print(json.dumps({"queue": "E13-101", "ledger": "E-38", "projection_total": PROJECTION["total"],
                  "queue_rows": sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()),
                  "ledger_rows": sum(1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip())}, indent=1))
