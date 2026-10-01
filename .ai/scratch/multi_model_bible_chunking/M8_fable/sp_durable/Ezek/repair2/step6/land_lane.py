#!/usr/bin/env python3
"""Land one REPAIR-2 step-6 author lane: digests checked, the orchestrator's gate re-run read, durable copy, receipt.

Refuses unless both deliverable digests equal the lane's report, the orchestrator's own gate run is ALL_CLEAN with no
hard member gaining a flag, and no receipt for this execution exists yet. Append-only, prefix-checked.

usage: python land_lane.py --lane h1_lane_a --agent-id <id> --proposal-sha <hex> --discharge-sha <hex>
                           --rerun-out <gate stdout file> --tokens <n> --tool-uses <n> --duration-ms <n> --reported <json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step6")
REC = EZ / "author" / "repair2_step6" / "ezek_repair2_step6_attempt_receipts.jsonl"


def arg(n):
    return sys.argv[sys.argv.index(n) + 1]


lane = arg("--lane")
half = int(lane[1])
att = "ezek_repair2_step6_%s_a1" % lane
exe = att + "#e1"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
want = {"proposal.json": arg("--proposal-sha"), "discharge.json": arg("--discharge-sha")}
src = SCR / lane
files = {}
for n, w in want.items():
    b = (src / n).read_bytes()
    if sha(b) != w:
        raise SystemExit("REFUSED: %s digest %s differs from the lane's report %s" % (n, sha(b), w))
t = Path(arg("--rerun-out")).read_text(encoding="utf-8")
a = json.loads(t[t.rfind('{\n "ALL_CLEAN"'):t.rfind('{\n "COMPLETION_MEASURE"')])
cm = json.loads(t[t.rfind('{\n "COMPLETION_MEASURE"'):])["COMPLETION_MEASURE"]
if not a["ALL_CLEAN"] or a["suite"]["hard_members_that_GAINED_flags"]:
    raise SystemExit("REFUSED: the orchestrator's gate run is not clean: %s" % {k: a[k] for k in ("ALL_CLEAN", "rows_unclean")})
REC.parent.mkdir(parents=True, exist_ok=True)
pre = REC.read_bytes() if REC.exists() else b""
if exe.encode("utf-8") in pre:
    raise SystemExit("REFUSED: a receipt for %s already exists" % exe)
dst = EZ / "author" / "repair2_step6" / lane
dst.mkdir(parents=True, exist_ok=True)
for n in want:
    b = (src / n).read_bytes()
    (dst / n).write_bytes(b)
    if sha((dst / n).read_bytes()) != want[n]:
        raise SystemExit("REFUSED: durable copy of %s does not match" % n)
    files[n] = {"sha256": want[n], "bytes": len(b), "durable": "Ezek/author/repair2_step6/%s/%s" % (lane, n)}
r = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_repair2_step6_transport_and_routed", "book": "Ezek",
     "attempt_id": att, "execution_id": exe, "execution_of": att, "execution_ordinal": 1, "previous_execution_id": None,
     "retry_of": None, "agent": "step-6 author, half %d, blind lane %s of 2" % (half, lane[-1].upper()),
     "agent_id": arg("--agent-id"), "parent_agent_id": "orchestrator", "session": "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4",
     "model": "claude-opus-5", "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
     "brief": {"file": "Ezek/repair2/step6/STEP6_AUTHOR_BRIEF_HALF%d.md" % half,
               "sha256": sha((EZ / "repair2" / "step6" / ("STEP6_AUTHOR_BRIEF_HALF%d.md" % half)).read_bytes())},
     "outcome": "COMPLETED - DELIVERABLE LANDED AND HELD FOR ADJUDICATION; digests match", "deliverables": files,
     "reported": json.loads(arg("--reported")),
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
print("landed", lane, "| gate", a["suite"]["candidate_summary"], "| register left on owed rows", cm.get("register_flags_left_on_owed_rows"))
