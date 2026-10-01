#!/usr/bin/env python3
"""Build BIBLE_CHUNKING_METHOD.v6.md from v5 by ANCHORED INSERTION, and report what changed.

WHY A GENERATOR AND WHY IT IS KEPT. v6's own §10 lesson is that a generator which produced a retained document must
be copied aside before it is extended, because the M8 scholar record's v1 generator was extended in place and its
bytes are gone. The same defect had already happened to this file's ancestor: v5's change table claims "a mechanical
check now verifies every section this table names", and no such check exists anywhere in the worktree - measured
2026-09-21 by searching every .py under the generation's tree for the record's filename. So v6 ships two retained
tools instead of one claim: this generator, and check_method_record.py.

HOW IT WORKS. Every operation names an anchor that must occur EXACTLY ONCE in v5's bytes; a miss or a second hit is a
hard failure, not a silent no-op, because an insertion that lands nowhere would produce a v6 whose change table lists
changes the document does not contain - the exact offence v5 recorded against itself. v5's bytes are never modified.

Usage: gen_method_v6.py [--check]   (--check regenerates to a temp file and compares digests only)
"""
import hashlib
import re
import sys
import tempfile
from pathlib import Path

M8 = Path(__file__).resolve().parent
SRC = M8 / "BIBLE_CHUNKING_METHOD.v5.md"
OUT = M8 / "BIBLE_CHUNKING_METHOD.v6.md"

# ---------------------------------------------------------------- new front matter

HEADER_RE = re.compile(r"\*\*This version:\*\* v5,.*?itself auditable\.", re.S)

HEADER_NEW = """**This version:** v6, written by generation **M8** at the **close of Ezekiel** (book 26 of 66). Measured at
close: **44 of 44** dual-blind primary review executions and **11** peer executions landed; a final reconciliation
wave of **18** executions (6 slices x two blind lanes + one reconciling reader each) disposed of **543** repair items
(478 carried out, 57 refused for want of evidence, 7 stopped, 1 question about a recorded grade); the book ships
**138** units after a re-tiling, with **131** recorded disputes, and its validator suite reports zero defects on the
shipped rows.
**Supersedes v5** (`BIBLE_CHUNKING_METHOD.v5.md`, sha256 `%s`), which carries the supersession chain back to v1 and
whose bytes, like every earlier version's, are kept unchanged so the evolution of this method is itself auditable."""

# ---------------------------------------------------------------- 0. change table

A_CHANGETABLE = "### v4 → v5 (M8, Ezekiel, 2026-09-15)"

