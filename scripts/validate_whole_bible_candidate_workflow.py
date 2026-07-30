#!/usr/bin/env python3
"""Validate the provider-neutral whole-Bible candidate campaign replay pack."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
FAMILY = ROOT / "config" / "agents" / "families" / "scripture-first-biblical-chunking"
WORKFLOW = FAMILY / "whole_bible_candidate_workflow.v1.yaml"
PROMPTS = FAMILY / "whole_bible_candidate_prompt_pack.v1.yaml"
ADAPTER = FAMILY / "codex_desktop_campaign_adapter.v1.yaml"
FAMILY_FILE = FAMILY / "family.v1.yaml"
ROLES = FAMILY / "role_profiles.v1.yaml"
RELEASE = FAMILY / "release.v1.yaml"
M7_CONTRACT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "review_contract.yaml"
M7_PROMPT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "campaign_prompt.md"
M7_CAMPAIGN = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "campaign.json"
M7_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
M7_RUNTIME_EVIDENCE = M7_ROOT / "runtime" / "codex_adapter.yaml"
M7_MODEL_MANIFEST = M7_ROOT / "model_manifest.yaml"
CANON = ROOT / "config" / "canon" / "canonical_66_books.yaml"
BUNDLE_REF = ".ai/scratch/multi_model_bible_chunking/M7_sol/checks/validate_book_completion_bundle.py"


class WorkflowValidationError(ValueError):
    """Raised when the replay pack violates a required invariant."""


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise WorkflowValidationError(f"missing {path.relative_to(ROOT).as_posix()}")
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise WorkflowValidationError(f"{path.relative_to(ROOT).as_posix()}: invalid YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise WorkflowValidationError(f"{path.relative_to(ROOT).as_posix()}: expected mapping")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WorkflowValidationError(message)


def require_candidate_scoped_path(value: Any, label: str) -> None:
    require(isinstance(value, str) and value, f"{label}: path must be non-empty")
    normalized = value.replace("\\", "/")
    parts = normalized.split("/")
    require(not normalized.startswith("/") and re.match(r"^[A-Za-z]:", normalized) is None, f"{label}: absolute path forbidden")
    require(all(part not in {"", ".", ".."} for part in parts), f"{label}: traversal or empty component forbidden")
    materialized = re.sub(r"<[A-Za-z_][A-Za-z0-9_]*>", "__template__", normalized)
    resolved = (ROOT / materialized).resolve()
    try:
        resolved.relative_to(M7_ROOT.resolve())
    except ValueError as exc:
        raise WorkflowValidationError(f"{label}: path escapes candidate model root: {value}") from exc

def validate_qualification_boundary(execution: dict[str, Any]) -> None:
    require(execution.get("mode") == "specification_only", "QF-14-QUALIFIED-BY-LABEL: live campaign must remain specification-only")
    require(
        execution.get("qualification_status")
        == "blocked_pending_materialized_B00_B10_terminal_completion_dry_replay_dimensional_calibration_and_independent_launch_review",
        "QF-14-QUALIFIED-BY-LABEL: qualification block missing or incomplete",
    )
    require(execution.get("launch_command") == "not-authorized", "QF-14-QUALIFIED-BY-LABEL: campaign launch must remain unauthorized")
    require(execution.get("auto_advance_requires_qualification_receipt") is True, "QF-14-QUALIFIED-BY-LABEL: qualification receipt must gate auto-advance")

def require_true(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(key for key in keys if mapping.get(key) is not True)
    require(not missing, f"{label}: required true fields missing or false: {missing}")


def validate_workflow() -> None:
    data = load_yaml(WORKFLOW)
    require(data.get("object_type") == "scripture_first_whole_bible_candidate_workflow", "workflow object_type mismatch")
    require(data.get("schema_version") == "scripture_first_whole_bible_candidate_workflow.v1", "workflow schema mismatch")
    require(data.get("artifact_class") == "portable_core", "workflow must be portable_core")
    require(data.get("lifecycle_status") == "candidate", "workflow must remain candidate")
    require(data.get("trust_zone") == "candidate", "workflow trust zone must remain candidate")
    require(data.get("workflow_version") == "1.2.0", "workflow version must be 1.2.0")
    require(data.get("non_authorizing") is True, "workflow must be non-authorizing")

    independence = data.get("independence_contract")
    require(isinstance(independence, dict), "workflow independence_contract missing")
    dimensions = independence.get("required_dimensions")
    require(isinstance(dimensions, dict), "workflow independence dimensions missing")
    require_true(
        dimensions,
        {
            "authoring_independent_from_sibling_maps",
            "primary_reviews_blind_to_each_other_artifacts",
            "reviewer_roles_separated",
            "writer_and_checker_attempt_ids_distinct",
            "shared_model_substrate_disclosed",
            "independent_model_or_provider_evidence_required_for_convergence",
            "reviewer_count_is_not_authority",
        },
        "workflow independence dimensions",
    )
    forbidden_claims = set(independence.get("forbidden_claims_without_external_evidence") or [])
    require(
        {"independent_model_consensus", "cross_provider_agreement", "multiple_independent_votes"}.issubset(forbidden_claims),
        "workflow must forbid unproved independent-model claims",
    )
    require(independence.get("correlated_mesh_weight_at_convergence") == "one_model_voice", "correlated mesh must count as one voice")

    stages = data.get("book_lifecycle")
    require(isinstance(stages, list), "workflow book_lifecycle missing")
    stage_ids = [stage.get("stage_id") for stage in stages if isinstance(stage, dict)]
    require(stage_ids == [f"B{index:02d}" for index in range(11)], f"workflow stages must be B00-B10 in order, got {stage_ids}")
    by_id = {stage["stage_id"]: stage for stage in stages}
    bindings = data.get("executable_stage_bindings")
    require(isinstance(bindings, dict) and list(bindings) == stage_ids, "executable stage bindings must cover B00-B10 in order")
    for stage_id, binding in bindings.items():
        require(isinstance(binding, dict), f"{stage_id}: executable binding must be an object")
        require(isinstance(binding.get("executor"), str) and binding["executor"], f"{stage_id}: executor missing")
        require(isinstance(binding.get("prompt_templates"), list), f"{stage_id}: prompt template bindings missing")
        require(isinstance(binding.get("receipt_kind"), str) and binding["receipt_kind"], f"{stage_id}: receipt kind missing")

    source_routing = data.get("source_routing_contract")
    require(isinstance(source_routing, dict), "source routing contract missing")
    require(source_routing.get("manifests_are_pinned_not_assumed") is True, "source manifests must be pinned")
    require(len(source_routing.get("old_testament_hebrew_and_aramaic") or []) >= 2, "OT Hebrew/Aramaic source routing incomplete")
    require(len(source_routing.get("new_testament_koine_greek") or []) >= 3, "NT Greek source routing incomplete")
    ancient = source_routing.get("second_temple_rabbinic_and_ancient_context") or {}
    require(ancient.get("simulation_forbidden") is True, "ancient-context simulation must be forbidden")
    require(ancient.get("current_default") == "corpus_gap_record_required", "unavailable ancient corpus must produce a gap")

    receipt_contract = data.get("stage_receipt_contract")
    require(isinstance(receipt_contract, dict), "stage receipt contract missing")
    required_receipt_fields = set(receipt_contract.get("required_fields") or [])
    require(
        {
            "book", "run_id", "stage_id", "attempt_id", "attempt_kind", "prompt_pack_sha256", "workflow_sha256",
            "runtime_adapter_sha256", "input_manifest_path", "input_manifest_sha256", "output_manifest_path", "output_manifest_sha256", "input_artifact_sha256", "output_artifact_sha256",
            "prior_stage_receipt_sha256", "outcome", "shared_model_substrate",
            "counts_as_cross_model_independent_vote", "independence_scope", "state_fingerprint",
        }.issubset(required_receipt_fields),
        "stage receipt contract lacks replay-critical fields",
    )
    stage_specific = receipt_contract.get("stage_specific_required_fields") or {}
    require(
        {"form_inventory_sha256", "hardest_passage_forecast_sha256", "source_gap_register_sha256"}
        .issubset(set(stage_specific.get("B01") or [])),
        "B01 receipt lacks form-inventory closure",
    )
    require(
        {"primary_role_ids", "frozen_chunks_sha256", "prompt_template_sha256", "review_revision"}
        .issubset(set(stage_specific.get("B04") or [])),
        "B04 receipt lacks primary role/revision freshness fields",
    )
    require(
        {"extended_evidence_manifest_sha256", "precompletion_stage_receipts_B00_B09", "completion_gate_bundle_sha256", "terminal_completion_receipt_path_intent"}
        .issubset(set(stage_specific.get("B10") or [])),
        "B10 receipt lacks extended evidence closure",
    )
    blockers = set(data.get("replay_qualification_blockers") or [])
    require(
        {
            "actual_B00_B10_stage_receipts_absent_or_invalid",
            "one_book_dry_replay_absent_or_failed",
            "form_inventory_artifact_or_B01_receipt_absent",
            "primary_role_identity_or_revision_freshness_unproved",
            "extended_evidence_manifest_or_hash_closure_unproved",
            "independent_launch_review_absent",
        }.issubset(blockers),
        "replay qualification blockers are incomplete",
    )
    boss_fields = set(receipt_contract.get("boss_stage_required_fields") or [])
    require(
        {"provisional_commit_receipt_sha256", "provisional_committed_before_peer_premortem_exposure", "final_commit_receipt_sha256"}.issubset(boss_fields),
        "boss stage receipt lacks provisional-first proof",
    )

    completion = data.get("completion_semantics") or {}
    appeal_progression = completion.get("unresolved_reasoned_appeal") or {}
    require(appeal_progression.get("blocks_promotion_and_cross_model_convergence") is True, "appeals must block promotion")
    require(appeal_progression.get("does_not_block_starting_the_next_canonical_book") is True, "appeal progression rule must be explicit")
    shared_write = data.get("shared_sidecar_write_contract") or {}
    require_true(
        shared_write,
        {
            "concurrent_book_writes_forbidden",
            "exclusive_campaign_lock_required",
            "atomic_replace_required",
            "backup_and_recovery_receipt_required_after_detected_corruption",
        },
        "shared sidecar write contract",
    )
    boss_sequence = by_id["B06"].get("sequencing") or []
    require(
        boss_sequence.index("boss_records_provisional_ruling_and_digest")
        < boss_sequence.index("only_then_boss_reads_peer_and_premortem"),
        "boss must freeze a provisional ruling before peer/premortem input",
    )
    package_order = by_id["B10"].get("ordering") or []
    require("write_terminal_completion_receipt_last" in package_order, "terminal completion receipt must be written last")

    gate_rows = data.get("required_completion_gates")
    require(isinstance(gate_rows, list), "required_completion_gates missing")
    gate_by_id = {row.get("gate_id"): row for row in gate_rows if isinstance(row, dict)}
    required_gates = {"exact_coverage", "official_chunk_map_schema", "review_packet_parity", "literary_quality", "workflow_replay_contract", "materialized_stage_chain_precompletion"}
    require(required_gates.issubset(gate_by_id), f"missing completion gates: {sorted(required_gates - set(gate_by_id))}")
    official_command = str(gate_by_id["official_chunk_map_schema"].get("command_template", ""))
    require("validate_whole_bible_chunk_map.py" in official_command and "--book <Book>" in official_command, "official chunk-map gate malformed")

    format_contract = data.get("format_contract")
    require(isinstance(format_contract, dict), "format_contract missing")
    require(
        format_contract.get("chunk_index_in_book") == "positive_contiguous_integer_separate_from_decision_id",
        "chunk index contract must require positive contiguous integers",
    )
    statuses = format_contract.get("review_status_values") or {}
    require(statuses.get("accepted") == "candidate_review_complete", "accepted final status mismatch")
    require(statuses.get("held_with_preserved_appeal") == "final_deferred_appeal", "appeal-backed status mismatch")
    require(statuses.get("held_without_appeal") == "final_deferred_review", "non-appeal held status mismatch")
    require(format_contract.get("held_chunk_required_field") == "candidate_hold_state", "held chunk field missing")
    receipts = format_contract.get("generated_receipts") or {}
    require(
        receipts.get("hash_closure_fields")
        == ["chunks", "review_packets", "decision_relations", "uncertainty_sidecars", "checker_verdict", "postcheck", "B10_precompletion_receipt"],
        "receipt hash closure fields mismatch",
    )
    extended = set(receipts.get("extended_hash_closure_fields") or [])
    require(
        {"premortem", "provisional_boss_ruling", "final_boss_ruling", "appeal_ledger", "precompletion_stage_receipts_B00_B09"}.issubset(extended),
        "extended receipt hash closure is incomplete",
    )
    relations_contract = format_contract.get("decision_relations") or {}
    require(relations_contract.get("empty_set_requires_explicit_reviewed_no_relation_receipt") is True, "no-relation receipt contract missing")
    require(relations_contract.get("never_invent_relation_to_satisfy_a_nonempty_gate") is True, "relation anti-invention rule missing")
    require(receipts.get("terminal_completion_receipt_is_acyclic_root") is True, "terminal receipt must be the acyclic root")
    require(receipts.get("completion_receipt_self_hash_forbidden") is True, "completion receipt self-hash must be forbidden")
    require(receipts.get("shell_free_fail_fast_completion_bundle_required") is True, "shell-free completion bundle must be required")
    bases = format_contract.get("held_chunk_required_basis") or {}
    require(bases.get("preserved_appeal") == "preserved_appeal", "appeal hold basis missing")
    require(bases.get("specialist_or_external_review") == "specialist_or_external_review", "review hold basis missing")

    implementation = data.get("replay_evidence_implementation") or {}
    expected_implementation = {
        "stage_schema": "config/agents/families/scripture-first-biblical-chunking/whole_bible_stage_receipt.schema.v1.json",
        "boss_phase_schema": "config/agents/families/scripture-first-biblical-chunking/whole_bible_boss_phase_receipt.schema.v1.json",
        "extended_manifest_schema": "config/agents/families/scripture-first-biblical-chunking/whole_bible_extended_evidence_manifest.schema.v1.json",
        "terminal_completion_schema": "config/agents/families/scripture-first-biblical-chunking/whole_bible_terminal_completion_receipt.schema.v1.json",
        "b00_preflight_builder": "scripts/build_whole_bible_b00_preflight.py",
        "stage_writer": "scripts/write_whole_bible_stage_receipt.py",
        "boss_phase_writer": "scripts/write_whole_bible_boss_phase_receipt.py",
        "extended_manifest_builder": "scripts/build_whole_bible_extended_evidence_manifest.py",
        "materialized_chain_validator": "scripts/validate_whole_bible_stage_receipts.py",
        "completion_gate_runner": "scripts/run_whole_bible_completion_gates.py",
        "terminal_completion_writer": "scripts/write_whole_bible_terminal_completion_receipt.py",
        "specification_validator": "scripts/validate_whole_bible_candidate_workflow.py",
    }
    require(implementation.get("spec_valid_is_not_replay_qualified") is True, "spec validation must not imply replay qualification")
    for key, relative in expected_implementation.items():
        require(implementation.get(key) == relative, f"replay implementation {key} mismatch")
        require((ROOT / relative).is_file(), f"replay implementation missing: {relative}")

    storage = data.get("stage_receipt_contract") or {}
    require(storage.get("attempts_are_immutable") is True, "stage attempts must be immutable")
    require(storage.get("selected_index_is_evidence") is False, "derived run index cannot be primary evidence")
    require(storage.get("replacement_attempt_truncates_downstream_selections_not_history") is True, "replacement attempts must preserve history")
    require(storage.get("same_state_failed_attempt_retry_forbidden") is True, "same-state failed retry must be forbidden")
    require(storage.get("acyclic_receipt_dag") == "B00_to_B09_then_precompletion_manifest_then_B10_then_terminal_completion_then_external_qualification", "receipt DAG mismatch")
    calibration = data.get("cross_form_calibration_lane")
    require(isinstance(calibration, dict) and calibration.get("runs_in_parallel_after_format_repair") is True, "cross-form calibration lane missing")
    capability_union = {
        capability
        for case in calibration.get("cases", [])
        if isinstance(case, dict)
        for capability in case.get("capabilities", [])
    }
    require({"poetry", "aramaic", "koine_greek", "synoptic_parallel", "argument"}.issubset(capability_union), "calibration lane lacks required form/language breadth")

    dad = data.get("dad_reporting")
    require(isinstance(dad, dict) and dad.get("candidate_metadata_only") is True, "DAD reporting must remain candidate metadata only")
    prohibited = set(dad.get("prohibited") or [])
    require({"scripture_text_or_source_rows", "raw_conversations_or_hidden_reasoning", "secrets_or_private_payloads"}.issubset(prohibited), "DAD privacy exclusions incomplete")


def validate_prompts() -> None:
    data = load_yaml(PROMPTS)
    require(data.get("artifact_class") == "portable_core", "prompt pack must be portable_core")
    require(data.get("lifecycle_status") == "candidate", "prompt pack must remain candidate")
    require(data.get("prompt_pack_version") == "1.2.0", "prompt pack version must be 1.2.0")
    require(str(data.get("workflow_ref")) == WORKFLOW.relative_to(ROOT).as_posix(), "prompt pack workflow_ref mismatch")
    preamble = str(data.get("shared_preamble", ""))
    require("share the same model substrate" in preamble, "prompt preamble must disclose shared substrate")
    require("not an independent model vote" in preamble, "prompt preamble must deny false independent votes")
    templates = data.get("templates")
    require(isinstance(templates, list), "prompt templates missing")
    by_id = {row.get("template_id"): row for row in templates if isinstance(row, dict)}
    required = {
        "root_author_candidate_map",
        "second_temple_rabbinic_context_scout",
        "original_language_translation_scout",
        "literary_form_scout",
        "canonical_relations_and_premortem_scout",
        "original_language_primary_review",
        "literary_primary_review",
        "peer_crosscheck",
        "premortem_review",
        "evidence_dispute_boss",
        "appeal_response",
        "final_post_resolution_check",
        "privacy_safe_dad_lesson_reporter",
    }
    require(required.issubset(by_id), f"missing prompt templates: {sorted(required - set(by_id))}")
    boss = str(by_id["evidence_dispute_boss"].get("instructions", ""))
    require("provisional" in boss and "Then read peer and premortem" in boss, "boss prompt must enforce provisional-first sequencing")
    for template_id in ("original_language_primary_review", "literary_primary_review"):
        primary_outputs = set(by_id[template_id].get("required_output") or [])
        require(
            {
                "reviewer_attempt_id", "frozen_chunks_sha256",
                "shared_model_substrate", "non_authorizing",
            }.issubset(primary_outputs),
            f"{template_id}: primary revision/freshness outputs incomplete",
        )
    literary_scout_outputs = set(by_id["literary_form_scout"].get("required_output") or [])
    require("form_inventory" in literary_scout_outputs, "literary scout must emit a form inventory")
    premortem = str(by_id["premortem_review"].get("instructions", ""))
    require("Do not prescribe exact boss rulings" in premortem, "premortem must not choreograph boss rulings")
    final_check = str(by_id["final_post_resolution_check"].get("instructions", ""))
    require("positive contiguous integer indices" in final_check, "postcheck prompt must check official index semantics")
    final_outputs = set(by_id["final_post_resolution_check"].get("required_output") or [])
    require(
        {
            "checked_chunks_sha256", "checked_review_packets_sha256",
            "checked_decision_relations_sha256", "checked_uncertainty_sidecar_sha256",
            "checked_decision_ids", "shared_model_substrate",
            "counts_as_cross_model_independent_vote", "independence_scope",
        }.issubset(final_outputs),
        "postcheck prompt lacks hash-closure or independence outputs",
    )
    workflow = load_yaml(WORKFLOW)
    bound_templates = {
        template_id
        for binding in (workflow.get("executable_stage_bindings") or {}).values()
        if isinstance(binding, dict)
        for template_id in binding.get("prompt_templates", [])
    }
    require(bound_templates.issubset(by_id), f"stage bindings reference missing templates: {sorted(bound_templates - set(by_id))}")


def validate_adapter_and_family() -> None:
    adapter = load_yaml(ADAPTER)
    require(adapter.get("artifact_class") == "runtime_adapter", "Codex adapter must be runtime_adapter")
    require(adapter.get("adapter_version") == "1.2.0", "Codex adapter version must be 1.2.0")
    require(str(adapter.get("portable_core_ref")) == WORKFLOW.relative_to(ROOT).as_posix(), "adapter core_ref mismatch")
    require(str(adapter.get("prompt_pack_ref")) == PROMPTS.relative_to(ROOT).as_posix(), "adapter prompt_ref mismatch")
    disclosure = adapter.get("identity_disclosure") or {}
    require(disclosure.get("shared_model_substrate_default") is True, "adapter must disclose shared substrate")
    require(disclosure.get("role_separation_is_not_model_independence") is True, "adapter must distinguish role and model independence")
    qualification = adapter.get("qualification") or {}
    require(qualification.get("status") == "unverified_without_replay_harness", "adapter must remain unverified before replay")
    require(qualification.get("replay_launch_blocked") is True, "adapter replay launch must remain blocked")
    required_qualification = set(qualification.get("required_before_reuse") or [])
    require(
        {
            "validate_form_inventory_artifact_and_B01_receipt",
            "validate_primary_role_identity_and_revision_freshness",
            "validate_provisional_boss_ordering_receipt",
            "validate_extended_evidence_manifest_and_hash_closure",
            "validate_B00_B10_receipt_schema_and_chain",
            "validate_run_attempt_immutability_and_selection_index",
            "validate_resolved_path_confinement",
            "validate_acyclic_terminal_completion_receipt_root",
            "validate_dimension_scoped_qualification_without_scope_inflation",
            "validate_authoritative_B00_campaign_source_and_dependency_projection",
            "validate_exact_completion_gate_runner_argv_and_stdout",
            "derive_terminal_holds_and_appeals_from_B07_B09",
            "reject_alternate_campaign_or_model_roots",
            "independent_launch_review_receipt",
        }.issubset(required_qualification),
        "adapter qualification requirements are incomplete",
    )
    require(qualification.get("unattended_execution_authorized") is False, "adapter must not authorize unattended execution")

    family = load_yaml(FAMILY_FILE)
    roles = load_yaml(ROLES)
    release = load_yaml(RELEASE)
    require(family.get("family_version") == "1.2.0", "family version must be 1.2.0")
    require(roles.get("family_version") == "1.2.0", "role profile version must match family")
    require(release.get("family_version") == "1.2.0", "release version must match family")
    constituents = family.get("constituents") or {}
    require(str(constituents.get("replay_workflow")) == WORKFLOW.relative_to(ROOT).as_posix(), "family replay_workflow ref missing")
    require(str(constituents.get("prompt_pack")) == PROMPTS.relative_to(ROOT).as_posix(), "family prompt_pack ref missing")
    require(ADAPTER.relative_to(ROOT).as_posix() in (constituents.get("runtime_adapters") or []), "family runtime adapter ref missing")
    schema_constituents = {
        "stage_receipt_schema": "whole_bible_stage_receipt.schema.v1.json",
        "boss_phase_receipt_schema": "whole_bible_boss_phase_receipt.schema.v1.json",
        "extended_evidence_manifest_schema": "whole_bible_extended_evidence_manifest.schema.v1.json",
        "terminal_completion_receipt_schema": "whole_bible_terminal_completion_receipt.schema.v1.json",
    }
    for key, name in schema_constituents.items():
        path = FAMILY / name
        require(constituents.get(key) == path.relative_to(ROOT).as_posix(), f"family {key} ref missing")
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    runtime_evidence = load_yaml(M7_RUNTIME_EVIDENCE)
    require(runtime_evidence.get("artifact_class") == "runtime_capability_evidence", "M7 local adapter must be subordinate capability evidence")
    require(runtime_evidence.get("authoritative_runtime_adapter") == ADAPTER.relative_to(ROOT).as_posix(), "M7 runtime evidence authoritative adapter mismatch")
    require(runtime_evidence.get("may_override_authoritative_adapter") is False, "M7 runtime evidence cannot override portable adapter")
    manifest = load_yaml(M7_MODEL_MANIFEST)
    require(manifest.get("authoritative_runtime_adapter") == ADAPTER.relative_to(ROOT).as_posix(), "M7 model manifest adapter authority mismatch")
    require(manifest.get("runtime_capability_evidence") == M7_RUNTIME_EVIDENCE.relative_to(ROOT).as_posix(), "M7 model manifest capability evidence mismatch")

    if M7_CONTRACT.is_file():
        contract = load_yaml(M7_CONTRACT)
        scope = contract.get("independence_scope") or {}
        require(scope.get("shared_model_substrate") is True, "M7 contract must disclose shared model substrate")
        require(scope.get("counts_as_cross_model_independent_votes") is False, "M7 contract must not claim cross-model votes")
        gates = contract.get("completion_gates") or {}
        require(gates.get("official_whole_bible_chunk_map_validator_required") is True, "M7 contract must require official map validator")
    if M7_PROMPT.is_file():
        text = M7_PROMPT.read_text(encoding="utf-8")
        require("two blind independent specialist reviews" not in text, "M7 prompt retains false independence wording")
        require("one correlated model voice" in text, "M7 prompt lacks correlated-voice disclosure")
        require("official whole-Bible chunk-map validator" in text, "M7 prompt lacks official map gate")



def validate_live_campaign() -> None:
    require(M7_CAMPAIGN.is_file(), "live M7 campaign is missing")
    require(Path(ROOT / BUNDLE_REF).is_file(), "completion bundle is missing")
    try:
        campaign = json.loads(M7_CAMPAIGN.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkflowValidationError(f"live M7 campaign is invalid JSON: {exc}") from exc
    require(isinstance(campaign, dict), "live M7 campaign must be an object")
    require(int(campaign.get("revision", 0)) >= 6, "live M7 campaign must use replay-contract revision 6+")
    execution = campaign.get("execution") or {}

    validate_qualification_boundary(execution)

    require((ROOT / execution.get("state_root", "")).is_dir(), "campaign state root must exist")
    replay = campaign.get("replay_contract") or {}
    for field, path in (("workflow", WORKFLOW), ("prompt_pack", PROMPTS), ("runtime_adapter", ADAPTER)):
        record = replay.get(field) or {}
        require(record.get("path") == path.relative_to(ROOT).as_posix(), f"replay contract {field} path mismatch")
        require(record.get("digest") == f"sha256:{digest(path)}", f"replay contract {field} digest stale")
    require(replay.get("unattended_launch_authorized") is False, "replay contract must not authorize unattended launch")

    canon = load_yaml(CANON).get("canonical_66_books")
    require(isinstance(canon, list) and len(canon) == 66, "canonical 66-book list malformed")
    try:
        jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    except (KeyError, IndexError, TypeError) as exc:
        raise WorkflowValidationError("live M7 campaign job topology is malformed") from exc
    require(isinstance(jobs, list) and len(jobs) == 67, "live campaign needs 66 book jobs plus merge")
    require(str(jobs[-1].get("id", "")).endswith("MERGE"), "final campaign job must be merge")

    observed_books: list[str] = []
    observed_idempotency: set[str] = set()
    unsafe_tokens = (";", "&&", "||", "|", ">", "<", chr(10), chr(13))
    workflow_data = load_yaml(WORKFLOW)
    expected_stage_bindings = workflow_data["executable_stage_bindings"]
    prompt_data = load_yaml(PROMPTS)
    valid_template_ids = {
        row.get("template_id")
        for row in prompt_data.get("templates", [])
        if isinstance(row, dict)
    }
    previous_job_id: str | None = None
    for job in jobs[:-1]:
        checkpoint = str(job.get("checkpoint", ""))
        match = re.fullmatch(r".*/books/([^/]+)[.]json", checkpoint)
        require(match is not None, f"{job.get('id')}: malformed book checkpoint")
        book = match.group(1)
        observed_books.append(book)
        expected_dependencies = [] if previous_job_id is None else [previous_job_id]
        require(job.get("depends_on") == expected_dependencies, f"{job.get('id')}: dependency chain mismatch")
        previous_job_id = job.get("id")
        idempotency = job.get("idempotency_key")
        require(
            isinstance(idempotency, str) and idempotency == f"T521-M7-sol:{book}:workflow-1.2.0:<run_id>",
            f"{job.get('id')}: idempotency key is not book-unique",
        )
        require(idempotency not in observed_idempotency, f"{job.get('id')}: duplicate idempotency key")
        observed_idempotency.add(idempotency)
        require(job.get("workflow_ref") == WORKFLOW.relative_to(ROOT).as_posix(), f"{job.get('id')}: workflow_ref mismatch")
        require(job.get("prompt_pack_ref") == PROMPTS.relative_to(ROOT).as_posix(), f"{job.get('id')}: prompt_pack_ref mismatch")
        require(job.get("runtime_adapter_ref") == ADAPTER.relative_to(ROOT).as_posix(), f"{job.get('id')}: runtime_adapter_ref mismatch")
        expected_command = f"python -m scripts.validate_whole_bible_stage_receipts --book {book} --run-id <run_id> --require-complete --require-terminal"
        require(job.get("durability_check") == expected_command, f"{job.get('id')}: durability command is not the terminal replay-chain gate")
        inputs = job.get("inputs") or []
        digests = job.get("input_digests") or {}
        require(BUNDLE_REF in inputs and BUNDLE_REF in digests, f"{job.get('id')}: bundle missing from pinned inputs")
        require(not any(str(value).endswith("/") for value in inputs), f"{job.get('id')}: directory input cannot be immutably pinned")
        require(set(inputs) == set(digests), f"{job.get('id')}: every input needs exactly one digest")
        campaign_ref = M7_CAMPAIGN.relative_to(ROOT).as_posix()
        for value in inputs:
            recorded = digests.get(value)
            if value == campaign_ref:
                require(
                    recorded == "stage_receipt:B00.input_artifact_sha256.campaign",
                    f"{job.get('id')}: campaign self-hash must be deferred to B00 receipt",
                )
            else:
                path = ROOT / value
                require(path.is_file(), f"{job.get('id')}: pinned input missing: {value}")
                require(recorded == f"sha256:{digest(path)}", f"{job.get('id')}: stale or placeholder input digest: {value}")
        stage_plan = job.get("stage_plan")
        require(isinstance(stage_plan, list) and [row.get("stage_id") for row in stage_plan] == list(expected_stage_bindings), f"{job.get('id')}: B00-B10 stage plan missing")
        receipts = job.get("stage_receipts")
        require(isinstance(receipts, list) and receipts == [row.get("receipt") for row in stage_plan], f"{job.get('id')}: stage receipt list mismatch")
        require(len(receipts) == 11 and len(set(receipts)) == 11, f"{job.get('id')}: stage receipts must be unique")
        require(all(f"/runs/<run_id>/stages/{stage_id}/<attempt_id>.json" in receipt for stage_id, receipt in zip(expected_stage_bindings, receipts)), f"{job.get('id')}: stage receipt paths must be immutable run/attempt templates")
        for row in stage_plan:
            expected_templates = expected_stage_bindings[row["stage_id"]].get("prompt_templates", [])
            require(row.get("prompt_template_ids") == expected_templates, f"{job.get('id')} {row['stage_id']}: prompt binding mismatch")
            require(set(expected_templates).issubset(valid_template_ids), f"{job.get('id')} {row['stage_id']}: missing prompt template")
        require(job.get("qualification_evidence_status") == "required_missing_blocks_launch", f"{job.get('id')}: missing qualification must block launch")
        require(job.get("auto_advance") is False, f"{job.get('id')}: unqualified campaign job must not auto-advance")
        dependency_digests = job.get("dependency_digests") or {}
        if book == "Num":
            lev_v2 = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/receipts/Lev_completion_v2.json"
            expected_waiver = f"precontract_snapshot_waiver:Lev_completion_v2:sha256:{digest(lev_v2)}"
            require(dependency_digests.get("J-003-LEV") == expected_waiver, f"{job.get('id')}: Leviticus precontract dependency waiver is not hash-bound")
        expected_testament = "old" if book in set(canon[:39]) else "new"
        expected_language = "hebrew_aramaic" if expected_testament == "old" else "koine_greek"
        source_route = job.get("source_route") or {}
        require(source_route.get("testament") == expected_testament, f"{job.get('id')}: testament source route mismatch")
        require(source_route.get("original_language") == expected_language, f"{job.get('id')}: original-language source route mismatch")
        expected_manifests = (
            workflow_data["source_routing_contract"]["old_testament_hebrew_and_aramaic"]
            if expected_testament == "old"
            else workflow_data["source_routing_contract"]["new_testament_koine_greek"]
        )
        require(source_route.get("manifest_paths") == expected_manifests, f"{job.get('id')}: original-language manifests mismatch")
        require(set(expected_manifests).issubset(inputs), f"{job.get('id')}: routed source manifests missing from inputs")
        outputs = set(job.get("outputs") or [])
        allowed = set(job.get("allowed_paths") or [])
        require(set(receipts).issubset(outputs), f"{job.get('id')}: stage receipts omitted from outputs")
        require(outputs.issubset(allowed), f"{job.get('id')}: outputs exceed allowed paths")
        for candidate_path in sorted(outputs | allowed):
            require_candidate_scoped_path(candidate_path, f"{job.get('id')} candidate path")
        for qualification_path in job.get("qualification_evidence") or []:
            require_candidate_scoped_path(qualification_path, f"{job.get('id')} qualification path")
        review_root = f".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/{book}"
        required_outputs = {
            f"{review_root}/premortem.json",
            f"{review_root}/boss_provisional.json",
            f"{review_root}/boss_rulings.json",
            f"{review_root}/appeals.jsonl",
            f"{review_root}/source_gap_register.json",
            f"{review_root}/role_separated_checker_verdict_v1.json",
            f"{review_root}/post_resolution_check_v2.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/receipts/{book}_completion_v3.<run_id>.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/extended_evidence_manifest.precompletion.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/completion_gate_bundles/<attempt_id>.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/run_index.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/receipts.jsonl",
        }
        required_outputs.update({
            f"{review_root}/appeal_disposition.json",
            f"{review_root}/hold_disposition.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/preflight/campaign_projection.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/preflight/preflight_report.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/preflight/dependency_evidence.json",
        })
        require(required_outputs.issubset(outputs), f"{job.get('id')}: review or closure outputs incomplete")
        form_inventory = f"{review_root}/form_inventory.json"
        require(job.get("form_inventory_artifact") == form_inventory, f"{job.get('id')}: form inventory artifact missing")
        require(form_inventory in outputs, f"{job.get('id')}: form inventory omitted from outputs")
        b01 = next(row for row in stage_plan if row["stage_id"] == "B01")
        require(form_inventory in (b01.get("required_artifacts") or []), f"{job.get('id')}: B01 does not require form inventory")
        for gate in job.get("acceptance", []):
            semantics = gate.get("result_semantics") or {}
            require("next book may proceed" in str(semantics.get("pass_with_holds", "")), f"{job.get('id')}: pass_with_holds progression missing")
            require("ordinary preserved boundary appeal" in str(semantics.get("blocked_human", "")), f"{job.get('id')}: blocked_human appeal distinction missing")
        escalation = job.get("escalation", {}).get("conditions", [])
        require(
            any("continue to the next book" in str(value) for value in escalation),
            f"{job.get('id')}: appeal escalation still stops canonical progress",
        )
        shared_write = job.get("shared_write_contract") or {}
        require_true(
            shared_write,
            {"exclusive_lock_required", "atomic_replace_required", "concurrent_book_writes_forbidden"},
            f"{job.get('id')} shared-write contract",
        )
        acceptance = job.get("acceptance") or []
        bundle_gates = [
            gate for gate in acceptance
            if isinstance(gate, dict) and gate.get("command") == expected_command
        ]
        require(len(bundle_gates) == 1, f"{job.get('id')}: expected one completion-bundle acceptance gate")
        for value in [job.get("durability_check", "")] + [
            gate.get("command", "") for gate in acceptance if isinstance(gate, dict)
        ]:
            if value == "not-applicable":
                continue
            command_without_templates = re.sub(r"<[A-Za-z_][A-Za-z0-9_]*>", "TOKEN", str(value))
            require(not any(token in command_without_templates for token in unsafe_tokens), f"{job.get('id')}: unsafe shell composition remains")
    require(observed_books == canon, "live campaign book jobs are not in exact canonical order")
    merge = jobs[-1]
    require(merge.get("auto_advance") is False, "unqualified merge job must not auto-advance")
    for candidate_path in merge.get("outputs") or []:
        require_candidate_scoped_path(candidate_path, "merge output")
    require(merge.get("depends_on") == [jobs[-2].get("id")], "merge job dependency mismatch")
    require(merge.get("idempotency_key") == "T521-M7-sol:merge:workflow-1.2.0:<campaign_run_id>", "merge idempotency mismatch")
    merge_inputs = merge.get("inputs") or []
    merge_digests = merge.get("input_digests") or {}
    require(set(merge_inputs) == set(merge_digests), "merge inputs and digests mismatch")
    require(not any(str(value).endswith("/") for value in merge_inputs), "merge cannot pin a directory input")
    require(
        not any("verified-at" in str(value) for value in merge_digests.values()),
        "merge retains placeholder digests",
    )
    require(merge.get("merge_input_resolution_required_at_dispatch") is True, "merge digest resolution contract missing")
    for book in canon:
        receipt = f".ai/scratch/multi_model_bible_chunking/M7_sol/receipts/{book}_completion_v3.<book_run_id>.json"
        require(receipt in merge_inputs, f"merge omits {book} completion receipt")
        require(
            merge_digests.get(receipt) == f"terminal_book_completion_receipt:{book}.sha256",
            f"merge receipt digest contract mismatch for {book}",
        )
    for gate in merge.get("acceptance", []):
        semantics = gate.get("result_semantics") or {}
        require("next book may proceed" in str(semantics.get("pass_with_holds", "")), "merge hold semantics missing")
        require("ordinary preserved boundary appeal" in str(semantics.get("blocked_human", "")), "merge blocked_human appeal distinction missing")
    human_stop = next(
        (row for row in campaign.get("stop_conditions", []) if row.get("code") == "human_gate_required"),
        {},
    )
    require("ordinary preserved boundary appeals enter" in str(human_stop.get("detection", "")), "campaign stop semantics still halt ordinary appeals")
    require(
        campaign.get("execution", {}).get("durability_command") == "python -m scripts.validate_whole_bible_stage_receipts --book <Book> --run-id <run_id> --require-complete --require-terminal",
        "generic campaign durability command is not the terminal replay-chain gate",
    )
def main() -> int:
    try:
        validate_workflow()
        validate_prompts()
        validate_adapter_and_family()
        validate_live_campaign()
    except WorkflowValidationError as exc:
        print(f"Whole-Bible candidate workflow validation failed: {exc}", file=sys.stderr)
        return 1
    print("Whole-Bible candidate workflow validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
