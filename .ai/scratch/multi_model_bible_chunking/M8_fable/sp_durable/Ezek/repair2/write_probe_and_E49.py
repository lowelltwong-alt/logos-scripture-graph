#!/usr/bin/env python3
"""Receipt the Fable dispatch probe, and amend E-48 with what the probe settles.

WHY A PROBE INSTEAD OF A FIFTH RETRY. Four launches had failed with the same HTTP 429 on claude-fable-5-1, and a fifth
identical launch would have added nothing. Retry discipline requires a materially different attempt, so the fifth
dispatch was made as small as a dispatch can be: one line of instruction, no file reads, no tool use of any kind,
ordered to reply with the single word OK. It failed with the same error. That eliminates every explanation that
depends on the SIZE of the work - brief bytes, pinned inputs, context, tool budget - and leaves the model itself.

WHY THIS IS AN AMENDMENT AND NOT AN EDIT. E-48 reads, in its own bytes, that the close gate "cannot be graded at all
until the window resets". That sentence is now known to be wrong, and E-44's lesson is that a position is destroyed by
being edited rather than superseded. So E-48 keeps its bytes and E-49 states what replaced them. The error in E-48 is
worth preserving: it is an instance of the very habit this ledger exists to catch - the first plausible cause was
adopted because it was measurable, and the measurement was real but was not a test of the hypothesis.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
TASK = Path(r"C:\Users\lowel\AppData\Local\Temp\claude"
            r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
            r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\tasks\ab7e0fb137fddb461.output")
NOW = datetime.now(timezone.utc).isoformat()

probe = {
    "schema": "m8_attempt_receipt.v1",
    "attempt_id": "ezek_fable_dispatch_probe_a1", "execution_id": "ezek_fable_dispatch_probe_a1#e1",
    "execution_of": "ezek_fable_dispatch_probe_a1", "execution_ordinal": 1,
    "previous_execution_id": None, "retry_of": None,
    "book": "Ezek", "lane": "diagnostic",
    "role": ("a deliberately minimal dispatch, to separate 'this model cannot be dispatched' from 'this particular "
             "launch was too large'. Not a review lane and it grades nothing."),
    "producer": "Fable 5.1 (ordered)", "catcher": "n/a",
    "agent": "general-purpose subagent", "parent_agent_id": "ab7e0fb137fddb461",
    "model": "claude-fable-5-1", "model_actual": "NONE - refused before any model work",
    "effort": "n/a",
    "orders": ("inline, 5 lines: reply with exactly the word OK; no tool use of any kind, no file read, no directory "
               "listing, no git; carried the OW-11 authority paragraph"),
    "brief": None, "brief_sha256": None,
    "launched_at": NOW, "recorded_at": NOW,
    "outcome": "FAILED AT LAUNCH",
    "error": {"http": 429, "type": "rate_limit", "request_id": "req_011CfHc78KDG3znGmj5kfibE",
              "message": "You're out of usage credits. Switch to another model, or manage usage credits",
              "model_sent_to_api": "claude-fable-5-1"},
    "what_this_attempt_ELIMINATES": [
        "brief size - this dispatch had no brief and read no file",
        "pinned-input cost - it opened nothing",
        "context or tool budget - it was forbidden every tool",
        "the five-hour window - measured at 6 percent used, fresh until 2026-09-22T06:10Z",
        "the weekly all-models window - measured at 14 percent used",
    ],
    "what_REMAINS": ("claude-fable-5-1 is not dispatchable on this account as configured. The error's own remedy is to "
                     "switch model or add usage credits, and extra usage is disabled with 0.00 of 65.00 USD spent."),
    "tier": "MEASURED by elimination across five dispatches; the CAUSE inside Anthropic's billing is not observable here",
    "output_file": str(TASK), "output_bytes": TASK.stat().st_size if TASK.exists() else None,
    "output_sha256": None, "final_message_sha256": None, "deliverable_source": None,
    "tokens_reported": "UNAVAILABLE",
    "token_note": "status failed, no usage block, 0-byte output - the same signature as the four audit-lane failures",
    "e19_selfreported": "n/a - the lane never ran", "form_defects": [], "tool_uses": None,
}

p = EZ / "ezek_close_audit_attempt_receipts.jsonl"
pre = p.read_bytes()
if probe["execution_id"] not in {json.loads(l).get("execution_id")
                                 for l in pre.decode("utf-8").splitlines() if l.strip()}:
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(probe, ensure_ascii=False) + "\n")
if not p.read_bytes().startswith(pre):
    raise SystemExit("INTEGRITY FAILURE: receipts file was not appended to")

delta = """
## E-49 (2026-09-21) - AMENDS E-48: THE FIRST MEASURABLE CAUSE WAS ADOPTED WITHOUT TESTING IT

