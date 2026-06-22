from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_manuscript_source_catalog_metadata_plan as validator


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / ".ai" / "control" / "manuscript_source_catalog_metadata_plan.yaml"


def read_plan() -> str:
    return PLAN.read_text(encoding="utf-8")


def test_t390_manuscript_source_catalog_metadata_plan_validates() -> None:
    result = validator.validate_manuscript_source_catalog_metadata_plan()

    assert result["plan_id"] == "t390_manuscript_source_catalog_metadata_plan"
    assert result["table_count"] == 11
    assert result["source_family_count"] == 5
    assert result["source_anchor_count"] == 13
    assert result["trust_rule_count"] == 9
    assert result["future_goal_count"] == 6


def test_t390_plan_is_metadata_only_and_non_authorizing() -> None:
    text = read_plan()

    for phrase in [
        "authorizes_sqlite_database_creation: false",
        "authorizes_metadata_row_population: false",
        "authorizes_source_text_import: false",
        "authorizes_transcription_storage: false",
        "authorizes_canonical_bible_text_change: false",
        "authorizes_canonical_passage_record_change: false",
        "authorizes_textual_critical_decision: false",
        "authorizes_preferred_reading: false",
        "authorizes_graph_edges: false",
        "authorizes_retrieval_truth: false",
        "authorizes_apologetic_conclusion_as_truth: false",
        "stores_scripture_text: false",
        "stores_transcription_text: false",
        "stores_boundary_text: false",
    ]:
        assert phrase in text


def test_t390_plan_uses_only_scripture_and_evidence_namespaces() -> None:
    text = read_plan()

    assert "canonical_" in text
    assert "forbidden_prefixes:" in text
    for table in validator.REQUIRED_TABLES:
        assert table.startswith(("scripture_", "evidence_"))
        assert f"table_name: {table}" in text
    assert "table_name: canonical_" not in text
    assert "Never create a canonical_* table or view" in text


def test_t390_plan_routes_boundary_and_doctrine_content_elsewhere() -> None:
    text = read_plan()

    assert "logos-scripture-graph" in text
    assert "logos-boundary-literature" in text
    assert "logos-doctrine-genealogy" in text
    assert "Church fathers, patristic citations, commentaries, theologian writings" in text
    assert "scripture references only" in text.lower()


def test_t390_plan_requires_core_fields_on_every_table() -> None:
    data = validator._read_yaml(PLAN)
    for table in data["sqlite_entity_plan"]["tables"]:
        fields = set(table["required_fields"])
        assert {"source_url", "provenance_note", "confidence", "review_status"} <= fields
        assert table["stores_scripture_text"] is False
        assert table["stores_transcription_text"] is False
        assert table["stores_boundary_text"] is False


def test_t390_plan_source_anchors_include_official_catalog_sources() -> None:
    text = read_plan()

    for anchor in validator.REQUIRED_SOURCE_ANCHORS:
        assert anchor in text
    for url in [
        "https://www.deadseascrolls.org.il/",
        "https://www.deadseascrolls.org.il/explore-the-archive",
        "https://www.deadseascrolls.org.il/learn-about-the-scrolls/discovery-and-publication",
        "https://www.deadseascrolls.org.il/learn-about-the-scrolls/scrolls-content",
        "https://dss.collections.imj.org.il/isaiah",
        "https://ntvmr.uni-muenster.de/",
        "https://ntvmr.uni-muenster.de/liste",
        "https://manuscripts.csntm.org/",
        "https://manuscripts.csntm.org/manuscript/View/GA_P52",
        "https://www.digitalcollections.manchester.ac.uk/view/MS-GREEK-P-00457",
        "https://www.codexsinaiticus.org/",
        "https://digi.vatlib.it/view/MSS_Vat.gr.1209",
        "https://searcharchives.bl.uk/catalog/040-001614686",
    ]:
        assert url in text


def test_t390_validator_rejects_database_creation_authority(monkeypatch: pytest.MonkeyPatch) -> None:
    data = validator._read_yaml(PLAN)
    data["authority"]["authorizes_sqlite_database_creation"] = True

    monkeypatch.setattr(validator, "_read_yaml", lambda path: data)

    with pytest.raises(validator.ManuscriptSourceCatalogPlanError, match="authorizes_sqlite_database_creation"):
        validator.validate_manuscript_source_catalog_metadata_plan(check_wiring=False)


def test_t390_validator_rejects_missing_source_url_field(monkeypatch: pytest.MonkeyPatch) -> None:
    data = validator._read_yaml(PLAN)
    data["sqlite_entity_plan"]["tables"][0]["required_fields"].remove("source_url")

    monkeypatch.setattr(validator, "_read_yaml", lambda path: data)

    with pytest.raises(validator.ManuscriptSourceCatalogPlanError, match="source_url"):
        validator.validate_manuscript_source_catalog_metadata_plan(check_wiring=False)
