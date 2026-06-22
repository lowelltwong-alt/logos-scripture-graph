from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_manuscript_witness_reliability_scaffold as validator


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / ".ai" / "control" / "manuscript_witness_reliability_scaffold.yaml"


def read_scaffold() -> str:
    return SCAFFOLD.read_text(encoding="utf-8")


def test_t387_manuscript_witness_reliability_scaffold_validates() -> None:
    result = validator.validate_manuscript_witness_reliability_scaffold()

    assert result["scaffold_id"] == "t387_manuscript_witness_reliability_scaffold"
    assert result["table_count"] == 6
    assert result["source_anchor_count"] == 8
    assert result["backlog_count"] == 5


def test_t387_scaffold_is_metadata_only_and_non_authorizing() -> None:
    text = read_scaffold()

    for phrase in [
        "authorizes_source_text_import: false",
        "authorizes_canonical_bible_text_change: false",
        "authorizes_canonical_passage_record_change: false",
        "authorizes_textual_critical_decision: false",
        "authorizes_preferred_reading: false",
        "authorizes_graph_edges: false",
        "authorizes_retrieval_truth: false",
        "authorizes_apologetic_conclusion_as_truth: false",
        "stores_scripture_text: false",
        "stores_boundary_text: false",
    ]:
        assert phrase in text


def test_t387_scaffold_forbids_canonical_namespace_for_reliability_tables() -> None:
    text = read_scaffold()

    assert "canonical_" in text
    assert "forbidden_prefixes:" in text
    for table in validator.REQUIRED_TABLES:
        assert table.startswith(("scripture_", "evidence_"))
        assert f"table_name: {table}" in text
    assert "table_name: canonical_" not in text


def test_t387_scaffold_preserves_scripture_boundary_split() -> None:
    text = read_scaffold()

    assert "owning_repo: logos-scripture-graph" in text
    assert "logos-boundary-literature" in text
    assert "logos-governance-architecture" in text
    assert "noncanonical or community-text corpus content from Qumran/DSS must not become canonical Scripture records" in text
    assert "early_creed_oral_tradition_bridge" in text
    assert "correct_repo: logos-boundary-literature" in text


def test_t387_scaffold_keeps_oldest_and_unchanged_claims_scoped() -> None:
    text = read_scaffold().lower()

    assert "do not use 'oldest', 'earliest', 'complete', or 'unchanged' unless the source and scope define exactly what the term means" in text
    assert "do not treat copy abundance as a standalone proof" in text
    assert "do not infer original text, preferred reading, or source-tradition priority from witness age alone" in text
    assert "do not store scripture text, creed wording, or manuscript transcription text" in text


def test_t387_scaffold_sources_include_required_primary_or_academic_anchors() -> None:
    text = read_scaffold()

    for anchor in validator.REQUIRED_SOURCE_ANCHORS:
        assert anchor in text
    for url in [
        "https://www.deadseascrolls.org.il/",
        "https://www.deadseascrolls.org.il/learn-about-the-scrolls/discovery-and-publication?locale=en_US",
        "https://dss.collections.imj.org.il/isaiah",
        "https://www.uni-muenster.de/INTF/en/institut/index.html",
        "https://www.uni-muenster.de/INTF/ECM.html",
        "https://www.digitalcollections.manchester.ac.uk/view/MS-GREEK-P-00457",
        "https://manuscripts.csntm.org/manuscript/View/GA_P52",
        "https://www.codexsinaiticus.org/",
    ]:
        assert url in text


def test_t387_validator_rejects_authorizing_source_text_import(monkeypatch: pytest.MonkeyPatch) -> None:
    data = validator._read_yaml(SCAFFOLD)
    data["authority"]["authorizes_source_text_import"] = True

    monkeypatch.setattr(validator, "_read_yaml", lambda path: data)

    with pytest.raises(validator.ManuscriptWitnessReliabilityError, match="authorizes_source_text_import"):
        validator.validate_manuscript_witness_reliability_scaffold(check_wiring=False)


def test_t387_validator_rejects_canonical_table_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    data = validator._read_yaml(SCAFFOLD)
    data["database_namespace_plan"]["tables"][0]["table_name"] = "canonical_manuscript_witness"

    monkeypatch.setattr(validator, "_read_yaml", lambda path: data)

    with pytest.raises(validator.ManuscriptWitnessReliabilityError, match="tables must be"):
        validator.validate_manuscript_witness_reliability_scaffold(check_wiring=False)
