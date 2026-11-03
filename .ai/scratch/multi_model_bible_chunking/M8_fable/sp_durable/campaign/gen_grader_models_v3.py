#!/usr/bin/env python3
"""Write the campaign grader carrier `campaign/grader_models.v3.json`, the version that adds the six OW-37 close shapes.

WHY A NEW VERSION. Any change to the carrier is a new version, never an edit (E-44). OW-37 (2026-11-01) gave Daniel's
merged-verdict shape to the six OW-36 books, which v2 does not list. v3 is v2's content, read from v2's pinned bytes and
copied unchanged, plus one `book_close_shapes` entry per book. v1, v2 and their generators are not touched.

TRANSCRIBED, WITH ONE DECLARED SUBSTITUTION. `shape` is v2's Daniel shape text. `close_action` is OW-37 point 3, cut from
ERROR_PATTERN_LEDGER.v1.md. The owner's words are the selected label, cut from the ledger line that holds it. OW-37 has no
weakness statement of its own: point 2 adopts Daniel's shape, so the statement is OW-33's, with its one book name replaced
by the book's and nothing else changed. Each entry says so in `weakness_statement_derivation` and carries the digest of
OW-33's own text. `directive` stays "OW-26" because that is the shape's name; `granted_by` names OW-37.

--check compares the cut text and v2's copied fields, never the ledger digest, because the ledger is append-only.

usage: gen_grader_models_v3.py [--check]     --check rebuilds in memory and prints MATCH or DIFFERS
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
V2 = HERE / "grader_models.v2.json"
V2_SHA = "efd78773fd122566ad923c6ae95a178385fff637344ed5272c7f79aa71214727"
OUT = HERE / "grader_models.v3.json"
OW37_HEAD = "## OWNER DIRECTIVE OW-37 (2026-11-01)"
OWNER_LINE = '> "Merged-verdict, all six books (Recommended)"'
POINT2_LEAD = "2. Close shape:"
POINT3_LEAD = "3. Close act:"
DAN_OPENING = "In Daniel's close the three verdicts"
# OW-36's order, the book keys the campaign's carriers use, with the name each weakness statement gives the book.
BOOKS = (("1Cor", "1 Corinthians"), ("John", "John"), ("Rom", "Romans"), ("Rev", "Revelation"), ("Heb", "Hebrews"), ("Matt", "Matthew"))


def v2_tool():
    spec = importlib.util.spec_from_file_location("gen_grader_models_v2", HERE / "gen_grader_models_v2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build():
    t = v2_tool()
    g = t.v1_tool()
    v2_bytes = V2.read_bytes()
    if hashlib.sha256(v2_bytes).hexdigest() != V2_SHA:
        raise SystemExit("REFUSED: grader_models.v2.json is not the bytes this tool pins")
    v2 = json.loads(v2_bytes.decode("utf-8"))
    _, d2 = t.build()
    keys = ("downgrade_statement", "downgrade_statement_sha256", "declared_fallback_model", "ow13_grader_model")
    drop = lambda s: {k: v for k, v in s.items() if k != "source_sha256_at_transcription"}  # noqa: E731
    if not (all(v2.get(k) == d2[k] for k in keys) and drop(v2["book_close_shapes"]["Dan"]) == drop(d2["book_close_shapes"]["Dan"])):
        raise SystemExit("REFUSED: v2 no longer transcribes the ledger; v3 will not copy it")
    raw = g.LEDGER.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    base, sec = g.section(lines, OW37_HEAD)
    hits = [i for i, l in enumerate(sec) if l.strip() == OWNER_LINE]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %d OW-37 lines hold the selected label; expected exactly one" % len(hits))
    ln_p3, point3 = g.paragraph(lines, OW37_HEAD, POINT3_LEAD)
    ln_p2, point2 = g.paragraph(lines, OW37_HEAD, POINT2_LEAD)
    dan = v2["book_close_shapes"]["Dan"]
    weak = dan["weakness_statement"]
    if weak.count(DAN_OPENING) != 1 or weak.count("Daniel") != 1:
        raise SystemExit("REFUSED: OW-33's weakness statement no longer names the book exactly once")
    if not all(n in point2 for _, n in BOOKS):
        raise SystemExit("REFUSED: OW-37 point 2 does not name all six books")
    d = dict(v2)
    d["schema"] = "m8_grader_models.v3"
    d["written"] = "2026-11-01"
    d["supersedes"] = {"file": "campaign/grader_models.v2.json", "sha256": V2_SHA,
                       "what_changed": "book_close_shapes gains the six OW-37 books; every other value is v2's, copied unchanged"}
    shapes = dict(v2["book_close_shapes"])
    for key, name in BOOKS:
        text = weak.replace(DAN_OPENING, "In %s's close the three verdicts" % name)
        shapes[key] = {
            "directive": "OW-26",
            "granted_by": "OW-37",
            "scope": "the six OW-36 books",
            "shape": dan["shape"],
            "transcript_audit": "OWED, NOT MET",
            "close_action": point3[len("3. "):],
            "close_action_line": ln_p3,
            "owner_words_transcribed": OWNER_LINE[3:-1],
            "owner_words_line": base + hits[0],
            "weakness_statement": text,
            "weakness_statement_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "weakness_statement_derivation": "OW-33's statement with its one book name replaced under OW-37 point 2; nothing else changed",
            "weakness_statement_ow33_sha256": dan["weakness_statement_sha256"],
            "weakness_statement_line": dan["weakness_statement_line"],
            "source": "ERROR_PATTERN_LEDGER.v1.md",
            "source_sha256_at_transcription": hashlib.sha256(raw).hexdigest(),
        }
    d["book_close_shapes"] = shapes
    d["generator"] = "campaign/gen_grader_models_v3.py"
    return (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8"), d


def main():
    data, d = build()
    if "--check" in sys.argv:
        if not OUT.is_file():
            print("DIFFERS (absent)")
            sys.exit(1)
        old = json.loads(OUT.read_bytes().decode("utf-8"))
        drop = ("source_sha256_at_transcription",)
        cut = lambda x: {b: {k: v for k, v in s.items() if k not in drop} for b, s in x["book_close_shapes"].items()}  # noqa: E731
        same = cut(old) == cut(d) and all(old.get(k) == v for k, v in d.items() if k != "book_close_shapes")
        print("MATCH" if same else "DIFFERS")
        sys.exit(0 if same else 1)
    if OUT.exists():
        if OUT.read_bytes() != data:
            raise SystemExit("REFUSED: %s exists with different bytes; never overwritten (E-44)" % OUT.name)
        state = "same bytes, left"
    else:
        OUT.write_bytes(data)
        state = "written"
    print(json.dumps({"carrier": OUT.name, "state": state, "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
                      "books": sorted(d["book_close_shapes"]),
                      "weakness_1cor_sha256": d["book_close_shapes"]["1Cor"]["weakness_statement_sha256"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
