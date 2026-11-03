#!/usr/bin/env python3
"""Bind a reviewer's per-unit classes of the corpus-wide sweep to one corpus: the hand record the parity arm reads.

The orchestrator classes nothing here. Each counter's hit list comes from a run of the sweep over the corpus; each unit's class
comes from the named review record, joined per row in hit order, the field equal or recorded "as swept". Any hit without a matching class, or with a class outside
--clears, stays residual, and a residual above zero means the parity arm stays RED. Book-agnostic (TE-7).

usage (from SP): python -B campaign/close_kit/gen_cwo_hand_record.py --book BOOK --corpus REL --review REL --unchanged REL
                 --map COUNTER=ORDER_ID [--map ...] --clears CLASS [--clears ...] --out REL [--check]
"""
import argparse
import collections
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from _cwo_parity import hits_digest  # noqa: E402


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    for name in ("book", "corpus", "review", "unchanged", "out"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--map", action="append", required=True)
    ap.add_argument("--clears", action="append", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    bk = HERE.parent / a.book
    K = json.loads((bk / "close" / "close_params.v1.json").read_text(encoding="utf-8"))["constants"]["CWO"]
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "sweep.json"
        r = subprocess.run([sys.executable, "-B", str(bk / K["sweep_tool"]), a.corpus, "--out", str(out)], capture_output=True, cwd=str(bk))
        if r.returncode:
            raise SystemExit("REFUSED: the sweep failed: %s" % r.stderr.decode("utf-8", "replace")[-300:])
        sweep = json.loads(out.read_text(encoding="utf-8"))
    rev_b, same_b = (bk / a.review).read_bytes(), (bk / a.unchanged).read_bytes()
    rev, same = json.loads(rev_b)["cwo"], json.loads(same_b)["cwo"]
    if same["pre"] != same["post"] or same["changed_classes"]:
        raise SystemExit("REFUSED: the later review records a changed class; these classes do not carry")
    orders = {}
    for item in a.map:
        key, _, order = item.partition("=")
        hits, classes = sweep[key].get("list") or [], rev[order]["my_classes"]
        pool = collections.defaultdict(list)
        for c in classes:
            pool[c["row"]].append(c)
        joined = []
        for h in hits:  # within a row the review lists its classes in hit order
            c = pool[h["row"]].pop(0) if pool[h["row"]] else None
            if c and c["field"] in (h["field"], "as swept"):
                joined.append((h, c))
        tally = collections.Counter(c["class"] for _, c in joined)
        cleared = sum(c["class"] in a.clears for _, c in joined)
        orders[key] = {"order": order, "hits": len(hits), "hits_sha256": hits_digest(hits), "joined": len(joined),
                       "classes": dict(sorted(tally.items())), "residual": len(hits) - cleared}
    doc = {"schema": "m8_cwo_hand_record.v1", "book": a.book, "corpus": a.corpus, "corpus_sha256": sha((bk / a.corpus).read_bytes()),
           "tier": "MEASURED (the sweep and the digests); REPORTED (the classes, the review named here)",
           "classes_from": {"path": a.review, "sha256": sha(rev_b)}, "unchanged_per": {"path": a.unchanged, "sha256": sha(same_b)},
           "clearing_classes": sorted(a.clears), "orders": orders}
    data = (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    target = bk / a.out
    if a.check:
        print("MATCH" if target.read_bytes() == data else "DIFFERS")
        return
    if target.exists() and target.read_bytes() != data:
        raise SystemExit("REFUSED: %s exists with other bytes" % a.out)
    target.write_bytes(data)
    print(json.dumps({"sha256": sha(data), "residual": {k: v["residual"] for k, v in orders.items()},
                      "classes": {k: v["classes"] for k, v in orders.items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
