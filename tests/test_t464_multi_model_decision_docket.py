"""Tests for T464 multi-model comparison decision docket validation."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts import validate_t464_multi_model_decision_docket as validator
from scripts.compare_multi_model_bible_chunk_maps import compare_models


ACTIVE_MODELS = [
    "M1_cursor",
    "M2_claude_sonnet5",
    "M3_claude_frontier",
    "M4_codex_gpt55",
    "M5_gemini_thinking",
    "M6_fable5",
]


def _base_matrix() -> dict:
    return {
        "models_compared": ACTIVE_MODELS,
        "complete_model_count": 6,
        "books_compared": validator.canonical_books(),
    }


def _base_docket(*, agreement_id: str = "AGREE-Phlm-00001", delta_id: str = "DELTA-Phlm-001") -> dict:
    return {
        "statuses": {
            "consensus_low_risk_candidate": [
                {
                    "source_id": agreement_id,
                    "source_ledger": "agreement_chunks.jsonl",
                    "non_authorizing": True,
                    "promotion_authority": "none",
                }
            ],
            "codex_fable_recommended_candidate": [
                {
                    "source_id": delta_id,
                    "source_ledger": "disagreement_delta.jsonl",
                    "non_authorizing": True,
                    "promotion_authority": "none",
                }
            ],
        }
    }


def _valid_agreement() -> dict:
    return {
        "agreement_id": "AGREE-Phlm-00001",
        "book": "Phlm",
        "span": "Phlm.1.1-Phlm.1.7",
        "models_agreeing": ACTIVE_MODELS,
        "docket_status": "consensus_low_risk_candidate",
        "requires_frontier_review": False,
        "non_authorizing": True,
        "promotion_authority": "none",
    }


def _valid_delta() -> dict:
    return {
        "delta_id": "DELTA-Phlm-001",
        "book": "Phlm",
        "region": "Phlm.1.1-Phlm.1.7",
        "models": {
            "M4_codex_gpt55": "Phlm.1.1-Phlm.1.7",
            "M6_fable5": "Phlm.1.1-Phlm.1.7",
        },
        "recommended_candidate_basis": "codex_fable_alignment",
        "docket_status": "codex_fable_recommended_candidate",
        "decision_route": "codex_fable_recommended_candidate",
        "requires_frontier_review": False,
        "non_authorizing": True,
        "promotion_authority": "none",
    }


def _chunk(model_id: str, book: str, idx: int, span: str, **extra: object) -> dict:
    row = {
        "model_id": model_id,
        "book": book,
        "span": span,
        "chunk_index_in_book": idx,
        "literature_type_guess": "gospel_ending",
        "boundary_evidence_refs": ["observation_substrate", "variant_sensitive"],
        "strong_or_hebrew_tags_used": False,
        "wj_or_red_letter_considered": False,
        "frontier_flag_considered": False,
        "confidence": "medium",
        "decision_id": f"{model_id}-{book}-{idx:03d}",
        "non_authorizing": True,
    }
    row.update(extra)
    return row


def _write_map(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def _write_manifest(folder: Path, model_id: str, *, books: list[str]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "model_manifest.yaml").write_text(
        yaml.safe_dump({"model_id": model_id, "research_baseline_read": True}),
        encoding="utf-8",
    )
    (folder / "marathon_progress.yaml").write_text(
        yaml.safe_dump(
            {
                "model_id": model_id,
                "marathon_status": "complete",
                "books_completed": 66,
                "books_total": 66,
                "book_completion": {book: {"status": "complete"} for book in books},
            }
        ),
        encoding="utf-8",
    )


def _validate_case(agreement: dict | None = None, delta: dict | None = None, docket: dict | None = None) -> list[str]:
    errors: list[str] = []
    validator._validate_outputs(
        active_models=ACTIVE_MODELS,
        agreements=[agreement or _valid_agreement()],
        deltas=[delta or _valid_delta()],
        matrix=_base_matrix(),
        docket=docket or _base_docket(),
        frontier_rows=[],
        errors=errors,
    )
    return errors


def test_valid_t464_outputs_pass_focused_validation() -> None:
    assert _validate_case() == []


def test_agreement_ledger_must_remain_non_authorizing() -> None:
    agreement = _valid_agreement()
    agreement["promotion_authority"] = "reviewed_gold"
    errors = _validate_case(agreement=agreement)
    assert any("promotion_authority must be none" in error for error in errors)


def test_m4_m6_alignment_must_be_marked_as_codex_fable_basis() -> None:
    delta = _valid_delta()
    delta["recommended_candidate_basis"] = "none"
    errors = _validate_case(delta=delta)
    assert any("M4/M6 agreement must be marked codex_fable_alignment" in error for error in errors)


def test_frontier_required_delta_cannot_bypass_frontier_status() -> None:
    delta = _valid_delta()
    delta["requires_frontier_review"] = True
    errors = _validate_case(delta=delta)
    assert any("frontier-required delta must route to frontier_review_required" in error for error in errors)


def test_stale_model_ids_are_rejected_in_delta_rows() -> None:
    delta = _valid_delta()
    delta["models"]["M2_codex"] = "Phlm.1.1-Phlm.1.7"
    errors = _validate_case(delta=delta)
    assert any("inactive model id" in error for error in errors)


def test_variant_hot_zone_agreement_routes_to_frontier() -> None:
    agreement = _valid_agreement()
    agreement["risk_flags"] = ["variant_hot_zone"]
    agreement["docket_status"] = "consensus_low_risk_candidate"
    agreement["requires_frontier_review"] = False
    errors = _validate_case(agreement=agreement)
    assert any("variant hot zone must route" in error for error in errors)


def test_mark_16_consensus_is_frontier_not_easy(tmp_path) -> None:
    folders = []
    for model_id in ACTIVE_MODELS:
        folder = tmp_path / model_id
        _write_manifest(folder, model_id, books=["Mark"])
        _write_map(
            folder / "whole_bible_chunk_map.jsonl",
            [_chunk(model_id, "Mark", 1, "Mark.16.9-Mark.16.20", confidence="high")],
        )
        folders.append(folder)

    result = compare_models(folders, books=["Mark"], allow_easy_at_n3=False)
    assert result["agreements"]
    row = result["agreements"][0]
    assert "variant_hot_zone" in row["risk_flags"]
    assert row["requires_frontier_review"] is True
    assert row["docket_status"] == "frontier_review_required"
    assert "codex_vaticanus_layout_review" in row["expert_review_lanes"]
    assert "codex_sinaiticus_ending_review" in row["expert_review_lanes"]
    assert "scribal_layout_and_blank_space_review" in row["expert_review_lanes"]
    assert "scribal_letters_per_column_capacity_review" in row["expert_review_lanes"]
