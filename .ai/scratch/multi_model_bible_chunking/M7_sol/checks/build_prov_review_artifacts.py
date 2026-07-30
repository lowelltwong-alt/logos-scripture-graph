from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Prov",
        expected_sha="9a10edf0d4928842493bfa34430d06d93671ad2ac4e57421d10c1601daa4c2d0",
        roles=(
            (
                "hebrew",
                "prov-primary-hebrew-textual-20260723-a",
                "Hebrew_wisdom_parallelism_collection_formula_textual_and_translation_specialist",
            ),
            (
                "literary",
                "prov-primary-literary-20260723-b",
                "parental_instruction_Wisdom_speech_aphoristic_collection_numerical_and_acrostic_specialist",
            ),
            (
                "canonical",
                "prov-primary-canonical-20260723-c",
                "canonical_relations_personified_Wisdom_authority_and_premortem_specialist",
            ),
        ),
        peer_attempt="prov-peer-crosscheck-20260723-d",
        boss_attempt="prov-boss-adjudicator-20260723-e",
        post_attempt="prov-post-resolution-checker-20260723-f",
        reviewer_hint=(
            "human_or_external_ai_Biblical_Hebrew_Proverbs_wisdom_parallelism_"
            "collection_history_LXX_and_ancient_Jewish_reception_specialist"
        ),
        relation_specs=(
            (
                "001",
                [f"M7_sol-Prov-{i:03d}" for i in range(1, 21)],
                ["Deut.4.1-Deut.6.25", "Job.28.1-Job.28.28", "Ps.1.1-Ps.1.6", "Ps.119.1-Ps.119.176"],
                "prologue_parental_instruction_two_ways_and_personified_Wisdom_relations",
            ),
            (
                "002",
                ["M7_sol-Prov-021"],
                ["Deut.15.1-Deut.15.23", "1Kgs.3.1-1Kgs.4.34", "Ps.37.1-Ps.37.40", "Eccl.1.1-Eccl.12.14"],
                "first_Solomonic_collection_justice_wealth_speech_labor_and_wisdom_relations",
            ),
            (
                "003",
                ["M7_sol-Prov-022", "M7_sol-Prov-023"],
                ["Deut.19.1-Deut.25.19", "Ps.49.1-Ps.49.20", "Isa.1.1-Isa.1.31"],
                "sayings_of_the_wise_poor_boundary_discipline_court_and_sluggard_relations",
            ),
            (
                "004",
                ["M7_sol-Prov-024"],
                ["1Kgs.4.1-1Kgs.4.34", "2Kgs.18.1-2Kgs.20.21", "2Chr.29.1-2Chr.32.33"],
                "Hezekiah_copied_collection_royal_court_fool_sluggard_friendship_and_governance_relations",
            ),
            (
                "005",
                [f"M7_sol-Prov-{i:03d}" for i in range(25, 35)],
                ["Deut.4.1-Deut.4.40", "Job.38.1-Job.42.6", "Ps.8.1-Ps.8.9", "Ps.104.1-Ps.104.35"],
                "Agur_confession_divine_word_petition_numerical_creation_and_social_order_relations",
            ),
            (
                "006",
                ["M7_sol-Prov-035", "M7_sol-Prov-036"],
                ["Ruth.1.1-Ruth.4.22", "1Kgs.3.1-1Kgs.3.28", "Ps.111.1-Ps.112.10", "Ps.119.1-Ps.119.176"],
                "Lemuel_royal_instruction_justice_household_alphabetic_poem_and_wisdom_relations",
            ),
        ),
    )
