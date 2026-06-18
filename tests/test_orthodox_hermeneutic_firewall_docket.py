from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_orthodox_hermeneutic_firewall_docket as validator


def test_orthodox_firewall_validates_current_repo() -> None:
    data = validator.validate_orthodox_firewall()

    assert data["object_type"] == "orthodox_hermeneutic_firewall_docket"
    assert data["affirmations"]["orthodoxy_boundary"] == "Nicene/Chalcedonian orthodox Christianity"
    assert data["authority"]["records_orthodox_firewall"] is True
    assert data["authority"]["authorizes_liberal_critical_default"] is False
    assert data["authority"]["authorizes_denominational_system_as_chunk_authority"] is False
    assert "FIREWALL-ORTH-005" in {item["rule_id"] for item in data["anti_smuggling_rules"]}


def test_orthodox_firewall_rejects_denominational_chunk_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_orthodox_firewall())
    data["authority"]["authorizes_denominational_system_as_chunk_authority"] = True
    candidate = tmp_path / "firewall.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.OrthodoxFirewallError, match="denominational_system"):
        validator.validate_orthodox_firewall(candidate)


def test_orthodox_firewall_rejects_lost_creedal_boundary(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_orthodox_firewall())
    data["affirmations"]["orthodoxy_boundary"] = "generic"
    candidate = tmp_path / "firewall.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.OrthodoxFirewallError, match="orthodoxy_boundary"):
        validator.validate_orthodox_firewall(candidate)
