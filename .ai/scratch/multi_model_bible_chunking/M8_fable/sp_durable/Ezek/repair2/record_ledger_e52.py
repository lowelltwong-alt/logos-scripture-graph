#!/usr/bin/env python3
"""Append ledger entry E-52 (a forward marker mention in DAD postflight text burned control marker C-28)."""
import hashlib
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
MD = M8 / "ERROR_PATTERN_LEDGER.v1.md"
PIN = "1fc8abb2177ac68fb211cb0801d88b39a7d11aa73b24f25059943712aa6cb61a"

ENTRY = """
## E-52 (2026-09-22) - A FORWARD MARKER NUMBER WRITTEN INTO A DAD RECORD BURNED THAT MARKER

**What happened.** The DAD intake for E-38..E-51 allocated controls C-25, C-26 and C-27 correctly. The postflight that
closed the session then carried the text "next free C-28" twice - once in a `--test` line and once in a `--next-action`
line - as a helpful pointer for the next intake. `dad_lessons_scan.py` allocates the next free marker from EVERY bare
`C-NN` mention in any non-index record (the 2026-09-15 fix, chosen so the allocator fails toward skipping). So the
postflight record itself took C-28: MEASURED on re-scan, C-28 has 1 hit (the postflight record `68720519...`), the
phrasing WARNING lists it beside C-14..C-16, and the scanner now reports NEXT FREE MARKER C-29. Found by the orchestrator
on its own re-scan, same session.

**Severity, scored on counterfactual blast radius, not luck.** Observed impact: one skipped number in an append-only
series - nothing collided, nothing was double-ingested, no record was edited. That is small only BECAUSE the 09-15 fix
chose the safe failure direction; under the earlier phrasing-based allocator the same sentence would have been ignored
and harmless, and under any allocator that trusted memory instead of the scan it would have been the number handed out.
The class is the dangerous part: a record written to help the NEXT writer silently changed the state the next writer
reads. **A pointer to future state, written into the store that defines that state, is a write to it.**

**Cure.** (1) Never write a forward marker number into any record; say "the next free marker per the scanner" and let
the next writer read it in the same scan that clears its dedupe. (2) Preventive control, enforced in a tool rather than
in memory (OW-18): `sp_durable/campaign/_dad_forward_marker_lint.py` runs on outgoing DAD text before `lesson add` or
`agent postflight` and REFUSES any `C-NN` at or beyond the scanner's next free marker unless it is in the consecutive
`--allocating` run this write legitimately takes; it uses the scanner's own bare-mention pattern so it is exactly as
broad as the allocator. Selftest 9/9; adversarial replay against the real 09-22 postflight source with next free C-28
REFUSES both mentions, and the E-38..E-51 ingest harness replays CLEAR with next free C-25 allocating C-25..C-27. (3)
C-28 stays burned: the series is append-only (E-44 amend, never edit), and a skipped number costs nothing. Routing
memory now says next free C-29. **Related:** E-51 (a cursor that advanced correctly over the wrong surface) is the
mirror image - there the position was read from a dead surface; here it was written into the live one.
"""

pre = MD.read_bytes()
if b"## E-52 " in pre:
    print("E-52 already present - not appended again")
else:
    if hashlib.sha256(pre).hexdigest() != PIN:
        raise SystemExit("LEDGER MOVED since it was pinned - re-read before appending: " + hashlib.sha256(pre).hexdigest())
    with MD.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)
    if not MD.read_bytes().startswith(pre):
        raise SystemExit("INTEGRITY FAILURE: the ledger was not appended to")
b = MD.read_bytes()
print("bytes %d  entries %d  sha256 %s" % (len(b), b.count(b"\n## "), hashlib.sha256(b).hexdigest()))
