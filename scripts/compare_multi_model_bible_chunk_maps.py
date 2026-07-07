#!/usr/bin/env python3
"""Compare T423 model whole_bible_chunk_map.jsonl files — agreement vs delta."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import (
    SCRATCH_ROOT,
    SpanRange,
    canonical_books,
    compare_book_verse_coverage,
    completed_books,
    discover_model_folders,
    load_chunk_map,
    load_fork_policy,
    load_model_manifest,
    majority_required,
    model_is_complete,
    normalize_span,
    parse_span,
    spans_overlap,
)

COMPARISON_ROOT = SCRATCH_ROOT / "comparison"
STRESS_ATLAS = ROOT / "eval" / "chunking_stress_atlas" / "biblical_chunking_stress_atlas.json"

CODEX_MODEL_ID = "M4_codex_gpt55"
FABLE_MODEL_ID = "M6_fable5"
STALE_MODEL_IDS = {"M2_codex", "M3_claude", "M4_gemini", "M5_composer_alt"}
CONFIDENCE_ORDER = {"low": 0, "medium_low": 1, "medium": 2, "high": 3}
DECISION_STATUSES = {
    "consensus_low_risk_candidate",
    "codex_fable_recommended_candidate",
    "frontier_review_required",
    "owner_decision_required",
    "harness_fix_or_rerun_required",
    "phase2_deferred",
}
HIGH_RISK_BOOKS = {
    "Job",
    "Ps",
    "Prov",
    "Eccl",
    "Song",
    "Isa",
    "Jer",
    "Lam",
    "Ezek",
    "Dan",
    "Hos",
    "Joel",
    "Amos",
    "Obad",
    "Jonah",
    "Mic",
    "Nah",
    "Hab",
    "Zeph",
    "Hag",
    "Zech",
    "Mal",
    "Matt",
    "Mark",
    "Luke",
    "John",
    "Rom",
    "1Cor",
    "2Cor",
    "Gal",
    "Eph",
    "Heb",
    "Jude",
    "Rev",
}
FRONTIER_RISK_FLAGS = {
    "frontier_book",
    "high_risk_book",
    "variant_hot_zone",
    "low_confidence",
    "wj_or_red_letter",
    "notes_or_variant_pressure",
    "poetry_liturgy",
    "prophetic_or_apocalyptic",
    "dense_epistle_argument",
    "sidecar_low_confidence_or_frontier",
}
SIDECAR_FILES = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)
VARIANT_HOT_ZONE_SCOPES = {
    "Mark": ("Mark.16.1-Mark.16.20", "Mark.16.9-Mark.16.20"),
    "John": ("John.7.53-John.8.11",),
    "Acts": ("Acts.8.37", "Acts.15.34", "Acts.24.7"),
    "Rom": ("Rom.16.25-Rom.16.27",),
    "Deut": ("Deut.32.8-Deut.32.9",),
    "Jer": ("Jer.1-Jer.52",),
    "Jude": ("Jude.5-Jude.15",),
    "Dan": ("Dan",),
    "Esth": ("Esth",),
    "1John": ("1John.5.6-1John.5.8",),
}


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_stress_books() -> set[str]:
    if not STRESS_ATLAS.is_file():
        return set()
    data = json.loads(STRESS_ATLAS.read_text(encoding="utf-8"))
    books: set[str] = set()
    for entry in data.get("entries", []):
        book = entry.get("book")
        if isinstance(book, str):
            books.add(book)
    return books


def _load_t417_overlap_books(policy: dict[str, Any]) -> set[str]:
    isolation = policy.get("parallel_path_isolation", {})
    overlap = isolation.get("overlap_books_with_T417_batch2", [])
    if isinstance(overlap, list):
        return {str(b) for b in overlap}
    return set()


def _iter_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.is_file():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                row = json.loads(stripped)
                if isinstance(row, dict):
                    rows.append(row)
    return rows


def _record_decision_id(record: dict[str, Any]) -> str:
    return str(record.get("decision_id") or record.get("chunk_decision_id") or "")


def _confidence_rollup(confidences: list[str]) -> str:
    if not confidences:
        return "medium"
    return min(confidences, key=lambda value: CONFIDENCE_ORDER.get(value, 1))


def _load_sidecar_refs(folder: Path, model_id: str) -> dict[str, list[str]]:
    refs: dict[str, list[str]] = defaultdict(list)
    for filename in SIDECAR_FILES:
        path = folder / filename
        if not path.is_file():
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                row = json.loads(stripped)
                if not isinstance(row, dict):
                    continue
                decision_id = _record_decision_id(row)
                if decision_id:
                    refs[decision_id].append(f"{model_id}:{filename}:{line_no}:{decision_id}")
    return dict(refs)


def _risk_flags_for_records(book: str, records: list[dict[str, Any]], sidecar_refs: list[str]) -> list[str]:
    flags: set[str] = set()
    variant_matches = _variant_hot_zone_matches(book, records)
    if variant_matches:
        flags.add("variant_hot_zone")
    if book in HIGH_RISK_BOOKS:
        flags.add("high_risk_book")
    if book in {"Dan", "Rev"}:
        flags.add("frontier_book")
    if book in {"Isa", "Jer", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal", "Rev"}:
        flags.add("prophetic_or_apocalyptic")
    if book in {"Rom", "1Cor", "2Cor", "Gal", "Eph", "Heb"}:
        flags.add("dense_epistle_argument")
    if sidecar_refs:
        flags.add("sidecar_low_confidence_or_frontier")

    for record in records:
        confidence = str(record.get("confidence", ""))
        if confidence in {"low", "medium_low"}:
            flags.add("low_confidence")
        if record.get("wj_or_red_letter_considered") is True:
            flags.add("wj_or_red_letter")
        if record.get("frontier_flag_considered") is True:
            flags.add("frontier_flag_considered")
        if record.get("strong_or_hebrew_tags_used") is True:
            flags.add("strongs_original_language_metadata")
        lit = str(record.get("literature_type_guess", "")).lower()
        refs = " ".join(str(item).lower() for item in record.get("boundary_evidence_refs", []))
        if any(token in lit or token in refs for token in ("poetry", "liturgy", "lament", "song", "acrostic", "doxology", "q1", "q2", "q3")):
            flags.add("poetry_liturgy")
        if any(token in refs for token in ("marker:f", "marker:x", "footnote", "crossref", "variant")):
            flags.add("notes_or_variant_pressure")
        if "wj" in refs or "red_letter" in refs:
            flags.add("wj_or_red_letter")
    return sorted(flags)


def _chapter_range_overlap(span: SpanRange, scope: str) -> bool:
    marker = f"{span.book}."
    if not scope.startswith(marker):
        return False
    parts = scope[len(marker):].split(f"-{span.book}.", 1)
    if len(parts) != 2:
        return False
    try:
        start_chapter = int(parts[0])
        end_chapter = int(parts[1])
    except ValueError:
        return False
    return not (span.end.chapter < start_chapter or span.start.chapter > end_chapter)


def _span_overlaps_variant_scope(span: SpanRange, scope: str) -> bool:
    if scope == span.book:
        return True
    try:
        scope_span = parse_span(scope)
    except ValueError:
        return _chapter_range_overlap(span, scope)
    return spans_overlap(span, scope_span)


def _variant_hot_zone_matches(book: str, records: list[dict[str, Any]]) -> list[str]:
    scopes = VARIANT_HOT_ZONE_SCOPES.get(book, ())
    if not scopes:
        return []
    matches: set[str] = set()
    for record in records:
        span_raw = record.get("span")
        if not isinstance(span_raw, str):
            continue
        try:
            span = parse_span(span_raw)
        except ValueError:
            continue
        for scope in scopes:
            if _span_overlaps_variant_scope(span, scope):
                matches.add(scope)
    return sorted(matches)


def _requires_frontier_review(flags: list[str]) -> bool:
    return bool(FRONTIER_RISK_FLAGS.intersection(flags))


def _expert_review_lanes(flags: list[str], variant_matches: list[str]) -> list[str]:
    lanes: set[str] = set()
    flag_set = set(flags)
    if "variant_hot_zone" in flag_set:
        lanes.update(
            {
                "textual_variant_source_tradition",
                "major_codex_witness_review",
                "scribal_layout_and_blank_space_review",
                "scribal_letters_per_column_capacity_review",
                "manuscript_transmission_history",
            }
        )
    if any(match.startswith("Mark.16") for match in variant_matches):
        lanes.update(
            {
                "mark16_longer_ending_specialist_packet",
                "codex_vaticanus_layout_review",
                "codex_sinaiticus_ending_review",
            }
        )
    if "strongs_original_language_metadata" in flag_set:
        lanes.add("original_language_alignment_review")
    if "wj_or_red_letter" in flag_set:
        lanes.add("wj_speaker_discourse_review")
    if "prophetic_or_apocalyptic" in flag_set:
        lanes.add("prophetic_apocalyptic_frontier_review")
    if "poetry_liturgy" in flag_set:
        lanes.add("poetry_liturgy_form_review")
    return sorted(lanes)


def _record_index(
    maps: dict[str, dict[str, list[dict[str, Any]]]],
) -> dict[str, dict[str, dict[str, dict[str, Any]]]]:
    by_book_span: dict[str, dict[str, dict[str, dict[str, Any]]]] = defaultdict(lambda: defaultdict(dict))
    for model_id, by_book in maps.items():
        for book, records in by_book.items():
            for record in records:
                span_raw = record.get("span")
                if not isinstance(span_raw, str):
                    continue
                try:
                    span = normalize_span(span_raw)
                except ValueError:
                    continue
                by_book_span[book][span][model_id] = record
    return by_book_span


def _sidecar_refs_for_records(
    records_by_model: dict[str, dict[str, Any]],
    sidecar_refs_by_model: dict[str, dict[str, list[str]]],
) -> list[str]:
    refs: list[str] = []
    for model_id, record in records_by_model.items():
        decision_id = _record_decision_id(record)
        refs.extend(sidecar_refs_by_model.get(model_id, {}).get(decision_id, []))
    return sorted(set(refs))


def _enrich_agreements(
    agreements: list[dict[str, Any]],
    *,
    records_by_book_span: dict[str, dict[str, dict[str, dict[str, Any]]]],
    sidecar_refs_by_model: dict[str, dict[str, list[str]]],
) -> None:
    for idx, row in enumerate(agreements, start=1):
        book = str(row.get("book", ""))
        span = str(row.get("span", ""))
        agreeing = [str(model_id) for model_id in row.get("models_agreeing", [])]
        span_records = records_by_book_span.get(book, {}).get(span, {})
        records_by_model = {
            model_id: span_records[model_id]
            for model_id in agreeing
            if model_id in span_records
        }
        confidences = {
            model_id: str(record.get("confidence", "medium"))
            for model_id, record in records_by_model.items()
        }
        sidecar_refs = _sidecar_refs_for_records(records_by_model, sidecar_refs_by_model)
        records = list(records_by_model.values())
        risk_flags = _risk_flags_for_records(book, records, sidecar_refs)
        variant_matches = _variant_hot_zone_matches(book, records)
        requires_frontier = _requires_frontier_review(risk_flags)
        row.update(
            {
                "agreement_id": f"AGREE-{book}-{idx:05d}",
                "model_decision_ids": {
                    model_id: _record_decision_id(record)
                    for model_id, record in records_by_model.items()
                },
                "confidence_by_model": confidences,
                "confidence_rollup": _confidence_rollup(list(confidences.values())),
                "risk_flags": risk_flags,
                "variant_hot_zone_matches": variant_matches,
                "expert_review_lanes": _expert_review_lanes(risk_flags, variant_matches),
                "sidecar_refs": sidecar_refs,
                "requires_frontier_review": requires_frontier,
                "docket_status": "frontier_review_required" if requires_frontier else "consensus_low_risk_candidate",
                "recommended_candidate_basis": "model_consensus",
            }
        )


def _enrich_deltas(
    deltas: list[dict[str, Any]],
    *,
    records_by_book_span: dict[str, dict[str, dict[str, dict[str, Any]]]],
    sidecar_refs_by_model: dict[str, dict[str, list[str]]],
) -> None:
    for row in deltas:
        book = str(row.get("book", ""))
        model_spans = {
            str(model_id): str(span)
            for model_id, span in (row.get("models") or {}).items()
            if isinstance(span, str)
        }
        records_by_model: dict[str, dict[str, Any]] = {}
        for model_id, span in model_spans.items():
            record = records_by_book_span.get(book, {}).get(span, {}).get(model_id)
            if record:
                records_by_model[model_id] = record
        sidecar_refs = _sidecar_refs_for_records(records_by_model, sidecar_refs_by_model)
        records = list(records_by_model.values())
        risk_flags = _risk_flags_for_records(book, records, sidecar_refs)
        variant_matches = _variant_hot_zone_matches(book, records)
        requires_frontier = _requires_frontier_review(risk_flags)
        m4_span = model_spans.get(CODEX_MODEL_ID)
        m6_span = model_spans.get(FABLE_MODEL_ID)
        codex_fable_alignment = bool(m4_span and m6_span and m4_span == m6_span)
        span_vote_count = list(model_spans.values()).count(m4_span) if m4_span else 0
        majority = majority_required(int(row.get("complete_model_count", 6) or 6))
        trusted_minority = codex_fable_alignment and span_vote_count < majority
        delta_kind = str(row.get("delta_kind", ""))
        if requires_frontier:
            status = "frontier_review_required"
        elif row.get("delta_kind") == "coverage_gap":
            status = "harness_fix_or_rerun_required"
        elif codex_fable_alignment:
            status = "codex_fable_recommended_candidate"
        elif delta_kind == "literature_routing_disagreement":
            status = "harness_fix_or_rerun_required"
        else:
            status = "owner_decision_required"
        row.update(
            {
                "codex_fable_alignment": codex_fable_alignment,
                "codex_fable_span": m4_span if codex_fable_alignment else None,
                "trusted_minority_candidate": trusted_minority,
                "recommended_candidate_basis": "codex_fable_alignment" if codex_fable_alignment else "none",
                "model_decision_ids": {
                    model_id: _record_decision_id(record)
                    for model_id, record in records_by_model.items()
                },
                "confidence_by_model": {
                    model_id: str(record.get("confidence", "medium"))
                    for model_id, record in records_by_model.items()
                },
                "confidence_rollup": _confidence_rollup(
                    [str(record.get("confidence", "medium")) for record in records_by_model.values()]
                ),
                "risk_flags": risk_flags,
                "variant_hot_zone_matches": variant_matches,
                "expert_review_lanes": _expert_review_lanes(risk_flags, variant_matches),
                "sidecar_refs": sidecar_refs,
                "requires_frontier_review": requires_frontier,
                "decision_route": status,
                "docket_status": status,
                "next_gate": "claude_frontier_review" if status == "frontier_review_required" else "owner_or_codex_reconciliation",
            }
        )


def select_models(
    folders: list[Path],
    *,
    min_complete: int,
    require_all_initial_target: bool,
    initial_target: int,
    interim: bool,
) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    complete = [f for f in folders if model_is_complete(f)]
    if require_all_initial_target and not interim:
        if len(complete) < initial_target:
            errors.append(
                f"need {initial_target} complete models for default compare; have {len(complete)}"
            )
    elif len(complete) < min_complete:
        errors.append(f"need at least {min_complete} complete models; have {len(complete)}")
    return complete, errors


def books_in_scope(
    model_folders: list[Path],
    *,
    books_filter: set[str] | None,
    require_book_complete: bool,
) -> list[str]:
    if books_filter:
        return sorted(books_filter)
    if require_book_complete:
        sets = [completed_books(f) for f in model_folders]
        if not sets:
            return []
        common = set.intersection(*sets)
        return sorted(common)
    return canonical_books()


def compare_models(
    model_folders: list[Path],
    *,
    books: list[str],
    allow_easy_at_n3: bool,
    t417_overlap_books: set[str] | None = None,
) -> dict[str, Any]:
    model_ids = [str(load_model_manifest(f).get("model_id", f.name)) for f in model_folders]
    n = len(model_folders)
    majority = majority_required(n)
    overlap = t417_overlap_books or set()
    maps: dict[str, dict[str, list[dict[str, Any]]]] = {}
    sidecar_refs_by_model: dict[str, dict[str, list[str]]] = {}
    for folder, model_id in zip(model_folders, model_ids, strict=True):
        by_book: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in load_chunk_map(folder):
            book = str(record.get("book", ""))
            if book in books:
                by_book[book].append(record)
        for book in by_book:
            by_book[book].sort(key=lambda r: int(r["chunk_index_in_book"]))
        maps[model_id] = by_book
        sidecar_refs_by_model[model_id] = _load_sidecar_refs(folder, model_id)

    agreements: list[dict[str, Any]] = []
    deltas: list[dict[str, Any]] = []
    per_book_stats: dict[str, dict[str, Any]] = {}
    stress_books = _load_stress_books()
    records_by_book_span = _record_index(maps)

    for book in books:
        book_chunks = {mid: maps[mid].get(book, []) for mid in model_ids}
        result = compare_book_verse_coverage(
            book_chunks,
            book,
            model_ids,
            allow_easy_at_n3=allow_easy_at_n3,
            stress_book=book in stress_books,
            overlap_t417=book in overlap,
        )
        agreements.extend(result.span_consensus_chunks)
        for delta in result.boundary_deltas:
            delta["complete_model_count"] = n
            delta["majority_required"] = majority
        deltas.extend(result.boundary_deltas)
        per_book_stats[book] = {
            "verse_coverage_agreement_rate": result.verse_coverage_agreement_rate,
            "verses_total": result.verses_total,
            "verses_agreed": result.verses_agreed,
            "agreement_rate_exact_span": result.agreement_rate_exact_span_legacy,
            "chunk_counts": result.chunk_counts,
            "chunk_count_mismatch": len(set(result.chunk_counts.values())) > 1,
        }

    _enrich_agreements(
        agreements,
        records_by_book_span=records_by_book_span,
        sidecar_refs_by_model=sidecar_refs_by_model,
    )
    _enrich_deltas(
        deltas,
        records_by_book_span=records_by_book_span,
        sidecar_refs_by_model=sidecar_refs_by_model,
    )

    total_verses = sum(s.get("verses_total", 0) for s in per_book_stats.values())
    total_agreed = sum(s.get("verses_agreed", 0) for s in per_book_stats.values())
    overall_verse_rate = (total_agreed / total_verses) if total_verses else 0.0

    total_chunks = sum(
        max(s.get("chunk_counts", {}).values()) if s.get("chunk_counts") else 0
        for s in per_book_stats.values()
    )
    legacy_agreed = sum(
        1 for a in agreements if a.get("book") in per_book_stats
    )
    overall_legacy_rate = (legacy_agreed / total_chunks) if total_chunks else 0.0

    false_consensus: list[dict[str, str]] = []
    for row in agreements:
        if row["agreement_tier"] == "full_consensus" and row["book"] in stress_books:
            false_consensus.append(
                {
                    "book": row["book"],
                    "span": row["span"],
                    "warning": "full_consensus_on_stress_atlas_book",
                }
            )

    return {
        "model_ids": model_ids,
        "complete_model_count": n,
        "majority_required": majority,
        "books_compared": books,
        "agreements": agreements,
        "deltas": deltas,
        "per_book_stats": per_book_stats,
        "overall_verse_coverage_agreement_rate": round(overall_verse_rate, 4),
        "overall_agreement_rate": round(overall_legacy_rate, 4),
        "false_consensus_warnings": false_consensus,
    }


def _docket_entry(row: dict[str, Any], *, source_ledger: str) -> dict[str, Any]:
    source_id = str(row.get("agreement_id") or row.get("delta_id") or "")
    return {
        "source_ledger": source_ledger,
        "source_id": source_id,
        "book": str(row.get("book", "")),
        "span_or_region": str(row.get("span") or row.get("region") or ""),
        "docket_status": str(row.get("docket_status", "")),
        "recommended_candidate_basis": str(row.get("recommended_candidate_basis", "none")),
        "codex_fable_alignment": bool(row.get("codex_fable_alignment", False)),
        "requires_frontier_review": bool(row.get("requires_frontier_review", False)),
        "risk_flags": row.get("risk_flags", []),
        "variant_hot_zone_matches": row.get("variant_hot_zone_matches", []),
        "expert_review_lanes": row.get("expert_review_lanes", []),
        "non_authorizing": True,
        "promotion_authority": "none",
    }


def _build_owner_docket(result: dict[str, Any]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {status: [] for status in sorted(DECISION_STATUSES)}
    for row in result["agreements"]:
        status = str(row.get("docket_status", "owner_decision_required"))
        grouped.setdefault(status, []).append(_docket_entry(row, source_ledger="agreement_chunks.jsonl"))
    for row in result["deltas"]:
        status = str(row.get("docket_status", "owner_decision_required"))
        grouped.setdefault(status, []).append(_docket_entry(row, source_ledger="disagreement_delta.jsonl"))
    return {
        "object_type": "t464_multi_model_owner_decision_docket",
        "schema_version": "t464_multi_model_owner_decision_docket.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "populated_non_authorizing",
        "models_compared": result["model_ids"],
        "complete_model_count": result["complete_model_count"],
        "preferred_disagreement_lens": [CODEX_MODEL_ID, FABLE_MODEL_ID],
        "source_ledgers": {
            "agreement": "agreement_chunks.jsonl",
            "delta": "disagreement_delta.jsonl",
            "frontier": "frontier_review_queue.jsonl",
            "harness": "harness_improvement_queue.md",
        },
        "status_counts": {status: len(entries) for status, entries in grouped.items()},
        "statuses": grouped,
        "non_authorizations": [
            "agreement_is_evidence_not_authority",
            "codex_fable_alignment_is_not_owner_selection",
            "no_reviewed_gold",
            "no_chunk_output",
            "no_child_spans",
            "no_route_or_evaluator_change",
            "no_graph_retrieval_vector_truth",
            "no_source_tradition_or_canon_authority",
            "no_theology_authority",
        ],
        "non_authorizing": True,
        "promotion_authority": "none",
    }


def _frontier_queue_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_ledger, records in (
        ("agreement_chunks.jsonl", result["agreements"]),
        ("disagreement_delta.jsonl", result["deltas"]),
    ):
        for record in records:
            if record.get("docket_status") != "frontier_review_required":
                continue
            rows.append(
                {
                    "source_ledger": source_ledger,
                    "source_id": str(record.get("agreement_id") or record.get("delta_id")),
                    "book": str(record.get("book", "")),
                    "span_or_region": str(record.get("span") or record.get("region") or ""),
                    "risk_flags": record.get("risk_flags", []),
                    "variant_hot_zone_matches": record.get("variant_hot_zone_matches", []),
                    "expert_review_lanes": record.get("expert_review_lanes", []),
                    "confidence_rollup": record.get("confidence_rollup", "medium"),
                    "suggested_reviewer": "claude_frontier",
                    "why_frontier_review_needed": "T464 routed this row because model consensus or M4/M6 alignment intersects high-risk genre, low-confidence, WJ/speaker, variant/source-note, poetry/liturgy, prophetic/apocalyptic, dense epistle, or sidecar pressure.",
                    "non_authorizing": True,
                    "promotion_authority": "none",
                }
            )
    return rows


def _write_harness_queue(path: Path, result: dict[str, Any]) -> None:
    harness_rows = [
        row for row in result["deltas"]
        if row.get("docket_status") == "harness_fix_or_rerun_required"
    ]
    lines = [
        "# T464 Harness Improvement Queue",
        "",
        "These rows are non-authorizing. They identify places where model disagreement likely reflects harness or instruction weakness rather than a ready owner decision.",
        "",
        "## Summary",
        f"- Harness/rerun rows: {len(harness_rows)}",
        f"- Preferred disagreement lens: {CODEX_MODEL_ID} + {FABLE_MODEL_ID}",
        "- Agreement and disagreement ledgers remain the source of truth for row details.",
        "",
        "## Top Items",
    ]
    for row in harness_rows[:50]:
        lines.append(
            f"- {row.get('delta_id')}: {row.get('book')} {row.get('region')} "
            f"({row.get('delta_kind')}; risk={','.join(row.get('risk_flags', [])) or 'none'})"
        )
    if len(harness_rows) > 50:
        lines.append(f"- ... {len(harness_rows) - 50} more in disagreement_delta.jsonl")
    lines.extend(
        [
            "",
            "## Harness Notes",
            "- If many rows cluster in one genre, improve the book-family prompt before rerunning that model family.",
            "- If M4 and M6 agree but all other models split differently, treat it as a trusted-minority candidate only.",
            "- If a row is high-risk, route to frontier review before owner selection.",
            "- See M6_fable5/harness_recommendations.md for model-authored harness critique.",
            "",
            "## Non-Authorizations",
            "- No reviewed gold, chunk output, child spans, route/evaluator behavior, graph/retrieval/vector truth, source-tradition choice, canon change, or theology authority.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(result: dict[str, Any], *, dry_run: bool) -> None:
    comp = COMPARISON_ROOT
    if dry_run:
        print(json.dumps({k: v for k, v in result.items() if k not in {"agreements", "deltas"}}, indent=2))
        print(f"agreements={len(result['agreements'])} deltas={len(result['deltas'])}")
        return

    _write_jsonl(comp / "agreement_chunks.jsonl", result["agreements"])
    _write_jsonl(comp / "disagreement_delta.jsonl", result["deltas"])
    frontier_rows = _frontier_queue_rows(result)
    _write_jsonl(comp / "frontier_review_queue.jsonl", frontier_rows)
    _write_harness_queue(comp / "harness_improvement_queue.md", result)

    top_disagreement = sorted(
        result["per_book_stats"].items(),
        key=lambda item: item[1].get("verse_coverage_agreement_rate", 0),
    )[:10]
    threshold = load_fork_policy().get("revert_policy", {}).get("revert_threshold", {})
    full_min = float(threshold.get("full_marathon_verse_coverage_agreement_rate_minimum", 0.50))
    fork_signal = "FULL_PASS" if result["overall_verse_coverage_agreement_rate"] >= full_min else "FULL_FAIL"

    matrix = {
        "object_type": "model_agreement_matrix",
        "schema_version": "model_agreement_matrix.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "complete_model_count": result["complete_model_count"],
        "majority_required": result["majority_required"],
        "models_compared": result["model_ids"],
        "books_compared": result["books_compared"],
        "overall_verse_coverage_agreement_rate": result["overall_verse_coverage_agreement_rate"],
        "overall_agreement_rate_exact_span_legacy": result["overall_agreement_rate"],
        "per_book": result["per_book_stats"],
        "false_consensus_warnings": result["false_consensus_warnings"],
        "non_authorizing": True,
        "promotion_authority": "none",
    }
    (comp / "model_agreement_matrix.yaml").write_text(
        yaml.safe_dump(matrix, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    focus = {
        "object_type": "delta_focus_queue",
        "schema_version": "delta_focus_queue.v1",
        "status": "populated",
        "strategy": "focus_governed_work_on_disagreement_only",
        "easy_chunks_from_agreement": "agreement_chunks.jsonl",
        "delta_source": "disagreement_delta.jsonl",
        "overall_verse_coverage_agreement_rate": result["overall_verse_coverage_agreement_rate"],
        "priority_books": [b for b, _ in top_disagreement],
        "candidates": [
            {
                "delta_id": d["delta_id"],
                "book": d["book"],
                "priority": d.get("priority", "medium"),
                "delta_kind": d.get("delta_kind"),
            }
            for d in result["deltas"][:50]
        ],
        "non_authorizing": True,
        "promotion_authority": "none",
    }
    (comp / "delta_focus_queue.yaml").write_text(
        yaml.safe_dump(focus, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (comp / "owner_decision_docket.yaml").write_text(
        yaml.safe_dump(_build_owner_docket(result), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    lines = [
        "# Delta Summary — Multi-Model Whole-Bible Chunk Comparison",
        "",
        "## Scope",
        f"- Models: {', '.join(result['model_ids'])}",
        f"- N = {result['complete_model_count']}; majority = ceil(0.7×N) = {result['majority_required']}",
        f"- Books compared: {len(result['books_compared'])}",
        "",
        "## Headline metrics",
        f"- Overall verse-coverage agreement rate: {result['overall_verse_coverage_agreement_rate']:.2%}",
        f"- Legacy exact-span rate (audit only): {result['overall_agreement_rate']:.2%}",
        f"- Easy chunk count: {len(result['agreements'])}",
        f"- Delta span count: {len(result['deltas'])}",
        f"- Frontier review queue rows: {len(frontier_rows)}",
        f"- Fork threshold signal: {fork_signal} (minimum {full_min:.2%})",
        "",
        "## Highest-disagreement books (top 10)",
    ]
    for book, stats in top_disagreement:
        lines.append(f"- {book}: {stats.get('verse_coverage_agreement_rate', 0):.2%}")
    lines.extend(
        [
            "",
            "## False consensus warnings",
        ]
    )
    if result["false_consensus_warnings"]:
        for w in result["false_consensus_warnings"][:20]:
            lines.append(f"- {w['book']} {w['span']}: {w['warning']}")
    else:
        lines.append("- none flagged")
    lines.extend(
        [
            "",
            "## Decision routing",
            "- `agreement_chunks.jsonl` contains non-authorizing consensus/easy-majority evidence.",
            "- `disagreement_delta.jsonl` contains non-authorizing deltas with M4/M6 alignment fields.",
            "- `owner_decision_docket.yaml` assigns every agreement/delta row a docket status.",
            "- `frontier_review_queue.jsonl` carries high-risk/low-confidence rows for Claude/frontier review.",
            "- `harness_improvement_queue.md` collects likely harness/rerun issues.",
            "",
            "## Non-authorizations",
            "- Agreement does not promote gold or chunk output",
            "- promotion_authority: none",
        ]
    )
    (comp / "delta_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-root", type=Path, default=SCRATCH_ROOT)
    parser.add_argument("--interim", action="store_true", help="Allow compare before initial_target complete")
    parser.add_argument("--book", action="append", dest="books", help="Compare specific book(s) only")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--require-book-complete",
        action="store_true",
        default=True,
        help="Only compare books marked complete in all model marathon_progress.yaml (default)",
    )
    args = parser.parse_args()

    policy = load_fork_policy()
    rules = policy.get("comparison_rules", {})
    model_count = policy.get("model_count", {})
    min_complete = int(rules.get("compare_when_at_least_models", 3))
    initial_target = int(model_count.get("initial_target", 5))
    interim_default = bool(rules.get("interim_compare_default_requires_initial_target", True))
    allow_easy_at_n3 = bool(rules.get("allow_easy_majority_at_n3", False))
    t417_overlap = _load_t417_overlap_books(policy)

    folders = discover_model_folders(args.scratch_root)
    if not folders:
        print("ERROR: no model folders found", file=sys.stderr)
        return 1

    selected, errors = select_models(
        folders,
        min_complete=min_complete,
        require_all_initial_target=interim_default and not args.interim,
        initial_target=initial_target,
        interim=args.interim,
    )
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    books_filter = set(args.books) if args.books else None
    books = books_in_scope(
        selected,
        books_filter=books_filter,
        require_book_complete=args.require_book_complete and not args.books,
    )
    if not books:
        print("ERROR: no books in scope for comparison", file=sys.stderr)
        return 1

    for folder in selected:
        map_path = folder / "whole_bible_chunk_map.jsonl"
        if not map_path.is_file():
            print(f"ERROR: missing {_rel(map_path)}", file=sys.stderr)
            return 1

    result = compare_models(
        selected,
        books=books,
        allow_easy_at_n3=allow_easy_at_n3,
        t417_overlap_books=t417_overlap,
    )
    write_outputs(result, dry_run=args.dry_run)
    if not args.dry_run:
        print(f"OK: compared {result['complete_model_count']} models, {len(books)} books")
        print(f"  verse_coverage_agreement_rate={result['overall_verse_coverage_agreement_rate']:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
