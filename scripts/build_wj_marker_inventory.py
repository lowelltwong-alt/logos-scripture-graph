#!/usr/bin/env python3
"""Build the words-of-Jesus marker inventory from canonical word tokens."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORD_TOKENS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "word_tokens.jsonl"
OBSERVED_STRESS = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "observed_stress_behavior.json"
OUTPUT = ROOT / ".ai" / "control" / "wj_marker_inventory.yaml"

CANONICAL_BOOK_ORDER = [
    "Gen",
    "Exod",
    "Lev",
    "Num",
    "Deut",
    "Josh",
    "Judg",
    "Ruth",
    "1Sam",
    "2Sam",
    "1Kgs",
    "2Kgs",
    "1Chr",
    "2Chr",
    "Ezra",
    "Neh",
    "Esth",
    "Job",
    "Ps",
    "Prov",
    "Eccl",
    "Song",
    "Isa",
    "Jer",
    "Lam",
    "Ezek",
    "Dan",
    "Hos",
    "Joel",
    "Amos",
    "Obad",
    "Jonah",
    "Mic",
    "Nah",
    "Hab",
    "Zeph",
    "Hag",
    "Zech",
    "Mal",
    "Matt",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Rom",
    "1Cor",
    "2Cor",
    "Gal",
    "Eph",
    "Phil",
    "Col",
    "1Thess",
    "2Thess",
    "1Tim",
    "2Tim",
    "Titus",
    "Phlm",
    "Heb",
    "Jas",
    "1Pet",
    "2Pet",
    "1John",
    "2John",
    "3John",
    "Jude",
    "Rev",
]
BOOK_INDEX = {book: index for index, book in enumerate(CANONICAL_BOOK_ORDER)}

KNOWN_WJ_CASE_IDS = {
    "gospels_wj_marker_spans",
    "john3_wj_speaker_boundary",
    "matt5_7_sermon_on_mount_wj_discourse",
    "john13_17_wj_farewell_discourse_marker_focus",
    "synoptic_apocalyptic_wj_discourses",
    "john7_53_8_11_wj_variant_speech",
}


def _book_sort_key(book: str) -> tuple[int, str]:
    return (BOOK_INDEX.get(book, 999), book)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _short_preview(words: list[str], *, limit: int = 28) -> str:
    preview = " ".join(words[:limit])
    if len(words) > limit:
        preview += " ..."
    return preview


def _finish_run(run: dict[str, Any], runs: list[dict[str, Any]]) -> None:
    words = run.pop("_words")
    refs = run.pop("_refs")
    contexts = run.pop("_contexts")
    run["verse_count"] = len(set(refs))
    run["first_refs"] = list(dict.fromkeys(refs))[:12]
    run["text_preview"] = _short_preview(words)
    run["nesting_contexts"] = [
        {"value": value, "count": count}
        for value, count in sorted(contexts.items(), key=lambda item: (-item[1], item[0]))
    ]
    runs.append(run)


def _known_review_cases() -> list[dict[str, Any]]:
    observed = _read_json(OBSERVED_STRESS)
    by_case = {
        entry["case_id"]: entry
        for entry in observed.get("entries", [])
        if entry.get("case_id") in KNOWN_WJ_CASE_IDS
    }
    cases = []
    for case_id in sorted(KNOWN_WJ_CASE_IDS):
        entry = by_case.get(case_id)
        if not isinstance(entry, dict):
            continue
        marker_evidence = entry.get("marker_evidence", {})
        cases.append(
            {
                "case_id": case_id,
                "passage": entry.get("passage"),
                "observed_status": entry.get("observed_status"),
                "review_packet_exists": entry.get("review_packet_exists"),
                "review_packet": entry.get("review_packet", "none"),
                "review_status": entry.get("review_status"),
                "recommended_next_step": entry.get("recommended_next_step"),
                "implementation_allowed": entry.get("implementation_allowed"),
                "wj_word_token_refs_count": marker_evidence.get("wj_word_token_refs_count", 0),
                "wj_sample_refs": marker_evidence.get("wj_sample_refs", []),
            }
        )
    return cases


def build_inventory(word_tokens_path: Path = WORD_TOKENS) -> dict[str, Any]:
    tokens = _read_jsonl(word_tokens_path)
    runs: list[dict[str, Any]] = []
    current_run: dict[str, Any] | None = None
    book_token_counts: Counter[str] = Counter()
    book_run_counts: Counter[str] = Counter()
    first_ref_by_book: dict[str, str] = {}
    last_ref_by_book: dict[str, str] = {}
    source_files = set()
    translation_ids = set()
    wj_token_count = 0

    for token in tokens:
        source_files.add(str(token.get("source_file", "")))
        translation_ids.add(str(token.get("translation_id", "")))
        is_wj = "wj" in token.get("nesting_context", [])
        if not is_wj:
            if current_run is not None:
                _finish_run(current_run, runs)
                current_run = None
            continue

        book = str(token.get("book", ""))
        ref = str(token.get("osis_ref", ""))
        word_index = int(token.get("word_index", 0))
        surface = str(token.get("surface_text", ""))
        context_key = "/".join(str(item) for item in token.get("nesting_context", []))
        wj_token_count += 1
        book_token_counts[book] += 1
        first_ref_by_book.setdefault(book, ref)
        last_ref_by_book[book] = ref

        if current_run is None:
            current_run = {
                "run_id": f"wj-run:eng-web:{len(runs) + 1:04d}",
                "book": book,
                "start_ref": ref,
                "end_ref": ref,
                "start_word_index": word_index,
                "end_word_index": word_index,
                "start_source_line": token.get("source_line"),
                "end_source_line": token.get("source_line"),
                "source_file": token.get("source_file"),
                "token_count": 0,
                "_words": [],
                "_refs": [],
                "_contexts": Counter(),
            }
            book_run_counts[book] += 1

        current_run["end_ref"] = ref
        current_run["end_word_index"] = word_index
        current_run["end_source_line"] = token.get("source_line")
        current_run["token_count"] += 1
        current_run["_words"].append(surface)
        current_run["_refs"].append(ref)
        current_run["_contexts"][context_key] += 1

    if current_run is not None:
        _finish_run(current_run, runs)

    book_summaries = []
    for book in sorted(book_token_counts, key=_book_sort_key):
        book_summaries.append(
            {
                "book": book,
                "wj_word_tokens": book_token_counts[book],
                "wj_token_runs": book_run_counts[book],
                "first_ref": first_ref_by_book[book],
                "last_ref": last_ref_by_book[book],
            }
        )

    outside_four_gospels = [
        item["book"]
        for item in book_summaries
        if item["book"] not in {"Matt", "Mark", "Luke", "John"}
    ]

    return {
        "object_type": "wj_marker_inventory",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "provenance_note": "Generated from canonical eng-web word_tokens.jsonl during T354; records observed words-of-Jesus marker token runs as evidence only.",
        "reason_for_inclusion": "Make red-letter/words-of-Jesus marker coverage visible before Gospel discourse, speaker-boundary, graph, retrieval, or chunking work cites it.",
        "schema_version": "wj_marker_inventory.v1",
        "inventory_id": "eng_web_words_of_jesus_marker_watchlist",
        "owner": "Lowell Wong",
        "authority": {
            "records_source_observations": True,
            "may_surface_for_review": True,
            "authorizes_jesus_speaker_attribution": False,
            "authorizes_speaker_boundary": False,
            "authorizes_discourse_boundary": False,
            "authorizes_chunk_boundaries": False,
            "authorizes_reviewed_gold": False,
            "authorizes_graph_edges": False,
            "authorizes_retrieval_truth": False,
            "authorizes_output_change": False,
        },
        "source_inputs": [
            {
                "path": "data/canonical/translations/eng-web/word_tokens.jsonl",
                "translation_id": sorted(translation_ids),
                "record_count": len(tokens),
                "source_file_count": len([item for item in source_files if item]),
                "used_for": "wj nesting-context token runs and book/ref counts",
            },
            {
                "path": "eval/chunking_gold/stress_atlas/observed_stress_behavior.json",
                "used_for": "known WJ review-case status and non-authorization cross-checks",
            },
        ],
        "normalization_policy": {
            "wj_detected_from_word_token_nesting_context": True,
            "inventory_unit": "contiguous canonical word-token runs where nesting_context includes wj",
            "does_not_claim_raw_marker_span_fidelity": True,
            "does_not_normalize_into_authority": True,
            "speaker_warning": "A wj token run is red-letter/source markup evidence only; it does not decide whether Jesus, narrator, a quotation, or another speaker controls a boundary.",
            "boundary_warning": "WJ run starts and ends do not authorize chunk boundaries without reviewed speaker/discourse evidence.",
        },
        "summary": {
            "wj_word_tokens": wj_token_count,
            "wj_token_runs": len(runs),
            "books_with_wj": [item["book"] for item in book_summaries],
            "books_outside_four_gospels_with_wj": outside_four_gospels,
        },
        "book_summaries": book_summaries,
        "known_review_cases": _known_review_cases(),
        "non_authorizations": [
            "wj_marker_as_speaker_authority",
            "wj_marker_as_speaker_boundary",
            "wj_marker_as_discourse_boundary",
            "wj_marker_as_chunk_boundary",
            "wj_marker_as_reviewed_gold",
            "wj_marker_as_graph_edge",
            "wj_marker_as_retrieval_truth",
            "wj_marker_as_output_change",
            "red_letter_markup_as_theological_truth",
        ],
        "wj_token_runs": runs,
        "validators": [
            "scripts/validate_wj_marker_inventory.py",
            "tests/test_wj_marker_inventory.py",
            "scripts/validate_chunking_agent_preflight.py",
            "scripts/validate_all.py",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help=f"write {OUTPUT.relative_to(ROOT).as_posix()}")
    args = parser.parse_args(argv)

    inventory = build_inventory()
    text = yaml.safe_dump(inventory, sort_keys=False, allow_unicode=False, width=120)
    if args.write:
        OUTPUT.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
