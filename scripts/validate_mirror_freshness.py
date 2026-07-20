#!/usr/bin/env python3
"""Validate Scripture-local freshness metadata for upstream governance mirrors."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / ".ai" / "control" / "governance_dependency_map_mirror.yaml"

EXPECTED_UPSTREAM_COMMIT = "ad338b5c2dc2c8d979843707aaaabb834cf64785"
SOURCE_ROOT_CANDIDATES = [
    "../logos-governance-architecture",
]
REQUIRED_UPSTREAM_PATHS = [
    "governance/GOVERNANCE_DEPENDENCY_MAP.yaml",
    "governance/MIRROR_FRESHNESS_STANDARD.yaml",
    "governance/CROSS_REPO_REFERENCE_MANIFEST.yaml",
]
REQUIRED_LOCAL_GATE_TRIGGER_TARGETS = [
    ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml",
    ".ai/control/original_language_phrase_context_policy.yaml",
    ".ai/control/textual_variant_source_tradition_dossier_queue.yaml",
]
REQUIRED_TOKENS = {
    "mirror_freshness:",
    "freshness_standard_ref: logos-governance-architecture:governance/MIRROR_FRESHNESS_STANDARD.yaml",
    "cross_repo_reference_manifest_ref: logos-governance-architecture:governance/CROSS_REPO_REFERENCE_MANIFEST.yaml",
    f"upstream_governance_commit: {EXPECTED_UPSTREAM_COMMIT}",
    "verified_against_upstream_commit_at: \"2026-07-07T00:00:00Z\"",
    "staleness_budget_days: 14",
    "local_source_repo_unavailable_policy: report_when_unavailable",
    "missing_or_drifted_upstream_control_policy: fail_closed_when_source_repo_available",
    "local_gate_trigger_target_policy: fail_closed_when_scripture_control_path_missing",
    "authorizes_child_repo_override: false",
}


def find_local_source_root(root: Path) -> Path | None:
    for candidate in SOURCE_ROOT_CANDIDATES:
        path = (root / candidate).resolve()
        if path.exists() and path.is_dir():
            return path
    return None


def git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=path,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def validate(root: Path = ROOT, *, require_local_source: bool = False) -> list[str]:
    errors: list[str] = []
    mirror = root / ".ai/control/governance_dependency_map_mirror.yaml"
    if not mirror.exists():
        return [".ai/control/governance_dependency_map_mirror.yaml is missing"]

    text = mirror.read_text(encoding="utf-8")
    for token in sorted(REQUIRED_TOKENS):
        if token not in text:
            errors.append(f"mirror freshness metadata missing token: {token}")

    for rel in REQUIRED_LOCAL_GATE_TRIGGER_TARGETS:
        if not (root / rel).exists():
            errors.append(f"governance-referenced gate trigger target missing: {rel}")

    source_root = find_local_source_root(root)
    if source_root is None:
        if require_local_source:
            errors.append("local source repo missing for mirror freshness validation")
        return errors

    for rel in REQUIRED_UPSTREAM_PATHS:
        if not (source_root / rel).exists():
            errors.append(f"missing upstream governance control: logos-governance-architecture:{rel}")

    head = git_head(source_root)
    if head is not None and head != EXPECTED_UPSTREAM_COMMIT:
        errors.append(
            f"upstream governance commit drift: expected {EXPECTED_UPSTREAM_COMMIT} got {head}"
        )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-local-source", action="store_true")
    args = parser.parse_args(argv)
    errors = validate(require_local_source=args.require_local_source)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Mirror freshness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
