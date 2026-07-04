from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t430_original_language_evidence_substrate as validator


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".ai/control/original_language_evidence_substrate.yaml"


def test_t430_original_language_evidence_substrate_validates_current_repo() -> None:
    data = validator.validate_t430_original_language_evidence_substrate()

    assert data["authority"]["authorizes_source_language_truth"] is False
    assert data["authority"]["authorizes_allowlisted_raw_downloads_via_t431"] is True
    assert "strongs_number_as_theology_authority" in data["non_authorizations"]


def _write_minimal_repo(tmp_path: Path, control: dict) -> Path:
    root = tmp_path
    (root / ".ai/control").mkdir(parents=True)
    (root / ".ai/context/agent_work/T431").mkdir(parents=True)
    (root / "docs/roadmap").mkdir(parents=True)
    (root / ".ai/control/original_language_evidence_substrate.yaml").write_text(
        yaml.safe_dump(control, sort_keys=False),
        encoding="utf-8",
    )
    (root / ".ai/control/original_language_source_allowlist.yaml").write_text(
        "object_type: original_language_source_allowlist\n",
        encoding="utf-8",
    )
    (root / ".ai/context/agent_work/T431/dad_preflight.md").write_text(
        "Status: dad_bridge_not_present_on_origin_main\n",
        encoding="utf-8",
    )
    (root / "docs/roadmap/T431_ORIGINAL_LANGUAGE_RAW_INTAKE.md").write_text(
        "Strong's numbers are hints. Oldest witness is evidence. Editorial layers. "
        "Variants are never silently normalized. No preferred readings.\n",
        encoding="utf-8",
    )
    (root / "docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md").write_text(
        "Owner Decision Menu. Greek/Hebrew-to-English alignment bridge. "
        "Manuscript witness chain. Variant and copying-error ledger. Early creed lane. "
        "Integrated original-language evidence workbench. Chain-of-custody and minute-error "
        "records. Claims about months after the resurrection require frontier review.\n",
        encoding="utf-8",
    )
    return root


def test_t430_validator_rejects_source_language_truth_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(yaml.safe_load(CONTROL.read_text(encoding="utf-8")))
    data["authority"]["authorizes_source_language_truth"] = True
    root = _write_minimal_repo(tmp_path, data)

    with pytest.raises(validator.T430EvidenceSubstrateError, match="authorizes_source_language_truth"):
        validator.validate_t430_original_language_evidence_substrate(root)


def test_t430_validator_rejects_missing_strongs_non_authorization(tmp_path: Path) -> None:
    data = copy.deepcopy(yaml.safe_load(CONTROL.read_text(encoding="utf-8")))
    data["non_authorizations"].remove("strongs_number_as_theology_authority")
    root = _write_minimal_repo(tmp_path, data)

    with pytest.raises(validator.T430EvidenceSubstrateError, match="strongs_number_as_theology_authority"):
        validator.validate_t430_original_language_evidence_substrate(root)


def test_t430_validator_rejects_missing_goal_option(tmp_path: Path) -> None:
    data = copy.deepcopy(yaml.safe_load(CONTROL.read_text(encoding="utf-8")))
    data["goal_options"] = [
        option
        for option in data["goal_options"]
        if option["option_id"] != "option_4_early_creed_lane"
    ]
    root = _write_minimal_repo(tmp_path, data)

    with pytest.raises(validator.T430EvidenceSubstrateError, match="exactly five"):
        validator.validate_t430_original_language_evidence_substrate(root)


def test_t430_validator_rejects_goal_option_authority_drift(tmp_path: Path) -> None:
    data = copy.deepcopy(yaml.safe_load(CONTROL.read_text(encoding="utf-8")))
    for option in data["goal_options"]:
        if option["option_id"] == "option_2_manuscript_custody_chain":
            option["authority_limit"] = ""
    root = _write_minimal_repo(tmp_path, data)

    with pytest.raises(validator.T430EvidenceSubstrateError, match="authority_limit"):
        validator.validate_t430_original_language_evidence_substrate(root)
