"""Tests for T310 Increment 1 — deterministic form detector (candidate sidecar only)."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "classification_assignment.schema.json"
CHUNKER = ROOT / "pipelines" / "chunking" / "chunker.py"
FIXTURES = ROOT / "tests" / "fixtures" / "chunking" / "form_detect_units.jsonl"
FORM_REGISTRY = ROOT / "config" / "chunking" / "form_registry.yaml"
MARKER_COVERAGE = ROOT / "config" / "ingest" / "usfm_marker_coverage.yaml"
CANON = ROOT / "data" / "canonical"
TEST_SOURCE_SHA256 = "a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e"
TEST_LICENSE = "public-domain"

PASSAGES = [
    {"id": "scripture:John.1.1", "type": "ScripturePassage", "osis_ref": "John.1.1", "book": "John", "chapter": 1,
     "source_sha256": TEST_SOURCE_SHA256, "license": TEST_LICENSE},
    {"id": "scripture:John.1.2", "type": "ScripturePassage", "osis_ref": "John.1.2", "book": "John", "chapter": 1,
     "source_sha256": TEST_SOURCE_SHA256, "license": TEST_LICENSE},
    {"id": "scripture:John.1.3", "type": "ScripturePassage", "osis_ref": "John.1.3", "book": "John", "chapter": 1,
     "source_sha256": TEST_SOURCE_SHA256, "license": TEST_LICENSE},
]
WITNESSES = [
    {"id": "w1", "type": "TranslationWitness", "passage_id": "scripture:John.1.1",
     "osis_ref": "John.1.1", "text": "In the beginning was the Word.",
     "source_sha256": TEST_SOURCE_SHA256, "license": TEST_LICENSE},
    {"id": "w2", "type": "TranslationWitness", "passage_id": "scripture:John.1.2",
     "osis_ref": "John.1.2", "text": "The same was in the beginning with God.",
     "source_sha256": TEST_SOURCE_SHA256, "license": TEST_LICENSE},
    {"id": "w3", "type": "TranslationWitness", "passage_id": "scripture:John.1.3",
     "osis_ref": "John.1.3", "text": "All things were made through him.",
     "source_sha256": TEST_SOURCE_SHA256, "license": TEST_LICENSE},
]


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def _load_fixture_units():
    units = []
    for line in FIXTURES.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            row["markers"] = set(row["markers"])
            units.append(row)
    return units


def _allowed_markers():
    from pipelines.chunking.detect_form import load_allowed_markers

    return load_allowed_markers(MARKER_COVERAGE)


def _make_record(units, **kwargs):
    from pipelines.chunking.detect_form import (
        aggregate_markers,
        detect_form_for_window,
        detect_overlays,
        load_form_registry,
        make_classification_assignment,
    )

    _, registered = load_form_registry(FORM_REGISTRY)
    registered.add("unknown")
    book_genre = kwargs.get("book_genre", "psalms")
    form_id, score, rule_id, reasons = detect_form_for_window(
        units,
        book_genre=book_genre,
        allowed_markers=_allowed_markers(),
        registered_forms=registered,
        window_kind=kwargs.get("window_kind", "chapter"),
    )
    overlays = detect_overlays(units, kwargs.get("overlay_index"))
    version, _ = load_form_registry(FORM_REGISTRY)
    return make_classification_assignment(
        units,
        form_id=form_id,
        numeric_confidence=score,
        rule_id=rule_id,
        reason_codes=reasons,
        book_genre=book_genre,
        window_kind=kwargs.get("window_kind", "chapter"),
        form_registry_version=version,
        overlays=overlays,
        marker_counts=aggregate_markers(units),
        source_sha256=kwargs.get("source_sha256", TEST_SOURCE_SHA256),
        license=kwargs.get("license", TEST_LICENSE),
    )


def test_detector_emits_valid_classification_assignment():
    units = _load_fixture_units()[:2]
    record = _make_record(units, book_genre="psalms")
    v = _validator()
    errors = list(v.iter_errors(record))
    assert not errors, errors
    assert record["type"] == "ClassificationAssignment"
    assert record["axis"] == "textual_form"
    assert record["assertion_mode"] == "inferred_rule"
    assert record["trust_zone"] == "candidate"
    assert record["status"] == "candidate"
    assert record["source_sha256"] == TEST_SOURCE_SHA256
    assert record["license"] == TEST_LICENSE
    assert record["provenance"]["created_by"]
    assert record["provenance"]["created_at"]
    assert record["provenance"]["basis"]
    assert record["subject_id"] == "span:eng-web:Ps.23.1--Ps.23.2"


def test_unknown_form_fails_closed():
    unit = _load_fixture_units()[3]
    record = _make_record([unit], book_genre="narrative", window_kind="section")
    assert record["value"] == "unknown"
    assert record["confidence"] == "unknown"
    assert "fail_closed" in record["provenance"]["basis"]
    v = _validator()
    assert not list(v.iter_errors(record))


def test_deterministic_form_logic():
    psalm_units = _load_fixture_units()[:2]
    record = _make_record(psalm_units, book_genre="psalms")
    assert record["value"] == "psalm_whole"
    assert record["confidence"] == "high"
    assert "superscription_attached" in record["overlays"]

    sp_unit = _load_fixture_units()[2]
    sp_record = _make_record([sp_unit], book_genre="wisdom", window_kind="section")
    assert sp_record["value"] == "speaker_dialogue"
    assert sp_record["confidence"] == "high"


def test_optional_sidecar_loading(tmp_path):
    from pipelines.chunking.detect_form import build_overlay_index, detect_overlays

    units = _load_fixture_units()[:1]
    assert detect_overlays(units, None) == ["superscription_attached"]

    word_tokens = tmp_path / "word_tokens_sidecar.jsonl"
    word_tokens.write_text(
        json.dumps({"osis_ref": "Ps.23.1", "nesting_context": ["wj"]}) + "\n",
        encoding="utf-8",
    )
    footnotes = tmp_path / "footnotes_sidecar.jsonl"
    footnotes.write_text(
        json.dumps({"osis_ref": "Ps.23.1", "alternate_readings": ["variant text"]}) + "\n",
        encoding="utf-8",
    )
    index = build_overlay_index(word_tokens, footnotes)
    overlays = detect_overlays(units, index)
    assert "words_of_jesus" in overlays
    assert "variant_reading" in overlays
    assert "footnote_carry" in overlays


def test_confidence_enum_mapping():
    from pipelines.chunking.detect_form import numeric_to_confidence_enum

    assert numeric_to_confidence_enum(1.0) == "high"
    assert numeric_to_confidence_enum(0.90) == "high"
    assert numeric_to_confidence_enum(0.75) == "medium"
    assert numeric_to_confidence_enum(0.70) == "medium"
    assert numeric_to_confidence_enum(0.50) == "low"
    assert numeric_to_confidence_enum(0.01) == "low"
    assert numeric_to_confidence_enum(0.0) == "unknown"


def test_no_chunker_output_mutation(tmp_path):
    passages = tmp_path / "passages.jsonl"
    witnesses = tmp_path / "witnesses.jsonl"
    out_before = tmp_path / "chunks_before.jsonl"
    out_after = tmp_path / "chunks_after.jsonl"
    passages.write_text("\n".join(json.dumps(r) for r in PASSAGES) + "\n", encoding="utf-8")
    witnesses.write_text("\n".join(json.dumps(r) for r in WITNESSES) + "\n", encoding="utf-8")

    cmd = [
        sys.executable,
        str(CHUNKER),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
    ]
    subprocess.run([*cmd, str(out_before)], cwd=ROOT, check=True, capture_output=True, text=True)
    import pipelines.chunking.detect_form  # noqa: F401

    subprocess.run([*cmd, str(out_after)], cwd=ROOT, check=True, capture_output=True, text=True)
    h1 = hashlib.sha256(out_before.read_bytes()).hexdigest()
    h2 = hashlib.sha256(out_after.read_bytes()).hexdigest()
    assert h1 == h2


def test_no_canonical_mutation(tmp_path):
    from pipelines.chunking.detect_form import write_classifications

    units = _load_fixture_units()[:2]
    record = _make_record(units, book_genre="psalms")
    out = tmp_path / "candidate" / "chunking" / "form_assignments" / "test.jsonl"
    count = write_classifications(iter([record]), out)
    assert count == 1
    assert str(out).startswith(str(tmp_path))
    assert not str(out).startswith(str(CANON.resolve()))


def test_cli_candidate_jsonl_passes_existing_jsonl_validator(tmp_path):
    passages = tmp_path / "passages.jsonl"
    witnesses = tmp_path / "witnesses.jsonl"
    boundary_claims = tmp_path / "boundary_claims.jsonl"
    out = tmp_path / "candidate" / "chunking" / "form_assignments" / "test.jsonl"
    passages.write_text("\n".join(json.dumps(r) for r in PASSAGES) + "\n", encoding="utf-8")
    witnesses.write_text("\n".join(json.dumps(r) for r in WITNESSES) + "\n", encoding="utf-8")
    boundary_claims.write_text("", encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "chunking" / "emit_form_assignments.py"),
            "--passages",
            str(passages),
            "--witnesses",
            str(witnesses),
            "--boundary-claims",
            str(boundary_claims),
            "--out",
            str(out),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_jsonl.py"), str(out)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_sp_splits_window():
    from pipelines.chunking.detect_form import detect_forms_for_corpus, load_form_registry

    units = _load_fixture_units()
    sp = units[2]
    prose = {
        **units[3],
        "osis_ref": "Job.3.2",
        "passage_id": "scripture:Job.3.2",
        "book": "Job",
        "chapter": 3,
        "markers": {"p"},
        "has_paragraph": True,
        "is_poetry": False,
    }
    version, registered = load_form_registry(FORM_REGISTRY)
    registered.add("unknown")
    records = list(
        detect_forms_for_corpus(
            [prose, sp],
            genres={"Job": "wisdom"},
            default_genre="narrative",
            allowed_markers=_allowed_markers(),
            registered_forms=registered,
            form_registry_version=version,
            overlay_index=None,
            source_metadata={"source_sha256": TEST_SOURCE_SHA256, "license": TEST_LICENSE},
        )
    )
    values = {r["value"] for r in records}
    assert "speaker_dialogue" in values
