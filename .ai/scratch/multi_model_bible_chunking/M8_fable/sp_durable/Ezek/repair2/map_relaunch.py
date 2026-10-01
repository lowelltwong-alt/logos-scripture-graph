#!/usr/bin/env python3
"""Re-map an attempt whose previous execution FAILED, as a new execution ordinal, through the guarded JSON patch.

map_launch.py refuses a key that is already mapped, which is right for a first launch and wrong for a relaunch: the
attempt id is the same, the execution is a new ordinal, and the map must carry the new agent id so the in-flight pin
guard follows the execution that is actually running. This addresses the existing key by its exact current value, keeps
the failed execution in the entry (so the history is not overwritten) and refuses if the entry moved.

usage: python map_relaunch.py --spec <spec.json> [--apply]
  spec = {"entries": [{"attempt_id", "agent_id", "ordinal", "role", "brief", "model_ordered", "rows"}]}
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
MAP = SP / "Ezek" / "_transcript_map.ezek.json"
TOOL = SP / "campaign" / "_guarded_json_patch.py"
SESSION = "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4"
SUB = (r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
       r"\%s\subagents\agent-%s.jsonl")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

spec = json.loads(Path(sys.argv[sys.argv.index("--spec") + 1]).read_text(encoding="utf-8"))
NOW = datetime.now(timezone.utc).isoformat()
current = json.loads(MAP.read_text(encoding="utf-8"))
edits = []
for e in spec["entries"]:
    k = e["attempt_id"]
    if k not in current:
        raise SystemExit("REFUSED: %s is not mapped; use map_launch.py for a first launch" % k)
    prev = current[k]
    n = int(e["ordinal"])
    brief = SP / e["brief"]
    edits.append({"key": k, "expect_before": prev, "why": "relaunch as execution ordinal %d after a failed execution (L-0017)" % n,
                  "set": {"attempt_id": k, "execution_id": "%s#e%d" % (k, n), "agent_id": e["agent_id"], "session": SESSION,
                          "role": e["role"], "brief": e["brief"].replace("\\", "/"),
                          "brief_sha256": sha(brief) if brief.is_file() else "UNAVAILABLE - brief not found at map time",
                          "model_ordered": e["model_ordered"], "launched_at": NOW, "rows": e["rows"],
                          "runtime_transcript_expected_at": SUB % (SESSION, e["agent_id"]),
                          "execution_ordinal": n,
                          "previous_executions": (prev.get("previous_executions") or []) + [
                              {"execution_id": prev.get("execution_id"), "agent_id": prev.get("agent_id"),
                               "launched_at": prev.get("launched_at"), "outcome": e.get("previous_outcome", "FAILED - weekly usage limit (429); no deliverable")}],
                          "note": "recorded at launch, while the agent runs (L-0017)"}})
plan = {"target": str(MAP), "expect_file_sha256": sha(MAP), "edits": edits,
        "receipt": str(SP / "Ezek" / "repair2" / ("_map_relaunch_receipt_%s.json" % NOW[:19].replace(":", "")))}
pp = Path(__file__).resolve().parent / "_map_relaunch_plan.json"
pp.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
args = [sys.executable, "-B", str(TOOL), "--plan", str(pp)] + (["--apply"] if "--apply" in sys.argv else [])
p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
d = json.loads(p.stdout[p.stdout.find("{"):]) if "{" in p.stdout else {"stderr": p.stderr[-400:]}
print(json.dumps({k: d.get(k) for k in ("status", "keys_addressed", "file_sha256_after", "postvalidation", "stderr")}, indent=1))
