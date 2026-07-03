"""Tests for scratch multi-model ladder validator."""
from __future__ import annotations

from scripts.validate_scratch_multi_model_ladder import (
    validate_batch2_manifest,
    validate_l1_artifacts,
    validate_policy,
)


def test_policy_validates_clean() -> None:
    assert validate_policy() == []


def test_batch2_manifest_validates() -> None:
    assert validate_batch2_manifest() == []


def test_l1_artifacts_present() -> None:
    assert validate_l1_artifacts() == []
