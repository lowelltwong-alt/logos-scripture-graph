#!/usr/bin/env python3
"""Scratch phase ladder runner: strengthening prep (phase 4) + owner gate prep (phase 5)."""
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
        r"candidate_id: (T402-LC-\d+), book: (\w+).*?proposed_parent: ([^,]+),"
        r".*?why_low_complexity: \"([^\"]+)\"",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        cid, book, span, why = match.groups()
        found[cid] = {"book": book, "span": span, "why_low_complexity": why}
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
    candidates = _load_candidates()
    drafts = _discover_drafts()
    written: list[str] = []
    OWNER_GATE_DIR.mkdir(parents=True, exist_ok=True)

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
            entry = {
                "candidate_id": cid,
                "book": row.get("book", meta.get("book", "")),
                "span": row.get("osis_ref_or_span", meta.get("span", "")),
                "strengthening_prep": (
                    STRENGTHEN_DIR
                    / f"{drafts[cid].stem.replace('_draft', '')}_strengthening_prep.md"
                ).relative_to(ROOT).as_posix(),
            }
            if entry not in by_batch.setdefault(batch_key, []):
                by_batch[batch_key].append(entry)

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
        out_path.write_text(
            "---\n" + yaml.safe_dump(packet, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        written.append(out_path.relative_to(ROOT).as_posix())
    return written


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
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        errors = validate_strengthening_prep() + validate_owner_gate_prep()
    else:
        queue = _read_yaml(QUEUE)
        skip_ids = set(queue.get("skip_strengthening_candidate_ids", []))
        errors: list[str] = []
        if args.all or args.strengthening:
            paths = run_strengthening_prep(skip_ids)
            print(f"strengthening prep: {len(paths)} files")
            for p in paths[:5]:
                print(f"  {p}")
            if len(paths) > 5:
                print(f"  ... and {len(paths) - 5} more")
        if args.all or args.owner_gate:
            paths = run_owner_gate_prep(skip_ids)
            print(f"owner gate prep: {len(paths)} batch packets")
            for p in paths:
                print(f"  {p}")
        for step in queue.get("t410_ladder_steps", []):
            sid = step.get("step_id")
            if sid == "strengthening_prep" and (args.all or args.strengthening):
                step["status"] = "complete"
            if sid == "owner_gate_prep" and (args.all or args.owner_gate):
                step["status"] = "complete"
        _write_queue(queue)
        errors = validate_strengthening_prep() + validate_owner_gate_prep()

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("scratch phase ladder: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
