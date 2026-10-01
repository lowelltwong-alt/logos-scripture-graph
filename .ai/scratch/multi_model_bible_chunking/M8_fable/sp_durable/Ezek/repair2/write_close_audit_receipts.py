#!/usr/bin/env python3
"""Receipt the two blind close-gate audit attempts, both of which failed at launch (OW-7: every attempt is receipted).

WHAT HAPPENED, MEASURED. Both lanes were launched 2026-09-21 with model claude-fable-5-1 and both terminated before
doing any work with HTTP 429, error type rate_limit, message "You're out of usage credits". The account's own usage
card, read immediately afterwards, shows the 5-HOUR window at 95 percent (resets 2026-09-21T23:30Z) while the weekly
all-models window stands at 13 percent - so this is the five-hour window, not the weekly exhaustion that stopped the
lanes on 2026-09-16, and extra usage is disabled.

WHY THIS IS WORTH RECORDING BEYOND THE RECEIPT. These two failures are a live instance of the exact signature the
residual record (ezek_ow15_residual.v1.json) attributed to the eighteen unmeasurable attempts: the runtime's
completion notification reports status failed, carries NO usage block at all, and the task output file it names is
0 bytes. Both .output files here were measured at 0 bytes. That was an inference about past attempts; it is now an
OBSERVED property of a failure of this kind on this machine. It does not make the eighteen recoverable - it confirms
why they are not, and it means these two attempts are themselves unmeasurable spend, however small.
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
R2 = EZ / "repair2"
TASKS = (r"C:\Users\lowel\AppData\Local\Temp\claude"
         r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
         r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\tasks\%s.output")
NOW = datetime.now(timezone.utc).isoformat()

LANES = [("a", "a6b0d88ea3d72bfde", "req_011CfHHdmRWHsQvvtJzBxV4y"),
         ("b", "a9d7aae5ecddffbe8", "req_011CfHHeWMvSU9CAuU8K3A3s")]

rows = []
for lane, agent_id, req in LANES:
    brief = R2 / ("CLOSE_AUDIT_BRIEF_%s.md" % lane.upper())
    out = Path(TASKS % agent_id)
    rows.append({
        "schema": "m8_attempt_receipt.v1",
        "attempt_id": "ezek_close_audit_lane_%s_a1" % lane,
        "execution_id": "ezek_close_audit_lane_%s_a1#e1" % lane,
        "execution_of": "ezek_close_audit_lane_%s_a1" % lane,
        "execution_ordinal": 1, "previous_execution_id": None, "retry_of": None,
        "book": "Ezek", "lane": "close_gate_audit_%s" % lane,
        "role": "blind audit lane over close-gate items 20-23 (OW-19 floor: two blind lanes, neither the author)",
        "producer": "Fable 5.1 (ordered)", "catcher": "n/a - the lane IS the catcher",
        "role_separation": ("the orchestrator authored items 21, 22 and 23 and must not audit them; that is why these "
                            "lanes exist and why the proposal adjudication is a third, separate execution"),
        "agent": "general-purpose subagent", "parent_agent_id": agent_id,
        "model": "claude-fable-5-1", "model_actual": "NONE - the request was refused before any model work",
        "effort": "n/a", "orders": str(brief),
        "brief": str(brief), "brief_sha256": hashlib.sha256(brief.read_bytes()).hexdigest(),
        "launched_at": NOW, "recorded_at": NOW,
        "outcome": "FAILED AT LAUNCH - no audit was performed and no finding of any kind exists",
        "error": {"http": 429, "type": "rate_limit", "request_id": req,
                  "message": "You're out of usage credits. Switch to another model, or manage usage credits",
                  "model_sent_to_api": "claude-fable-5-1"},
        "account_state_when_it_failed": {
            "tier": "MEASURED - read from the account usage card immediately after the failure",
            "plan": "Pro", "five_hour_window_percent_used": 95, "five_hour_resets_at": "2026-09-21T23:30:00Z",
            "weekly_all_models_percent_used": 13, "weekly_resets_at": "2026-09-28T14:00:00Z",
            "extra_usage_enabled": False,
            "so": "this is the FIVE-HOUR window, not the weekly exhaustion that stopped the 2026-09-16 lanes"},
        "output_file": str(out),
        "output_bytes": out.stat().st_size if out.exists() else None,
        "output_sha256": None, "final_message_sha256": None, "deliverable_source": None,
        "tokens_reported": "UNAVAILABLE",
        "token_note": ("the runtime's completion notification for this attempt reports status failed and carries NO "
                       "usage block - no subagent_tokens, no tool_uses, no duration_ms - and the task output file it "
                       "names is 0 bytes. The spend is therefore UNRECOVERABLE, not zero. This is the same signature "
                       "ezek_ow15_residual.v1.json records for the eighteen unmeasurable attempts, observed live here."),
        "e19_selfreported": "n/a - the lane never ran",
        "form_defects": [], "tool_uses": None,
        "how_to_read": ("an attempt that failed at launch still consumed something and still counts as an attempt. It "
                        "is receipted so the census sees it; its spend is declared UNAVAILABLE, never assumed zero."),
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
                  "already_present": sorted(existing), "bytes": p.stat().st_size,
                  "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}, ensure_ascii=False, indent=1))
