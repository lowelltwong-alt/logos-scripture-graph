"""Shared utilities for T423 whole-Bible chunk map validation and comparison."""
from __future__ import annotations

import hashlib
import json
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRATCH_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking"
CANON_BOOKS_PATH = ROOT / "config" / "canon" / "canonical_66_books.yaml"
FORK_POLICY = ROOT / ".ai" / "control" / "multi_model_whole_bible_chunking_fork.yaml"
VERSE_OBSERVATIONS = ROOT / "build" / "observation_substrate" / "current" / "verse_observations.jsonl"
SCAN_MANIFEST = ROOT / "build" / "observation_substrate" / "current" / "scan_manifest.json"

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
    "frontier_flag_considered",
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


def contiguous_verse_runs(
    ordered_verse_keys: list[VerseRef],
    disagreeing: list[VerseRef],
) -> list[list[VerseRef]]:
    """Split disagreeing verses into contiguous runs (same chapter, adjacent in substrate order)."""
    if not disagreeing:
        return []
    index = {ref.key(): i for i, ref in enumerate(ordered_verse_keys)}
    sorted_dis = sorted(disagreeing, key=lambda v: v.key())
    runs: list[list[VerseRef]] = []
    current = [sorted_dis[0]]
    for ref in sorted_dis[1:]:
        prev = current[-1]
        prev_idx = index.get(prev.key())
        cur_idx = index.get(ref.key())
        adjacent = (
            prev.book == ref.book
            and prev.chapter == ref.chapter
            and prev_idx is not None
            and cur_idx is not None
            and cur_idx == prev_idx + 1
        )
        if adjacent:
            current.append(ref)
        else:
            runs.append(current)
            current = [ref]
    runs.append(current)
    return runs


def region_span_for_verses(verses: list[VerseRef]) -> str:
    start, end = verses[0], verses[-1]
    region = f"{start.book}.{start.chapter}.{start.verse}"
    if end.key() != start.key():
        region = f"{region}-{end.book}.{end.chapter}.{end.verse}"
    return region


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def substrate_build_fingerprint() -> dict[str, str]:
    """Fingerprint of the current Rust observation substrate build."""
    if not SCAN_MANIFEST.is_file():
        return {"status": "missing", "scan_manifest_sha256": "", "source_sha256_short": ""}
    data = json.loads(SCAN_MANIFEST.read_text(encoding="utf-8"))
    return {
        "status": "present",
        "scan_manifest_sha256": file_sha256(SCAN_MANIFEST),
        "source_sha256_short": str(data.get("source_sha256_short", "")),
        "scanner_version": str(data.get("scanner_version", "")),
    }


def pin_substrate_to_manifest(model_folder: Path) -> dict[str, str]:
    """Record substrate fingerprint in model_manifest.yaml before marathon start."""
    fp = substrate_build_fingerprint()
    manifest_path = model_folder / "model_manifest.yaml"
    manifest = load_yaml(manifest_path) if manifest_path.is_file() else {}
    manifest["observation_substrate_scan_sha256"] = fp.get("scan_manifest_sha256", "")
    manifest["observation_substrate_source_sha256_short"] = fp.get("source_sha256_short", "")
    manifest["observation_substrate_pinned_at"] = datetime_now_iso()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return fp


def datetime_now_iso() -> str:
    from datetime import UTC, datetime

    return datetime.now(UTC).isoformat()


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
    if path.is_file():
        return [record for _, record in iter_jsonl(path)]
    return load_chunk_map_from_book_chunks(folder)


BOOK_CHUNKS_DIR = "book_chunks"
BOOK_CHUNK_FILENAME = "chunks.jsonl"


def book_chunk_file(model_folder: Path, book: str) -> Path:
    return model_folder / BOOK_CHUNKS_DIR / book / BOOK_CHUNK_FILENAME


def list_book_chunk_dirs(model_folder: Path) -> list[str]:
    root = model_folder / BOOK_CHUNKS_DIR
    if not root.is_dir():
        return []
    books: list[str] = []
    for path in sorted(root.iterdir()):
        if path.is_dir() and (path / BOOK_CHUNK_FILENAME).is_file():
            books.append(path.name)
    return books


