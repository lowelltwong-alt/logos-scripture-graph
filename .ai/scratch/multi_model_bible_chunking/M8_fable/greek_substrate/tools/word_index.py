#!/usr/bin/env python3
"""Skeleton word index over one Greek witness (rp or sbl). Every count names its unit.

A query form is reduced to its skeleton (greek_lib.skeleton) and matched against whole skeleton tokens, so the
index answers "which verses contain this form ignoring accents, breathings and case". It returns
{"tokens": n, "verses": m, "refs": [...first 50]}; tokens and verses are never conflated (a verse with the form
twice counts 2 tokens, 1 verse).

Usage: word_index.py rp|sbl FORM [Book ...]
       word_index.py --selftest
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import greek_lib as g


def index(space: str, books: list[str]) -> dict[str, list[str]]:
    idx: dict[str, list[str]] = defaultdict(list)
    for b in books:
        for (c, v), t in g.load(space)[b].items():
            for tok in g.skeleton(t).split():
                idx[tok].append(f"{space}:{b}.{c}.{v}")
    return idx


def query(space: str, form: str, books: list[str]) -> dict:
    key = g.skeleton(form)
    if not key or " " in key:
        return {"status": "RED", "error": f"form must be one word, got {form!r}"}
    refs = index(space, books).get(key, [])
    uniq = list(dict.fromkeys(refs))
    return {"status": "GREEN", "space": space, "form_skeleton": key, "tokens": len(refs), "verses": len(uniq),
            "refs": uniq[:50], "books": books if len(books) < len(g.BOOKS) else "all"}


def selftest() -> int:
    fails = []
    # constructed check on the fixture book: count tokens by direct scan and compare with the index
    for sp in ("rp", "sbl"):
        text = {k: g.skeleton(t).split() for k, t in g.load(sp)["3John"].items()}
        want_tok = sum(ws.count("αγαπητε") for ws in text.values())
        want_vs = sum(1 for ws in text.values() if "αγαπητε" in ws)
        r = query(sp, "Ἀγαπητέ", ["3John"])
        if (r["tokens"], r["verses"]) != (want_tok, want_vs) or want_tok == 0:
            fails.append(f"{sp} 3John αγαπητε: index {r['tokens']}/{r['verses']} vs scan {want_tok}/{want_vs}")
    if query("rp", "two words", ["3John"])["status"] != "RED":
        fails.append("multi-word form must be refused")
    print(json.dumps({"status": "GREEN" if not fails else "RED", "selftest": "word_index", "fails": fails}))
    return 0 if not fails else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) < 3 or sys.argv[1] not in ("rp", "sbl"):
        print(json.dumps({"status": "RED", "usage": "word_index.py rp|sbl FORM [Book ...] | --selftest"}))
        return 2
    books = sys.argv[3:] or g.BOOKS
    if any(b not in g.BOOKS for b in books):
        print(json.dumps({"status": "RED", "error": "unknown book"}))
        return 2
    r = query(sys.argv[1], sys.argv[2], books)
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["status"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
