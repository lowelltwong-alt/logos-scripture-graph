from __future__ import annotations

import json
import copy
from pathlib import Path

import pytest

from scripts import build_scripture_first_biblical_chunking_catalog as builder
from scripts import validate_scripture_first_biblical_chunking_family as validator


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "scripture_first_biblical_chunking_family"


def _expectation_cases() -> list[dict]:
    data = json.loads((FIXTURE_DIR / "fixture_expectations.v1.json").read_text(encoding="utf-8"))
    return data["cases"]


def test_repository_family_contract_is_valid_and_held() -> None:
    result = validator.validate_repository()

    assert result["contracts"] == 4
    assert result["roles"] == {
        "control_roles": 7,
        "campaign_roles": 8,
        "specialist_packs": 14,
        "routed_forms": 19,
    }
    assert result["aliases"] == 4
    assert result["pilot_cases"] == 15
    assert result["shadow_passages"] == 31_103
    assert result["dad_publication_eligible"] is False


@pytest.mark.parametrize("case", _expectation_cases(), ids=lambda case: case["path"])
def test_schema_and_semantic_fixture_expectations(case: dict) -> None:
    instance = validator.materialize_fixture(FIXTURE_DIR / case["path"])
    schema_errors = validator._schema_errors(case["contract"], instance)
    assert (not schema_errors) is case["expected_schema_valid"]

    error = None
    try:
        validator.validate_instance_semantics(case["contract"], instance)
    except validator.FamilyValidationError as exc:
        error = exc

    assert (error is None) is case["expected_family_validator_valid"]
    if error is not None:
        assert error.code == case["expected_error_code"]


def test_generated_catalog_is_deterministic_and_payload_free() -> None:
    outputs = builder.build_outputs()
    builder._write_or_check(outputs, check=True)

    catalog = outputs[builder.KNOWLEDGE_CATALOG]
    assert catalog["entry_count"] == 29
    assert catalog["contains_scripture_or_source_payloads"] is False
    assert [entry["knowledge_id"] for entry in catalog["entries"]] == sorted(
        entry["knowledge_id"] for entry in catalog["entries"]
    )


def test_whole_bible_shadow_accounts_for_scope_without_claiming_boundaries() -> None:
    shadow = json.loads(builder.SHADOW_REPORT.read_text(encoding="utf-8"))

    assert shadow["accounted_passage_count"] == 31_103
    assert shadow["canonical_book_count"] == 66
    assert shadow["missing_canonical_books"] == []
    assert shadow["unexpected_or_noncanonical_books"] == []
    assert shadow["noncanonical_default_scope_rows"] == 0
    assert shadow["specialist_activation_counts"] == {}
    assert shadow["boundary_proposals_emitted"] == 0
    assert shadow["candidate_activations"] == 0
    assert shadow["chunk_outputs_changed"] == 0
    assert shadow["gate_results"]["candidate_boundary_trial_complete"] is False
    assert shadow["gate_results"]["whole_bible_shadow_gate_passed"] is False


def test_controlled_pilot_preflight_retains_ambiguity_holds() -> None:
    report = json.loads(builder.PILOT_REPORT.read_text(encoding="utf-8"))
    cases = {case["case_id"]: case for case in report["cases"]}

    assert report["case_count"] == 15
    assert report["boundary_proposals_emitted"] == 0
    assert report["automatic_candidates_activated"] == 0
    assert cases["john_3"]["route_state"] == "hold_for_owner_required"
    assert cases["first_corinthians_8_10"]["route_state"] == "hold_for_owner_required"
    assert cases["genesis_5"]["expected_primary_pack"] == "scripture_first_genealogy_list_specialist"
    assert cases["revelation_1"]["expected_primary_pack"] == "scripture_first_apocalyptic_specialist"


def test_dad_adaptation_is_hash_linked_metadata_only_and_ineligible() -> None:
    adaptation = json.loads(builder.DAD_ADAPTATION.read_text(encoding="utf-8"))

    assert adaptation["eligible_for_dad_publication"] is False
    assert adaptation["contains_scripture_text"] is False
    assert adaptation["contains_source_rows"] is False
    assert adaptation["contains_private_conversations"] is False
    assert adaptation["contains_logos_authority"] is False
    assert adaptation["dad_may_override_logos_governance"] is False
    assert adaptation["dad_may_write_or_push_into_logos"] is False
    assert len(adaptation["constituent_hashes"]) == 6
    assert adaptation["blockers"]