def load_chunk_map_from_book_chunks(model_folder: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for book in list_book_chunk_dirs(model_folder):
        path = book_chunk_file(model_folder, book)
        records.extend(record for _, record in iter_jsonl(path))
    return records


def load_fork_policy() -> dict[str, Any]:
    return load_yaml(FORK_POLICY)


def agreement_tier(models_agreeing: int, complete_model_count: int) -> str | None:
    if models_agreeing == complete_model_count:
        return "full_consensus"
    required = majority_required(complete_model_count)
    if models_agreeing >= required:
        return "easy_majority"
    return None


def verse_in_span(ref: VerseRef, span_range: SpanRange) -> bool:
    if ref.book != span_range.book:
        return False
    return not verse_before(ref, span_range.start) and not verse_before(span_range.end, ref)


def iter_verses_in_span(span_range: SpanRange) -> Iterator[VerseRef]:
    if span_range.start.chapter == span_range.end.chapter:
        for verse in range(span_range.start.verse, span_range.end.verse + 1):
            yield VerseRef(book=span_range.book, chapter=span_range.start.chapter, verse=verse)
        return
    substrate_verses = load_book_verse_keys(span_range.book)
    if substrate_verses:
        for ref in substrate_verses:
            if verse_in_span(ref, span_range):
                yield ref
        return
    yield span_range.start
    if span_range.end.key() != span_range.start.key():
        yield span_range.end


def span_for_verse(chunks: list[dict[str, Any]], verse_ref: VerseRef) -> str | None:
    for chunk in chunks:
        span_raw = chunk.get("span")
        if not isinstance(span_raw, str):
            continue
        try:
            span_range = parse_span(span_raw)
        except ValueError:
            continue
        if verse_in_span(verse_ref, span_range):
            return normalize_span(span_raw)
    return None


def _verses_from_chunks(chunks_by_model: dict[str, list[dict[str, Any]]], book: str) -> list[VerseRef]:
    seen: set[tuple[str, int, int]] = set()
    verses: list[VerseRef] = []
    for chunks in chunks_by_model.values():
        for chunk in chunks:
            if str(chunk.get("book", "")) != book:
                continue
            span_raw = chunk.get("span")
            if not isinstance(span_raw, str):
                continue
            try:
                for ref in iter_verses_in_span(parse_span(span_raw)):
                    key = ref.key()
                    if key not in seen:
                        seen.add(key)
                        verses.append(ref)
            except ValueError:
                continue
    verses.sort(key=lambda v: v.key())
    return verses


def load_book_verse_keys(
    book: str,
    *,
    chunks_by_model: dict[str, list[dict[str, Any]]] | None = None,
    substrate_path: Path | None = None,
) -> list[VerseRef]:
    path = substrate_path or VERSE_OBSERVATIONS
    verses: list[VerseRef] = []
    if path.is_file():
        for _, record in iter_jsonl(path):
            if str(record.get("book", "")) != book:
                continue
            chapter = record.get("chapter")
            verse = record.get("verse")
            if isinstance(chapter, int) and isinstance(verse, int):
                verses.append(VerseRef(book=book, chapter=chapter, verse=verse))
        if verses:
            verses.sort(key=lambda v: v.key())
            return verses
    if chunks_by_model:
        return _verses_from_chunks(chunks_by_model, book)
    return []


@dataclass
class BookCompareResult:
    book: str
    verse_coverage_agreement_rate: float
    verses_total: int
    verses_agreed: int
    span_consensus_chunks: list[dict[str, Any]] = field(default_factory=list)
    boundary_deltas: list[dict[str, Any]] = field(default_factory=list)
    chunk_counts: dict[str, int] = field(default_factory=dict)
    agreement_rate_exact_span_legacy: float = 0.0


def compare_book_verse_coverage(
    chunks_by_model: dict[str, list[dict[str, Any]]],
    book: str,
    model_ids: list[str],
    *,
    allow_easy_at_n3: bool = False,
    stress_book: bool = False,
    overlap_t417: bool = False,
) -> BookCompareResult:
    n = len(model_ids)
    book_chunks = {mid: [c for c in chunks_by_model.get(mid, []) if str(c.get("book", "")) == book] for mid in model_ids}
    for mid in model_ids:
        book_chunks[mid].sort(key=lambda r: int(r["chunk_index_in_book"]))
    counts = {mid: len(book_chunks[mid]) for mid in model_ids}

    verse_keys = load_book_verse_keys(book, chunks_by_model=book_chunks)
    if not verse_keys:
        return BookCompareResult(
            book=book,
            verse_coverage_agreement_rate=0.0,
            verses_total=0,
            verses_agreed=0,
            chunk_counts=counts,
        )

    majority = majority_required(n)
    verses_agreed = 0
    verse_span_by_model: dict[tuple[str, int, int], dict[str, str | None]] = {}

    for ref in verse_keys:
        vkey = ref.key()
        spans_for_verse: dict[str, str | None] = {}
        for mid in model_ids:
            spans_for_verse[mid] = span_for_verse(book_chunks[mid], ref)
        verse_span_by_model[vkey] = spans_for_verse

        present = {mid: s for mid, s in spans_for_verse.items() if s is not None}
        if len(present) < 2:
            continue
        groups: dict[str, list[str]] = defaultdict(list)
        for mid, span in present.items():
            groups[span].append(mid)
        best_count = max(len(g) for g in groups.values())
        if best_count >= majority:
            verses_agreed += 1

    verses_total = len(verse_keys)
    rate = (verses_agreed / verses_total) if verses_total else 0.0

    span_model_sets: dict[str, set[str]] = defaultdict(set)
    lit_by_span: dict[str, str] = {}
    for mid in model_ids:
        for chunk in book_chunks[mid]:
            try:
                norm = normalize_span(str(chunk["span"]))
            except (ValueError, KeyError):
                continue
            span_model_sets[norm].add(mid)
            lit_by_span.setdefault(norm, str(chunk.get("literature_type_guess", "")))

    span_consensus: list[dict[str, Any]] = []
    for span, models in sorted(span_model_sets.items()):
        agreeing = sorted(models)
        tier = agreement_tier(len(agreeing), n)
        if not tier:
            continue
        if not (allow_easy_at_n3 or n >= 4 or tier == "full_consensus"):
            continue
        span_consensus.append(
            {
                "book": book,
                "span": span,
                "models_agreeing": agreeing,
                "complete_model_count": n,
                "agreement_tier": tier,
                "literature_type_guess": lit_by_span.get(span, ""),
                "easy_chunk": True,
                "t417_overlap_book": overlap_t417,
                "non_authorizing": True,
                "promotion_authority": "none",
            }
        )

    deltas: list[dict[str, Any]] = []
    delta_idx = 0

    uncovered: dict[str, list[str]] = {}
    for mid in model_ids:
        covered: set[tuple[str, int, int]] = set()
        for chunk in book_chunks[mid]:
            try:
                for ref in iter_verses_in_span(parse_span(str(chunk["span"]))):
                    covered.add(ref.key())
            except ValueError:
                continue
        missing = [f"{book}.{c}.{v}" for b, c, v in [k for k in (vk.key() for vk in verse_keys) if k not in covered]]
        if missing:
            uncovered[mid] = missing[:5]

    if uncovered:
        delta_idx += 1
        deltas.append(
            {
                "delta_id": f"DELTA-{book}-COVERAGE-{delta_idx:03d}",
                "book": book,
                "region": book,
                "models": uncovered,
                "delta_kind": "coverage_gap",
                "priority": "high",
                "theology_risk_note": "stress_atlas_book" if stress_book else "",
                "t417_overlap_book": overlap_t417,
                "governed_work_recommended": True,
                "non_authorizing": True,
                "promotion_authority": "none",
            }
        )

    disagreeing_verses = []
    for ref in verse_keys:
        vkey = ref.key()
        spans_for_verse = verse_span_by_model[vkey]
        present = {mid: s for mid, s in spans_for_verse.items() if s is not None}
        if len(present) < 2:
            continue
        groups: dict[str, list[str]] = defaultdict(list)
        for mid, span in present.items():
            groups[span].append(mid)
        if max(len(g) for g in groups.values()) >= majority:
            continue
        disagreeing_verses.append(ref)

    if disagreeing_verses:
        runs = contiguous_verse_runs(verse_keys, disagreeing_verses)
        for run in runs:
            region_start = run[0]
            region_end = run[-1]
            span_by_model: dict[str, str] = {}
            lit_by_model: dict[str, str] = {}
            for ref in run:
                for mid in model_ids:
                    s = verse_span_by_model[ref.key()].get(mid)
                    if s:
                        span_by_model[mid] = s
                for mid in model_ids:
                    for chunk in book_chunks[mid]:
                        try:
                            if span_for_verse([chunk], ref) is not None:
                                lit_by_model[mid] = str(chunk.get("literature_type_guess", ""))
                        except ValueError:
                            pass

            region = region_span_for_verses(run)

            delta_kind = "boundary_shift"
            if len(set(lit_by_model.get(m, "") for m in span_by_model)) > 1:
                delta_kind = "literature_routing_disagreement"

            near = False
            parsed: dict[str, SpanRange] = {}
            for mid, span in span_by_model.items():
                try:
                    parsed[mid] = parse_span(span)
                except ValueError:
                    continue
            mids = list(parsed)
            for i in range(len(mids)):
                for j in range(i + 1, len(mids)):
                    if is_near_miss(parsed[mids[i]], parsed[mids[j]]):
                        near = True
                        break

            delta_idx += 1
            deltas.append(
                {
                    "delta_id": f"DELTA-{book}-{delta_idx:03d}",
                    "book": book,
                    "region": region,
                    "models": span_by_model,
                    "delta_kind": delta_kind,
                    "near_miss": near,
                    "verses_disagreeing": len(run),
                    "priority": "high" if stress_book else "medium",
                    "theology_risk_note": "stress_atlas_book" if stress_book else "",
                    "t417_overlap_book": overlap_t417,
                    "governed_work_recommended": True,
                    "non_authorizing": True,
                    "promotion_authority": "none",
                }
            )

    legacy_agreed = len(span_consensus)
    legacy_total = max(counts.values()) if counts else 0
    legacy_rate = (legacy_agreed / legacy_total) if legacy_total else 0.0

    return BookCompareResult(
        book=book,
        verse_coverage_agreement_rate=round(rate, 4),
        verses_total=verses_total,
        verses_agreed=verses_agreed,
        span_consensus_chunks=span_consensus,
        boundary_deltas=deltas,
        chunk_counts=counts,
        agreement_rate_exact_span_legacy=round(legacy_rate, 4),
    )
