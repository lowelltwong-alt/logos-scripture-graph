"""Tests for scratch scope validator."""
from scripts.validate_scratch_scope import validate_scratch_scope


def test_scratch_branch_allows_agent_work_paths() -> None:
    errors = validate_scratch_scope(
        branch="scratch/test-lane",
        changed_files=[
            ".ai/context/agent_work/T417/review_packet_drafts/phlm_opening_draft.md",
            ".ai/scratch/submissions/SUB-001/promotion_packet.yaml",
        ],
    )
    assert errors == []


def test_scratch_branch_blocks_canonical_data() -> None:
    errors = validate_scratch_scope(
        branch="scratch/test-lane",
        changed_files=["data/canonical/foo.jsonl"],
    )
    assert any("hard-forbidden" in e for e in errors)


def test_non_scratch_branch_fails() -> None:
    errors = validate_scratch_scope(
        branch="main",
        changed_files=[".ai/scratch/foo.md"],
    )
    assert any("must start with" in e for e in errors)
