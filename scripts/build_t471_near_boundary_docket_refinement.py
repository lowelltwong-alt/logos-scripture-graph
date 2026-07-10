#!/usr/bin/env python3
"""Build T471 near-boundary and owner-docket refinement artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import boundary_shift_verses, parse_span, spans_overlap

COMPARISON = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "comparison"
T465_DOCKET = ROOT / ".ai" / "context" / "agent_work" / "T465" / "owner_candidate_docket.yaml"
OUTPUT_ROOT = ROOT / ".ai" / "context" / "agent_work" / "T471"
DELTA_OUT = OUTPUT_ROOT / "near_boundary_delta_refinement.jsonl"
OWNER_OUT = OUTPUT_ROOT / "owner_candidate_support_debate_docket.yaml"
SUMMARY_OUT = OUTPUT_ROOT / "refinement_summary.md"

CODEX_MODEL_ID = "M4_codex_gpt55"
FABLE_MODEL_ID = "M6_fable5"
NEAR_BOUNDARY_THRESHOLD = 3

HARD_EXCEPTION_BOOKS = {"Jer", "Dan", "Esth", "Rev"}
HARD_EXCEPTION_SCOPES = {
    "Mark.16",
    "John.7.53",
    "John.8.",
    "Rom.16.25",
    "Deut.32.8",
    "Deut.32.9",
    "1John.5.6",
    "1John.5.7",
    "1John.5.8",
}

REFINED_CLASSES = {
    "codex_fable_owner_ready_candidate",
    "minor_near_boundary_offset",
    "real_literary_disagreement",
    "frontier_review_required",
    "harness_fix_or_rerun_required",
    "owner_decision_required",
}


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(_strip_front_matter(path.read_text(encoding="utf-8")))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


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
            rows.append(row)
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _region_matches_hard_exception(row: dict[str, Any]) -> bool:
    book = str(row.get("book", ""))
    if book in HARD_EXCEPTION_BOOKS:
        return True
    region = str(row.get("region", ""))
    matches = row.get("variant_hot_zone_matches", [])
    if isinstance(matches, list) and matches:
        return True
    return any(scope in region for scope in HARD_EXCEPTION_SCOPES)


def _span_pair_stats(model_spans: dict[str, str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    malformed: list[str] = []
    for model_id, span_raw in model_spans.items():
        try:
            parsed[model_id] = parse_span(span_raw)
        except ValueError:
            malformed.append(model_id)
    shifts: list[int] = []
    overlap_pairs = 0
    total_pairs = 0
    models = sorted(parsed)
    for i, left in enumerate(models):
        for right in models[i + 1 :]:
            total_pairs += 1
            a = parsed[left]
            b = parsed[right]
            if spans_overlap(a, b):
                overlap_pairs += 1
                shifts.append(boundary_shift_verses(a, b))
    return {
        "models_parseable": sorted(parsed),
        "malformed_span_models": malformed,
        "min_boundary_shift_verses": min(shifts) if shifts else None,
        "max_boundary_shift_verses": max(shifts) if shifts else None,
        "overlap_pair_count": overlap_pairs,
        "pair_count": total_pairs,
        "all_parseable_pairs_overlap": bool(total_pairs and overlap_pairs == total_pairs),
    }


def _span_vote_summary(model_spans: dict[str, str]) -> dict[str, Any]:
    counts = Counter(model_spans.values())
    top_span, top_count = ("", 0)
    if counts:
        top_span, top_count = counts.most_common(1)[0]
    return {
        "unique_span_count": len(counts),
        "top_span": top_span,
        "top_span_model_count": top_count,
        "span_counts": dict(sorted(counts.items())),
    }


def _refined_class(row: dict[str, Any], stats: dict[str, Any]) -> str:
    status = str(row.get("docket_status", ""))
    if _region_matches_hard_exception(row) or row.get("requires_frontier_review") is True or status == "frontier_review_required":
        return "frontier_review_required"
    if status == "harness_fix_or_rerun_required" or row.get("delta_kind") == "coverage_gap":
        return "harness_fix_or_rerun_required"
    if row.get("codex_fable_alignment") is True:
        return "codex_fable_owner_ready_candidate"
    min_shift = stats.get("min_boundary_shift_verses")
    if row.get("near_miss") is True or (isinstance(min_shift, int) and min_shift <= NEAR_BOUNDARY_THRESHOLD):
        return "minor_near_boundary_offset"
    if row.get("delta_kind") == "literature_routing_disagreement":
        return "real_literary_disagreement"
    return "owner_decision_required"


def _next_gate(refined_class: str) -> str:
    return {
        "codex_fable_owner_ready_candidate": "T472_owner_packet_strengthening_candidate",
        "minor_near_boundary_offset": "near_boundary_metric_review_before_owner_gate",
        "real_literary_disagreement": "codex_reconciliation_or_frontier_if_high_risk",
        "frontier_review_required": "claude_frontier_or_specialist_review",
        "harness_fix_or_rerun_required": "harness_fix_or_model_rerun_before_owner_gate",
        "owner_decision_required": "owner_decision_after_codex_packet",
    }[refined_class]


def refine_delta_rows(deltas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in deltas:
        model_spans = {
            str(model_id): str(span)
            for model_id, span in (row.get("models") or {}).items()
            if isinstance(span, str)
        }
        pair_stats = _span_pair_stats(model_spans)
        vote_summary = _span_vote_summary(model_spans)
        refined = _refined_class(row, pair_stats)
        rows.append(
            {
                "object_type": "t471_near_boundary_delta_refinement_row",
                "schema_version": "t471_near_boundary_delta_refinement_row.v1",
                "source_id": str(row.get("delta_id", "")),
                "book": str(row.get("book", "")),
                "region": str(row.get("region", "")),
                "source_delta_kind": str(row.get("delta_kind", "")),
                "source_docket_status": str(row.get("docket_status", "")),
                "refined_class": refined,
                "recommended_next_gate": _next_gate(refined),
                "near_boundary_threshold_verses": NEAR_BOUNDARY_THRESHOLD,
                "source_near_miss": bool(row.get("near_miss", False)),
                "span_vote_summary": vote_summary,
                "boundary_pair_stats": pair_stats,
                "codex_fable_alignment": bool(row.get("codex_fable_alignment", False)),
                "codex_fable_span": row.get("codex_fable_span"),
                "requires_frontier_review": refined == "frontier_review_required",
                "hard_exception_or_variant_pressure": _region_matches_hard_exception(row),
                "risk_flags": row.get("risk_flags", []),
                "variant_hot_zone_matches": row.get("variant_hot_zone_matches", []),
                "t470_support_level": _support_level_for_refined_class(refined),
                "how_concluded": _how_concluded_for_refined_class(refined),
                "downstream_chunking_implication": _implication_for_refined_class(refined),
                "limits": "T471 is triage evidence only and does not authorize owner selection, reviewed gold, chunk output, or source-tradition decisions.",
                "source_refs": [
                    {
                        "label": "T464 disagreement_delta.jsonl",
                        "path": ".ai/scratch/multi_model_bible_chunking/comparison/disagreement_delta.jsonl",
                    },
                    {
                        "label": "T470 transparent evidence rubric",
                        "path": ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml",
                    },
                ],
                "non_authorizing": True,
                "promotion_authority": "none",
            }
        )
    return rows


def _support_level_for_refined_class(refined_class: str) -> str:
    if refined_class == "codex_fable_owner_ready_candidate":
        return "well_supported_with_project_scope"
    if refined_class == "minor_near_boundary_offset":
        return "supported_but_contextual"
    if refined_class in {"frontier_review_required", "real_literary_disagreement"}:
        return "debated"
    return "supported_but_contextual"


def _how_concluded_for_refined_class(refined_class: str) -> str:
    return {
        "codex_fable_owner_ready_candidate": "M4_codex_gpt55 and M6_fable5 agree on the candidate span, and the source row is not frontier-routed.",
        "minor_near_boundary_offset": "At least one pair of model spans overlaps with a small boundary shift, so the mismatch should be reviewed as a near-boundary offset before escalation.",
        "real_literary_disagreement": "Models route the region as different literary or discourse units rather than a tiny boundary offset.",
        "frontier_review_required": "The source row intersects high-risk, low-confidence, variant, source-tradition, or other frontier review pressure.",
        "harness_fix_or_rerun_required": "The source row points to harness or rerun weakness before an owner decision can be trusted.",
        "owner_decision_required": "The row is not resolved by M4/M6 alignment, near-boundary triage, harness routing, or frontier routing.",
    }[refined_class]


def _implication_for_refined_class(refined_class: str) -> str:
    return {
        "codex_fable_owner_ready_candidate": "May enter a T472 owner packet as candidate evidence after a T470 support/debate table is prepared.",
        "minor_near_boundary_offset": "Do not over-escalate until near-boundary/WindowDiff-style review decides whether the disagreement is only a small offset.",
        "real_literary_disagreement": "Needs Codex reconciliation and possibly frontier review if the literary form is high-risk.",
        "frontier_review_required": "Must go to Claude/frontier or specialist review before any owner/output gate.",
        "harness_fix_or_rerun_required": "Improve harness or rerun affected model lane before owner selection.",
        "owner_decision_required": "Needs an explicit owner-facing option packet before any later promotion.",
    }[refined_class]


def _candidate_support_table(candidate: dict[str, Any], delta: dict[str, Any]) -> list[dict[str, Any]]:
    hard = _region_matches_hard_exception(delta)
    return [
        {
            "claim": "M4_codex_gpt55 and M6_fable5 agree on this candidate span.",
            "support_level": "well_supported_with_project_scope",
            "how_concluded": "The T465 owner docket lists recommended_candidate_basis=codex_fable_alignment for this source_id.",
            "source_refs": [
                {"label": "T465 owner candidate docket", "path": ".ai/context/agent_work/T465/owner_candidate_docket.yaml"},
                {"label": "T464 disagreement delta", "path": ".ai/scratch/multi_model_bible_chunking/comparison/disagreement_delta.jsonl"},
            ],
            "downstream_chunking_implication": "Can be reviewed in T472 as candidate evidence, not as owner selection or reviewed gold.",
            "limits": "Model agreement is never authority and does not bypass owner, Codex, or frontier gates.",
        },
        {
            "claim": "Strong's/original-language metadata is present as evidence only.",
            "support_level": "supported_but_contextual",
            "how_concluded": f"Risk flags for {candidate.get('source_id')} include {', '.join(candidate.get('risk_flags', [])) or 'none'}.",
            "source_refs": [
                {"label": "T470 evidence rubric WS-003/WS-006", "path": ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml"}
            ],
            "downstream_chunking_implication": "Packet should include original-language alignment notes if relevant, but Strong's metadata cannot select the boundary by itself.",
            "limits": "No source-language, lexical, or theology authority is created.",
        },
        {
            "claim": "No hard-exception downgrade is authorized by this docket row.",
            "support_level": "debated" if hard else "not_authorized",
            "how_concluded": "T471 checks T468/T470 hard-exception and variant/source-tradition pressure before recommending any next gate.",
            "source_refs": [
                {"label": "T468 owner faithful-route policy", "path": ".ai/control/t468_owner_faithful_chunking_policy.yaml"},
                {"label": "T470 debated-claim rubric", "path": ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml"},
            ],
            "downstream_chunking_implication": "If a hard exception is present, route to frontier/specialist review; otherwise keep the row as owner-packet candidate evidence only.",
            "limits": "This row does not decide variants, source tradition, inspiration, canon, or theology.",
        },
    ]


def _span_length_estimate(delta: dict[str, Any]) -> int:
    value = delta.get("verses_disagreeing")
    if isinstance(value, int):
        return value
    return 999


def build_owner_candidate_docket(candidates: list[dict[str, Any]], deltas_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    enriched: list[dict[str, Any]] = []
    for candidate in candidates:
        source_id = str(candidate.get("source_id", ""))
        delta = deltas_by_id[source_id]
        enriched.append(
            {
                "source_id": source_id,
                "book": str(delta.get("book", "")),
                "span": str(candidate.get("span", "")),
                "span_length_verses_estimate": _span_length_estimate(delta),
                "recommended_candidate_basis": candidate.get("recommended_candidate_basis"),
                "risk_flags": candidate.get("risk_flags", []),
                "variant_hot_zone_matches": delta.get("variant_hot_zone_matches", []),
                "expert_lanes": candidate.get("expert_lanes", []),
                "t470_support_debate_table": _candidate_support_table(candidate, delta),
                "non_authorizing": True,
                "promotion_authority": "none",
            }
        )

    preferred_order = {"DELTA-2John-001": 0, "DELTA-2Tim-004": 1, "DELTA-Num-036": 2}
    enriched.sort(key=lambda row: (preferred_order.get(str(row["source_id"]), 10), row["span_length_verses_estimate"], row["source_id"]))
    for rank, row in enumerate(enriched, start=1):
        row["t471_owner_packet_priority_rank"] = rank

    first = enriched[0]
    return {
        "object_type": "t471_owner_candidate_support_debate_docket",
        "schema_version": "t471_owner_candidate_support_debate_docket.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_task_id": "T465",
        "source_docket": ".ai/context/agent_work/T465/owner_candidate_docket.yaml",
        "candidate_count": len(enriched),
        "recommended_first_t472_candidate": {
            "source_id": first["source_id"],
            "span": first["span"],
            "rationale": "First candidate is the safest small owner-packet starting point under T470: M4/M6 aligned, short, and non-authorizing.",
            "non_authorizing": True,
            "promotion_authority": "none",
        },
        "candidates": enriched,
        "non_authorizations": [
            "target_selection",
            "reviewed_gold_promotion",
            "chunk_output",
            "child_spans",
            "route_or_evaluator_behavior",
            "graph_retrieval_or_vector_truth",
            "source_tradition_preference",
            "canon_change",
            "variant_or_inspiration_decision",
            "theology_authority",
        ],
        "non_authorizing": True,
        "promotion_authority": "none",
    }


def _summary_markdown(refined_rows: list[dict[str, Any]], owner_docket: dict[str, Any]) -> str:
    counts = Counter(row["refined_class"] for row in refined_rows)
    first = owner_docket["recommended_first_t472_candidate"]
    lines = [
        "# T471 Near-Boundary Refinement Summary",
        "",
        "T471 refines T464/T465 comparison evidence without mutating the frozen comparison outputs.",
        "",
        "## Refined Delta Counts",
    ]
    for refined_class in sorted(REFINED_CLASSES):
        lines.append(f"- {refined_class}: {counts.get(refined_class, 0)}")
    lines.extend(
        [
            "",
            "## Recommended First T472 Candidate",
            f"- source_id: {first['source_id']}",
            f"- span: {first['span']}",
            "- status: owner-packet candidate evidence only",
            "",
            "## How To Use This",
            "- Use `minor_near_boundary_offset` rows for WindowDiff/near-boundary review before escalation.",
            "- Use `codex_fable_owner_ready_candidate` rows to prepare owner packets, starting with the recommended first candidate.",
            "- Keep `frontier_review_required` rows with Claude/frontier or specialist lanes.",
            "- Keep `harness_fix_or_rerun_required` rows out of owner promotion until harness issues are addressed.",
            "",
            "## Non-Authorizations",
            "- No target selection.",
            "- No reviewed gold.",
            "- No chunk output.",
            "- No child spans.",
            "- No route/evaluator behavior changes.",
            "- No graph/retrieval/vector truth.",
            "- No source-tradition choice, canon change, variant/inspiration decision, or theology authority.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_outputs(root: Path = ROOT) -> dict[str, Any]:
    deltas = _read_jsonl(root / ".ai" / "scratch" / "multi_model_bible_chunking" / "comparison" / "disagreement_delta.jsonl")
    t465 = _read_yaml(root / ".ai" / "context" / "agent_work" / "T465" / "owner_candidate_docket.yaml")
    candidates = t465.get("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError("T465 owner candidate docket candidates must be a list")
    deltas_by_id = {str(row.get("delta_id", "")): row for row in deltas}
    refined = refine_delta_rows(deltas)
    owner_docket = build_owner_candidate_docket(candidates, deltas_by_id)
    return {
        "refined": refined,
        "owner_docket": owner_docket,
        "summary": _summary_markdown(refined, owner_docket),
    }


def write_outputs(outputs: dict[str, Any]) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    _write_jsonl(DELTA_OUT, outputs["refined"])
    _write_yaml(OWNER_OUT, outputs["owner_docket"])
    SUMMARY_OUT.write_text(outputs["summary"], encoding="utf-8")


def _outputs_match(outputs: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not DELTA_OUT.is_file() or not OWNER_OUT.is_file() or not SUMMARY_OUT.is_file():
        return ["T471 outputs are missing; run builder without --check"]
    actual_refined = _read_jsonl(DELTA_OUT)
    actual_owner = _read_yaml(OWNER_OUT)
    actual_summary = SUMMARY_OUT.read_text(encoding="utf-8")
    if actual_refined != outputs["refined"]:
        errors.append("near_boundary_delta_refinement.jsonl is stale")
    expected_owner = dict(outputs["owner_docket"])
    actual_owner_compare = dict(actual_owner)
    expected_owner.pop("generated_at", None)
    actual_owner_compare.pop("generated_at", None)
    if actual_owner_compare != expected_owner:
        errors.append("owner_candidate_support_debate_docket.yaml is stale")
    if actual_summary != outputs["summary"]:
        errors.append("refinement_summary.md is stale")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated outputs are current")
    args = parser.parse_args(argv)
    outputs = build_outputs()
    if args.check:
        errors = _outputs_match(outputs)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("T471 generated refinement artifacts are current.")
        return 0
    write_outputs(outputs)
    print(f"Wrote {DELTA_OUT}")
    print(f"Wrote {OWNER_OUT}")
    print(f"Wrote {SUMMARY_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
