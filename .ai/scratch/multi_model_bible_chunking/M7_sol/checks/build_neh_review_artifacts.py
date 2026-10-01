from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Neh",
        expected_sha="d8686deef49f0d82fdff6c2ca819717530d8fb63b05e6d07c72a4b71708c1253",
        roles=(
            ("hebrew", "neh-primary-hebrew-20260723-a", "Hebrew_translation_WEB_MT_versification_memoir_and_register_specialist"),
            ("literary", "neh-primary-literary-20260723-b", "memoir_prayer_register_opposition_assembly_covenant_and_dedication_specialist"),
            ("canonical", "neh-primary-canonical-20260723-c", "canonical_relations_and_premortem_specialist"),
        ),
        peer_attempt="neh-peer-crosscheck-20260723-d",
        boss_attempt="neh-boss-adjudicator-20260723-e",
        post_attempt="neh-post-resolution-checker-20260723-f",
        reviewer_hint="human_or_external_ai_Hebrew_Persian_administration_Second_Temple_Torah_assembly_register_and_ethics_specialist",
        relation_specs=(
            ("001", [f"M7_sol-Neh-{i:03d}" for i in range(1, 4)], ["Ezra.4.1-Ezra.6.22", "Ezra.7.1-Ezra.8.36", "Dan.9.1-Dan.9.27"], "Jerusalem_report_prayer_royal_commission_survey_and_appeal_relations"),
            ("002", [f"M7_sol-Neh-{i:03d}" for i in range(4, 7)], ["Isa.52.1-Isa.52.12", "Isa.60.1-Isa.62.12", "Zech.1.1-Zech.2.13"], "wall_register_mockery_prayer_defense_and_prophetic_city_relations"),
            ("003", [f"M7_sol-Neh-{i:03d}" for i in range(7, 10)], ["Exod.22.21-Exod.23.13", "Lev.25.1-Lev.25.55", "Deut.15.1-Deut.15.23"], "economic_restitution_governor_practice_intrigue_and_completion_relations"),
            ("004", ["M7_sol-Neh-010", "M7_sol-Neh-011"], ["Ezra.2.1-Ezra.2.70"], "security_genealogical_inquiry_and_returnee_register_relations"),
            ("005", [f"M7_sol-Neh-{i:03d}" for i in range(12, 17)], ["Lev.23.1-Lev.23.44", "Deut.31.1-Deut.31.13", "Ezra.9.1-Ezra.10.44"], "Torah_reading_festival_confession_covenant_and_commitment_relations"),
            ("006", ["M7_sol-Neh-017", "M7_sol-Neh-018"], ["1Chr.9.1-1Chr.9.44", "Ezra.2.1-Ezra.2.70"], "resettlement_priest_Levite_succession_and_service_register_relations"),
            ("007", ["M7_sol-Neh-019"], ["1Chr.15.1-1Chr.16.43", "2Chr.29.1-2Chr.31.21", "Ps.48.1-Ps.48.14"], "wall_dedication_processions_joy_and_cultic_appointment_relations"),
            ("008", [f"M7_sol-Neh-{i:03d}" for i in range(20, 25)], ["Exod.20.8-Exod.20.11", "Deut.7.1-Deut.7.26", "Deut.23.1-Deut.23.25", "Ezra.9.1-Ezra.10.44"], "final_exclusion_storeroom_Sabbath_marriage_priesthood_and_remembrance_relations"),
        ),
    )
