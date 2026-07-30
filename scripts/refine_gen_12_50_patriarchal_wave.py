#!/usr/bin/env python3
"""Refine Genesis 12–50 patriarchal/Joseph metadata without changing spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Gen/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "gen_12_50_patriarchal_wave.v1"

DETAILS = {
    12: ("abraham_call_and_migration", "Abram call, migration, land promise, and journey episodes", ["call_formula", "journey_notice", "promise_or_scene_closure"]),
    13: ("land_separation_narrative", "Abram/Lot separation and land-promise reaffirmation", ["quarrel_or_separation", "land_choice", "promise_closure"]),
    14: ("war_and_royal_meeting_narrative", "Regional war, rescue, victory, and royal/priestly meeting", ["battle_report", "rescue_and_return", "royal_meeting"]),
    15: ("covenant_vision_dialogue", "Promise dialogue, ritual vision, and covenant-cutting scene", ["promise_question", "ritual_action", "vision_or_covenant_closure"]),
    16: ("household_surrogate_narrative", "Sarai, Hagar, household conflict, and wilderness encounter", ["household_case", "flight_scene", "divine_encounter"]),
    17: ("covenant_sign_speech", "Covenant sign, naming, household obligation, and promise speech", ["covenant_heading", "sign_instruction", "promise_closure"]),
    18: ("visitor_and_intercession_narrative", "Visitor episode, promise announcement, and intercession dialogue", ["visitor_scene", "announcement", "intercession"]),
    19: ("city_judgment_and_escape_narrative", "City judgment, rescue, escape, and aftermath episodes", ["messenger_scene", "judgment_sequence", "aftermath_closure"]),
    20: ("royal_household_narrative", "Abraham/Abimelech household episode and dream warning", ["royal_encounter", "dream_warning", "restoration_closure"]),
    21: ("birth_and_household_separation", "Isaac birth, household feast, expulsion, and covenant at Beer-sheba", ["birth_announcement", "household_separation", "oath_or_covenant"]),
    22: ("testing_and_provision_narrative", "Testing command, mountain ascent, binding, and provision closure", ["command_and_response", "mountain_ritual", "provision_or_oath_closure"]),
    23: ("burial_purchase_narrative", "Sarah death, mourning, negotiation, and burial purchase", ["death_notice", "negotiation_dialogue", "burial_closure"]),
    24: ("marriage_negotiation_narrative", "Servant mission, oath, family negotiation, and marriage closure", ["mission_and_oath", "family_dialogue", "marriage_closure"]),
    25: ("descendant_and_death_register", "Descendant register, birth-oracle, sibling conflict, and patriarchal death notices", ["genealogy_formula", "birth_oracle", "death_register"]),
    26: ("isaac_sojourn_and_covenant", "Isaac sojourn, wells, conflict, and covenant renewal", ["sojourn_notice", "well_episode", "oath_or_covenant"]),
    27: ("blessing_deception_narrative", "Birthright/blessing deception, discovery, and family response", ["household_plan", "blessing_speech", "discovery_and_response"]),
    28: ("bethel_dream_and_departure", "Departure, dream/ladder vision, vow, and journey closure", ["departure_notice", "dream_vision", "vow_closure"]),
    29: ("jacob_arrival_and_marriage_narrative", "Arrival, household labor, marriage negotiation, and Leah/Rachel sequence", ["arrival_scene", "labor_or_contract", "marriage_transition"]),
    30: ("household_birth_and_competition", "Household births, rivalry, and fertility-name sequence", ["birth_formula", "household_rivalry", "name_or_closure_formula"]),
    31: ("departure_and_covenant_narrative", "Departure from Laban, pursuit, household dispute, and boundary covenant", ["departure_notice", "household_dispute", "boundary_covenant"]),
    32: ("return_and_encounter_narrative", "Return preparation, messenger report, night encounter, and naming", ["return_notice", "encounter_scene", "name_or_blessing_closure"]),
    33: ("reconciliation_narrative", "Meeting with Esau, reconciliation, settlement, and altar notice", ["approach_and_gifts", "reconciliation_dialogue", "settlement_or_altar"]),
    34: ("dinah_and_retribution_narrative", "Dinah episode, negotiation, deception, and retaliatory action", ["abduction_or_conflict", "negotiation", "retaliation_closure"]),
    35: ("bethel_return_and_death_notices", "Bethel return, altar/household purification, births, and deaths", ["return_command", "altar_or_purification", "death_notice"]),
    36: ("esau_genealogy_register", "Esau/Edom genealogy, chiefs, kings, and register closure", ["genealogy_formula", "chief_or_king_list", "register_closure"]),
    37: ("joseph_dream_and_sale_narrative", "Joseph dreams, family conflict, sale, and mourning frame", ["dream_report", "sibling_conflict", "mourning_closure"]),
    38: ("judah_and_tamar_case_narrative", "Judah household, Tamar case, recognition, and birth closure", ["household_case", "legal_or_recognition_turn", "birth_closure"]),
    39: ("joseph_household_and_prison_narrative", "Joseph household service, accusation, and prison transition", ["household_service", "accusation_scene", "prison_closure"]),
    40: ("prison_dream_interpretation", "Cupbearer/baker dreams, interpretations, and remembered promise", ["dream_report", "interpretation_dialogue", "memory_closure"]),
    41: ("pharaoh_dream_and_administration", "Pharaoh dreams, interpretation, appointment, and famine administration", ["royal_dream", "interpretation_and_counsel", "administrative_closure"]),
    42: ("brother_mission_and_accusation", "Famine mission, recognition, accusation, and return conditions", ["mission_notice", "recognition_or_accusation", "return_condition"]),
    43: ("second_brother_mission_narrative", "Benjamin mission, household fear, meal, and concealed-cup setup", ["departure_condition", "meal_scene", "test_setup"]),
    44: ("plea_and_substitution_speech", "Cup discovery, Judah plea, substitution offer, and speech closure", ["accusation_or_discovery", "plea_speech", "substitution_closure"]),
    45: ("recognition_and_reconciliation_speech", "Joseph recognition, reconciliation, provision, and report to Jacob", ["recognition_speech", "reconciliation", "return_report"]),
    46: ("migration_and_divine_assurance", "Jacob departure, divine assurance, family migration, and reunion", ["departure_register", "divine_assurance", "reunion_closure"]),
    47: ("famine_administration_and_blessing", "Famine administration, land transactions, settlement, and patriarchal blessing request", ["administrative_sequence", "land_transaction", "blessing_request"]),
    48: ("adoption_and_blessing_speech", "Ephraim/Manasseh adoption, crossed hands, and blessing speech", ["adoption_ritual", "blessing_gesture", "blessing_closure"]),
    49: ("tribal_blessing_poetry", "Jacob tribal sayings/blessings and death-charge frame", ["deathbed_frame", "tribal_unit_sequence", "poetic_closure"]),
    50: ("burial_and_prose_closure", "Jacob burial, brother fear/reassurance, Joseph death, and book closure", ["mourning_and_burial", "reassurance_speech", "death_and_closure"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Gen":
            continue
        chapter = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if chapter not in DETAILS:
            continue
        form, title, seams = DETAILS[chapter]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained provisionally; narrative, speech, genealogy, dream, legal-case, blessing, and closure signals are seam leads requiring qualified Hebrew review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Hebrew narrative sequencing, kinship/legal vocabulary, dream-report formulae, blessing syntax, and genealogy/register transitions require source-level review"]
        row["original_language_translation_holds"] = ["OSHB/UXLC comparison required; English headings and paragraphing cannot decide seams"]
        row["cross_reference_clusters"] = ["Patriarchal promise, covenant, genealogy, exodus, blessing, and Joseph motifs are evidence-only internal relation leads"]
        row["cross_reference_holds"] = ["Do not use later canonical reuse or theological harmonization as boundary authority"]
        row["hard_passage_forecast"] = ["Dream speech, household/legal cases, genealogical registers, and blessing poetry may cross modern chapter edges"]
        row["red_team_questions"] = ["Does each seam survive removal of English headings and chapter numbers?", "Are legal, genealogical, and speech labels grounded in local signals rather than later interpretation?"]
        row["red_team_premortem_holds"] = ["Do not turn patriarchal promise, election, blessing, or Joseph typology into theological conclusions; preserve Hebrew lexical and textual-variant holds"]
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
    print(json.dumps({"book": "Gen", "wave": WAVE, "rows_changed": reports, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
