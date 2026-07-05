from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_t451_bible_edge_candidate_type_catalog.py"
CONTROL = ROOT / ".ai" / "control" / "bible_edge_candidate_type_catalog.yaml"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_t451", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def load_catalog() -> dict:
    return yaml.safe_load(CONTROL.read_text(encoding="utf-8"))


def test_t451_validator_passes_current_catalog() -> None:
    module = load_validator()
    assert module.main() == 0


def test_t451_rejects_graph_generation_authority() -> None:
    module = load_validator()
    data = load_catalog()
    data["authority_boundary"]["generates_graph_edges"] = True
    with pytest.raises(module.T451CatalogError, match="generates_graph_edges"):
        module.validate_catalog(data)


def test_t451_requires_wj_and_original_language_frontier_guards() -> None:
    module = load_validator()
    data = load_catalog()
    data["frontier_escalation_required_for"]["families"].remove("linguistic_original_language")
    with pytest.raises(module.T451CatalogError, match="linguistic_original_language"):
        module.validate_catalog(data)

    data = load_catalog()
    data["frontier_escalation_required_for"]["triggers"].remove("WJ_or_speaker_boundary")
    with pytest.raises(module.T451CatalogError, match="WJ_or_speaker_boundary"):
        module.validate_catalog(data)


def test_t451_requires_key_bible_edge_types() -> None:
    module = load_validator()
    data = load_catalog()
    data["candidate_edge_types"] = [
        edge for edge in data["candidate_edge_types"] if edge["edge_type_id"] != "feast_calendar_worship_unit"
    ]
    with pytest.raises(module.T451CatalogError, match="feast_calendar_worship_unit"):
        module.validate_catalog(data)

    data = load_catalog()
    data["candidate_edge_types"] = [
        edge for edge in data["candidate_edge_types"] if edge["edge_type_id"] != "person_kinship_office_role_evidence"
    ]
    with pytest.raises(module.T451CatalogError, match="person_kinship_office_role_evidence"):
        module.validate_catalog(data)

    data = load_catalog()
    data["candidate_edge_types"] = [
        edge for edge in data["candidate_edge_types"] if edge["edge_type_id"] != "site_or_route_identification_candidate"
    ]
    with pytest.raises(module.T451CatalogError, match="site_or_route_identification_candidate"):
        module.validate_catalog(data)


def test_t451_rejects_high_risk_type_without_authority_denial() -> None:
    module = load_validator()
    data = load_catalog()
    candidate = copy.deepcopy(data)
    for edge in candidate["candidate_edge_types"]:
        if edge["edge_type_id"] == "fulfillment_claim_candidate":
            edge["never_auto_create"] = ["automatic_fulfillment"]
            break
    with pytest.raises(module.T451CatalogError, match="fulfillment_claim_candidate"):
        module.validate_catalog(candidate)


def test_t451_requires_global_never_auto_create_for_apologetic_truth() -> None:
    module = load_validator()
    data = load_catalog()
    data["global_evidence_floor"]["universal_never_auto_create"].remove("apologetic_conclusion_as_truth")
    with pytest.raises(module.T451CatalogError, match="apologetic_conclusion_as_truth"):
        module.validate_catalog(data)


def test_t451_rejects_registered_predicate_snapshot_drift() -> None:
    module = load_validator()
    data = load_catalog()
    data["current_registered_predicates"]["predicates"].append("fakeRegisteredPredicate")
    with pytest.raises(module.T451CatalogError, match="fakeRegisteredPredicate"):
        module.validate_catalog(data)

    data = load_catalog()
    data["current_registered_predicates"]["predicates"].remove("quotesFrom")
    with pytest.raises(module.T451CatalogError, match="quotesFrom"):
        module.validate_catalog(data)


def test_t451_rejects_medium_risk_type_without_authority_denial() -> None:
    module = load_validator()
    data = load_catalog()
    candidate = copy.deepcopy(data)
    for edge in candidate["candidate_edge_types"]:
        if edge["edge_type_id"] == "explicit_quotation_candidate":
            edge["never_auto_create"] = ["automatic_quote"]
            break
    with pytest.raises(module.T451CatalogError, match="explicit_quotation_candidate"):
        module.validate_catalog(candidate)
