"""Canonical 66-book allow-list and filtering helpers.

T327B adds the filter mechanism only. Existing generated outputs may still
contain non-66 records until T327C regeneration.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Any

from pipelines.util.usfm_to_osis import osis_book


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config" / "canon" / "canonical_66_books.yaml"


class CanonicalScopeError(ValueError):
    """Raised when a canonical-output record is outside the 66-book scope."""


def _load_scalar_list(config_path: Path, key: str) -> tuple[str, ...]:
    values: list[str] = []
    in_list = False
    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current_key = line[:-1].strip()
            if in_list and current_key != key:
                break
            in_list = current_key == key
            continue
        if in_list:
            stripped = line.strip()
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip('"').strip("'"))
            elif not line.startswith(" "):
                break
    if not values:
        raise CanonicalScopeError(f"No values found for {key} in {config_path}")
    return tuple(values)


@lru_cache(maxsize=1)
def canonical_66_books(config_path: Path = DEFAULT_CONFIG) -> tuple[str, ...]:
    """Return the configured canonical 66-book OSIS allow-list in order."""
    books = _load_scalar_list(config_path, "canonical_66_books")
    if len(books) != 66:
        raise CanonicalScopeError(f"Expected 66 canonical books, found {len(books)}")
    if len(set(books)) != 66:
        raise CanonicalScopeError("Canonical 66-book allow-list contains duplicates")
    return books


@lru_cache(maxsize=1)
def excluded_books(config_path: Path = DEFAULT_CONFIG) -> tuple[str, ...]:
    """Return explicitly excluded non-66/front/glossary OSIS identifiers."""
    return _load_scalar_list(config_path, "excluded_books")


def normalize_book_id(book_id: str | None) -> str | None:
    """Normalize a USFM, OSIS, or OSIS ref-like value to an OSIS book id."""
    if not book_id:
        return None
    first = str(book_id).split(".", 1)[0]
    return osis_book(first)


def is_canonical_66_book(book_id: str | None) -> bool:
    """Return true when the supplied USFM/OSIS book is in the 66-book allow-list."""
    normalized = normalize_book_id(book_id)
    return normalized in set(canonical_66_books())


def record_book_id(record: Mapping[str, Any]) -> str | None:
    """Extract a best-effort book id from a generated output record."""
    for key in ("book", "osis_book", "usfm_book", "osis_ref", "passage_id"):
        value = record.get(key)
        if not value:
            continue
        if key == "passage_id" and isinstance(value, str) and value.startswith("scripture:"):
            value = value.removeprefix("scripture:")
        normalized = normalize_book_id(str(value))
        if normalized:
            return normalized
    return None


def filter_to_canonical_66(records: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Return only records whose discovered book belongs to the 66-book allow-list."""
    return [record for record in records if is_canonical_66_book(record_book_id(record))]


def assert_records_are_canonical_66(records: Iterable[Mapping[str, Any]], source: str = "records") -> None:
    """Fail closed when canonical-output records are not classifiable as 66-book Scripture."""
    blocked = set(excluded_books())
    for index, record in enumerate(records, start=1):
        book = record_book_id(record)
        record_id = record.get("id", "<missing-id>")
        if book is None:
            raise CanonicalScopeError(
                f"{source}:{index}: {record_id} is missing canonical book identity"
            )
        if book in blocked or (book is not None and not is_canonical_66_book(book)):
            raise CanonicalScopeError(
                f"{source}:{index}: {record_id} uses non-66 canonical-scope book {book}"
            )
