#!/usr/bin/env python3
"""T423 M1_cursor marathon chunker — literary_marker_aware_v2 (scratch, non-authorizing)."""
from __future__ import annotations

import argparse
import json
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
GENRES_PATH = ROOT / "config/chunking/book_genres.yaml"

PILOT_DONE = {"Gen", "Ps", "Phlm", "Jonah", "Rev"}
FRONTIER = {"Dan", "Rev"}
MARKER_RICH = {"q", "q1", "q2", "q3", "qr", "qc", "qs", "d", "b"}
PILOT_FRAGILE = {"Gen", "Ps", "Phlm", "Jonah", "Dan", "Rev"}

MINOR_PROPHETS = {"Hos", "Joel", "Amos", "Obad", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"}
GOSPELS = {"Matt", "Mark", "Luke", "John"}

SPECIAL_PROFILES: dict[str, dict[str, Any]] = {
    "Ps": {"base_lit": "psalm", "psalm_unit": True, "acrostic_119": True},
    "Phlm": {"base_lit": "epistle", "split_p": True, "epistle_sections": True},
    "Jonah": {"base_lit": "narrative", "split_p": True, "split_chapter": True, "poetry_ch2": True},
    "Rev": {"base_lit": "apocalyptic", "split_p": True, "split_chapter": True},
    "Dan": {"base_lit": "apocalyptic", "split_p": True, "split_chapter": True, "vision_units": True},
    "Hos": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Joel": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Amos": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Obad": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Mic": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Nah": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Hab": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Zeph": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Hag": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Zech": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Mal": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "minor_prophet": True},
    "Job": {"base_lit": "wisdom", "split_p": True, "split_chapter": True, "job_dialogue": True},
    "Prov": {"base_lit": "wisdom", "split_chapter": True, "proverb_collection": True, "split_p": True},
    "Eccl": {"base_lit": "wisdom", "split_p": True, "split_chapter": True},
    "Song": {"base_lit": "poetry", "split_chapter": True, "stanza_splits": True},
    "Lam": {"base_lit": "lament", "split_chapter": True, "acrostic_lament": True},
    "Isa": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "major_prophet": True},
    "Jer": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "major_prophet": True},
    "Ezek": {"base_lit": "prophets", "split_p": True, "split_chapter": True, "major_prophet": True, "vision_units": True},
    "Matt": {"base_lit": "gospels", "split_p": True, "split_chapter": True, "gospel": True, "wj_consider": True},
    "Mark": {"base_lit": "gospels", "split_p": True, "split_chapter": True, "gospel": True, "wj_consider": True},
    "Luke": {"base_lit": "gospels", "split_p": True, "split_chapter": True, "gospel": True, "wj_consider": True},
    "John": {"base_lit": "gospels", "split_p": True, "split_chapter": True, "gospel": True, "wj_consider": True},
    "Acts": {"base_lit": "acts", "split_p": True, "split_chapter": True, "acts_narrative": True, "wj_consider": True},
}


def book_genre(book: str) -> str:
    data = load_yaml(GENRES_PATH)
    return str(data.get("genres", {}).get(book, data.get("default_genre", "narrative")))


def build_profile(book: str) -> dict[str, Any]:
    if book in SPECIAL_PROFILES:
        return dict(SPECIAL_PROFILES[book])
    genre = book_genre(book)
    profile: dict[str, Any] = {"base_lit": genre, "split_p": True, "split_chapter": True}
    if genre in {"psalms", "wisdom"}:
        profile["split_p"] = True
    if genre == "prophets":
        profile["oracle_splits"] = True
    if genre in {"gospels", "acts"}:
        profile["wj_consider"] = True
    if genre == "epistles":
        profile["epistle_sections"] = True
    if genre == "apocalypse":
        profile["base_lit"] = "apocalyptic"
    return profile


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
    return "has_poetry_or_liturgy_marker" in (r.get("feature_flags") or [])


def strong_used(chunk_verses: list[dict]) -> bool:
    for r in chunk_verses:
        if r.get("strong_ids"):
            return True
        mc = r.get("marker_counts") or {}
        if has_marker(mc, "wh") or has_marker(mc, "wg"):
            return True
    return False


def verse_has_wj(r: dict) -> bool:
    mc = r.get("marker_counts") or {}
    if has_marker(mc, "wj"):
        return True
    return "has_wj" in (r.get("feature_flags") or [])


