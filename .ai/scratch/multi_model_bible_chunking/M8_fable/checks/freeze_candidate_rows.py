#!/usr/bin/env python3
"""Freeze M8_fable draft decisions into candidate chunk rows v0 and reviewer cluster dossiers.

Deterministic Tier-0 tooling: coverage math, row shaping, hashing, clustering.
No model judgment happens here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MODEL_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M8_fable"
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def canonical_refs(book: str) -> list[str]:
    return [row["osis_ref"] for row in read_jsonl(PASSAGES) if row.get("book") == book]


def span_ref_list(span: str, book: str, refs: list[str], positions: dict[str, int]) -> list[str]:
    start_raw, end_raw = span.split("-")
    sb, sc, sv = start_raw.split(".")
    eb, ec, ev = end_raw.split(".")
    if sb != book or eb != book:
        raise SystemExit(f"span {span} not in {book}")
    start = f"{book}.{int(sc)}.{int(sv)}"
    end = f"{book}.{int(ec)}.{int(ev)}"
    if start not in positions or end not in positions:
        raise SystemExit(f"span {span} endpoint absent from canonical inventory")
    a, b = positions[start], positions[end]
    if a > b:
        raise SystemExit(f"span {span} inverted")
    return refs[a : b + 1]


def chunk_digest(row: dict) -> str:
    payload = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--draft", type=Path, required=True, help="draft_decisions.json from the book_writer")
    parser.add_argument("--out-dir", type=Path, required=True, help="workspace dir for frozen rows + clusters")
    parser.add_argument("--cluster-size", type=int, default=8)
    args = parser.parse_args()

    book = args.book
    draft = json.loads(args.draft.read_text(encoding="utf-8"))
    if draft.get("book") != book:
        raise SystemExit("draft book mismatch")
    decisions = draft["decisions"]

    refs = canonical_refs(book)
    positions = {ref: index for index, ref in enumerate(refs)}
    covered: list[str] = []
    rows = []
    for index, decision in enumerate(decisions, start=1):
        span_verses = span_ref_list(decision["span"], book, refs, positions)
        covered.extend(span_verses)
        row = {
            "model_id": "M8_fable",
            "book": book,
            "span": decision["span"],
            "chunk_index_in_book": index,
            "literature_type_guess": decision["literature_type_guess"],
            "boundary_rationale": decision["boundary_rationale"],
            "strongest_rejected_alternative": decision["strongest_rejected_alternative"],
            "boundary_evidence_refs": decision["boundary_evidence_refs"],
            "strong_or_hebrew_tags_used": bool(decision.get("strong_or_hebrew_tags_used", False)),
            "wj_or_red_letter_considered": True,
            "frontier_flag_considered": True,
            "confidence": decision["confidence"],
            "decision_id": decision["decision_id"],
            "review_revision": 0,
            "non_authorizing": True,
        }
        rows.append(row)

    if covered != refs:
        covered_set = set(covered)
        missing = [ref for ref in refs if ref not in covered_set]
        duplicates = sorted({ref for ref in covered if covered.count(ref) > 1})
        raise SystemExit(
            f"coverage FAIL expected={len(refs)} covered={len(covered)} "
            f"missing={missing[:8]} duplicates={duplicates[:8]}"
        )

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    frozen_path = out_dir / "frozen_rows_v0.jsonl"
    with frozen_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    clusters = []
    for start in range(0, len(rows), args.cluster_size):
        cluster_rows = rows[start : start + args.cluster_size]
        cluster_id = f"cluster_{start // args.cluster_size + 1:02d}"
        cluster = {
            "cluster_id": cluster_id,
            "book": book,
            "decision_ids": [row["decision_id"] for row in cluster_rows],
            "decisions": [
                {
                    "decision_id": row["decision_id"],
                    "span": row["span"],
                    "literature_type_guess": row["literature_type_guess"],
                    "boundary_rationale": row["boundary_rationale"],
                    "strongest_rejected_alternative": row["strongest_rejected_alternative"],
                    "boundary_evidence_refs": row["boundary_evidence_refs"],
                    "confidence": row["confidence"],
                    "frozen_sha256": chunk_digest(row),
                }
                for row in cluster_rows
            ],
        }
        cluster_path = out_dir / f"{cluster_id}.json"
        cluster_path.write_text(json.dumps(cluster, indent=1, ensure_ascii=False), encoding="utf-8")
        clusters.append({"cluster_id": cluster_id, "count": len(cluster_rows), "path": str(cluster_path)})

    summary = {
        "book": book,
        "decision_count": len(rows),
        "verse_coverage": f"{len(covered)}/{len(refs)}",
        "clusters": clusters,
        "confidence_spread": {
            level: sum(1 for row in rows if row["confidence"] == level)
            for level in ("high", "medium", "medium_low", "low")
        },
        "chapter_shaped_spans": [
            row["span"] for row in rows
            if row["span"] in {
                f"{book}.{ch}.1-{book}.{ch}.{max(int(r.split('.')[2]) for r in refs if r.split('.')[1] == str(ch))}"
                for ch in {int(r.split(".")[1]) for r in refs}
            }
        ],
    }
    (out_dir / "freeze_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
