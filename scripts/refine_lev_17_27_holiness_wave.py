#!/usr/bin/env python3
"""Refine Leviticus 17–27 metadata without changing candidate spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Lev/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "lev_17_27_holiness_wave.v1"
DETAILS = {
    17: ("blood_and_sacrifice_law", "Slaughter, sacrifice, blood, and carcass-handling law", ["sacrifice_location", "blood_prohibition", "carcass_case"]),
    18: ("holiness_boundary_law", "Prohibited sexual/cultic acts with land-defilement closure", ["prohibition_list", "defilement_consequence", "guarding_closure"]),
    19: ("holiness_stipulation_collection", "Holiness call with social, worship, gleaning, and neighbor duties", ["holiness_heading", "social_stipulation", "neighbor_closure"]),
    20: ("sanction_and_separation_law", "Molech, medium, family, and sexual sanctions with separation close", ["sanction_case", "family_or_sexual_case", "separation_closure"]),
    21: ("priestly_holiness_law", "Priestly mourning, marriage, physical conditions, and sanctuary access", ["priestly_status", "marriage_or_mourning", "access_condition"]),
    22: ("holy_food_and_offering_law", "Priestly purity, household eligibility, and acceptable offerings", ["eligibility_case", "offering_condition", "name_sanctification_closure"]),
    23: ("appointed_times_calendar", "Weekly Sabbath and annual appointed-times calendar", ["calendar_heading", "festival_sequence", "rest_or_convocation_formula"]),
    24: ("sanctuary_service_and_case_law", "Continual lamp/bread service and name-blasphemy case with equal-law ruling", ["service_instruction", "case_narrative", "equal_law_closure"]),
    25: ("sabbath_year_and_jubilee_law", "Sabbath year, jubilee proclamation, land pricing, and redemption cases", ["land_sabbath", "jubilee_formula", "redemption_case"]),
    26: ("covenant_blessing_and_sanction_speech", "Conditional blessing, escalating sanctions, confession, and covenant colophon", ["condition_formula", "sanction_escalation", "confession_and_colophon"]),
    27: ("vow_and_dedication_valuation_law", "Valuation, dedicated property, firstborn exceptions, tithes, and Sinai colophon", ["valuation_case", "dedication_exception", "tithe_and_colophon"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Lev":
            continue
        chapter = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if chapter not in DETAILS:
            continue
        form, title, seams = DETAILS[chapter]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained provisionally; holiness, sanction, calendar, economic, and colophon signals are seam leads requiring qualified Hebrew review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Technical Hebrew holiness, sanction, valuation, calendar, and economic vocabulary plus condition-action-result syntax require source-level review"]
        row["original_language_translation_holds"] = ["OSHB/UXLC comparison required; English legal labels and chapter headings cannot decide seams"]
        row["cross_reference_clusters"] = ["Holiness, covenant, festival, jubilee, and redemption parallels are evidence-only internal relation leads"]
        row["cross_reference_holds"] = ["Do not use later canonical legal reuse or theological harmonization as boundary authority"]
        row["hard_passage_forecast"] = ["Sanction escalation, calendar formulae, valuation cases, and colophon transitions may cross modern chapter edges"]
        row["red_team_questions"] = ["Does every proposed seam preserve legal condition→action→result logic after removing English headings?", "Are economic and ritual terms source-verified rather than assumed from translation tradition?"]
        row["red_team_premortem_holds"] = ["Do not collapse distinct holiness, sanction, jubilee, or vow functions; preserve unresolved Hebrew lexical and textual-variant holds"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        refs = list(row.get("boundary_evidence_refs") or [])
        if WAVE not in refs:
            refs.append(WAVE)
        row["boundary_evidence_refs"] = refs
        row["candidate_only"] = True
        row["non_authorizing"] = True
        changed += 1
    return changed


def main() -> int:
    reports = []
    for path in PATHS:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        changed = refine(rows)
        path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
        reports.append({"path": str(path), "rows_changed": changed})
    print(json.dumps({"book": "Lev", "wave": WAVE, "rows_changed": reports, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
