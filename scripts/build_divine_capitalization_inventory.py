#!/usr/bin/env python3
"""Build the divine-name/title capitalization inventory from canonical tokens."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORD_TOKENS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "word_tokens.jsonl"
TRANSLATION_WITNESSES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "translation_witnesses.jsonl"
OUTPUT = ROOT / ".ai" / "control" / "divine_capitalization_inventory.yaml"
TEXT_TOKEN_RE = re.compile(r"[A-Za-z]+(?:['\u2019]s)?")

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

TOKEN_WATCHES = [
    {
        "term_id": "god",
        "normalized_forms": ["god"],
        "risk_note": "God/god/GOD casing may look like divine identity, but remains translation evidence only.",
    },
    {
        "term_id": "gods",
        "normalized_forms": ["gods"],
        "risk_note": "Plural gods language must not create automatic polemical, identity, or graph claims.",
    },
    {
        "term_id": "lord",
        "normalized_forms": ["lord"],
        "risk_note": "LORD/Lord/lord casing can reflect translation convention, source rendering, title, or social address.",
    },
    {
        "term_id": "lords",
        "normalized_forms": ["lords"],
        "risk_note": "Plural lords language must not create automatic hierarchy or divine-title claims.",
    },
    {
        "term_id": "spirit",
        "normalized_forms": ["spirit"],
        "risk_note": "Spirit/spirit casing can affect pneumatology if treated as identity authority.",
    },
    {
        "term_id": "spirits",
        "normalized_forms": ["spirits"],
        "risk_note": "Spirits/spirits casing is evidence only and does not identify referents by itself.",
    },
    {
        "term_id": "father",
        "normalized_forms": ["father"],
        "risk_note": "Father/father casing may affect divine-person or family-relation interpretation.",
    },
    {
        "term_id": "fathers",
        "normalized_forms": ["fathers"],
        "risk_note": "Fathers/fathers casing is evidence only and does not authorize patriarchal or divine identity.",
    },
    {
        "term_id": "son",
        "normalized_forms": ["son"],
        "risk_note": "Son/son casing may affect Christology or title-vs-genealogy boundaries.",
    },
    {
        "term_id": "sons",
        "normalized_forms": ["sons"],
        "risk_note": "Sons/sons casing is evidence only and does not authorize identity-class claims.",
    },
    {
        "term_id": "word",
        "normalized_forms": ["word"],
        "risk_note": "Word/word casing may affect Logos/word interpretation, especially near John 1.",
    },
    {
        "term_id": "words",
        "normalized_forms": ["words"],
        "risk_note": "Words/words casing is evidence only and does not authorize lexical or doctrine labels.",
    },
    {
        "term_id": "christ",
        "normalized_forms": ["christ"],
        "risk_note": "Christ/christ casing is evidence only and does not settle title/name use by itself.",
    },
    {
        "term_id": "messiah",
        "normalized_forms": ["messiah"],
        "risk_note": "Messiah/messiah casing is evidence only and does not settle title/name use by itself.",
    },
    {
        "term_id": "holy",
        "normalized_forms": ["holy"],
        "risk_note": "Holy/holy casing can mark title, description, or source convention; it is not authority by itself.",
    },
    {
        "term_id": "lamb",
        "normalized_forms": ["lamb"],
        "risk_note": "Lamb/lamb casing may affect Christological or Revelation-symbol labels if overread.",
    },
    {
        "term_id": "he",
        "normalized_forms": ["he"],
        "risk_note": "He/he casing is broad pronoun evidence only and must not identify divine referents automatically.",
    },
    {
        "term_id": "him",
        "normalized_forms": ["him"],
        "risk_note": "Him/him casing is broad pronoun evidence only and must not identify divine referents automatically.",
    },
    {
        "term_id": "his",
        "normalized_forms": ["his"],
        "risk_note": "His/his casing is broad pronoun evidence only and must not identify divine referents automatically.",
    },
    {
        "term_id": "himself",
        "normalized_forms": ["himself"],
        "risk_note": "Himself/himself casing is broad pronoun evidence only and must not identify divine referents automatically.",
    },
]

PHRASE_WATCHES = [
    {
        "phrase_id": "holy_spirit",
        "normalized_sequence": ["holy", "spirit"],
        "risk_note": "Holy Spirit/holy spirit casing is evidence only and does not authorize pneumatological identity by itself.",
    },
    {
        "phrase_id": "son_of_god",
        "normalized_sequence": ["son", "of", "god"],
        "risk_note": "Son of God casing is evidence only and does not authorize Christological graph edges by itself.",
    },
    {
        "phrase_id": "son_of_man",
        "normalized_sequence": ["son", "of", "man"],
        "risk_note": "Son of Man/son of man casing is evidence only and must preserve genre and corpus context.",
    },
    {
        "phrase_id": "word_of_god",
        "normalized_sequence": ["word", "of", "god"],
        "risk_note": "Word of God/word of God casing is evidence only and does not authorize Logos or revelation labels.",
    },
    {
        "phrase_id": "lord_god",
        "normalized_sequence": ["lord", "god"],
        "risk_note": "Lord God casing is evidence only and must not collapse title, name, or source-language distinctions.",
    },
    {
        "phrase_id": "living_god",
        "normalized_sequence": ["living", "god"],
        "risk_note": "Living God casing is evidence only and does not authorize a graph edge by itself.",
    },
    {
        "phrase_id": "lamb_of_god",
        "normalized_sequence": ["lamb", "of", "god"],
        "risk_note": "Lamb of God casing is evidence only and does not authorize typological labels by itself.",
    },
    {
        "phrase_id": "holy_one",
        "normalized_sequence": ["holy", "one"],
        "risk_note": "Holy One/holy one casing is evidence only and does not authorize identity edges by itself.",
    },
    {
        "phrase_id": "alpha_and_omega",
        "normalized_sequence": ["alpha", "and", "omega"],
        "risk_note": "Alpha and Omega language is evidence only and must not authorize Revelation chunk labels by itself.",
    },
    {
        "phrase_id": "alpha_and_the_omega",
        "normalized_sequence": ["alpha", "and", "the", "omega"],
        "risk_note": "Alpha and the Omega language is evidence only and must not authorize Revelation chunk labels by itself.",
    },
    {
        "phrase_id": "first_and_the_last",
        "normalized_sequence": ["first", "and", "the", "last"],
        "risk_note": "First and the Last language is evidence only and must not authorize divine-identity edges by itself.",
    },
    {
        "phrase_id": "beginning_and_the_end",
        "normalized_sequence": ["beginning", "and", "the", "end"],
        "risk_note": "Beginning and the End language is evidence only and must not authorize eschatological labels by itself.",
    },
]


def _normalize_surface(surface: str) -> str:
    cleaned = re.sub(r"^[^A-Za-z]+|[^A-Za-z]+$", "", surface.strip())
    cleaned = re.sub(r"(?:['\u2019]s)$", "", cleaned)
    return cleaned


def _book_sort_key(book: str) -> tuple[int, str]:
    return (BOOK_INDEX.get(book, 999), book)


def _counter_items(counter: Counter[str], *, limit: int | None = None) -> list[dict[str, Any]]:
    items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    if limit is not None:
        items = items[:limit]
    return [{"value": value, "count": count} for value, count in items]


def _variant_items(
    variant_counts: dict[str, Counter[str]],
    variant_books: dict[str, set[str]],
    variant_refs: dict[str, list[str]],
    variant_strongs: dict[str, Counter[str]],
) -> list[dict[str, Any]]:
    result = []
    for surface_form, count in sorted(
        ((form, sum(counter.values())) for form, counter in variant_counts.items()),
        key=lambda item: (-item[1], item[0]),
    ):
        result.append(
            {
                "surface_form": surface_form,
                "count": count,
                "books": sorted(variant_books[surface_form], key=_book_sort_key),
                "first_refs": variant_refs[surface_form],
                "strong_numbers_top": _counter_items(variant_strongs[surface_form], limit=12),
            }
        )
    return result


def _add_first_ref(refs: list[str], seen: set[str], ref: str, *, limit: int = 12) -> None:
    if ref in seen or len(refs) >= limit:
        return
    seen.add(ref)
    refs.append(ref)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def build_inventory(word_tokens_path: Path = WORD_TOKENS) -> dict[str, Any]:
    tokens = _read_jsonl(word_tokens_path)
    witnesses = _read_jsonl(TRANSLATION_WITNESSES)
    watch_by_form: dict[str, list[str]] = defaultdict(list)
    for watch in TOKEN_WATCHES:
        for form in watch["normalized_forms"]:
            watch_by_form[form].append(watch["term_id"])

    term_variant_counts: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    term_variant_books: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    term_variant_refs: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    term_variant_seen_refs: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    term_variant_strongs: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    source_files = set()
    translation_ids = set()

    for token in tokens:
        source_files.add(str(token.get("source_file", "")))
        translation_ids.add(str(token.get("translation_id", "")))
        ref = str(token["osis_ref"])
        surface_form = _normalize_surface(str(token.get("surface_text", "")))
        normalized = surface_form.lower()
        for term_id in watch_by_form.get(normalized, []):
            term_variant_counts[term_id][surface_form][ref] += 1
            term_variant_books[term_id][surface_form].add(str(token.get("book", "")))
            _add_first_ref(
                term_variant_refs[term_id][surface_form],
                term_variant_seen_refs[term_id][surface_form],
                ref,
            )
            strong = str(token.get("strong") or "")
            if strong:
                term_variant_strongs[term_id][surface_form][strong] += 1

    token_watch_terms = []
    for watch in TOKEN_WATCHES:
        term_id = watch["term_id"]
        variants = _variant_items(
            term_variant_counts[term_id],
            term_variant_books[term_id],
            term_variant_refs[term_id],
            term_variant_strongs[term_id],
        )
        token_watch_terms.append(
            {
                "term_id": term_id,
                "normalized_forms": watch["normalized_forms"],
                "risk_note": watch["risk_note"],
                "total_occurrences": sum(item["count"] for item in variants),
                "observed_variants": variants,
            }
        )

    phrase_variant_counts: dict[str, Counter[str]] = defaultdict(Counter)
    phrase_variant_books: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    phrase_variant_refs: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    phrase_variant_seen_refs: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for witness in witnesses:
        ref = str(witness["osis_ref"])
        book = str(witness.get("book", ""))
        surfaces = [_normalize_surface(match.group(0)) for match in TEXT_TOKEN_RE.finditer(str(witness.get("text", "")))]
        surfaces = [surface for surface in surfaces if surface]
        normalized = [surface.lower() for surface in surfaces]
        for watch in PHRASE_WATCHES:
            phrase_id = watch["phrase_id"]
            sequence = watch["normalized_sequence"]
            length = len(sequence)
            if length > len(normalized):
                continue
            for index in range(0, len(normalized) - length + 1):
                if normalized[index : index + length] != sequence:
                    continue
                surface_phrase = " ".join(surfaces[index : index + length])
                phrase_variant_counts[phrase_id][surface_phrase] += 1
                phrase_variant_books[phrase_id][surface_phrase].add(book)
                _add_first_ref(
                    phrase_variant_refs[phrase_id][surface_phrase],
                    phrase_variant_seen_refs[phrase_id][surface_phrase],
                    ref,
                )

    phrase_watch_terms = []
    for watch in PHRASE_WATCHES:
        phrase_id = watch["phrase_id"]
        variants = []
        for surface_phrase, count in sorted(
            phrase_variant_counts[phrase_id].items(),
            key=lambda item: (-item[1], item[0]),
        ):
            variants.append(
                {
                    "surface_phrase": surface_phrase,
                    "count": count,
                    "books": sorted(phrase_variant_books[phrase_id][surface_phrase], key=_book_sort_key),
                    "first_refs": phrase_variant_refs[phrase_id][surface_phrase],
                    "source_observation": "translation_witness_text",
                }
            )
        phrase_watch_terms.append(
            {
                "phrase_id": phrase_id,
                "normalized_sequence": watch["normalized_sequence"],
                "risk_note": watch["risk_note"],
                "total_occurrences": sum(item["count"] for item in variants),
                "observed_variants": variants,
            }
        )

    return {
        "object_type": "divine_capitalization_inventory",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "provenance_note": "Generated from canonical eng-web word tokens and translation witnesses during T353; records observed capitalization variants as evidence only.",
        "reason_for_inclusion": "Make God/god, Spirit/spirit, Father/father, Word/word, LORD/Lord/lord, divine-pronoun, and related title capitalization visible before graph, retrieval, or chunking work.",
        "schema_version": "divine_capitalization_inventory.v1",
        "inventory_id": "eng_web_divine_name_title_capitalization_watchlist",
        "owner": "Lowell Wong",
        "authority": {
            "records_source_observations": True,
            "may_surface_for_review": True,
            "authorizes_divine_identity": False,
            "authorizes_trinitarian_relation": False,
            "authorizes_christology": False,
            "authorizes_pneumatology": False,
            "authorizes_speaker_attribution": False,
            "authorizes_lexical_truth": False,
            "authorizes_graph_edges": False,
            "authorizes_chunk_boundaries": False,
            "authorizes_retrieval_truth": False,
            "authorizes_output_change": False,
        },
        "source_inputs": [
            {
                "path": "data/canonical/translations/eng-web/word_tokens.jsonl",
                "translation_id": sorted(translation_ids),
                "record_count": len(tokens),
                "source_file_count": len([item for item in source_files if item]),
                "used_for": "single-token capitalization variants and Strong's-style metadata summaries",
            },
            {
                "path": "data/canonical/translations/eng-web/translation_witnesses.jsonl",
                "translation_id": sorted({str(record.get("translation_id", "")) for record in witnesses}),
                "record_count": len(witnesses),
                "used_for": "phrase capitalization variants from canonical witness text",
            }
        ],
        "normalization_policy": {
            "case_observed_from_surface_text": True,
            "normalizes_for_matching": "Strip surrounding punctuation and possessive suffix, then lowercase for watchlist matching.",
            "does_not_normalize_into_authority": True,
            "pronoun_warning": "Pronoun casing is inventoried as broad evidence only; this inventory does not decide whether a pronoun refers to God, Christ, the Spirit, or another referent.",
            "strong_number_warning": "Strong's-style numbers are preserved as source metadata evidence only; they do not authorize lexical truth, identity, or graph edges.",
        },
        "non_authorizations": [
            "capitalization_driven_divine_identity",
            "capitalization_driven_trinitarian_relation",
            "capitalization_driven_christology",
            "capitalization_driven_pneumatology",
            "capitalization_driven_speaker_attribution",
            "capitalization_driven_graph_edge",
            "capitalization_driven_chunk_boundary",
            "capitalization_driven_retrieval_truth",
            "capitalization_driven_output_change",
            "strong_number_driven_lexical_truth",
            "pronoun_capitalization_as_referent_identity",
        ],
        "token_watch_terms": token_watch_terms,
        "phrase_watch_terms": phrase_watch_terms,
        "validators": [
            "scripts/validate_divine_capitalization_inventory.py",
            "tests/test_divine_capitalization_inventory.py",
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
