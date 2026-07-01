from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts import validate_t411_cursor_batch_artifacts as validator


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    _write(path, "\n".join(json.dumps(row) for row in rows) + "\n")


def _minimal_task(tmp_path: Path) -> Path:
    task = {
        "id": "T411",
        "branch": "codex/t411-cursor-readiness-gate",
        "cursor_execution_allowed": False,
        "cursor_run_status": "not_started",
        "claude_final_audit_gate": {"status": "passed_no_p0_p1_forward_p2s_only"},
        "rust_observation_substrate_gate": {
            "task_id": "T412",
            "cursor_may_start_before_substrate_validates": False,
            "default_cursor_input": "compressed_observation_ledgers",
        },
        "cursor_allowed_write_roots": [".ai/context/agent_work/T411/", ".ai/handoffs/T411/"],
        "authorization": {
            "cursor_may_select_target": False,
            "promotes_reviewed_gold": False,
            "implements_chunk_output": False,
            "adds_child_spans": False,
            "changes_route_behavior": False,
            "changes_evaluator_behavior": False,
            "creates_graph_or_retrieval_truth": False,
            "runs_embeddings_or_builds_indexes": False,
            "imports_boundary_material": False,
            "chooses_backend": False,
            "promotes_retrieval_profile": False,
            "selects_preferred_reading_or_source_tradition": False,
            "changes_canon_scope": False,
            "authorizes_source_or_manuscript_rows": False,
            "authorizes_theology_authority": False,
        },
        "candidate_docket": {
            "cursor_may_choose_candidates": False,
            "candidates": [
                {"candidate_id": "T402-LC-063", "parent_span": "2John.1.1-2John.1.3"},
                {"candidate_id": "T402-LC-057", "parent_span": "Phlm.1.1-Phlm.1.7"},
                {"candidate_id": "T402-LC-032", "parent_span": "Jonah.1.1-Jonah.1.3"},
            ],
        },
    }
    path = tmp_path / "T411.task.yaml"
    _write(path, yaml.safe_dump(task, sort_keys=False))
    return path


def _setup_agent_work(tmp_path: Path) -> tuple[Path, Path]:
    agent_work = tmp_path / "agent_work" / "T411"
    handoff = tmp_path / "handoffs" / "T411"
    _write(agent_work / "candidate_options_docket.md", "T402-LC-063\nT402-LC-057\nT402-LC-032\nnon-authorizing\n")
    _write(agent_work / "per_candidate_prompt_notes.md", "Greek\nHebrew\nnon-authorizing\n")
    _write(agent_work / "validation_runtime_note.md", "validate_all.py\n900000\n")
    for name in ("biblical_literature_review.md", "greek_review.md", "hebrew_review.md", "frontier_review.md"):
        _write(agent_work / "escalation_packet_templates" / name, "non-authorizing template\n")
    _write(handoff / "handoff.md", "# Task Handoff\n\n## Task\n\n## Agent\n\n## Files read\n\n## Files changed\n\n## Decisions made\n\n## Validation run\n\n## Known risks\n\n## Open questions\n\n## Next agent instruction\n")
    return agent_work, handoff


def _complete_artifacts(agent_work: Path, handoff: Path) -> None:
    (agent_work / "escalation_packets").mkdir(parents=True, exist_ok=True)
    _write_jsonl(
        agent_work / "source_size_manifest.jsonl",
        [
            {
                "task_id": "T411",
                "source_path": "data/raw/bible/eng-web/eng-web_usfm.zip",
                "source_kind": "raw_usfm",
                "bytes_read": 10,
                "char_count": 10,
                "line_count": 1,
                "record_count": 1,
                "chapter_count": 1,
                "verse_count": 3,
                "sha256_short": "abcdef12",
                "files_read": True,
            }
        ],
    )
    _write_jsonl(
        agent_work / "confidence_register.jsonl",
        [
            {
                "task_id": "T411",
                "book": "2John",
                "osis_ref_or_span": "2John.1.1-2John.1.3",
                "claim_id": "T411-CLAIM-001",
                "confidence": "medium",
                "confidence_reason": "Observed local opening greeting markers.",
                "evidence_type": "raw_usfm",
                "evidence_refs": ["source_size_manifest.jsonl:1"],
                "inferred_or_observed": "observed",
                "theology_sensitive": False,
                "escalation_required": False,
                "escalation_reason": "",
                "non_authorizing": True,
            }
        ],
    )
    _write_jsonl(
        agent_work / "audit_log.jsonl",
        [
            {
                "timestamp_utc": "2026-06-30T00:00:00Z",
                "task_id": "T411",
                "command_or_action": "python scripts/validate_parallel_execution_safety.py --task-id T411 --require-task-branch",
                "inputs": ["T411"],
                "outputs": ["Parallel execution safety validation passed."],
                "result": "passed",
                "limitations": [],
                "non_authorizing": True,
                "git_status_preflight": "clean",
            }
        ],
    )
    _write(agent_work / "claim_traceability_matrix.md", "T411-CLAIM-001 | medium | evidence | non-authorizing\n")
    notes = "\n".join(f"## {section.replace('_', ' ').title()}" for section in validator._read_yaml(validator.CONTRACT)["required_handoff_note"]["required_sections"])
    _write(handoff / "cursor_notes_to_codex.md", notes + "\n")


