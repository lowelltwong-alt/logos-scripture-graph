from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_manuscript_source_catalog_research_packet as validator


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / ".ai" / "control" / "manuscript_source_catalog_research_packet.yaml"


def read_packet() -> str:
    return PACKET.read_text(encoding="utf-8")


def test_t391_manuscript_source_catalog_research_packet_validates() -> None:
    result = validator.validate_manuscript_source_catalog_research_packet()

    assert result["packet_id"] == "t391_manuscript_source_catalog_research_packet"
    assert result["source_family_count"] == 5
    assert result["source_count"] == 18
    assert result["dss_confirmed_fact_count"] >= 6
    assert result["nt_confirmed_fact_count"] >= 10
    assert result["timeline_anchor_count"] >= 5


def test_t391_packet_is_metadata_only_and_non_authorizing() -> None:
    text = read_packet()

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
        "No images, transcriptions, or text are imported.",
    ]:
        assert phrase in text
    assert "do not import source text" in text.lower()


def test_t391_packet_uses_reputable_official_source_anchors() -> None:
    text = read_packet()

    for source_id in validator.REQUIRED_SOURCE_IDS:
        assert source_id in text
    for url in [
        "https://www.deadseascrolls.org.il/",
        "https://www.deadseascrolls.org.il/explore-the-archive",
        "https://www.deadseascrolls.org.il/learn-about-the-scrolls/discovery-and-publication",
        "https://www.deadseascrolls.org.il/learn-about-the-scrolls/scrolls-content",
        "https://dss.collections.imj.org.il/isaiah",
        "https://www.imj.org.il/en/collections/198208-0",
        "https://ntvmr.uni-muenster.de/",
        "https://ntvmr.uni-muenster.de/liste",
        "https://www.uni-muenster.de/INTF/en/institut/index.html",
        "https://www.uni-muenster.de/INTF/en/forschung/ecm/index.html",
        "https://www.uni-muenster.de/INTF/en/forschung/cbgm/index.html",
        "https://manuscripts.csntm.org/",
        "https://manuscripts.csntm.org/manuscript/View/GA_P52",
        "https://www.digitalcollections.manchester.ac.uk/view/MS-GREEK-P-00457",
        "https://www.codexsinaiticus.org/",
        "https://www.codexsinaiticus.org/en/project/",
        "https://digi.vatlib.it/view/MSS_Vat.gr.1209",
        "https://searcharchives.bl.uk/catalog/040-001614686",
    ]:
        assert url in text


def test_t391_packet_separates_confirmed_candidate_and_blocked_claims() -> None:
    text = read_packet()

    assert "confirmed_facts:" in text
    assert "candidate_claims:" in text
    assert "blocked_claims:" in text
    assert "open_questions_and_blocked_claims:" in text
    assert "blocked_until_row_level_catalog_review" in text
    assert "owner_review_required" in text


def test_t391_packet_routes_boundary_and_doctrine_elsewhere() -> None:
    text = read_packet()

    assert "logos-boundary-literature" in text
    assert "logos-doctrine-genealogy" in text
    assert "Church fathers, patristic citations, commentaries" in text
    assert "who built theology on whom" in text


def test_t391_validator_rejects_database_creation_authority(monkeypatch: pytest.MonkeyPatch) -> None:
    data = validator._read_yaml(PACKET)
    data["authority"]["authorizes_sqlite_database_creation"] = True

    monkeypatch.setattr(validator, "_read_yaml", lambda path: data)

    with pytest.raises(
        validator.ManuscriptSourceCatalogResearchPacketError,
        match="authorizes_sqlite_database_creation",
    ):
        validator.validate_manuscript_source_catalog_research_packet(check_wiring=False)


def test_t391_validator_rejects_unknown_claim_source(monkeypatch: pytest.MonkeyPatch) -> None:
    data = validator._read_yaml(PACKET)
    data["dss_biblical_witness_packet"]["confirmed_facts"][0]["source_ids"] = ["unknown_source"]

    monkeypatch.setattr(validator, "_read_yaml", lambda path: data)

    with pytest.raises(validator.ManuscriptSourceCatalogResearchPacketError, match="unknown source_ids"):
        validator.validate_manuscript_source_catalog_research_packet(check_wiring=False)


def test_t391_validator_rejects_missing_provenance(monkeypatch: pytest.MonkeyPatch) -> None:
    data = validator._read_yaml(PACKET)
    data["curated_sources"][0]["provenance_note"] = ""

    monkeypatch.setattr(validator, "_read_yaml", lambda path: data)

    with pytest.raises(validator.ManuscriptSourceCatalogResearchPacketError, match="provenance_note"):
        validator.validate_manuscript_source_catalog_research_packet(check_wiring=False)
