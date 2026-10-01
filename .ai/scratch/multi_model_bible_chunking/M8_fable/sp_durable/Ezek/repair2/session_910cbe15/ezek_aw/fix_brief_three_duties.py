#!/usr/bin/env python3
"""Add the three duties the brief omitted, so the governing document is correct for its next reader.

The brief-vs-suite control identified exactly these three, from the suite's own member list, without being told
which had regressed. Adding them here and re-running that control is the loop the wave should have gone through
before launch.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
TARGETS = [EZ / "AUTHOR_WAVE_BRIEF.v1.md", HERE / "AUTHOR_WAVE_BRIEF.v1.md"]

SECTION = """
---

## 13. Three duties the validator suite enforces that earlier versions of this brief did not name

These were missing, and six author agents complied with the brief and still broke three checks that were green.
That was the brief's defect, not theirs. Each duty below is enforced mechanically, so it is not advice.

### 13.1 The single-witness disclosure — `citation_sweep`

Parashah marks, paseq and puncta extraordinaria are **tier-3 weak, single-witness** corroboration in the
Prophets. Any `boundary_evidence_refs` entry whose annotation claims one **must contain the literal phrase
`single-witness`**. The checker matches that exact string, hyphenated or spaced. 320 pre-existing entries
observe it.

**The rotation rule's six-word limit governs your FREE TEXT only. A required disclosure is not free text and
sits outside that budget.** An earlier version of this brief left those two rules in contradiction, which is how
a compliant agent fails a gate. Write:

```
oshb:Ezek.4.12 [DISCLOSURE-mark] setumah inside the span (single-witness, tier-3)
```

Also enforced by the same check, and worth knowing before you write: a claimed mark TYPE must match the record
(pe is never conflated with samekh); a paseq is **count-only** and its intra-verse position is not sourceable; a
`selah`, reversed-nun, suspended-letter or large/small-letter claim is an error anywhere in this book.

### 13.2 The register rule — `register`

A decision row is a **scholar-facing record**. Its prose must not name:

- **staged files or their stems** — not `Ezek_oshb.txt`, `pmarks_Ezek.json`, `verse_inventory.json`,
  `ezek_device_inventory.json`, `book_strategy_Ezek.md`, `web_mt_offset_map.json`, `verse_map_oshb.json`, nor
  any stem of them. Say **the pointed Hebrew witness**, **the English witness**, **the section-mark record**,
  **the verse census**, **the device census**, **the division plan**, **the numbering crosswalk**, **the staged
  verse text**.
- **internal rule labels** — not "the precedence rule", "the over-split guard", "the mark-disclosure duty" as a
  name, "§7", "per the strategy", "the strategy's". **State the substance**: "a licensed text signal outranks a
  section mark"; "a row under three verses is held only for a complete word-event unit"; "reading each mark as
  standing on the verse it follows".
- **process talk** — not "this wave", "the worklist", "the preceding row", "row below", any row identifier, any
  ledger id, or the word "campaign".

**You still name your evidence and its tier.** OW-18 is unchanged, and this is not a licence to drop provenance.
The campaign's practice reconciles the two: cite the **witness by reference** and state the tier, without naming
the file the measurement ran over.

### 13.3 Hebrew is sliced, never typed — `hebrew_normalize_dryrun`

Every Hebrew run in a row must be **byte-identical** to the witness, accents included, standing on word
boundaries. **Never hand-type Hebrew. Slice it from the staged verse text.** Three rules the wave's failures
taught:

- **Slice the WHOLE run, from the verse the sentence actually refers to.** The same word carries different
  accents in different verses, so a first-match slice yields an accurate quotation of the **wrong** verse and
  then passes every byte check. The orchestrator's own repair did this, giving two occurrences of one word the
  same verse's bytes when the second referred to another.
- **The field must cite the verse the run came from**, with an `oshb:` reference, or the citation sweep cannot
  collate it.
- **An unpointed run is a skeleton mention, not a quotation**, and will not collate. If you mean a sweep
  pattern, say so in words; otherwise quote the pointed bytes at a cited verse. A Qere is different: it lives in
  the note layer and is legitimately absent from the verse bytes.

### 13.4 Why this section exists at all

The earlier brief was written from the RULINGS. The rulings say what to repair; the suite decides what
"correct" looks like mechanically. A brief that governs a mutation wave must be checked against the gate it will
be measured by, and `check_brief_vs_suite.py` now does that from the suite's own member list: for every check,
either this brief carries its duty or the check is declared out of scope with a reason.
"""

for p in TARGETS:
    t = p.read_text(encoding="utf-8")
    if "## 13. Three duties the validator suite enforces" in t:
        print("already present:", p.name)
        continue
    p.write_text(t.rstrip("\n") + "\n" + SECTION, encoding="utf-8", newline="\n")
    print("updated %s -> %s (%d lines)" % (p.name, hashlib.sha256(p.read_bytes()).hexdigest(),
                                           len(p.read_text(encoding="utf-8").splitlines())))

r = subprocess.run([sys.executable, str(HERE / "check_brief_vs_suite.py")], capture_output=True, text=True,
                   encoding="utf-8", errors="replace")
print()
print(r.stdout[-1200:])
print("brief_vs_suite exit:", r.returncode)
