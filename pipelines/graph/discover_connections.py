#!/usr/bin/env python3
"""Discover conservative candidate intertextual connections for human review.

The script is intentionally deterministic and candidate-only. It writes no raw or
canonical files; all discovered edges are RelationshipObject JSONL records under
``data/candidate`` with concrete evidence refs and provenance.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:  # scripts are run directly from the repo root
    from pipelines.util.canon import testament
except ModuleNotFoundError:  # pragma: no cover - convenience for direct execution elsewhere
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from pipelines.util.canon import testament

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_PREDICATES = {
    "quotesFrom",
    "alludesTo",
    "echoes",
    "fulfills",
    "typifies",
    "parallelTo",
    "thematicallyRelatedTo",
    "groundedIn",
}
DEFAULT_AGENT = "codex-5.5"
TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
CITATION_FORMULAS = (
    "as it is written",
    "it is written",
    "the scripture says",
    "scripture says",
    "spoken through the prophet",
    "spoken by the prophet",
    "that it might be fulfilled",
    "that which was spoken",
)
STOP_PHRASE_TOKENS = {
    "the", "and", "that", "this", "with", "from", "have", "will", "shall", "your",
    "you", "for", "are", "was", "were", "his", "her", "their", "not", "but", "all",
    "they", "them", "him", "she", "who", "what", "when", "where", "there", "then",
}
GENERIC_PHRASE_FRAGMENTS = (
    "it is written",
    "as it is written",
    "is written in",
    "the book of",
    "book of the",
    "the law of",
    "law of moses",
)


@dataclass(frozen=True)
class VerseText:
    osis_ref: str
    passage_id: str
    text: str
    tokens: tuple[str, ...]
    testament: str


@dataclass
class Candidate:
    subject_osis: str
    predicate: str
    object_osis: str
    discovery_method: str
    evidence_refs: list[str]
    confidence: float
    method: str
    params: dict[str, object] = field(default_factory=dict)
    score: float = 0.0

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.subject_osis, self.predicate, self.object_osis)


def book_from_osis(osis_ref: str) -> str:
    return osis_ref.split(".", 1)[0]


def scripture_id(osis_ref: str) -> str:
    return f"scripture:{osis_ref}"


def normalize_tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def load_witnesses(path: Path) -> dict[str, VerseText]:
    verses: dict[str, VerseText] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rec = json.loads(line)
            osis = rec["osis_ref"]
            book = book_from_osis(osis)
            verses[osis] = VerseText(
                osis_ref=osis,
                passage_id=rec.get("passage_id", scripture_id(osis)),
                text=rec.get("text", ""),
                tokens=tuple(normalize_tokens(rec.get("text", ""))),
                testament=testament(book),
            )
    return verses


def load_editorial_crossref_pairs(path: Path) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    if not path.exists():
        return pairs
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rec = json.loads(line)
            src = rec.get("osis_ref")
            if not src:
                continue
            for target in rec.get("candidate_osis_refs") or []:
                pairs.add((src, target))
                pairs.add((target, src))
    return pairs


def is_valid_candidate_direction(candidate: Candidate, verses: dict[str, VerseText]) -> bool:
    if verses.get(candidate.subject_osis) is None or verses.get(candidate.object_osis) is None:
        return False
    if candidate.method in {"shared_rare_phrase", "citation_formula"}:
        return verses[candidate.subject_osis].testament == "NT" and verses[candidate.object_osis].testament == "OT"
    return candidate.subject_osis != candidate.object_osis


def is_deduped(candidate: Candidate, editorial_pairs: set[tuple[str, str]]) -> bool:
    return (candidate.subject_osis, candidate.object_osis) in editorial_pairs


def relationship_id(subject_osis: str, predicate: str, object_osis: str) -> str:
    return f"cand:rel:{subject_osis}--{predicate}--{object_osis}"


def candidate_to_record(candidate: Candidate, agent: str, created_at: str) -> dict[str, object]:
    assert candidate.predicate in ALLOWED_PREDICATES
    return {
        "id": relationship_id(candidate.subject_osis, candidate.predicate, candidate.object_osis),
        "type": "RelationshipObject",
        "subject_id": scripture_id(candidate.subject_osis),
        "predicate": candidate.predicate,
        "object_id": scripture_id(candidate.object_osis),
        "assertion_mode": "candidate",
        "discovery_method": candidate.discovery_method,
        "evidence_refs": candidate.evidence_refs,
        "confidence": round(max(0.0, min(1.0, candidate.confidence)), 3),
        "trust_zone": "candidate",
        "provenance": {
            "created_by": f"connection_discoverer:{agent}",
            "created_at": created_at,
            "method": candidate.method,
            "params": candidate.params,
        },
        "status": "candidate",
    }


def discover_lexical_cooccurrence(
    word_tokens_path: Path,
    verses: dict[str, VerseText],
    *,
    rare_df_max: int = 6,
    min_shared_strongs: int = 2,
    max_candidates: int = 250,
) -> list[Candidate]:
    """Propose NT->OT thematic candidates sharing multiple rare Strong's ids."""
    strong_to_verses: dict[str, set[str]] = defaultdict(set)
    with word_tokens_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rec = json.loads(line)
            strong = rec.get("strong") or (rec.get("attributes") or {}).get("strong")
            osis = rec.get("osis_ref")
            if strong and osis in verses:
                strong_to_verses[str(strong)].add(osis)

    rare = {s: refs for s, refs in strong_to_verses.items() if 1 < len(refs) <= rare_df_max}
    pair_to_strongs: dict[tuple[str, str], set[str]] = defaultdict(set)
    for strong, refs in rare.items():
        refs_sorted = sorted(refs)
        for i, left in enumerate(refs_sorted):
            for right in refs_sorted[i + 1:]:
                if book_from_osis(left) == book_from_osis(right):
                    continue
                pair_to_strongs[(left, right)].add(strong)

    candidates: list[Candidate] = []
    for (nt, ot), strongs in pair_to_strongs.items():
        if len(strongs) < min_shared_strongs:
            continue
        sorted_strongs = sorted(strongs, key=lambda s: (len(rare[s]), s))
        rarity_score = sum(1.0 / len(rare[s]) for s in sorted_strongs)
        confidence = min(0.72, 0.42 + 0.08 * len(sorted_strongs) + min(0.12, rarity_score / 8))
        candidates.append(Candidate(
            subject_osis=nt,
            predicate="thematicallyRelatedTo",
            object_osis=ot,
            discovery_method="lexical_strongs_cooccurrence",
            evidence_refs=[f"strong:{s}:df={len(rare[s])}" for s in sorted_strongs[:8]] + [nt, ot],
            confidence=confidence,
            method="lexical_cooccurrence",
            params={"rare_df_max": rare_df_max, "min_shared_strongs": min_shared_strongs},
            score=rarity_score + len(sorted_strongs),
        ))
    return sorted(candidates, key=lambda c: (-c.score, c.subject_osis, c.object_osis))[:max_candidates]


