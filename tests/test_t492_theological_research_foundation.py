from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/validate_t492_theological_research_foundation.py"
CONTROL = ROOT / ".ai/control/t492_theological_research_foundation.yaml"


def module():
    spec = importlib.util.spec_from_file_location("validate_t492", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(loaded)
    return loaded


def data():
    return yaml.safe_load(CONTROL.read_text(encoding="utf-8"))


def test_current_foundation_passes():
    assert module().main() == 0


def test_rejects_graph_authority():
    candidate = data()
    candidate["authority"]["graph_edges_or_predicate_promotion"] = True
    with pytest.raises(SystemExit):
        module().validate(candidate)


def test_requires_all_dossier_lanes():
    candidate = data()
    candidate["dossier_lane_map"].pop()
    with pytest.raises(SystemExit):
        module().validate(candidate)


def test_requires_complete_unresolved_questions():
    candidate = data()
    del candidate["hard_unsolved_question_register"]["questions"][0]["competing_options"]
    with pytest.raises(SystemExit):
        module().validate(candidate)


def test_future_tasks_remain_uncreated():
    candidate = data()
    candidate["future_tasks"][0]["create_now"] = True
    with pytest.raises(SystemExit):
        module().validate(candidate)
