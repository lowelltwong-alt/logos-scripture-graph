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


def _reviewed_case(manifest: dict, case_id: str) -> dict:
    for case in manifest["reviewed_gold"]:
        if case["case_id"] == case_id:
            return case
    raise AssertionError(f"missing reviewed case {case_id}")


def test_current_psalms_gold_manifest_validates() -> None:
    assert validate_manifest(PSALMS_MANIFEST) == []


def test_pending_psalm_cases_are_non_authorizing_and_ps89_is_promoted() -> None:
    manifest = _base_manifest()
    pending_cases = {
        case["case_id"]: case
        for case in manifest["characterization_only"]
        if case["case_id"] in {
            "ps136_refrain_litany_pending_review",
        }
    }

    assert set(pending_cases) == {"ps136_refrain_litany_pending_review"}
    for case in pending_cases.values():
        assert case["status"] == "pending_human_review"
        assert case["implementation_allowed"] is False
        assert case["output_change_authorized"] is False
        assert "PrMan" not in json.dumps(case)
        assert "Ps151" not in json.dumps(case)

    ps89 = _reviewed_case(manifest, "ps89_owner_decision_option_c")
    assert ps89["status"] == "approved_structural_split_under_parent_whole_psalm"
    assert ps89["owner_decision"]["implementation_allowed"] is True
    assert ps89["owner_decision"]["output_change_authorized"] is True
    assert ps89["owner_decision"]["reviewed_gold_promoted"] is True
    assert ps89["expected"]["child_chunks"][-1]["osis_start"] == "Ps.89.49"
    assert ps89["expected"]["child_chunks"][-1]["osis_end"] == "Ps.89.52"
    assert ps89["expected"]["child_chunks"][-1]["book_iii_doxology_ref"] == "Ps.89.52"


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
    case = copy.deepcopy(_reviewed_case(manifest, "ps78_parent_child_structural_split"))
    case["status"] = "characterization_only"
    manifest["reviewed_gold"] = []
    manifest["characterization_only"] = [case]

    failures = validate_manifest(_write_manifest(tmp_path, manifest))

    assert any("must not carry promoted-output flags" in failure for failure in failures)


def test_approved_structural_split_requires_parent_and_children(tmp_path: Path) -> None:
    manifest = _base_manifest()
    case = _reviewed_case(manifest, "ps78_parent_child_structural_split")
    del case["parent_literary_unit"]
    case["expected"]["child_chunks"] = []

    failures = validate_manifest(_write_manifest(tmp_path, manifest))

    assert any("parent_literary_unit must be an object" in failure for failure in failures)
    assert any("expected.child_chunks must be a non-empty list" in failure for failure in failures)
