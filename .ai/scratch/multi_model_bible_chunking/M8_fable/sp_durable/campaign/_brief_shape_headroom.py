"""Measure how much room a brief's example wording leaves under the ngram7 gate, and refuse a shape that leaves too little.

Why this exists (control from the FIXUP-3 run-1 failure, CYCLE_STATE 2026-09-12 and learning log L-0012): the FIXUP-3 brief offered
mark-disclosure shapes as literal sentences. Shape A's tail already stood in 6 rows from an earlier wave, so with the gate at 10 only three
more rows could carry it. One author used it in four rows and the applied corpus failed the HARD ngram7 gate. A brief that hands authors
literal wording is handing every author the same 7-grams; whether that crosses the gate is a measurable fact about the corpus, not a matter
of telling authors to vary.

The arithmetic: a gram already standing in R rows of the corpus fails once R + W >= GATE, where W is the number of rows this wave could add.
The wave's part count is the honest upper bound for W when every part may use the shape once, so a shape is SAFE only when

    R + parts <= GATE - 1,   i.e.   headroom = GATE - 1 - R >= parts.

Tokenization is not reimplemented here: this imports the book's installed ngram7 and uses its own prose walk, its Hebrew and quotation
stripping, its citation-apparatus regex and its WEB 7-gram exclusion. A private copy of that pipeline would drift from the gate it predicts,
which is the failure this control exists to stop. The installed tool's digest is reported so a brief can pin what measured it.

A shape is measured as the brief will hand it over: its own 7-grams, less any that occur in the WEB text (ngram7 excludes those, so they
cannot fail the gate).

Usage:
  _brief_shape_headroom.py --book Ezek --corpus repair/rows_v6_fixup3.jsonl --shapes shapes.json --parts 6 [--gate 10] [--out report.json]

--shapes is a JSON list of {"id": "...", "text": "the literal sentence the brief would offer"}; a bare list of strings is also accepted.
Exit status is 1 when any shape is REFUSED, so a brief builder can make this a hard stop.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_ngram7(book: str):
    """Import the book's installed ngram7 with its own tools dir on the path and the book dir as cwd (load_verse_maps reads relative)."""
    tools = SP / book / "tools"
    mod_path = tools / "ngram7.py"
    if not mod_path.is_file():
        raise SystemExit("ABORT: %s does not exist" % mod_path)
    sys.path.insert(0, str(tools))
    cwd = Path.cwd()
    os.chdir(SP / book)
    try:
        spec = importlib.util.spec_from_file_location("ngram7_installed_%s" % book, mod_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        web, _ = mod.load_verse_maps()
    finally:
        os.chdir(cwd)
    return mod, web, sha(mod_path)


def grams_of(mod, text: str) -> list[str]:
    """The 7-grams of a string under the installed tool's own pipeline."""
    s = mod.HEB_RUN.sub(" ", text)
    s = re.sub(r"\u201c[^\u201d]*\u201d", " ", s)
    s = mod.REF_TOKENS.sub(" ", s)
    toks = re.findall(r"[a-z]+", mod.norm_english(s).lower())
    return [" ".join(toks[i:i + 7]) for i in range(len(toks) - 6)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--corpus", required=True, help="rows file, absolute or relative to the book dir")
    ap.add_argument("--shapes", required=True)
    ap.add_argument("--parts", type=int, required=True, help="rows this wave could add: the part count when every part may use the shape once")
    ap.add_argument("--gate", type=int, default=None)
    # A brief writes its shapes with placeholders ('MT <c>:<v>'), but an author writes a real key ('MT 24:27'), which the installed tool
    # strips as citation apparatus before tokenizing. Measuring the placeholder text would yield grams containing 'mt c v' that no row can
    # ever carry, and would miss the grams that actually run across the key. So the placeholders are realized first, with any concrete key:
    # which key does not matter, because the tool removes it either way.
    ap.add_argument("--realize", default='{"<c>:<v>": "24:27", "<c>": "24", "<v>": "27"}',
                    help="JSON map of placeholder -> concrete text, applied to each shape before measuring")
    ap.add_argument("--out")
    a = ap.parse_args()
    realize_map = json.loads(a.realize)

    def realize(text: str) -> str:
        for k, v in sorted(realize_map.items(), key=lambda kv: -len(kv[0])):
            text = text.replace(k, v)
        return text

    mod, web, tool_sha = load_ngram7(a.book)
    gate = a.gate if a.gate is not None else mod.GATE
    corpus = Path(a.corpus) if Path(a.corpus).is_absolute() else SP / a.book / a.corpus
    if not corpus.is_file():
        raise SystemExit("ABORT: corpus %s does not exist" % corpus)
    shapes = json.loads(Path(a.shapes).read_text(encoding="utf-8"))
    shapes = [{"id": "shape_%d" % i, "text": s} if isinstance(s, str) else s for i, s in enumerate(shapes, 1)]
    if not shapes:
        raise SystemExit("ABORT: no shapes given")

    webtext = mod.norm_english(" ".join(d["text"] for d in web.values())).lower()
    web_tokens = re.findall(r"[a-z]+", webtext)
    web_7grams = {" ".join(web_tokens[i:i + 7]) for i in range(len(web_tokens) - 6)}

    # every 7-gram of the corpus, with the rows it stands in, under the installed pipeline
    corpus_rows = 0
    corpus_grams: dict[str, set[str]] = {}
    for row in mod.rows_from(corpus):
        if not isinstance(row, dict):
            continue
        rid = row.get("decision_id") or "row_%d" % corpus_rows
        corpus_rows += 1
        for g in grams_of(mod, mod.prose(row)):
            if g not in web_7grams:
                corpus_grams.setdefault(g, set()).add(rid)

    results, refused = [], 0
    for sh in shapes:
        realized = realize(sh["text"])
        gs = [g for g in grams_of(mod, realized) if g not in web_7grams]
        measured = []
        for g in gs:
            rows = sorted(corpus_grams.get(g, ()))
            measured.append({"gram": g, "rows_in_corpus": len(rows), "headroom": gate - 1 - len(rows), "row_ids": rows})
        worst = min(measured, key=lambda m: m["headroom"]) if measured else None
        if not gs:
            verdict, why = "SAFE", "the shape yields no 7-gram outside the WEB text, so it cannot reach the gate"
        elif worst["headroom"] < a.parts:
            verdict, why = "REFUSE", ("'%s' already stands in %d of %d rows; with the gate at %d only %d more rows may carry it, and this "
                                      "wave has %d parts" % (worst["gram"], worst["rows_in_corpus"], corpus_rows, gate,
                                                             max(worst["headroom"], 0), a.parts))
        else:
            verdict, why = "SAFE", ("the tightest gram '%s' stands in %d rows, leaving room for %d more against this wave's %d parts"
                                    % (worst["gram"], worst["rows_in_corpus"], worst["headroom"], a.parts))
        refused += verdict == "REFUSE"
        results.append({"id": sh.get("id"), "text": sh["text"], "measured_as": realized, "verdict": verdict, "why": why,
                        "grams_measured": len(gs), "tightest": worst, "grams": measured})

    report = {"schema": "m8_brief_shape_headroom.v1", "book": a.book, "corpus": str(corpus), "corpus_sha256": sha(corpus)[:16],
              "corpus_rows": corpus_rows, "gate": gate, "parts": a.parts,
              "measured_by": {"tool": str(SP / a.book / "tools" / "ngram7.py"), "tool_sha256": sha(SP / a.book / "tools" / "ngram7.py")[:16],
                              "note": "tokenization, stripping and WEB exclusion are the installed tool's own, not a copy"},
              "rule": "a shape is SAFE only when gate - 1 - rows_already_carrying_the_gram >= parts",
              "placeholders_realized": realize_map,
              "verdict": "REFUSE" if refused else "SAFE", "refused": refused, "shapes": results}
    assert tool_sha == report["measured_by"]["tool_sha256"] or tool_sha.startswith(report["measured_by"]["tool_sha256"])
    if a.out:
        Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report if not a.out else {k: report[k] for k in ("verdict", "refused", "gate", "parts", "corpus_rows", "corpus_sha256")},
                     ensure_ascii=False, indent=1))
    if a.out:
        print("report: %s" % a.out)
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
