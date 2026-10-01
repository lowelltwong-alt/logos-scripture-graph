#!/usr/bin/env python3
"""Append E-59 to ERROR_PATTERN_LEDGER.v1.md (append-only). Refuses unless the ledger's sha256 is the one the
E-52..E-58 DAD ingest pinned and E-59 is absent; the append is idempotent-safe by that check."""
import hashlib
import sys
from pathlib import Path

MD = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md")
PIN16 = "7d5dc23015456815"
ENTRY = """
## E-59 (2026-09-23) - DAD RECORDS DRAFTED AFTER A COMPACTION CARRIED THREE CLAUSES THE LEDGER DOES NOT SAY

**What happened.** The DAD records for E-52..E-58 and OW-25..OW-30 were drafted just after a context compaction, from
the compaction summary and not from a fresh read of the ledger. Before the write, every record was checked against the
ledger text (lines 2133-2378). Three clauses were not supported: (1) OW-27's record said scripts read the ceiling carrier
and never hardcode the value, which the ledger does not say; (2) OW-29's record said a scarce-model brief runs with no
tools and asks for a JSON-only reply, when the owner asked only that its input and output be kept token-efficient; (3)
E-53's record left out that the in-place briefs were never dispatched, and it said nothing was regenerated where the
ledger says no write made while the guard was blind touched a pinned path. All three were cut or corrected before the
write. Every figure in the records (100 pins, 22 vectors and 3 red, 82 files, 226 attempts, 152 of 185 groups, about
1.66x, about 2.6x, about 90 percent) was MEASURED against the ledger text and holds.

**Severity, scored on counterfactual blast radius.** Observed impact: nil. Nothing unsupported reached DAD. Counterfactual:
medium. Three candidate records would have presented the orchestrator's paraphrase as TRANSCRIBED or MEASURED content,
and that is the half-truth OW-18 forbids, in a shared store later sessions read as evidence. The control that caught it
was a deliberate re-read and not a gate.

**Root cause.** A compaction summary is a lossy carrier. Drafting durable records from it lets plausible generalisations
that sound like the source stand in for the source.

**Cure.** Records bound for any durable store are drafted from, or checked clause by clause against, a fresh read of
their source range, never from a compaction summary. Figures are checked by extraction. No tool can check that a
paraphrase is supported, so this control is procedural, and it is recorded here so the next delta harness brief carries
it. The E-52..E-58 ingest ran only after the check (13 records, problems none).
"""


def main():
    b = MD.read_bytes()
    if hashlib.sha256(b).hexdigest()[:16] != PIN16:
        raise SystemExit("REFUSED: the ledger moved since the ingest pinned it")
    t = b.decode("utf-8")
    if "\n## E-59 (" in t:
        raise SystemExit("REFUSED: E-59 already present")
    with MD.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(("" if t.endswith("\n") else "\n") + ENTRY)
    print("appended E-59; ledger sha256", hashlib.sha256(MD.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
