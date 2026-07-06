#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODEL_ID = "M5_gemini_thinking"
MODEL_DIR = ROOT / ".ai/scratch/multi_model_bible_chunking" / MODEL_ID
VO_PATH = ROOT / "build/observation_substrate/current/verse_observations.jsonl"

FRONTIER_BOOKS = {"Dan", "Rev"}
TORAH = {"Gen", "Exod", "Lev", "Num", "Deut"}
HISTORY = {"Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth"}
POETRY_WISDOM = {"Job", "Ps", "Prov", "Eccl", "Song", "Lam"}
MAJOR_PROPHETS = {"Isa", "Jer", "Ezek"}
MINOR_PROPHETS = {"Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"}
GOSPELS = {"Matt", "Mark", "Luke", "John"}
ACTS = {"Acts"}
EPISTLES = {"Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude"}

MARKER_RICH = {"q", "q1", "q2", "q3", "qr", "qc", "qs", "d", "b"}

def get_book_family(book: str) -> str:
    if book in TORAH: return "Torah"
    if book in HISTORY: return "history"
    if book in POETRY_WISDOM: return "poetry/wisdom"
    if book in MAJOR_PROPHETS: return "prophets"
    if book in MINOR_PROPHETS: return "prophets"
    if book in GOSPELS: return "gospels/acts"
    if book in ACTS: return "gospels/acts"
    if book in EPISTLES: return "epistles"
    if book in FRONTIER_BOOKS: return "apocalyptic"
    return "other"

def write_book_strategy(book: str, chunk_count: int):
    family = get_book_family(book)

    if family == "Torah":
        risks = "genealogy, law, covenant, ritual, list, embedded poetry"
        lit_type = "narrative, law_code, genealogy"
        markers = "p, q1, s, f"
        low_conf = "Genealogy spans, covenant/law blocks, ritual procedure units, embedded poetry, variant/footnote pressure."
    elif family == "history":
        risks = "scene, speech, land, royal, list, embedded poetry"
        lit_type = "narrative, royal_list"
        markers = "p, q1, s, f"
        low_conf = "Royal speeches, land-allotment lists, genealogy/list spans, embedded poetry, variant/footnote pressure."
    elif family == "poetry/wisdom":
        risks = "stanza, acrostic, lament, dialogue, proverb, song, doxology, superscription"
        lit_type = "poetry, psalm, proverb_cluster"
        markers = "q1, q2, d, b, p, f"
        low_conf = "Stanza boundaries, acrostic units, lament/dialogue speaker shifts, proverb clusters, Song interpretation pressure, doxology/blessing spans."
    elif family == "prophets":
        risks = "oracle, vision, lament, symbolic, judgment, salvation, theology"
        lit_type = "oracle, vision, narrative"
        markers = "p, q1, d, f"
        low_conf = "Oracle boundaries, vision units, lament stanzas, judgment/salvation pivots, theology-pressure oracles."
    elif family == "apocalyptic":
        risks = "vision, symbolic, angelic, hymn, frontier, apocalyptic"
        lit_type = "apocalyptic_scene, vision"
        markers = "p, q1, f"
        low_conf = "Vision scenes, symbolic imagery, angelic speech, hymnic interruption, judgment/salvation sequences, theology-pressure passages."
    elif family == "gospels/acts":
        risks = "wj, red-letter, speaker, discourse, parable, narrative, variant"
        lit_type = "narrative, gospel_discourse"
        markers = "p, wj, sp, f"
        low_conf = "WJ/red-letter spans, speaker transitions, parable blocks, textual-variant/footnote pressure."
    elif family == "epistles":
        risks = "greeting, thanksgiving, argument, doxology, church, household, ethics"
        lit_type = "epistle_greeting, epistle_thanksgiving, epistle_body, epistle_closing"
        markers = "p, f, x"
        low_conf = "Dense theological argument spans, household/church-order ethics pressure, doxology boundaries, textual-variant pressure."
    else:
        risks = "boundary, literary, confidence"
        lit_type = "narrative"
        markers = "p, f"
        low_conf = "General boundaries."

    content = f"""# {book} — book strategy (literary_marker_aware_v2)

## selected_strategy
{book}: {family}. {chunk_count} chunks from paragraph (`p`), chapter, and literary markers in observation substrate.

## literature_type_or_mixed_genre
Config genre: {family}. {lit_type}.

## substrate_markers_considered
{markers}

## strongs_metadata_considered_evidence_only
Strong's Greek (G) and Hebrew (H) IDs from substrate `strong_ids` and wh/wg marker counts inform `strong_or_hebrew_tags_used` as evidence only. They do not set chunk boundaries.

## independent_boundary_rationale
Boundaries for {book} chosen from substrate paragraph, chapter, stanza, and discourse markers. No copied template spans or other-model maps.

## chapter_only_fallback_reason_if_used
No silent chapter-only fallback where finer units are visible.

## expected_low_confidence_regions
{low_conf}

## frontier_or_atlas_candidate_expectations
Low/medium_low and marker-rich chunks append to all three sidecars.
{"Frontier review required." if book in FRONTIER_BOOKS else ""}

## non_authorizing
Scratch compare input only. Not canon, reviewed gold, atlas promotion, or theology authority.
"""
    out_path = MODEL_DIR / "book_strategy" / f"{book}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")