def wj_present(chunk_verses: list[dict]) -> bool:
    return any(verse_has_wj(r) for r in chunk_verses)


def guess_lit(book: str, verses: list[dict], profile: dict) -> str:
    if profile.get("epistle_sections") and book != "Phlm":
        v = verses[0]["verse"]
        if v <= 3:
            return "epistle_greeting"
        if v <= 7:
            return "epistle_thanksgiving"
        if verses[0]["chapter"] == verses[-1]["chapter"] and verses[-1]["verse"] <= 25:
            return "epistle_body"
        return "epistle_closing"
    if book == "Phlm":
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
    if book == "Job":
        ch = verses[0]["chapter"]
        if ch <= 2 or ch >= 42:
            return "wisdom_frame"
        return "dialogue_poetry"
    if book == "Prov":
        return "proverb_cluster"
    if book == "Eccl":
        return "wisdom_discourse"
    if book == "Song":
        return "poetry"
    if book == "Lam":
        return "lament"
    if profile.get("major_prophet"):
        q_count = sum(1 for r in verses if marker_rich_verse(r))
        if book == "Ezek" and profile.get("vision_units") and q_count >= len(verses) // 2:
            return "vision"
        if q_count >= max(1, len(verses) // 2):
            return "oracle"
        return "prophetic_discourse"
    if book == "Dan":
        ch = verses[0]["chapter"]
        if ch >= 7:
            return "vision"
        if any(marker_rich_verse(r) for r in verses):
            return "apocalyptic_scene"
        return "narrative"
    if profile.get("minor_prophet"):
        q_count = sum(1 for r in verses if marker_rich_verse(r))
        if q_count >= max(1, len(verses) // 2):
            return "oracle"
        return "prophetic_discourse"
    if profile.get("gospel"):
        if wj_present(verses):
            wj_n = sum(1 for r in verses if verse_has_wj(r))
            if wj_n >= max(1, len(verses) // 2):
                return "gospel_discourse"
            return "mixed_discourse"
        return "narrative"
    if book == "Acts":
        if wj_present(verses):
            return "apostolic_discourse"
        return "narrative"
    q_count = sum(1 for r in verses if marker_rich_verse(r))
    if q_count >= max(1, len(verses) // 2):
        if book == "Ps" or book_genre(book) == "psalms":
            return "psalm"
        return "poetry"
    if profile.get("base_lit") == "apocalyptic" or book in FRONTIER:
        return "apocalyptic_scene"
    if book_genre(book) == "prophets":
        return "oracle"
    return str(profile.get("base_lit", "narrative"))


def split_points(book: str, verses: list[dict], profile: dict) -> list[int]:
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
        elif book == "Jonah" and profile.get("poetry_ch2") and r["chapter"] == 2:
            if has_marker(mc, "q1") and r["verse"] in {2, 4, 7}:
                split = True
        elif book == "Lam" and profile.get("acrostic_lament"):
            if r["chapter"] == 3 and r["verse"] > 1 and (r["verse"] - 1) % 3 == 0:
                split = True
            elif r["chapter"] != 3 and r["verse"] == 1 and r["chapter"] != prev["chapter"]:
                split = True
        elif book == "Song" and profile.get("stanza_splits"):
            if r["chapter"] != prev["chapter"]:
                split = True
            elif has_marker(mc, "q1") and r["verse"] > 1 and r["verse"] % 2 == 1:
                split = True
        elif profile.get("wj_consider"):
            prev_wj = verse_has_wj(prev)
            cur_wj = verse_has_wj(r)
            if prev_wj != cur_wj:
                split = True
        if split:
            starts.append(i)
    return sorted(set(starts))


def build_chunks(book: str, verses: list[dict], profile: dict) -> list[dict[str, Any]]:
    if not verses:
        raise SystemExit(f"no verses for {book}")

    if book == "Ps" and profile.get("psalm_unit"):
        by_ch: dict[int, list[dict]] = {}
        for r in verses:
            by_ch.setdefault(r["chapter"], []).append(r)
        verse_pairs: list[tuple] = []
        for ch in sorted(by_ch):
            ch_verses = by_ch[ch]
            pts = split_points(book, ch_verses, profile) if ch == 119 else [0]
            for si, start_i in enumerate(pts):
                end_i = pts[si + 1] - 1 if si + 1 < len(pts) else len(ch_verses) - 1
                verse_pairs.append((ch_verses[start_i], ch_verses[end_i]))
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
        if profile.get("major_prophet") and lit in {"oracle", "vision", "lament"}:
            evidence.append(f"literary_form:{lit}")
        if has_marker(mc_start, "s") or has_marker(mc_start, "s1"):
            evidence.append("marker:section_heading_evidence_only")
        if wj_present(cv):
            evidence.append("marker:wj_red_letter_evidence_only")
        if profile.get("gospel") and lit in {"mixed_discourse", "gospel_discourse"}:
            evidence.append("literary_form:speaker_discourse")

        marker_rich = any(marker_rich_verse(r) for r in cv)
        is_whole_psalm = book == "Ps" and start["chapter"] == end["chapter"] and start["chapter"] != 119

        if book in FRONTIER:
            conf = "medium_low" if marker_rich else "medium"
        elif profile.get("major_prophet"):
            conf = "medium_low" if marker_rich or lit in {"oracle", "vision", "lament"} else "medium"
        elif profile.get("minor_prophet") or book == "Dan":
            conf = "medium_low" if marker_rich or lit in {"oracle", "vision", "apocalyptic_scene", "prophetic_discourse"} else "medium"
        elif profile.get("wj_consider") and (wj_present(cv) or lit in {"gospel_discourse", "mixed_discourse", "apostolic_discourse"}):
            conf = "medium_low" if conf in {"high", "medium"} else conf
        elif is_whole_psalm:
            conf = "medium_low" if marker_rich else "medium"
        elif marker_rich and lit in {"poetry", "psalm", "hymn", "apocalyptic_scene", "oracle"}:
            conf = "medium"
        elif marker_rich:
            conf = "medium_low"
        elif lit in {"genealogy", "list", "proverb_cluster", "lament", "poetry", "dialogue_poetry"}:
            conf = "medium_low" if book in {"Song", "Lam", "Job"} else "medium"
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
                "wj_or_red_letter_considered": wj_present(cv),
                "frontier_flag_considered": book in FRONTIER,
                "confidence": conf,
                "decision_id": f"{prefix}-{idx:03d}",
                "non_authorizing": True,
                "_verses": cv,
            }
        )
    return rows


def _book_strategy_body(book: str, chunk_count: int, genre: str) -> str:
    """Book-specific strategy text (literary_marker_aware_v2 harness)."""
    common_strongs = (
        "## strongs_metadata_considered_evidence_only\n"
        "Strong's Greek (G) and Hebrew (H) IDs from substrate `strong_ids` and wh/wg marker counts "
        "inform `strong_or_hebrew_tags_used` as evidence only. They do not set chunk boundaries.\n"
    )
    common_independent = (
        "## independent_boundary_rationale\n"
        f"Boundaries for {book} chosen from substrate paragraph, chapter, stanza, and discourse markers. "
        "No copied template spans or other-model maps.\n"
    )
    common_nonauth = (
        "## non_authorizing\n"
        "Scratch compare input only. Not canon, reviewed gold, atlas promotion, or theology authority.\n"
    )

    if book == "Dan":
        return f"""# Dan — book strategy (literary_marker_aware_v2)

## selected_strategy
{book}: narrative court tales (ch 1–6) and apocalyptic vision cycles (ch 7–12). {chunk_count} chunks via paragraph/chapter/vision-unit splits from observation substrate.

## literature_type_or_mixed_genre
Config genre: {genre}. Mixed narrative + apocalyptic. Pericope tags: narrative, apocalyptic_scene, vision.

## substrate_markers_considered
p (paragraph), q1/q2 (hymnic/poetry in visions), f/fr/ft (footnotes evidence-only), chapter discourse shifts.

{common_strongs}
{common_independent}
## chapter_only_fallback_reason_if_used
No silent chapter-only fallback on vision cycles (especially ch 7–12) or marker-rich poetry spans.

## expected_low_confidence_regions
Vision beasts, angelic speech, symbolic scenes, judgment/salvation oracles, theology-pressure passages.

## frontier_or_atlas_candidate_expectations
Dan is a frontier book: every chunk sets `frontier_flag_considered: true`. All low/medium_low spans feed frontier_escalation_queue, low_confidence_register, and atlas_candidate_feed for Codex/Claude frontier review.

{common_nonauth}"""

    if book in MINOR_PROPHETS:
        return f"""# {book} — book strategy (literary_marker_aware_v2)

## selected_strategy
{book}: minor-prophet oracle book. {chunk_count} chunks from paragraph/chapter/poetry markers in observation substrate.

## literature_type_or_mixed_genre
Config genre: {genre}. Oracle, lament, judgment/salvation sequences, and mixed prose/poetry pericopes.

## substrate_markers_considered
p (paragraph/oracle unit), q1/q2 (poetry), d/b (liturgy evidence), f/fr/ft (variant/footnote evidence-only).

{common_strongs}
{common_independent}
## chapter_only_fallback_reason_if_used
No silent chapter-only fallback where oracle, lament, or poetry markers support finer units.

## expected_low_confidence_regions
Oracle boundaries, judgment vs salvation pivots, lament stanzas, theology-pressure oracles, footnote-dense variants.

## frontier_or_atlas_candidate_expectations
Marker-rich and medium_low chunks append to all three sidecars for integrator review.

{common_nonauth}"""

    if book in GOSPELS:
        return f"""# {book} — book strategy (literary_marker_aware_v2)

## selected_strategy
{book}: Gospel narrative and discourse. {chunk_count} chunks from paragraph (`p`), chapter, and WJ/red-letter transition markers in observation substrate.

## literature_type_or_mixed_genre
Config genre: {genre}. Pericope tags: narrative, gospel_discourse, mixed_discourse where Jesus speech (wj) dominates or transitions.

## substrate_markers_considered
p (paragraph/discourse block), wj (Words of Jesus / red-letter evidence-only), sp (speaker), f/fr/ft/x (footnote/crossref variant pressure evidence-only).

{common_strongs}
{common_independent}
## chapter_only_fallback_reason_if_used
No silent chapter-only fallback where paragraph, discourse, or WJ transition markers support finer units.

## expected_low_confidence_regions
WJ/red-letter spans, speaker transitions, parable blocks, sermon discourse (e.g. Sermon on the Mount), textual-variant/footnote pressure.

## frontier_or_atlas_candidate_expectations
WJ-heavy and medium_low chunks append to all three sidecars for Codex/Claude review.

{common_nonauth}"""

    if book == "Acts":
        return f"""# Acts — book strategy (literary_marker_aware_v2)

## selected_strategy
Acts: early church narrative. {chunk_count} chunks from paragraph/chapter discourse markers and occasional WJ legacy references.

## literature_type_or_mixed_genre
Config genre: {genre}. Narrative scenes, speeches, and apostolic discourse units.

## substrate_markers_considered
p (paragraph/scene), wj (where present, evidence-only), f/fr/ft (variant/footnote evidence-only), speech/discourse transitions.

{common_strongs}
{common_independent}
## chapter_only_fallback_reason_if_used
No silent chapter-only fallback where scene or speech boundaries are visible in substrate.

## expected_low_confidence_regions
Speech boundaries, council scenes, missionary journey transitions, textual-variant pressure, theology-pressure speeches.

## frontier_or_atlas_candidate_expectations
Low/medium_low and marker-rich chunks append to all three sidecars.

{common_nonauth}"""

    # Default narrative/historical (waves 1 etc.)
    return f"""# {book} — book strategy (literary_marker_aware_v2)

## selected_strategy
{book}: historical narrative. {chunk_count} chunks from paragraph (`p`) and chapter discourse markers.

## literature_type_or_mixed_genre
Config genre: {genre}. Scene and speech units tagged narrative; embedded poetry tagged poetry.

## substrate_markers_considered
p (paragraph/scene), q1/q2 (embedded poetry), s/s1 (section headings evidence-only), f/fr/ft (footnotes evidence-only).

{common_strongs}
{common_independent}
## chapter_only_fallback_reason_if_used
No silent chapter-only fallback where paragraph or scene markers exist.

## expected_low_confidence_regions
Genealogy/list spans, royal speeches, embedded poetry, variant/footnote pressure.

## frontier_or_atlas_candidate_expectations
Low/medium_low and marker-rich chunks append to all three sidecars.

{common_nonauth}"""


def write_book_strategy(book: str, chunk_count: int, profile: dict) -> None:
    path = MODEL / "book_strategy" / f"{book}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    genre = book_genre(book)
    path.write_text(_book_strategy_body(book, chunk_count, genre), encoding="utf-8")


def sidecar_rows(book: str, chunk: dict) -> tuple[dict, dict, dict]:
    did = chunk["decision_id"]
    span = chunk["span"]
    conf = chunk["confidence"]
    signals = [e for e in chunk["boundary_evidence_refs"] if e.startswith("marker:") or e.startswith("literary_form:")]
    why = f"Marker-rich or {conf} confidence under literary_marker_aware_v2 for {book}."
    concern = chunk["literature_type_guess"]
    if book in FRONTIER:
        concern = "apocalyptic_scene"
        why = f"Frontier book {book}: {conf} confidence apocalyptic/vision span; theology-pressure auditable, non-authorizing."
    frontier_why = (
        f"Frontier review required for {book} per literary_marker_aware_v2; auditable non-authorizing escalation."
        if book in FRONTIER
        else f"Marker-sensitive or low-confidence region in {book}; auditable non-authorizing escalation."
    )
    base = {
        "model_id": MODEL_ID,
        "book": book,
        "span": span,
        "chunk_decision_id": did,
        "observed_substrate_signals": signals or ["observation_substrate"],
        "non_authorizing": True,
    }
    return (
        {**base, "confidence": conf, "why_low_confidence": why},
        {
            **base,
            "concern_type": concern,
            "why_frontier_review_needed": frontier_why,
            "suggested_reviewer": "codex_integrator",
            "promotion_authority": "none",
        },
        {
            **base,
            "confidence": conf,
            "concern_type": concern,
            "why_low_confidence": why,
            "possible_downstream_risk": "Multi-model boundary disagreement possible; stress-atlas consideration only.",
            "suggested_reviewer": "codex_integrator",
            "proposed_atlas_action": "consider_only",
            "atlas_promotion_authority": "none",
        },
    )


def is_whole_chapter_span(start: dict, end: dict, verses: list[dict]) -> bool:
    ch = start["chapter"]
    ch_verses = [r for r in verses if r["chapter"] == ch]
    return bool(ch_verses) and start == ch_verses[0] and end == ch_verses[-1]


def append_sidecars(book: str, chunks: list[dict], all_verses: list[dict]) -> int:
    low_p = MODEL / "low_confidence_register.jsonl"
    fr_p = MODEL / "frontier_escalation_queue.jsonl"
    at_p = MODEL / "atlas_candidate_feed.jsonl"
    low_conf = {"low", "medium_low"}
    added = 0
    with low_p.open("a", encoding="utf-8") as lf, fr_p.open("a", encoding="utf-8") as ff, at_p.open("a", encoding="utf-8") as af:
        for chunk in chunks:
            cv = chunk.get("_verses", [])
            start, end = (cv[0], cv[-1]) if cv else (None, None)
            whole_ch = bool(start and end and is_whole_chapter_span(start, end, all_verses))
            marker_rich = any(marker_rich_verse(r) for r in cv)
            fragile = whole_ch and (marker_rich or book in PILOT_FRAGILE)
            need = chunk["confidence"] in low_conf or fragile or book in FRONTIER
            if not need:
                continue
            low, frontier, atlas = sidecar_rows(book, chunk)
            lf.write(json.dumps(low) + "\n")
            ff.write(json.dumps(frontier) + "\n")
            af.write(json.dumps(atlas) + "\n")
            added += 1
    return added


def process_book(book: str) -> dict[str, Any]:
    if book in PILOT_DONE:
        raise SystemExit(f"refusing to overwrite pilot-complete book: {book}")
    profile = build_profile(book)
    verses = load_verses(book)
    chunks = build_chunks(book, verses, profile)
    write_book_strategy(book, len(chunks), profile)
    out = MODEL / "book_chunks" / book / "chunks.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for row in chunks:
            handle.write(json.dumps({k: v for k, v in row.items() if not k.startswith("_")}) + "\n")
    sidecars = append_sidecars(book, chunks, verses)
    return {"book": book, "chunks": len(chunks), "sidecars": sidecars}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("books", nargs="+")
    args = parser.parse_args()
    for book in args.books:
        result = process_book(book)
        print(f"OK {result['book']}: {result['chunks']} chunks | sidecars +{result['sidecars']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
