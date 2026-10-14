#!/usr/bin/env python3
"""Build BIBLE_CHUNKING_METHOD.v7.md from v6 by ANCHORED INSERTION of the text an adjudicator adopted.

WHY. Close-gate item 23 (OW-17 c): every method-change proposal a book's proposer makes is adjudicated by someone who
is neither the proposer nor the orchestrator, and each ADOPTED proposal is carried into a new method version with a
change table. Daniel's proposer made eight proposals; the adjudicator adopted six and rejected two. This generator
carries the six adopted texts into v7 BYTE FOR BYTE as the adjudicator returned them: it reads `adopted_text` from the
landed adjudication record, whose sha256 it pins, and authors none of it. What this generator does author is named in
v7's provenance tail: the header, the change table's wording around each adopted lead sentence, two pointer lines,
one label, and the tail itself.

HOW IT WORKS. As gen_method_v6.py: every anchor must occur EXACTLY ONCE in v6's bytes; a miss or a second hit is a
hard failure. v6's bytes are never modified. A section gains text at its END, which is found from the next section's
heading (stepping back over the rule line that closes a section, where there is one).

Usage: gen_method_v7.py [--check]   (--check regenerates to a temp file and compares digests only)
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

M8 = Path(__file__).resolve().parent
SRC = M8 / "BIBLE_CHUNKING_METHOD.v6.md"
OUT = M8 / "BIBLE_CHUNKING_METHOD.v7.md"
DAN = M8 / "sp_durable" / "Dan"
ADJ = DAN / "close" / "landed" / "D5_e1" / "method_change_adjudications.Dan.v1.json"
ADJ_SHA = "efc1b89b4a504618ef3efa23471aabfeaad4dd6dfb338f7f70eeca7516ba0cae"
ROWS = DAN / "rows_v1_final.jsonl"
ROWS_SHA = "783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09"
ROUTED = DAN / "fable_end_review" / "routed_items.v1.jsonl"
DATE = "2026-10-13"

# proposal -> (section it enters, the heading of the NEXT section, which is where that section ends)
SECTION_END = {
    5: "## 6. The received paragraph layer",
    7: "## 8. Numbering divergence between witnesses",
    9: "## 10. Capture discipline",
    12: "## 13. Open method questions handed forward",
    13: "## 14. Anti-patterns, stated for a chunker",
}
# order matters inside a section: the adjudicator's cross-proposal note puts Dan-P01 before Dan-P05 in section 9
PLACE = [("Dan-P02", 5), ("Dan-P03", 7), ("Dan-P01", 9), ("Dan-P05", 9), ("Dan-P04", 12), ("Dan-P06", 18)]
A_S18 = "**Enforce it in a tool, not in your memory.**"

# Dan-P06's adopted text carries two placement lines of the adjudicator's own. They are obeyed, not pasted.
P06_HEAD = "In section 18, after 'Enforce it in a tool':"
P06_S9 = "In section 9, one line: "
LABEL_S9 = "**From Dan-P06 (new in v7, M8, Daniel).** In brief: "
POINTER_S13 = ("**Pointers (new in v7, M8, Daniel).** Question 6 above: §12 gained a paragraph in v7 (from Dan-P04) that bears "
               "on it. Question 10 above: §9 gained a paragraph in v7 (from Dan-P05) that bears on it. Neither paragraph "
               "closes its question; each prescribes a control Daniel did not run.")
POINTER_S18 = ("**Pointer (new in v7, M8, Daniel; from Dan-P02).** When the check for a convention must be installed, and what "
               "a form check does not prove, are stated in §5, in the paragraphs new in v7.")

HEADER_RE = re.compile(r"\*\*This version:\*\* v6,.*?itself auditable\.", re.S)
HEADER_NEW = """**This version:** v7, written by generation **M8** for the **close of Daniel** (book 27 of 66), before that book's
close tool ran. Measured when written: the book's final rows file holds **%(rows)d** units; **12** controlling rulings
(E1 to E12) are on file; **%(routed)d** questions are carried open to the end review; the book's proposer made **8**
method-change proposals, of which an adjudicator who was neither the proposer nor the orchestrator adopted **6** and
rejected **2**. Every paragraph v7 adds is that adjudicator's text, and every one prescribes a control Daniel did not
run or ran only in part: read each as a control handed forward untried, which §13 warns about.
**Supersedes v6** (`BIBLE_CHUNKING_METHOD.v6.md`, sha256 `%(v6)s`), which carries the supersession chain back to v1 and
whose bytes, like every earlier version's, are kept unchanged so the evolution of this method is itself auditable."""

