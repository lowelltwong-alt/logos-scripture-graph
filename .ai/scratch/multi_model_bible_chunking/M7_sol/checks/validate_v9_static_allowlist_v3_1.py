#!/usr/bin/env python3
"""Validate the closed T550/Hos V9 V3.1 static allowlist.

Only three immutable metadata artifacts are opened: this generation, its
frozen V3 predecessor, and the frozen V6 source manifest.  Canonical targets,
global sentinels, live processes, clocks, and Windows state are never opened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping
import unicodedata


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
REVIEW = MODEL / "reviews" / "Hos"
ALLOWLIST = REVIEW / "v9_static_allowlist_v3_1.json"
PREDECESSOR_ALLOWLIST = REVIEW / "v9_static_allowlist_v3.json"
SOURCE_MANIFEST = (
    REVIEW
    / "rematerialization_attempts"
    / "T550-HOS-SEMANTIC-PROSE-REMATERIALIZATION-V6-ONE-SHOT"
    / "prepare_manifest_v6.json"
)

EXPECTED_ALLOWLIST_SHA256 = (
    "a3e18ac151a4d0fb51afc282874e873f2c3344b5aab858bc5da1d1e2acec4a80"
)
EXPECTED_PREDECESSOR_SHA256 = (
    "ceb51bb9bf51679164390cf07a46c5f3a1d307428355d987a6f4ae5b24bfa4ed"
)
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "f272661602efa1cab09fe224b6283fb2e0c1e072e9a8b54d0edcd6fa024885c4"
)
EXPECTED_APPLICATION_FAMILY = "T550-HOS-SEMANTIC-PROSE-REMATERIALIZATION-V9"
EXPECTED_PREDECESSOR = {
    "schema_version": "m7_hosea_v9_static_allowlist.v3",
    "path": (
        ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Hos/"
        "v9_static_allowlist_v3.json"
    ),
    "sha256": EXPECTED_PREDECESSOR_SHA256,
}
EXPECTED_SOURCE_RENDER = {
    "generation": "V6_CONTENT_REUSED_WITHOUT_TRANSACTION_AUTHORITY",
    "prepare_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
    "independent_content_pass_sha256": (
        "0f34c6524c4079ac4c9d0467ab80ffe3d7df16f25f7da7afe9393ab3a73d2999"
    ),
    "decision_count": 38,
    "coverage": "197/197",
    "accepted": 36,
    "held": 2,
}
EXPECTED_NORMALIZATION = {
    "path_separator": "/",
    "relative_to": "M7_sol_model_root",
    "absolute_paths_forbidden": True,
    "dot_and_dotdot_components_forbidden": True,
    "alternate_data_stream_suffix_forbidden": True,
    "trailing_dot_or_space_forbidden": True,
    "unicode_normalization": "NFC",
    "windows_casefold_uniqueness_required": True,
    "windows_reserved_device_names_forbidden": True,
}
EXPECTED_COUNTS = {
    "governed_member_count": 13,
    "replacement_count": 8,
    "guard_only_count": 5,
    "sentinel_count": 3,
}
EXPECTED_TARGET_DESCRIPTORS = (
    (1, "hos-v9-target-01", "decision_evidence", "replace", "reviews/Hos/decision_evidence_v2.jsonl"),
    (2, "hos-v9-target-02", "chunk_map", "replace", "book_chunks/Hos/chunks.jsonl"),
    (3, "hos-v9-target-03", "review_packets", "replace", "reviews/Hos/review_packets.jsonl"),
    (4, "hos-v9-target-04", "decision_relations", "guard_only", "reviews/Hos/decision_relations.jsonl"),
    (5, "hos-v9-target-05", "primary_hebrew_review", "replace", "reviews/Hos/primary_hebrew_v2.json"),
    (6, "hos-v9-target-06", "primary_literary_review", "guard_only", "reviews/Hos/primary_literary_v2.json"),
    (7, "hos-v9-target-07", "canonical_premortem", "replace", "reviews/Hos/canonical_premortem_v2.json"),
    (8, "hos-v9-target-08", "peer_crosscheck", "replace", "reviews/Hos/peer_crosscheck_v2.json"),
    (9, "hos-v9-target-09", "boss_ruling", "guard_only", "reviews/Hos/boss_ruling_v2.json"),
    (10, "hos-v9-target-10", "book_local_sidecar_rows", "replace", "reviews/Hos/sidecar_rows_v2.json"),
    (11, "hos-v9-target-11", "append_only_appeal_ledger", "guard_only", "reviews/Hos/appeal_ledger.jsonl"),
    (12, "hos-v9-target-12", "post_resolution_check", "replace", "reviews/Hos/post_resolution_check_v2.json"),
    (13, "hos-v9-target-13", "book_completion_receipt", "guard_only", "receipts/Hos_completion_v2.json"),
)
EXPECTED_SENTINEL_DESCRIPTORS = (
    (
        1,
        "hos-v9-global-sentinel-01",
        "global_low_confidence_register_immutable_guard",
        "low_confidence_register.jsonl",
        "ca548ec6b205ec030df6cebffe3a657e46aba01be97600382a55cb50f648c5b6",
    ),
    (
        2,
        "hos-v9-global-sentinel-02",
        "global_frontier_escalation_queue_immutable_guard",
        "frontier_escalation_queue.jsonl",
        "8d101775088cba9a7ddde6e506db981d1fd1d866958caa57e8243df3a24268b1",
    ),
    (
        3,
        "hos-v9-global-sentinel-03",
        "global_atlas_candidate_feed_immutable_guard",
        "atlas_candidate_feed.jsonl",
        "7bdbfc263fbd8d3fe0083fdfec978f3714ec84ad5f703cc9c428de616a608ca0",
    ),
)

_SHA = re.compile(r"^[0-9a-f]{64}$")
_WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
_TOP_KEYS = {
    "schema_version",
    "task_id",
    "book",
    "application_family",
    "predecessor_allowlist",
    "source_render",
    "normalization",
    "governed_counts",
    "targets",
    "sentinels",
    "file_identity_rows_deferred_to_post_static_execution_freeze",
    "live_measurement_executed",
    "candidate_only",
    "non_authorizing",
}
_PREDECESSOR_KEYS = {"schema_version", "path", "sha256"}
_SOURCE_RENDER_KEYS = set(EXPECTED_SOURCE_RENDER)
_NORMALIZATION_KEYS = set(EXPECTED_NORMALIZATION)
_COUNT_KEYS = set(EXPECTED_COUNTS)
_TARGET_KEYS = {
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
}
_LEGACY_TARGET_KEYS = _TARGET_KEYS - {"operation"}
_SENTINEL_KEYS = {
    "ordinal",
    "sentinel_id",
    "role",
    "path_token",
    "parent_token",
    "leaf_name",
    "expected_sha256",
}
_PREDECESSOR_TOP_KEYS = {
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
_SOURCE_TARGET_KEYS = {
    "archive_sha256",
    "archive_size_bytes",
    "ordinal",
    "path",
    "preimage_sha256",
    "preimage_size_bytes",
    "staged_sha256",
    "staged_size_bytes",
    "target_id",
}


class StaticAllowlistV31Error(ValueError):
    """Raised when V3.1 metadata is not exact and fail-closed."""


def _digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StaticAllowlistV31Error(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json_bytes(raw: bytes, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StaticAllowlistV31Error(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, Mapping):
        raise StaticAllowlistV31Error(f"{label} root must be an object")
    return value


def _load_exact(path: Path, expected_sha256: str, label: str) -> Mapping[str, Any]:
    raw = path.read_bytes()
    if _digest_bytes(raw) != expected_sha256:
        raise StaticAllowlistV31Error(f"{label} file hash drift")
    return parse_json_bytes(raw, label)


def _closed(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != keys:
        actual = set(value) if isinstance(value, Mapping) else set()
        raise StaticAllowlistV31Error(
            f"{label} schema drift: missing={sorted(keys - actual)}, "
            f"extra={sorted(actual - keys)}"
        )
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise StaticAllowlistV31Error(f"{label} must be non-empty text")
    return value


def _integer(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise StaticAllowlistV31Error(f"{label} must be a nonnegative integer")
    return value


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or _SHA.fullmatch(value) is None:
        raise StaticAllowlistV31Error(f"{label} must be lowercase SHA-256")
    return value


def _path_relation(path_token: str, parent_token: str, leaf_name: str) -> str:
    path_token = _text(path_token, "path token")
    parent_token = _text(parent_token, "parent token")
    leaf_name = _text(leaf_name, "leaf name")
    for value in (path_token, parent_token, leaf_name):
        if unicodedata.normalize("NFC", value) != value:
            raise StaticAllowlistV31Error("path metadata must be NFC")
    if (
        "\\" in path_token
        or path_token.startswith("/")
        or ":" in path_token
        or any(ord(character) < 32 or character in '<>"|?*' for character in path_token)
    ):
        raise StaticAllowlistV31Error("unsafe Windows path token")
    parts = path_token.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise StaticAllowlistV31Error("dot or empty path component")
    for part in parts:
        if part.endswith((" ", ".")):
            raise StaticAllowlistV31Error("trailing dot or space")
        if part.split(".", 1)[0].casefold() in _WINDOWS_RESERVED:
            raise StaticAllowlistV31Error("Windows reserved device name")
    derived_parent = "/".join(parts[:-1]) or "."
    if parent_token != derived_parent or leaf_name != parts[-1]:
        raise StaticAllowlistV31Error("parent/leaf/path relation drift")
    return path_token.casefold()


def _require_unique_windows_keys(keys: list[str]) -> None:
    if len(keys) != len(set(keys)):
        raise StaticAllowlistV31Error("Windows casefold path collision")


def validate_objects(
    allowlist: Any,
    predecessor_allowlist: Any,
    source_manifest: Any,
) -> dict[str, Any]:
    row = _closed(allowlist, _TOP_KEYS, "allowlist")
    if (
        row["schema_version"] != "m7_hosea_v9_static_allowlist.v3_1"
        or row["task_id"] != "T550"
        or row["book"] != "Hos"
        or row["application_family"] != EXPECTED_APPLICATION_FAMILY
        or row["file_identity_rows_deferred_to_post_static_execution_freeze"] is not True
        or row["live_measurement_executed"] is not False
        or row["candidate_only"] is not True
        or row["non_authorizing"] is not True
    ):
        raise StaticAllowlistV31Error("allowlist authority or identity drift")

    predecessor_ref = _closed(
        row["predecessor_allowlist"], _PREDECESSOR_KEYS, "predecessor reference"
    )
    source_render = _closed(row["source_render"], _SOURCE_RENDER_KEYS, "source render")
    normalization = _closed(
        row["normalization"], _NORMALIZATION_KEYS, "normalization"
    )
    counts = _closed(row["governed_counts"], _COUNT_KEYS, "governed counts")
    if dict(predecessor_ref) != EXPECTED_PREDECESSOR:
        raise StaticAllowlistV31Error("predecessor reference drift")
    if dict(source_render) != EXPECTED_SOURCE_RENDER:
        raise StaticAllowlistV31Error("source render drift")
    if dict(normalization) != EXPECTED_NORMALIZATION:
        raise StaticAllowlistV31Error("normalization drift")
    if dict(counts) != EXPECTED_COUNTS:
        raise StaticAllowlistV31Error("governed count declaration drift")

    predecessor = _closed(
        predecessor_allowlist, _PREDECESSOR_TOP_KEYS, "predecessor allowlist"
    )
    if (
        predecessor["schema_version"] != EXPECTED_PREDECESSOR["schema_version"]
        or predecessor["task_id"] != "T550"
        or predecessor["book"] != "Hos"
        or predecessor["application_family"] != EXPECTED_APPLICATION_FAMILY
        or predecessor["source_render"] != EXPECTED_SOURCE_RENDER
    ):
        raise StaticAllowlistV31Error("predecessor semantic drift")
    prior_normalization = _closed(
        predecessor["normalization"],
        {
            "path_separator",
            "relative_to",
            "absolute_paths_forbidden",
            "dot_and_dotdot_components_forbidden",
            "alternate_data_stream_suffix_forbidden",
            "trailing_dot_or_space_forbidden",
        },
        "predecessor normalization",
    )
    for key, value in prior_normalization.items():
        if normalization[key] != value:
            raise StaticAllowlistV31Error("predecessor normalization projection drift")

    if not isinstance(source_manifest, Mapping):
        raise StaticAllowlistV31Error("source manifest root must be an object")
    if (
        source_manifest.get("schema_version") != "m7_hosea_render_prepare_manifest.v6"
        or source_manifest.get("task_id") != "T550"
        or source_manifest.get("book") != "Hos"
        or source_manifest.get("application_id")
        != "T550-HOS-SEMANTIC-PROSE-REMATERIALIZATION-V6-ONE-SHOT"
        or source_manifest.get("target_count") != 13
        or source_manifest.get("candidate_only") is not True
        or source_manifest.get("non_authorizing") is not True
    ):
        raise StaticAllowlistV31Error("source V6 identity drift")

    targets = row["targets"]
    prior_targets = predecessor["targets"]
    source_targets = source_manifest.get("targets")
    sentinels = row["sentinels"]
    prior_sentinels = predecessor["sentinels"]
    if not isinstance(targets, list) or len(targets) != 13:
        raise StaticAllowlistV31Error("exactly 13 governed targets are required")
    if not isinstance(prior_targets, list) or len(prior_targets) != 13:
        raise StaticAllowlistV31Error("predecessor target count drift")
    if not isinstance(source_targets, list) or len(source_targets) != 13:
        raise StaticAllowlistV31Error("source target count drift")
    if not isinstance(sentinels, list) or len(sentinels) != 3:
        raise StaticAllowlistV31Error("exactly three sentinels are required")
    if not isinstance(prior_sentinels, list) or len(prior_sentinels) != 3:
        raise StaticAllowlistV31Error("predecessor sentinel count drift")

    windows_path_keys: list[str] = []
    target_ids: set[str] = set()
    operation_counts = {"replace": 0, "guard_only": 0}
    for index, (raw, prior_raw, source_raw, descriptor) in enumerate(
        zip(targets, prior_targets, source_targets, EXPECTED_TARGET_DESCRIPTORS, strict=True),
        1,
    ):
        target = _closed(raw, _TARGET_KEYS, f"target[{index}]")
        prior = _closed(prior_raw, _LEGACY_TARGET_KEYS, f"predecessor target[{index}]")
        source = _closed(source_raw, _SOURCE_TARGET_KEYS, f"source target[{index}]")
        observed_descriptor = (
            target["ordinal"],
            target["target_id"],
            target["role"],
            target["operation"],
            target["path_token"],
        )
        if observed_descriptor != descriptor:
            raise StaticAllowlistV31Error(f"target[{index}] descriptor drift")
        windows_path_keys.append(
            _path_relation(
                target["path_token"], target["parent_token"], target["leaf_name"]
            )
        )
        target_id = _text(target["target_id"], f"target[{index}] ID")
        if target_id in target_ids:
            raise StaticAllowlistV31Error("duplicate target ID")
        target_ids.add(target_id)
        preimage = (
            _sha(target["preimage_sha256"], "preimage hash"),
            _integer(target["preimage_size_bytes"], "preimage size"),
        )
        staged = (
            _sha(target["staged_sha256"], "staged hash"),
            _integer(target["staged_size_bytes"], "staged size"),
        )
        operation = target["operation"]
        operation_counts[operation] += 1
        if operation == "guard_only" and preimage != staged:
            raise StaticAllowlistV31Error("guard_only row must preserve exact state")
        if operation == "replace" and preimage == staged:
            raise StaticAllowlistV31Error("replace row must change exact state")
        legacy_projection = {
            key: target[key] for key in _LEGACY_TARGET_KEYS
        }
        if legacy_projection != dict(prior):
            raise StaticAllowlistV31Error("V3 predecessor target projection drift")
        for current, expected, label in (
            (target["ordinal"], source["ordinal"], "source ordinal"),
            (target["path_token"], source["path"], "source path"),
            (target["preimage_sha256"], source["preimage_sha256"], "source preimage hash"),
            (target["preimage_size_bytes"], source["preimage_size_bytes"], "source preimage size"),
            (target["staged_sha256"], source["staged_sha256"], "source staged hash"),
            (target["staged_size_bytes"], source["staged_size_bytes"], "source staged size"),
        ):
            if current != expected:
                raise StaticAllowlistV31Error(f"{label} drift")

    sentinel_ids: set[str] = set()
    for index, (raw, prior_raw, descriptor) in enumerate(
        zip(sentinels, prior_sentinels, EXPECTED_SENTINEL_DESCRIPTORS, strict=True),
        1,
    ):
        sentinel = _closed(raw, _SENTINEL_KEYS, f"sentinel[{index}]")
        prior = _closed(prior_raw, _SENTINEL_KEYS, f"predecessor sentinel[{index}]")
        observed_descriptor = (
            sentinel["ordinal"],
            sentinel["sentinel_id"],
            sentinel["role"],
            sentinel["path_token"],
            sentinel["expected_sha256"],
        )
        if observed_descriptor != descriptor:
            raise StaticAllowlistV31Error(f"sentinel[{index}] descriptor drift")
        windows_path_keys.append(
            _path_relation(
                sentinel["path_token"],
                sentinel["parent_token"],
                sentinel["leaf_name"],
            )
        )
        sentinel_id = _text(sentinel["sentinel_id"], f"sentinel[{index}] ID")
        if sentinel_id in sentinel_ids:
            raise StaticAllowlistV31Error("duplicate sentinel ID")
        sentinel_ids.add(sentinel_id)
        _sha(sentinel["expected_sha256"], "sentinel hash")
        if dict(sentinel) != dict(prior):
            raise StaticAllowlistV31Error("V3 predecessor sentinel projection drift")

    _require_unique_windows_keys(windows_path_keys)
    if operation_counts != {
        "replace": EXPECTED_COUNTS["replacement_count"],
        "guard_only": EXPECTED_COUNTS["guard_only_count"],
    }:
        raise StaticAllowlistV31Error("derived operation counts drift")

    return {
        "verdict": "PASS_STATIC_ALLOWLIST_V3_1_ONLY",
        "governed_member_count": len(targets),
        "replacement_count": operation_counts["replace"],
        "guard_only_count": operation_counts["guard_only"],
        "sentinel_count": len(sentinels),
        "predecessor_projection_exact": True,
        "source_v6_projection_exact": True,
        "live_measurement_executed": False,
        "canonical_or_global_targets_opened": False,
        "candidate_only": True,
        "non_authorizing": True,
    }


def validate_files(
    allowlist_path: Path = ALLOWLIST,
    predecessor_path: Path = PREDECESSOR_ALLOWLIST,
    source_manifest_path: Path = SOURCE_MANIFEST,
) -> dict[str, Any]:
    allowlist = _load_exact(
        allowlist_path, EXPECTED_ALLOWLIST_SHA256, "V3.1 allowlist"
    )
    predecessor = _load_exact(
        predecessor_path, EXPECTED_PREDECESSOR_SHA256, "V3 predecessor"
    )
    source = _load_exact(
        source_manifest_path, EXPECTED_SOURCE_MANIFEST_SHA256, "V6 source manifest"
    )
    result = validate_objects(allowlist, predecessor, source)
    result.update(
        {
            "allowlist_sha256": EXPECTED_ALLOWLIST_SHA256,
            "predecessor_allowlist_sha256": EXPECTED_PREDECESSOR_SHA256,
            "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        }
    )
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
