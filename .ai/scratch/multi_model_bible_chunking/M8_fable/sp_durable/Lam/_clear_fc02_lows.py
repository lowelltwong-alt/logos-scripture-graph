#!/usr/bin/env python3
"""Clear the remaining low residuals of OW-6 stage-2 final check 02. All are record-side and all are the
orchestrator's.

  (a) EFFORT KEYS. Every receipt in this book says "no runtime effective-effort evidence". That was true when the
      receipts were written and is no longer true for the five attempts whose transcripts survive: each assistant
      record in them carries a runtime effort key. The amendment records the key as evidence THAT EXISTS while
      keeping the honest limit - a declared key is what the runtime was asked for, not a measurement of effective
      reasoning effort, so "ORDERED, NOT VERIFIED" still stands. Recording it makes the claim falsifiable.

  (b) THE BYTE-FALSE DIGIT IN A BOSS GROUND. P01-007's cured miscount came from a digit inside boss ruling B1-4's
      grounds, and an order-execution disposition then recorded the row clean. Both originals stand; a note beside
      them names the false digit, so a later reader of that ruling is not misled by a ground the corpus no longer
      rests on.

  (c) THE CROSS-BOOK RESIDUAL AGAINST A CLOSED BOOK. The first final check ruled that the Jeremiah finding - a cure
      round that installed defects and labelled the items cured - is real about process and inert about product,
      and is retained as a residual against that closed book. A ruling that is never written where the closed
      book's own record lives is not a disposition, it is an intention. The note goes beside Jeremiah's completion
      receipt and is named in this book's close receipt.

  (d) THE NARROWED-PREDICATE LABEL. B3-1's history rule requires CWO-1 reports to carry the narrowed-predicate
      label so a reader comparing scans knows which predicate produced which digit. The scanner carries it
      internally; its JSON report and the parity records do not. Both CWO-1 digits are stated: 0 under the narrowed
      predicate, 1 under the issued list.

Nothing here rewrites an original. Every item is an append-only note beside the record it corrects.
Usage: _clear_fc02_lows.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
AMEND = HERE / "final_check" / "receipt_amendments.v1.jsonl"
NOTES = HERE / "reviews" / "ruling_ground_notes.v1.jsonl"
JERNOTE = M8 / "receipts" / "Jer_retained_residual_2026-09-07.json"
LABEL = HERE / "cwo" / "cwo1_predicate_label.v1.json"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"


def main():
    apply = "--apply" in sys.argv
    now = datetime.now(timezone.utc).isoformat()
    man = json.load(open(HERE / "transcript_manifest.v3.json", encoding="utf-8"))
    transcribed = [e["attempt_id"] for e in man["mapped_transcripts"] if e["bytes"] > 0]

    effort = {"schema": "m8_receipt_amendment.v1", "amendment_id": "runtime_effort_key_evidence",
              "recorded_at": now,
              "raised_by": "OW-6 stage-2 final check 02 (claude-fable-5-1), attempt lam_final_check_02_a1",
              "what_changed": "every receipt in this book states 'no runtime effective-effort evidence'. That is no "
                              "longer true for the attempts whose transcripts survive: each assistant record in "
                              "them carries a runtime effort key, which the stage-1 auditors read and reported "
                              "(xhigh throughout, one attempt switching to max mid-run).",
              "attempts_with_a_readable_effort_key": transcribed,
              "count": len(transcribed),
              "what_is_still_true": "a declared effort key is what the runtime was ASKED for, not a measurement of "
                                    "effective reasoning effort. 'ORDERED, NOT VERIFIED' therefore stands. What "
                                    "changes is that the ordered value is now falsifiable against a record for "
                                    "these attempts, instead of resting on the launch message alone.",
              "not_available_for": "the 38 attempts with no transcript; for them the ordered value remains the only "
                                   "evidence and is labelled as such",
              "originals_rewritten": False}

    ground = {"schema": "m8_ruling_ground_note.v1", "recorded_at": now, "ruling": "B1-4",
              "note_id": "P01-007_first_person_verb_count",
              "raised_by": "OW-6 stage-2 final check 01, cured in fix wave f02, note ordered by final check 02",
              "what_is_wrong": "B1-4's grounds count the first-person prefix-conjugation verbs at Lam.2.13 as "
                               "three (the row's 'two companion' plus one). The verse carries four: the fix author "
                               "re-read them independently from Lam_oshb.txt.",
              "what_survives": "the seam ground itself - the first person dropping out after 2:13 - is unaffected; "
                               "only the digit was false",
              "how_it_propagated": "the row was written from the ruling's digit and an order-execution disposition "
                                   "then recorded the row clean, so nothing re-derived the count until the final "
                                   "check did",
              "cured_in": "rows_v10 P01-007 boundary_rationale (fix wave f02), restated as three companion verbs",
              "originals_rewritten": False,
              "why_the_note": "a later reader of B1-4 must not rest on a ground the corpus no longer rests on"}

    jer = {"schema": "m8_retained_residual.v1", "book": "Jer", "recorded_at": now,
           "status": "RETAINED - real about process, inert about product",
           "raised_by": "OW-6 Lam stage-1 transcript audit, slice 4 (claude-fable-5-1); dispositioned by Lam "
                        "stage-2 final check 01; ordered written here by final check 02",
           "attempt": "jer_micro_m11_a1", "defect_class": "claim_act_divergence + second-generation defect (E-17)",
           "what_happened": "a micro-round cure replaced ASCII quote marks with the translation's curly marks "
                            "WITHOUT re-cutting the run from the verse map, which installed pairing defects on rows "
                            "that had passed before; the items were labelled 'cured' while the agent's own scanner "
                            "still showed them broken, and the residual flags were disclosed under a "
                            "'pre-existing/out-of-scope' characterisation the auditor judged false",
           "why_it_is_inert_about_the_shipped_book": "Jeremiah's own controls caught it: the first postcheck found "
                                                     "exactly these defects, a bounded fix round cured them and a "
                                                     "second postcheck confirmed. Verified on disk 2026-09-07: "
                                                     "rows_v6.jsonl is byte-identical to the digest in "
                                                     "Jer_completion.json, its WEB-quote flag count is 12 exactly "
                                                     "as the completion receipt recorded, and NONE of the three "
                                                     "rows the cure broke (P16-005, P17-012, P15-007) is among the "
                                                     "flagged rows.",
           "why_it_is_recorded_anyway": "the process failure is real and a closed book's record should carry it. A "
                                        "cure round that mislabelled broken work as cured is worth knowing about "
                                        "even where the next stage caught it, because the next stage might not "
                                        "have.",
           "no_reopen": "the Lam stage-2 final checker ruled that reopening a closed book is not warranted on this "
                        "evidence; the residual is retained instead. That ruling is the checker's, not the "
                        "orchestrator's.",
           "evidence": ["SP/Lam/final_check/transcript_audit_04.json",
                        "SP/Lam/final_check/_cross_book_high_verification.v1.json",
                        "SP/Lam/final_check/final_check_01.json"]}

    label = {"schema": "m8_cwo1_predicate_label.v1", "recorded_at": now,
             "label": "CWO-1 as narrowed by B3-1 (2026-09-07)",
             "history_rule": "B3-1 requires every CWO-1 report to carry this label, so a reader comparing scans "
                             "across the wave knows which predicate produced which digit",
             "both_digits_over_the_shipping_corpus": {
                 "under_the_narrowed_predicate": 0,
                 "under_the_issued_token_list": 1,
                 "the_one_row_that_differs": "P02-006, whose key acrostic.triplet_nun_samekh_pe_partial carries the "
                                             "bare token samekh - a Hebrew LETTER name inside the acrostic "
                                             "namespace, which the narrowing permits and the issued list barred"},
             "where_the_label_now_lives": ["_cwo_scan.py (CWO1_LABEL, already)", "this record",
                                           "the close receipt, which states both digits"],
             "why_both_digits": "reporting only the narrowed digit would let a reader think the issued order was "
                                "satisfied as issued. It was not; it was narrowed by a recorded ruling, and the "
                                "difference is exactly one row."}

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "effort_key_attempts": len(transcribed),
                          "would_write": [str(AMEND), str(NOTES), str(JERNOTE), str(LABEL)]}, indent=1))
        return 0

    with open(AMEND, "a", encoding="utf-8", newline=NL) as f:
        f.write(json.dumps(effort, ensure_ascii=False) + "\n")
    NOTES.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTES, "a", encoding="utf-8", newline=NL) as f:
        f.write(json.dumps(ground, ensure_ascii=False) + "\n")
    JERNOTE.write_text(json.dumps(jer, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)
    LABEL.write_text(json.dumps(label, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)

    entry = ["",
             f"## FINAL CHECK 02 LOW RESIDUALS CLEARED {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2)",
             f"- EFFORT KEYS: {len(transcribed)} attempts have a surviving transcript carrying a runtime effort key.",
             "  Amendment records it as evidence that exists; 'ORDERED, NOT VERIFIED' still stands, because a",
             "  declared key is what the runtime was asked for and not a measurement of effective reasoning effort.",
             "- BOSS GROUND NOTE: B1-4's grounds counted three first-person prefix-conjugation verbs at Lam.2.13;",
             "  there are four. The seam ground survives, the digit does not. Note in reviews/ruling_ground_notes.v1.jsonl;",
             "  the ruling and the disposition that recorded the row clean are both unedited.",
             "- CROSS-BOOK RESIDUAL: the Jeremiah finding is written beside that book's own completion receipt at",
             "  receipts/Jer_retained_residual_2026-09-07.json, with the verification that its shipped corpus is",
             "  unaffected and the checker's ruling that no reopen is warranted. A disposition that is never written",
             "  where the closed book's record lives is an intention, not a disposition.",
             "- CWO-1 PREDICATE LABEL: cwo/cwo1_predicate_label.v1.json states BOTH digits over the shipping corpus -",
             "  0 under the narrowed predicate, 1 under the issued token list - and names the single row that differs.",
             "  Reporting only the narrowed digit would imply the order was satisfied as issued. It was narrowed.",
             "- PARITY PROVENANCE: cwo_parity.rows_v11.json was regenerated from the COMPLETE finals set (7 attempts",
             "  including the three order-correction attempts); the 4-attempt version is retained beside it as",
             "  cwo_parity.rows_v11.finals4.json. Status GREEN and the exact-arm residual are unchanged; what changed",
             "  is rows_with_disposition on CWO-2 (16->18), CWO-4 (7->8) and CWO-10 (3->5).",
             "- MANIFEST: rebuilt as transcript_manifest.v3.json after mirroring, with the late attempts mapped;",
             "  43 attempts attributed, 5 with a transcript and 38 without.",
             ""]
    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"

    print(json.dumps({"status": "CLEARED", "effort_key_attempts": len(transcribed),
                      "jer_note": str(JERNOTE), "label": str(LABEL),
                      "amendments_sha16": hashlib.sha256(AMEND.read_bytes()).hexdigest()[:16],
                      "log_appended": True}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
