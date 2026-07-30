"""Tests for T423 literary-marker quality protocol."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.validate_t423_literary_quality_protocol import validate_model_folder, validate_policy


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def _manifest(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "model_manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "model_id": "M_TEST",
                "quality_protocol": {
                    "strategy_id": "literary_marker_aware_v2",
                    "control": ".ai/control/t423_literary_marker_quality_protocol.yaml",
                    "low_confidence_register_required": True,
                    "frontier_escalation_queue_required": True,
                    "atlas_candidate_feed_required": True,
                    "book_strategy_required": True,
                },
            }
        ),
        encoding="utf-8",
    )


def _chunk(**extra: object) -> dict:
    row = {
        "model_id": "M_TEST",
        "book": "Phlm",
        "span": "Phlm.1.1-Phlm.1.25",
        "chunk_index_in_book": 1,
        "literature_type_guess": "epistles",
        "boundary_evidence_refs": [
            "observation_substrate:Phlm.1.1",
            "span_kind:chapter_observed_feature_rollup",
            "book_genre:epistles",
        ],
        "strong_or_hebrew_tags_used": False,
        "wj_or_red_letter_considered": False,
        "frontier_flag_considered": False,
        "confidence": "medium",
        "decision_id": "MTEST-PHLM-001",
        "non_authorizing": True,
    }
    row.update(extra)
    return row


def _strategy(folder: Path, book: str = "Phlm") -> None:
    path = folder / "book_strategy" / f"{book}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "strategy: literary marker aware. Strong's metadata considered evidence-only. "
        "Substrate evidence reviewed before fallback.\n"
        "literary_form_decision_matrix: recorded.\n"
        "larger_unit_preservation_check: recorded.\n"
        "list_register_function_check: recorded.\n"
        "epistle_unit_check_if_applicable: recorded.\n"
        "source_metadata_evidence_only_check: recorded.\n"
        "over_split_risk_check: recorded.\n"
        "sidecar_specificity_plan: recorded.\n",
        encoding="utf-8",
    )


def _sidecar_row(decision_id: str = "MTEST-PHLM-001") -> dict:
    return {
        "model_id": "M_TEST",
        "book": "Phlm",
        "span": "Phlm.1.1-Phlm.1.25",
        "chunk_decision_id": decision_id,
        "confidence": "low",
        "concern_type": "chapter_only_fallback",
        "observed_substrate_signals": ["span_kind:chapter_observed_feature_rollup", "pilot_fragile_book"],
        "why_low_confidence": "One-chapter Philemon fallback hides greeting/body/closing structure.",
        "why_frontier_review_needed": "Low-confidence pilot-fragile epistle fallback should be scrutinized.",
        "possible_downstream_risk": "False model agreement on chapter-only epistle structure.",
        "suggested_reviewer": "codex",
        "proposed_atlas_action": "consider_only",
        "non_authorizing": True,
        "promotion_authority": "none",
        "atlas_promotion_authority": "none",
    }


def test_policy_validates() -> None:
    assert validate_policy() == []


def test_chapter_only_pilot_fallback_cannot_stay_medium(tmp_path: Path) -> None:
    folder = tmp_path / "M_TEST"
    _manifest(folder)
    _strategy(folder)
    _write_jsonl(folder / "book_chunks" / "Phlm" / "chunks.jsonl", [_chunk()])

    errors = validate_model_folder(folder, books={"Phlm"}, require_artifacts=True)
    assert any("chapter-only fallback" in error for error in errors)


def test_low_confidence_fallback_requires_and_accepts_sidecars(tmp_path: Path) -> None:
    folder = tmp_path / "M_TEST"
    _manifest(folder)
    _strategy(folder)
    _write_jsonl(folder / "book_chunks" / "Phlm" / "chunks.jsonl", [_chunk(confidence="low")])
    row = _sidecar_row()
    _write_jsonl(folder / "low_confidence_register.jsonl", [row])
    _write_jsonl(folder / "frontier_escalation_queue.jsonl", [row])
    _write_jsonl(folder / "atlas_candidate_feed.jsonl", [row])

    assert validate_model_folder(folder, books={"Phlm"}, require_artifacts=True) == []


def test_whole_psalm_is_not_forced_low_as_a_chapter_fallback(tmp_path: Path) -> None:
    folder = tmp_path / "M_TEST"
    _manifest(folder)
    _strategy(folder, "Ps")
    psalm = _chunk(
        book="Ps",
        span="Ps.1.1-Ps.1.6",
        literature_type_guess="wisdom_psalm",
        literary_form="wisdom_psalm",
        decision_id="MTEST-PS-001",
        confidence="high",
        boundary_evidence_refs=[
            "observation_substrate:Ps.1.1",
            "span_kind:chapter_observed_feature_rollup",
            "canonical_poem_outer_unit",
        ],
    )
    _write_jsonl(folder / "book_chunks" / "Ps" / "chunks.jsonl", [psalm])

    assert validate_model_folder(folder, books={"Ps"}, require_artifacts=True) == []

def test_require_artifacts_enforces_t467_book_strategy_sections(tmp_path: Path) -> None:
    folder = tmp_path / "M_TEST"
    _manifest(folder)
    strategy_path = folder / "book_strategy" / "Phlm.md"
    strategy_path.parent.mkdir(parents=True, exist_ok=True)
    strategy_path.write_text(
        "strategy: literary marker aware. Strong's metadata considered evidence-only.",
        encoding="utf-8",
    )
    _write_jsonl(folder / "book_chunks" / "Phlm" / "chunks.jsonl", [_chunk(confidence="low")])
    row = _sidecar_row()
    _write_jsonl(folder / "low_confidence_register.jsonl", [row])
    _write_jsonl(folder / "frontier_escalation_queue.jsonl", [row])
    _write_jsonl(folder / "atlas_candidate_feed.jsonl", [row])

    errors = validate_model_folder(folder, books={"Phlm"}, require_artifacts=True)
    assert any("missing T467 required section(s)" in error for error in errors)
    assert any("larger_unit_preservation_check" in error for error in errors)


def test_frontier_books_require_frontier_flag(tmp_path: Path) -> None:
    folder = tmp_path / "M_TEST"
    _manifest(folder)
    _strategy(folder, "Dan")
    dan = _chunk(
        book="Dan",
        span="Dan.7.1-Dan.7.28",
        literature_type_guess="apocalyptic",
        decision_id="MTEST-DAN-001",
        confidence="medium",
        boundary_evidence_refs=["observation_substrate:Dan.7.1", "book_genre:prophets"],
    )
    _write_jsonl(folder / "book_chunks" / "Dan" / "chunks.jsonl", [dan])

    errors = validate_model_folder(folder, books={"Dan"}, require_artifacts=True)
    assert any("frontier_flag_considered must be true" in error for error in errors)
