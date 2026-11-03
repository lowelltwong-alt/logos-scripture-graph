#!/usr/bin/env python3
"""One book's deferred end-review packet (OW-28). Book-agnostic port of sp_durable/Dan/fable_end_review/gen_fable_end_packet.py:
every book fact and pin comes from the book's close parameters.

OW-28: a gate that needs a Fable model is recorded DEFERRED to the campaign-end Fable review, never MET, and each close
carries a packet for that review. This generator packs, deterministically:
  * the routed items, each with the digest of its own line and the landed outputs of the execution it came from, read from
    the pinned landed-outputs manifest (path + sha256);
  * every low and medium_low row of the final corpus, whole, with the digest of its line;
  * each such row's sidecar, when the book's sidecar source is installed; until then the packet says UNAVAILABLE, and the
    close tool's gate on the sidecar digest stays UNMET until this generator is run again;
  * the digest of every input.
Nothing in the packet is a verdict. No clock, no randomness, no directory scan: every input is a named path. A pin still
PENDING is refused. `held_rows` is empty by measurement: the generator refuses if any row carries a hold, because a book
with a hold ruling needs that ruling bound here first.

Usage:  gen_fable_end_packet.py --book BOOK [--m8-root DIR] [--params FILE] [--book-root DIR] [--out-root DIR] (--write | --check)
  --m8-root    the M8 tree (default: found from this file's location)
  --params     the close parameters (default: <BOOK>/close/close_params.v1.json)
  --book-root  the book directory the inputs are read from (default: sp_durable/<BOOK> under the M8 tree)
  --out-root   where the packet is written or checked (default: --book-root)
  --check      regenerate and compare bytes; prints one JSON line, then MATCH or MISMATCH; exit 0 only on MATCH
  --write      write the packet. An existing packet with the same bytes is kept; one with different bytes is first kept
               beside it as <name>.pre_<sha12> (E-44: nothing is overwritten without a kept copy).
"""
import argparse
import collections
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PENDING = "PENDING"
STATUS = ("DEFERRED (OW-28): claude-fable-5-1 reviews this packet at the campaign's end; nothing in this packet is MET, "
          "and no Fable call is made for it without a new owner authorization (OW-30)")


def shab(b):
    return hashlib.sha256(b).hexdigest()


def load(a):
    """The parameters of --book, refused unless they are this book's; PINS from them, a PENDING pin refused."""
    m8 = Path(a.m8_root).resolve() if a.m8_root else HERE.parent.parent
    root = Path(a.book_root).resolve() if a.book_root else m8 / "sp_durable" / a.book
    p = Path(a.params) if a.params else root / "close" / "close_params.v1.json"
    doc = json.loads(p.read_bytes().decode("utf-8"))
    if doc.get("schema") != "m8_close_params.v1" or doc.get("book") != a.book:
        raise SystemExit("REFUSED: %s is not the close parameters of %s" % (p, a.book))
    C = doc["constants"]
    pins = {"corpus": (C["CORPUS"], C["CORPUS_PIN"]), "routed_items": (C["ROUTED_REL"], C["ROUTED_PIN"]),
            "landed_outputs_manifest": (C["LANDED_REL"], C["LANDED_PIN"])}
    held_back = [n for n, (_, pin) in pins.items() if pin == PENDING] + [n for n in ("ROWS", "ROUTED_ITEMS") if C[n] == PENDING]
    if held_back:
        raise SystemExit("REFUSED: PENDING in the parameters: %s" % held_back)
    return root, C, pins


def read_pinned(root, name, PINS):
    rel, pin = PINS[name]
    b = (root / rel).read_bytes()
    if shab(b) != pin:
        raise SystemExit("REFUSED: %s is not the pinned bytes (%s, want %s)" % (rel, shab(b)[:16], pin[:16]))
    if b"\r" in b:
        raise SystemExit("REFUSED: CR byte in %s (E-73: digests are recorded on LF bytes only)" % rel)
    return b


def lines(b):
    return [l for l in b.decode("utf-8").split("\n") if l.strip()]


