from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
    / "validate_v9_static_allowlist_v3_1.py"
)
SPEC = importlib.util.spec_from_file_location("validate_v9_allowlist_v31_test", SCRIPT)
assert SPEC and SPEC.loader
V = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = V
SPEC.loader.exec_module(V)


def objects():
    return (
        V.parse_json_bytes(V.ALLOWLIST.read_bytes(), "allowlist"),
        V.parse_json_bytes(V.PREDECESSOR_ALLOWLIST.read_bytes(), "predecessor"),
        V.parse_json_bytes(V.SOURCE_MANIFEST.read_bytes(), "source"),
    )


def test_exact_v31_static_allowlist_passes_metadata_only() -> None:
    result = V.validate_files()
    assert result == {
        "verdict": "PASS_STATIC_ALLOWLIST_V3_1_ONLY",
        "governed_member_count": 13,
        "replacement_count": 8,
        "guard_only_count": 5,
        "sentinel_count": 3,
        "predecessor_projection_exact": True,
        "source_v6_projection_exact": True,
        "live_measurement_executed": False,
        "canonical_or_global_targets_opened": False,
        "candidate_only": True,
        "non_authorizing": True,
        "allowlist_sha256": V.EXPECTED_ALLOWLIST_SHA256,
        "predecessor_allowlist_sha256": V.EXPECTED_PREDECESSOR_SHA256,
        "source_manifest_sha256": V.EXPECTED_SOURCE_MANIFEST_SHA256,
    }


def test_exact_operation_map_resolves_noop_ambiguity() -> None:
    allowlist, predecessor, source = objects()
    result = V.validate_objects(allowlist, predecessor, source)
    operations = {
        row["ordinal"]: row["operation"] for row in allowlist["targets"]
    }
    assert operations == {
        1: "replace",
        2: "replace",
        3: "replace",
        4: "guard_only",
        5: "replace",
        6: "guard_only",
        7: "replace",
        8: "replace",
        9: "guard_only",
        10: "replace",
        11: "guard_only",
        12: "replace",
        13: "guard_only",
    }
    assert result["replacement_count"] == 8
    assert result["guard_only_count"] == 5


def test_duplicate_json_key_is_rejected_before_semantics() -> None:
    with pytest.raises(V.StaticAllowlistV31Error, match="duplicate JSON key"):
        V.parse_json_bytes(b'{"task_id":"T550","task_id":"other"}', "probe")


def test_nonobject_json_root_is_rejected() -> None:
    with pytest.raises(V.StaticAllowlistV31Error, match="root must be an object"):
        V.parse_json_bytes(b"[]", "probe")


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda a: a.__setitem__("application_family", "other"),
            "identity",
        ),
        (
            lambda a: a["predecessor_allowlist"].__setitem__("path", "other.json"),
            "predecessor reference",
        ),
        (
            lambda a: a["source_render"].__setitem__("generation", "other"),
            "source render",
        ),
        (
            lambda a: a["source_render"].__setitem__(
                "independent_content_pass_sha256", "0" * 64
            ),
            "source render",
        ),
        (
            lambda a: a["normalization"].__setitem__(
                "windows_casefold_uniqueness_required", False
            ),
            "normalization",
        ),
        (
            lambda a: a["governed_counts"].__setitem__("replacement_count", 13),
            "count",
        ),
        (
            lambda a: a["targets"][0].__setitem__("target_id", "other"),
            "descriptor",
        ),
        (
            lambda a: a["targets"][0].__setitem__("role", "other"),
            "descriptor",
        ),
        (
            lambda a: a["sentinels"][0].__setitem__("sentinel_id", "other"),
            "descriptor",
        ),
        (
            lambda a: a["sentinels"][0].__setitem__("role", "other"),
            "descriptor",
        ),
    ],
)
def test_exact_semantic_fields_are_closed_and_pinned(mutation, message) -> None:
    allowlist, predecessor, source = objects()
    mutation(allowlist)
    with pytest.raises(V.StaticAllowlistV31Error, match=message):
        V.validate_objects(allowlist, predecessor, source)


def test_unknown_nested_field_fails_closed() -> None:
    allowlist, predecessor, source = objects()
    allowlist["normalization"]["unknown"] = True
    with pytest.raises(V.StaticAllowlistV31Error, match="schema drift"):
        V.validate_objects(allowlist, predecessor, source)


def test_unknown_target_field_fails_closed() -> None:
    allowlist, predecessor, source = objects()
    allowlist["targets"][0]["unknown"] = True
    with pytest.raises(V.StaticAllowlistV31Error, match="schema drift"):
        V.validate_objects(allowlist, predecessor, source)


