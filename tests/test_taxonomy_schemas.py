"""Tests for the v0.2 taxonomy structural schemas.

Enforces the asserted/inferred/tradition separation structurally (taxonomy-scaffold
v0.2 Patch 8): the ClassificationAssignment schema must REJECT interpretation stored
as a textual fact, and REQUIRE tradition_scope for tradition-dependent axes.

Skips schema-validation assertions cleanly if jsonschema is not installed
(dependency-light default; CI installs the [validate] extra).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

NEW_SCHEMAS = [
    "classification_assignment.schema.json",
    "witness.schema.json",
    "textual_variant.schema.json",
    "lexeme.schema.json",
    "semantic_domain.schema.json",
    "translation_note.schema.json",
    "alignment_record.schema.json",
    "extra_biblical_source.schema.json",
]


def test_new_schemas_are_valid_json():
    for name in NEW_SCHEMAS:
        path = SCHEMAS / name
        assert path.exists(), f"missing schema {name}"
        json.loads(path.read_text(encoding="utf-8"))


def _validator(name):
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def test_extra_biblical_layer_must_be_context():
    jsonschema = pytest.importorskip("jsonschema")
    v = _validator("extra_biblical_source.schema.json")
    bad = {
        "id": "extra:ane:enuma-elish", "type": "ExtraBiblicalSource",
        "label": "Enuma Elish", "source_class": "ane_text",
        "layer": "canonical",  # FORBIDDEN — fence violation
        "trust_zone": "context",
        "provenance": {"created_by": "t", "created_at": "2026-06-04", "basis": "t"},
        "status": "active",
    }
    assert list(v.iter_errors(bad)), "extra-biblical source with layer=canonical must be rejected"


def test_interpretive_axis_cannot_be_asserted_textual():
    jsonschema = pytest.importorskip("jsonschema")
    v = _validator("classification_assignment.schema.json")
    bad = {
        "id": "c1", "type": "ClassificationAssignment", "subject_id": "scripture:Exod.12",
        "axis": "theological_concept", "value": "passover",
        "assertion_mode": "asserted_textual",  # FORBIDDEN on an interpretive axis
        "provenance": {"created_by": "t", "created_at": "2026-06-04", "basis": "t"},
        "evidence": [{"kind": "scripture", "ref": "Exod.12.11"}],
        "status": "active",
    }
    assert list(v.iter_errors(bad)), "interpretive axis marked asserted_textual must be rejected"


def test_doctrine_axis_requires_tradition_scope():
    jsonschema = pytest.importorskip("jsonschema")
    v = _validator("classification_assignment.schema.json")
    bad = {
        "id": "c2", "type": "ClassificationAssignment", "subject_id": "scripture:Rom.3",
        "axis": "doctrine", "value": "justification",
        "assertion_mode": "asserted_curated",
        "evidence": [{"kind": "scripture", "ref": "Rom.3.28"}],
        "provenance": {"created_by": "t", "created_at": "2026-06-04", "basis": "t"},
        "status": "active",
        # tradition_scope intentionally omitted -> must fail
    }
    assert list(v.iter_errors(bad)), "doctrine axis without tradition_scope must be rejected"


def test_valid_interpretive_classification_passes():
    jsonschema = pytest.importorskip("jsonschema")
    v = _validator("classification_assignment.schema.json")
    good = {
        "id": "c3", "type": "ClassificationAssignment", "subject_id": "scripture:Exod.12",
        "axis": "theological_concept", "value": "passover",
        "assertion_mode": "asserted_curated",
        "evidence": [{"kind": "scripture", "ref": "Exod.12.11"}],
        "provenance": {"created_by": "t", "created_at": "2026-06-04", "basis": "t"},
        "status": "active",
    }
    assert not list(v.iter_errors(good)), "a well-formed curated classification should validate"
