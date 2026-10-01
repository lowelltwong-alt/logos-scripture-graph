from build_review_artifacts_generic import build

if __name__ == "__main__":
    build(
        book="1Chr",
        expected_sha="91afe4d1197d7fbdc430c7030d24d6cfcc108be82669029550f99daea7e34465",
        roles=(
            ("hebrew","1chr-primary-hebrew-20260722-a","original_language_translation_and_register_specialist"),
            ("literary","1chr-primary-literary-20260722-b","literary_form_and_list_function_specialist"),
            ("canonical","1chr-primary-canonical-20260722-c","canonical_intertext_and_premortem_specialist"),
        ),
        peer_attempt="1chr-peer-crosscheck-20260722-d",
        boss_attempt="1chr-boss-adjudicator-20260722-e",
        post_attempt="1chr-post-resolution-checker-20260722-f",
        reviewer_hint="human_or_external_ai_Hebrew_genealogy_Chronicles_textual_versification_cultic_register_poetry_and_ancient_context_specialist",
        relation_specs=(
            ("001",["M7_sol-1Chr-001","M7_sol-1Chr-002","M7_sol-1Chr-003","M7_sol-1Chr-004","M7_sol-1Chr-005","M7_sol-1Chr-006"],["Gen.5.1-Gen.5.32","Gen.10.1-Gen.11.32","Gen.25.1-Gen.25.34","Gen.36.1-Gen.36.43"],"primeval_Abraham_Esau_Edom_ancestry_relations"),
            ("002",["M7_sol-1Chr-007","M7_sol-1Chr-008","M7_sol-1Chr-009","M7_sol-1Chr-010","M7_sol-1Chr-011"],["Gen.29.31-Gen.30.24","Gen.46.1-Gen.46.27","Ruth.4.18-Ruth.4.22"],"Israel_Judah_Perez_David_and_clan_relations"),
            ("003",["M7_sol-1Chr-016","M7_sol-1Chr-017","M7_sol-1Chr-018","M7_sol-1Chr-019","M7_sol-1Chr-020","M7_sol-1Chr-021"],["Num.26.1-Num.26.65","Josh.13.1-Josh.13.33","Josh.19.1-Josh.19.9","2Kgs.15.29-2Kgs.17.6"],"tribal_settlement_transjordan_war_and_exile_relations"),
            ("004",["M7_sol-1Chr-022","M7_sol-1Chr-023","M7_sol-1Chr-024","M7_sol-1Chr-025","M7_sol-1Chr-026","M7_sol-1Chr-027"],["Exod.6.16-Exod.6.25","Num.3.1-Num.4.49","Num.35.1-Num.35.8","Josh.21.1-Josh.21.45","Neh.11.1-Neh.12.47"],"Levitical_priestly_cultic_and_city_register_relations"),
            ("005",["M7_sol-1Chr-035","M7_sol-1Chr-036","M7_sol-1Chr-037","M7_sol-1Chr-038","M7_sol-1Chr-039","M7_sol-1Chr-040","M7_sol-1Chr-041","M7_sol-1Chr-042"],["1Sam.9.1-1Sam.31.13","Neh.11.1-Neh.11.36"],"Saul_ancestry_resettlement_office_and_terminal_battle_relations"),
            ("006",["M7_sol-1Chr-043","M7_sol-1Chr-044","M7_sol-1Chr-045","M7_sol-1Chr-046","M7_sol-1Chr-047"],["1Sam.22.1-1Sam.30.31","2Sam.5.1-2Sam.5.10","2Sam.23.8-2Sam.23.39"],"David_accession_supporters_and_warrior_relations"),
            ("007",["M7_sol-1Chr-048","M7_sol-1Chr-049","M7_sol-1Chr-050","M7_sol-1Chr-051","M7_sol-1Chr-052","M7_sol-1Chr-053"],["2Sam.6.1-2Sam.6.23","Ps.96.1-Ps.96.13","Ps.105.1-Ps.105.15","Ps.106.1-Ps.106.48"],"ark_transport_installation_worship_and_psalm_relations"),
            ("008",["M7_sol-1Chr-054"],["2Sam.7.1-2Sam.7.29","Ps.89.1-Ps.89.52","Ps.132.1-Ps.132.18"],"Nathan_oracle_David_prayer_and_later_Davidic_relations"),
            ("009",["M7_sol-1Chr-061","M7_sol-1Chr-062","M7_sol-1Chr-063","M7_sol-1Chr-064"],["2Sam.24.1-2Sam.24.25","2Chr.3.1-2Chr.3.1"],"census_plague_thresing_floor_and_temple_site_relations"),
            ("010",["M7_sol-1Chr-065","M7_sol-1Chr-066","M7_sol-1Chr-067","M7_sol-1Chr-068","M7_sol-1Chr-069","M7_sol-1Chr-070","M7_sol-1Chr-071","M7_sol-1Chr-072","M7_sol-1Chr-073","M7_sol-1Chr-074","M7_sol-1Chr-075","M7_sol-1Chr-076","M7_sol-1Chr-077","M7_sol-1Chr-078","M7_sol-1Chr-079","M7_sol-1Chr-080","M7_sol-1Chr-081","M7_sol-1Chr-082","M7_sol-1Chr-083","M7_sol-1Chr-084","M7_sol-1Chr-085","M7_sol-1Chr-086","M7_sol-1Chr-087"],["Exod.25.1-Exod.31.18","Num.3.1-Num.4.49","1Kgs.1.1-1Kgs.8.66","Ezra.2.1-Ezra.3.13","Neh.7.1-Neh.12.47"],"temple_preparation_service_rosters_final_assembly_and_succession_relations"),
        ),
    )
