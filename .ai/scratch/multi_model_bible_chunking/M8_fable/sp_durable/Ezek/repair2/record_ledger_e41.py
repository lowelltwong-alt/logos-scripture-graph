#!/usr/bin/env python3
"""Append ledger E-41 (a generator re-run rewrote a file a running agent pinned) - append-only, idempotent, prefix-checked."""
import json
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
LJ, LM = M8 / "error_pattern_ledger.v1.jsonl", M8 / "ERROR_PATTERN_LEDGER.v1.md"
row = {"id": "E-41", "kind": "error_pattern", "date": "2026-09-16", "severity": "medium",
       "headline": "a generator re-run rewrote, in place, a file a running agent had pinned by digest",
       "instance": ("while the #e16 controlling-agent ruling was running, the orchestrator widened the step-7 reconciler (to read "
                    "a third out-of-scope key name) and re-ran it; the re-run rewrote Ezek/repair2/step7/step7_reconciled.v1.json, "
                    "which #e16's brief pins at 7da382ee... and whose change orders the agent to stop. The orchestrator saw it "
                    "within about two minutes, reproduced the pinned bytes exactly with the original extraction (--legacy; digest "
                    "7da382ee... verified) and wrote the widened reconciliation as a new v2 file. No row changed; whether the agent "
                    "hashed the file inside the window is known only when it returns."),
       "root_cause": ("the in-flight pin guard is run before RECORD writes, but a deterministic generator's output was not treated as a "
                      "record write, and the generator overwrote its versioned output unconditionally"),
       "cure": ("(1) generators refuse to overwrite an existing output whose bytes differ (reconcile_strides.py now does; --overwrite "
                "only after the in-flight guard); (2) a changed extraction writes a new version, never the pinned one; (3) before "
                "re-running any generator whose outputs a launch pinned, run the in-flight guard on each output path")}
md = """
## E-41 - a generator re-run rewrote, in place, a file a running agent had pinned by digest

**Instance.** While the #e16 ruling was running, the orchestrator widened the step-7 reconciler and re-ran it; the re-run rewrote step7_reconciled.v1.json, which #e16's brief pins (7da382ee...) and whose change orders the agent to stop. Seen within about two minutes; the pinned bytes were reproduced exactly (--legacy, digest verified) and the widened result written as a v2 file. No row changed; whether the agent hashed the file inside the window is known only when it returns.

**Root cause.** The in-flight guard ran before record writes, but a generator's output was not treated as one, and the generator overwrote its versioned output unconditionally.

**Cure.** Generators refuse to overwrite an existing output with different bytes (--overwrite only after the in-flight guard); a changed extraction writes a new version; run the in-flight guard on every output path before re-running a generator whose outputs a launch pinned.
"""
jl, mb = LJ.read_bytes(), LM.read_bytes()
if any(json.loads(l).get("id") == "E-41" for l in jl.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E-41 already recorded")
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(md)
assert LJ.read_bytes().startswith(jl) and LM.read_bytes().startswith(mb)
print("E-41 appended; ledger rows:", sum(1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip()))
