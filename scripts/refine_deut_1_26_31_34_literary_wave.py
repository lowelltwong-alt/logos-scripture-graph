#!/usr/bin/env python3
"""Refine Deuteronomy metadata without changing any outer candidate spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Deut/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "deut_1_26_31_34_literary_wave.v1"

DETAILS = {
    1: ("retrospective_wilderness_address", "Retrospective address: departure, route, and refusal episode", ["address_opening", "recollection_sequence", "speech_to_narrative_turn"]),
    2: ("retrospective_wilderness_address", "Retrospective address: wilderness itinerary and emissary episode", ["itinerary_notice", "reported_speech", "episode_closure"]),
    3: ("retrospective_wilderness_address", "Retrospective address: conflict, conquest report, and allocation notice", ["battle_report", "request_response", "allocation_closure"]),
    4: ("retrospective_exhortation", "Retrospective address: hearing, teaching, warning, and covenant appeal", ["historical_recollection", "instruction_turn", "warning_and_appeal"]),
    5: ("covenant_exhortation", "Covenant recitation and imperative exhortation", ["covenant_recitation", "imperative_sequence", "speech_closure"]),
    6: ("covenant_exhortation", "Instruction, confession, and household-teaching exhortation", ["confession_formula", "instruction_sequence", "household_address"]),
    7: ("covenant_exhortation", "Covenant allegiance exhortation and separation warnings", ["command_cluster", "warning_turn", "promise_or_closure_formula"]),
    8: ("covenant_exhortation", "Wilderness-memory exhortation and testing reflection", ["memory_recap", "testing_exhortation", "warning_closure"]),
    9: ("covenant_exhortation", "Rebellion recollection and intercession narrative", ["accusation_or_recollection", "intercession_report", "tablets_or_covenant_turn"]),
    10: ("covenant_exhortation", "Covenant restoration, service, and circumcision-of-heart exhortation", ["restoration_notice", "service_exhortation", "blessing_or_appeal"]),
    11: ("covenant_exhortation", "Love-and-obedience exhortation with blessing/curse alternatives", ["address_shift", "refrain_or_condition", "blessing_curse_transition"]),
    12: ("covenant_stipulation_collection", "Centralization and worship stipulation collection", ["stipulation_opening", "case_or_exception", "instruction_closure"]),
    13: ("covenant_stipulation_collection", "Loyalty-testing and false-prophet case-law cluster", ["case_law_opening", "test_or_verdict", "sanction_closure"]),
    14: ("covenant_stipulation_collection", "Holiness, food, tithe, and household stipulation cluster", ["classification_list", "ritual_or_social_case", "tithe_transition"]),
    15: ("covenant_stipulation_collection", "Debt release, servant release, and firstborn stipulations", ["release_formula", "conditional_case", "firstborn_closure"]),
    16: ("covenant_stipulation_collection", "Festival calendar and judicial/leadership stipulation cluster", ["festival_sequence", "justice_instruction", "leadership_transition"]),
    17: ("covenant_stipulation_collection", "Sacrifice, adjudication, kingship, and authority cases", ["sacrifice_case", "court_procedure", "royal_instruction"]),
    18: ("covenant_stipulation_collection", "Priestly support and authorized-prophet discernment instructions", ["provision_case", "forbidden_practice_list", "prophet_test"]),
    19: ("covenant_stipulation_collection", "Cities of refuge, testimony, and boundary-law cases", ["refuge_provision", "witness_procedure", "boundary_or_restitution_case"]),
    20: ("covenant_stipulation_collection", "Warfare address, exemptions, siege, and city-case instructions", ["war_speech", "exemption_list", "siege_case"]),
    21: ("covenant_stipulation_collection", "Unsolved death, family status, and inheritance case-law cluster", ["ritual_case", "household_case", "inheritance_closure"]),
    22: ("covenant_stipulation_collection", "Neighbor, garment, property, and sexual-conduct case-law cluster", ["neighbor_duty", "property_case", "household_or_sexual_case"]),
    23: ("covenant_stipulation_collection", "Assembly access, camp purity, fugitive, and economic cases", ["assembly_rule", "camp_purity", "social_or_economic_case"]),
    24: ("covenant_stipulation_collection", "Marriage, pledge, labor, and vulnerable-person case-law cluster", ["marriage_case", "pledge_or_labor_case", "gleaning_or_vulnerable_person_closure"]),
    25: ("covenant_stipulation_collection", "Judicial penalty, levirate, weights, and remembrance cases", ["judicial_case", "family_case", "ethical_measure_closure"]),
    26: ("covenant_stipulation_collection", "Firstfruits confession and tithe declaration closure", ["offering_instruction", "confession_formula", "declaration_closure"]),
    31: ("succession_document_and_prose_frame", "Succession address, document deposit, witness, and song introduction", ["succession_speech", "document_notice", "song_introduction"]),
    32: ("embedded_song_poetry", "Embedded song with stanza/refrain and rare-diction holds", ["song_opening", "stanza_or_refrain", "song_closure"]),
    33: ("tribal_blessing_poetry", "Tribal blessing poem with formulaic tribal units", ["blessing_opening", "tribal_unit_sequence", "poetic_closure"]),
    34: ("death_notice_and_epilogue_frame", "Death notice, succession closure, and epilogue frame", ["mountain_scene", "death_notice", "succession_or_epilogue_closure"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Deut":
            continue
        chapter = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if chapter not in DETAILS or 27 <= chapter <= 30:
            continue
        form, title, seams = DETAILS[chapter]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained; Hebrew discourse/formula and local form transitions are metadata leads only and require independent review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Hebrew discourse particles, formula scope, legal condition-action-result syntax, and poetry/case-law transitions require source-level review"]
        row["original_language_translation_holds"] = ["OSHB and UXLC comparison required; English headings and punctuation cannot decide seams"]
        row["cross_reference_clusters"] = ["Internal covenant, song, blessing, and legal-form parallels are retrieval leads only"]
        row["cross_reference_holds"] = ["Do not use Decalogue/covenant/poetic or later canonical echoes as boundary authority"]
        row["hard_passage_forecast"] = ["Formulaic repetition, embedded declarations, and legal condition-action-result chains may cross chapter edges"]
        row["red_team_questions"] = ["Can the proposed internal seam survive removal of English headings and chapter numbers?", "Does it preserve the local speaker/form and legal or poetic closure?"]
        row["red_team_premortem_holds"] = ["No seam based solely on English chapter or heading; preserve 32:8-9 rare-diction/textual-variant uncertainty as a hold"]
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
    counts = []
    for path in PATHS:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        changed = refine(rows)
        path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
        counts.append({"path": str(path), "rows_changed": changed})
    print(json.dumps({"book": "Deut", "wave": WAVE, "rows_changed": counts, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
