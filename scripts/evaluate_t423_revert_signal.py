#!/usr/bin/env python3
"""Evaluate T423 revert signal from offline batch compare matrix."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import SCRATCH_ROOT, load_fork_policy
MATRIX = SCRATCH_ROOT / "comparison" / "model_agreement_matrix.yaml"


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_matrix(path: Path = MATRIX) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def evaluate(*, matrix: dict[str, Any], policy: dict[str, Any], pilot_only: bool) -> dict[str, Any]:
    threshold = policy.get("revert_policy", {}).get("revert_threshold", {})
    pilot_books = set(threshold.get("pilot_books", []))
    pilot_min = float(threshold.get("pilot_verse_coverage_agreement_rate_minimum", 0.60))
    full_min = float(threshold.get("full_marathon_verse_coverage_agreement_rate_minimum", 0.50))

    overall = float(
        matrix.get(
            "overall_verse_coverage_agreement_rate",
            matrix.get("overall_agreement_rate", 0.0),
        )
    )
    per_book = matrix.get("per_book", {})
    pilot_rates = [
        float(per_book[b].get("verse_coverage_agreement_rate", 0.0))
        for b in pilot_books
        if b in per_book
    ]
    pilot_avg = sum(pilot_rates) / len(pilot_rates) if pilot_rates else overall

    false_consensus = matrix.get("false_consensus_warnings", [])
    shared_error_gate = threshold.get("shared_error_gate", {})
    warnings_only = bool(shared_error_gate.get("does_not_auto_revert", True))

    reasons: list[str] = []
    if pilot_only:
        passed = pilot_avg >= pilot_min and len(pilot_rates) == len(pilot_books)
        if len(pilot_rates) != len(pilot_books):
            reasons.append(f"pilot books incomplete in matrix: have {len(pilot_rates)}/{len(pilot_books)}")
        if pilot_avg < pilot_min:
            reasons.append(f"pilot verse-coverage {pilot_avg:.2%} < minimum {pilot_min:.2%}")
        verdict = "PILOT_PASS" if passed else "PILOT_FAIL"
    else:
        passed = overall >= full_min
        if overall < full_min:
            reasons.append(f"full verse-coverage {overall:.2%} < minimum {full_min:.2%}")
        verdict = "FULL_PASS" if passed else "FULL_FAIL"

    if false_consensus and not warnings_only:
        reasons.append(f"false_consensus_warnings: {len(false_consensus)}")
    elif false_consensus:
        reasons.append(f"warning_only false_consensus: {len(false_consensus)}")

    return {
        "verdict": verdict,
        "passed": passed,
        "overall_verse_coverage_agreement_rate": overall,
        "pilot_average_verse_coverage": round(pilot_avg, 4),
        "pilot_minimum": pilot_min,
        "full_minimum": full_min,
        "reasons": reasons,
        "false_consensus_count": len(false_consensus) if isinstance(false_consensus, list) else 0,
        "metric": "verse_coverage_agreement_rate",
        "legacy_exact_span_deprecated": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=MATRIX)
    parser.add_argument("--pilot-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.matrix.is_file():
        print(f"ERROR: missing {_rel(args.matrix)} — run batch compare after all models complete", file=sys.stderr)
        return 2

    policy = load_fork_policy()
    matrix = load_matrix(args.matrix)
    result = evaluate(matrix=matrix, policy=policy, pilot_only=args.pilot_only)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["verdict"])
        for reason in result["reasons"]:
            print(f"  - {reason}")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
