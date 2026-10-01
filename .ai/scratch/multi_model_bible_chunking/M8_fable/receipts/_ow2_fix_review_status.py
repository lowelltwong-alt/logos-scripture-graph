#!/usr/bin/env python3
"""OW-2 item 3 (owner directive 2026-08-31): resolve the 347 finalized
Eccl/Song/Isa rows still labeled review_status=draft.

Guarded byte-surgical execution:
- exact targets only: book_chunks/{Eccl,Song,Isa}/chunks.jsonl +
  whole_bible_chunk_map.jsonl rows of those three books;
- expected-before pinned: EXACTLY 86/38/223 draft rows per book on both
  surfaces, no other status value present for those books;
- line-level substring replacement of the review_status value ONLY
  (no reserialization; every untouched line stays byte-identical);
- post-proof: parse both surfaces, recount, field-level diff on every
  changed line (review_status is the only differing key);
- pre/post sha256 recorded in receipts/OW2_review_status_resolution.json.
Pre-change hashes preserved per the OW-1 preservation law.
"""
import hashlib
import json
from pathlib import Path

M8 = Path(__file__).resolve().parent.parent
TARGET_BOOKS = {"Eccl": 86, "Song": 38, "Isa": 223}
OLD, NEW = "draft", "candidate_review_complete"
PATTERNS = [f'"review_status": "{OLD}"', f'"review_status":"{OLD}"']
REPLACEMENTS = [f'"review_status": "{NEW}"', f'"review_status":"{NEW}"']

FILES = [M8 / "book_chunks" / b / "chunks.jsonl" for b in TARGET_BOOKS] + \
        [M8 / "whole_bible_chunk_map.jsonl"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def process(path: Path, restrict_books):
    raw = path.read_text(encoding="utf-8")
    lines = raw.split("\n")
    changed = 0
    out_lines = []
    for line in lines:
        if line.strip():
            row = json.loads(line)
            book = row.get("book")
            if book in restrict_books and row.get("review_status") == OLD:
                hits = sum(line.count(p) for p in PATTERNS)
                assert hits == 1, f"{path.name}: expected exactly 1 pattern in line, got {hits}"
                new_line = line
                for p, r in zip(PATTERNS, REPLACEMENTS):
                    new_line = new_line.replace(p, r)
                new_row = json.loads(new_line)
                diff = {k for k in set(row) | set(new_row)
                        if row.get(k) != new_row.get(k)}
                assert diff == {"review_status"}, f"{path.name}: diff {diff}"
                out_lines.append(new_line)
                changed += 1
                continue
            assert not (book in restrict_books and row.get("review_status") not in (OLD, NEW)), \
                f"{path.name}: unexpected status {row.get('review_status')} for {book}"
        out_lines.append(line)
    return "\n".join(out_lines), changed


receipt = {"schema": "m8_ow2_review_status_resolution.v1",
           "executed": "2026-08-31",
           "authorization": "owner directive OW-2 item 3, in chat 2026-08-31 "
                            "('Resolve the 347 finalized Eccl/Song/Isa rows still labeled draft')",
           "change": {"field": "review_status", "from": OLD, "to": NEW,
                      "books": dict(TARGET_BOOKS)},
           "method": "line-level substring replacement of the review_status value only; "
                     "no reserialization; untouched lines byte-identical; field-level "
                     "diff proven per changed line",
           "files": {}}

# expected-before check on all surfaces first (fail closed before any write)
plans = {}
for f in FILES:
    restrict = ({f.parent.name} if f.parent.name in TARGET_BOOKS
                else set(TARGET_BOOKS))
    pre_text = f.read_text(encoding="utf-8")
    pre_counts = {}
    for line in pre_text.split("\n"):
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("book") in restrict or f.parent.name in TARGET_BOOKS:
            b = row.get("book")
            if b in TARGET_BOOKS:
                pre_counts[b] = pre_counts.get(b, 0) + (row.get("review_status") == OLD)
    for b in (restrict & set(TARGET_BOOKS)):
        assert pre_counts.get(b, 0) == TARGET_BOOKS[b], \
            f"{f}: expected {TARGET_BOOKS[b]} draft rows for {b}, found {pre_counts.get(b, 0)}"
    plans[f] = restrict

total_changed = 0
for f in FILES:
    pre_hash = sha(f)
    new_text, changed = process(f, plans[f])
    tmp = f.with_suffix(f.suffix + ".ow2tmp")
    tmp.write_text(new_text, encoding="utf-8", newline="")
    tmp.replace(f)
    post_hash = sha(f)
    # post-proof: parse + recount
    post_draft = 0
    post_new = 0
    for line in f.read_text(encoding="utf-8").split("\n"):
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("book") in TARGET_BOOKS:
            post_draft += row.get("review_status") == OLD
            post_new += row.get("review_status") == NEW
    expected = (TARGET_BOOKS[f.parent.name] if f.parent.name in TARGET_BOOKS
                else sum(TARGET_BOOKS.values()))
    assert post_draft == 0 and post_new == expected and changed == expected, \
        f"{f}: post draft={post_draft} new={post_new} changed={changed} expected={expected}"
    rel = f.relative_to(M8).as_posix()
    receipt["files"][rel] = {"sha256_pre": pre_hash, "sha256_post": post_hash,
                             "rows_changed": changed}
    total_changed += changed

receipt["total_row_edits"] = total_changed
receipt["note"] = ("total_row_edits counts per-surface edits: 347 rows on the "
                   "book_chunks surface + the same 347 rows mirrored in "
                   "whole_bible_chunk_map.jsonl")
out = M8 / "receipts" / "OW2_review_status_resolution.json"
json.dump(receipt, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"total_row_edits": total_changed,
                  "files": {k: v["rows_changed"] for k, v in receipt["files"].items()},
                  "receipt": out.name}, indent=1))
