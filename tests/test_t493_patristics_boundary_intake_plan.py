from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/validate_t493_patristics_boundary_intake_plan.py"
CONTROL = ROOT / ".ai/control/t493_patristics_boundary_intake_plan.yaml"

def module():
    spec = importlib.util.spec_from_file_location("validate_t493", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(loaded)
    return loaded

def data(): return yaml.safe_load(CONTROL.read_text(encoding="utf-8"))

def test_current_plan_passes(): assert module().main() == 0

def test_rejects_import_authority():
    candidate = data(); candidate["authority"]["imports_or_downloads_authorized"] = True
    with pytest.raises(SystemExit): module().validate(candidate)

def test_rejects_scripture_repo_destination():
    candidate = data(); candidate["handoff_packet"]["destination"] = "logos-scripture-graph"
    with pytest.raises(SystemExit): module().validate(candidate)

def test_unresolved_question_cannot_become_conclusion():
    candidate = data(); candidate["unresolved_questions"][0]["conclusion"] = "selected"
    with pytest.raises(SystemExit): module().validate(candidate)
