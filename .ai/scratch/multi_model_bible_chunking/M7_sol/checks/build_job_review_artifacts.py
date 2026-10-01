from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Job",
        expected_sha="b94766a696f990d8c7fc93484858937b949aa90492da8c3bbf2bb666a0206509",
        roles=(
            ("hebrew", "job-primary-hebrew-textual-20260723-a", "rare_Hebrew_textual_speaker_versification_and_poetry_specialist"),
            ("literary", "job-primary-literary-20260723-b", "speaker_turn_dialogue_cycle_poem_oath_Elihu_and_divine_speech_specialist"),
            ("canonical", "job-primary-canonical-20260723-c", "canonical_relations_doctrine_authority_and_premortem_specialist"),
        ),
        peer_attempt="job-peer-crosscheck-20260723-d",
        boss_attempt="job-boss-adjudicator-20260723-e",
        post_attempt="job-post-resolution-checker-20260723-f",
        reviewer_hint="human_or_external_ai_Biblical_Hebrew_Job_textual_criticism_poetry_speaker_allocation_ANE_wisdom_and_theology_specialist",
        relation_specs=(
            ("001", [f"M7_sol-Job-{i:03d}" for i in range(1, 7)], ["Gen.1.1-Gen.3.24", "Gen.22.1-Gen.22.24", "1Kgs.22.1-1Kgs.22.40", "Zech.3.1-Zech.3.10"], "prose_trial_catastrophe_lament_creation_and_heavenly_court_relations"),
            ("002", [f"M7_sol-Job-{i:03d}" for i in range(7, 13)], ["Ps.22.1-Ps.22.31", "Ps.88.1-Ps.88.18", "Prov.1.1-Prov.9.18"], "first_dialogue_cycle_lament_wisdom_and_retribution_relations"),
            ("003", [f"M7_sol-Job-{i:03d}" for i in range(13, 20)], ["Ps.37.1-Ps.37.40", "Ps.73.1-Ps.73.28", "Eccl.1.1-Eccl.12.14"], "second_dialogue_cycle_suffering_redeemer_wisdom_and_prosperity_relations"),
            ("004", [f"M7_sol-Job-{i:03d}" for i in range(20, 24)], ["Deut.32.1-Deut.32.47", "Ps.49.1-Ps.49.20", "Prov.8.1-Prov.9.18"], "disrupted_third_cycle_speaker_allocation_and_wisdom_hymn_relations"),
            ("005", ["M7_sol-Job-024"], ["Deut.27.1-Deut.30.20", "Ps.26.1-Ps.26.12", "Ps.44.1-Ps.44.26"], "Job_final_recollection_lament_oath_defense_and_legal_relations"),
            ("006", [f"M7_sol-Job-{i:03d}" for i in range(25, 30)], ["Gen.2.7-Gen.2.7", "Num.22.1-Num.24.25", "Ps.78.1-Ps.78.72"], "Elihu_spirit_breath_mediation_wisdom_and_divine_speech_prelude_relations"),
            ("007", [f"M7_sol-Job-{i:03d}" for i in range(30, 34)], ["Gen.1.1-Gen.2.25", "Ps.104.1-Ps.104.35", "Isa.40.1-Isa.40.31"], "storm_creation_Behemoth_Leviathan_divine_speech_and_Job_response_relations"),
            ("008", ["M7_sol-Job-034", "M7_sol-Job-035"], ["Gen.20.1-Gen.20.18", "Gen.42.1-Gen.50.26", "Ezek.14.12-Ezek.14.23", "Jas.5.7-Jas.5.20"], "verdict_sacrifice_intercession_restoration_and_later_reception_relations"),
        ),
    )
