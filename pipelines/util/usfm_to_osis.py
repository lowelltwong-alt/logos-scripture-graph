"""USFM book-code and reference helpers for deterministic WEB ingestion."""
from __future__ import annotations

import re

USFM_TO_OSIS = {
    "GEN": "Gen",
    "EXO": "Exod",
    "LEV": "Lev",
    "NUM": "Num",
    "DEU": "Deut",
    "JOS": "Josh",
    "JDG": "Judg",
    "RUT": "Ruth",
    "1SA": "1Sam",
    "2SA": "2Sam",
    "1KI": "1Kgs",
    "2KI": "2Kgs",
    "1CH": "1Chr",
    "2CH": "2Chr",
    "EZR": "Ezra",
    "NEH": "Neh",
    "EST": "Esth",
    "JOB": "Job",
    "PSA": "Ps",
    "PRO": "Prov",
    "ECC": "Eccl",
    "SNG": "Song",
    "ISA": "Isa",
    "JER": "Jer",
    "LAM": "Lam",
    "EZK": "Ezek",
    "DAN": "Dan",
    "HOS": "Hos",
    "JOL": "Joel",
    "AMO": "Amos",
    "OBA": "Obad",
    "JON": "Jonah",
    "MIC": "Mic",
    "NAM": "Nah",
    "HAB": "Hab",
    "ZEP": "Zeph",
    "HAG": "Hag",
    "ZEC": "Zech",
    "MAL": "Mal",
    "TOB": "Tob",
    "JDT": "Jdt",
    "ESG": "AddEsth",
    "WIS": "Wis",
    "SIR": "Sir",
    "BAR": "Bar",
    "1MA": "1Macc",
    "2MA": "2Macc",
    "1ES": "1Esd",
    "MAN": "PrMan",
    "PS2": "Ps151",
    "3MA": "3Macc",
    "2ES": "2Esd",
    "4MA": "4Macc",
    "DAG": "AddDan",
    "MAT": "Matt",
    "MRK": "Mark",
    "LUK": "Luke",
    "JHN": "John",
    "ACT": "Acts",
    "ROM": "Rom",
    "1CO": "1Cor",
    "2CO": "2Cor",
    "GAL": "Gal",
    "EPH": "Eph",
    "PHP": "Phil",
    "COL": "Col",
    "1TH": "1Thess",
    "2TH": "2Thess",
    "1TI": "1Tim",
    "2TI": "2Tim",
    "TIT": "Titus",
    "PHM": "Phlm",
    "HEB": "Heb",
    "JAS": "Jas",
    "1PE": "1Pet",
    "2PE": "2Pet",
    "1JN": "1John",
    "2JN": "2John",
    "3JN": "3John",
    "JUD": "Jude",
    "REV": "Rev",
}

OSIS_TO_USFM = {osis: usfm for usfm, osis in USFM_TO_OSIS.items()}

BOOK_ALIASES = {
    "genesis": "Gen",
    "exodus": "Exod",
    "leviticus": "Lev",
    "numbers": "Num",
    "deuteronomy": "Deut",
    "joshua": "Josh",
    "judges": "Judg",
    "ruth": "Ruth",
    "1 samuel": "1Sam",
    "2 samuel": "2Sam",
    "1 kings": "1Kgs",
    "2 kings": "2Kgs",
    "1 chronicles": "1Chr",
    "2 chronicles": "2Chr",
    "ezra": "Ezra",
    "nehemiah": "Neh",
    "esther": "Esth",
    "job": "Job",
    "psalm": "Ps",
    "psalms": "Ps",
    "proverbs": "Prov",
    "ecclesiastes": "Eccl",
    "song of solomon": "Song",
    "song": "Song",
    "isaiah": "Isa",
    "jeremiah": "Jer",
    "lamentations": "Lam",
    "ezekiel": "Ezek",
    "daniel": "Dan",
    "hosea": "Hos",
    "joel": "Joel",
    "amos": "Amos",
    "obadiah": "Obad",
    "jonah": "Jonah",
    "micah": "Mic",
    "nahum": "Nah",
    "habakkuk": "Hab",
    "zephaniah": "Zeph",
    "haggai": "Hag",
    "zechariah": "Zech",
    "malachi": "Mal",
    "tobit": "Tob",
    "judith": "Jdt",
    "wisdom": "Wis",
    "sirach": "Sir",
    "baruch": "Bar",
    "1 maccabees": "1Macc",
    "2 maccabees": "2Macc",
    "1 esdras": "1Esd",
    "2 esdras": "2Esd",
    "3 maccabees": "3Macc",
    "4 maccabees": "4Macc",
    "matthew": "Matt",
    "mark": "Mark",
    "luke": "Luke",
    "john": "John",
    "acts": "Acts",
    "romans": "Rom",
    "1 corinthians": "1Cor",
    "2 corinthians": "2Cor",
    "galatians": "Gal",
    "ephesians": "Eph",
    "philippians": "Phil",
    "colossians": "Col",
    "1 thessalonians": "1Thess",
    "2 thessalonians": "2Thess",
    "1 timothy": "1Tim",
    "2 timothy": "2Tim",
    "titus": "Titus",
    "philemon": "Phlm",
    "hebrews": "Heb",
    "james": "Jas",
    "1 peter": "1Pet",
    "2 peter": "2Pet",
    "1 john": "1John",
    "2 john": "2John",
    "3 john": "3John",
    "jude": "Jude",
    "revelation": "Rev",
}

_BOOK_PATTERN = "|".join(
    re.escape(name) for name in sorted(BOOK_ALIASES, key=len, reverse=True)
)
REFERENCE_RE = re.compile(
    rf"\b(?P<book>{_BOOK_PATTERN})\s+(?P<chapter>\d+):(?P<verse>\d+)(?:-(?P<end>\d+))?",
    re.IGNORECASE,
)


def osis_book(usfm_code: str) -> str:
    """Return the OSIS book code for a USFM book code."""
    return USFM_TO_OSIS.get(usfm_code, usfm_code)


def osis_ref(usfm_code: str, chapter: int, verse: int) -> str:
    """Return an OSIS-style verse reference."""
    return f"{osis_book(usfm_code)}.{chapter}.{verse}"


def parse_unambiguous_refs(text: str) -> list[str]:
    """Parse explicit Book chapter:verse references from editorial crossref text.

    This deliberately ignores bare chapter:verse references because they depend on
    context and are ambiguous as standalone sidecar metadata.
    """
    refs: list[str] = []
    for match in REFERENCE_RE.finditer(text):
        book = BOOK_ALIASES[match.group("book").lower()]
        chapter = int(match.group("chapter"))
        verse = int(match.group("verse"))
        end = match.group("end")
        refs.append(f"{book}.{chapter}.{verse}")
        if end:
            refs[-1] = f"{refs[-1]}-{book}.{chapter}.{int(end)}"
    return refs
