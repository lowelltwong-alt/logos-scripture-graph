#!/usr/bin/env python3
"""Queue E13-114 and ledger rows E-42/E-43: the final remediation is applied and the book is hard GREEN."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
M8 = EZ.parent.parent
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
LED = M8 / "error_pattern_ledger.v1.jsonl"
LEDMD = M8 / "ERROR_PATTERN_LEDGER.v1.md"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
qpre = Q.read_bytes()
if not any(json.loads(l).get("id") == "E13-114" for l in qpre.decode("utf-8").splitlines() if l.strip()):
    e = {"id": "E13-114", "opened_at": NOW, "severity": "HIGH", "tier": "MEASURED", "blocks_close": True,
         "raised_by": "orchestrator (claude-opus-5)",
         "status": "DONE: REPAIR-2's final remediation is applied; the book is HARD GREEN. The close-gate items remain.",
         "headline": ("The final remediation landed in six slices, each two blind Opus lanes reconciled by a Fable adjudicator "
                      "(OW-13, OW-19): 18 executions, 543 owed items, 126 rows changed. Merged (348/348 fields), then the K3 "
                      "grade caps (7/7) and the measured signals sweep with one role-token repair (5/5). The whole suite now "
                      "reads HARD GREEN: citation_sweep, role_tokens, mark_symmetry, web_quotes, refs_mirror, language_zones, "
                      "ngram7, cap_sweep and register all GREEN; universals (triage, never a close criterion) stands at 804."),
         "chain": {"before_the_batch": "03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554",
                   "merged_remediation": "6e329bf1254fc8b1d363c40b78479d63227f7fb5b80552e05ea9d48c07d2745b",
                   "k3_grade_caps": "f4aab0c78ec71f2ef943b3a2f65aa5e79d7ac2c48c50595e4501c5f286d9eeef",
                   "signals_and_token_fix": "e24048cc869f1493ac5d65a7e37fd6457909d2848da31583e9d55211601611a7"},
         "completion_measure": {"register_flags_book_wide": 0, "web_quotes": 0, "mark_symmetry": 0, "role_tokens": 0,
                                "citation_sweep_problems": 0, "universals_triage": 804},
         "k3_caps_applied": ["P01-012", "P03-009", "P06-002", "P06-004", "P07-004", "P07-009", "P09-002"],
         "signals_removed_after_measurement": {"P03-003": ["wordevent.strict_onset"], "P03-004": ["wordevent.strict_onset"],
                                               "P03-005": ["wordevent.strict_onset", "oath.as_i_live"],
                                               "P03-021": ["closure.formula_final", "oath.as_i_live"],
                                               "how": "each measured on the witness skeleton by the orchestrator before removal; none was removed on report alone"},
         "what_the_reviews_caught_that_no_flag_list_held": [
             "a Hebrew splice byte-perfect but from the wrong clause of 8:18 (the eye-and-pity clause where the sentence claimed the loud-voice clause)",
             "a quotation for 35:12 that was not the WEB's wording at all",
             "both lanes agreeing that 8:18 'ends' on a clause that is words 9-12 of 16",
             "an order mis-targeted at the wrong row (40:38, true at P10-005, ordered on P01-002)",
             "a category enum still standing in P06-001's device notes",
             "#e17's own required tokens placing a samekh on the verse AFTER the mark at 16:51, 17:19, 18:24, 18:27, 21:11 and 46:20"],
         "open_at_this_point": {"grade_questions": ["F-414 (P03-001): both seams two-faced, no statable ground for the lower grade; routed with faces"],
                                "routed_class_questions": ["R-1 the 40:38 order's row id", "R-2 the 27:10/27:11 one-verse slip",
                                                           "R-3 the 27:36 far-face token class question", "the plan's 40:28 self-contradiction (K7)"],
                                "note": "each is recorded for the close packet; none blocks the suite"},
         "cost_measured": {"final_batch_receipts": 18, "tokens": 8484979}}
    with Q.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    assert Q.read_bytes().startswith(qpre)

lpre = LED.read_bytes()
rows = []
if b'"E-42"' not in lpre:
    rows.append({"id": "E-42", "at": NOW, "kind": "orchestrator_defect", "severity": "HIGH (near miss; contained by the review layer)",
                 "what": ("The witness extract the orchestrator built for each slice looked up a verse's apparatus by its MT key and "
                          "FELL BACK to its WEB key when the MT key held nothing. Outside the chapter 20-21 zone the two keys are the "
                          "same and nothing moved; inside it, WEB 21:3 (= MT 21:8, which has no paseq) picked up the paseq recorded at "
                          "MT 21:3 (= WEB 20:47). Two blind lanes then disclosed a paseq that does not exist."),
                 "how_it_was_caught": ("the slice-5 Fable adjudicator measured the claim against the pinned marks file, refused to carry "
                                       "it, and routed the mis-mapping to the orchestrator - the defect never reached the corpus"),
                 "counterfactual": ("had both lanes agreed and the adjudicator trusted them, a false apparatus claim would have shipped in "
                                    "the scholar-facing record; the blast radius is every zone row of every future book that uses the "
                                    "extract pattern"),
                 "cure": ("(1) build_slice_extract.py now looks up marks, paseq and K/Q by the MT key ONLY, with the reason written at the "
                          "line; (2) verify_zone_apparatus_claims.py re-measures every apparatus claim on a zone row in the landed "
                          "proposals before a merge is applied (run: 35 claims checked, the false one absent, the rest true on the face "
                          "each names); (3) an extract that derives a second numbering carries the derivation, never a fallback")})
if b'"E-43"' not in lpre:
    rows.append({"id": "E-43", "at": NOW, "kind": "member_false_positive", "severity": "LOW",
                 "what": ("check_register.py's schema_vocabulary arm - which exists to catch the rows' own schema words used as words in "
                          "PROSE - was applied to observed_substrate_signals, whose elements are schema tokens by construction. Three "
                          "flags stood on P07-003 and P07-004 for 'utterance.mid_unit' and 'recognition.mid_unit' with nothing wrong in "
                          "either row, and they were the last register flags in the book."),
                 "cure": ("the arm is excluded on that field only; every other arm still applies there, so a signals element naming a file, "
                          "a rule or another row is still a defect. A selftest vector proves the exemption (53 vectors GREEN), and the "
                          "member now reads 0 on the live rows."),
                 "lesson_for_the_method_record": "a register rule written for prose is not automatically true of a structured field; scope each arm to the field class it was written for"})
if rows:
    with LED.open("a", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    assert LED.read_bytes().startswith(lpre)
    md = LEDMD.read_bytes()
    add = ("\n\n## E-42 (2026-09-21) - AN EXTRACT THAT FELL BACK TO THE OTHER NUMBERING\n\n"
           "The per-slice witness extract looked up a verse's apparatus by its MT key and fell back to its WEB key when the MT key held "
           "nothing. Outside the chapter 20-21 zone the keys are identical, so the bug was invisible; inside it, WEB 21:3 (= MT 21:8, no "
           "paseq) picked up the paseq recorded at MT 21:3 (= WEB 20:47). Two blind lanes disclosed a paseq that does not exist. **The "
           "slice-5 adjudicator measured it against the pinned marks file, refused to carry it, and routed the mis-mapping back.** The "
           "defect never reached the corpus - the layered review caught it, not luck. Cure: the MT key is now the only key, with the "
           "reason written at the line; a verifier re-measures every apparatus claim on a zone row before a merge is applied; and an "
           "extract that derives a second numbering carries the derivation rather than a fallback.\n\n"
           "## E-43 (2026-09-21) - A PROSE RULE APPLIED TO A STRUCTURED FIELD\n\n"
           "The register member's schema-vocabulary arm, written to catch schema words used as words in prose, was applied to "
           "`observed_substrate_signals`, whose elements are schema tokens by construction. It flagged 'utterance.mid_unit' and "
           "'recognition.mid_unit' on two rows that had nothing wrong with them - the last three register flags in the book. The arm is "
           "now excluded on that field only, with a selftest vector proving it; every other arm still applies there. Lesson for the method "
           "record: **scope each arm to the field class it was written for** - a rule true of prose is not automatically true of a "
           "structured field.\n")
    with LEDMD.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(add)
    assert LEDMD.read_bytes().startswith(md)
print(json.dumps({"queue_rows": sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()),
                  "ledger_rows_added": [r["id"] for r in rows]}, indent=1))
