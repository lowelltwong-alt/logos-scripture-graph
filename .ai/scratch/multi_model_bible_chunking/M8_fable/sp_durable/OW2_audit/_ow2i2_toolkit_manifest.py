#!/usr/bin/env python3
r"""E-21 stray/mutation guard for the five per-book audit trees (SP\Ps, SP\Job,
SP\Prov, SP\Eccl, SP\Song): --pin records every file's sha256 at staging into
_ow2i2_toolkit_manifest.json; --check reports any added, removed, or changed
file (interpreter __pycache__ excluded by design — regenerable). Auditors are
forbidden to write anywhere under SP; a non-CLEAN check is a wave-close stop.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
BOOKS = ["Ps", "Job", "Prov", "Eccl", "Song"]
MANIFEST = HERE / "_ow2i2_toolkit_manifest.json"


def snapshot() -> dict:
    out = {}
    for b in BOOKS:
        root = SP / b
        for p in sorted(root.rglob("*")):
            if p.is_dir() or "__pycache__" in p.parts:
                continue
            rel = f"{b}/{p.relative_to(root).as_posix()}"
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode == "--pin":
        snap = snapshot()
        MANIFEST.write_text(json.dumps({"schema": "m8_ow2_i2_toolkit_manifest.v1", "pinned": "2026-09-03",
                                        "files": snap}, ensure_ascii=False, indent=1),
                            encoding="utf-8", newline="\n")
        print(json.dumps({"status": "PINNED", "files": len(snap),
                          "per_book": {b: sum(1 for k in snap if k.startswith(b + "/")) for b in BOOKS}}))
        return 0
    pinned = json.load(open(MANIFEST, encoding="utf-8"))["files"]
    now = snapshot()
    added = sorted(k for k in now if k not in pinned)
    removed = sorted(k for k in pinned if k not in now)
    changed = sorted(k for k in now if k in pinned and now[k] != pinned[k])
    status = "CLEAN" if not (added or removed or changed) else "STRAYS_OR_MUTATIONS"
    print(json.dumps({"status": status, "files_checked": len(now), "added": added,
                      "removed": removed, "changed": changed}, ensure_ascii=False, indent=1))
    return 0 if status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
