#!/usr/bin/env python3
"""Resume smoke (session 2026-08-28): bare Jer.9.1 vs MT 8:23 bytes -> byte tier;
Jer.10.11 -> byte tier + language Aramaic. Invokes the real collate.py CLI."""
import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent / "tools"
sys.path.insert(0, str(TOOLS))
from jer_lib import load_verse_maps  # noqa: E402

_, oshb = load_verse_maps()
mt_823 = oshb["Jer.8.23"]["text"]
mt_1011 = oshb["Jer.10.11"]["text"]

results = {}
for name, ref, quote in (("zone_seam", "Jer.9.1", mt_823), ("aramaic_island", "Jer.10.11", mt_1011)):
    p = subprocess.run([sys.executable, str(TOOLS / "collate.py"), "--ref", ref, "--quote", quote],
                       capture_output=True, text=True, encoding="utf-8")
    results[name] = {"exit": p.returncode, "out": json.loads(p.stdout)}

r1, r2 = results["zone_seam"]["out"], results["aramaic_island"]["out"]
ok = (r1["tier"] == "byte" and r1["mt_window"] == "Jer.8.23-8.23"
      and r2["tier"] == "byte" and r2["language"] == "Aramaic")
print(json.dumps({"results": results, "smoke": "PASS" if ok else "FAIL"}, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
