from __future__ import annotations

import copy
import importlib.util
import inspect
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
    / "validate_v9_static_allowlist_v3_2.py"
)
SPEC = importlib.util.spec_from_file_location(
    "validate_v9_allowlist_v32_test", SCRIPT
)
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


def _changed(value):
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return "0" * 64 if len(value) == 64 and value != "0" * 64 else value + "-drift"
    raise AssertionError(f"unsupported bounded mutation value: {value!r}")


def test_zero_argument_fixed_validator_reports_exact_open_scope():
    assert tuple(inspect.signature(V.validate_files).parameters) == ()
    result = V.validate_files()
    assert result["verdict"] == "PASS_STATIC_ALLOWLIST_V3_2_VALIDATOR_ONLY"
    assert result["validation_input_mode"] == (
        "zero_argument_fixed_three_pinned_paths"
    )
    assert result["opened_path_count"] == 3
    assert result["caller_path_injection_available"] is False
    assert result["metadata_or_cloud_zero_effect_claimed"] is False
    assert [row["artifact_id"] for row in result["opened_inputs"]] == [
        "v3_1_allowlist",
        "v3_predecessor_allowlist",
        "v6_source_manifest",
    ]
    assert {
        row["declared_path"] for row in result["opened_inputs"]
    } == {
        V.ALLOWLIST.relative_to(ROOT).as_posix(),
        V.PREDECESSOR_ALLOWLIST.relative_to(ROOT).as_posix(),
        V.SOURCE_MANIFEST.relative_to(ROOT).as_posix(),
    }
    assert all(
        row["access_metadata_effect"] == "unmeasured_may_change"
        and row["cloud_hydration_effect"] == "unmeasured_may_change"
        and row["path_identity_reparse_hardlink_status"] == "unmeasured"
        for row in result["opened_inputs"]
    )
    assert result["runtime_code_dependency"] == {
        "declared_path": V._V31_PATH.relative_to(ROOT).as_posix(),
        "expected_and_observed_sha256": V._EXPECTED_V31_DEPENDENCY_SHA256,
        "counted_as_metadata_input": False,
        "access_metadata_effect": "unmeasured_may_change",
        "cloud_hydration_effect": "unmeasured_may_change",
    }


def test_object_injection_is_the_only_test_seam_and_opens_no_files(monkeypatch):
    allowlist, predecessor, source = objects()

    def forbidden_read(_self):
        raise AssertionError("object validation attempted filesystem access")

    monkeypatch.setattr(Path, "read_bytes", forbidden_read)
    result = V.validate_objects(allowlist, predecessor, source)
    assert result["validation_input_mode"] == (
        "object_injection_no_filesystem_access"
    )


def test_validate_files_rejects_all_arguments():
    with pytest.raises(TypeError):
        V.validate_files(V.ALLOWLIST)
    with pytest.raises(TypeError):
        V.validate_files(allowlist_path=V.ALLOWLIST)


@pytest.mark.parametrize(
    "key",
    [
        "schema_version",
        "task_id",
        "book",
        "application_family",
        "file_identity_rows_deferred_to_post_static_execution_freeze",
        "live_measurement_executed",
        "candidate_only",
        "non_authorizing",
    ],
)
def test_every_scalar_top_level_field_is_pinned(key):
    allowlist, predecessor, source = objects()
    allowlist[key] = _changed(allowlist[key])
    with pytest.raises(V.StaticAllowlistV32Error):
        V.validate_objects(allowlist, predecessor, source)


@pytest.mark.parametrize(
    "container",
    ["predecessor_allowlist", "source_render", "normalization", "governed_counts"],
)
def test_every_closed_nested_field_is_pinned(container):
    allowlist, predecessor, source = objects()
    for key in tuple(allowlist[container]):
        candidate = copy.deepcopy(allowlist)
        candidate[container][key] = _changed(candidate[container][key])
        with pytest.raises(V.StaticAllowlistV32Error):
            V.validate_objects(candidate, predecessor, source)


@pytest.mark.parametrize("index", range(13))
@pytest.mark.parametrize(
    "key",
    [
        "ordinal",
        "target_id",
        "role",
        "operation",
        "path_token",
        "parent_token",
        "leaf_name",
        "preimage_sha256",
        "preimage_size_bytes",
        "staged_sha256",
        "staged_size_bytes",
    ],
)
def test_every_field_of_every_target_is_semantically_bound(index, key):
    allowlist, predecessor, source = objects()
    allowlist["targets"][index][key] = _changed(
        allowlist["targets"][index][key]
    )
    with pytest.raises(V.StaticAllowlistV32Error):
        V.validate_objects(allowlist, predecessor, source)


@pytest.mark.parametrize("index", range(3))
@pytest.mark.parametrize(
    "key",
    [
        "ordinal",
        "sentinel_id",
        "role",
        "path_token",
        "parent_token",
        "leaf_name",
        "expected_sha256",
    ],
)
def test_every_field_of_every_sentinel_is_semantically_bound(index, key):
    allowlist, predecessor, source = objects()
    allowlist["sentinels"][index][key] = _changed(
        allowlist["sentinels"][index][key]
    )
    with pytest.raises(V.StaticAllowlistV32Error):
        V.validate_objects(allowlist, predecessor, source)


@pytest.mark.parametrize(
    ("section", "index"),
    [("targets", 0), ("sentinels", 0)],
)
def test_unknown_row_fields_fail_closed(section, index):
    allowlist, predecessor, source = objects()
    allowlist[section][index]["unknown"] = True
    with pytest.raises(V.StaticAllowlistV32Error, match="schema drift"):
        V.validate_objects(allowlist, predecessor, source)


def test_unknown_top_level_and_duplicate_json_keys_fail_closed():
    allowlist, predecessor, source = objects()
    allowlist["unknown"] = True
    with pytest.raises(V.StaticAllowlistV32Error, match="schema drift"):
        V.validate_objects(allowlist, predecessor, source)
    with pytest.raises(V.StaticAllowlistV32Error, match="duplicate JSON key"):
        V.parse_json_bytes(b'{"task_id":"T550","task_id":"other"}', "probe")


@pytest.mark.parametrize(
    ("path_token", "parent_token", "leaf_name"),
    [
        ("reviews/Hos/file:ads", "reviews/Hos", "file:ads"),
        ("reviews/Hos/NUL.txt", "reviews/Hos", "NUL.txt"),
        ("reviews/Hos/file.", "reviews/Hos", "file."),
        ("reviews/Hos/file ", "reviews/Hos", "file "),
        ("reviews/./file", "reviews/.", "file"),
        ("/absolute/file", "/absolute", "file"),
        ("reviews/Hos/e\u0301.json", "reviews/Hos", "e\u0301.json"),
        ("reviews\\Hos\\file", "reviews/Hos", "file"),
    ],
)
def test_bounded_windows_path_ambiguity_matrix(
    path_token, parent_token, leaf_name
):
    with pytest.raises(V.StaticAllowlistV32Error):
        V._v31._path_relation(path_token, parent_token, leaf_name)


@pytest.mark.parametrize("replacement", [1.0, True, -1])
def test_numeric_type_and_range_mutations_fail_closed(replacement):
    allowlist, predecessor, source = objects()
    allowlist["targets"][0]["preimage_size_bytes"] = replacement
    with pytest.raises(V.StaticAllowlistV32Error, match="nonnegative integer"):
        V.validate_objects(allowlist, predecessor, source)
