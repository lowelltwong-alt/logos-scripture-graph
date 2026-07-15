#!/usr/bin/env python3
"""Validate the governed Scripture-first biblical chunking family."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

try:
    from scripts import build_scripture_first_biblical_chunking_catalog as builder
except ImportError:  # pragma: no cover - direct script execution
    import build_scripture_first_biblical_chunking_catalog as builder


ROOT = Path(__file__).resolve().parent.parent
FAMILY_DIR = ROOT / "config" / "agents" / "families" / "scripture-first-biblical-chunking"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "scripture_first_biblical_chunking_family"
EXPECTATIONS = FIXTURE_DIR / "fixture_expectations.v1.json"
SCHEMA_PATHS = {
    "family": ROOT / "schemas" / "scripture-first-biblical-chunking-family.schema.json",
    "knowledge_manifest": ROOT / "schemas" / "biblical-chunking-knowledge-manifest.schema.json",
    "packet": ROOT / "schemas" / "biblical-chunking-packet.schema.json",
    "release": ROOT / "schemas" / "biblical-chunking-family-release.schema.json",
}
CONFIG_INSTANCES = {
    "family": FAMILY_DIR / "family.v1.yaml",
    "knowledge_manifest": FAMILY_DIR / "knowledge_manifest.v1.yaml",
    "release": FAMILY_DIR / "release.v1.yaml",
}
CANON_ALLOWLIST = ROOT / "config" / "canon" / "canonical_66_books.yaml"
FORM_REGISTRY = ROOT / "config" / "chunking" / "form_registry.yaml"
ROLES = FAMILY_DIR / "role_profiles.v1.yaml"
ROUTING = FAMILY_DIR / "routing_policy.v1.yaml"
PILOTS = FAMILY_DIR / "pilot_suite.v1.yaml"
AGENT_ROLES = ROOT / "config" / "agents" / "agent_roles.yaml"

PROHIBITED_FIRST_PASS = {
    "commentary",
    "creed",
    "systematic_theology",
    "denominational_outline",
    "modern_heading",
    "historical_reconstruction",
}
REQUIRED_CONTROL_ROLES = {
    "scripture_first_router",
    "scripture_first_authority_guardian",
    "scripture_first_family_architect",
    "scripture_first_foreman",
    "scripture_first_boundary_synthesizer",
    "scripture_first_anti_imputation_checker",
    "scripture_first_freshness_sentinel",
}
REQUIRED_CAMPAIGN_ROLES = {
    "scripture_first_parent_unit_worker": "Ezra",
    "scripture_first_child_necessity_reviewer": "Jethro",
    "scripture_first_textual_witness_specialist": "Jeremiah",
    "scripture_first_speaker_specialist": "John",
    "scripture_first_reviewed_gold_custodian": "Joshua",
    "scripture_first_model_map_calibrator": "Caleb",
    "scripture_first_evidence_dispute_boss": "Gamaliel",
    "scripture_first_human_docket_steward": "Esther",
}
REQUIRED_CONTROL_DISPLAY_NAMES = {
    "scripture_first_router": "Bezalel",
    "scripture_first_authority_guardian": "Esther",
    "scripture_first_family_architect": "Gamaliel",
    "scripture_first_foreman": "Nehemiah",
    "scripture_first_boundary_synthesizer": "Ezra",
    "scripture_first_anti_imputation_checker": "Nathan",
    "scripture_first_freshness_sentinel": "Haggai",
}
REQUIRED_SPECIALIST_PACKS = {
    "scripture_first_prose_discourse_specialist",
    "scripture_first_narrative_scene_specialist",
    "scripture_first_genealogy_list_specialist",
    "scripture_first_law_covenant_specialist",
    "scripture_first_psalms_poetry_specialist",
    "scripture_first_wisdom_dialogue_specialist",
    "scripture_first_prophetic_specialist",
    "scripture_first_gospel_specialist",
    "scripture_first_acts_specialist",
    "scripture_first_epistle_specialist",
    "scripture_first_apocalyptic_specialist",
    "scripture_first_hebrew_structure_specialist",
    "scripture_first_greek_structure_specialist",
    "scripture_first_canonical_intertext_specialist",
}
REQUIRED_ALIASES = {
    "chunking_architect",
    "biblical_literature_reviewer",
    "hebrew_reviewer",
    "greek_reviewer",
}
HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


class FamilyValidationError(RuntimeError):
    """Validation failure with a stable error code."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FamilyValidationError("BCF-FILE-INVALID", f"{_rel(path)}: {exc}") from exc
    if not isinstance(value, dict):
        raise FamilyValidationError("BCF-FILE-INVALID", f"{_rel(path)} must be an object")
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise FamilyValidationError("BCF-FILE-INVALID", f"{_rel(path)}: {exc}") from exc
    if not isinstance(value, dict):
        raise FamilyValidationError("BCF-FILE-INVALID", f"{_rel(path)} must be a mapping")
    return value


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _schema_errors(contract: str, instance: dict[str, Any]) -> list[str]:
    schema = _load_json(SCHEMA_PATHS[contract])
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def _pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise FamilyValidationError("BCF-FIXTURE-PATCH", f"invalid JSON pointer: {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def _apply_patch(document: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(document)
    for operation in operations:
        parts = _pointer_parts(str(operation.get("path", "")))
        parent = result
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        leaf = parts[-1]
        op = operation.get("op")
        if op == "remove":
            if isinstance(parent, list):
                parent.pop(int(leaf))
            else:
                del parent[leaf]
        elif op in {"add", "replace"}:
            value = copy.deepcopy(operation.get("value"))
            if isinstance(parent, list):
                if leaf == "-":
                    parent.append(value)
                elif op == "add":
                    parent.insert(int(leaf), value)
                else:
                    parent[int(leaf)] = value
            else:
                parent[leaf] = value
        else:
            raise FamilyValidationError("BCF-FIXTURE-PATCH", f"unsupported patch op: {op}")
    return result


def materialize_fixture(path: Path) -> dict[str, Any]:
    fixture = _load_json(path)
    if fixture.get("fixture_format") != "json_patch_fixture.v1":
        return fixture
    base = fixture.get("base_fixture")
    operations = fixture.get("operations")
    if not isinstance(base, str) or not isinstance(operations, list):
        raise FamilyValidationError("BCF-FIXTURE-PATCH", f"{_rel(path)} malformed patch fixture")
    return _apply_patch(_load_json(FIXTURE_DIR / base), operations)


def _raise(code: str, condition: bool, message: str) -> None:
    if condition:
        raise FamilyValidationError(code, message)


def _canonical_books() -> set[str]:
    books = _load_yaml(CANON_ALLOWLIST).get("canonical_66_books")
    if not isinstance(books, list) or len(books) != 66 or len(set(books)) != 66:
        raise FamilyValidationError("BCF-PACKET-CANONICAL-66", "canonical allowlist is not exactly 66 unique books")
    return {str(book) for book in books}


def validate_family_semantics(instance: dict[str, Any]) -> None:
    limits = instance.get("execution_limits", {})
    _raise("BCF-FAMILY-DELEGATION-DEPTH", limits.get("delegation_depth") != 1, "delegation depth must equal one")
    _raise("BCF-FAMILY-SPECIALIST-LIMIT", limits.get("max_active_domain_specialists") != 3, "maximum active specialists must equal three")
    constitution = instance.get("constitution", {})
    evidence = constitution.get("evidence_precedence", [])
    ranks = [item.get("rank") for item in evidence if isinstance(item, dict)]
    thematic_use = evidence[4].get("boundary_use") if len(evidence) >= 5 and isinstance(evidence[4], dict) else None
    _raise("BCF-FAMILY-EVIDENCE-PRECEDENCE", ranks != [1, 2, 3, 4, 5] or thematic_use not in {"candidate_only", "candidate_only_never_boundary_driver"}, "evidence precedence or thematic lane is invalid")
    prohibited = set(constitution.get("first_pass_prohibited_inputs", []))
    _raise("BCF-FAMILY-FIRST-PASS-EXCLUSION", not PROHIBITED_FIRST_PASS <= prohibited, "required first-pass exclusions are missing")
    campaign = instance.get("campaign_foundation", {})
    _raise("BCF-FAMILY-PARENT-FIRST", campaign.get("parent_units_first") is not True, "parent units must be proposed first")
    _raise("BCF-FAMILY-CHILD-DEFAULT", campaign.get("child_boundary_default") != "no_children", "child review must default to no children")
    _raise("BCF-FAMILY-MAJORITY-AUTHORITY", campaign.get("model_majority_is_truth") is not False, "model majority cannot be truth")
    maps = campaign.get("historical_model_maps", {})
    _raise("BCF-FAMILY-HISTORICAL-MAPS", maps.get("authority") != "evidence_only_no_vote" or maps.get("mechanical_outliers") != ["M1", "M5"], "historical model maps must remain non-voting evidence")


def _knowledge_cycles(entries: list[dict[str, Any]]) -> bool:
    graph = {str(entry.get("knowledge_id")): [str(item) for item in entry.get("depends_on", [])] for entry in entries}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dependency in graph.get(node, []):
            if dependency in graph and visit(dependency):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def validate_knowledge_semantics(instance: dict[str, Any], *, resolve_paths: bool = False) -> None:
    entries = instance.get("entries", [])
    if not isinstance(entries, list):
        raise FamilyValidationError("BCF-KNOWLEDGE-HASH-MISSING", "entries must be a list")
    knowledge_ids = [
        str(entry.get("knowledge_id"))
        for entry in entries
        if isinstance(entry, dict) and entry.get("knowledge_id")
    ]
    _raise(
        "BCF-KNOWLEDGE-DUPLICATE-ID",
        len(knowledge_ids) != len(set(knowledge_ids)),
        "knowledge_id values must be unique",
    )
    known_ids = set(knowledge_ids)
    authority_trust = {
        "owner_approved_local_governance": {"authority"},
        "logos_governed_policy": {"authority"},
        "logos_reviewed_evidence": {"reviewed", "asserted"},
        "logos_operational_registry": {"derived_metadata", "reviewed"},
        "candidate_reference": {"candidate"},
    }
    if resolve_paths:
        roles = _load_yaml(ROLES)
        known_roles = {
            str(item.get("profile_id"))
            for lane in ("control_roles", "observational_roles", "specialist_packs")
            for item in roles.get(lane, [])
            if isinstance(item, dict)
        }
    else:
        known_roles = {
            "authority-guardian",
            "boundary-synthesizer",
        }
    covered_roles: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise FamilyValidationError("BCF-KNOWLEDGE-HASH-MISSING", "entry must be an object")
        _raise(
            "BCF-KNOWLEDGE-PATH-MISSING",
            not isinstance(entry.get("source_path"), str) or not entry.get("source_path"),
            f"{entry.get('knowledge_id')}: source path missing",
        )
        allowed_authorities = {
            "owner_approved_local_governance",
            "logos_governed_policy",
            "logos_reviewed_evidence",
            "logos_operational_registry",
            "candidate_reference",
        }
        _raise(
            "BCF-KNOWLEDGE-UNAUTHORIZED-AUTHORITY",
            entry.get("authority") not in allowed_authorities,
            f"{entry.get('knowledge_id')}: unauthorized authority class",
        )
        if entry.get("authority") in authority_trust:
            _raise(
                "BCF-KNOWLEDGE-TRUST-MISMATCH",
                entry.get("trust_zone") not in authority_trust[entry["authority"]],
                f"{entry.get('knowledge_id')}: authority/trust-zone mismatch",
            )
        dependencies = entry.get("depends_on", [])
        _raise(
            "BCF-KNOWLEDGE-UNKNOWN-DEPENDENCY",
            any(dependency not in known_ids for dependency in dependencies),
            f"{entry.get('knowledge_id')}: unknown dependency",
        )
        applicable_roles = set(entry.get("applicable_roles", []))
        _raise(
            "BCF-KNOWLEDGE-UNKNOWN-ROLE",
            not applicable_roles <= known_roles,
            f"{entry.get('knowledge_id')}: unknown applicable role(s): {sorted(applicable_roles - known_roles)}",
        )
        if resolve_paths:
            covered_roles.update(applicable_roles)
        source_hash = entry.get("source_sha256")
        _raise("BCF-KNOWLEDGE-HASH-MISSING", not isinstance(source_hash, str) or not HASH_PATTERN.fullmatch(source_hash), f"{entry.get('knowledge_id')}: source hash missing")
        freshness = entry.get("freshness", {})
        _raise("BCF-KNOWLEDGE-STALE", freshness.get("status") != "current", f"{entry.get('knowledge_id')}: reference is not current")
        _raise("BCF-KNOWLEDGE-HASH-MISMATCH", freshness.get("verified_sha256") != source_hash, f"{entry.get('knowledge_id')}: verified hash differs")
        if resolve_paths:
            relative = entry.get("source_path")
            if not isinstance(relative, str):
                raise FamilyValidationError("BCF-KNOWLEDGE-MISSING", "source path missing")
            path = (ROOT / relative).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError as exc:
                raise FamilyValidationError("BCF-KNOWLEDGE-UNAUTHORIZED", f"reference escapes Logos: {relative}") from exc
            if not path.is_file():
                raise FamilyValidationError("BCF-KNOWLEDGE-MISSING", f"source does not resolve: {relative}")
            actual = f"sha256:{_sha256(path)}"
            _raise("BCF-KNOWLEDGE-HASH-MISMATCH", actual != source_hash, f"{relative}: declared hash differs from source")
    _raise("BCF-KNOWLEDGE-CYCLE", _knowledge_cycles(entries), "knowledge dependency cycle detected")
    if resolve_paths:
        specialist_ids = {
            str(item.get("profile_id"))
            for item in _load_yaml(ROLES).get("specialist_packs", [])
            if isinstance(item, dict)
        }
        _raise(
            "BCF-KNOWLEDGE-PACK-COVERAGE",
            not specialist_ids <= covered_roles,
            f"specialist packs lack knowledge coverage: {sorted(specialist_ids - covered_roles)}",
        )


def validate_packet_semantics(instance: dict[str, Any]) -> None:
    scope = instance.get("passage_scope", {})
    _raise("BCF-PACKET-CANONICAL-66", scope.get("book_id") not in _canonical_books(), "packet book is outside canonical 66")
    payload = instance.get("payload", {})
    packet_type = instance.get("packet_type")
    lane = instance.get("lane")
    parent_assignment = instance.get("parent_assignment_packet_id")
    if packet_type == "assignment":
        _raise(
            "BCF-PACKET-LANE-SEPARATION",
            parent_assignment is not None or payload.get("lane") != lane,
            "assignment lane must match the packet lane and cannot have a parent assignment",
        )
        writer = payload.get("writer", {}).get("agent_instance_id")
        checker = payload.get("checker", {}).get("agent_instance_id")
        _raise("BCF-PACKET-WRITER-CHECKER-COLLISION", not writer or writer == checker, "assignment writer and checker must differ")
        specialist_ids = payload.get("specialist_role_ids", [])
        assignment_roles = {
            assignment.get("role_id")
            for assignment in payload.get("assignments", [])
            if isinstance(assignment, dict)
        }
        _raise("BCF-PACKET-SPECIALIST-LIMIT", len(specialist_ids) > 3, "assignment activates more than three specialists")
        _raise(
            "BCF-PACKET-ASSIGNMENT-ROLE-LEAKAGE",
            not assignment_roles <= set(specialist_ids),
            "assignment role is hidden outside specialist_role_ids",
        )
    else:
        _raise(
            "BCF-PACKET-LANE-SEPARATION",
            not isinstance(parent_assignment, str) or not parent_assignment.startswith("bcf-packet:"),
            "non-assignment packet must reference its parent assignment",
        )
    if packet_type == "independent_review":
        writer = payload.get("writer_agent_instance_id")
        checker = payload.get("checker_agent_instance_id")
        creator = instance.get("created_by", {}).get("agent_instance_id")
        _raise(
            "BCF-PACKET-WRITER-CHECKER-COLLISION",
            writer == checker or creator != checker or creator == writer,
            "independent reviewer identity collides with writer or packet creator is not the checker",
        )
    if packet_type == "observation":
        _raise("BCF-PACKET-LANE-SEPARATION", bool(payload.get("boundary_candidates")), "observation packet contains boundary candidates")
    if packet_type == "candidate_set" and payload.get("theological_ambiguity"):
        _raise(
            "BCF-PACKET-THEOLOGICAL-HOLD",
            not payload.get("hold_for_owner")
            or payload.get("decision_state") != "hold_for_owner"
            or instance.get("status") != "hold_for_owner",
            "theological ambiguity must hold in payload and top-level status",
        )
    evidence_refs = [
        evidence for evidence in instance.get("evidence_refs", []) if isinstance(evidence, dict)
    ]
    evidence_ids = [evidence.get("evidence_id") for evidence in evidence_refs]
    _raise(
        "BCF-PACKET-DUPLICATE-EVIDENCE-ID",
        len(evidence_ids) != len(set(evidence_ids)),
        "packet evidence_id values must be unique",
    )
    evidence_by_id = {evidence["evidence_id"]: evidence for evidence in evidence_refs}
    expected_evidence = {
        "canonical_text": ("exact_canonical_text_and_structural_markers", 1, "not_applicable"),
        "structural_marker": ("exact_canonical_text_and_structural_markers", 1, "not_applicable"),
        "original_language_structural_observation": ("exact_canonical_text_and_structural_markers", 1, "not_applicable"),
        "immediate_context": ("immediate_discourse_paragraph_chapter_and_whole_book_context", 2, "not_applicable"),
        "explicit_canonical_quotation": ("explicit_quotations_parallel_accounts_and_clear_authorial_callbacks", 3, "explicit_quotation"),
        "canonical_parallel_account": ("explicit_quotations_parallel_accounts_and_clear_authorial_callbacks", 3, "parallel_account"),
        "clear_authorial_callback": ("explicit_quotations_parallel_accounts_and_clear_authorial_callbacks", 3, "clear_authorial_callback"),
        "repeated_formulation": ("strong_repeated_formulations_or_lexical_syntactic_echoes", 4, "repeated_formulation"),
        "lexical_syntactic_echo": ("strong_repeated_formulations_or_lexical_syntactic_echoes", 4, "lexical_syntactic_echo"),
        "thematic_similarity": ("thematic_similarity", 5, "thematic_similarity"),
        "verified_historical_context": ("verified_historical_context_non_authorizing", None, "not_applicable"),
    }
    for evidence in evidence_by_id.values():
        source_kind = evidence.get("source_kind")
        _raise("BCF-PACKET-PROHIBITED-FIRST-PASS-INPUT", source_kind in PROHIBITED_FIRST_PASS, f"prohibited first-pass input: {source_kind}")
        expected = expected_evidence.get(source_kind)
        if expected is not None:
            evidence_class, rank, relationship = expected
            _raise(
                "BCF-PACKET-EVIDENCE-CLASS-CONSISTENCY",
                evidence.get("evidence_class") != evidence_class
                or evidence.get("precedence_rank") != rank
                or evidence.get("relationship_basis") != relationship,
                f"{source_kind} is mislabeled across evidence class, rank, or relationship basis",
            )
        if evidence.get("evidence_class") == "thematic_similarity":
            _raise("BCF-PACKET-THEME-BOUNDARY", evidence.get("may_drive_boundary") is not False, "thematic similarity may not drive a boundary")
        if evidence.get("evidence_class") == "verified_historical_context_non_authorizing":
            _raise("BCF-PACKET-EXTERNAL-CONTEXT-NONAUTHORIZING", evidence.get("may_drive_boundary") is not False, "historical context may not drive a boundary")
        if source_kind == "original_language_structural_observation":
            forbidden_keys = {"doctrine_selection", "translation_selection", "preferred_reading", "source_tradition_preference"}
            _raise(
                "BCF-PACKET-ORIGINAL-LANGUAGE-NONAUTHORIZATION",
                bool(forbidden_keys & set(evidence)) or evidence.get("may_drive_boundary") is not False,
                "original-language evidence attempts a selection or drives a boundary",
            )
    historical_evidence = [
        evidence
        for evidence in evidence_by_id.values()
        if evidence.get("source_kind") == "verified_historical_context"
        or evidence.get("evidence_class") == "verified_historical_context_non_authorizing"
    ]
    if historical_evidence:
        _raise(
            "BCF-PACKET-LANE-SEPARATION",
            lane != "external_context_review"
            or packet_type not in {"observation", "challenge", "independent_review"},
            "historical context must be isolated in a separate non-authorizing external-context review packet",
        )
    if lane == "external_context_review":
        _raise(
            "BCF-PACKET-LANE-SEPARATION",
            packet_type not in {"observation", "challenge", "independent_review"} or not historical_evidence,
            "external-context lane is review-only and must contain verified historical evidence",
        )
    referenced_evidence: list[tuple[str, list[str]]] = []
    if packet_type == "observation":
        observations = payload.get("observations", [])
        observation_ids = [item.get("observation_id") for item in observations]
        _raise(
            "BCF-PACKET-DUPLICATE-OBSERVATION-ID",
            len(observation_ids) != len(set(observation_ids)),
            "observation_id values must be unique",
        )
        for observation in observations:
            referenced_evidence.append((str(observation.get("observation_id")), observation.get("evidence_ids", [])))
        known_observations = set(observation_ids)
        for inference in payload.get("inferences", []):
            unresolved = [item for item in inference.get("derived_from_observation_ids", []) if item not in known_observations]
            _raise(
                "BCF-PACKET-OBSERVATION-REF",
                bool(unresolved),
                f"{inference.get('inference_id')}: unresolved observation IDs: {unresolved}",
            )
    elif packet_type == "challenge":
        for finding in payload.get("findings", []):
            referenced_evidence.append((str(finding.get("finding_id")), finding.get("evidence_ids", [])))
    elif packet_type == "independent_review":
        for finding in payload.get("anti_imputation_findings", []):
            referenced_evidence.append((str(finding.get("finding_id")), finding.get("evidence_ids", [])))
    for reference_owner, reference_ids in referenced_evidence:
        unresolved = [item for item in reference_ids if item not in evidence_by_id]
        _raise(
            "BCF-PACKET-EVIDENCE-REF",
            bool(unresolved),
            f"{reference_owner}: unresolved evidence IDs: {unresolved}",
        )
    if packet_type == "candidate_set":
        for candidate in payload.get("candidates", []):
            supporting_ids = candidate.get("supporting_evidence_ids", [])
            unresolved_ids = [item for item in supporting_ids if item not in evidence_by_id]
            _raise(
                "BCF-PACKET-EVIDENCE-REF",
                bool(unresolved_ids),
                f"{candidate.get('candidate_id')}: unresolved supporting evidence IDs: {unresolved_ids}",
            )
            supporting = [evidence_by_id[item] for item in supporting_ids]
            eligible = [
                evidence
                for evidence in supporting
                if evidence
                and evidence.get("precedence_rank") in {1, 2, 3}
                and evidence.get("may_drive_boundary") is True
            ]
            _raise(
                "BCF-PACKET-CANDIDATE-EVIDENCE",
                not eligible,
                f"{candidate.get('candidate_id')}: candidate lacks boundary-eligible rank 1-3 evidence",
            )


def validate_release_semantics(instance: dict[str, Any], *, resolve_hashes: bool = False) -> None:
    dad = instance.get("dad_adaptation", {})
    _raise("BCF-RELEASE-DAD-PAYLOAD", any(dad.get(key) is True for key in ("contains_scripture_payload", "contains_source_payload", "contains_private_payload")), "DAD adaptation contains a prohibited payload")
    if dad.get("eligible"):
        ready = dad.get("framework_status") == "merged_reviewed" and dad.get("portfolio_drift_reconciled") is True and dad.get("logos_dad_hash_match") is True
        _raise("BCF-RELEASE-DAD-GATE", not ready, "DAD eligibility asserted before prerequisites")
    activation = instance.get("activation", {})
    _raise("BCF-RELEASE-ACTIVATION", activation.get("eligible") is True or activation.get("approved") is True, "candidate activation attempted")
    pilot = instance.get("pilot_status", {})
    if pilot.get("status") == "passed":
        _raise(
            "BCF-RELEASE-PILOT-EVIDENCE",
            pilot.get("reviewed_behavior_preserved") is not True
            or pilot.get("ambiguities_retained") is not True
            or pilot.get("chunk_outputs_changed") is not False,
            "passed pilot lacks preservation, ambiguity, or zero-change evidence",
        )
    shadow = instance.get("shadow_status", {})
    if shadow.get("status") == "passed":
        _raise(
            "BCF-RELEASE-SHADOW-EVIDENCE",
            shadow.get("canonical_books_accounted") != 66
            or shadow.get("noncanonical_records_admitted") != 0
            or shadow.get("candidate_auto_activation") is not False
            or shadow.get("chunk_outputs_changed") is not False,
            "passed shadow lacks canonical-66 or zero-activation evidence",
        )
    release_status = instance.get("release_status")
    if release_status == "shadow_candidate":
        _raise(
            "BCF-RELEASE-STATUS-TRANSITION",
            pilot.get("status") != "passed" or shadow.get("status") != "passed",
            "shadow_candidate requires passed pilot and shadow evidence",
        )
    if release_status == "dad_adaptation_eligible":
        _raise(
            "BCF-RELEASE-STATUS-TRANSITION",
            pilot.get("status") != "passed"
            or shadow.get("status") != "passed"
            or dad.get("eligible") is not True,
            "dad_adaptation_eligible requires passed pilot and shadow evidence plus DAD eligibility",
        )
    validation_evidence = instance.get("validation_evidence", [])
    if release_status == "owner_decision_ready":
        _raise(
            "BCF-RELEASE-READINESS",
            pilot.get("status") != "passed"
            or shadow.get("status") != "passed"
            or not validation_evidence
            or any(item.get("status") != "passed" for item in validation_evidence),
            "owner_decision_ready asserted without passed pilots, shadow, and validation",
        )
        for evidence in validation_evidence:
            reference = ROOT / str(evidence.get("evidence_ref"))
            declared = evidence.get("evidence_sha256")
            _raise(
                "BCF-RELEASE-VALIDATION-EVIDENCE",
                not reference.is_file()
                or not isinstance(declared, str)
                or not HASH_PATTERN.fullmatch(declared)
                or declared != f"sha256:{_sha256(reference)}",
                f"owner-ready validation evidence missing or hash-drifted: {_rel(reference)}",
            )
    status_evidence = (
        ("pilot", pilot, "BCF-RELEASE-PILOT-EVIDENCE-REF"),
        ("shadow", shadow, "BCF-RELEASE-SHADOW-EVIDENCE-REF"),
    )
    if resolve_hashes or release_status == "owner_decision_ready":
        for label, status_record, error_code in status_evidence:
            reference = ROOT / str(status_record.get("evidence_ref"))
            declared = status_record.get("evidence_sha256")
            _raise(
                error_code,
                not reference.is_file()
                or not isinstance(declared, str)
                or not HASH_PATTERN.fullmatch(declared)
                or declared != f"sha256:{_sha256(reference)}",
                f"{label} evidence missing or hash-drifted: {_rel(reference)}",
            )
    hashes = instance.get("constituent_hashes", [])
    identifiers = [item.get("constituent_id") for item in hashes if isinstance(item, dict)]
    _raise("BCF-RELEASE-DUPLICATE-CONSTITUENT", len(identifiers) != len(set(identifiers)), "duplicate release constituent ID")
    for item in hashes:
        declared = item.get("sha256")
        _raise("BCF-RELEASE-HASH", not isinstance(declared, str) or not HASH_PATTERN.fullmatch(declared), "invalid constituent hash")
        if resolve_hashes:
            source = ROOT / str(item.get("source_path"))
            if not source.is_file():
                raise FamilyValidationError("BCF-RELEASE-HASH", f"release constituent missing: {_rel(source)}")
            _raise("BCF-RELEASE-HASH", declared != f"sha256:{_sha256(source)}", f"release hash drift: {_rel(source)}")
    if resolve_hashes:
        for evidence in validation_evidence:
            reference = ROOT / str(evidence.get("evidence_ref"))
            declared = evidence.get("evidence_sha256")
            if not reference.is_file() or not isinstance(declared, str) or not HASH_PATTERN.fullmatch(declared):
                raise FamilyValidationError("BCF-RELEASE-VALIDATION-EVIDENCE", f"validation evidence is missing or unhashed: {_rel(reference)}")
            _raise(
                "BCF-RELEASE-VALIDATION-EVIDENCE",
                declared != f"sha256:{_sha256(reference)}",
                f"validation evidence hash drift: {_rel(reference)}",
            )


def validate_instance_semantics(contract: str, instance: dict[str, Any]) -> None:
    if contract == "family":
        validate_family_semantics(instance)
    elif contract == "knowledge_manifest":
        validate_knowledge_semantics(instance)
    elif contract == "packet":
        validate_packet_semantics(instance)
    elif contract == "release":
        validate_release_semantics(instance)
    else:
        raise FamilyValidationError("BCF-CONTRACT-UNKNOWN", contract)


def validate_fixture_expectations() -> dict[str, Any]:
    expectations = _load_json(EXPECTATIONS)
    cases = expectations.get("cases", [])
    if not isinstance(cases, list) or not cases:
        raise FamilyValidationError("BCF-FIXTURE-INDEX", "fixture expectations are empty")
    schema_valid_count = 0
    semantic_valid_count = 0
    for case in cases:
        path = FIXTURE_DIR / str(case.get("path"))
        contract = str(case.get("contract"))
        instance = materialize_fixture(path)
        errors = _schema_errors(contract, instance)
        schema_valid = not errors
        if schema_valid:
            schema_valid_count += 1
        if schema_valid != case.get("expected_schema_valid"):
            raise FamilyValidationError("BCF-FIXTURE-SCHEMA-EXPECTATION", f"{_rel(path)} schema expectation mismatch: {errors}")
        semantic_error: FamilyValidationError | None = None
        try:
            validate_instance_semantics(contract, instance)
        except FamilyValidationError as exc:
            semantic_error = exc
        semantic_valid = semantic_error is None
        if semantic_valid:
            semantic_valid_count += 1
        if semantic_valid != case.get("expected_family_validator_valid"):
            raise FamilyValidationError("BCF-FIXTURE-SEMANTIC-EXPECTATION", f"{_rel(path)} semantic expectation mismatch")
        expected_code = case.get("expected_error_code")
        if not semantic_valid and semantic_error and semantic_error.code != expected_code:
            raise FamilyValidationError("BCF-FIXTURE-ERROR-CODE", f"{_rel(path)} expected {expected_code}, got {semantic_error.code}")
    return {"case_count": len(cases), "schema_valid_count": schema_valid_count, "semantic_valid_count": semantic_valid_count}


def _validate_roles_and_routing() -> dict[str, int]:
    roles = _load_yaml(ROLES)
    routing = _load_yaml(ROUTING)
    control_ids = {str(item.get("profile_id")) for item in roles.get("control_roles", [])}
    control_names = {str(item.get("profile_id")): item.get("display_name") for item in roles.get("control_roles", [])}
    campaign_roles = {str(item.get("profile_id")): item for item in roles.get("campaign_roles", [])}
    pack_ids = {str(item.get("profile_id")) for item in roles.get("specialist_packs", [])}
    if control_ids != REQUIRED_CONTROL_ROLES:
        raise FamilyValidationError("BCF-ROLES-CONTROL-COVERAGE", f"control role mismatch: {sorted(control_ids ^ REQUIRED_CONTROL_ROLES)}")
    if any(control_names.get(role_id) != display_name for role_id, display_name in REQUIRED_CONTROL_DISPLAY_NAMES.items()):
        raise FamilyValidationError("BCF-ROLES-DISPLAY-IDENTITY", "control display identities are missing or mismatched")
    if set(campaign_roles) != set(REQUIRED_CAMPAIGN_ROLES):
        raise FamilyValidationError("BCF-ROLES-CAMPAIGN-COVERAGE", f"campaign role mismatch: {sorted(set(campaign_roles) ^ set(REQUIRED_CAMPAIGN_ROLES))}")
    if any(campaign_roles[role_id].get("display_name") != display_name for role_id, display_name in REQUIRED_CAMPAIGN_ROLES.items()):
        raise FamilyValidationError("BCF-ROLES-DISPLAY-IDENTITY", "campaign display identities are missing or mismatched")
    child = campaign_roles["scripture_first_child_necessity_reviewer"]
    if child.get("default_decision") != "no_children" or child.get("requires_existing_parent") is not True:
        raise FamilyValidationError("BCF-ROLES-CHILD-CONTRACT", "child reviewer must default to no children and require a parent")
    calibrator = campaign_roles["scripture_first_model_map_calibrator"]
    if calibrator.get("historical_map_authority") != "evidence_only_no_vote" or calibrator.get("mechanical_outlier_maps") != ["M1", "M5"]:
        raise FamilyValidationError("BCF-ROLES-MODEL-MAP-AUTHORITY", "historical model maps received authority")
    if campaign_roles["scripture_first_textual_witness_specialist"].get("may_select_preferred_reading") is not False:
        raise FamilyValidationError("BCF-ROLES-TEXTUAL-WITNESS-AUTHORITY", "textual-witness role may select a reading")
    if campaign_roles["scripture_first_speaker_specialist"].get("unresolved_speaker_action") != "hold_for_owner":
        raise FamilyValidationError("BCF-ROLES-SPEAKER-HOLD", "speaker ambiguity must hold for owner")
    if campaign_roles["scripture_first_reviewed_gold_custodian"].get("may_edit_or_promote_gold") is not False:
        raise FamilyValidationError("BCF-ROLES-GOLD-AUTHORITY", "reviewed-gold custodian may edit or promote gold")
    if campaign_roles["scripture_first_evidence_dispute_boss"].get("may_create_human_decision") is not False:
        raise FamilyValidationError("BCF-ROLES-BOSS-AUTHORITY", "evidence-dispute boss may create a human decision")
    if campaign_roles["scripture_first_human_docket_steward"].get("decision_authority") != "none":
        raise FamilyValidationError("BCF-ROLES-DOCKET-AUTHORITY", "human docket steward received decision authority")
    if any(not str(role.get("duty_anchor", "")).strip() for role in campaign_roles.values()):
        raise FamilyValidationError("BCF-ROLES-DUTY-ANCHOR", "campaign display identity lacks a duty anchor")
    if pack_ids != REQUIRED_SPECIALIST_PACKS:
        raise FamilyValidationError("BCF-ROLES-PACK-COVERAGE", f"specialist pack mismatch: {sorted(pack_ids ^ REQUIRED_SPECIALIST_PACKS)}")
    scope_gate = routing.get("scope_gate", {})
    if scope_gate.get("required_canon_profile") != "canonical_66":
        raise FamilyValidationError("BCF-ROUTING-CANONICAL-SCOPE", "router must require canonical_66")
    if scope_gate.get("front_matter_action") != "exclude_from_boundary_candidates_metadata_only":
        raise FamilyValidationError("BCF-ROUTING-FRONT-MATTER", "front matter must remain metadata-only")
    if scope_gate.get("early_church_tier_action") != "reject_excluded_noncanonical_or_boundary_material":
        raise FamilyValidationError("BCF-ROUTING-NONCANONICAL", "early-church forms must be rejected")
    routes = routing.get("primary_form_routes", {})
    if not isinstance(routes, dict):
        raise FamilyValidationError("BCF-ROUTING-FORM-COVERAGE", "primary_form_routes must be a mapping")
    form_data = _load_yaml(FORM_REGISTRY)
    expected_forms = {
        str(item.get("id"))
        for item in form_data.get("forms", [])
        if item.get("tier") not in {"front_matter", "early_church"}
    }
    if set(routes) != expected_forms:
        raise FamilyValidationError("BCF-ROUTING-FORM-COVERAGE", f"canonical form route mismatch: {sorted(set(routes) ^ expected_forms)}")
    unknown_packs = set(str(value) for value in routes.values()) - pack_ids
    if unknown_packs:
        raise FamilyValidationError("BCF-ROUTING-UNKNOWN-PACK", f"unknown routed packs: {sorted(unknown_packs)}")
    pack_form_owners: dict[str, list[str]] = {}
    for pack in roles.get("specialist_packs", []):
        for form_id in pack.get("form_ids", []):
            pack_form_owners.setdefault(str(form_id), []).append(str(pack.get("profile_id")))
    duplicate_forms = {form_id: owners for form_id, owners in pack_form_owners.items() if len(owners) != 1}
    if duplicate_forms:
        raise FamilyValidationError("BCF-ROUTING-FORM-LEAKAGE", f"forms assigned across packs: {duplicate_forms}")
    mismatched_routes = {
        form_id: pack_id
        for form_id, pack_id in routes.items()
        if pack_form_owners.get(str(form_id)) != [str(pack_id)]
    }
    if mismatched_routes:
        raise FamilyValidationError("BCF-ROUTING-FORM-LEAKAGE", f"route differs from pack ownership: {mismatched_routes}")
    augmentation_packs = {
        str(item.get("add_specialist"))
        for item in routing.get("augmentation_routes", [])
        if isinstance(item, dict) and item.get("add_specialist")
    }
    if not augmentation_packs <= pack_ids:
        raise FamilyValidationError("BCF-ROUTING-UNKNOWN-PACK", f"unknown augmentation packs: {sorted(augmentation_packs - pack_ids)}")
    campaign_augmentations = {
        str(item.get("when")): str(item.get("add_campaign_role"))
        for item in routing.get("augmentation_routes", [])
        if isinstance(item, dict) and item.get("add_campaign_role")
    }
    required_augmentations = {
        "variant_or_source_tradition_dependency": "scripture_first_textual_witness_specialist",
        "unresolved_speaker_identity_or_boundary": "scripture_first_speaker_specialist",
    }
    if any(campaign_augmentations.get(trigger) != role for trigger, role in required_augmentations.items()):
        raise FamilyValidationError("BCF-ROUTING-CAMPAIGN-AUGMENTATION", "textual-witness or speaker augmentation is missing")
    algorithm = routing.get("selection_algorithm", {})
    if algorithm.get("maximum_active_domain_specialists") != 3:
        raise FamilyValidationError("BCF-FAMILY-SPECIALIST-LIMIT", "routing specialist limit differs")
    if algorithm.get("delegation_depth") != 1:
        raise FamilyValidationError("BCF-FAMILY-DELEGATION-DEPTH", "routing delegation depth differs")
    campaign_contract = routing.get("campaign_assignment_contract", {})
    if campaign_contract.get("parent_worker") not in campaign_roles or campaign_contract.get("child_reviewer") not in campaign_roles:
        raise FamilyValidationError("BCF-ROUTING-CAMPAIGN-ROLE", "campaign parent/child route is missing")
    if campaign_contract.get("cross_packet_enforcement_deferred_to") != "T512":
        raise FamilyValidationError("BCF-ROUTING-RUNTIME-OWNER", "cross-packet enforcement must remain assigned to T512")
    return {"control_roles": len(control_ids), "campaign_roles": len(campaign_roles), "specialist_packs": len(pack_ids), "routed_forms": len(routes)}


def _validate_aliases() -> int:
    agent_roles = _load_yaml(AGENT_ROLES)
    aliases = agent_roles.get("compatibility_aliases", {})
    if not isinstance(aliases, dict) or not REQUIRED_ALIASES <= set(aliases):
        raise FamilyValidationError("BCF-ALIASES-MISSING", f"missing compatibility aliases: {sorted(REQUIRED_ALIASES - set(aliases or {}))}")
    for alias in REQUIRED_ALIASES:
        value = aliases[alias]
        if not isinstance(value, dict) or not str(value.get("target_profile", "")).startswith("scripture_first_"):
            raise FamilyValidationError("BCF-ALIASES-INVALID", f"{alias} does not point to a Scripture-first profile")
    return len(REQUIRED_ALIASES)


def _validate_pilot_refs() -> int:
    pilots = _load_yaml(PILOTS)
    count = 0
    for lane in ("reviewed_invariants", "ambiguity_holds", "breadth_cases"):
        cases = pilots.get(lane, [])
        if not isinstance(cases, list):
            raise FamilyValidationError("BCF-PILOT-SHAPE", f"{lane} must be a list")
        for case in cases:
            count += 1
            evidence_ref = case.get("evidence_ref")
            if evidence_ref and not (ROOT / str(evidence_ref)).is_file():
                raise FamilyValidationError("BCF-PILOT-REFERENCE", f"missing pilot evidence: {evidence_ref}")
    if count != 15:
        raise FamilyValidationError("BCF-PILOT-COVERAGE", f"expected 15 controlled cases, found {count}")
    return count


def validate_repository() -> dict[str, Any]:
    for contract, path in CONFIG_INSTANCES.items():
        instance = _load_yaml(path)
        errors = _schema_errors(contract, instance)
        if errors:
            raise FamilyValidationError("BCF-CONFIG-SCHEMA", f"{_rel(path)}: {errors[0]}")
        if contract == "family":
            validate_family_semantics(instance)
        elif contract == "knowledge_manifest":
            validate_knowledge_semantics(instance, resolve_paths=True)
        elif contract == "release":
            validate_release_semantics(instance, resolve_hashes=True)
    roles = _validate_roles_and_routing()
    alias_count = _validate_aliases()
    pilot_count = _validate_pilot_refs()
    fixtures = validate_fixture_expectations()
    try:
        outputs = builder.build_outputs()
        builder._write_or_check(outputs, check=True)
    except builder.BuildError as exc:
        raise FamilyValidationError("BCF-GENERATED-STALE", str(exc)) from exc
    shadow = _load_json(builder.SHADOW_REPORT)
    if shadow.get("accounted_passage_count") != 31_103 or shadow.get("canonical_book_count") != 66:
        raise FamilyValidationError("BCF-SHADOW-COVERAGE", "whole-Bible shadow does not account for canonical corpus")
    if shadow.get("candidate_activations") != 0 or shadow.get("chunk_outputs_changed") != 0:
        raise FamilyValidationError("BCF-SHADOW-AUTHORITY", "shadow activated candidates or changed output")
    dad = _load_json(builder.DAD_ADAPTATION)
    if dad.get("eligible_for_dad_publication") is not False or dad.get("contains_scripture_text") is not False or dad.get("contains_source_rows") is not False:
        raise FamilyValidationError("BCF-RELEASE-DAD-PAYLOAD", "generated DAD adaptation violates hold or payload rules")
    return {"contracts": 4, "roles": roles, "aliases": alias_count, "pilot_cases": pilot_count, "fixtures": fixtures, "shadow_passages": 31_103, "dad_publication_eligible": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit validation summary as JSON")
    args = parser.parse_args()
    try:
        result = validate_repository()
    except FamilyValidationError as exc:
        print(f"Scripture-first biblical chunking family validation failed: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(
            "Scripture-first biblical chunking family validation passed: "
            f"{result['roles']['control_roles']} controls, {result['roles']['specialist_packs']} packs, "
            f"{result['roles']['routed_forms']} forms, {result['pilot_cases']} pilot cases, "
            f"{result['shadow_passages']} canonical passages accounted; DAD publication remains held."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
