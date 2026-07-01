#!/usr/bin/env python3
"""Run all repository validation gates (green/red for CI and agents).

Always-run gates: repo, control plane, handoffs, source manifest.
Conditional gates: JSONL referential integrity + canon presence run only when
the generated canonical data is present (so clean checkouts stay green; CI
regenerates the data first, then this gate is real). The 432 MB word_tokens
file is intentionally excluded for runtime — validate it separately/nightly.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

MANIFEST = ROOT / "data" / "raw" / "bible" / "eng-web" / "source_manifest.yaml"
CANON_DIR = ROOT / "data" / "canonical"
SMALL_CANON = [
    CANON_DIR / "scripture" / "passages" / "passages.jsonl",
    CANON_DIR / "translations" / "eng-web" / "translation_witnesses.jsonl",
    CANON_DIR / "translations" / "eng-web" / "section_headings.jsonl",
    CANON_DIR / "translations" / "eng-web" / "footnotes.jsonl",
    CANON_DIR / "translations" / "eng-web" / "editorial_cross_references.jsonl",
    CANON_DIR / "translations" / "eng-web" / "glossary_entries.jsonl",
]
CANON_SCOPE_FILES = [
    *SMALL_CANON,
    CANON_DIR / "translations" / "eng-web" / "boundary_claims.jsonl",
    CANON_DIR / "translations" / "eng-web" / "word_tokens.jsonl",
]
QA_REQUIRED = [
    CANON_DIR / "scripture" / "passages" / "passages.jsonl",
    CANON_DIR / "translations" / "eng-web" / "translation_witnesses.jsonl",
]


def changed_paths() -> list[str]:
    paths: list[str] = []
    for args in (
        ["git", "diff", "--name-only", "origin/main...HEAD"],
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


def build_gates() -> list[tuple[str, list[str]]]:
    gates: list[tuple[str, list[str]]] = [
        ("validate_repo.py", [PY, str(ROOT / "scripts" / "validate_repo.py")]),
        ("validate_control_plane.py", [PY, str(ROOT / "scripts" / "validate_control_plane.py")]),
        ("validate_repository_link_contract.py", [PY, str(ROOT / "scripts" / "validate_repository_link_contract.py")]),
        (
            "validate_governance_dependency_map_mirror.py",
            [PY, str(ROOT / "scripts" / "validate_governance_dependency_map_mirror.py")],
        ),
        ("validate_handoffs.py", [PY, str(ROOT / "scripts" / "agent" / "validate_handoffs.py")]),
        *task_scope_gates(),
        *parallel_execution_safety_gates(),
        ("validate_canonical_66_scope.py", [PY, str(ROOT / "scripts" / "validate_canonical_66_scope.py")]),
        ("validate_vectorization_plan.py", [PY, str(ROOT / "scripts" / "validate_vectorization_plan.py")]),
        (
            "validate_chunking_theological_decision_register.py",
            [PY, str(ROOT / "scripts" / "validate_chunking_theological_decision_register.py")],
        ),
        (
            "validate_chunking_lesson_index.py",
            [PY, str(ROOT / "scripts" / "validate_chunking_lesson_index.py")],
        ),
        (
            "validate_test_runtime_preflight.py",
            [PY, str(ROOT / "scripts" / "validate_test_runtime_preflight.py")],
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
            "validate_source_metadata_research_atlas.py",
            [PY, str(ROOT / "scripts" / "validate_source_metadata_research_atlas.py")],
        ),
        (
            "validate_apocalyptic_prophetic_intertext_dossier_queue.py",
            [PY, str(ROOT / "scripts" / "validate_apocalyptic_prophetic_intertext_dossier_queue.py")],
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
            "validate_bible_verse_passage_coverage_inventory.py",
            [PY, str(ROOT / "scripts" / "validate_bible_verse_passage_coverage_inventory.py")],
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
            "validate_1cor8_10_parent_evidence_packet.py",
            [PY, str(ROOT / "scripts" / "validate_1cor8_10_parent_evidence_packet.py")],
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
            "validate_divine_capitalization_inventory.py",
            [PY, str(ROOT / "scripts" / "validate_divine_capitalization_inventory.py")],
        ),
        (
            "validate_wj_marker_inventory.py",
            [PY, str(ROOT / "scripts" / "validate_wj_marker_inventory.py")],
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
    scope_present = [p for p in CANON_SCOPE_FILES if p.exists()]
    if scope_present:
        scope_cmd = [PY, str(ROOT / "scripts" / "validate_canonical_66_scope.py"), *[str(p) for p in scope_present]]
        gates.append(("validate_canonical_66_scope.py (canonical)", scope_cmd))
    present = [p for p in SMALL_CANON if p.exists()]
    if present:
        cmd = [PY, str(ROOT / "scripts" / "validate_jsonl.py"), "--require-canon", *[str(p) for p in present]]
        gates.append(("validate_jsonl.py (canonical)", cmd))
    if all(path.exists() for path in QA_REQUIRED):
        qa_cmd = [PY, str(ROOT / "scripts" / "qa_canonical_corpus.py")]
        if not (CANON_DIR / "translations" / "eng-web" / "word_tokens.jsonl").exists():
            qa_cmd.append("--skip-word-tokens")
        gates.append(("qa_canonical_corpus.py", qa_cmd))
    return gates


def main() -> int:
    failures = []
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
