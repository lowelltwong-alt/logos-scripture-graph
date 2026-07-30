from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Ezra",
        expected_sha="c0f45529e723e5d755298c24ae7c04db4b6d1d30e46bec9f74273c9a0c9a6c57",
        roles=(
            ("hebrew", "ezra-primary-hebrew-aramaic-20260723-a", "Hebrew_Imperial_Aramaic_translation_document_and_register_specialist"),
            ("literary", "ezra-primary-literary-20260723-b", "literary_form_document_response_register_prayer_and_assembly_specialist"),
            ("canonical", "ezra-primary-canonical-20260723-c", "canonical_relations_and_premortem_specialist"),
        ),
        peer_attempt="ezra-peer-crosscheck-20260723-d",
        boss_attempt="ezra-boss-adjudicator-20260723-e",
        post_attempt="ezra-post-resolution-checker-20260723-f",
        reviewer_hint="human_or_external_ai_Hebrew_Imperial_Aramaic_Persian_administration_Second_Temple_register_and_ethics_specialist",
        relation_specs=(
            ("001", ["M7_sol-Ezra-001"], ["2Chr.36.22-2Chr.36.23", "Isa.44.24-Isa.45.13", "Jer.25.1-Jer.29.32"], "Cyrus_proclamation_exile_and_restoration_relations"),
            ("002", ["M7_sol-Ezra-002"], ["Num.1.1-Num.4.49", "Neh.7.5-Neh.7.73"], "returnee_priest_Levite_servant_genealogy_and_parallel_register_relations"),
            ("003", ["M7_sol-Ezra-003", "M7_sol-Ezra-004"], ["Exod.27.1-Exod.30.38", "Lev.23.1-Lev.23.44", "Hag.1.1-Hag.2.23", "Zech.1.1-Zech.8.23"], "altar_festival_foundation_prophetic_and_temple_relations"),
            ("004", [f"M7_sol-Ezra-{i:03d}" for i in range(5, 9)], ["Hag.1.1-Hag.2.23", "Zech.1.1-Zech.8.23", "Dan.6.1-Dan.6.28"], "opposition_correspondence_prophetic_restart_decree_completion_and_Passover_relations"),
            ("005", [f"M7_sol-Ezra-{i:03d}" for i in range(9, 12)], ["Deut.17.14-Deut.17.20", "Deut.31.1-Deut.31.13", "Neh.8.1-Neh.8.18"], "Ezra_genealogy_Aramaic_commission_law_and_thanksgiving_relations"),
            ("006", ["M7_sol-Ezra-012", "M7_sol-Ezra-013"], ["Exod.25.1-Exod.30.38", "Num.3.1-Num.4.49", "Neh.1.1-Neh.2.20"], "returnee_recruitment_fast_treasure_journey_arrival_and_offering_relations"),
            ("007", ["M7_sol-Ezra-014"], ["Deut.7.1-Deut.7.26", "Deut.23.1-Deut.23.25", "Deut.30.1-Deut.30.20", "Neh.9.1-Neh.9.38"], "officials_report_embodied_response_and_confession_relations"),
            ("008", ["M7_sol-Ezra-015", "M7_sol-Ezra-016"], ["Deut.7.1-Deut.7.26", "Neh.10.1-Neh.10.39", "Neh.13.1-Neh.13.31"], "assembly_oath_investigation_case_register_and_covenant_relations"),
        ),
    )
