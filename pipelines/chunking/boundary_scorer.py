#!/usr/bin/env python3
"""Boundary scoring helpers for Bible chunking.

Production implementation should load config/chunking/chunking_policy.yaml.
This file encodes the core policy logic in a small dependency-free form.
"""
from __future__ import annotations

DEFAULT_SCORES = {
    "book_boundary": 1.00,
    "source_text_boundary": 1.00,
    "license_boundary": 1.00,
    "usfm_major_section": 0.92,
    "usfm_section_heading": 0.88,
    "usfm_paragraph": 0.78,
    "whole_psalm": 0.95,
    "english_sentence": 0.86,
    "direct_speech_end": 0.84,
    "poetic_line": 0.88,
    "poetic_stanza": 0.90,
    "verse_boundary": 0.35,
    "token_budget": 0.20,
}

FORBIDDEN_SPLITS = {
    "english_sentence_midpoint",
    "psalm_superscription",
    "poetic_colon_midpoint",
    "direct_quotation_midpoint",
    "source_license_boundary",
}


def score_boundary(evidence_types: list[str]) -> float:
    """Return max boundary score from evidence type list."""
    if not evidence_types:
        return 0.0
    if any(e in FORBIDDEN_SPLITS for e in evidence_types):
        return -1.0
    return max(DEFAULT_SCORES.get(e, 0.0) for e in evidence_types)


def is_valid_split(evidence_types: list[str], threshold: float = 0.78) -> bool:
    return score_boundary(evidence_types) >= threshold
