#!/usr/bin/env python3
"""Validate the static T550/Hos V9 allowlist without opening live targets."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
REVIEW = MODEL / "reviews" / "Hos"
ALLOWLIST = REVIEW / "v9_static_allowlist_v3.json"
SOURCE_MANIFEST = (
    REVIEW
    / "rematerialization_attempts"
    / "T550-HOS-SEMANTIC-PROSE-REMATERIALIZATION-V6-ONE-SHOT"
    / "prepare_manifest_v6.json"
)
EXPECTED_ALLOWLIST_SHA256 = (
    "ceb51bb9bf51679164390cf07a46c5f3a1d307428355d987a6f4ae5b24bfa4ed"
)
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "f272661602efa1cab09fe224b6283fb2e0c1e072e9a8b54d0edcd6fa024885c4"
)
EXPECTED_SENTINELS = (
    (
        "low_confidence_register.jsonl",
        "ca548ec6b205ec030df6cebffe3a657e46aba01be97600382a55cb50f648c5b6",
    ),
    (
        "frontier_escalation_queue.jsonl",
        "8d101775088cba9a7ddde6e506db981d1fd1d866958caa57e8243df3a24268b1",
    ),
    (
        "atlas_candidate_feed.jsonl",
        "7bdbfc263fbd8d3fe0083fdfec978f3714ec84ad5f703cc9c428de616a608ca0",
    ),
)
_SHA = re.compile(r"^[0-9a-f]{64}$")
_TOP_KEYS = {
    "schema_version",
    "task_id",
    "book",
    "application_family",
    "source_render",
    "normalization",
    "targets",
    "sentinels",
    "file_identity_and_size_rows_deferred_to_post_static_execution_freeze",
    "live_measurement_executed",
    "candidate_only",
    "non_authorizing",
}
_TARGET_KEYS = {
    "ordinal",
    "target_id",
    "role",
    "path_token",
    "parent_token",
    "leaf_name",
    "preimage_sha256",
    "preimage_size_bytes",
    "staged_sha256",
    "staged_size_bytes",
}
_SENTINEL_KEYS = {
    "ordinal",
    "sentinel_id",
    "role",
    "path_token",
    "parent_token",
    "leaf_name",
    "expected_sha256",
}


class StaticAllowlistV3Error(ValueError):
    """Raised when the V9 static allowlist is not exact."""


def _digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def _closed(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != keys:
        actual = set(value) if isinstance(value, Mapping) else set()
        raise StaticAllowlistV3Error(
            f"{label} schema drift: missing={sorted(keys - actual)}, "
            f"extra={sorted(actual - keys)}"
        )
    return value


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or _SHA.fullmatch(value) is None:
        raise StaticAllowlistV3Error(f"{label} must be lowercase SHA-256")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise StaticAllowlistV3Error(f"{label} must be non-empty text")
    return value


def _size(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise StaticAllowlistV3Error(f"{label} must be a nonnegative integer")
    return value


def _path_relation(path_token: str, parent_token: str, leaf: str) -> None:
    if (
        "\\" in path_token
        or path_token.startswith("/")
        or ":" in path_token
        or any(part in ("", ".", "..") for part in path_token.split("/"))
        or leaf != path_token.split("/")[-1]
    ):
        raise StaticAllowlistV3Error("unsafe or ambiguous path token")
    derived_parent = "/".join(path_token.split("/")[:-1]) or "."
    if parent_token != derived_parent:
        raise StaticAllowlistV3Error("parent/leaf/path relation drift")


def validate_objects(
    allowlist: Any, source_manifest: Any
) -> dict[str, Any]:
    row = _closed(allowlist, _TOP_KEYS, "allowlist")
    if (
        row["schema_version"] != "m7_hosea_v9_static_allowlist.v3"
        or row["task_id"] != "T550"
        or row["book"] != "Hos"
        or row["file_identity_and_size_rows_deferred_to_post_static_execution_freeze"]
        is not True
        or row["live_measurement_executed"] is not False
        or row["candidate_only"] is not True
        or row["non_authorizing"] is not True
    ):
        raise StaticAllowlistV3Error("allowlist authority/scope drift")
    source = row["source_render"]
    if (
        not isinstance(source, Mapping)
        or source.get("prepare_manifest_sha256")
        != EXPECTED_SOURCE_MANIFEST_SHA256
        or source.get("decision_count") != 38
        or source.get("coverage") != "197/197"
        or source.get("accepted") != 36
        or source.get("held") != 2
    ):
        raise StaticAllowlistV3Error("frozen content-source scope drift")
    targets = row["targets"]
    sentinels = row["sentinels"]
    if not isinstance(targets, list) or len(targets) != 13:
        raise StaticAllowlistV3Error("exactly 13 targets are required")
    if not isinstance(sentinels, list) or len(sentinels) != 3:
        raise StaticAllowlistV3Error("exactly three sentinels are required")
    source_targets = source_manifest.get("targets")
    if not isinstance(source_targets, list) or len(source_targets) != 13:
        raise StaticAllowlistV3Error("source manifest target count drift")
    target_ids: set[str] = set()
    target_paths: set[str] = set()
    for ordinal, (raw, frozen) in enumerate(
        zip(targets, source_targets, strict=True), 1
    ):
        target = _closed(raw, _TARGET_KEYS, f"target[{ordinal}]")
        if target["ordinal"] != ordinal or frozen.get("ordinal") != ordinal:
            raise StaticAllowlistV3Error("target ordinal drift")
        target_id = _text(target["target_id"], "target_id")
        role = _text(target["role"], "target role")
        path_token = _text(target["path_token"], "target path")
        parent_token = _text(target["parent_token"], "target parent")
        leaf = _text(target["leaf_name"], "target leaf")
        _path_relation(path_token, parent_token, leaf)
        if target_id in target_ids or path_token in target_paths:
            raise StaticAllowlistV3Error("duplicate target ID or path")
        target_ids.add(target_id)
        target_paths.add(path_token)
        if not role:
            raise StaticAllowlistV3Error("target role is empty")
        for current, expected, label in (
            (
                _sha(target["preimage_sha256"], "preimage"),
                frozen.get("preimage_sha256"),
                "preimage hash",
            ),
            (
                _size(target["preimage_size_bytes"], "preimage size"),
                frozen.get("preimage_size_bytes"),
                "preimage size",
            ),
            (
                _sha(target["staged_sha256"], "staged"),
                frozen.get("staged_sha256"),
                "staged hash",
            ),
            (
                _size(target["staged_size_bytes"], "staged size"),
                frozen.get("staged_size_bytes"),
                "staged size",
            ),
            (path_token, frozen.get("path"), "target path"),
        ):
            if current != expected:
                raise StaticAllowlistV3Error(f"{label} differs from frozen V6")
    sentinel_paths: set[str] = set()
    for ordinal, (raw, expected) in enumerate(
        zip(sentinels, EXPECTED_SENTINELS, strict=True), 1
    ):
        sentinel = _closed(raw, _SENTINEL_KEYS, f"sentinel[{ordinal}]")
        if sentinel["ordinal"] != ordinal:
            raise StaticAllowlistV3Error("sentinel ordinal drift")
        path_token = _text(sentinel["path_token"], "sentinel path")
        parent_token = _text(sentinel["parent_token"], "sentinel parent")
        leaf = _text(sentinel["leaf_name"], "sentinel leaf")
        _path_relation(path_token, parent_token, leaf)
        if path_token in sentinel_paths or path_token in target_paths:
            raise StaticAllowlistV3Error("duplicate sentinel/target path")
        sentinel_paths.add(path_token)
        if (
            path_token != expected[0]
            or _sha(sentinel["expected_sha256"], "sentinel hash")
            != expected[1]
        ):
            raise StaticAllowlistV3Error("global sentinel allowlist drift")
    return {
        "verdict": "PASS_STATIC_ALLOWLIST_ONLY",
        "target_count": 13,
        "sentinel_count": 3,
        "live_measurement_executed": False,
        "candidate_only": True,
        "non_authorizing": True,
    }


def validate_files(
    allowlist_path: Path = ALLOWLIST,
    source_manifest_path: Path = SOURCE_MANIFEST,
) -> dict[str, Any]:
    if _digest(allowlist_path) != EXPECTED_ALLOWLIST_SHA256:
        raise StaticAllowlistV3Error("static allowlist file hash drift")
    if _digest(source_manifest_path) != EXPECTED_SOURCE_MANIFEST_SHA256:
        raise StaticAllowlistV3Error("source V6 manifest hash drift")
    with allowlist_path.open("r", encoding="utf-8") as handle:
        allowlist = json.load(handle)
    with source_manifest_path.open("r", encoding="utf-8") as handle:
        source = json.load(handle)
    result = validate_objects(allowlist, source)
    result["allowlist_sha256"] = EXPECTED_ALLOWLIST_SHA256
    result["source_manifest_sha256"] = EXPECTED_SOURCE_MANIFEST_SHA256
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate_files()
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(result["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
