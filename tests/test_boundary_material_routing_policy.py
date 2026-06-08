from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
POLICY = ROOT / ".ai" / "control" / "boundary_material_routing.yaml"
ROADMAP = ROOT / "docs" / "roadmap" / "T327A1_THREE_REPO_ROUTING_GUARDRAILS.md"
T327A2_ROADMAP = ROOT / "docs" / "roadmap" / "T327A2_BOUNDARY_GOVERNANCE_STOP_RULES.md"

WARNING_TEXT = """WARNING: Boundary-layer request conflicts with higher-authority governance.

The requested boundary-layer task appears to require changing or bypassing governance-layer policy, canonical Scripture authority, repository-link contracts, routing policy, trust hierarchy, or canonical scope.

Governance is binding authority, not an obstacle to optimize around.

Do not automate, route, or implement this change from the boundary layer. A human maintainer must review the conflict directly in the higher-authority repository.

Owner-reserved authorization required: only Lowell Wong, as project owner, may authorize a boundary-originated request to change higher-authority governance, canonical Scripture authority, repository-link contracts, canonical scope, trust hierarchy, or cross-repo policy. Contributor consensus, contributor volume, automated recommendation, agent routing, or boundary-layer operational need is not sufficient authority.
"""


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
    assert data["governance_registry_source_of_truth"] == (
        "logos-governance-architecture/governance/LOGOS_REPO_REGISTRY.yaml"
    )


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
        "repo_registry_policy",
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
    assert "governance/LOGOS_REPO_REGISTRY.yaml" in front
    assert "Boundary text source intake" in front
    assert "must not override, contaminate, or become equal authority" in front
    assert ".ai/control/boundary_material_routing.yaml" in front
    assert "Supporting boundary literature repo" in toc
    assert "never equal or superior authority to canonical Scripture" in toc


def test_t327a1_roadmap_records_governance_registry_and_no_output_change() -> None:
    text = ROADMAP.read_text(encoding="utf-8")
    assert "Governance Registry Source Of Truth" in text
    assert "governance/LOGOS_REPO_REGISTRY.yaml" in text
    assert "does not mutate data" in text
    assert "does not" in text and "start T327B" in text
    assert "If a task appears to require boundary material to modify canonical Scripture outputs" in text


def test_boundary_governance_stop_rules_are_machine_readable() -> None:
    data = policy()
    stop_rule = data["boundary_governance_constraint_policy"]
    assert stop_rule["policy_id"] == "BOUNDARY-GOV-001"
    assert stop_rule["title"] == "Governance Is Constraint, Not Obstacle"
    assert stop_rule["importance"] == "P0"
    assert stop_rule["required_behavior"] == "stop_and_create_human_escalation_warning"
    assert stop_rule["warning_required"] is True
    assert stop_rule["boundary_layer_may_treat_governance_as_blocker_or_obstacle"] is False
    assert stop_rule["boundary_layer_may_optimize_around_governance"] is False
    assert stop_rule["boundary_layer_may_auto_request_governance_change"] is False
    assert stop_rule["boundary_layer_may_auto_route_permission_request"] is False
    assert stop_rule["boundary_layer_may_bundle_governance_change_with_boundary_work"] is False


def test_boundary_originated_higher_layer_changes_are_owner_reserved() -> None:
    owner_policy = policy()["owner_reserved_authorization"]
    assert owner_policy["policy_id"] == "BOUNDARY-GOV-002"
    assert owner_policy["authorized_owner"] == "Lowell Wong"
    assert owner_policy["requires_explicit_owner_authorization"] is True
    assert owner_policy["authorization_must_occur_in_higher_authority_repo"] is True
    for key in [
        "contributor_consensus_sufficient",
        "contributor_volume_sufficient",
        "automated_recommendation_sufficient",
        "agent_routing_sufficient",
        "boundary_layer_operational_need_sufficient",
    ]:
        assert owner_policy[key] is False


def test_boundary_escalation_warning_is_available_to_agents() -> None:
    data = policy()
    assert data["boundary_layer_escalation_warning_text"] == WARNING_TEXT
    front = FRONT_DOOR.read_text(encoding="utf-8")
    assert WARNING_TEXT in front
    assert "BOUNDARY-GOV-001 - Governance Is Constraint, Not Obstacle" in ROADMAP.read_text(
        encoding="utf-8"
    )
    assert "BOUNDARY-GOV-002 - Owner-Reserved Authorization" in T327A2_ROADMAP.read_text(
        encoding="utf-8"
    )


def test_boundary_stop_rules_protect_higher_authority_targets() -> None:
    data = policy()
    protected = set(data["boundary_governance_constraint_policy"]["protected_higher_authority_targets"])
    assert "logos-governance-architecture" in protected
    assert "logos-scripture-graph" in protected
    assert "canonical_scripture_authority" in protected
    assert "repository_link_contracts" in protected
    assert "cross_repo_policy" in protected
    assert "trust_hierarchy" in protected
    assert "canonical_scope" in protected
    assert "boundary_originated_request_lacks_owner_authorization" in data["stop_triggers"]
