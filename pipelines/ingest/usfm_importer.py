#!/usr/bin/env python3
"""Deterministic WEB Classic USFM importer with embedded feature extraction."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ingest.usfm_inline_parser import (  # noqa: E402
    GENERATION_METHOD,
    LICENSE,
    SOURCE_ARCHIVE,
    SOURCE_FORMAT,
    SOURCE_ID,
    SOURCE_SHA256,
    TRANSLATION_ID,
    InlineContext,
    InlineParser,
    contains_raw_usfm_marker,
    marker_counts as inline_marker_counts,
    normalize_clean_text,
    strip_inline_usfm,
)
from pipelines.util.usfm_to_osis import osis_book, osis_ref  # noqa: E402
from pipelines.util.canon import canon_profiles, testament  # noqa: E402
from pipelines.util.canonical_scope import is_canonical_66_book  # noqa: E402

BOOK_RE = re.compile(r"^\\id\s+(?P<book>\S+)")
MARKER_RE = re.compile(r"^\\(?P<marker>[A-Za-z0-9]+)\s*(?P<body>.*)$")
VERSE_BODY_RE = re.compile(r"^(?P<verse>\d+)(?P<suffix>[A-Za-z]?)\s*(?P<text>.*)$")

CONTENT_EXCLUDE = {"FRT", "GLO"}
STRUCTURAL_MARKERS = {
    "p",
    "m",
    "mi",
    "pi1",
    "q1",
    "q2",
    "q3",
    "d",
    "b",
    "sp",
    "s1",
    "ms1",
    "ili",
    "li1",
    "nb",
    "pc",
    "cl",
    "cp",
}
HEADING_MARKERS = {"s", "s1", "s2", "s3", "ms", "ms1", "ms2", "mt", "mt1", "mt2", "mt3", "d", "sp"}
KNOWN_LINE_MARKERS = STRUCTURAL_MARKERS | HEADING_MARKERS | {
    "id",
    "ide",
    "h",
    "toc1",
    "toc2",
    "toc3",
    "c",
    "v",
    "ip",
    "imt",
    "imt1",
    "imt2",
    "is",
    "is1",
    "is2",
    "iot",
    "io1",
    "io2",
    "io3",
    "ili1",
    "ili2",
    "li2",
}


ANCHOR_KINDS = {
    "current_content",
    "next_content_start",
    "between_units",
    "chapter_context",
    "book_context",
    "unresolved",
}
BODY_DISPOSITIONS = {"append_current", "editorial_only", "none", "unresolved"}
CURRENT_OR_NEXT_CONTENT_MARKERS = {
    "p",
    "m",
    "mi",
    "pi1",
    "q1",
    "q2",
    "q3",
    "pc",
    "li1",
    "li2",
    "ili",
}
NEXT_CONTENT_HEADING_MARKERS = {"s", "s1", "s2", "s3", "ms", "ms1", "ms2", "d", "sp"}
BETWEEN_UNIT_MARKERS = {"b", "nb"}
CHAPTER_CONTEXT_MARKERS = {"c", "cl", "cp"}
BOOK_CONTEXT_MARKERS = {
    "id",
    "ide",
    "h",
    "toc1",
    "toc2",
    "toc3",
    "mt",
    "mt1",
    "mt2",
    "mt3",
    "ip",
    "imt",
    "imt1",
    "imt2",
    "is",
    "is1",
    "is2",
    "iot",
    "io1",
    "io2",
    "io3",
    "ili1",
    "ili2",
}


@dataclass(frozen=True)
class MarkerResolution:
    """Explicitly separate marker ownership from the parser's current verse."""

    anchor_kind: str
    anchor_osis_ref: str | None
    prior_osis_ref: str | None
    next_osis_ref: str | None
    body_disposition: str

    def __post_init__(self) -> None:
        if self.anchor_kind not in ANCHOR_KINDS:
            raise ValueError(f"Unknown marker anchor kind: {self.anchor_kind}")
        if self.body_disposition not in BODY_DISPOSITIONS:
            raise ValueError(f"Unknown marker body disposition: {self.body_disposition}")

    @property
    def anchor_resolved(self) -> bool:
        return self.anchor_kind != "unresolved" and (
            self.anchor_osis_ref is not None
            or self.anchor_kind in {"chapter_context", "book_context", "between_units"}
        )

    def fields(self) -> dict[str, Any]:
        return {
            "anchor_kind": self.anchor_kind,
            "anchor_osis_ref": self.anchor_osis_ref,
            "prior_osis_ref": self.prior_osis_ref,
            "next_osis_ref": self.next_osis_ref,
            "body_disposition": self.body_disposition,
            "anchor_resolved": self.anchor_resolved,
        }


