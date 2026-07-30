from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Jer",
        expected_sha="0a3847d9a0fa160208d0047f78dad18e2455d0ec2438aea9b144f9ea365ace04",
        roles=(
            (
                "hebrew",
                "jer-primary-hebrew-textual-20260723-a",
                "Hebrew_Aramaic_prophetic_form_MT_LXX_DSS_order_variants_wordplay_versification_and_translation_specialist",
            ),
            (
                "canonical",
                "jer-primary-canonical-premortem-20260723-b",
                "canonical_relations_scene_oracle_sign_confession_letter_scroll_nation_oracle_appendix_and_premortem_specialist",
            ),
        ),
        peer_attempt="jer-peer-crosscheck-20260723-c",
        boss_attempt="jer-boss-adjudicator-20260723-d",
        post_attempt="jer-role-separated-postchecker-20260723-f",
        reviewer_hint=(
            "human_or_external_ai_Biblical_Hebrew_Jeremiah_prophetic_form_MT_LXX_DSS_"
            "textual_criticism_ANE_history_and_Jewish_reception_specialist"
        ),
        relation_specs=(
            ("001", [f"M7_sol-Jer-{i:03d}" for i in range(1, 10)], ["Deut.28.1-Deut.32.47", "2Kgs.22.1-2Kgs.23.30", "Hos.1.1-Hos.4.19"], "call_visions_covenant_lawsuit_return_alarm_city_search_siege_and_Josiah_frame_relations"),
            ("002", [f"M7_sol-Jer-{i:03d}" for i in range(10, 18)], ["Exod.20.1-Exod.24.18", "Deut.12.1-Deut.18.22", "Ps.73.1-Ps.73.28"], "temple_sermon_Topheth_lament_idol_contrast_covenant_conspiracy_confession_and_neighbors_relations"),
            ("003", [f"M7_sol-Jer-{i:03d}" for i in range(18, 29)], ["Num.14.1-Num.14.45", "Deut.18.1-Deut.18.22", "2Kgs.23.31-2Kgs.24.20"], "linen_belt_drought_celibacy_potter_smashed_jar_Pashhur_and_royal_oracle_relations"),
            ("004", [f"M7_sol-Jer-{i:03d}" for i in range(29, 39)], ["2Sam.7.1-2Sam.7.29", "2Kgs.24.1-2Kgs.25.30", "Ezek.34.1-Ezek.37.28"], "shepherds_figs_cup_yoke_false_prophets_letter_and_Babylon_relations"),
            ("005", [f"M7_sol-Jer-{i:03d}" for i in range(39, 49)], ["Deut.30.1-Deut.30.20", "Hos.1.1-Hos.3.5", "Ezek.36.1-Ezek.37.28"], "consolation_restoration_Rachel_new_covenant_rebuilding_and_land_purchase_relations"),
            ("006", [f"M7_sol-Jer-{i:03d}" for i in range(49, 60)], ["Exod.24.1-Exod.24.18", "Deut.15.1-Deut.15.23", "2Kgs.24.1-2Kgs.25.30"], "covenant_release_siege_courtyard_rescue_and_Zedekiah_relations"),
            ("007", [f"M7_sol-Jer-{i:03d}" for i in range(60, 72)], ["Deut.31.1-Deut.31.30", "2Kgs.22.1-2Kgs.23.30", "2Kgs.24.1-2Kgs.25.30"], "scroll_reading_burning_rewriting_field_prison_and_city_fall_relations"),
            ("008", [f"M7_sol-Jer-{i:03d}" for i in range(72, 82)], ["2Kgs.25.1-2Kgs.25.30", "Ezek.8.1-Ezek.24.27", "Lam.1.1-Lam.5.22"], "Gedaliah_assassination_remnant_Egypt_flight_Baruch_and_aftermath_relations"),
            ("009", [f"M7_sol-Jer-{i:03d}" for i in range(82, 96)], ["Isa.13.1-Isa.23.18", "Ezek.25.1-Ezek.32.32", "Amos.1.1-Amos.2.16"], "Egypt_Philistia_Moab_Ammon_Edom_Damascus_Kedar_Elam_nation_oracle_relations"),
            ("010", [f"M7_sol-Jer-{i:03d}" for i in range(96, 99)], ["Isa.13.1-Isa.14.23", "Hab.1.1-Hab.3.19", "Rev.17.1-Rev.19.21"], "Babylon_oracle_scroll_sign_and_order_variant_relations"),
            ("011", ["M7_sol-Jer-099"], ["2Kgs.24.18-2Kgs.25.30", "2Chr.36.1-2Chr.36.23", "Lam.1.1-Lam.5.22"], "Jeremiah_52_Kings_parallel_appendix_and_Jehoiachin_release_relations"),
        ),
    )
