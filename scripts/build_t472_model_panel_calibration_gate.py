#!/usr/bin/env python3
"""Build the T472 model-panel calibration and provenance-correction overlay."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking"
COMPARISON = SCRATCH / "comparison"
DELTA_SOURCE = COMPARISON / "disagreement_delta.jsonl"
AGREEMENT_SOURCE = COMPARISON / "agreement_chunks.jsonl"
T465_DOCKET = ROOT / ".ai" / "context" / "agent_work" / "T465" / "owner_candidate_docket.yaml"
T471_DOCKET = ROOT / ".ai" / "context" / "agent_work" / "T471" / "owner_candidate_support_debate_docket.yaml"
COVERAGE = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_inventory.jsonl"
OUTPUT = ROOT / ".ai" / "context" / "agent_work" / "T472"

MODEL_IDS = (
    "M1_cursor",
    "M2_claude_sonnet5",
    "M3_claude_frontier",
    "M4_codex_gpt55",
    "M5_gemini_thinking",
    "M6_fable5",
)
CORE_MODELS = (
    "M2_claude_sonnet5",
    "M3_claude_frontier",
    "M4_codex_gpt55",
    "M6_fable5",
)
AUDIT_ONLY_MODELS = ("M1_cursor", "M5_gemini_thinking")
CODEX = "M4_codex_gpt55"
FABLE = "M6_fable5"

CLASSIFICATION_OUT = OUTPUT / "all_delta_mechanical_classification.jsonl"
DISSENT_OUT = OUTPUT / "larger_unit_dissent.jsonl"
ROUTING_OUT = OUTPUT / "corrected_routing_overlay.jsonl"
LEGACY_19_OUT = OUTPUT / "corrected_legacy_19_docket.yaml"
AGREEMENT_OUT = OUTPUT / "agreement_recalibration.yaml"
CALIBRATION_OUT = OUTPUT / "model_panel_calibration.yaml"
FROZEN_OUT = OUTPUT / "frozen_artifact_manifest.yaml"
SUMMARY_OUT = OUTPUT / "correction_summary.md"

GENRE_NOTES = {
    "1Chr": "Chronicles register, genealogy, worship-service, and narrative units routinely cross chapter divisions; require whole-functional-register review.",
    "2Chr": "Chronicles temple, covenant-renewal, and reign narratives may cross chapters; chapter coincidence is not literary proof.",
    "1Sam": "Narrative scene and speech framing control; chapter coincidence requires explicit scene evidence.",
    "2Sam": "Narrative episode and covenant/rebellion movement control; preserve larger scene dissent.",
    "2Kgs": "Narrative episode and prophetic speech framing control; the Hezekiah/Sennacherib unit crosses chapters 18-19.",
    "Exod": "Covenant, legal, ritual, and narrative units control; chapter numbers are editorial evidence only.",
    "Josh": "Allotment and territorial-register function controls; test whether a chapter is only a slice of the larger allotment.",
    "Neh": "Register, covenant-community, and narrative function controls; retain totals and governing frames.",
    "Num": "Census, legal, ritual-calendar, and journey units control; whole functional lists may cross chapters.",
    "2John": "Short epistle structure requires greeting/body/warning/closing evidence and existing-gold overlap review; whole-letter agreement is not present.",
    "2Tim": "Epistle argument, charge, travel note, and closing structure control; dense doctrinal movement may require frontier review.",
}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            row = json.loads(stripped)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            row = dict(row)
            row["_source_line"] = line_no
            rows.append(row)
    return rows


def _read_yaml(path: Path) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for document in yaml.safe_load_all(path.read_text(encoding="utf-8")):
        if isinstance(document, dict):
            merged.update(document)
    if not merged:
        raise ValueError(f"{path}: expected YAML mapping")
    return merged


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8", newline="\n")


def _scalar_span(value: Any) -> str | None:
    return value if isinstance(value, str) and value.count(".") >= 2 else None


def _point(raw: str) -> tuple[str, int, int]:
    book, chapter, verse = raw.split(".")
    return book, int(chapter), int(verse)


def _span_bounds(raw: str) -> tuple[str, tuple[int, int], tuple[int, int]]:
    if "-" in raw:
        start_raw, end_raw = raw.split("-", 1)
    else:
        start_raw = end_raw = raw
    start_book, start_chapter, start_verse = _point(start_raw)
    end_book, end_chapter, end_verse = _point(end_raw)
    if start_book != end_book:
        raise ValueError(f"cross-book span not supported: {raw}")
    return start_book, (start_chapter, start_verse), (end_chapter, end_verse)


def _strictly_contains(outer_raw: str | None, inner_raw: str | None) -> bool:
    if outer_raw is None or inner_raw is None:
        return False
    try:
        outer_book, outer_start, outer_end = _span_bounds(outer_raw)
        inner_book, inner_start, inner_end = _span_bounds(inner_raw)
    except (TypeError, ValueError):
        return False
    return (
        outer_book == inner_book
        and outer_start <= inner_start
        and outer_end >= inner_end
        and (outer_start < inner_start or outer_end > inner_end)
    )


def _chapter_maxima() -> dict[tuple[str, int], int]:
    maxima: dict[tuple[str, int], int] = {}
    for row in _read_jsonl(COVERAGE):
        book = str(row.get("book", ""))
        chapter = row.get("chapter")
        verse_end = row.get("verse_end")
        if book and isinstance(chapter, int) and isinstance(verse_end, int):
            key = (book, chapter)
            maxima[key] = max(maxima.get(key, 0), verse_end)
    return maxima


def _is_complete_chapter(raw: str | None, maxima: dict[tuple[str, int], int]) -> bool:
    if raw is None:
        return False
    try:
        book, start, end = _span_bounds(raw)
    except ValueError:
        return False
    return start[1] == 1 and maxima.get((book, end[0])) == end[1]


def _features(row: dict[str, Any], maxima: dict[tuple[str, int], int]) -> dict[str, Any]:
    models = row.get("models", {})
    if not isinstance(models, dict):
        models = {}
    scalar_models = {str(model): _scalar_span(span) for model, span in models.items()}
    scalar_values = {span for span in scalar_models.values() if span is not None}
    region = row.get("region") if isinstance(row.get("region"), str) else None
    m4 = scalar_models.get(CODEX)
    m6 = scalar_models.get(FABLE)
    pair_aligned = bool(m4 and m6 and m4 == m6)

    larger_dissent: list[dict[str, str]] = []
    if pair_aligned:
        for model_id in ("M2_claude_sonnet5", "M3_claude_frontier"):
            proposed = scalar_models.get(model_id)
            if _strictly_contains(proposed, m4):
                larger_dissent.append(
                    {
                        "model_id": model_id,
                        "larger_span": str(proposed),
                        "contained_pair_span": str(m4),
                    }
                )

    core_values = [scalar_models.get(model_id) for model_id in CORE_MODELS]
    core_equal = all(value is not None for value in core_values) and len(set(core_values)) == 1
    oversplit_only = False
    if core_equal:
        base = core_values[0]
        oversplit_only = all(_strictly_contains(base, scalar_models.get(model_id)) for model_id in AUDIT_ONLY_MODELS)

    frontier = bool(
        row.get("requires_frontier_review")
        or "sidecar_low_confidence_or_frontier" in set(row.get("risk_flags", []))
        or "variant_hot_zone" in set(row.get("risk_flags", []))
        or row.get("variant_hot_zone_matches")
    )
    return {
        "region_not_observed_as_model_span": bool(region and region not in scalar_values),
        "pair_aligned": pair_aligned,
        "pair_span": m4 if pair_aligned else None,
        "pair_span_chapter_coincident": pair_aligned and _is_complete_chapter(m4, maxima),
        "strict_larger_calibrated_dissent": bool(larger_dissent),
        "larger_dissent": larger_dissent,
        "m1_m5_oversplit_only": oversplit_only,
        "variant_or_frontier": frontier,
        "scalar_model_spans": scalar_models,
    }


def _classify(row: dict[str, Any], features: dict[str, Any]) -> str:
    if row.get("delta_kind") == "coverage_gap":
        return "coverage_gap"
    if features["region_not_observed_as_model_span"]:
        return "region_pair_span_mismatch"
    if features["strict_larger_calibrated_dissent"]:
        return "strict_larger_calibrated_dissent"
    if features["m1_m5_oversplit_only"]:
        return "m1_m5_oversplit_only"
    if features["pair_span_chapter_coincident"]:
        return "chapter_coincident_pair_alignment"
    if features["variant_or_frontier"]:
        return "variant_frontier"
    return "genuine_non_chapter_literary_disagreement"


def _effective_route(classification: str, features: dict[str, Any]) -> str:
    routes = {
        "coverage_gap": "harness_fix_or_rerun_required",
        "region_pair_span_mismatch": "provenance_reconciliation_required",
        "strict_larger_calibrated_dissent": "real_literary_disagreement",
        "m1_m5_oversplit_only": "fixed_harness_pilot_required",
        "chapter_coincident_pair_alignment": "chapter_anchor_literary_review_required",
        "variant_frontier": "frontier_review_required",
        "genuine_non_chapter_literary_disagreement": "real_literary_disagreement",
    }
    route = routes[classification]
    if features["variant_or_frontier"] and route != "frontier_review_required":
        return f"{route}+frontier_review_required"
    return route


def _classification_rows(deltas: list[dict[str, Any]], maxima: dict[tuple[str, int], int]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    classified: list[dict[str, Any]] = []
    dissent: list[dict[str, Any]] = []
    routing: list[dict[str, Any]] = []
    for source in deltas:
        source_id = str(source.get("delta_id", ""))
        features = _features(source, maxima)
        classification = _classify(source, features)
        effective_route = _effective_route(classification, features)
        row = {
            "source_id": source_id,
            "source_line": source["_source_line"],
            "book": source.get("book"),
            "disagreement_region": source.get("region"),
            "delta_kind": source.get("delta_kind"),
            "model_spans": features["scalar_model_spans"],
            "model_decision_ids": source.get("model_decision_ids", {}),
            "legacy_route": source.get("docket_status"),
            "mechanical_class": classification,
            "effective_route": effective_route,
            "region_not_observed_as_model_span": features["region_not_observed_as_model_span"],
            "pair_alignment_observation": features["pair_aligned"],
            "pair_span": features["pair_span"],
            "pair_span_chapter_coincident": features["pair_span_chapter_coincident"],
            "strict_larger_calibrated_dissent": features["strict_larger_calibrated_dissent"],
            "larger_dissent": features["larger_dissent"],
            "m1_m5_oversplit_only": features["m1_m5_oversplit_only"],
            "variant_or_frontier": features["variant_or_frontier"],
            "candidate_eligible": False,
            "promotion_authority": "none",
            "non_authorizing": True,
        }
        classified.append(row)
        routing.append(
            {
                "historical_source_id": source_id,
                "frozen_artifact_sha256": _sha256(DELTA_SOURCE),
                "legacy_route": source.get("docket_status"),
                "effective_route": effective_route,
                "blocking_conditions": [
                    key
                    for key, active in (
                        ("region_span_provenance", features["region_not_observed_as_model_span"]),
                        ("strict_larger_calibrated_dissent", features["strict_larger_calibrated_dissent"]),
                        ("chapter_coincident_without_literary_identity", features["pair_span_chapter_coincident"]),
                        ("uncalibrated_model_panel", True),
                        ("frontier_or_variant_pressure", features["variant_or_frontier"]),
                    )
                    if active
                ],
                "supersedes_routing_only": True,
                "candidate_eligible": False,
                "promotion_authority": "none",
                "non_authorizing": True,
            }
        )
        if features["strict_larger_calibrated_dissent"]:
            dissent.append(
                {
                    "source_id": source_id,
                    "book": source.get("book"),
                    "disagreement_region": source.get("region"),
                    "pair_span": features["pair_span"],
                    "larger_dissent": features["larger_dissent"],
                    "all_model_spans": features["scalar_model_spans"],
                    "model_decision_ids": source.get("model_decision_ids", {}),
                    "effective_route": "real_literary_disagreement",
                    "frontier_also_required": features["variant_or_frontier"],
                    "candidate_eligible": False,
                    "non_authorizing": True,
                    "promotion_authority": "none",
                }
            )
    return classified, dissent, routing


def _legacy_19(
    deltas_by_id: dict[str, dict[str, Any]],
    classified_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    t465 = _read_yaml(T465_DOCKET)
    rows: list[dict[str, Any]] = []
    for candidate in t465.get("candidates", []):
        source_id = str(candidate.get("source_id", ""))
        delta = deltas_by_id[source_id]
        corrected = classified_by_id[source_id]
        actual_pair = corrected.get("pair_span")
        legacy_span = candidate.get("span")
        mismatch = bool(actual_pair and legacy_span != actual_pair)
        rows.append(
            {
                "source_id": source_id,
                "book": delta.get("book"),
                "legacy_docket_span": legacy_span,
                "disagreement_region": delta.get("region"),
                "actual_pair_span": actual_pair,
                "model_spans": corrected.get("model_spans"),
                "model_decision_ids": corrected.get("model_decision_ids"),
                "legacy_route": delta.get("docket_status"),
                "legacy_region_span_mismatch": mismatch,
                "pair_span_chapter_coincident": corrected.get("pair_span_chapter_coincident"),
                "strict_larger_calibrated_dissent": corrected.get("strict_larger_calibrated_dissent"),
                "larger_dissent": corrected.get("larger_dissent"),
                "genre_specific_review_note": GENRE_NOTES.get(str(delta.get("book")), "Require book-specific literary evidence; chapter or model agreement is insufficient."),
                "corrected_disposition": (
                    "withdrawn_provenance_defect"
                    if mismatch
                    else corrected.get("effective_route")
                ),
                "owner_ready": False,
                "candidate_eligible": False,
                "non_authorizing": True,
                "promotion_authority": "none",
            }
        )
    return {
        "object_type": "t472_corrected_legacy_19_docket",
        "schema_version": "t472_corrected_legacy_19_docket.v1",
        "task_id": "T472",
        "source_task_ids": ["T464", "T465", "T471"],
        "legacy_row_count": len(rows),
        "owner_ready_count": 0,
        "region_span_mismatch_count": sum(bool(row["legacy_region_span_mismatch"]) for row in rows),
        "chapter_coincident_count": sum(bool(row["pair_span_chapter_coincident"]) for row in rows),
        "strict_larger_dissent_count": sum(bool(row["strict_larger_calibrated_dissent"]) for row in rows),
        "potentially_defensible_after_literary_review_count": sum(
            not row["legacy_region_span_mismatch"]
            and bool(row["pair_span_chapter_coincident"])
            and not row["strict_larger_calibrated_dissent"]
            for row in rows
        ),
        "rows": rows,
        "non_authorizing": True,
        "promotion_authority": "none",
    }


def _granularity(span: str) -> str:
    _, start, end = _span_bounds(span)
    if start[0] != end[0]:
        return "cross_chapter"
    return "single_verse" if start == end else "same_chapter_multi_verse"


def _model_calibration() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for model_id in MODEL_IDS:
        folder = SCRATCH / model_id
        chunks = _read_jsonl(folder / "whole_bible_chunk_map.jsonl")
        counts = Counter(_granularity(str(row["span"])) for row in chunks)
        manifest = _read_yaml(folder / "model_manifest.yaml")
        progress = _read_yaml(folder / "marathon_progress.yaml")
        manifest_status = str(manifest.get("status", ""))
        progress_status = str(progress.get("marathon_status", ""))
        status_consistent = (
            manifest_status in {"complete", "marathon_complete"}
            and progress_status in {"complete", "marathon_complete"}
        ) or manifest_status == progress_status
        consistent = status_consistent and manifest.get("books_completed") == progress.get("books_completed")
        audit_only = model_id in AUDIT_ONLY_MODELS
        rows.append(
            {
                "model_id": model_id,
                "chunk_count": len(chunks),
                "single_verse_chunks": counts["single_verse"],
                "same_chapter_multi_verse_chunks": counts["same_chapter_multi_verse"],
                "cross_chapter_chunks": counts["cross_chapter"],
                "manifest_status": manifest_status,
                "manifest_books_completed": manifest.get("books_completed"),
                "progress_status": progress_status,
                "progress_books_completed": progress.get("books_completed"),
                "manifest_progress_consistent": consistent,
                "evidence_role": ("audit_only_pending_fixed_harness_pilot" if audit_only else {"M2_claude_sonnet5": "review_evidence_only", "M3_claude_frontier": "frontier_review_evidence_only", "M4_codex_gpt55": "proposer_evidence_only", "M6_fable5": "critic_or_proposer_evidence_only"}[model_id]),
                "eligible_for_confidence_or_majority": False,
                "delete_or_discard": False,
                "map_sha256": _sha256(folder / "whole_bible_chunk_map.jsonl"),
            }
        )
    return {
        "object_type": "t472_model_panel_calibration",
        "schema_version": "t472_model_panel_calibration.v1",
        "task_id": "T472",
        "models": rows,
        "preferred_pair": None,
        "model_agreement_role": "queue_sorting_evidence_only",
        "all_self_reported_confidence_role": "archival_only",
        "non_authorizing": True,
    }


def _agreement_recalibration(maxima: dict[tuple[str, int], int]) -> dict[str, Any]:
    rows = _read_jsonl(AGREEMENT_SOURCE)
    easy = [row for row in rows if row.get("easy_chunk") is True]
    core_four = [row for row in easy if set(CORE_MODELS).issubset(set(row.get("models_agreeing", [])))]
    dropped = [str(row.get("agreement_id")) for row in easy if row not in core_four]
    chapter_coincident = [row for row in core_four if _is_complete_chapter(_scalar_span(row.get("span")), maxima)]
    return {
        "object_type": "t472_agreement_recalibration",
        "schema_version": "t472_agreement_recalibration.v1",
        "task_id": "T472",
        "legacy_easy_agreement_count": len(easy),
        "core_four_present_count": len(core_four),
        "dropped_when_M1_M5_are_ineligible": dropped,
        "core_four_chapter_coincident_count": len(chapter_coincident),
        "owner_accepted_candidate_evidence_count_from_T468": 143,
        "automatic_reviewed_gold_count": 0,
        "model_agreement_role": "candidate_queue_sorting_only",
        "requires_literary_and_overlap_review": True,
        "non_authorizing": True,
        "promotion_authority": "none",
    }


def _frozen_manifest() -> dict[str, Any]:
    paths = [
        DELTA_SOURCE,
        AGREEMENT_SOURCE,
        T465_DOCKET,
        T471_DOCKET,
    ]
    return {
        "object_type": "t472_frozen_artifact_manifest",
        "schema_version": "t472_frozen_artifact_manifest.v1",
        "task_id": "T472",
        "artifacts": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": _sha256(path),
                "mutation_allowed_by_T472": False,
                "routing_superseded_only": True,
            }
            for path in paths
        ],
    }


def build_outputs() -> dict[str, Any]:
    maxima = _chapter_maxima()
    deltas = _read_jsonl(DELTA_SOURCE)
    classified, dissent, routing = _classification_rows(deltas, maxima)
    deltas_by_id = {str(row["delta_id"]): row for row in deltas}
    classified_by_id = {str(row["source_id"]): row for row in classified}
    legacy = _legacy_19(deltas_by_id, classified_by_id)
    agreement = _agreement_recalibration(maxima)
    calibration = _model_calibration()
    frozen = _frozen_manifest()
    class_counts = Counter(str(row["mechanical_class"]) for row in classified)
    feature_counts = {
        "region_not_observed_as_model_span": sum(bool(row["region_not_observed_as_model_span"]) for row in classified),
        "pair_alignment_observation": sum(bool(row["pair_alignment_observation"]) for row in classified),
        "pair_span_chapter_coincident": sum(bool(row["pair_span_chapter_coincident"]) for row in classified),
        "strict_larger_calibrated_dissent": sum(bool(row["strict_larger_calibrated_dissent"]) for row in classified),
        "m1_m5_oversplit_only": sum(bool(row["m1_m5_oversplit_only"]) for row in classified),
        "variant_or_frontier": sum(bool(row["variant_or_frontier"]) for row in classified),
    }
    summary_lines = [
        "# T472 Model-Panel Calibration And Provenance Correction",
        "",
        "T472 preserves the frozen T464/T465/T471 evidence and supersedes routing only.",
        "",
        "## Delta Classification",
        f"- total: {len(classified)}",
        *[f"- {name}: {class_counts[name]}" for name in sorted(class_counts)],
        "",
        "## Feature Totals",
        *[f"- {name}: {feature_counts[name]}" for name in sorted(feature_counts)],
        "",
        "## Legacy 19 Correction",
        f"- region/span defects: {legacy['region_span_mismatch_count']}",
        f"- chapter-coincident pair spans: {legacy['chapter_coincident_count']}",
        f"- strict-larger calibrated dissent: {legacy['strict_larger_dissent_count']}",
        f"- potentially defensible only after literary review: {legacy['potentially_defensible_after_literary_review_count']}",
        "- owner-ready rows after correction: 0",
        "",
        "## 2 John",
        "- disagreement region: 2John.1.1-2John.1.13",
        "- actual M4/M6 span: 2John.1.12-2John.1.13",
        "- whole-letter owner packet: withdrawn",
        "- existing reviewed-gold/output overlap: 2John.1.1-2John.1.3",
        "",
        "## Model Disposition",
        "- M1_cursor and M5_gemini_thinking are preserved as audit evidence.",
        "- Neither is eligible for confidence or majority routing until a fixed-harness pilot passes.",
        "- M4/M6 agreement is an observation only, not a preferred lens or owner-candidate route.",
        "",
        "No reviewed gold, chunk output, child spans, route/evaluator behavior, graph/retrieval/vector truth, source-tradition preference, canon change, variant decision, or theology authority is authorized.",
        "",
    ]
    return {
        "classification": classified,
        "dissent": dissent,
        "routing": routing,
        "legacy": legacy,
        "agreement": agreement,
        "calibration": calibration,
        "frozen": frozen,
        "summary": "\n".join(summary_lines),
    }


def write_outputs(outputs: dict[str, Any]) -> None:
    _write_jsonl(CLASSIFICATION_OUT, outputs["classification"])
    _write_jsonl(DISSENT_OUT, outputs["dissent"])
    _write_jsonl(ROUTING_OUT, outputs["routing"])
    _write_yaml(LEGACY_19_OUT, outputs["legacy"])
    _write_yaml(AGREEMENT_OUT, outputs["agreement"])
    _write_yaml(CALIBRATION_OUT, outputs["calibration"])
    _write_yaml(FROZEN_OUT, outputs["frozen"])
    SUMMARY_OUT.write_text(outputs["summary"], encoding="utf-8", newline="\n")


def _jsonl_equals(path: Path, expected: list[dict[str, Any]]) -> bool:
    if not path.is_file():
        return False
    actual = _read_jsonl(path)
    for row in actual:
        row.pop("_source_line", None)
    return actual == expected


def check_outputs(outputs: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path, key in (
        (CLASSIFICATION_OUT, "classification"),
        (DISSENT_OUT, "dissent"),
        (ROUTING_OUT, "routing"),
    ):
        if not _jsonl_equals(path, outputs[key]):
            errors.append(f"{path.relative_to(ROOT)} is missing or stale")
    for path, key in (
        (LEGACY_19_OUT, "legacy"),
        (AGREEMENT_OUT, "agreement"),
        (CALIBRATION_OUT, "calibration"),
        (FROZEN_OUT, "frozen"),
    ):
        if not path.is_file() or _read_yaml(path) != outputs[key]:
            errors.append(f"{path.relative_to(ROOT)} is missing or stale")
    if not SUMMARY_OUT.is_file() or SUMMARY_OUT.read_text(encoding="utf-8") != outputs["summary"]:
        errors.append(f"{SUMMARY_OUT.relative_to(ROOT)} is missing or stale")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    outputs = build_outputs()
    if args.check:
        errors = check_outputs(outputs)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("T472 model-panel calibration outputs are current.")
        return 0
    write_outputs(outputs)
    print(f"Wrote {len(outputs['classification'])} T472 delta classifications.")
    print(f"Wrote {len(outputs['dissent'])} strict-larger dissent rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())