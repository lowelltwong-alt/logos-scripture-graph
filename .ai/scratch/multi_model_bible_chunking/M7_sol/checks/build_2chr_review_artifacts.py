from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="2Chr",
        expected_sha="2ace41a11eebbad9b68040807a67d6ee3519e5bed194652f7168e06f8ef2def7",
        roles=(
            ("hebrew", "2chr-primary-hebrew-20260723-a", "original_language_translation_and_versification_specialist"),
            ("literary", "2chr-primary-literary-20260723-b", "literary_form_scene_speech_register_and_prayer_specialist"),
            ("canonical", "2chr-primary-canonical-20260723-c", "canonical_relations_and_premortem_specialist"),
        ),
        peer_attempt="2chr-peer-crosscheck-20260723-d",
        boss_attempt="2chr-boss-adjudicator-20260723-e",
        post_attempt="2chr-post-resolution-checker-20260723-f",
        reviewer_hint="human_or_external_ai_Hebrew_Chronicles_WEB_MT_versification_regnal_oracle_cultic_register_and_parallel_account_specialist",
        relation_specs=(
            ("001", [f"M7_sol-2Chr-{i:03d}" for i in range(1, 14)], ["1Chr.28.1-1Chr.29.30", "1Kgs.1.1-1Kgs.11.43", "Ps.72.1-Ps.72.20", "Ps.132.1-Ps.132.18"], "Solomon_accession_temple_dedication_royal_and_wisdom_relations"),
            ("002", [f"M7_sol-2Chr-{i:03d}" for i in range(14, 20)], ["1Kgs.12.1-1Kgs.14.31"], "Rehoboam_division_fortification_invasion_and_regnal_relations"),
            ("003", [f"M7_sol-2Chr-{i:03d}" for i in range(20, 24)], ["1Kgs.15.1-1Kgs.16.34"], "Abijah_Asa_oracle_reform_conflict_and_regnal_relations"),
            ("004", [f"M7_sol-2Chr-{i:03d}" for i in range(24, 30)], ["1Kgs.22.1-1Kgs.22.53", "Ps.83.1-Ps.83.18"], "Jehoshaphat_teaching_judgment_battle_prayer_and_prophetic_relations"),
            ("005", [f"M7_sol-2Chr-{i:03d}" for i in range(30, 37)], ["2Kgs.8.1-2Kgs.14.22"], "Jehoram_Ahaziah_Athaliah_Joash_Amaziah_parallel_regnal_relations"),
            ("006", [f"M7_sol-2Chr-{i:03d}" for i in range(37, 42)], ["2Kgs.14.21-2Kgs.17.41", "Isa.7.1-Isa.12.6"], "Uzziah_Jotham_Ahaz_regnal_prophetic_and_cultic_relations"),
            ("007", [f"M7_sol-2Chr-{i:03d}" for i in range(42, 46)], ["2Kgs.18.1-2Kgs.18.12"], "Hezekiah_temple_cleansing_passover_and_provision_relations"),
            ("008", [f"M7_sol-2Chr-{i:03d}" for i in range(46, 48)], ["2Kgs.18.13-2Kgs.20.21", "Isa.36.1-Isa.39.8"], "Hezekiah_siege_prayer_deliverance_illness_and_envoy_relations"),
            ("009", [f"M7_sol-2Chr-{i:03d}" for i in range(48, 54)], ["2Kgs.21.1-2Kgs.23.30", "Jer.22.1-Jer.22.30"], "Manasseh_Amon_Josiah_book_covenant_passover_and_Neco_relations"),
            ("010", [f"M7_sol-2Chr-{i:03d}" for i in range(54, 59)], ["2Kgs.23.31-2Kgs.25.30", "Jer.24.1-Jer.29.32", "Jer.39.1-Jer.52.34", "Ezra.1.1-Ezra.1.4"], "final_kings_exile_land_rest_and_Cyrus_Ezra_bridge_relations"),
        ),
    )
