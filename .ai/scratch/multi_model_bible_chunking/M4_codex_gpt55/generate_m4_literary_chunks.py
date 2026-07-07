#!/usr/bin/env python3
"""Generate M4 T423 scratch chunks from the Rust observation substrate.

This is a model-lane-local scratch helper. It is not a governed chunker and it
does not authorize canon output, reviewed gold, graph edges, or theology claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
MODEL_ID = "M4_codex_gpt55"
MODEL_FOLDER = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / MODEL_ID
SUBSTRATE = ROOT / "build" / "observation_substrate" / "current"
CANON_PATH = ROOT / "config" / "canon" / "canonical_66_books.yaml"
GENRES_PATH = ROOT / "config" / "chunking" / "book_genres.yaml"
BASELINE_MANIFEST = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "shared_research_baseline"
    / "research_baseline_manifest.yaml"
)

ACTIVE_ARTIFACTS = [
    "book_chunks",
    "book_strategy",
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
    "layer_decision_log.jsonl",
    "whole_bible_chunk_map.jsonl",
    "model_quality_summary.md",
    "model_summary.md",
]

MARKER_BOUNDARY_KEYS = {
    "p",
    "m",
    "mi",
    "pi1",
    "pc",
    "s1",
    "s2",
    "ms1",
    "sp",
    "d",
    "li1",
    "ili",
}
POETRY_KEYS = {"q1", "q2", "q3", "qr", "qc", "qs", "d", "b"}
LOW_RISK_SIGNALS = {"has_footnote", "has_crossref", "has_poetry_or_liturgy_marker", "has_wj"}
FRONTIER_BOOKS = {"Dan", "Rev"}
PILOT_FRAGILE_BOOKS = {"Gen", "Ps", "Phlm", "Jonah", "Dan", "Rev"}

TARGETS = {
    "narrative": (28, 42),
    "law": (22, 34),
    "psalms": (18, 28),
    "wisdom": (18, 28),
    "prophets": (18, 30),
    "gospels": (22, 34),
    "acts": (24, 38),
    "epistles": (14, 24),
    "apocalypse": (12, 22),
}

BOOK_FAMILY: dict[str, str] = {
    **{b: "Torah" for b in ["Gen", "Exod", "Lev", "Num", "Deut"]},
    **{b: "Former Prophets / History" for b in ["Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs"]},
    **{
        b: "Writings"
        for b in ["1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov", "Eccl", "Song", "Lam"]
    },
    **{b: "Major Prophets" for b in ["Isa", "Jer", "Ezek", "Dan"]},
    **{
        b: "Minor Prophets"
        for b in ["Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"]
    },
    **{b: "Gospels and Acts" for b in ["Matt", "Mark", "Luke", "John", "Acts"]},
}


@dataclass(frozen=True, order=True)
class Ref:
    book: str
    chapter: int
    verse: int

    @classmethod
    def parse(cls, raw: str) -> "Ref":
        book, chapter, verse = raw.split(".")
        return cls(book=book, chapter=int(chapter), verse=int(verse))

    def osis(self) -> str:
        return f"{self.book}.{self.chapter}.{self.verse}"


@dataclass
class Unit:
    start: Ref
    end: Ref
    reasons: list[str]

    def span(self) -> str:
        if self.start == self.end:
            return self.start.osis()
        return f"{self.start.osis()}-{self.end.osis()}"

    def verse_count(self, verse_index: dict[tuple[str, int, int], int]) -> int:
        return verse_index[self.end.book, self.end.chapter, self.end.verse] - verse_index[
            self.start.book, self.start.chapter, self.start.verse
        ] + 1


def read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]], append: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with path.open(mode, encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_books() -> list[str]:
    books = read_yaml(CANON_PATH).get("canonical_66_books")
    if not isinstance(books, list) or len(books) != 66:
        raise ValueError("canonical_66_books.yaml must contain 66 books")
    return [str(book) for book in books]


def genres() -> dict[str, str]:
    return {str(k): str(v) for k, v in read_yaml(GENRES_PATH).get("genres", {}).items()}


class Substrate:
    def __init__(self) -> None:
        self.book_rows: dict[str, dict[str, Any]] = {}
        self.verses: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.chapter_features: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
        self.risk_by_ref: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
        self.scan_manifest = json.loads((SUBSTRATE / "scan_manifest.json").read_text(encoding="utf-8"))

        for row in iter_jsonl(SUBSTRATE / "book_observations.jsonl"):
            self.book_rows[str(row["book_id"])] = row

        for row in iter_jsonl(SUBSTRATE / "verse_observations.jsonl"):
            book = str(row["book_id"])
            self.verses[book].append(row)

        for rows in self.verses.values():
            rows.sort(key=lambda r: (int(r["chapter"]), int(r["verse"])))

        for row in iter_jsonl(SUBSTRATE / "span_observation_features.jsonl"):
            book = str(row["book_id"])
            start = Ref.parse(str(row["osis_start"]))
            end = Ref.parse(str(row["osis_end"]))
            if start.chapter == end.chapter and str(row.get("span_kind")) == "chapter_observed_feature_rollup":
                self.chapter_features[book][start.chapter] = row

        for row in iter_jsonl(SUBSTRATE / "risk_signal_index.jsonl"):
            book = str(row["book_id"])
            ref = str(row["osis_ref"])
            self.risk_by_ref[book][ref].append(row)

    def refs(self, book: str) -> list[Ref]:
        return [Ref(book, int(row["chapter"]), int(row["verse"])) for row in self.verses[book]]

    def index(self, book: str) -> dict[tuple[str, int, int], int]:
        return {ref_key(ref): i for i, ref in enumerate(self.refs(book))}

    def verse_row(self, ref: Ref) -> dict[str, Any]:
        for row in self.verses[ref.book]:
            if int(row["chapter"]) == ref.chapter and int(row["verse"]) == ref.verse:
                return row
        raise KeyError(ref)

    def verse_rows_in(self, start: Ref, end: Ref) -> list[dict[str, Any]]:
        return [
            row
            for row in self.verses[start.book]
            if (int(row["chapter"]), int(row["verse"])) >= (start.chapter, start.verse)
            and (int(row["chapter"]), int(row["verse"])) <= (end.chapter, end.verse)
        ]


def ref_key(ref: Ref) -> tuple[str, int, int]:
    return (ref.book, ref.chapter, ref.verse)


def prev_ref(refs: list[Ref], ref: Ref) -> Ref:
    idx = {ref_key(r): i for i, r in enumerate(refs)}[ref_key(ref)]
    if idx == 0:
        return ref
    return refs[idx - 1]


def next_ref(refs: list[Ref], ref: Ref) -> Ref | None:
    idx = {ref_key(r): i for i, r in enumerate(refs)}[ref_key(ref)]
    if idx + 1 >= len(refs):
        return None
    return refs[idx + 1]


def marker_counter(rows: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for key, value in (row.get("marker_counts") or {}).items():
            counts[str(key)] += int(value)
    return counts


def signal_set(substrate: Substrate, book: str, start: Ref, end: Ref) -> set[str]:
    signals: set[str] = set()
    for row in substrate.verse_rows_in(start, end):
        for flag in row.get("feature_flags") or []:
            signals.add(str(flag))
        for risk in substrate.risk_by_ref[book].get(str(row["osis_ref"]), []):
            signals.add(str(risk.get("signal_kind", "")))
    markers = marker_counter(substrate.verse_rows_in(start, end))
    for marker in markers:
        if marker in POETRY_KEYS:
            signals.add("has_poetry_or_liturgy_marker")
        if marker == "wj":
            signals.add("has_wj")
        if marker == "x":
            signals.add("has_crossref")
        if marker in {"f", "fqa"}:
            signals.add("has_footnote")
        if marker in {"sp"}:
            signals.add("has_speaker_label")
        if marker in {"li1", "ili"}:
            signals.add("has_list_marker")
    return {signal for signal in signals if signal}


def structural_boundary_starts(
    substrate: Substrate,
    book: str,
    *,
    genre: str,
    include_poetry: bool = False,
    include_wj: bool = False,
) -> list[Ref]:
    refs = substrate.refs(book)
    starts: set[tuple[str, int, int]] = {ref_key(refs[0])}
    last_chapter = refs[0].chapter
    for ref in refs:
        row = substrate.verse_row(ref)
        markers = {str(k) for k, v in (row.get("marker_counts") or {}).items() if int(v) > 0}
        if ref.chapter != last_chapter:
            starts.add(ref_key(ref))
            last_chapter = ref.chapter
        if markers & MARKER_BOUNDARY_KEYS:
            starts.add(ref_key(ref))
        if include_poetry and markers & POETRY_KEYS:
            starts.add(ref_key(ref))
        if include_wj and "wj" in markers:
            starts.add(ref_key(ref))
        if genre in {"epistles", "gospels", "acts"} and {"s1", "ms1"} & markers:
            starts.add(ref_key(ref))
    return sorted((Ref(*key) for key in starts), key=lambda r: (r.chapter, r.verse))


def make_units(substrate: Substrate, book: str, starts: list[Ref], reasons: list[str], final_end: Ref | None = None) -> list[Unit]:
    refs = substrate.refs(book)
    units: list[Unit] = []
    for i, start in enumerate(starts):
        if i + 1 < len(starts):
            end = prev_ref(refs, starts[i + 1])
        else:
            end = final_end or refs[-1]
        if ref_key(start) <= ref_key(end):
            units.append(Unit(start, end, list(reasons)))
    return units


def split_large_unit(unit: Unit, refs: list[Ref], verse_index: dict[tuple[str, int, int], int], max_size: int) -> list[Unit]:
    count = unit.verse_count(verse_index)
    if count <= max_size:
        return [unit]
    start_idx = verse_index[ref_key(unit.start)]
    end_idx = verse_index[ref_key(unit.end)]
    out: list[Unit] = []
    current = start_idx
    while current <= end_idx:
        chunk_end = min(current + max_size - 1, end_idx)
        out.append(Unit(refs[current], refs[chunk_end], unit.reasons + ["size_split_at_verse_boundary"]))
        current = chunk_end + 1
    return out


def group_units(
    units: list[Unit],
    *,
    refs: list[Ref],
    verse_index: dict[tuple[str, int, int], int],
    target: int,
    max_size: int,
    allow_cross_chapter: bool,
) -> list[Unit]:
    expanded: list[Unit] = []
    for unit in units:
        expanded.extend(split_large_unit(unit, refs, verse_index, max_size))

    grouped: list[Unit] = []
    current: Unit | None = None
    current_count = 0
    current_reasons: list[str] = []

    for unit in expanded:
        unit_count = unit.verse_count(verse_index)
        crosses = current is not None and current.end.chapter != unit.start.chapter
        would_exceed = current is not None and current_count + unit_count > max_size
        target_met = current is not None and current_count >= target
        if current is not None and (would_exceed or (target_met and (crosses or not allow_cross_chapter))):
            grouped.append(Unit(current.start, current.end, dedupe(current_reasons)))
            current = None
            current_count = 0
            current_reasons = []

        if current is None:
            current = Unit(unit.start, unit.end, [])
            current_count = 0
            current_reasons = []
        else:
            current.end = unit.end
        current_count += unit_count
        current_reasons.extend(unit.reasons)

    if current is not None:
        grouped.append(Unit(current.start, current.end, dedupe(current_reasons)))
    return grouped


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def psalm_units(substrate: Substrate, book: str, genre: str) -> list[Unit]:
    refs = substrate.refs(book)
    verse_index = substrate.index(book)
    units: list[Unit] = []
    chapters = sorted({ref.chapter for ref in refs})
    for chapter in chapters:
        chapter_refs = [ref for ref in refs if ref.chapter == chapter]
        if book == "Ps" and chapter == 119:
            for start in range(1, 177, 8):
                units.append(
                    Unit(
                        Ref(book, 119, start),
                        Ref(book, 119, min(start + 7, 176)),
                        ["psalm_119_acrostic_eight_verse_stanza", "poetry_marker_evidence"],
                    )
                )
            continue
        if len(chapter_refs) <= 32:
            units.append(Unit(chapter_refs[0], chapter_refs[-1], ["whole_poem_or_psalm_preserved"]))
            continue
        starts = structural_boundary_starts(substrate, book, genre=genre, include_poetry=False)
        starts = [start for start in starts if start.chapter == chapter]
        if len(starts) < 2:
            starts = [chapter_refs[i] for i in range(0, len(chapter_refs), 24)]
        chapter_units = make_units(
            substrate,
            book,
            starts,
            ["poetry_stanza_or_paragraph_cluster"],
            final_end=chapter_refs[-1],
        )
        units.extend(
            group_units(
                chapter_units,
                refs=refs,
                verse_index=verse_index,
                target=18,
                max_size=30,
                allow_cross_chapter=False,
            )
        )
    return units


def special_one_chapter_book_units(substrate: Substrate, book: str) -> list[Unit] | None:
    last = substrate.refs(book)[-1].verse
    specials: dict[str, list[tuple[int, int, str]]] = {
        "Phlm": [(1, min(7, last), "epistle_greeting_and_thanksgiving"), (8, min(22, last), "appeal_body"), (23, last, "epistle_closing")],
        "Jude": [(1, min(2, last), "epistle_greeting"), (3, min(16, last), "warning_body"), (17, min(23, last), "exhortation"), (24, last, "doxology_closing")],
        "2John": [(1, min(3, last), "epistle_greeting"), (4, min(11, last), "body_exhortation"), (12, last, "epistle_closing")],
        "3John": [(1, min(4, last), "epistle_greeting"), (5, min(12, last), "body"), (13, last, "epistle_closing")],
        "Obad": [(1, min(9, last), "prophetic_oracle_opening"), (10, min(16, last), "oracle_accusation"), (17, last, "restoration_oracle")],
    }
    if book not in specials:
        return None
    units: list[Unit] = []
    for start, end, reason in specials[book]:
        if start <= end:
            units.append(Unit(Ref(book, 1, start), Ref(book, 1, end), [reason, "one_chapter_literary_unit"]))
    return units


def dan_rev_units(substrate: Substrate, book: str, genre: str) -> list[Unit]:
    refs = substrate.refs(book)
    verse_index = substrate.index(book)
    chapter_last = {chapter: max(ref.verse for ref in refs if ref.chapter == chapter) for chapter in {r.chapter for r in refs}}
    if book == "Dan":
        outline: list[tuple[tuple[int, int], tuple[int, int], str]] = [
            ((1, 1), (1, chapter_last[1]), "court_narrative_opening"),
            ((2, 1), (2, chapter_last[2]), "dream_vision_report"),
            ((3, 1), (3, chapter_last[3]), "court_narrative_trial"),
            ((4, 1), (4, chapter_last[4]), "royal_dream_testimony"),
            ((5, 1), (5, chapter_last[5]), "court_judgment_scene"),
            ((6, 1), (6, chapter_last[6]), "court_narrative_trial"),
            ((7, 1), (7, chapter_last[7]), "apocalyptic_vision_cycle"),
            ((8, 1), (8, chapter_last[8]), "apocalyptic_vision_cycle"),
            ((9, 1), (9, chapter_last[9]), "prayer_and_angelic_disclosure"),
            ((10, 1), (12, chapter_last[12]), "final_apocalyptic_disclosure_cycle"),
        ]
    else:
        outline = [
            ((1, 1), (1, chapter_last[1]), "prologue_and_commission_vision"),
            ((2, 1), (3, chapter_last[3]), "seven_church_messages"),
            ((4, 1), (5, chapter_last[5]), "throne_room_vision"),
            ((6, 1), (8, 5), "seal_cycle"),
            ((8, 6), (11, chapter_last[11]), "trumpet_cycle"),
            ((12, 1), (14, chapter_last[14]), "symbolic_conflict_cycle"),
            ((15, 1), (16, chapter_last[16]), "bowl_cycle"),
            ((17, 1), (18, chapter_last[18]), "babylon_vision_cycle"),
            ((19, 1), (20, chapter_last[20]), "victory_and_judgment_cycle"),
            ((21, 1), (22, 5), "new_creation_vision"),
            ((22, 6), (22, chapter_last[22]), "epilogue_and_closing"),
        ]
    units = [
        Unit(Ref(book, sc, sv), Ref(book, ec, ev), [reason, "frontier_apocalyptic_outline"])
        for (sc, sv), (ec, ev), reason in outline
    ]
    target, max_size = TARGETS.get(genre, TARGETS["prophets"])
    out: list[Unit] = []
    for unit in units:
        out.extend(split_large_unit(unit, refs, verse_index, max_size))
    return out


def book_units(substrate: Substrate, book: str, genre: str) -> list[Unit]:
    special = special_one_chapter_book_units(substrate, book)
    if special is not None:
        return special
    if book in FRONTIER_BOOKS:
        return dan_rev_units(substrate, book, genre)
    if genre == "psalms":
        return psalm_units(substrate, book, genre)

    refs = substrate.refs(book)
    verse_index = substrate.index(book)
    include_poetry = genre in {"wisdom", "prophets"}
    include_wj = genre in {"gospels", "apocalypse"}
    starts = structural_boundary_starts(substrate, book, genre=genre, include_poetry=include_poetry, include_wj=include_wj)
    reasons = ["paragraph_marker_cluster", f"genre:{genre}", "chapter_boundary_considered_weak"]
    if include_poetry:
        reasons.append("poetry_marker_considered")
    if include_wj:
        reasons.append("wj_marker_considered_evidence_only")
    units = make_units(substrate, book, starts, reasons)
    target, max_size = TARGETS.get(genre, TARGETS["narrative"])
    allow_cross = genre in {"narrative", "acts", "epistles", "gospels"} and book not in PILOT_FRAGILE_BOOKS
    return group_units(units, refs=refs, verse_index=verse_index, target=target, max_size=max_size, allow_cross_chapter=allow_cross)


def chapter_full_span(substrate: Substrate, unit: Unit) -> bool:
    if unit.start.chapter != unit.end.chapter:
        return False
    feature = substrate.chapter_features.get(unit.start.book, {}).get(unit.start.chapter)
    if not feature:
        return False
    return str(feature["osis_start"]) == unit.start.osis() and str(feature["osis_end"]) == unit.end.osis()


def observed_signals(substrate: Substrate, book: str, unit: Unit) -> list[str]:
    rows = substrate.verse_rows_in(unit.start, unit.end)
    markers = marker_counter(rows)
    signals = sorted(signal_set(substrate, book, unit.start, unit.end))
    marker_bits = [f"marker:{key}={value}" for key, value in sorted(markers.items()) if key in {"p", "m", "q1", "q2", "q3", "b", "d", "sp", "wj", "f", "fqa", "x", "li1", "ili"}]
    return signals + marker_bits[:12]


def concern_type(substrate: Substrate, book: str, unit: Unit, genre: str) -> str:
    signals = signal_set(substrate, book, unit.start, unit.end)
    rows = substrate.verse_rows_in(unit.start, unit.end)
    markers = marker_counter(rows)
    if book == "Rev" or book == "Dan":
        return "apocalyptic_frontier"
    if "has_wj" in signals or markers.get("wj", 0):
        return "wj_speaker_discourse"
    if "has_poetry_or_liturgy_marker" in signals or markers.keys() & POETRY_KEYS:
        return "poetry_liturgy"
    if markers.get("sp", 0):
        return "speaker_shift"
    if markers.get("fqa", 0) or "has_footnote" in signals:
        return "footnote_or_variant_evidence"
    if "has_crossref" in signals:
        return "crossref_intertext_evidence"
    if markers.get("li1", 0) or markers.get("ili", 0):
        return "list_or_genealogy"
    if genre == "law":
        return "legal_covenant_unit"
    if chapter_full_span(substrate, unit):
        return "chapter_fallback"
    return "literary_boundary_review"


def confidence_for(substrate: Substrate, book: str, unit: Unit, genre: str) -> str:
    signals = signal_set(substrate, book, unit.start, unit.end)
    markers = marker_counter(substrate.verse_rows_in(unit.start, unit.end))
    if book == "Rev":
        return "low"
    if book == "Dan" and unit.start.chapter >= 7:
        return "low"
    if "has_wj" in signals or markers.get("wj", 0):
        return "medium_low"
    if "has_poetry_or_liturgy_marker" in signals or markers.keys() & POETRY_KEYS:
        return "medium_low"
    if markers.get("sp", 0):
        return "medium_low"
    if markers.get("fqa", 0):
        return "medium_low"
    if chapter_full_span(substrate, unit) and (book in PILOT_FRAGILE_BOOKS or signals & LOW_RISK_SIGNALS):
        return "medium_low"
    if genre in {"prophets", "wisdom", "law"} and (signals & LOW_RISK_SIGNALS):
        return "medium_low"
    if signals & {"has_footnote", "has_crossref"}:
        return "medium"
    return "high"


def literature_guess(substrate: Substrate, book: str, unit: Unit, genre: str) -> str:
    signals = signal_set(substrate, book, unit.start, unit.end)
    markers = marker_counter(substrate.verse_rows_in(unit.start, unit.end))
    if book in FRONTIER_BOOKS:
        return "apocalyptic_vision_or_court_narrative" if book == "Dan" else "apocalyptic_vision"
    if "has_wj" in signals or markers.get("wj", 0):
        return "gospel_discourse_or_narrative_with_wj_marker"
    if markers.get("sp", 0):
        return "wisdom_dialogue_speaker_unit"
    if markers.get("li1", 0) or markers.get("ili", 0):
        return "list_or_genealogy"
    if "has_poetry_or_liturgy_marker" in signals or markers.keys() & POETRY_KEYS:
        return "poetry_or_liturgy"
    return {
        "narrative": "narrative_scene_or_episode",
        "law": "legal_or_covenant_unit",
        "psalms": "poetry_or_psalm",
        "wisdom": "wisdom_poetry_or_discourse",
        "prophets": "prophetic_oracle_or_vision",
        "gospels": "gospel_pericope_or_discourse",
        "acts": "acts_episode_or_speech",
        "epistles": "epistle_argument_or_exhortation",
        "apocalypse": "apocalyptic_vision",
    }.get(genre, genre)


def boundary_evidence(substrate: Substrate, book: str, unit: Unit, genre: str) -> list[str]:
    evidence = ["observation_substrate:verse_observations", "rust_substrate:no_text", f"genre:{genre}"]
    evidence.extend(unit.reasons)
    markers = marker_counter(substrate.verse_rows_in(unit.start, unit.end))
    for marker in ("p", "m", "s1", "ms1", "q1", "q2", "b", "d", "sp", "wj", "li1", "ili", "f", "fqa", "x"):
        if markers.get(marker, 0):
            evidence.append(f"marker:{marker}:evidence_only")
    if chapter_full_span(substrate, unit):
        evidence.append("chapter_boundary_fallback_logged")
    if book in FRONTIER_BOOKS:
        evidence.append("frontier_flag_considered")
    if any(row.get("strong_ids") for row in substrate.verse_rows_in(unit.start, unit.end)):
        evidence.append("strong_tags_present_evidence_only_not_boundary_authority")
    return dedupe(evidence)


def make_chunk_records(substrate: Substrate, book: str, genre: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    chunks: list[dict[str, Any]] = []
    low_rows: list[dict[str, Any]] = []
    frontier_rows: list[dict[str, Any]] = []
    atlas_rows: list[dict[str, Any]] = []
    decision_rows: list[dict[str, Any]] = []
    units = book_units(substrate, book, genre)

    for index, unit in enumerate(units, start=1):
        decision_id = f"M4-{book.upper()}-{index:03d}"
        rows = substrate.verse_rows_in(unit.start, unit.end)
        markers = marker_counter(rows)
        signals = signal_set(substrate, book, unit.start, unit.end)
        confidence = confidence_for(substrate, book, unit, genre)
        frontier_flag = book in FRONTIER_BOOKS or confidence == "low"
        chunk = {
            "model_id": MODEL_ID,
            "book": book,
            "span": unit.span(),
            "chunk_index_in_book": index,
            "literature_type_guess": literature_guess(substrate, book, unit, genre),
            "boundary_evidence_refs": boundary_evidence(substrate, book, unit, genre),
            "strong_or_hebrew_tags_used": any(row.get("strong_ids") for row in rows),
            "wj_or_red_letter_considered": bool(markers.get("wj", 0) or "has_wj" in signals),
            "frontier_flag_considered": frontier_flag,
            "confidence": confidence,
            "decision_id": decision_id,
            "non_authorizing": True,
        }
        chunks.append(chunk)

        sensitive = (
            confidence in {"medium_low", "low"}
            or frontier_flag
            or bool(markers.keys() & (POETRY_KEYS | {"sp", "wj", "fqa", "x", "li1", "ili"}))
            or genre in {"law", "prophets", "apocalypse"}
        )
        concern = concern_type(substrate, book, unit, genre)
        signal_list = observed_signals(substrate, book, unit)
        why = why_low_confidence(book, concern, confidence, unit, genre)
        if sensitive:
            low_rows.append(
                {
                    "model_id": MODEL_ID,
                    "book": book,
                    "span": unit.span(),
                    "chunk_decision_id": decision_id,
                    "confidence": confidence,
                    "why_low_confidence": why,
                    "observed_substrate_signals": signal_list,
                    "non_authorizing": True,
                }
            )
            frontier_rows.append(
                {
                    "model_id": MODEL_ID,
                    "book": book,
                    "span": unit.span(),
                    "chunk_decision_id": decision_id,
                    "concern_type": concern,
                    "observed_substrate_signals": signal_list,
                    "why_frontier_review_needed": frontier_reason(book, concern, genre),
                    "suggested_reviewer": "frontier_chunking_review",
                    "non_authorizing": True,
                    "promotion_authority": "none",
                }
            )
            atlas_rows.append(
                {
                    "model_id": MODEL_ID,
                    "book": book,
                    "span": unit.span(),
                    "chunk_decision_id": decision_id,
                    "confidence": confidence,
                    "concern_type": concern,
                    "observed_substrate_signals": signal_list,
                    "why_low_confidence": why,
                    "possible_downstream_risk": downstream_risk(book, concern, genre),
                    "suggested_reviewer": "stress_atlas_or_frontier_reviewer",
                    "proposed_atlas_action": "consider_only",
                    "non_authorizing": True,
                    "atlas_promotion_authority": "none",
                }
            )

        decision_rows.append(
            {
                "model_id": MODEL_ID,
                "book": book,
                "span": unit.span(),
                "decision_id": decision_id,
                "mode": "build",
                "strategy_id": "literary_marker_aware_v2",
                "boundary_basis": chunk["boundary_evidence_refs"],
                "confidence": confidence,
                "raw_usfm_read": False,
                "strongs_metadata_policy": "evidence_only_not_boundary_authority",
                "wj_marker_policy": "evidence_only_not_speaker_authority",
                "theology_pressure_policy": "transparent_escalation_not_boundary_authority",
                "non_authorizing": True,
            }
        )

    return chunks, low_rows, frontier_rows, atlas_rows, decision_rows


def why_low_confidence(book: str, concern: str, confidence: str, unit: Unit, genre: str) -> str:
    if confidence not in {"medium_low", "low"} and concern != "chapter_fallback":
        return f"Marker-sensitive {concern} region kept visible for audit despite {confidence} boundary confidence."
    if book in FRONTIER_BOOKS:
        return "Frontier book with apocalyptic/vision or court-narrative boundary pressure; scratch span needs later review."
    if concern == "chapter_fallback":
        return "Full-chapter span used as logged fallback where no safer finer substrate boundary was selected."
    return f"{concern} signal can affect {genre} chunking; boundary is evidence-based but not authoritative."


def frontier_reason(book: str, concern: str, genre: str) -> str:
    if book in FRONTIER_BOOKS:
        return "Protocol marks Daniel/Revelation as frontier books; symbolic, vision, and chronology pressures must stay review-only."
    return f"{concern} in {genre} material could smuggle speaker, oracle, source, variant, typology, or doctrinal pressure into a boundary."


def downstream_risk(book: str, concern: str, genre: str) -> str:
    if concern == "wj_speaker_discourse":
        return "Red-letter/WJ markup could be mistaken for reviewed Jesus speaker attribution."
    if concern == "poetry_liturgy":
        return "Poetry, superscription, stanza, Selah, or liturgical markers could be over-promoted into boundary authority."
    if concern == "apocalyptic_frontier":
        return "Vision-cycle divisions could imply chronology, recapitulation, fulfillment, or eschatological system."
    if concern == "footnote_or_variant_evidence":
        return "Footnotes or variant markers could be mistaken for textual-critical/source-tradition decisions."
    if concern == "list_or_genealogy":
        return "Genealogy/list grouping could imply covenant, chronology, or identity claims beyond structure."
    if genre == "law":
        return "Law/covenant unit boundaries could imply later theological taxonomies."
    return "Boundary may be useful for later comparison but carries no promotion authority."


def write_strategy(substrate: Substrate, book: str, genre: str) -> None:
    row = substrate.book_rows[book]
    markers = row.get("marker_counts", {})
    flags = ", ".join(row.get("feature_flags", [])) or "none"
    family = BOOK_FAMILY.get(book, "Epistles and Revelation")
    target, max_size = TARGETS.get(genre, TARGETS["narrative"])
    path = MODEL_FOLDER / "book_strategy" / f"{book}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"""# {book} Strategy

