#!/usr/bin/env python3
"""Record the A4 extraction gap, and the lesson about correlated lenses that it teaches.

This is the most important methodological finding of the wave, so it gets a ledger row as well as a queue entry.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
M8 = EZ.parents[1]
HERE = Path(__file__).resolve().parent
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
MD = M8 / "ERROR_PATTERN_LEDGER.v1.md"
JL = M8 / "error_pattern_ledger.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

shutil.copy2(HERE / "a4_extraction_gap.v1.json", EZ / "a4_extraction_gap.v1.json")
g = json.loads((EZ / "a4_extraction_gap.v1.json").read_text(encoding="utf-8"))

entry = {
    "id": "E13-77",
    "severity": "HIGH",
    "headline": "THE A4 CLASS IS INCOMPLETE BY ~53 CITATIONS ON 22 ROWS: my member cannot see a DOTTED "
                "CONTINUATION of a citation list, and neither can the controlling agent's recount - so the "
                "292-for-292 set equality confirmed my code and not my reading of the definition",
    "raised_by": "author lane 03 on P04-001 (it found two); extent MEASURED by the orchestrator",
    "status": "OPEN - the member must be extended, re-run, and a supplementary batch authored",
    "blocks_author_wave": False, "tier": "MEASURED",
    "the_gap": g["the_gap"],
    "measured": {"candidates": g["candidates_total"], "in_a_list_context": g["in_a_list_context"],
                 "already_extracted": g["of_those_already_extracted"],
                 "missed_by_the_member": g["MISSED_BY_THE_MEMBER"],
                 "missed_and_in_window": g["missed_and_in_the_a4_window"],
                 "missed_in_window_and_unmirrored": g["missed_in_window_and_UNMIRRORED"],
                 "rows_affected": len(g["rows_affected"])},
    "THE_LESSON_AND_IT_IS_THE_BIGGEST_OF_THIS_WAVE": (
        "my P2 distinct check matched the controlling agent's independent recount at SET EQUALITY, 292 items "
        "for 292, row by row and verse list by verse list, zero differences. I reported that as strong "
        "evidence, and it was - for the wrong proposition. Both implementations read DEF-A4-ARGUED clause 1's "
        "enumeration of citation FORMS, and that enumeration omits the dotted continuation. Two independently "
        "written implementations of ONE DEFINITION are ONE LENS: they agree exactly because they share the "
        "definition's blind spot, and their agreement measures code fidelity rather than coverage of the "
        "corpus. The decorrelated lens that found this was an author reading the PROSE OF A ROW instead of the "
        "specification. OW-19 says a third lens counts only if DECORRELATED; this is that principle one level "
        "deeper than I had applied it, and I had explicitly called the recount decorrelated."),
    "why_the_reading_that_fixes_it_is_not_a_definitional_change": (
        "clause 1 opens 'Any verse anchor a prose field carries' and then names four forms. The governing "
        "phrase is the first one; the four forms illustrate it. A dotted continuation of a list IS a verse "
        "anchor a prose field carries, and clause 2 already makes a comma/'and' list one citation PER MEMBER - "
        "so a three-verse list is three citations whatever the members' spelling. I am therefore implementing "
        "clause 1's rule rather than extending it, AND routing the reading for confirmation, because an "
        "incomplete Tier-0 gate is red at the close either way and the safer error is to over-disclose the "
        "interpretation."),
    "plan": ["apply the six validated lanes first, since their expected_before values are pinned to the current "
             "digest",
             "extend the member to read a dotted continuation in an OSIS list context; add fixtures for the "
             "three-member list and for the decimal that must NOT match",
             "re-run over the POST-WAVE rows and distinct-check the delta",
             "author a supplementary batch for the affected rows",
             "route the clause-1 reading to the controlling agent with this measurement"],
    "what_i_will_not_do": ("silently widen the pattern and report the A4 class as complete. The 292 figure is "
                           "in a landed record, a ruling relied on it, and the correction has to be as visible "
                           "as the original claim."),
    "artifact": {"file": "Ezek/a4_extraction_gap.v1.json", "sha256": sha(EZ / "a4_extraction_gap.v1.json")},
    "opened_at": NOW,
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

rows = [json.loads(l) for l in JL.read_text(encoding="utf-8").splitlines() if l.strip()]
assert not any(r.get("id") == "E-33" for r in rows), "E-33 already present"
ADD = """
---

## Addendum 2026-09-16 (E-33, session 910cbe15, Ezekiel's author wave) — TWO INDEPENDENT IMPLEMENTATIONS OF ONE DEFINITION ARE ONE LENS: set equality between them measures code fidelity, not coverage

WHAT HAPPENED. A validator member extracted "argued citations" from decision-row prose under a written
definition that enumerated four citation forms. An independent recount, written by a different agent without
sight of the member's source, agreed with it at SET EQUALITY: 292 items against 292, matching row by row, class
by class and verse list by verse list, with zero differences either way. That agreement was recorded as strong
evidence that the class was correctly and completely measured.

It was not. An author agent, reading the actual prose of one row, noticed that
`"oshb:Ezek.20.9, 20.14 and 20.22"` names THREE verses while the member had extracted ONE. The dotted
continuations `20.14` and `20.22` match none of the definition's four enumerated forms. Measured across the
corpus: **53 argued, in-window, unmirrored citations on 22 rows that neither implementation could see** - about
an 18% undercount of the class.

