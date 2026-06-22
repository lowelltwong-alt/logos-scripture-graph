#!/usr/bin/env python3
"""Build the Bible-wide verse/passage coverage inventory for T386."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
TRANSLATION_WITNESSES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "translation_witnesses.jsonl"
WORD_TOKENS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "word_tokens.jsonl"
FOOTNOTES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "footnotes.jsonl"
CROSS_REFS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "editorial_cross_references.jsonl"
BOUNDARY_CLAIMS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "boundary_claims.jsonl"

CONTROL = ROOT / ".ai" / "control"
OUTPUT_INVENTORY = CONTROL / "bible_verse_passage_coverage_inventory.jsonl"
OUTPUT_TAXONOMY = CONTROL / "bible_verse_passage_coverage_taxonomy.yaml"
OUTPUT_SUMMARY = CONTROL / "bible_verse_passage_coverage_summary.yaml"
OUTPUT_MATRIX = CONTROL / "bible_verse_passage_readiness_matrix.yaml"
OUTPUT_GAPS = CONTROL / "bible_verse_passage_gap_register.yaml"
OUTPUT_DOCKET = CONTROL / "bible_verse_passage_human_review_docket.yaml"

BOOK_ORDER = [
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

BOOK_LANES = {
    **{book: "torah_narrative_law_covenant" for book in ["Gen", "Exod", "Lev", "Num", "Deut"]},
    **{
        book: "historical_narrative"
        for book in [
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
        ]
    },
    **{book: "wisdom_dialogue_poetry" for book in ["Job", "Ps", "Prov", "Eccl", "Song"]},
    **{
        book: "prophetic_oracle_vision"
        for book in [
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
        ]
    },
    **{book: "gospel_discourse_wj" for book in ["Matt", "Mark", "Luke", "John"]},
    "Acts": "acts_narrative_speech_transition",
    **{
        book: "epistle_argument"
        for book in [
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
        ]
    },
    "Rev": "revelation_apocalyptic",
}

CONTROL_SOURCES = {
    ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml": {
        "flags": {"cross_reference_or_intertext_risk", "theological_downstream_risk", "review_packet_needed"},
        "source_id": "apocalyptic_prophetic_intertext_dossier_queue",
        "decision_ids": {"T386-HDM-004", "T386-HDM-007"},
    },
    ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml": {
        "flags": {"theological_downstream_risk", "review_packet_needed"},
        "source_id": "epistle_argument_theological_issue_dossier_queue",
        "decision_ids": {"T386-HDM-001", "T386-HDM-007"},
    },
    ".ai/control/gospel_wj_discourse_dossier_queue.yaml": {
        "flags": {
            "speaker_wj_red_letter_discourse_boundary_risk",
            "theological_downstream_risk",
            "review_packet_needed",
        },
        "source_id": "gospel_wj_discourse_dossier_queue",
        "decision_ids": {"T386-HDM-003", "T386-HDM-007"},
    },
    ".ai/control/narrative_legal_covenant_dossier_queue.yaml": {
        "flags": {"theological_downstream_risk", "review_packet_needed"},
        "source_id": "narrative_legal_covenant_dossier_queue",
        "decision_ids": {"T386-HDM-001", "T386-HDM-007"},
    },
    ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml": {
        "flags": {"theological_downstream_risk", "review_packet_needed"},
        "source_id": "wisdom_dialogue_poetry_dossier_queue",
        "decision_ids": {"T386-HDM-001", "T386-HDM-007"},
    },
    ".ai/control/prophetic_oracle_vision_dossier_queue.yaml": {
        "flags": {"cross_reference_or_intertext_risk", "theological_downstream_risk", "review_packet_needed"},
        "source_id": "prophetic_oracle_vision_dossier_queue",
        "decision_ids": {"T386-HDM-004", "T386-HDM-007"},
    },
    ".ai/control/textual_variant_source_tradition_dossier_queue.yaml": {
        "flags": {
            "textual_variant_source_tradition_sensitive",
            "theological_downstream_risk",
            "review_packet_needed",
            "human_owner_decision_required",
            "blocked_authority_action",
        },
        "source_id": "textual_variant_source_tradition_dossier_queue",
        "decision_ids": {"T386-HDM-002", "T386-HDM-006", "T386-HDM-007"},
    },
    ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml": {
        "flags": {
            "known_non_orthodox_pressure_passage",
            "original_language_phrase_context_review",
            "theological_downstream_risk",
            "review_packet_needed",
            "human_owner_decision_required",
        },
        "source_id": "orthodox_original_language_pressure_dossier_queue",
        "decision_ids": {"T386-HDM-005", "T386-HDM-006", "T386-HDM-007"},
    },
    ".ai/control/john3_wj_owner_review_docket.yaml": {
        "flags": {
            "speaker_wj_red_letter_discourse_boundary_risk",
            "theological_downstream_risk",
            "review_packet_needed",
        },
        "source_id": "john3_wj_owner_review_docket",
        "decision_ids": {"T386-HDM-003", "T386-HDM-007"},
    },
    ".ai/control/1cor8_10_epistle_owner_review_docket.yaml": {
        "flags": {"theological_downstream_risk", "review_packet_needed"},
        "source_id": "1cor8_10_epistle_owner_review_docket",
        "decision_ids": {"T386-HDM-001", "T386-HDM-007"},
    },
    "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml": {
        "flags": {"theological_downstream_risk", "review_packet_needed"},
        "source_id": "1cor8_10_parent_only_evidence_packet",
        "decision_ids": {"T386-HDM-001", "T386-HDM-007"},
    },
}

SCOPE_KEYS = {
    "exact_passage_scope",
    "passage",
    "exact_parent_candidate",
    "selected_parent",
    "selected_parent_candidate",
    "span",
    "source_passages",
    "candidate_intertexts",
    "affected_passages",
    "target_passages",
    "passages",
    "passage_scope",
    "refs",
    "references",
    "wj_sample_refs",
}

STATUS_DEEP_FLAGS = {
    "review_packet_needed",
    "original_language_phrase_context_review",
    "textual_variant_source_tradition_sensitive",
    "cross_reference_or_intertext_risk",
    "speaker_wj_red_letter_discourse_boundary_risk",
    "known_non_orthodox_pressure_passage",
    "theological_downstream_risk",
}

DIVINE_WATCH_TERMS = {
    "god",
    "gods",
    "lord",
    "lords",
    "yahweh",
    "spirit",
    "spirits",
    "father",
    "fathers",
    "son",
    "sons",
    "word",
    "words",
    "christ",
    "messiah",
    "holy",
    "lamb",
    "he",
    "him",
    "his",
    "himself",
}

NON_AUTHORIZATIONS = [
    "chunk_output_change",
    "reviewed_gold_promotion",
    "child_span_selection",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "boundary_import",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "denominational_systematic_theology_as_chunk_authority",
]

REF_RE = re.compile(r"^(?P<book>[1-3]?[A-Za-z]+)(?:\.(?P<chapter>\d+)(?:\.(?P<verse>\d+))?)?$")


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def read_yaml(path: Path) -> Any:
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    return yaml.safe_load(text)


def normalize_token(token: str) -> str:
    return re.sub(r"[^A-Za-z]", "", token).lower()


def collect_scope_strings(value: Any, parent_key: str | None = None) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            found.extend(collect_scope_strings(nested, str(key)))
    elif isinstance(value, list):
        if parent_key in SCOPE_KEYS:
            for item in value:
                if isinstance(item, str):
                    found.append(item)
        else:
            for item in value:
                found.extend(collect_scope_strings(item, parent_key))
    elif isinstance(value, str) and parent_key in SCOPE_KEYS:
        found.append(value)
    return found


class PassageIndex:
    def __init__(self, passages: list[dict[str, Any]]) -> None:
        self.passages = passages
        self.refs = [str(p["osis_ref"]) for p in passages]
        self.by_ref = {str(p["osis_ref"]): p for p in passages}
        self.index_by_ref = {ref: index for index, ref in enumerate(self.refs)}
        self.refs_by_book: dict[str, list[str]] = defaultdict(list)
        self.refs_by_book_chapter: dict[tuple[str, int], list[str]] = defaultdict(list)
        for passage in passages:
            book = str(passage["book"])
            chapter = int(passage["chapter"])
            ref = str(passage["osis_ref"])
            self.refs_by_book[book].append(ref)
            self.refs_by_book_chapter[(book, chapter)].append(ref)

    def parse_ref(self, value: str) -> tuple[str, int | None, int | None] | None:
        match = REF_RE.match(value.strip())
        if not match:
            return None
        book = match.group("book")
        if book not in self.refs_by_book:
            return None
        chapter = int(match.group("chapter")) if match.group("chapter") else None
        verse = int(match.group("verse")) if match.group("verse") else None
        return book, chapter, verse

    def endpoint(self, value: str, *, last: bool) -> str | None:
        parsed = self.parse_ref(value)
        if parsed is None:
            return None
        book, chapter, verse = parsed
        if chapter is None:
            refs = self.refs_by_book[book]
            return refs[-1] if last else refs[0]
        if verse is None:
            refs = self.refs_by_book_chapter.get((book, chapter), [])
            if not refs:
                return None
            return refs[-1] if last else refs[0]
        ref = f"{book}.{chapter}.{verse}"
        return ref if ref in self.index_by_ref else None

    def expand_scope(self, scope: str) -> list[str]:
        scope = scope.strip().strip("\"'")
        if not scope:
            return []
        if "-" in scope:
            start, end = scope.split("-", 1)
            start_ref = self.endpoint(start, last=False)
            end_ref = self.endpoint(end, last=True)
            if start_ref is None or end_ref is None:
                return []
            start_i = self.index_by_ref[start_ref]
            end_i = self.index_by_ref[end_ref]
            if start_i > end_i:
                return []
            return self.refs[start_i : end_i + 1]
        endpoint = self.endpoint(scope, last=False)
        if endpoint is None:
            return []
        parsed = self.parse_ref(scope)
        if parsed is None:
            return []
        book, chapter, verse = parsed
        if chapter is None:
            return list(self.refs_by_book[book])
        if verse is None:
            return list(self.refs_by_book_chapter.get((book, chapter), []))
        return [endpoint]


def add_flag(record: dict[str, Any], flag: str, source: str | None = None) -> None:
    record["flags"].add(flag)
    if source:
        record["source_surface_ids"].add(source)


def add_decisions(record: dict[str, Any], decision_ids: Iterable[str]) -> None:
    record["owner_decision_ids"].update(decision_ids)


def apply_control_source(path: Path, config: dict[str, Any], index: PassageIndex, records: dict[str, dict[str, Any]]) -> int:
    if not path.exists():
        return 0
    loaded = read_yaml(path)
    scopes = collect_scope_strings(loaded)
    touched: set[str] = set()
    for scope in scopes:
        for ref in index.expand_scope(scope):
            if ref in records:
                touched.add(ref)
    for ref in touched:
        record = records[ref]
        for flag in config["flags"]:
            add_flag(record, flag, config["source_id"])
        add_decisions(record, config["decision_ids"])
    return len(touched)


def build_records(passages: list[dict[str, Any]]) -> tuple[PassageIndex, dict[str, dict[str, Any]], dict[str, int]]:
    index = PassageIndex(passages)
    records: dict[str, dict[str, Any]] = {}
    for passage in passages:
        ref = str(passage["osis_ref"])
        records[ref] = {
            "schema_version": "bible_verse_passage_coverage.v1",
            "coverage_id": f"coverage:{ref}",
            "passage_id": passage["id"],
            "osis_ref": ref,
            "book": passage["book"],
            "chapter": passage["chapter"],
            "verse_start": passage["verse_start"],
            "verse_end": passage["verse_end"],
            "lane_id": BOOK_LANES[str(passage["book"])],
            "coverage_status": "routine_under_existing_policy",
            "flags": set(),
            "source_evidence_counts": {
                "translation_witnesses": 0,
                "word_tokens": 0,
                "strongs_tokens": 0,
                "wj_tokens": 0,
                "footnotes": 0,
                "alternate_reading_footnotes": 0,
                "hebrew_word_footnotes": 0,
                "greek_word_footnotes": 0,
                "editorial_cross_references": 0,
                "boundary_claims": 0,
                "divine_capitalization_tokens": 0,
            },
            "source_surface_ids": set(),
            "owner_decision_ids": set(),
            "non_authorizations": NON_AUTHORIZATIONS,
        }

    diagnostics: dict[str, int] = {}
    for witness in read_jsonl(TRANSLATION_WITNESSES):
        ref = witness.get("osis_ref")
        if ref in records:
            records[ref]["source_evidence_counts"]["translation_witnesses"] += 1

    for record in records.values():
        if record["source_evidence_counts"]["translation_witnesses"] == 0:
            add_flag(record, "translation_witness_missing", "translation_witnesses")
            add_flag(record, "blocked_authority_action", "translation_witnesses")
            add_decisions(record, {"T386-HDM-008"})

    for footnote in read_jsonl(FOOTNOTES):
        ref = footnote.get("osis_ref")
        if ref not in records:
            continue
        record = records[ref]
        counts = record["source_evidence_counts"]
        counts["footnotes"] += 1
        add_flag(record, "source_metadata_sensitive", "footnotes")
        if footnote.get("alternate_readings"):
            counts["alternate_reading_footnotes"] += 1
            add_flag(record, "textual_variant_source_tradition_sensitive", "footnotes")
            add_flag(record, "human_owner_decision_required", "footnotes")
            add_flag(record, "blocked_authority_action", "footnotes")
            add_decisions(record, {"T386-HDM-002", "T386-HDM-006"})
        if footnote.get("hebrew_word_spans"):
            counts["hebrew_word_footnotes"] += 1
            add_flag(record, "original_language_phrase_context_review", "footnotes")
            add_decisions(record, {"T386-HDM-005"})
        if footnote.get("greek_word_spans"):
            counts["greek_word_footnotes"] += 1
            add_flag(record, "original_language_phrase_context_review", "footnotes")
            add_decisions(record, {"T386-HDM-005"})

    for cross_ref in read_jsonl(CROSS_REFS):
        ref = cross_ref.get("osis_ref")
        if ref not in records:
            continue
        record = records[ref]
        record["source_evidence_counts"]["editorial_cross_references"] += 1
        add_flag(record, "source_metadata_sensitive", "editorial_cross_references")
        add_flag(record, "editorial_cross_reference_present", "editorial_cross_references")
        add_flag(record, "cross_reference_or_intertext_risk", "editorial_cross_references")
        add_decisions(record, {"T386-HDM-004"})

    for boundary in read_jsonl(BOUNDARY_CLAIMS):
        ref = boundary.get("osis_ref")
        if ref not in records:
            continue
        record = records[ref]
        record["source_evidence_counts"]["boundary_claims"] += 1
        add_flag(record, "source_metadata_sensitive", "boundary_claims")

    for token in read_jsonl(WORD_TOKENS):
        ref = token.get("osis_ref")
        if ref not in records:
            continue
        record = records[ref]
        counts = record["source_evidence_counts"]
        counts["word_tokens"] += 1
        if token.get("strong"):
            counts["strongs_tokens"] += 1
            add_flag(record, "source_metadata_sensitive", "word_tokens")
            add_flag(record, "strongs_metadata_present", "word_tokens")
        context = token.get("nesting_context") or []
        if any("wj" in str(item).lower() for item in context):
            counts["wj_tokens"] += 1
            add_flag(record, "source_metadata_sensitive", "word_tokens")
            add_flag(record, "speaker_wj_red_letter_discourse_boundary_risk", "word_tokens")
            add_decisions(record, {"T386-HDM-003"})
        if normalize_token(str(token.get("surface_text", ""))) in DIVINE_WATCH_TERMS:
            counts["divine_capitalization_tokens"] += 1
            add_flag(record, "source_metadata_sensitive", "word_tokens")
            add_flag(record, "divine_name_title_capitalization_sensitive", "word_tokens")
            add_decisions(record, {"T386-HDM-005"})

    for rel, config in CONTROL_SOURCES.items():
        touched = apply_control_source(ROOT / rel, config, index, records)
        diagnostics[f"control_refs:{config['source_id']}"] = touched

    for record in records.values():
        flags = record["flags"]
        if "blocked_authority_action" in flags:
            record["coverage_status"] = "blocked_before_chunking"
        elif "human_owner_decision_required" in flags:
            record["coverage_status"] = "human_decision_required"
        elif STATUS_DEEP_FLAGS & flags:
            record["coverage_status"] = "deeper_review_required"
        else:
            record["coverage_status"] = "routine_under_existing_policy"
        record["flags"] = sorted(record["flags"])
        record["source_surface_ids"] = sorted(record["source_surface_ids"])
        record["owner_decision_ids"] = sorted(record["owner_decision_ids"])

    return index, records, diagnostics


def inventory_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_jsonl(records: dict[str, dict[str, Any]], index: PassageIndex) -> None:
    with OUTPUT_INVENTORY.open("w", encoding="utf-8", newline="\n") as handle:
        for ref in index.refs:
            handle.write(json.dumps(records[ref], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")


def sample_refs(refs: Iterable[str], limit: int = 12) -> list[str]:
    return list(refs)[:limit]


def build_taxonomy() -> dict[str, Any]:
    return {
        "object_type": "bible_verse_passage_coverage_taxonomy",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "provenance_note": "Created 2026-06-22 during T386 from canonical passages, eng-web sidecars, and governed research queues.",
        "reason_for_inclusion": "Define deterministic statuses, flags, and non-authorizations for Bible-wide verse/passage coverage before chunk-output work resumes.",
        "schema_version": "bible_verse_passage_coverage_taxonomy.v1",
        "taxonomy_id": "t386_bible_verse_passage_coverage_taxonomy",
        "task_id": "T386",
        "owner": "Lowell Wong",
        "authority": {
            "records_coverage": True,
            "records_review_needs": True,
            "records_owner_decision_needs": True,
            "authorizes_chunk_output_change": False,
            "authorizes_reviewed_gold_promotion": False,
            "authorizes_child_spans": False,
            "authorizes_route_behavior_change": False,
            "authorizes_evaluator_change": False,
            "authorizes_graph_edges": False,
            "authorizes_retrieval_truth": False,
            "authorizes_embedding_or_vector_work": False,
            "authorizes_boundary_import": False,
            "authorizes_preferred_reading_or_source_tradition": False,
            "authorizes_canon_scope_change": False,
            "authorizes_denominational_systematic_theology_as_chunk_authority": False,
        },
        "coverage_statuses": [
            {
                "status": "routine_under_existing_policy",
                "meaning": "Passage is accounted for at triage depth and has no current T386 risk flag requiring a packet or owner decision before ordinary review/prep.",
            },
            {
                "status": "deeper_review_required",
                "meaning": "Passage is accounted for and flagged for review-packet or context work before it may be used for chunking decisions.",
            },
            {
                "status": "human_decision_required",
                "meaning": "Passage is accounted for and needs owner confirmation before promotion, implementation, or authority-sensitive chunking use.",
            },
            {
                "status": "blocked_before_chunking",
                "meaning": "Passage is accounted for, but an authority-changing use must remain blocked until a later exact owner gate and validator update.",
            },
        ],
        "flag_taxonomy": [
            "translation_witness_missing",
            "source_metadata_sensitive",
            "strongs_metadata_present",
            "original_language_phrase_context_review",
            "textual_variant_source_tradition_sensitive",
            "editorial_cross_reference_present",
            "cross_reference_or_intertext_risk",
            "speaker_wj_red_letter_discourse_boundary_risk",
            "divine_name_title_capitalization_sensitive",
            "known_non_orthodox_pressure_passage",
            "theological_downstream_risk",
            "review_packet_needed",
            "human_owner_decision_required",
            "blocked_authority_action",
        ],
        "decision_id_taxonomy": [
            "T386-HDM-001",
            "T386-HDM-002",
            "T386-HDM-003",
            "T386-HDM-004",
            "T386-HDM-005",
            "T386-HDM-006",
            "T386-HDM-007",
            "T386-HDM-008",
        ],
        "validator": "scripts/validate_bible_verse_passage_coverage_inventory.py",
    }


def build_docket() -> dict[str, Any]:
    decisions = [
        {
            "decision_id": "T386-HDM-001",
            "title": "Review-packet strengthening order before chunk output",
            "trigger_flags": ["review_packet_needed", "theological_downstream_risk"],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-001-A",
                    "summary": "Strengthen one exact review packet at a time, preserving parent-first and no-output defaults.",
                    "repercussion": "Slower than broad implementation, but keeps theology-bearing boundaries auditable.",
                },
                {
                    "option_id": "T386-HDM-001-B",
                    "summary": "Prepare multiple packets in parallel as research-only surfaces, then ask the owner to select one.",
                    "repercussion": "Faster research throughput, but requires careful stop conditions before promotion.",
                },
            ],
            "recommended_conservative_path": "T386-HDM-001-B for research/prep only, then one exact owner selection before promotion or implementation.",
            "stop_conditions": [
                "A packet would select chunk output.",
                "A packet would imply reviewed-gold promotion.",
                "A packet would require child spans before owner review.",
            ],
        },
        {
            "decision_id": "T386-HDM-002",
            "title": "Textual-variant and source-tradition policy for variant-sensitive passages",
            "trigger_flags": ["textual_variant_source_tradition_sensitive", "blocked_authority_action"],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-002-A",
                    "summary": "Keep TCP-T378-B case-by-case owner confirmation for each variant-sensitive promotion.",
                    "repercussion": "Prevents hidden critical-text, TR, majority-text, or current-source defaults.",
                },
                {
                    "option_id": "T386-HDM-002-B",
                    "summary": "Create a later broader textual-critical framework after enough cases are documented.",
                    "repercussion": "Could reduce repeated decisions later, but is a higher-authority theological/source-tradition gate.",
                },
            ],
            "recommended_conservative_path": "Use T386-HDM-002-A until the owner explicitly authorizes a broader policy.",
            "stop_conditions": [
                "A preferred reading is needed.",
                "A source-tradition preference is implied.",
                "A canon-scope or boundary-material decision is required.",
            ],
        },
        {
            "decision_id": "T386-HDM-003",
            "title": "WJ/red-letter/speaker/discourse boundary decisions",
            "trigger_flags": ["speaker_wj_red_letter_discourse_boundary_risk"],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-003-A",
                    "summary": "Treat WJ/red-letter markers as source metadata and require packet evidence before speaker-boundary use.",
                    "repercussion": "Preserves Jesus/narrator and quotation boundaries without treating edition formatting as authority.",
                },
                {
                    "option_id": "T386-HDM-003-B",
                    "summary": "Avoid WJ-dependent target promotion until a stronger WJ discourse packet exists.",
                    "repercussion": "Safest for ambiguous discourse, but may defer Gospel work.",
                },
            ],
            "recommended_conservative_path": "Use T386-HDM-003-A with exact-scope owner review.",
            "stop_conditions": [
                "A red-letter marker would become speaker attribution.",
                "Narrator/Jesus boundary cannot be preserved.",
                "A WJ route behavior change is needed.",
            ],
        },
        {
            "decision_id": "T386-HDM-004",
            "title": "Cross-reference and intertext handling",
            "trigger_flags": ["cross_reference_or_intertext_risk", "editorial_cross_reference_present"],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-004-A",
                    "summary": "Surface crossrefs/intertexts as evidence-only review signals.",
                    "repercussion": "Keeps canonical links visible without generating graph truth.",
                },
                {
                    "option_id": "T386-HDM-004-B",
                    "summary": "Require a separate intertext dossier before any intertext-aware chunk target is promoted.",
                    "repercussion": "Higher audit burden, but safer for Revelation, prophecy, and typology-heavy passages.",
                },
            ],
            "recommended_conservative_path": "Use T386-HDM-004-B for high-risk intertext lanes and T386-HDM-004-A for routine metadata surfacing.",
            "stop_conditions": [
                "An editorial cross-reference would become a graph edge.",
                "Absence of a cross-reference would be treated as absence of an intertext.",
                "A typology or fulfillment system would become a chunking default.",
            ],
        },
        {
            "decision_id": "T386-HDM-005",
            "title": "Original-language phrase/context and divine capitalization handling",
            "trigger_flags": [
                "original_language_phrase_context_review",
                "divine_name_title_capitalization_sensitive",
                "known_non_orthodox_pressure_passage",
            ],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-005-A",
                    "summary": "Use Greek/Hebrew/Strong's/capitalization only inside phrase, clause, discourse, book, and canonical context.",
                    "repercussion": "Prevents isolated-word theology and preserves orthodox review space.",
                },
                {
                    "option_id": "T386-HDM-005-B",
                    "summary": "Hold pressure passages until a grammar-overlay dossier is written.",
                    "repercussion": "Safest for LDS, Watch Tower, and anti-Trinitarian pressure passages, but slows those targets.",
                },
            ],
            "recommended_conservative_path": "Use T386-HDM-005-A generally and T386-HDM-005-B for pressure passages.",
            "stop_conditions": [
                "A Strong's number or gloss would become lexical truth.",
                "A capitalization convention would become doctrine authority.",
                "A pressure-passage label would import non-orthodox source authority.",
            ],
        },
        {
            "decision_id": "T386-HDM-006",
            "title": "Blocked authority actions before chunking",
            "trigger_flags": ["blocked_authority_action", "human_owner_decision_required"],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-006-A",
                    "summary": "Keep blocked actions blocked until exact owner review, decision-register entry, and validator update.",
                    "repercussion": "Maintains auditability and prevents hidden authority changes.",
                }
            ],
            "recommended_conservative_path": "Use T386-HDM-006-A.",
            "stop_conditions": [
                "The work would authorize output.",
                "The work would prefer a source tradition.",
                "The work would change canon scope or boundary import policy.",
            ],
        },
        {
            "decision_id": "T386-HDM-007",
            "title": "Exact next non-output step after Bible-wide coverage",
            "trigger_flags": ["review_packet_needed", "human_owner_decision_required"],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-007-A",
                    "summary": "Proceed to T385 owner decision packet using T384 synthesis plus T386 coverage as required inputs.",
                    "repercussion": "Best continuation path toward chunking without silently selecting implementation targets.",
                },
                {
                    "option_id": "T386-HDM-007-B",
                    "summary": "Add more research-only dossiers before T385.",
                    "repercussion": "May improve evidence depth, but delays the owner decision packet.",
                },
            ],
            "recommended_conservative_path": "T386-HDM-007-A.",
            "stop_conditions": [
                "The next step would implement chunks.",
                "The next step would promote reviewed gold.",
                "The next step would select a target without owner review.",
            ],
        },
        {
            "decision_id": "T386-HDM-008",
            "title": "Canonical passage has no translation witness",
            "trigger_flags": ["translation_witness_missing"],
            "faithful_options": [
                {
                    "option_id": "T386-HDM-008-A",
                    "summary": "Block chunking for the missing-witness passage until source integrity is repaired.",
                    "repercussion": "Protects against silent Scripture omission.",
                }
            ],
            "recommended_conservative_path": "T386-HDM-008-A.",
            "stop_conditions": ["Any missing witness is present in the canonical passage registry."],
        },
    ]
    return {
        "object_type": "bible_verse_passage_human_review_docket",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "provenance_note": "Created 2026-06-22 during T386 from the Bible-wide coverage taxonomy and existing owner decision patterns.",
        "reason_for_inclusion": "Gather foreseeable human decisions before chunking resumes, with faithful options and stop conditions.",
        "schema_version": "bible_verse_passage_human_review_docket.v1",
        "docket_id": "t386_bible_verse_passage_human_review_docket",
        "task_id": "T386",
        "owner": "Lowell Wong",
        "authority": build_taxonomy()["authority"],
        "orthodoxy_boundary": "nicene_chalcedonian_core",
        "decisions": decisions,
        "exact_next_non_output_step": {
            "task_id": "T385",
            "title": "Owner Decision Packet From T384/T386 Readiness Coverage",
            "route_type": "owner_decision_packet_only",
            "required_inputs": [
                ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml",
                ".ai/control/bible_verse_passage_coverage_summary.yaml",
                ".ai/control/bible_verse_passage_human_review_docket.yaml",
                ".ai/control/bible_verse_passage_gap_register.yaml",
            ],
            "output_change_authorized": False,
            "reviewed_gold_promoted": False,
            "implementation_authorized": False,
        },
        "non_authorizations": NON_AUTHORIZATIONS,
    }


def build_summaries(
    records: dict[str, dict[str, Any]],
    index: PassageIndex,
    diagnostics: dict[str, int],
    digest: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    status_counts = Counter(record["coverage_status"] for record in records.values())
    flag_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    lane_status: dict[str, Counter[str]] = defaultdict(Counter)
    lane_flags: dict[str, Counter[str]] = defaultdict(Counter)
    book_status: dict[str, Counter[str]] = defaultdict(Counter)
    book_flags: dict[str, Counter[str]] = defaultdict(Counter)
    flag_refs: dict[str, list[str]] = defaultdict(list)
    for ref in index.refs:
        record = records[ref]
        book = record["book"]
        lane = record["lane_id"]
        status = record["coverage_status"]
        lane_status[lane][status] += 1
        book_status[book][status] += 1
        for flag in record["flags"]:
            flag_counts[flag] += 1
            lane_flags[lane][flag] += 1
            book_flags[book][flag] += 1
            flag_refs[flag].append(ref)
        for decision_id in record["owner_decision_ids"]:
            decision_counts[decision_id] += 1

    summary = {
        "object_type": "bible_verse_passage_coverage_summary",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "provenance_note": "Generated 2026-06-22 during T386 from canonical passage records, eng-web sidecars, and governed research queues.",
        "reason_for_inclusion": "Summarize deterministic Bible-wide passage coverage before chunk-output work resumes.",
        "schema_version": "bible_verse_passage_coverage_summary.v1",
        "summary_id": "t386_bible_verse_passage_coverage_summary",
        "task_id": "T386",
        "owner": "Lowell Wong",
        "inventory_path": ".ai/control/bible_verse_passage_coverage_inventory.jsonl",
        "inventory_sha256": digest,
        "canonical_scope": "canonical_66",
        "canonical_book_count": len(index.refs_by_book),
        "canonical_passage_count": len(index.refs),
        "status_counts": dict(sorted(status_counts.items())),
        "flag_counts": dict(sorted(flag_counts.items())),
        "owner_decision_counts": dict(sorted(decision_counts.items())),
        "control_source_ref_counts": dict(sorted(diagnostics.items())),
        "authority": build_taxonomy()["authority"],
        "exact_next_non_output_step": "T385 owner decision packet using T384 synthesis plus T386 coverage surfaces as required inputs.",
        "non_authorizations": NON_AUTHORIZATIONS,
    }

    matrix = {
        "object_type": "bible_verse_passage_readiness_matrix",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "provenance_note": "Generated 2026-06-22 during T386 from the Bible-wide passage coverage inventory.",
        "reason_for_inclusion": "Show book-by-book and lane-by-lane readiness before chunking resumes.",
        "schema_version": "bible_verse_passage_readiness_matrix.v1",
        "matrix_id": "t386_bible_verse_passage_readiness_matrix",
        "task_id": "T386",
        "owner": "Lowell Wong",
        "inventory_path": ".ai/control/bible_verse_passage_coverage_inventory.jsonl",
        "inventory_sha256": digest,
        "book_matrix": [
            {
                "book": book,
                "lane_id": BOOK_LANES[book],
                "passage_count": len(index.refs_by_book[book]),
                "status_counts": dict(sorted(book_status[book].items())),
                "flag_counts": dict(sorted(book_flags[book].items())),
            }
            for book in BOOK_ORDER
        ],
        "lane_matrix": [
            {
                "lane_id": lane,
                "book_count": sum(1 for book in BOOK_ORDER if BOOK_LANES[book] == lane),
                "passage_count": sum(len(index.refs_by_book[book]) for book in BOOK_ORDER if BOOK_LANES[book] == lane),
                "status_counts": dict(sorted(lane_status[lane].items())),
                "flag_counts": dict(sorted(lane_flags[lane].items())),
            }
            for lane in sorted(set(BOOK_LANES.values()))
        ],
        "authority": build_taxonomy()["authority"],
        "non_authorizations": NON_AUTHORIZATIONS,
    }

    gaps = {
        "object_type": "bible_verse_passage_gap_register",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "provenance_note": "Generated 2026-06-22 during T386 from the Bible-wide passage coverage inventory.",
        "reason_for_inclusion": "List coverage gaps and deeper-research queues so later chunking work can see unresolved risks.",
        "schema_version": "bible_verse_passage_gap_register.v1",
        "gap_register_id": "t386_bible_verse_passage_gap_register",
        "task_id": "T386",
        "owner": "Lowell Wong",
        "inventory_path": ".ai/control/bible_verse_passage_coverage_inventory.jsonl",
        "inventory_sha256": digest,
        "gap_entries": [
            {
                "gap_id": f"T386-GAP-{index_num:03d}",
                "flag": flag,
                "passage_count": flag_counts[flag],
                "sample_refs": sample_refs(flag_refs[flag]),
                "requires_owner_decision_ids": sorted(
                    {
                        decision_id
                        for ref in flag_refs[flag]
                        for decision_id in records[ref]["owner_decision_ids"]
                    }
                ),
                "authority_status": "evidence_only_non_authorizing",
            }
            for index_num, flag in enumerate(sorted(flag_counts), start=1)
            if flag
        ],
        "status_counts": dict(sorted(status_counts.items())),
        "authority": build_taxonomy()["authority"],
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    return summary, matrix, gaps


def build_inventory() -> None:
    passages = list(read_jsonl(PASSAGES))
    index, records, diagnostics = build_records(passages)
    write_jsonl(records, index)
    digest = inventory_hash(OUTPUT_INVENTORY)
    taxonomy = build_taxonomy()
    docket = build_docket()
    summary, matrix, gaps = build_summaries(records, index, diagnostics, digest)
    dump_yaml(OUTPUT_TAXONOMY, taxonomy)
    dump_yaml(OUTPUT_SUMMARY, summary)
    dump_yaml(OUTPUT_MATRIX, matrix)
    dump_yaml(OUTPUT_GAPS, gaps)
    dump_yaml(OUTPUT_DOCKET, docket)


def main() -> int:
    build_inventory()
    print(f"wrote {OUTPUT_INVENTORY.relative_to(ROOT).as_posix()}")
    print(f"wrote {OUTPUT_TAXONOMY.relative_to(ROOT).as_posix()}")
    print(f"wrote {OUTPUT_SUMMARY.relative_to(ROOT).as_posix()}")
    print(f"wrote {OUTPUT_MATRIX.relative_to(ROOT).as_posix()}")
    print(f"wrote {OUTPUT_GAPS.relative_to(ROOT).as_posix()}")
    print(f"wrote {OUTPUT_DOCKET.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
