"""Replaceable, disabled-by-default local OCR runtime adapters."""

from __future__ import annotations

import csv
import io
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Protocol

from .contracts import ContractError, sha256_file


class OcrEngine(Protocol):
    engine_id: str
    diversity_signature: tuple[str, ...]
    def recognize(self, source: Path) -> dict[str, Any]: ...


def _validate_identity(manifest: dict[str, Any]) -> tuple[str, ...]:
    fields = ("engine_family", "model_id", "model_sha256", "runtime_id", "executable_sha256")
    missing = [field for field in fields if not manifest.get(field)]
    if missing:
        raise ContractError(f"engine identity missing: {', '.join(missing)}")
    for field in ("model_sha256", "executable_sha256"):
        if not re.fullmatch(r"[0-9a-fA-F]{64}", str(manifest[field])):
            raise ContractError(f"{field} must be 64 hexadecimal characters")
    return tuple(str(manifest[field]) for field in fields)


def _verify(manifest: dict[str, Any]) -> Path:
    if manifest.get("enabled") is not True:
        raise ContractError(f"engine is disabled: {manifest['engine_id']}")
    evidence = Path(manifest.get("model_path") or manifest.get("model_evidence_path") or "")
    if not evidence.is_file() or sha256_file(evidence) != manifest["model_sha256"]:
        raise ContractError("engine model/model-evidence hash mismatch")
    executable = Path(manifest.get("executable") or (manifest.get("command") or [""])[0])
    if not executable.is_file() or sha256_file(executable) != manifest["executable_sha256"]:
        raise ContractError("engine executable hash mismatch")
    return executable


class CommandJsonEngine:
    """Run an argv-only local command whose final stdout line is a JSON object."""
    def __init__(self, manifest: dict[str, Any]):
        self.manifest, self.engine_id = manifest, str(manifest["engine_id"])
        self.diversity_signature = _validate_identity(manifest)

    def recognize(self, source: Path) -> dict[str, Any]:
        _verify(self.manifest)
        command = self.manifest.get("command")
        if not isinstance(command, list) or not command:
            raise ContractError("command_json requires a non-empty argv list")
        argv = [str(part).replace("{input}", str(source.resolve())) for part in command]
        result = subprocess.run(argv, check=True, capture_output=True, text=True, shell=False,
                                timeout=int(self.manifest.get("timeout_seconds", 180)))
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        try:
            value = json.loads(lines[-1])
        except (IndexError, json.JSONDecodeError) as exc:
            raise ContractError("engine returned no valid JSON result") from exc
        if not isinstance(value, dict) or not isinstance(value.get("text"), str):
            raise ContractError("engine JSON result requires string field 'text'")
        return value


class TesseractEngine:
    def __init__(self, manifest: dict[str, Any]):
        self.manifest, self.engine_id = manifest, str(manifest["engine_id"])
        self.diversity_signature = _validate_identity(manifest)

    def recognize(self, source: Path) -> dict[str, Any]:
        executable = _verify(self.manifest)
        base = [str(executable), str(source.resolve()), "stdout", "-l", str(self.manifest.get("language", "eng")),
                "--oem", "1", "--psm", str(self.manifest.get("psm", 3))]
        common = {"check": True, "capture_output": True, "text": True, "shell": False,
                  "timeout": int(self.manifest.get("timeout_seconds", 180))}
        text_run, tsv_run = subprocess.run(base, **common), subprocess.run(base + ["tsv"], **common)
        words, confidences = [], []
        for row in csv.DictReader(io.StringIO(tsv_run.stdout), delimiter="\t"):
            if row.get("level") != "5" or not (row.get("text") or "").strip():
                continue
            confidence = None if row.get("conf") in {None, "", "-1"} else float(row["conf"]) / 100
            if confidence is not None:
                confidences.append(confidence)
            words.append({"text": row["text"], "confidence": confidence,
                          "box": [int(row["left"]), int(row["top"]), int(row["width"]), int(row["height"])]})
        return {"text": text_run.stdout, "words": words,
                "raw_confidence": sum(confidences) / len(confidences) if confidences else None,
                "confidence_is_calibrated": False}


class WindowsMediaEngine:
    def __init__(self, manifest: dict[str, Any]):
        self.manifest, self.engine_id = manifest, str(manifest["engine_id"])
        self.diversity_signature = _validate_identity(manifest)

    def recognize(self, source: Path) -> dict[str, Any]:
        executable = _verify(self.manifest)
        helper = Path(__file__).parent / "adapters" / "windows_media_ocr.ps1"
        if sha256_file(helper) != self.manifest.get("helper_sha256"):
            raise ContractError("bundled Windows OCR helper hash mismatch")
        result = subprocess.run(
            [str(executable), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(helper),
             "-ImagePath", str(source.resolve()), "-Language", str(self.manifest.get("language", "en-US"))],
            check=True, capture_output=True, text=True, shell=False,
            timeout=int(self.manifest.get("timeout_seconds", 180)),
        )
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        try:
            value = json.loads(lines[-1])
        except (IndexError, json.JSONDecodeError) as exc:
            raise ContractError("Windows Media OCR returned no valid JSON") from exc
        value.update({"raw_confidence": None, "confidence_is_calibrated": False})
        return value


def build_engine(manifest: dict[str, Any]) -> OcrEngine:
    adapters = {"command_json": CommandJsonEngine, "tesseract_cli": TesseractEngine,
                "windows_media": WindowsMediaEngine}
    try:
        return adapters[str(manifest.get("adapter"))](manifest)
    except KeyError as exc:
        raise ContractError(f"unknown engine adapter: {manifest.get('adapter')}") from exc
