import importlib.util
from pathlib import Path
import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/validate_t497_fable_architecture_owner_decisions.py"
CONTROL = ROOT / ".ai/control/t497_fable_architecture_owner_decisions.yaml"


def module():
    spec = importlib.util.spec_from_file_location("t497_validator", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def data():
    return yaml.safe_load(CONTROL.read_text(encoding="utf-8"))


def test_current_record_passes():
    assert module().main() == 0


def test_registration_cannot_be_smuggled_in():
    value = data()
    value["decisions"]["OD-A1"]["registration_authorized"] = True
    with pytest.raises(SystemExit):
        module().validate(value)


def test_influence_threshold_cannot_be_weakened():
    value = data()
    value["decisions"]["OD-A2"]["influence_record_requires_one_of"] = ["E4", "E5"]
    with pytest.raises(SystemExit):
        module().validate(value)


def test_kernel_order_is_binding():
    value = data()
    value["decisions"]["OD-K"]["dependency_order"] = ["LSG-O1A", "LSG-O2A", "LSG-O3A"]
    with pytest.raises(SystemExit):
        module().validate(value)


def test_authority_packets_cannot_be_batch_approved():
    value = data()
    value["decisions"]["OD-Q"]["authority_consequence_batch_approval_allowed"] = True
    with pytest.raises(SystemExit):
        module().validate(value)
