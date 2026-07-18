from __future__ import annotations

from scripts import validate_pre_download_readiness as validator


def test_pre_download_readiness_passes() -> None:
    result = validator.validate_pre_download_readiness()
    assert result["ok"], result["errors"]


def test_readiness_rejects_acquisition_authorization() -> None:
    original = validator.PACKET.read_text(encoding="utf-8")
    try:
        validator.PACKET.write_text(
            original.replace("binary_acquisition_authorized: false", "binary_acquisition_authorized: true"),
            encoding="utf-8",
        )
        result = validator.validate_pre_download_readiness()
        assert not result["ok"]
        assert any("binary_acquisition_authorized" in error for error in result["errors"])
    finally:
        validator.PACKET.write_text(original, encoding="utf-8")


def test_readiness_rejects_broadened_root_authorization() -> None:
    original = validator.PACKET.read_text(encoding="utf-8")
    try:
        validator.PACKET.write_text(
            original.replace(
                "authorized_actions: [record_exact_path, preflight_exact_path]",
                "authorized_actions: [record_exact_path, preflight_exact_path, download]",
            ),
            encoding="utf-8",
        )
        result = validator.validate_pre_download_readiness()
        assert not result["ok"]
        assert any("record-and-preflight only" in error for error in result["errors"])
    finally:
        validator.PACKET.write_text(original, encoding="utf-8")