A_CHANGETABLE = "### v5 → v6 (M8, Ezekiel close, 2026-09-21)"
A_PROV = re.compile(r"## Provenance and limits of this version\n.*$", re.S)
PROV_NEW = """## Provenance and limits of this version

- Written at **M8, for Daniel's close**, %(date)s, before the close tool ran. Every paragraph new in v7 is the
  adopted text of one adjudication in `sp_durable/Dan/close/landed/D5_e1/method_change_adjudications.Dan.v1.json`
  (sha256 `%(adj)s`), carried byte for byte, with one exception stated here: the text adopted from Dan-P06 came with two placement
  lines of the adjudicator's own ("In section 18, after ..." and "In section 9, one line: ..."). Those two lines were
  obeyed and are not reproduced; the section 9 line itself is reproduced after a label. The proposals are in
  `sp_durable/Dan/close/landed/D3_e1/method_change_proposals.Dan.candidate.jsonl` (sha256 `%(prop)s`). Each of the six
  adopted texts differs from its proposal's wording; the adjudication record states each difference.
- **What the adjudication is, and is not.** One reader adjudicated all eight proposals. That reader ran on the
  campaign's recorded fallback model (owner directive OW-25), in the same model family as the proposer, as every
  Daniel lane the proposals cite, and as the ruling role. The adjudicator agreed with the proposer's rating on all
  eight. Under §19 that agreement is one voice and not a confirmation, and six adopted of eight is a high rate from
  one book. The adjudicator found a citation that did not hold as cited in seven proposals and a path defect in the
  eighth; it reports that in no adopted proposal did the underlying fact fail on the other evidence it read. Its
  evidence was read through script extracts, not whole packets, and the counts it quotes from its sources are
  quoted and not re-measured.
- **Untried controls.** Each adopted paragraph prescribes a control that Daniel did not run or ran only in part, and
  says so in its own text. The owner or the architect role may prefer any of them to stand as an open question.
  The paragraph from Dan-P01 records flags by a flag key that the tooling does not yet define: Dan-P07, which would
  have defined it, was rejected as method text and sent to the tool backlog. Until that tool change is made, the
  Dan-P01 control is weaker than its text reads.
- **Written by the orchestrator, not by the adjudicator:** the header, the wording of the change table around each
  adopted paragraph's lead sentence, the pointer lines in §13 and §18, the label before the §9 line and this tail. The adjudicator asked
  for the §13 pointers at questions 6 and 10; they stand as one paragraph at the end of §13 instead, so that no
  question's own text was altered.
- **Checked mechanically.** `check_method_record.py`, kept beside this file, verifies the version in the header
  against the filename, the superseded version's digest against its bytes on disk, the bidirectional agreement
  between the newest change table and the sections it names, the obligation list, the carried-forward open questions
  and the presence of §19's floor. Its selftest tampers with a copy in each of those ways and requires the
  corresponding check to fail. Run both before you trust this file's change table.
- **This file was generated**, by `gen_method_v7.py` from v6 by anchored insertion; v6's bytes were not modified. The
  generator pins the adjudication record's digest and refuses to run against any other bytes. `gen_method_v6.py` is
  retained unchanged beside it.
- **Not verified:** M9's conventions and its closed books, and M7's method — §1 exists *because* that reconciliation
  has not happened. The remaining 39 books are not here. No New Testament book has been chunked under this method,
  so nothing in this version has been tested against a Greek witness, and §7's witness discipline is written from
  Hebrew, Aramaic and English evidence only. No statement in v6 was re-verified in making v7; v6's text is carried.
- **Unmeasured, and staying that way:** v6's figure of 11 rate-limited review attempts in Ezekiel's final wave stands
  as v6 disclosed it. In Daniel's close phase two executions were interrupted by a usage limit and resumed; the
  token use of each first segment is unavailable and is disclosed rather than estimated (§18).
- The per-book scholar-facing record required by OW-17 is a **different** document with a different reader, generated
  from the landed records. Daniel's is at v1. Its licence wording was carried from Ezekiel's record and has not been
  confirmed against Daniel's own witness files; confirm it before any publication.
- Witness licensing travels with any published quotation: the Hebrew and Aramaic witness (OSHB) and the translation
  (WEB) carry their own attribution terms, which a published record must state.
- **Canonical home:** this file sits under `M8_fable/` because that is where this generation's write authority reaches.
  Its proper home is above any single generation's directory; placing it there is the owner's act, as is publication.
"""

