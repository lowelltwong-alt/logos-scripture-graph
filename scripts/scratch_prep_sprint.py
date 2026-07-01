#!/usr/bin/env python3
"""Fast scratch-lane draft generator from sprint queue + T411 claims."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPRINT_QUEUE = ROOT / ".ai" / "scratch" / "prep_sprint" / "scratch_prep_sprint_queue.yaml"
LC_QUEUE = ROOT / ".ai" / "control" / "whole_bible_low_complexity_chunking_candidate_queue.yaml"
CLAIMS = ROOT / ".ai" / "context" / "agent_work" / "T411" / "confidence_register.jsonl"
DRAFT_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "review_packet_drafts"
WORK_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417"

DRAFT_TEMPLATE = """# {title}

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `{candidate_id}`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `{span}`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `{escalation_packet}`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`{span}` — {why_low_complexity}

## Claim Traceability

{claim_lines}

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

{theology_note}

No reviewed gold is promoted.
"""

SLUG_BY_BOOK = {
    "Col": "col_closing",
    "1Thess": "1thess_opening",
    "2Thess": "2thess_opening",
    "2Tim": "2tim_closing",
    "Titus": "titus_opening",
    "Gal": "gal_opening",
    "Eph": "eph_closing",
    "Phil": "phil_opening",
    "Phlm": "phlm_opening",
    "Jude": "jude_opening",
    "Jonah": "jonah_opening",
    "Heb": "heb_closing",
    "1Pet": "1pet_closing",
}


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


def _load_candidates() -> dict[str, dict[str, str]]:
    text = LC_QUEUE.read_text(encoding="utf-8")
    found: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"candidate_id: (T402-LC-\d+), book: (\w+), lane_id: ([^,]+), "
        r"proposed_parent: ([^,]+),.*?why_low_complexity: \"([^\"]+)\"",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        cid, book, lane, span, why = match.groups()
        found[cid] = {"book": book, "lane_id": lane, "span": span, "why_low_complexity": why}
    return found


def _load_claims() -> dict[str, list[dict[str, Any]]]:
    by_span: dict[str, list[dict[str, Any]]] = {}
    for line in CLAIMS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        span = row.get("osis_ref_or_span", "")
        by_span.setdefault(span, []).append(row)
    return by_span


def _escalation_packet(candidate_id: str) -> str:
    packet_dir = ROOT / ".ai" / "context" / "agent_work" / "T411" / "escalation_packets"
    matches = list(packet_dir.glob(f"{candidate_id}_*.md"))
    if not matches:
        return ""
    return f".ai/context/agent_work/T411/escalation_packets/{matches[0].name}"


def _draft_filename(book: str, candidate_id: str) -> str:
    slug = SLUG_BY_BOOK.get(book)
    if not slug:
        slug = f"{book.lower()}_{candidate_id.rsplit('-', 1)[-1]}"
    return f"{slug}_draft.md"


def generate_batch(batch_id: str) -> list[str]:
    sprint = _read_yaml(SPRINT_QUEUE)
    batch = next((b for b in sprint.get("batches", []) if b.get("batch_id") == batch_id), None)
    if batch is None:
        raise ValueError(f"unknown batch_id: {batch_id}")
    candidates = _load_candidates()
    claims_by_span = _load_claims()
    written: list[str] = []
    trace_rows: list[dict[str, Any]] = []

    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    for candidate_id in batch.get("candidates", []):
        meta = candidates.get(candidate_id)
        if not meta:
            raise ValueError(f"missing queue metadata for {candidate_id}")
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
        title = f"{book} {span} Review Packet (Draft)"
        body = DRAFT_TEMPLATE.format(
            title=title,
            candidate_id=candidate_id,
            span=span,
            escalation_packet=_escalation_packet(candidate_id),
            why_low_complexity=meta.get("why_low_complexity", meta["lane_id"].replace("_", " ")),
            claim_lines=claim_lines or "- (no claims loaded)",
            theology_note=theology_note,
        )
        out = DRAFT_DIR / _draft_filename(book, candidate_id)
        out.write_text(body, encoding="utf-8")
        written.append(out.relative_to(ROOT).as_posix())
        for row in claim_rows:
            trace_rows.append(
                {
                    "task_id": "T417",
                    "batch_id": batch_id,
                    "candidate_id": candidate_id,
                    "book": book,
                    "osis_ref_or_span": span,
                    "claim_id": row["claim_id"],
                    "confidence": row["confidence"],
                    "theology_sensitive": row.get("theology_sensitive", False),
                    "draft_packet": out.relative_to(ROOT).as_posix(),
                    "non_authorizing": True,
                }
            )

    trace_path = WORK_DIR / f"claim_traceability_{batch_id}.jsonl"
    with trace_path.open("w", encoding="utf-8") as fh:
        for row in trace_rows:
            fh.write(json.dumps(row) + "\n")
    written.append(trace_path.relative_to(ROOT).as_posix())
    return written


def validate_outputs() -> list[str]:
    import importlib.util

    validator_path = ROOT / "scripts" / "validate_t417_batch2_review_packet_drafts.py"
    spec = importlib.util.spec_from_file_location("validate_t417_drafts", validator_path)
    if spec is None or spec.loader is None:
        return [f"cannot load validator at {validator_path}"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_drafts()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", default="batch4", help="batch_id from sprint queue")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if args.validate_only:
        errors = validate_outputs()
    else:
        paths = generate_batch(args.batch)
        print("generated:")
        for p in paths:
            print(f"  {p}")
        errors = validate_outputs()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("scratch prep sprint: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
