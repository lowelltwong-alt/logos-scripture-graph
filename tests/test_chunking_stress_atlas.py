from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "chunking_stress_cases.json"

CONTROLLED_DIFFICULTY_TYPES = {
    "long_structured_unit",
    "long_verse",
    "short_context_dependent_unit",
    "long_original_language_sentence",
    "punctuation_dependent",
    "major_textual_variant",
    "textual_tradition_divergence",
    "speaker_change_ambiguity",
    "prophetic_oracle_collection",
    "apocalyptic_vision_sequence",
    "legal_case_block",
    "genealogy_or_list",
    "parallel_account_alignment",
    "rhetorical_argument_section",
    "hard_exegesis",
    "parent_child_needed",
}

REQUIRED_CASE_IDS = {
    "ps89_royal_lament",
    "ps105_historical_psalm",
    "ps106_historical_confession",
    "ps136_refrain_litany",
    "lam1_4_acrostic_poems",
    "prov31_10_31_acrostic_woman",
    "job38_41_divine_speeches",
    "deut32_song_of_moses",
    "isa52_13_53_12_servant_song",
    "dan10_12_final_vision",
    "rev12_18_vision_cycle",
    "eph1_3_14_greek_sentence",
    "mark16_9_20_longer_ending",
    "john7_53_8_11_pericope_adulterae",
    "jeremiah_mt_lxx_divergence",
    "1sam10_27_11_1_dss_nahash",
    "gen6_1_4_sons_of_god",
    "deut32_8_9_divine_council_variant",
    "ps82_divine_council",
    "1kgs22_micaiah_council_scene",
    "ezek1_throne_vision",
    "ezek40_48_temple_vision",
    "zech1_6_night_visions",
    "matt24_25_olivet_discourse",
    "john13_17_farewell_discourse",
    "rom9_11_argument",
    "1pet3_18_22_spirits_prison",
    "jude5_15_examples_and_enoch",
    "esth8_9_long_administrative_verse",
    "matt1_genealogy",
    "luke3_genealogy",
    "1chr1_9_primeval_genealogies",
    "josh13_21_land_allotments",
    "lev16_day_of_atonement",
    "exod20_23_covenant_code",
    "heb7_10_priesthood_argument",
    "1cor8_10_food_offered_to_idols",
    "gospels_wj_marker_spans",
    "psalms_selah_qs_markers",
    "john3_wj_speaker_boundary",
    "matt5_7_sermon_on_mount_wj_discourse",
    "john13_17_wj_farewell_discourse_marker_focus",
    "synoptic_apocalyptic_wj_discourses",
    "john7_53_8_11_wj_variant_speech",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "passage",
    "book",
    "genre",
    "difficulty_types",
    "why_hard",
    "expected_chunking_risk",
    "text_critical_risk",
    "punctuation_risk",
    "translation_mismatch_risk",
    "speaker_boundary_risk",
    "parent_child_candidate",
    "proposed_gold_needed",
    "implementation_allowed",
    "status",
    "notes",
}


def atlas() -> dict:
    return json.loads(ATLAS.read_text(encoding="utf-8"))


def test_stress_atlas_root_is_proposed_only() -> None:
    data = atlas()
    assert data["schema_version"] == "chunking-stress-atlas.v0"
    assert data["status"] == "proposed"
    assert data["implementation_allowed"] is False
    assert set(data["controlled_difficulty_types"]) == CONTROLLED_DIFFICULTY_TYPES
    assert data["baseline"]["chunk_output_changed"] is False


def test_stress_atlas_contains_required_cases() -> None:
    cases = {case["case_id"]: case for case in atlas()["cases"]}
    assert REQUIRED_CASE_IDS <= set(cases)
    assert len(cases) >= len(REQUIRED_CASE_IDS)


def test_stress_cases_use_required_fields_and_guardrails() -> None:
    for case in atlas()["cases"]:
        assert REQUIRED_CASE_FIELDS <= set(case), case.get("case_id")
        assert case["status"] == "proposed", case["case_id"]
        assert case["implementation_allowed"] is False, case["case_id"]
        assert isinstance(case["parent_child_candidate"], bool), case["case_id"]
        assert case["difficulty_types"], case["case_id"]
        assert set(case["difficulty_types"]) <= CONTROLLED_DIFFICULTY_TYPES, case["case_id"]


def test_stress_atlas_covers_all_required_difficulty_types() -> None:
    observed = {
        difficulty
        for case in atlas()["cases"]
        for difficulty in case["difficulty_types"]
    }
    assert CONTROLLED_DIFFICULTY_TYPES <= observed


def test_requested_major_text_critical_cases_are_high_risk() -> None:
    cases = {case["case_id"]: case for case in atlas()["cases"]}
    for case_id in {
        "mark16_9_20_longer_ending",
        "john7_53_8_11_pericope_adulterae",
        "deut32_8_9_divine_council_variant",
        "1sam10_27_11_1_dss_nahash",
        "jeremiah_mt_lxx_divergence",
    }:
        case = cases[case_id]
        assert any(
            difficulty in case["difficulty_types"]
            for difficulty in ("major_textual_variant", "textual_tradition_divergence")
        )
        assert case["text_critical_risk"].startswith("high")


def test_t316c_marker_sensitive_cases_are_proposed_and_non_authorizing() -> None:
    cases = {case["case_id"]: case for case in atlas()["cases"]}
    marker_cases = {
        "gospels_wj_marker_spans",
        "psalms_selah_qs_markers",
        "john3_wj_speaker_boundary",
        "matt5_7_sermon_on_mount_wj_discourse",
        "john13_17_wj_farewell_discourse_marker_focus",
        "synoptic_apocalyptic_wj_discourses",
        "john7_53_8_11_wj_variant_speech",
    }
    for case_id in marker_cases:
        case = cases[case_id]
        joined = " ".join(str(value) for value in case.values())
        lowered = joined.lower()
        assert case["status"] == "proposed"
        assert case["implementation_allowed"] is False
        assert "human review" in lowered
        assert "output change" in lowered or "output-changing" in lowered


def test_words_of_jesus_cases_treat_wj_as_evidence_not_authority() -> None:
    cases = {case["case_id"]: case for case in atlas()["cases"]}
    wj_cases = {
        "gospels_wj_marker_spans",
        "john3_wj_speaker_boundary",
        "matt5_7_sermon_on_mount_wj_discourse",
        "john13_17_wj_farewell_discourse_marker_focus",
        "synoptic_apocalyptic_wj_discourses",
        "john7_53_8_11_wj_variant_speech",
    }
    for case_id in wj_cases:
        case = cases[case_id]
        joined = " ".join(str(value) for value in case.values())
        lowered = joined.lower()
        assert "\\wj" in joined
        assert "evidence, not authority" in joined
        assert "speaker" in case["difficulty_types"][0] or "speaker_change_ambiguity" in case["difficulty_types"]
        assert "speaker attribution" in lowered


def test_selah_case_tracks_qs_marker_without_authorizing_boundaries() -> None:
    case = {case["case_id"]: case for case in atlas()["cases"]}["psalms_selah_qs_markers"]
    joined = " ".join(str(value) for value in case.values())
    assert "\\qs" in joined
    assert "Selah" in joined
    assert case["parent_child_candidate"] is True
    assert "not automatically approved chunk boundaries" in joined
