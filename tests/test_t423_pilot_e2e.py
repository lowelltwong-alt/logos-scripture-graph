"""End-to-end T423 pilot dry-run: book_chunks → merge → compare → revert signal."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.compare_multi_model_bible_chunk_maps import compare_models
from scripts.evaluate_t423_revert_signal import evaluate
from scripts.t423_chunk_map_utils import book_chunk_file, load_fork_policy
from scripts.t423_merge_book_chunks import merge_book_chunks, write_merged_map
from scripts.t423_resume_book import mark_book_complete
from tests.test_t423_chunk_map_compare import _chunk, _write_map


def _write_book_chunks(folder: Path, model_id: str, book: str, rows: list[dict]) -> None:
    path = book_chunk_file(folder, book)
    _write_map(path, rows)


def _setup_model(folder: Path, model_id: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "model_manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "model_id": model_id,
                "research_baseline_read": True,
                "observation_substrate_scan_sha256": "test-fixture",
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
    (folder / "marathon_progress.yaml").write_text(
        yaml.safe_dump(
            {
                "model_id": model_id,
                "marathon_status": "in_progress",
                "books_completed": 0,
                "books_total": 66,
                "book_completion": {},
            }
        ),
        encoding="utf-8",
    )
    strategy_dir = folder / "book_strategy"
    strategy_dir.mkdir(parents=True, exist_ok=True)
    for book in ("Phlm", "Jude"):
        (strategy_dir / f"{book}.md").write_text(
            "strategy: literary marker aware fixture. Strong's metadata considered evidence-only. "
            "Substrate evidence reviewed.\n"
            "literary_form_decision_matrix: fixture.\n"
            "larger_unit_preservation_check: fixture.\n"
            "list_register_function_check: fixture.\n"
            "epistle_unit_check_if_applicable: fixture.\n"
            "source_metadata_evidence_only_check: fixture.\n"
            "over_split_risk_check: fixture.\n"
            "sidecar_specificity_plan: fixture.\n",
            encoding="utf-8",
        )


def test_pilot_e2e_book_chunks_merge_compare_revert(tmp_path: Path) -> None:
    """Synthetic 2-model pilot over Phlm + Jude through full toolchain."""
    m1 = tmp_path / "M1_cursor"
    m2 = tmp_path / "M2_claude_sonnet5"
    _setup_model(m1, "M1_cursor")
    _setup_model(m2, "M2_claude_sonnet5")

    _write_book_chunks(
        m1,
        "M1_cursor",
        "Phlm",
        [
            _chunk("M1_cursor", "Phlm", 1, "Phlm.1.1-Phlm.1.7"),
            _chunk("M1_cursor", "Phlm", 2, "Phlm.1.8-Phlm.1.25"),
        ],
    )
    _write_book_chunks(
        m2,
        "M2_claude_sonnet5",
        "Phlm",
        [
            _chunk("M2_claude_sonnet5", "Phlm", 1, "Phlm.1.1-Phlm.1.3"),
            _chunk("M2_claude_sonnet5", "Phlm", 2, "Phlm.1.4-Phlm.1.25"),
        ],
    )
    _write_book_chunks(
        m1,
        "M1_cursor",
        "Jude",
        [_chunk("M1_cursor", "Jude", 1, "Jude.1.1-Jude.1.2")],
    )
    _write_book_chunks(
        m2,
        "M2_claude_sonnet5",
        "Jude",
        [_chunk("M2_claude_sonnet5", "Jude", 1, "Jude.1.1-Jude.1.2")],
    )

    for folder, book in [(m1, "Phlm"), (m1, "Jude"), (m2, "Phlm"), (m2, "Jude")]:
        assert mark_book_complete(folder, book) == []

    for folder in (m1, m2):
        rows, errors = merge_book_chunks(folder)
        assert not errors
        write_merged_map(folder, rows)

    result = compare_models([m1, m2], books=["Phlm", "Jude"], allow_easy_at_n3=True)
    assert result["overall_verse_coverage_agreement_rate"] > 0
    assert any(d["book"] == "Phlm" for d in result["deltas"])
    assert any(a["book"] == "Jude" for a in result["agreements"])

    matrix = {
        "overall_verse_coverage_agreement_rate": result["overall_verse_coverage_agreement_rate"],
        "per_book": result["per_book_stats"],
        "false_consensus_warnings": result["false_consensus_warnings"],
    }
    policy = load_fork_policy()
    pilot_eval = evaluate(matrix=matrix, policy=policy, pilot_only=True)
    assert pilot_eval["metric"] == "verse_coverage_agreement_rate"
    assert "verdict" in pilot_eval


def test_mark_complete_repairs_progress_manifest_and_preserves_metadata(tmp_path: Path) -> None:
    folder = tmp_path / "M7_sol"
    _setup_model(folder, "M7_sol")
    progress_path = folder / "marathon_progress.yaml"
    progress = yaml.safe_load(progress_path.read_text(encoding="utf-8"))
    progress["books_completed"] = 1
    progress["book_completion"] = {
        "Gen": {"status": "complete", "chunks": 82, "held_decisions": 1},
        "Exod": {"status": "candidate_complete_with_explicit_holds", "chunks": 67},
    }
    progress_path.write_text(yaml.safe_dump(progress, sort_keys=False), encoding="utf-8")
    manifest_path = folder / "model_manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest.update({"status": "marathon_in_progress_leviticus_complete_with_hold", "books_completed": 1})
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    assert mark_book_complete(folder, "Exod", skip_validate=True) == []

    repaired_progress = yaml.safe_load(progress_path.read_text(encoding="utf-8"))
    repaired_manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    assert repaired_progress["books_completed"] == 2
    assert repaired_progress["book_completion"]["Gen"]["chunks"] == 82
    assert repaired_progress["book_completion"]["Gen"]["held_decisions"] == 1
    assert repaired_progress["book_completion"]["Exod"]["chunks"] == 67
    assert repaired_progress["book_completion"]["Exod"]["status"] == "complete"
    assert repaired_manifest["status"] == "marathon_in_progress"
    assert repaired_manifest["books_completed"] == 2
    assert repaired_manifest["current_book"] == "Lev"


def test_segmented_disagreement_regions() -> None:
    """Two disagreement pockets in one book produce two deltas, not one over-wide region."""
    from scripts.t423_chunk_map_utils import VerseRef, compare_book_verse_coverage

    verse_keys = [VerseRef("Gen", 1, v) for v in range(1, 11)] + [VerseRef("Gen", 49, v) for v in range(1, 4)]
    chunks_m1 = [
        _chunk("M1", "Gen", 1, "Gen.1.1-Gen.1.5"),
        _chunk("M1", "Gen", 2, "Gen.1.6-Gen.1.10"),
        _chunk("M1", "Gen", 3, "Gen.49.1-Gen.49.3"),
    ]
    chunks_m2 = [
        _chunk("M2", "Gen", 1, "Gen.1.1-Gen.1.3"),
        _chunk("M2", "Gen", 2, "Gen.1.4-Gen.1.10"),
        _chunk("M2", "Gen", 3, "Gen.49.1-Gen.49.1"),
        _chunk("M2", "Gen", 4, "Gen.49.2-Gen.49.3"),
    ]

    def fake_load(book: str, **kwargs):  # noqa: ANN003
        if book == "Gen":
            return verse_keys
        return []

    import scripts.t423_chunk_map_utils as utils

    original = utils.load_book_verse_keys
    utils.load_book_verse_keys = fake_load
    try:
        result = compare_book_verse_coverage(
            {"M1": chunks_m1, "M2": chunks_m2},
            "Gen",
            ["M1", "M2"],
            allow_easy_at_n3=True,
        )
    finally:
        utils.load_book_verse_keys = original

    boundary_deltas = [d for d in result.boundary_deltas if d.get("delta_kind") != "coverage_gap"]
    assert len(boundary_deltas) >= 2
    regions = [d["region"] for d in boundary_deltas]
    assert not any("Gen.1.10-Gen.49" in r for r in regions)
