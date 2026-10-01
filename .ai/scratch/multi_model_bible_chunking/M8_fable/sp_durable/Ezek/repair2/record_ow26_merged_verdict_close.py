#!/usr/bin/env python3
"""Record owner directive OW-26 (Ezekiel's OW-22 scope cut: the merged-verdict close).

Appends to two surfaces, each pinned and append-verified: the error-pattern ledger (OW-26) and the Ezekiel close-gate
ruling file (section 4c). Append only - E-44: amend, never edit.
"""
import hashlib
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
LEDGER = M8 / "ERROR_PATTERN_LEDGER.v1.md"
LEDGER_PIN = "4bdeb19cb33a782f1b9d32d9f7afde1d6375794c1b3386f8a352ef2e8a80d960"
RULING = M8 / "sp_durable" / "Ezek" / "EZEK_CLOSE_GATE_OWNER_RULING.v1.md"
RULING_PIN = "4373126f7664d3a867553b745abe742e6128c86382a80b70dac673a589d35598"

OW26 = """
## OWNER DIRECTIVE OW-26 (2026-09-22) - EZEKIEL'S OW-22 SCOPE CUT: THE MERGED-VERDICT CLOSE

**The choice (TRANSCRIBED, owner's answer to a structured question in chat, 2026-09-22):** "Merged-verdict close
(Recommended)". It is the named scope cut OW-22 requires in place of a further raise, brought after OW-25 made every
remaining pass Opus 5.5 work and the v2 section 4 forecast showed the four passes as separately scoped would cross the
72,000,000 hard line. **Scope: Ezekiel only.** Whether later books use the same shape is a per-book decision.

**What was chosen, as offered.** (1) Apply the `#e16` ruling (v2 section 2 pass 1). (2) Run ONE pair of blind
`claude-opus-5-5` checker lanes; each lane returns all three verdicts in one pass: the postcheck `fit_to_assemble`, the
OW-6 final check `fit_to_close` bound to the corpus sha256, and the grades for close-gate items 20-23. (3) The
transcript audit (v2 pass 3) is recorded as OWED, NOT MET - it is not run and not claimed. Forecast offered with the
choice: +1.9M to +2.5M, putting the measured lower bound at roughly 71.4M-72.0M against the hard line (an ESTIMATE from
Ezekiel's own measured whole-book lane costs, 550,726-817,960 per lane).

**The weakness, stated with the choice and recorded so no reader mistakes it for three independent passes.** The three
verdicts share one reader per lane: a checker that misses something misses it in all three. The two-lane floor (OW-19)
is still met - two blind non-author lanes - but the passes are no longer separate lenses, and the completion receipt
must say so beside the OW-25 `grader_fallback` statement.

**What it does NOT change.** OW-22 stays a hard line: if the measured bound after the checker pair leaves no room for a
remediation round, the book is brought to the owner at the line, not over it. OW-11 stays: assembly, completion
receipt, campaign-log and progress appends are performed only as far as the Lamentations precedent shows they were the
orchestrator's to perform, and publication is the owner's act.
"""

SEC4C = """
## 4c. The scope cut — chosen 2026-09-22 (OW-26)

The owner chose (TRANSCRIBED) "Merged-verdict close (Recommended)": apply `#e16`, then ONE pair of blind Opus 5.5
checker lanes, each returning the postcheck `fit_to_assemble`, the OW-6 final check `fit_to_close` and the item 20-23
grades in one pass; the transcript audit is recorded as owed, not met. Forecast +1.9M to +2.5M (ESTIMATE). Recorded in
the ledger as OW-26 with its stated weakness: one reader per lane carries all three verdicts. The hard line and OW-11 are
unchanged.
"""


def append(path, text, marker, pin=None):
    pre = path.read_bytes()
    if marker.encode("utf-8") in pre:
        return f"{path.name}: already present - not appended again"
    got = hashlib.sha256(pre).hexdigest()
    if pin and got != pin:
        raise SystemExit(f"{path.name} MOVED since it was pinned: {got}")
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    post = path.read_bytes()
    if not post.startswith(pre):
        raise SystemExit(f"INTEGRITY FAILURE: {path.name} was not appended to")
    return f"{path.name}: {len(pre)} -> {len(post)} bytes  sha256 {hashlib.sha256(post).hexdigest()}"


print(append(LEDGER, OW26, "## OWNER DIRECTIVE OW-26 ", LEDGER_PIN))
print(append(RULING, SEC4C, "## 4c. ", RULING_PIN))
