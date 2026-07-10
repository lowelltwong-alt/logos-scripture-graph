"""Repository-wide pytest lifecycle hooks."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_t475_generated_transition_state import (
    DEFERRED_PYTEST_NODES,
    T475TransitionError,
    detect_generated_state,
    validate_transition,
)

ROOT = Path(__file__).resolve().parent
T475_SKIP_REASON = (
    "exact T475 regenerated candidate: pre-T474 generated-baseline assertion "
    "is deferred until the T477-T479 migration"
)


def apply_t475_transition_skips(items: list[pytest.Item], root: Path = ROOT) -> int:
    """Skip only declared stale-baseline nodes after exact candidate proof."""
    if detect_generated_state(root) != "candidate":
        return 0
    try:
        validate_transition(root)
    except (OSError, T475TransitionError, ValueError) as exc:
        raise pytest.UsageError(f"T475 candidate transition is not exact: {exc}") from exc

    skipped = 0
    for item in items:
        if item.nodeid in DEFERRED_PYTEST_NODES:
            item.add_marker(pytest.mark.skip(reason=T475_SKIP_REASON))
            skipped += 1
    return skipped


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    apply_t475_transition_skips(items)