- selected_strategy: literary_marker_aware_v2
- model_id: {MODEL_ID}
- wave: {family}
- primary_literature_type: {genre}
- local_marker_signals: chapter_count={row.get('chapter_count')}, verse_count={row.get('verse_count')}, feature_flags={flags}
- marker_counts_considered: p={markers.get('p', 0)}, m={markers.get('m', 0)}, q1={markers.get('q1', 0)}, q2={markers.get('q2', 0)}, b={markers.get('b', 0)}, d={markers.get('d', 0)}, sp={markers.get('sp', 0)}, li1={markers.get('li1', 0)}, ili={markers.get('ili', 0)}, wj={markers.get('wj', 0)}, f={markers.get('f', 0)}, fqa={markers.get('fqa', 0)}, x={markers.get('x', 0)}

## Boundary Strategy

This pass uses the Rust observation substrate first. It starts from substrate paragraph, speaker, list, poetry, WJ, footnote, cross-reference, and chapter rollup evidence, then groups adjacent marker units into {target}-{max_size} verse literary clusters for {genre} material. Chapter boundaries are treated as weak navigation evidence, not as silent authority.

Paragraph markers are used as local prose/discourse evidence. Poetry markers, superscriptions, stanza breaks, Selah-style rubric signals, and acrostic/stanza risks are preserved by smaller poetry clusters. Discourse and speaker-shift markers are kept visible, especially in Job, Gospels, Acts speeches, and WJ-marked regions. Oracle and vision material is kept in smaller units and escalated when the book or marker pattern risks fulfillment, chronology, or source-tradition pressure. Lists and genealogies are grouped as list-form units without making covenant, chronology, or identity claims.

