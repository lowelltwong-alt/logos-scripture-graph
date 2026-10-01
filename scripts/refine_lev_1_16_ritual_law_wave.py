#!/usr/bin/env python3
"""Refine Leviticus 1–16 ritual/legal metadata without changing spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Lev/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "lev_1_16_ritual_law_wave.v1"

DETAILS = {
    1: ("offering_instruction", "Burnt-offering procedure by herd, flock, and bird", ["offering_heading", "variant_procedure", "fire_or_closure_formula"]),
    2: ("offering_instruction", "Grain-offering forms, restrictions, salt, and first produce", ["variant_procedure", "restriction_clause", "first_produce_closure"]),
    3: ("offering_instruction", "Well-being offering procedure and fat/blood statute", ["ritual_sequence", "shared_meal_or_allocation", "fat_blood_transition"]),
    4: ("purification_offering_law", "Unintentional-sin purification offerings by status", ["status_case", "ritual_action", "disposal_or_closure"]),
    5: ("purification_and_reparation_law", "Specified offenses, confession, and means-based alternatives", ["offense_case", "confession_or_restitution", "means_based_variant"]),
    6: ("reparation_offering_law", "Holy-property trespass and unknown-command liability", ["trespass_case", "liability_formula", "offering_closure"]),
    7: ("reparation_and_restitution_law", "Neighbor fraud, restitution, and reparation offering", ["fraud_case", "restitution_condition", "offering_closure"]),
    8: ("priestly_offering_instruction", "Priestly burnt-offering handling and perpetual altar fire", ["priestly_heading", "altar_fire_sequence", "perpetual_formula"]),
    9: ("priestly_offering_instruction", "Priestly handling and consumption of grain offerings", ["priestly_procedure", "consumption_rule", "holiness_closure"]),
    10: ("priestly_installation_offering", "Priestly installation grain offering", ["installation_heading", "daily_procedure", "fire_or_closure_formula"]),
    11: ("priestly_purification_offering", "Priestly handling of purification offerings", ["priestly_procedure", "blood_or_disposal_rule", "consumption_boundary"]),
    12: ("reparation_offering_instruction", "Reparation-offering procedure", ["offering_heading", "ritual_sequence", "priestly_allocation"]),
    13: ("priestly_allocation_law", "Cross-offering priestly allocations", ["allocation_summary", "shared_rule", "collection_transition"]),
    14: ("wellbeing_offering_law", "Thanksgiving, vow, freewill, and purity rules", ["offering_variant", "time_or_purity_condition", "consumption_closure"]),
    15: ("fat_blood_prohibition", "Prohibition of eating fat and blood", ["prohibition_formula", "life_or_fat_blood_clause", "holiness_closure"]),
    16: ("offering_corpus_colophon", "Priestly portions and offering-corpus colophon", ["allocation_recap", "source_or_colophon_formula", "collection_closure"]),
    17: ("ordination_narrative", "Assembly, washing, clothing, and anointing of Aaron and sons", ["assembly_notice", "vesting_sequence", "anointing_closure"]),
    18: ("ordination_narrative", "Ordination sacrifices, blood application, meal, and seven-day charge", ["sacrifice_sequence", "blood_application", "seven_day_charge"]),
    19: ("inaugural_service_narrative", "Eighth-day inaugural service and glory-fire climax", ["service_instruction", "blessing_or_appearance", "fire_climax"]),
    20: ("priestly_incident_narrative", "Unauthorized fire, death, removal, and mourning constraints", ["incident_report", "death_and_removal", "mourning_instruction"]),
    21: ("priestly_instruction", "Priestly sobriety, distinction, and teaching mandate", ["sobriety_rule", "distinction_instruction", "teaching_closure"]),
    22: ("priestly_incident_and_case", "Remaining offerings, disputed consumption, and accepted explanation", ["offering_case", "disputed_consumption", "acceptance_or_closure"]),
    23: ("purity_classification_law", "Land, water, bird, and winged-creature food classifications", ["classification_list", "case_transition", "purity_closure"]),
    24: ("purity_transmission_law", "Carcass contact and transmission procedures", ["contact_case", "washing_or_time_condition", "status_closure"]),
    25: ("purity_classification_summary", "Creeping-creature prohibition, holiness rationale, and summary", ["prohibition_list", "holiness_formula", "classification_closure"]),
    26: ("childbirth_purity_law", "Childbirth purification periods and offering alternatives", ["time_condition", "purification_action", "means_based_offering"]),
    27: ("diagnostic_purity_law", "Bodily surface diagnosis, isolation, and public status", ["diagnostic_case", "inspection_or_time_condition", "status_decision"]),
    28: ("diagnostic_purity_law", "Garment and leather-surface diagnosis", ["material_case", "inspection_sequence", "cleansing_or_disposal"]),
    29: ("restoration_purity_law", "Restored-person cleansing and reduced-cost alternative", ["restoration_sequence", "offering_variant", "status_closure"]),
    30: ("house_diagnostic_law", "House diagnosis, cleansing, and surface-condition summary", ["house_case", "inspection_or_removal", "summary_closure"]),
    31: ("discharge_purity_law", "Male/female discharge cases, cleansing, sanctuary-risk rationale, and summary", ["case_pairing", "washing_or_time_condition", "sanctuary_risk_closure"]),
    32: ("day_of_atonement_preparation", "Death-framed access warning, vesting, offerings, and two-goat selection", ["access_warning", "vesting_and_offering", "goat_selection"]),
    33: ("day_of_atonement_ritual", "Inner-sanctuary, altar, live-goat, exit, and disposal rites", ["inner_sanctuary_sequence", "live_goat_rite", "disposal_or_exit"]),
    34: ("day_of_atonement_statute", "Annual self-affliction, rest, and atonement statute", ["annual_formula", "self_affliction_and_rest", "statute_closure"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Lev":
            continue
        idx = int(row["chunk_index_in_book"])
        if idx not in DETAILS:
            continue
        form, title, seams = DETAILS[idx]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained provisionally; ritual/legal condition-action-result sequences and priestly/formula transitions are seam leads requiring qualified Hebrew review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Technical Hebrew ritual terms, purity/status vocabulary, priestly allocation formulas, and condition-action-result syntax require source-level review"]
        row["original_language_translation_holds"] = ["OSHB/UXLC comparison required; English ritual labels and paragraphing cannot decide seams"]
        row["cross_reference_clusters"] = ["Offering, purity, priestly, and atonement parallels are evidence-only internal relation leads"]
        row["cross_reference_holds"] = ["Do not use later canonical ritual reuse or theological harmonization as boundary authority"]
        row["hard_passage_forecast"] = ["Technical diagnosis, variant offerings, disposal rules, and ritual sequences may cross modern chapter edges"]
        row["red_team_questions"] = ["Does each seam preserve legal condition→action→result logic after removing English headings?", "Are technical categories being treated as source-verified observations rather than translation assumptions?"]
        row["red_team_premortem_holds"] = ["Do not collapse distinct ritual functions or infer theology from purity/atonement terminology; preserve unresolved lexical variants"]
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