CHANGETABLE_NEW = """### v5 → v6 (M8, Ezekiel close, 2026-09-21)

| Change | Why |
|---|---|
| **§6 gains the DISCLOSURE SET a unit owes the received mark layer: the front seam (the verse before the span's start), every mark interior to the span, and the end verse — disclosed unconditionally, whether or not the unit's prose engages that layer.** | v5 fixed the *direction* of a mark claim and left the *extent* of the obligation open as §13 question 4. M8 settled it in a tool rather than in prose: the seam-and-interior set is checked against a byte-extracted mark inventory keyed to the Hebrew witness, with a dual-reading arm inside a numbering-divergence zone. Ezekiel's shipped rows reach zero under it. |
| **§8 gains the derivation rule for a divergence zone: an extract that must show a verse under a second numbering DERIVES the key, and never falls back to the other witness's key when its own lookup misses.** A miss is a defect to report, not a value to substitute. **And every apparatus claim on a zone row is re-measured before a merge.** | Measured, and mine: a slice extract built for the final wave fell back to a translation-keyed entry when the Hebrew key carried no apparatus entry, so two blind lanes were shown a scribal mark that does not exist at that verse. A blind lane cannot detect a fabricated input; the reconciling reader caught it. Falling back is how an extraction layer invents evidence while every check above it passes. |
| **§10 gains: keep the GENERATOR, not only the document — copy it aside BEFORE you extend it — and re-issue a generated record as vN+1 rather than overwriting it.** | Measured, and mine: the v1 scholar record's generator was extended in place to produce v2, so v1's document and its check record survive and its digest can still be verified, but v1 cannot be re-derived. Worse, it could not have been re-derived from current inputs in any case, because the re-tiling superseded the rows it read. A retained document whose generator is gone is an assertion with a digest on it. |
| **§10 also gains: fix the OUTPUT FIELD NAMES at launch and validate them on landing.** | Measured: six parallel reconciling executions each named the adopted decision differently — `what_i_wrote`, `what_i_adopt` twice, `what_i_adopted`, `adjudication`, `decision`. Nothing was lost, but every reader of those records must now carry a per-slice mapping and disclose it. One schema line in the brief and one landing check would have cost nothing. |
| **§12 gains validator-scope discipline: scope each arm of a checker to the FIELD CLASS it was written for, and scope a document-wide test by PATTERN rather than by a hard-coded heading.** | Two measurements. A vocabulary arm written for schema-controlled fields was applied to a free-observation field and raised three false flags on sound rows; the cure excludes that field on that arm only, with 53 selftest vectors green. And the scholar record's vocabulary test was scoped by splitting on the literal heading "## 6. Provenance"; inserting a section renumbered that heading, and the test would have kept passing over a shrinking document. A test that passes because its scope moved is worse than no test. |
| **§12 also gains the NEGATIVE CONTROL rule: a gate whose pass you report must be shown to fail.** | Measured: the scholar record's checker returned 12 of 12 on the true document, and on a tampered copy — one quoted refusal deleted and a line of internal codes planted — it failed three checks and caught all four planted tokens. Before that, "12 of 12 pass" was a number without a demonstration behind it. |
| **§12 also records a DISCLOSURE against v5 itself: v5's change table claims a mechanical check verifies every section that table names, and those bytes were not retained.** v6 ships `check_method_record.py`, and makes the rule bidirectional — every section the newest change table names must carry a v6 marker, and every section carrying a v6 marker must appear in the table. | A check whose bytes are gone is indistinguishable from a check that never ran. The one-directional version could also be satisfied by a table row pointing at a section that was never touched. Both holes are closed by a tool that is kept beside the document it checks. |
| **§13 question 4 is marked ANSWERED IN PRACTICE** (see §6), and two new questions are handed forward: re-tiling a book after review, and what a second reading owes a first. | §13's value is that it is honest about what a generation could not settle. An answered question left in the open list wastes the next generation's attention; an unanswered one removed from it hides a problem. |
| **§16 gains obligations 12 and 13.** | A rule nobody is obliged to check erodes — v5's own reason for obligation 11, now applied to the negative control and to generator retention. |

"""

# ---------------------------------------------------------------- 6. marks

A_S6_TAIL = "\n---\n\n## 7. Witnesses and quotation discipline"

S6_NEW = """
**The disclosure set, new in v6.** Direction is not the whole obligation. A unit owes the mark layer a statement about
**every mark relevant to its span**: the mark on the verse **before** its start (its front seam), **every mark
interior** to its span, and the mark on its **end verse**. Disclosure is **unconditional** — it is owed even when the
unit's prose does not otherwise engage the mark layer, and even when the mark corroborates the unit only weakly. What
the unit *concludes* from the mark is its judgement; that the mark *is there* is not.

Check it mechanically against a **byte-extracted inventory keyed to the Hebrew witness**, and inside a
numbering-divergence zone check the claim under **both** readings (§8). Two arms are worth building at the same time:
the **off-by-one signature** (a claim whose verse is one off from a real mark, which is the direction error above,
seen from the tool's side), and an **absence arm** scoped to the span (a unit asserting "no mark here" is making a
checkable claim about the inventory, not a rhetorical aside).

M8's shipped Ezekiel rows report **zero** span-relevant marks left undisclosed under that check. Take the zero as
evidence about the rows, not about the rule: the same check on an earlier corpus is what turned §13's question 4 from
an open decision into a settled obligation.
"""

# ---------------------------------------------------------------- 8. numbering

A_S8_TAIL = "\n---\n\n## 9. Review design: what actually found things"