def iter_ngrams(tokens: tuple[str, ...], n_min: int, n_max: int) -> Iterable[tuple[str, ...]]:
    for n in range(n_min, n_max + 1):
        if len(tokens) < n:
            continue
        for i in range(0, len(tokens) - n + 1):
            phrase = tokens[i:i+n]
            phrase_text = " ".join(phrase)
            if any(fragment in phrase_text for fragment in GENERIC_PHRASE_FRAGMENTS):
                continue
            if sum(1 for t in phrase if t not in STOP_PHRASE_TOKENS) < 3:
                continue
            yield phrase


def build_phrase_index(
    verses: dict[str, VerseText],
    *,
    n_min: int = 4,
    n_max: int = 7,
    max_occurrences: int = 4,
) -> dict[tuple[str, ...], list[str]]:
    occurrences: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for osis, verse in verses.items():
        if verse.testament not in {"OT", "NT"}:
            continue
        for phrase in set(iter_ngrams(verse.tokens, n_min, n_max)):
            occurrences[phrase].add(osis)
    return {
        phrase: sorted(refs)
        for phrase, refs in occurrences.items()
        if 1 < len(refs) <= max_occurrences
    }


def discover_shared_rare_phrase(
    verses: dict[str, VerseText],
    *,
    n_min: int = 4,
    n_max: int = 7,
    max_phrase_occurrences: int = 4,
    max_candidates: int = 250,
) -> list[Candidate]:
    phrase_index = build_phrase_index(verses, n_min=n_min, n_max=n_max, max_occurrences=max_phrase_occurrences)
    best: dict[tuple[str, str], dict[str, object]] = {}
    for phrase, refs in phrase_index.items():
        ots = [r for r in refs if verses[r].testament == "OT"]
        nts = [r for r in refs if verses[r].testament == "NT"]
        if not ots or not nts:
            continue
        phrase_text = " ".join(phrase)
        for nt in nts:
            for ot in ots:
                key = (nt, ot)
                entry = best.setdefault(key, {"phrases": [], "score": 0.0})
                entry["phrases"].append((len(phrase), phrase_text, len(refs)))
                entry["score"] = float(entry["score"]) + len(phrase) / len(refs)

    candidates: list[Candidate] = []
    for (nt, ot), entry in best.items():
        phrases = sorted(entry["phrases"], key=lambda x: (-x[0], x[1]))
        longest = phrases[0][0]
        evidence_phrases = []
        seen = set()
        for _, text, occ in phrases:
            if text in seen:
                continue
            seen.add(text)
            evidence_phrases.append(f"phrase:{text}:occ={occ}")
            if len(evidence_phrases) >= 3:
                break
        predicate = "quotesFrom" if longest >= 7 or len(evidence_phrases) >= 2 else "alludesTo"
        confidence = min(0.86, 0.50 + 0.045 * longest + 0.05 * (len(evidence_phrases) - 1))
        candidates.append(Candidate(
            subject_osis=nt,
            predicate=predicate,
            object_osis=ot,
            discovery_method="shared_rare_phrase",
            evidence_refs=evidence_phrases + [nt, ot],
            confidence=confidence,
            method="shared_rare_phrase",
            params={"n_min": n_min, "n_max": n_max, "max_phrase_occurrences": max_phrase_occurrences},
            score=float(entry["score"]),
        ))
    return sorted(candidates, key=lambda c: (-c.score, c.subject_osis, c.object_osis))[:max_candidates]


