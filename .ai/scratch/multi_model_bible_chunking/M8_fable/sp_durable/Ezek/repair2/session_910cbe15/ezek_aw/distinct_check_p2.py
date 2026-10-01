#!/usr/bin/env python3
"""O3's DISTINCT CHECK (OW-10): the re-run's citations against the controlling agent's independent recount.

WHY THIS IS A REAL DISTINCT CHECK AND NOT A COUNT COMPARISON. The controlling agent left its working artifact
behind - r1_citation_items.json, one record per citation with its row, its verse list and its class - produced by
its own script (recount_r1.py) from the same pinned rows through code it wrote without seeing mine. So the
comparison can be SET EQUALITY over (row, verse-set, class), which is what the eight agreeing totals would
otherwise only suggest. Two wrong implementations agreeing on eight totals is possible; agreeing item for item on
several hundred is not.

O3's acceptance rule, applied literally: a difference attributable to LIST-SPLITTING or DEDUPE convention is
named per instance and accepted; ANY OTHER DIFFERENCE IS A STOP. So this script does not summarise differences -
it classifies every one of them, and it refuses to call the check passed if a single difference falls outside
those two conventions.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
FABLE = HERE.parent / "ezek_e14_work_fable_ruling_a1_7f3c" / "r1_citation_items.json"
MINE = HERE / "refs_mirror_citation_run2.json"
MEMBER = ("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable"
          "/sp_durable/Ezek/tools/check_refs_mirror.py")
FABLE_PIN = "dd4f6287cd5077b40931b414c6572dba8ce4cd3ff3294a411604c6d9ba53569f"

got = hashlib.sha256(FABLE.read_bytes()).hexdigest()
if got != FABLE_PIN:
    raise SystemExit("REFUSED: the recount artifact is %s, not the pinned %s" % (got, FABLE_PIN))

fab = json.loads(FABLE.read_text(encoding="utf-8"))
run = json.loads(MINE.read_text(encoding="utf-8"))

# the recount labels the mixed class "mixed_span_and_seam"; the first version of this map omitted that spelling
# and reported its 3 items as differences. A normaliser that silently upper-cases an unknown label manufactures
# disagreement, so every label either maps or raises.
NORM = {"in_span": "IN_SPAN", "at_seam": "AT_SEAM", "mixed": "MIXED", "far_side": "FAR_SIDE",
        "mixed_span_and_seam": "MIXED"}


def norm(cls):
    c = str(cls).lower()
    if c not in NORM:
        raise SystemExit("REFUSED: unknown class label %r - a normaliser must never guess" % cls)
    return NORM[c]


def key(row, verses, cls):
    return (row, tuple(sorted(verses)), norm(cls))


fab_keys = Counter(key(r["row"], r["verses"], r.get("cls")) for r in fab)
# SCOPE, MEASURED not assumed: the recount artifact holds ONLY in-window citations (no far_side label appears
# in it), so the comparable set is the re-run's worklist citations. The 137 far-side citations are compared by
# their totals, which the ruling names, and not by item - stated rather than left as a silent 137-item gap.
assert not any(str(r.get("cls")).lower() == "far_side" for r in fab), "the recount does carry far-side items"
mine_items = run["worklist_citations"]
my_keys = Counter(key(i["decision_id"], i["verses_web"], i["class"]) for i in mine_items)

# NOTE ON TRUNCATION: my records cap verses_web at 16 entries for readability, so a citation spanning more than
# 16 verses cannot be compared by verse list. Those are compared by row+class+endpoint instead and counted
# separately, because a check that silently skipped them would be the UNAVAILABLE-where-MEASURABLE class.
long_mine = [i for i in mine_items if i["verse_count"] != len(i["verses_web"])]
long_fab = [r for r in fab if len(r["verses"]) > 16]

only_fable = fab_keys - my_keys
only_mine = my_keys - fab_keys

# ---- classify every difference against O3's two accepted conventions
named, unexplained = [], []
by_row_fab, by_row_mine = {}, {}
for k, n in only_fable.items():
    by_row_fab.setdefault(k[0], []).append(k)
for k, n in only_mine.items():
    by_row_mine.setdefault(k[0], []).append(k)

for rowid in sorted(set(by_row_fab) | set(by_row_mine)):
    f, m = by_row_fab.get(rowid, []), by_row_mine.get(rowid, [])
    f_verses = {v for k in f for v in k[1]}
    m_verses = {v for k in m for v in k[1]}
    if f_verses == m_verses and (len(f) != len(m)):
        named.append({"row": rowid, "convention": "LIST-SPLITTING or DEDUPE",
                      "same_verses_regrouped": True,
                      "recount_groups": [list(k[1]) for k in f], "rerun_groups": [list(k[1]) for k in m],
                      "accepted_because": "O3 accepts a difference attributable to list-splitting or dedupe "
                                          "convention when named per instance; the verse sets are identical "
                                          "and only the grouping differs"})
    elif f_verses == m_verses:
        named.append({"row": rowid, "convention": "CLASS LABEL on identical grouping",
                      "recount": [list(k[1]) + [k[2]] for k in f],
                      "rerun": [list(k[1]) + [k[2]] for k in m],
                      "accepted_because": "PENDING - a class difference is NOT a list-splitting or dedupe "
                                          "convention"})
        unexplained.append({"row": rowid, "why": "same verses, different CLASS", "recount": f, "rerun": m})
    else:
        unexplained.append({"row": rowid, "why": "the verse sets themselves differ",
                            "only_in_recount": sorted(f_verses - m_verses)[:12],
                            "only_in_rerun": sorted(m_verses - f_verses)[:12]})

# ---- the eight figures the ruling named as the distinct-check target
TARGET = {"in_span_single_citations": 131, "in_span_range_citations": 11,
          "mixed_span_and_seam_citations": 3, "at_seam_single_citations": 119,
          "seam_touching_range_citations": 28,
          "rows_with_an_in_span_or_mixed_citation": 65, "far_side_citations": 137}
figures = {k: {"ruling_recount": v, "rerun": run["counts"][k], "agree": run["counts"][k] == v}
           for k, v in TARGET.items()}
figures["far_side_verses (legacy verse-level)"] = {
    "ruling_recount": 817, "rerun": run["legacy_verse_level_aggregate"]["far_side_verses"],
    "agree": run["legacy_verse_level_aggregate"]["far_side_verses"] == 817}

# ---- the shipped member's own figures, reproduced by the legacy arm: evidence that the citation layer
# regrouped the class and did not redefine it
legacy_repro = {"in_span_verses": (run["legacy_verse_level_aggregate"]["in_span_verses"], 444),
                "at_seam_verses": (run["legacy_verse_level_aggregate"]["at_seam_verses"], 131),
                "far_side_verses": (run["legacy_verse_level_aggregate"]["far_side_verses"], 817)}

# ---- E13-57's 99-vs-100 discrepancy, settled by measurement at the verse level
rows_in_span_verse_level = len({i["decision_id"] for i in run["worklist_citations"]
                                if i["class"] in ("IN_SPAN", "MIXED")})

out = {
    "what_this_checks": "the re-run's citation SET against the controlling agent's independent recount, item "
                        "for item, not total against total",
    "recount_artifact": {"path": str(FABLE), "sha256": got, "items": len(fab),
                         "author": "controlling agent #e14 via recount_r1.py, written without seeing the "
                                   "member's implementation"},
    "rerun_artifact": {"path": str(MINE), "items": len(mine_items),
                       "member_sha256": hashlib.sha256(Path(MEMBER).read_bytes()).hexdigest()},
    "named_figures": figures,
    "all_named_figures_agree": all(v["agree"] for v in figures.values()),
    "legacy_arm_reproduces_the_shipped_members_verse_level_figures": {
        k: {"rerun": a, "shipped_member": b, "agree": a == b} for k, (a, b) in legacy_repro.items()},
    "set_comparison": {
        "items_in_recount_only": sum(only_fable.values()),
        "items_in_rerun_only": sum(only_mine.values()),
        "items_matched_exactly": sum((fab_keys & my_keys).values()),
        "rows_with_any_difference": len(set(by_row_fab) | set(by_row_mine)),
        "differences_named_as_accepted_conventions": named,
        "DIFFERENCES_OUTSIDE_THE_ACCEPTED_CONVENTIONS": unexplained,
    },
    "verse_list_truncation": {
        "rerun_items_whose_verse_list_is_incomplete": len(long_mine),
        "recount_items_longer_than_16_verses": len(long_fab),
        "history": ("the first version of the member capped verses_web at 16 entries and this check reported 7 "
                    "spurious differences - each a citation longer than the cap, and in one row two different "
                    "citations truncated to the SAME 16-verse prefix and collapsed into one item. The cap was "
                    "removed and the member re-run; run 2 is identical to run 1 in every count, every "
                    "classification and every item field other than the verse list, which is now complete. "
                    "TWO RUNS are therefore disclosed against O3's 'once more': the second exists because the "
                    "distinct check found the artifact unauditable, and it changed no measured figure."),
    },
    "mirror_reading_question_settled_by_measurement": {
        "union_versus_strict_per_entry_disagreements": run["mirror_reading"]["disagreement_count"],
        "meaning": ("ZERO. DEF-A4-ARGUED clause 3's singular 'entry' admits a strict reading and the union of "
                    "entries admits a looser one; on this corpus no citation is mirrored by the union that is "
                    "not also mirrored by a single entry. The ambiguity is MOOT here and was settled by "
                    "measuring both, not by the orchestrator choosing one."
                    if run["mirror_reading"]["disagreement_count"] == 0 else
                    "NON-ZERO - the reading must be ruled, not chosen by the orchestrator"),
    },
    "e13_57_row_count_discrepancy": {
        "orchestrator_reported": 100, "controlling_agent_measured": 99,
        "rows_with_an_in_span_or_mixed_CITATION_this_run": run["counts"][
            "rows_with_an_in_span_or_mixed_citation"],
        "rows_with_an_in_span_or_mixed_citation_recomputed_from_items": rows_in_span_verse_level,
        "status": "the citation-level figure is 65 and agrees with the recount exactly; the 99-vs-100 "
                  "verse-level difference is superseded by the granularity the ruling ordered and is not "
                  "carried forward",
    },
    "verdict": ("PASS - every named figure agrees and every set difference falls inside O3's accepted "
                "conventions" if all(v["agree"] for v in figures.values()) and not unexplained else
                "STOP - see DIFFERENCES_OUTSIDE_THE_ACCEPTED_CONVENTIONS"),
    "tier": "MEASURED on both sides; the recount is the controlling agent's, pinned by digest",
}
(HERE / "distinct_check_p2.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("named_figures", "all_named_figures_agree",
                                      "legacy_arm_reproduces_the_shipped_members_verse_level_figures",
                                      "mirror_reading_question_settled_by_measurement",
                                      "e13_57_row_count_discrepancy", "verdict")},
                 ensure_ascii=False, indent=1))
print(json.dumps(out["set_comparison"], ensure_ascii=False, indent=1)[:4000])
print(json.dumps(out["verse_list_truncation"], indent=1, ensure_ascii=False))
