#!/usr/bin/env python3
"""Fast scratch-lane draft generator from sprint queue + T411 claims."""
from __future__ import annotations

import argparse
import importlib.util
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
    "2John": "2john_opening",
    "3John": "3john_opening",
    "Jas": "jas_opening",
    "2Cor": "2cor_opening",
    "1Tim": "1tim_opening",
    "Rom": "rom_opening",
    "Matt": "matt_opening",
    "Mark": "mark_opening",
    "Luke": "luke_opening",
    "Hag": "hag_opening",
    "Ps": "ps117_whole",
    "Gen": "gen_genealogy",
    "Exod": "exod_offering_list",
    "Num": "num_census",
    "Josh": "josh_kings_list",
    "Judg": "judg_minor_judges",
    "Ruth": "ruth_genealogy",
    "1Sam": "1sam_gift_list",
    "2Sam": "2sam_mighty_men",
    "1Kgs": "1kgs_officials",
    "2Kgs": "2kgs_regnal_notice",
    "1Chr": "1chr_genealogy",
    "2Chr": "2chr_inventory",
    "Ezra": "ezra_returnee_list",
    "Neh": "neh_returnee_list",
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


def _write_sprint_queue(data: dict[str, Any]) -> None:
    header = (
        "---\n"
        "object_type: scratch_prep_sprint_queue\n"
        "schema_version: scratch_prep_sprint_queue.v1\n"
        "---\n"
    )
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    SPRINT_QUEUE.write_text(header + body, encoding="utf-8")


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


def _discover_existing_drafts() -> set[str]:
    existing: set[str] = set()
    for path in DRAFT_DIR.glob("*_draft.md"):
        match = re.search(r"T402-LC-\d+", path.read_text(encoding="utf-8"))
        if match:
            existing.add(match.group(0))
    return existing


def _escalation_packet(candidate_id: str) -> str:
    packet_dir = ROOT / ".ai" / "context" / "agent_work" / "T411" / "escalation_packets"
    matches = list(packet_dir.glob(f"{candidate_id}_*.md"))
    if not matches:
        return "(none — theology pressure documented in T411 claims only)"
    return f".ai/context/agent_work/T411/escalation_packets/{matches[0].name}"


def _draft_filename(book: str, candidate_id: str, lane_id: str) -> str:
    slug = SLUG_BY_BOOK.get(book)
    if not slug:
        slug = f"{book.lower()}_{candidate_id.rsplit('-', 1)[-1]}"
    return f"{slug}_draft.md"


def _batch_sort_key(batch_id: str) -> tuple[int, str]:
    match = re.search(r"(\d+)$", batch_id)
    return (int(match.group(1)) if match else 9999, batch_id)


def _queued_batches(sprint: dict[str, Any]) -> list[dict[str, Any]]:
    batches = sprint.get("batches", [])
    return [
        b
        for b in batches
        if b.get("status", "queued") not in ("complete", "skipped")
    ]


def list_queue() -> None:
    sprint = _read_yaml(SPRINT_QUEUE)
    existing = _discover_existing_drafts()
    print(f"sprint_id: {sprint.get('sprint_id')}")
    print(f"session_target_hours: {sprint.get('session_target_hours', 'n/a')}")
    for batch in sorted(sprint.get("batches", []), key=lambda b: _batch_sort_key(b["batch_id"])):
        status = batch.get("status", "queued")
        candidates = batch.get("candidates", [])
        done = sum(1 for cid in candidates if cid in existing)
        print(f"  {batch['batch_id']}: {status} ({done}/{len(candidates)} drafted) — {batch.get('lane', '')}")