WHY THE TWO IMPLEMENTATIONS AGREED ANYWAY. They were not two lenses on the CORPUS. They were two lenses on the
DEFINITION, and they shared the definition's blind spot. Independent authorship removes correlated bugs; it does
not remove a correlated PREMISE. The stronger the agreement between such implementations, the more confident the
wrong conclusion becomes - 292-for-292 with zero differences reads as near-proof, and its actual content was
"both of us read clause 1 the same way".

THE DISTINCTION THIS FORCES, and it is sharper than "use two lenses":

  * A check that re-derives a figure FROM THE SAME SPECIFICATION tests IMPLEMENTATION FIDELITY.
  * A check that re-derives it FROM THE SOURCE MATERIAL tests COVERAGE.
  * These are different properties and one does not imply the other. A campaign that requires "an independent
    second derivation" without saying which of the two it means will keep buying the first and believing it has
    the second.

WHAT ACTUALLY CAUGHT IT. A reader working through the corpus for a different purpose, whose attention was on the
text rather than on the rule. That is the lens no specification-derived check can replace, and its findings
arrive as a by-product of other work rather than on demand - which is a reason to route author-wave observations
upward rather than treating a repair wave as pure execution.

THE CURE.
  1. When a class is defined by an ENUMERATION of surface forms, the enumeration is a hypothesis about the
     corpus and must be tested against it - by sampling the source for anchors of that class that the
     enumeration does not match. "Which forms exist in the text?" is a different question from "does my code
     implement the listed forms?", and only the second is usually asked.
  2. A definition whose governing phrase is general ("any verse anchor a prose field carries") followed by
     examples should be implemented from the GENERAL phrase, with the examples as tests rather than as the
     specification.
  3. Record what an agreement between two derivations does and does not establish, at the moment of recording
     it. Writing "set equality, zero differences" without naming the shared premise is how a correlated check
     gets filed as a decorrelated one.

GENERALISABLE: any two parsers, extractors, schema validators or migration scripts written from one spec;
any A/B reimplementation used as verification; any "we got the same answer twice" that shares an input contract.
"""
E33 = {
    "id": "E-33", "kind": "error_pattern", "date": "2026-09-16",
    "headline": ("two independent implementations of one definition are ONE lens - set equality between them "
                 "measures implementation fidelity, not coverage of the corpus"),
    "severity": "high",
    "severity_basis": ("a Tier-0 class was measured 18% short (53 citations on 22 rows) and the shortfall was "
                       "reported as confirmed by a zero-difference independent recount; caught by an author "
                       "reading prose, before the close, so no row shipped wrong"),
    "what_happened": ("a member and an independently written recount agreed 292-for-292 at set equality on an "
                      "'argued citation' class; both read a definition enumerating four citation forms; a "
                      "dotted continuation of a citation list matches none of them; 53 in-window unmirrored "
                      "citations on 22 rows were invisible to both"),
    "why_they_agreed": ("independent authorship removes correlated BUGS, not a correlated PREMISE. They were "
                        "two lenses on the definition, not on the corpus, and shared its blind spot."),
    "the_distinction_it_forces": [
        "a check re-deriving a figure FROM THE SAME SPECIFICATION tests IMPLEMENTATION FIDELITY",
        "a check re-deriving it FROM THE SOURCE MATERIAL tests COVERAGE",
        "neither implies the other, and a requirement for 'an independent second derivation' that does not say "
        "which one will keep buying the first while believing it bought the second"],
    "what_caught_it": ("a reader working through the corpus for a different purpose, attending to the text "
                       "rather than the rule - which is a reason to route repair-wave observations upward "
                       "instead of treating a repair wave as pure execution"),
    "cure": ["where a class is defined by an ENUMERATION of surface forms, treat the enumeration as a "
             "hypothesis about the corpus and TEST IT against the source by sampling for anchors the "
             "enumeration does not match",
             "implement a definition from its GENERAL governing phrase, using its examples as tests rather "
             "than as the specification",
             "state what an agreement between two derivations does and does not establish AT THE MOMENT of "
             "recording it; 'set equality, zero differences' without naming the shared premise is how a "
             "correlated check is filed as a decorrelated one"],
    "generalisable": ("any two parsers, extractors, schema validators or migration scripts written from one "
                      "spec; any A/B reimplementation used as verification; any 'we got the same answer twice' "
                      "that shares an input contract"),
    "relation_to_OW_19": ("OW-19 requires a third lens to be DECORRELATED and treats same-family agreement as "
                          "one voice. This extends the test from the lens's FAMILY to its PREMISE: two lenses "
                          "reading one specification are one voice however differently they are built."),
    "recorded_by": "orchestrator (claude-opus-5)", "recorded_at": NOW,
}
md_pre, jl_pre = MD.read_bytes(), JL.read_bytes()
t1 = MD.with_suffix(".md.tmpE33")
t1.write_bytes(md_pre + ADD.encode("utf-8"))
t1.replace(MD)
t2 = JL.with_suffix(".jsonl.tmpE33")
t2.write_bytes(jl_pre + (json.dumps(E33, ensure_ascii=False) + "\n").encode("utf-8"))
t2.replace(JL)

print(json.dumps({"appended": "E13-77", "ledger_row": "E-33",
                  "queue_rows": len(Q.read_text(encoding="utf-8").strip().splitlines()),
                  "ledger_md_lines": len(MD.read_text(encoding="utf-8").splitlines()),
                  "ledger_md_sha256": sha(MD),
                  "ledger_rows": len([l for l in JL.read_text(encoding="utf-8").splitlines() if l.strip()]),
                  "ledger_jsonl_sha256": sha(JL)}, indent=1))