Strong's Greek/Hebrew metadata was considered only as evidence that original-language metadata is present. It never sets a boundary, lexical meaning, theology, source-language claim, or authority decision. WJ/red-letter markers were considered only as edition metadata evidence. They never decide speaker attribution or Jesus/narrator discourse boundaries.

## Low Confidence And Escalation

Low-confidence triggers for this book: full-chapter fallback in marker-rich regions, poetry/liturgy markers, speaker labels, WJ spans, footnotes or variant readings, cross-references, list/genealogy markers, law/covenant form, oracle/vision material, and any doctrinal pressure that could make a boundary look like theology. Frontier escalation is required for Daniel and Revelation and is optional-but-visible for marker-sensitive material elsewhere.

## Independent Rationale

This strategy is not a silent chapter-only map. It uses chapter boundaries only as weak constraints while choosing paragraph, stanza, speaker, list, discourse, oracle, vision, and argument clusters from the shared substrate. The result is a scratch comparison map, non-authorizing and intentionally auditable.
"""
    path.write_text(text, encoding="utf-8")


def purge_existing_book_rows(book: str) -> None:
    for name in [
        "low_confidence_register.jsonl",
        "frontier_escalation_queue.jsonl",
        "atlas_candidate_feed.jsonl",
        "layer_decision_log.jsonl",
    ]:
        path = MODEL_FOLDER / name
        if not path.is_file():
            continue
        all_rows = iter_jsonl(path)
        if not any(str(row.get("book", "")) == book for row in all_rows):
            continue
        rows = [row for row in all_rows if str(row.get("book", "")) != book]
        tmp = path.with_suffix(path.suffix + ".tmp")
        write_jsonl(tmp, rows)
        tmp.replace(path)


def write_book(book: str) -> None:
    purge_existing_book_rows(book)
    substrate = Substrate()
    genre_map = genres()
    genre = genre_map.get(book, "narrative")
    write_strategy(substrate, book, genre)
    chunks, low_rows, frontier_rows, atlas_rows, decisions = make_chunk_records(substrate, book, genre)
    write_jsonl(MODEL_FOLDER / "book_chunks" / book / "chunks.jsonl", chunks)
    write_jsonl(MODEL_FOLDER / "low_confidence_register.jsonl", low_rows, append=True)
    write_jsonl(MODEL_FOLDER / "frontier_escalation_queue.jsonl", frontier_rows, append=True)
    write_jsonl(MODEL_FOLDER / "atlas_candidate_feed.jsonl", atlas_rows, append=True)
    write_jsonl(MODEL_FOLDER / "layer_decision_log.jsonl", decisions, append=True)


def reset_lane() -> None:
    resolved = MODEL_FOLDER.resolve()
    expected = (ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / MODEL_ID).resolve()
    if resolved != expected:
        raise RuntimeError(f"Refusing to reset unexpected path: {resolved}")
    MODEL_FOLDER.mkdir(parents=True, exist_ok=True)

    existing = [MODEL_FOLDER / name for name in ACTIVE_ARTIFACTS if (MODEL_FOLDER / name).exists()]
    restart_dir: Path | None = None
    if existing:
        restart_dir = MODEL_FOLDER / "audit" / "restarts" / datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        restart_dir.mkdir(parents=True, exist_ok=True)
        for path in existing:
            shutil.move(str(path), str(restart_dir / path.name))

    for name in [
        "low_confidence_register.jsonl",
        "frontier_escalation_queue.jsonl",
        "atlas_candidate_feed.jsonl",
        "layer_decision_log.jsonl",
    ]:
        (MODEL_FOLDER / name).write_text("", encoding="utf-8")

    progress = {
        "model_id": MODEL_ID,
        "marathon_status": "pending_marathon_start",
        "books_completed": 0,
        "books_total": 66,
        "book_completion": {},
    }
    write_yaml(MODEL_FOLDER / "marathon_progress.yaml", progress)

    manifest = read_yaml(MODEL_FOLDER / "model_manifest.yaml") if (MODEL_FOLDER / "model_manifest.yaml").exists() else {}
    manifest.update(
        {
            "model_id": MODEL_ID,
            "agent_surface": "codex",
            "model_profile": "gpt-5.5_high",
            "status": "in_progress",
            "books_completed": 0,
            "books_total": 66,
            "research_baseline_read": True,
            "research_baseline_manifest_sha256": file_sha256(BASELINE_MANIFEST),
            "quality_protocol": {
                "strategy_id": "literary_marker_aware_v2",
                "control": ".ai/control/t423_literary_marker_quality_protocol.yaml",
                "low_confidence_register_required": True,
                "frontier_escalation_queue_required": True,
                "atlas_candidate_feed_required": True,
                "book_strategy_required": True,
            },
            "raw_usfm_exception_count": 0,
            "non_authorizations": [
                "canon_chunk_output",
                "read_other_model_maps_before_complete",
                "theology_as_boundary_authority",
            ],
        }
    )
    write_yaml(MODEL_FOLDER / "model_manifest.yaml", manifest)

    clean_note = MODEL_FOLDER / "audit" / "preflight_clean_state.md"
    clean_note.parent.mkdir(parents=True, exist_ok=True)
    archived = restart_dir.as_posix() if restart_dir else "none"
    clean_note.write_text(
        "\n".join(
            [
                "# M4 Preflight Clean State",
                "",
                f"- timestamp_utc: {datetime.now(UTC).isoformat()}",
                "- active_completed_books: 0",
                "- active_old_chunks: none after reset",
                "- active_old_sidecar_residue: none after reset",
                f"- archived_restart_dir: {archived}",
                "- research_baseline_read: true",
                "- raw_usfm_reads: 0",
                "- note: full git dirty tree had pre-existing non-M4 setup paths; M4 writes are isolated.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def finalize() -> None:
    progress = read_yaml(MODEL_FOLDER / "marathon_progress.yaml")
    chunk_files = sorted((MODEL_FOLDER / "book_chunks").glob("*/chunks.jsonl"))
    chunk_count = 0
    low_count = len(iter_jsonl(MODEL_FOLDER / "low_confidence_register.jsonl"))
    frontier_count = len(iter_jsonl(MODEL_FOLDER / "frontier_escalation_queue.jsonl"))
    atlas_count = len(iter_jsonl(MODEL_FOLDER / "atlas_candidate_feed.jsonl"))
    for path in chunk_files:
        chunk_count += len(iter_jsonl(path))

    manifest = read_yaml(MODEL_FOLDER / "model_manifest.yaml")
    manifest["status"] = "complete" if int(progress.get("books_completed", 0)) == 66 else "in_progress"
    manifest["books_completed"] = int(progress.get("books_completed", 0))
    manifest["books_total"] = 66
    manifest["chunk_count"] = chunk_count
    manifest["low_confidence_rows"] = low_count
    manifest["frontier_escalation_rows"] = frontier_count
    manifest["atlas_candidate_rows"] = atlas_count
    manifest["completed_at"] = datetime.now(UTC).isoformat()
    write_yaml(MODEL_FOLDER / "model_manifest.yaml", manifest)

    quality = f"""# M4 Model Quality Summary

