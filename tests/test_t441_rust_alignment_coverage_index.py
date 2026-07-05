from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts import validate_t441_rust_alignment_coverage_index as validator


ROOT = Path(__file__).resolve().parents[1]


def test_t441_contract_validates_current_repo() -> None:
    validator.validate_contract()


def test_t441_rejects_authority_true() -> None:
    row = {
        "authority": {"authorizes_word_level_alignment_truth": True},
        "text_storage_policy": {
            "no_text": True,
            "stores_source_text": False,
            "stores_translation_text": False,
            "stores_manuscript_transcription": False,
            "stores_manuscript_image": False,
        },
    }

    with pytest.raises(validator.T441ValidationError, match="authorizes_word_level_alignment_truth"):
        validator._require_authority_false(row, "row")


def test_t441_rejects_visible_greek_or_hebrew_text() -> None:
    row = {"note": "\u05d9\u05d5\u05e0\u05d4"}

    with pytest.raises(validator.T441ValidationError, match="Greek/Hebrew"):
        validator._reject_text_leak(row, "row")


def test_t441_rejects_metadata_value_hash_keys() -> None:
    row = {"lemma_value_hash": "abc123"}

    with pytest.raises(validator.T441ValidationError, match="lemma_value_hash"):
        validator._reject_text_leak(row, "row")


