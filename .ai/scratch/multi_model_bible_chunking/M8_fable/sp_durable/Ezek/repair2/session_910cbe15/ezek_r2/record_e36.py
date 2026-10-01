#!/usr/bin/env python3
"""Record E-36 (the vacuous check) and queue entry E13-96 (step 4's mechanical arm, built and distinct-checked).

Written with a file writer and not a shell heredoc, which is itself the point of the lesson below.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CAMP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = CAMP / "sp_durable" / "Ezek"
HERE = Path(__file__).resolve().parent
LJ = CAMP / "error_pattern_ledger.v1.jsonl"
LM = CAMP / "ERROR_PATTERN_LEDGER.v1.md"
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

row = {
    "id": "E-36",
    "kind": "error_pattern",
    "date": "2026-09-16",
    "headline": "a check that made ZERO comparisons reported GREEN: 'no disagreement' was true because nothing "
                "was compared",
    "severity": "high",
    "severity_basis": (
        "nothing shipped - the vacuous green was caught in the same execution. The counterfactual is the "
        "severity: this was the ONLY independent check on 111 mechanical edits to the corpus's evidence "
        "vocabulary, and it was reporting success while inert. A systematic sign error in the sweep it was "
        "built to police would have passed."),
    "the_instance": {
        "what_the_check_was": ("a second, decorrelated reader of the same 111 face qualifiers: one reader "
                               "derives the face from (verse, span) and reads no English; the other reads the "
                               "annotation's own wording and never sees the span"),
        "the_proximate_cause": ("every word-boundary escape in the reader's patterns had been turned into a "
                                "literal BACKSPACE byte (0x08) - 66 of them - by the shell heredoc that wrote "
                                "the patch. No pattern could match anything."),
        "what_it_printed": ("'GREEN - no disagreement between the two readers', with 111 of 111 entries "
                            "classified UNSPOKEN and an AGREE count of zero"),
        "why_the_zero_did_not_look_wrong": ("the reader legitimately reports UNSPOKEN for terse annotations "
                                            "that name no face, and a high UNSPOKEN count was expected. The "
                                            "figure that mattered was AGREE = 0, and the verdict line did not "
                                            "read it."),
        "third_instance": ("this is the third time a word boundary has been lost to a shell heredoc in this "
                           "campaign. The first was invisible in grep output; the second was a trailing "
                           "boundary that was wrong for a different reason. A rule broken three times is not "
                           "a control."),
    },
    "the_two_cures_and_why_both": [
        "PATTERNS ARE NEVER WRITTEN THROUGH A SHELL HEREDOC - they go through a file writer, and where an "
        "escape must survive a transport it is BUILT (chr(92) + 'b') rather than typed. This removes the "
        "proximate cause.",
        "A CHECK THAT CORROBORATED NOTHING CANNOT REPORT A PASS. If the comparison count is zero the verdict "
        "is BROKEN, not GREEN. This is the control that matters, because it catches any future way of "
        "disabling the reader and not merely this one.",
        "FIXTURES GATE THE VERDICT: the reader now runs a selftest first and refuses to compute a verdict if "
        "it cannot match its own examples. A reader that cannot match its fixtures cannot corroborate "
        "anything.",
    ],
    "the_general_shape": (
        "a verification reports the ABSENCE of findings without reporting how many comparisons produced that "
        "absence. Zero findings from zero comparisons and zero findings from a thousand comparisons print the "
        "same sentence. Every check must publish its denominator, and a zero denominator must fail."),
    "sibling_instances_in_this_campaign": [
        "a no-op patch that reported success because nothing asserted the replacement count",
        "an A6 exact-text comparison that reported 66 phantom misses, the mirror image of the same defect",
        "a census harvester that read only `count` keys and silently missed four figures",
        "a slice builder that read a guessed key name, attached nothing, and said nothing",
    ],
    "detection": ("every check publishes the number of comparisons it made beside its verdict, and a verdict "
                  "computed from zero comparisons is a failure by construction"),
    "tier": "MEASURED - the backspace bytes were counted in the file and the selftest reproduces the failure",
    "provenance": {"book": "Ezek", "found_by": "orchestrator (claude-opus-5) at REPAIR-2 step 4 preparation",
                   "found_at": NOW},
}
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")

md = [
    "",
    "## E-36 - the vacuous check: zero comparisons reported as no disagreement",
    "",
    "**The shape.** A verification reports the *absence* of findings without reporting how many comparisons",
    "produced that absence. Zero findings from zero comparisons and zero findings from a thousand comparisons",
    "print the same sentence.",
    "",
    "**The instance.** The mechanical face sweep proposed 111 qualifier edits to the corpus's evidence",
    "vocabulary. Its one independent control was a second, decorrelated reader: reader 1 derives the face from",
    "(verse, span) and reads no English; reader 2 reads the annotation's own wording and never sees the span. The",
    "control printed *\"GREEN - no disagreement between the two readers\"*.",
    "",
    "It had compared nothing. Every word-boundary escape in reader 2's patterns had become a literal BACKSPACE",
    "byte - 66 of them - inserted by the shell heredoc that wrote the patch. No pattern could fire, all 111",
    "entries came back UNSPOKEN, and the AGREE count was zero.",
    "",
    "**Why the zero did not look wrong.** The reader legitimately reports UNSPOKEN for terse annotations that",
    "name no face, and a high UNSPOKEN count was expected. The figure that mattered was AGREE = 0, and the",
    "verdict line never read it.",
    "",
    "**Third instance.** This is the third time a word boundary has been lost to a shell heredoc in this",
    "campaign - once invisible in grep output, once a trailing boundary wrong for a different reason. A rule",
    "broken three times is not a control.",
    "",
    "**Cure - two, because they do different work.**",
    "",
    "1. *Removing the cause:* patterns are never written through a shell heredoc; they go through a file writer,",
    "   and an escape that must survive a transport is **built** (`chr(92) + \"b\"`) rather than typed.",
    "2. *Removing the class:* **a check that corroborated nothing cannot report a pass.** If the comparison",
    "   count is zero the verdict is BROKEN, not GREEN. This catches every future way of disabling the reader,",
    "   not merely this one.",
    "3. *Proving the reader works before trusting it:* fixtures run first and refuse the verdict on failure. A",
    "   reader that cannot match its own examples cannot corroborate anything.",
    "",
    "**After the cure**, the same check reports what it actually did: 88 of 111 qualifiers corroborated by the",
    "independent reader, 0 contradicted, 23 annotations naming no face and therefore corroborating nothing. The",
    "seven \"disagreements\" its first version had reported were its own bug - it read deixis (\"here\", \"at this",
    "verse\") as a near-face claim, when pointing at a verse says nothing about which side of a seam it sits on.",
    "",
    "**Every check publishes its denominator.** A verdict computed from a zero denominator is a failure by",
    "construction.",
    "",
]
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(md))

plan = json.loads((HERE / "face_qualification_plan.v1.json").read_text(encoding="utf-8"))
chk = json.loads((HERE / "face_distinct_check.v1.json").read_text(encoding="utf-8"))
entry = {
    "id": "E13-96", "opened_at": NOW, "severity": "MEDIUM",
    "headline": ("REPAIR-2 STEP 4's MECHANICAL ARM IS BUILT AND DISTINCT-CHECKED, held for application until "
                 "step 2 lands. 111 face qualifiers derivable, 0 undecidable faces, and a decorrelated second "
                 "reader corroborates 88 with 0 contradictions. New ledger class E-36 - the check reported "
                 "GREEN while comparing nothing."),
    "raised_by": "orchestrator (claude-opus-5)", "status": "BUILT, not applied", "blocks_close": False,
    "tier": "MEASURED",
    "the_order": ("#e15 Q5 clause 6 v2 retro_qualification: every WARRANT-onset and WARRANT-close token this "
                  "wave installed receives its derived face qualifier by a mechanical sweep, distinct-checked; "
                  "pre-wave descriptive entries are not re-tokenised"),
    "what_the_dry_run_found": {
        "warrant_onset_tokens": plan["tally"].get("WARRANT-onset_total"),
        "warrant_close_tokens": plan["tally"].get("WARRANT-close_total"),
        "derivable_now": len(plan["derivable_now"]),
        "by_face": {k: v for k, v in plan["tally"].items() if k.startswith("derived")},
        "routed_to_the_author_batch_because_of_the_zone": len(plan["routed_to_the_author_batch_zone"]),
        "refused_needs_an_author": len(plan["refused_needs_an_author"]),
        "failed_loud_no_face_derivable": plan["tally"].get("FAILED_LOUD_no_face_derivable", 0),
        "what_the_zero_means": ("every wave-installed onset/close token outside the zone sits on a derivable "
                                "face - the seam verse, the verse across the seam, or an in-span verse whose "
                                "annotation names a device. No token needed a face the geometry could not "
                                "give, which is evidence the wave's installs were geometrically coherent."),
        "the_two_refusals": [x["why"][:150] for x in plan["refused_needs_an_author"]],
    },
    "the_zone_is_excluded_by_name_not_by_arithmetic": (
        "WEB and MT do not number Ezekiel alike: the offset map records the five verses WEB prints as 20:45-49 "
        "as MT 21:1-5, and MT 21:6-37 as WEB 21:1-32, equal totals at 1273 - a shift, not a gap. Its tier-0 "
        "clause requires an explicit dual or numeric qualifier for any ref touching WEB 20:45-49, WEB ch 21 or "
        "MT ch 21, and #e15 makes the mechanical sweep valid only outside the zone. Everything touching it is "
        "routed to authors and nothing is computed. The verse counts come from their carrier, which obliges a "
        "consumer to assert the face it expects - this sweep asserts WEB and refuses if the carrier says "
        "otherwise."),
    "the_distinct_check": {
        "design": chk["the_two_readers"],
        "selftest": "14 fixtures, 0 failed",
        "result": chk["summary"], "verdict": chk["verdict"],
    },
    "two_defects_in_my_own_check_found_before_it_was_trusted": chk["two_corrections_to_this_reader_disclosed"],
    "ledger": {"new_class": "E-36"},
    "artifacts": {"plan": "scratchpad/ezek_r2/face_qualification_plan.v1.json",
                  "plan_sha256": sha(HERE / "face_qualification_plan.v1.json"),
                  "check": "scratchpad/ezek_r2/face_distinct_check.v1.json",
                  "check_sha256": sha(HERE / "face_distinct_check.v1.json")},
    "why_it_is_held": ("two blind author lanes are writing step 2's ground prose against the rows at "
                       "1238eb24...; mutating the same rows underneath them would invalidate their gate runs, "
                       "which is the mistake already recorded as E13-81. The sweep applies after step 2 lands."),
}
entry["ledger"]["jsonl_rows_after"] = len([1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip()])
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(json.dumps({"ledger_jsonl_rows": entry["ledger"]["jsonl_rows_after"],
                  "ledger_md_lines": len(LM.read_text(encoding="utf-8").splitlines()),
                  "queue_rows": len([1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()])},
                 indent=1))
