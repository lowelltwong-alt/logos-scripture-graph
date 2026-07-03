#!/usr/bin/env python3
"""Validate multi-model whole-Bible chunking fork scaffold."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "multi_model_whole_bible_chunking_fork.yaml"
SCRATCH_MANIFEST = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "manifest.yaml"
SCRATCH_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking"
BASELINE = SCRATCH_ROOT / "shared_research_baseline" / "research_baseline_manifest.yaml"
MODEL_IDS_REQUIRED = ("M1_cursor", "M2_codex", "M3_claude", "M4_gemini")
MODEL_IDS_OPTIONAL = ("M5_composer_alt",)
COMPARE_SCRIPT = ROOT / "scripts" / "compare_multi_model_bible_chunk_maps.py"
CHUNK_MAP_VALIDATOR = ROOT / "scripts" / "validate_whole_bible_chunk_map.py"
MARATHON_STATUS = ROOT / "scripts" / "t423_marathon_status.py"
MERGE_SCRIPT = ROOT / "scripts" / "t423_merge_book_chunks.py"
RESUME_SCRIPT = ROOT / "scripts" / "t423_resume_book.py"
SUPERVISOR_SCRIPT = ROOT / "scripts" / "t423_marathon_supervisor.py"
REVERT_SCRIPT = ROOT / "scripts" / "evaluate_t423_revert_signal.py"
PILOT_GATE = ROOT / "scripts" / "validate_t423_pilot_gate.py"
PARALLEL_ISO = ROOT / "scripts" / "validate_t423_parallel_isolation.py"
TEMPLATE = SCRATCH_ROOT / "models" / "_TEMPLATE"


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{_rel(path)}: expected mapping")
    return data


def validate() -> list[str]:
    errors: list[str] = []
    if not POLICY.is_file():
        return [f"missing {_rel(POLICY)}"]
    policy = _read_yaml(POLICY)
    if policy.get("fork_id") != "whole_bible_multi_model_chunking_v1":
        errors.append("fork_id mismatch")
    if policy.get("task_id") != "T423":
        errors.append("task_id must be T423")
    authority = policy.get("authority", {})
    if authority.get("authorizes_canon_chunk_output"):
        errors.append("fork must not authorize canon chunk output")
    slots = policy.get("model_slots", [])
    if len(slots) < 4:
        errors.append("model_slots must have at least 4 entries (M1-M4)")
    mc = policy.get("model_count", {})
    if mc.get("maximum_supported", 0) < 10:
        errors.append("model_count.maximum_supported should be at least 10")
    if not SCRATCH_MANIFEST.is_file():
        errors.append(f"missing {_rel(SCRATCH_MANIFEST)}")
    if not BASELINE.is_file():
        errors.append(f"missing {_rel(BASELINE)}")
    for mid in MODEL_IDS_REQUIRED:
        folder = SCRATCH_ROOT / mid
        if not folder.is_dir():
            errors.append(f"missing model folder {_rel(folder)}")
        elif not (folder / "model_manifest.yaml").is_file():
            errors.append(f"missing {_rel(folder / 'model_manifest.yaml')}")
    for mid in MODEL_IDS_OPTIONAL:
        folder = SCRATCH_ROOT / mid
        if folder.is_dir() and not (folder / "model_manifest.yaml").is_file():
            errors.append(f"missing optional {_rel(folder / 'model_manifest.yaml')}")
    comp = SCRATCH_ROOT / "comparison"
    for name in ("delta_focus_queue.yaml", "model_agreement_matrix.yaml"):
        if not (comp / name).is_file():
            errors.append(f"missing {_rel(comp / name)}")
    redteam_prompt = ROOT / ".ai/prompts/multi_model_whole_bible_chunking_redteam_premortem_prompt.md"
    if not redteam_prompt.is_file():
        errors.append(f"missing {_rel(redteam_prompt)}")
    for script in (
        COMPARE_SCRIPT,
        CHUNK_MAP_VALIDATOR,
        MARATHON_STATUS,
        MERGE_SCRIPT,
        RESUME_SCRIPT,
        SUPERVISOR_SCRIPT,
        REVERT_SCRIPT,
        PILOT_GATE,
        PARALLEL_ISO,
        ROOT / "scripts" / "t423_pin_substrate.py",
    ):
        if not script.is_file():
            errors.append(f"missing {_rel(script)}")
    rust = policy.get("rust_observation_substrate", {})
    if not rust.get("required_before_marathon"):
        errors.append("rust_observation_substrate.required_before_marathon must be true")
    if not TEMPLATE.is_dir():
        errors.append(f"missing {_rel(TEMPLATE)}")
    rules = policy.get("comparison_rules", {})
    if rules.get("compare_when_at_least_models", 0) < 3:
        errors.append("comparison_rules.compare_when_at_least_models must be >= 3")
    revert = policy.get("revert_policy", {}).get("revert_threshold", {})
    if not revert.get("pilot_verse_coverage_agreement_rate_minimum"):
        errors.append("revert_policy.revert_threshold.pilot_verse_coverage_agreement_rate_minimum required")
    if not policy.get("pilot_gate", {}).get("required_books"):
        errors.append("pilot_gate.required_books required")
    isolation = policy.get("parallel_path_isolation", {})
    if not isolation.get("forbidden_reads"):
        errors.append("parallel_path_isolation.forbidden_reads required")
    if not isolation.get("worktree_required"):
        errors.append("parallel_path_isolation.worktree_required must be true")
    manifest_data = _read_yaml(SCRATCH_MANIFEST) if SCRATCH_MANIFEST.is_file() else {}
    active = manifest_data.get("model_count", {}).get("active_slots", [])
    for mid in MODEL_IDS_REQUIRED:
        if mid not in active:
            errors.append(f"manifest active_slots missing {mid}")
    for path in SCRATCH_ROOT.iterdir() if SCRATCH_ROOT.is_dir() else []:
        if path.is_dir() and path.name.startswith("M") and path.name[1:2].isdigit():
            mid_prefix = path.name.split("_", 1)[0]
            if mid_prefix in {"M6", "M7", "M8", "M9", "M10"}:
                models = manifest_data.get("models", {})
                if path.name not in models and f"{mid_prefix}_" not in str(manifest_data):
                    if not any(k.startswith(mid_prefix) for k in models):
                        errors.append(
                            f"reserved slot folder {_rel(path)} exists but not registered in manifest.yaml"
                        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate()
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"OK: {_rel(POLICY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
