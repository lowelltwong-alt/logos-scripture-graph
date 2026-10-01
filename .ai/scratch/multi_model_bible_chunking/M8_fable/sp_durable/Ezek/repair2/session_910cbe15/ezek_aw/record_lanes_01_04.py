#!/usr/bin/env python3
"""Record lanes 01 and 04 as validated, route their findings, and own the two defects that are mine."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
E = []


def add(**kw):
    E.append(dict(kw, opened_at=NOW))


add(id="E13-70",
    severity="HIGH",
    headline="FOR THE CONTROLLING AGENT: the boss audit's MARKS_3D items give the WRONG MARK CLASS on both of "
             "them - it calls MT 22:31 and MT 24:14 closed-section where pmarks records PE, petuchah, OPEN",
    raised_by="author lane 04 (claude-opus-5 subagent), measured against pmarks; recorded by the orchestrator",
    status="OPEN - needs the controlling agent",
    blocks_author_wave=False, tier="MEASURED",
    what_the_audit_said="both MARKS_3D work orders describe the mark as a closed-section mark (samekh)",
    what_pmarks_records="[\"PE\"] at MT 22:31 and [\"PE\"] at MT 24:14 - petuchah, an OPEN section mark",
    what_reproduces="the mark's EXISTENCE and its onset-seam DIRECTION reproduce exactly on both rows. Only the "
                    "CLASS is wrong.",
    independent_corroboration=("row P05-007, written before this wave and by a different agent, already calls "
                               "the MT 24:14 mark a pe. So the rows' own prose disagrees with the audit's "
                               "label, which is how the lane came to check it."),
    why_it_is_reported_as_a_PATTERN_not_a_slip=("two independent items carry the same wrong class, which points "
                                               "at the audit's mark-class FIELD rather than at a typo in one "
                                               "order. A single wrong label is a slip; the same wrong label "
                                               "twice is a mechanism."),
    what_the_lane_did="corrected the class in the row it was repairing and escalated the pattern rather than "
                      "silently fixing two orders and moving on",
    why_it_matters_beyond_these_two=("PE and SAMEKH are never to be conflated in this campaign - the contract "
                                     "makes parashah marks weak single-witness corroboration and forbids "
                                     "treating one as the other. If the audit's mark-class field is wrong in "
                                     "general, other orders built on it may carry the same error."))

add(id="E13-71",
    headline="AUTHOR LANES 01 AND 04 ARE VALIDATED: digest parity EXACT on both, 0 edits touching a protected "
             "field, every ROLE token well-formed, and every sweep validates in the ruling's order",
    raised_by="orchestrator (claude-opus-5)",
    status="DONE", blocks_author_wave=False, tier="MEASURED",
    lane_01={"edits": 63, "items_in_the_order": 84, "accounted_for": 91, "not_discharged": 0,
             "by_sweep": {"grounds": 3, "a4": 48, "a6": 12}, "escalations": 5,
             "deliverable_sha256": "34ed205eac2ef8f06e063eddbc707e5486855179dff84ec687ff8b10156773d5"},
    lane_04={"edits": 82, "items_in_the_order": 85, "not_discharged": 0,
             "by_sweep": {"confidence": 2, "grounds": 6, "marks": 2, "a4": 66, "a6": 6}, "escalations": 5,
             "deliverable_sha256": "2378ecf952b6492b49c39713f360e5f49a5f39e95cfedd47275fe4a4c572af5a"},
    the_finding_i_value_most_from_lane_01=(
        "TWO OF THE ROW'S GLOSSES WERE PARAPHRASES, NOT QUOTATIONS. The row had 'and you, son of man, hear' "
        "where the translation reads 'But', and 'a hand stretched out to me' where it reads 'was stretched "
        "out'. Delimiting those as quotations - which is what the item literally ordered - would have "
        "MANUFACTURED A FALSE QUOTATION: a claim that the translation says something it does not. The lane "
        "corrected the wording to the translation's before delimiting, and ruled a third run exempt because it "
        "is not a run of the translation at all. An install order carried out literally can create a falsehood; "
        "that is worth more than the 27 items it discharged correctly."),
    the_finding_i_value_most_from_lane_04=(
        "it added THREE refs entries beyond its 63 citation items, to mirror in-window anchors that ITS OWN "
        "ORDERED REWRITES introduced - 'otherwise the repair would have created fresh unmirrored citations'. "
        "Repairing a ground can introduce a new argued citation, and a wave that only installs the citations "
        "measured BEFORE the repair leaves the gate red afterwards. No order told it to think of that."),
    other_findings_routed=[
        "lane 01: the false ground at P01-009 was false THREE times over, not once - three of the five interior "
        "marks stand before verses that ARE members of the messenger class and carry the formula "
        "verse-initially. The replacement ground is one that holds.",
        "lane 01: the order said 'four interior marks'; the lane found FIVE and wrote all five rather than "
        "guess which four were meant.",
        "lane 04: P06-009 quoted the WRONG VERSE'S English as its own close - the phrase occurs book-wide at "
        "exactly one verse, outside the span. In the CONSONANTAL Hebrew the two verses do end identically, "
        "differing only in pointing (2fs against 2ms), which is why a related claim was NARROWED to the Hebrew "
        "rather than struck.",
        "lane 04: three of the audit's A6 attachment lists are INCOMPLETE, which changed two judgements - an "
        "in-span occurrence exists where the attachment said the runs were all outside the span. An incomplete "
        "premise and a false one need different responses and it reported them as such.",
        "lane 04: strategy section 7 line 409 says 'four messenger paragraphs (30:2, 30:10, 30:13)' - the COUNT "
        "four is byte-correct but its own LIST omits 30:6. Scored no row.",
        "lane 04: four seam or tiling divergences from strategy section 7, escalated and not acted on, "
        "including a ch-28 cut site where the MARKS FAVOUR THE ROWS over the strategy's named sites.",
    ])

add(id="E13-72",
    severity="MEDIUM",
    headline="TWO DEFECTS IN MY OWN WAVE DESIGN, both found by the lanes: the worklist carries NO STABLE ITEM "
             "IDS, and the rotation rule sets a floor that is structurally unreachable for small classes",
    raised_by="author lanes 01 and 04; owned by the orchestrator",
    status="OPEN - fixed for Daniel; worked around for this wave", blocks_author_wave=False, tier="MEASURED",
    defect_1_no_item_ids={
        "what": ("author_wave_worklist.v4.json's items carry no id field. Lane 01 minted 'l01#NN' from the "
                 "array index and supplied an item_identification block mapping every id to its (row, class, "
                 "field, citation/run) tuple; lane 04 did likewise. Both told me to remap through their block "
                 "rather than through their index."),
        "why_it_matters": ("an item's identity is how a wave proves it discharged what was ordered. Without a "
                           "stable id the proof is a count, and a count cannot tell WHICH item was dropped. "
                           "Each lane inventing its own scheme also means six incompatible id spaces."),
        "why_the_lanes_handled_it_well": "both volunteered a mapping block unprompted rather than leaving me to "
                                         "guess at their indices",
        "fix_now": "the accounting check compares COUNTS against the order and uses each lane's mapping block "
                   "for the per-item trace",
        "fix_for_daniel": "every worklist item carries a stable id assigned by the builder, and the deliverable "
                          "schema requires it",
    },
    defect_2_unreachable_rotation_floor={
        "what": ("my brief requires at least 4 distinct formulations per annotation type. Lane 04 reported that "
                 "this is UNREACHABLE for two of its token classes because its worklist carries only 3 "
                 "citations of each. It stated that plainly instead of padding to four or quietly missing the "
                 "floor."),
        "why_it_matters": ("a floor that cannot be met invites exactly the two bad responses - invent a fourth "
                           "formulation nobody needs, or fail silently. Either is worse than the rule's "
                           "absence."),
        "the_rule_i_should_have_written": "at least 4 distinct formulations where the class has 4 or more "
                                          "items; otherwise every formulation distinct. The purpose is to "
                                          "defeat the duplicate-ngram gate, and 3 distinct formulations over 3 "
                                          "items already does that.",
        "measured_compliance_despite_it": "every annotation in both lanes is distinct and within six words",
    })

add(id="E13-73",
    severity="LOW",
    headline="A JUDGEMENT CALL I AM MAKING AND DISCLOSING: lane 04 delimited a translation run inside a GENRE "
             "LABEL field, and flagged it for me. The edit stands; whether label fields should be exempt is a "
             "METHOD question, not a row question.",
    raised_by="author lane 04, which asked rather than assumed", status="DECIDED", blocks_author_wave=False,
    the_edit="literature_type_guess becomes: qinah \"over the king of Tyre\" (web:Ezek.28.12, WEB)",
    the_lanes_objection=("the field is a genre label, not argued prose, and it executed only because the item "
                         "is marked INSTALL rather than AUTHOR_JUDGEMENT and the formula exemption does not "
                         "reach the run"),
    my_decision=("KEEP IT. The quotation convention as ruled covers any field carrying a run of five or more "
                 "words identical to the translation; it carves out formula renderings, not label fields. "
                 "Applying it here is the rule, and an undelimited translation run in a label is the very "
                 "thing the convention exists to surface. Reverting it would be me narrowing a ruled "
                 "convention on my own taste."),
    what_i_am_routing_instead=("whether the convention SHOULD exempt label-type fields is a change to the "
                               "method, and it goes to the once-per-book method-change proposal loop with this "
                               "instance as its evidence. That is the honest place for it."),
    tier="the edit is MEASURED against the translation; the decision is mine and is disclosed as a decision")

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"appended": [e["id"] for e in E], "queue_rows": len(rows),
                  "open_for_the_controlling_agent": [r["id"] for r in rows
                                                     if "needs the controlling agent" in str(r.get("status"))],
                  "queue_sha256": hashlib.sha256(Q.read_bytes()).hexdigest()}, indent=1))
