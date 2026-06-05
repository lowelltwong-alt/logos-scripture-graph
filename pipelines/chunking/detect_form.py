#!/usr/bin/env python3
"""Deterministic textual-form detector (T310 Increment 1).

Reads canonical passage/witness/boundary evidence and emits candidate-zone
ClassificationAssignment records (axis=textual_form). Parallel to the chunker;
does not route, apply skills, or mutate canonical data.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GENRES = ROOT / "config" / "chunking" / "book_genres.yaml"
DEFAULT_FORM_REGISTRY = ROOT / "config" / "chunking" / "form_registry.yaml"
DEFAULT_MARKER_COVERAGE = ROOT / "config" / "ingest" / "usfm_marker_coverage.yaml"

DETECTOR_VERSION = "detect_form.v0.1.0"
SOURCE_TEXT_ID = "eng-web"
SOURCE_METADATA_KEYS = ("source_sha256", "license")

# Read-only seam into chunker (no chunker.py edits).
from pipelines.chunking.chunker import (  # noqa: E402
    HEADING_MARKERS,
    PARAGRAPH_MARKERS,
    POETRY_MARKERS,
    POETRY_GENRES,
    build_units,
    load_genres,
    load_jsonl,
)

POETRY_BOOKS = {"Ps", "Song", "Lam", "PrMan", "Ps151"}
LIST_MARKERS = {"ili", "li1"}
MAJOR_TITLE_MARKERS = {"mt1", "mt2", "mt3"}
INTRO_MARKERS = {"is1", "ip"}
SECTION_HEADING_MARKERS = {"ms1", "s1", "ms", "s", "s1", "s2"}

BOOK_PRIOR_TO_FORM: dict[str, str] = {
    "law": "law_statute",
    "wisdom": "wisdom_saying_cluster",
    "prophets": "prophetic_oracle",
    "apocalypse": "apocalyptic_cycle",
    "gospels": "gospel_pericope",
    "epistles": "epistle_argument",
    "acts": "acts_speech_or_episode",
    "narrative": "narrative_scene",
    "psalms": "psalm_whole",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_allowed_markers(path: Path) -> set[str]:
    allowed: set[str] = set()
    section: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("markers:"):
            section = "markers"
            continue
        if stripped.startswith("forward_declared:"):
            section = "forward_declared"
            continue
        if section and stripped and not stripped.startswith("#"):
            if line.startswith("  ") and not line.startswith("   ") and stripped.endswith(":"):
                continue
            m = re.match(r"\s+([A-Za-z0-9]+):", line)
            if m and section in {"markers", "forward_declared"}:
                allowed.add(m.group(1))
    return allowed


def load_form_registry(path: Path) -> tuple[str, set[str]]:
    """Return (version, registered_form_ids). Dependency-light YAML scan."""
    version = "0.1.0"
    form_ids: set[str] = set()
    in_forms = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("version:"):
            version = stripped.split(":", 1)[1].strip()
            continue
        if stripped.startswith("forms:"):
            in_forms = True
            continue
        if in_forms:
            if line and not line.startswith((" ", "\t")):
                in_forms = False
                continue
            inline = re.match(r"-\s+\{id:\s*([a-z_0-9]+)", stripped)
            if inline:
                form_ids.add(inline.group(1))
                continue
            dash_id = re.match(r"-\s+id:\s*([a-z_0-9]+)", stripped)
            if dash_id:
                form_ids.add(dash_id.group(1))
                continue
            bare_id = re.match(r"id:\s*([a-z_0-9]+)", stripped)
            if bare_id:
                form_ids.add(bare_id.group(1))
    return version, form_ids


def load_source_metadata(paths: list[Path]) -> dict[str, str]:
    """Read required source metadata from actual input JSONL records."""
    values: dict[str, set[str]] = {key: set() for key in SOURCE_METADATA_KEYS}
    for path in paths:
        if not path.exists():
            continue
        for row in load_jsonl(path):
            for key in SOURCE_METADATA_KEYS:
                value = row.get(key)
                if value:
                    values[key].add(value)

    metadata: dict[str, str] = {}
    for key, seen in values.items():
        if not seen:
            raise ValueError(f"Missing {key} in form detector source inputs")
        if len(seen) > 1:
            raise ValueError(f"Conflicting {key} values in form detector source inputs: {sorted(seen)}")
        metadata[key] = next(iter(seen))
    return metadata


def numeric_to_confidence_enum(score: float) -> str:
    if score <= 0.0:
        return "unknown"
    if score >= 0.90:
        return "high"
    if score >= 0.70:
        return "medium"
    return "low"


def aggregate_markers(units: list[dict[str, Any]]) -> Counter:
    counts: Counter = Counter()
    for unit in units:
        for marker in unit.get("markers") or set():
            if marker:
                counts[marker] += 1
    return counts


def poetry_ratio(units: list[dict[str, Any]]) -> float:
    if not units:
        return 0.0
    poetry_verses = sum(1 for u in units if u.get("is_poetry") or (u.get("markers") & POETRY_MARKERS))
    return poetry_verses / len(units)


def list_ratio(units: list[dict[str, Any]]) -> float:
    if not units:
        return 0.0
    list_verses = sum(1 for u in units if u.get("markers") & LIST_MARKERS)
    return list_verses / len(units)


def has_interior_superscription(units: list[dict[str, Any]]) -> bool:
    for i, unit in enumerate(units):
        if i > 0 and unit.get("has_superscription"):
            return True
    return False


def unregistered_markers(markers: Counter, allowed: set[str]) -> list[str]:
    return sorted(m for m in markers if m and m not in allowed)


def detect_form_for_unit(
    unit: dict[str, Any],
    *,
    book_genre: str,
    allowed_markers: set[str],
    registered_forms: set[str],
) -> tuple[str, float, str, list[str]]:
    """Return (form_id, numeric_confidence, rule_id, reason_codes)."""
    markers = unit.get("markers") or set()
    counts = Counter(markers)
    bad = unregistered_markers(counts, allowed_markers)
    if bad:
        return "unknown", 0.0, "fail_closed_unregistered_marker", [f"UNREGISTERED_MARKER:{bad[0]}"]

    if "sp" in markers:
        return "speaker_dialogue", 1.0, "marker_sp_v1", []

    if markers & LIST_MARKERS:
        return "genealogy_or_list", 1.0, "marker_list_v1", []

    if markers & MAJOR_TITLE_MARKERS:
        return "major_title_block", 1.0, "marker_major_title_v1", []

    if markers & INTRO_MARKERS:
        return "intro_block", 1.0, "marker_intro_v1", []

    units = [unit]
    return _classify_aggregate(units, book_genre=book_genre, registered_forms=registered_forms)


def _classify_aggregate(
    units: list[dict[str, Any]],
    *,
    book_genre: str,
    registered_forms: set[str],
) -> tuple[str, float, str, list[str]]:
    markers = aggregate_markers(units)
    marker_keys = set(markers.keys())
    book = units[0].get("book", "")
    ratio_poetry = poetry_ratio(units)
    ratio_list = list_ratio(units)

    if ratio_list >= 0.5:
        return "genealogy_or_list", 1.0, "aggregate_list_v1", []

    if ratio_poetry >= 0.5:
        if has_interior_superscription(units) and "b" in marker_keys:
            return "poetry_acrostic_section", 0.95, "poetry_acrostic_interior_d_v1", []
        if "b" in marker_keys:
            return "poetry_stanza", 0.95, "poetry_stanza_b_v1", []
        if book in POETRY_BOOKS or book_genre == "psalms":
            return "psalm_whole", 1.0, "poetry_psalm_chapter_v1", []
        return "poetry_line_or_colon", 0.95, "poetry_line_v1", []

    if any(u.get("has_heading") for u in units) and (marker_keys & SECTION_HEADING_MARKERS):
        if book_genre == "gospels":
            return "gospel_pericope", 0.92, "heading_gospel_v1", []
        return "prose_section_heading", 0.92, "heading_section_v1", []

    if marker_keys & PARAGRAPH_MARKERS:
        prior_form = BOOK_PRIOR_TO_FORM.get(book_genre)
        if prior_form and prior_form in registered_forms:
            return prior_form, 0.75, "book_prior_fallback_v1", []
        return "prose_paragraph", 0.72, "prose_paragraph_v1", []

    return "unknown", 0.0, "fail_closed_no_match", ["NO_MATCHING_RULE"]


def detect_form_for_window(
    units: list[dict[str, Any]],
    *,
    book_genre: str,
    allowed_markers: set[str],
    registered_forms: set[str],
    window_kind: str,
) -> tuple[str, float, str, list[str]]:
    if not units:
        return "unknown", 0.0, "fail_closed_empty_window", ["EMPTY_WINDOW"]

    markers = aggregate_markers(units)
    bad = unregistered_markers(markers, allowed_markers)
    if bad:
        return "unknown", 0.0, "fail_closed_unregistered_marker", [f"UNREGISTERED_MARKER:{bad[0]}"]

    # Single-verse sp/list shortcuts at window level.
    if len(units) == 1:
        return detect_form_for_unit(
            units[0],
            book_genre=book_genre,
            allowed_markers=allowed_markers,
            registered_forms=registered_forms,
        )

    # Any sp in multi-verse window should have been split; if not, prefer dialogue.
    if "sp" in markers:
        return "speaker_dialogue", 1.0, "marker_sp_window_v1", []

    form, score, rule, reasons = _classify_aggregate(
        units, book_genre=book_genre, registered_forms=registered_forms
    )
    if window_kind == "chapter" and form == "psalm_whole":
        score = max(score, 1.0)
    return form, score, rule, reasons


def subject_id_for_window(units: list[dict[str, Any]], source_text_id: str = SOURCE_TEXT_ID) -> str:
    start = units[0]["osis_ref"]
    end = units[-1]["osis_ref"]
    if start == end:
        return units[0]["passage_id"]
    return f"span:{source_text_id}:{start}--{end}"


def build_overlay_index(
    word_tokens_path: Path | None,
    footnotes_path: Path | None,
) -> dict[str, Any]:
    index: dict[str, Any] = {
        "wj_by_osis": set(),
        "lexeme_by_osis": set(),
        "footnote_by_osis": set(),
        "variant_by_osis": set(),
    }
    if word_tokens_path and word_tokens_path.exists():
        for row in load_jsonl(word_tokens_path):
            osis = row.get("osis_ref")
            if not osis:
                continue
            index["lexeme_by_osis"].add(osis)
            nesting = row.get("nesting_context") or []
            if any(n == "wj" for n in nesting):
                index["wj_by_osis"].add(osis)
    if footnotes_path and footnotes_path.exists():
        for row in load_jsonl(footnotes_path):
            osis = row.get("osis_ref")
            if not osis:
                continue
            index["footnote_by_osis"].add(osis)
            if row.get("alternate_readings"):
                index["variant_by_osis"].add(osis)
    return index


def detect_overlays(
    units: list[dict[str, Any]],
    overlay_index: dict[str, Any] | None,
) -> list[str]:
    overlays: list[str] = []
    osis_set = {u["osis_ref"] for u in units}

    if any(u.get("has_superscription") for u in units):
        overlays.append("superscription_attached")
    if any("qs" in (u.get("markers") or set()) for u in units):
        overlays.append("selah_rubric")

    if overlay_index:
        if osis_set & overlay_index.get("wj_by_osis", set()):
            overlays.append("words_of_jesus")
        if osis_set & overlay_index.get("variant_by_osis", set()):
            overlays.append("variant_reading")
        if osis_set & overlay_index.get("footnote_by_osis", set()):
            overlays.append("footnote_carry")
        if osis_set & overlay_index.get("lexeme_by_osis", set()):
            overlays.append("lexeme_alignment")

    return overlays


def make_classification_assignment(
    units: list[dict[str, Any]],
    *,
    form_id: str,
    numeric_confidence: float,
    rule_id: str,
    reason_codes: list[str],
    book_genre: str,
    window_kind: str,
    form_registry_version: str,
    overlays: list[str],
    marker_counts: Counter,
    source_sha256: str,
    license: str,
) -> dict[str, Any]:
    osis_start = units[0]["osis_ref"]
    osis_end = units[-1]["osis_ref"]
    conf_enum = numeric_to_confidence_enum(numeric_confidence)
    if form_id == "unknown":
        conf_enum = "unknown"

    record: dict[str, Any] = {
        "id": f"classify-form--{SOURCE_TEXT_ID}--{osis_start}--{osis_end}--{form_id}--v1",
        "type": "ClassificationAssignment",
        "subject_id": subject_id_for_window(units),
        "axis": "textual_form",
        "value": form_id,
        "assertion_mode": "inferred_rule",
        "confidence": conf_enum,
        "source_sha256": source_sha256,
        "license": license,
        "provenance": {
            "created_by": DETECTOR_VERSION,
            "created_at": utc_now(),
            "basis": (
                f"usfm_marker_rules_v1; rule_id={rule_id}; "
                f"form_registry={form_registry_version}; fail_closed={'yes' if form_id == 'unknown' else 'no'}"
            ),
        },
        "trust_zone": "candidate",
        "status": "candidate",
        "span": {
            "source_text_id": SOURCE_TEXT_ID,
            "osis_start": osis_start,
            "osis_end": osis_end,
        },
        "overlays": overlays,
        "detection": {
            "rule_id": rule_id,
            "book_genre_prior": book_genre,
            "window_kind": window_kind,
            "markers_present": sorted(marker_counts.keys()),
            "numeric_confidence": numeric_confidence,
            "reason_codes": reason_codes,
            "form_registry_version": form_registry_version,
        },
    }
    if reason_codes:
        record["evidence"] = [
            {
                "kind": "scripture",
                "ref": osis_start if osis_start == osis_end else f"{osis_start}..{osis_end}",
                "note": f"rule={rule_id}; reasons={','.join(reason_codes)}",
            }
        ]
    elif marker_counts:
        record["evidence"] = [
            {
                "kind": "scripture",
                "ref": osis_start if osis_start == osis_end else f"{osis_start}..{osis_end}",
                "note": f"rule={rule_id}; markers={','.join(sorted(marker_counts.keys())[:12])}",
            }
        ]
    return record


def _is_psalm_like(book: str, genres: dict[str, str], default_genre: str) -> bool:
    genre = genres.get(book, default_genre)
    return genre == "psalms" or book in POETRY_BOOKS


def _should_start_new_window(
    unit: dict[str, Any],
    current: list[dict[str, Any]],
    *,
    genres: dict[str, str],
    default_genre: str,
) -> bool:
    if not current:
        return False
    prev = current[-1]
    if unit["book"] != prev["book"]:
        return True
    markers = unit.get("markers") or set()
    if "sp" in markers:
        return True
    if unit.get("has_heading"):
        return True
    book = unit["book"]
    if _is_psalm_like(book, genres, default_genre):
        if unit.get("chapter") != prev.get("chapter"):
            return True
    return False


def segment_windows(
    units: list[dict[str, Any]],
    genres: dict[str, str],
    default_genre: str,
) -> list[tuple[list[dict[str, Any]], str]]:
    """Return (units, window_kind) segments."""
    windows: list[tuple[list[dict[str, Any]], str]] = []
    current: list[dict[str, Any]] = []

    def flush(kind: str) -> None:
        nonlocal current
        if current:
            windows.append((current, kind))
            current = []

    for unit in units:
        if _should_start_new_window(unit, current, genres=genres, default_genre=default_genre):
            prev = current[-1]
            kind = "chapter" if _is_psalm_like(prev["book"], genres, default_genre) else "heading"
            flush(kind)
        current.append(unit)

    if current:
        book = current[0]["book"]
        kind = "chapter" if _is_psalm_like(book, genres, default_genre) else "section"
        flush(kind)

    return windows


def detect_forms_for_corpus(
    units: list[dict[str, Any]],
    *,
    genres: dict[str, str],
    default_genre: str,
    allowed_markers: set[str],
    registered_forms: set[str],
    form_registry_version: str,
    overlay_index: dict[str, Any] | None,
    source_metadata: dict[str, str],
) -> Iterator[dict[str, Any]]:
    for window_units, window_kind in segment_windows(units, genres, default_genre):
        book = window_units[0]["book"]
        book_genre = genres.get(book, default_genre)
        form_id, score, rule_id, reasons = detect_form_for_window(
            window_units,
            book_genre=book_genre,
            allowed_markers=allowed_markers,
            registered_forms=registered_forms,
            window_kind=window_kind,
        )
        if form_id not in registered_forms and form_id != "unknown":
            form_id, score, rule_id, reasons = (
                "unknown",
                0.0,
                "fail_closed_unregistered_form",
                [f"UNREGISTERED_FORM:{form_id}"],
            )
        marker_counts = aggregate_markers(window_units)
        overlays = detect_overlays(window_units, overlay_index)
        yield make_classification_assignment(
            window_units,
            form_id=form_id,
            numeric_confidence=score,
            rule_id=rule_id,
            reason_codes=reasons,
            book_genre=book_genre,
            window_kind=window_kind,
            form_registry_version=form_registry_version,
            overlays=overlays,
            marker_counts=marker_counts,
            source_sha256=source_metadata["source_sha256"],
            license=source_metadata["license"],
        )


def write_classifications(records: Iterator[dict[str, Any]], out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit candidate textual_form ClassificationAssignments")
    parser.add_argument("--passages", required=True)
    parser.add_argument("--witnesses", required=True)
    parser.add_argument("--boundary-claims", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--genres", default=str(DEFAULT_GENRES))
    parser.add_argument("--form-registry", default=str(DEFAULT_FORM_REGISTRY))
    parser.add_argument("--marker-coverage", default=str(DEFAULT_MARKER_COVERAGE))
    parser.add_argument("--word-tokens", default=None, help="Optional sidecar for wj/lexeme overlays")
    parser.add_argument("--footnotes", default=None, help="Optional sidecar for footnote overlays")
    args = parser.parse_args()

    genres, default_genre = load_genres(Path(args.genres))
    form_registry_version, registered_forms = load_form_registry(Path(args.form_registry))
    registered_forms.add("unknown")
    allowed_markers = load_allowed_markers(Path(args.marker_coverage))
    source_metadata = load_source_metadata(
        [Path(args.passages), Path(args.witnesses), Path(args.boundary_claims)]
    )

    overlay_index = build_overlay_index(
        Path(args.word_tokens) if args.word_tokens else None,
        Path(args.footnotes) if args.footnotes else None,
    )
    if not args.word_tokens and not args.footnotes:
        overlay_index = None

    units = list(
        build_units(
            Path(args.passages),
            Path(args.witnesses),
            Path(args.boundary_claims),
        )
    )
    records = detect_forms_for_corpus(
        units,
        genres=genres,
        default_genre=default_genre,
        allowed_markers=allowed_markers,
        registered_forms=registered_forms,
        form_registry_version=form_registry_version,
        overlay_index=overlay_index,
        source_metadata=source_metadata,
    )
    count = write_classifications(records, Path(args.out))
    print(f"Wrote {count} candidate ClassificationAssignment records to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
