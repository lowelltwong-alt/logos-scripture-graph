from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Isa",
        expected_sha="615feb5682bcfc4a9b2b44ec5753a76191e63e83f1e4cd37ff2a5a382a424376",
        roles=(
            (
                "hebrew",
                "isa-primary-hebrew-textual-20260723-a",
                "Hebrew_prophetic_form_MT_LXX_DSS_wordplay_versification_and_translation_specialist",
            ),
            (
                "literary",
                "isa-primary-literary-20260723-b",
                "vision_oracle_sign_woe_nation_prose_disputation_servant_Zion_and_prayer_specialist",
            ),
            (
                "canonical",
                "isa-primary-canonical-20260723-c",
                "canonical_relations_identity_strata_fulfillment_authority_and_premortem_specialist",
            ),
        ),
        peer_attempt="isa-peer-crosscheck-20260723-d",
        boss_attempt="isa-boss-adjudicator-20260723-e",
        post_attempt="isa-post-resolution-checker-20260723-f",
        reviewer_hint=(
            "human_or_external_ai_Biblical_Hebrew_Isaiah_prophetic_form_DSS_LXX_MT_"
            "textual_criticism_ANE_history_and_Jewish_reception_specialist"
        ),
        relation_specs=(
            ("001", [f"M7_sol-Isa-{i:03d}" for i in range(1, 11)], ["Deut.28.1-Deut.32.47", "Ps.50.1-Ps.50.23", "Mic.1.1-Mic.5.15"], "opening_vision_lawsuit_Zion_Day_vineyard_and_woe_relations"),
            ("002", [f"M7_sol-Isa-{i:03d}" for i in range(11, 19)], ["2Kgs.15.1-2Kgs.20.21", "2Chr.26.1-2Chr.32.33", "Ps.46.1-Ps.48.14"], "vision_commission_sign_Immanuel_Assyria_child_remnant_and_thanksgiving_relations"),
            ("003", [f"M7_sol-Isa-{i:03d}" for i in range(19, 33)], ["Gen.10.1-Gen.11.32", "2Kgs.14.1-2Kgs.20.21", "Jer.46.1-Jer.51.64"], "Babylon_nation_city_oracle_taunt_lament_sign_and_watchman_relations"),
            ("004", [f"M7_sol-Isa-{i:03d}" for i in range(33, 37)], ["Gen.6.1-Gen.9.29", "Exod.24.1-Exod.24.18", "Ps.96.1-Ps.99.9"], "world_judgment_city_feast_song_resurrection_image_vineyard_and_gathering_relations"),
            ("005", [f"M7_sol-Isa-{i:03d}" for i in range(37, 47)], ["Exod.14.1-Exod.15.27", "Deut.28.1-Deut.30.20", "Ps.46.1-Ps.48.14"], "woe_disputation_cornerstone_Ariel_Egypt_Zion_Edom_and_wilderness_restoration_relations"),
            ("006", [f"M7_sol-Isa-{i:03d}" for i in range(47, 51)], ["2Kgs.18.1-2Kgs.20.21", "2Chr.29.1-2Chr.32.33", "Ps.75.1-Ps.76.12"], "Assyrian_embassy_prayer_deliverance_illness_sign_and_Babylon_envoy_relations"),
            ("007", [f"M7_sol-Isa-{i:03d}" for i in range(51, 64)], ["Gen.1.1-Gen.2.25", "Exod.1.1-Exod.15.27", "Deut.4.1-Deut.6.25"], "comfort_creator_idol_trial_servant_Cyrus_Babylon_and_new_exodus_relations"),
            ("008", [f"M7_sol-Isa-{i:03d}" for i in range(64, 73)], ["Gen.22.1-Gen.22.24", "Exod.12.1-Exod.15.27", "Ps.22.1-Ps.22.31"], "servant_Zion_disciple_awake_exodus_suffering_restoration_and_invitation_relations"),
            ("009", [f"M7_sol-Isa-{i:03d}" for i in range(73, 79)], ["Deut.10.1-Deut.16.22", "Ps.51.1-Ps.51.19", "Ps.72.1-Ps.72.20"], "community_inclusion_watchmen_idolatry_fast_justice_confession_warrior_and_redeemer_relations"),
            ("010", [f"M7_sol-Isa-{i:03d}" for i in range(79, 82)], ["Ps.48.1-Ps.48.14", "Ps.87.1-Ps.87.7", "Zech.8.1-Zech.8.23"], "Zion_light_nations_pilgrimage_spirit_proclamation_watchmen_and_highway_relations"),
            ("011", [f"M7_sol-Isa-{i:03d}" for i in range(82, 89)], ["Gen.1.1-Gen.3.24", "Deut.32.1-Deut.33.29", "Ps.74.1-Ps.74.23"], "warrior_remembrance_communal_lament_divine_answer_servants_new_creation_and_final_worship_relations"),
        ),
    )
