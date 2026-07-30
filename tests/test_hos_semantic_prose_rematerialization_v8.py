from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "reviews" / "Hos" / "rematerialize_semantic_prose_v8.py"
SPEC = importlib.util.spec_from_file_location("hos_rematerialize_v8_policy", SCRIPT)
assert SPEC and SPEC.loader
REMAT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REMAT
SPEC.loader.exec_module(REMAT)


def test_exact_scoped_qualification_is_evidence_not_authority() -> None:
    evidence = REMAT.qualification_evidence()
    assert evidence == {
        "kernel_v5_sha256": REMAT.EXPECTED_PINS[REMAT.KERNEL_PATH],
        "kernel_v5_independent_check_sha256": REMAT.EXPECTED_PINS[REMAT.KERNEL_V5_INDEPENDENT_CHECK],
        "rooted_replace_sha256": REMAT.EXPECTED_PINS[REMAT.ROOTED_REPLACE_PATH],
        "rooted_replace_independent_check_sha256": REMAT.EXPECTED_PINS[REMAT.ROOTED_REPLACE_CHECK],
        "architecture_ruling_sha256": REMAT.EXPECTED_PINS[REMAT.HANDLE_REPLACEMENT_ARCHITECTURE_RULING],
        "environment_gate_premortem_sha256": REMAT.EXPECTED_PINS[REMAT.ENVIRONMENT_GATE_PREMORTEM],
    }
    kernel = REMAT.load_json(REMAT.KERNEL_V5_INDEPENDENT_CHECK)
    rooted = REMAT.load_json(REMAT.ROOTED_REPLACE_CHECK)
    environment = REMAT.load_json(REMAT.ENVIRONMENT_GATE_PREMORTEM)
    assert kernel["publication_authorized"] is False
    assert rooted["verdict"]["current_publication_authority"] == "FAIL"
    assert environment["verdict"] == "CONDITIONAL_PASS_GATE_DESIGN_CURRENT_READINESS_FAIL"
    assert environment["publication_authorized"] is False


def test_prior_v7_failure_and_rejection_are_preserved() -> None:
    REMAT.verify_v7_rejected_scaffold_preserved()


def test_render_is_exactly_thirteen_targets_and_reuses_only_bytes() -> None:
    rendered, metadata = REMAT.build_render()
    assert tuple(rendered) == REMAT.TARGETS
    assert len(rendered) == 13
    assert metadata["decision_count"] == 38
    REMAT.validate_known_render_hashes(rendered)
    entries = [
        {"path": rel, "staged_sha256": REMAT.digest_bytes(rendered[rel]), "staged_size_bytes": len(rendered[rel])}
        for rel in REMAT.TARGETS
    ]
    for reuse in (REMAT.v5_staged_content_reuse(entries), REMAT.v6_staged_content_reuse(entries)):
        assert reuse["verdict"] == "REUSED_PASS_ONLY_BECAUSE_ALL_13_TARGETS_BYTE_IDENTICAL"
        assert reuse["checked_target_count"] == 13
        assert reuse["transaction_verdict_not_reused"] is True
    drifted = [dict(row) for row in entries]
    drifted[0]["staged_sha256"] = "0" * 64
    with pytest.raises(RuntimeError, match="not byte-identical"):
        REMAT.v5_staged_content_reuse(drifted)


def test_exact_human_text_does_not_exist_as_authorization_artifact() -> None:
    premortem = REMAT.load_json(REMAT.ENVIRONMENT_GATE_PREMORTEM)
    assert premortem["exact_lowell_acknowledgment_text"] == REMAT.EXACT_LOWELL_ACKNOWLEDGMENT_TEXT
    assert not REMAT.ATTEMPT.exists()
    assert not REMAT.PREPARE_RECEIPT.exists()