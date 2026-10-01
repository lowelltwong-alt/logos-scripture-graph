#!/usr/bin/env python3
"""Receipt execution #e2 of both close-gate audit lanes, and record what the second failure PROVES that the first did not.

THE DIAGNOSIS CHANGED, AND THAT IS THE POINT OF RUNNING IT TWICE. Execution #e1 of both lanes failed with HTTP 429
"out of usage credits" while the account's five-hour window stood at 95 percent, so the obvious reading was that the
short window was exhausted and the lanes would run after it reset. The window then rolled over - MEASURED at 6 percent
used, fresh until 2026-09-22T06:10Z - the brief pins were re-verified MATCH, and both lanes were relaunched. They
failed again, same HTTP 429, same message, same model. A hypothesis that survives a 95-percent window and a 6-percent
window is not a window hypothesis. The blocker is the MODEL: claude-fable-5-1 cannot be dispatched on this account's
plan (Pro), and the error's own advice - "switch to another model" - together with extra usage being disabled
(0.00 spent of a 65.00 monthly limit) is consistent with Fable needing credits this plan does not grant.

WHY THIS MATTERS BEYOND TWO RECEIPTS. OW-13 assigns the checking and adjudicating role to Fable 5.1, and OW-19
forbids the orchestrator from grading its own work. Ezekiel's close gate therefore cannot be graded by the model the
directives name, and no retry changes that. Enabling extra usage is a financial setting and is the owner's alone;
substituting a different model in a role an owner directive assigns is also the owner's call, not the orchestrator's.
The book is held at the gate with every non-Fable item finished, and the decision is put to the owner.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
R2 = EZ / "repair2"
TASKS = (r"C:\Users\lowel\AppData\Local\Temp\claude"
         r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
         r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\tasks\%s.output")
NOW = datetime.now(timezone.utc).isoformat()

# lane, agent_id, request_id  - request ids are copied from the runtime's own failure notifications
LANES = [("a", "a8779d9785b355135", "req_011CfHbn4MZLLUgabVmyr63F"),
         ("b", "a820a104a53bc70f2", "req_011CfHbnxuuerDzN7YTZm2gZ")]

rows = []
for lane, agent_id, req in LANES:
    brief = R2 / ("CLOSE_AUDIT_BRIEF_%s.md" % lane.upper())
    out = Path(TASKS % agent_id)
    rows.append({
        "schema": "m8_attempt_receipt.v1",
        "attempt_id": "ezek_close_audit_lane_%s_a1" % lane,
        "execution_id": "ezek_close_audit_lane_%s_a1#e2" % lane,
        "execution_of": "ezek_close_audit_lane_%s_a1" % lane,
        "execution_ordinal": 2,
        "previous_execution_id": "ezek_close_audit_lane_%s_a1#e1" % lane,
        "retry_of": "ezek_close_audit_lane_%s_a1#e1" % lane,
        "why_retried": ("#e1 failed on HTTP 429 while the five-hour window stood at 95 percent; the window then "
                        "rolled over to 6 percent used, which made a retry a materially different attempt rather "
                        "than a repetition of a failed action"),
        "book": "Ezek", "lane": "close_gate_audit_%s" % lane,
        "role": "blind audit lane over close-gate items 20-23 (OW-19 floor; the orchestrator may not grade its own work)",
        "producer": "Fable 5.1 (ordered)", "catcher": "n/a - the lane IS the catcher",
        "agent": "general-purpose subagent", "parent_agent_id": agent_id,
        "model": "claude-fable-5-1", "model_actual": "NONE - refused before any model work",
        "effort": "n/a", "orders": str(brief),
        "brief": str(brief), "brief_sha256": hashlib.sha256(brief.read_bytes()).hexdigest(),
        "brief_pins_verified_before_launch": "MATCH - 21 of 21 pins, _brief_pin_check.py, immediately before launch",
        "launched_at": NOW, "recorded_at": NOW,
        "outcome": "FAILED AT LAUNCH - no audit was performed and no finding of any kind exists",
        "error": {"http": 429, "type": "rate_limit", "request_id": req,
                  "message": "You're out of usage credits. Switch to another model, or manage usage credits",
                  "model_sent_to_api": "claude-fable-5-1"},
        "account_state_when_it_failed": {
            "tier": "MEASURED - read from the account usage card minutes before this launch",
            "plan": "Pro", "five_hour_window_percent_used": 6, "five_hour_resets_at": "2026-09-22T06:10:00Z",
            "weekly_all_models_percent_used": 14, "extra_usage_enabled": False,
            "extra_usage_spent_of_limit": "0.00 of 65.00 USD",
            "per_model_weekly_window": "ABSENT from the usage card - the card reports only 5-hour and weekly-all-models"},
        "diagnosis": {
            "tier": "INFERRED from two measurements, and the inference is the whole value of the retry",
            "ruled_out": ("the five-hour window. #e1 failed at 95 percent used and #e2 failed at 6 percent used with "
                          "an identical error, so window exhaustion does not explain it."),
            "standing_explanation": ("claude-fable-5-1 is not dispatchable on this plan. The error itself advises "
                                     "switching model, and extra usage is disabled with nothing spent."),
            "not_established": ("that enabling extra usage would make Fable run. Nothing here measures that, and it "
                                "is a paid setting only the owner may change.")},
        "output_file": str(out),
        "output_bytes": out.stat().st_size if out.exists() else None,
        "output_sha256": None, "final_message_sha256": None, "deliverable_source": None,
        "tokens_reported": "UNAVAILABLE",
        "token_note": ("the runtime's notification reports status failed and carries NO usage block - no "
                       "subagent_tokens, no tool_uses, no duration_ms - and the task output file is 0 bytes. The "
                       "spend is UNRECOVERABLE, not zero."),
        "e19_selfreported": "n/a - the lane never ran",
        "form_defects": [], "tool_uses": None,
        "consequence_for_the_close": ("close-gate items 20-23 have NO independent grade. The orchestrator authored "
                                      "items 21, 22 and 23 and may not grade them (OW-19), and OW-13 names Fable for "
                                      "the checking role. Ezekiel is HELD at the gate, not closed and not waived; "
                                      "every item that does not need Fable is finished."),
    })

p = EZ / "ezek_close_audit_attempt_receipts.jsonl"
pre = p.read_bytes() if p.exists() else b""
existing = {json.loads(l).get("execution_id") for l in pre.decode("utf-8").splitlines() if l.strip()}
new = [r for r in rows if r["execution_id"] not in existing]
with p.open("a", encoding="utf-8", newline="\n") as fh:
    for r in new:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
if not p.read_bytes().startswith(pre):
    raise SystemExit("INTEGRITY FAILURE: %s was not appended to" % p.name)
print(json.dumps({"file": p.name, "appended": [r["execution_id"] for r in new],
                  "total_rows": len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]),
                  "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}, ensure_ascii=False, indent=1))
