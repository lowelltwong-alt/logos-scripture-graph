#!/usr/bin/env python3
"""Record launch-time transcript-map entries through SP/campaign/_guarded_json_patch.py (dry run, then apply).

Every launch is mapped WHILE the agent runs (L-0017): the in-flight pin guard reads this map, so an unmapped launch is
invisible to the one control that stops a pinned input changing underneath a running agent.

usage: python map_launch.py --spec <spec.json> [--apply]
  spec = {"entries": [{"attempt_id", "agent_id", "role", "brief", "model_ordered", "rows"}]}
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
    if k in current:
        raise SystemExit("REFUSED: %s already mapped" % k)
    brief = SP / e["brief"]
    edits.append({"key": k, "expect_before": "__ABSENT__", "why": "transcript-map entry recorded at launch (L-0017)",
                  "set": {"attempt_id": k, "execution_id": k + "#e1", "agent_id": e["agent_id"], "session": SESSION,
                          "role": e["role"], "brief": e["brief"].replace("\\", "/"),
                          "brief_sha256": sha(brief) if brief.is_file() else "UNAVAILABLE - brief not found at map time",
                          "model_ordered": e["model_ordered"], "launched_at": NOW, "rows": e["rows"],
                          "runtime_transcript_expected_at": SUB % (SESSION, e["agent_id"]),
                          "note": "recorded at launch, while the agent runs (L-0017)"}})
plan = {"target": str(MAP), "expect_file_sha256": sha(MAP), "edits": edits,
        "receipt": str(SP / "Ezek" / "repair2" / ("_map_patch_receipt_%s.json" % NOW[:19].replace(":", "")))}
pp = Path(__file__).resolve().parent / "_map_launch_plan.json"
pp.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
args = [sys.executable, "-B", str(TOOL), "--plan", str(pp)] + (["--apply"] if "--apply" in sys.argv else [])
p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
d = json.loads(p.stdout[p.stdout.find("{"):])
print(json.dumps({k: d.get(k) for k in ("status", "keys_addressed", "file_sha256_after", "postvalidation")}, indent=1))
