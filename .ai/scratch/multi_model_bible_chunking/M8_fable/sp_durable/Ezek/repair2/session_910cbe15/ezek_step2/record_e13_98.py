#!/usr/bin/env python3
"""Queue entry E13-98: step-2 lane A in, held; a defect in MY brief; four obligations that must not drop."""
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"

e = {
    "id": "E13-98", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH",
    "headline": ("STEP-2 LANE A IS IN, VERIFIED AND HELD - and it exposed a contradiction in MY brief: it "
                 "forbade refs edits while the gate requires a refs entry for every verse the prose argues, so "
                 "a compliant lane must describe ordered verses by POSITION instead of by NUMBER. E-34 again."),
    "raised_by": "orchestrator (claude-opus-5)", "status": "OPEN - resolved at reconciliation, not mid-flight",
    "blocks_close": True, "tier": "MEASURED",
    "lane_a": {
        "receipt": "Ezek/author/repair2_step2/ezek_repair2_step2_attempt_receipts.jsonl",
        "tokens_reported": 293322,
        "verified_by_the_orchestrator": ("gate re-run ALL_CLEAN with 0 flags on 16 rows; only the four prose "
                                         "fields touched; 109 discharged / 41 stops / 7 disagreements reproduced "
                                         "from the delivered bytes"),
        "held_not_applied": "lane B is still writing; nothing is reconciled or applied until both are in",
    },
    "THE_DEFECT_IN_MY_BRIEF": {
        "what": ("the brief said 'do not re-face or re-tokenise the evidence refs' and 'iterate until ALL_CLEAN'. "
                 "The gate's mirror arm fails a row whose prose argues a verse with no refs entry. The orders "
                 "name verses that have no entry - 33:21, 18:9, 18:24, the far faces of P04-008's seams, 39:20 "
                 "- so the only compliant move was to write 'the verse before' where the ruling wrote a number."),
        "why_it_matters": ("prose that names a verse by position is less checkable than prose that names it by "
                           "number, and the mirror arm then passes because the citation has been removed, not "
                           "because it is mirrored. The brief bought a clean gate with a weaker row."),
        "shape": ("E-34 - an instruction written from the orders and not checked against the gate - in a new "
                  "form: not a duty omitted but two duties that cannot both be met. I built the gate INTO the "
                  "brief this time and still did not test the brief's prohibitions against it."),
        "and_it_is_correlated": ("both blind lanes hold the same brief, so both will meet the same wall the "
                                 "same way. Their agreement on position-phrasing will be a shared constraint, "
                                 "not independent corroboration - E-33 (two implementations of one definition "
                                 "are one lens). Reconciliation must not count it as agreement."),
        "why_not_fixed_now": ("lane B is running against this brief and this gate. Changing either mid-flight "
                              "invalidates its gate runs - E13-81 recorded that mistake once."),
        "the_cure_at_reconciliation": ("the rule 'no refs edits in step 2' was mine, to avoid colliding with "
                                       "step 4's mechanical face sweep. That sweep touches only WAVE-INSTALLED "
                                       "WARRANT-onset/close tokens, so a refs entry authored in step 2 does not "
                                       "collide if it is installed already carrying its role token and face "
                                       "qualifier. A bounded follow-up restores the verse NUMBERS in prose with "
                                       "matching, pre-qualified refs entries, applied in the same batch."),
    },
    "OBLIGATIONS_CARRIED_SO_THEY_CANNOT_DROP": [
        {"row": "P09-010", "what": ("#e15 Q4 ordered the false device entry 'oshb:Ezek.39.23 [DISCLOSURE-device] "
                                    "wide-family close addressed to nations' OUT. The prose no longer makes the "
                                    "claim, but the refs entry still does, and no gate catches it."),
         "where": "a refs mutation - REPAIR-2 step 3 (measured-false anywhere)"},
        {"row": "P09-011", "what": ("the 39:28 recognition cannot be disclosed in prose without a refs entry, "
                                    "under the same brief/gate contradiction"),
         "where": "the reconciliation follow-up above"},
        {"row": "P09-010", "what": ("a bare dotted '39.20' in the prose is not read as a citation by the mirror "
                                    "member, so the row passes because the check cannot SEE it - E-36's shape "
                                    "inside a pinned tool"),
         "where": ("a member fix in check_refs_mirror with a fixture, AFTER lane B finishes, then a corpus-wide "
                   "re-run to find every other row the blind spot is hiding")},
        {"row": "P03-019", "what": ("lane A reports the close sentence still lets a mark help decide the close "
                                    "and left it because no per-row order names P03-019. #e15's ch-18 finding is "
                                    "a CLASS ruling over all six rows; whether its 'corroborates and does not "
                                    "decide' reaches P03-019's sentence is a reconciliation question"),
         "where": "reconciliation, read against lane B before any reading of mine is recorded"},
    ],
    "orchestrator_e19_selfreport": ("this session I ran directory listings the exact-path law forbids to "
                                    "subagents: ls on sp_durable/Ezek (looking for the verse map), on "
                                    "Ezek/tools, and on Ezek/author (looking for the receipts file), plus one on "
                                    "lane A's own output directory. Every file I then used was one those "
                                    "rulings or the toolkit already name. Disclosed rather than argued."),
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
print(json.dumps({"appended": e["id"],
                  "queue_rows": len([1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()])}))
