#!/usr/bin/env python3
"""Regression test for the TRUNCATION GUARD in sp_durable/orchestrator_scratch/_mirror_transcripts.py.

WHY IT EXISTS. The mirror refreshes a durable transcript copy whenever the live file's digest differs. That is right
for a transcript still GROWING and destructive for one DECAYING: a truncation to a shorter non-zero size would
overwrite the fuller durable copy with the damaged one. The guard refuses to replace a durable copy with a smaller
live file. The first edit of that guard referenced an uninitialised list and would have crashed on the first real
shrink - so this file exists to make sure the guard is exercised, not merely present.

SAFETY. Runs entirely inside a temp directory. The tool's destination is redirected with M8_MIRROR_DST, so the real
durable transcript store is never touched.

Usage: _test_mirror_truncation_guard.py      exit 0 = GREEN, exit 1 = RED
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "orchestrator_scratch" / "_mirror_transcripts.py"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if not TOOL.is_file():
        print(json.dumps({"verdict": "RED", "why": "tool not found at %s" % TOOL}))
        return 1
    tmp = Path(tempfile.mkdtemp())
    try:
        sess = tmp / "fake_session"
        sc, tasks, dst = sess / "sc", sess / "tasks", tmp / "store"
        for d in (sc, tasks, dst):
            d.mkdir(parents=True)
        shutil.copy(TOOL, sc / "_mirror_transcripts.py")
        head = json.dumps({"agentId": "x", "isSidechain": True}) + "\n"

        def w(p, n):
            p.write_text(head + ("y" * n), encoding="utf-8")

        w(tasks / "grow.output", 500)
        w(dst / "grow.output", 100)          # live LARGER  -> copied
        w(tasks / "shrink.output", 100)
        w(dst / "shrink.output", 900)        # live SMALLER -> REFUSED, durable kept
        (tasks / "zero.output").write_text("", encoding="utf-8")
        w(dst / "zero.output", 700)          # zero bytes   -> skipped, durable kept
        w(tasks / "same.output", 300)
        shutil.copy(tasks / "same.output", dst / "same.output")   # identical -> unchanged
        w(tasks / "new.output", 250)         # not in store -> copied
        (tasks / "shell.output").write_text("not json at all\n", encoding="utf-8")   # not a transcript

        before = {p.name: sha(p) for p in dst.glob("*.output")}
        env = dict(os.environ, M8_MIRROR_DST=str(dst), PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, str(sc / "_mirror_transcripts.py")],
                           capture_output=True, text=True, env=env)
        try:
            out = json.loads(r.stdout)
        except Exception:
            print(json.dumps({"verdict": "RED", "why": "tool output not JSON", "stdout": r.stdout[:400],
                              "stderr": r.stderr[:400]}))
            return 1
        after = {p.name: sha(p) for p in dst.glob("*.output")}

        checks = [
            ("exit 0", r.returncode == 0),
            ("a grown live file is copied", after.get("grow.output") == sha(tasks / "grow.output")),
            ("a SHRUNK live file is refused and the larger durable copy is kept",
             after.get("shrink.output") == before["shrink.output"]),
            ("the refusal is reported, not silent",
             out.get("refused_shrink_count") == 1 and out["refused_shrink"][0]["file"] == "shrink.output"),
            ("a zero-byte live file never overwrites a durable copy",
             after.get("zero.output") == before["zero.output"]),
            ("an identical file is left unchanged", out.get("unchanged") == 1),
            ("a new transcript is copied", "new.output" in after),
            ("orchestrator shell output is excluded by content",
             "shell.output" not in after and out.get("skipped_not_transcript") == 1),
            ("copied is exactly grow + new", out.get("copied") == 2),
        ]
        failed = [n for n, ok in checks if not ok]
        print(json.dumps({"tool": str(TOOL), "tool_sha256": sha(TOOL),
                          "checks": len(checks), "passed": len(checks) - len(failed), "failed": failed,
                          "verdict": "GREEN" if not failed else "RED"}, indent=1))
        return 1 if failed else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
