#!/usr/bin/env python3
"""Read-only canonical corpus QA for generated 66-book outputs."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.util.canonical_scope import canonical_66_books, excluded_books, record_book_id  # noqa: E402


DEFAULT_CANONICAL_ROOT = ROOT / "data" / "canonical"
TRANSLATION_ROOT = Path("translations") / "eng-web"
PASSAGES_REL = Path("scripture") / "passages" / "passages.jsonl"
WITNESSES_REL = TRANSLATION_ROOT / "translation_witnesses.jsonl"
GLOSSARY_REL = TRANSLATION_ROOT / "glossary_entries.jsonl"
SIDECAR_RELS = (
    TRANSLATION_ROOT / "boundary_claims.jsonl",
    TRANSLATION_ROOT / "footnotes.jsonl",
    TRANSLATION_ROOT / "editorial_cross_references.jsonl",
    TRANSLATION_ROOT / "section_headings.jsonl",
)
WORD_TOKENS_REL = TRANSLATION_ROOT / "word_tokens.jsonl"
KNOWN_EMPTY_WITNESS_REFS = {
    # WEB preserves these verse addresses with empty witness text and textual-variant footnotes.
    "Luke.17.36",
    "Acts.8.37",
    "Acts.15.34",
    "Acts.24.7",
    "Rom.16.25",
}
NON_SCRIPTURE_GLOSSARY_SCOPES = {
    "non_scripture",
    "non_scripture_support",
    "supporting_reference",
    "source_metadata",
}


class CanonicalCorpusQAError(ValueError):
    """Raised when generated canonical outputs fail corpus-level QA."""


@dataclass(frozen=True)
class CanonicalCorpusQAReport:
    """Summary of read-only canonical corpus checks."""

    canonical_root: Path
    passage_count: int
    witness_count: int
    canonical_books: tuple[str, ...]
    sidecar_counts: dict[str, int] = field(default_factory=dict)
    word_token_count: int | None = None
    allowed_empty_witness_refs: tuple[str, ...] = ()


def iter_jsonl(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if line.strip():
                yield line_no, json.loads(line)


def require_file(path: Path, failures: list[str]) -> bool:
    if not path.exists():
        failures.append(f"missing required canonical output: {path}")
        return False
    return True


def is_non_scripture_glossary_record(record: Mapping[str, Any]) -> bool:
    if record.get("scripture_content") is False:
        return True
    if record.get("canonical_scripture") is False:
        return True
    for key in ("scope", "content_scope", "record_scope"):
        value = record.get(key)
        if isinstance(value, str) and value in NON_SCRIPTURE_GLOSSARY_SCOPES:
            return True
    return False


def validate_book_identity(
    record: Mapping[str, Any],
    *,
    source: str,
    line_no: int,
    expected_books: set[str],
    blocked_books: set[str],
    failures: list[str],
) -> str | None:
    book = record_book_id(record)
    record_id = record.get("id", "<missing-id>")
    if not book:
        failures.append(f"{source}:{line_no}: {record_id} is missing canonical book identity")
        return None
    if book in blocked_books or book not in expected_books:
        failures.append(f"{source}:{line_no}: {record_id} uses non-66 book {book}")
        return book
    return book


def _append_limited(failures: list[str], message: str, limit: int = 50) -> None:
    if len(failures) < limit:
        failures.append(message)
    elif len(failures) == limit:
        failures.append("additional QA failures suppressed")


def run_qa(
    canonical_root: Path = DEFAULT_CANONICAL_ROOT,
    *,
    expected_books: tuple[str, ...] | None = None,
    blocked_books: set[str] | None = None,
    include_word_tokens: bool = True,
) -> CanonicalCorpusQAReport:
    """Validate existing generated canonical outputs without writing or regenerating files."""
    expected_books = expected_books or canonical_66_books()
    expected_book_set = set(expected_books)
    blocked_book_set = blocked_books or set(excluded_books())
    failures: list[str] = []

    passages_path = canonical_root / PASSAGES_REL
    witnesses_path = canonical_root / WITNESSES_REL
    required_paths = [passages_path, witnesses_path, canonical_root / GLOSSARY_REL]
    required_paths.extend(canonical_root / rel for rel in SIDECAR_RELS)
    if include_word_tokens:
        required_paths.append(canonical_root / WORD_TOKENS_REL)
    for path in required_paths:
        require_file(path, failures)
    if failures:
        raise CanonicalCorpusQAError("\n".join(failures))

    passage_ids: set[str] = set()
    books_in_order: list[str] = []
    seen_books: set[str] = set()
    passage_count = 0
    for line_no, record in iter_jsonl(passages_path):
        source = str(passages_path)
        book = validate_book_identity(
            record,
            source=source,
            line_no=line_no,
            expected_books=expected_book_set,
            blocked_books=blocked_book_set,
            failures=failures,
        )
        if book and book not in seen_books:
            seen_books.add(book)
            books_in_order.append(book)
        passage_id = record.get("id")
        if not isinstance(passage_id, str) or not passage_id:
            _append_limited(failures, f"{source}:{line_no}: passage record is missing id")
        elif passage_id in passage_ids:
            _append_limited(failures, f"{source}:{line_no}: duplicate passage id {passage_id}")
        else:
            passage_ids.add(passage_id)
        if "text" in record and not str(record.get("text") or "").strip():
            _append_limited(failures, f"{source}:{line_no}: passage text field is empty")
        passage_count += 1

    if tuple(books_in_order) != expected_books:
        failures.append(
            "passage book order/set mismatch: "
            f"expected {list(expected_books)}, observed {books_in_order}"
        )

    witness_passage_ids: set[str] = set()
    allowed_empty_witness_refs: list[str] = []
    witness_count = 0
    for line_no, record in iter_jsonl(witnesses_path):
        source = str(witnesses_path)
        validate_book_identity(
            record,
            source=source,
            line_no=line_no,
            expected_books=expected_book_set,
            blocked_books=blocked_book_set,
            failures=failures,
        )
        passage_id = record.get("passage_id")
        if not isinstance(passage_id, str) or not passage_id:
            _append_limited(failures, f"{source}:{line_no}: witness is missing passage_id")
        elif passage_id in witness_passage_ids:
            _append_limited(failures, f"{source}:{line_no}: duplicate witness passage_id {passage_id}")
        else:
            witness_passage_ids.add(passage_id)
        if not str(record.get("text") or "").strip():
            osis_ref = record.get("osis_ref")
            if isinstance(osis_ref, str) and osis_ref in KNOWN_EMPTY_WITNESS_REFS:
                allowed_empty_witness_refs.append(osis_ref)
            else:
                _append_limited(failures, f"{source}:{line_no}: witness text is empty")
        witness_count += 1

    if witness_count != passage_count:
        failures.append(f"translation_witnesses count {witness_count} != passages count {passage_count}")
    missing_witnesses = sorted(passage_ids - witness_passage_ids)
    extra_witnesses = sorted(witness_passage_ids - passage_ids)
    if missing_witnesses:
        failures.append(f"translation_witnesses missing passage ids: {missing_witnesses[:10]}")
    if extra_witnesses:
        failures.append(f"translation_witnesses contain unknown passage ids: {extra_witnesses[:10]}")

    sidecar_counts: dict[str, int] = {}
    footnote_passage_ids: set[str] = set()
    for rel in SIDECAR_RELS:
        path = canonical_root / rel
        count = 0
        for line_no, record in iter_jsonl(path):
            source = str(path)
            validate_book_identity(
                record,
                source=source,
                line_no=line_no,
                expected_books=expected_book_set,
                blocked_books=blocked_book_set,
                failures=failures,
            )
            passage_id = record.get("passage_id")
            if passage_id and passage_id not in passage_ids:
                _append_limited(failures, f"{source}:{line_no}: unknown passage_id {passage_id}")
            if rel.name == "footnotes.jsonl" and isinstance(passage_id, str) and str(record.get("text") or "").strip():
                footnote_passage_ids.add(passage_id)
            count += 1
        sidecar_counts[str(rel)] = count

    for osis_ref in allowed_empty_witness_refs:
        passage_id = f"scripture:{osis_ref}"
        if passage_id not in footnote_passage_ids:
            failures.append(f"{passage_id} has allowed empty witness text but no explanatory footnote")

    glossary_path = canonical_root / GLOSSARY_REL
    glossary_count = 0
    for line_no, record in iter_jsonl(glossary_path):
        if not is_non_scripture_glossary_record(record):
            failures.append(
                f"{glossary_path}:{line_no}: glossary entry is not explicitly marked non-Scripture"
            )
        glossary_count += 1
    sidecar_counts[str(GLOSSARY_REL)] = glossary_count

    word_token_count: int | None = None
    if include_word_tokens:
        word_token_path = canonical_root / WORD_TOKENS_REL
        word_token_count = 0
        for line_no, record in iter_jsonl(word_token_path):
            source = str(word_token_path)
            validate_book_identity(
                record,
                source=source,
                line_no=line_no,
                expected_books=expected_book_set,
                blocked_books=blocked_book_set,
                failures=failures,
            )
            passage_id = record.get("passage_id")
            if passage_id and passage_id not in passage_ids:
                _append_limited(failures, f"{source}:{line_no}: unknown passage_id {passage_id}")
            word_token_count += 1

    if failures:
        raise CanonicalCorpusQAError("\n".join(failures))

    return CanonicalCorpusQAReport(
        canonical_root=canonical_root,
        passage_count=passage_count,
        witness_count=witness_count,
        canonical_books=tuple(books_in_order),
        sidecar_counts=sidecar_counts,
        word_token_count=word_token_count,
        allowed_empty_witness_refs=tuple(sorted(allowed_empty_witness_refs)),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--canonical-root",
        default=str(DEFAULT_CANONICAL_ROOT),
        help="Existing generated canonical output root to inspect. The script is read-only.",
    )
    parser.add_argument(
        "--skip-word-tokens",
        action="store_true",
        help="Skip streaming word_tokens QA. Other canonical outputs are still checked.",
    )
    args = parser.parse_args(argv)

    try:
        report = run_qa(Path(args.canonical_root), include_word_tokens=not args.skip_word_tokens)
    except CanonicalCorpusQAError as exc:
        print(f"Canonical corpus QA failed:\n{exc}", file=sys.stderr)
        return 1

    print("Canonical corpus QA passed.")
    print(f"- canonical root: {report.canonical_root}")
    print(f"- canonical books: {len(report.canonical_books)}")
    print(f"- passage records: {report.passage_count}")
    print(f"- translation witness records: {report.witness_count}")
    if report.allowed_empty_witness_refs:
        print(f"- allowed empty textual-variant witnesses: {len(report.allowed_empty_witness_refs)}")
        for osis_ref in report.allowed_empty_witness_refs:
            print(f"  - {osis_ref}")
    for rel, count in sorted(report.sidecar_counts.items()):
        print(f"- {rel}: {count}")
    if report.word_token_count is not None:
        print(f"- {WORD_TOKENS_REL}: {report.word_token_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
