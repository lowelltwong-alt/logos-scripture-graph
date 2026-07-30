from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Eccl",
        expected_sha="a62fb2971f428a498caf2f2de7929e76eb87c5bd3d9fb5186182da0faa8153b8",
        roles=(
            (
                "hebrew",
                "eccl-primary-hebrew-textual-20260723-a",
                "Hebrew_Qohelet_voice_hebel_refrain_versification_and_translation_specialist",
            ),
            (
                "literary",
                "eccl-primary-literary-20260723-b",
                "frame_investigation_observation_refrain_poem_saying_chain_and_epilogue_specialist",
            ),
            (
                "canonical",
                "eccl-primary-canonical-20260723-c",
                "canonical_relations_voice_afterlife_judgment_authority_and_premortem_specialist",
            ),
        ),
        peer_attempt="eccl-peer-crosscheck-20260723-d",
        boss_attempt="eccl-boss-adjudicator-20260723-e",
        post_attempt="eccl-post-resolution-checker-20260723-f",
        reviewer_hint=(
            "human_or_external_ai_Biblical_Hebrew_Ecclesiastes_Qohelet_voice_textual_"
            "criticism_wisdom_reception_and_LXX_specialist"
        ),
        relation_specs=(
            (
                "001",
                [f"M7_sol-Eccl-{i:03d}" for i in range(1, 7)],
                ["Gen.1.1-Gen.3.24", "1Kgs.3.1-1Kgs.11.43", "Job.1.1-Job.3.26", "Prov.1.1-Prov.9.18"],
                "frame_hebel_creation_cycle_royal_investigation_toil_wisdom_and_enjoyment_relations",
            ),
            (
                "002",
                [f"M7_sol-Eccl-{i:03d}" for i in range(7, 10)],
                ["Gen.1.1-Gen.2.25", "Deut.32.1-Deut.32.47", "Job.14.1-Job.14.22", "Ps.90.1-Ps.90.17"],
                "time_poem_work_gift_injustice_mortality_and_creation_relations",
            ),
            (
                "003",
                [f"M7_sol-Eccl-{i:03d}" for i in range(10, 17)],
                ["Deut.15.1-Deut.15.23", "1Sam.8.1-1Sam.12.25", "Job.24.1-Job.24.25", "Prov.10.1-Prov.22.16"],
                "oppression_toil_companionship_rule_worship_wealth_enjoyment_and_appetite_relations",
            ),
            (
                "004",
                [f"M7_sol-Eccl-{i:03d}" for i in range(17, 22)],
                ["Deut.17.1-Deut.17.20", "Job.28.1-Job.28.28", "Ps.37.1-Ps.37.40", "Prov.25.1-Prov.29.27"],
                "better_sayings_wisdom_limits_royal_command_delayed_justice_and_unsearchability_relations",
            ),
            (
                "005",
                [f"M7_sol-Eccl-{i:03d}" for i in range(22, 27)],
                ["Gen.3.1-Gen.3.24", "Deut.30.1-Deut.30.20", "Job.7.1-Job.7.21", "Prov.10.1-Prov.22.16"],
                "common_fate_enjoyment_chance_poor_wisdom_folly_work_and_ruler_relations",
            ),
            (
                "006",
                ["M7_sol-Eccl-027", "M7_sol-Eccl-028"],
                ["Gen.2.7-Gen.3.24", "Deut.8.1-Deut.8.20", "Ps.90.1-Ps.90.17", "Prov.30.1-Prov.30.33"],
                "risk_diligence_youth_judgment_aging_dust_spirit_and_hebel_relations",
            ),
            (
                "007",
                ["M7_sol-Eccl-029"],
                ["Deut.6.1-Deut.6.25", "Deut.30.1-Deut.30.20", "Prov.1.1-Prov.9.18", "Prov.31.1-Prov.31.31"],
                "epilogue_wisdom_words_fear_commandment_judgment_and_frame_relations",
            ),
        ),
    )