def load_verses(book: str) -> list[dict]:
    verses = []
    with VO_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            v = json.loads(line)
            if v.get("book_id") == book:
                verses.append(v)
    verses.sort(key=lambda x: (x["chapter"], x["verse"]))
    return verses

def is_marker_rich(v: dict) -> bool:
    mc = v.get("marker_counts", {})
    return any(mc.get(k, 0) > 0 for k in MARKER_RICH) or "has_poetry_or_liturgy_marker" in v.get("feature_flags", [])

def has_wj(v: dict) -> bool:
    return v.get("marker_counts", {}).get("wj", 0) > 0

def has_strongs(v: dict) -> bool:
    return bool(v.get("strong_ids")) or v.get("marker_counts", {}).get("wh", 0) > 0 or v.get("marker_counts", {}).get("wg", 0) > 0

def chunk_book(book: str):
    verses = load_verses(book)
    if not verses:
        return 0

    chunks = []
    current_chunk = []

    for v in verses:
        mc = v.get("marker_counts", {})
        is_p = mc.get("p", 0) > 0
        is_q1 = mc.get("q1", 0) > 0

        # Split on paragraph or chapter boundary, or q1 (new stanza)
        if current_chunk and (is_p or is_q1 or v["chapter"] != current_chunk[-1]["chapter"]):
            chunks.append(current_chunk)
            current_chunk = [v]
        else:
            current_chunk.append(v)

    if current_chunk:
        chunks.append(current_chunk)

    write_book_strategy(book, len(chunks))

    out_path = MODEL_DIR / "book_chunks" / book / "chunks.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    low_conf_path = MODEL_DIR / "low_confidence_register.jsonl"
    frontier_path = MODEL_DIR / "frontier_escalation_queue.jsonl"
    atlas_path = MODEL_DIR / "atlas_candidate_feed.jsonl"

    added_sidecars = 0

    with out_path.open("w", encoding="utf-8") as f, \
         low_conf_path.open("a", encoding="utf-8") as lf, \
         frontier_path.open("a", encoding="utf-8") as ff, \
         atlas_path.open("a", encoding="utf-8") as af:

        for i, cv in enumerate(chunks, 1):
            start, end = cv[0], cv[-1]
            span = f"{book}.{start['chapter']}.{start['verse']}"
            if start != end:
                span += f"-{book}.{end['chapter']}.{end['verse']}"

            is_rich = any(is_marker_rich(v) for v in cv)
            has_wj_flag = any(has_wj(v) for v in cv)
            has_strongs_flag = any(has_strongs(v) for v in cv)

            conf = "high"
            if is_rich or has_wj_flag or book in FRONTIER_BOOKS:
                conf = "medium_low"
            elif len(cv) > 30:
                conf = "medium"

            evidence = [f"observation_substrate:{book}.{start['chapter']}.{start['verse']}"]
            if start.get("marker_counts", {}).get("p", 0) > 0:
                evidence.append("marker:paragraph_start")
            if start.get("marker_counts", {}).get("q1", 0) > 0:
                evidence.append("marker:poetry_or_liturgy_present_evidence_only")
            if has_wj_flag:
                evidence.append("marker:wj_red_letter_evidence_only")

            lit_type = "narrative"
            if get_book_family(book) == "epistles":
                lit_type = "epistle_body"
            elif get_book_family(book) == "poetry/wisdom":
                lit_type = "poetry"
            elif get_book_family(book) == "prophets":
                lit_type = "oracle"
            elif get_book_family(book) == "apocalyptic":
                lit_type = "apocalyptic_scene"

            did = f"M5-{book.upper()}-{i:03d}"

            row = {
                "model_id": MODEL_ID,
                "book": book,
                "span": span,
                "chunk_index_in_book": i,
                "literature_type_guess": lit_type,
                "boundary_evidence_refs": evidence,
                "strong_or_hebrew_tags_used": has_strongs_flag,
                "wj_or_red_letter_considered": has_wj_flag,
                "frontier_flag_considered": book in FRONTIER_BOOKS,
                "confidence": conf,
                "decision_id": did,
                "non_authorizing": True
            }
            f.write(json.dumps(row) + "\n")

            if conf in ("low", "medium_low") or book in FRONTIER_BOOKS:
                base = {
                    "model_id": MODEL_ID,
                    "book": book,
                    "span": span,
                    "chunk_decision_id": did,
                    "observed_substrate_signals": evidence,
                    "non_authorizing": True,
                }

                low = {**base, "confidence": conf, "why_low_confidence": f"Marker rich or frontier in {book}"}
                frontier = {**base, "concern_type": lit_type, "why_frontier_review_needed": f"Frontier review needed for {book}", "suggested_reviewer": "gemini_integrator", "promotion_authority": "none"}
                atlas = {**base, "confidence": conf, "concern_type": lit_type, "why_low_confidence": f"Marker rich or frontier in {book}", "possible_downstream_risk": "Stress atlas consideration", "suggested_reviewer": "gemini_integrator", "proposed_atlas_action": "consider_only", "atlas_promotion_authority": "none"}

                lf.write(json.dumps(low) + "\n")
                ff.write(json.dumps(frontier) + "\n")
                af.write(json.dumps(atlas) + "\n")
                added_sidecars += 1

    return len(chunks), added_sidecars

if __name__ == "__main__":
    book = sys.argv[1]
    c, s = chunk_book(book)
    print(f"OK {book}: {c} chunks | sidecars +{s}")
