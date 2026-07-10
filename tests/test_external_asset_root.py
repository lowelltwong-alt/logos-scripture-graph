from __future__ import annotations

import os
from pathlib import Path

from scripts import guard_primary_witness_acquisition as guard
from scripts import validate_external_asset_root as root_validator


def test_missing_env_blocks_acquisition_gate() -> None:
    os.environ.pop("LOGOS_EXTERNAL_ASSET_ROOT", None)
    result = root_validator.validate_external_asset_root(require_env=True)
    assert not result["ok"]
    assert any("not set" in err for err in result["errors"])


def test_unsafe_path_inside_repo_fails(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parent.parent
    result = root_validator.validate_external_asset_root(root=repo / "data", require_env=False)
    assert not result["ok"]


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
