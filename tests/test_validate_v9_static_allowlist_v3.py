from __future__ import annotations

import copy
import importlib.util
import json
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
    / "validate_v9_static_allowlist_v3.py"
)
SPEC = importlib.util.spec_from_file_location("validate_v9_allowlist_test", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def objects():
    with VALIDATOR.ALLOWLIST.open("r", encoding="utf-8") as handle:
        allowlist = json.load(handle)
    with VALIDATOR.SOURCE_MANIFEST.open("r", encoding="utf-8") as handle:
        source = json.load(handle)
    return allowlist, source


def test_exact_static_allowlist_passes_without_live_targets() -> None:
    result = VALIDATOR.validate_files()
    assert result["verdict"] == "PASS_STATIC_ALLOWLIST_ONLY"
    assert result["target_count"] == 13
    assert result["sentinel_count"] == 3
    assert result["live_measurement_executed"] is False


@pytest.mark.parametrize(
    ("section", "index", "field", "value", "message"),
    [
        ("targets", 0, "path_token", "reviews/Hos/alternate.jsonl", "unsafe"),
        ("targets", 0, "parent_token", "reviews", "relation"),
        ("targets", 0, "preimage_sha256", "0" * 64, "frozen V6"),
        ("targets", 0, "staged_size_bytes", 1, "frozen V6"),
        ("sentinels", 0, "expected_sha256", "0" * 64, "sentinel"),
        ("sentinels", 0, "path_token", "../outside.jsonl", "unsafe"),
    ],
)
def test_protected_allowlist_mutations_fail(
    section, index, field, value, message
) -> None:
    allowlist, source = objects()
    drifted = copy.deepcopy(allowlist)
    drifted[section][index][field] = value
    with pytest.raises(VALIDATOR.StaticAllowlistV3Error, match=message):
        VALIDATOR.validate_objects(drifted, source)


def test_unknown_field_fails_closed() -> None:
    allowlist, source = objects()
    allowlist["targets"][0]["unexpected"] = True
    with pytest.raises(VALIDATOR.StaticAllowlistV3Error, match="schema"):
        VALIDATOR.validate_objects(allowlist, source)
