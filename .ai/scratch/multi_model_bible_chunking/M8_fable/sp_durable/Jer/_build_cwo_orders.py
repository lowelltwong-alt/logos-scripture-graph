#!/usr/bin/env python3
"""Build the Jeremiah CWO-wave orders (E-18: every corpus-wide order executes as its OWN sweep)
from the deterministic scan over the post-apply corpus (rows_v2.jsonl) + the remedy docket's
verbatim order texts + the boss rulings. One order per row carrying every CWO item that hits it;
slices <=8 rows; authors are sonnet; verification = re-running _cwo_scan.py over the revised corpus
(every exact arm must return 0 candidates; heuristic arms are re-triaged with the authors'
dispositions) + the fresh full sweep. Writes cwo/orders_cwo_NN.json + cwo_orders.v1.json (the
executed/ordered parity record the close gate requires).
Usage: _build_cwo_orders.py rows_v2.jsonl scan.json"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CWO_TEXT = {}
d = json.load(open(HERE / "remedy_docket.v1.json", encoding="utf-8"))
for c in d["corpus_wide_orders"]:
    CWO_TEXT[c["id"]] = {"summary": c.get("orchestrator_summary") or c.get("order"), "verbatim": c.get("order_full_remedy_verbatim") or c.get("order"),
                         "source_row": c.get("source_row"), "peer_file": c.get("peer_file")}
CWO_TEXT["CWO-9"] = {"summary": "bare in-zone chapter.verse coordinates in row prose take an explicit dual or numeric qualifier (boss B1-6 corpus-scoped order)",
                     "verbatim": "CORPUS-SCOPED ORDER (boss B1-6): every bare in-zone chapter.verse coordinate in row prose (web ch 9 / oshb:Jer.8.23 / oshb ch 9) takes an explicit dual or numeric qualifier; the class recurs at P03-010, P03-011 and P03-013; it remains its OWN sweep over every row touching the zone.",
                     "source_row": "P03-007", "peer_file": "reviews/boss_jer_b1.json"}
CWO_TEXT["CWO-5"]["policy"] = ("BOSS B4-6 RULED (option i, bind-or-drop): a closure-classed observed_substrate_signals key is valid ONLY where the device it names stands in the "
                               "DECLARING UNIT'S OWN CLOSING VERSE; where dropped, the device is disclosed in prose with its verse ref and tier - never re-encoded under another key.")


def main():
    rows_path, scan_path = Path(sys.argv[1]), Path(sys.argv[2])
    rows = {r["writer_decision_id"]: r for r in (json.loads(l) for l in rows_path.read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    scan = json.load(open(scan_path, encoding="utf-8"))["orders"]
    per_row = defaultdict(list)
    # CWO-1: rows carrying offending grams
    ng = scan["CWO-1"]["result"]
    grams = ng.get("offending_7grams") or []
    for g in grams:
        gram = g.get("gram") or g.get("ngram") or g
        for rid in (g.get("row_ids") or []):   # 2026-09-06: "rows" is the COUNT; row_ids carries the ids (scan runs ngram7 --full-ids)
            per_row[rid].append({"cwo": "CWO-1", "arm": "exact", "evidence": {"gram": gram, "rows_sharing": g.get("rows") or len(g.get("row_ids") or [])},
                                 "instruction": "Re-formulate the mandated disclosure sentence(s) carrying this 7-gram in a distinct shape that shares no 7-gram with the listed gram; keep every fact, ref, tier and digit; the class is verified by ngram7 --gate 10 over the revised corpus."})
    for c in scan["CWO-2"]["candidates"]:
        per_row[c["row"]].append({"cwo": "CWO-2", "arm": "exact", "evidence": c, "instruction": "Separate the two armies-title objects: the key names the title the bytes carry in the span (the full Elohei-Yisrael stack where present); disclose per site with tier + digit."})
    for rid in scan["CWO-3"]["candidates"]:
        per_row[rid].append({"cwo": "CWO-3", "arm": "exact", "evidence": {"key": "word_event.discourse_imperative_onset"}, "instruction": "Re-file the discourse-imperative class out of the word_event key family into the key family the corpus uses for that class; keep the prose warrant; no respan."})
    for c in scan["CWO-4"]["candidates"]:
        per_row[c["row"]].append({"cwo": "CWO-4", "arm": "heuristic", "evidence": c, "instruction": "Re-read the form at each delivery-construction site in your span off the pointed bytes (waw-prefixed 2ms suffix conjugation, NOT an imperative; the imperative at 13:18 is the contrasting control); correct every label/key/claim that calls it an imperative or discourse-frame imperative or rests a seam on its exclusivity (sweep: 18 verses, sites named); if no such label exists in the row, report the row as clean for this order."})
    for c in scan["CWO-5"]["candidates"]:
        per_row[c["row"]].append({"cwo": "CWO-5", "arm": "exact", "evidence": c, "instruction": "DROP the closure-classed key whose device is absent from the closing verse; add one sentence to boundary_rationale stating that the closing verse carries no closure formula and naming what closes the unit; disclose in-span token positions in prose with MT ref + byte tier; never re-encode under another key."})
    for c in scan["CWO-6"]["candidates"]:
        per_row[c["row"]].append({"cwo": "CWO-6", "arm": "heuristic", "evidence": c, "instruction": "Strip or re-site the byte-tier label attached to a bare coordinate so a tier label always names a quoted run."})
    for c in scan["CWO-7"]["candidates"]:
        per_row[c["row"]].append({"cwo": "CWO-7", "arm": "heuristic", "evidence": c, "instruction": "Correct the date label on the OAN header unit: check the header verse's bytes for a year/reign/month token and the classified date-site census; a header identifying its target by a strike already inflicted carries no date element (49:34's accession clause is the one byte-present exception); if the row's date language is byte-true, report it clean."})
    for c in scan["CWO-8"]["candidates"] + [{"row": "P19-008"}, {"row": "P19-009"}]:
        per_row[c["row"]].append({"cwo": "CWO-8", "arm": "heuristic+named", "evidence": c, "instruction": "No mark-absence stands as evidence in strongest_rejected_alternative: re-ground the rival on a text signal; parashah paragraphing, if named, is tier-3 single-witness corroboration only."})
    for c in scan["CWO-9"]["candidates"]:
        per_row[c["row"]].append({"cwo": "CWO-9", "arm": "exact", "evidence": c, "instruction": "Give every bare in-zone chapter.verse coordinate an explicit dual or numeric qualifier (web:Jer.9.N = oshb:Jer.9.N-1 form, or '(MT c:v)')."})
    per_row = {rid: items for rid, items in per_row.items() if items and rid in rows}
    ids = sorted(per_row, key=lambda r: rows[r]["chunk_index_in_book"])
    out_dir = HERE / "cwo"
    out_dir.mkdir(exist_ok=True)
    slices = []
    for n in range(0, len(ids), 8):
        k = n // 8 + 1
        ch = ids[n:n + 8]
        sl = {"schema": "jer_cwo_orders_slice.v1", "agent": f"cwo{k:02d}", "attempt_id": f"jer_cwo_{k:02d}_a1",
              "output_file": f"cwo/cwo_{k:02d}.jsonl", "row_ids": ch,
              "orders": {rid: {"row_id": rid, "op": "replace", "current_row": rows[rid], "items": per_row[rid],
                               "cwo_texts": {it["cwo"]: CWO_TEXT[it["cwo"]] for it in per_row[rid]}} for rid in ch}}
        (out_dir / f"orders_cwo_{k:02d}.json").write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        slices.append({"slice": sl["agent"], "attempt_id": sl["attempt_id"], "rows": ch, "cwos": sorted({it["cwo"] for rid in ch for it in per_row[rid]})})
    parity = {cwo: {"ordered": True, "candidates_from_scan": (len(scan[cwo]["candidates"]) if isinstance(scan[cwo].get("candidates"), list) else "ngram7 grams " + str(len(grams))),
                    "rows_ordered": sorted({rid for rid, its in per_row.items() if any(it["cwo"] == cwo for it in its)})} for cwo in CWO_TEXT}
    rec = {"schema": "jer_cwo_orders.v1", "corpus": str(rows_path), "scan": str(scan_path), "rows_ordered": len(ids), "slices": slices, "parity": parity,
           "law": "E-18: every CWO carried to execution as its OWN sweep; executed/ordered parity is recorded at the wave close by re-running _cwo_scan.py over the revised corpus"}
    (HERE / "cwo_orders.v1.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"rows_ordered": len(ids), "slices": slices, "parity_counts": {k: v["candidates_from_scan"] for k, v in parity.items()}}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
