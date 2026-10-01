#!/usr/bin/env python3
"""Record owner directive OW-25 (Fable unavailable; Opus 5.5 is the declared fallback for every Fable role).

Appends to two surfaces, each pinned and append-verified: the error-pattern ledger (OW-25) and the Ezekiel close-gate
ruling file (section 4b). Append only - E-44: amend, never edit.
"""
import hashlib
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
LEDGER = M8 / "ERROR_PATTERN_LEDGER.v1.md"
LEDGER_PIN = "8bf2075ac4b6a9f22b6129122811295079f3a05441a7884fe7af32623297f975"
RULING = M8 / "sp_durable" / "Ezek" / "EZEK_CLOSE_GATE_OWNER_RULING.v1.md"

OW25 = """
## OWNER DIRECTIVE OW-25 (2026-09-22) - FABLE UNAVAILABLE; OPUS 5.5 IS THE DECLARED FALLBACK FOR EVERY FABLE ROLE

**The directive (TRANSCRIBED, owner in chat, 2026-09-22):** "i am signed in to pro max but it is insisting on usage
credits to use fable. continue on jsut this modle its opus 5.5 which is new". It answers the question returned in
`sp_durable/Ezek/EZEK_CLOSE_GATE_OWNER_RULING.v1.md` section 4a after the owner checked the account, and it reads with
the owner's earlier "lets do that for the rest of this entire project". **Scope: project-wide, all 42 remaining books.**

**What it settles.** (1) Every role runs on `claude-opus-5-5`: orchestration, authoring, research, and the checking,
architecting and adjudicating roles OW-13 assigned to `claude-fable-5-1`. "Just this model" also retires Sonnet and
Haiku from bounded low-level work; that direction is stricter, never weaker. (2) This is the declared-in-advance
fallback grader that decision packet v2 section 7 asked for: option B for Ezekiel, generalised to the campaign.

**What it does NOT change.** OW-19 stands: two blind lanes are the floor, the orchestrator never grades its own items,
and a grading lane must be a non-author subagent. OW-22 stands: 72,000,000 is a hard line for Ezekiel, and this
directive changes who grades, not how much may be spent. OW-11 stands: closing, publication and campaign-log appends
remain the owner's act.

**The downgrade, stated so no reader mistakes a fallback grade for an OW-13 grade.** Author and grader now share one set
of weights. A blind Opus lane is a genuine non-author and a genuine second context; it is a weaker second MIND than
OW-13 intended, because correlated habits are what a same-weights reviewer is least able to see. Model-family
decorrelation is therefore unavailable for the rest of the campaign, so the two-lane floor must be decorrelated by the
means that remain: blind briefs that differ in method and read order, no shared intermediate files, deterministic
gates wherever a check can be computed, and evidence that cites source bytes rather than another lane's prose. Every
completion receipt from here on records `grader_fallback` with the model id and this statement.

**The code gates.** The Lamentations close tool's `claude-fable-5-1` assertions (lines 58, 60, 61, 88) are NOT deleted
or edited: Lamentations is closed and its tool is its record. Ezekiel's close tool does not exist yet; when it is built
from the Lamentations pattern, the grader model is READ from a campaign carrier that names the declared fallback, and
the tool asserts that the completion receipt carries the downgrade statement - the gate keeps naming its model rather
than being loosened to accept any.

**Account, recorded and not pursued.** The owner REPORTS being signed into Max; the usage card MEASURED on 2026-09-22 read
`plan: Pro`. Unreconciled and no longer blocking. No billing, credit or account act was taken or is advised.
"""

SEC4B = """
## 4b. The grader question — answered 2026-09-22 (OW-25)

After checking the account the owner wrote (TRANSCRIBED): "i am signed in to pro max but it is insisting on usage credits
to use fable. continue on jsut this modle its opus 5.5 which is new". **Option B is chosen for Ezekiel and generalised to
the campaign:** `claude-opus-5-5` is the declared fallback for every Fable role, with the downgrade recorded in the
ledger as OW-25 and in every completion receipt. Section 4a's reserved acts are released only as far as that ruling
reaches: reassigning the grader role and building Ezekiel's close tool against a declared-fallback carrier. Still NOT
released: any billing or account act, any change to the closed Lamentations tool, and any spend above the OW-22 hard
line - which section 4 of decision packet v2 shows the remaining passes would cross, so a named scope cut goes to the
owner before any pass starts.
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


print(append(LEDGER, OW25, "## OWNER DIRECTIVE OW-25 ", LEDGER_PIN))
print(append(RULING, SEC4B, "## 4b. "))
