from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_t450_bible_edge_taxonomy.py"
CONTROL = ROOT / ".ai" / "control" / "bible_edge_taxonomy_research_program.yaml"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_t450", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_t450_validator_passes_current_contract():
    module = load_validator()
    assert module.main() == 0


def test_t450_requires_high_risk_edge_lanes():
    module = load_validator()
    data = yaml.safe_load(CONTROL.read_text(encoding="utf-8"))
    data["edge_family_lanes"] = [
        lane for lane in data["edge_family_lanes"] if lane["lane_id"] != "prophecy_apocalyptic"
    ]
    with pytest.raises(SystemExit):
        module.validate_control(data)


def test_t450_fails_if_graph_generation_authorized():
    module = load_validator()
    data = yaml.safe_load(CONTROL.read_text(encoding="utf-8"))
    data["authority_boundary"]["generates_graph_edges"] = True
    with pytest.raises(SystemExit):
        module.validate_control(data)


def test_t450_requires_rust_not_decide_theology():
    module = load_validator()
    data = yaml.safe_load(CONTROL.read_text(encoding="utf-8"))
    data["future_rust_validator_lane"]["rust_forbidden_for"] = ["resolving textual variants"]
    with pytest.raises(SystemExit):
        module.validate_control(data)
