#!/usr/bin/env python3
r"""OW-2 item-2 audit batch verifier — run after every audit batch.

Per batch: packet parses; attempt_id + book match the slice; exactly one entry
per assigned row, in order, none outside; verdict/severity vocabulary; findings
on every defect row (none on clean rows); every finding carries a BOOLEAN
span_change (the item-1 hardening — no pattern fallback) and non-empty
grounds; every slice trigger tag is dispositioned exactly once with the
allowed vocabulary and non-empty grounds; a confirmed_defect trigger requires
a defect verdict; summary tallies (rows, findings, span changes, triggers)
recomputed; normalize dry-run byte-clean with the BOOK's own normalizer
(SP\<Book>\tools\normalize_hebrew_in_json.py); the routing queue (every
medium/high finding + every span-flagged finding) extracted for the Fable
adjudication lane; the per-book toolkit trees checked against the staging
manifest (E-21 stray/mutation detector, via _ow2i2_toolkit_manifest.py).
Usage: _ow2i2_verify.py i2_Ps_01 [i2_Ps_02 ...] [--reviews-dir DIR] [--no-manifest]
  --reviews-dir DIR  read packets from DIR instead of ./reviews (fixture proof runs
                     only — never for real verification); flags are consumed WITH
                     their values before positional parsing (E-20 flag-value law).
  --no-manifest      skip the per-book toolkit manifest guard (fixture runs only).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
SEVS = {"low", "medium", "high"}
DISPOSITIONS = {"confirmed_defect", "not_a_defect"}

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("batches", nargs="*")
ap.add_argument("--reviews-dir", default=None)
ap.add_argument("--no-manifest", action="store_true")
ns = ap.parse_args()
args = ns.batches
if not args:
    print("usage: _ow2i2_verify.py i2_Ps_01 [i2_Job_03 ...] [--reviews-dir DIR] [--no-manifest]")
    sys.exit(2)
REVIEWS_DIR = Path(ns.reviews_dir).resolve() if ns.reviews_dir else None


def grounds_text(g, note: dict):
    """grounds may be a string or a list of strings (an accepted shape deviation —
    counted in note['grounds_as_list'] so the census can record it); any other
    type is returned as None (a reported problem, never a crash)."""
    if isinstance(g, str):
        return g
    if isinstance(g, list) and all(isinstance(x, str) for x in g):
        note["grounds_as_list"] = note.get("grounds_as_list", 0) + 1
        return " | ".join(x.strip() for x in g)
    return None


results = {}
census = {"rows": 0, "clean": 0, "defect_rows": 0, "low": 0, "medium": 0, "high": 0,
          "span_changes_proposed": 0, "triggers": 0, "confirmed_defect": 0,
          "not_a_defect": 0, "files": 0}
per_book = {}
routing_queue = []
hard_fail = False
books_seen = set()
for b in args:
    sl = json.load(open(HERE / "slices" / f"slice_{b}.json", encoding="utf-8"))
    book = sl["book"]
    books_seen.add(book)
    fname = sl["output_file"]
    out_path = (REVIEWS_DIR / Path(fname).name) if REVIEWS_DIR else (HERE / fname)
    probs = []
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
    rows = doc.get("rows") or []
    got = [r.get("row_id") for r in rows]
    if got != sl["row_ids"]:
        probs.append(f"row ids {got} != assigned {sl['row_ids']}")
    tall = {"rows": 0, "clean": 0, "defect_rows": 0, "low": 0, "medium": 0, "high": 0,
            "span_changes_proposed": 0, "triggers": 0, "confirmed_defect": 0, "not_a_defect": 0}
    note = {}
    for r in rows:
        rid = r.get("row_id")
        v = r.get("verdict")
        finds = r.get("findings") or []
        trigs = r.get("triggers") or []
        if v not in ("clean", "defect"):
            probs.append(f"{rid}: bad verdict {v}")
        if v == "defect" and not finds:
            probs.append(f"{rid}: defect with no findings")
        if v == "clean" and finds:
            probs.append(f"{rid}: clean but carries findings")
        tall["rows"] += 1
        tall["clean"] += v == "clean"
        tall["defect_rows"] += v == "defect"
        # trigger dispositions: exactly the assigned tags, each once
        want = list(sl["trigger_tags_by_row"].get(rid, []))
        got_tags = [t.get("tag") for t in trigs]
        if sorted(got_tags) != sorted(want):
            probs.append(f"{rid}: trigger tags {got_tags} != assigned {want}")
        for t in trigs:
            d = t.get("disposition")
            if d not in DISPOSITIONS:
                probs.append(f"{rid}: trigger {t.get('tag')} bad disposition {d}")
                continue
            tg = grounds_text(t.get("grounds"), note)
            if tg is None:
                probs.append(f"{rid}: trigger {t.get('tag')} grounds of unsupported type {type(t.get('grounds')).__name__}")
            elif not tg.strip():
                probs.append(f"{rid}: trigger {t.get('tag')} empty grounds")
            if d == "confirmed_defect" and v != "defect":
                probs.append(f"{rid}: trigger {t.get('tag')} confirmed_defect on a clean row")
            tall["triggers"] += 1
            tall[d] += 1
        for f in finds:
            sev = f.get("severity")
            if sev not in SEVS:
                probs.append(f"{rid}: bad severity {sev}")
                continue
            fg = grounds_text(f.get("grounds"), note)
            if fg is None:
                probs.append(f"{rid}: finding grounds of unsupported type {type(f.get('grounds')).__name__}")
            elif not fg.strip():
                probs.append(f"{rid}: finding with empty grounds")
            explicit = f.get("span_change")
            if not isinstance(explicit, bool):
                probs.append(f"{rid}: finding lacks a boolean span_change")
                explicit = False
            tall[sev] += 1
            if explicit:
                tall["span_changes_proposed"] += 1
            if sev in ("medium", "high") or explicit:
                routing_queue.append({"batch": b, "book": book, "row_id": rid, "severity": sev,
                                      "claim": (f.get("claim") or "")[:160], "span_change": explicit})
    summ = doc.get("summary") or {}
    sf = summ.get("findings") or {}
    st = summ.get("triggers") or {}
    checks = [("rows", summ.get("rows"), tall["rows"]), ("clean", summ.get("clean"), tall["clean"]),
              ("defect_rows", summ.get("defect_rows"), tall["defect_rows"]),
              ("findings.low", sf.get("low"), tall["low"]), ("findings.medium", sf.get("medium"), tall["medium"]),
              ("findings.high", sf.get("high"), tall["high"]),
              ("span_changes_proposed", summ.get("span_changes_proposed"), tall["span_changes_proposed"]),
              ("triggers.total", st.get("total"), tall["triggers"]),
              ("triggers.confirmed_defect", st.get("confirmed_defect"), tall["confirmed_defect"]),
              ("triggers.not_a_defect", st.get("not_a_defect"), tall["not_a_defect"])]
    for name, said, real in checks:
        if said != real:
            probs.append(f"summary {name} {said} != recomputed {real}")
    norm_tool = SP / book / "tools" / "normalize_hebrew_in_json.py"
    norm = subprocess.run([sys.executable, str(norm_tool), str(out_path)],
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

# toolkit manifest guard (E-21) over every book touched by this run
manifest_check = None
if books_seen and not ns.no_manifest:
    mc = subprocess.run([sys.executable, str(HERE / "_ow2i2_toolkit_manifest.py"), "--check"],
                        capture_output=True, text=True, encoding="utf-8")
    try:
        manifest_check = json.loads(mc.stdout)
    except json.JSONDecodeError:
        manifest_check = {"status": "UNPARSEABLE", "raw": (mc.stdout + mc.stderr)[-400:]}
    if manifest_check.get("status") != "CLEAN":
        hard_fail = True

print(json.dumps({"batch": args,
                  "verify": "FAIL" if hard_fail else "PASS",
                  "census": census,
                  "per_book": per_book,
                  "routing_queue_size": len(routing_queue),
                  "routing_queue": routing_queue,
                  "toolkit_manifest": manifest_check,
                  "results": results},
                 ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
