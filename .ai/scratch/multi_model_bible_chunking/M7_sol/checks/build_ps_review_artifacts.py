from build_review_artifacts_generic import build


if __name__ == "__main__":
    build(
        book="Ps",
        expected_sha="e8427691acfd2ac015a06ee0002c0a94cd8ed33a15b2ef5a610fdd6a69b54a4e",
        roles=(
            ("hebrew", "ps-primary-hebrew-poetics-20260723-a", "Hebrew_poetics_superscriptions_WEB_MT_LXX_acrostic_and_refrain_specialist"),
            ("literary", "ps-primary-literary-20260723-b", "whole_psalm_strophe_refrain_acrostic_liturgical_and_collection_specialist"),
            ("canonical", "ps-primary-canonical-20260723-c", "canonical_relations_imprecation_messianic_authority_and_premortem_specialist"),
        ),
        peer_attempt="ps-peer-crosscheck-20260723-d",
        boss_attempt="ps-boss-adjudicator-20260723-e",
        post_attempt="ps-fresh-post-resolution-20260723-repair",
        reviewer_hint="human_or_external_ai_Biblical_Hebrew_Psalms_poetics_Masoretic_accents_LXX_numbering_liturgy_and_reception_specialist",
        relation_specs=(
            ("001", [f"M7_sol-Ps-{i:03d}" for i in range(1, 56)], ["Gen.1.1-Gen.50.26", "Deut.1.1-Deut.34.12", "1Sam.1.1-2Sam.24.25"], "Psalms_book_one_Torah_David_lament_royal_and_wisdom_relations"),
            ("002", [f"M7_sol-Ps-{i:03d}" for i in range(56, 104)], ["Exod.1.1-Exod.40.38", "2Sam.1.1-2Sam.24.25", "Isa.1.1-Isa.39.8"], "Psalms_book_two_exodus_royal_Zion_lament_and_Asaph_Korah_relations"),
            ("003", [f"M7_sol-Ps-{i:03d}" for i in range(104, 141)], ["Num.1.1-Num.36.13", "1Kgs.1.1-2Kgs.25.30", "Isa.40.1-Isa.66.24"], "Psalms_book_three_sanctuary_exile_covenant_and_communal_lament_relations"),
            ("004", [f"M7_sol-Ps-{i:03d}" for i in range(141, 178)], ["Gen.1.1-Gen.11.32", "Deut.32.1-Deut.33.29", "1Chr.16.1-1Chr.16.43"], "Psalms_book_four_creation_Moses_enthronement_history_and_worship_relations"),
            ("005", [f"M7_sol-Ps-{i:03d}" for i in range(178, 264)], ["Exod.12.1-Exod.15.27", "Ezra.1.1-Neh.13.31", "Prov.1.1-Prov.31.31"], "Psalms_book_five_thanksgiving_Torah_ascents_restoration_and_final_praise_relations"),
            ("006", ["M7_sol-Ps-056", "M7_sol-Ps-057"], ["Ps.42.1-Ps.43.5"], "Psalms_42_43_refrain_lexical_relation_without_forced_merger"),
        ),
    )