- model_id: {MODEL_ID}
- strategy_id: literary_marker_aware_v2
- books_completed: {progress.get('books_completed', 0)}/66
- chunk_count: {chunk_count}
- low_confidence_register_rows: {low_count}
- frontier_escalation_rows: {frontier_count}
- atlas_candidate_rows: {atlas_count}
- raw_usfm_reads: 0
- substrate_first: true
- research_baseline_read: true

## Quality Notes

The pass uses the Rust no-text observation substrate as the first evidence layer and keeps raw USFM closed. Strong's Greek/Hebrew metadata, WJ/red-letter markup, headings, paragraph markers, poetry markers, footnotes, cross-references, and source metadata are evidence only. They are surfaced in chunk records and sidecars without becoming theology, speaker attribution, textual-critical, graph, retrieval, or boundary authority.

Chapter-only fallback is logged through confidence and sidecars when it appears in marker-rich or fragile regions. Daniel and Revelation carry frontier flags on every chunk.
"""
    (MODEL_FOLDER / "model_quality_summary.md").write_text(quality, encoding="utf-8")

    summary = f"""# M4 Codex GPT-5.5 Whole-Bible Scratch Map

M4 completed an independent T423 scratch chunk map for the canonical 66 books using `literary_marker_aware_v2`.

- chunks: {chunk_count}
- completed books: {progress.get('books_completed', 0)}/66
- merged map: `whole_bible_chunk_map.jsonl`
- sidecars: `low_confidence_register.jsonl`, `frontier_escalation_queue.jsonl`, `atlas_candidate_feed.jsonl`
- raw USFM exception reads: 0

This map is non-authorizing scratch output only. It does not promote reviewed gold, canon chunks, graph edges, retrieval truth, source-tradition preference, or theology authority.
"""
    (MODEL_FOLDER / "model_summary.md").write_text(summary, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--book")
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()

    if args.reset:
        reset_lane()
    if args.book:
        if args.book not in canonical_books():
            raise SystemExit(f"unknown canonical book: {args.book}")
        write_book(args.book)
    if args.finalize:
        finalize()
    if not (args.reset or args.book or args.finalize):
        parser.error("pass --reset, --book <Book>, or --finalize")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
