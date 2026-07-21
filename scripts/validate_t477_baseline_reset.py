#!/usr/bin/env python3
"""Validate owner-authorized T477 baseline reset after audited candidate regeneration."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts.validate_t475_generated_transition_state import (
        CANDIDATE_COUNTS,
        CANDIDATE_MANIFEST,
        DEFERRED_PYTEST_NODES,
        REQUIRED_DEFERRED,
        T475TransitionError,
        detect_generated_state,
        validate_semantic_manifest,
    )
except ModuleNotFoundError:  # pragma: no cover
    from validate_t475_generated_transition_state import (
        CANDIDATE_COUNTS,
        CANDIDATE_MANIFEST,
        DEFERRED_PYTEST_NODES,
        REQUIRED_DEFERRED,
        T475TransitionError,
        detect_generated_state,
        validate_semantic_manifest,
    )

ROOT = Path(__file__).resolve().parent.parent
FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
T475_CONTROL = ROOT / ".ai" / "control" / "t475_usfm_shadow_delta_gate.yaml"
ALLOWED_FOCUS = {"T477", "T478"}


class T477BaselineError(ValueError):
    """Raised when the T477 baseline reset is incomplete or unauthorized."""


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        header = yaml.safe_load(parts[1]) or {}
        body = yaml.safe_load(parts[2]) or {}
        return {**header, **body}
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise T477BaselineError(f"{path}: expected YAML mapping")
    return data


def current_task(root: Path = ROOT) -> str | None:
    focus_path = root / ".ai" / "control" / "current_focus.yaml"
    try:
        data = yaml.safe_load(focus_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    if not isinstance(data, dict):
        return None
    task = data.get("current_task")
    return task if isinstance(task, str) else None


def t477_migration_active(root: Path = ROOT) -> bool:
    """True when focus is T477/T478 and regenerated surfaces match the audited candidate."""
    if current_task(root) not in ALLOWED_FOCUS:
        return False
    return detect_generated_state(root) == "candidate"


def validate_baseline_reset(root: Path = ROOT) -> dict[str, Any]:
    task = current_task(root)
    if task not in ALLOWED_FOCUS:
        raise T477BaselineError(f"current_task must be T477 or T478 during baseline migration, observed {task!r}")
    state = detect_generated_state(root)
    if state != "candidate":
        raise T477BaselineError(
            "regenerated surfaces must match audited post-T519 candidate counts "
            f"(word_tokens={CANDIDATE_COUNTS[0]}, footnotes={CANDIDATE_COUNTS[1]}); observed {state}"
        )
    control = _read_yaml(root / ".ai" / "control" / "t475_usfm_shadow_delta_gate.yaml")
    exec_state = control.get("execution_state")
    if not isinstance(exec_state, dict):
        raise T477BaselineError("T475 execution_state missing")
    required_evidence = control.get("required_evidence")
    if not isinstance(required_evidence, dict):
        raise T477BaselineError("T475 required_evidence missing")
    if required_evidence.get("independent_audit_status") != "PASS":
        raise T477BaselineError("T477 requires T475 independent_audit_status PASS")
    if exec_state.get("independent_audit_complete") is not True:
        raise T477BaselineError("T477 requires independent_audit_complete")
    if exec_state.get("evidence_ready_for_T476") is not True:
        raise T477BaselineError("T477 requires evidence_ready_for_T476")
    if exec_state.get("t476_owner_authorized_T477") is not True:
        raise T477BaselineError("T477 requires t476_owner_authorized_T477 in T475 execution_state")
    if exec_state.get("t477_baseline_reset_complete") is not True:
        raise T477BaselineError("T477 requires t477_baseline_reset_complete after regeneration")

    policy = control.get("ci_generated_transition_policy")
    if not isinstance(policy, dict):
        raise T477BaselineError("CI generated-transition policy missing")
    if policy.get("superseded_by") != "T477":
        raise T477BaselineError("T475 transition policy must record superseded_by: T477")
    if set(policy.get("deferred_legacy_generated_validators", [])) != REQUIRED_DEFERRED:
        raise T477BaselineError("deferred validator set drifted from reviewed T475/T477 set")
    if set(policy.get("deferred_pytest_nodes", [])) != DEFERRED_PYTEST_NODES:
        raise T477BaselineError("deferred pytest node set drifted from reviewed T475/T477 set")
    if policy.get("authorizes_gold_or_output_change") is not False:
        raise T477BaselineError("gold/output change must remain unauthorized through T477")
    if policy.get("authorizes_baseline_update") is not True:
        raise T477BaselineError("T477 must authorize baseline update after owner Option A")

    result = validate_semantic_manifest(root, root / ".ai" / "context" / "agent_work" / "T475" / "candidate_manifest_t519.json")
    return {
        "state": "post_t477_baseline",
        "current_task": task,
        **result,
        "deferred": sorted(REQUIRED_DEFERRED),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        result = validate_baseline_reset(ROOT)
    except (T477BaselineError, T475TransitionError) as exc:
        print(f"T477 baseline reset validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T477 baseline reset validation passed "
        f"({result['surfaces']} JSONL surfaces; {result['rows']} rows; focus={result['current_task']})."
    )
    print("Gold/chunker migration nodes remain deferred until T478-T479:")
    for name in sorted(REQUIRED_DEFERRED):
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
