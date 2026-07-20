"""Atomic N-engine OCR evidence pipeline with A/B and governed C."""

from __future__ import annotations

import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .comparison import compare_candidates
from .contracts import ContractError, canonical_sha256, sha256_file, write_json_exclusive
from .engines import OcrEngine
from .routing import route_third_engine


def _candidate(engine: OcrEngine, source: Path, label: str) -> dict[str, Any]:
    result = engine.recognize(source)
    text = str(result.get("text") or "")
    return {"candidate_id": str(uuid.uuid4()), "blind_label": label, "engine_id": engine.engine_id,
            "text": text, "text_sha256": canonical_sha256(text),
            "engine_result": {key: value for key, value in result.items() if key != "text"},
            "not_source_truth": True}


def run_pipeline(source: Path, output_root: Path, engines: list[OcrEngine], policy: dict[str, Any]) -> Path:
    if len(engines) < 2:
        raise ContractError("at least two independently configured engines are required")
    if len({engine.engine_id for engine in engines}) != len(engines):
        raise ContractError("engine identities must be distinct")
    signatures = [getattr(engine, "diversity_signature", None) for engine in engines]
    if any(sig is None for sig in signatures) or len(set(signatures)) != len(signatures):
        raise ContractError("engines require distinct attested family/model/runtime/executable identities")
    if not source.is_file() or source.is_symlink():
        raise ContractError(f"source must be a regular file: {source}")
    output_root.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    final = output_root / run_id
    staging = Path(tempfile.mkdtemp(prefix=f".{run_id}-", dir=output_root))
    try:
        original_hash = sha256_file(source)
        snapshot = staging / f"source{source.suffix.lower()}"
        shutil.copyfile(source, snapshot)
        if sha256_file(snapshot) != original_hash or sha256_file(source) != original_hash:
            raise ContractError("source changed while immutable snapshot was created")
        candidates = [_candidate(engines[0], snapshot, "Candidate A"),
                      _candidate(engines[1], snapshot, "Candidate B")]
        comparison = compare_candidates(candidates)
        route = route_third_engine(comparison, policy)
        if route["run_third_engine"]:
            if len(engines) < 3:
                raise ContractError("policy requires Engine C, but no approved third engine is available")
            candidates.append(_candidate(engines[2], snapshot, "Candidate C"))
            comparison = compare_candidates(candidates)
            route["status"] = "third_engine_completed"
        manifest = {
            "schema": "portable_ocr_run.v1", "run_id": run_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source": {"filename": source.name, "sha256": original_hash}, "policy": policy,
            "candidates": candidates, "comparison": comparison, "routing": route,
            "winner": None, "promoted": False,
            "human_review_required": not comparison["all_candidates_agree"] or policy.get("review_agreements", True),
        }
        write_json_exclusive(staging / "run.json", manifest)
        if sha256_file(snapshot) != original_hash or sha256_file(source) != original_hash:
            raise ContractError("source or immutable snapshot changed during execution")
        staging.rename(final)
        return final
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