def test_role_rules_are_isolated_by_primary_form() -> None:
    roles = validator._load_yaml(validator.ROLES)
    routing = validator._load_yaml(validator.ROUTING)
    pack_forms = {
        pack["profile_id"]: set(pack.get("form_ids", []))
        for pack in roles["specialist_packs"]
    }

    for form_id, pack_id in routing["primary_form_routes"].items():
        assert form_id in pack_forms[pack_id]
    assert pack_forms["scripture_first_hebrew_structure_specialist"] == set()
    assert pack_forms["scripture_first_greek_structure_specialist"] == set()
    assert pack_forms["scripture_first_canonical_intertext_specialist"] == set()


def test_campaign_roles_preserve_parent_child_and_non_voting_map_contracts() -> None:
    roles = validator._load_yaml(validator.ROLES)
    campaign = {role["profile_id"]: role for role in roles["campaign_roles"]}

    assert campaign["scripture_first_parent_unit_worker"]["display_name"] == "Ezra"
    assert campaign["scripture_first_child_necessity_reviewer"]["default_decision"] == "no_children"
    assert campaign["scripture_first_child_necessity_reviewer"]["requires_existing_parent"] is True
    assert campaign["scripture_first_reviewed_gold_custodian"]["may_edit_or_promote_gold"] is False
    assert campaign["scripture_first_model_map_calibrator"]["historical_map_authority"] == "evidence_only_no_vote"
    assert campaign["scripture_first_human_docket_steward"]["decision_authority"] == "none"


def test_family_semantics_rejects_child_first_campaign() -> None:
    family = validator._load_yaml(validator.FAMILY_DIR / "family.v1.yaml")
    family["campaign_foundation"]["parent_units_first"] = False

    with pytest.raises(validator.FamilyValidationError, match="BCF-FAMILY-PARENT-FIRST"):
        validator.validate_family_semantics(family)


def test_family_semantics_rejects_model_majority_as_truth() -> None:
    family = validator._load_yaml(validator.FAMILY_DIR / "family.v1.yaml")
    family["campaign_foundation"]["model_majority_is_truth"] = True

    with pytest.raises(validator.FamilyValidationError, match="BCF-FAMILY-MAJORITY-AUTHORITY"):
        validator.validate_family_semantics(family)


def test_compatibility_aliases_preserve_legacy_roles() -> None:
    roles = validator._load_yaml(validator.AGENT_ROLES)
    aliases = roles["compatibility_aliases"]

    for role_id in validator.REQUIRED_ALIASES:
        assert aliases[role_id]["legacy_role_retained"] is True
        assert aliases[role_id]["target_family"] == "scripture-first-biblical-chunking"
        assert aliases[role_id]["target_profile"].startswith("scripture_first_")


def _mutated_routing_check(monkeypatch: pytest.MonkeyPatch, *, mutate_roles=None, mutate_routing=None) -> None:
    original = validator._load_yaml
    roles = copy.deepcopy(original(validator.ROLES))
    routing = copy.deepcopy(original(validator.ROUTING))
    if mutate_roles:
        mutate_roles(roles)
    if mutate_routing:
        mutate_routing(routing)

    def load(path: Path) -> dict:
        if path == validator.ROLES:
            return roles
        if path == validator.ROUTING:
            return routing
        return original(path)

    monkeypatch.setattr(validator, "_load_yaml", load)
    validator._validate_roles_and_routing()


def test_route_isolation_rejects_duplicate_form_ownership(monkeypatch: pytest.MonkeyPatch) -> None:
    def mutate(roles: dict) -> None:
        roles["specialist_packs"][1]["form_ids"].append("prose_paragraph")

    with pytest.raises(validator.FamilyValidationError, match="BCF-ROUTING-FORM-LEAKAGE"):
        _mutated_routing_check(monkeypatch, mutate_roles=mutate)


def test_routing_rejects_noncanonical_default_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    def mutate(routing: dict) -> None:
        routing["scope_gate"]["required_canon_profile"] = "canonical_80"

    with pytest.raises(validator.FamilyValidationError, match="BCF-ROUTING-CANONICAL-SCOPE"):
        _mutated_routing_check(monkeypatch, mutate_routing=mutate)


def test_routing_rejects_front_matter_boundary_candidates(monkeypatch: pytest.MonkeyPatch) -> None:
    def mutate(routing: dict) -> None:
        routing["scope_gate"]["front_matter_action"] = "emit_candidate_boundary"

    with pytest.raises(validator.FamilyValidationError, match="BCF-ROUTING-FRONT-MATTER"):
        _mutated_routing_check(monkeypatch, mutate_routing=mutate)
