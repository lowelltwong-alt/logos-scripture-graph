#!/usr/bin/env python3
"""Build Ezekiel's rows_v10_final.jsonl from rows_v9_final.jsonl: the OW-30 hold round, write-new, never an overwrite.

ONE SOURCE, PINNED BY DIGEST. Fable's item-22 hold ruling (fable_end_review/atlas_hold_ruling.v1.json, OW-30, the one
authorized Fable call). Only a row ruled keep_held changes, and only its hold fields:
  review_status          candidate_review_complete -> final_deferred_review
  candidate_hold_state   (absent) -> deferred_human_or_external_ai   inserted right after review_status
  candidate_hold_basis   (absent) -> specialist_or_external_review   inserted after candidate_hold_state
This is the shape Deut and Judg shipped for their held rows (checks/assemble_review_artifacts.py lines 161-167) and the
basis checks/validate_book_review_coverage.py accepts for a held packet with no appeal. release and drop_from_feed change
no corpus row (the ruling says so); the builder refuses any other decision.

WHICH ROW. The ruling is keyed by atlas id M8-Ezek-NNN, which is chunk_index_in_book NNN. EXPECT pins each keep_held
atlas id to the row and span the dispatch brief put to Fable; a row that no longer matches is refused.

BYTES. Every v9 line round-trips through json.dumps(ensure_ascii=False) unchanged (checked per line), so only the
changed row is re-serialised and every other line is carried byte for byte. After the build the tool re-parses both
files and asserts: same row count and order; unchanged rows byte-identical; the changed row equal on every field it
does not name, in the same key order apart from the two inserted keys. It writes rows_v10_final.jsonl and
rows_v10_final.manifest.json (lineage, per-field before/after sha256; an absent field has before_sha256 null). An
existing output with the same bytes is left; with different bytes the tool refuses.

usage: build_rows_v10.py [--check]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SRC, SRC_PIN = EZ / "rows_v9_final.jsonl", "a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c"
RUL = EZ / "fable_end_review" / "atlas_hold_ruling.v1.json"
RUL_PIN = "24f6f8b0f4b2c4527db95505c9cf44d7a547c68b725675d32aa437d8bc130e5c"
OUT, MAN = EZ / "rows_v10_final.jsonl", EZ / "rows_v10_final.manifest.json"
EXPECT = {"M8-Ezek-113": ("P10-016", "Ezek.40.28-Ezek.40.37")}
NO_CORPUS_CHANGE = {"release", "drop_from_feed"}
HOLD = (("review_status", "final_deferred_review"),
        ("candidate_hold_state", "deferred_human_or_external_ai"),
        ("candidate_hold_basis", "specialist_or_external_review"))
sha = lambda b: hashlib.sha256(b).hexdigest()                                 # noqa: E731
dump = lambda o: json.dumps(o, ensure_ascii=False)                            # noqa: E731

ap = argparse.ArgumentParser()
ap.add_argument("--check", action="store_true")
a = ap.parse_args()

src_b = SRC.read_bytes()
if sha(src_b) != SRC_PIN:
    raise SystemExit("REFUSED: rows_v9_final.jsonl is not at its pinned digest")
if sha(RUL.read_bytes()) != RUL_PIN:
    raise SystemExit("REFUSED: the Fable hold ruling is not at its pinned digest")
ruling = json.loads(RUL.read_text(encoding="utf-8"))
if ruling.get("schema") != "ezek_atlas_hold_ruling.v1":
    raise SystemExit("REFUSED: the ruling is not an ezek_atlas_hold_ruling.v1")
keep = sorted(k for k, v in ruling["rulings"].items() if v["decision"] == "keep_held")
bad = sorted(k for k, v in ruling["rulings"].items() if v["decision"] not in NO_CORPUS_CHANGE | {"keep_held"})
if bad:
    raise SystemExit("REFUSED: the ruling carries a decision this builder does not implement: %s" % bad)
if set(keep) != set(EXPECT):
    raise SystemExit("REFUSED: keep_held rows %s are not the expected %s" % (keep, sorted(EXPECT)))

lines = src_b.decode("utf-8").split("\n")
if lines[-1] != "":
    raise SystemExit("REFUSED: the source does not end in one newline")
lines = lines[:-1]
rows = [json.loads(l) for l in lines]
if any(dump(r) != l for r, l in zip(rows, lines)):
    raise SystemExit("REFUSED: a source line does not round-trip; re-serialising it would drift bytes")
if [r["chunk_index_in_book"] for r in rows] != list(range(1, len(rows) + 1)):
    raise SystemExit("REFUSED: chunk_index_in_book is not 1..N, so atlas ids cannot be mapped to rows")

new_lines, record, changed = list(lines), [], {}
for aid in keep:
    i = int(aid.rsplit("-", 1)[1]) - 1
    row = json.loads(lines[i])
    want_row, want_span = EXPECT[aid]
    if (row["decision_id"], row["span"]) != (want_row, want_span):
        raise SystemExit("REFUSED: %s is %s %s, not the %s %s the ruling was given"
                         % (aid, row["decision_id"], row["span"], want_row, want_span))
    if row["review_status"] != "candidate_review_complete" or "candidate_hold_state" in row or "candidate_hold_basis" in row:
        raise SystemExit("REFUSED: %s already carries a hold or a non-final status" % aid)
    out = {}
    for k, v in row.items():
        out[k] = v
        if k == "review_status":
            for hk, hv in HOLD:
                out[hk] = hv
    for hk, hv in HOLD:
        before = row.get(hk)
        record.append({"row": row["decision_id"], "atlas_id": aid, "line": i + 1, "field": hk, "source": "ruling",
                       "before_sha256": sha(dump(before).encode("utf-8")) if hk in row else None,
                       "after_sha256": sha(dump(hv).encode("utf-8")), "before": before, "after": hv})
    new_lines[i] = dump(out)
    changed[row["decision_id"]] = aid
out_b = ("\n".join(new_lines) + "\n").encode("utf-8")

# post-build proof, from the bytes
o_lines = out_b.decode("utf-8").split("\n")[:-1]
assert len(o_lines) == len(lines)
hold_keys = [k for k, _ in HOLD]
for i, (x, y) in enumerate(zip(lines, o_lines)):
    rx, ry = json.loads(x), json.loads(y)
    assert rx["decision_id"] == ry["decision_id"]
    if rx["decision_id"] not in changed:
        assert x == y, "unchanged row %d drifted" % (i + 1)
        continue
    assert [k for k in ry if k not in hold_keys[1:]] == list(rx), "row %d key order drifted" % (i + 1)
    assert all(rx[k] == ry[k] for k in rx if k != "review_status"), "row %d drifted" % (i + 1)
    assert [ry[k] for k in hold_keys] == [v for _, v in HOLD] and rx["confidence"] == ry["confidence"]

man = {"schema": "ezek_rows_manifest.v1", "corpus": OUT.name, "corpus_sha256": sha(out_b), "rows": len(o_lines),
       "built_from": {"file": SRC.name, "sha256": SRC_PIN},
       "sources": {"ruling": {"file": "fable_end_review/" + RUL.name, "sha256": RUL_PIN,
                              "keep_held": keep, "facts_sha256": ruling.get("facts_sha256")}},
       "builder": "repair2/fixround_v10/build_rows_v10.py", "builder_sha256": sha(Path(__file__).read_bytes()),
       "why": "OW-30: Fable ruled keep_held for M8-Ezek-113 (P10-016) under precedent P3: the evidence clause its hold "
              "named is measured still present and both v9 blind delta lanes found it still false (lane A R1, lane B "
              "N1). The row is re-versioned held; release and drop_from_feed change no corpus row.",
       "changes": record, "rows_changed": sorted(changed),
       "unchanged_rows_byte_identical": len(lines) - len(changed)}
man_b = (json.dumps(man, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
summary = {"corpus_sha256": sha(out_b), "rows_changed": sorted(changed), "changes": len(record)}
if a.check:
    for p, b in ((OUT, out_b), (MAN, man_b)):
        summary[p.name] = ("MATCH" if p.exists() and p.read_bytes() == b else "DIFFERS" if p.exists() else "ABSENT")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    raise SystemExit(0)
for p, b in ((OUT, out_b), (MAN, man_b)):
    if p.exists():
        if p.read_bytes() != b:
            raise SystemExit("REFUSED: %s exists with different bytes; never overwritten" % p.name)
    else:
        p.write_bytes(b)
summary["written"] = [OUT.name, MAN.name]
print(json.dumps(summary, ensure_ascii=False, indent=1))