S8_NEW = """
**Derive, never fall back (new in v6, and it cost M8 a fabricated input).** Any artefact that presents a verse under
a second numbering — an extract, a brief, a reviewer packet — must **derive** the second key from the offset map. If
the derived key misses in the source it is reading, that is a **defect to report**, and never a licence to substitute
the other witness's key "so the row has something in it". M8's final-wave slice extracts did exactly that: where the
Hebrew key carried no apparatus entry, the builder fell back to the translation key, and two blind lanes were shown a
scribal mark that does not exist at that verse. A blind lane has no way to detect a fabricated input; only the
reconciling reader caught it, and only because it re-read the witness.

Two rules follow, and the second is the one that generalises:

- **Fail loudly on a missing key.** A lookup that misses returns nothing and says so. Any fallback that silently
  changes *which witness* a value came from is a provenance fault (§18), not a convenience.
- **Re-measure every apparatus claim on a zone row before a merge.** Zone rows are the rows most likely to carry a
  key that was derived rather than read, so they are the rows where a re-measurement pays. M8 built that check after
  the fact and re-measured every apparatus claim on its zone rows before the merge landed.
"""

# ---------------------------------------------------------------- 10. capture

A_S10_TAIL = "\n---\n\n## 11. Verify coverage as SET EQUALITY, not as a count"

S10_NEW = """
**Keep the generator, not only the document (new in v6, measured on my own work).** A record that is generated from
pinned inputs is worth far more than a hand-written one, because a checker can re-derive it and compare digests —
that is how "nothing in here that is not in a record" gets *established* rather than asserted. All of which collapses
the moment the generator's bytes are gone.

M8's scholar record v1 was generated, digested and checked. Its generator was then **extended in place** to produce
v2. v1's document and its check record are still on disk and its digest still verifies, but v1 can no longer be
re-derived; and it could not have been re-derived from current inputs anyway, because the re-tiling superseded the
rows it read. So:

- **Copy a generator aside before you extend it**, under a name that records what it produced. A generator that
  produced a retained document is part of that document's provenance.
- **Re-issue a generated record as vN+1; never overwrite it.** The same rule this method record follows (§16.6) is
  owed to every document a generation retains.
- **A retained document whose generator is gone keeps its digest and loses its reproducibility.** Say so in the
  document, in those words. M8's v2 carries that disclosure.

**Fix the output field names at launch (new in v6).** When you fan a wave out, state in the brief the exact field
names each execution must write, and validate them as the records land. M8 did not, and its six parallel reconciling
executions named the adopted decision six different ways — `what_i_wrote`, `what_i_adopt` twice, `what_i_adopted`,
`adjudication`, `decision`. Nothing was lost, but every later reader carries a per-slice mapping and has to disclose
it, and a reader who guessed the field name instead would have silently read nothing.
"""

# ---------------------------------------------------------------- 12. scaffolding

A_S12_TAIL = "\n---\n\n## 13. Open method questions handed forward"

S12_NEW = """
**Scope discipline, new in v6 — a checker that is right about the wrong field.** Two measurements from Ezekiel's
close, both about *scope* rather than logic:

- **Scope each arm to the field class it was written for.** A vocabulary arm written for schema-controlled fields was
  applied to a **free-observation** field, where an observer's own words are the point, and raised three false flags
  on sound rows. False flags are not harmless: someone must adjudicate each one, and a checker that cries wolf is a
  checker people start overriding. The cure excluded that one field on that one arm, with selftest vectors (53, all
  green) so the exclusion itself cannot rot.
- **Scope a document-wide test by pattern, not by a hard-coded heading.** The scholar record's vocabulary test took
  the body as everything before the literal string `## 6. Provenance`. Inserting a section renumbered that heading to
  `## 7.`, at which point the split would have found nothing, the "body" would have been the whole document, and the
  test would have gone on passing while checking something other than what it was written to check. A test that
  passes because its scope moved is worse than no test, because it reports a guarantee. Match the boundary with a
  pattern, and fail hard if the boundary is not found.

**Show that your gate can fail (new in v6).** A gate whose pass you report must have a **negative control**: tamper
with a copy of the artefact in exactly the way the gate exists to catch, run the gate, and record that it failed.
M8's scholar-record checker returned 12 of 12 on the true document; on a copy with one quoted refusal deleted and a
line of internal codes planted, it failed three checks and caught all four planted tokens. Only after that does "12
of 12" mean anything. Budget the control: it is one run of a tool you already have.

**A disclosure about this record, recorded here rather than quietly fixed.** v5's change table says that "a
mechanical check now verifies every section this table names". Measured 2026-09-21: **no such check exists** anywhere
under this generation's tree. Its bytes were not retained — the same defect class as the lost generator in §10, and
committed in the file that defines provenance discipline. v6 ships `check_method_record.py` beside this document and
makes the rule **bidirectional**: every section named in the newest change table must carry a v6 marker, and every
section carrying a v6 marker must be named in that table. One direction alone would still pass a table row pointing
at a section nobody touched.
"""

