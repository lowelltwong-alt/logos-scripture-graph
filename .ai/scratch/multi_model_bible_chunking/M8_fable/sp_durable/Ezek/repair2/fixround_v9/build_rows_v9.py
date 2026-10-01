#!/usr/bin/env python3
"""Build Ezekiel's rows_v9_final.jsonl from rows_v8_final.jsonl: the OW-28 fix round, write-new, never an overwrite.

TWO SOURCES, EACH PINNED BY DIGEST AND EACH LIMITED TO ITS OWN FIELDS.
  signals   signals_v9.proposal.json (measure_signals_v9.py, MEASURED on the witness): observed_substrate_signals only
  author    the bounded author's proposal.json, transcribed durable under author_a1/: prose and refs only, never
            confidence, span, signals or review_status (the author never changes a grade)
A row both sources touch, a field outside a source's scope, or a proposal naming a row that does not exist is refused.
A boundary_rationale change must keep the old string as an exact prefix (the order was to APPEND one sentence).

BYTES. Every v8 line round-trips through json.dumps(ensure_ascii=False) unchanged (checked here, per line), so only the
changed rows are re-serialised and every other line is carried byte for byte. After the build the tool re-parses both
files and asserts: same row count and order; unchanged rows byte-identical; changed rows equal on every field the
proposal does not name. It writes rows_v9_final.jsonl and rows_v9_final.manifest.json (lineage, per-field before/after
sha256). An existing output with the same bytes is left; with different bytes the tool refuses.

usage: build_rows_v9.py --author-sha <hex|none> [--check]
       --author-sha none builds the signals-only image (used for a dry look before the author lands; never --write-able)
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SRC, SRC_PIN = EZ / "rows_v8_final.jsonl", "b2160ad6281184dc1dedf15a764bc058bc79a181928ed6323dbc332ec09cb0e7"
SIG, SIG_PIN = HERE / "signals_v9.proposal.json", "925ca474a49527bebd5c5e8025128d759814fe2387723231095340c065f043ba"
AUTH = HERE / "author_a1" / "proposal.json"
OUT, MAN = EZ / "rows_v9_final.jsonl", EZ / "rows_v9_final.manifest.json"
SCOPE = {"signals": {"observed_substrate_signals"},
         "author": {"boundary_rationale", "device_notes", "boundary_evidence_refs", "strongest_rejected_alternative",
                    "literature_type_guess"}}
sha = lambda b: hashlib.sha256(b).hexdigest()                                 # noqa: E731
dump = lambda o: json.dumps(o, ensure_ascii=False)                            # noqa: E731

ap = argparse.ArgumentParser()
ap.add_argument("--author-sha", required=True)
ap.add_argument("--check", action="store_true")
a = ap.parse_args()

src_b = SRC.read_bytes()
if sha(src_b) != SRC_PIN:
    raise SystemExit("REFUSED: rows_v8_final.jsonl is not at its pinned digest")
if sha(SIG.read_bytes()) != SIG_PIN:
    raise SystemExit("REFUSED: the signals proposal is not at its pinned digest")
sources = {"signals": json.loads(SIG.read_text(encoding="utf-8"))}
if a.author_sha != "none":
    if sha(AUTH.read_bytes()) != a.author_sha:
        raise SystemExit("REFUSED: the author proposal is not at the digest given")
    ap_ = json.loads(AUTH.read_text(encoding="utf-8"))
    if ap_.get("rows_sha256") != SRC_PIN or ap_.get("attempt_id") != "ezek_fixround_v9_author_a1":
        raise SystemExit("REFUSED: the author proposal is not bound to rows_v8_final / this attempt")
    sources["author"] = ap_.get("rows") or {}

lines = src_b.decode("utf-8").split("\n")
if lines[-1] != "":
    raise SystemExit("REFUSED: the source does not end in one newline")
lines = lines[:-1]
rows = [json.loads(l) for l in lines]
if any(dump(r) != l for r, l in zip(rows, lines)):
    raise SystemExit("REFUSED: a source line does not round-trip; re-serialising it would drift bytes")
index = {r["decision_id"]: i for i, r in enumerate(rows)}

edits, touched = {}, {}
for name, prop in sources.items():
    for rid, fields in prop.items():
        if rid not in index:
            raise SystemExit("REFUSED: %s names a row that does not exist: %s" % (name, rid))
        if rid in touched:
            raise SystemExit("REFUSED: %s and %s both touch %s" % (touched[rid], name, rid))
        bad = set(fields) - SCOPE[name]
        if bad:
            raise SystemExit("REFUSED: %s may not write %s on %s" % (name, sorted(bad), rid))
        touched[rid] = name
        edits[rid] = fields

new_lines, record = list(lines), []
for rid, fields in sorted(edits.items()):
    i = index[rid]
    row = json.loads(lines[i])
    for k, v in fields.items():
        old = row[k]
        if type(v) is not type(old):
            raise SystemExit("REFUSED: %s.%s changes type" % (rid, k))
        if k == "boundary_rationale" and not (v.startswith(old) and len(v) > len(old)):
            raise SystemExit("REFUSED: %s boundary_rationale is not an append to the old string" % rid)
        if v == old:
            raise SystemExit("REFUSED: %s.%s proposes no change" % (rid, k))
        record.append({"row": rid, "line": i + 1, "field": k, "source": touched[rid],
                       "before_sha256": sha(dump(old).encode("utf-8")), "after_sha256": sha(dump(v).encode("utf-8")),
                       "appended": v[len(old):] if k == "boundary_rationale" else None})
        row[k] = v
    new_lines[i] = dump(row)
out_b = ("\n".join(new_lines) + "\n").encode("utf-8")

# post-build proof, from the bytes
o_lines = out_b.decode("utf-8").split("\n")[:-1]
assert len(o_lines) == len(lines)
for i, (x, y) in enumerate(zip(lines, o_lines)):
    rx, ry = json.loads(x), json.loads(y)
    assert rx["decision_id"] == ry["decision_id"]
    named = set(edits.get(rx["decision_id"], {}))
    if not named:
        assert x == y, "unchanged row %d drifted" % (i + 1)
    else:
        assert list(rx) == list(ry) and all(rx[k] == ry[k] for k in rx if k not in named), "row %d drifted" % (i + 1)
        assert rx["confidence"] == ry["confidence"] and rx["review_status"] == ry["review_status"]

man = {"schema": "ezek_rows_manifest.v1", "corpus": OUT.name, "corpus_sha256": sha(out_b), "rows": len(o_lines),
       "built_from": {"file": SRC.name, "sha256": SRC_PIN},
       "sources": {"signals": {"file": "repair2/fixround_v9/" + SIG.name, "sha256": SIG_PIN},
                   "author": ({"file": "repair2/fixround_v9/author_a1/proposal.json", "sha256": a.author_sha}
                              if "author" in sources else None)},
       "builder": "repair2/fixround_v9/build_rows_v9.py", "builder_sha256": sha(Path(__file__).read_bytes()),
       "why": "OW-28 fix round: lane B P06-015 SIGNAL_OUT_OF_SPAN (MEASURED removals) and lane A P03-001 grade ground "
              "(F-414) plus the P10-016 F-337 remainder, per the bounded author",
       "changes": record, "rows_changed": sorted(edits),
       "unchanged_rows_byte_identical": len(lines) - len(edits)}
man_b = (json.dumps(man, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
summary = {"corpus_sha256": sha(out_b), "rows_changed": sorted(edits), "changes": len(record),
           "appended": [c["appended"] for c in record if c["appended"]]}
if a.check or "author" not in sources:
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