def has_citation_formula(text: str) -> str | None:
    lower = text.lower()
    for formula in CITATION_FORMULAS:
        if formula in lower:
            return formula
    return None


def tokens_after_formula(text: str, formula: str) -> tuple[str, ...]:
    lower = text.lower()
    index = lower.find(formula)
    if index < 0:
        return tuple(normalize_tokens(text))
    return tuple(normalize_tokens(text[index + len(formula):]))


def discover_citation_formula(
    verses: dict[str, VerseText],
    *,
    n_min: int = 4,
    n_max: int = 9,
    max_phrase_occurrences: int = 6,
    max_candidates: int = 150,
) -> list[Candidate]:
    phrase_index = build_phrase_index(verses, n_min=n_min, n_max=n_max, max_occurrences=max_phrase_occurrences)
    candidates: list[Candidate] = []
    for nt, verse in sorted(verses.items()):
        if verse.testament != "NT":
            continue
        formula = has_citation_formula(verse.text)
        if not formula:
            continue
        trailing_tokens = tokens_after_formula(verse.text, formula)
        matches: dict[str, list[tuple[int, str, int]]] = defaultdict(list)
        for phrase in set(iter_ngrams(trailing_tokens, n_min, n_max)):
            refs = phrase_index.get(phrase)
            if not refs:
                continue
            for ot in refs:
                if verses[ot].testament == "OT":
                    matches[ot].append((len(phrase), " ".join(phrase), len(refs)))
        for ot, phrases in matches.items():
            phrases = sorted(phrases, key=lambda x: (-x[0], x[1]))
            longest = phrases[0][0]
            evidence = [f"formula:{formula}"]
            seen = set()
            for _, text, occ in phrases:
                if text in seen:
                    continue
                seen.add(text)
                evidence.append(f"phrase:{text}:occ={occ}")
                if len(evidence) >= 4:
                    break
            confidence = min(0.93, 0.68 + 0.025 * longest + 0.04 * (len(evidence) - 2))
            candidates.append(Candidate(
                subject_osis=nt,
                predicate="quotesFrom",
                object_osis=ot,
                discovery_method="citation_formula_phrase_match",
                evidence_refs=evidence + [nt, ot],
                confidence=confidence,
                method="citation_formula",
                params={"n_min": n_min, "n_max": n_max, "max_phrase_occurrences": max_phrase_occurrences},
                score=confidence + longest / 10,
            ))
    return sorted(candidates, key=lambda c: (-c.score, c.subject_osis, c.object_osis))[:max_candidates]


