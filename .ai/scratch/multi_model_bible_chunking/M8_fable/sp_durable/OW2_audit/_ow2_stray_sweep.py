#!/usr/bin/env python3
"""Deterministic stray sweep of the shared SP/OW2_audit tree (E-21 detector):
every file must match the expected-artifact allowlist. Run at every batch close."""
import fnmatch
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

ALLOW = [
    "_build_lf_frame.py", "frame_isa_lf.v1.json",
    "AUDIT_BRIEF_LF.md", "_ow2lf_verify.py", "_ow2_stray_sweep.py",
    "slices/slice_b[0-9][0-9].json",
    "reviews/ow2lf_b[0-9][0-9].json",
    "ow2lf_attempt_receipts.jsonl",
    # fable adjudication lane (staged 2026-09-01 at wave A2 close)
    "ADJUDICATION_BRIEF_FABLE.md", "_build_adj_slices.py", "_ow2adj_verify.py",
    "slices/slice_adj[0-9][0-9].json", "reviews/ow2adj_[0-9][0-9].json",
    "ow2adj_attempt_receipts.jsonl",
    # item-2 + prov38 lanes (staged when those launch)
    "AUDIT_BRIEF_ITEM2.md", "_build_item2_slices.py",
    "slices/slice_i2_*.json", "reviews/ow2i2_*.json",
    "AUDIT_BRIEF_PROV38.md", "_build_prov38_frame.py", "frame_prov38.v1.json",
    "slices/slice_p38_*.json", "reviews/ow2p38_*.json",
    # item-2 lane staged 2026-09-03 (orchestrator-owned edit): frame, verifier,
    # toolkit-manifest guard, receipts carrier, and the item-2 Fable adjudication
    # + prov38 verifier/receipt names reserved ahead of their launch
    "frame_item2.v1.json", "_ow2i2_verify.py", "_ow2i2_toolkit_manifest.py",
    "_ow2i2_toolkit_manifest.json", "ow2i2_attempt_receipts.jsonl",
    "ADJUDICATION_BRIEF_ITEM2.md", "_build_i2adj_slices.py", "_ow2i2adj_verify.py",
    "slices/slice_i2adj_*.json", "reviews/ow2i2adj_*.json", "ow2i2adj_attempt_receipts.jsonl",
    "_ow2p38_verify.py", "ow2p38_attempt_receipts.jsonl",
    # OW-3 (owner directive 2026-09-04) lane: bounded Isaiah re-adjudication + placeholder gate
    "READJUDICATION_BRIEF_OW3.md", "_build_ow3_readj_slices.py", "_ow2_placeholder_check.py",
    "slices/slice_ow3re_*.json", "reviews/ow2adj_re_*.json", "ow2adj_re_attempt_receipts.jsonl",
]

strays = []
for p in sorted(HERE.rglob("*")):
    if p.is_dir():
        continue
    rel = p.relative_to(HERE).as_posix()
    if not any(fnmatch.fnmatch(rel, pat) for pat in ALLOW):
        strays.append({"path": rel, "bytes": p.stat().st_size})
print(json.dumps({"sweep": "CLEAN" if not strays else "STRAYS_FOUND",
                  "files_checked": sum(1 for p in HERE.rglob("*") if p.is_file()),
                  "strays": strays}, indent=1))
sys.exit(1 if strays else 0)
