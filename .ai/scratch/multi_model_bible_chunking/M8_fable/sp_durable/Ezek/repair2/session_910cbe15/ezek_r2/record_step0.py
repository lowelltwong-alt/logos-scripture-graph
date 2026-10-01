#!/usr/bin/env python3
"""Record REPAIR-2 step 0: the baselines, taken BEFORE any mutation, as the ruling ordered citing E13-79."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

shutil.copy2(HERE / "order_to_edit_trace.v1.json", EZ / "order_to_edit_trace.v1.json")
trace = json.loads((EZ / "order_to_edit_trace.v1.json").read_text(encoding="utf-8"))
E = []


def add(**kw):
    E.append(dict(kw, opened_at=NOW))


add(id="E13-92",
    severity="HIGH",
    headline="#e15 LANDED (digest parity EXACT, fourth consecutive) AND IT REFRAMED Q1: six of the seven rows "
             "my spot lanes flagged as re-decided were executing ground changes #e13 ORDERED BY NAME. The "
             "lanes could not know - I gave them the diffs and not the orders.",
    raised_by="orchestrator (claude-opus-5)", status="DONE - the ruling is landed", blocks_close=False,
    tier="MEASURED",
    ruling={"file": "Ezek/ezek_controlling_agent_ruling_e15.v1.json",
            "sha256": sha(EZ / "ezek_controlling_agent_ruling_e15.v1.json"), "bytes": 84698,
            "close_clearance": "NOT CLEARED", "seam_moves_ordered": 0, "grade_moves_ordered": 9,
            "tokens_reported": 502514},
    q1_the_correction_to_me=("the ruling's words: 'Every lane says it had no access to the rulings - that, not "
                             "care, produced three thresholds.' My spot brief carried the pre- and post-wave "
                             "diffs but NOT the per-row orders, so three reviewers judged authorised work as "
                             "unauthorised and reached three different thresholds. The cure is in the ruling: "
                             "spot slices will carry the per-row orders AS DATA."),
    the_one_row_that_did_exceed_its_order=("P08-002. The author wrote that CUT-RULE limb (a) licenses the 33:12 "
                                           "ve'attah; the ruling OVERRULES it on the merits - 'house of Israel' "
                                           "and 'children of your people' are two titles for one audience "
                                           "within one speech - so the concession is reversed and medium_low "
                                           "stands."),
    the_line_now_defined=("decision-bearing elements are span/type/parent, grade, rival identity, rival "
                          "verdict, and ground CLASS. An ordered change is a controlling-agent decision "
                          "executed by the wave. A FALSE ONLY-GROUND IS A STOP, NEVER A SUBSTITUTION - which "
                          "is the clause I most needed, because three rows had replaced a false only-ground "
                          "with a true one and called it a repair."),
    eight_self_corrections_the_ruling_discloses=[
        "R11's third premise was false (pmarks names MT 33:20)",
        "its A12-b predicate parenthetical misdescribed A12 and named an unswept verb set",
        "its P04-008 grade was one step low",
        "its P07-008 adopted a peer's under-proposal without applying the scale",
        "its D11 named the wrong row for a verse",
        "its boss audit's mark class was wrong at both 22:31 and 24:14 (both PE) - confirming E13-70",
        "CONF-CAL's HIGH and MEDIUM limbs used DIFFERENT rival predicates - now unified",
        "DEF-A4-ARGUED clause 6 could not express face or single-verse absence - clause 6 v2 ordered",
    ],
    q2_unified=("a rival bars HIGH if LICENSED (any licensed driver) or TWO-FACED (onset-class device on its "
                "near face, verse-final close-role signal on its far face); marks and mid-verse formulae make "
                "no face. P05-008 medium and P02-020 high BOTH stand - the wave's two readings were both "
                "defensible under a scale that carried two predicates."),
    q11_confirmed="my clause-1 reading is CONFIRMED and clause 1 is amended to carry the dotted form; the 39 "
                  "installed entries stay")

add(id="E13-93",
    severity="HIGH",
    headline="REPAIR-2 STEP 0 BASELINES TAKEN BEFORE ANY MUTATION, as ordered. The two ordered checker fixes "
             "each surfaced the class they were built for on their first run: citation_sweep found 2 hidden "
             "wrong-verse attributions, and the register arms found 116 flags where the old checker found 0.",
    raised_by="orchestrator (claude-opus-5)", status="DONE - step 0 complete", blocks_close=False,
    tier="MEASURED",
    baseline_rows="64d9eff05f0e49dc5dfa6aa74ebbbd81809cb8cb2fb8bc24013e03bb3fce0476",
    q6_citation_sweep={
        "member_sha256": sha(EZ / "tools" / "citation_sweep.py"),
        "fixes": ["finditer with per-occurrence, SENTENCE-SCOPED collation: each run is now judged at its own "
                  "position against the reference governing its own clause, replacing a first-match search "
                  "that judged every identical run where the first one stood",
                  "the paseq arm strips the ROLE TOKEN before matching, because [DISCLOSURE-paseq] contains "
                  "the device name and fired its own arm",
                  "the paseq and mark arms gain the puncta arm's adjacent-negation guard, and a NEGATED claim "
                  "is verified as an ABSENCE - a non-empty census at that verse is now the defect"],
        "BASELINE": "RED, 2 problems - BOTH newly visible, and both are the class the fix was built for: "
                    "P08-011's unpointed run and P10-008's pointed run do not collate against the reference "
                    "governing their own clause. The first-match search had hidden them.",
        "why_that_matters": "the fix found two real wrong-verse attributions on its first run, which is the "
                            "strongest evidence available that the defect was worth fixing",
    },
    q9_register={
        "member_sha256": sha(EZ / "tools" / "check_register.py"),
        "arms_added": ["bare_rule_id", "repair_narration", "artifact_referent"],
        "selftest": "39 vectors, 0 failed, including six new fixtures",
        "BASELINE": {"flag_count": 116, "status": "FLAGS",
                     "by_arm": {"bare_rule_id": 43, "repair_narration": 15, "artifact_referent": 58}},
        "what_this_says_about_my_earlier_report": ("I reported 'register GREEN, 0 flags' after my substitution. "
                                                   "The rule's actual violations number 116. The old checker "
                                                   "measured its own patterns; I reported that as the rule. The "
                                                   "ruling's sentence is the one to keep: 'the checker's "
                                                   "patterns are a floor under that rule, not the rule.'"),
        "and_my_own_phrase_is_in_it": ("'the division plan' - which I introduced to replace the barred word "
                                       "'strategy' - is matched by the artifact_referent arm, because the "
                                       "ruling holds that a paraphrase of a barred referent is barred. My 30 "
                                       "register edits are mine to undo in the prose pass."),
    },
    order_to_edit_trace={
        "file": "Ezek/order_to_edit_trace.v1.json", "sha256": sha(EZ / "order_to_edit_trace.v1.json"),
        "what_it_corrects": ("my E13-65 fixture asserted every per-row order had a worklist ITEM; it never "
                             "asserted the item's EDIT carried the order's CONTENT. The ruling: 'this trace is "
                             "the fixture E13-65's builder gate lacked: it tests DISCHARGE, not existence.'"),
        "orders_traced": trace["orders_traced"], "tally": trace["tally"],
        "partial": [{"row": r["row"], "why": r["why"]} for r in trace.get("PARTIAL", [])],
        "unclear": [{"row": r["row"], "order": r["order"][:80]} for r in trace.get("UNCLEAR", [])],
        "an_honest_limit": ("three orders name no verse and no device word ('replace the false ground'), so the "
                            "trace reports them UNCLEAR rather than passed. A trace that guessed would report "
                            "discharge it cannot see, which is the failure it exists to catch."),
        "and_a_correction_i_made_mid_run": ("my first version traced only the orders that LACKED a worklist "
                                            "item, because that is the list my artifact carried - testing the "
                                            "part of the order set I had to hand, which is the exact mistake "
                                            "this trace exists to catch. It now re-derives all 22 from the four "
                                            "rulings."),
    },
    still_to_build_for_step_0=["the census-consistency member (Q10)", "the CONF-CAL audit sweep (Q2/Q3)"],
    repair2_sequence=["0 baselines (in progress)", "1 the nine grade moves, mechanical, with grounds",
                      "2 grounds: P08-002, the stale-ground prose, the three findings of fact",
                      "3 measured-false-anywhere after distinct checks, plus the trace's undischarged items",
                      "4 vocabulary: face qualifiers, absence tokens, MT devices re-faced",
                      "5 the register prose pass, read back as English",
                      "6 the eight released transport items and seven A16 weighings",
                      "7 full suite, then a SPOT RE-READ at full coverage with the ORDERS in the slices"])

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"appended": [e["id"] for e in E], "queue_rows": len(rows)}, indent=1))
