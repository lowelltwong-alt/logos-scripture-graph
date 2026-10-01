#!/usr/bin/env python3
r"""OW-2 item-2/3 Fable-adjudication batch verifier — run after every batch.

Per batch: packet parses; attempt_id + book match the slice; exactly one entry per
assigned item id, in order, none outside; verdict vocabulary; coherence laws
(refute=>none; confirm=>filed severity; downgrade strictly lower never none; upgrade
strictly higher; span_ruling n/a exactly when span_change false); grounds non-empty
(string or list of strings; other types reported); summary tallies recomputed;
normalize dry-run byte-clean with the BOOK's normalizer; the five-book toolkit
manifest checked (E-21 guard) unless --no-manifest.
Usage: _ow2i2adj_verify.py i2adj_Ps_01 [i2adj_Job_01 ...] [--reviews-dir DIR] [--no-manifest]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}
VERDICTS = {"confirm", "downgrade", "upgrade", "refute"}
RULINGS = {"n/a", "endorse_proposal", "decline_proposal", "defer_book_level"}

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("batches", nargs="*")
ap.add_argument("--reviews-dir", default=None)
ap.add_argument("--no-manifest", action="store_true")
ns = ap.parse_args()
args = ns.batches
if not args:
    print("usage: _ow2i2adj_verify.py i2adj_Ps_01 [...] [--reviews-dir DIR] [--no-manifest]")
    sys.exit(2)
REVIEWS_DIR = Path(ns.reviews_dir).resolve() if ns.reviews_dir else None


def grounds_text(g, note):
    if isinstance(g, str):
        return g
    if isinstance(g, list) and all(isinstance(x, str) for x in g):
        note["grounds_as_list"] = note.get("grounds_as_list", 0) + 1
        return " | ".join(x.strip() for x in g)
    return None


results = {}
census = {"items": 0, "confirm": 0, "downgrade": 0, "upgrade": 0, "refute": 0,
          "final_none": 0, "final_low": 0, "final_medium": 0, "final_high": 0,
          "span_endorsed": 0, "span_declined": 0, "book_level_deferred": 0, "files": 0}
per_book = {}
hard_fail = False
for b in args:
    sl = json.load(open(HERE / "slices" / f"slice_{b}.json", encoding="utf-8"))
    book = sl["book"]
    filed = {}
    for r in sl["rows"]:
        for it in r["queue_items"]:
            filed[it["item_id"]] = it
    fname = sl["output_file"]
    out_path = (REVIEWS_DIR / Path(fname).name) if REVIEWS_DIR else (HERE / fname)
    probs = []
    note = {}
    if not out_path.exists():
        results[fname] = {"status": "FAIL", "problems": ["output MISSING"]}
        hard_fail = True
        continue
    try:
        doc = json.load(open(out_path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        results[fname] = {"status": "FAIL", "problems": [f"unparseable: {e}"]}
        hard_fail = True
        continue
    if doc.get("attempt_id") != sl["attempt_id"]:
        probs.append(f"attempt_id {doc.get('attempt_id')} != {sl['attempt_id']}")
    if doc.get("book") != book:
        probs.append(f"book {doc.get('book')} != {book}")
    # OW-3 item 3: unexpanded {placeholder} tokens are rejected (resolve from source bytes first)
    for m in re.finditer(r"\{[A-Za-z0-9][A-Za-z0-9_\-\.:]*\}", json.dumps(doc, ensure_ascii=False)):
        probs.append(f"unexpanded placeholder {m.group(0)}")
        break
    items = doc.get("items") or []
    got = [i.get("item_id") for i in items]
    if got != sl["item_ids"]:
        probs.append(f"item ids {got} != assigned {sl['item_ids']}")
    tall = {"items": 0, "confirm": 0, "downgrade": 0, "upgrade": 0, "refute": 0,
            "final_none": 0, "final_low": 0, "final_medium": 0, "final_high": 0,
            "span_endorsed": 0, "span_declined": 0, "book_level_deferred": 0}
    for i in items:
        iid = i.get("item_id")
        f = filed.get(iid)
        v = i.get("verdict")
        fs = i.get("final_severity")
        sr = i.get("span_ruling")
        if v not in VERDICTS:
            probs.append(f"{iid}: bad verdict {v}")
            continue
        if fs not in RANK:
            probs.append(f"{iid}: bad final_severity {fs}")
            continue
        if sr not in RULINGS:
            probs.append(f"{iid}: bad span_ruling {sr}")
            continue
        g = grounds_text(i.get("grounds"), note)
        if g is None:
            probs.append(f"{iid}: grounds of unsupported type {type(i.get('grounds')).__name__}")
        elif not g.strip():
            probs.append(f"{iid}: empty grounds")
        if f is not None:
            orig = f["severity"]
            if f.get("row_id") != i.get("row_id"):
                probs.append(f"{iid}: row_id mismatch")
            if v == "refute" and fs != "none":
                probs.append(f"{iid}: refute with final {fs}")
            if v == "confirm" and fs != orig:
                probs.append(f"{iid}: confirm but final {fs} != filed {orig}")
            if v == "downgrade" and not (0 < RANK[fs] < RANK[orig]):
                probs.append(f"{iid}: downgrade {orig}->{fs} incoherent")
            if v == "upgrade" and not (RANK[fs] > RANK[orig]):
                probs.append(f"{iid}: upgrade {orig}->{fs} incoherent")
            want_ruling = bool(f.get("span_change"))
            if want_ruling and sr == "n/a":
                probs.append(f"{iid}: span item with span_ruling n/a")
            if not want_ruling and sr != "n/a":
                probs.append(f"{iid}: non-span item with span_ruling {sr}")
        tall["items"] += 1
        tall[v] += 1
        tall[f"final_{fs}"] += 1
        tall["span_endorsed"] += sr == "endorse_proposal"
        tall["span_declined"] += sr == "decline_proposal"
        tall["book_level_deferred"] += sr == "defer_book_level"
    summ = doc.get("summary") or {}
    fin = summ.get("final") or {}
    checks = [("items", summ.get("items"), tall["items"]), ("confirm", summ.get("confirm"), tall["confirm"]),
              ("downgrade", summ.get("downgrade"), tall["downgrade"]), ("upgrade", summ.get("upgrade"), tall["upgrade"]),
              ("refute", summ.get("refute"), tall["refute"]),
              ("final.none", fin.get("none"), tall["final_none"]), ("final.low", fin.get("low"), tall["final_low"]),
              ("final.medium", fin.get("medium"), tall["final_medium"]), ("final.high", fin.get("high"), tall["final_high"]),
              ("span_endorsed", summ.get("span_endorsed"), tall["span_endorsed"]),
              ("span_declined", summ.get("span_declined"), tall["span_declined"]),
              ("book_level_deferred", summ.get("book_level_deferred"), tall["book_level_deferred"])]
    for name, said, real in checks:
        if said != real:
            probs.append(f"summary {name} {said} != recomputed {real}")
    norm = subprocess.run([sys.executable, str(SP / book / "tools" / "normalize_hebrew_in_json.py"), str(out_path)],
                          capture_output=True, text=True, encoding="utf-8")
    try:
        nout = json.loads(norm.stdout)
        if nout.get("fixed", 0) or nout.get("defect_count", 0):
            probs.append(f"nfd: fixed={nout.get('fixed')} defects={nout.get('defect_count')} {nout.get('defects')}")
    except json.JSONDecodeError:
        probs.append(f"normalize unparseable: {norm.stdout[-200:]} {norm.stderr[-200:]}")
    status = "PASS" if not probs else "FAIL"
    if probs:
        hard_fail = True
    results[fname] = {"status": status, "problems": probs, "schema_notes": note}
    for k in tall:
        census[k] += tall[k]
    pb = per_book.setdefault(book, {k: 0 for k in tall})
    for k in tall:
        pb[k] += tall[k]
    census["files"] += 1

manifest_check = None
if not ns.no_manifest:
    mc = subprocess.run([sys.executable, str(HERE / "_ow2i2_toolkit_manifest.py"), "--check"],
                        capture_output=True, text=True, encoding="utf-8")
    try:
        manifest_check = json.loads(mc.stdout)
    except json.JSONDecodeError:
        manifest_check = {"status": "UNPARSEABLE", "raw": (mc.stdout + mc.stderr)[-400:]}
    if manifest_check.get("status") != "CLEAN":
        hard_fail = True

print(json.dumps({"batch": args, "verify": "FAIL" if hard_fail else "PASS", "census": census,
                  "per_book": per_book, "toolkit_manifest": manifest_check, "results": results},
                 ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
