#!/usr/bin/env python3
"""Land one REPAIR-2 step-5 Fable adjudication: digests, the orchestrator's gate re-run, durable copy, receipt.

usage: python land_adjudication.py --half <1|2> --agent-id <id> --proposal-sha <hex> --adjudication-sha <hex>
                                   --rerun-out <gate stdout> --tokens <n> --tool-uses <n> --duration-ms <n> --reported <json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_adjudication")
REC = EZ / "author" / "repair2_step5" / "ezek_repair2_step5_attempt_receipts.jsonl"


def arg(n):
    return sys.argv[sys.argv.index(n) + 1]


h = int(arg("--half"))
att = "ezek_repair2_step5_h%d_adjudication_a1" % h
exe = att + "#e1"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
want = {"proposal.json": arg("--proposal-sha"), "adjudication.json": arg("--adjudication-sha")}
src = SCR / ("h%d" % h)
for n, w in want.items():
    if sha((src / n).read_bytes()) != w:
        raise SystemExit("REFUSED: %s digest differs from the adjudicator's report" % n)
t = Path(arg("--rerun-out")).read_text(encoding="utf-8")
a = json.loads(t[t.rfind('{\n "ALL_CLEAN"'):t.rfind('{\n "COMPLETION_MEASURE"')])
cm = json.loads(t[t.rfind('{\n "COMPLETION_MEASURE"'):])["COMPLETION_MEASURE"]
if not a["ALL_CLEAN"] or a["suite"]["hard_members_that_GAINED_flags"]:
    raise SystemExit("REFUSED: the orchestrator's gate run is not clean")
pre = REC.read_bytes()
if exe.encode("utf-8") in pre:
    raise SystemExit("REFUSED: a receipt for %s already exists" % exe)
dst = EZ / "author" / "repair2_step5" / ("h%d_adjudication" % h)
dst.mkdir(parents=True, exist_ok=True)
files = {}
for n, w in want.items():
    b = (src / n).read_bytes()
    (dst / n).write_bytes(b)
    if sha((dst / n).read_bytes()) != w:
        raise SystemExit("REFUSED: durable copy of %s does not match" % n)
    files[n] = {"sha256": w, "bytes": len(b), "durable": "Ezek/author/repair2_step5/h%d_adjudication/%s" % (h, n)}
brief = EZ / "repair2" / "step5" / ("STEP5_ADJUDICATION_BRIEF_HALF%d.md" % h)
r = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_repair2_step5_register_prose", "book": "Ezek",
     "attempt_id": att, "execution_id": exe, "execution_of": att, "execution_ordinal": 1, "previous_execution_id": None,
     "retry_of": None, "agent": "step-5 controlling adjudicator, half %d (OW-13: Fable adjudicates)" % h,
     "agent_id": arg("--agent-id"), "parent_agent_id": "orchestrator", "session": "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4",
     "model": "claude-fable-5-1", "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
     "brief": {"file": "Ezek/repair2/step5/" + brief.name, "sha256": sha(brief.read_bytes())},
     "outcome": "COMPLETED - DELIVERABLE LANDED; digests match", "deliverables": files, "reported": json.loads(arg("--reported")),
     "orchestrator_gate_rerun": {"ALL_CLEAN": a["ALL_CLEAN"], "rows_unclean": a["rows_unclean"],
                                 "hard_gained": a["suite"]["hard_members_that_GAINED_flags"],
                                 "summary": a["suite"]["candidate_summary"], "completion": cm},
     "tokens_reported": int(arg("--tokens")), "tool_uses": int(arg("--tool-uses")), "duration_ms": int(arg("--duration-ms")),
     "token_note": "runtime-reported subagent tokens from the completion notification",
     "recorded_at": datetime.now(timezone.utc).isoformat()}
with REC.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
if not REC.read_bytes().startswith(pre):
    raise SystemExit("REFUSED: receipt file prefix changed")
print("landed half %d adjudication | gate %s | register left on owed rows %s" % (h, a["suite"]["candidate_summary"], cm.get("register_flags_left_on_owed_rows")))
