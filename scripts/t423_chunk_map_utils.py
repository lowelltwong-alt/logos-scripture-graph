"""Shared utilities for T423 whole-Bible chunk map validation and comparison."""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRATCH_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking"
CANON_BOOKS_PATH = ROOT / "config" / "canon" / "canonical_66_books.yaml"
FORK_POLICY = ROOT / ".ai" / "control" / "multi_model_whole_bible_chunking_fork.yaml"

SPAN_RE = re.compile(
    r"^([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+)"
    r"(?:-([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+))?$"
)

REQUIRED_CHUNK_FIELDS = (
    "model_id",
    "book",
    "span",
    "chunk_index_in_book",
    "literature_type_guess",
    "boundary_evidence_refs",
    "strong_or_hebrew_tags_used",
    "wj_or_red_letter_considered",
    "confidence",
    "decision_id",
    "non_authorizing",
)


@dataclass(frozen=True)
class VerseRef:
    book: str
    chapter: int
    verse: int

    def key(self) -> tuple[str, int, int]:
        return (self.book, self.chapter, self.verse)


@dataclass(frozen=True)
class SpanRange:
    book: str
    start: VerseRef
    end: VerseRef

    def normalized_span(self) -> str:
        s = f"{self.start.book}.{self.start.chapter}.{self.start.verse}"
        e = f"{self.end.book}.{self.end.chapter}.{self.end.verse}"
        return s if s == e else f"{s}-{e}"


def load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def canonical_books() -> list[str]:
    data = load_yaml(CANON_BOOKS_PATH)
    books = data.get("canonical_66_books")
    if not isinstance(books, list) or len(books) != 66:
        raise ValueError(f"{CANON_BOOKS_PATH}: expected 66 canonical books")
    return [str(b) for b in books]


def majority_required(complete_model_count: int) -> int:
    return math.ceil(0.7 * complete_model_count)


def iter_jsonl(path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if stripped:
                record = json.loads(stripped)
                if not isinstance(record, dict):
                    raise ValueError(f"{path}:{line_no}: expected JSON object")
                yield line_no, record


def normalize_book_id(book: str) -> str:
    return book.strip()


def parse_verse_ref(book: str, chapter: str, verse: str) -> VerseRef:
    return VerseRef(book=book, chapter=int(chapter), verse=int(verse))


def parse_span(span: str) -> SpanRange:
    raw = span.strip()
    match = SPAN_RE.match(raw)
    if not match:
        raise ValueError(f"malformed span: {span!r}")
    b1, c1, v1, b2, c2, v2 = match.groups()
    start = parse_verse_ref(b1, c1, v1)
    if b2 is None:
        end = start
    else:
        end = parse_verse_ref(b2, c2, v2)
        if start.book != end.book:
            raise ValueError(f"span crosses books: {span!r}")
    if (end.chapter, end.verse) < (start.chapter, start.verse):
        raise ValueError(f"span end before start: {span!r}")
    return SpanRange(book=start.book, start=start, end=end)


def normalize_span(span: str) -> str:
    return parse_span(span).normalized_span()


def verse_before(a: VerseRef, b: VerseRef) -> bool:
    return a.key() < b.key()


def spans_overlap(a: SpanRange, b: SpanRange) -> bool:
    if a.book != b.book:
        return False
    return not verse_before(a.end, b.start) and not verse_before(b.end, a.start)


def boundary_shift_verses(a: SpanRange, b: SpanRange) -> int:
    if a.book != b.book:
        return 999
    return abs(a.start.verse - b.start.verse) + abs(a.end.verse - b.end.verse) + abs(
        a.start.chapter - b.start.chapter
    ) * 100 + abs(a.end.chapter - b.end.chapter) * 100


def is_near_miss(a: SpanRange, b: SpanRange, max_verse_shift: int = 3) -> bool:
    if a.book != b.book or a.normalized_span() == b.normalized_span():
        return False
    if not spans_overlap(a, b):
        return False
    return boundary_shift_verses(a, b) <= max_verse_shift


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover_model_folders(scratch_root: Path | None = None) -> list[Path]:
    root = scratch_root or SCRATCH_ROOT
    folders: list[Path] = []
    for path in sorted(root.iterdir()):
        if not path.is_dir():
            continue
        name = path.name
        if name in {"comparison", "shared_research_baseline", "models", "redteam"}:
            continue
        if name.startswith("M") and (path / "model_manifest.yaml").is_file():
            folders.append(path)
    return folders


def load_model_manifest(folder: Path) -> dict[str, Any]:
    return load_yaml(folder / "model_manifest.yaml")


def load_marathon_progress(folder: Path) -> dict[str, Any]:
    path = folder / "marathon_progress.yaml"
    if not path.is_file():
        return {}
    return load_yaml(path)


def model_is_complete(folder: Path) -> bool:
    progress = load_marathon_progress(folder)
    status = str(progress.get("marathon_status", "")).lower()
    if status == "complete":
        return True
    books_completed = progress.get("books_completed")
    books_total = progress.get("books_total", 66)
    return isinstance(books_completed, int) and books_completed >= books_total


def completed_books(folder: Path) -> set[str]:
    progress = load_marathon_progress(folder)
    completion = progress.get("book_completion", {})
    if not isinstance(completion, dict):
        return set()
    done: set[str] = set()
    for book, info in completion.items():
        if isinstance(info, dict) and str(info.get("status", "")).lower() == "complete":
            done.add(str(book))
    return done


def load_chunk_map(folder: Path) -> list[dict[str, Any]]:
    path = folder / "whole_bible_chunk_map.jsonl"
    if not path.is_file():
        return []
    return [record for _, record in iter_jsonl(path)]


def load_fork_policy() -> dict[str, Any]:
    return load_yaml(FORK_POLICY)


def agreement_tier(models_agreeing: int, complete_model_count: int) -> str | None:
    if models_agreeing == complete_model_count:
        return "full_consensus"
    required = majority_required(complete_model_count)
    if models_agreeing >= required:
        return "easy_majority"
    return None