def build(root, BOOK, C, PINS):
    ROWS, ITEMS, HOLD_FIELDS, SIDECAR = C["ROWS"], C["ROUTED_ITEMS"], C["HOLD_FIELDS"], C["SIDECAR"]
    corpus_b, routed_b, landed_b = (read_pinned(root, n, PINS) for n in ("corpus", "routed_items", "landed_outputs_manifest"))
    rows = [(l, json.loads(l)) for l in lines(corpus_b)]
    items = [(l, json.loads(l)) for l in lines(routed_b)]
    landed = json.loads(landed_b.decode("utf-8"))
    if len(rows) != ROWS or len(items) != ITEMS:
        raise SystemExit("REFUSED: %d rows and %d routed items, want %d and %d" % (len(rows), len(items), ROWS, ITEMS))
    held = [r["decision_id"] for _, r in rows if any(r.get(k) != v for k, v in HOLD_FIELDS.items())]
    if held:
        raise SystemExit("REFUSED: rows carry a hold or a non-final status: %s" % held[:5])
    ids = [it["id"] for _, it in items]
    if len(set(ids)) != len(ids) or any(it.get("book") != BOOK for _, it in items):
        raise SystemExit("REFUSED: routed item ids repeat, or an item names another book (E-65)")
    by_exec = collections.defaultdict(list)
    for o in landed["outputs"]:
        by_exec[o["execution_id"]].append({"path": o["path"], "sha256": o["sha256"]})
    try:
        side_b = (root / SIDECAR).read_bytes()
    except FileNotFoundError:
        side_b = None
    side = {}
    if side_b is not None:
        if b"\r" in side_b:
            raise SystemExit("REFUSED: CR byte in %s" % SIDECAR)
        for l in lines(side_b):
            s = json.loads(l)
            side[s["writer_decision_id"]] = s
    low_rows = []
    for i, (l, r) in enumerate(rows, 1):
        if r["confidence"] not in ("low", "medium_low"):
            continue
        low_rows.append({
            "decision_id": r["decision_id"], "writer_decision_id": r["writer_decision_id"],
            "assembled_decision_id": C["DECISION_ID_FORM"] % i, "span": r["span"], "confidence": r["confidence"],
            "row_line_sha256": shab(l.encode("utf-8")), "row": r,
            "sidecar": side.get(r["writer_decision_id"]) if side_b is not None else
            "UNAVAILABLE: %s is not installed under the book directory; regenerate after the atlas build lands" % SIDECAR})
    if side_b is not None and set(side) != {x["writer_decision_id"] for x in low_rows}:
        raise SystemExit("REFUSED: the sidecar set is not exactly the low and medium_low rows")
    routed = []
    for l, it in items:
        src = sorted(by_exec.get(it["from"], []), key=lambda x: x["path"])
        routed.append({"item": it, "item_line_sha256": shab(l.encode("utf-8")),
                       "source_execution": it["from"],
                       "source_landed_outputs": src if src else
                       "UNAVAILABLE: the landed-outputs manifest lists no output under this id"})
    pk = {
        "schema": "m8_fable_end_review_packet.v1", "book": BOOK, "status": STATUS,
        "reviewer": "claude-fable-5-1, at the campaign's end (OW-28)",
        "corpus": {"file": PINS["corpus"][0], "sha256": shab(corpus_b), "rows": len(rows)},
        "corpus_sha256": shab(corpus_b),
        "row_ids": [x["decision_id"] for x in low_rows],
        "confidence_of_packed_rows": dict(sorted(collections.Counter(x["confidence"] for x in low_rows).items())),
        "rows": low_rows,
        "held_rows": {},
        "held_rows_note": "MEASURED: no row of the corpus carries a hold; the routed items are questions, not holds",
        "sidecar_source": ({"file": SIDECAR, "sha256": shab(side_b), "rows": len(side)} if side_b is not None else
                           {"file": SIDECAR, "sha256": None, "rows": None, "state": "UNAVAILABLE at generation"}),
        "routed_items_count": len(routed),
        "routed_item_ids": ids,
        "routed_items_by_ruling": dict(sorted(collections.Counter(it["ruling"] for _, it in items).items())),
        "routed_items_by_source": dict(sorted(collections.Counter(it["from"] for _, it in items).items())),
        "routed_items": routed,
        "inputs": {n: {"path": "sp_durable/%s/" % BOOK + PINS[n][0], "sha256": PINS[n][1]} for n in sorted(PINS)},
        "tiers": {"digests and counts": "MEASURED by this generator",
                  "rows, sidecars and routed items": "TRANSCRIBED whole from the named inputs",
                  "every ruling, decision and order inside a routed item": "REPORTED by the execution named in its `from`",
                  "source_landed_outputs": "EXTRACTED from the landed-outputs manifest by execution id; the files "
                                           "themselves are not opened here"},
        "limits": ["A packet is material for a review that has not happened. It settles nothing.",
                   "Every lane of this book ran on one model family; agreement among them is one voice (OW-19).",
                   "A routed item's source digests are those of the outputs landed under its execution id, not of a "
                   "passage inside them."],
        "builder": "sp_durable/campaign/gen_fable_end_packet.py",
        "builder_sha256": shab(Path(__file__).read_bytes()),
    }
    return (json.dumps(pk, ensure_ascii=False, indent=1) + "\n").encode("utf-8"), pk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--m8-root")
    ap.add_argument("--params")
    ap.add_argument("--book-root")
    ap.add_argument("--out-root")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    a = ap.parse_args()
    root, C, pins = load(a)
    out = (Path(a.out_root).resolve() if a.out_root else root) / C["PACKET_REL"]
    b, pk = build(root, a.book, C, pins)
    info = {"packet_sha256": shab(b), "bytes": len(b), "rows": len(pk["row_ids"]), "routed_items": pk["routed_items_count"],
            "sidecar_sha256": pk["sidecar_source"]["sha256"], "corpus_sha256": pk["corpus_sha256"]}
    try:
        cur = out.read_bytes()
    except FileNotFoundError:
        cur = None
    if a.check:
        print(json.dumps(info))
        print("MATCH" if cur == b else "MISMATCH")
        return 0 if cur == b else 1
    if cur == b:
        info["written"] = "kept (same bytes)"
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        if cur is not None:
            keep = out.with_name(out.name + ".pre_" + shab(cur)[:12])
            with open(keep, "xb") as fh:
                fh.write(cur)
            info["kept_previous"] = keep.name
        tmp = out.with_name(out.name + ".tmp")
        tmp.write_bytes(b)
        os.replace(tmp, out)
        info["written"] = str(out)
    print(json.dumps(info))
    return 0


if __name__ == "__main__":
    sys.exit(main())
