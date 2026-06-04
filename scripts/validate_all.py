#!/usr/bin/env python3
"""Run all repository validation gates (green/red for CI and agents).

Always-run gates: repo, control plane, handoffs, source manifest.
Conditional gates: JSONL referential integrity + canon presence run only when
the generated canonical data is present (so clean checkouts stay green; CI
regenerates the data first, then this gate is real). The 432 MB word_tokens
file is intentionally excluded for runtime — validate it separately/nightly.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

MANIFEST = ROOT / "data" / "raw" / "bible" / "eng-web" / "source_manifest.yaml"
CANON_DIR = ROOT / "data" / "canonical"
SMALL_CANON = [
    CANON_DIR / "scripture" / "passages" / "passages.jsonl",
    CANON_DIR / "translations" / "eng-web" / "translation_witnesses.jsonl",
    CANON_DIR / "translations" / "eng-web" / "section_headings.jsonl",
    CANON_DIR / "translations" / "eng-web" / "footnotes.jsonl",
    CANON_DIR / "translations" / "eng-web" / "editorial_cross_references.jsonl",
    CANON_DIR / "translations" / "eng-web" / "glossary_entries.jsonl",
]


def build_gates() -> list[tuple[str, list[str]]]:
    gates: list[tuple[str, list[str]]] = [
        ("validate_repo.py", [PY, str(ROOT / "scripts" / "validate_repo.py")]),
        ("validate_control_plane.py", [PY, str(ROOT / "scripts" / "validate_control_plane.py")]),
        ("validate_handoffs.py", [PY, str(ROOT / "scripts" / "agent" / "validate_handoffs.py")]),
    ]
    # Raw-source gates (the committed raw archives are the real pipeline input).
    if (ROOT / "data" / "raw").exists():
        gates.append(("validate_raw_coverage.py", [PY, str(ROOT / "scripts" / "validate_raw_coverage.py")]))
        gates.append(("scan_raw_sources.py --check", [PY, str(ROOT / "scripts" / "scan_raw_sources.py"), "--check"]))
    if MANIFEST.exists():
        gates.append(
            ("validate_manifest.py", [PY, str(ROOT / "pipelines" / "validate" / "validate_manifest.py"), str(MANIFEST)])
        )
    present = [p for p in SMALL_CANON if p.exists()]
    if present:
        cmd = [PY, str(ROOT / "scripts" / "validate_jsonl.py"), "--require-canon", *[str(p) for p in present]]
        gates.append(("validate_jsonl.py (canonical)", cmd))
    return gates


def main() -> int:
    failures = []
    for name, cmd in build_gates():
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            failures.append(name)
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
        else:
            print(result.stdout.strip())
    if failures:
        print(f"\nVALIDATION SUITE FAILED: {', '.join(failures)}")
        return 1
    print("\nAll validation gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
