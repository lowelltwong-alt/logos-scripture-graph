#!/usr/bin/env python3
"""E-51: the lesson-routing convention was keyed by row number to a ledger surface that stopped being written."""
import hashlib
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
MD = M8 / "ERROR_PATTERN_LEDGER.v1.md"

ENTRY = """
## E-51 (2026-09-22) - THE ROUTING CONVENTION WAS KEYED TO A LEDGER SURFACE THAT HAD STOPPED BEING WRITTEN

**What happened.** This campaign keeps the error ledger in TWO surfaces: `ERROR_PATTERN_LEDGER.v1.md` and
`error_pattern_ledger.v1.jsonl`. The DAD lesson-routing rule tracks its intake position as a ROW NUMBER - "next delta
starts at ledger row 86" - and that row number indexes the **JSONL**. MEASURED 2026-09-22: the JSONL holds 98 rows and
ends at E-43, last written 2026-09-21 12:29; the markdown holds 82 entries and ends at E-50, last written 2026-09-21
22:59. Row 85 of the JSONL is E-37, which is exactly where the 2026-09-16 ingest stopped, confirming the convention
indexes the JSONL and not the markdown.

**The divergence is one-way and silent.** A grep for writers shows more than twenty `record_*.py` scripts appending to
the markdown and **no Python that reads or writes the JSONL at all** - it survives only as a citation inside method
documents, playbooks and archived prompts. So the live ledger kept growing while the indexed one froze, and nothing
raised an error, because an append-only convention that never re-reads its target cannot notice the target is dead.

**What it would have cost.** E-44 through E-50 exist ONLY in the markdown. That set includes E-48/E-49 (a governance
floor that depends on one named model, and the wrong first diagnosis that had to be amended) and E-50 (completeness
measured over the task list instead of over the gate) - the three most transferable lessons of the session. Routing
"from row 86" would have ingested E-38..E-43 and OW-21..OW-24, reported success, and left the seven newest lessons
permanently unrouted. **A cursor that advances correctly over the wrong surface reports success while losing the
payload.**

**Cure.** (1) Key the intake to CONTENT - the entry id plus the source file's sha at write time - and treat the row
number as a convenience only, never as the identity. (2) Name ONE surface authoritative; a second surface that no tool
writes is not a backup, it is a decoy that outranks the real file in the routing rule. (3) Any convention that stores
a position into a file must, at read time, assert that the file is still the one being written - cheapest form: compare
its mtime and last id against the surface the writers actually target. **Related:** E-47 (a reader decided what a row
was by string-matching its schema name) is the same family - identity inferred from a proxy rather than read.
"""

pre = MD.read_bytes()
if b"## E-51 " in pre:
    print("E-51 already present - not appended again")
else:
    with MD.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)
    if not MD.read_bytes().startswith(pre):
        raise SystemExit("INTEGRITY FAILURE: the ledger was not appended to")
b = MD.read_bytes()
print("bytes %d  entries %d  sha256 %s" % (len(b), b.count(b"\n## "), hashlib.sha256(b).hexdigest()))
