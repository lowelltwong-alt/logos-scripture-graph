#!/usr/bin/env python3
"""Record lanes 02 and 05, and own the brief defect lane 05 caught."""
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


add(id="E13-74",
    severity="HIGH",
    headline="MY OWN BRIEF SECTION 12 COLLAPSED THE EXACT DISTINCTION I HAD CRITICISED A RULING FOR COLLAPSING, "
             "one message after criticising it. Lane 05 caught it and correctly preferred the ruled order to my "
             "brief.",
    raised_by="author lane 05 (claude-opus-5 subagent); owned by the orchestrator",
    status="OPEN - the brief must be corrected before another author agent reads it",
    blocks_author_wave=False, tier="MEASURED",
    what_i_wrote_in_the_brief=("'MT 33:20's sof pasuq is UNAVAILABLE at verse granularity and no row is scored "
                               "on it. Do not resolve it, do not assert it either way, and do not treat the "
                               "strategy's mention as a measurement.'"),
    what_i_had_recorded_minutes_earlier=("queue E13-67, from P6's measurement: pmarks NAMES MT 33:20 explicitly "
                                         "at arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses.verse "
                                         "with a finding and a status. What is UNAVAILABLE is INDEPENDENT "
                                         "VERIFICATION - the only pinned witness carries no sof pasuq anywhere "
                                         "- not the NAME. I wrote in that same entry that '#e13's wording "
                                         "collapses that distinction'."),
    what_i_then_did=("collapsed it myself. My brief says the FACT is unavailable and forbids asserting it, when "
                     "the name is MEASURED and only its verification is unavailable. A ruled item in lane 05's "
                     "worklist orders the opposite of my brief, so the lane was handed a direct contradiction "
                     "between its controlling instruction and its work order."),
    what_the_lane_did_right=("carried the RULED ORDER, cited the pmarks key, and told me to fix section 12 "
                             "before the next author agent hits it. It preferred the ruling to the brief, which "
                             "is the correct precedence, and it did not silently resolve the contradiction."),
    why_this_is_worth_a_HIGH=("not because a row is wrong - none is - but because it is the E-31 family again "
                              "in a new place: I authored the criticism and then committed the thing criticised. "
                              "An UNAVAILABLE that is really an UNVERIFIED is a half-truth in the strongest "
                              "sense OW-18 means it, because it forbids exactly the assertion the evidence "
                              "supports."),
    the_fix=("section 12 will read: the NAME is MEASURED in pmarks; INDEPENDENT VERIFICATION is UNAVAILABLE "
             "because the pinned witness carries no sof pasuq anywhere; no row is scored on it; cite the pmarks "
             "key when the order requires the fact and never present the strategy's mention as a measurement."))

