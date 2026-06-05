#!/usr/bin/env python3
"""Discover candidate Scripture connections from deterministic corpus evidence.

This script only emits candidate RelationshipObject records. It never writes raw
or canonical data and never promotes a discovered edge.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
import itertools
import json
import re
import time
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]

import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.util.canon import testament  # noqa: E402


AGENT_DEFAULT = "codex-5.5"
CREATED_BY_PREFIX = "connection_discoverer"
ALLOWED_DISCOVERY_PREDICATES = {
    "quotesFrom",
    "alludesTo",
    "echoes",
    "fulfills",
    "typifies",
    "parallelTo",
    "thematicallyRelatedTo",
    "groundedIn",
}

BOOK_ORDER = [
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam",
    "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov",
    "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos",
    "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal", "Tob",
    "Jdt", "AddEsth", "Wis", "Sir", "Bar", "1Macc", "2Macc", "AddDan", "1Esd",
    "PrMan", "Ps151", "3Macc", "2Esd", "4Macc", "Matt", "Mark", "Luke", "John",
    "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess",
    "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet",
    "1John", "2John", "3John", "Jude", "Rev",
]
BOOK_RANK = {book: i for i, book in enumerate(BOOK_ORDER)}

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
CITATION_PATTERNS = [
    re.compile(r"\bas it is written\b", re.IGNORECASE),
    re.compile(r"\bit is written\b", re.IGNORECASE),
    re.compile(r"\bthe scripture says\b", re.IGNORECASE),
    re.compile(r"\bscripture says\b", re.IGNORECASE),
    re.compile(r"\bspoken through the prophet\b", re.IGNORECASE),
    re.compile(r"\bspoken by the prophet\b", re.IGNORECASE),
    re.compile(r"\bthat it might be fulfilled which was spoken\b", re.IGNORECASE),
]


@dataclass(frozen=True)
class Witness:
    osis_ref: str
    text: str

    @property
    def book(self) -> str:
        return book_of(self.osis_ref)

    @property
    def testament(self) -> str:
        return testament(self.book)


@dataclass
class Candidate:
    subject_osis: str
    predicate: str
    object_osis: str
    discovery_method: str
    evidence_refs: list[str]
    confidence: float
    method_params: dict[str, Any] = field(default_factory=dict)

    @property
    def key(self) -> tuple[str, str, str]:
        return (f"scripture:{self.subject_osis}", self.predicate, f"scripture:{self.object_osis}")

    def to_record(self, agent: str, created_at: str) -> dict[str, Any]:
        subject_id, predicate, object_id = self.key
        return {
            "id": f"cand:rel:{self.subject_osis}--{predicate}--{self.object_osis}",
            "type": "RelationshipObject",
            "subject_id": subject_id,
            "predicate": predicate,
            "object_id": object_id,
            "assertion_mode": "candidate",
            "discovery_method": self.discovery_method,
            "evidence_refs": sorted(set(self.evidence_refs)),
            "confidence": round(min(1.0, max(0.0, self.confidence)), 3),
            "trust_zone": "candidate",
            "provenance": {
                "created_by": f"{CREATED_BY_PREFIX}:{agent}",
                "created_at": created_at,
                "method": self.discovery_method,
                "params": self.method_params,
            },
            "status": "candidate",
        }


def book_of(osis_ref: str) -> str:
    return osis_ref.split(".", 1)[0]


def osis_sort_key(osis_ref: str) -> tuple[int, int, int, str]:
    parts = osis_ref.split(".")
    book = parts[0]
    chapter = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    verse_digits = "".join(ch for ch in parts[2]) if len(parts) > 2 else ""
    verse = int(verse_digits) if verse_digits.isdigit() else 0
    return (BOOK_RANK.get(book, 999), chapter, verse, osis_ref)


def pair_key(a: str, b: str) -> frozenset[str]:
    return frozenset((a, b))


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower().replace("'", "") for m in WORD_RE.finditer(text)]


def slug(text: str) -> str:
    words = tokenize(text)
    return "-".join(words[:10])


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def load_witnesses(path: Path) -> dict[str, Witness]:
    witnesses: dict[str, Witness] = {}
    for rec in iter_jsonl(path):
        osis = rec.get("osis_ref")
        text = rec.get("text", "")
        if osis and text:
            witnesses[osis] = Witness(osis_ref=osis, text=text)
    return witnesses


def load_editorial_pairs(path: Path) -> set[frozenset[str]]:
    pairs: set[frozenset[str]] = set()
    if not path.exists():
        return pairs
    for rec in iter_jsonl(path):
        source = rec.get("osis_ref")
        if not source:
            continue
        for target in rec.get("candidate_osis_refs", []) or []:
            if target:
                pairs.add(pair_key(source, target))
    return pairs


def load_editorial_sources(path: Path) -> set[str]:
    sources: set[str] = set()
    if not path.exists():
        return sources
    for rec in iter_jsonl(path):
        source = rec.get("osis_ref")
        if source and rec.get("candidate_osis_refs"):
            sources.add(source)
    return sources


def is_editorial_dup(subject_osis: str, object_osis: str, editorial_pairs: set[frozenset[str]]) -> bool:
    return pair_key(subject_osis, object_osis) in editorial_pairs


def phrase_text(tokens: list[str], start: int, n: int) -> str:
    return " ".join(tokens[start : start + n])


def verse_phrases(tokens: list[str], min_n: int, max_n: int) -> set[tuple[str, int]]:
    phrases: set[tuple[str, int]] = set()
    for n in range(min_n, max_n + 1):
        if len(tokens) < n:
            continue
        for i in range(0, len(tokens) - n + 1):
            phrases.add((phrase_text(tokens, i, n), n))
    return phrases


def build_phrase_index(
    witnesses: dict[str, Witness],
    *,
    min_n: int,
    max_n: int,
    max_phrase_df: int,
) -> dict[str, dict[str, Any]]:
    phrase_refs: dict[str, dict[str, Any]] = {}
    for osis, witness in witnesses.items():
        tokens = tokenize(witness.text)
        for phrase, n in verse_phrases(tokens, min_n, max_n):
            entry = phrase_refs.setdefault(phrase, {"n": n, "refs": set(), "testaments": defaultdict(set)})
            entry["refs"].add(osis)
            entry["testaments"][witness.testament].add(osis)

    return {
        phrase: entry
        for phrase, entry in phrase_refs.items()
        if 1 < len(entry["refs"]) <= max_phrase_df
    }


def discover_shared_rare_phrases(
    witnesses: dict[str, Witness],
    editorial_pairs: set[frozenset[str]],
    *,
    min_n: int = 4,
    max_n: int = 7,
    max_phrase_df: int = 3,
    limit: int = 200,
) -> tuple[list[Candidate], dict[str, Any]]:
    phrase_index = build_phrase_index(
        witnesses,
        min_n=min_n,
        max_n=max_n,
        max_phrase_df=max_phrase_df,
    )
    scored: list[tuple[float, Candidate]] = []
    skipped_editorial = 0
    params = {
        "min_n": min_n,
        "max_n": max_n,
        "max_phrase_df": max_phrase_df,
        "limit": limit,
    }
    for phrase, entry in phrase_index.items():
        nt_refs = sorted(entry["testaments"].get("NT", []), key=osis_sort_key)
        ot_refs = sorted(entry["testaments"].get("OT", []), key=osis_sort_key)
        if not nt_refs or not ot_refs:
            continue
        n = int(entry["n"])
        df = len(entry["refs"])
        predicate = "quotesFrom" if n >= 7 else "alludesTo"
        confidence = 0.84 if predicate == "quotesFrom" else 0.72 + min(0.08, (n - min_n) * 0.02)
        rarity_score = n + (1.0 / df)
        for nt_ref in nt_refs:
            for ot_ref in ot_refs:
                if is_editorial_dup(nt_ref, ot_ref, editorial_pairs):
                    skipped_editorial += 1
                    continue
                candidate = Candidate(
                    subject_osis=nt_ref,
                    predicate=predicate,
                    object_osis=ot_ref,
                    discovery_method="shared_rare_phrase",
                    evidence_refs=[f"phrase:{slug(phrase)}", nt_ref, ot_ref],
                    confidence=confidence,
                    method_params=params,
                )
                scored.append((rarity_score, candidate))

    scored.sort(key=lambda item: (-item[0], -item[1].confidence, item[1].subject_osis, item[1].object_osis))
    return [candidate for _, candidate in scored[:limit]], {
        "rare_phrases": len(phrase_index),
        "deduped_editorial_crossrefs": skipped_editorial,
    }


def discover_citation_formulas(
    witnesses: dict[str, Witness],
    editorial_pairs: set[frozenset[str]],
    *,
    editorial_sources: set[str] | None = None,
    min_n: int = 4,
    max_n: int = 7,
    max_phrase_df: int = 4,
    limit: int = 100,
) -> tuple[list[Candidate], dict[str, Any]]:
    phrase_index = build_phrase_index(
        witnesses,
        min_n=min_n,
        max_n=max_n,
        max_phrase_df=max_phrase_df,
    )
    ot_phrase_index = {
        phrase: entry
        for phrase, entry in phrase_index.items()
        if entry["testaments"].get("OT")
    }
    scored: list[tuple[float, Candidate]] = []
    formulas_seen = 0
    skipped_editorial = 0
    skipped_formula_sources = 0
    editorial_sources = editorial_sources or set()
    params = {
        "min_n": min_n,
        "max_n": max_n,
        "max_phrase_df": max_phrase_df,
        "limit": limit,
    }
    for nt_ref, witness in sorted(witnesses.items(), key=lambda item: osis_sort_key(item[0])):
        if witness.testament != "NT":
            continue
        if nt_ref in editorial_sources:
            # If the edition already supplies a cross-reference lead for the
            # formula verse, do not propose weaker alternate formula matches.
            skipped_formula_sources += 1
            continue
        for pattern in CITATION_PATTERNS:
            match = pattern.search(witness.text)
            if not match:
                continue
            formulas_seen += 1
            tail_tokens = tokenize(witness.text[match.end() :])
            for phrase, n in verse_phrases(tail_tokens, min_n, max_n):
                entry = ot_phrase_index.get(phrase)
                if not entry:
                    continue
                for ot_ref in sorted(entry["testaments"]["OT"], key=osis_sort_key):
                    if is_editorial_dup(nt_ref, ot_ref, editorial_pairs):
                        skipped_editorial += 1
                        continue
                    candidate = Candidate(
                        subject_osis=nt_ref,
                        predicate="quotesFrom",
                        object_osis=ot_ref,
                        discovery_method="citation_formula",
                        evidence_refs=[f"formula:{slug(match.group(0))}", f"phrase:{slug(phrase)}", nt_ref, ot_ref],
                        confidence=min(0.95, 0.86 + 0.01 * n),
                        method_params=params,
                    )
                    scored.append((n + 1.0 / len(entry["refs"]), candidate))
    scored.sort(key=lambda item: (-item[0], -item[1].confidence, item[1].subject_osis, item[1].object_osis))
    return [candidate for _, candidate in scored[:limit]], {
        "nt_formula_occurrences": formulas_seen,
        "rare_phrases": len(phrase_index),
        "deduped_editorial_crossrefs": skipped_editorial,
        "skipped_formula_sources_with_editorial_xref": skipped_formula_sources,
    }


def lexical_strong_df(word_tokens_path: Path) -> dict[str, set[str]]:
    strong_refs: dict[str, set[str]] = defaultdict(set)
    for rec in iter_jsonl(word_tokens_path):
        strong = rec.get("strong")
        osis = rec.get("osis_ref")
        if strong and osis:
            strong_refs[str(strong)].add(str(osis))
    return strong_refs


def discover_lexical_cooccurrence(
    word_tokens_path: Path,
    editorial_pairs: set[frozenset[str]],
    *,
    rare_df_max: int = 6,
    min_shared_lemmas: int = 2,
    limit: int = 150,
) -> tuple[list[Candidate], dict[str, Any]]:
    strong_refs = lexical_strong_df(word_tokens_path)
    rare = {
        strong: sorted(refs, key=osis_sort_key)
        for strong, refs in strong_refs.items()
        if 1 < len(refs) <= rare_df_max
    }
    pair_to_strongs: dict[tuple[str, str], set[str]] = defaultdict(set)
    skipped_editorial = 0
    for strong, refs in sorted(rare.items()):
        for a, b in itertools.combinations(refs, 2):
            if is_editorial_dup(a, b, editorial_pairs):
                skipped_editorial += 1
                continue
            a_book = book_of(a)
            b_book = book_of(b)
            if a_book == b_book:
                a_ch = osis_sort_key(a)[1]
                b_ch = osis_sort_key(b)[1]
                if abs(a_ch - b_ch) <= 1:
                    continue
            first, second = sorted((a, b), key=osis_sort_key)
            pair_to_strongs[(second, first)].add(strong)

    scored: list[tuple[float, Candidate]] = []
    params = {
        "rare_df_max": rare_df_max,
        "min_shared_lemmas": min_shared_lemmas,
        "limit": limit,
    }
    for (subject, obj), shared in pair_to_strongs.items():
        if len(shared) < min_shared_lemmas:
            continue
        rarity = sum(1.0 / len(strong_refs[s]) for s in shared)
        confidence = min(0.7, 0.45 + 0.08 * len(shared) + min(0.15, rarity))
        candidate = Candidate(
            subject_osis=subject,
            predicate="thematicallyRelatedTo",
            object_osis=obj,
            discovery_method="lexical_cooccurrence",
            evidence_refs=[f"strong:{s}" for s in sorted(shared)],
            confidence=confidence,
            method_params=params,
        )
        scored.append((rarity, candidate))
    scored.sort(key=lambda item: (-item[0], -item[1].confidence, item[1].subject_osis, item[1].object_osis))
    return [candidate for _, candidate in scored[:limit]], {
        "strong_total": len(strong_refs),
        "rare_strong_total": len(rare),
        "pair_total_before_min_shared": len(pair_to_strongs),
        "deduped_editorial_crossrefs": skipped_editorial,
    }


def merge_candidates(candidates: Iterable[Candidate]) -> list[Candidate]:
    merged: dict[tuple[str, str, str], Candidate] = {}
    for candidate in candidates:
        key = (candidate.subject_osis, candidate.predicate, candidate.object_osis)
        existing = merged.get(key)
        if existing is None:
            merged[key] = candidate
            continue
        existing.evidence_refs = sorted(set(existing.evidence_refs) | set(candidate.evidence_refs))
        existing.confidence = max(existing.confidence, candidate.confidence)
        if candidate.discovery_method not in existing.discovery_method.split("+"):
            existing.discovery_method = "+".join(sorted(set(existing.discovery_method.split("+") + [candidate.discovery_method])))
        existing.method_params = {**existing.method_params, candidate.discovery_method: candidate.method_params}
    return sorted(merged.values(), key=lambda c: (-c.confidence, c.subject_osis, c.predicate, c.object_osis))


def validate_candidate_record(record: dict[str, Any], registry_predicates: set[str] | None = None) -> None:
    if record.get("assertion_mode") != "candidate":
        raise ValueError(f"{record.get('id')}: assertion_mode must be candidate")
    if record.get("status") != "candidate":
        raise ValueError(f"{record.get('id')}: status must be candidate")
    if record.get("trust_zone") != "candidate":
        raise ValueError(f"{record.get('id')}: trust_zone must be candidate")
    if not record.get("evidence_refs"):
        raise ValueError(f"{record.get('id')}: evidence_refs required")
    predicate = record.get("predicate")
    allowed = registry_predicates or ALLOWED_DISCOVERY_PREDICATES
    if predicate not in allowed:
        raise ValueError(f"{record.get('id')}: unregistered predicate {predicate}")


def load_registry_predicates(path: Path) -> set[str]:
    try:
        import yaml
    except ImportError:
        return set(ALLOWED_DISCOVERY_PREDICATES)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return set((data.get("predicates") or {}).keys()) & ALLOWED_DISCOVERY_PREDICATES


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml
    except ImportError:
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return
    path.write_text(yaml.safe_dump(manifest, sort_keys=True), encoding="utf-8")


def write_report(path: Path, records: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter(record["predicate"] for record in records)
    methods = Counter(record.get("discovery_method", "") for record in records)
    lines = [
        "# Connection Discovery Report",
        "",
        f"- Agent: `{manifest['agent']}`",
        f"- Created: `{manifest['created_at']}`",
        f"- Candidates emitted: **{len(records)}**",
        f"- Dropped as editorial cross-reference duplicates: **{manifest['deduped_editorial_crossrefs']}**",
        "",
        "## Predicate Counts",
        "",
    ]
    for predicate, count in sorted(counts.items()):
        lines.append(f"- `{predicate}`: {count}")
    lines.extend(["", "## Method Counts", ""])
    for method, count in sorted(methods.items()):
        lines.append(f"- `{method}`: {count}")
    lines.extend(["", "## Top 30 Candidates", ""])
    for record in sorted(records, key=lambda r: (-r["confidence"], r["subject_id"], r["predicate"], r["object_id"]))[:30]:
        evidence = ", ".join(record["evidence_refs"][:4])
        lines.append(
            f"- `{record['subject_id']}` `{record['predicate']}` `{record['object_id']}` "
            f"confidence={record['confidence']} evidence={evidence}"
        )
    lines.extend([
        "",
        "## False-Positive Notes",
        "",
        "- English surface phrase overlap can catch repeated liturgical or legal formulae that are not quotations.",
        "- Lexical co-occurrence is capped and requires two rare Strong's ids, but it still indicates a thematic lead rather than a claim.",
        "- Citation-formula candidates require both a trigger phrase and rare phrase overlap; unmatched formulas are intentionally dropped.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def run_discovery(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    started = time.perf_counter()
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    editorial_pairs = load_editorial_pairs(Path(args.crossrefs))
    editorial_sources = load_editorial_sources(Path(args.crossrefs))
    witnesses = load_witnesses(Path(args.witnesses))

    method_outputs: dict[str, dict[str, Any]] = {}
    all_candidates: list[Candidate] = []

    before = len(all_candidates)
    phrase_candidates, phrase_stats = discover_shared_rare_phrases(
        witnesses,
        editorial_pairs,
        min_n=args.min_ngram,
        max_n=args.max_ngram,
        max_phrase_df=args.max_phrase_df,
        limit=args.phrase_limit,
    )
    all_candidates.extend(phrase_candidates)
    method_outputs["shared_rare_phrase"] = {"emitted_before_merge": len(all_candidates) - before, **phrase_stats}

    before = len(all_candidates)
    formula_candidates, formula_stats = discover_citation_formulas(
        witnesses,
        editorial_pairs,
        editorial_sources=editorial_sources,
        min_n=args.min_ngram,
        max_n=args.max_ngram,
        max_phrase_df=args.citation_max_phrase_df,
        limit=args.citation_limit,
    )
    all_candidates.extend(formula_candidates)
    method_outputs["citation_formula"] = {"emitted_before_merge": len(all_candidates) - before, **formula_stats}

    before = len(all_candidates)
    lexical_candidates, lexical_stats = discover_lexical_cooccurrence(
        Path(args.word_tokens),
        editorial_pairs,
        rare_df_max=args.rare_strong_df_max,
        min_shared_lemmas=args.min_shared_lemmas,
        limit=args.lexical_limit,
    )
    all_candidates.extend(lexical_candidates)
    method_outputs["lexical_cooccurrence"] = {"emitted_before_merge": len(all_candidates) - before, **lexical_stats}

    merged = merge_candidates(all_candidates)
    registry_predicates = load_registry_predicates(Path(args.predicate_registry))
    records = [candidate.to_record(args.agent, created_at) for candidate in merged[: args.total_limit]]
    for record in records:
        validate_candidate_record(record, registry_predicates)

    emitted_pairs = {pair_key(r["subject_id"].removeprefix("scripture:"), r["object_id"].removeprefix("scripture:")) for r in records}
    deduped_editorial = sum(stats.get("deduped_editorial_crossrefs", 0) for stats in method_outputs.values())
    manifest = {
        "agent": args.agent,
        "created_at": created_at,
        "inputs": {
            "word_tokens": str(args.word_tokens),
            "witnesses": str(args.witnesses),
            "crossrefs": str(args.crossrefs),
        },
        "methods": {
            "lexical_cooccurrence": {
                "rare_df_max": args.rare_strong_df_max,
                "min_shared_lemmas": args.min_shared_lemmas,
                "limit": args.lexical_limit,
            },
            "shared_rare_phrase": {
                "min_n": args.min_ngram,
                "max_n": args.max_ngram,
                "max_phrase_df": args.max_phrase_df,
                "limit": args.phrase_limit,
            },
            "citation_formula": {
                "min_n": args.min_ngram,
                "max_n": args.max_ngram,
                "max_phrase_df": args.citation_max_phrase_df,
                "limit": args.citation_limit,
            },
        },
        "method_stats": method_outputs,
        "total_candidates": len(records),
        "breakdown_by_predicate": dict(sorted(Counter(r["predicate"] for r in records).items())),
        "deduped_editorial_crossrefs": deduped_editorial,
        "editorial_crossref_pairs_loaded": len(editorial_pairs),
        "emitted_pairs": len(emitted_pairs),
        "runtime_seconds": round(time.perf_counter() - started, 3),
    }
    return records, manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--word-tokens", default=str(ROOT / "data/canonical/translations/eng-web/word_tokens.jsonl"))
    parser.add_argument("--witnesses", default=str(ROOT / "data/canonical/translations/eng-web/translation_witnesses.jsonl"))
    parser.add_argument("--crossrefs", default=str(ROOT / "data/canonical/translations/eng-web/editorial_cross_references.jsonl"))
    parser.add_argument("--predicate-registry", default=str(ROOT / "config/governance/predicate_registry.yaml"))
    parser.add_argument("--agent", default=AGENT_DEFAULT)
    today = datetime.now(timezone.utc).date().isoformat()
    parser.add_argument("--out", default=str(ROOT / f"data/candidate/connections/{AGENT_DEFAULT}-{today}.jsonl"))
    parser.add_argument("--manifest", default=str(ROOT / f"data/candidate/connections/{AGENT_DEFAULT}-{today}.manifest.yaml"))
    parser.add_argument("--report", default=str(ROOT / f"build/discovery/{AGENT_DEFAULT}-report.md"))
    parser.add_argument("--rare-strong-df-max", type=int, default=6)
    parser.add_argument("--min-shared-lemmas", type=int, default=2)
    parser.add_argument("--lexical-limit", type=int, default=150)
    parser.add_argument("--min-ngram", type=int, default=4)
    parser.add_argument("--max-ngram", type=int, default=7)
    parser.add_argument("--max-phrase-df", type=int, default=3)
    parser.add_argument("--phrase-limit", type=int, default=200)
    parser.add_argument("--citation-max-phrase-df", type=int, default=4)
    parser.add_argument("--citation-limit", type=int, default=100)
    parser.add_argument("--total-limit", type=int, default=350)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    records, manifest = run_discovery(args)
    write_jsonl(Path(args.out), records)
    write_manifest(Path(args.manifest), manifest)
    write_report(Path(args.report), records, manifest)
    print(f"Wrote {len(records)} candidates to {args.out}")
    print(f"Wrote manifest to {args.manifest}")
    print(f"Wrote report to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
