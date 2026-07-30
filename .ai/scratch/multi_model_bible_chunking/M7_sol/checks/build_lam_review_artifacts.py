from build_review_artifacts_generic import build

if __name__ == "__main__":
    build(
        book="Lam", expected_sha="d95f5186fd07b10865a1e381bf66e2eb637864495b1d28774dd3e84ef460427f",
        roles=(
            ("hebrew","lam-primary-hebrew-textual-20260723-a","Hebrew_acrostic_triple_acrostic_pe_ayin_qinah_syntax_versions_and_translation_specialist"),
            ("literary","lam-primary-literary-20260723-b","lament_poetry_voice_addressee_catalogue_wisdom_prayer_and_closure_specialist"),
            ("canonical","lam-primary-canonical-premortem-20260723-c","canonical_relations_authorship_history_divine_agency_reception_authority_and_premortem_specialist"),
        ),
        peer_attempt="lam-peer-crosscheck-20260723-d", boss_attempt="lam-boss-adjudicator-20260723-e",
        post_attempt="lam-role-separated-postchecker-20260723-f",
        reviewer_hint="human_or_external_ai_Biblical_Hebrew_Lamentations_acrostic_poetry_textual_criticism_ancient_lament_Jewish_liturgy_and_reception_specialist",
        relation_specs=(
            ("001",[f"M7_sol-Lam-{i:03d}" for i in range(1,5)],["Deut.28.1-Deut.32.47","2Kgs.24.1-2Kgs.25.30","Jer.8.1-Jer.10.25"],"city_desolation_exile_covenant_curse_Zion_voice_and_closing_petition_relations"),
            ("002",[f"M7_sol-Lam-{i:03d}" for i in range(5,8)],["2Kgs.25.1-2Kgs.25.30","Jer.7.1-Jer.7.34","Jer.52.1-Jer.52.34"],"divine_destruction_temple_city_silence_witness_grief_address_and_petition_relations"),
            ("003",[f"M7_sol-Lam-{i:03d}" for i in range(8,15)],["Job.3.1-Job.7.21","Ps.22.1-Ps.22.31","Ps.88.1-Ps.88.18"],"afflicted_speaker_remembrance_hope_wisdom_justice_communal_return_tears_pit_and_imprecation_relations"),
            ("004",[f"M7_sol-Lam-{i:03d}" for i in range(15,19)],["Deut.28.47-Deut.28.68","2Kgs.25.1-2Kgs.25.30","Ezek.5.1-Ezek.7.27"],"siege_reversal_starvation_wrath_prophet_priest_pollution_pursuit_and_anointed_capture_relations"),
            ("005",["M7_sol-Lam-018"],["Jer.49.7-Jer.49.22","Ezek.25.12-Ezek.25.14","Obad.1.1-Obad.1.21"],"Edom_Zion_vocative_coda_and_nation_oracle_relations"),
            ("006",[f"M7_sol-Lam-{i:03d}" for i in range(19,22)],["Deut.26.1-Deut.26.19","Ps.74.1-Ps.74.23","Ps.79.1-Ps.79.13"],"communal_remember_catalogue_social_reversal_Zion_desolation_throne_protest_and_restore_relations"),
        ),
    )