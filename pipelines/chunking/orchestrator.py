#!/usr/bin/env python3
"""T310 Increment 2 chunking orchestrator shim.

This is intentionally only a byte-identical wrapper around the current Pass-2
chunker path. It does not route by form, consume form detector output, or apply
specialized skills. Route metadata is emitted only to a separate JSONL ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.chunking import chunker  # noqa: E402
DEFAULT_APPROVED_SKILLS = ROOT / "registry" / "chunking" / "approved-skills.json"
DEFAULT_SKILL_ID = "monolith-pass2-v1"
DEFAULT_SOURCE_CORPUS = "eng-web_usfm"
DEFAULT_SOURCE_TEXT_ID = "eng-web"
ROUTE_MODE = "monolith_pass2"


@dataclass(frozen=True)
class OrchestratorResult:
    chunks_path: Path
    context_path: Path | None
    route_ledger_path: Path | None
    chunk_count: int
    context_count: int
    output_hash: str
    context_output_hash: str | None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_path(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def input_manifest_hash(files: dict[str, Path | None]) -> str:
    entries: list[dict[str, str | None]] = []
    for name in sorted(files):
        path = files[name]
        entries.append({
            "name": name,
            "path": normalized_path(path),
            "sha256": sha256_file(path) if path and path.exists() else None,
        })
    manifest = json.dumps({"inputs": entries}, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(manifest.encode("utf-8"))


def load_skill_version(registry_path: Path, skill_id: str) -> str:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for skill in registry.get("skills", []):
        if skill.get("skill_id") == skill_id:
            return skill.get("version", "unknown")
    raise ValueError(f"Skill {skill_id!r} not found in {registry_path}")


def write_jsonl(records: list[dict[str, Any]], out_path: Path) -> None:
    # Keep serialization byte-for-byte aligned with chunker.py.
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_route_ledger(record: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def run_monolith_pass2(
    *,
    passages: Path,
    witnesses: Path,
    out: Path,
    boundary_claims: Path | None,
    footnotes: Path | None,
    crossrefs: Path | None,
    genres_path: Path,
    policy_path: Path,
    context_out: Path | None,
    route_ledger: Path | None,
    registry_path: Path,
    skill_id: str,
    source_corpus: str,
    source_text_id: str,
) -> OrchestratorResult:
    """Delegate to the existing Pass-2 chunker path and optionally write ledger."""
    policy_version = chunker.read_policy_version(policy_path)
    budgets = chunker.load_budgets(policy_path)
    genres, default_genre = chunker.load_genres(genres_path)
    footnotes_by_osis = chunker.index_by_osis(footnotes, "id") if footnotes else {}
    crossrefs_by_osis = chunker.index_by_osis(crossrefs, "id") if crossrefs else {}

    units = chunker.build_units(passages, witnesses, boundary_claims)
    chunks, packets = chunker.chunk_corpus(
        units,
        genres,
        default_genre,
        budgets,
        policy_version,
        footnotes_by_osis,
        crossrefs_by_osis,
    )

    write_jsonl(chunks, out)
    if context_out and packets:
        write_jsonl(packets, context_out)

    output_hash = sha256_file(out)
    context_hash = sha256_file(context_out) if context_out and packets and context_out.exists() else None

    if route_ledger:
        registry_hash = sha256_file(registry_path)
        ledger = {
            "type": "ChunkingRouteLedger",
            "run_id": f"chunk-orchestrator-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            "source_corpus": source_corpus,
            "source_text_id": source_text_id,
            "chunking_policy_version": policy_version,
            "registry_surface_sha": registry_hash,
            "route_mode": ROUTE_MODE,
            "skill_id": skill_id,
            "skill_version": load_skill_version(registry_path, skill_id),
            "registry_ref": normalized_path(registry_path),
            "input_hash": input_manifest_hash({
                "approved_skills_registry": registry_path,
                "boundary_claims": boundary_claims,
                "crossrefs": crossrefs,
                "footnotes": footnotes,
                "genres": genres_path,
                "passages": passages,
                "policy": policy_path,
                "witnesses": witnesses,
            }),
            "output_hash": output_hash,
            "context_output_hash": context_hash,
            "created_at": utc_now(),
            "validation_status": "byte_identical_pending",
            "form_based_routing_enabled": False,
            "detect_form_consumed": False,
        }
        write_route_ledger(ledger, route_ledger)

    return OrchestratorResult(
        chunks_path=out,
        context_path=context_out if context_out and packets and context_out.exists() else None,
        route_ledger_path=route_ledger,
        chunk_count=len(chunks),
        context_count=len(packets),
        output_hash=output_hash,
        context_output_hash=context_hash,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="T310 byte-identical chunking orchestrator shim")
    parser.add_argument("--passages", required=True)
    parser.add_argument("--witnesses", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--boundary-claims", default=None)
    parser.add_argument("--footnotes", default=None)
    parser.add_argument("--crossrefs", default=None)
    parser.add_argument("--genres", default=str(chunker.DEFAULT_GENRES))
    parser.add_argument("--policy", default=str(chunker.DEFAULT_POLICY))
    parser.add_argument("--context-out", default=None)
    parser.add_argument("--route-ledger", default=None)
    parser.add_argument("--approved-skills", default=str(DEFAULT_APPROVED_SKILLS))
    parser.add_argument("--skill-id", default=DEFAULT_SKILL_ID)
    parser.add_argument("--source-corpus", default=DEFAULT_SOURCE_CORPUS)
    parser.add_argument("--source-text-id", default=DEFAULT_SOURCE_TEXT_ID)
    args = parser.parse_args()

    result = run_monolith_pass2(
        passages=Path(args.passages),
        witnesses=Path(args.witnesses),
        out=Path(args.out),
        boundary_claims=Path(args.boundary_claims) if args.boundary_claims else None,
        footnotes=Path(args.footnotes) if args.footnotes else None,
        crossrefs=Path(args.crossrefs) if args.crossrefs else None,
        genres_path=Path(args.genres),
        policy_path=Path(args.policy),
        context_out=Path(args.context_out) if args.context_out else None,
        route_ledger=Path(args.route_ledger) if args.route_ledger else None,
        registry_path=Path(args.approved_skills),
        skill_id=args.skill_id,
        source_corpus=args.source_corpus,
        source_text_id=args.source_text_id,
    )
    print(
        f"Wrote {result.chunk_count} chunks to {result.chunks_path} "
        f"(route mode {ROUTE_MODE}); {result.context_count} context packets"
    )
    if result.route_ledger_path:
        print(f"Wrote route ledger to {result.route_ledger_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
