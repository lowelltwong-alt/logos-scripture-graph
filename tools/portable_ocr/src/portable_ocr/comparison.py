"""Unicode-aware pairwise OCR comparison for arbitrary writing systems."""

from __future__ import annotations

import difflib
import itertools
import unicodedata
from typing import Any


IMPORTANT_PUNCTUATION = set(",.;:!?()[]{}'\"-/\\|\u00b7\u037e\u0387\u05be\u05c0\u05c3\u05f3\u05f4\u2013\u2014")


def _script(character: str) -> str | None:
    name = unicodedata.name(character, "")
    if "GREEK" in name:
        return "Greek"
    if "HEBREW" in name:
        return "Hebrew"
    return None


def _tokens(text: str) -> list[str]:
    """Tokenize by Unicode categories without assuming a Latin alphabet."""
    tokens: list[str] = []
    current = ""
    for char in unicodedata.normalize("NFC", text or ""):
        category = unicodedata.category(char)
        if category[0] in {"L", "N", "M"}:
            current += char
        else:
            if current:
                tokens.append(current)
                current = ""
            if not char.isspace():
                tokens.append(char)
    if current:
        tokens.append(current)
    return tokens


def _base_and_mark_clusters(text: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Preserve which base character owns each combining mark.

    This deliberately uses a bounded base-plus-combining-mark representation,
    not a full Unicode grapheme segmenter. It is sufficient to prevent an
    accent or niqqud mark moved to an adjacent base from disappearing into a
    document-wide bag of marks.
    """
    clusters: list[tuple[str, list[str]]] = []
    for char in unicodedata.normalize("NFD", text or ""):
        if unicodedata.combining(char) and clusters:
            clusters[-1][1].append(char)
        else:
            clusters.append((char, []))
    return tuple((base, tuple(marks)) for base, marks in clusters)


def compare_text(left: str, right: str) -> dict[str, Any]:
    left_nfc, right_nfc = unicodedata.normalize("NFC", left or ""), unicodedata.normalize("NFC", right or "")
    left_tokens, right_tokens = _tokens(left_nfc), _tokens(right_nfc)
    matcher = difflib.SequenceMatcher(a=left_tokens, b=right_tokens, autojunk=False)
    deltas = [
        {"operation": tag, "left": left_tokens[i1:i2], "right": right_tokens[j1:j2],
         "left_span": [i1, i2], "right_span": [j1, j2]}
        for tag, i1, i2, j1, j2 in matcher.get_opcodes() if tag != "equal"
    ]
    flags: set[str] = set()
    left_clusters = _base_and_mark_clusters(left_nfc)
    right_clusters = _base_and_mark_clusters(right_nfc)
    left_marks = tuple(marks for _, marks in left_clusters)
    right_marks = tuple(marks for _, marks in right_clusters)
    if left_marks != right_marks and ({_script(c) for c in left_nfc + right_nfc} & {"Greek", "Hebrew"}):
        flags.add("diacritic_disagreement")
    left_scripts = sorted({s for c in left_nfc if (s := _script(c))})
    right_scripts = sorted({s for c in right_nfc if (s := _script(c))})
    if left_scripts != right_scripts:
        flags.add("script_disagreement")
    left_punctuation = [t for t in left_tokens if t in IMPORTANT_PUNCTUATION]
    right_punctuation = [t for t in right_tokens if t in IMPORTANT_PUNCTUATION]
    if left_punctuation != right_punctuation:
        flags.add("punctuation_disagreement")
    if left_nfc.count("\n") != right_nfc.count("\n"):
        flags.add("layout_disagreement")
    if abs(len(left_tokens) - len(right_tokens)) >= 2:
        flags.add("missing_line_suspected")
    if deltas:
        flags.add("text_disagreement")
    ratio = difflib.SequenceMatcher(a=left_nfc, b=right_nfc, autojunk=False).ratio()
    return {
        "flags": sorted(flags) or ["none"], "delta_count": len(deltas),
        "character_disagreement_rate": round(1.0 - ratio, 6), "deltas": deltas,
        "scripts": {"left": left_scripts, "right": right_scripts},
        "unicode_normalization": "NFC", "agreement_is_truth": False,
    }


def compare_candidates(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if len(candidates) < 2:
        raise ValueError("at least two OCR candidates are required")
    pairwise = [
        {"left_candidate_id": left["candidate_id"], "right_candidate_id": right["candidate_id"],
         **compare_text(str(left.get("text") or ""), str(right.get("text") or ""))}
        for left, right in itertools.combinations(candidates, 2)
    ]
    return {
        "schema": "portable_ocr_comparison.v1", "candidate_count": len(candidates),
        "pairwise": pairwise, "all_candidates_agree": all(row["delta_count"] == 0 for row in pairwise),
        "winner": None, "automatic_truth_selection_allowed": False,
    }
