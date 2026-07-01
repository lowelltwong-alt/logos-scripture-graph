"""Tests for scratch lane policy validator."""
from scripts.validate_scratch_lane_policy import validate_policy


def test_scratch_lane_policy_validates() -> None:
    assert validate_policy() == []
