from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / ".ai" / "control" / "governance_dependency_map_mirror.yaml"


def test_governance_dependency_map_mirror_records_upstream_gate() -> None:
    data = yaml.safe_load(MIRROR.read_text(encoding="utf-8"))

    assert data["object_type"] == "governance_dependency_map_mirror"
    assert data["owner_repo"] == "logos-scripture-graph"
    assert data["upstream_dependency_map"]["repo"] == "logos-governance-architecture"
    assert data["upstream_dependency_map"]["path"] == "governance/GOVERNANCE_DEPENDENCY_MAP.yaml"
    assert data["upstream_dependency_map"]["artifact_id"] == "GD-014"
    assert data["authority"]["local_repo_may_override_upstream_dependency_map"] is False
    assert data["authority"]["local_repo_must_stop_if_upstream_map_conflicts"] is True


def test_governance_dependency_map_mirror_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_governance_dependency_map_mirror.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
