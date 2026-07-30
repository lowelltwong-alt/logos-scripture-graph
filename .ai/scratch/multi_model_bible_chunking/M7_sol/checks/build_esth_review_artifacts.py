from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Esth",
        expected_sha="6eb18e83e90ce5fb39938867c9288d3fa2c2bb19800157a94bac7c4429d06998",
        roles=(
            ("hebrew", "esth-primary-hebrew-textual-20260723-a", "Hebrew_Persian_terms_MT_LXX_additions_textual_specialist"),
            ("literary", "esth-primary-literary-20260723-b", "banquet_decree_recognition_irony_reversal_conflict_and_festival_specialist"),
            ("canonical", "esth-primary-canonical-20260723-c", "canonical_relations_ethics_authority_and_premortem_specialist"),
        ),
        peer_attempt="esth-peer-crosscheck-20260723-d",
        boss_attempt="esth-boss-adjudicator-20260723-e",
        post_attempt="esth-post-resolution-checker-20260723-f",
        reviewer_hint="human_or_external_ai_Hebrew_Persian_court_MT_LXX_Esther_additions_Purim_and_violence_ethics_specialist",
        relation_specs=(
            ("001", ["M7_sol-Esth-001", "M7_sol-Esth-002"], ["Gen.39.1-Gen.41.57", "Dan.1.1-Dan.6.28"], "court_banquet_refusal_search_selection_and_exile_court_relations"),
            ("002", ["M7_sol-Esth-003"], ["Gen.40.1-Gen.41.57", "Eccl.8.1-Eccl.8.17"], "assassination_discovery_record_and_later_recognition_relations"),
            ("003", ["M7_sol-Esth-004", "M7_sol-Esth-005"], ["Exod.17.8-Exod.17.16", "1Sam.15.1-1Sam.15.35"], "Haman_Amalek_reception_edict_mourning_dialogue_and_fast_relations"),
            ("004", [f"M7_sol-Esth-{i:03d}" for i in range(6, 9)], ["Gen.41.1-Gen.41.57", "Dan.5.1-Dan.6.28", "Prov.16.1-Prov.16.33"], "approach_banquets_insomnia_honor_exposure_execution_and_reversal_relations"),
            ("005", ["M7_sol-Esth-009", "M7_sol-Esth-010"], ["Exod.17.8-Exod.17.16", "Deut.25.17-Deut.25.19", "1Sam.15.1-1Sam.15.35"], "counter_edict_conflict_rest_spoil_and_Amalek_reception_relations"),
            ("006", ["M7_sol-Esth-011", "M7_sol-Esth-012"], ["Exod.12.1-Exod.13.16", "Deut.16.1-Deut.16.17"], "Purim_memorial_letters_feast_practice_and_closing_office_relations"),
        ),
    )