# ---------------------------------------------------------------- 13. open questions

A_S13_Q4 = """4. **In-span mark disclosure.** Must a unit disclose a received mark falling *inside* its own span, not only at its
   seams? Four independent executions found undisclosed in-span marks. Decide the obligation, then build the check in
   both directions (§9)."""

S13_Q4_NEW = """4. **In-span mark disclosure — ANSWERED IN PRACTICE (v6, see §6).** Must a unit disclose a received mark falling
   *inside* its own span, not only at its seams? Four independent executions found undisclosed in-span marks. M8
   answers **yes, unconditionally**, and enforces it in a tool rather than in prose: the disclosure set is the front
   seam, every interior mark and the end verse. The answer is recorded as a *practice with a check behind it*, not as
   a ruling — a later generation with a witness that carries within-verse position (question 1) may refine what
   "interior" means, but not whether disclosure is owed."""

A_S13_TAIL = """8. **Conjectural emendations in glosses.** One unit glossed a byte-exact quotation with a conjectural reading rather
   than what the witness says. Decide whether that is permitted and how it must be marked."""

S13_TAIL_NEW = """

**New in v6, handed forward unsettled:**

9. **Re-tiling a book after review.** Ezekiel's units were re-tiled after its primary round, so 13 recorded disputes
   are addressed to units that no longer exist. M8 cured the *reporting* — name the passage rather than the unit, pin
   the superseded division, and mark those findings as belonging to it — but not the *question*: should a tiling be
   frozen before review opens, and when a re-tiling is unavoidable, what is the minimum re-review owed to a finding
   whose unit dissolved? Re-running every lane is honest and expensive; re-mapping by overlap is cheap and quietly
   changes what a reviewer was asked.
10. **What a second reading owes a first.** Ezekiel's final wave re-measured 543 repair items and found 57 with
   nothing to repair and 8 it refused to act on. Whether that ratio says more about the repair pass or about the
   reader cannot be told from one book. Record yours in comparable form, and the second generation to do so can
   answer it."""

# ---------------------------------------------------------------- 16. obligations

A_S16_TAIL = """11. **Never review a unit group with one lens** (§19). State your per-book lens count and the reason for it; an
    unrecorded lens count is a form problem. If you add a lane to a book someone else already chunked, say which
    of the two retrofit shapes it was, and never call an audit of existing rows a second blind lane."""

S16_TAIL_NEW = """
12. **Ship a negative control with every gate whose pass you report** (§12, new in v6). Tamper with a copy in the way
    the gate exists to catch, run the gate, record that it failed. A gate that has never been shown to fail is an
    assertion wearing a number.
13. **Keep the generator, not only the document** (§10, new in v6). Copy it aside before you extend it, re-issue a
    generated record as vN+1, and if a retained document's generator is gone, say so in the document."""

# ---------------------------------------------------------------- provenance tail

A_PROV = re.compile(r"## Provenance and limits of this version\n.*$", re.S)

