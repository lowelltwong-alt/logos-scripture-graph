#!/usr/bin/env python3
"""Dependency-pin reconciliation check (E-25 control, 2026-09-06 s3). For every
receipts/tool_dependency_applicability.*.json, take the LATEST record's new_sha256 per tool
(a later record supersedes an earlier one for the same tool) and verify the DURABLE copy under
M8_fable hashes to it; with --live <scratchpad root> also verify the live SP copy. Prints the tool's
COUNT of mismatches (read the count, never the status line alone); exit 1 on any mismatch or
absent pinned file. Never writes. Usage: _dep_pin_check.py [--live <scratchpad root>]"""
import glob
import hashlib
import json
import os
import re
import sys

M8 = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable"
LIVE_MAP = {"sp_durable/Jer/": "SP/Jer/", "sp_durable/Lam/": "SP/Lam/", "sp_durable/OW2_audit/": "SP/OW2_audit/", "sp_durable/REPAIR/": "SP/REPAIR/"}   # 2026-09-07 s3: Lam lane live-checked from v7 on


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def version_key(path):
    m = re.search(r"\.v(\d+)\.json$", path)
    return (int(m.group(1)) if m else 0, path)


def expand(tool, new):
    """A brace-set tool entry with a dict of per-file hashes expands to one pin per file."""
    if isinstance(new, str):
        return [(tool, new)]
    if isinstance(new, dict):
        base = tool.split("{")[0]
        return [(base + fn, h) for fn, h in new.items()]
    return []


def main():
    live_root = None
    if "--live" in sys.argv:
        live_root = sys.argv[sys.argv.index("--live") + 1]
    recs = sorted(glob.glob(os.path.join(M8, "receipts", "tool_dependency_applicability.*.json")), key=version_key)
    latest = {}
    for rec in recs:
        d = json.load(open(rec, encoding="utf-8"))
        for c in d.get("changes", []):
            for tool, h in expand(c["tool"], c.get("new_sha256")):
                latest[tool] = {"pinned": h, "record": os.path.relpath(rec, M8).replace(os.sep, "/")}
    mism, checked = [], 0
    for tool, info in sorted(latest.items()):
        checked += 1
        dur = os.path.join(M8, tool.replace("/", os.sep))
        got = sha(dur) if os.path.isfile(dur) else "ABSENT"
        if got != info["pinned"]:
            mism.append({"tool": tool, "copy": "durable", "pinned": info["pinned"][:16], "got": got[:16], "record": info["record"]})
        if live_root:
            for pre, lp in LIVE_MAP.items():
                if tool.startswith(pre):
                    lv = os.path.join(live_root, (lp + tool[len(pre):]).replace("/", os.sep))
                    if os.path.isfile(lv):
                        lg = sha(lv)
                        if lg != info["pinned"]:
                            mism.append({"tool": tool, "copy": "live", "pinned": info["pinned"][:16], "got": lg[:16], "record": info["record"]})
    out = {"check": "dependency_pin_reconciliation", "records": [os.path.basename(r) for r in recs], "tools_checked": checked,
           "mismatch_count": len(mism), "mismatches": mism, "status": "CLEAN" if not mism else "MISMATCH"}
    print(json.dumps(out, indent=1))
    return 0 if not mism else 1


if __name__ == "__main__":
    sys.exit(main())
