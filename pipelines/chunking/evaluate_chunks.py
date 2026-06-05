#!/usr/bin/env python3
"""Deterministic A/B evaluation harness for chunking variants.

Scores one or more chunks.jsonl files against the EVALUATION_PLAN metrics and
prints a side-by-side comparison. Variant-agnostic: it does not care who produced
the chunks (a config variant, a different agent, a different model) — it just
measures them. This is the objective half of multi-agent A/B testing; independent
agent review is the qualitative half (see docs/chunking/EXECUTION_PLAN.md).

Usage:
  python pipelines/chunking/evaluate_chunks.py A=build/ab/A.jsonl B=build/ab/B.jsonl \
      [--report build/ab/report.md] [--json build/ab/scores.json]

Metrics (per variant):
  chunks                  total chunk count
  tokens p50/p90/max      approx word-count distribution
  sentence_integrity      % prose chunks ending on a sentence (higher better)
  psalms_fragmented       legacy alias for literal_psalms_fragmented (lower better)
  literal_psalms_fragmented
                          # literal Psalms split into >1 chunk, by book+chapter
  poetry_books_fragmented # poetry/psalm-genre books split into >1 chunk, by book+chapter
  psalm119_section_chunks # explicit non-penalty signal for intentional Ps 119 sections
  book_crossings          # chunks spanning >1 book (must be 0)
  boundary_basis_cov      % chunks with >=1 boundary basis
  metadata_carry          % chunks carrying footnote/crossref refs OR lexeme flag
  gold: psalm23_one       Psalm 23 is exactly one chunk (gold check)
  gold: gen1_no_midsent   Genesis 1 region chunks all sentence-complete
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

SENTENCE_END_RE = re.compile(r"[.!?][\"')\]”’»›]*$")
RAW_USFM = re.compile(r"\\(?:\+?[A-Za-z0-9]+)\*?")
INTENTIONAL_SECTION_CHAPTERS = {("Ps", "119")}


def approx_tokens(text: str) -> int:
    return max(1, len(text.split()))


def sentence_ended(text: str) -> bool:
    return bool(SENTENCE_END_RE.search(text.strip()))


def book_of(osis: str) -> str:
    return (osis or "").split(".")[0]


def book_chapter_of(osis: str) -> tuple[str, str]:
    parts = (osis or "").split(".")
    book = parts[0] if parts and parts[0] else "?"
    chapter = parts[1] if len(parts) > 1 and parts[1] else "?"
    return book, chapter


def fragmented_book_chapters(chunks: list[dict], *, literal_psalms_only: bool) -> dict[tuple[str, str], int]:
    grouped: dict[tuple[str, str], int] = {}
    for c in chunks:
        book, chapter = book_chapter_of(c.get("osis_start", ""))
        if (book, chapter) in INTENTIONAL_SECTION_CHAPTERS:
            continue
        if literal_psalms_only:
            qualifies = book == "Ps"
        else:
            qualifies = c.get("genre") == "psalms" or book == "Ps"
        if qualifies:
            key = (book, chapter)
            grouped[key] = grouped.get(key, 0) + 1
    return {key: count for key, count in grouped.items() if count > 1}


def load(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def score(chunks: list[dict]) -> dict:
    n = len(chunks)
    toks = [approx_tokens(c.get("text", "")) for c in chunks]
    prose = [c for c in chunks if c.get("genre") != "psalms"]
    prose_ok = sum(1 for c in prose if c.get("validation", {}).get("sentence_ended", sentence_ended(c.get("text", ""))))
    literal_psalms_fragmented = len(fragmented_book_chapters(chunks, literal_psalms_only=True))
    poetry_books_fragmented = len(fragmented_book_chapters(chunks, literal_psalms_only=False))
    ps119_section_chunks = sum(1 for c in chunks if book_chapter_of(c.get("osis_start", "")) == ("Ps", "119"))
    crossings = sum(1 for c in chunks if book_of(c.get("osis_start", "")) != book_of(c.get("osis_end", "")))
    basis_cov = sum(1 for c in chunks if c.get("boundary_basis"))
    meta = sum(1 for c in chunks if c.get("footnote_refs") or c.get("editorial_crossref_refs") or c.get("has_lexeme_alignment"))
    leaks = sum(1 for c in chunks if RAW_USFM.search(c.get("text", "")))
    ps23 = [c for c in chunks if c.get("osis_start", "").startswith("Ps.23.") or c.get("osis_end", "").startswith("Ps.23.")]
    gen1 = [c for c in chunks if c.get("osis_start", "").startswith("Gen.1.") or c.get("osis_end", "").startswith("Gen.1.")]
    gen1_ok = all(c.get("validation", {}).get("sentence_ended", sentence_ended(c.get("text", ""))) for c in gen1) if gen1 else None
    return {
        "chunks": n,
        "tok_p50": int(statistics.median(toks)) if toks else 0,
        "tok_p90": int(sorted(toks)[int(0.9 * (len(toks) - 1))]) if toks else 0,
        "tok_max": max(toks) if toks else 0,
        "sentence_integrity_pct": round(100 * prose_ok / len(prose), 1) if prose else 100.0,
        "psalms_fragmented": literal_psalms_fragmented,
        "literal_psalms_fragmented": literal_psalms_fragmented,
        "poetry_books_fragmented": poetry_books_fragmented,
        "psalm119_section_chunks": ps119_section_chunks,
        "book_crossings": crossings,
        "usfm_leaks": leaks,
        "boundary_basis_cov_pct": round(100 * basis_cov / n, 1) if n else 0.0,
        "metadata_carry_pct": round(100 * meta / n, 1) if n else 0.0,
        "gold_psalm23_one_chunk": (len(ps23) == 1),
        "gold_gen1_no_midsentence": gen1_ok,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("variants", nargs="+", help="name=path.jsonl pairs")
    parser.add_argument("--report", default=None)
    parser.add_argument("--json", default=None)
    # Scorecard mode: write a committed, comparable record per run (multi-agent A/B).
    parser.add_argument("--scorecard-dir", default=None, help="Write eval/chunking_runs/<run-id>.json scorecards here")
    parser.add_argument("--agent", default="unknown", help="Agent/model id producing these chunks")
    parser.add_argument("--pass-num", default="1", help="Pass number (agents may do >1)")
    args = parser.parse_args()

    results: dict[str, dict] = {}
    for spec in args.variants:
        name, _, path = spec.partition("=")
        p = Path(path)
        if not p.exists():
            print(f"WARN: missing {path}")
            continue
        results[name] = score(load(p))

    if not results:
        print("No variants scored.")
        return 1

    metrics = list(next(iter(results.values())).keys())
    names = list(results)
    width = max(len(m) for m in metrics) + 2
    header = "metric".ljust(width) + "".join(n.ljust(16) for n in names)
    lines = [header, "-" * len(header)]
    for m in metrics:
        row = m.ljust(width) + "".join(str(results[n][m]).ljust(16) for n in names)
        lines.append(row)
    table = "\n".join(lines)
    print(table)

    if args.report:
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        md = ["# Chunking A/B comparison (generated)", "", "```", table, "```", ""]
        rp.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
        print(f"\nWrote {rp}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2), encoding="utf-8")

    if args.scorecard_dir:
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        scdir = Path(args.scorecard_dir)
        scdir.mkdir(parents=True, exist_ok=True)
        for name, metrics in results.items():
            run_id = f"{args.agent}__pass{args.pass_num}__{name}__{ts}"
            card = {
                "run_id": run_id,
                "agent": args.agent,
                "pass": args.pass_num,
                "variant": name,
                "created_at": ts,
                "metrics": metrics,
            }
            out = scdir / f"{run_id}.json"
            out.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
            print(f"scorecard: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
