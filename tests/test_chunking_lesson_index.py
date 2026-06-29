from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_chunking_lesson_index import (
    LessonIndexError,
    validate_changed_path_gate,
    validate_lesson_index,
)


ROOT = Path(__file__).resolve().parents[1]
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"


def test_chunking_lesson_index_validates_and_is_non_authorizing() -> None:
    data = validate_lesson_index(LESSON_INDEX)

    assert data["object_type"] == "chunking_lesson_index"
    assert data["trust_zone"] == "canonical"
    assert data["lifecycle_status"] == "active"
    assert data["authority"]["records_lessons"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_route_behavior"] is False
    assert data["authority"]["authorizes_graph_edges"] is False
    assert data["authority"]["authorizes_retrieval_truth"] is False


def test_chunking_lesson_index_has_required_tags_and_use_when_routing() -> None:
    data = validate_lesson_index(LESSON_INDEX)
    by_id = {lesson["lesson_id"]: lesson for lesson in data["lessons"]}

    assert set(by_id) >= {f"LSN-{number:03d}" for number in range(1, 32)}
    assert "source-metadata" in by_id["LSN-001"]["tags"]
    assert "lessons-learned" in by_id["LSN-002"]["tags"]
    assert "ai-toc" in by_id["LSN-003"]["tags"]
    assert "original-language" in by_id["LSN-004"]["tags"]
    assert "orthodox-hermeneutic-firewall" in by_id["LSN-005"]["tags"]
    assert "textual-critical-policy" in by_id["LSN-006"]["tags"]
    assert "owner-projection" in by_id["LSN-007"]["tags"]
    assert "parent-first-pilot" in by_id["LSN-008"]["tags"]
    assert "graph" in by_id["LSN-009"]["tags"]
    assert "no-context-review" in by_id["LSN-010"]["tags"]
    assert "contextual-reading" in by_id["LSN-011"]["tags"]
    assert "historical-context" in by_id["LSN-011"]["tags"]
    assert "research-runway" in by_id["LSN-012"]["tags"]
    assert "authority-boundary" in by_id["LSN-012"]["tags"]
    assert "bible-wide-readiness" in by_id["LSN-013"]["tags"]
    assert "research-synthesis" in by_id["LSN-013"]["tags"]
    assert "human-decision-map" in by_id["LSN-013"]["tags"]
    assert "chunking-ready" in by_id["LSN-013"]["tags"]
    assert "owner-decision-packet" in by_id["LSN-020"]["tags"]
    assert "recommendation-not-selection" in by_id["LSN-020"]["tags"]
    assert "goal4" in by_id["LSN-020"]["tags"]
    assert "ephesians" in by_id["LSN-020"]["tags"]
    assert ".ai/control/t385_owner_decision_packet.yaml" in by_id["LSN-020"]["source_surfaces"]
    assert "review-packet-strengthening" in by_id["LSN-021"]["tags"]
    assert "premortem" in by_id["LSN-021"]["tags"]
    assert "red-team" in by_id["LSN-021"]["tags"]
    assert "promotion-gate" in by_id["LSN-021"]["tags"]
    assert "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md" in by_id["LSN-021"]["source_surfaces"]
    assert "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md" in by_id["LSN-021"]["source_surfaces"]
    assert "CD-067" in by_id["LSN-021"]["related_decision_ids"]
    assert "reviewed-gold-promotion-decision" in by_id["LSN-022"]["tags"]
    assert "recommendation-not-selection" in by_id["LSN-022"]["tags"]
    assert "variant-non-dependency" in by_id["LSN-022"]["tags"]
    assert "child-span-necessity" in by_id["LSN-022"]["tags"]
    assert ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml" in by_id["LSN-022"]["source_surfaces"]
    assert "docs/roadmap/T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md" in by_id["LSN-022"]["source_surfaces"]
    assert "CD-068" in by_id["LSN-022"]["related_decision_ids"]
    assert "source-catalog-research" in by_id["LSN-023"]["tags"]
    assert "official-sources" in by_id["LSN-023"]["tags"]
    assert ".ai/control/manuscript_source_catalog_research_packet.yaml" in by_id["LSN-023"]["source_surfaces"]
    assert "CD-069" in by_id["LSN-023"]["related_decision_ids"]
    assert "source-catalog-sqlite" in by_id["LSN-024"]["tags"]
    assert "sqlite-shell" in by_id["LSN-024"]["tags"]
    assert "seed-rows" in by_id["LSN-024"]["tags"]
    assert "t395" in by_id["LSN-024"]["tags"]
    assert ".ai/control/manuscript_source_catalog_sqlite_shell.yaml" in by_id["LSN-024"]["source_surfaces"]
    assert "data/candidate/source_catalog/manuscript_reliability/sqlite/schema.sql" in by_id["LSN-024"]["source_surfaces"]
    assert "docs/roadmap/T395_SQLITE_SOURCE_CATALOG_SCHEMA_SHELL.md" in by_id["LSN-024"]["source_surfaces"]
    assert "CD-070" in by_id["LSN-024"]["related_decision_ids"]
    assert "reviewed-gold" in by_id["LSN-025"]["tags"]
    assert "parent-only" in by_id["LSN-025"]["tags"]
    assert "goal6" in by_id["LSN-025"]["tags"]
    assert "t394" in by_id["LSN-025"]["tags"]
    assert "implementation-blocked" in by_id["LSN-025"]["tags"]
    assert ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml" in by_id["LSN-025"]["source_surfaces"]
    assert "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json" in by_id["LSN-025"]["source_surfaces"]
    assert "docs/roadmap/T394_EPH1_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md" in by_id["LSN-025"]["source_surfaces"]
    assert "CD-071" in by_id["LSN-025"]["related_decision_ids"]
    assert "phase-one-research" in by_id["LSN-026"]["tags"]
    assert "whole-corpus" in by_id["LSN-026"]["tags"]
    assert "triage-not-exegesis" in by_id["LSN-026"]["tags"]
    assert "goal2" in by_id["LSN-026"]["tags"]
    assert "focused-research" in by_id["LSN-026"]["tags"]
    assert ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml" in by_id["LSN-026"]["source_surfaces"]
    assert "docs/roadmap/T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md" in by_id["LSN-026"]["source_surfaces"]
    assert "scripts/validate_t398_bible_wide_phase_one_research_synthesis.py" in by_id["LSN-026"]["source_surfaces"]
    assert "CD-072" in by_id["LSN-026"]["related_decision_ids"]
    assert "focused-research-queue" in by_id["LSN-027"]["tags"]
    assert "owner-decision-map" in by_id["LSN-027"]["tags"]
    assert "scoring-not-authority" in by_id["LSN-027"]["tags"]
    assert "variant-blocked-status" in by_id["LSN-027"]["tags"]
    assert ".ai/control/t399_focused_bible_wide_research_queue.yaml" in by_id["LSN-027"]["source_surfaces"]
    assert "docs/roadmap/T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md" in by_id["LSN-027"]["source_surfaces"]
    assert "CD-073" in by_id["LSN-027"]["related_decision_ids"]
    assert "route-isolation-harness" in by_id["LSN-028"]["tags"]
    assert "non-target-identity" in by_id["LSN-028"]["tags"]
    assert "spill-protection" in by_id["LSN-028"]["tags"]
    assert "child-span-denial" in by_id["LSN-028"]["tags"]
    assert ".ai/control/t397_eph1_route_isolation_harness.yaml" in by_id["LSN-028"]["source_surfaces"]
    assert "scripts/chunking/route_isolation_harness.py" in by_id["LSN-028"]["source_surfaces"]
    assert "CD-074" in by_id["LSN-028"]["related_decision_ids"]
    assert "dss-biblical-witness-rows" in by_id["LSN-029"]["tags"]
    assert "great-isaiah-scroll" in by_id["LSN-029"]["tags"]
    assert "witness-row-population" in by_id["LSN-029"]["tags"]
    assert "t396" in by_id["LSN-029"]["tags"]
    assert ".ai/control/dss_biblical_witness_source_rows.yaml" in by_id["LSN-029"]["source_surfaces"]
    assert "data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows.jsonl" in by_id["LSN-029"]["source_surfaces"]
    assert "docs/roadmap/T396_DSS_BIBLICAL_WITNESS_SOURCE_ROWS.md" in by_id["LSN-029"]["source_surfaces"]
    assert "CD-075" in by_id["LSN-029"]["related_decision_ids"]
    assert "eph1-output-pilot" in by_id["LSN-030"]["tags"]
    assert "output-pilot" in by_id["LSN-030"]["tags"]
    assert "exact-output-change" in by_id["LSN-030"]["tags"]
    assert "proof-manifest" in by_id["LSN-030"]["tags"]
    assert "post-pilot-review" in by_id["LSN-030"]["tags"]
    assert "goal7" in by_id["LSN-030"]["tags"]
    assert "t401" in by_id["LSN-030"]["tags"]
    assert ".ai/control/t401_eph1_output_pilot_manifest.yaml" in by_id["LSN-030"]["source_surfaces"]
    assert "docs/roadmap/T401_EPH1_OUTPUT_PILOT.md" in by_id["LSN-030"]["source_surfaces"]
    assert "scripts/validate_t401_eph1_output_pilot.py" in by_id["LSN-030"]["source_surfaces"]
    assert "CD-076" in by_id["LSN-030"]["related_decision_ids"]
    assert "governance-dependency-map" in by_id["LSN-031"]["tags"]
    assert "child-repo-mirror" in by_id["LSN-031"]["tags"]
    assert "upstream-governance" in by_id["LSN-031"]["tags"]
    assert ".ai/control/governance_dependency_map_mirror.yaml" in by_id["LSN-031"]["source_surfaces"]
    assert "config/governance/repository_link_contract.yaml" in by_id["LSN-031"]["source_surfaces"]
    assert "scripts/validate_governance_dependency_map_mirror.py" in by_id["LSN-031"]["validators"]
    assert "local_override_of_upstream_governance" in by_id["LSN-031"]["non_authorizations"]
    assert all(lesson["use_when"] for lesson in by_id.values())


def test_chunking_lesson_index_graph_references_known_lessons() -> None:
    data = validate_lesson_index(LESSON_INDEX)
    lesson_ids = {lesson["lesson_id"] for lesson in data["lessons"]}

    assert data["lesson_graph"]
    for edge in data["lesson_graph"]:
        assert edge["from"] in lesson_ids
        assert edge["to"] in lesson_ids
        assert edge["relation"] in {"governs_update_of", "constrains", "audits", "discovers"}


def test_lesson_changed_path_gate_requires_index_update() -> None:
    with pytest.raises(LessonIndexError, match="lesson index must be updated"):
        validate_changed_path_gate(
            changed_files=[".ai/control/chunking_agent_preflight.yaml"],
            index_updated=False,
        )

    validate_changed_path_gate(
        changed_files=[
            ".ai/control/chunking_agent_preflight.yaml",
            ".ai/control/chunking_lesson_index.yaml",
        ],
        index_updated=None,
    )