def test_t441_rejects_count_parity_authority_in_generated_rows(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir()
    source_rows = [
        _source_row("sblgnt", "Phlm", ref_count=25, source_token_count=334, alignment_record_count=25),
        _source_row(
            "openscriptures_oshb",
            "Jonah",
            ref_count=48,
            source_token_count=688,
            lemma_attr_count=688,
            morph_attr_count=688,
        ),
        _source_row("tanach_us_uxlc", "Jonah", ref_count=48, source_token_count=688),
    ]
    coverage_rows = [_phlm_coverage_row(index) for index in range(1, 26)]
    coverage_rows += [
        _jonah_coverage_row("openscriptures_oshb", index) for index in range(1, 49)
    ]
    coverage_rows += [_jonah_coverage_row("tanach_us_uxlc", index) for index in range(1, 49)]
    coverage_rows[-1]["count_parity_is_semantic_authority"] = True
    guardrail_rows = [_guardrail_row(guardrail_id) for guardrail_id in validator.EXPECTED_NEGATIVE_FIXTURES]
    required_guardrails = {
        "no_visible_biblical_text",
        "generated_build_outputs_only",
        "python_authority_validator",
        "t439_bridge_low_confidence",
        "count_parity_not_semantic_parity",
        "oshb_lemma_lookup_hint_only",
        "oshb_morph_metadata_only",
        "no_production_roots_opened",
        "t440_negative_fixtures_carried_forward",
    }
    guardrail_rows = [_guardrail_row(item) for item in sorted(required_guardrails)]
    negative = {
        "object_type": "t441_negative_fixture_summary",
        "task_id": "T441",
        "negative_fixture_ids": sorted(validator.EXPECTED_NEGATIVE_FIXTURES),
        "negative_fixture_count": len(validator.EXPECTED_NEGATIVE_FIXTURES),
        **_common(),
    }
    manifest = {
        "object_type": "t441_rust_alignment_coverage_manifest",
        "task_id": "T441",
        "no_authority": True,
        "no_text": True,
        "evidence_mode": "deterministic_no_text_coverage_index",
        "coverage_scope": {
            "philemon_refs": 25,
            "philemon_source_tokens": 334,
            "philemon_alignment_records": 25,
            "philemon_editorial_layers": 98,
            "jonah_sources": ["openscriptures_oshb", "tanach_us_uxlc"],
            "jonah_refs_per_source": 48,
            "jonah_tokens_all_sources": 1376,
            "count_parity_is_semantic_authority": False,
        },
        "output_files": sorted(validator.EXPECTED_OUTPUT_FILES),
        "row_counts": {
            "source_ref_coverage": 3,
            "alignment_coverage_index": 121,
            "semantic_guardrail_index": 9,
            "negative_fixture_summary": 9,
        },
        **_common(),
    }
    _write_json(out / "coverage_manifest.json", manifest)
    _write_jsonl(out / "source_ref_coverage.jsonl", source_rows)
    _write_jsonl(out / "alignment_coverage_index.jsonl", coverage_rows)
    _write_jsonl(out / "semantic_guardrail_index.jsonl", guardrail_rows)
    _write_json(out / "negative_fixture_summary.json", negative)

    with pytest.raises(validator.T441ValidationError, match="count parity"):
        validator.validate_generated(out)


def test_t441_validate_all_uses_contract_mode_only() -> None:
    text = (ROOT / "scripts" / "validate_all.py").read_text(encoding="utf-8")

    assert "validate_t441_rust_alignment_coverage_index.py" in text
    assert "t441_alignment_coverage" not in text


def _common() -> dict[str, object]:
    return {
        "schema_version": "t441_rust_alignment_coverage_index.v1",
        "trust_zone": "candidate",
        "status": "coverage_shadow",
        "authority": {
            "authorizes_source_language_truth": False,
            "authorizes_lexical_truth": False,
            "authorizes_word_level_alignment_truth": False,
            "authorizes_strongs_as_source_text": False,
            "authorizes_lemma_or_morphology_population": False,
            "authorizes_preferred_reading": False,
            "authorizes_source_tradition_preference": False,
            "authorizes_textual_critical_decision": False,
            "authorizes_manuscript_witness_support": False,
            "authorizes_canon_scope_change": False,
            "authorizes_translation_judgment": False,
            "authorizes_chunk_boundary": False,
            "authorizes_reviewed_gold": False,
            "authorizes_chunk_output": False,
            "authorizes_route_behavior": False,
            "authorizes_evaluator_behavior": False,
            "authorizes_graph_or_retrieval_truth": False,
            "authorizes_embeddings_or_indexes": False,
            "authorizes_theology_authority": False,
        },
        "text_storage_policy": {
            "no_text": True,
            "stores_source_text": False,
            "stores_translation_text": False,
            "stores_manuscript_transcription": False,
            "stores_manuscript_image": False,
        },
    }


def _source_row(
    source_id: str,
    book_id: str,
    *,
    ref_count: int,
    source_token_count: int,
    alignment_record_count: int | None = None,
    lemma_attr_count: int = 0,
    morph_attr_count: int = 0,
) -> dict[str, object]:
    row = {
        "id": f"t441:source-ref-coverage:{source_id}:{book_id}",
        "type": "T441SourceRefCoverage",
        "task_id": "T441",
        "source_id": source_id,
        "book_id": book_id,
        "source_view_path": f"data/candidate/original_language_evidence/canonical_source_views/{source_id}/files/{book_id}.xml",
        "ref_count": ref_count,
        "source_token_count": source_token_count,
        "lemma_attr_count": lemma_attr_count,
        "morph_attr_count": morph_attr_count,
        "strong_attr_count": 0,
        **_common(),
    }
    if alignment_record_count is not None:
        row["alignment_record_count"] = alignment_record_count
    return row


def _phlm_coverage_row(index: int) -> dict[str, object]:
    return {
        "id": f"t441:alignment-coverage:sblgnt-eng-web:Phlm.1.{index}",
        "type": "T441AlignmentCoverageObservation",
        "task_id": "T441",
        "book_id": "Phlm",
        "osis_ref": f"Phlm.1.{index}",
        "source_id": "sblgnt",
        "confidence": "low",
        "review_status": "unreviewed",
        "word_level_alignment_truth": False,
        "translation_judgment": False,
        "translation_side_strong_hints_are_source_text": False,
        **_common(),
    }


def _jonah_coverage_row(source_id: str, index: int) -> dict[str, object]:
    return {
        "id": f"t441:alignment-coverage:{source_id}:Jonah.1.{index}",
        "type": "T441AlignmentCoverageObservation",
        "task_id": "T441",
        "book_id": "Jonah",
        "osis_ref": f"Jonah.1.{index}",
        "source_id": source_id,
        "word_level_alignment_truth": False,
        "translation_judgment": False,
        "count_parity_is_semantic_authority": False,
        "preferred_source_tradition": False,
        **_common(),
    }


def _guardrail_row(guardrail_id: str) -> dict[str, object]:
    return {
        "id": f"t441:semantic-guardrail:{guardrail_id}",
        "type": "T441SemanticGuardrail",
        "task_id": "T441",
        "guardrail_id": guardrail_id,
        **_common(),
    }


def _write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("\n".join(json.dumps(copy.deepcopy(row)) for row in rows) + "\n", encoding="utf-8")
