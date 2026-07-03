#!/usr/bin/env python3
"""Pin Rust observation substrate fingerprint to a model manifest before marathon."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import SCRATCH_ROOT, pin_substrate_to_manifest, substrate_build_fingerprint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_folder", type=Path, help="Model folder e.g. M1_cursor")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    folder = args.model_folder
    if not folder.is_dir():
        folder = SCRATCH_ROOT / args.model_folder
    if not folder.is_dir():
        print(f"ERROR: folder not found: {folder}", file=sys.stderr)
        return 1

    fp = substrate_build_fingerprint()
    if fp.get("status") != "present":
        print(
            "ERROR: observation substrate missing — run T412 rust scan first "
            "(see .ai/control/rust_first_observation_substrate.yaml)",
            file=sys.stderr,
        )
        return 2

    pin_substrate_to_manifest(folder)
    if args.json:
        print(json.dumps(fp, indent=2))
    else:
        print(f"OK: pinned substrate to {folder / 'model_manifest.yaml'}")
        print(f"  scan_manifest_sha256={fp['scan_manifest_sha256'][:16]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
