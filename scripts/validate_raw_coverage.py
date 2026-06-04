#!/usr/bin/env python3
"""HARD GATE: every USFM marker in the real raw source must be classified.

Scans data/raw/ for the markers that ACTUALLY appear and checks them against
config/ingest/usfm_marker_coverage.yaml. Fails (exit 1) if:
  - a marker present in the raw source is NOT declared in the registry, or
  - a declared marker has `handling: UNHANDLED`.

This is the enforcement behind the rule "do a first pass on the actual raw
documents and make sure the chunking algorithm will actually work with them."
A new source archive cannot pass CI until every marker it contains is classified.

Dependency-light (regex fallback if PyYAML absent).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COVERAGE = ROOT / "config" / "ingest" / "usfm_marker_coverage.yaml"

# Reuse the deterministic scanner.
sys.path.insert(0, str(ROOT))
from scripts.scan_raw_sources import find_archives, scan_archive, all_markers  # noqa: E402


def load_declared() -> tuple[set[str], set[str]]:
    """Return (declared_markers, unhandled_markers) from the coverage registry."""
    declared: set[str] = set()
    unhandled: set[str] = set()
    text = COVERAGE.read_text(encoding="utf-8")
    try:
        import yaml

        data = yaml.safe_load(text) or {}
        for section in ("markers", "forward_declared"):
            for name, spec in (data.get(section) or {}).items():
                declared.add(str(name))
                if isinstance(spec, dict) and str(spec.get("handling", "")).upper() == "UNHANDLED":
                    unhandled.add(str(name))
        return declared, unhandled
    except ImportError:
        pass
    # Fallback: extract `  marker:` keys under markers:/forward_declared:
    in_block = False
    for line in text.splitlines():
        if re.match(r"^(markers|forward_declared):\s*$", line):
            in_block = True
            continue
        if line and not line.startswith((" ", "\t")) and ":" in line:
            in_block = False
        if in_block:
            m = re.match(r"^  ([A-Za-z0-9]+):", line)
            if m:
                declared.add(m.group(1))
                if "UNHANDLED" in line:
                    unhandled.add(m.group(1))
    return declared, unhandled


def main() -> int:
    archives = find_archives()
    if not archives:
        print("No raw archives under data/raw/ — nothing to check.")
        return 0
    if not COVERAGE.exists():
        print(f"Missing coverage registry: {COVERAGE.relative_to(ROOT)}", file=sys.stderr)
        return 1

    declared, unhandled = load_declared()
    found: set[str] = set()
    for path in archives:
        found |= all_markers(scan_archive(path))

    failures = []
    undeclared = sorted(found - declared)
    if undeclared:
        failures.append(
            "Raw source contains markers NOT in config/ingest/usfm_marker_coverage.yaml: "
            + ", ".join(f"\\{m}" for m in undeclared)
            + " — classify each before processing."
        )
    present_unhandled = sorted(found & unhandled)
    if present_unhandled:
        failures.append(
            "Markers present in raw but declared handling: UNHANDLED: "
            + ", ".join(f"\\{m}" for m in present_unhandled)
        )

    if failures:
        print("RAW COVERAGE GATE FAILED")
        for f in failures:
            print(f"- {f}")
        return 1
    print(f"Raw coverage OK: {len(found)} distinct markers across {len(archives)} archive(s), all classified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
