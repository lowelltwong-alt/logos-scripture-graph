#!/usr/bin/env python3
"""Apply the landed author-wave deliverables to the swept chain head, producing ONE new rows file. Nothing is overwritten.

Inputs: the chain head the orders were built on, and one landed deliverable per part. Each deliverable must have a LANDED
receipt whose output digest equals the file. A deliverable whose receipt names form defects is refused; that part gets a
new execution instead.

Steps:
  - replace rows by decision_id (the _op key dropped), drop retired rows, add new rows;
  - give each new row a final id: the next unused number in its part. An id that ever existed in the part is never
    reused, retired ids included. The matching writer_decision_id goes with it;
  - order all rows by span and assert that the whole book tiles exactly (every WEB verse once, 1:1 through 48:35), and
    that each part's rows stay inside that part's original verses;
  - renumber chunk_index_in_book 1..N in span order.
Authored rows are written in the 22-field order; rows no author touched keep their bytes. The manifest records every
input digest and receipt, the provisional -> final id map, the retired ids, the chunk-index map and the tiling assertion.

FIXUP-1 mode (--fixup; ezek_controlling_rulings_a1#e4 ruling FIXUP-1): the receipts are fixup1/ezek_author_fixup_attempt_receipts.jsonl;
any op but replace is refused, as is any change to span, unit_type, confidence, parent_collection, writer_decision_id,
writer_attempt_id or chunk_index_in_book, and any chunk-index renumbering; the manifest is m8_fixup_apply.v1.

Usage: _apply_author_wave_ezek.py --rows repair/rows_v2_swept_r3.jsonl --out repair/rows_v2_authored.jsonl [--fixup]
       --landed author/ezek_author_p01_a1.jsonl [author/... ...]
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
RECEIPTS = EZ / "author" / "ezek_author_attempt_receipts.jsonl"
FIXUP1_RECEIPTS = "fixup1/ezek_author_fixup_attempt_receipts.jsonl"
FIXUP1_ORDERED_BY = "ezek_controlling_rulings_a1#e4 ruling FIXUP-1"
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import LAST_VERSE  # noqa: E402

FIELDS = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "boundary_rationale", "boundary_evidence_refs",
          "strongest_rejected_alternative", "literature_type_guess", "confidence", "strong_or_hebrew_tags_used",
          "wj_or_red_letter_considered", "frontier_flag_considered", "non_authorizing", "review_status", "parent_collection",
          "unit_type", "writer_part", "writer_decision_id", "writer_attempt_id", "observed_substrate_signals", "device_notes"]
SPAN = re.compile(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verses(span):
    c1, v1, c2, v2 = map(int, SPAN.match(span).groups())
    out, c, v = [], c1, v1
    while (c, v) <= (c2, v2):
        out.append((c, v))
        c, v = (c, v + 1) if v < LAST_VERSE[c] else (c + 1, 1)
    return out


def abort(msg):
    raise SystemExit("ABORT: " + msg + " - nothing written")


def fixup_receipts_path(arg):
    """The fix-up receipts path under SP/Ezek: --receipts when given, else the FIXUP-1 path (#e9 ruling S2-ROUTING (5))."""
    return EZ / (arg if arg else FIXUP1_RECEIPTS)


def fixup_ordered_by(orders_list):
    """The apply manifest's ordered_by in fix-up mode: the landed orders files' own field, one value across all parts; FIXUP-1's
    literal when the field is absent (#e9 ruling S2-ROUTING (5))."""
    vals = {o.get("ordered_by") or FIXUP1_ORDERED_BY for o in orders_list}
    if len(vals) != 1:
        abort("the landed orders name %d different ordering rulings" % len(vals))
    return vals.pop()


def no_op_ids(chain, replaced):
    """Replaced rows whose serialized bytes equal the chain row's (S2-16: a no-op replace is recorded as such)."""
    cur = {r["decision_id"]: r for r in chain}
    return sorted(d for d, row in replaced.items() if json.dumps(row, ensure_ascii=False) == json.dumps(cur[d], ensure_ascii=False))


def selftest():
    s2r = "ezek_controlling_rulings_a1#e9 ruling S2-ROUTING"
    results = []

    def check(name, got, want):
        results.append({"vector": name, "want": str(want), "got": str(got), "ok": got == want})

    check("--receipts absent keeps the fixup1 receipts path", fixup_receipts_path(None), EZ / "fixup1" / "ezek_author_fixup_attempt_receipts.jsonl")
    check("--receipts names the FIXUP-2 receipts path", fixup_receipts_path("fixup2/ezek_author_fixup_attempt_receipts.jsonl"),
          EZ / "fixup2" / "ezek_author_fixup_attempt_receipts.jsonl")
    check("FIXUP-1 orders keep the FIXUP-1 ordered_by", fixup_ordered_by([{"ordered_by": FIXUP1_ORDERED_BY}, {}]), FIXUP1_ORDERED_BY)
    check("FIXUP-2 orders resolve #e9's ruling", fixup_ordered_by([{"ordered_by": s2r}, {"ordered_by": s2r}]), s2r)
    try:
        fixup_ordered_by([{"ordered_by": s2r}, {"ordered_by": FIXUP1_ORDERED_BY}])
        got = "accepted"
    except SystemExit:
        got = "refused"
    check("orders naming two ordering rulings are refused", got, "refused")
    row = {k: (1 if k == "chunk_index_in_book" else "x") for k in FIELDS}
    check("a byte-identical replace is a no-op", no_op_ids([dict(row, decision_id="P01-001")], {"P01-001": dict(row, decision_id="P01-001")}), ["P01-001"])
    check("a changed replace is not a no-op",
          no_op_ids([dict(row, decision_id="P01-001")], {"P01-001": dict(row, decision_id="P01-001", device_notes="y")}), [])
    failed = [r for r in results if not r["ok"]]
    print(json.dumps({"selftest": "_apply_author_wave_ezek fix-up plumbing", "vectors": len(results), "failed": failed,
                      "verdict": "GREEN" if not failed else "RED"}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--landed", nargs="+", required=True)
    ap.add_argument("--fixup", action="store_true", help="FIXUP-1 mode (#e4 ruling FIXUP-1 (3), (5))")
    ap.add_argument("--receipts", default=None, help="fix-up receipts path under SP/Ezek; the fixup1 path when omitted (#e9 ruling S2-ROUTING (5))")
    a = ap.parse_args()
    receipts_p = fixup_receipts_path(a.receipts) if a.fixup else RECEIPTS
    rows_p, out_p = EZ / a.rows, EZ / a.out
    chain = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    receipts = [json.loads(l) for l in receipts_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    replaced, retired, new, inputs, parts_done = {}, set(), [], [], set()
    orders_seen = []
    for lp in a.landed:
        p = EZ / lp
        rel = "Ezek/" + lp.replace("\\", "/")
        recs = [r for r in receipts if r.get("output_file") == rel and r.get("output_sha256") == sha(p)]
        if not recs:
            abort("%s has no receipt matching its bytes" % lp)
        rec = recs[-1]
        if rec["outcome"] != "LANDED":
            abort("%s landed as %s; a defective deliverable is never applied" % (lp, rec["outcome"]))
        orders = json.loads((SP / rec["orders"]["path"]).read_text(encoding="utf-8"))
        if sha(SP / rec["orders"]["path"]) != rec["orders"]["sha256"]:
            abort("the orders behind %s changed after landing" % lp)
        if orders["sources"]["rows"]["sha256"] != sha(rows_p):
            abort("%s was ordered on another chain head" % lp)
        if orders["part"] in parts_done:
            abort("two deliverables for %s" % orders["part"])
        parts_done.add(orders["part"])
        orders_seen.append(orders)
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            op = obj.pop("_op")
            did = obj["decision_id"]
            if a.fixup and op != "replace":
                abort("%s: %s of %s; FIXUP-1 (3) allows replace only" % (lp, op, did))
            if op == "retire":
                retired.add(did)
            elif op == "replace":
                if did in replaced:
                    abort("%s replaced twice" % did)
                replaced[did] = {k: obj[k] for k in FIELDS}
            else:
                new.append({k: obj[k] for k in FIELDS})
        inputs.append({"file": rel, "sha256": sha(p), "execution_id": rec["execution_id"], "orders": rec["orders"]})

    known = {r["decision_id"] for r in chain}
    for d in list(replaced) + sorted(retired):
        if d not in known:
            abort("%s is not in the chain head" % d)
    if a.fixup:
        cur = {r["decision_id"]: r for r in chain}
        for d, row in replaced.items():
            for f in ("span", "unit_type", "confidence", "parent_collection", "writer_decision_id", "writer_attempt_id", "chunk_index_in_book"):
                if row[f] != cur[d][f]:
                    abort("%s: %s changed (%r -> %r); FIXUP-1 (3) allows no span, unit_type, confidence or parent change"
                          % (d, f, cur[d][f], row[f]))
    result = [replaced.get(r["decision_id"], r) for r in chain if r["decision_id"] not in retired]
    ever = {}
    for r in chain:
        ever.setdefault(r["writer_part"], set()).add(int(r["decision_id"].split("-")[1]))
    id_map = {}
    for n in sorted(new, key=lambda o: verses(o["span"])[0]):
        part = n["writer_part"]
        k = max(ever[part]) + 1
        ever[part].add(k)
        final, wfinal = "P%s-%03d" % (part[1:], k), "%s-%d" % (part, k)
        id_map[n["decision_id"]] = {"decision_id": final, "writer_decision_id": wfinal, "span": n["span"]}
        n["decision_id"], n["writer_decision_id"] = final, wfinal
        result.append(n)
    result.sort(key=lambda r: verses(r["span"])[0])

    book = [(c, v) for c in sorted(LAST_VERSE) for v in range(1, LAST_VERSE[c] + 1)]
    got = [v for r in result for v in verses(r["span"])]
    if got != book:
        first = next((i for i, (x, y) in enumerate(zip(got, book)) if x != y), min(len(got), len(book)))
        abort("the book does not tile: %d verses vs %d; first mismatch at position %d (%s vs %s)"
              % (len(got), len(book), first, got[first] if first < len(got) else None, book[first] if first < len(book) else None))
    part_verses = {}
    for r in chain:
        part_verses.setdefault(r["writer_part"], set()).update(verses(r["span"]))
    for r in result:
        if not set(verses(r["span"])) <= part_verses[r["writer_part"]]:
            abort("%s (%s) leaves its part's verses" % (r["decision_id"], r["span"]))
    ci_map = {}
    for i, r in enumerate(result, 1):
        if r["chunk_index_in_book"] != i:
            ci_map[r["decision_id"]] = [r["chunk_index_in_book"], i]
            r = r  # the dict is shared with `result`; renumber in place
        r["chunk_index_in_book"] = i

    if a.fixup and ci_map:
        abort("FIXUP-1 renumbered chunk_index_in_book for %d rows; no row order may change" % len(ci_map))
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in result)
    if out_p.exists() and out_p.read_text(encoding="utf-8") != body:
        abort("%s exists with different content" % a.out)
    out_p.write_text(body, encoding="utf-8", newline="\n")
    manifest = {"schema": "m8_fixup_apply.v1" if a.fixup else "m8_author_wave_apply.v1", "book": "Ezek",
                "ordered_by": fixup_ordered_by(orders_seen) if a.fixup else "ezek_controlling_rulings_a1#e2 ruling R2",
                "input_rows": {"path": "Ezek/" + a.rows, "sha256": sha(rows_p), "rows": len(chain)},
                "landed": inputs, "parts_applied": sorted(parts_done),
                "parts_not_applied": sorted({r["writer_part"] for r in chain} - parts_done),
                "replaced": sorted(replaced), "retired": sorted(retired), "new_row_ids": id_map,
                "chunk_index_renumbered": ci_map,
                "tiling": {"verses": len(got), "expected": len(book), "assert": "every WEB verse exactly once, span order"},
                "output": {"path": "Ezek/" + a.out, "sha256": sha(out_p), "rows": len(result)}}
    if a.fixup and a.receipts:
        nops = no_op_ids(chain, replaced)
        manifest["no_op_replaced"] = nops
        manifest["replaced_statement"] = "replaced %d, of which %d no-op%s" % (len(replaced), len(nops), (" (%s)" % ", ".join(nops)) if nops else "")
        manifest["receipts"] = {"path": "Ezek/" + a.receipts.replace("\\", "/"), "sha256": sha(receipts_p)}
        manifest["tools"] = {n: sha(EZ / n) for n in ("_apply_author_wave_ezek.py", "_land_author_part_ezek.py")}
    mp = out_p.with_suffix(".manifest.json")
    mbody = json.dumps(manifest, ensure_ascii=False, indent=1)
    if mp.exists() and mp.read_text(encoding="utf-8") != mbody:
        abort("%s exists with different content" % mp.name)
    mp.write_text(mbody, encoding="utf-8", newline="\n")
    print(json.dumps({k: manifest[k] for k in ("parts_applied", "parts_not_applied", "new_row_ids", "tiling", "output")}
                     | {"replaced": len(replaced), "retired": len(retired)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    raise SystemExit(main())