def resolve_line_marker(
    marker: str,
    body: str,
    *,
    current_osis_ref: str | None,
    prior_osis_ref: str | None,
    next_osis_ref: str | None,
    book: str | None,
) -> MarkerResolution:
    """Resolve a line marker before emitting any canonical or processed record."""

    has_body = bool(body.strip())
    if marker in CHAPTER_CONTEXT_MARKERS:
        disposition = "editorial_only" if has_body else "none"
        return MarkerResolution("chapter_context", None, prior_osis_ref, next_osis_ref, disposition)
    if marker in BOOK_CONTEXT_MARKERS or (
        book in CONTENT_EXCLUDE and marker in {"ili", "li1", "li2"}
    ):
        disposition = "editorial_only" if has_body else "none"
        return MarkerResolution("book_context", None, prior_osis_ref, next_osis_ref, disposition)
    if marker in BETWEEN_UNIT_MARKERS:
        if has_body:
            return MarkerResolution("unresolved", None, prior_osis_ref, next_osis_ref, "unresolved")
        return MarkerResolution("between_units", next_osis_ref, prior_osis_ref, next_osis_ref, "none")
    if marker in NEXT_CONTENT_HEADING_MARKERS:
        if next_osis_ref is None:
            return MarkerResolution("unresolved", None, prior_osis_ref, None, "editorial_only")
        return MarkerResolution(
            "next_content_start", next_osis_ref, prior_osis_ref, next_osis_ref, "editorial_only"
        )
    if marker in CURRENT_OR_NEXT_CONTENT_MARKERS:
        if has_body and current_osis_ref is not None:
            return MarkerResolution(
                "current_content", current_osis_ref, current_osis_ref, next_osis_ref, "append_current"
            )
        if not has_body and next_osis_ref is not None:
            return MarkerResolution(
                "next_content_start", next_osis_ref, prior_osis_ref, next_osis_ref, "none"
            )
        return MarkerResolution("unresolved", None, prior_osis_ref, next_osis_ref, "unresolved")
    disposition = "unresolved" if has_body else "none"
    return MarkerResolution("unresolved", None, prior_osis_ref, next_osis_ref, disposition)


class JsonlWriter:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("w", encoding="utf-8", newline="\n")

    def write(self, record: dict[str, Any]) -> None:
        self.handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    def close(self) -> None:
        self.handle.close()


