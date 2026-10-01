#!/usr/bin/env python3
"""Record the 2026-09-16 weekly-rate-limit failures, and the two owner directives of 2026-09-21 (OW-23, OW-24).

Eleven executions died mid-flight on a weekly usage limit (HTTP 429), each with NO completion usage figure, so their
spend is real but UNMEASURED - the receipt census cannot see it (the E-38 shape). This writes:
  (1) a FAILED receipt per execution, which also clears the in-flight pin guard (in flight = mapped with no receipt);
  (2) queue entry E13-113 with the failure list and the budget disclosure;
  (3) ledger rows OW-23 (hardest books first; Revelation named) and OW-24 (token economy), plus the markdown addenda.
Nothing is overwritten; every append is prefix-checked.

usage: python record_ratelimit_failures.py
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
M8 = EZ.parent.parent
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
LED = M8 / "error_pattern_ledger.v1.jsonl"
LEDMD = M8 / "ERROR_PATTERN_LEDGER.v1.md"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
FAILED = [
    ("ezek_final_s1_adjudication_a1", "a24f3f3ce7de04e33", "claude-fable-5-1", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl",
     "final remediation controlling adjudicator, slice 1", "wrote its own working dumps (items 161KB, e17 58KB) before the limit"),
    ("ezek_final_s2_adjudication_a1", "a9dc1f9a5122abb42", "claude-fable-5-1", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl",
     "final remediation controlling adjudicator, slice 2", "had read its lanes and begun the remaining 21 rows"),
    ("ezek_final_s3_lane_a_a1", "a8e2d24ee557df40b", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 3, lane A", ""),
    ("ezek_final_s3_lane_b_a1", "a524752dbc26d9804", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 3, lane B", ""),
    ("ezek_final_s4_lane_a_a1", "a23d26c93c03639e9", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 4, lane A", ""),
    ("ezek_final_s4_lane_b_a1", "a2260abbae3b3a8a5", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 4, lane B", ""),
    ("ezek_final_s5_lane_a_a1", "a825ef7d3f1f6fa2e", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 5, lane A", ""),
    ("ezek_final_s5_lane_b_a1", "a09cd95e6bc96cc26", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 5, lane B", ""),
    ("ezek_final_s6_lane_a_a1", "a926616c3b5bf8b50", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 6, lane A", ""),
    ("ezek_final_s6_lane_b_a1", "a92bbc5b9c7cf0494", "claude-opus-5", EZ / "author" / "final", "ezek_final_attempt_receipts.jsonl", "author, slice 6, lane B", ""),
    ("ezek_strategy_v2_check_a1", "a8e45168098e063fb", "claude-fable-5-1", EZ / "author" / "strategy_v2", "ezek_strategy_v2_attempt_receipts.jsonl",
     "strategy v2 distinct check (OW-10)", "had bound all 17 pinned digests as matching before the limit"),
]
written = []
for att, agent_id, model, dst, recname, role, note in FAILED:
    rec = dst / recname
    dst.mkdir(parents=True, exist_ok=True)
    pre = rec.read_bytes() if rec.exists() else b""
    exe = att + "#e1"
    if exe.encode("utf-8") in pre:
        continue
    r = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_final_remediation" if "final" in att else "ezek_strategy_v2",
         "book": "Ezek", "attempt_id": att, "execution_id": exe, "execution_of": att, "execution_ordinal": 1,
         "previous_execution_id": None, "retry_of": None, "agent": role, "agent_id": agent_id, "parent_agent_id": "orchestrator",
         "session": "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4", "model": model,
         "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
         "outcome": ("FAILED - the runtime terminated this execution on the account's WEEKLY USAGE LIMIT (HTTP 429, "
                     "2026-09-16). No deliverable was written and nothing was landed. A new execution ordinal is owed."),
         "deliverables": {}, "failure": {"kind": "rate_limit", "http": 429, "at": "2026-09-16", "reset": "2026-09-21T10:00-04:00",
                                         "observed": note or "terminated before any deliverable"},
         "tokens_reported": "UNAVAILABLE - a failed execution carries no completion usage figure; the spend is real and "
                            "unmeasured, and the receipt census cannot see it (E-38 shape)",
         "recorded_at": NOW}
    with rec.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    assert rec.read_bytes().startswith(pre)
    written.append(att)

qpre = Q.read_bytes()
if not any(json.loads(l).get("id") == "E13-113" for l in qpre.decode("utf-8").splitlines() if l.strip()):
    e = {"id": "E13-113", "opened_at": NOW, "severity": "HIGH", "tier": "MEASURED for what landed; the failures' spend is UNAVAILABLE",
         "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
         "status": "OPEN: the final remediation stands at slices 1-2 authored (4 lanes landed) with every adjudication and slices 3-6 OWED",
         "headline": ("Eleven executions died on the account's WEEKLY USAGE LIMIT (HTTP 429) on 2026-09-16, minutes after launch: both "
                      "slice adjudicators, all eight slice 3-6 author lanes, and the strategy v2 distinct check. No deliverable was "
                      "written by any of them; nothing was landed; the rows never moved (03327cf4). FAILED receipts are now written, "
                      "which also clears the in-flight pin guard."),
         "what_survived": {"landed_lanes": ["ezek_final_s1_lane_a_a1 (457,871)", "ezek_final_s1_lane_b_a1 (437,352)",
                                            "ezek_final_s2_lane_a_a1 (477,225)", "ezek_final_s2_lane_b_a1 (445,589)"],
                           "landed_candidate": "ezek_strategy_v2_author_a1 (365,630) - held for its distinct check",
                           "rows": "03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554 (138 rows)"},
         "budget_disclosure": ("the measured lower bound stands at 62,181,504 for receipted agents plus 365,630 for the strategy author "
                               "= 62,547,134 of the 72,000,000 hard line. The eleven failed executions spent real tokens that NO receipt "
                               "and NO notification records; the census cannot see them. The position is therefore a LOWER BOUND with a "
                               "known gap, not a complete figure, and the gap is disclosed rather than estimated into the census."),
         "owner_directives": {"OW-23": "after Ezekiel closes, the hardest books come first - Revelation named - and Revelation is gated by "
                                       "the unmade Greek-witness decision",
                              "OW-24": "token economy: cache reads are the real bill; the fix is installed globally (settings, hooks, a "
                                       "weekly deterministic watchdog) and written into the global policy"},
         "relaunch_rule": ("each owed execution relaunches as a NEW ordinal (#e2) under its own attempt id, never by reusing #e1; the brief "
                           "digests are re-checked (_brief_pin_check MATCH) because the pinned inputs must not have moved")}
    with Q.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    assert Q.read_bytes().startswith(qpre)

lpre = LED.read_bytes()
rows = []
if b'"OW-23"' not in lpre:
    rows.append({"id": "OW-23", "at": NOW, "kind": "owner_directive", "book_scope": "campaign",
                 "directive": ("2026-09-21, owner verbatim: 'lets do the hardest books first after you complete this, revelation, and what "
                               "ever else is anticpated to be very hard to chunk properly.' Ezekiel finishes first; then the remaining books "
                               "are ordered HARDEST FIRST, with Revelation named."),
                 "constraint_surfaced": ("Revelation is Greek New Testament. The campaign has no staged Greek witness, and the OW-19 lens floor "
                                         "plus a single-witness Greek text is what currently gates 27 of the 42 remaining books. The witness "
                                         "choice (which Greek text, under which licence, with what apparatus) is the owner's and is owed before "
                                         "Revelation's Phase 0. Daniel (OW-20) remains authorized and is Hebrew-Aramaic, so it is not gated."),
                 "owed": "at Ezekiel's close, bring the owner (a) the Greek-witness options with licences, (b) a measured difficulty ranking of "
                         "the remaining books so 'hardest first' is a measurement, not an impression"})
if b'"OW-24"' not in lpre:
    rows.append({"id": "OW-24", "at": NOW, "kind": "owner_directive", "book_scope": "every project on this machine",
                 "directive": ("2026-09-21, owner: optimise the token burn - 'cache read' is 'killing out tokens', '1.2 billion tokens is insane'; "
                               "compact/clear/reset at the appropriate time; 'make this something you do universally no matter the chat or project'; "
                               "and run a periodic subagent that reads token usage, fixes new waste, and re-checks at an interval that is not too "
                               "often because it costs tokens."),
                 "measured": ("one orchestrating session: 5,566 requests, 2.61e9 cache-read tokens, 3.0e7 cache writes, 1.16e7 output. Weighted "
                              "(read 0.1x, write 2x, out 5x) carrying cost: Write payloads 284M, Bash results 216M, Bash commands 100M, Agent "
                              "prompts 44M. Cause is structural: each payload in context is re-read by every later request."),
                 "cure": ("global CLAUDE.md section 20; ~/.claude/settings.json autoCompactWindow 200000, bashOutputMaxChars 8000, "
                          "taskOutputMaxChars 8000; three hooks from ~/.claude/hooks/token_economy.py (read-guard denies whole-file reads over "
                          "400KB, write-nudge over 20KB, tick every 150 tool calls, reset on PostCompact); weekly 'token-economy-watchdog' "
                          "scheduled task running token_economy_audit.py --if-due, which measures with zero model tokens, escalates only on "
                          "ISSUES, and sets its own next date (2 days after ISSUES, 7 after OK)."),
                 "m8_consequence": ("subagent briefs pin scoped extracts, not whole witnesses; agents are told to build in one pass and bound "
                                    "their gate runs; the orchestrator compacts at every phase boundary.")})
if rows:
    with LED.open("a", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    assert LED.read_bytes().startswith(lpre)
    md = LEDMD.read_bytes()
    add = ("\n\n## OWNER DIRECTIVE OW-23 (2026-09-21) - HARDEST BOOKS FIRST, REVELATION NAMED\n\n"
           "Ezekiel finishes first. After it, the remaining books are taken HARDEST FIRST; the owner named Revelation. **Revelation is Greek "
           "New Testament and the campaign has no staged Greek witness**: with the OW-19 lens floor, that unmade decision gates 27 of the 42 "
           "remaining books. The witness choice - which Greek text, under which licence, with what apparatus - is the owner's, and is owed "
           "before Revelation's Phase 0. Daniel (OW-20) is Hebrew-Aramaic and is not gated. Owed at Ezekiel's close: the Greek-witness options "
           "with licences, and a MEASURED difficulty ranking of the remaining books so that 'hardest first' rests on measurement.\n\n"
           "## OWNER DIRECTIVE OW-24 (2026-09-21) - TOKEN ECONOMY, UNIVERSAL\n\n"
           "Cache reads are the bill. Measured on one orchestrating session: 5,566 requests, **2.61 billion cache-read tokens**; weighted "
           "carrying cost led by Write payloads (284M), Bash results (216M), Bash commands (100M) and Agent prompts (44M). Cost is not per "
           "call: every payload in context is re-read by every later request. Cure, installed globally on 2026-09-21: global policy section 20; "
           "`autoCompactWindow` 200000 with `bashOutputMaxChars`/`taskOutputMaxChars` 8000; three hooks (whole-file reads above 400KB refused, "
           "large-write nudge, a compaction reminder every 150 tool calls, reset on compaction); and a weekly deterministic watchdog that "
           "measures with no model tokens, only escalates on ISSUES, and widens its own interval while things are in order. For M8: subagents "
           "get scoped extracts rather than whole witnesses, are told to build in one pass with bounded gate runs, and the orchestrator "
           "compacts at every phase boundary.\n")
    with LEDMD.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(add)
    assert LEDMD.read_bytes().startswith(md)
print(json.dumps({"failed_receipts_written": written, "ledger_rows": [r["id"] for r in rows],
                  "queue_rows": sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip())}, indent=1))
