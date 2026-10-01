#!/usr/bin/env python3
"""Land one REPAIR-2 step-7 spot reader: digest check, parse check, durable copy, receipt (append-only, prefix-checked).

usage: python land_reader.py --lane s3_lane_a --agent-id <id> --sha <hex> --tokens <n> --tool-uses <n> --duration-ms <n>
                             --reported <json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step7")
REC = EZ / "author" / "repair2_step7" / "ezek_repair2_step7_attempt_receipts.jsonl"


def arg(n):
    return sys.argv[sys.argv.index(n) + 1]


lane = arg("--lane")
stride = int(lane[1])
att = "ezek_repair2_step7_%s_a1" % lane
exe = att + "#e1"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
b = (SCR / lane / "findings.json").read_bytes()
if sha(b) != arg("--sha"):
    raise SystemExit("REFUSED: findings.json digest %s differs from the reader's report" % sha(b))
f = json.loads(b.decode("utf-8-sig"))
slices = json.loads((EZ / "repair2" / "step7" / ("step7_spot_lane_%d.v1.json" % stride)).read_text(encoding="utf-8"))["slices"]
per_row = f.get("per_row") or {}
missing = sorted(set(slices) - set(per_row))
if missing:
    raise SystemExit("REFUSED: the reader's findings omit %d rows of its slice: %s" % (len(missing), missing[:10]))
REC.parent.mkdir(parents=True, exist_ok=True)
pre = REC.read_bytes() if REC.exists() else b""
if exe.encode("utf-8") in pre:
    raise SystemExit("REFUSED: a receipt for %s already exists" % exe)
dst = EZ / "author" / "repair2_step7" / lane
dst.mkdir(parents=True, exist_ok=True)
(dst / "findings.json").write_bytes(b)
if sha((dst / "findings.json").read_bytes()) != arg("--sha"):
    raise SystemExit("REFUSED: durable copy does not match")
brief = EZ / "repair2" / "step7" / ("STEP7_SPOT_BRIEF_STRIDE%d.md" % stride)
r = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_repair2_step7_spot_reread", "book": "Ezek",
     "attempt_id": att, "execution_id": exe, "execution_of": att, "execution_ordinal": 1, "previous_execution_id": None,
     "retry_of": None, "agent": "step-7 spot reader, stride %d, blind lane %s of 2" % (stride, lane[-1].upper()),
     "agent_id": arg("--agent-id"), "parent_agent_id": "orchestrator", "session": "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4",
     "model": "claude-opus-5", "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
     "brief": {"file": "Ezek/repair2/step7/" + brief.name, "sha256": sha(brief.read_bytes())},
     "outcome": "COMPLETED - FINDINGS LANDED; digest matches; every slice row answered",
     "deliverables": {"findings.json": {"sha256": arg("--sha"), "bytes": len(b), "durable": "Ezek/author/repair2_step7/%s/findings.json" % lane}},
     "reported": json.loads(arg("--reported")), "rows_in_slice": len(slices), "rows_answered": len(per_row),
     "tokens_reported": int(arg("--tokens")), "tool_uses": int(arg("--tool-uses")), "duration_ms": int(arg("--duration-ms")),
     "token_note": "runtime-reported subagent tokens from the completion notification",
     "recorded_at": datetime.now(timezone.utc).isoformat()}
with REC.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
if not REC.read_bytes().startswith(pre):
    raise SystemExit("REFUSED: receipt file prefix changed")
print("landed", lane, "| rows answered", len(per_row), "of", len(slices))
