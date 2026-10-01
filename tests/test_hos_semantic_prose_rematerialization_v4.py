from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "reviews"
    / "Hos"
    / "rematerialize_semantic_prose_v4.py"
)
SPEC = importlib.util.spec_from_file_location("hos_rematerialize_v4", SCRIPT)
assert SPEC and SPEC.loader
REMAT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REMAT
SPEC.loader.exec_module(REMAT)


def mutate_json_bytes(payload: bytes, mutator) -> bytes:
    value = [
        json.loads(line)
        for line in payload.decode("utf-8").splitlines()
        if line.strip()
    ]
    mutator(value)
    return REMAT.jsonl_bytes(value)


def test_render_is_exactly_pinned_and_covers_hosea() -> None:
    rendered, metadata = REMAT.build_render()
    assert set(rendered) == set(REMAT.TARGETS)
    assert metadata["decision_count"] == 38
    assert metadata["accepted_count"] == 36
    assert metadata["held_count"] == 2
    assert metadata["coverage_count"] == 197
    assert metadata["logical_route_change_count"] == 114
    assert metadata["derived_sidecar_change_count"] == 4
    assert set(metadata["sidecar_diff_paths"]) == REMAT.ALLOWED_SIDECAR_DIFFS
    REMAT.validate_known_render_hashes(rendered)


@pytest.mark.parametrize(
    ("target", "mutator"),
    [
        (
            "book_chunks/Hos/chunks.jsonl",
            lambda rows: rows[0].__setitem__("span", "Hos.1.1-Hos.1.2"),
        ),
        (
            "book_chunks/Hos/chunks.jsonl",
            lambda rows: rows[0].__setitem__("confidence", "low"),
        ),
        (
            "reviews/Hos/review_packets.jsonl",
            lambda rows: rows[0]["primary_reviews"][0].__setitem__(
                "reviewer_attempt_id",
                "mutated-attempt",
            ),
        ),
    ],
    ids=["boundary", "confidence", "review_attempt_id"],
)
def test_protected_render_mutations_fail_exact_hash_gate(
    target: str,
    mutator,
) -> None:
    rendered, _metadata = REMAT.build_render()
    rendered[target] = mutate_json_bytes(rendered[target], mutator)
    with pytest.raises(RuntimeError, match="predicted staged hash drift"):
        REMAT.validate_known_render_hashes(rendered)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("hold_id", "WRONG-HOLD"),
        ("human_question", "Wrong question?"),
        ("review_status", "accepted_candidate"),
        ("decision_id", "M7_sol-Hos-999"),
        ("non_authorizing", False),
    ],
)
def test_non_prose_sidecar_mutations_are_not_allowlisted(
    field: str,
    value,
) -> None:
    old = json.loads((REMAT.MODEL / REMAT.TARGETS[9]).read_text("utf-8"))
    rendered, _metadata = REMAT.build_render()
    new = json.loads(rendered[REMAT.TARGETS[9]])
    row = new["rows"]["low_confidence_register.jsonl"][0]
    row[field] = value
    diffs = set(REMAT.recursive_diff(old, new))
    assert diffs != REMAT.ALLOWED_SIDECAR_DIFFS
    assert any(path.endswith(f".{field}") for path in diffs)


def test_fifth_sidecar_scalar_is_not_allowlisted() -> None:
    old = json.loads((REMAT.MODEL / REMAT.TARGETS[9]).read_text("utf-8"))
    rendered, _metadata = REMAT.build_render()
    new = json.loads(rendered[REMAT.TARGETS[9]])
    new["rows"]["frontier_escalation_queue.jsonl"][0][
        "possible_downstream_risk"
    ] = "unauthorized fifth scalar"
    diffs = set(REMAT.recursive_diff(old, new))
    assert diffs != REMAT.ALLOWED_SIDECAR_DIFFS
    assert len(diffs) == 5


def test_closed_checker_schema_rejects_minimal_pass_object() -> None:
    minimal = {
        "verdict": "PASS",
        "book": "Hos",
        "checked_implementation_sha256": "wrong",
    }
    with pytest.raises(RuntimeError, match="closed-schema drift"):
        REMAT.require_exact_mapping(
            minimal,
            {
                "verdict",
                "book",
                "checked_implementation_sha256",
                "checked_kernel_sha256",
            },
            "implementation checker",
        )


def test_checker_fails_closed_without_failure_matrix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing = tmp_path / "missing-failure-evidence.json"
    monkeypatch.setattr(REMAT, "FAILURE_EVIDENCE", missing)
    with pytest.raises(FileNotFoundError):
        REMAT.validate_failure_evidence()

def test_legacy_writer_guard_denies_concurrent_open() -> None:
    if REMAT.os.name != "nt":
        pytest.skip("reviewed guard is Windows-environment-bound")
    with REMAT.LegacyExecutionGuard():
        with pytest.raises(OSError):
            REMAT.LEGACY_ADAPTER.read_bytes()
    assert REMAT.LEGACY_ADAPTER.read_bytes()


def test_symlink_or_reparse_substitution_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "root"
    root.mkdir()
    target = root / "target.json"
    target.write_text("{}\n", encoding="utf-8")
    original = Path.is_symlink

    def pretend_symlink(path: Path) -> bool:
        return path == target or original(path)

    monkeypatch.setattr(Path, "is_symlink", pretend_symlink)
    with pytest.raises(RuntimeError, match="symbolic link"):
        REMAT.ensure_regular_contained(target, root)


def test_before_completed_rehashes_global_sentinels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed = []
    monkeypatch.setattr(REMAT, "validate_runtime_paths", lambda _paths: None)
    monkeypatch.setattr(
        REMAT,
        "validator_program_hashes",
        lambda: {"validator": "pinned"},
    )
    monkeypatch.setattr(REMAT, "verify_explicit_hashes", lambda *_args: None)

    def sentinel_check(*, include_globals=True, include_legacy=True):
        observed.append((include_globals, include_legacy))
        if include_globals:
            raise RuntimeError("global sentinel race")

    monkeypatch.setattr(REMAT, "verify_pins", sentinel_check)
    manifest = {
        "writer_sha256": REMAT.digest(REMAT.Path(REMAT.__file__)),
        "kernel_sha256": REMAT.digest(REMAT.KERNEL_PATH),
        "targets": [],
    }
    invariants = REMAT.build_transaction_invariants(
        manifest=manifest,
        evidence_paths=[],
        evidence_hashes={},
    )
    with pytest.raises(RuntimeError, match="global sentinel race"):
        invariants("before_completed")
    assert observed == [(True, False)]