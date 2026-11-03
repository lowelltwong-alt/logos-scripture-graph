#!/usr/bin/env python3
"""Regression test for build_review_launch.red_members (2026-10-20): the suite's per_check values are plain strings, and
a dict-only filter dropped "ngram7: RED" from the S1 brief's book-wide line in a dry run. Writes nothing.

usage: python -B test_red_members.py   (prints PASS or exits non-zero)
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_review_launch import red_members  # noqa: E402

cases = [
    ({"ngram7": "RED", "web_quotes": "GREEN", "greek_normalize_dryrun": "ok=619 fixed=0 defects=0"}, ["ngram7"]),
    ({"universals": "FLAGS", "register": {"status": "RED"}, "cap_sweep": {"status": "GREEN"}}, ["register", "universals"]),
    ({"greek_normalize_dryrun": "ok=10 fixed=0 defects=2"}, ["greek_normalize_dryrun"]),
    ({"a": "GREEN", "b": "PASS"}, []),
]
for per_check, want in cases:
    got = red_members(per_check)
    if got != want:
        raise SystemExit("FAIL: %r -> %r, want %r" % (per_check, got, want))
try:
    red_members({"x": "MAYBE"})
except SystemExit as e:
    if "unrecognised status" not in str(e):
        raise SystemExit("FAIL: wrong refusal %r" % e)
else:
    raise SystemExit("FAIL: an unrecognised status was not refused")
print("PASS", len(cases) + 1)
