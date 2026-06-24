#!/usr/bin/env python3
"""Fail-closed route-isolation comparison for future chunk output pilots.

This harness compares two chunk JSONL surfaces and proves that all
non-target records remain byte-identical. It does not generate chunks and it
does not authorize an output change by itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class RouteIsolationError(ValueError):
    """Raised when a candidate output is not route-isolated."""


@dataclass(frozen=True, order=True)
class OsisRef:
    book: str
    chapter: int
    verse: int

    @classmethod
    def parse(cls, value: str) -> "OsisRef":
        parts = value.split(".")
        if len(parts) != 3 or not parts[0] or not parts[1].isdigit() or not parts[2].isdigit():
            raise RouteIsolationError(f"invalid OSIS ref: {value!r}")
        return cls(parts[0], int(parts[1]), int(parts[2]))


@dataclass(frozen=True)
class OsisSpan:
    start: OsisRef
    end: OsisRef

    @classmethod
    def parse(cls, value: str) -> "OsisSpan":
        if "-" not in value:
            raise RouteIsolationError(f"target span must use start-end form: {value!r}")
        start, end = value.split("-", 1)
        return cls.from_refs(start, end)

    @classmethod
    def from_refs(cls, start: str, end: str) -> "OsisSpan":
        span = cls(OsisRef.parse(start), OsisRef.parse(end))
        if span.start.book != span.end.book:
            raise RouteIsolationError(f"cross-book span is not supported by this harness: {span.label}")
        if (span.end.chapter, span.end.verse) < (span.start.chapter, span.start.verse):
            raise RouteIsolationError(f"span ends before it starts: {span.label}")
        return span

    @property
    def label(self) -> str:
        return f"{self.start.book}.{self.start.chapter}.{self.start.verse}-{self.end.book}.{self.end.chapter}.{self.end.verse}"

    def equals(self, other: "OsisSpan") -> bool:
        return self.start == other.start and self.end == other.end

    def contains(self, other: "OsisSpan") -> bool:
        if self.start.book != other.start.book or self.start.book != other.end.book:
            return False
        return (
            (self.start.chapter, self.start.verse)
            <= (other.start.chapter, other.start.verse)
            <= (other.end.chapter, other.end.verse)
            <= (self.end.chapter, self.end.verse)
        )


@dataclass(frozen=True)
class ChunkLine:
    line_no: int
    raw: bytes
    record: dict[str, Any]
    key: str
    span: OsisSpan


@dataclass(frozen=True)
class IsolationReport:
    baseline_count: int
    candidate_count: int
    baseline_sha256: str
    candidate_sha256: str
    changed_keys: list[str]
    added_keys: list[str]
    removed_keys: list[str]
    changed_spans: list[str]
    non_target_byte_identical: bool
    target_span: str
    child_spans_authorized: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "baseline_count": self.baseline_count,
            "candidate_count": self.candidate_count,
            "baseline_sha256": self.baseline_sha256,
            "candidate_sha256": self.candidate_sha256,
            "changed_keys": self.changed_keys,
            "added_keys": self.added_keys,
            "removed_keys": self.removed_keys,
            "changed_spans": self.changed_spans,
            "non_target_byte_identical": self.non_target_byte_identical,
            "target_span": self.target_span,
            "child_spans_authorized": self.child_spans_authorized,
        }


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _record_span(record: dict[str, Any]) -> OsisSpan:
    if isinstance(record.get("osis_start"), str) and isinstance(record.get("osis_end"), str):
        return OsisSpan.from_refs(record["osis_start"], record["osis_end"])
    if isinstance(record.get("osis_span"), str) and "-" in record["osis_span"]:
        return OsisSpan.parse(record["osis_span"])
    raise RouteIsolationError("record must include osis_start/osis_end or osis_span")


def _record_key(record: dict[str, Any], span: OsisSpan, line_no: int) -> str:
    raw_key = record.get("id") or record.get("chunk_id")
    if isinstance(raw_key, str) and raw_key.strip():
        return raw_key.strip()
    return f"{span.label}#line-{line_no}"


def _load_jsonl(path: Path) -> tuple[bytes, list[ChunkLine]]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise RouteIsolationError(f"{path}: unreadable: {exc}") from exc

    rows: list[ChunkLine] = []
    seen: set[str] = set()
    for index, raw in enumerate(data.splitlines(keepends=True), start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RouteIsolationError(f"{path}:{index}: JSON unreadable: {exc}") from exc
        if not isinstance(record, dict):
            raise RouteIsolationError(f"{path}:{index}: expected JSON object")
        span = _record_span(record)
        key = _record_key(record, span, index)
        if key in seen:
            raise RouteIsolationError(f"{path}:{index}: duplicate chunk key {key!r}")
        seen.add(key)
        rows.append(ChunkLine(index, raw, record, key, span))
    return data, rows


def _has_child_span_payload(record: dict[str, Any]) -> bool:
    for key in ("selected_children", "children", "child_chunks"):
        value = record.get(key)
        if isinstance(value, list) and value:
            return True
    return False


def _is_allowed_target_change(span: OsisSpan, target: OsisSpan, child_spans_authorized: bool) -> bool:
    if span.equals(target):
        return True
    return child_spans_authorized and target.contains(span)


def _assert_allowed_change(line: ChunkLine, target: OsisSpan, child_spans_authorized: bool, label: str) -> None:
    if not _is_allowed_target_change(line.span, target, child_spans_authorized):
        raise RouteIsolationError(
            f"{label} {line.key!r} touches unauthorized span {line.span.label}; "
            f"allowed target is {target.label}"
        )
    if not child_spans_authorized and _has_child_span_payload(line.record):
        raise RouteIsolationError(f"{label} {line.key!r} carries child-span payload without authorization")


def compare_chunk_jsonl(
    baseline_path: Path,
    candidate_path: Path,
    *,
    target_span: str,
    child_spans_authorized: bool = False,
) -> IsolationReport:
    """Compare baseline and candidate chunk JSONL surfaces.

    Non-target records are compared as raw bytes after excluding records whose
    span is exactly the allowed target span. If child spans are not authorized,
    any target-overlap subspan or spillover record fails instead of becoming an
    allowed change.
    """

    target = OsisSpan.parse(target_span)
    baseline_bytes, baseline_rows = _load_jsonl(baseline_path)
    candidate_bytes, candidate_rows = _load_jsonl(candidate_path)

    baseline_by_key = {row.key: row for row in baseline_rows}
    candidate_by_key = {row.key: row for row in candidate_rows}

    changed_keys = sorted(
        key
        for key in baseline_by_key.keys() & candidate_by_key.keys()
        if baseline_by_key[key].raw != candidate_by_key[key].raw
    )
    added_keys = sorted(candidate_by_key.keys() - baseline_by_key.keys())
    removed_keys = sorted(baseline_by_key.keys() - candidate_by_key.keys())

    for key in changed_keys:
        _assert_allowed_change(baseline_by_key[key], target, child_spans_authorized, "changed baseline record")
        _assert_allowed_change(candidate_by_key[key], target, child_spans_authorized, "changed candidate record")
    for key in added_keys:
        _assert_allowed_change(candidate_by_key[key], target, child_spans_authorized, "added record")
    for key in removed_keys:
        _assert_allowed_change(baseline_by_key[key], target, child_spans_authorized, "removed record")

    def is_target_line(row: ChunkLine) -> bool:
        return _is_allowed_target_change(row.span, target, child_spans_authorized)

    baseline_non_target = b"".join(row.raw for row in baseline_rows if not is_target_line(row))
    candidate_non_target = b"".join(row.raw for row in candidate_rows if not is_target_line(row))
    non_target_byte_identical = baseline_non_target == candidate_non_target
    if not non_target_byte_identical:
        raise RouteIsolationError("non-target records are not byte-identical")

    changed_spans = sorted(
        {
            row.span.label
            for key in [*changed_keys, *added_keys, *removed_keys]
            for row in (baseline_by_key.get(key), candidate_by_key.get(key))
            if row is not None
        }
    )
    return IsolationReport(
        baseline_count=len(baseline_rows),
        candidate_count=len(candidate_rows),
        baseline_sha256=_sha256(baseline_bytes),
        candidate_sha256=_sha256(candidate_bytes),
        changed_keys=changed_keys,
        added_keys=added_keys,
        removed_keys=removed_keys,
        changed_spans=changed_spans,
        non_target_byte_identical=non_target_byte_identical,
        target_span=target.label,
        child_spans_authorized=child_spans_authorized,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--target-span", required=True)
    parser.add_argument("--child-spans-authorized", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)

    try:
        report = compare_chunk_jsonl(
            args.baseline,
            args.candidate,
            target_span=args.target_span,
            child_spans_authorized=args.child_spans_authorized,
        )
    except RouteIsolationError as exc:
        print(f"Route isolation validation failed: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(report.as_dict(), sort_keys=True, indent=2)
    if args.report:
        args.report.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
