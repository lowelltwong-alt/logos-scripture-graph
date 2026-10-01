#!/usr/bin/env python3
"""PRE-SEND LINT for text bound for the DAD lesson tree (ledger E-52's cure): refuse a FORWARD marker mention.

WHY THIS TOOL. `dad_lessons_scan.py` allocates the next control marker from EVERY bare `<PREFIX>-NN` mention in any
non-index record, because a phrasing-based allocator once under-reported and caused a collision (2026-09-15). That
failure direction is right, but it means ANY text that names a marker number beyond those allocated - "next free
marker C-28" in a postflight next-action - takes that number the moment it is written. On 2026-09-22 exactly that
burned C-28. This lint runs on the outgoing text BEFORE `lesson add` / `agent postflight` and refuses it.

RULE. Using the scanner's own bare-mention pattern, every `<PREFIX>-NN` in the outgoing text must be EITHER below the
scanner's next-free marker (a reference to a marker that already exists) OR in the `--allocating` set, which must be
the consecutive run starting at next-free (the markers this very write legitimately takes). Anything else is a forward
mention and is refused. To refer to a future marker, write "the next free marker per the scanner" - never a number.

usage: python _dad_forward_marker_lint.py (--scan-json <scan.json> | --next-free C-NN) [--allocating C-NN ...]
                                          (--text <s> ... | --file <path> ...) [--prefix C]
       python _dad_forward_marker_lint.py --selftest
Exit 0 CLEAR, 1 REFUSED, 2 usage or input error. Read-only.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def parse_marker(s, prefix):
    m = re.fullmatch(re.escape(prefix) + r"-(\d+)", str(s).strip())
    if not m:
        raise ValueError(f"not a {prefix}-NN marker: {s!r}")
    return int(m.group(1))


def lint(texts, next_free, allocating, prefix="C"):
    """Return a list of violation strings; empty means CLEAR."""
    problems = []
    alloc = sorted(set(allocating))
    if alloc and alloc != list(range(next_free, next_free + len(alloc))):
        problems.append(f"--allocating {alloc} is not the consecutive run starting at next free {next_free}")
    pat = re.compile(r"\b" + re.escape(prefix) + r"-(\d+)\b")  # the scanner's own bare-mention pattern
    for i, t in enumerate(texts):
        for m in pat.finditer(t):
            n = int(m.group(1))
            if n >= next_free and n not in alloc:
                ctx = t[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")
                problems.append(f"text #{i}: forward mention {prefix}-{n:02d} would burn it -> ...{ctx}...")
    return problems


def selftest():
    cases = [
        # (texts, next_free, allocating, expect_clear, label)
        (["next delta after E-51 - next free marker C-28"], 28, [], False, "the 2026-09-22 slip itself"),
        (["next free marker per the scanner"], 28, [], True, "the cure wording"),
        (["M8_fable campaign control C-28 slug [OW-25]: tail"], 28, [28], True, "a record allocating its marker"),
        (["extends C-25 and C-27"], 28, [], True, "references to existing markers"),
        (["campaign control C-29"], 28, [29], False, "allocating set skips next free"),
        (["C-28 and C-29 in one batch"], 28, [28, 29], True, "consecutive batch allocation"),
        (["see C-30 later"], 28, [28, 29], False, "forward mention beyond the batch"),
        (["C-280 is not C-28"], 28, [], False, "multi-digit forward mention"),
        (["ABC-99 and XC-40"], 28, [], True, "word boundary - not a bare C- mention"),
    ]
    bad = 0
    for texts, nf, al, want, label in cases:
        got = not lint(texts, nf, al)
        ok = got == want
        bad += not ok
        print(("ok   " if ok else "FAIL ") + label)
    print("SELFTEST: " + ("PASS (%d/%d)" % (len(cases), len(cases)) if not bad else "FAIL (%d bad)" % bad))
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan-json")
    ap.add_argument("--next-free")
    ap.add_argument("--allocating", action="append", default=[])
    ap.add_argument("--text", action="append", default=[])
    ap.add_argument("--file", action="append", default=[])
    ap.add_argument("--prefix", default="C")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if bool(a.scan_json) == bool(a.next_free):
            raise ValueError("give exactly one of --scan-json or --next-free")
        nf_raw = json.loads(Path(a.scan_json).read_text(encoding="utf-8"))["next_marker"] if a.scan_json else a.next_free
        next_free = parse_marker(nf_raw, a.prefix)
        allocating = [parse_marker(x, a.prefix) for x in a.allocating]
        texts = list(a.text) + [Path(f).read_text(encoding="utf-8") for f in a.file]
        if not texts:
            raise ValueError("no --text or --file given")
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print(f"usage or input error: {e}", file=sys.stderr)
        return 2
    problems = lint(texts, next_free, allocating, a.prefix)
    for p in problems:
        print("REFUSED: " + p)
    print("VERDICT: " + ("CLEAR" if not problems else "REFUSED (%d)" % len(problems)))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
