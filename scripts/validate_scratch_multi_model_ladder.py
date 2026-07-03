#!/usr/bin/env python3
"""Validate scratch multi-model ladder manifests and L1 completeness."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "scratch_multi_model_ladder_policy.yaml"
BATCH2_MANIFEST = ROOT / ".ai" / "context" / "agent_work" / "T417" / "model_layers" / "batch2" / "manifest.yaml"
L1_ROOT = ROOT / ".ai" / "context" / "agent_work" / "T417" / "model_layers" / "batch2" / "L1_cursor"
L2_ROOT = ROOT / ".ai" / "context" / "agent_work" / "T417" / "model_layers" / "batch2" / "L2_codex"
L3_ROOT = ROOT / ".ai" / "context" / "agent_work" / "T417" / "model_layers" / "batch2" / "L3_claude"

L1_REQUIRED = (
    "strengthened_review_packets/t411_batch2_phlm_opening_review.md",
    "strengthened_review_packets/t411_batch2_jude_opening_review.md",
    "strengthened_review_packets/t411_batch2_jonah_opening_review.md",
    "gold_candidacy_assessment.yaml",
    "harness_scratch_assessment.yaml",
    "output_pilot_scratch_assessment.yaml",
    "layer_decision_log.jsonl",
    "layer_summary.md",
)

L2_REQUIRED = (
    "gold_candidacy_assessment.yaml",
    "strengthening_gaps.md",
    "codex_promotion_suggestion.yaml",
    "layer_decision_log.jsonl",
    "layer_summary.md",
)

L3_REQUIRED = (
    "architecture_audit.md",
    "gold_candidacy_assessment.yaml",
    "layer_decision_log.jsonl",
    "layer_summary.md",
)

TRANSPARENCY_REQUIRED = (
    "decision_id",
    "layer_id",
    "model_surface",
    "step_id",
    "choice",
    "rationale",
    "might_be_wrong",
    "confidence",
    "gold_recommendation",
    "non_authorizations",
)


class ScratchMultiModelLadderError(ValueError):
    pass


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ScratchMultiModelLadderError(f"{_rel(path)}: expected YAML mapping")
    return data


def validate_policy(data: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if data is None:
        if not POLICY.is_file():
            return [f"missing {_rel(POLICY)}"]
        data = _read_yaml(POLICY)
    if data.get("object_type") != "scratch_multi_model_ladder_policy":
        errors.append("object_type must be scratch_multi_model_ladder_policy")
    authority = data.get("authority", {})
    if authority.get("authorizes_reviewed_gold_promotion"):
        errors.append("policy must not authorize reviewed gold promotion")
    if authority.get("authorizes_canon_promotion"):
        errors.append("policy must not authorize canon promotion")
    layers = data.get("layer_stack", [])
    if len(layers) < 3:
        errors.append("layer_stack must have at least 3 layers")
    return errors


def validate_batch2_manifest() -> list[str]:
    errors: list[str] = []
    if not BATCH2_MANIFEST.is_file():
        return [f"missing {_rel(BATCH2_MANIFEST)}"]
    data = _read_yaml(BATCH2_MANIFEST)
    if data.get("batch_id") != "batch2":
        errors.append("manifest batch_id must be batch2")
    candidates = data.get("candidates", [])
    if len(candidates) != 3:
        errors.append("batch2 manifest must list 3 candidates")
    layers = data.get("layers", {})
    for lid in ("L1_cursor", "L2_codex", "L3_claude"):
        if lid not in layers:
            errors.append(f"manifest missing layer {lid}")
    l1 = layers.get("L1_cursor", {})
    if l1.get("status") != "complete":
        errors.append("L1_cursor must be complete for current batch2 scaffold")
    l2 = layers.get("L2_codex", {})
    if l2.get("status") == "complete" and not l2.get("verdict"):
        errors.append("L2_codex complete requires verdict field")
    l3 = layers.get("L3_claude", {})
    if l3.get("status") == "complete" and not l3.get("verdict"):
        errors.append("L3_claude complete requires verdict field")
    return errors


def _validate_layer_log(layer_root: Path, layer_label: str) -> list[str]:
    errors: list[str] = []
    log_path = layer_root / "layer_decision_log.jsonl"
    if not log_path.is_file():
        return errors
    lines = [ln for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) < 3:
        errors.append(f"{layer_label} layer_decision_log.jsonl must have at least 3 decisions")
    for idx, line in enumerate(lines):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"{layer_label} decision log line {idx + 1} invalid JSON")
            continue
        if not isinstance(rec, dict):
            errors.append(f"{layer_label} decision log line {idx + 1} must be object")
            continue
        missing = [k for k in TRANSPARENCY_REQUIRED if k not in rec]
        if missing:
            errors.append(f"{layer_label} decision {rec.get('decision_id', idx)} missing: {missing}")
    return errors


def validate_l2_artifacts(manifest_layers: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if manifest_layers is None:
        if not BATCH2_MANIFEST.is_file():
            return errors
        manifest_layers = _read_yaml(BATCH2_MANIFEST).get("layers", {})
    l2 = manifest_layers.get("L2_codex", {})
    if l2.get("status") != "complete":
        return errors
    for rel in L2_REQUIRED:
        path = L2_ROOT / rel
        if not path.is_file():
            errors.append(f"missing L2 artifact {_rel(path)}")
    errors.extend(_validate_layer_log(L2_ROOT, "L2"))
    return errors


def validate_l3_artifacts(manifest_layers: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if manifest_layers is None:
        if not BATCH2_MANIFEST.is_file():
            return errors
        manifest_layers = _read_yaml(BATCH2_MANIFEST).get("layers", {})
    l3 = manifest_layers.get("L3_claude", {})
    if l3.get("status") != "complete":
        return errors
    for rel in L3_REQUIRED:
        path = L3_ROOT / rel
        if not path.is_file():
            errors.append(f"missing L3 artifact {_rel(path)}")
    errors.extend(_validate_layer_log(L3_ROOT, "L3"))
    return errors


def validate_l1_artifacts() -> list[str]:
    errors: list[str] = []
    for rel in L1_REQUIRED:
        path = L1_ROOT / rel
        if not path.is_file():
            errors.append(f"missing L1 artifact {_rel(path)}")
    log_path = L1_ROOT / "layer_decision_log.jsonl"
    errors.extend(_validate_layer_log(L1_ROOT, "L1"))
    matrix = ROOT / ".ai/context/agent_work/T417/model_layers/batch2/decision_transparency/batch_comparison_matrix.yaml"
    if not matrix.is_file():
        errors.append(f"missing {_rel(matrix)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors: list[str] = []
    errors.extend(validate_policy())
    errors.extend(validate_batch2_manifest())
    errors.extend(validate_l1_artifacts())
    manifest_layers = _read_yaml(BATCH2_MANIFEST).get("layers", {}) if BATCH2_MANIFEST.is_file() else {}
    errors.extend(validate_l2_artifacts(manifest_layers))
    errors.extend(validate_l3_artifacts(manifest_layers))
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    layers_done = ["L1"]
    if manifest_layers.get("L2_codex", {}).get("status") == "complete":
        layers_done.append("L2")
    if manifest_layers.get("L3_claude", {}).get("status") == "complete":
        layers_done.append("L3")
    print(f"OK: scratch multi-model ladder (batch2 {'+'.join(layers_done)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
