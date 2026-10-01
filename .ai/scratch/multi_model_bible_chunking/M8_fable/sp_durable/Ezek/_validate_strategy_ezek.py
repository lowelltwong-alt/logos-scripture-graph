#!/usr/bin/env python3
"""Validate book_strategy/Ezek.md against the staged inventories.

The tiling law is the one thing a strategy cannot be wrong about: every writer part inherits it, and a gap or an
overlap propagates silently into the corpus. The author asserted its own arithmetic; an assertion is a candidate
finding, so parents and parts are re-summed here from verse_inventory.json.

PARENT-SEAM STRADDLE — the ruled invariant, not the original instruction. The launch brief told the author that
parts must never span a parent seam. Two do. That deviation was RULED ACCEPTABLE on 2026-09-08
(ezek_p0_repair_a1#e1) because:
  - the binding law is that ROWS never straddle a parent seam; a part is a work assignment, a row is a claim
    about the text, and only the second is a correctness boundary;
  - parent-aligned parts would run 65 verses against 260, a four-fold review-depth imbalance on a hard book;
  - a part containing a parent seam puts BOTH SIDES of it in one reviewer's hands, which is exactly what the
    standing "assess a seam from both sides" rule wants.
So this file does NOT check "no straddle". It checks the invariant that actually protects the corpus: **every
straddle is DISCLOSED in the part table**. An undisclosed straddle is still a hard failure, because it is a seam
nobody was told about. The check was tightened, not deleted.

Usage: _validate_strategy_ezek.py <path to book_strategy_Ezek.md>
"""
import json
import re
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent

PARENTS = [(1, 1, 3, 27), (4, 1, 7, 27), (8, 1, 11, 25), (12, 1, 19, 14),
           (20, 1, 24, 27), (25, 1, 32, 32), (33, 1, 39, 29), (40, 1, 48, 35)]
PARTS = [(1, 1, 7, 27), (8, 1, 14, 23), (15, 1, 19, 14), (20, 1, 21, 32), (22, 1, 24, 27),
         (25, 1, 28, 26), (29, 1, 32, 32), (33, 1, 36, 38), (37, 1, 39, 29), (40, 1, 43, 27),
         (44, 1, 48, 35)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    md = Path(sys.argv[1]) if len(sys.argv) > 1 else SP / "book_strategy_Ezek.md"
    text = md.read_text(encoding="utf-8")
    inv = {int(k): v for k, v in
           json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))["chapters"].items()}
    total = sum(inv.values())

    def span(c1, v1, c2, v2):
        n = 0
        for c in range(c1, c2 + 1):
            hi = v2 if c == c2 else inv.get(c, 0)
            lo = v1 if c == c1 else 1
            if c not in inv or hi > inv[c]:
                return None
            n += hi - lo + 1
        return n

    def contiguity(spans):
        bad = []
        for i in range(len(spans) - 1):
            _, _, c2, v2 = spans[i]
            c1n, v1n, _, _ = spans[i + 1]
            nxt = (c2, v2 + 1) if v2 < inv[c2] else (c2 + 1, 1)
            if (c1n, v1n) != nxt:
                bad.append("after %d:%d expected %s got %d:%d" % (c2, v2, nxt, c1n, v1n))
        return bad

    problems = []
    psum = sum(span(*s) or 0 for s in PARENTS)
    tsum = sum(span(*s) or 0 for s in PARTS)
    if psum != total:
        problems.append("parents sum to %d, inventory has %d" % (psum, total))
    if tsum != total:
        problems.append("parts sum to %d, inventory has %d" % (tsum, total))
    problems += ["parents: " + g for g in contiguity(PARENTS)]
    problems += ["parts: " + g for g in contiguity(PARTS)]

    for n in range(1, 11):
        if not re.search(r"^##+\s*§%d\b" % n, text, re.M):
            problems.append("section §%d missing" % n)

    # straddles: found, then required to be disclosed
    starts = {(c1, v1) for c1, v1, _, _ in PARENTS}
    straddles, undisclosed = [], []
    for c1, v1, c2, v2 in PARTS:
        for (pc, pv) in sorted(starts):
            inside = ((pc > c1) or (pc == c1 and pv > v1)) and ((pc < c2) or (pc == c2 and pv <= v2))
            if inside:
                straddles.append((c1, v1, c2, v2, pc, pv))
                if not re.search(r"internal parent seam \d+:\d+/%d:%d" % (pc, pv), text):
                    undisclosed.append("part %d:%d-%d:%d spans parent start %d:%d and does NOT disclose it"
                                       % (c1, v1, c2, v2, pc, pv))
    problems += undisclosed

    # every zone ref carries its dual
    zone_bad = [i for i, l in enumerate(text.splitlines(), 1)
                if re.search(r"web:Ezek\.(?:21\.\d+|20\.4[5-9])", l) and "oshb:Ezek.21." not in l]
    if zone_bad:
        problems.append("zone refs without an oshb dual on lines %s" % zone_bad[:10])

    print(json.dumps({
        "file": str(md), "bytes": len(text.encode("utf-8")),
        "parents": {"count": len(PARENTS), "sum": psum, "contiguous": not contiguity(PARENTS)},
        "parts": {"count": len(PARTS), "sum": tsum, "contiguous": not contiguity(PARTS)},
        "inventory_total": total,
        "parent_seam_straddles": [
            {"part": "%d:%d-%d:%d" % s[:4], "parent_start": "%d:%d" % s[4:],
             "disclosed": not any("%d:%d" % s[4:] in u for u in undisclosed)} for s in straddles],
        "straddle_rule": "RULED ACCEPTABLE when disclosed; an undisclosed straddle is a hard failure",
        "zone_refs_missing_dual": len(zone_bad),
        "problems": problems,
        "verdict": "GREEN" if not problems else "RED"}, ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
