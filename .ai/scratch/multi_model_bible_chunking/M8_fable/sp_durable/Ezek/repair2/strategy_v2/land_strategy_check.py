#!/usr/bin/env python3
"""Land the strategy v2 DISTINCT CHECK: digest checked against the checker's report, durable copy, receipt. Landing the
check is what clears its in-flight pin on the candidate, so it happens BEFORE the corrections are applied.

usage: python land_strategy_check.py --agent-id <id> --ordinal N --check-sha <hex> --tokens <n> --tool-uses <n>
                                     --duration-ms <n> --reported <json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SRC = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_strategy_v2_check\strategy_v2_check.json")
DST = EZ / "author" / "strategy_v2"
REC = DST / "ezek_strategy_v2_attempt_receipts.jsonl"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
arg = lambda n: sys.argv[sys.argv.index(n) + 1]                                # noqa: E731
att = "ezek_strategy_v2_check_a1"
ORD = int(arg("--ordinal"))
exe = "%s#e%d" % (att, ORD)
want = arg("--check-sha")
b = SRC.read_bytes()
if sha(b) != want:
    raise SystemExit("REFUSED: strategy_v2_check.json digest %s differs from the report %s" % (sha(b), want))
chk = json.loads(b.decode("utf-8"))
pre = REC.read_bytes() if REC.exists() else b""
if exe.encode("utf-8") in pre:
    raise SystemExit("REFUSED: a receipt for %s already exists" % exe)
DST.mkdir(parents=True, exist_ok=True)
(DST / "strategy_v2_check.json").write_bytes(b)
if sha((DST / "strategy_v2_check.json").read_bytes()) != want:
    raise SystemExit("REFUSED: the durable copy does not match")
brief = HERE / "STRATEGY_V2_CHECK_BRIEF.md"
r = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_strategy_v2", "book": "Ezek", "attempt_id": att, "execution_id": exe,
     "execution_of": att, "execution_ordinal": ORD,
     "previous_execution_id": ("%s#e%d" % (att, ORD - 1)) if ORD > 1 else None,
     "retry_of": ("%s#e%d" % (att, ORD - 1)) if ORD > 1 else None,
     "agent": "strategy v2 distinct checker (OW-10; OW-13 Fable checks)", "agent_id": arg("--agent-id"),
     "parent_agent_id": "orchestrator", "session": "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4", "model": "claude-fable-5-1",
     "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
     "brief": {"file": "Ezek/repair2/strategy_v2/" + brief.name, "sha256": sha(brief.read_bytes())},
     "outcome": "COMPLETED - CHECK LANDED; verdict %s; %d dispositions confirmed, %d defects each carrying an exact correction"
                % (chk.get("verdict"), (chk.get("disposition_counts") or {}).get("confirmed", len(chk.get("dispositions") or [])),
                   len(chk.get("defects") or [])),
     "deliverables": {"strategy_v2_check.json": {"sha256": want, "bytes": len(b), "durable": "Ezek/author/strategy_v2/strategy_v2_check.json"}},
     "verdict": chk.get("verdict"), "defect_ids": [d.get("id") for d in (chk.get("defects") or [])],
     "reported": json.loads(arg("--reported")), "tokens_reported": int(arg("--tokens")), "tool_uses": int(arg("--tool-uses")),
     "duration_ms": int(arg("--duration-ms")),
     "token_note": "runtime-reported subagent tokens from the completion notification",
     "recorded_at": datetime.now(timezone.utc).isoformat()}
with REC.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
if not REC.read_bytes().startswith(pre):
    raise SystemExit("REFUSED: receipt file prefix changed")
print(json.dumps({"landed": exe, "verdict": chk.get("verdict"), "defects": [d.get("id") for d in (chk.get("defects") or [])]}, indent=1))
