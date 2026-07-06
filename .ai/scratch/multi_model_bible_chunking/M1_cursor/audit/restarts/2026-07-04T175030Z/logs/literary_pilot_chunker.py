#!/usr/bin/env python3
"""T423 M1_cursor pilot chunker — literary_marker_aware_v2 (scratch, non-authorizing)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import load_yaml

MODEL_ID = "M1_cursor"
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M1_cursor"
VO = ROOT / "build/observation_substrate/current/verse_observations.jsonl"
SPAN_FEAT = ROOT / "build/observation_substrate/current/span_observation_features.jsonl"
GENRES = ROOT / "config/chunking/book_genres.yaml"

PILOT = {"Gen", "Ps", "Phlm", "Jonah", "Rev"}
FRONTIER = {"Dan", "Rev"}
MARKER_RICH = {"q", "q1", "q2", "q3", "qr", "qc", "qs", "d", "b"}
POETRY_BOOKS = {"Ps", "Song", "Lam"}

BOOK_PROFILE: dict[str, dict[str, Any]] = {
    "Gen": {"base_lit": "narrative", "split_p": True, "split_chapter": True},
    "Ps": {"base_lit": "psalm", "psalm_unit": True, "acrostic_119": True},
    "Phlm": {"base_lit": "epistle", "split_p": True, "epistle_sections": True},
    "Jonah": {"base_lit": "narrative", "split_p": True, "split_chapter": True, "poetry_ch2": True},
    "Rev": {"base_lit": "apocalyptic", "split_p": True, "split_chapter": True},
}


def load_verses(book: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with VO.open(encoding="utf-8") as handle:
        for line in handle:
            r = json.loads(line)
            if r.get("book_id") == book:
                rows.append(r)
    rows.sort(key=lambda r: (r["chapter"], r["verse"]))
    return rows


def span_str(book: str, start: dict, end: dict) -> str:
    s = f"{book}.{start['chapter']}.{start['verse']}"
    e = f"{book}.{end['chapter']}.{end['verse']}"
    return s if s == e else f"{s}-{e}"


def has_marker(mc: dict, key: str) -> bool:
    return int(mc.get(key, 0) or 0) > 0


def marker_rich_verse(r: dict) -> bool:
    mc = r.get("marker_counts") or {}
    if any(has_marker(mc, k) for k in MARKER_RICH):
        return True
    flags = r.get("feature_flags") or []
    return "has_poetry_or_liturgy_marker" in flags


def strong_used(chunk_verses: list[dict]) -> bool:
    for r in chunk_verses:
        if r.get("strong_ids"):
            return True
        mc = r.get("marker_counts") or {}
        if has_marker(mc, "wh") or has_marker(mc, "wg"):
            return True
    return False


def guess_lit(book: str, verses: list[dict], profile: dict) -> str:
    if book == "Phlm" and profile.get("epistle_sections"):
        v = verses[0]["verse"]
        if v <= 3:
            return "epistle_greeting"
        if v <= 7:
            return "epistle_thanksgiving"
        if v <= 20:
            return "epistle_body"
        return "epistle_closing"
    if book == "Jonah" and verses[0]["chapter"] == 2:
        return "hymn"
    q_count = sum(1 for r in verses if marker_rich_verse(r))
    if q_count >= max(1, len(verses) // 2):
        if book == "Ps":
            return "psalm"
        return "poetry"
    if book == "Rev":
        return "apocalyptic_scene"
    return str(profile.get("base_lit", "narrative"))


def split_points(book: str, verses: list[dict], profile: dict) -> list[int]:
    """Return verse indices (0-based) where a new chunk starts."""
    starts = [0]
    if book == "Ps" and profile.get("acrostic_119"):
        for i, r in enumerate(verses):
            if r["chapter"] == 119 and r["verse"] in {1, 9, 17, 25, 33, 41, 49, 57, 65, 73, 81, 89, 97, 105, 113, 121, 129, 137, 145, 153, 161, 169}:
                if i not in starts:
                    starts.append(i)
        return sorted(set(starts))

    for i, r in enumerate(verses):
        if i == 0:
            continue
        mc = r.get("marker_counts") or {}
        prev = verses[i - 1]
        split = False
        if profile.get("split_chapter") and r["chapter"] != prev["chapter"]:
            split = True
        elif profile.get("split_p") and has_marker(mc, "p"):
            split = True
        elif book == "Ps" and profile.get("psalm_unit") and r["chapter"] != prev["chapter"]:
            split = True
        elif book == "Jonah" and profile.get("poetry_ch2") and r["chapter"] == 2 and i > 0:
            if has_marker(mc, "q1") and r["verse"] in {2, 4, 7}:
                split = True
        if split:
            starts.append(i)
    return sorted(set(starts))


def build_chunks(book: str, verses: list[dict]) -> list[dict[str, Any]]:
    profile = BOOK_PROFILE[book]
    if not verses:
        raise SystemExit(f"no verses for {book}")

    if book == "Ps" and profile.get("psalm_unit"):
        by_ch: dict[int, list[dict]] = {}
        for r in verses:
            by_ch.setdefault(r["chapter"], []).append(r)
        all_chunks: list[dict] = []
        for ch in sorted(by_ch):
            ch_verses = by_ch[ch]
            if ch == 119:
                pts = split_points(book, ch_verses, profile)
            else:
                pts = [0]
            for si, start_i in enumerate(pts):
                end_i = pts[si + 1] - 1 if si + 1 < len(pts) else len(ch_verses) - 1
                all_chunks.append((ch_verses[start_i], ch_verses[end_i]))
        verse_pairs = all_chunks
    else:
        pts = split_points(book, verses, profile)
        verse_pairs = []
        for si, start_i in enumerate(pts):
            end_i = pts[si + 1] - 1 if si + 1 < len(pts) else len(verses) - 1
            verse_pairs.append((verses[start_i], verses[end_i]))

    prefix = f"M1-{book.upper()}"
    rows: list[dict] = []
    for idx, (start, end) in enumerate(verse_pairs, start=1):
        cv = [r for r in verses if (start["chapter"], start["verse"]) <= (r["chapter"], r["verse"]) <= (end["chapter"], end["verse"])]
        span = span_str(book, start, end)
        lit = guess_lit(book, cv, profile)
        mc_start = start.get("marker_counts") or {}
        evidence = [f"observation_substrate:{book}.{start['chapter']}.{start['verse']}"]
        if has_marker(mc_start, "p"):
            evidence.append("marker:paragraph_start")
        if any(marker_rich_verse(r) for r in cv):
            evidence.append("marker:poetry_or_liturgy_present_evidence_only")
        if book == "Ps" and start["chapter"] != end["chapter"]:
            evidence.append("literary_form:psalm_span")
        elif book == "Ps":
            evidence.append("literary_form:psalm_unit")
            if start["chapter"] == 119:
                evidence.append("literary_form:acrostic_stanza")
        if book == "Phlm":
            evidence.append(f"literary_form:{lit}")

        marker_rich = any(marker_rich_verse(r) for r in cv)
        single_chapter = start["chapter"] == end["chapter"]
        is_whole_psalm = book == "Ps" and single_chapter and start["chapter"] != 119

        if book in FRONTIER:
            conf = "medium_low" if marker_rich else "medium"
        elif is_whole_psalm:
            conf = "medium_low" if marker_rich else "medium"
        elif marker_rich and lit in {"poetry", "psalm", "hymn", "apocalyptic_scene"}:
            conf = "medium"
        elif marker_rich:
            conf = "medium_low"
        else:
            conf = "high" if len(cv) <= 40 else "medium"

        rows.append(
            {
                "model_id": MODEL_ID,
                "book": book,
                "span": span,
                "chunk_index_in_book": idx,
                "literature_type_guess": lit,
                "boundary_evidence_refs": evidence,
                "strong_or_hebrew_tags_used": strong_used(cv),
                "wj_or_red_letter_considered": False,
                "frontier_flag_considered": book in FRONTIER,
                "confidence": conf,
                "decision_id": f"{prefix}-{idx:03d}",
                "non_authorizing": True,
                "_verses": cv,
            }
        )
    return rows


def write_book_strategy(book: str, chunk_count: int) -> None:
    profile = BOOK_PROFILE[book]
    path = MODEL / "book_strategy" / f"{book}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {book} — book strategy (literary_marker_aware_v2)",
        "",
        "## selected_strategy",
        f"Independent scratch chunking for {book} using Rust observation substrate verse markers.",
        f"Produced {chunk_count} chunks. Strategy profile: {json.dumps({k: v for k, v in profile.items()})}.",
        "",
        "## literature_type_or_mixed_genre",
        f"Base genre: {profile.get('base_lit')}. Per-chunk literature_type_guess assigned from markers and epistle/psalm heuristics.",
        "",
        "## substrate_markers_considered",
        "Verse-level marker_counts: p (paragraph), q1/q2 (poetry stanzas), d (superscription/doxology evidence), f/fr/ft (footnotes evidence-only).",
        "Chapter rollups used for coverage checks only, not as silent boundary authority.",
        "",
        "## strongs_metadata_considered_evidence_only",
        "strong_ids and wh/wg marker counts inform strong_or_hebrew_tags_used only; never boundary authority.",
        "",
        "## independent_boundary_rationale",
        "Boundaries chosen from paragraph and pericope signals visible in substrate without copying other models or template example spans.",
        "",
        "## chapter_only_fallback_reason_if_used",
    ]
    if book == "Ps":
        lines.append(
            "Non-Ps119 psalms use one psalm-per-chapter spans with medium_low confidence where stanza markers exist "
            "but stanza-level splits would over-fragment; Ps119 split into 22 acrostic letter stanzas (8 verses each)."
        )
    else:
        lines.append(
            "No silent chapter-only fallback; paragraph (p) and chapter boundaries drive splits where substrate shows them."
        )
    lines.extend(
        [
            "",
            "## expected_low_confidence_regions",
            "Marker-rich poetry, embedded hymn (Jonah 2), epistle transitions (Phlm), apocalyptic scenes (Rev), mixed narrative-law (Gen).",
            "",
            "## frontier_or_atlas_candidate_expectations",
            "Rev: every chunk frontier_flag_considered; low/medium_low chunks feed all three sidecars.",
            "",
            "## non_authorizing",
            "Scratch compare input only. Not canon, gold, atlas promotion, or theology authority.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sidecar_rows(book: str, chunk: dict) -> tuple[dict, dict, dict]:
    did = chunk["decision_id"]
    span = chunk["span"]
    conf = chunk["confidence"]
    signals = [e for e in chunk["boundary_evidence_refs"] if e.startswith("marker:") or e.startswith("literary_form:")]
    why = f"Marker-rich or {conf} confidence chunk under literary_marker_aware_v2 for {book}."
    concern = chunk["literature_type_guess"]
    if book == "Rev":
        concern = "apocalyptic_scene"
    base = {
        "model_id": MODEL_ID,
        "book": book,
        "span": span,
        "chunk_decision_id": did,
        "observed_substrate_signals": signals or ["observation_substrate"],
        "non_authorizing": True,
    }
    low = {
        **base,
        "confidence": conf,
        "why_low_confidence": why,
    }
    frontier = {
        **base,
        "concern_type": concern,
        "why_frontier_review_needed": f"Pilot/marker-sensitive region in {book}; independent model judgment requires review.",
        "suggested_reviewer": "codex_integrator",
        "promotion_authority": "none",
    }
    atlas = {
        **base,
        "confidence": conf,
        "concern_type": concern,
        "why_low_confidence": why,
        "possible_downstream_risk": "Boundary disagreement likely in multi-model compare; stress-atlas consideration only.",
        "suggested_reviewer": "codex_integrator",
        "proposed_atlas_action": "consider_only",
        "atlas_promotion_authority": "none",
    }
    return low, frontier, atlas


def is_whole_chapter_span(book: str, start: dict, end: dict, verses_in_book: list[dict]) -> bool:
    ch = start["chapter"]
    ch_verses = [r for r in verses_in_book if r["chapter"] == ch]
    if not ch_verses:
        return False
    return start == ch_verses[0] and end == ch_verses[-1]


def append_sidecars(book: str, chunks: list[dict], all_verses: list[dict]) -> tuple[int, int, int]:
    low_p = MODEL / "low_confidence_register.jsonl"
    fr_p = MODEL / "frontier_escalation_queue.jsonl"
    at_p = MODEL / "atlas_candidate_feed.jsonl"
    lc = 0
    low_conf = {"low", "medium_low"}
    with low_p.open("a", encoding="utf-8") as lf, fr_p.open("a", encoding="utf-8") as ff, at_p.open("a", encoding="utf-8") as af:
        for chunk in chunks:
            cv = chunk.get("_verses", [])
            start = cv[0] if cv else None
            end = cv[-1] if cv else None
            whole_ch = bool(start and end and is_whole_chapter_span(book, start, end, all_verses))
            marker_rich = any(marker_rich_verse(r) for r in cv)
            fragile = whole_ch and (marker_rich or book in PILOT)
            need = chunk["confidence"] in low_conf or fragile or book in FRONTIER
            if not need:
                continue
            low, frontier, atlas = sidecar_rows(book, chunk)
            lf.write(json.dumps(low) + "\n")
            ff.write(json.dumps(frontier) + "\n")
            af.write(json.dumps(atlas) + "\n")
            lc += 1
    return lc, lc, lc


def write_chunks(book: str, chunks: list[dict]) -> Path:
    out = MODEL / "book_chunks" / book / "chunks.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for row in chunks:
            clean = {k: v for k, v in row.items() if not k.startswith("_")}
            handle.write(json.dumps(clean) + "\n")
    return out


def process_book(book: str) -> None:
    verses = load_verses(book)
    chunks = build_chunks(book, verses)
    write_book_strategy(book, len(chunks))
    path = write_chunks(book, chunks)
    lc, fc, ac = append_sidecars(book, chunks, verses)
    print(f"OK {book}: {len(chunks)} chunks -> {path.relative_to(ROOT)} | sidecars +{lc}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("book")
    args = parser.parse_args()
    if args.book not in PILOT:
        print(f"ERROR: {args.book} not in pilot set", file=sys.stderr)
        return 1
    process_book(args.book)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
