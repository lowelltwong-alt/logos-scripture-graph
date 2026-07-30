#!/usr/bin/env python3
"""Build low-confidence, candidate-only literary units for Samuel/Kings.

This deliberately uses chapter-complete spans: the canonical passage inventory
supplies the first/last verse of each chapter, while the hand-reviewed unit
table proposes structural seams.  It does not alter canonical text or claim
authority.  Every row carries the same review holds, including difficult
Hebrew, translation, intertext, and ancient-context cases.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"

# (start chapter, end chapter, title, literary form, difficulty classes, seeds)
UNITS: dict[str, list[tuple[int, int, str, str, list[str], list[str]]]] = {
    "1Sam": [
        (1,1,"Hannah's petition and Samuel's birth","narrative+vow",["vow_language","birth_narrative"],[]),
        (2,2,"Hannah's song and the sanctuary contrast","song+oracle",["poetic_parallelism","lexical_ambiguity"],["Luke.1.46-Luke.1.55"]),
        (3,3,"Samuel's call and prophetic recognition","narrative_call+oracle",["prophetic_call","priestly_terms"],["1Sam.2.27-1Sam.2.36"]),
        (4,4,"Ark capture and Eli's death","battle_report+birth_notice",["ark_narrative","wordplay"],["1Sam.4.1-1Sam.4.22"]),
        (5,6,"The ark among the Philistines and its return","etiological_narrative+ritual",["foreign_cult_context","ritual_terms"],["1Sam.6.1-1Sam.6.21"]),
        (7,7,"Mizpah repentance and Samuel's judging","assembly_narrative+victory_report",["assembly_formula","intertextual_echo"],["Josh.4.1-Josh.4.24"]),
        (8,8,"Israel asks for a king","prophetic_warning+dialogue",["kingship_lexicon","speech_boundaries"],["Deut.17.14-Deut.17.20"]),
        (9,10,"Saul's search, anointing, and public selection","commission+narrative+lot",["anointing_terms","sign_sequences","translation_variants"],["1Sam.8.1-1Sam.8.22"]),
        (11,12,"Jabesh rescue and Samuel's farewell","battle_report+farewell_speech",["covenant_assembly","rhetorical_recap"],["Deut.31.1-Deut.31.30"]),
        (13,14,"Saul and Jonathan at Michmash","battle_report+oath_narrative",["oath_formula","textual_difficulty"],["1Sam.14.24-1Sam.14.46"]),
        (15,15,"Amalek command and Saul's rejection","prophetic_command+dialogue",["herem_vocabulary","obedience_wordplay"],["Deut.25.17-Deut.25.19"]),
        (16,16,"David anointed and brought to Saul","anointing+narrative_transition",["spirit_language","music_terms"],["1Sam.16.1-1Sam.16.23"]),
        (17,17,"David and Goliath","heroic_battle_narrative",["textual_doublets","warrior_terms"],["1Sam.17.1-1Sam.17.58"]),
        (18,19,"Saul's jealousy and David's escapes","court_narrative+lament",["spirit_possession_language","repeated_scene"],["1Sam.19.1-1Sam.19.24"]),
        (20,20,"Jonathan's covenant test","covenant_dialogue+sign",["covenant_terminology","messenger_code"],["1Sam.20.1-1Sam.20.42"]),
        (21,23,"David's fugitivity: Nob, Gath, Keilah, and Ziph","episodic_fugitive_narrative",["priestly_terms","divination_language","geography"],["1Sam.23.1-1Sam.23.29"]),
        (24,24,"David spares Saul in the cave","royal_encounter+oath",["honorifics","oath_language"],["1Sam.24.1-1Sam.24.22"]),
        (25,25,"Nabal and Abigail","wisdom-inflected_narrative",["blessing_formula","gendered_speech"],["1Sam.25.1-1Sam.25.44"]),
        (26,27,"David spares Saul again and joins Philistia","royal_encounter+fugitive_report",["duplicate_narrative","ethnic_terms"],["1Sam.26.1-1Sam.26.25"]),
        (28,28,"Endor and the Saul oracle","necromancy_narrative+oracle",["lexical_ambiguity","medium_term"],["1Sam.28.3-1Sam.28.25"]),
        (29,30,"Philistine rejection and Ziklag recovery","battle_report+lament+inquiry",["inquiry_formula","war_plunder_terms"],["1Sam.30.1-1Sam.30.31"]),
        (31,31,"Saul's death and Jabesh burial","battle_report+burial_notice",["death_formula","chronological_transition"],["2Sam.1.1-2Sam.1.27"]),
    ],
    "2Sam": [
        (1,1,"David's lament for Saul and Jonathan","lament+royal_poem",["poetic_register","proper_names"],["2Sam.1.17-2Sam.1.27"]),
        (2,3,"David in Hebron and Abner's transfer","succession_narrative+court_dialogue",["chronology","covenant_language"],["2Sam.3.1-2Sam.3.39"]),
        (4,5,"Ish-bosheth's murder and David's Jerusalem accession","succession_narrative+royal_installation",["name_forms","political_terms"],["2Sam.5.1-2Sam.5.25"]),
        (6,6,"Ark brought to Jerusalem","processional_ritual+narrative",["ritual_terms","dance_language"],["2Sam.6.1-2Sam.6.23"]),
        (7,7,"Nathan's oracle and David's prayer","royal_oracle+prayer",["covenant_formula","house/seed_terms"],["1Chr.17.1-1Chr.17.27"]),
        (8,10,"David's victories, Mephibosheth, and Ammon war","royal_annals+court_story",["annalistic_style","kinship_terms","war_report"],["2Sam.9.1-2Sam.10.19"]),
        (11,12,"Bathsheba, Uriah, and Nathan's confrontation","court_narrative+prophetic_parable",["legal_parable","wordplay","sexual_ethics_terms"],["Ps.51.1-Ps.51.19"]),
        (13,14,"Amnon and Tamar; Absalom's return","court_tragedy+reconciliation",["kinship_lexicon","narrative_time"],["2Sam.13.1-2Sam.14.33"]),
        (15,16,"Absalom's revolt and David's flight","revolt_narrative+lament",["loyalty_terms","counsel_speech"],["2Sam.15.1-2Sam.16.14"]),
        (17,17,"Competing counsel and the Jordan crossing","counsel_dialogue+flight_report",["counsel_terminology","messenger_route"],["2Sam.17.1-2Sam.17.29"]),
        (18,19,"Absalom's death and David's lament/restoration","battle_report+lament+succession",["lament_form","restoration_formula"],["2Sam.18.1-2Sam.19.8"]),
        (20,20,"Sheba's revolt","royal_restoration+siege_report",["tribal_politics","rebellion_formula"],["2Sam.19.9-2Sam.20.26"]),
        (21,21,"Gibeonite famine and giant-war notices","annalistic_notice+war_list",["bloodguilt_terms","genealogical_forms"],["2Sam.21.1-2Sam.21.22"]),
        (22,22,"David's song of deliverance","song+royal_testimony",["poetic_parallelism","textual_parallel"],["Ps.18.1-Ps.18.50"]),
        (23,23,"David's last words and mighty men","royal_speech+hero_list",["poetic_register","proper_name_forms"],["2Sam.23.1-2Sam.23.39"]),
        (24,24,"Census, plague, and altar purchase","annalistic_narrative+ritual_resolution",["census_terms","agency_language","textual_parallel"],["1Chr.21.1-1Chr.21.30"]),
    ],
    "1Kgs": [
        (1,2,"Solomon's succession and consolidation","succession_narrative+royal_charge",["chronology","legal_execution_terms"],["1Kgs.1.1-1Kgs.2.46"]),
        (3,4,"Solomon's wisdom, judgment, and administration","wisdom_narrative+court_list",["wisdom_terms","administrative_lists"],["1Kgs.3.1-1Kgs.3.28"]),
        (5,7,"Temple preparations and construction","building_report+royal_annals",["technical_lexicon","measurements","loanwords"],["1Kgs.5.1-1Kgs.7.51"]),
        (8,8,"Temple dedication and prayer","ritual_procession+dedicatory_prayer",["prayer_forms","ark_language","theophany_terms"],["1Kgs.8.1-1Kgs.8.66"]),
        (9,10,"Covenant warning, projects, and the queen of Sheba","royal_oracle+court_report",["conditional_formula","international_titles"],["2Chr.9.1-2Chr.9.31"]),
        (11,11,"Solomon's apostasy and adversaries","annalistic_judgment+succession_notice",["foreign_deity_names","judgment_formula"],["1Kgs.11.1-1Kgs.11.43"]),
        (12,12,"Kingdom division and rival sanctuaries","assembly_dialogue+cultic_foundation",["political_speech","cultic_vocabulary"],["1Kgs.12.1-1Kgs.12.33"]),
        (13,13,"Man of God against Bethel altar","prophetic_sign_narrative",["prophetic_formula","deception_dialogue"],["1Kgs.13.1-1Kgs.13.34"]),
        (14,16,"Jeroboam/Rehoboam through Omri and Ahab","royal_annals+dynastic_notice",["formulaic_annals","name_etymologies"],["1Kgs.14.1-1Kgs.16.34"]),
        (17,17,"Elijah and the widow of Zarephath","prophetic_narrative+miracle",["food_terms","prophetic_word_formula"],["1Kgs.17.1-1Kgs.17.24"]),
        (18,18,"Carmel contest and rain","prophetic_contest+narrative",["mockery_register","altar_ritual"],["1Kgs.18.1-1Kgs.18.46"]),
        (19,19,"Elijah at Horeb and Elisha's call","theophany+commission",["sound_imagery","commission_formula"],["1Kgs.19.1-1Kgs.19.21"]),
        (20,20,"Ahab and Aram wars","battle_report+prophetic_judgment",["war_terms","unnamed_prophet"],["1Kgs.20.1-1Kgs.20.43"]),
        (21,21,"Naboth's vineyard","court_narrative+prophetic_oracle",["land_law","false_witness_terms"],["1Kgs.21.1-1Kgs.21.29"]),
        (22,22,"Micaiah, Ahab's death, and Jehoshaphat/Ahaziah notices","prophetic_council+battle_report+annals",["heavenly_council","prophetic_speech","chronology"],["1Kgs.22.1-1Kgs.22.54"]),
    ],
    "2Kgs": [
        (1,1,"Ahaziah and Elijah's fire narratives","prophetic_judgment+narrative",["fire_theophany","messenger_formula"],["2Kgs.1.1-2Kgs.1.18"]),
        (2,2,"Elijah's ascent and Elisha succession","succession_narrative+miracle",["mantle_symbolism","prophetic_spirit_terms"],["2Kgs.2.1-2Kgs.2.25"]),
        (3,3,"Moab campaign and prophetic intervention","battle_report+prophetic_oracle",["water_ritual","war_curse_terms"],["2Kgs.3.1-2Kgs.3.27"]),
        (4,4,"Elisha's household and public miracles","miracle_cycle+prophetic_narrative",["miracle_formula","hospitality_terms"],["2Kgs.4.1-2Kgs.4.44"]),
        (5,5,"Naaman and Gehazi","healing_narrative+judgment",["purity_language","servant_speech"],["Luke.4.24-Luke.4.27"]),
        (6,7,"Prophetic signs, siege, and Samaria's deliverance","miracle+siege_report",["chariot_imagery","famine_lexicon","chronology"],["2Kgs.6.1-2Kgs.7.20"]),
        (8,8,"Shunammite restoration, Hazael, and Judah's notices","court_report+prophetic_oracle+royal_annals",["land_restoration_terms","oracle_ambiguity","name_forms"],["2Kgs.8.1-2Kgs.8.29"]),
        (9,10,"Jehu's anointing and purge","coup_narrative+royal_annals",["anointing_formula","rhetorical_purge","proper_names"],["2Kgs.9.1-2Kgs.10.36"]),
        (11,12,"Athaliah's overthrow and Joash's temple repair","palace_coup+temple_report",["covenant_assembly","repair_accounts"],["2Kgs.11.1-2Kgs.12.21"]),
        (13,13,"Jehoahaz/Jehoash and Elisha's death","royal_annals+prophetic_epilogue",["annalistic_formula","burial_notice"],["2Kgs.13.1-2Kgs.13.25"]),
        (14,15,"Amaziah through the northern dynastic succession","royal_annals+chronological_notices",["synchronism_formula","genealogies"],["2Kgs.14.1-2Kgs.15.38"]),
        (16,17,"Ahaz and the fall of Samaria","royal_annals+exile_explanation",["cultic_terms","deportation_formula","etiology"],["2Kgs.17.1-2Kgs.17.41"]),
        (18,20,"Hezekiah, Sennacherib, and healing","siege_report+prophetic_oracle+court_notice",["Assyrian_titles","taunt_speech","chronology"],["2Kgs.18.1-2Kgs.20.21"]),
        (21,21,"Manasseh and Amon","royal_annals+judgment_oracle",["cultic_vocabulary","bloodguilt_terms"],["2Kgs.21.1-2Kgs.21.26"]),
        (22,23,"Josiah's discovery and reform","temple_discovery+reform_report",["book_of_law_reference","covenant_renewal"],["2Kgs.22.1-2Kgs.23.30"]),
        (23,25,"Final kings, Jerusalem's fall, and Jehoiachin's release","exile_annals+court_epilogue",["deportation_terms","chronological_endings","name_forms"],["2Kgs.23.31-2Kgs.25.30"]),
    ],
}

def load_chapters(book: str) -> dict[int, tuple[int, int]]:
    out: dict[int, tuple[int, int]] = {}
    path = ROOT / "data/canonical/scripture/passages/passages.jsonl"
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if row.get("book") != book:
                continue
            c = int(row["chapter"])
            lo, hi = int(row["verse_start"]), int(row["verse_end"])
            if c not in out:
                out[c] = (lo, hi)
            else:
                out[c] = (min(out[c][0], lo), max(out[c][1], hi))
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("books", nargs="*", default=list(UNITS))
    args = ap.parse_args()
    for book in args.books:
        chapters = load_chapters(book)
        if not chapters:
            raise SystemExit(f"no canonical passages for {book}")
        covered: set[int] = set()
        rows = []
        for idx, (start, end, title, form, diffs, seeds) in enumerate(UNITS[book], 1):
            missing = [c for c in range(start, end + 1) if c not in chapters]
            if missing or any(c in covered for c in range(start, end + 1)):
                raise SystemExit(f"invalid/overlapping unit {book} {start}-{end}: {missing}")
            covered.update(range(start, end + 1))
            lo = chapters[start][0]; hi = chapters[end][1]
            rows.append({
                "model_id": "M7_sol", "book": book,
                "span": f"{book}.{start}.{lo}-{book}.{end}.{hi}",
                "chunk_index_in_book": idx, "working_title": title,
                "literature_type_guess": form,
                "boundary_evidence_refs": ["canonical_passage_identity_only", "whole_bible_role_source_matrix.v1", "historical_books_structural_unit_table.v1"],
                "strong_or_hebrew_tags_used": ["evidence_only", "lexical_review_pending"],
                "wj_or_red_letter_considered": False, "frontier_flag_considered": True,
                "confidence": "low", "decision_id": f"M7_sol-{book}-{idx:03d}",
                "boundary_rationale": "Candidate literary/structural seam based on narrative, speech, song, oracle, annal, or ritual transition; chapter-complete coverage is provisional pending the full B01 role mesh.",
                "difficulty_classes": diffs, "cross_reference_seed_refs": seeds,
                "review_revision": 0, "review_status": "candidate_structural_unit_pending_b01_mesh",
                "review_holds": ["original_language_translation_review", "literary_form_redteam", "canonical_cross_reference_premortem", "ancient_context_gap", "boss_authorization", "external_provider_review", "human_appeal_review"],
                "non_authorizing": True,
            })
        if covered != set(chapters):
            raise SystemExit(f"coverage mismatch {book}: missing {sorted(set(chapters)-covered)} extra {sorted(covered-set(chapters))}")
        out = MODEL / "book_chunks" / book / "chunks.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
        strategy = MODEL / "book_strategy" / f"{book}.md"; strategy.parent.mkdir(parents=True, exist_ok=True)
        strategy.write_text(f"# {book} candidate structural strategy\n\n- candidate_only: true\n- non_authorizing: true\n- units: {len(rows)}\n- exact_chapter_coverage: true\n- confidence: low\n- B01 role mesh: pending\n- ancient-context corpus: explicit gap until qualified\n\nUnits are provisional literary/structural observations only. Difficulty classes and cross-reference seeds identify review targets; they do not establish theology, preferred readings, or authority.\n", encoding="utf-8", newline="\n")
        print(json.dumps({"book": book, "chunks": len(rows), "chapters": len(chapters), "status": "candidate_structural_units_pending_b01_mesh"}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
