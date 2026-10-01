from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "reviews" / "Hos" / "rematerialize_semantic_prose_v8.py"
SPEC = importlib.util.spec_from_file_location("hos_rematerialize_v8_prepare", SCRIPT)
assert SPEC and SPEC.loader
REMAT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REMAT
SPEC.loader.exec_module(REMAT)


def test_prepare_gate_fails_before_attempt_creation(monkeypatch: pytest.MonkeyPatch) -> None:
    before = REMAT.ATTEMPT.exists()
    monkeypatch.setattr(
        REMAT,
        "require_qualified_publication_primitives",
        lambda: (_ for _ in ()).throw(RuntimeError("qualification blocked")),
    )
    with pytest.raises(RuntimeError, match="qualification blocked"):
        REMAT.prepare_v8()
    assert REMAT.ATTEMPT.exists() is before


def test_prepare_and_validation_bind_all_qualification_hashes() -> None:
    source = inspect.getsource(REMAT.prepare_v8) + inspect.getsource(REMAT.validate_prepared_v8)
    for field in (
        "kernel_v5_sha256",
        "kernel_v5_independent_check_sha256",
        "rooted_replace_sha256",
        "rooted_replace_independent_check_sha256",
        "architecture_ruling_sha256",
        "environment_gate_premortem_sha256",
    ):
        assert field in source
    assert "v5_staged_content_reuse" in source
    assert "v6_staged_content_reuse" in source
    assert "REUSED_PASS_ONLY_BECAUSE_ALL_13_TARGETS_BYTE_IDENTICAL" in source


def test_prepare_contract_names_all_five_validators() -> None:
    source = inspect.getsource(REMAT.validate_complete_staged_contract)
    for validator_id in (
        "official_chunk_map",
        "corrective_review_depth",
        "literary_quality_protocol",
        "exact_book_coverage",
        "review_coverage",
    ):
        assert validator_id in source


def test_prepare_receipt_is_candidate_only_and_not_completion() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert '"candidate_only": True' in source
    assert '"non_authorizing": True' in source
    assert '"completion_state": "not_completed"' in source
    assert "prepare_receipt_v8.json" in source