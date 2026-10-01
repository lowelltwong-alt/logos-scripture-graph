#!/usr/bin/env python3
'''Atomically replace one book partition in the three M7 uncertainty sidecars.'''
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / '.ai' / 'scratch' / 'multi_model_bible_chunking' / 'M7_sol'
SIDECARS = (
    'low_confidence_register.jsonl',
    'frontier_escalation_queue.jsonl',
    'atlas_candidate_feed.jsonl',
)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def encoded_row(row: dict[str, Any]) -> bytes:
    return (json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')


def replace_partition(path: Path, book: str, replacement: list[dict[str, Any]]) -> dict[str, Any]:
    before = path.read_bytes() if path.is_file() else b''
    kept: list[bytes] = []
    insert_at: int | None = None
    removed = 0
    for raw in before.splitlines(keepends=True):
        if not raw.strip():
            kept.append(raw)
            continue
        row = json.loads(raw)
        if row.get('book') == book:
            if insert_at is None:
                insert_at = len(kept)
            removed += 1
        else:
            kept.append(raw if raw.endswith((b'\n', b'\r')) else raw + b'\n')
    if insert_at is None:
        insert_at = len(kept)
    replacement_bytes = [encoded_row(row) for row in replacement]
    after = b''.join([*kept[:insert_at], *replacement_bytes, *kept[insert_at:]])
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f'.{path.name}.', suffix='.tmp', delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(after)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    reread = path.read_bytes()
    if reread != after:
        raise RuntimeError(f'atomic replacement read-back failed for {path}')
    return {
        'path': path.relative_to(ROOT).as_posix(),
        'removed_rows': removed,
        'installed_rows': len(replacement),
        'sha256_before': digest(before),
        'sha256_after': digest(after),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--book', required=True)
    parser.add_argument('--rows')
    args = parser.parse_args()
    book = args.book
    rows_path = Path(args.rows) if args.rows else MODEL / 'reviews' / book / 'sidecar_rows_v2.json'
    payload = json.loads(rows_path.read_text(encoding='utf-8'))
    if payload.get('book') != book or payload.get('non_authorizing') is not True:
        raise SystemExit('sidecar replacement payload lost book/non-authorizing guard')
    rows = payload.get('rows')
    if not isinstance(rows, dict) or set(rows) != set(SIDECARS):
        raise SystemExit('sidecar replacement payload has the wrong sidecar set')
    for filename, values in rows.items():
        if not isinstance(values, list):
            raise SystemExit(f'{filename}: replacement rows must be a list')
        decision_ids = [row.get('chunk_decision_id') for row in values]
        if any(row.get('book') != book or row.get('non_authorizing') is not True for row in values):
            raise SystemExit(f'{filename}: row lost book/non-authorizing guard')
        if len(decision_ids) != len(set(decision_ids)) or any(not value for value in decision_ids):
            raise SystemExit(f'{filename}: replacement decision IDs must be unique and non-empty')
    lock = MODEL / '.sidecar_install.lock'
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise SystemExit(f'exclusive sidecar lock already exists: {lock}') from exc
    try:
        os.write(descriptor, f'{book}\n'.encode('utf-8'))
        os.close(descriptor)
        report = [replace_partition(MODEL / filename, book, rows[filename]) for filename in SIDECARS]
    finally:
        if lock.exists():
            lock.unlink()
    print(json.dumps({'book': book, 'status': 'installed', 'sidecars': report}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
