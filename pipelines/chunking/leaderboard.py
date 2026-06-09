#!/usr/bin/env python3
"""Multi-agent chunking leaderboard.

Reads the committed per-run scorecards in eval/chunking_runs/*.json (each produced by
`evaluate_chunks.py --scorecard-dir`) and ranks them so many agents' chunking attempts
can be compared to converge on the best ("get it perfect"). The big chunks.jsonl outputs
stay gitignored under data/derived/chunks/variants/; only the small scorecards are
committed, so runs from different agents/PRs/machines are durably comparable.
Scorecards may span corpus baselines; compare runs within the same corpus_baseline.

Ranking:
  1. HARD GATES (must pass to be eligible): usfm_leaks==0, book_crossings==0,
     sentence_integrity_pct==100, gold_psalm23_one_chunk==True,
     gold_gen1_no_midsentence==True.
  2. Among eligible, sort by: final unreviewed literal Psalm fragmentation asc, then
     size-fitness |p50-600| asc.
  Transparent composite shown; humans make the final call.

Usage: python pipelines/chunking/leaderboard.py [--runs-dir eval/chunking_runs] [--out eval/LEADERBOARD.md]
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_P50 = 600  # target median tokens for retrieval fitness


def eligible(m: dict) -> bool:
    return (
        m.get("usfm_leaks", 1) == 0
        and m.get("book_crossings", 1) == 0
        and m.get("sentence_integrity_pct", 0) == 100.0
        and m.get("gold_psalm23_one_chunk", False) is True
        and m.get("gold_gen1_no_midsentence", False) is True
    )


OVERSIZE_LIMIT = 1600  # hard_max tokens; chunks above this hurt retrieval (monster chunks)


def composite(m: dict) -> float:
    score = 100.0
    score -= m.get("literal_psalms_fragmented", m.get("psalms_fragmented", 0)) * 0.5
    score -= abs(m.get("tok_p50", 0) - TARGET_P50) / 20.0
    # Penalize monster chunks (e.g. an unsplit Ps 119) — the single worst retrieval failure.
    score -= max(0, m.get("tok_max", 0) - OVERSIZE_LIMIT) / 100.0
    score -= (100.0 - m.get("boundary_basis_cov_pct", 0)) * 0.1
    score -= (100.0 - m.get("metadata_carry_pct", 0)) * 0.1
    return round(score, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-dir", default=str(ROOT / "eval" / "chunking_runs"))
    parser.add_argument("--out", default=str(ROOT / "eval" / "LEADERBOARD.md"))
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)
    cards = []
    for p in sorted(runs_dir.glob("*.json"), key=lambda x: x.as_posix()):
        try:
            cards.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            print(f"WARN: bad scorecard {p}")

    if not cards:
        print(f"No scorecards in {runs_dir}. Run evaluate_chunks.py --scorecard-dir first.")
        return 0

    rows = []
    for c in cards:
        m = c.get("metrics", {})
        reviewed_splits = m.get("reviewed_structural_splits") or []
        if not isinstance(reviewed_splits, list):
            reviewed_splits = []
        rows.append({
            "run_id": c.get("run_id", "?"),
            "agent": c.get("agent", "?"),
            "pass": c.get("pass", "?"),
            "corpus_baseline": c.get("corpus_baseline", "pre_t327_wider_corpus"),
            "eligible": eligible(m),
            "composite": composite(m) if eligible(m) else None,
            "chunks": m.get("chunks"),
            "tok_p50": m.get("tok_p50"),
            "psalms_fragmented": m.get("psalms_fragmented"),
            "literal_psalms_fragmented_raw": m.get("literal_psalms_fragmented_raw"),
            "reviewed_structural_splits": len(reviewed_splits),
            "literal_psalms_fragmented": m.get("literal_psalms_fragmented"),
            "poetry_books_fragmented": m.get("poetry_books_fragmented"),
            "psalm119_section_chunks": m.get("psalm119_section_chunks"),
            "sent_pct": m.get("sentence_integrity_pct"),
            "leaks": m.get("usfm_leaks"),
            "crossings": m.get("book_crossings"),
        })
    # eligible first, ranked by composite desc; ineligible after
    rows.sort(key=lambda r: (not r["eligible"], -(r["composite"] or -1e9)))

    cols = ["rank", "agent", "pass", "corpus_baseline", "eligible", "composite", "chunks", "tok_p50",
            "psalms_fragmented", "literal_psalms_fragmented_raw", "reviewed_structural_splits",
            "literal_psalms_fragmented", "poetry_books_fragmented", "psalm119_section_chunks",
            "sent_pct", "leaks", "crossings", "run_id"]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for i, r in enumerate(rows, 1):
        rank = i if r["eligible"] else "—"
        cells = [str(rank), r["agent"], str(r["pass"]), r["corpus_baseline"],
                 "yes" if r["eligible"] else "NO", str(r["composite"]),
                 str(r["chunks"]), str(r["tok_p50"]), str(r["psalms_fragmented"]),
                 str(r["literal_psalms_fragmented_raw"]), str(r["reviewed_structural_splits"]),
                 str(r["literal_psalms_fragmented"]), str(r["poetry_books_fragmented"]),
                 str(r["psalm119_section_chunks"]), str(r["sent_pct"]), str(r["leaks"]),
                 str(r["crossings"]), r["run_id"]]
        lines.append("| " + " | ".join(cells) + " |")
    table = "\n".join(lines)
    print(table)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    md = [
        "# Chunking Leaderboard (generated)",
        "",
        f"**Generated:** {now}  |  **Runs:** {len(cards)}  |  target p50={TARGET_P50} tokens",
        "",
        "Hard gates (must pass to rank): 0 USFM leaks, 0 book crossings, 100% prose",
        "sentence integrity, Psalm 23 = one whole-psalm chunk, Genesis 1 = no mid-sentence",
        "split. Ineligible runs shown last.",
        "",
        "Scoring provenance: T311 corrected Psalm fragmentation grouping from bare chapter to",
        "`(book, chapter)`. The unchanged D / Claude pass2 output scored 88.5 under the old",
        "evaluator and 93.0 under the T311 book/chapter evaluator. T314 excludes reviewed",
        "parent/child structural Psalm splits, such as Ps.78, from the bad-fragmentation penalty;",
        "the same unchanged output now scores 93.5. These are evaluator-policy corrections, not",
        "chunk-output improvement.",
        "",
        "Corpus provenance: pre-T327 scorecards are wider-corpus baselines produced before",
        "the owner-approved 66-book canonical scope correction. T327D introduces the",
        "post-T327 canonical-66 corpus baseline after T327C removed non-66 canonical outputs.",
        "Movement between pre-T327 and post-T327 rows is corpus-scope correction / baseline",
        "reset, not chunking improvement. Compare leaderboard rows within the same",
        "`corpus_baseline`.",
        "",
        table,
        "",
        "> Big chunk outputs live under `data/derived/chunks/variants/<run_id>/` (gitignored).",
        "> Only these scorecards are committed. The human picks the winner to promote.",
        "",
    ]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
