#!/usr/bin/env python3
"""CWO execution parity for one book's close: one record, bound to ONE corpus sha256, showing that every corpus-wide order
still holds over the bytes that will be assembled (E-18, close-gate item 5). Book-agnostic port of Dan/_cwo_parity_dan.py:
everything that names a book comes from the book's close parameters (constant CWO).

TWO ADAPTERS, because a book's sweep tool writes one of two forms.
  orders    The sweep writes `orders` with hit counts and `rows_sha256` (Daniel). Exact orders need zero hits; the zone order
            runs the sweep's dispose tool and needs zero zone hits. Byte-for-byte the record Daniel's tool wrote.
  counters  The sweep writes one block per order with a counter and a `list` (1 Corinthians). Every counter must be zero, or
            be cleared by a pinned hand record that binds that counter's exact hit list by digest with residual 0. A mechanical
            class is never a clearance. Without that record a nonzero counter is RESIDUAL and the status is RED.

Second witnesses are read from the corpus's own validator report. The widened id arm is this tool's own measure, reported
beside the orders; a hit there sets status FINDING, because a row id in prose is the defect such an order names.

NEVER OVERWRITES. An existing output with the same bytes is left in place; if its bytes differ, the tool refuses.
Usage: _cwo_parity.py --book BOOK [--check] [--m8-root DIR] [--params FILE]
  --check  recompute and compare with the installed record, write nothing. Exit 0 only on MATCH and GREEN.
No clock, no randomness, no directory scan. Non-authorizing.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PENDING = "PENDING"
CR, LF = b"\r", b"\n"


def shab(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return shab(Path(p).read_bytes())


def dump(o):
    return (json.dumps(o, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def strs(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from strs(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from strs(x)


def lf(p):
    return Path(p).read_bytes().replace(CR + LF, LF)


def hits_digest(hits):
    """The digest a hand record binds: one counter's whole hit list, canonical JSON."""
    return shab(json.dumps(hits, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load(a):
    m8 = Path(a.m8_root).resolve() if a.m8_root else HERE.parent.parent
    bk = m8 / "sp_durable" / a.book
    p = Path(a.params) if a.params else bk / "close" / "close_params.v1.json"
    doc = json.loads(p.read_bytes().decode("utf-8"))
    if doc.get("schema") != "m8_close_params.v1" or doc.get("book") != a.book:
        raise SystemExit("REFUSED: %s is not the close parameters of %s" % (p, a.book))
    return bk, doc["constants"]


def orders_arm(K, sweep, disp):
    orders = sweep["orders"]
    zone = [h for h in disp["hits"] if h.get("disposition") == "zone"]
    parity, residual = {}, []
    for k in K["exact_orders"]:
        hits = orders[k].get("hits") or []
        n = orders[k]["hit_count"]
        parity[k] = {"arm": "exact", "method": K["exact_method"],
                     "status": "COVERED" if n == 0 else "RESIDUAL", "residual_count": n, "tier": "MEASURED"}
        if n:
            residual.append({"order": k, "hits": hits if isinstance(hits, list) else n})
    z = K["zone_order"]
    parity[z] = {"arm": K["zone_arm"], "method": K["zone_method"], "status": "COVERED" if not zone else "RESIDUAL",
                 "hit_count": orders[z]["hit_count"], "counts_by_disposition": disp["counts"], "residual_count": len(zone),
                 "tier": "MEASURED", "disposition_tier": K["zone_tier"]}
    if zone:
        residual.append({"order": z, "hits": zone})
    return parity, residual


def counters_arm(K, sweep, hand, csha):
    """A counter is COVERED at zero, or when the hand record binds this exact hit list over this exact corpus with residual 0."""
    parity, residual = {}, []
    orders = hand.get("orders") or {} if hand and hand.get("corpus_sha256") == csha else {}
    for key, field in K["counters"]:
        block = sweep[key]
        n, hits = block[field], block.get("list") or []
        e = orders.get(key) or {}
        cleared = bool(n) and e.get("hits") == n and e.get("hits_sha256") == hits_digest(hits) and e.get("residual") == 0
        parity[key] = {"arm": "exact", "method": "%s over the corpus" % K["sweep_tool"], "hit_count": n,
                       "status": "COVERED" if not n else ("COVERED_BY_HAND_RECORD" if cleared else "RESIDUAL"),
                       "residual_count": 0 if (cleared or not n) else n, "hits_sha256": hits_digest(hits),
                       "tier": "MEASURED" if not cleared else "MEASURED (the digest); REPORTED (the hand classes)"}
        if n and not cleared:
            residual.append({"order": key, "hits": hits if isinstance(hits, list) else n})
    return parity, residual


def compute(tmp, a, bk, C):
    K, corpus_name = C["CWO"], C["CORPUS"]
    if K.get("adapter") not in ("orders", "counters"):
        raise SystemExit("REFUSED: unknown sweep adapter %r" % K.get("adapter"))
    corpus = bk / corpus_name
    stem = corpus_name.replace(".jsonl", "")
    suite_p = bk / (corpus_name + ".validator_report.json")
    csha = sha(corpus)
    tools = [K["sweep_tool"]] + ([K["dispose_tool"]] if K.get("dispose_tool") else [])
    sweep_p, disp_p = tmp / "cwo_sweep.json", tmp / "cwo03_dispositions.json"
    cmds = [[bk / K["sweep_tool"], corpus_name, "--out", sweep_p]]
    if K.get("dispose_tool"):
        cmds.append([bk / K["dispose_tool"], sweep_p, disp_p])
    for cmd in cmds:
        r = subprocess.run([sys.executable, "-B"] + [str(c) for c in cmd], capture_output=True, cwd=str(bk))
        if r.returncode != 0:
            raise SystemExit("REFUSED: %s exit %d: %s" % (Path(cmd[0]).name, r.returncode, r.stderr.decode("utf-8", "replace")[-400:]))
    sweep_b = lf(sweep_p)
    sweep = json.loads(sweep_b.decode("utf-8"))
    side = {"cwo_sweep.json": sweep_b}
    if CR in suite_p.read_bytes() or CR in corpus.read_bytes():  # E-73: a digest is recorded on LF bytes only
        raise SystemExit("REFUSED: CR byte in the corpus or its validator report; convert to LF before recording a digest")
    suite = json.loads(suite_p.read_bytes().decode("utf-8"))
    rows = [json.loads(x) for x in corpus.read_bytes().decode("utf-8").splitlines() if x.strip()]
    wide_re, wide = re.compile(K["wide_id"]), []
    for r in rows:
        for f in K["fields"]:
            for s in strs(r.get(f)):
                for m in wide_re.finditer(s):
                    wide.append({"row": r["writer_decision_id"], "field": f, "match": m.group(0)})
    hand, hand_ref, rulings_ok = None, K.get("hand_record"), K["rulings"] != PENDING
    if K["adapter"] == "orders":
        disp_b = lf(disp_p)
        side["cwo03_dispositions.json"] = disp_b
        parity, residual = orders_arm(K, sweep, json.loads(disp_b.decode("utf-8")))
        same_rows = sweep["rows"] == len(rows) == C["ROWS"] and sweep["rows_sha256"] == csha
    else:
        if isinstance(hand_ref, dict):
            b = (bk / hand_ref["path"]).read_bytes()
            if shab(b) != hand_ref.get("sha256"):
                raise SystemExit("REFUSED: the hand record is not its pinned bytes")
            hand = json.loads(b.decode("utf-8"))
            if hand.get("book") != a.book:
                raise SystemExit("REFUSED: the hand record names another book (E-65)")
        parity, residual = counters_arm(K, sweep, hand, csha)
        same_rows = sweep["rows_scanned"] == len(rows) == C["ROWS"]
    second, second_ok = {}, True
    for label, member, order, zero in K["witnesses"]:
        m = suite.get(member, {})
        second[label] = {"status": m.get("status"), "flag_count": m.get("flag_count"), "order": order}
        second_ok = second_ok and m.get("status") == "GREEN" and not (zero and m.get("flag_count"))
    summary = suite.get("summary") or {}
    ok = (not residual and same_rows and second_ok and rulings_ok and suite.get("rows_file") == corpus_name
          and summary.get("hard_status") == "GREEN")
    rec = {
        "schema": K["schema"], "book": a.book, "post_corpus": corpus_name, "post_corpus_sha256": csha, "rows": len(rows),
        "suite_report": {"path": suite_p.name, "sha256": sha(suite_p), "hard_status": summary.get("hard_status"),
                         "binding": "the report names the rows file, not its digest; it was written by the suite run over this corpus "
                                    "and is re-read here (REPORTED by the suite, digest MEASURED here)"},
        "parity": parity, "second_witnesses": second, "exact_arm_residual": residual, "routed_open": [],
        "supplementary_widened_id_arm": {"pattern": wide_re.pattern, "fields": list(K["fields"]), "hit_count": len(wide), "hits": wide,
                                         "note": K["wide_note"]},
        "status": "GREEN" if ok and not wide else ("FINDING" if ok else "RED"),
        "tools": {Path(t).name: sha(bk / t) for t in tools},
        "rulings": {Path(p).name: sha(bk / p) for p in K["rulings"]} if rulings_ok else "UNAVAILABLE: no ruling file is named in the parameters",
        "side_records": {n: shab(b) for n, b in side.items()},
        "coverage_dir": "cwo/coverage_%s/" % stem,
        "law": "E-18: every corpus-wide order checked again as its own sweep over the corpus being closed",
        "limits": K["limits"],
    }
    if K["adapter"] == "counters":
        rec["hand_record"] = hand_ref if isinstance(hand_ref, dict) else "UNAVAILABLE: no hand record is named in the parameters"
    return rec, side


def install(p, b):
    if CR in b:
        raise SystemExit("REFUSED: CR byte in %s" % p.name)
    if p.exists():
        if p.read_bytes() != b:
            raise SystemExit("REFUSED: %s exists with different bytes" % p)
        return "kept"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b)
    return "written"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--m8-root")
    ap.add_argument("--params")
    a = ap.parse_args()
    bk, C = load(a)
    stem = C["CORPUS"].replace(".jsonl", "")
    cwo = bk / "cwo"
    cov, rec_p = cwo / ("coverage_" + stem), cwo / ("cwo_parity.%s.json" % stem)
    with tempfile.TemporaryDirectory() as t:
        rec, side = compute(Path(t), a, bk, C)
    b = dump(rec)
    if a.check:
        same = rec_p.exists() and rec_p.read_bytes() == b and all((cov / n).exists() and (cov / n).read_bytes() == sb for n, sb in side.items())
        print(json.dumps({"check": "MATCH" if same else "DIFFERS", "status": rec["status"], "record_sha256": shab(b)}))
        return 0 if same and rec["status"] == "GREEN" else 1
    acts = {n: install(cov / n, sb) for n, sb in side.items()}
    acts[rec_p.name] = install(rec_p, b)
    print(json.dumps({"status": rec["status"], "post_corpus_sha256": rec["post_corpus_sha256"],
                      "residual": len(rec["exact_arm_residual"]), "widened_id_hits": rec["supplementary_widened_id_arm"]["hit_count"],
                      "installed": acts, "record_sha256": shab(b)}, ensure_ascii=False))
    return 0 if rec["status"] == "GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