def test_guard_only_requires_exactly_unchanged_state() -> None:
    allowlist, predecessor, source = objects()
    allowlist["targets"][3]["staged_sha256"] = "0" * 64
    with pytest.raises(V.StaticAllowlistV31Error, match="guard_only"):
        V.validate_objects(allowlist, predecessor, source)


def test_replace_requires_a_real_state_change() -> None:
    allowlist, predecessor, source = objects()
    row = allowlist["targets"][0]
    row["staged_sha256"] = row["preimage_sha256"]
    row["staged_size_bytes"] = row["preimage_size_bytes"]
    with pytest.raises(V.StaticAllowlistV31Error, match="replace row"):
        V.validate_objects(allowlist, predecessor, source)


def test_operation_assignment_itself_is_exact() -> None:
    allowlist, predecessor, source = objects()
    allowlist["targets"][3]["operation"] = "replace"
    with pytest.raises(V.StaticAllowlistV31Error, match="descriptor"):
        V.validate_objects(allowlist, predecessor, source)


def test_v3_predecessor_projection_drift_fails() -> None:
    allowlist, predecessor, source = objects()
    predecessor["targets"][0]["role"] = "other"
    with pytest.raises(V.StaticAllowlistV31Error, match="predecessor target"):
        V.validate_objects(allowlist, predecessor, source)


def test_v6_source_projection_drift_fails() -> None:
    allowlist, predecessor, source = objects()
    source["targets"][0]["staged_sha256"] = "0" * 64
    with pytest.raises(V.StaticAllowlistV31Error, match="source staged hash"):
        V.validate_objects(allowlist, predecessor, source)


@pytest.mark.parametrize(
    ("path_token", "parent_token", "leaf_name", "message"),
    [
        ("reviews/Hos/file:ads", "reviews/Hos", "file:ads", "unsafe"),
        ("reviews/Hos/NUL.txt", "reviews/Hos", "NUL.txt", "reserved"),
        ("reviews/Hos/file.", "reviews/Hos", "file.", "trailing"),
        ("reviews/Hos/file ", "reviews/Hos", "file ", "trailing"),
        ("reviews/./file", "reviews/.", "file", "dot or empty"),
        ("/absolute/file", "/absolute", "file", "unsafe"),
        ("reviews/Hos/e\u0301.json", "reviews/Hos", "e\u0301.json", "NFC"),
        ("reviews\\Hos\\file", "reviews/Hos", "file", "unsafe"),
    ],
)
def test_windows_path_ambiguities_fail(
    path_token, parent_token, leaf_name, message
) -> None:
    with pytest.raises(V.StaticAllowlistV31Error, match=message):
        V._path_relation(path_token, parent_token, leaf_name)


def test_windows_casefold_collision_fails() -> None:
    with pytest.raises(V.StaticAllowlistV31Error, match="casefold"):
        V._require_unique_windows_keys(["reviews/hos/file.json", "reviews/hos/file.json"])


def test_source_manifest_identity_is_exact() -> None:
    allowlist, predecessor, source = objects()
    source["application_id"] = "other"
    with pytest.raises(V.StaticAllowlistV31Error, match="source V6 identity"):
        V.validate_objects(allowlist, predecessor, source)


def test_only_frozen_metadata_paths_are_inputs() -> None:
    assert {
        V.ALLOWLIST.relative_to(ROOT).as_posix(),
        V.PREDECESSOR_ALLOWLIST.relative_to(ROOT).as_posix(),
        V.SOURCE_MANIFEST.relative_to(ROOT).as_posix(),
    } == {
        ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Hos/v9_static_allowlist_v3_1.json",
        ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Hos/v9_static_allowlist_v3.json",
        (
            ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Hos/"
            "rematerialization_attempts/"
            "T550-HOS-SEMANTIC-PROSE-REMATERIALIZATION-V6-ONE-SHOT/"
            "prepare_manifest_v6.json"
        ),
    }


def test_hash_pins_are_exact() -> None:
    assert V.EXPECTED_ALLOWLIST_SHA256 == (
        "a3e18ac151a4d0fb51afc282874e873f2c3344b5aab858bc5da1d1e2acec4a80"
    )
    assert V.EXPECTED_PREDECESSOR_SHA256 == (
        "ceb51bb9bf51679164390cf07a46c5f3a1d307428355d987a6f4ae5b24bfa4ed"
    )
    assert V.EXPECTED_SOURCE_MANIFEST_SHA256 == (
        "f272661602efa1cab09fe224b6283fb2e0c1e072e9a8b54d0edcd6fa024885c4"
    )
