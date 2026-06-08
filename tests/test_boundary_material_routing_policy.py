from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
POLICY = ROOT / ".ai" / "control" / "boundary_material_routing.yaml"
ROADMAP = ROOT / "docs" / "roadmap" / "T327A1_THREE_REPO_ROUTING_GUARDRAILS.md"


def policy() -> dict:
    return yaml.safe_load(POLICY.read_text(encoding="utf-8"))


def test_boundary_material_routing_policy_root() -> None:
    data = policy()
    assert data["routing_policy_id"] == "BOUNDARY-MATERIAL-ROUTING-v1"
    assert data["owner_repo"] == "logos-scripture-graph"
    assert data["canonical_authority_repo"] == "logos-scripture-graph"
    assert data["supporting_boundary_repo"] == "logos-boundary-literature"
    assert data["governance_authority_repo"] == "logos-governance-architecture"
    assert data["status"] == "active_policy"


def test_authority_hierarchy_fails_closed_for_boundary_material() -> None:
    hierarchy = policy()["authority_hierarchy"]
    assert hierarchy["boundary_repo_can_override_scripture"] is False
    assert hierarchy["boundary_repo_can_equal_scripture_authority"] is False
    assert hierarchy["governance_repo_can_define_cross_repo_policy"] is True
    assert policy()["canonical_scope"]["default_corpus"] == "canonical_66"
    assert policy()["canonical_scope"]["canonical_claims_owned_here"] is True


def test_boundary_and_governance_routes_are_explicit() -> None:
    data = policy()
    for route in [
        "deuterocanonical_apocrypha",
        "noncanonical_boundary_literature",
        "heterodox_or_gnostic_texts",
        "disputed_attribution_texts",
        "known_forgery_or_fake_texts",
        "commentary_reception_corpus",
        "josephus_philo_dss_qumran_corpora",
        "patristic_reception_corpora",
    ]:
        assert route in data["route_to_boundary_repo"]
    for route in [
        "cross_repo_authority_policy",
        "repository_link_contracts",
        "rule_registry_policy",
        "update_flow_policy",
        "validation_contract_policy",
    ]:
        assert route in data["route_to_governance_repo"]


def test_forbidden_and_allowed_data_flows_are_recorded() -> None:
    data = policy()
    assert "canonical_passage_records_for_boundary_material" in data["forbidden_in_scripture_graph"]
    assert "canonical_chunks_for_boundary_material" in data["forbidden_in_scripture_graph"]
    assert "leaderboard_inputs_from_boundary_material" in data["forbidden_in_scripture_graph"]
    assert "default_scripture_retrieval_from_boundary_material" in data["forbidden_in_scripture_graph"]
    assert "planning_docs" in data["allowed_in_scripture_graph"]
    assert "cross_repo_contract_references" in data["allowed_in_scripture_graph"]
    assert "scoped_background_links" in data["allowed_in_scripture_graph"]
    assert set(data["boundary_claims_require_scope"]) == {
        "trust_level",
        "tradition_scope",
        "profile_scope",
        "provenance",
    }


def test_front_door_and_toc_name_three_repo_routing() -> None:
    front = FRONT_DOOR.read_text(encoding="utf-8")
    toc = TOC.read_text(encoding="utf-8")
    assert "## Canonical Scripture entry point" in front
    assert "logos-boundary-literature" in front
    assert "logos-governance-architecture" in front
    assert "Boundary text source intake" in front
    assert "must not override, contaminate, or become equal authority" in front
    assert ".ai/control/boundary_material_routing.yaml" in front
    assert "Supporting boundary literature repo" in toc
    assert "never equal or superior authority to canonical Scripture" in toc


def test_t327a1_roadmap_records_governance_follow_up_and_no_output_change() -> None:
    text = ROADMAP.read_text(encoding="utf-8")
    assert "Governance-Repo Follow-Up" in text
    assert "pre-existing dirty work" in text
    assert "does not mutate data" in text
    assert "does not" in text and "start T327B" in text
    assert "If a task appears to require boundary material to modify canonical Scripture outputs" in text
