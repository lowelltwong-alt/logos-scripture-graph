#!/usr/bin/env python3
"""Land one FINAL REMEDIATION deliverable - an author lane or a slice's Fable adjudication: digests checked against the
agent's report, the orchestrator's own gate run read (ALL_CLEAN, no hard member gaining a flag), durable copy, receipt.

Append-only and prefix-checked; refuses a second receipt for the same execution. A lane whose gate run is not clean is
refused here - it is recorded by the orchestrator as a form defect instead, never landed.

usage: python land_final.py --role lane --slice K --lane A|B | --role adjudication --slice K
       --agent-id <id> --proposal-sha <hex> --second-sha <hex> --rerun-out <gate stdout file>
       --tokens <n> --tool-uses <n> --duration-ms <n> --reported <json>
       (--second-sha is discharge.json for a lane, adjudication.json for an adjudication)
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final")
REC = EZ / "author" / "final" / "ezek_final_attempt_receipts.jsonl"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731


def arg(n):
    return sys.argv[sys.argv.index(n) + 1]


role, k = arg("--role"), int(arg("--slice"))
if role == "lane":
    lane = arg("--lane").upper()
    name = "s%d_lane_%s" % (k, lane.lower())
    second, model = "discharge.json", "claude-opus-5"
    brief = EZ / "repair2" / "final" / ("FINAL_AUTHOR_BRIEF_S%d_%s.md" % (k, lane))
    agent = "final remediation author, slice %d, blind lane %s of 2" % (k, lane)
elif role == "adjudication":
    name = "s%d_adjudication" % k
    second, model = "adjudication.json", "claude-fable-5-1"
    brief = EZ / "repair2" / "final" / ("FINAL_ADJUDICATION_BRIEF_S%d.md" % k)
    agent = "final remediation controlling adjudicator, slice %d (OW-13: Fable adjudicates)" % k
else:
    raise SystemExit("usage: --role lane|adjudication")
att = "ezek_final_%s_a1" % name
ORD = int(arg("--ordinal")) if "--ordinal" in sys.argv else 1
exe = "%s#e%d" % (att, ORD)
want = {"proposal.json": arg("--proposal-sha"), second: arg("--second-sha")}
src = SCR / name
for n, w in want.items():
    if sha((src / n).read_bytes()) != w:
        raise SystemExit("REFUSED: %s digest %s differs from the agent's report %s" % (n, sha((src / n).read_bytes()), w))
t = Path(arg("--rerun-out")).read_text(encoding="utf-8")
a = json.loads(t[t.rfind('{\n "ALL_CLEAN"'):t.rfind('{\n "COMPLETION_MEASURE"')])
cm = json.loads(t[t.rfind('{\n "COMPLETION_MEASURE"'):])["COMPLETION_MEASURE"]
if not a["ALL_CLEAN"] or a["suite"]["hard_members_that_GAINED_flags"]:
    raise SystemExit("REFUSED: the orchestrator's gate run is not clean: %s" % {k2: a[k2] for k2 in ("ALL_CLEAN", "rows_unclean")})
REC.parent.mkdir(parents=True, exist_ok=True)
pre = REC.read_bytes() if REC.exists() else b""
if exe.encode("utf-8") in pre:
    raise SystemExit("REFUSED: a receipt for %s already exists" % exe)
dst = EZ / "author" / "final" / name
dst.mkdir(parents=True, exist_ok=True)
files = {}
for n, w in want.items():
    b = (src / n).read_bytes()
    (dst / n).write_bytes(b)
    if sha((dst / n).read_bytes()) != w:
        raise SystemExit("REFUSED: durable copy of %s does not match" % n)
    files[n] = {"sha256": w, "bytes": len(b), "durable": "Ezek/author/final/%s/%s" % (name, n)}
r = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_final_remediation", "book": "Ezek",
     "attempt_id": att, "execution_id": exe, "execution_of": att, "execution_ordinal": ORD,
     "previous_execution_id": ("%s#e%d" % (att, ORD - 1)) if ORD > 1 else None,
     "retry_of": ("%s#e%d" % (att, ORD - 1)) if ORD > 1 else None, "agent": agent, "agent_id": arg("--agent-id"), "parent_agent_id": "orchestrator",
     "session": "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4", "model": model,
     "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
     "brief": {"file": "Ezek/repair2/final/" + brief.name, "sha256": sha(brief.read_bytes())},
     "outcome": ("COMPLETED - DELIVERABLE LANDED AND HELD FOR ADJUDICATION; digests match" if role == "lane"
                 else "COMPLETED - DELIVERABLE LANDED; digests match"),
     "deliverables": files, "reported": json.loads(arg("--reported")),
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
print("landed", name, "| gate", a["suite"]["candidate_summary"], "| register left on owed rows", cm.get("register_flags_left_on_owed_rows"))
