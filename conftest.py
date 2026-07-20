"""Repository-wide pytest lifecycle hooks."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

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
GENERATED_DATA_MARKER = "generated_data"


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


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "generated_data(*paths): skip this test in a clean checkout when one or more "
        "declared data/canonical inputs are absent",
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Enforce explicit generated-sidecar dependencies at the test boundary."""
    marker = item.get_closest_marker(GENERATED_DATA_MARKER)
    if marker is None:
        return
    if not marker.args:
        raise pytest.UsageError("generated_data marker requires at least one repository-relative path")

    missing: list[str] = []
    for raw_path in marker.args:
        marker_path = PurePosixPath(raw_path) if isinstance(raw_path, str) else None
        if (
            marker_path is None
            or marker_path.is_absolute()
            or marker_path.parts[:2] != ("data", "canonical")
            or ".." in marker_path.parts
            or "\\" in raw_path
        ):
            raise pytest.UsageError(
                "generated_data marker paths must be repository-relative under data/canonical/"
            )
        path = ROOT / raw_path
        if not path.is_file():
            missing.append(raw_path)
    if missing:
        pytest.skip(
            "generated canonical sidecar(s) absent in clean checkout: "
            f"{', '.join(missing)}; run `python pipelines/ingest/usfm_importer.py "
            "--canonical-66-filter` before full-data verification"
        )
