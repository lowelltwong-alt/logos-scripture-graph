#!/usr/bin/env python3
"""CLI wrapper for the T310 read-only form detector."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.chunking.detect_form import main


if __name__ == "__main__":
    raise SystemExit(main())
