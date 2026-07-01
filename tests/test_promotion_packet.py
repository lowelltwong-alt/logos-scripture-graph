"""Tests for promotion packet validator."""
from pathlib import Path

import yaml

from scripts.validate_promotion_packet import validate_promotion_packet

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / ".ai" / "scratch" / "submissions" / "_template" / "promotion_packet.yaml"


def _sample_packet() -> dict:
    text = TEMPLATE.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        body = parts[1] + "\n" + parts[2] if len(parts) == 3 else parts[1]
    else:
        body = text
    data = yaml.safe_load(body)
    assert isinstance(data, dict)
    data["submission_id"] = "SUB-001-test"
    data["risk_summary"] = {"high": [], "medium": ["example"], "low": ["wording"]}
    return data


def test_valid_promotion_packet(tmp_path: Path) -> None:
    path = tmp_path / "promotion_packet.yaml"
    path.write_text(yaml.safe_dump(_sample_packet()), encoding="utf-8")
    assert validate_promotion_packet(path) == []


def test_template_submission_id_rejected() -> None:
    errors = validate_promotion_packet(TEMPLATE)
    assert any("template placeholder" in e for e in errors)
