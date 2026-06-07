from __future__ import annotations

import copy
import json
from pathlib import Path

from scripts.validate_chunking_gold import ROOT, validate_manifest


PSALMS_MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "psalms_gold_manifest.json"


def _base_manifest() -> dict:
    return json.loads(PSALMS_MANIFEST.read_text(encoding="utf-8"))


def _write_manifest(tmp_path: Path, manifest: dict) -> Path:
    path = tmp_path / "test_manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def test_current_psalms_gold_manifest_validates() -> None:
    assert validate_manifest(PSALMS_MANIFEST) == []


def test_reviewed_case_requires_explicit_status(tmp_path: Path) -> None:
    manifest = _base_manifest()
    del manifest["reviewed_gold"][0]["status"]

    failures = validate_manifest(_write_manifest(tmp_path, manifest))

    assert any("explicit status is required" in failure for failure in failures)


def test_pending_case_cannot_live_under_reviewed_gold(tmp_path: Path) -> None:
    manifest = _base_manifest()
    manifest["reviewed_gold"][0]["status"] = "pending_human_review"

    failures = validate_manifest(_write_manifest(tmp_path, manifest))

    assert any("cannot live under reviewed_gold" in failure for failure in failures)


def test_characterization_case_cannot_carry_promoted_flags(tmp_path: Path) -> None:
    manifest = _base_manifest()
    case = copy.deepcopy(manifest["reviewed_gold"][-1])
    case["status"] = "characterization_only"
    manifest["reviewed_gold"] = []
    manifest["characterization_only"] = [case]

    failures = validate_manifest(_write_manifest(tmp_path, manifest))

    assert any("must not carry promoted-output flags" in failure for failure in failures)


def test_approved_structural_split_requires_parent_and_children(tmp_path: Path) -> None:
    manifest = _base_manifest()
    case = manifest["reviewed_gold"][-1]
    del case["parent_literary_unit"]
    case["expected"]["child_chunks"] = []

    failures = validate_manifest(_write_manifest(tmp_path, manifest))

    assert any("parent_literary_unit must be an object" in failure for failure in failures)
    assert any("expected.child_chunks must be a non-empty list" in failure for failure in failures)
