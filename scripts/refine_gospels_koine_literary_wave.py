#!/usr/bin/env python3
"""Refine Gospel literary metadata and Koine holds without changing spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Matt/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Mark/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Luke/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/John/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "gospels_koine_literary_wave.v1"

FORMS = {
    "Matt": [
        ("genealogy_birth_narrative", ["genealogy", "birth_narrative", "quotation_formula"]),
        ("infancy_and_return_narrative", ["dream_or_angel_notice", "flight_narrative", "return_closure"]),
        ("baptism_testing_and_call_narrative", ["baptism_scene", "testing_sequence", "call_or_proclamation"]),
        ("teaching_discourse", ["beatitude_or_heading", "quotation_or_exposition", "discourse_closure"]),
        ("miracle_and_discipleship_collection", ["healing_sequence", "discipleship_response", "commission_or_transition"]),
        ("parable_and_mission_discourse", ["parable_sequence", "mission_instruction", "rejection_or_response"]),
        ("identity_and_conflict_narrative", ["recognition_dialogue", "prediction_or_response", "transfiguration_or_transition"]),
        ("community_and_judgment_discourse", ["community_instruction", "parable_or_judgment", "discourse_closure"]),
        ("journey_and_conflict_narrative", ["journey_notice", "healing_or_conflict", "arrival_transition"]),
        ("temple_dispute_discourse", ["entry_or_action", "authority_dispute", "parable_or_wisdom_response"]),
        ("eschatological_discourse", ["temple_prediction", "watchfulness_parable", "discourse_closure"]),
        ("passion_narrative", ["meal_or_anointing", "arrest_trial", "crucifixion_and_burial"]),
        ("resurrection_narrative", ["empty_tomb", "appearance_or_commission", "book_closure"]),
        ("resurrection_narrative", ["appearance_sequence", "commission_speech", "closure_formula"]),
        ("passion_transition", ["betrayal_or_trial", "passion_sequence", "burial_closure"]),
        ("resurrection_and_commission", ["empty_tomb", "appearance", "commission_closure"]),
    ],
    "Mark": [
        ("opening_call_narrative", ["prologue", "baptism_or_testing", "call_sequence"]),
        ("conflict_and_authority_collection", ["healing_or_call", "authority_dispute", "parable_response"]),
        ("parable_and_storm_narrative", ["parable_sequence", "interpretation", "storm_crossing"]),
        ("miracle_and_discipleship_collection", ["exorcism_or_healing", "feeding_or_purity", "mission_transition"]),
        ("purity_and_recognition_narrative", ["purity_dispute", "gentile_encounter", "recognition_dialogue"]),
        ("journey_and_prediction_narrative", ["healing_or_disciple_response", "prediction", "teaching_transition"]),
        ("temple_and_eschatological_discourse", ["entry_or_temple_action", "authority_dispute", "eschatological_discourse"]),
        ("passion_narrative", ["meal_or_anointing", "arrest_trial", "crucifixion_and_burial"]),
        ("resurrection_narrative", ["empty_tomb", "appearance_or_commission", "ending_hold"]),
        ("resurrection_closure", ["appearance_sequence", "commission_or_response", "textual_ending_hold"]),
    ],
    "Luke": [
        ("preface_and_infancy_narrative", ["preface", "annunciation_or_birth", "childhood_closure"]),
        ("genealogy_testing_and_program", ["genealogy", "testing_sequence", "nazareth_program"]),
        ("call_healing_and_teaching_collection", ["call_sequence", "healing_or_conflict", "plain_teaching"]),
        ("faith_encounter_and_parable_collection", ["faith_encounter", "women_or_meal_scene", "parable_discourse"]),
        ("mission_and_recognition_narrative", ["mission", "feeding_or_recognition", "transfiguration"]),
        ("journey_teaching_and_parable_collection", ["journey_notice", "parable_sequence", "discipleship_instruction"]),
        ("journey_conflict_and_lament", ["journey_or_meal", "conflict_speech", "lament_or_prediction"]),
        ("temple_and_eschatological_discourse", ["entry_or_temple_action", "authority_dispute", "eschatological_discourse"]),
        ("passion_narrative", ["meal_or_prayer", "arrest_trial", "crucifixion_and_burial"]),
        ("resurrection_and_appearance_narrative", ["empty_tomb", "road_or_appearance", "commission_closure"]),
        ("resurrection_appearance_collection", ["appearance_sequence", "scripture_exposition", "commission_or_closure"]),
        ("passion_transition", ["betrayal_or_trial", "passion_sequence", "burial_closure"]),
        ("resurrection_narrative", ["empty_tomb", "appearance", "book_closure"]),
        ("resurrection_and_ascension_closure", ["appearance_sequence", "ascension_or_blessing", "closure_formula"]),
    ],
    "John": [
        ("prologue_and_witness_narrative", ["prologue", "witness_testimony", "disciple_call"]),
        ("sign_and_discourse_collection", ["sign_sequence", "temple_or_nicodemus_discourse", "samaritan_transition"]),
        ("sign_and_bread_discourse", ["healing_sign", "feeding_sign", "bread_discourse"]),
        ("festival_dispute_discourse", ["festival_setting", "witness_dispute", "symbolic_saying_sequence"]),
        ("sign_and_shepherd_discourse", ["blindness_sign", "shepherd_discourse", "festival_transition"]),
        ("resurrection_sign_and_teaching", ["lazarus_sign", "anointing_or_entry", "teaching_transition"]),
        ("farewell_discourse", ["footwashing_or_meal", "departure_discourse", "command_or_paraclete"]),
        ("farewell_prayer_and_arrest", ["prayer_discourse", "unity_or_mission", "arrest_transition"]),
        ("passion_trial_and_crucifixion", ["trial_dialogue", "crucifixion", "burial_closure"]),
        ("resurrection_appearance_narrative", ["empty_tomb", "appearance_sequence", "epilogue_closure"]),
    ],
}


def refine(rows: list[dict], book: str) -> int:
    changed = 0
    forms = FORMS[book]
    for row in rows:
        if row.get("book") != book:
            continue
        idx = int(row["chunk_index_in_book"])
        if idx < 1 or idx > len(forms):
            continue
        form, seams = forms[idx - 1]
        row["literature_type_guess"] = form
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained provisionally; narrative, discourse, parable/sign, passion, and closure signals are seam leads requiring independent Koine review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Koine Greek aspect, participial chains, quotation scope, discourse particles, and translation paragraphing require source-level review"]
        row["original_language_translation_holds"] = ["CNTR/SBLGNT/UGNT comparison required; English headings and harmonized Gospel ordering cannot decide seams"]
        row["cross_reference_clusters"] = ["Synoptic and Johannine parallels, scriptural quotations, and internal Gospel echoes are evidence-only relation leads"]
        row["cross_reference_holds"] = ["Do not harmonize Gospel accounts or use later canonical reception as boundary authority"]
        row["hard_passage_forecast"] = ["Embedded quotations, parable boundaries, discourse resumption, and passion/resurrection sequencing may cross modern chapter edges"]
        row["red_team_questions"] = ["Does each seam survive removal of English headings and chapter numbers?", "Is a quotation, parable, or discourse voice being mistaken for an authorial boundary?"]
        row["red_team_premortem_holds"] = ["Do not convert Gospel literary labels into theological conclusions; preserve Greek textual and ending variants as holds"]
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
    rows_by_path = {}
    for path in PATHS:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        for book in FORMS:
            changed = refine(rows, book)
            if changed:
                reports.append({"path": str(path), "book": book, "rows_changed": changed})
        path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"books": list(FORMS), "wave": WAVE, "reports": reports, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
