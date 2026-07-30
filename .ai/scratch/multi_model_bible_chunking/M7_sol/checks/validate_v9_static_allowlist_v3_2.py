#!/usr/bin/env python3
"""Fixed-input V3.2 validator for the frozen T550/Hos V3.1 allowlist.

The file entry point has no path parameters.  It opens exactly three pinned
metadata paths and reports the opened path scope and unmeasured metadata/cloud
effects honestly.  ``validate_objects`` is the sole injection seam for tests.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any


_V31_PATH = Path(__file__).with_name("validate_v9_static_allowlist_v3_1.py")
_EXPECTED_V31_DEPENDENCY_SHA256 = (
    "9aad85eee7adf116198cfa3cd2f77e2223e7e8c48b2cfc652496d6144749a98b"
)
if hashlib.sha256(_V31_PATH.read_bytes()).hexdigest() != _EXPECTED_V31_DEPENDENCY_SHA256:
    raise ImportError("frozen V3.1 validator dependency hash drift")
_V31_SPEC = importlib.util.spec_from_file_location(
    "_t550_validate_v9_static_allowlist_v31_dependency", _V31_PATH
)
if _V31_SPEC is None or _V31_SPEC.loader is None:
    raise ImportError(f"cannot load frozen V3.1 validator dependency: {_V31_PATH}")
_v31 = importlib.util.module_from_spec(_V31_SPEC)
sys.modules[_V31_SPEC.name] = _v31
_V31_SPEC.loader.exec_module(_v31)

ROOT = _v31.ROOT
ALLOWLIST = _v31.ALLOWLIST
PREDECESSOR_ALLOWLIST = _v31.PREDECESSOR_ALLOWLIST
SOURCE_MANIFEST = _v31.SOURCE_MANIFEST
EXPECTED_ALLOWLIST_SHA256 = _v31.EXPECTED_ALLOWLIST_SHA256
EXPECTED_PREDECESSOR_SHA256 = _v31.EXPECTED_PREDECESSOR_SHA256
EXPECTED_SOURCE_MANIFEST_SHA256 = _v31.EXPECTED_SOURCE_MANIFEST_SHA256
EXPECTED_TARGET_DESCRIPTORS = _v31.EXPECTED_TARGET_DESCRIPTORS
EXPECTED_SENTINEL_DESCRIPTORS = _v31.EXPECTED_SENTINEL_DESCRIPTORS
StaticAllowlistV32Error = _v31.StaticAllowlistV31Error
parse_json_bytes = _v31.parse_json_bytes


def validate_objects(
    allowlist: Any,
    predecessor_allowlist: Any,
    source_manifest: Any,
) -> dict[str, Any]:
    """Validate injected objects without filesystem access."""
    result = _v31.validate_objects(
        allowlist, predecessor_allowlist, source_manifest
    )
    result["verdict"] = "PASS_STATIC_ALLOWLIST_V3_2_VALIDATOR_ONLY"
    result["validation_input_mode"] = "object_injection_no_filesystem_access"
    return result


def _opened_input(
    artifact_id: str, path: Path, expected_sha256: str
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "declared_path": path.relative_to(ROOT).as_posix(),
        "opened_absolute_path": os.fspath(path.absolute()),
        "expected_and_observed_sha256": expected_sha256,
        "access_operation": "Path.read_bytes",
        "path_identity_reparse_hardlink_status": "unmeasured",
        "access_metadata_effect": "unmeasured_may_change",
        "cloud_hydration_effect": "unmeasured_may_change",
    }


def validate_files() -> dict[str, Any]:
    """Open exactly the three internally pinned metadata files."""
    allowlist = _v31._load_exact(
        ALLOWLIST, EXPECTED_ALLOWLIST_SHA256, "V3.1 allowlist"
    )
    predecessor = _v31._load_exact(
        PREDECESSOR_ALLOWLIST,
        EXPECTED_PREDECESSOR_SHA256,
        "V3 predecessor",
    )
    source = _v31._load_exact(
        SOURCE_MANIFEST,
        EXPECTED_SOURCE_MANIFEST_SHA256,
        "V6 source manifest",
    )
    result = validate_objects(allowlist, predecessor, source)
    result.update(
        {
            "validation_input_mode": "zero_argument_fixed_three_pinned_paths",
            "opened_path_count": 3,
            "opened_path_scope": "exact_three_reviewed_metadata_artifacts",
            "caller_path_injection_available": False,
            "opened_inputs": [
                _opened_input(
                    "v3_1_allowlist", ALLOWLIST, EXPECTED_ALLOWLIST_SHA256
                ),
                _opened_input(
                    "v3_predecessor_allowlist",
                    PREDECESSOR_ALLOWLIST,
                    EXPECTED_PREDECESSOR_SHA256,
                ),
                _opened_input(
                    "v6_source_manifest",
                    SOURCE_MANIFEST,
                    EXPECTED_SOURCE_MANIFEST_SHA256,
                ),
            ],
            "allowlist_sha256": EXPECTED_ALLOWLIST_SHA256,
            "predecessor_allowlist_sha256": EXPECTED_PREDECESSOR_SHA256,
            "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
            "metadata_or_cloud_zero_effect_claimed": False,
            "runtime_code_dependency": {
                "declared_path": _V31_PATH.relative_to(ROOT).as_posix(),
                "expected_and_observed_sha256": _EXPECTED_V31_DEPENDENCY_SHA256,
                "counted_as_metadata_input": False,
                "access_metadata_effect": "unmeasured_may_change",
                "cloud_hydration_effect": "unmeasured_may_change",
            },
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
