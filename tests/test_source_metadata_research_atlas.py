from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_source_metadata_research_atlas as validator


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / ".ai" / "control" / "source_metadata_research_atlas.yaml"


def load_atlas() -> dict:
    return yaml.safe_load(ATLAS.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "source_metadata_research_atlas.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_source_metadata_research_atlas_passes_current_repo() -> None:
    data = validator.validate_source_metadata_research_atlas()

    assert data["object_type"] == "source_metadata_research_atlas"
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["scope"]["corpus_scope"] == "canonical_66"


def test_atlas_records_required_metadata_families() -> None:
    data = load_atlas()
    families = {family["family_id"]: family for family in data["metadata_families"]}

    for family_id in validator.REQUIRED_FAMILIES:
        assert family_id in families
        assert "evidence only" in families[family_id]["authority_boundary"]

    assert "automatic_cross_reference_edge" in families["editorial_cross_references"]["non_authorizations"]
    assert "automatic_strongs_lexical_authority" in families["strongs_style_word_numbers"]["non_authorizations"]
    assert "isolated_word_as_theological_truth" in families["strongs_style_word_numbers"]["non_authorizations"]
    assert "isolated_lemma_as_doctrine" in families["lexical_rarity_and_shared_lemmas"]["non_authorizations"]
    assert "wj_marker_as_speaker_attribution" in families["wj_red_letter_markers"]["non_authorizations"]
    assert "capitalization_as_theological_truth" in families["divine_name_title_capitalization"]["non_authorizations"]

    strongs_text = " ".join(families["strongs_style_word_numbers"]["required_review_questions"])
    assert "phrase" in strongs_text
    assert "clause" in strongs_text
    assert "discourse" in strongs_text


def test_atlas_records_observed_canonical_source_counts() -> None:
    data = load_atlas()
    surfaces = {surface["surface_id"]: surface for surface in data["observed_source_surfaces"]}

    assert surfaces["canonical_word_tokens"]["record_count"] == 677688
    assert surfaces["editorial_cross_references"]["record_count"] == 340
    assert surfaces["footnotes"]["record_count"] == 1130
    assert surfaces["section_headings"]["record_count"] == 283
    assert surfaces["boundary_claims"]["record_count"] == 28165
    assert surfaces["wj_marker_inventory"]["observed_counts"]["wj_token_runs"] == 675


def test_atlas_requires_priority_research_cases() -> None:
    data = load_atlas()
    cases = {case["case_id"]: case for case in data["priority_research_cases"]}

    for case_id in validator.REQUIRED_CASES:
        assert case_id in cases

    assert "Rev.12.1-Rev.14.20" in cases["revelation_crossrefs_wj_and_symbolic_intertexts"]["passages"]
    assert cases["john3_wj_speaker_boundary_metadata"]["status"] == "owner_review_pending"


def test_atlas_rejects_authorizing_flag(tmp_path: Path) -> None:
    data = load_atlas()
    data["authority"]["authorizes_graph_edges"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.SourceMetadataResearchAtlasError, match="authorizes_graph_edges must be false"):
        validator.validate_source_metadata_research_atlas(candidate)


def test_atlas_rejects_missing_family_non_authorization(tmp_path: Path) -> None:
    data = load_atlas()
    for family in data["metadata_families"]:
        if family["family_id"] == "wj_red_letter_markers":
            family["non_authorizations"].remove("wj_marker_as_speaker_attribution")
            break
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.SourceMetadataResearchAtlasError, match="wj_marker_as_speaker_attribution"):
        validator.validate_source_metadata_research_atlas(candidate)


def test_atlas_rejects_stale_record_count(tmp_path: Path) -> None:
    data = load_atlas()
    for surface in data["observed_source_surfaces"]:
        if surface["surface_id"] == "footnotes":
            surface["record_count"] += 1
            break
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.SourceMetadataResearchAtlasError, match="record_count"):
        validator.validate_source_metadata_research_atlas(candidate)
