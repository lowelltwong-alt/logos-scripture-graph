#!/usr/bin/env python3
"""Chunking orchestrator shim with a literal-Psalm candidate seam.

The orchestrator routes literal Book of Psalms units through the candidate Psalm
skill while non-target books remain on the current Pass-2 monolith fallback. It
does not consume form detector output. Route metadata is emitted only to a
separate JSONL ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.chunking import chunker  # noqa: E402
DEFAULT_APPROVED_SKILLS = ROOT / "registry" / "chunking" / "approved-skills.json"
DEFAULT_SKILL_TOC = ROOT / "registry" / "chunking" / "skill-toc.json"
DEFAULT_SKILL_GRAPH = ROOT / "registry" / "chunking" / "skill-graph-index.json"
DEFAULT_SKILL_ID = "monolith-pass2-v1"
PSALM_SKILL_ID = "psalm-whole-then-stanza-v1"
PSALM_TARGET_BOOK = "Ps"
PSALM_SKILL_DIR = ROOT / "pipelines" / "chunking" / "skills" / "candidate" / PSALM_SKILL_ID
DEFAULT_SOURCE_CORPUS = "eng-web_usfm"
DEFAULT_SOURCE_TEXT_ID = "eng-web"
ROUTE_MODE = "literal_psalm_candidate_seam"
ROUTE_VALIDATION_STATUS = "t374_additive_parent_overlay_parent_only"
T374_OVERLAY_ID = "chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--1Cor.8.1--1Cor.10.33--T374-OVERLAP-B"
T374_OVERLAY_START = "1Cor.8.1"
T374_OVERLAY_END = "1Cor.10.33"
T374_OVERLAY_REVIEWED_GOLD_CASE_ID = "1cor8_10_parent_only_reviewed_gold"
T374_OVERLAY_OWNER_DECISION_REF = ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml"
T374_OVERLAY_IMPLEMENTATION_MANIFEST = ".ai/control/t374_additive_parent_overlay_manifest.yaml"
T374_OVERLAY_DECISION_REGISTER_ENTRY = "CD-056"
T374_OVERLAY_BOUNDARY_BASIS = [
    "additive_parent_overlay",
    "owner_selected_t374_overlap_b",
    "reviewed_gold_parent_only",
    "route_isolated_exact_pilot",
]


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


def registry_surface_sha(registry_path: Path) -> str:
    """Hash the small committed routing registry surface, not generated outputs."""
    paths = {
        "approved_skills": registry_path,
        "skill_toc": DEFAULT_SKILL_TOC,
        "skill_graph_index": DEFAULT_SKILL_GRAPH,
    }
    return input_manifest_hash(paths)


def load_skill_metadata(skill_id: str) -> dict[str, Any] | None:
    for state in ("approved", "candidate"):
        path = ROOT / "pipelines" / "chunking" / "skills" / state / skill_id / "SKILL_METADATA.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return None


def load_skill_version(registry_path: Path, skill_id: str) -> str:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for skill in registry.get("skills", []):
        if skill.get("skill_id") == skill_id:
            return skill.get("version", "unknown")
    metadata = load_skill_metadata(skill_id)
    if metadata:
        return metadata.get("version", "unknown")
    raise ValueError(f"Skill {skill_id!r} not found in {registry_path}")


def load_psalm_skill_algorithm() -> ModuleType:
    path = PSALM_SKILL_DIR / "algorithm.py"
    spec = importlib.util.spec_from_file_location("psalm_whole_then_stanza_v1_algorithm", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load candidate Psalm skill algorithm from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_jsonl(records: list[dict[str, Any]], out_path: Path) -> None:
    # Keep serialization byte-for-byte aligned with chunker.py.
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_route_ledger(records: list[dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def route_for_book(book: str) -> tuple[str, str]:
    if book == PSALM_TARGET_BOOK:
        return PSALM_SKILL_ID, "literal_book_ps_candidate_seam"
    return DEFAULT_SKILL_ID, "monolith_fallback_non_target_book"


def osis_parts(osis: str) -> tuple[str, int, int]:
    parts = osis.split(".")
    if len(parts) != 3:
        raise ValueError(f"Unsupported OSIS reference for T374 overlay: {osis!r}")
    return parts[0], int(parts[1]), int(parts[2])


def is_t374_overlay_unit(unit: dict[str, Any]) -> bool:
    book, chapter, verse = osis_parts(unit["osis_ref"])
    if book != "1Cor":
        return False
    return (chapter > 8 or (chapter == 8 and verse >= 1)) and (
        chapter < 10 or (chapter == 10 and verse <= 33)
    )


def make_t374_parent_overlay(
    units: list[dict[str, Any]],
    policy_version: str,
    footnotes_by_osis: dict[str, list],
    crossrefs_by_osis: dict[str, list],
) -> dict[str, Any] | None:
    selected = [unit for unit in units if is_t374_overlay_unit(unit)]
    if not selected:
        return None
    first = selected[0]["osis_ref"]
    last = selected[-1]["osis_ref"]
    if first != T374_OVERLAY_START or last != T374_OVERLAY_END:
        raise ValueError(
            "T374 overlay requires the exact parent span "
            f"{T374_OVERLAY_START}-{T374_OVERLAY_END}; observed {first}-{last}"
        )

    text = " ".join(unit["text"].strip() for unit in selected if unit["text"].strip()).strip()
    footnote_refs: list[Any] = []
    crossref_refs: list[Any] = []
    for unit in selected:
        osis = unit["osis_ref"]
        footnote_refs.extend(footnotes_by_osis.get(osis, []))
        crossref_refs.extend(crossrefs_by_osis.get(osis, []))

    return {
        "id": T374_OVERLAY_ID,
        "type": "RetrievalChunk",
        "chunk_kind": "epistles_parent_overlay",
        "genre": "epistles",
        "source_text_id": DEFAULT_SOURCE_TEXT_ID,
        "source_artifact_id": DEFAULT_SOURCE_CORPUS,
        "osis_start": T374_OVERLAY_START,
        "osis_end": T374_OVERLAY_END,
        "text": text,
        "included_text_span_ids": [unit["passage_id"] for unit in selected],
        "boundary_basis": T374_OVERLAY_BOUNDARY_BASIS,
        "footnote_refs": footnote_refs,
        "editorial_crossref_refs": crossref_refs,
        "has_lexeme_alignment": True,
        "chunking_policy_version": policy_version,
        "license": "public-domain",
        "validation": {
            "sentence_ended": chunker.sentence_ended(text),
            "book_boundary_crossed": False,
            "starts_on_heading_or_superscription": bool(
                selected[0]["has_heading"] or selected[0]["has_superscription"]
            ),
            "parent_only_overlay": True,
            "selected_children_empty": True,
        },
        "status": "active",
        "overlay_kind": "additive_parent_only",
        "overlay_status": "owner_selected_t374_overlap_b_implemented",
        "reviewed_gold_case_id": T374_OVERLAY_REVIEWED_GOLD_CASE_ID,
        "owner_decision_ref": T374_OVERLAY_OWNER_DECISION_REF,
        "implementation_manifest": T374_OVERLAY_IMPLEMENTATION_MANIFEST,
        "decision_register_entry": T374_OVERLAY_DECISION_REGISTER_ENTRY,
        "selected_children": [],
        "baseline_chunks_preserved_byte_identical": True,
        "non_truth_bearing_overlay": True,
        "graph_retrieval_truth_authorized": False,
        "child_span_authorized": False,
        "broader_epistle_generalization_authorized": False,
    }


def chunk_routed_corpus(
    units_iter,
    genres: dict[str, str],
    default_genre: str,
    budgets: dict[str, int],
    policy_version: str,
    footnotes_by_osis: dict[str, list],
    crossrefs_by_osis: dict[str, list],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Route literal Psalms through the candidate skill and isolate all others."""
    all_chunks: list[dict[str, Any]] = []
    context_packets: list[dict[str, Any]] = []
    route_records: list[dict[str, Any]] = []
    book_units: list[dict[str, Any]] = []
    current_book: str | None = None
    idx = 1
    psalm_skill = load_psalm_skill_algorithm()

    def process_book(bunits: list[dict[str, Any]], book: str) -> None:
        nonlocal idx
        genre = genres.get(book, default_genre)
        skill_id, route_reason = route_for_book(book)
        first_index = idx
        if skill_id == PSALM_SKILL_ID:
            chunks, idx = psalm_skill.chunk_psalm_book(
                bunits,
                genre,
                budgets,
                policy_version,
                footnotes_by_osis,
                crossrefs_by_osis,
                idx,
            )
        else:
            chunks, idx = chunker.chunk_book(
                bunits,
                genre,
                budgets,
                policy_version,
                footnotes_by_osis,
                crossrefs_by_osis,
                idx,
            )
        all_chunks.extend(chunks)
        route_records.append({
            "type": "ChunkingRouteLedgerRoute",
            "book": book,
            "osis_start": bunits[0]["osis_ref"],
            "osis_end": bunits[-1]["osis_ref"],
            "genre_prior": genre,
            "route_mode": ROUTE_MODE,
            "skill_id": skill_id,
            "route_reason": route_reason,
            "chunk_index_start": first_index,
            "chunk_index_end": idx - 1,
            "chunk_count": len(chunks),
            "form_based_routing_enabled": False,
            "detect_form_consumed": False,
        })

    for unit in units_iter:
        if book_units and unit["book"] != current_book:
            process_book(book_units, current_book)
            book_units = []
        current_book = unit["book"]
        book_units.append(unit)
    if book_units:
        process_book(book_units, current_book)

    prev = None
    for chunk in all_chunks:
        if chunk["genre"] == "epistles":
            head = chunk["text"].lstrip().lower()
            if any(head.startswith(c) for c in chunker.CONTEXT_CONNECTORS):
                context_packets.append(chunker.make_context_packet(chunk, prev))
        prev = chunk
    return all_chunks, context_packets, route_records


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
    enable_t374_overlay: bool = True,
) -> OrchestratorResult:
    """Run the routed chunking path and optionally write a route ledger."""
    policy_version = chunker.read_policy_version(policy_path)
    budgets = chunker.load_budgets(policy_path)
    genres, default_genre = chunker.load_genres(genres_path)
    footnotes_by_osis = chunker.index_by_osis(footnotes, "id") if footnotes else {}
    crossrefs_by_osis = chunker.index_by_osis(crossrefs, "id") if crossrefs else {}

    units = list(chunker.build_units(passages, witnesses, boundary_claims))
    chunks, packets, route_records = chunk_routed_corpus(
        units,
        genres,
        default_genre,
        budgets,
        policy_version,
        footnotes_by_osis,
        crossrefs_by_osis,
    )
    overlays: list[dict[str, Any]] = []
    if enable_t374_overlay:
        overlay = make_t374_parent_overlay(units, policy_version, footnotes_by_osis, crossrefs_by_osis)
        if overlay:
            overlays.append(overlay)
            chunks.extend(overlays)

    write_jsonl(chunks, out)
    if context_out and packets:
        write_jsonl(packets, context_out)

    output_hash = sha256_file(out)
    context_hash = sha256_file(context_out) if context_out and packets and context_out.exists() else None

    if route_ledger:
        registry_hash = registry_surface_sha(registry_path)
        skill_versions = {
            skill: load_skill_version(registry_path, skill)
            for skill in sorted({r["skill_id"] for r in route_records})
        }
        skill_counts = Counter(r["skill_id"] for r in route_records)
        run_id = f"chunk-orchestrator-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        common = {
            "run_id": run_id,
            "source_corpus": source_corpus,
            "source_text_id": source_text_id,
            "chunking_policy_version": policy_version,
            "registry_surface_sha": registry_hash,
            "registry_ref": normalized_path(registry_path),
            "created_at": utc_now(),
            "form_based_routing_enabled": False,
            "detect_form_consumed": False,
        }
        ledger = [{
            "type": "ChunkingRouteLedger",
            "route_mode": ROUTE_MODE,
            "skill_id": DEFAULT_SKILL_ID,
            "skill_version": load_skill_version(registry_path, DEFAULT_SKILL_ID),
            "candidate_skill_ids": [PSALM_SKILL_ID],
            "skills_used": [
                {
                    "skill_id": used_skill,
                    "skill_version": skill_versions[used_skill],
                    "route_count": skill_counts[used_skill],
                }
                for used_skill in sorted(skill_counts)
            ],
            "route_record_count": len(route_records),
            "input_hash": input_manifest_hash({
                "approved_skills_registry": registry_path,
                "boundary_claims": boundary_claims,
                "crossrefs": crossrefs,
                "footnotes": footnotes,
                "genres": genres_path,
                "passages": passages,
                "policy": policy_path,
                "skill_graph_index": DEFAULT_SKILL_GRAPH,
                "skill_toc": DEFAULT_SKILL_TOC,
                "witnesses": witnesses,
            }),
            "output_hash": output_hash,
            "context_output_hash": context_hash,
            "validation_status": ROUTE_VALIDATION_STATUS,
            "t374_additive_overlay_enabled": enable_t374_overlay,
            "t374_additive_overlay_count": len(overlays),
            "t374_additive_overlay_ids": [overlay["id"] for overlay in overlays],
            **common,
        }]
        ledger.extend({
            **record,
            **common,
            "skill_version": skill_versions[record["skill_id"]],
            "validation_status": ROUTE_VALIDATION_STATUS,
        } for record in route_records)
        ledger.extend({
            "type": "ChunkingRouteLedgerOverlay",
            "overlay_id": overlay["id"],
            "overlay_kind": overlay["overlay_kind"],
            "osis_start": overlay["osis_start"],
            "osis_end": overlay["osis_end"],
            "selected_children": overlay["selected_children"],
            "owner_decision_ref": overlay["owner_decision_ref"],
            "decision_register_entry": overlay["decision_register_entry"],
            "reviewed_gold_case_id": overlay["reviewed_gold_case_id"],
            "baseline_chunks_preserved_byte_identical": overlay["baseline_chunks_preserved_byte_identical"],
            "non_truth_bearing_overlay": overlay["non_truth_bearing_overlay"],
            "graph_retrieval_truth_authorized": overlay["graph_retrieval_truth_authorized"],
            "child_span_authorized": overlay["child_span_authorized"],
            **common,
            "validation_status": ROUTE_VALIDATION_STATUS,
        } for overlay in overlays)
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
    parser.add_argument(
        "--disable-t374-overlay",
        action="store_true",
        help="Generate the pre-T374 baseline without the additive 1Cor.8.1-1Cor.10.33 parent overlay.",
    )
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
        enable_t374_overlay=not args.disable_t374_overlay,
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
