#!/usr/bin/env python3
"""Amend _close_book.py (v9b, 2026-09-23): the --acf choice must meet the campaign coverage validator's per-book feed rule.

Why. checks/validate_book_review_coverage.py (lines 177-194) requires a book's atlas_candidate_feed rows to be exactly its
low/medium_low chunks, each mirroring the chunk's span, confidence, review status and hold state. The close tool
appended either option unchecked. Also, an owner question about the choice was framed from the docstring and not from
measurement, and it misdescribed the shared feed's existing shapes (near-miss, disclosed). So the dry report now carries
both options' measured coverage and the shared feed's shapes by book, and any --acf (dry or close) is gated on the rule.

Pins the tool BEFORE, runs the pin guard, applies exact-once edits, compiles, keeps .pre_<sha12>, rolls back on failure.
usage: patch_close_book_v9b.py
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SP = EZ.parent
T = EZ / "_close_book.py"
BEFORE = "b18ab1934447b4cabe458dec9a87fca6e5b33f459873f0113f2cfd964c80b507"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731

EDITS = [
    ("  Choosing is the owner's act (OW-11), and appending both is refused.\n",
     "  Choosing is the owner's act (OW-11), and appending both is refused.\n"
     "  AMENDED 2026-09-23 (v9b): any --acf, dry or close, must meet checks/validate_book_review_coverage.py's per-book\n"
     "  feed rule, measured here (one row per low/medium_low chunk and no other, each mirroring the chunk's span,\n"
     "  confidence, review status and hold state). The dry report gives both options' coverage and the shared feed's\n"
     "  existing shapes by book, so a question about the choice is sourced from the report.\n"),
    ('    acf = {"lam_pattern": acf_lam, "item22": acf_item22}.get(a.acf)\n',
     '    acf = {"lam_pattern": acf_lam, "item22": acf_item22}.get(a.acf)\n'
     '    by_id = {r["decision_id"]: r for r in final}\n'
     '    low_ids = {k for k, r in by_id.items() if r["confidence"] in ("low", "medium_low")}\n'
     '\n'
     '    def coverage(opt):\n'
     '        """The coverage validator\'s per-book feed rule (its lines 177-194), measured over an option\'s rows."""\n'
     '        ids = [x.get("chunk_decision_id") for x in opt]\n'
     '        stale = [x["chunk_decision_id"] for x in opt if x.get("chunk_decision_id") in low_ids and any(\n'
     '            x.get(f) != by_id[x["chunk_decision_id"]].get(g) for f, g in (\n'
     '                ("span", "span"), ("confidence", "confidence"), ("chunk_review_status", "review_status"),\n'
     '                ("candidate_hold_state", "candidate_hold_state")))]\n'
     '        return {"duplicates": len(ids) - len(set(ids)), "missing": sorted(low_ids - set(ids)),\n'
     '                "orphan": sorted(set(ids) - low_ids), "stale": sorted(stale)}\n'
     '    cov = {"lam_pattern": coverage(acf_lam), "item22": coverage(acf_item22)}\n'
     '    cov_ok = lambda c: not (c["duplicates"] or c["missing"] or c["orphan"] or c["stale"])      # noqa: E731\n'
     '    if a.acf:\n'
     '        gate("atlas feed option %s meets the coverage validator\'s per-book rule" % a.acf, cov_ok(cov[a.acf]),\n'
     '             {k: (v if isinstance(v, int) else v[:4]) for k, v in cov[a.acf].items()})\n'
     '    shapes = collections.defaultdict(set)\n'
     '    for x in jl(M8 / "atlas_candidate_feed.jsonl"):\n'
     '        shapes["%d_fields" % len(x)].add(x.get("book"))\n'),
    ('                              "item22_confidence": dict(collections.Counter(x.get("confidence") for x in acf_item22))},\n',
     '                              "item22_confidence": dict(collections.Counter(x.get("confidence") for x in acf_item22)),\n'
     '                              "fields": {"lam_pattern": len(acf_lam[0]) if acf_lam else 0,\n'
     '                                         "item22": len(acf_item22[0]) if acf_item22 else 0},\n'
     '                              "coverage": {k: {"meets_rule": cov_ok(v), **{f: (x if isinstance(x, int) else len(x))\n'
     '                                                                         for f, x in v.items()}} for k, v in cov.items()},\n'
     '                              "coverage_detail": {k: {f: x for f, x in v.items() if not isinstance(x, int)}\n'
     '                                                  for k, v in cov.items()},\n'
     '                              "shared_feed_shapes_by_book": {k: sorted(v) for k, v in sorted(shapes.items())}},\n'),
]

g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target",
                    "Ezek/_close_book.py"], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                   env=dict(os.environ, PYTHONUTF8="1"))
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: " + g.stdout[-300:])
before = T.read_bytes()
if sha(before) != BEFORE:
    raise SystemExit("REFUSED: _close_book.py is at %s, not the expected-before digest" % sha(before)[:12])
src = before.decode("utf-8")
for old, new in EDITS:
    if src.count(old) != 1:
        raise SystemExit("REFUSED: an anchor occurs %d times: %r" % (src.count(old), old[:70]))
    src = src.replace(old, new)
keep = T.with_name(T.name + ".pre_" + BEFORE[:12])
if keep.exists() and keep.read_bytes() != before:
    raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
keep.write_bytes(before)
try:
    compile(src, str(T), "exec")
except SyntaxError as e:
    raise SystemExit("REFUSED: the amended tool does not compile: %s" % e)
tmp = T.with_suffix(".py.tmp")
tmp.write_bytes(src.encode("utf-8"))
os.replace(tmp, T)
after = T.read_bytes()
if after != src.encode("utf-8"):
    T.write_bytes(before)
    raise SystemExit("ROLLED BACK: post-write check failed")
print(json.dumps({"tool": [BEFORE, sha(after)], "kept": keep.name, "edits": len(EDITS)}))
