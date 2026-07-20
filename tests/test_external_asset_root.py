from __future__ import annotations

import os
from pathlib import Path

import pytest

from scripts import guard_primary_witness_acquisition as guard
from scripts import validate_external_asset_root as root_validator


def test_missing_env_blocks_acquisition_gate() -> None:
    os.environ.pop("LOGOS_EXTERNAL_ASSET_ROOT", None)
    result = root_validator.validate_external_asset_root(require_env=True)
    assert not result["ok"]
    assert any("not set" in err for err in result["errors"])


def test_owner_authorization_is_narrow_and_exact() -> None:
    result = root_validator.validate_owner_authorization()
    assert result["ok"], result["errors"]
    approval = result["approval"]
    assert approval["exact_private_quarantine_root"] == r"C:\LogosExternal"
    assert approval["authorized_actions"] == ["record_exact_path", "preflight_exact_path"]
    assert approval["environment_binding"]["persisted_by_task"] is False
    assert approval["root_mutation"]["performed_by_task"] is False
    assert "downloads" in approval["non_authorizations"]
    assert "theology_or_interpretation_authority" in approval["non_authorizations"]


def test_approved_root_preflight_never_authorizes_acquisition() -> None:
    approved_root = Path(r"C:\LogosExternal")
    if not approved_root.exists():
        pytest.skip("live private quarantine root exists only on the approved Windows host")
    result = root_validator.validate_approved_external_asset_root(
        root=approved_root,
        require_env=False,
    )
    assert result["ok"], result["errors"]
    assert result["storage_preflight_passed"] is True
    assert result["acquisition_allowed"] is False
    assert result["download_authorized"] is False
    assert result["checks"]["env_var_set"] is False
    assert result["checks"]["path_override_supplied"] is True


def test_storage_only_approval_keeps_acquisition_gate_closed(monkeypatch) -> None:
    approved_root = Path(r"C:\LogosExternal")
    if not approved_root.exists():
        pytest.skip("live private quarantine root exists only on the approved Windows host")
    monkeypatch.setenv("LOGOS_EXTERNAL_ASSET_ROOT", str(approved_root))
    with pytest.raises(RuntimeError, match="download is not authorized"):
        root_validator.assert_acquisition_gate_open()


def test_unapproved_root_fails_even_when_filesystem_checks_pass(tmp_path: Path) -> None:
    result = root_validator.validate_approved_external_asset_root(
        root=tmp_path,
        require_env=False,
    )
    assert not result["ok"]
    assert any("does not match owner-approved root" in error for error in result["errors"])


def test_missing_optional_environment_stays_green_but_not_preflighted(monkeypatch) -> None:
    monkeypatch.delenv("LOGOS_EXTERNAL_ASSET_ROOT", raising=False)
    result = root_validator.validate_approved_external_asset_root(require_env=False)
    assert result["ok"], result["errors"]
    assert result["storage_preflight_passed"] is False
    assert result["acquisition_allowed"] is False
    assert result["download_authorized"] is False


def test_unsafe_path_inside_repo_fails(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parent.parent
    result = root_validator.validate_external_asset_root(root=repo / "data", require_env=False)
    assert not result["ok"]


def test_unsafe_path_inside_shared_workspace_fails(tmp_path: Path) -> None:
    external_root = tmp_path / "primary-assets"
    external_root.mkdir()
    result = root_validator.validate_external_asset_root(
        root=external_root,
        require_env=False,
        min_budget_bytes=0,
        workspace_root=tmp_path,
    )
    assert not result["ok"]
    assert any("shared workspace" in err for err in result["errors"])


def test_guard_download_blocked_in_wave0(tmp_path: Path, monkeypatch) -> None:
    external_root = tmp_path / "logos-external"
    external_root.mkdir()
    monkeypatch.setenv("LOGOS_EXTERNAL_ASSET_ROOT", str(external_root))
    result = guard.guard_download(
        source_id="codex_sinaiticus_xml",
        planned_bytes=1000,
        rights_status="metadata_only",
    )
    assert not result["ok"]
