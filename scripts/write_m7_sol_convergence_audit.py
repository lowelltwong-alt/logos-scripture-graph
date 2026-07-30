#!/usr/bin/env python3
"""Persist the whole-Bible packet audit as candidate governance evidence."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    proc = subprocess.run([sys.executable, str(ROOT / "scripts/validate_m7_sol_whole_bible_packet_convergence.py")], cwd=ROOT, text=True, capture_output=True)
    line = next((x for x in proc.stdout.splitlines() if x.startswith("{")), "{}")
    out = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/packet_convergence_audit.json"
    out.write_text(json.dumps(json.loads(line), indent=2) + "\n", encoding="utf-8", newline="\n")
    print(out)
    return proc.returncode

if __name__ == "__main__": raise SystemExit(main())