def merge_candidates(candidates: Iterable[Candidate], editorial_pairs: set[tuple[str, str]], verses: dict[str, VerseText], max_total: int) -> tuple[list[Candidate], int, int]:
    by_key: dict[tuple[str, str, str], Candidate] = {}
    deduped = 0
    invalid_direction = 0
    predicate_rank = {"quotesFrom": 4, "alludesTo": 3, "echoes": 2, "thematicallyRelatedTo": 1}
    for cand in candidates:
        if not is_valid_candidate_direction(cand, verses):
            invalid_direction += 1
            continue
        if is_deduped(cand, editorial_pairs):
            deduped += 1
            continue
        existing = by_key.get(cand.key)
        if existing is None or (cand.confidence, predicate_rank.get(cand.predicate, 0), cand.score) > (existing.confidence, predicate_rank.get(existing.predicate, 0), existing.score):
            by_key[cand.key] = cand
    merged = sorted(by_key.values(), key=lambda c: (-c.confidence, -c.score, c.subject_osis, c.predicate, c.object_osis))
    return merged[:max_total], deduped, invalid_direction


def write_jsonl(records: Iterable[dict[str, object]], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            count += 1
    return count


def write_manifest(path: Path, *, agent: str, created_at: str, out: Path, report: Path, counts: dict[str, object], params: dict[str, object], runtime_seconds: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Hand-written YAML subset to keep dependencies optional.
    lines = [
        "version: 1",
        f"agent: {agent}",
        f"created_at: {created_at}",
        f"output: {out.as_posix()}",
        f"report: {report.as_posix()}",
        f"runtime_seconds: {runtime_seconds:.3f}",
        "methods:",
    ]
    for name, method_params in params.items():
        lines.append(f"  {name}:")
        for key, value in method_params.items():
            lines.append(f"    {key}: {value}")
    lines.append("counts:")
    for key, value in counts.items():
        if isinstance(value, dict):
            lines.append(f"  {key}:")
            for k2, v2 in value.items():
                lines.append(f"    {k2}: {v2}")
        else:
            lines.append(f"  {key}: {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(path: Path, *, agent: str, created_at: str, records: list[dict[str, object]], counts: dict[str, object], params: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_predicate = Counter(r["predicate"] for r in records)
    by_method = Counter(r["discovery_method"] for r in records)
    lines = [
        f"# Connection discovery report — {agent}",
        "",
        f"Generated: {created_at}",
        "",
        "## Summary",
        "",
        f"- Total emitted candidates: {len(records)}",
        f"- Dropped as existing editorial `\\x`: {counts.get('deduped_editorial_crossrefs', 0)}",
        f"- Dropped for non NT→OT direction: {counts.get('dropped_non_nt_to_ot', 0)}",
        "- Assertion mode/status/trust zone: candidate/candidate/candidate for every emitted edge.",
        "",
        "## Parameters",
        "",
    ]
    for method, method_params in params.items():
        lines.append(f"- {method}: " + ", ".join(f"{k}={v}" for k, v in method_params.items()))
    lines.extend(["", "## Breakdown by predicate", ""])
    for pred, count in sorted(by_predicate.items()):
        lines.append(f"- {pred}: {count}")
    lines.extend(["", "## Breakdown by method", ""])
    for method, count in sorted(by_method.items()):
        lines.append(f"- {method}: {count}")
    lines.extend(["", "## Top 30 by confidence", ""])
    lines.append("| # | confidence | subject | predicate | object | evidence |")
    lines.append("|---|------------|---------|-----------|--------|----------|")
    for i, rec in enumerate(records[:30], start=1):
        evidence = "; ".join(str(e) for e in rec.get("evidence_refs", [])[:4])
        lines.append(f"| {i} | {rec['confidence']} | {rec['subject_id']} | {rec['predicate']} | {rec['object_id']} | {evidence} |")
    lines.extend([
        "",
        "## False-positive notes",
        "",
        "- Shared English phrases can reflect translation style rather than source-text dependence; exact phrase candidates stay candidate-only.",
        "- Lexical Strong's co-occurrence is capped to rare multi-lemma bridges and emitted as thematicallyRelatedTo only.",
        "- Citation formulas are linked only when the formula verse also shares a rare phrase with an OT verse.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_discovery(args: argparse.Namespace) -> tuple[list[dict[str, object]], dict[str, object]]:
    started = time.perf_counter()
    verses = load_witnesses(Path(args.witnesses))
    editorial_pairs = load_editorial_crossref_pairs(Path(args.crossrefs))
    params = {
        "lexical_cooccurrence": {"rare_df_max": args.lexical_rare_df_max, "min_shared_strongs": args.lexical_min_shared_strongs, "max_candidates": args.lexical_max_candidates},
        "shared_rare_phrase": {"n_min": args.phrase_n_min, "n_max": args.phrase_n_max, "max_phrase_occurrences": args.phrase_max_occurrences, "max_candidates": args.phrase_max_candidates},
        "citation_formula": {"n_min": args.citation_n_min, "n_max": args.citation_n_max, "max_phrase_occurrences": args.citation_max_occurrences, "max_candidates": args.citation_max_candidates},
    }
    lexical = discover_lexical_cooccurrence(Path(args.word_tokens), verses, rare_df_max=args.lexical_rare_df_max, min_shared_strongs=args.lexical_min_shared_strongs, max_candidates=args.lexical_max_candidates)
    phrases = discover_shared_rare_phrase(verses, n_min=args.phrase_n_min, n_max=args.phrase_n_max, max_phrase_occurrences=args.phrase_max_occurrences, max_candidates=args.phrase_max_candidates)
    citations = discover_citation_formula(verses, n_min=args.citation_n_min, n_max=args.citation_n_max, max_phrase_occurrences=args.citation_max_occurrences, max_candidates=args.citation_max_candidates)
    merged, deduped, invalid_direction = merge_candidates([*citations, *phrases, *lexical], editorial_pairs, verses, args.max_total_candidates)
    created_at = args.created_at or datetime.now(timezone.utc).date().isoformat()
    records = [candidate_to_record(c, args.agent, created_at) for c in merged]
    emitted = write_jsonl(records, Path(args.out))
    counts: dict[str, object] = {
        "total_candidates": emitted,
        "raw_by_method": {"lexical_cooccurrence": len(lexical), "shared_rare_phrase": len(phrases), "citation_formula": len(citations)},
        "by_predicate": dict(Counter(r["predicate"] for r in records)),
        "deduped_editorial_crossrefs": deduped,
        "dropped_non_nt_to_ot": invalid_direction,
        "verses_loaded": len(verses),
    }
    runtime = time.perf_counter() - started
    write_manifest(Path(args.manifest), agent=args.agent, created_at=created_at, out=Path(args.out), report=Path(args.report), counts=counts, params=params, runtime_seconds=runtime)
    write_report(Path(args.report), agent=args.agent, created_at=created_at, records=records, counts=counts, params=params)
    return records, counts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--word-tokens", required=True)
    parser.add_argument("--witnesses", required=True)
    parser.add_argument("--crossrefs", required=True)
    parser.add_argument("--agent", default=DEFAULT_AGENT)
    parser.add_argument("--out", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--created-at", default="")
    parser.add_argument("--max-total-candidates", type=int, default=500)
    parser.add_argument("--lexical-rare-df-max", type=int, default=6)
    parser.add_argument("--lexical-min-shared-strongs", type=int, default=2)
    parser.add_argument("--lexical-max-candidates", type=int, default=250)
    parser.add_argument("--phrase-n-min", type=int, default=4)
    parser.add_argument("--phrase-n-max", type=int, default=7)
    parser.add_argument("--phrase-max-occurrences", type=int, default=2)
    parser.add_argument("--phrase-max-candidates", type=int, default=250)
    parser.add_argument("--citation-n-min", type=int, default=4)
    parser.add_argument("--citation-n-max", type=int, default=9)
    parser.add_argument("--citation-max-occurrences", type=int, default=3)
    parser.add_argument("--citation-max-candidates", type=int, default=150)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    records, counts = run_discovery(args)
    print(f"Wrote {len(records)} candidate connections to {args.out}")
    print(f"Dropped {counts['deduped_editorial_crossrefs']} existing editorial cross-reference candidate(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
