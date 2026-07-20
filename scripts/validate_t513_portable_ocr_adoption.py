"""Validate the T513 portable OCR candidate and its non-authorization gates."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ai" / "control" / "t513_portable_ocr_adoption.yaml"
TASK = ROOT / ".ai" / "tasks" / "T513.task.yaml"
ROADMAP = ROOT / "docs" / "roadmap" / "T513_PORTABLE_OCR_RESEARCH_ADOPTION.md"
CORE = ROOT / "tools" / "portable_ocr"
ADAPTER = ROOT / "pipelines" / "ingest" / "portable_ocr_adapter.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    for path in (POLICY, TASK, ROADMAP, CORE, ADAPTER):
        require(path.exists(), f"required T513 artifact missing: {path.relative_to(ROOT)}")
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    task = yaml.safe_load(TASK.read_text(encoding="utf-8"))
    require(task["id"] == "T513", "task identity drifted")
    require(policy["status"] == "complete_candidate_foundation_only", "portable OCR must remain a completed candidate-only foundation")

    authority = policy["authority"]
    denied = (
        "portable_tool_activation_authorized",
        "induocr_download_authorized",
        "induocr_execution_authorized",
        "induocr_training_authorized",
        "manuscript_ocr_execution_authorized",
        "scripture_truth_promotion_authorized",
        "graph_retrieval_or_vector_truth_change_authorized",
    )
    for key in denied:
        require(authority[key] is False, f"unauthorized T513 capability enabled: {key}")
    indu = policy["benchmarks"]["induocr"]
    require(indu["enabled"] is False, "InduOCR must remain disabled")
    require(indu["download_mode"] == "never_automatic", "InduOCR may never auto-download")
    require(indu["training_use"] == "prohibited", "InduOCR training use must be prohibited")
    require("unresolved" in indu["license_status"], "InduOCR rights uncertainty must stay explicit")
    portable_indu = json.loads((CORE / "benchmarks" / "induocr.profile.json").read_text(encoding="utf-8"))
    require(portable_indu["enabled"] is False, "portable InduOCR profile must remain disabled")
    require(portable_indu["automatic_download"] is False, "portable InduOCR profile may not download")
    require(portable_indu["training_use"] is False, "portable InduOCR profile may not authorize training")
    require(portable_indu["expected_files_and_sha256"] == [], "unapproved InduOCR payload hashes may not be guessed")
    require(policy["storage"]["tracked_payloads_prohibited"] is True, "tracked OCR payloads are prohibited")

    code_paths = [
        path for path in CORE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    ] + [ADAPTER]
    forbidden = ("data/raw", "data/canonical", "write_scripture_graph", "huggingface_hub.snapshot_download")
    combined = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in code_paths).casefold()
    for marker in forbidden:
        require(marker.casefold() not in combined, f"portable OCR code contains forbidden coupling: {marker}")

    manifests = sorted({*CORE.rglob("*MANIFEST*.json"), *CORE.rglob("*manifest*.json")})
    require(manifests, "portable OCR content-hash provenance manifest is missing")
    valid_hashes = 0
    for path in manifests:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        files = record.get("files", [])
        valid_hashes += sum(
            1 for item in files if isinstance(item, dict) and len(str(item.get("sha256", ""))) == 64
        )
        source_hashes = record.get("imported_source_sha256", {})
        if isinstance(source_hashes, dict):
            valid_hashes += sum(1 for value in source_hashes.values() if len(str(value)) == 64)
    require(valid_hashes > 0, "portable OCR provenance manifest has no file hashes")
    require(policy["domain_evaluation"]["authorized_public_domain_or_licensed_gold_required"] is True,
            "domain-specific authorized gold must remain required")
    print(f"T513 portable OCR adoption validation passed: {len(code_paths)} code files, {valid_hashes} provenance hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
