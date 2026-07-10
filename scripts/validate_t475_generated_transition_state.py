#!/usr/bin/env python3
"""Validate the exact T475 regenerated candidate while downstream baselines remain held."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts.run_t475_shadow_delta import jsonl_stats
except ModuleNotFoundError:
    from run_t475_shadow_delta import jsonl_stats

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "t475_usfm_shadow_delta_gate.yaml"
CANDIDATE_MANIFEST = ROOT / ".ai" / "context" / "agent_work" / "T475" / "candidate_manifest.json"
WORD_TOKENS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "word_tokens.jsonl"
FOOTNOTES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "footnotes.jsonl"

BASELINE_COUNTS = (677688, 1130)
CANDIDATE_COUNTS = (677686, 1127)
REQUIRED_DEFERRED = {
    "validate_t374_additive_parent_overlay.py",
    "validate_t401_eph1_output_pilot.py",
    "validate_t415_batch1_output_pilot.py",
    "validate_source_metadata_research_atlas.py",
    "validate_1cor8_10_parent_evidence_packet.py",
    "validate_divine_capitalization_inventory.py",
    "validate_wj_marker_inventory.py",
}


class T475TransitionError(ValueError):
    """Raised when regenerated output is not an exact declared T475 state."""


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        header = yaml.safe_load(parts[1]) or {}
        body = yaml.safe_load(parts[2]) or {}
        return {**header, **body}
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise T475TransitionError(f"{path}: expected YAML mapping")
    return data


def _count_rows(path: Path) -> int:
    if not path.is_file():
        return -1
    with path.open("rb") as handle:
        return sum(1 for line in handle if line.strip())


def classify_counts(word_tokens: int, footnotes: int) -> str:
    counts = (word_tokens, footnotes)
    if counts == BASELINE_COUNTS:
        return "baseline"
    if counts == CANDIDATE_COUNTS:
        return "candidate"
    return "unknown"


def detect_generated_state(root: Path = ROOT) -> str:
    return classify_counts(
        _count_rows(root / WORD_TOKENS.relative_to(ROOT)),
        _count_rows(root / FOOTNOTES.relative_to(ROOT)),
    )


def _generated_path(
    root: Path,
    manifest_path: str,
    *,
    canonical_root: Path | None = None,
    processed_root: Path | None = None,
) -> Path:
    rel = Path(manifest_path)
    if rel.parts[0] == "canonical":
        base = canonical_root or root / "data" / "canonical"
        return base / Path(*rel.parts[1:])
    if rel.parts[0] == "processed":
        base = processed_root or root / "data" / "processed" / "bible" / "eng-web" / "usfm"
        return base / Path(*rel.parts[1:])
    raise T475TransitionError(f"unsupported manifest path: {manifest_path}")


def validate_semantic_manifest(
    root: Path,
    manifest_path: Path,
    *,
    canonical_root: Path | None = None,
    processed_root: Path | None = None,
) -> dict[str, int]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest.get("files")
    if not isinstance(rows, list):
        raise T475TransitionError("candidate manifest files must be a list")
    checked = 0
    total_rows = 0
    for row in rows:
        if not isinstance(row, dict):
            raise T475TransitionError("candidate manifest row must be an object")
        rel = str(row.get("path", ""))
        if not rel.endswith(".jsonl"):
            continue
        target = _generated_path(
            root,
            rel,
            canonical_root=canonical_root,
            processed_root=processed_root,
        )
        if not target.is_file():
            raise T475TransitionError(f"generated candidate surface missing: {target}")
        count, digest = jsonl_stats(target, rel)
        if count != row.get("row_count"):
            raise T475TransitionError(
                f"{rel}: row_count {count} != frozen candidate {row.get('row_count')}"
            )
        if digest != row.get("stable_key_digest"):
            raise T475TransitionError(f"{rel}: stable-key semantic digest differs from frozen candidate")
        checked += 1
        total_rows += count
    if checked < 10:
        raise T475TransitionError(f"expected at least 10 JSONL surfaces, checked {checked}")
    return {"surfaces": checked, "rows": total_rows}


def validate_transition(root: Path = ROOT) -> dict[str, Any]:
    state = detect_generated_state(root)
    if state != "candidate":
        raise T475TransitionError(f"generated state must be exact candidate, observed {state}")
    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    policy = control.get("ci_generated_transition_policy")
    if not isinstance(policy, dict):
        raise T475TransitionError("CI generated-transition policy is missing")
    if policy.get("active_task_required") != "T475":
        raise T475TransitionError("transition policy must require active task T475")
    if policy.get("detected_candidate_counts") != {
        "word_tokens": CANDIDATE_COUNTS[0],
        "footnotes": CANDIDATE_COUNTS[1],
    }:
        raise T475TransitionError("transition policy candidate counts differ from the frozen state")
    if set(policy.get("deferred_legacy_generated_validators", [])) != REQUIRED_DEFERRED:
        raise T475TransitionError("deferred validator set differs from the reviewed T475 set")
    for key in (
        "authorizes_baseline_update",
        "authorizes_gold_or_output_change",
    ):
        if policy.get(key) is not False:
            raise T475TransitionError(f"transition policy {key} must be false")
    result = validate_semantic_manifest(
        root,
        root / CANDIDATE_MANIFEST.relative_to(ROOT),
    )
    return {"state": state, **result, "deferred": sorted(REQUIRED_DEFERRED)}


def validate_allowed_state(root: Path = ROOT) -> dict[str, Any]:
    """Accept the old baseline or prove the exact regenerated candidate."""
    state = detect_generated_state(root)
    if state == "baseline":
        return {"state": state, "surfaces": 0, "rows": 0, "deferred": []}
    if state == "unknown":
        raise T475TransitionError("generated state is neither the baseline nor the exact candidate")
    return validate_transition(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        result = validate_allowed_state(ROOT)
    except T475TransitionError as exc:
        print(f"T475 generated transition validation failed: {exc}", file=sys.stderr)
        return 1
    if result["state"] == "baseline":
        print("T475 generated transition validation passed (baseline state; no gates deferred).")
        return 0
    print(
        "T475 exact generated candidate validation passed "
        f"({result['surfaces']} JSONL surfaces; {result['rows']} rows)."
    )
    print("Deferred pre-T474 generated-baseline validators:")
    for name in result["deferred"]:
        print(f"- {name}")
    print("Deferral is non-authorizing; baseline/gold/output migration remains blocked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