MARK_RE = re.compile(r"\s*\(new in v7[^)]*\)")
BANNED = ("TODO", "TBD", "FIXME", "XXX", "<fill", "LOREM")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def once(text, anchor):
    n = text.count(anchor)
    if n != 1:
        sys.exit("FAIL: anchor occurs %d times, not once: %s" % (n, anchor[:60]))
    return text.index(anchor)


def at_section_end(text, sec, payload):
    pos = once(text, SECTION_END[sec])
    if text[:pos].endswith("\n---\n\n"):
        pos -= len("---\n\n")
    if not text[:pos].endswith("\n\n"):
        sys.exit("FAIL: section %d does not end on a blank line" % sec)
    return text[:pos] + payload + "\n\n" + text[pos:]


def after_paragraph(text, anchor, payload):
    pos = once(text, anchor)
    end = text.index("\n\n", pos)
    return text[:end] + "\n\n" + payload + text[end:]


def load():
    if sha(ADJ) != ADJ_SHA:
        sys.exit("FAIL: the adjudication record is not the bytes this generator pins")
    if sha(ROWS) != ROWS_SHA:
        sys.exit("FAIL: the final rows file is not the bytes this generator pins")
    d = json.loads(ADJ.read_text(encoding="utf-8"))
    adj = {a["proposal_id"]: a for a in d["adjudications"]}
    want = {p for p, _ in PLACE}
    got = {k for k, a in adj.items() if a["verdict"] == "ADOPT"}
    if got != want:
        sys.exit("FAIL: adopted set %s is not the set this generator places %s" % (sorted(got), sorted(want)))
    for p in want:
        if p == "Dan-P06":
            ps = adj[p]["adopted_text"].split("\n\n")
            if ps[0] != P06_HEAD or not ps[-1].startswith(P06_S9) or len(ps) < 3:
                sys.exit("FAIL: Dan-P06's placement lines are not the ones this generator was written against")
            adj[p]["s9_line"] = ps[-1][len(P06_S9):]
            adj[p]["adopted_text"] = "\n\n".join(ps[1:-1])
        t = adj[p]["adopted_text"]
        if len(MARK_RE.findall(t)) < 1 or any(b in t for b in BANNED) or "\r" in t or not t.startswith("**"):
            sys.exit("FAIL: adopted text of %s lacks a v7 marker, a bold lead, or holds a banned token" % p)
    return d, adj


def lead(t):
    s = MARK_RE.sub("", re.match(r"\*\*(.+?)\*\*", t, re.S).group(1)).strip()
    if "|" in s or "§" in s or "\n" in s:
        sys.exit("FAIL: a lead sentence cannot stand in a table cell: %s" % s[:60])
    return s


