from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Song",
        expected_sha="d09352901c58f0b543f846eb5471a858f7b0154ec1980bd105d7e960f3d325c7",
        roles=(
            (
                "hebrew",
                "song-primary-hebrew-speaker-20260723-a",
                "Hebrew_lyric_gender_number_speaker_versification_and_translation_specialist",
            ),
            (
                "literary",
                "song-primary-literary-20260723-b",
                "lyric_dialogue_search_praise_garden_invitation_refrain_and_closure_specialist",
            ),
            (
                "canonical",
                "song-primary-canonical-20260723-c",
                "canonical_relations_gender_drama_erotic_allegory_authority_and_premortem_specialist",
            ),
        ),
        peer_attempt="song-peer-crosscheck-20260723-d",
        boss_attempt="song-boss-adjudicator-20260723-e",
        post_attempt="song-post-resolution-checker-20260723-f",
        reviewer_hint=(
            "human_or_external_ai_Biblical_Hebrew_Song_lyric_gender_number_textual_"
            "criticism_ancient_love_poetry_and_Jewish_reception_specialist"
        ),
        relation_specs=(
            (
                "001",
                ["M7_sol-Song-001", "M7_sol-Song-002", "M7_sol-Song-003"],
                ["Gen.1.26-Gen.2.25", "Ps.45.1-Ps.45.17", "Prov.5.1-Prov.5.23"],
                "title_opening_desire_vineyard_praise_presence_and_first_adjuration_relations",
            ),
            (
                "002",
                ["M7_sol-Song-004", "M7_sol-Song-005", "M7_sol-Song-006"],
                ["Gen.24.1-Gen.24.67", "Ps.19.1-Ps.19.14", "Ps.72.1-Ps.72.20"],
                "spring_invitation_night_search_procession_and_royal_display_relations",
            ),
            (
                "003",
                ["M7_sol-Song-007", "M7_sol-Song-008", "M7_sol-Song-009"],
                ["Gen.2.4-Gen.3.24", "Ps.42.1-Ps.43.5", "Prov.31.10-Prov.31.31"],
                "body_praise_garden_invitation_failed_encounter_search_and_belonging_relations",
            ),
            (
                "004",
                ["M7_sol-Song-010", "M7_sol-Song-011", "M7_sol-Song-012", "M7_sol-Song-013"],
                ["Gen.29.1-Gen.30.24", "Ps.45.1-Ps.45.17", "Prov.5.1-Prov.5.23"],
                "renewed_praise_garden_return_body_catalogue_country_invitation_and_adjuration_relations",
            ),
            (
                "005",
                ["M7_sol-Song-014"],
                ["Gen.2.18-Gen.2.25", "Deut.6.1-Deut.6.25", "Ps.63.1-Ps.63.11"],
                "emergence_awakening_seal_love_death_fire_and_unbuyable_love_relations",
            ),
            (
                "006",
                ["M7_sol-Song-015", "M7_sol-Song-016", "M7_sol-Song-017"],
                ["Gen.29.1-Gen.30.24", "Isa.5.1-Isa.5.30", "Ps.80.1-Ps.80.19"],
                "sister_wall_vineyard_economic_contrast_garden_voice_and_final_call_relations",
            ),
        ),
    )
