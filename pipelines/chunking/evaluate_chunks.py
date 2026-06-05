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
  psalms_fragmented       # psalms split into >1 chunk (lower better)
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


def approx_tokens(text: str) -> int:
    return max(1, len(text.split()))


def sentence_ended(text: str) -> bool:
    return bool(SENTENCE_END_RE.search(text.strip()))


def book_of(osis: str) -> str:
    return (osis or "").split(".")[0]


def load(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def score(chunks: list[dict]) -> dict:
    n = len(chunks)
    toks = [approx_tokens(c.get("text", "")) for c in chunks]
    prose = [c for c in chunks if c.get("genre") != "psalms"]
    prose_ok = sum(1 for c in prose if c.get("validation", {}).get("sentence_ended", sentence_ended(c.get("text", ""))))
    # psalm fragmentation: group psalms chunks by chapter
    psalm_chaps: dict[str, int] = {}
    for c in chunks:
        if c.get("genre") == "psalms" or book_of(c.get("osis_start", "")) == "Ps":
            ch = c.get("osis_start", "").split(".")[1] if c.get("osis_start", "").count(".") >= 1 else "?"
            psalm_chaps[ch] = psalm_chaps.get(ch, 0) + 1
    fragmented = sum(1 for v in psalm_chaps.values() if v > 1)
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
        "psalms_fragmented": fragmented,
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