def change_table(d, adj):
    rows = ["### v6 → v7 (M8, Daniel close, %s)" % DATE, "", "| Change | Why |", "|---|---|"]
    for p, sec in PLACE:
        a = adj[p]
        rows.append("| **§%d gains: %s** (%s) | Adopted by adjudication and rated %s by the adjudicator, as the proposer "
                    "had estimated. The measured cause in Daniel is stated in the paragraph itself. The control is handed "
                    "forward untried. The adopted wording differs from the proposal's; the adjudication record states how. |"
                    % (sec, lead(a["adopted_text"]), p, a["rating"]))
    rows.append("| **§13 gains one paragraph of pointers** from questions 6 and 10 to the paragraphs above (Dan-P04, "
                "Dan-P05). | The adjudicator asked for the pointers. They close neither question. |")
    r = d["rates"]
    rows.append("| Not adopted: Dan-P07 and Dan-P08. No section changes. | Both were rejected and rated LOW_REWARD. "
                "Dan-P07 is by its own account a tool fix and is sent to the tool backlog; Dan-P08 gives no text to adopt. "
                "Both stay in the proposal log with the reasons, because a rejected proposal is evidence. Rates for this "
                "book: proposed %d, adopted %d, rejected %d, deferred %d. |"
                % (r["proposed"], r["adopted"], r["rejected"], r["deferred"]))
    return "\n".join(rows) + "\n\n"


def build():
    d, adj = load()
    text = SRC.read_text(encoding="utf-8")
    head = "# BIBLE CHUNKING METHOD — v6\n"
    if not text.startswith(head):
        sys.exit("FAIL: v6 title line is not what this generator was written against")
    text = head.replace("v6", "v7") + text[len(head):]
    nrows = sum(1 for ln in ROWS.read_text(encoding="utf-8").splitlines() if ln.strip())
    nrouted = sum(1 for ln in ROUTED.read_text(encoding="utf-8").splitlines() if ln.strip())
    if len(HEADER_RE.findall(text)) != 1 or len(A_PROV.findall(text)) != 1:
        sys.exit("FAIL: the header or the provenance tail was not found exactly once")
    text = HEADER_RE.sub(lambda _m: HEADER_NEW % {"rows": nrows, "routed": nrouted, "v6": sha(SRC)}, text, count=1)
    pos = once(text, A_CHANGETABLE)
    text = text[:pos] + change_table(d, adj) + text[pos:]
    for p, sec in PLACE:
        t = adj[p]["adopted_text"]
        if sec == 18:
            text = after_paragraph(text, A_S18, t + "\n\n" + POINTER_S18)
        else:
            text = at_section_end(text, sec, t)
    text = at_section_end(text, 9, LABEL_S9 + adj["Dan-P06"]["s9_line"])
    text = at_section_end(text, 13, POINTER_S13)
    text = A_PROV.sub(lambda _m: PROV_NEW % {"date": DATE, "adj": ADJ_SHA, "prop": d["proposals_sha256"]}, text, count=1)
    return text.encode("utf-8")


def main():
    data = build()
    digest = hashlib.sha256(data).hexdigest()
    if "--check" in sys.argv:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / OUT.name
            p.write_bytes(data)
            again = hashlib.sha256(build()).hexdigest()
        on_disk = sha(OUT) if OUT.exists() else "ABSENT"
        ok = digest == again == on_disk
        print("regenerated %s, on disk %s: %s" % (digest[:16], on_disk[:16], "MATCH" if ok else "DIFFER"))
        sys.exit(0 if ok else 1)
    if OUT.exists() and sha(OUT) != digest and "--replace" not in sys.argv:
        sys.exit("REFUSED: %s exists with other bytes; a method version is re-issued, never overwritten" % OUT.name)
    OUT.write_bytes(data)
    print("%s sha256 %s bytes %d" % (OUT.name, digest, len(data)))


if __name__ == "__main__":
    main()
