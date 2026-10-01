#!/usr/bin/env python3
"""Run all repository validation gates (green/red for CI and agents).

Always-run gates: repo, control plane, handoffs, source manifest.
Conditional gates: JSONL referential integrity + canon presence run only when
the generated canonical data is present (so clean checkouts stay green; CI
regenerates the data first, then this gate is real). The large word_tokens file
is checked through focused Rust fast-path wrappers when present; Python remains
the orchestration and fallback surface.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import os
from pathlib import Path

import yaml

try:
    from scripts.generated_data_lifecycle import (
        missing_declared_inputs,
        runnable_generated_data_gates,
        skipped_generated_data_gates,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from generated_data_lifecycle import (
        missing_declared_inputs,
        runnable_generated_data_gates,
        skipped_generated_data_gates,
    )

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

MANIFEST = ROOT / "data" / "raw" / "bible" / "eng-web" / "source_manifest.yaml"
CANON_DIR = ROOT / "data" / "canonical"
T475_TRANSITION_WORD_TOKENS = CANON_DIR / "translations" / "eng-web" / "word_tokens.jsonl"
T475_TRANSITION_FOOTNOTES = CANON_DIR / "translations" / "eng-web" / "footnotes.jsonl"
T475_DEFERRED_GENERATED_GATES = {
    "validate_t374_additive_parent_overlay.py",
    "validate_t401_eph1_output_pilot.py",
    "validate_t415_batch1_output_pilot.py",
    "validate_source_metadata_research_atlas.py",
    "validate_1cor8_10_parent_evidence_packet.py",
    "validate_divine_capitalization_inventory.py",
    "validate_wj_marker_inventory.py",
}
def _count_nonempty_lines(path: Path) -> int:
    if not path.is_file():
        return -1
    with path.open("rb") as handle:
        return sum(1 for line in handle if line.strip())


def t475_candidate_transition_active() -> bool:
    focus = ROOT / ".ai" / "control" / "current_focus.yaml"
    try:
        current = yaml.safe_load(focus.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return False
    if not isinstance(current, dict) or current.get("current_task") != "T475":
        return False
    counts = (
        _count_nonempty_lines(T475_TRANSITION_WORD_TOKENS),
        _count_nonempty_lines(T475_TRANSITION_FOOTNOTES),
    )
    return counts == (677686, 1130)


def t477_baseline_reset_active() -> bool:
    focus = ROOT / ".ai" / "control" / "current_focus.yaml"
    try:
        current = yaml.safe_load(focus.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return False
    if not isinstance(current, dict) or current.get("current_task") not in {"T477", "T478"}:
        return False
    counts = (
        _count_nonempty_lines(T475_TRANSITION_WORD_TOKENS),
        _count_nonempty_lines(T475_TRANSITION_FOOTNOTES),
    )
    return counts == (677686, 1130)


def changed_paths() -> list[str]:
    paths: list[str] = []
    base_ref = "origin/main"
    github_base = os.environ.get("GITHUB_BASE_REF")
    if github_base:
        base_ref = f"origin/{github_base}"
    for args in (
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "diff", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ):
        try:
            result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        paths.extend(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())
    return paths


def changed_task_ids(paths: list[str]) -> list[str]:
    return sorted(
        {
            Path(path).name.removesuffix(".task.yaml")
            for path in paths
            if path.startswith(".ai/tasks/") and path.endswith(".task.yaml")
        }
    )


def task_base_ref(task_id: str) -> str:
    task_file = ROOT / ".ai" / "tasks" / f"{task_id}.task.yaml"
    try:
        data = yaml.safe_load(task_file.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return ""
    if not isinstance(data, dict):
        return ""
    base_ref = data.get("base_ref")
    return base_ref.strip() if isinstance(base_ref, str) else ""


def task_integrates_task_ids(task_id: str) -> list[str]:
    task_file = ROOT / ".ai" / "tasks" / f"{task_id}.task.yaml"
    try:
        data = yaml.safe_load(task_file.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return []
    if not isinstance(data, dict):
        return []
    integrated = data.get("integrates_task_ids")
    if not isinstance(integrated, list):
        return []
    return sorted(item.strip() for item in integrated if isinstance(item, str) and item.strip())


def integration_task_scope_ids(task_ids: list[str]) -> list[str]:
    """Use an explicit integration task when it covers every changed task."""

    if len(task_ids) <= 1:
        return task_ids
    task_id_set = set(task_ids)
    for task_id in task_ids:
        integrated = set(task_integrates_task_ids(task_id))
        if integrated and task_id_set <= integrated | {task_id}:
            return [task_id]
    return task_ids


def stack_tip_task_ids(task_ids: list[str]) -> list[str]:
    """For stacked PRs, validate only task tips that explicitly base on earlier task branches."""

    if len(task_ids) <= 1:
        return task_ids
    normalized = {task_id: task_id.lower().replace("_", "-") for task_id in task_ids}
    inherited: set[str] = set()
    for task_id in task_ids:
        base_ref = task_base_ref(task_id).lower().replace("_", "-")
        if not base_ref:
            continue
        for other_task_id, other_needle in normalized.items():
            if other_task_id != task_id and other_needle in base_ref:
                inherited.add(other_task_id)
    tips = [task_id for task_id in task_ids if task_id not in inherited]
    return tips or task_ids


def task_scope_gates() -> list[tuple[str, list[str]]]:
    """Use the changed task file when a PR clearly scopes to one task."""

    paths = changed_paths()
    task_ids = changed_task_ids(paths)
    if len(task_ids) == 1:
        task_id = task_ids[0]
        return [
            (
                f"validate_task_scope.py --task-id {task_id}",
                [PY, str(ROOT / "scripts" / "validate_task_scope.py"), "--task-id", task_id],
            )
        ]
    if "T464" in task_ids and set(task_ids) <= {"T423", "T424", "T464"}:
        return [
            (
                "validate_task_scope.py --task-id T464",
                [PY, str(ROOT / "scripts" / "validate_task_scope.py"), "--task-id", "T464"],
            )
        ]
    if set(task_ids) <= {"T417", "T420"}:
        return [
            (
                "validate_task_scope.py --task-id T417",
                [PY, str(ROOT / "scripts" / "validate_task_scope.py"), "--task-id", "T417"],
            )
        ]
    task_ids = integration_task_scope_ids(task_ids)
    if len(task_ids) == 1:
        task_id = task_ids[0]
        return [
            (
                f"validate_task_scope.py --task-id {task_id}",
                [PY, str(ROOT / "scripts" / "validate_task_scope.py"), "--task-id", task_id],
            )
        ]
    task_ids = stack_tip_task_ids(task_ids)
    if len(task_ids) == 1:
        task_id = task_ids[0]
        return [
            (
                f"validate_task_scope.py --task-id {task_id}",
                [PY, str(ROOT / "scripts" / "validate_task_scope.py"), "--task-id", task_id],
            )
        ]
    if task_ids:
        return [
            (
                f"validate_task_scope.py --task-id {task_id}",
                [PY, str(ROOT / "scripts" / "validate_task_scope.py"), "--task-id", task_id],
            )
            for task_id in task_ids
        ]
    return [("validate_task_scope.py", [PY, str(ROOT / "scripts" / "validate_task_scope.py")])]


def parallel_execution_safety_gates() -> list[tuple[str, list[str]]]:
    """Validate live git/worktree state without requiring a clean pre-commit tree."""

    paths = changed_paths()
    task_ids = changed_task_ids(paths)
    if len(task_ids) == 1:
        task_id = task_ids[0]
        return [
            (
                f"validate_parallel_execution_safety.py --task-id {task_id}",
                [
                    PY,
                    str(ROOT / "scripts" / "validate_parallel_execution_safety.py"),
                    "--task-id",
                    task_id,
                    "--allow-current-task-dirty",
                ],
            )
        ]
    if "T464" in task_ids and set(task_ids) <= {"T423", "T424", "T464"}:
        return [
            (
                "validate_parallel_execution_safety.py --task-id T464",
                [
                    PY,
                    str(ROOT / "scripts" / "validate_parallel_execution_safety.py"),
                    "--task-id",
                    "T464",
                    "--allow-current-task-dirty",
                ],
            )
        ]
    if set(task_ids) <= {"T417", "T420"}:
        return [
            (
                "validate_parallel_execution_safety.py --task-id T420",
                [
                    PY,
                    str(ROOT / "scripts" / "validate_parallel_execution_safety.py"),
                    "--task-id",
                    "T420",
                    "--allow-current-task-dirty",
                ],
            )
        ]
    task_ids = integration_task_scope_ids(task_ids)
    if len(task_ids) == 1:
        task_id = task_ids[0]
        return [
            (
                f"validate_parallel_execution_safety.py --task-id {task_id}",
                [
                    PY,
                    str(ROOT / "scripts" / "validate_parallel_execution_safety.py"),
                    "--task-id",
                    task_id,
                    "--allow-current-task-dirty",
                ],
            )
        ]
    task_ids = stack_tip_task_ids(task_ids)
    if len(task_ids) == 1:
        task_id = task_ids[0]
        return [
            (
                f"validate_parallel_execution_safety.py --task-id {task_id}",
                [
                    PY,
                    str(ROOT / "scripts" / "validate_parallel_execution_safety.py"),
                    "--task-id",
                    task_id,
                    "--allow-current-task-dirty",
                ],
            )
        ]
    return [
        (
            "validate_parallel_execution_safety.py",
            [
                PY,
                str(ROOT / "scripts" / "validate_parallel_execution_safety.py"),
                "--allow-current-task-dirty",
            ],
        )
    ]


def generated_canonical_missing() -> list[Path]:
    return list(missing_declared_inputs(ROOT))


def generated_data_gates() -> list[tuple[str, list[str]]]:
    return runnable_generated_data_gates(PY, ROOT)


def build_gates() -> list[tuple[str, list[str]]]:
    gates: list[tuple[str, list[str]]] = [
        ("validate_repo.py", [PY, str(ROOT / "scripts" / "validate_repo.py")]),
        ("validate_control_plane.py", [PY, str(ROOT / "scripts" / "validate_control_plane.py")]),
        ("validate_task_ledger.py", [PY, str(ROOT / "scripts" / "validate_task_ledger.py")]),
        ("validate_repository_link_contract.py", [PY, str(ROOT / "scripts" / "validate_repository_link_contract.py")]),
        (
            "validate_governance_dependency_map_mirror.py",
            [PY, str(ROOT / "scripts" / "validate_governance_dependency_map_mirror.py")],
        ),
        (
            "validate_llos_v1_adapter.py",
            [PY, str(ROOT / "scripts" / "validate_llos_v1_adapter.py")],
        ),
        (
            "validate_dad_transport_contract.py",
            [PY, str(ROOT / "scripts" / "validate_dad_transport_contract.py")],
        ),
        ("validate_dad_outbox.py", [PY, str(ROOT / "scripts" / "validate_dad_outbox.py")]),
        (
            "validate_validation_gate_lifecycle.py",
            [PY, str(ROOT / "scripts" / "validate_validation_gate_lifecycle.py")],
        ),
        (
            "validate_ai_pr_lifecycle_policy.py",
            [PY, str(ROOT / "scripts" / "validate_ai_pr_lifecycle_policy.py")],
        ),
        ("validate_handoffs.py", [PY, str(ROOT / "scripts" / "agent" / "validate_handoffs.py")]),
        *task_scope_gates(),
        *parallel_execution_safety_gates(),
        ("validate_canonical_66_scope.py", [PY, str(ROOT / "scripts" / "validate_canonical_66_scope.py")]),
        ("validate_vectorization_plan.py", [PY, str(ROOT / "scripts" / "validate_vectorization_plan.py")]),
        (
            "validate_t492_theological_research_foundation.py",
            [PY, str(ROOT / "scripts" / "validate_t492_theological_research_foundation.py")],
        ),
        (
            "validate_t493_patristics_boundary_intake_plan.py",
            [PY, str(ROOT / "scripts" / "validate_t493_patristics_boundary_intake_plan.py")],
        ),
        ("validate_t494_theological_edge_taxonomy_research.py", [PY, str(ROOT / "scripts" / "validate_t494_theological_edge_taxonomy_research.py")]),
        ("validate_t495_doctrine_genealogy_governance_handoff.py", [PY, str(ROOT / "scripts" / "validate_t495_doctrine_genealogy_governance_handoff.py")]),
        ("validate_t497_fable_architecture_owner_decisions.py", [PY, str(ROOT / "scripts" / "validate_t497_fable_architecture_owner_decisions.py")]),
        (
            "validate_chunking_theological_decision_register.py",
            [PY, str(ROOT / "scripts" / "validate_chunking_theological_decision_register.py")],
        ),
        (
            "validate_chunking_lesson_index.py",
            [PY, str(ROOT / "scripts" / "validate_chunking_lesson_index.py")],
        ),
        (
            "validate_t450_bible_edge_taxonomy.py",
            [PY, str(ROOT / "scripts" / "validate_t450_bible_edge_taxonomy.py")],
        ),
        (
            "validate_test_runtime_preflight.py",
            [PY, str(ROOT / "scripts" / "validate_test_runtime_preflight.py")],
        ),
        (
            "validate_coding_runtime_language_preflight.py",
            [PY, str(ROOT / "scripts" / "validate_coding_runtime_language_preflight.py")],
        ),
        (
            "validate_governance_memory_durability.py",
            [PY, str(ROOT / "scripts" / "validate_governance_memory_durability.py")],
        ),
        (
            "validate_owner_decision_projection_policy.py",
            [PY, str(ROOT / "scripts" / "validate_owner_decision_projection_policy.py")],
        ),
        (
            "validate_bible_chunking_readiness_map.py",
            [PY, str(ROOT / "scripts" / "validate_bible_chunking_readiness_map.py")],
        ),
        (
            "validate_chunking_agent_preflight.py",
            [PY, str(ROOT / "scripts" / "validate_chunking_agent_preflight.py")],
        ),
        (
            "validate_bible_chunking_research_triage.py",
            [PY, str(ROOT / "scripts" / "validate_bible_chunking_research_triage.py")],
        ),
        (
            "validate_bible_wide_chunking_research_registry.py",
            [PY, str(ROOT / "scripts" / "validate_bible_wide_chunking_research_registry.py")],
        ),
        (
            "validate_epistle_argument_theological_issue_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_epistle_argument_theological_issue_dossier_queue.py")],
        ),
        (
            "validate_gospel_wj_discourse_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_gospel_wj_discourse_dossier_queue.py")],
        ),
        (
            "validate_narrative_legal_covenant_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_narrative_legal_covenant_dossier_queue.py")],
        ),
        (
            "validate_wisdom_dialogue_poetry_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_wisdom_dialogue_poetry_dossier_queue.py")],
        ),
        (
            "validate_prophetic_oracle_vision_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_prophetic_oracle_vision_dossier_queue.py")],
        ),
        (
            "validate_textual_variant_source_tradition_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_textual_variant_source_tradition_dossier_queue.py")],
        ),
        (
            "validate_orthodox_original_language_pressure_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_orthodox_original_language_pressure_dossier_queue.py")],
        ),
        (
            "validate_original_language_phrase_context_policy.py",
            [PY, str(ROOT / "scripts" / "validate_original_language_phrase_context_policy.py")],
        ),
        (
            "validate_t430_original_language_evidence_substrate.py",
            [PY, str(ROOT / "scripts" / "validate_t430_original_language_evidence_substrate.py")],
        ),
        (
            "validate_t432_original_language_schema_contracts.py",
            [PY, str(ROOT / "scripts" / "validate_t432_original_language_schema_contracts.py")],
        ),
        (
            "validate_t433_phlm_alignment_pilot.py",
            [PY, str(ROOT / "scripts" / "validate_t433_phlm_alignment_pilot.py")],
        ),
        (
            "validate_t435_original_language_observation_scanner.py",
            [PY, str(ROOT / "scripts" / "validate_t435_original_language_observation_scanner.py")],
        ),
        (
            "validate_t436_jonah_hebrew_metadata_pilot.py",
            [PY, str(ROOT / "scripts" / "validate_t436_jonah_hebrew_metadata_pilot.py")],
        ),
        (
            "validate_t437_oshb_lemma_attribute_policy.py",
            [PY, str(ROOT / "scripts" / "validate_t437_oshb_lemma_attribute_policy.py")],
        ),
        (
            "validate_t438_alignment_bridge_goal.py",
            [PY, str(ROOT / "scripts" / "validate_t438_alignment_bridge_goal.py")],
        ),
        (
            "validate_t439_phlm_alignment_bridge_expansion.py",
            [PY, str(ROOT / "scripts" / "validate_t439_phlm_alignment_bridge_expansion.py")],
        ),
        (
            "validate_t440_jonah_hebrew_parser_contract.py",
            [PY, str(ROOT / "scripts" / "validate_t440_jonah_hebrew_parser_contract.py")],
        ),
        (
            "validate_t441_rust_alignment_coverage_index.py",
            [PY, str(ROOT / "scripts" / "validate_t441_rust_alignment_coverage_index.py")],
        ),
        (
            "validate_t442_production_candidate_root_decision_packet.py",
            [PY, str(ROOT / "scripts" / "validate_t442_production_candidate_root_decision_packet.py")],
        ),
        (
            "validate_original_language_raw_sources.py",
            [PY, str(ROOT / "scripts" / "validate_original_language_raw_sources.py")],
        ),
        (
            "validate_contextual_reading_policy.py",
            [PY, str(ROOT / "scripts" / "validate_contextual_reading_policy.py")],
        ),
        (
            "validate_orthodox_hermeneutic_firewall_docket.py",
            [PY, str(ROOT / "scripts" / "validate_orthodox_hermeneutic_firewall_docket.py")],
        ),
        (
            "validate_textual_critical_policy_docket.py",
            [PY, str(ROOT / "scripts" / "validate_textual_critical_policy_docket.py")],
        ),
        (
            "validate_textual_critical_policy_owner_options.py",
            [PY, str(ROOT / "scripts" / "validate_textual_critical_policy_owner_options.py")],
        ),
        (
            "validate_textual_critical_case_policy.py",
            [PY, str(ROOT / "scripts" / "validate_textual_critical_case_policy.py")],
        ),
        (
            "validate_t371_variant_dependency_owner_decision_packet.py",
            [PY, str(ROOT / "scripts" / "validate_t371_variant_dependency_owner_decision_packet.py")],
        ),
        (
            "validate_t371_parent_only_reviewed_gold_promotion.py",
            [PY, str(ROOT / "scripts" / "validate_t371_parent_only_reviewed_gold_promotion.py")],
        ),
        (
            "validate_t372_route_isolation_harness_plan.py",
            [PY, str(ROOT / "scripts" / "validate_t372_route_isolation_harness_plan.py")],
        ),
        (
            "validate_owner_decision_option_presentation_policy.py",
            [PY, str(ROOT / "scripts" / "validate_owner_decision_option_presentation_policy.py")],
        ),
        (
            "validate_t373_owner_implementation_authorization.py",
            [PY, str(ROOT / "scripts" / "validate_t373_owner_implementation_authorization.py")],
        ),
        (
            "validate_t374_baseline_overlap_owner_decision_packet.py",
            [PY, str(ROOT / "scripts" / "validate_t374_baseline_overlap_owner_decision_packet.py")],
        ),
        (
            "validate_t374_additive_parent_overlay.py",
            [PY, str(ROOT / "scripts" / "validate_t374_additive_parent_overlay.py")],
        ),
        (
            "validate_t375_post_pilot_review.py",
            [PY, str(ROOT / "scripts" / "validate_t375_post_pilot_review.py")],
        ),
        (
            "validate_t376_epistle_research_runway.py",
            [PY, str(ROOT / "scripts" / "validate_t376_epistle_research_runway.py")],
        ),
        (
            "validate_t384_bible_wide_research_readiness.py",
            [PY, str(ROOT / "scripts" / "validate_t384_bible_wide_research_readiness.py")],
        ),
        (
            "validate_manuscript_witness_reliability_scaffold.py",
            [PY, str(ROOT / "scripts" / "validate_manuscript_witness_reliability_scaffold.py")],
        ),
        (
            "validate_manuscript_source_catalog_metadata_plan.py",
            [PY, str(ROOT / "scripts" / "validate_manuscript_source_catalog_metadata_plan.py")],
        ),
        (
            "validate_manuscript_source_catalog_research_packet.py",
            [PY, str(ROOT / "scripts" / "validate_manuscript_source_catalog_research_packet.py")],
        ),
        (
            "validate_manuscript_source_catalog_sqlite_shell.py",
            [PY, str(ROOT / "scripts" / "validate_manuscript_source_catalog_sqlite_shell.py")],
        ),
        (
            "validate_primary_bible_witness_catalog.py",
            [PY, str(ROOT / "scripts" / "validate_primary_bible_witness_catalog.py")],
        ),
        (
            "validate_external_asset_root.py",
            [PY, str(ROOT / "scripts" / "validate_external_asset_root.py"), "--allow-missing-env"],
        ),
        (
            "validate_dss_biblical_witness_source_rows.py",
            [PY, str(ROOT / "scripts" / "validate_dss_biblical_witness_source_rows.py")],
        ),
        (
            "validate_t385_owner_decision_packet.py",
            [PY, str(ROOT / "scripts" / "validate_t385_owner_decision_packet.py")],
        ),
        (
            "validate_t392_eph1_review_packet_strengthening.py",
            [PY, str(ROOT / "scripts" / "validate_t392_eph1_review_packet_strengthening.py")],
        ),
        (
            "validate_t393_eph1_reviewed_gold_promotion_decision_packet.py",
            [PY, str(ROOT / "scripts" / "validate_t393_eph1_reviewed_gold_promotion_decision_packet.py")],
        ),
        (
            "validate_t394_eph1_parent_only_reviewed_gold_promotion.py",
            [PY, str(ROOT / "scripts" / "validate_t394_eph1_parent_only_reviewed_gold_promotion.py")],
        ),
        (
            "validate_t397_eph1_route_isolation_harness.py",
            [PY, str(ROOT / "scripts" / "validate_t397_eph1_route_isolation_harness.py")],
        ),
        (
            "validate_t401_eph1_output_pilot.py",
            [PY, str(ROOT / "scripts" / "validate_t401_eph1_output_pilot.py")],
        ),
        (
            "validate_t411_cursor_batch_artifacts.py",
            [PY, str(ROOT / "scripts" / "validate_t411_cursor_batch_artifacts.py")],
        ),
        (
            "validate_t413_batch1_review_packet_strengthening.py",
            [PY, str(ROOT / "scripts" / "validate_t413_batch1_review_packet_strengthening.py")],
        ),
        (
            "validate_t414_batch1_parent_only_reviewed_gold_promotion.py",
            [PY, str(ROOT / "scripts" / "validate_t414_batch1_parent_only_reviewed_gold_promotion.py")],
        ),
        (
            "validate_t415_batch1_output_pilot.py",
            [PY, str(ROOT / "scripts" / "validate_t415_batch1_output_pilot.py")],
        ),
        (
            "validate_t416_batch1_post_pilot_review.py",
            [PY, str(ROOT / "scripts" / "validate_t416_batch1_post_pilot_review.py")],
        ),
        (
            "validate_autonomous_run_queue.py",
            [PY, str(ROOT / "scripts" / "validate_autonomous_run_queue.py")],
        ),
        (
            "validate_multi_agent_review_cadence.py",
            [PY, str(ROOT / "scripts" / "validate_multi_agent_review_cadence.py")],
        ),
        (
            "validate_ai_agnostic_rust_subagents.py",
            [PY, str(ROOT / "scripts" / "validate_ai_agnostic_rust_subagents.py")],
        ),
        (
            "validate_standing_owner_escalation_policy.py",
            [PY, str(ROOT / "scripts" / "validate_standing_owner_escalation_policy.py")],
        ),
        (
            "validate_t417_batch2_review_packet_drafts.py",
            [PY, str(ROOT / "scripts" / "validate_t417_batch2_review_packet_drafts.py")],
        ),
        (
            "validate_scratch_lane_policy.py",
            [PY, str(ROOT / "scripts" / "validate_scratch_lane_policy.py")],
        ),
        (
            "validate_scratch_multi_model_ladder.py",
            [PY, str(ROOT / "scripts" / "validate_scratch_multi_model_ladder.py")],
        ),
        (
            "validate_multi_model_whole_bible_chunking_fork.py",
            [PY, str(ROOT / "scripts" / "validate_multi_model_whole_bible_chunking_fork.py")],
        ),
        (
            "validate_t423_pilot_gate.py",
            [PY, str(ROOT / "scripts" / "validate_t423_pilot_gate.py")],
        ),
        (
            "validate_t423_parallel_isolation.py",
            [PY, str(ROOT / "scripts" / "validate_t423_parallel_isolation.py"), "--policy-only"],
        ),
        (
            "validate_t423_literary_quality_protocol.py",
            [PY, str(ROOT / "scripts" / "validate_t423_literary_quality_protocol.py"), "--policy-only"],
        ),
        (
            "validate_t464_multi_model_decision_docket.py",
            [PY, str(ROOT / "scripts" / "validate_t464_multi_model_decision_docket.py")],
        ),
        (
            "validate_t465_multi_model_reconciliation_gate.py",
            [PY, str(ROOT / "scripts" / "validate_t465_multi_model_reconciliation_gate.py")],
        ),
        (
            "validate_t467_chunking_harness_hardening.py",
            [PY, str(ROOT / "scripts" / "validate_t467_chunking_harness_hardening.py")],
        ),
        (
            "validate_t468_owner_faithful_chunking_policy.py",
            [PY, str(ROOT / "scripts" / "validate_t468_owner_faithful_chunking_policy.py")],
        ),
        (
            "validate_t470_transparent_chunking_research_evidence_rubric.py",
            [PY, str(ROOT / "scripts" / "validate_t470_transparent_chunking_research_evidence_rubric.py")],
        ),
        (
            "validate_t471_near_boundary_docket_refinement.py",
            [PY, str(ROOT / "scripts" / "validate_t471_near_boundary_docket_refinement.py")],
        ),
        (
            "validate_t472_model_panel_calibration_gate.py",
            [PY, str(ROOT / "scripts" / "validate_t472_model_panel_calibration_gate.py")],
        ),
        (
            "validate_t473_semantic_harness_pilot.py",
            [PY, str(ROOT / "scripts" / "validate_t473_semantic_harness_pilot.py")],
        ),
        (
            "validate_t474_usfm_marker_anchor_contract.py",
            [PY, str(ROOT / "scripts" / "validate_t474_usfm_marker_anchor_contract.py")],
        ),
        (
            "validate_scripture_first_biblical_chunking_family.py",
            [PY, str(ROOT / "scripts" / "validate_scripture_first_biblical_chunking_family.py")],
        ),
        (
            "validate_whole_bible_candidate_workflow.py",
            [PY, str(ROOT / "scripts" / "validate_whole_bible_candidate_workflow.py")],
        ),
        (
            "validate_t513_portable_ocr_adoption.py",
            [PY, str(ROOT / "scripts" / "validate_t513_portable_ocr_adoption.py")],
        ),
        (
            "validate_task_execution_overlay.py --task-id T475",
            [PY, str(ROOT / "scripts" / "validate_task_execution_overlay.py"), "--task-id", "T475"],
        ),
        (
            "validate_t475_usfm_shadow_delta_gate.py --require-artifacts",
            [PY, str(ROOT / "scripts" / "validate_t475_usfm_shadow_delta_gate.py"), "--require-artifacts"],
        ),
        (
            "validate_scratch_scope.py",
            [PY, str(ROOT / "scripts" / "validate_scratch_scope.py"), "--branch", "scratch/ci-smoke", "--file", ".ai/scratch/vendor/.gitkeep"],
        ),
        (
            "validate_t402_low_complexity_chunking_runway.py",
            [PY, str(ROOT / "scripts" / "validate_t402_low_complexity_chunking_runway.py")],
        ),
        (
            "validate_cursor_low_risk_chunking_handoff.py",
            [PY, str(ROOT / "scripts" / "validate_cursor_low_risk_chunking_handoff.py")],
        ),
        (
            "validate_parallel_chunking_prompt_pack.py",
            [PY, str(ROOT / "scripts" / "validate_parallel_chunking_prompt_pack.py")],
        ),
        (
            "validate_t411_cursor_batch_artifacts.py",
            [PY, str(ROOT / "scripts" / "validate_t411_cursor_batch_artifacts.py")],
        ),
        (
            "validate_rust_observation_substrate.py",
            [PY, str(ROOT / "scripts" / "validate_rust_observation_substrate.py")],
        ),
        (
            "validate_t398_bible_wide_phase_one_research_synthesis.py",
            [PY, str(ROOT / "scripts" / "validate_t398_bible_wide_phase_one_research_synthesis.py")],
        ),
        (
            "validate_t399_focused_bible_wide_research_queue.py",
            [PY, str(ROOT / "scripts" / "validate_t399_focused_bible_wide_research_queue.py")],
        ),
        (
            "validate_epistle_argument_review_packets.py",
            [PY, str(ROOT / "scripts" / "validate_epistle_argument_review_packets.py")],
        ),
        (
            "validate_1cor8_10_owner_review_docket.py",
            [PY, str(ROOT / "scripts" / "validate_1cor8_10_owner_review_docket.py")],
        ),
        (
            "validate_chunking_human_decision_forecast.py",
            [PY, str(ROOT / "scripts" / "validate_chunking_human_decision_forecast.py")],
        ),
        ("validate_audit_surface_map.py", [PY, str(ROOT / "scripts" / "validate_audit_surface_map.py")]),
        (
            "validate_owner_selection_implementation_gate.py",
            [PY, str(ROOT / "scripts" / "validate_owner_selection_implementation_gate.py")],
        ),
        (
            "validate_source_metadata_authority.py",
            [PY, str(ROOT / "scripts" / "validate_source_metadata_authority.py")],
        ),
        (
            "validate_wj_speaker_discourse_policy.py",
            [PY, str(ROOT / "scripts" / "validate_wj_speaker_discourse_policy.py")],
        ),
        (
            "validate_john3_owner_review_docket.py",
            [PY, str(ROOT / "scripts" / "validate_john3_owner_review_docket.py")],
        ),
    ]
    gates.extend(generated_data_gates())
    if t475_candidate_transition_active():
        gates = [
            (name, cmd)
            for name, cmd in gates
            if name not in T475_DEFERRED_GENERATED_GATES
        ]
        gates.append(
            (
                "validate_t475_generated_transition_state.py",
                [PY, str(ROOT / "scripts" / "validate_t475_generated_transition_state.py")],
            )
        )
    elif t477_baseline_reset_active():
        gates = [
            (name, cmd)
            for name, cmd in gates
            if name not in T475_DEFERRED_GENERATED_GATES
        ]
        gates.append(
            (
                "validate_t477_baseline_reset.py",
                [PY, str(ROOT / "scripts" / "validate_t477_baseline_reset.py")],
            )
        )
    # Raw-source gates (the committed raw archives are the real pipeline input).
    if (ROOT / "data" / "raw").exists():
        gates.append(("validate_raw_coverage.py", [PY, str(ROOT / "scripts" / "validate_raw_coverage.py")]))
        gates.append(("scan_raw_sources.py --check", [PY, str(ROOT / "scripts" / "scan_raw_sources.py"), "--check"]))
    if MANIFEST.exists():
        gates.append(
            ("validate_manifest.py", [PY, str(ROOT / "pipelines" / "validate" / "validate_manifest.py"), str(MANIFEST)])
        )
    gold_dir = ROOT / "eval" / "chunking_gold" / "per_form"
    if gold_dir.exists():
        gates.append(("validate_chunking_gold.py", [PY, str(ROOT / "scripts" / "validate_chunking_gold.py")]))
    return gates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-generated-data",
        action="store_true",
        help="Fail before validation when any lifecycle-declared generated canonical input is absent.",
    )
    args = parser.parse_args(argv)
    failures = []
    missing_generated = generated_canonical_missing()
    if missing_generated:
        missing = ", ".join(path.relative_to(ROOT).as_posix() for path in missing_generated)
        if args.require_generated_data:
            print(
                "Release/full-data validation requires every lifecycle-declared generated canonical input. "
                "Run `python pipelines/ingest/usfm_importer.py --canonical-66-filter` first. "
                f"Missing: {missing}",
                file=sys.stderr,
            )
            return 1
        skipped = skipped_generated_data_gates(ROOT)
        print(
            "Generated canonical sidecars are absent; skipping lifecycle-declared generated-data gates. "
            "Run `python pipelines/ingest/usfm_importer.py --canonical-66-filter` before release/full-data "
            f"verification to enable them. Missing: {missing}. Skipped gates: {', '.join(sorted(skipped))}"
        )
    for name, cmd in build_gates():
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            failures.append(name)
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
        else:
            print(result.stdout.strip())
    if failures:
        print(f"\nVALIDATION SUITE FAILED: {', '.join(failures)}")
        return 1
    print("\nAll validation gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