add(id="E13-75",
    headline="AUTHOR LANES 02 AND 05 ARE VALIDATED: parity EXACT on both, 133 edits, 0 protected-field edits, "
             "every sweep validating in order",
    raised_by="orchestrator (claude-opus-5)", status="DONE", blocks_author_wave=False, tier="MEASURED",
    lane_02={"edits": 70, "items": "83/83, zero drops",
             "by_sweep": {"a4": 43, "a6": 15, "grounds": 9, "vocab": 2, "confidence": 1}, "escalations": 8,
             "deliverable_sha256": "2e2215e2ddd63c2a68e3c951ba8ea0c65a946ba9307741a1c6197f8b29daa630"},
    lane_05={"edits": 63, "items": "83/83 - 70 with edits, 13 NOT discharged each with a named disposition",
             "by_sweep": {"a4": 37, "a6": 12, "confidence": 6, "grounds": 5, "disclosures": 3},
             "escalations": 5,
             "deliverable_sha256": "fd8ad6330bf8ec34f8891213b8437dec7ddf5c73f60c65124e9ebd1151513a3a"},
    the_finding_i_value_most_from_lane_02=(
        "IT TREATED ITS OWN READER AS THE FIRST SUSPECT. Its opening quotation pass returned ZERO hits for "
        "three INSTALL runs, which looks exactly like three unsupported orders. The cause was its own "
        "normaliser keeping apostrophes as word characters, in verses that open a nested quotation. It fixed "
        "the reader and all three then measure exactly one hit at exactly the cited verse. In its words: 'the "
        "correct response was to fix the reader, not to report three claims unsupported.' That is the same "
        "failure my own C1 reader made against pmarks, reached independently and handled correctly."),
    lane_02_other_findings=[
        "FOUR translation misquotations corrected against the cited verse's own wording. The sharpest: two rows "
        "attributed a five-word refrain to a verse where the ENGLISH run stands at ONE verse only, while the "
        "HEBREW refrain stands at all five the rows list. It fixed the English attribution and PRESERVED the "
        "row's five-verse list, because the list is correct in Hebrew. A cruder repair would have deleted a "
        "true claim to fix a false one.",
        "ONE MARK WAS WRITTEN UP BACKWARDS: a row read the mark on MT 14:1 as corroborating itself, but a mark "
        "is recorded ON the verse it FOLLOWS, so it corroborates the RIVAL cut. Re-disclosed for the "
        "alternative it corroborates - which is the PRECEDENCE rule's own direction clause, applied without "
        "being pointed at it.",
        "IT RAN THE DUPLICATE-NGRAM GATE AGAINST ITSELF: 22 colliding seven-gram pairs in its first draft, "
        "rotated down to 2 - and the surviving 2 ARE the mandated quotation plus its reference, which cannot be "
        "rotated without falsifying a quotation. Reported rather than mangled.",
        "FOUR defects outside its worklist, evidenced and not written: a paseq implied where pmarks has a "
        "samekh; a distinctness claim measured false against a 15-verse stem; a device_notes figure stale "
        "against inventory v2; a superseded description still standing in a field this wave does not re-tokenise.",
        "it checked whether the ch 20/21 dual-writing rule applied to its rows and found it does not - CHECKED, "
        "not assumed, with the offset map's identity statement named",
    ],
    lane_05_other_findings=[
        "ALL THREE of its boss-return reproductions reproduce INDEPENDENTLY of mine - the anomaly record, the "
        "separator counts, and the exact codepoint difference. That is a decorrelated confirmation of my own C1 "
        "work, which I could not have supplied myself.",
        "TWO MEASURABLY FALSE CLAIMS left in place at P08-007 because they are not in its worklist: the row "
        "says two K/Q notes have their separators stripped, and both carry ZERO separators in pmarks. Same "
        "defect class as an ordered correction elsewhere, so it likely recurs. Exact corrective wording is in "
        "the escalation.",
        "ONE OF MY OWN A6_UNION ITEMS IS UNEXECUTABLE: the peer-named run is absent from all four fields of the "
        "row, so there is nothing to delimit. It does occur once in the translation, in span. This is the "
        "honest outcome of building that class from a superset - the item had nothing to do, and the lane said "
        "so rather than inventing work.",
        "two of its own detectors produced FALSE NEGATIVES which it caught and corrected before either reached "
        "the deliverable - apostrophe tokenisation, and partial diacritic stripping returning 0 for a genuine "
        "18-verse run",
        "its own seven-gram scan found 16 duplicates in its first draft and it reworded until zero remained",
        "it labelled two input digests TRANSCRIBED from the launch table rather than MEASURED, because it never "
        "opened those two files - an unprompted OW-18 distinction most agents would have glossed",
    ])

add(id="E13-76",
    severity="MEDIUM",
    headline="A DESIGN CONSEQUENCE THREE LANES HIT INDEPENDENTLY: one field can carry work from two different "
             "sweeps, so a few edits pool an A6 component into an A4-labelled edit and the per-sweep parity "
             "digits attribute them to one sweep",
    raised_by="author lanes 02, 05 and 06, each unprompted", status="OPEN - recorded; affects parity reporting, "
                                                                    "not correctness",
    blocks_author_wave=False, tier="MEASURED",
    the_mechanism=("authors work by ROW because judgement needs the whole row, and the orchestrator applies by "
                   "SWEEP because #e13 orders the sweeps and E-18 wants parity digits per sweep. When a "
                   "citation install and a quotation repair land on the SAME field of the same row, they cannot "
                   "be two independent edits: a later whole-field set cannot survive an earlier append, and an "
                   "append cannot carry the repair. So the lane emits ONE edit doing both."),
    measured={"lane_02": "1 edit (P01-013), labelled a4, carrying one a6 component",
              "lane_05": "3 edits pooling an a6 item into an a4 or grounds edit",
              "lane_06": "2 edits (P10-012, P10-013), set-on-refs rather than appends"},
    why_it_is_not_a_correctness_problem=("the final text is the same either way, every such edit names its "
                                         "expected_before exactly, and all three lanes' plans validate in sweep "
                                         "order under simulation. What is affected is the ATTRIBUTION in the "
                                         "per-sweep parity digits: six edits do work belonging to two sweeps "
                                         "and are counted under one."),
    what_i_will_do=("report the pooling explicitly in each sweep's receipt, naming the edits that carry a "
                    "second sweep's component, so the parity digits are not read as a clean per-class count "
                    "when they are not. All three lanes offered to separate them if I would rather re-pool; I "
                    "will not, because splitting them would require an edit whose expected_before cannot be "
                    "stated until the other has been applied - which is strictly more fragile."),
    for_daniel=("the sweep unit should be (sweep, field) rather than sweep, or the deliverable schema should "
                "let one edit declare several sweep components. Three independent lanes hitting this in one "
                "wave makes it a design flaw and not an accident."))

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"appended": [e["id"] for e in E], "queue_rows": len(rows),
                  "open_for_the_controlling_agent": [r["id"] for r in rows
                                                     if "needs the controlling agent" in str(r.get("status"))],
                  "queue_sha256": hashlib.sha256(Q.read_bytes()).hexdigest()}, indent=1))
