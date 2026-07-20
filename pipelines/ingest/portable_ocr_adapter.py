"""Fail-closed Logos admission adapter for the portable OCR candidate.

This module validates metadata and emits an execution *plan*. It deliberately
does not open the input, run OCR, download a benchmark, or write Scripture data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Mapping


class OcrAdmissionError(ValueError):
    """Raised when an OCR request crosses an authority or storage boundary."""


@dataclass(frozen=True)
class OcrExecutionPlan:
    source_id: str
    use_class: str
    input_path: Path
    output_root: Path
    engine_ids: tuple[str, ...]
    payload_access_authorized: bool
    execution_authorized: bool
    stage: str
    scripture_promotion_authorized: bool = False


def _sha256(value: Any, field: str) -> str:
    text = str(value or "")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", text):
        raise OcrAdmissionError(f"{field} must be a 64-character hexadecimal SHA-256")
    return text.lower()


def _rights_record(request: Mapping[str, Any]) -> Mapping[str, Any]:
    record = request.get("rights_record")
    if not isinstance(record, Mapping):
        raise OcrAdmissionError("a structured rights_record is required")
    if record.get("status") != "approved" or not str(record.get("decision_id", "")).strip():
        raise OcrAdmissionError("rights_record must contain an approved status and decision_id")
    _sha256(record.get("record_sha256"), "rights_record.record_sha256")
    return record


def _resolved_external(path: str, external_root: Path, repo_root: Path) -> Path:
    candidate = Path(path).expanduser().resolve()
    external = external_root.expanduser().resolve()
    repo = repo_root.resolve()
    try:
        candidate.relative_to(external)
    except ValueError as exc:
        raise OcrAdmissionError("OCR payload path must be under LOGOS_EXTERNAL_ASSET_ROOT") from exc
    try:
        candidate.relative_to(repo)
    except ValueError:
        pass
    else:
        raise OcrAdmissionError("OCR payloads may not be stored inside the Logos repository")
    if "onedrive" in {part.casefold() for part in candidate.parts}:
        raise OcrAdmissionError("OCR payloads may not be stored under OneDrive")
    return candidate


def build_execution_plan(
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    repo_root: Path,
    external_root: Path | None,
) -> OcrExecutionPlan:
    """Validate a request and return a non-executing, metadata-only plan."""

    required = ("source_id", "use_class", "input_path", "output_root", "engine_ids")
    missing = [field for field in required if not request.get(field)]
    if missing:
        raise OcrAdmissionError(f"missing required OCR admission fields: {', '.join(missing)}")
    if external_root is None:
        raise OcrAdmissionError("LOGOS_EXTERNAL_ASSET_ROOT is required")

    use_class = str(request["use_class"])
    allowed = set(policy["logos_adapter"]["permitted_use_classes"])
    if use_class not in allowed:
        raise OcrAdmissionError(f"unsupported OCR use class: {use_class}")

    input_path = _resolved_external(str(request["input_path"]), external_root, repo_root)
    output_root = _resolved_external(str(request["output_root"]), external_root, repo_root)
    engines = tuple(str(value) for value in request["engine_ids"])
    if len(set(engines)) < int(policy["portable_core"]["minimum_independent_engines"]):
        raise OcrAdmissionError("at least two genuinely distinct OCR engine identities are required")

    authority = policy["authority"]
    if use_class == "synthetic_fixture":
        authorized = bool(authority["synthetic_fixture_validation_authorized"])
    elif use_class == "external_benchmark":
        benchmark_id = str(request.get("benchmark_id", ""))
        if benchmark_id != "induocr":
            raise OcrAdmissionError("only the registered InduOCR benchmark profile is recognized")
        benchmark = policy["benchmarks"]["induocr"]
        rights = _rights_record(request)
        if request.get("benchmark_revision") != benchmark["pinned_huggingface_revision"]:
            raise OcrAdmissionError("InduOCR benchmark revision does not match the registered revision")
        _sha256(request.get("benchmark_manifest_sha256"), "benchmark_manifest_sha256")
        authorized = bool(
            benchmark["enabled"]
            and authority["induocr_download_authorized"]
            and authority["induocr_execution_authorized"]
            and rights
        )
    else:
        rights = _rights_record(request)
        _sha256(request.get("content_sha256"), "content_sha256")
        authorized = bool(
            authority["manuscript_ocr_execution_authorized"]
            and rights
        )

    if not authorized:
        raise OcrAdmissionError(
            "OCR execution is not authorized for this use class; obtain the required rights and owner gate"
        )
    return OcrExecutionPlan(
        source_id=str(request["source_id"]),
        use_class=use_class,
        input_path=input_path,
        output_root=output_root,
        engine_ids=engines,
        payload_access_authorized=False,
        execution_authorized=False,
        stage="preliminary_metadata_only",
    )
