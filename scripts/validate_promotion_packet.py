#!/usr/bin/env python3
"""Validate promotion packet structure before scratch-to-main PR."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "scratch_lane_policy.yaml"


class PromotionPacketError(ValueError):
    """Raised when a promotion packet is incomplete or unsafe."""


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
        raise PromotionPacketError(f"{_rel(path)}: expected YAML mapping")
    return data


def _load_policy() -> dict[str, Any]:
    return _read_yaml(POLICY)


def validate_promotion_packet(
    packet_path: Path,
    policy: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not packet_path.is_file():
        return [f"missing packet {_rel(packet_path)}"]

    if policy is None:
        policy = _load_policy()

    packet = _read_yaml(packet_path)
    spec = policy.get("promotion_packet", {})
    required_top = spec.get("required_top_level_fields", [])
    for field in required_top:
        if field not in packet:
            errors.append(f"missing required field: {field}")

    if packet.get("object_type") != "promotion_packet":
        errors.append("object_type must be promotion_packet")

    submission_id = str(packet.get("submission_id", ""))
    if submission_id.endswith("-template") or submission_id == "SUB-000-template":
        errors.append("submission_id must not be the template placeholder")

    risk = packet.get("risk_summary", {})
    if not isinstance(risk, dict):
        errors.append("risk_summary must be a mapping")
    else:
        for bucket in spec.get("risk_summary_required_buckets", []):
            if bucket not in risk or not isinstance(risk[bucket], list):
                errors.append(f"risk_summary.{bucket} must be a list")

    decisions = packet.get("decisions", [])
    if not isinstance(decisions, list) or not decisions:
        errors.append("decisions must be a non-empty list")
    else:
        required_decision = set(spec.get("decision_entry_required_fields", []))
        for idx, entry in enumerate(decisions):
            if not isinstance(entry, dict):
                errors.append(f"decisions[{idx}] must be a mapping")
                continue
            missing = required_decision - set(entry)
            if missing:
                errors.append(f"decisions[{idx}] missing: {sorted(missing)}")

    requested = packet.get("requested_promotion")
    allowed = set(spec.get("requested_promotion_allowed_values", []))
    if requested not in allowed:
        errors.append(f"requested_promotion must be one of {sorted(allowed)}")

    high_risk = packet.get("risk_summary", {}).get("high", [])
    if requested in {"reviewed_gold_promotion", "chunk_output_pilot"} and high_risk:
        errors.append("high risk items block gold/output promotion requests")

    non_auth = packet.get("non_authorizations", [])
    if not isinstance(non_auth, list) or not non_auth:
        errors.append("non_authorizations must be a non-empty list")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packet",
        type=Path,
        default=ROOT / ".ai" / "scratch" / "submissions" / "_template" / "promotion_packet.yaml",
        help="Path to promotion_packet.yaml",
    )
    parser.add_argument("--allow-template", action="store_true", help="Validate template without submission_id check")
    args = parser.parse_args()

    errors = validate_promotion_packet(args.packet.resolve())
    if args.allow_template:
        errors = [e for e in errors if "template placeholder" not in e]

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: {_rel(args.packet.resolve())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
