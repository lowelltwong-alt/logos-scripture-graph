#!/usr/bin/env python3
"""Compatibility check: the former T472 2 John packet must remain withdrawn."""
from __future__ import annotations

import sys

from scripts.validate_t472_model_panel_calibration_gate import validate_t472


def main() -> int:
    errors = validate_t472()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T472 2 John packet withdrawal validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