PROV_NEW = """## Provenance and limits of this version

- Written at **M8 / Ezekiel's close**, 2026-09-21. Measured at close: **44 of 44** dual-blind primary executions and
  **11** peer executions landed; **18** final-wave executions disposed of **543** repair items; the book ships **138**
  units and **131** recorded disputes; the validator suite reports zero defects on the shipped rows across citation,
  role-token, mark-symmetry, quotation, reference-mirror, language-zone, n-gram, capitalisation and register arms.
  Every measured claim in this version traces to a landed record under `M8_fable/sp_durable/Ezek/` or a finding under
  `M8_fable/sp_durable/campaign/`.
- **Checked mechanically.** `check_method_record.py`, kept beside this file, verifies the version in the header
  against the filename, the superseded version's digest against its bytes on disk, the bidirectional agreement
  between the newest change table and the sections it names, the obligation list, the carried-forward open questions
  and the presence of §19's floor. It ships with a selftest that tampers with a copy in each of those ways and
  requires the corresponding check to fail. Run both before you trust this file's change table.
- **This file was generated**, by `gen_method_v6.py` from v5 by anchored insertion; v5's bytes were not modified. The
  generator is retained — which is §10's new rule, applied to this document.
- **Not verified:** M9's conventions and its closed books, and M7's method — §1 exists *because* that reconciliation
  has not happened. Daniel and the remaining 40 books are not here. Nor is any Greek witness: at Ezekiel's close the
  campaign has no staged Greek text, so nothing in this version has been tested against a New Testament book, and
  §7's witness discipline is written from Hebrew and English evidence only.
- **One figure is unmeasured and stays that way:** 11 review attempts failed on a provider rate limit during the
  final wave. That spend is real and is not captured by the receipts census, and it is disclosed rather than
  estimated (§18).
- The per-book scholar-facing record required by OW-17 is a **different** document with a different reader, generated
  from the landed records. Ezekiel's is at v2; its v1 is retained and digest-checkable but not re-derivable (§10).
- Witness licensing travels with any published quotation: the Hebrew witness (OSHB) and the translation (WEB) carry
  their own attribution terms, which a published record must state.
- **Canonical home:** this file sits under `M8_fable/` because that is where this generation's write authority reaches.
  Its proper home is above any single generation's directory; placing it there is the owner's act, as is publication.
"""

OPS = [
    ("re", HEADER_RE, None),
    ("before", A_CHANGETABLE, CHANGETABLE_NEW),
    ("before", A_S6_TAIL, S6_NEW),
    ("before", A_S8_TAIL, S8_NEW),
    ("before", A_S10_TAIL, S10_NEW),
    ("before", A_S12_TAIL, S12_NEW),
    ("replace", A_S13_Q4, S13_Q4_NEW),
    ("replace", A_S13_TAIL, A_S13_TAIL + S13_TAIL_NEW),
    ("replace", A_S16_TAIL, A_S16_TAIL + S16_TAIL_NEW),
    ("re", A_PROV, PROV_NEW),
]


def build():
    src = SRC.read_text(encoding="utf-8")
    v5_sha = hashlib.sha256(SRC.read_bytes()).hexdigest()
    text = src
    if not text.startswith("# BIBLE CHUNKING METHOD — v5\n"):
        sys.exit("FAIL: v5 title line is not what this generator was written against")
    text = text.replace("# BIBLE CHUNKING METHOD — v5\n", "# BIBLE CHUNKING METHOD — v6\n", 1)
    for mode, anchor, payload in OPS:
        if mode == "re":
            n = len(anchor.findall(text))
            if n != 1:
                sys.exit("FAIL: regex anchor matched %d times: %s" % (n, anchor.pattern[:60]))
            text = anchor.sub(lambda _m: (HEADER_NEW % v5_sha) if payload is None else payload, text, count=1)
            continue
        n = text.count(anchor)
        if n != 1:
            sys.exit("FAIL: anchor occurs %d times (needs exactly 1): %r" % (n, anchor[:70]))
        text = text.replace(anchor, payload if mode == "replace" else payload + anchor, 1)
    return text, v5_sha


def main():
    text, v5_sha = build()
    data = text.encode("utf-8")
    if "--check" in sys.argv:
        with tempfile.NamedTemporaryFile("wb", suffix=".md", delete=False) as fh:
            fh.write(data)
            tmp = Path(fh.name)
        on_disk = hashlib.sha256(OUT.read_bytes()).hexdigest() if OUT.exists() else "ABSENT"
        rebuilt = hashlib.sha256(data).hexdigest()
        tmp.unlink()
        print("on_disk  %s\nrebuilt  %s\n%s" % (on_disk, rebuilt,
                                                "DETERMINISTIC: MATCH" if on_disk == rebuilt else "MISMATCH"))
        sys.exit(0 if on_disk == rebuilt else 1)
    OUT.write_bytes(data)
    print("wrote    %s\nbytes    %d\nlines    %d\nsha256   %s\nfrom v5  %s" % (
        OUT.name, len(data), text.count("\n"), hashlib.sha256(data).hexdigest(), v5_sha))
    print("sections %d  v6 markers %d  obligations %d" % (
        len(re.findall(r"(?m)^## \d+\. ", text)), text.count("new in v6") + text.count("New in v6") + text.count("v6,"),
        len(re.findall(r"(?m)^\d+\. \*\*", text))))


if __name__ == "__main__":
    main()
