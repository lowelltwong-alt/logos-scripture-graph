#!/usr/bin/env python3
"""Land the strategy v2 author's deliverables as a CANDIDATE (not yet the book's strategy): digests checked against the
agent's report, every collected order disposed, durable copy under Ezek/author/strategy_v2/, receipt. Promotion to
Ezek/book_strategy_Ezek.v2.md happens only after the distinct Fable check returns fit (a separate step).

usage: python land_strategy_v2.py --agent-id <id> --v2-sha <hex> --dispositions-sha <hex> --tokens <n> --tool-uses <n>
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
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_strategy_v2")
DST = EZ / "author" / "strategy_v2"
REC = DST / "ezek_strategy_v2_attempt_receipts.jsonl"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
arg = lambda n: sys.argv[sys.argv.index(n) + 1]                                # noqa: E731
att, exe = "ezek_strategy_v2_author_a1", "ezek_strategy_v2_author_a1#e1"
want = {"book_strategy_Ezek.v2.md": arg("--v2-sha"), "strategy_v2_dispositions.json": arg("--dispositions-sha")}
for n, w in want.items():
    if sha((SRC / n).read_bytes()) != w:
        raise SystemExit("REFUSED: %s digest differs from the agent's report" % n)
orders = json.loads((HERE / "strategy_v2_orders.v2.json").read_text(encoding="utf-8"))
disp = json.loads((SRC / "strategy_v2_dispositions.json").read_text(encoding="utf-8"))
blob = json.dumps(disp, ensure_ascii=False)
n_expected = len(orders["orders"]) + len(orders["structural_orders"])
DST.mkdir(parents=True, exist_ok=True)
pre = REC.read_bytes() if REC.exists() else b""
if exe.encode("utf-8") in pre:
    raise SystemExit("REFUSED: a receipt for %s already exists" % exe)
files = {}
for n, w in want.items():
    b = (SRC / n).read_bytes()
    (DST / n).write_bytes(b)
    if sha((DST / n).read_bytes()) != w:
        raise SystemExit("REFUSED: durable copy of %s does not match" % n)
    files[n] = {"sha256": w, "bytes": len(b), "durable": "Ezek/author/strategy_v2/%s" % n}
r = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_strategy_v2", "book": "Ezek", "attempt_id": att, "execution_id": exe,
     "execution_of": att, "execution_ordinal": 1, "previous_execution_id": None, "retry_of": None,
     "agent": "strategy v2 author (#e15 close clearance item 4)", "agent_id": arg("--agent-id"), "parent_agent_id": "orchestrator",
     "session": "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4", "model": "claude-opus-5",
     "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
     "brief": {"file": "Ezek/repair2/strategy_v2/STRATEGY_V2_AUTHOR_BRIEF.md", "sha256": sha((HERE / "STRATEGY_V2_AUTHOR_BRIEF.md").read_bytes())},
     "outcome": "COMPLETED - CANDIDATE LANDED, HELD FOR THE DISTINCT CHECK; digests match", "deliverables": files,
     "orders_expected": n_expected, "reported": json.loads(arg("--reported")),
     "tokens_reported": int(arg("--tokens")), "tool_uses": int(arg("--tool-uses")), "duration_ms": int(arg("--duration-ms")),
     "token_note": "runtime-reported subagent tokens from the completion notification", "recorded_at": datetime.now(timezone.utc).isoformat()}
with REC.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
if not REC.read_bytes().startswith(pre):
    raise SystemExit("REFUSED: receipt file prefix changed")
print(json.dumps({"landed": att, "orders_expected": n_expected, "reported_dispositions": r["reported"].get("dispositions"),
                  "dispositions_bytes": len(blob)}, indent=1))