def generate_batch(batch_id: str, *, skip_existing: bool = False, mark_complete: bool = False) -> list[str]:
    sprint = _read_yaml(SPRINT_QUEUE)
    batch = next((b for b in sprint.get("batches", []) if b.get("batch_id") == batch_id), None)
    if batch is None:
        raise ValueError(f"unknown batch_id: {batch_id}")
    candidates = _load_candidates()
    claims_by_span = _load_claims()
    existing = _discover_existing_drafts() if skip_existing else set()
    written: list[str] = []
    trace_rows: list[dict[str, Any]] = []

    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    for candidate_id in batch.get("candidates", []):
        if skip_existing and candidate_id in existing:
            print(f"  skip {candidate_id} (draft exists)")
            continue
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
        out = DRAFT_DIR / _draft_filename(book, candidate_id, meta["lane_id"])
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

    if trace_rows:
        trace_path = WORK_DIR / f"claim_traceability_{batch_id}.jsonl"
        with trace_path.open("w", encoding="utf-8") as fh:
            for row in trace_rows:
                fh.write(json.dumps(row) + "\n")
        written.append(trace_path.relative_to(ROOT).as_posix())

    if mark_complete and written:
        for b in sprint.get("batches", []):
            if b.get("batch_id") == batch_id:
                b["status"] = "complete"
        _write_sprint_queue(sprint)

    return written


def run_queued(*, skip_existing: bool = True, mark_complete: bool = True) -> list[str]:
    sprint = _read_yaml(SPRINT_QUEUE)
    all_written: list[str] = []
    for batch in sorted(_queued_batches(sprint), key=lambda b: _batch_sort_key(b["batch_id"])):
        batch_id = batch["batch_id"]
        print(f"=== {batch_id} ({batch.get('lane', '')}) ===")
        paths = generate_batch(batch_id, skip_existing=skip_existing, mark_complete=mark_complete)
        if not paths:
            print(f"  (no new files for {batch_id})")
            continue
        for path in paths:
            print(f"  {path}")
        all_written.extend(paths)
    return all_written


def run_through(through_batch: str, **kwargs: Any) -> list[str]:
    sprint = _read_yaml(SPRINT_QUEUE)
    through_num = _batch_sort_key(through_batch)[0]
    all_written: list[str] = []
    for batch in sorted(sprint.get("batches", []), key=lambda b: _batch_sort_key(b["batch_id"])):
        if _batch_sort_key(batch["batch_id"])[0] > through_num:
            break
        if batch.get("status") == "complete":
            continue
        batch_id = batch["batch_id"]
        print(f"=== {batch_id} ===")
        paths = generate_batch(batch_id, **kwargs)
        for path in paths:
            print(f"  {path}")
        all_written.extend(paths)
    return all_written


def validate_outputs() -> list[str]:
    validator_path = ROOT / "scripts" / "validate_t417_batch2_review_packet_drafts.py"
    spec = importlib.util.spec_from_file_location("validate_t417_drafts", validator_path)
    if spec is None or spec.loader is None:
        return [f"cannot load validator at {validator_path}"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_drafts()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", help="single batch_id from sprint queue")
    parser.add_argument("--run-queued", action="store_true", help="generate all queued batches in order")
    parser.add_argument("--through", metavar="BATCH_ID", help="generate queued batches up through this id")
    parser.add_argument("--list", action="store_true", help="show sprint queue status")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--no-skip-existing", action="store_true", help="regenerate even if draft exists")
    parser.add_argument("--no-mark-complete", action="store_true", help="do not update queue status")
    args = parser.parse_args()

    skip_existing = not args.no_skip_existing
    mark_complete = not args.no_mark_complete

    if args.list:
        list_queue()
        return 0

    if args.validate_only:
        errors = validate_outputs()
    elif args.run_queued:
        run_queued(skip_existing=skip_existing, mark_complete=mark_complete)
        errors = validate_outputs()
    elif args.through:
        run_through(
            args.through,
            skip_existing=skip_existing,
            mark_complete=mark_complete,
        )
        errors = validate_outputs()
    elif args.batch:
        paths = generate_batch(args.batch, skip_existing=skip_existing, mark_complete=mark_complete)
        print("generated:")
        for path in paths:
            print(f"  {path}")
        errors = validate_outputs()
    else:
        parser.error("specify --batch, --run-queued, --through, --list, or --validate-only")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("scratch prep sprint: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