class ImportState:
    def __init__(self, archive: Path, source_sha256: str, canonical_66_filter_enabled: bool = False):
        self.archive = archive
        self.source_sha256 = source_sha256
        self.canonical_66_filter_enabled = canonical_66_filter_enabled
        self.parser = InlineParser()
        self.book: str | None = None
        self.chapter: int | None = None
        self.current: dict[str, Any] | None = None
        self.last_osis_ref: str | None = None
        self.ids: set[str] = set()
        self.counts: Counter[str] = Counter()
        self.marker_counts: Counter[str] = Counter()
        self.unsupported_marker_counts: Counter[str] = Counter()
        self.unsupported_samples: dict[str, list[str]] = defaultdict(list)
        self.clean_text_marker_leaks: list[dict[str, Any]] = []
        self.files: list[dict[str, Any]] = []

    def common(self) -> dict[str, Any]:
        return {
            "source_id": SOURCE_ID,
            "source_archive": SOURCE_ARCHIVE,
            "source_sha256": self.source_sha256,
            "source_format": SOURCE_FORMAT,
            "license": LICENSE,
            "status": "imported",
            "generation_method": GENERATION_METHOD,
        }

    def unique(self, record: dict[str, Any]) -> None:
        rid = record["id"]
        if rid in self.ids:
            raise ValueError(f"Duplicate generated id: {rid}")
        self.ids.add(rid)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_manifest(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def iter_archive_entries(archive: Path):
    with zipfile.ZipFile(archive) as zf:
        for info in sorted(zf.infolist(), key=lambda i: i.filename):
            if info.is_dir():
                continue
            yield info.filename, zf.read(info.filename)


def safe_extract_archive(archive: Path, extracted_dir: Path) -> list[dict[str, Any]]:
    if extracted_dir.exists():
        shutil.rmtree(extracted_dir)
    extracted_dir.mkdir(parents=True, exist_ok=True)
    manifest_entries = []
    for name, payload in iter_archive_entries(archive):
        target = extracted_dir / name
        resolved = target.resolve()
        if extracted_dir.resolve() not in resolved.parents and resolved != extracted_dir.resolve():
            raise ValueError(f"Unsafe archive member path: {name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        manifest_entries.append(
            {
                "path": name,
                "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return manifest_entries


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    def emit(key: str, value: Any, indent: int = 0) -> None:
        pad = "  " * indent
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            for child_key, child_value in value.items():
                emit(str(child_key), child_value, indent + 1)
        elif isinstance(value, list):
            lines.append(f"{pad}{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{pad}  -")
                    for child_key, child_value in item.items():
                        emit(str(child_key), child_value, indent + 2)
                else:
                    lines.append(f"{pad}  - {yaml_scalar(item)}")
        else:
            lines.append(f"{pad}{key}: {yaml_scalar(value)}")

    for top_key, top_value in data.items():
        emit(top_key, top_value)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def record_usfm_event(
    state: ImportState,
    writers: dict[str, JsonlWriter],
    marker: str,
    raw_line: str,
    source_file: str,
    source_line: int,
    resolution: MarkerResolution,
    text: str = "",
) -> None:
    event_id = f"usfm-event:{source_file}:{source_line}:{marker}".replace("\\", "/")
    anchor_ref = resolution.anchor_osis_ref
    passage_id = f"scripture:{anchor_ref}" if anchor_ref else None
    record = {
        **state.common(),
        **resolution.fields(),
        "id": event_id,
        "type": "USFMEvent",
        "marker": marker,
        "book": state.book,
        "osis_book": osis_book(state.book) if state.book else None,
        "chapter": state.chapter,
        "passage_id": passage_id,
        "osis_ref": anchor_ref,
        "text": strip_inline_usfm(text) if text else "",
        "raw_marker": raw_line,
        "source_file": source_file,
        "source_line": source_line,
    }
    state.unique(record)
    writers["usfm_events"].write(record)
    state.counts["usfm_events"] += 1
    if state.canonical_66_filter_enabled and not is_canonical_66_book(state.book):
        return
    if marker in STRUCTURAL_MARKERS:
        boundary = {
            **state.common(),
            **canonical_book_identity(state),
            **resolution.fields(),
            "id": f"boundary-claim:{source_file}:{source_line}:{marker}".replace("\\", "/"),
            "type": "BoundaryClaim",
            "passage_id": passage_id,
            "osis_ref": anchor_ref,
            "translation_id": TRANSLATION_ID,
            "boundary_kind": "usfm_structural_marker",
            "marker": marker,
            "claim_scope": "future_chunking_evidence",
            "is_canonical_ancient_boundary": False,
            "source_event_id": event_id,
            "raw_marker": raw_line,
            "source_file": source_file,
            "source_line": source_line,
        }
        state.unique(boundary)
        writers["boundary_claims"].write(boundary)
        state.counts["boundary_claims"] += 1
    if marker in HEADING_MARKERS and text:
        heading = {
            **state.common(),
            **canonical_book_identity(state),
            **resolution.fields(),
            "id": f"section-heading:{source_file}:{source_line}:{marker}".replace("\\", "/"),
            "type": "SectionHeading",
            "passage_id": passage_id,
            "osis_ref": anchor_ref,
            "translation_id": TRANSLATION_ID,
            "marker": marker,
            "text": strip_inline_usfm(text),
            "source_event_id": event_id,
            "raw_marker": raw_line,
            "source_file": source_file,
            "source_line": source_line,
        }
        state.unique(heading)
        writers["section_headings"].write(heading)
        state.counts["section_headings"] += 1


def canonical_book_identity(state: ImportState) -> dict[str, str]:
    """Return canonical book identity fields for canonical sidecar records."""
    if not state.book:
        return {}
    osis_b = osis_book(state.book)
    return {"book": osis_b, "osis_book": osis_b, "usfm_book": state.book}


def attach_book_identity(state: ImportState, record: dict[str, Any]) -> dict[str, Any]:
    """Add book identity to canonical sidecars that may not have a verse scope."""
    return {**canonical_book_identity(state), **record}


def write_inline_sidecars(
    state: ImportState,
    writers: dict[str, JsonlWriter],
    result: Any,
) -> None:
    for token in result.word_tokens:
        token = attach_book_identity(state, token)
        state.unique(token)
        writers["word_tokens"].write(token)
        state.counts["word_tokens"] += 1
    for footnote in result.footnotes:
        footnote = attach_book_identity(state, footnote)
        state.unique(footnote)
        writers["footnotes"].write(footnote)
        state.counts["footnotes"] += 1
    for crossref in result.crossrefs:
        crossref = attach_book_identity(state, crossref)
        state.unique(crossref)
        writers["editorial_crossrefs"].write(crossref)
        state.counts["editorial_crossrefs"] += 1
    for unsupported in result.unsupported_markers:
        state.unique(unsupported)
        writers["unsupported_markers"].write(unsupported)
        state.counts["unsupported_markers"] += 1
        state.unsupported_marker_counts[unsupported["marker"]] += 1
        samples = state.unsupported_samples[unsupported["marker"]]
        if len(samples) < 5:
            samples.append(unsupported["raw_marker"])


def append_verse_text(
    state: ImportState,
    writers: dict[str, JsonlWriter],
    text: str,
    source_file: str,
    source_line: int,
) -> None:
    if not state.current or not text.strip():
        return
    ctx = InlineContext(
        passage_id=state.current["passage_id"],
        osis_ref=state.current["osis_ref"],
        source_file=source_file,
        source_line=source_line,
        word_index=state.current["word_index"],
        footnote_index=state.current["footnote_index"],
        crossref_index=state.current["crossref_index"],
        source_sha256=state.source_sha256,
    )
    result = state.parser.parse(text, ctx)
    if result.clean_text:
        state.current["parts"].append(result.clean_text)
    state.current["word_index"] = result.word_index
    state.current["footnote_index"] = result.footnote_index
    state.current["crossref_index"] = result.crossref_index
    write_inline_sidecars(state, writers, result)


def emit_editorial_inline_sidecars(
    state: ImportState,
    writers: dict[str, JsonlWriter],
    text: str,
    source_file: str,
    source_line: int,
) -> None:
    """Emit typed footnotes/crossrefs from editorial-only bodies.

    Heading prose must not enter TranslationWitness text. Heading-embedded
    word tokens (e.g. Strong's in ``\\d`` / ``\\sp``) must not become
    WordTokens. Footnote IDs stay file:line-scoped via ``osis_ref=None``.
    """
    if not text.strip():
        return
    ctx = InlineContext(
        passage_id=None,
        osis_ref=None,
        source_file=source_file,
        source_line=source_line,
        word_index=0,
        footnote_index=0,
        crossref_index=0,
        source_sha256=state.source_sha256,
    )
    result = state.parser.parse(text, ctx)
    for footnote in result.footnotes:
        footnote = attach_book_identity(state, footnote)
        state.unique(footnote)
        writers["footnotes"].write(footnote)
        state.counts["footnotes"] += 1
    for crossref in result.crossrefs:
        crossref = attach_book_identity(state, crossref)
        state.unique(crossref)
        writers["editorial_crossrefs"].write(crossref)
        state.counts["editorial_crossrefs"] += 1
    for unsupported in result.unsupported_markers:
        state.unique(unsupported)
        writers["unsupported_markers"].write(unsupported)
        state.counts["unsupported_markers"] += 1
        state.unsupported_marker_counts[unsupported["marker"]] += 1
        samples = state.unsupported_samples[unsupported["marker"]]
        if len(samples) < 5:
            samples.append(unsupported["raw_marker"])


def flush_verse(state: ImportState, writers: dict[str, JsonlWriter]) -> None:
    if not state.current:
        return
    clean_text = normalize_clean_text(" ".join(state.current["parts"]))
    if contains_raw_usfm_marker(clean_text):
        state.clean_text_marker_leaks.append(
            {"osis_ref": state.current["osis_ref"], "text": clean_text[:200]}
        )
    osis_b = osis_book(state.current["book"])
    passage = {
        **state.common(),
        "id": state.current["passage_id"],
        "type": "ScripturePassage",
        "osis_ref": state.current["osis_ref"],
        "book": osis_b,
        "usfm_book": state.current["book"],
        "chapter": state.current["chapter"],
        "verse_start": state.current["verse"],
        "verse_end": state.current["verse"],
        "testament": testament(osis_b),
        "canon_profiles": canon_profiles(osis_b),
        "source_file": state.current["source_file"],
        "source_line": state.current["source_line"],
    }
    witness = {
        **state.common(),
        "id": f"translation-witness:{TRANSLATION_ID}:{state.current['osis_ref']}",
        "type": "TranslationWitness",
        "passage_id": state.current["passage_id"],
        "osis_ref": state.current["osis_ref"],
        "translation_id": TRANSLATION_ID,
        "translation_title": "World English Bible Classic",
        "language": "eng",
        "dialect": "American",
        "text": clean_text,
        "source_file": state.current["source_file"],
        "source_line": state.current["source_line"],
    }
    state.unique(passage)
    state.unique(witness)
    writers["passages"].write(passage)
    writers["translation_witnesses"].write(witness)
    state.counts["passages"] += 1
    state.counts["translation_witnesses"] += 1
    state.last_osis_ref = state.current["osis_ref"]
    state.current = None


def start_verse(state: ImportState, verse: int, source_file: str, source_line: int) -> None:
    if state.book is None or state.chapter is None:
        raise ValueError(f"Verse before book/chapter at {source_file}:{source_line}")
    ref = osis_ref(state.book, state.chapter, verse)
    state.current = {
        "book": state.book,
        "chapter": state.chapter,
        "verse": verse,
        "osis_ref": ref,
        "passage_id": f"scripture:{ref}",
        "parts": [],
        "word_index": 0,
        "footnote_index": 0,
        "crossref_index": 0,
        "source_file": source_file,
        "source_line": source_line,
    }
    state.counts["verse_markers"] += 1


def parse_glossary_line(
    state: ImportState,
    writers: dict[str, JsonlWriter],
    raw_line: str,
    source_file: str,
    source_line: int,
    body: str,
) -> None:
    term_match = re.search(r"\\k\s+(?P<term>.*?)\\k\*", body)
    if not term_match:
        return
    term = normalize_clean_text(term_match.group("term"))
    definition = normalize_clean_text(strip_inline_usfm(body[term_match.end() :]))
    slug = re.sub(r"[^A-Za-z0-9]+", "-", term.lower()).strip("-")
    record = {
        **state.common(),
        "id": f"glossary-entry:{TRANSLATION_ID}:{slug}",
        "type": "GlossaryEntry",
        "term": term,
        "definition": definition,
        "translation_id": TRANSLATION_ID,
        "source_file": source_file,
        "source_line": source_line,
        "raw_marker": raw_line,
    }
    state.unique(record)
    writers["glossary_entries"].write(record)
    state.counts["glossary_entries"] += 1


def prepare_line_contexts(text: str) -> tuple[list[tuple[int, str, str]], list[str | None]]:
    """Return source lines and the next verse ref at or after each line in O(n)."""

    lines = [
        (source_line, raw_line, raw_line.strip())
        for source_line, raw_line in enumerate(text.splitlines(), start=1)
    ]
    book: str | None = None
    chapter: int | None = None
    verse_at_line: list[str | None] = [None] * len(lines)
    for index, (_source_line, _raw_line, line) in enumerate(lines):
        id_match = BOOK_RE.match(line)
        if id_match:
            book = id_match.group("book")
            chapter = None
            continue
        marker_match = MARKER_RE.match(line)
        if not marker_match:
            continue
        marker = marker_match.group("marker")
        body = marker_match.group("body")
        if marker == "c":
            try:
                chapter = int(body.split()[0])
            except (IndexError, ValueError):
                chapter = None
            continue
        if marker != "v" or book is None or chapter is None:
            continue
        verse_match = VERSE_BODY_RE.match(body)
        if verse_match:
            verse_at_line[index] = osis_ref(book, chapter, int(verse_match.group("verse")))

    next_verse_refs: list[str | None] = [None] * len(lines)
    next_ref: str | None = None
    for index in range(len(lines) - 1, -1, -1):
        if verse_at_line[index] is not None:
            next_ref = verse_at_line[index]
        next_verse_refs[index] = next_ref
    return lines, next_verse_refs


def parse_usfm_file(state: ImportState, writers: dict[str, JsonlWriter], source_file: str, text: str) -> None:
    state.book = None
    state.chapter = None
    state.current = None
    state.last_osis_ref = None
    local_markers = Counter()
    lines, next_verse_refs = prepare_line_contexts(text)
    for index, (source_line, raw_line, line) in enumerate(lines):
        if not line:
            continue
        next_ref = next_verse_refs[index]
        current_ref = state.current["osis_ref"] if state.current else None
        prior_ref = current_ref or state.last_osis_ref
        state.marker_counts.update(inline_marker_counts(line))
        local_markers.update(inline_marker_counts(line))
        id_match = BOOK_RE.match(line)
        if id_match:
            flush_verse(state, writers)
            state.book = id_match.group("book")
            state.chapter = None
            resolution = resolve_line_marker(
                "id",
                line,
                current_osis_ref=current_ref,
                prior_osis_ref=prior_ref,
                next_osis_ref=next_ref,
                book=state.book,
            )
            record_usfm_event(
                state,
                writers,
                "id",
                raw_line,
                source_file,
                source_line,
                resolution,
                line,
            )
            continue
        marker_match = MARKER_RE.match(line)
        if not marker_match:
            append_verse_text(state, writers, line, source_file, source_line)
            continue
        marker = marker_match.group("marker")
        body = marker_match.group("body")
        if marker not in KNOWN_LINE_MARKERS:
            state.unsupported_marker_counts[marker] += 1
            samples = state.unsupported_samples[marker]
            if len(samples) < 5:
                samples.append(raw_line)
        if marker == "c":
            flush_verse(state, writers)
            state.chapter = int(body.split()[0])
            resolution = resolve_line_marker(
                marker,
                body,
                current_osis_ref=current_ref,
                prior_osis_ref=prior_ref,
                next_osis_ref=next_ref,
                book=state.book,
            )
            record_usfm_event(
                state,
                writers,
                marker,
                raw_line,
                source_file,
                source_line,
                resolution,
                body,
            )
            state.counts["chapter_markers"] += 1
            continue
        if marker == "v":
            flush_verse(state, writers)
            verse_match = VERSE_BODY_RE.match(body)
            if not verse_match:
                state.unsupported_marker_counts["v"] += 1
                state.unsupported_samples["v"].append(raw_line)
                continue
            verse = int(verse_match.group("verse"))
            if (
                is_canonical_66_book(state.book)
                if state.canonical_66_filter_enabled
                else state.book not in CONTENT_EXCLUDE
            ):
                start_verse(state, verse, source_file, source_line)
                append_verse_text(state, writers, verse_match.group("text"), source_file, source_line)
            anchor_ref = state.current["osis_ref"] if state.current else next_ref
            resolution = MarkerResolution(
                "current_content",
                anchor_ref,
                prior_ref,
                anchor_ref,
                "append_current" if verse_match.group("text").strip() else "none",
            )
            record_usfm_event(
                state,
                writers,
                marker,
                raw_line,
                source_file,
                source_line,
                resolution,
                verse_match.group("text"),
            )
            continue
        resolution = resolve_line_marker(
            marker,
            body,
            current_osis_ref=current_ref,
            prior_osis_ref=prior_ref,
            next_osis_ref=next_ref,
            book=state.book,
        )
        record_usfm_event(
            state,
            writers,
            marker,
            raw_line,
            source_file,
            source_line,
            resolution,
            body,
        )
        if state.canonical_66_filter_enabled and not is_canonical_66_book(state.book):
            continue
        if marker == "ili" and state.book == "GLO":
            parse_glossary_line(state, writers, raw_line, source_file, source_line, body)
            continue
        if resolution.body_disposition == "append_current":
            append_verse_text(state, writers, body, source_file, source_line)
        elif resolution.body_disposition == "editorial_only":
            emit_editorial_inline_sidecars(state, writers, body, source_file, source_line)
    flush_verse(state, writers)
    state.files.append(
        {
            "path": source_file,
            "book": state.book,
            "markers": dict(sorted(local_markers.items())),
        }
    )


def build_writers(canonical_root: Path, processed_root: Path) -> dict[str, JsonlWriter]:
    translation_root = canonical_root / "translations" / TRANSLATION_ID
    return {
        "passages": JsonlWriter(canonical_root / "scripture" / "passages" / "passages.jsonl"),
        "translation_witnesses": JsonlWriter(translation_root / "translation_witnesses.jsonl"),
        "word_tokens": JsonlWriter(translation_root / "word_tokens.jsonl"),
        "footnotes": JsonlWriter(translation_root / "footnotes.jsonl"),
        "editorial_crossrefs": JsonlWriter(translation_root / "editorial_cross_references.jsonl"),
        "section_headings": JsonlWriter(translation_root / "section_headings.jsonl"),
        "boundary_claims": JsonlWriter(translation_root / "boundary_claims.jsonl"),
        "glossary_entries": JsonlWriter(translation_root / "glossary_entries.jsonl"),
        "usfm_events": JsonlWriter(processed_root / "usfm_events.jsonl"),
        "unsupported_markers": JsonlWriter(processed_root / "unsupported_usfm_markers.jsonl"),
    }


def write_reports(
    state: ImportState,
    processed_root: Path,
    extraction_entries: list[dict[str, Any]],
) -> None:
    usfm_files = [entry for entry in extraction_entries if entry["path"].lower().endswith((".usfm", ".sfm"))]
    content_files = [
        entry for entry in usfm_files if not re.match(r"^(00-FRT|106-GLO)", Path(entry["path"]).name)
    ]
    extraction_manifest = {
        "source_archive": SOURCE_ARCHIVE,
        "source_sha256": state.source_sha256,
        "generated_by": GENERATION_METHOD,
        "entry_count": len(extraction_entries),
        "usfm_file_count": len(usfm_files),
        "content_book_file_count_excluding_frt_glo": len(content_files),
        "entries": extraction_entries,
    }
    write_yaml(processed_root / "extraction_manifest.yaml", extraction_manifest)
    report = {
        "source_archive": SOURCE_ARCHIVE,
        "source_sha256": state.source_sha256,
        "generated_by": GENERATION_METHOD,
        "archive_inventory": {
            "entries": len(extraction_entries),
            "usfm_files": len(usfm_files),
            "content_book_files_excluding_frt_glo": len(content_files),
        },
        "counts": dict(sorted(state.counts.items())),
        "marker_counts": dict(sorted(state.marker_counts.items())),
        "word_tag_counts": {
            "direct_w": state.marker_counts.get("w", 0),
            "nested_plus_w": state.marker_counts.get("+w", 0),
            "word_token_records": state.counts.get("word_tokens", 0),
            "hebrew_strong_occurrences": state.counts.get("hebrew_strong_occurrences", 0),
            "greek_strong_occurrences": state.counts.get("greek_strong_occurrences", 0),
        },
        "feature_counts": {
            "footnotes": state.counts.get("footnotes", 0),
            "editorial_cross_references": state.counts.get("editorial_crossrefs", 0),
            "section_headings": state.counts.get("section_headings", 0),
            "boundary_claims": state.counts.get("boundary_claims", 0),
            "glossary_entries": state.counts.get("glossary_entries", 0),
        },
        "unsupported_marker_counts": dict(sorted(state.unsupported_marker_counts.items())),
        "unsupported_marker_samples": {k: v for k, v in sorted(state.unsupported_samples.items())},
        "clean_text_contains_raw_usfm_markers": bool(state.clean_text_marker_leaks),
        "clean_text_marker_leak_samples": state.clean_text_marker_leaks[:10],
        "files": state.files,
    }
    write_yaml(processed_root / "parser_report.yaml", report)


def update_strong_counts(state: ImportState, word_tokens_path: Path) -> None:
    with word_tokens_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            strong = record.get("strong") or ""
            if strong.startswith("H"):
                state.counts["hebrew_strong_occurrences"] += 1
            elif strong.startswith("G"):
                state.counts["greek_strong_occurrences"] += 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", default=SOURCE_ARCHIVE)
    parser.add_argument("--manifest", default="data/raw/bible/eng-web/source_manifest.yaml")
    parser.add_argument("--canonical-root", default="data/canonical")
    parser.add_argument("--processed-root", default="data/processed/bible/eng-web/usfm")
    parser.add_argument("--out", help="Compatibility alias for --processed-root")
    parser.add_argument("--skip-sha-check", action="store_true", help="Only for local fixtures in tests.")
    parser.add_argument(
        "--canonical-66-filter",
        action="store_true",
        help=(
            "Apply the T327B 66-book canonical-output filter. T327C owns regeneration "
            "of existing canonical outputs with this flag."
        ),
    )
    args = parser.parse_args(argv)

    default_archive = (ROOT / SOURCE_ARCHIVE).resolve()
    archive = Path(args.archive)
    if not archive.is_absolute():
        archive = (ROOT / args.archive).resolve()
    else:
        archive = archive.resolve()

    manifest_path = ROOT / args.manifest
    manifest = parse_manifest(manifest_path) if manifest_path.exists() else {}
    if manifest.get("archive_path") and archive == default_archive:
        archive = (ROOT / manifest["archive_path"]).resolve()

    processed_root = ROOT / (args.out or args.processed_root)
    canonical_root = ROOT / args.canonical_root
    source_sha = sha256_file(archive)
    if not args.skip_sha_check:
        expected_sha = manifest.get("sha256")
        if expected_sha in {None, "", "null"}:
            expected_sha = SOURCE_SHA256
        if source_sha.lower() != expected_sha.lower():
            raise SystemExit(f"Unexpected archive SHA256: {source_sha} (expected {expected_sha})")

    state = ImportState(archive, source_sha, canonical_66_filter_enabled=args.canonical_66_filter)
    extraction_entries = safe_extract_archive(archive, processed_root / "extracted")
    writers = build_writers(canonical_root, processed_root)
    try:
        for name, payload in iter_archive_entries(archive):
            if not name.lower().endswith((".usfm", ".sfm")):
                continue
            text = payload.decode("utf-8-sig", errors="replace")
            parse_usfm_file(state, writers, name, text)
    finally:
        for writer in writers.values():
            writer.close()
    update_strong_counts(state, canonical_root / "translations" / TRANSLATION_ID / "word_tokens.jsonl")
    write_reports(state, processed_root, extraction_entries)
    print(f"Wrote canonical records under {canonical_root}")
    print(f"Wrote processed USFM reports under {processed_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
