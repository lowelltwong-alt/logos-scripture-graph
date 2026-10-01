#!/usr/bin/env python3
"""Ledger E-50: the scope of "done" was inferred from the task list instead of from the gate that defines done."""
import hashlib
import json
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")

delta = """
## E-50 (2026-09-21) - "EVERY REMAINING ITEM IS FINISHED" WAS MEASURED OVER THE TASK LIST, NOT OVER THE GATE

Within one hour of writing E-49 - whose whole lesson is that the first true, measurable thing found is not the answer
\u2014 the same error was made again at a larger scale, and this time it reached an owner-facing document. An owner
decision packet (`EZEK_CLOSE_GATE_OWNER_DECISION.v1.md`) stated that the Fable-gated grade of close-gate items 20-23
was the only thing standing between Ezekiel and closure, and that "every close item that does not need Fable is
finished". Each item in that claim was individually true and individually verified. **The set was invented.** The
items checked were the items in hand from the current phase; nothing was read that defines what closing a book
actually requires.

What reading the gate produced, minutes later: Ezekiel has **no postcheck packet** (`fit_to_assemble`, authored by
Opus and therefore never blocked at all), **no stage-1 transcript-audit packets**, **no OW-6 final-check packet**
(`fit_to_close`), and **no assembled corpus** - four outstanding passes, plus no `_close_book.py` for the book. The
tool that closed Lamentations refuses at explicit assertions naming `claude-fable-5-1` and the verdict `fit_to_close`
(lines 58, 60, 61, 88), so the dependency is compiled into the pipeline and not merely written in policy.

**The distinct mechanism, worth separating from E-49.** E-49 is about adopting the first plausible CAUSE. This is
about inferring the SCOPE of completion from the artifacts one happens to be holding. A phase hands the agent a set
of items; finishing them produces a true and verifiable statement about those items; and the leap is from "these are
done" to "what remains is done", which no measurement supports. It is especially dangerous when the surviving blocker
is genuine and well-evidenced, because the evidence for the blocker lends unearned credibility to the claim about
everything else - the packet was careful and rigorous about the one thing it had actually checked.

**Cure: completeness is measured against the mechanism that enforces it, never against the task list.** Before any
claim that a unit is finished or near-finished, read the gate, tool or checklist that decides the unit is finished and
enumerate its requirements from ITS bytes; for this campaign that means the close tool's own assertions and the
directory each one requires. A statement of the form "everything else is done" is a claim about a set, and a claim
about a set needs the set's definition read from disk, not recalled. Corollary, learned the same hour: **an
owner-facing document stating a near-completion must cite where its definition of "complete" came from**, so a false
premise cannot be smuggled into a decision the owner then makes on it. v1 was retained rather than edited and v2
opens by stating what it supersedes and why - the correction is part of the record, not a replacement of it.
"""

d = M8 / "sp_durable" / "Ezek" / "repair2" / "ledger_delta_E50.md"
d.write_text(delta, encoding="utf-8", newline="\n")
led = M8 / "ERROR_PATTERN_LEDGER.v1.md"
pre = led.read_bytes()
if "## E-50 " not in pre.decode("utf-8"):
    with led.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(delta)
if not led.read_bytes().startswith(pre):
    raise SystemExit("INTEGRITY FAILURE: the ledger was not appended to")
txt = led.read_text(encoding="utf-8")
print(json.dumps({"ledger_bytes": led.stat().st_size, "grew_by": led.stat().st_size - len(pre),
                  "entries": txt.count("\n## E-"), "E50_present": "## E-50 " in txt,
                  "sha256": hashlib.sha256(led.read_bytes()).hexdigest()}, ensure_ascii=False, indent=1))
