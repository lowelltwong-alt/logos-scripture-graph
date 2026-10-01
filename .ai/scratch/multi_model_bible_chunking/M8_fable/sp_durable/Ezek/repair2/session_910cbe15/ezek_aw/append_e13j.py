#!/usr/bin/env python3
"""Record what precondition P2 measured, and the interpretation question it raises that the orchestrator must not
resolve. Also records P1, P7 and P8 as executed."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
pre = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
E = []


def add(**kw):
    E.append(dict(kw, opened_at=NOW, raised_by="orchestrator (claude-opus-5)", status="OPEN"))


add(id="E13-57",
    severity="HIGH",
    headline="P2 IS DONE AND IT RAISES THE ONE QUESTION THAT DECIDES THE AUTHOR WAVE'S SIZE: the fixed member "
            "reports 444 in-span verses where the peers hand-named about 47",
    source="orchestrator, executing precondition P2",
    what_was_done=("R1's four changes are applied and the member has been run once. own_span is no longer "
                   "subtracted, the window contains the span plus both seam verses, a range counts as one "
                   "citation, the tool asserts the declared numbering face at startup, and a boundary at the "
                   "book's edge is REPORTED rather than collapsing the window. Selftest 10 of 10, including "
                   "regressions for both book edges and for an unresolvable span."),
    measured={"rows_checked": 145, "flags": 128,
              "in_span_argued_but_unmirrored_verses": 444,
              "rows_carrying_an_in_span_verse": 100,
              "at_seam_verses": 131,
              "far_side_verses_discharged": 817,
              "before_the_fix": "115 flags, 0 in-span verses visible - the class was invisible by construction"},
    the_question=("R1 sets the worklist as 'fixed member UNION the peers' hand-named in-window verses (47 verses "
                  "across five groups plus P03-016, P11-013)'. The fixed member now yields 444 in-span verses on "
                  "100 rows. The union is therefore about 444, not about 47 - a tenfold difference in how many "
                  "references the author wave installs."),
    why_the_orchestrator_will_not_pick=("the gap is not a defect in either number; it is the difference between "
                                        "'argued' and 'argued AS EVIDENCE'. peer_11 named it exactly: its A4 "
                                        "argues-test could not separate an evidentiary mention from a narrative "
                                        "one, so it filed conservatively and referred the scope upward. The "
                                        "member has no such judgement - an in-span verse a row merely discusses "
                                        "reads the same to it as one the row's warrant rests on. Choosing 444 "
                                        "would install hundreds of references for narrative mentions; choosing "
                                        "47 would discard a class the ruling just made visible on purpose. "
                                        "Either choice is a scoping decision, and R10 already holds that no "
                                        "orchestrator tool output is a worklist basis for this book."),
    options_stated_without_preference=[
        "the union as literally written: about 444 verses across 100 rows",
        "the peers' hand-named set only: about 47 verses, with the member's 444 kept as a net for the author to "
        "consult per row",
        "a narrowed member: flag an in-span verse only where the row's prose ties it to a boundary warrant, "
        "which needs a definition of 'evidentiary mention' that does not currently exist in any ruling",
    ],
    blocks_author_wave=True,
    tier="MEASURED for every count; the interpretive gap is the orchestrator's reading and is offered as a "
         "question rather than a finding")

add(id="E13-58",
    headline="preconditions P1, P2, P7 and P8 are executed; P8 is running",
    source="orchestrator",
    p1=("DONE. verse_inventory.json declares numbering_face WEB, PROVED before labelling: every per-chapter count "
        "equals the WEB side of the crosswalk and the two divergent chapters carry the WEB figure. Per-chapter "
        "counts unchanged. Its digest changed by design and the author brief pins the new one."),
    p2=("DONE - see E13-57 for what it measured and the question it raises."),
    p7=("DONE. NO peer re-run. The translation parse is PROVED at 1273 verses with 522 continuation lines joined, "
        "equal to the Hebrew witness. Fable's one named test resolves in the peer's favour: peer_06's zero across "
        "eight rows is CORROBORATED by an independent parse, not a dropped-continuation artifact. All six groups' "
        "figure comparisons remain UNKNOWN, because the validator arm applies no exemption where those peers "
        "exercised judgement A6-b later codified - three peers' counts sit below the arm's floor and that is "
        "equally consistent with corruption and with a correct exemption. Recorded in "
        "peer_figure_rederivation_p7.v2.json with v1 kept; no packet edited."),
    p8=("RUNNING. Coverage computed in boss_audit_scoping.v1.json: full coverage of the 14 both-support rows, 21 "
        "decline/reversal rows, all 32 HIGH rows, all 79 rows of the six groups P7 left UNKNOWN, and P08-012 - "
        "100 rows - plus an every-fifth sample of the remaining 45, which is 9. The section-7 held-region set is "
        "UNKNOWN and handed to the boss to derive, because deriving it needs a reading of the strategy's section "
        "7 that the controlling agent's own ruling records as partial."),
    an_orchestrator_defect_in_the_scoping=("the first decline/reversal pattern included the word 'stands', which "
                                           "appears in nearly every peer item, and matched 133 of 145 rows - "
                                           "collapsing the ruling's every-fifth sample to ONE row and turning a "
                                           "scoped audit into a 98.6% read. Narrowed to 21 rows. A superset is "
                                           "defensible; a pattern that matches nearly everything is not a "
                                           "superset but a failure to scope."),
    remaining=["P3 A6 arm re-run on the joined parse", "P4 universals non-scoring (ruled, nothing to execute)",
               "P5 arithmetic arm and mark worklist", "P6 inventory next version, distinct-checked",
               "P9 worklist builder distinct-checked with fixtures firing", "P10 author brief"],
    blocks_author_wave=False, tier="MEASURED")

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
post = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"rows_before": len(pre), "rows_after": len(post), "appended": [e["id"] for e in E],
                  "blocking": len([r for r in post if r.get("blocks_author_wave")]),
                  "high": [r["id"] for r in post if r.get("severity") == "HIGH"],
                  "sha256": hashlib.sha256(Q.read_bytes()).hexdigest()[:32]}, indent=1))
