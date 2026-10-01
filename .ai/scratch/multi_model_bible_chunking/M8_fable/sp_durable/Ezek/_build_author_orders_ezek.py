#!/usr/bin/env python3
"""Author-wave work orders for Ezekiel, one file per part (ruling R2 of ezek_controlling_agent_rulings.v1.json).

R2 routes these to fresh per-part author executions:
  - the boundary amendments and row-content orders (every ruling order addressed to author_wave);
  - the residuals the deterministic sweeps could not do, as routed in their manifests (CWO-EZ-01, -02, -04, -05);
  - the tags vocabulary (CWO-EZ-06), boilerplate variation (CWO-EZ-07) and register rewrites (CWO-EZ-08);
  - every HARD finding the Tier-0 suite still reports on a row.

This builder is deterministic. It embeds per row, VERBATIM, every item that binds the row, and judges nothing. It never
edits a row. E-18: every corpus-wide item carries its CWO id and narrowed predicate, and after the wave a per-CWO
coverage sweep re-evaluates each predicate over the applied rows. The label travels with the item.

Ops for the boundary amendments, derived from the ruled exact_spans against the current rows:
  - every ruled span already present -> "replace" (content only);
  - otherwise the k ruled spans take the m overlapped rows' decision_ids in span order: "replace" for the first
    min(k, m), "new_row" for any extra span (provisional id <row>.<n>), "retire" for any extra row;
  - an order whose text says no span changes -> "hold" (no output row expected).
CWO-EZ-03 is not here: its scan disagreements go to the controlling agent first, and any cut it orders is passed with
--extra-orders.

Usage: _build_author_orders_ezek.py --rows repair/rows_v2_swept_r3.jsonl --report <suite report over those exact bytes>
       --out author [--extra-orders <json list of {ruling_id, order, exact_spans, ...}>]
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import HEB_RUN, LAST_VERSE  # noqa: E402

RULINGS = EZ / "ezek_controlling_agent_rulings.v1.json"
ORIGINAL_ROWS = EZ / "writer" / "draft_rows_combined.jsonl"
ROUTED = [  # (cwo, manifest, key)
    ("CWO-EZ-01", "repair/rows_s1_cwo01.manifest.json", "routed_to_author_wave_unprefixed_string_entries"),
    ("CWO-EZ-02", "repair/rows_s3_cwo02_r2.manifest.json", "routed_to_author_wave_unbound_hebrew"),
    ("CWO-EZ-04", "repair/rows_s2_cwo04_r2.manifest.json", "routed_to_author_wave_hebrew_defects"),
    ("CWO-EZ-05", "repair/rows_s4_cwo05_r2.manifest.json", "routed_to_author_wave_mark_claims_contradicting_inventory"),
]
NO_SPAN_CHANGE = re.compile(r"\bno change to\b[^.]*\bspans?\b", re.I)
STRONGS = re.compile(r"\b[HG]\d{2,5}\b")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verses(span):
    c1, v1, c2, v2 = map(int, re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$", span).groups())
    out, c, v = [], c1, v1
    while (c, v) <= (c2, v2):
        out.append((c, v))
        c, v = (c, v + 1) if v < LAST_VERSE[c] else (c + 1, 1)
    return out


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--extra-orders")
    a = ap.parse_args()
    rows_p = EZ / a.rows
    rep_p = Path(a.report) if Path(a.report).is_absolute() else EZ / a.report
    out_dir = Path(a.out) if Path(a.out).is_absolute() else EZ / a.out
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    rep_rows_file = Path(rep["rows_file"])
    if not rep_rows_file.is_file() or sha(rep_rows_file) != sha(rows_p):
        raise SystemExit("ABORT: the report was not produced over the exact bytes of %s" % a.rows)
    if rep["citation_sweep"].get("rows") not in (None, len(rows)):
        raise SystemExit("ABORT: report row count differs from the rows file")
    rul = json.loads(RULINGS.read_text(encoding="utf-8"))
    by_id = {r["decision_id"]: r for r in rows}
    by_wid = {r["writer_decision_id"]: r["decision_id"] for r in rows}
    vset = {r["decision_id"]: set(verses(r["span"])) for r in rows}
    order_of = {r["decision_id"]: i for i, r in enumerate(rows)}
    items = {r["decision_id"]: [] for r in rows}
    new_rows, retire, holds, problems = [], [], [], []

    def add(did, item):
        if did not in items:
            problems.append("item for unknown row %r: %s" % (did, json.dumps(item, ensure_ascii=False)[:160]))
            return
        items[did].append(item)

    # ---- 1. ruling orders to the author wave (boundary amendments and content orders) ----
    orders = []
    for r in rul["rulings"]:
        n = 0
        for o in r.get("orders", []):
            if o.get("to") == "author_wave":
                n += 1
                orders.append({"ref": "%s#%d" % (r["id"], n), "ruling_id": r["id"], "ruling": r["ruling"],
                               "decision": r["decision"], "reason": r["reason"], "evidence": r.get("evidence", []),
                               "order": o["order"], "exact_spans": o.get("exact_spans", [])})
    if a.extra_orders:
        extra = json.loads(Path(a.extra_orders).read_text(encoding="utf-8"))
        for i, o in enumerate(extra, 1):
            o.setdefault("ref", "%s#x%d" % (o["ruling_id"], i))
        orders += extra
    orders_by_ref = {o["ref"]: o for o in orders}
    for o in orders:
        spans = o["exact_spans"]
        want = set().union(*[set(verses(s)) for s in spans]) if spans else set()
        hit = sorted((d for d in vset if vset[d] & want), key=order_of.get)
        present = {r["span"] for r in rows}
        verbatim = {"kind": "ruling_order", "ref": o["ref"]}   # the order itself is embedded once, under ruling_orders
        if not hit:
            problems.append("ruling %s names spans no current row overlaps: %s" % (o["ruling_id"], spans))
            continue
        if NO_SPAN_CHANGE.search(o["order"]):
            for d in hit:
                holds.append({"decision_id": d, "ruling_id": o["ruling_id"]})
                add(d, dict(verbatim, op="hold"))
            continue
        if all(s in present for s in spans) and len(hit) == len(spans):
            for d in hit:
                add(d, dict(verbatim, op="replace", target_span=by_id[d]["span"]))
            continue
        # a re-span: ruled spans take the overlapped rows' ids in span order
        covered = set().union(*[vset[d] for d in hit])
        if covered != want:
            problems.append("ruling %s: the overlapped rows cover %d verses, the ruled spans %d - not a clean re-span"
                            % (o["ruling_id"], len(covered), len(want)))
        for i, s in enumerate(spans):
            if i < len(hit):
                add(hit[i], dict(verbatim, op="replace", target_span=s))
            else:
                base = hit[-1]
                nid = "%s.%d" % (base, i - len(hit) + 1)
                new_rows.append({"provisional_decision_id": nid, "provisional_writer_decision_id":
                                 "%s.%d" % (by_id[base]["writer_decision_id"], i - len(hit) + 1),
                                 "target_span": s, "part": by_id[base]["writer_part"], "from_row": base})
                add(base, dict(verbatim, op="new_row", target_span=s, provisional_decision_id=nid))
        for d in hit[len(spans):]:
            retire.append({"decision_id": d, "writer_decision_id": by_id[d]["writer_decision_id"], "ruling_id": o["ruling_id"]})
            add(d, dict(verbatim, op="retire"))

    # ---- 2. residuals routed by the deterministic sweeps ----
    cwo_text = {c["id"]: c for c in rul["corpus_wide_orders"]}
    for cwo, man, key in ROUTED:
        m = json.loads((EZ / man).read_text(encoding="utf-8"))
        for it in m.get(key) or []:
            did = it.get("row") or it.get("decision_id") if isinstance(it, dict) else None
            label = {"kind": "routed_residual", "cwo": cwo, "routed_by": "%s %s" % (man, key), "verbatim": it}
            if did is None:
                hits = [r["decision_id"] for r in rows if any(str(it) in s for s in strings(r))]
                if not hits:
                    problems.append("%s routed item bound to no row: %r" % (cwo, it))
                for d in hits:
                    add(d, label)
            else:
                add(did, label)

    # ---- 3. CWO-EZ-06 tags vocabulary (ruling P5), evaluated here on the current rows ----
    for r in rows:
        for i, e in enumerate(r.get("strong_or_hebrew_tags_used") or []):
            heb = HEB_RUN.findall(e) if isinstance(e, str) else []
            words = sum(len(h.split()) for h in heb)
            why = [w for w, bad in (("no Hebrew", not heb), ("more than 5 Hebrew words", words > 5),
                                    ("no oshb: ref in the entry", "oshb:Ezek." not in str(e)),
                                    ("a Strong's number", bool(STRONGS.search(str(e))))) if bad]
            if why:
                add(r["decision_id"], {"kind": "cwo_item", "cwo": "CWO-EZ-06", "field": "strong_or_hebrew_tags_used[%d]" % i,
                                       "entry": e, "why": why})

    # ---- 4. CWO-EZ-07 boilerplate and CWO-EZ-08 register, from the suite report ----
    for g in rep["ngram7"].get("offending_7grams", []):
        for d in g["row_ids"]:
            add(d, {"kind": "cwo_item", "cwo": "CWO-EZ-07", "gram": g["gram"], "rows_sharing_it": g["rows"],
                    "row_ids": g["row_ids"]})
    for f in rep["register"].get("flags", []):
        d = by_wid.get(f["decision_id"], f["decision_id"])
        add(d, {"kind": "cwo_item", "cwo": "CWO-EZ-08", "field": f["field"], "class": f["class"], "match": f["match"],
                "context": f["context"]})

    # ---- 5. every remaining HARD finding on a row ----
    cs = rep["citation_sweep"]
    for p in cs["problems"] + cs.get("nfd_degraded", []) + cs.get("prose_pair_problems", []):
        d = p.split(":", 1)[0]
        add(d, {"kind": "hard_finding", "member": "citation_sweep", "finding": p})
    for run in rep["hebrew_normalize_dryrun"].get("defects", []):
        hits = [r["decision_id"] for r in rows if any(run in s for s in strings(r))]
        if not hits:
            problems.append("normalizer defect bound to no row: %r" % run)
        for d in hits:
            add(d, {"kind": "hard_finding", "member": "normalizer (E-01)", "finding": "Hebrew run in neither the verse bytes "
                    "nor the K/Q note layer: %s" % run})
    for f in rep["cap_sweep"].get("failures", []):
        d = by_wid.get(f.split(" ", 1)[0])
        add(d, {"kind": "hard_finding", "member": "cap_sweep (E-02)", "finding": f})

    # ---- write one file per part ----
    out_dir.mkdir(parents=True, exist_ok=True)
    src = {"rulings": {"path": "Ezek/" + RULINGS.name, "sha256": sha(RULINGS)},
           "rows": {"path": "Ezek/" + a.rows, "sha256": sha(rows_p)},
           "suite_report": {"path": str(rep_p), "sha256": sha(rep_p), "rows_file_sha256": sha(rep_rows_file)},
           "original_rows": {"path": "Ezek/writer/draft_rows_combined.jsonl", "sha256": sha(ORIGINAL_ROWS)},
           "routed_manifests": {man: sha(EZ / man) for _, man, _ in ROUTED}}
    parts = []
    for r in rows:
        if r["writer_part"] not in parts:
            parts.append(r["writer_part"])
    index = {"schema": "m8_author_orders_index.v1", "book": "Ezek", "ordered_by": "ezek_controlling_rulings_a1#e2 ruling R2",
             "sources": src, "parts": {}, "problems": problems}
    for part in parts:
        prow = [r for r in rows if r["writer_part"] == part]
        entries = []
        for i, r in enumerate(prow):
            if not items[r["decision_id"]]:
                continue
            entries.append({"decision_id": r["decision_id"], "writer_decision_id": r["writer_decision_id"], "span": r["span"],
                            "ops": sorted({it.get("op", "replace") for it in items[r["decision_id"]]}),
                            "previous_row": {k: prow[i - 1][k] for k in ("decision_id", "span")} if i else None,
                            "next_row": {k: prow[i + 1][k] for k in ("decision_id", "span")} if i + 1 < len(prow) else None,
                            "items": items[r["decision_id"]], "current_row": r})
        aid = "ezek_author_%s_a1" % part
        used_refs = sorted({it["ref"] for e in entries for it in e["items"] if it.get("ref")})
        used_cwos = sorted({it["cwo"] for e in entries for it in e["items"] if it.get("cwo")})
        doc = {"schema": "m8_author_orders.v1", "book": "Ezek", "part": part, "attempt_id": aid, "execution_id": aid + "#e1",
               "ordered_by": "ezek_controlling_rulings_a1#e2 ruling R2", "sources": src,
               "ruling_orders": {k: orders_by_ref[k] for k in used_refs},
               "corpus_wide_orders": {k: {"order": cwo_text[k]["order"], "predicate": cwo_text[k]["predicate"],
                                          "why": cwo_text[k].get("why")} for k in used_cwos},
               "part_rows": [{"decision_id": r["decision_id"], "span": r["span"]} for r in prow],
               "rows_with_orders": entries,
               "new_rows": [n for n in new_rows if n["part"] == part],
               "retire": [x for x in retire if by_id[x["decision_id"]]["writer_part"] == part],
               "holds": [h for h in holds if by_id[h["decision_id"]]["writer_part"] == part]}
        counts = {}
        for e in entries:
            for it in e["items"]:
                k = it.get("cwo") or it["kind"]
                counts[k] = counts.get(k, 0) + 1
        doc["item_counts"] = counts
        p = out_dir / ("orders_%s.json" % aid)
        body = json.dumps(doc, ensure_ascii=False, indent=1)
        if p.exists() and p.read_text(encoding="utf-8") != body:
            raise SystemExit("ABORT: %s exists with different content; orders are never silently replaced" % p.name)
        p.write_text(body, encoding="utf-8", newline="\n")
        index["parts"][part] = {"file": p.name, "sha256": sha(p), "rows_in_part": len(prow), "rows_with_orders": len(entries),
                                "new_rows": len(doc["new_rows"]), "retire": len(doc["retire"]), "holds": len(doc["holds"]),
                                "item_counts": counts}
    ip = out_dir / "orders_index.json"
    body = json.dumps(index, ensure_ascii=False, indent=1)
    if ip.exists() and ip.read_text(encoding="utf-8") != body:
        raise SystemExit("ABORT: orders_index.json exists with different content")
    ip.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"parts": {k: {x: v[x] for x in ("rows_in_part", "rows_with_orders", "new_rows", "retire", "holds", "item_counts")}
                                for k, v in index["parts"].items()}, "problems": problems}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
