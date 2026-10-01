#!/usr/bin/env python3
"""Preserve one step-2 author lane's deliverable durably and write its attempt receipt (OW-7).

HELD, NOT LANDED. A lane's proposal is not applied here - it cannot be until both blind lanes are in and
reconciled. What this does is the E-29 duty (write early): the deliverable is copied byte-for-byte out of the
session scratchpad into the durable tree, digests checked on both sides, and the attempt is recorded with its
runtime token figure, so a lost session cannot lose the lane.

usage: python land_lane.py a 293322 48 1666697
"""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
DUR = EZ / "author" / "repair2_step2"
REC = DUR / "ezek_repair2_step2_attempt_receipts.jsonl"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731

lane, tokens, tool_uses, ms = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
src = HERE / ("lane_%s" % lane)
dst = DUR / ("lane_%s" % lane)
dst.mkdir(parents=True, exist_ok=True)

files = {}
for name in ("proposal.json", "discharge.json"):
    b = (src / name).read_bytes()
    json.loads(b.decode("utf-8"))                       # must parse, or nothing is recorded
    (dst / name).write_bytes(b)
    if sha((dst / name).read_bytes()) != sha(b):
        raise SystemExit("REFUSED: the durable copy of %s does not match its source" % name)
    files[name] = {"sha256": sha(b), "bytes": len(b), "durable": "Ezek/author/repair2_step2/lane_%s/%s"
                   % (lane, name)}

attempt = "ezek_repair2_step2_lane_%s_a1" % lane
if REC.exists():
    for l in REC.read_text(encoding="utf-8").splitlines():
        if l.strip() and json.loads(l).get("execution_id") == attempt + "#e1":
            raise SystemExit("REFUSED: a receipt for %s#e1 already exists" % attempt)

d = json.loads((src / "discharge.json").read_text(encoding="utf-8"))
rows = d.get("rows", {})
receipt = {
    "schema": "m8_attempt_receipt.v1",
    "lane": "ezek_repair2_step2_grounds",
    "book": "Ezek",
    "attempt_id": attempt,
    "execution_id": attempt + "#e1",
    "execution_of": attempt,
    "execution_ordinal": 1,
    "previous_execution_id": None,
    "retry_of": None,
    "agent": "step-2 grounds author, blind lane %s of 2" % lane.upper(),
    "parent_agent_id": "orchestrator",
    "model": "claude-opus-5",
    "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
    "effort": "ORDERED session default, NOT VERIFIED",
    "producer": "REPAIR-2 step 2 per #e15 repair2_batch_composition_and_sequence item 2",
    "catcher": ("scratchpad/ezek_step2/check_candidate.py (register arms + refs/citation mirror, in memory); "
                "the orchestrator RE-RAN it on the delivered proposal rather than accepting the lane's report"),
    "role_separation": "the lane proposes; the orchestrator reconciles two blind lanes and applies",
    "outcome": "COMPLETED - DELIVERABLE HELD, NOT APPLIED (awaiting the second blind lane and reconciliation)",
    "recorded_at": datetime.now(timezone.utc).isoformat(),
    "brief": {"file": "scratchpad/ezek_step2/STEP2_BRIEF.md",
              "sha256": sha((HERE / "STEP2_BRIEF.md").read_bytes())},
    "inputs": {"slices_sha256": sha((HERE / "step2_slices.v1.json").read_bytes()),
               "gate_sha256": sha((HERE / "check_candidate.py").read_bytes()),
               "rows_at_dispatch": "1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425"},
    "deliverables": files,
    "orchestrator_verification": json.loads((HERE / ("lane_%s_verification.json" % lane)).read_text(
        encoding="utf-8")),
    "counts_from_the_deliverable": {
        "rows": len(rows),
        "orders_discharged": sum(len(v.get("orders_discharged", [])) for v in rows.values()),
        "stops": sum(len(v.get("stops", [])) for v in rows.values()),
        "disagreements": sum(len(v.get("disagreements", [])) for v in rows.values()),
    },
    "tokens_reported": tokens,
    "tool_uses": tool_uses,
    "duration_ms": ms,
    "token_note": "runtime-reported subagent tokens for this execution, from its completion notification",
    "e19_selfreported": d.get("e19_selfreport") or d.get("limit"),
}
with REC.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")
print(json.dumps({"receipt": REC.name, "attempt": attempt, "tokens_reported": tokens,
                  "deliverables": files, "receipts_sha256": sha(REC.read_bytes())}, indent=1))
