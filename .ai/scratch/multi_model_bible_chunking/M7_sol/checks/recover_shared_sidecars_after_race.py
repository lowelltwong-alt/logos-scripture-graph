#!/usr/bin/env python3
"""Recover the three shared sidecars after the T521 concurrent-write race."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
RECOVERY = MODEL / "runtime" / "recovery" / "t521_shared_sidecar_race"
SIDECARS = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)


def valid_gen_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        decision_id = row.get("chunk_decision_id")
        if row.get("book") == "Gen" and isinstance(decision_id, str) and decision_id not in seen:
            seen.add(decision_id)
            rows.append(row)
    return rows


def expected_gen_ids() -> set[str]:
    chunks = MODEL / "book_chunks" / "Gen" / "chunks.jsonl"
    return {
        row["decision_id"]
        for row in (json.loads(line) for line in chunks.read_text(encoding="utf-8").splitlines() if line.strip())
        if row.get("confidence") in {"low", "medium_low"}
    }


def write_atomic(path: Path, rows: list[dict]) -> None:
    temporary = path.with_name(f"{path.name}.{os.getpid()}.recovery.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)

def main() -> int:
    expected = expected_gen_ids()
    RECOVERY.mkdir(parents=True, exist_ok=True)
    for name in SIDECARS:
        path = MODEL / name
        backup = RECOVERY / f"{name}.corrupt-backup"
        if backup.exists():
            raise SystemExit(f"refusing repeat recovery; backup already exists: {backup.relative_to(ROOT)}")
        rows = valid_gen_rows(path)
        observed = {row["chunk_decision_id"] for row in rows}
        if observed != expected:
            raise SystemExit(
                f"{name}: cannot safely salvage Genesis rows; "
                f"missing={sorted(expected - observed)} extra={sorted(observed - expected)}"
            )
        shutil.copy2(path, backup)
        write_atomic(path, rows)
        print(f"backed up corrupted {name}; restored {len(rows)} verified Genesis rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())