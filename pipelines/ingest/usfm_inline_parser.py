"""Inline USFM feature extraction for WEB Classic.

The parser is intentionally deterministic and conservative. It removes inline
USFM markup from readable text, emits sidecar records for supported embedded
features, and records unsupported markers for audit instead of silently dropping
them.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import hashlib
import re
from typing import Any

from pipelines.util.usfm_to_osis import parse_unambiguous_refs

SOURCE_ID = "eng-web"
TRANSLATION_ID = "eng-web"
SOURCE_ARCHIVE = "data/raw/bible/eng-web/usfm/eng-web_usfm.zip"
SOURCE_SHA256 = "a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e"
SOURCE_FORMAT = "USFM"
LICENSE = "public-domain"
GENERATION_METHOD = "web-usfm-feature-extraction-v2a"

MARKER_AT_RE = re.compile(r"\\(?P<marker>\+?[A-Za-z0-9]+)(?P<closing>\*)?")
ATTR_RE = re.compile(r"([A-Za-z0-9_-]+)=\"([^\"]*)\"")
RAW_MARKER_RE = re.compile(r"\\(?:\+?[A-Za-z0-9]+)\*?")


@dataclass
class InlineContext:
    passage_id: str | None = None
    osis_ref: str | None = None
    translation_id: str = TRANSLATION_ID
    source_id: str = SOURCE_ID
    source_archive: str = SOURCE_ARCHIVE
    source_sha256: str = SOURCE_SHA256
    source_format: str = SOURCE_FORMAT
    license: str = LICENSE
    source_file: str | None = None
    source_line: int | None = None
    word_index: int = 0
    footnote_index: int = 0
    crossref_index: int = 0


@dataclass
class InlineParseResult:
    clean_text: str
    word_tokens: list[dict[str, Any]] = field(default_factory=list)
    footnotes: list[dict[str, Any]] = field(default_factory=list)
    crossrefs: list[dict[str, Any]] = field(default_factory=list)
    unsupported_markers: list[dict[str, Any]] = field(default_factory=list)
    marker_counts: Counter[str] = field(default_factory=Counter)
    word_index: int = 0
    footnote_index: int = 0
    crossref_index: int = 0


def normalize_clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def contains_raw_usfm_marker(text: str) -> bool:
    return bool(RAW_MARKER_RE.search(text))


def marker_counts(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for match in MARKER_AT_RE.finditer(text):
        if not match.group("closing"):
            counts[match.group("marker")] += 1
    return counts


def parse_attrs(text: str) -> dict[str, str]:
    return {key: value for key, value in ATTR_RE.findall(text)}


def strip_inline_usfm(text: str) -> str:
    """Strip inline USFM markup without emitting sidecars."""
    return normalize_clean_text(InlineParser().parse(text, InlineContext()).clean_text)


class InlineParser:
    def parse(self, text: str, context: InlineContext | None = None) -> InlineParseResult:
        ctx = context or InlineContext()
        state = {
            "word_index": ctx.word_index,
            "footnote_index": ctx.footnote_index,
            "crossref_index": ctx.crossref_index,
            "word_tokens": [],
            "footnotes": [],
            "crossrefs": [],
            "unsupported_markers": [],
            "marker_counts": marker_counts(text),
        }
        clean = self._parse_segment(text, ctx, state, [])
        return InlineParseResult(
            clean_text=normalize_clean_text(clean),
            word_tokens=state["word_tokens"],
            footnotes=state["footnotes"],
            crossrefs=state["crossrefs"],
            unsupported_markers=state["unsupported_markers"],
            marker_counts=state["marker_counts"],
            word_index=state["word_index"],
            footnote_index=state["footnote_index"],
            crossref_index=state["crossref_index"],
        )

    def _parse_segment(
        self,
        text: str,
        ctx: InlineContext,
        state: dict[str, Any],
        nesting: list[str],
    ) -> str:
        out: list[str] = []
        i = 0
        while i < len(text):
            if text[i] != "\\":
                out.append(text[i])
                i += 1
                continue
            parsed = self._read_marker(text, i)
            if not parsed:
                out.append(text[i])
                i += 1
                continue
            marker, closing, marker_end = parsed
            if closing:
                i = marker_end
                continue
            if marker in {"w", "+w"}:
                clean, next_i = self._handle_word(text, i, marker, marker_end, ctx, state, nesting)
                out.append(clean)
                i = next_i
                continue
            if marker == "f":
                next_i = self._handle_footnote(text, i, marker_end, ctx, state)
                i = next_i
                continue
            if marker == "x":
                next_i = self._handle_crossref(text, i, marker_end, ctx, state)
                i = next_i
                continue
            if marker in {"wj", "bk", "+bk", "+wh", "k", "qs"}:
                clean, next_i = self._handle_container(text, i, marker, marker_end, ctx, state, nesting)
                out.append(clean)
                i = next_i
                continue
            state["unsupported_markers"].append(self._unsupported(marker, text[i:marker_end], ctx, nesting))
            i = marker_end
        return "".join(out)

    def _handle_word(
        self,
        text: str,
        marker_start: int,
        marker: str,
        marker_end: int,
        ctx: InlineContext,
        state: dict[str, Any],
        nesting: list[str],
    ) -> tuple[str, int]:
        close = f"\\{marker}*"
        close_at = text.find(close, marker_end)
        if close_at < 0:
            raw = text[marker_start:]
            state["unsupported_markers"].append(self._unsupported(marker, raw, ctx, nesting, "missing closing word marker"))
            return "", len(text)
        body = text[marker_end:close_at].strip()
        surface_part, _, attr_part = body.partition("|")
        surface = normalize_clean_text(surface_part)
        attrs = parse_attrs(attr_part)
        state["word_index"] += 1
        source_marker = text[marker_start : close_at + len(close)]
        record = {
            **self._common(ctx),
            "id": f"word-token:{ctx.translation_id}:{self._scope(ctx)}:{state['word_index']:06d}",
            "type": "WordToken",
            "passage_id": ctx.passage_id,
            "osis_ref": ctx.osis_ref,
            "translation_id": ctx.translation_id,
            "word_index": state["word_index"],
            "surface_text": surface,
            "strong": attrs.get("strong"),
            "attributes": attrs,
            "is_nested": marker.startswith("+"),
            "nesting_context": list(nesting),
            "source_marker": source_marker,
        }
        state["word_tokens"].append(record)
        return surface, close_at + len(close)

    def _handle_footnote(
        self,
        text: str,
        marker_start: int,
        ctx_start: int,
        ctx: InlineContext,
        state: dict[str, Any],
    ) -> int:
        close = "\\f*"
        close_at = text.find(close, ctx_start)
        if close_at < 0:
            raw = text[marker_start:]
            state["unsupported_markers"].append(self._unsupported("f", raw, ctx, [], "missing closing footnote marker"))
            return len(text)
        raw = text[marker_start : close_at + len(close)]
        body = text[ctx_start:close_at].strip()
        state["footnote_index"] += 1
        fields = self._parse_note_fields(body)
        record = {
            **self._common(ctx),
            "id": f"footnote:{ctx.translation_id}:{self._scope(ctx)}:{state['footnote_index']:04d}",
            "type": "Footnote",
            "passage_id": ctx.passage_id,
            "osis_ref": ctx.osis_ref,
            "translation_id": ctx.translation_id,
            "footnote_index": state["footnote_index"],
            "caller": fields.get("caller"),
            "reference": fields.get("fr"),
            "text": fields.get("ft"),
            "alternate_readings": [v for key in ("fqa", "fq") for v in fields["submarkers"].get(key, [])],
            "labels": fields["submarkers"].get("fl", []),
            "hebrew_word_spans": fields["submarkers"].get("+wh", []),
            "book_title_spans": fields["submarkers"].get("+bk", []),
            "submarkers": fields["submarkers"],
            "raw_marker": raw,
        }
        state["footnotes"].append(record)
        return close_at + len(close)

    def _handle_crossref(
        self,
        text: str,
        marker_start: int,
        ctx_start: int,
        ctx: InlineContext,
        state: dict[str, Any],
    ) -> int:
        close = "\\x*"
        close_at = text.find(close, ctx_start)
        if close_at < 0:
            raw = text[marker_start:]
            state["unsupported_markers"].append(self._unsupported("x", raw, ctx, [], "missing closing crossref marker"))
            return len(text)
        raw = text[marker_start : close_at + len(close)]
        body = text[ctx_start:close_at].strip()
        state["crossref_index"] += 1
        fields = self._parse_note_fields(body)
        target_text = fields.get("xt", "")
        record = {
            **self._common(ctx),
            "id": f"editorial-crossref:{ctx.translation_id}:{self._scope(ctx)}:{state['crossref_index']:04d}",
            "type": "EditorialCrossReference",
            "passage_id": ctx.passage_id,
            "osis_ref": ctx.osis_ref,
            "translation_id": ctx.translation_id,
            "relation_type": "editorial_cross_reference",
            "crossref_index": state["crossref_index"],
            "origin": fields.get("xo"),
            "target_text": target_text,
            "candidate_osis_refs": parse_unambiguous_refs(target_text),
            "submarkers": fields["submarkers"],
            "raw_marker": raw,
        }
        state["crossrefs"].append(record)
        return close_at + len(close)

    def _handle_container(
        self,
        text: str,
        marker_start: int,
        marker: str,
        marker_end: int,
        ctx: InlineContext,
        state: dict[str, Any],
        nesting: list[str],
    ) -> tuple[str, int]:
        close = f"\\{marker}*"
        close_at = text.find(close, marker_end)
        if close_at < 0:
            state["unsupported_markers"].append(
                self._unsupported(marker, text[marker_start:marker_end], ctx, nesting, "missing closing container marker")
            )
            return "", marker_end
        inner = text[marker_end:close_at]
        clean = self._parse_segment(inner, ctx, state, [*nesting, marker])
        return clean, close_at + len(close)

    def _parse_note_fields(self, body: str) -> dict[str, Any]:
        body = body.strip()
        caller = None
        if body and not body.startswith("\\"):
            parts = body.split(None, 1)
            caller = parts[0]
            body = parts[1] if len(parts) > 1 else ""
        markers = list(MARKER_AT_RE.finditer(body))
        submarkers: dict[str, list[str]] = {}
        for idx, match in enumerate(markers):
            marker = match.group("marker")
            if match.group("closing"):
                continue
            if marker.startswith("+"):
                close = f"\\{marker}*"
                close_at = body.find(close, match.end())
                end = close_at if close_at >= 0 else self._next_top_level_marker_start(markers, idx, len(body))
            else:
                end = self._next_top_level_marker_start(markers, idx, len(body))
            value = strip_inline_usfm(body[match.end() : end])
            submarkers.setdefault(marker, []).append(value)
        return {
            "caller": caller,
            "fr": self._first(submarkers.get("fr")),
            "ft": " ".join(submarkers.get("ft", [])) if submarkers.get("ft") else None,
            "fq": self._first(submarkers.get("fq")),
            "fqa": self._first(submarkers.get("fqa")),
            "fl": self._first(submarkers.get("fl")),
            "xo": self._first(submarkers.get("xo")),
            "xt": " ".join(submarkers.get("xt", [])) if submarkers.get("xt") else "",
            "submarkers": submarkers,
        }

    def _read_marker(self, text: str, index: int) -> tuple[str, bool, int] | None:
        match = MARKER_AT_RE.match(text, index)
        if not match:
            return None
        return match.group("marker"), bool(match.group("closing")), match.end()

    def _common(self, ctx: InlineContext) -> dict[str, Any]:
        return {
            "source_id": ctx.source_id,
            "source_archive": ctx.source_archive,
            "source_sha256": ctx.source_sha256,
            "source_format": ctx.source_format,
            "license": ctx.license,
            "status": "imported",
            "generation_method": GENERATION_METHOD,
            "source_file": ctx.source_file,
            "source_line": ctx.source_line,
        }

    def _unsupported(
        self,
        marker: str,
        raw: str,
        ctx: InlineContext,
        nesting: list[str],
        reason: str = "unsupported inline marker",
    ) -> dict[str, Any]:
        digest = hashlib.sha256(f"{marker}|{raw}|{ctx.source_file}|{ctx.source_line}|{ctx.osis_ref}".encode("utf-8")).hexdigest()[:12]
        return {
            **self._common(ctx),
            "id": f"unsupported-usfm-marker:{ctx.osis_ref or 'global'}:{digest}",
            "type": "UnsupportedUSFMMarker",
            "passage_id": ctx.passage_id,
            "osis_ref": ctx.osis_ref,
            "translation_id": ctx.translation_id,
            "marker": marker,
            "raw_marker": raw,
            "nesting_context": list(nesting),
            "reason": reason,
        }

    @staticmethod
    def _first(values: list[str] | None) -> str | None:
        return values[0] if values else None

    @staticmethod
    def _next_top_level_marker_start(markers: list[re.Match[str]], idx: int, default: int) -> int:
        for later in markers[idx + 1 :]:
            marker = later.group("marker")
            if not later.group("closing") and not marker.startswith("+"):
                return later.start()
        return default

    @staticmethod
    def _scope(ctx: InlineContext) -> str:
        if ctx.osis_ref:
            return ctx.osis_ref
        raw = f"{ctx.source_file or 'global'}:{ctx.source_line or 0}"
        return re.sub(r"[^A-Za-z0-9_.:-]+", "-", raw)
