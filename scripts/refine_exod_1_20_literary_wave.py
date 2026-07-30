#!/usr/bin/env python3
"""Refine Exodus 1–20 literary metadata while preserving candidate spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Exod/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "exod_1_20_literary_wave.v1"

DETAILS = {
    1: ("genealogical_opening", "Israelite family-list opening and multiplication threshold", ["register_opening", "multiplication_formula", "narrative_turn"]),
    2: ("oppression_and_birth_narrative", "Oppression escalation, midwife resistance, and river decree", ["royal_decree", "midwife_dialogue", "decree_closure"]),
    3: ("birth_rescue_narrative", "Moses birth, river rescue, adoption, and naming sequence", ["birth_frame", "river_rescue", "naming_closure"]),
    4: ("flight_and_midian_narrative", "Moses intervention, flight, and Midian settlement episode", ["conflict_scene", "flight_transition", "settlement_closure"]),
    5: ("call_commission_dialogue", "Israelite cry, bush encounter, commission, and objection dialogue", ["divine_appearance", "commission_dialogue", "objection_closure"]),
    6: ("commission_continuation", "Departure from Midian and return-to-Egypt commission", ["departure_notice", "commission_formula", "return_transition"]),
    7: ("ritual_incident", "Lodging-place circumcision incident with abrupt narrative seam", ["travel_frame", "ritual_incident", "closure_or_appeal"]),
    8: ("recognition_and_return_narrative", "Aaron meeting, signs, Israelite recognition, and response", ["meeting_scene", "sign_report", "recognition_closure"]),
    9: ("pharaoh_confrontation_narrative", "First audience, increased burden, protest, and divine response", ["audience_scene", "burden_escalation", "response_closure"]),
    10: ("renewed_commission_dialogue", "Renewed commission speech and Moses objection", ["commission_formula", "objection_dialogue", "speech_closure"]),
    11: ("commission_genealogy", "Genealogical register identifying Moses and Aaron for the commission", ["register_heading", "genealogy_formula", "commission_return"]),
    12: ("rod_sign_commission_narrative", "Resumed commission and rod sign before Pharaoh", ["commission_resume", "rod_sign", "pharaoh_response"]),
    13: ("plague_cycle", "Nile confrontation and blood-plague cycle", ["warning_formula", "sign_execution", "pharaoh_response"]),
    14: ("plague_cycle", "Frog-plague warning, removal request, and reversal", ["plague_warning", "intercession_or_removal", "reversal_formula"]),
    15: ("plague_cycle", "Dust/lice sign and magicians' recognition", ["sign_execution", "magician_response", "hardening_or_closure"]),
    16: ("plague_cycle", "Swarms, negotiation, removal, and renewed refusal", ["distinction_formula", "negotiation_dialogue", "reversal_formula"]),
    17: ("plague_cycle", "Livestock-plague warning, distinction, and refusal", ["warning_formula", "distinction_test", "refusal_closure"]),
    18: ("plague_cycle", "Ashes/boils sign and magicians' inability to stand", ["ritual_action", "bodily_sign", "response_closure"]),
    19: ("plague_cycle", "Hail warning, differentiated response, storm, and reversal", ["warning_and_choice", "storm_sequence", "reversal_formula"]),
    20: ("plague_cycle", "Locust warning, negotiation, devastation, and reversal", ["warning_formula", "negotiation_dialogue", "devastation_and_reversal"]),
    21: ("plague_transition", "Darkness confrontation and continuous final-plague announcement", ["darkness_sign", "confrontation", "final_plague_announcement"]),
    22: ("passover_instruction", "Passover and unleavened-bread instruction with responsive compliance", ["ritual_instruction", "household_application", "compliance_closure"]),
    23: ("exodus_departure_narrative", "Firstborn death, urgent departure, and vigil summary", ["death_notice", "departure_sequence", "vigil_summary"]),
    24: ("passover_ordinance", "Passover participation ordinance and departure compliance", ["ordinance_heading", "participant_case", "compliance_closure"]),
    25: ("firstborn_remembrance_instruction", "Firstborn consecration, departure remembrance, and teaching signs", ["consecration_instruction", "remembrance_formula", "teaching_sign"]),
    26: ("sea_crossing_narrative", "Wilderness route, pursuit, sea crossing, and prose resolution", ["route_notice", "pursuit_dialogue", "crossing_and_resolution"]),
    27: ("victory_song_and_refrain", "Song of the Sea, prose bridge, and Miriam responsive refrain", ["song_opening", "stanza_or_refrain", "prose_to_refrain_transition"]),
    28: ("wilderness_provision_narrative", "Marah testing, provision, and Elim transition", ["travel_notice", "testing_scene", "provision_closure"]),
    29: ("manna_provision_instruction", "Manna/quail provision, Sabbath test, naming, and memorial", ["complaint_and_provision", "sabbath_test", "memorial_closure"]),
    30: ("water_crisis_narrative", "Rephidim water crisis and naming closure", ["complaint_scene", "staff_or_water_action", "naming_closure"]),
    31: ("war_and_memorial_narrative", "Amalek conflict and memorial closure", ["battle_narrative", "raised_hands_scene", "memorial_formula"]),
    32: ("jethro_arrival_narrative", "Jethro arrival, recounting, acclaim, and meal", ["arrival_notice", "recounting_speech", "meal_closure"]),
    33: ("judicial_counsel_narrative", "Judicial overload, counsel, implementation, and departure", ["problem_report", "counsel_speech", "implementation_closure"]),
    34: ("sinai_covenant_preparation", "Sinai arrival, covenant address, preparation, and theophany bounds", ["arrival_formula", "covenant_address", "preparation_and_bounds"]),
    35: ("covenant_decalogue_speech", "Divine covenant address and fearful people response", ["direct_speech_opening", "command_sequence", "fearful_response"]),
    36: ("covenant_code_threshold", "Covenant-Code threshold with speech reminder and altar directives", ["speech_reminder", "altar_instruction", "legal_collection_transition"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Exod":
            continue
        idx = int(row["chunk_index_in_book"])
        if idx not in DETAILS:
            continue
        form, title, seams = DETAILS[idx]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained provisionally; scene, speech, plague-cycle, song, and legal-form signals are internal seam leads requiring independent Hebrew review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Hebrew narrative sequencing, plague formula repetition, ritual/legal vocabulary, and speech-to-narrative transitions require source-level review"]
        row["original_language_translation_holds"] = ["OSHB/UXLC comparison required; English headings and paragraphing cannot decide seams"]
        row["cross_reference_clusters"] = ["Exodus creation, covenant, wilderness, song, and later legal/prophetic reuse are evidence-only relation leads"]
        row["cross_reference_holds"] = ["Do not use later canonical reuse or theological harmonization as boundary authority"]
        row["hard_passage_forecast"] = ["Repeated plague formulas, embedded songs, ritual instructions, and prose-to-law transitions may cross modern chapter edges"]
        row["red_team_questions"] = ["Does the proposed seam survive removal of English headings and chapter numbers?", "Are repeated plague/ritual formulas being treated as architecture rather than automatic chapter boundaries?"]
        row["red_team_premortem_holds"] = ["Do not turn deliverance, covenant, or law labels into theological conclusions; preserve Hebrew wording and source-variant uncertainty"]
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
    print(json.dumps({"book": "Exod", "wave": WAVE, "rows_changed": reports, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
