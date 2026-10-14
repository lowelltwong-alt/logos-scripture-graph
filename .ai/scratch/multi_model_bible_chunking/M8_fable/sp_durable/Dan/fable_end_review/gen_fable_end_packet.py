#!/usr/bin/env python3
"""Daniel's deferred end-review packet (OW-28). Ported from sp_durable/Ezek/fable_end_review/gen_fable_end_packet.py.

OW-28: a gate that needs a Fable model is recorded DEFERRED to the campaign-end Fable review, never MET, and each close
carries a packet for that review. This generator packs, deterministically:
  * the 46 routed items (fable_end_review/routed_items.v1.jsonl), each with the digest of its own line and the landed
    outputs of the execution it came from, read from the pinned landed-outputs manifest (path + sha256);
  * every low and medium_low row of the final corpus, whole, with the digest of its line;
  * each such row's sidecar, when sidecar_src_dan.jsonl is installed; until then the packet says UNAVAILABLE, and the
    close tool's gate on the sidecar digest stays UNMET until this generator is run again;
  * the digest of every input.
Nothing in the packet is a verdict. No clock, no randomness, no directory scan: every input is a named path.

Daniel differs from Ezekiel: no held row and no hold ruling exist, so `held_rows` is empty by measurement (the generator
refuses if any row carries a hold), and there is no delta landing to bind.

Usage:  gen_fable_end_packet.py [--dan-root DIR] [--out-root DIR] (--write | --check)
  --dan-root  the installed Daniel directory (default: the parent of this file's directory)
  --out-root  where fable_end_review/Dan_fable_end_packet.v1.json is written or checked (default: --dan-root)
  --check     regenerate and compare bytes; prints one JSON line, then MATCH or MISMATCH; exit 0 only on MATCH
  --write     write the packet. An existing packet with the same bytes is kept; one with different bytes is first kept
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
BOOK = "Dan"
PACKET = "Dan_fable_end_packet.v1.json"
# name -> (path under --dan-root, pinned sha256). MEASURED 2026-10-12 by work/pin_check.py over the brief's pins.
PINS = {
    "corpus": ("rows_v1_final.jsonl", "783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09"),
    "routed_items": ("fable_end_review/routed_items.v1.jsonl", "42efe601b731e212ba60bc9b19fd9b3199d86e8d5a152bb7571f8e956376b0d6"),
    "landed_outputs_manifest": ("close/dan_landed_outputs_manifest.v2.json", "5fadae2c09ab3bdc9a51184e40f72bc13a1b0e0182a39c070bebde99d9be9449"),
}
SIDECAR = "sidecar_src_dan.jsonl"  # optional until the atlas build is installed; never pinned here, its digest is recorded
ROWS, ITEMS = 75, 46
HOLD_FIELDS = {"review_status": "candidate_review_complete", "candidate_hold_state": None, "candidate_hold_basis": None}
STATUS = ("DEFERRED (OW-28): claude-fable-5-1 reviews this packet at the campaign's end; nothing in this packet is MET, "
          "and no Fable call is made for it without a new owner authorization (OW-30)")


def shab(b):
    return hashlib.sha256(b).hexdigest()


def read_pinned(root, name):
    rel, pin = PINS[name]
    b = (root / rel).read_bytes()
    if shab(b) != pin:
        raise SystemExit("REFUSED: %s is not the pinned bytes (%s, want %s)" % (rel, shab(b)[:16], pin[:16]))
    if b"\r" in b:
        raise SystemExit("REFUSED: CR byte in %s (E-73: digests are recorded on LF bytes only)" % rel)
    return b


def lines(b):
    return [l for l in b.decode("utf-8").split("\n") if l.strip()]


def build(root):
    corpus_b, routed_b, landed_b = (read_pinned(root, n) for n in ("corpus", "routed_items", "landed_outputs_manifest"))
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
            "assembled_decision_id": "M8-%s-%03d" % (BOOK, i), "span": r["span"], "confidence": r["confidence"],
            "row_line_sha256": shab(l.encode("utf-8")), "row": r,
            "sidecar": side.get(r["writer_decision_id"]) if side_b is not None else
            "UNAVAILABLE: %s is not installed under --dan-root; regenerate after the atlas build lands" % SIDECAR})
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
        "inputs": {n: {"path": "sp_durable/Dan/" + PINS[n][0], "sha256": PINS[n][1]} for n in sorted(PINS)},
        "tiers": {"digests and counts": "MEASURED by this generator",
                  "rows, sidecars and routed items": "TRANSCRIBED whole from the named inputs",
                  "every ruling, decision and order inside a routed item": "REPORTED by the execution named in its `from`",
                  "source_landed_outputs": "EXTRACTED from the landed-outputs manifest by execution id; the files "
                                           "themselves are not opened here"},
        "limits": ["A packet is material for a review that has not happened. It settles nothing.",
                   "Every lane of this book ran on one model family; agreement among them is one voice (OW-19).",
                   "A routed item's source digests are those of the outputs landed under its execution id, not of a "
                   "passage inside them."],
        "builder": "sp_durable/Dan/fable_end_review/gen_fable_end_packet.py",
        "builder_sha256": shab(Path(__file__).read_bytes()),
    }
    return (json.dumps(pk, ensure_ascii=False, indent=1) + "\n").encode("utf-8"), pk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dan-root")
    ap.add_argument("--out-root")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    a = ap.parse_args()
    root = Path(a.dan_root).resolve() if a.dan_root else HERE.parent
    out = (Path(a.out_root).resolve() if a.out_root else root) / "fable_end_review" / PACKET
    b, pk = build(root)
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