def test_repo_t411_setup_validates_without_cursor_artifacts() -> None:
    result = validator.validate_t411_cursor_batch_artifacts()

    assert result["artifacts"]["mode"] in {"setup", "artifacts"}


def test_setup_rejects_cursor_execution_enabled(tmp_path: Path) -> None:
    task_file = _minimal_task(tmp_path)
    agent_work, handoff = _setup_agent_work(tmp_path)
    data = yaml.safe_load(task_file.read_text(encoding="utf-8"))
    data["cursor_execution_allowed"] = True
    task_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.T411CursorBatchArtifactError, match="cursor_execution_allowed"):
        validator.validate_task_setup(task_file=task_file, agent_work=agent_work, handoff_dir=handoff)


def test_setup_rejects_wrong_candidate_docket(tmp_path: Path) -> None:
    task_file = _minimal_task(tmp_path)
    agent_work, handoff = _setup_agent_work(tmp_path)
    data = yaml.safe_load(task_file.read_text(encoding="utf-8"))
    data["candidate_docket"]["candidates"].append({"candidate_id": "T402-LC-064", "parent_span": "3John.1.1-3John.1.4"})
    task_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.T411CursorBatchArtifactError, match="candidate docket"):
        validator.validate_task_setup(task_file=task_file, agent_work=agent_work, handoff_dir=handoff)


def test_require_artifacts_rejects_missing_future_outputs(tmp_path: Path) -> None:
    agent_work, handoff = _setup_agent_work(tmp_path)

    with pytest.raises(validator.T411CursorBatchArtifactError, match="missing required"):
        validator.validate_emitted_artifacts(agent_work=agent_work, handoff_dir=handoff, require_artifacts=True)


def test_complete_future_artifact_set_validates(tmp_path: Path) -> None:
    agent_work, handoff = _setup_agent_work(tmp_path)
    _complete_artifacts(agent_work, handoff)

    result = validator.validate_emitted_artifacts(agent_work=agent_work, handoff_dir=handoff, require_artifacts=True)

    assert result["mode"] == "artifacts"
    assert result["claims"] == 1


def test_confidence_register_requires_non_authorizing(tmp_path: Path) -> None:
    agent_work, handoff = _setup_agent_work(tmp_path)
    _complete_artifacts(agent_work, handoff)
    rows = [json.loads((agent_work / "confidence_register.jsonl").read_text(encoding="utf-8").splitlines()[0])]
    rows[0]["non_authorizing"] = False
    _write_jsonl(agent_work / "confidence_register.jsonl", rows)

    with pytest.raises(validator.T411CursorBatchArtifactError, match="non_authorizing"):
        validator.validate_emitted_artifacts(agent_work=agent_work, handoff_dir=handoff, require_artifacts=True)


def test_theology_sensitive_claim_requires_escalation_packet(tmp_path: Path) -> None:
    agent_work, handoff = _setup_agent_work(tmp_path)
    _complete_artifacts(agent_work, handoff)
    rows = [json.loads((agent_work / "confidence_register.jsonl").read_text(encoding="utf-8").splitlines()[0])]
    rows[0]["theology_sensitive"] = True
    rows[0]["escalation_required"] = True
    rows[0]["escalation_reason"] = "identity claim pressure"
    _write_jsonl(agent_work / "confidence_register.jsonl", rows)

    with pytest.raises(validator.T411CursorBatchArtifactError, match="escalation packet required"):
        validator.validate_emitted_artifacts(agent_work=agent_work, handoff_dir=handoff, require_artifacts=True)


def test_artifacts_reject_forbidden_authority_claim(tmp_path: Path) -> None:
    agent_work, handoff = _setup_agent_work(tmp_path)
    _complete_artifacts(agent_work, handoff)
    _write(agent_work / "claim_traceability_matrix.md", "T411-CLAIM-001\npromotes_reviewed_gold: true\n")

    with pytest.raises(validator.T411CursorBatchArtifactError, match="forbidden authority"):
        validator.validate_emitted_artifacts(agent_work=agent_work, handoff_dir=handoff, require_artifacts=True)
