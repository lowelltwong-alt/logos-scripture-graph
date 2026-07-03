#!/usr/bin/env python3
"""Scratch phase ladder runner: strengthening through output-pilot prep (phases 4-8)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
QUEUE = ROOT / ".ai" / "scratch" / "prep_sprint" / "scratch_phase_ladder_queue.yaml"
DRAFT_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "review_packet_drafts"
STRENGTHEN_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "review_packet_strengthening_prep"
OWNER_GATE_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "owner_gate_prep"
GOLD_PREP_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "reviewed_gold_promotion_prep"
HARNESS_PREP_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "route_harness_prep"
OUTPUT_PREP_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "output_pilot_prep"
WORK_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417"
LC_QUEUE = ROOT / ".ai" / "control" / "whole_bible_low_complexity_chunking_candidate_queue.yaml"

REQUIRED_STRENGTHEN_MARKERS = (
    "strengthening_prep_pending_codex",
    "Strengthened packet: false",
    "Reviewed gold promoted: false",
    "Implementation allowed: false",
    "No reviewed gold is promoted.",
    "## Contextual Reading Fields",
    "## Proposed Review Options",
)

FORBIDDEN_STRENGTHEN_MARKERS = (
    "eval/chunking_gold/",
    "Strengthened packet: true",
    "reviewed_gold_promoted: true",
    "authorizes_chunk_output",
)

FORBIDDEN_PREP_MARKERS = (
    "eval/chunking_gold/",
    "promoted_as_reviewed_gold: true",
    "output_change_authorized: true",
    "implementation_authorized: true",
    "authorizes_chunk_output_change: true",
    "authorizes_exact_additive_parent_overlay: true",
)

REQUIRED_GOLD_PREP_FIELDS = (
    "gold_promotion_prep_pending_owner_and_codex",
    "promoted_as_reviewed_gold: false",
    "reviewed_gold_promotion",
)

REQUIRED_HARNESS_PREP_FIELDS = (
    "harness_prep_pending_codex",
    "route_isolation_harness_prep",
)

REQUIRED_OUTPUT_PREP_FIELDS = (
    "output_pilot_prep_pending_owner_and_codex",
    "output_change_authorized: false",
    "implementation_authorized: false",
)

STRENGTHEN_HEADER = """# {title}

## Status

- Status: `strengthening_prep_pending_codex`
- T402 candidate ID: `{candidate_id}`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `{span}`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Review-only strengthening prep: true
- Source draft: `{source_draft}`
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `{escalation_packet}`

This strengthening prep lives under `.ai/context/agent_work/T417/review_packet_strengthening_prep/` only.
It does not authorize reviewed gold, chunk output, child spans, route/evaluator change, or theology authority.
Codex promotion review is deferred per scratch lane policy.

## Review Target

`{span}` — {why_low_complexity}

## Current Chunk Behavior

Observed behavior is inherited from the Rust observation substrate and current generated baseline surfaces.
No fresh chunk regeneration was performed in scratch lane. Diagnostic only — not reviewed gold.

## Contextual Reading Fields

- exact_passage_scope: `{span}`.
- immediate_following_context: see book/chapter context; following unit must remain visible.
- source_metadata_context_if_used: paragraph markers, footnotes, Strong's-style tags are evidence only.
- assumptions_avoided: theology pressure flags and lane metadata are not chunk authority.
- orthodox_options_preserved: Nicene/Chalcedonian orthodox readings remain possible under canonical Scripture.
- theological_downstream_risks: see escalation packet and T411 low-confidence claims.
- non_authorizations: reviewed-gold promotion, child-span selection, chunk output, route/evaluator behavior,
  graph/retrieval/vector truth, boundary import, preferred reading, source-tradition preference, and
  denominational systematic theology as chunk authority.

## Claim Traceability

{claim_lines}

## Variant And Source-Tradition Flags

- variant_sensitive_for_current_packet: false
- source_tradition_preference_authorized: false
- preferred_reading_authorized: false

## Theological Risk Flags

- Theology pressure from T411 queue is evidence-only and non-boundary.
- Liberal-critical, anti-supernatural, anti-canonical, heterodox, or one-denomination systematic defaults refused.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: prep treated as owner docket or Codex approval. Fix: require Codex promotion review and standing policy.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

## Proposed Review Options

