#!/usr/bin/env python3
"""L-0074..L-0077: the OW-30 Fable ruling's cost, the v10 delta lanes' cost and self-report, the v10 build's text-edit
lessons, and the OW-29 close sequence with the coverage validator's review_packets gap. Evidence digests are computed
at append time from the named files. Idempotent: rows already present are not appended again."""
import hashlib
import json
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
LOG = M8 / "orchestration_learning_log.v1.jsonl"


def at(p):
    return "%s@%s" % (str(p.relative_to(M8)).replace("\\", "/"), hashlib.sha256(p.read_bytes()).hexdigest())


LEDGER = M8 / "ERROR_PATTERN_LEDGER.v1.md"
RULING = EZ / "fable_end_review" / "atlas_hold_ruling.v1.json"
LAND10 = EZ / "merged_close" / "delta_v10" / "landing_manifest.v1.json"
REC10 = EZ / "repair2" / "fixround_v10" / "ezek_fixround_v10_attempt_receipts.jsonl"
DERIVE = EZ / "repair2" / "fixround_v10" / "derive_lane_tools_v10.py"
CLOSE = EZ / "_close_book.py"
TEST = EZ / "_test_close_book_gates.py"
RECEIPT = M8 / "receipts" / "Ezek_completion.json"
BASE = {"schema": "m8_orchestration_learning.v1", "date": "2026-09-23", "book": "Ezek", "supersedes": None}
ROWS = [
    dict(BASE, id="L-0074", stage="fable_ruling", element="fable_call_cost",
         observation=("The one owner-authorized Fable call (OW-30) ruled the eight atlas holds in a single pass and "
                      "returned a standing precedent (P1 release a hold whose row defect is measured absent; P2 a class "
                      "question releases, or drops from the feed a row graded above medium_low; P3 a defect still "
                      "present keeps the hold, re-versions the corpus, and needs two blind lanes to re-check it). It "
                      "measured 65,795 tokens in the notification unit, against an orchestrator estimate of 15-25K "
                      "(E-58). The brief was small; most of the cost was the call's own context and tool loading."),
         recommendation=("Record every Fable ruling's precedent where later books read it, so the same ruling is "
                         "not bought twice (done: memory fable-hold-precedent-ow30). Estimate a Fable call from "
                         "measured Fable calls, not from the size of the brief. Propose to the owner a lean Fable agent "
                         "definition with no tools, a pinned facts file and a fixed output schema."),
         verdict="ADOPTED for the precedent record; PROPOSED for the lean Fable agent definition (owner's decision)",
         metric="1 Fable call, 65,795 notification tokens MEASURED vs 15-25K INFERRED estimate; 8 holds ruled",
         evidence_refs=[at(RULING), at(LEDGER) + " (E-58, OW-30)"]),
    dict(BASE, id="L-0075", stage="v10_delta_lanes", element="lane_cost_vs_estimate",
         observation=("The two blind v10 delta lanes both returned fit_to_assemble and fit_to_close. Both judged all "
                      "eight ruled ids implemented as ruled, and neither found a high or medium residual. They measured "
                      "154,052 and 143,375 tokens in the notification unit (spend 195,173 and 157,614), against an "
                      "INFERRED estimate of 110-130K each taken from the v9 lanes' 134.9K and 134.8K. Lane A exceeded "
                      "the top of the range by 24K. Lane A's own report gave 28 tool calls; its notification counted 27. "
                      "The lane disclosed the discrepancy itself."),
         recommendation=("Forecast a re-check lane from the largest measured sibling lane plus a growth allowance, "
                         "never below the last measured pair. Take usage and tool counts from the runtime's usage "
                         "fields at landing only. A lane's self-report is a claim to check, not a measure."),
         verdict="ADOPTED",
         metric="2 lanes, 297,427 notification tokens MEASURED vs 220-260K INFERRED; 1 self-report off by 1 tool call",
         evidence_refs=[at(LAND10), at(REC10)]),
    dict(BASE, id="L-0076", stage="v10_build", element="text_edit_mechanics",
         observation=("Three text-mechanics faults came up while building v10. (1) An anchor written with LF missed a "
                      "CRLF file; the counted-anchor guard refused, the edit rolled back cleanly, and newline-aware "
                      "anchors fixed it. (2) An escape-bearing Python snippet sent through a shell heredoc was mangled "
                      "again, a repeat of an earlier lesson. (3) Appending to an empty receipts file would have "
                      "started with a stray newline, because the separator test read only 'file does not end in a "
                      "newline'. The derived landing tool now also tests for an empty file."),
         recommendation=("Make anchors newline-aware wherever a file's line endings are not pinned. Write Python "
                         "that carries regexes or escapes with the file tools, never through a shell heredoc. Any "
                         "append helper treats an empty file as needing no separator."),
         verdict="ADOPTED",
         metric="3 faults, 0 bad bytes landed (1 refused and rolled back, 1 caught at a rerun, 1 fixed at derivation)",
         evidence_refs=[at(DERIVE)]),
    dict(BASE, id="L-0077", stage="close", element="ow29_close_sequence",
         observation=("The first dry run showed 122 gates with 0 unmet. The gate test was then updated (53 cases "
                      "PASS), which changed bytes under Ezek/, so that dry preview's retention and receipt digests "
                      "went stale (retention 40fd0561 -> f4cda365, receipt e85ccabc -> 8110b4ff). A second dry run "
                      "with the same arguments showed 0 unmet. --close --acf item22 then wrote a receipt byte-equal to "
                      "the second preview (8110b4ff). After the close, the coverage validator passed 17 closed books "
                      "and failed 9 (Eccl, Ezek, Isa, Jer, Job, Lam, Prov, Ps, Song), each on a missing "
                      "reviews/<book>/review_packets.jsonl (E-57). The failure is on file absence, so the per-book "
                      "rule is never reached for those books."),
         recommendation=("Re-run the dry close immediately before --close whenever anything under the book's folder "
                         "changed after the last dry run: a dry preview binds only the bytes it saw. Run the "
                         "coverage validator at every close, and give the owner the review_packets decision: backfill "
                         "the nine books, or amend the validator's contract for the later mesh."),
         verdict="ADOPTED for the re-dry rule; the review_packets gap is PENDING the owner's decision",
         metric="dry 122/0 twice, close CLOSED (138 chunks, 26/66); coverage validator 17 OK / 9 missing review_packets",
         evidence_refs=[at(CLOSE), at(TEST), at(RECEIPT), at(LEDGER) + " (E-57)"]),
]

pre = LOG.read_bytes()
new = [r for r in ROWS if ('"%s"' % r["id"]).encode() not in pre]
if new:
    sep = b"" if not pre or pre.endswith(b"\n") else b"\n"
    with LOG.open("ab") as fh:
        fh.write(sep + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in new).encode("utf-8"))
    if not LOG.read_bytes().startswith(pre):
        raise SystemExit("INTEGRITY FAILURE: the learning log was not appended to")
print(json.dumps({"appended": [r["id"] for r in new], "skipped": [r["id"] for r in ROWS if r not in new],
                  "total_rows": len([l for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]),
                  "sha256": hashlib.sha256(LOG.read_bytes()).hexdigest()}, indent=1))
