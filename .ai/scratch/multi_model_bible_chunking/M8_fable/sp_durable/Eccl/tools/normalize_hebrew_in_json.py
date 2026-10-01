#!/usr/bin/env python3
"""Generalized Hebrew byte-normalization for any Eccl campaign JSON (Tier-0).

Walks every string field of the given JSON file(s). Each maximal Hebrew run
(letters/points + internal spaces/maqaf) must be a byte-identical substring of
Eccl_oshb.txt. Runs that are only Unicode-canonically equivalent (NFD-equal) to
a source window are REPLACED with the source's exact bytes (content-preserving).
Bare-consonant runs whose skeleton occurs in the source are accepted as form
mentions. Anything else is reported as a defect and left untouched.

NEVER hand-type Hebrew — slice from verse_map_oshb.json.
Usage: normalize_hebrew_in_json.py [--write] file1.json [file2.json ...]
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

FREEZE = Path(__file__).resolve().parent
SP = FREEZE.parent
RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")
MIN_LEN = 2   # lesson f (Ps close): the standard re-splice cure runs MIN_LEN=2


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def build_index():
    src = (SP / "Eccl_oshb.txt").read_text(encoding="utf-8")
    verses = [l.split("\t", 1)[1] for l in src.splitlines() if "\t" in l]
    skel_src = POINTS.sub("", src)
    return src, verses, skel_src


def find_source_bytes(run: str, src: str, verses: list[str]) -> str | None:
    if run in src:
        return run
    target = nfd(run)
    for text in verses:
        if target not in nfd(text):
            continue
        words = text.split(" ")
        for i in range(len(words)):
            for j in range(i, len(words)):
                window = " ".join(words[i : j + 1])
                if nfd(window) == target:
                    return window
                if j == i and "־" in window:
                    parts = window.split("־")
                    for a in range(len(parts)):
                        for b in range(a, len(parts)):
                            piece = "־".join(parts[a : b + 1])
                            if nfd(piece) == target:
                                return piece
                if len(nfd(window)) > len(target) + 40:
                    break
    return None


def fix_string(s: str, src, verses, skel_src, stats, defects):
    out, last = [], 0
    for m in RUN.finditer(s):
        run = m.group(0)
        if len(run.strip()) < MIN_LEN:
            continue
        if run in src:
            stats["ok"] += 1
            continue
        if not POINTS.search(run):
            if POINTS.sub("", run) in skel_src:
                stats["mention"] += 1
                continue
            defects.append(run[:50])
            continue
        hit = find_source_bytes(run, src, verses)
        if hit is not None:
            out.append(s[last : m.start()]); out.append(hit); last = m.end()
            stats["fixed"] += 1
        else:
            defects.append(run[:50])
    if out:
        out.append(s[last:])
        return "".join(out)
    return s


def walk(o, src, verses, skel_src, stats, defects):
    if isinstance(o, list):
        return [walk(x, src, verses, skel_src, stats, defects) for x in o]
    if isinstance(o, dict):
        return {k: walk(v, src, verses, skel_src, stats, defects) for k, v in o.items()}
    if isinstance(o, str):
        return fix_string(o, src, verses, skel_src, stats, defects)
    return o


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--write"]
    write = "--write" in sys.argv
    src, verses, skel_src = build_index()
    any_defects = False
    for f in args:
        p = Path(f)
        text = p.read_text(encoding="utf-8-sig")
        is_jsonl = p.suffix == ".jsonl"
        if is_jsonl:
            data = [json.loads(l) for l in text.splitlines() if l.strip()]
        else:
            data = json.loads(text)
        stats = {"ok": 0, "fixed": 0, "mention": 0}
        defects: list[str] = []
        new = walk(data, src, verses, skel_src, stats, defects)
        if write and stats["fixed"]:
            if is_jsonl:
                p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in new) + "\n",
                             encoding="utf-8")
            else:
                p.write_text(json.dumps(new, indent=1, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"file": p.name, "mode": "write" if write else "dry-run",
                          **stats, "defects": defects[:15], "defect_count": len(defects)},
                         ensure_ascii=False))
        any_defects = any_defects or bool(defects)
    return 1 if any_defects else 0


if __name__ == "__main__":
    sys.exit(main())
