"""Control plane and master-context governance tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_control_plane_validation_passes():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_control_plane.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_master_context_is_human_governed():
    text = (ROOT / ".ai" / "control" / "MASTER_CONTEXT.md").read_text(encoding="utf-8")
    assert "HUMAN-ONLY FILE" in text
    assert "READ ONLY" in text


def test_front_door_routes_to_master_context():
    text = (ROOT / "AI_FRONT_DOOR.md").read_text(encoding="utf-8")
    assert "MASTER_CONTEXT.md" in text
    assert "validate_control_plane.py" in text


def test_validate_all_suite():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_all.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
