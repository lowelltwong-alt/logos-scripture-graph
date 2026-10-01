#!/usr/bin/env python3
"""Derive append_delta_launch_v10.py and land_delta_v10.py from their pinned v9 originals by exact, counted
substitutions (no regex), and create the empty v10 receipts file. Write-new: same bytes left, different bytes refused.
Every substitution must occur exactly the number of times stated, and no v9 token may survive in the output.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
V9 = HERE.parent / "fixround_v9"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
SRC = {"append_delta_launch_v9.py": ("append_delta_launch_v10.py", None),
       "land_delta_v9.py": ("land_delta_v10.py", None)}
COMMON = [("fixround_v9", "fixround_v10"), ("delta_v9", "delta_v10"), ("DELTA_BRIEF_V9_", "DELTA_BRIEF_V10_"),
          ("ezek_fixround_v9_", "ezek_fixround_v10_"), ("one v9 blind delta lane", "one v10 blind delta lane"),
          ("one v9 delta re-check lane", "one v10 delta re-check lane"), ("ezek_delta_v9_landing.v1", "ezek_delta_v10_landing.v1"),
          ("land_delta_v9.py", "land_delta_v10.py"), ("append_delta_launch_v9.py", "append_delta_launch_v10.py")]
SPECIFIC = {
    "append_delta_launch_v9.py": [
        ('("blind delta re-check lane %s over rows_v9_final (OW-19 floor of two; OW-28): lineage, the three changed "\n'
         '                "rows, the v1 docket, derived records, items 22 and 23, the typed gate dispositions, both verdicts. "\n'
         '                "Checks and reports; applies nothing" % L.upper())',
         '("blind delta re-check lane %s over rows_v10_final (OW-19 floor of two; OW-28; OW-30): lineage v9->v10, "\n'
         '                "the eight ruled holds as implemented, derived records, item 22, both verdicts. "\n'
         '                "Checks and reports; applies nothing" % L.upper())', 1),
        ('"producer": "the v9 fix round (bounded author ezek_fixround_v9_author_a1 and the orchestrator\'s builds)"',
         '"producer": "the v10 hold round (Fable\'s OW-30 ruling, implemented by the orchestrator\'s builds)"', 1)],
    "land_delta_v9.py": []}
NL = (r'(b"" if before.endswith(b"\n") else b"\n")', r'(b"" if not before or before.endswith(b"\n") else b"\n")', 1)
for v in SPECIFIC.values():
    v.append(NL)
TOKENS = ("v9", "V9")
res = {}
for name, (out_name, _) in SRC.items():
    s = (V9 / name).read_bytes().decode("utf-8")
    if "\r" in s:
        raise SystemExit("REFUSED: %s carries CR bytes" % name)
    for a, b, n in SPECIFIC[name]:
        if s.count(a) != n:
            raise SystemExit("REFUSED: %s: specific anchor occurs %d times, not %d: %r" % (name, s.count(a), n, a[:60]))
        s = s.replace(a, b)
    counts = {}
    for a, b in COMMON:
        counts[a] = s.count(a)
        s = s.replace(a, b)
    left = [ln for ln in s.splitlines() if any(t in ln.replace("v9->v10", "") for t in TOKENS)]
    if left:
        raise SystemExit("REFUSED: %s keeps v9 tokens: %s" % (out_name, left[:4]))
    p, b = HERE / out_name, s.encode("utf-8")
    if p.exists() and p.read_bytes() != b:
        raise SystemExit("REFUSED: %s exists with different bytes" % out_name)
    if not p.exists():
        p.write_bytes(b)
    res[out_name] = {"from": name, "from_sha256": sha((V9 / name).read_bytes()), "sha256": sha(b),
                     "substitutions": {k: v for k, v in counts.items() if v}}
rec = HERE / "ezek_fixround_v10_attempt_receipts.jsonl"
if not rec.exists():
    rec.write_bytes(b"")
res[rec.name] = {"sha256": sha(rec.read_bytes()), "bytes": rec.stat().st_size}
print(json.dumps(res, indent=1))
