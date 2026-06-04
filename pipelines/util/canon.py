"""Canon-profile helper — tradition-scoped book membership (CANON-1 / ADR-0005).

Authoritative source of truth for canon membership. Dependency-free and
deterministic so the importer can use it without extra packages.

`config/canon/canon_profiles.yaml` is a human-readable mirror of this module;
this Python module is authoritative (see ADR-0005).

Design principle (MASTER_CONTEXT §7): recording that a book belongs to a
tradition's canon is NOT a global canonical assertion. We record membership
*per tradition*; we assert nothing universally.

Statuses per tradition:
- "included"          — protocanonical in that tradition
- "deuterocanonical"  — second-canon, accepted as scripture in that tradition
- "appendix"          — printed in an appendix, not counted canonical
- "excluded"          — not part of that tradition's canon
"""
from __future__ import annotations

# 27 NT books (OSIS codes)
NT_BOOKS = {
    "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal",
    "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm",
    "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev",
}

# 39 protocanonical OT books (OSIS codes)
PROTOCANON_OT = {
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam",
    "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job",
    "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos",
    "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag",
    "Zech", "Mal",
}

TRADITIONS = ("protestant", "roman_catholic", "eastern_orthodox")

# Tradition-scoped membership for the deuterocanonical / additional books that
# appear in the WEB Classic archive (OSIS codes). Anything not protocanonical
# and not listed here defaults to "excluded" in every tradition.
DEUTERO_STATUS: dict[str, dict[str, str]] = {
    "Tob":     {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "Jdt":     {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "AddEsth": {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "Wis":     {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "Sir":     {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "Bar":     {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "1Macc":   {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "2Macc":   {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "AddDan":  {"protestant": "excluded", "roman_catholic": "deuterocanonical", "eastern_orthodox": "deuterocanonical"},
    "1Esd":    {"protestant": "excluded", "roman_catholic": "appendix", "eastern_orthodox": "deuterocanonical"},
    "PrMan":   {"protestant": "excluded", "roman_catholic": "appendix", "eastern_orthodox": "deuterocanonical"},
    "Ps151":   {"protestant": "excluded", "roman_catholic": "excluded", "eastern_orthodox": "deuterocanonical"},
    "3Macc":   {"protestant": "excluded", "roman_catholic": "excluded", "eastern_orthodox": "deuterocanonical"},
    "2Esd":    {"protestant": "excluded", "roman_catholic": "appendix", "eastern_orthodox": "appendix"},
    "4Macc":   {"protestant": "excluded", "roman_catholic": "excluded", "eastern_orthodox": "appendix"},
}


def testament(osis_book: str) -> str:
    """Return 'NT', 'OT', or 'unknown' for an OSIS book code.

    Deuterocanonical / OT-era additional books are classified 'OT'.
    """
    if osis_book in NT_BOOKS:
        return "NT"
    if osis_book in PROTOCANON_OT or osis_book in DEUTERO_STATUS:
        return "OT"
    return "unknown"


def canon_profiles(osis_book: str) -> dict[str, str]:
    """Return tradition -> membership status for an OSIS book code.

    Protocanonical OT + all NT are 'included' in every tradition.
    Deuterocanonical/additional books use DEUTERO_STATUS.
    Unknown books are 'excluded' everywhere (fail-safe; assert nothing).
    """
    if osis_book in PROTOCANON_OT or osis_book in NT_BOOKS:
        return {t: "included" for t in TRADITIONS}
    if osis_book in DEUTERO_STATUS:
        return dict(DEUTERO_STATUS[osis_book])
    return {t: "excluded" for t in TRADITIONS}


def is_deuterocanonical(osis_book: str) -> bool:
    """True if the book is outside the 66-book Protestant canon."""
    return osis_book in DEUTERO_STATUS