E-48 recorded that the two blind close-gate lanes failed on the account's five-hour usage window, measured at 95
percent with the weekly window at 13 percent, and concluded the gate "cannot be graded at all until the window
resets". The measurement was real. The conclusion was not tested. The window then reset - MEASURED at 6 percent used,
fresh for five hours - the brief pins were re-verified MATCH, and both lanes were relaunched. **Both failed again with
the identical HTTP 429.** A cause that holds at 95 percent and at 6 percent is not the window.

Rather than launch a fifth identical lane, the next dispatch was made as small as a dispatch can be: one line of
instruction, no brief, no file read, every tool forbidden, ordered to reply with the single word `OK`. It failed the
same way. That eliminates brief size, pinned-input cost, context and tool budget, and both usage windows. What remains
is the model: **`claude-fable-5-1` is not dispatchable on this account as configured**, which is also what the error
says in its own words - switch model, or add usage credits - with extra usage disabled at 0.00 of 65.00 USD.

**The lesson is not about a rate limit.** Five dispatches over two window states produced one diagnosis in about an
hour, and four of them were spent on a hypothesis that a single cheap probe would have refuted first. The habit to
break: *a measurement taken next to a failure is not a test of the failure's cause*. The five-hour window was at 95
percent, which was true, available and causally plausible - and being the first true thing found is not evidence.
**Cure: before retrying a failure whose cause is inferred, spend the smallest dispatch that would DISCRIMINATE between
the candidate causes, and prefer the probe that can falsify rather than the retry that can only confirm.** A probe
that costs one line is cheaper than any retry of the real work, and the cheapest probe is the one that removes every
variable except the one under test.

**The governance consequence stands and is now permanent rather than temporary.** OW-13 names Fable 5.1 for the
checking and adjudicating role; OW-19 forbids the orchestrator from grading its own work. Close-gate items 20-23 are
authored by the orchestrator and therefore have no admissible grader on this account today. An Opus lane is not a
substitute - same family and, for these items, the same author, which OW-19 counts as one voice. Ezekiel is therefore
**HELD at the close gate with every non-Fable item finished**, and the choice between enabling paid credits, naming a
different grader, or accepting a recorded grading gap is the owner's, not the orchestrator's. **E-48's design lesson
survives its own diagnosis being wrong: a governance floor that depends on a single named model can vanish for
reasons the campaign does not control, so the floor needs a declared fallback grader chosen in advance - by the
owner - rather than improvised at the gate by the agent the floor exists to check.**
"""

d = EZ / "repair2" / "ledger_delta_E49.md"
d.write_text(delta, encoding="utf-8", newline="\n")
led = M8 / "ERROR_PATTERN_LEDGER.v1.md"
lpre = led.read_bytes()
if "## E-49 " not in lpre.decode("utf-8"):
    with led.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(delta)
if not led.read_bytes().startswith(lpre):
    raise SystemExit("INTEGRITY FAILURE: the ledger was not appended to")

txt = led.read_text(encoding="utf-8")
print(json.dumps({
    "receipts_file": p.name,
    "receipt_rows": len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]),
    "receipts_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
    "ledger_bytes": led.stat().st_size, "ledger_grew_by": led.stat().st_size - len(lpre),
    "ledger_entries": txt.count("\n## E-"), "ledger_sha256": hashlib.sha256(led.read_bytes()).hexdigest(),
    "E49_present": "## E-49 " in txt,
}, ensure_ascii=False, indent=1))