- Preserve current chunk behavior and record text-local structure concern only.
- Later owner may promote parent `{span}` with no child chunks under standing policy after Codex review.
- Defer if frontier review finds pressure framing required beyond text-local structure.

{theology_note}

No reviewed gold is promoted.
"""


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def _write_queue(data: dict[str, Any]) -> None:
    header = (
        "---\nobject_type: scratch_phase_ladder_queue\nschema_version: scratch_phase_ladder_queue.v1\n---\n"
    )
    QUEUE.write_text(header + yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _load_candidates() -> dict[str, dict[str, str]]:
    text = LC_QUEUE.read_text(encoding="utf-8")
    found: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"candidate_id: (T402-LC-\d+), book: (\w+), lane_id: ([^,]+), "
        r"proposed_parent: ([^,]+),"
        r".*?why_low_complexity: \"([^\"]+)\"",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        cid, book, lane, span, why = match.groups()
        found[cid] = {
            "book": book,
            "lane_id": lane.strip(),
            "span": span,
            "why_low_complexity": why,
        }
    return found


def _load_claims_by_span() -> dict[str, list[dict[str, Any]]]:
    claims_path = ROOT / ".ai" / "context" / "agent_work" / "T411" / "confidence_register.jsonl"
    by_span: dict[str, list[dict[str, Any]]] = {}
    for line in claims_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        by_span.setdefault(row.get("osis_ref_or_span", ""), []).append(row)
    return by_span


def _escalation_packet(candidate_id: str) -> str:
    packet_dir = ROOT / ".ai" / "context" / "agent_work" / "T411" / "escalation_packets"
    matches = list(packet_dir.glob(f"{candidate_id}_*.md"))
    if not matches:
        return "(none — see T411 claims)"
    return f".ai/context/agent_work/T411/escalation_packets/{matches[0].name}"


def _discover_drafts() -> dict[str, Path]:
    drafts: dict[str, Path] = {}
    for path in sorted(DRAFT_DIR.glob("*_draft.md")):
        match = re.search(r"T402-LC-\d+", path.read_text(encoding="utf-8"))
        if match:
            drafts[match.group(0)] = path
    return drafts


def _gold_case_slug(book: str, span: str) -> str:
    match = re.match(r"(\w+)\.(\d+)\.(\d+)", span)
    if match:
        b, chapter, verse = match.groups()
        return f"{b.lower()}_{chapter}_{verse}_parent_only_reviewed_gold_prep"
    return f"{book.lower()}_parent_only_reviewed_gold_prep"


def _overlay_id(lane_id: str, span: str, candidate_id: str) -> str:
    start = span.split("-")[0] if "-" in span else span
    end = span.split("-")[-1] if "-" in span else span
    suffix = candidate_id.replace("T402-LC-", "LC")
    return (
        f"chunk--eng-web--chunk-policy-v0.1.0--{lane_id}--"
        f"{start}--{end}--T417-PREP-{suffix}"
    )


def _batch_entries(skip_ids: set[str]) -> dict[str, list[dict[str, str]]]:
    candidates = _load_candidates()
    drafts = _discover_drafts()
    by_batch: dict[str, list[dict[str, str]]] = {}
    for batch_id in range(2, 11):
        trace_path = WORK_DIR / f"claim_traceability_batch{batch_id}.jsonl"
        if not trace_path.is_file():
            continue
        batch_key = f"batch{batch_id}"
        for line in trace_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            cid = row.get("candidate_id")
            if not isinstance(cid, str) or cid in skip_ids:
                continue
            if cid not in drafts:
                continue
            meta = candidates.get(cid, {})
            slug = drafts[cid].stem.replace("_draft", "")
            entry = {
                "candidate_id": cid,
                "book": row.get("book", meta.get("book", "")),
                "lane_id": meta.get("lane_id", "parent_overlay"),
                "span": row.get("osis_ref_or_span", meta.get("span", "")),
                "draft": drafts[cid].relative_to(ROOT).as_posix(),
                "strengthening_prep": (
                    STRENGTHEN_DIR / f"{slug}_strengthening_prep.md"
                ).relative_to(ROOT).as_posix(),
            }
            if entry not in by_batch.setdefault(batch_key, []):
                by_batch[batch_key].append(entry)
    return by_batch


def _dump_yaml_packet(packet: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(packet, sort_keys=False, allow_unicode=True)


def run_strengthening_prep(skip_ids: set[str]) -> list[str]:
    candidates = _load_candidates()
    claims_by_span = _load_claims_by_span()
    drafts = _discover_drafts()
    written: list[str] = []
    STRENGTHEN_DIR.mkdir(parents=True, exist_ok=True)

    for candidate_id, draft_path in sorted(drafts.items(), key=lambda x: x[0]):
        if candidate_id in skip_ids:
            continue
        meta = candidates.get(candidate_id)
        if not meta:
            continue
        span = meta["span"]
        book = meta["book"]
        claim_rows = claims_by_span.get(span, [])
        claim_lines = "\n".join(
            f"- {r['claim_id']} ({r['confidence']}): {r['confidence_reason'][:100]}."
            for r in claim_rows[:4]
        )
        theology_note = "Theology flags are evidence-only; parent-only text-local structure governs."
        for r in claim_rows:
            if r.get("theology_sensitive"):
                theology_note = f"Theology pressure ({r['claim_id']}) is non-boundary; see escalation packet."
                break
        slug = draft_path.stem.replace("_draft", "")
        out_name = f"{slug}_strengthening_prep.md"
        out_path = STRENGTHEN_DIR / out_name
        body = STRENGTHEN_HEADER.format(
            title=f"{book} {span} Review Packet (Strengthening Prep)",
            candidate_id=candidate_id,
            span=span,
            source_draft=draft_path.relative_to(ROOT).as_posix(),
            escalation_packet=_escalation_packet(candidate_id),
            why_low_complexity=meta["why_low_complexity"],
            claim_lines=claim_lines or "- (no claims loaded)",
            theology_note=theology_note,
        )
        out_path.write_text(body, encoding="utf-8")
        written.append(out_path.relative_to(ROOT).as_posix())
    return written


def run_owner_gate_prep(skip_ids: set[str]) -> list[str]:
    written: list[str] = []
    OWNER_GATE_DIR.mkdir(parents=True, exist_ok=True)
    by_batch = _batch_entries(skip_ids)

    for batch_key, entries in sorted(by_batch.items()):
        if not entries:
            continue
        packet = {
            "object_type": "owner_gate_prep_packet",
            "schema_version": "owner_gate_prep_packet.v1",
            "batch_id": batch_key,
            "status": "owner_gate_prep_pending_standing_policy",
            "owner_unlock_phrase": "APPROVE_STANDING_ESCALATION_POLICY",
            "standing_policy": ".ai/control/standing_owner_escalation_policy.yaml",
            "standing_policy_note": (
                "APPROVE_STANDING_ESCALATION_POLICY records owner disposition toward the "
                "standing escalation policy only. It does not by itself authorize reviewed "
                "gold promotion, chunk output change, route isolation harness, or output pilot."
            ),
            "informational_follow_on_steps": [
                {
                    "step": "final_review_packet_strengthening",
                    "requires": "per_batch_owner_docket_or_standing_disposition_plus_codex_review",
                    "authorizes_in_this_prep": "nothing",
                },
                {
                    "step": "reviewed_gold_promotion_prep",
                    "requires": "explicit_owner_gate_per_batch_plus_codex_promotion_review",
                    "authorizes_in_this_prep": "nothing",
                },
                {
                    "step": "route_isolation_harness_prep",
                    "requires": "explicit_owner_gate_per_batch_plus_codex_promotion_review",
                    "authorizes_in_this_prep": "nothing",
                },
                {
                    "step": "output_pilot_prep",
                    "requires": "explicit_owner_gate_per_batch_plus_codex_promotion_review",
                    "authorizes_in_this_prep": "nothing",
                },
            ],
            "owner_options_not_authorizing": [
                {
                    "option_id": f"{batch_key.upper()}-A",
                    "label": (
                        "Record intent to proceed parent-only per standing disposition "
                        "(not gold/output authorization)"
                    ),
                    "rationale": "Text-local spans with theology flags evidence-only",
                },
                {
                    "option_id": f"{batch_key.upper()}-B",
                    "label": "Hold batch pending frontier review on medium-risk theology framing",
                    "rationale": "Conservative hold if Codex flags strengthening gaps",
                },
                {
                    "option_id": f"{batch_key.upper()}-C",
                    "label": "Defer batch until explicit per-batch owner docket",
                    "rationale": "Override standing policy for this batch only",
                },
            ],
            "candidates": entries,
            "non_authorizations": [
                "reviewed_gold_promotion",
                "chunk_output_change",
                "child_span_selection",
                "standing_policy_activation",
                "codex_review_bypass",
                "ladder_auto_unlock_from_standing_phrase",
            ],
            "reviewer_notes": (
                "Scratch lane owner-gate PREP only. Standing phrase records disposition; "
                "each ladder step still needs separate owner and Codex gates. "
                "Codex promotion review still required before canon surfaces change."
            ),
        }
        out_path = OWNER_GATE_DIR / f"{batch_key}_owner_gate_prep.yaml"
        out_path.write_text(_dump_yaml_packet(packet), encoding="utf-8")
        written.append(out_path.relative_to(ROOT).as_posix())
    return written


def run_gold_promotion_prep(skip_ids: set[str]) -> list[str]:
    written: list[str] = []
    GOLD_PREP_DIR.mkdir(parents=True, exist_ok=True)
    for _batch_key, entries in sorted(_batch_entries(skip_ids).items()):
        for entry in entries:
            cid = entry["candidate_id"]
            book = entry["book"]
            span = entry["span"]
            slug = Path(entry["draft"]).stem.replace("_draft", "")
            packet = {
                "object_type": "reviewed_gold_promotion_prep_packet",
                "schema_version": "reviewed_gold_promotion_prep_packet.v1",
                "candidate_id": cid,
                "book": book,
                "status": "gold_promotion_prep_pending_owner_and_codex",
                "selected_parent": span,
                "promoted_as_reviewed_gold": False,
                "parent_span_as_chunk_boundary_authorized": False,
                "child_spans_authorized": False,
                "source_draft": entry["draft"],
                "strengthening_prep": entry["strengthening_prep"],
                "proposed_reviewed_gold_case_id": _gold_case_slug(book, span),
                "standing_policy": ".ai/control/standing_owner_escalation_policy.yaml",
                "precedent": ".ai/control/t414_batch1_parent_only_reviewed_gold_promotion.yaml",
                "non_authorizations": [
                    "reviewed_gold_promotion",
                    "eval/chunking_gold_writes",
                    "chunk_output_change",
                    "child_span_selection",
                    "standing_policy_activation",
                    "codex_review_bypass",
                    "parent_span_as_chunk_boundary",
                ],
                "reviewer_notes": (
                    "Scratch lane gold-promotion PREP only. Does not write eval/chunking_gold. "
                    "Owner + Codex gates still required before any promotion."
                ),
            }
            out_path = GOLD_PREP_DIR / f"{slug}_gold_promotion_prep.yaml"
            out_path.write_text(_dump_yaml_packet(packet), encoding="utf-8")
            written.append(out_path.relative_to(ROOT).as_posix())
    return written


def run_harness_prep(skip_ids: set[str]) -> list[str]:
    written: list[str] = []
    HARNESS_PREP_DIR.mkdir(parents=True, exist_ok=True)
    for batch_key, entries in sorted(_batch_entries(skip_ids).items()):
        if not entries:
            continue
        packet = {
            "object_type": "route_isolation_harness_prep_packet",
            "schema_version": "route_isolation_harness_prep_packet.v1",
            "batch_id": batch_key,
            "status": "harness_prep_pending_codex",
            "harness_reference": "scripts/chunking/route_isolation_harness.py",
            "precedent": ".ai/control/t415_batch1_route_isolation_harness.yaml",
            "checks_prep_only": [
                "non_target_byte_identity_comparison",
                "exact_parent_target_change_allowance_only",
                "child_span_denial_check",
            ],
            "target_spans": [e["span"] for e in entries],
            "candidates": [
                {
                    "candidate_id": e["candidate_id"],
                    "span": e["span"],
                    "gold_promotion_prep": (
                        GOLD_PREP_DIR
                        / f"{Path(e['draft']).stem.replace('_draft', '')}_gold_promotion_prep.yaml"
                    ).relative_to(ROOT).as_posix(),
                }
                for e in entries
            ],
            "non_authorizations": [
                "chunk_output_change",
                "child_span_selection",
                "route_behavior_change",
                "reviewed_gold_promotion",
                "harness_execution_in_scratch",
            ],
            "reviewer_notes": (
                "Scratch lane route-isolation harness PREP only. Checklist references T415 "
                "harness; no harness run or output change authorized in scratch."
            ),
        }
        out_path = HARNESS_PREP_DIR / f"{batch_key}_route_harness_prep.yaml"
        out_path.write_text(_dump_yaml_packet(packet), encoding="utf-8")
        written.append(out_path.relative_to(ROOT).as_posix())
    return written


def run_output_pilot_prep(skip_ids: set[str]) -> list[str]:
    written: list[str] = []
    OUTPUT_PREP_DIR.mkdir(parents=True, exist_ok=True)
    for batch_key, entries in sorted(_batch_entries(skip_ids).items()):
        for entry in entries:
            cid = entry["candidate_id"]
            book = entry["book"]
            span = entry["span"]
            lane_id = entry["lane_id"]
            slug = Path(entry["draft"]).stem.replace("_draft", "")
            packet = {
                "object_type": "output_pilot_prep_packet",
                "schema_version": "output_pilot_prep_packet.v1",
                "candidate_id": cid,
                "book": book,
                "status": "output_pilot_prep_pending_owner_and_codex",
                "selected_parent": span,
                "proposed_overlay_id": _overlay_id(lane_id, span, cid),
                "output_change_authorized": False,
                "implementation_authorized": False,
                "overlay_appended_after_baseline_records": False,
                "baseline_records_mutated": False,
                "gold_promotion_prep": (
                    GOLD_PREP_DIR / f"{slug}_gold_promotion_prep.yaml"
                ).relative_to(ROOT).as_posix(),
                "harness_prep_batch": (
                    HARNESS_PREP_DIR / f"{batch_key}_route_harness_prep.yaml"
                ).relative_to(ROOT).as_posix(),
                "precedent": ".ai/control/t415_batch1_output_pilot_manifest.yaml",
                "non_authorizations": [
                    "chunk_output_change",
                    "implementation",
                    "route_behavior_change",
                    "child_span_selection",
                    "reviewed_gold_promotion",
                    "eval/chunking_gold_writes",
                ],
                "reviewer_notes": (
                    "Scratch lane output-pilot PREP only. Proposed overlay id is informational; "
                    "no chunk regeneration or hash recording performed in scratch."
                ),
            }
            out_path = OUTPUT_PREP_DIR / f"{slug}_output_pilot_prep.yaml"
            out_path.write_text(_dump_yaml_packet(packet), encoding="utf-8")
            written.append(out_path.relative_to(ROOT).as_posix())
    return written


def _validate_prep_dir(
    directory: Path,
    glob_pattern: str,
    required_substrings: tuple[str, ...],
    label: str,
) -> list[str]:
    errors: list[str] = []
    if not directory.is_dir():
        return [f"missing {label} directory"]
    files = list(directory.glob(glob_pattern))
    if not files:
        errors.append(f"no {label} files generated")
    for path in files:
        text = path.read_text(encoding="utf-8")
        for marker in required_substrings:
            if marker not in text:
                errors.append(f"{path.name}: missing {marker!r}")
        for marker in FORBIDDEN_PREP_MARKERS:
            if marker in text:
                errors.append(f"{path.name}: forbidden {marker!r}")
    return errors


def validate_gold_promotion_prep() -> list[str]:
    return _validate_prep_dir(
        GOLD_PREP_DIR,
        "*_gold_promotion_prep.yaml",
        REQUIRED_GOLD_PREP_FIELDS,
        "gold promotion prep",
    )


def validate_harness_prep() -> list[str]:
    return _validate_prep_dir(
        HARNESS_PREP_DIR,
        "*_route_harness_prep.yaml",
        REQUIRED_HARNESS_PREP_FIELDS,
        "route harness prep",
    )


def validate_output_pilot_prep() -> list[str]:
    return _validate_prep_dir(
        OUTPUT_PREP_DIR,
        "*_output_pilot_prep.yaml",
        REQUIRED_OUTPUT_PREP_FIELDS,
        "output pilot prep",
    )


def _all_validate_errors() -> list[str]:
    return (
        validate_strengthening_prep()
        + validate_owner_gate_prep()
        + validate_gold_promotion_prep()
        + validate_harness_prep()
        + validate_output_pilot_prep()
    )


def validate_strengthening_prep() -> list[str]:
    errors: list[str] = []
    if not STRENGTHEN_DIR.is_dir():
        return ["missing strengthening prep directory"]
    files = list(STRENGTHEN_DIR.glob("*_strengthening_prep.md"))
    if not files:
        errors.append("no strengthening prep files generated")
    for path in files:
        text = path.read_text(encoding="utf-8")
        for marker in REQUIRED_STRENGTHEN_MARKERS:
            if marker not in text:
                errors.append(f"{path.name}: missing {marker!r}")
        for marker in FORBIDDEN_STRENGTHEN_MARKERS:
            if marker in text:
                errors.append(f"{path.name}: forbidden {marker!r}")
        if "T402-LC-" not in text:
            errors.append(f"{path.name}: missing candidate id")
    return errors


def validate_owner_gate_prep() -> list[str]:
    errors: list[str] = []
    if not OWNER_GATE_DIR.is_dir():
        return ["missing owner gate prep directory"]
    files = list(OWNER_GATE_DIR.glob("*_owner_gate_prep.yaml"))
    if not files:
        errors.append("no owner gate prep files generated")
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8").split("---\n", 1)[-1])
        if not isinstance(data, dict):
            errors.append(f"{path.name}: invalid yaml")
            continue
        if data.get("status") != "owner_gate_prep_pending_standing_policy":
            errors.append(f"{path.name}: wrong status")
        if "recommended_next_ladder_after_owner_unlock" in data:
            errors.append(
                f"{path.name}: forbidden field recommended_next_ladder_after_owner_unlock"
            )
        if not data.get("standing_policy_note"):
            errors.append(f"{path.name}: missing standing_policy_note")
        follow_on = data.get("informational_follow_on_steps")
        if not isinstance(follow_on, list) or not follow_on:
            errors.append(f"{path.name}: missing informational_follow_on_steps")
        if "reviewed_gold_promotion" not in data.get("non_authorizations", []):
            errors.append(f"{path.name}: missing gold non-authorization")
        if "ladder_auto_unlock_from_standing_phrase" not in data.get("non_authorizations", []):
            errors.append(f"{path.name}: missing ladder auto-unlock non-authorization")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strengthening", action="store_true")
    parser.add_argument("--owner-gate", action="store_true")
    parser.add_argument("--gold-prep", action="store_true")
    parser.add_argument("--harness-prep", action="store_true")
    parser.add_argument("--output-prep", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    run_any = args.all or any(
        (
            args.strengthening,
            args.owner_gate,
            args.gold_prep,
            args.harness_prep,
            args.output_prep,
        )
    )

    if args.validate_only:
        errors = _all_validate_errors()
    elif run_any:
        queue = _read_yaml(QUEUE)
        skip_ids = set(queue.get("skip_strengthening_candidate_ids", []))
        errors: list[str] = []
        if args.all or args.strengthening:
            paths = run_strengthening_prep(skip_ids)
            print(f"strengthening prep: {len(paths)} files")
        if args.all or args.owner_gate:
            paths = run_owner_gate_prep(skip_ids)
            print(f"owner gate prep: {len(paths)} batch packets")
        if args.all or args.gold_prep:
            paths = run_gold_promotion_prep(skip_ids)
            print(f"gold promotion prep: {len(paths)} files")
        if args.all or args.harness_prep:
            paths = run_harness_prep(skip_ids)
            print(f"route harness prep: {len(paths)} batch packets")
        if args.all or args.output_prep:
            paths = run_output_pilot_prep(skip_ids)
            print(f"output pilot prep: {len(paths)} files")
        step_map = {
            "strengthening_prep": args.all or args.strengthening,
            "owner_gate_prep": args.all or args.owner_gate,
            "reviewed_gold_promotion_prep": args.all or args.gold_prep,
            "route_isolation_harness_prep": args.all or args.harness_prep,
            "output_pilot_prep": args.all or args.output_prep,
        }
        for step in queue.get("t410_ladder_steps", []):
            if step_map.get(step.get("step_id")):
                step["status"] = "complete"
        _write_queue(queue)
        errors = _all_validate_errors()
    else:
        parser.print_help()
        return 2

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("scratch phase ladder: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
