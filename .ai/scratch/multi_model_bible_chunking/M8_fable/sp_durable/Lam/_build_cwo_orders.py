#!/usr/bin/env python3
"""Build the Lamentations CWO-wave orders (E-18: every corpus-wide order executes as its OWN sweep) from the
deterministic scan over the post-author-apply corpus (rows_v2.jsonl) + the boss ledger's VERBATIM corpus_wide_orders
(reviews/boss_lam_b1.json, 13 entries; ruling B1-8 is the record decision). One order per row carrying every CWO item
that hits it: EXACT-arm items (CWO-1/2/4/6/10) only where the scan found a candidate (with the scan evidence);
HEURISTIC-arm items (CWO-3/5/7/8/9/11/12/13) on EVERY row of the 26-row scope (with the scan's screen evidence).
Slices = the four review clusters (review_clusters.json; <=7 rows each, canonical order; seam-consistent);
authors are sonnet; verification = re-running _cwo_scan.py over the revised corpus (every exact arm must return
0 candidates; heuristic arms are reconciled against the authors' per-item dispositions) + the fresh full sweep.
Writes cwo/orders_cwo_NN.json + cwo_orders.v1.json (the executed/ordered parity record the close gate requires).
Usage: _build_cwo_orders.py rows_v2.jsonl scan.json"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXACT = ("CWO-1", "CWO-2", "CWO-4", "CWO-6", "CWO-10")
HEUR = ("CWO-3", "CWO-5", "CWO-7", "CWO-8", "CWO-9", "CWO-11", "CWO-12", "CWO-13")
INSTR = {
    "CWO-1": "REMOVE every observed_substrate_signals key whose token set names the parashah mark layer (the scan lists the key); the disclosure the key carried must stand in device_notes prose with the single-witness and tier-3-weak caveats and the PE-never-conflated-with-SAMEKH note (verify the mark type at the verse from pmarks_Lam.json before writing it); if the device the key encoded is a TEXT phenomenon (e.g. a closing hymn, an imprecatory close), re-key it to that text device under one settled key per device - never to a mark.",
    "CWO-2": "For every listed sentence: either add, INSIDE THE SAME SENTENCE, a sweep citation carrying a DIGIT and a unit word (verses / occurrences / tokens / marks / segments / notes) obtained by running sweep.py on the named object at the named tier, or rewrite the sentence without the universal/exclusivity word (an ordinal use such as 'the first two sites' is rewritten with a non-listed word); the claim is never tier-dampened by a weak witness. Re-run the sentence test on your saved row: zero unmatched sentences.",
    "CWO-4": "device_notes must name BOTH the in-span verse and the out-of-span verse for the listed adjacency (the scan gives the form, its book-wide hit count, the in-span hits and the adjacent out-of-span verse); verify the hit yourself with sweep.py before writing; keep the disclosure count-true.",
    "CWO-6": "Replace the listed positional / neighbouring-unit phrase with a formulation naming the VERSE (cross-row references are verse-anchored; self-reference as 'this unit' is exempt); zero hits on re-scan.",
    "CWO-10": "Add the ketiv/qere disclosure IN THE SAME FIELD as the listed oshb: splice: name that the verse is marked in the K/Q inventory (pmarks_Lam.json kq) and whether the spliced form stands at the variant; at Lam.4.3 and Lam.5.7 disclose BOTH notes (doubled-note verses).",
    "CWO-3": "Re-derive every digit-bearing sweep citation on the row (the scan lists the candidate sentences): re-run the sweep on the named OBJECT at the named tier with sweep.py, read every member's form class from the pointed bytes, and confirm the digit reproduces; split any blended citation (one digit over two objects) into one citation per object; rewrite a citation whose digit does not reproduce with its true object and digit. Report each citation as verified or rewritten.",
    "CWO-5": "Read every sentence of boundary_rationale and strongest_rejected_alternative in which a parashah / setumah / petuchah / SAMEKH / PE term stands (the scan lists the sentences where a driver verb co-occurs; read the others too): a mark may only CORROBORATE a close already carried by a text signal; rewrite driver wording to corroboration wording or delete it; every mark citation carries the single-witness and tier-3-weak disclosure with the two mark types never conflated.",
    "CWO-7": "For every form-class label on the row (the scan lists them with context): splice the token from the pointed verse it names (verse_map_oshb.json) and read it; the label must survive the reading or be corrected; each check names its verse in device_notes where the label is load-bearing.",
    "CWO-8": "Locate the defining form of the row's unit_type value inside the span and name its verse; where it is absent, or rides on a minority of the span's verses, device_notes carries EXACTLY ONE sentence disclosing the per-bytes deviation with arithmetic true to the span's verse count (the scan gives the count); literature_type_guess asserts no speech class the substrate does not carry; the unit_type VALUE itself is not changed in this wave (a value change is a boss-level decision - report it if you judge one is needed).",
    "CWO-9": "For every observed_substrate_signals key, name (to yourself, from the bytes) the verse INSIDE the span whose pointed bytes carry the phenomenon; delete a key whose phenomenon stands only outside the span, or re-object it to a phenomenon the span's own bytes carry (one key per device; no positional or _stack suffix; no blend of a device with a title or addressee).",
    "CWO-11": "Resolve the strongest_rejected_alternative to an explicit contiguous verse range the witness carries (chapter verse counts 22/22/66/22/22) and confirm the stated ground argues FOR the alternative rather than restating the ground for the seam taken; rewrite where it fails; a criterion that indicts the row's own close as much as the alternative is replaced.",
    "CWO-12": "Name (in boundary_rationale) the tier-1 text signal at EACH seam with its verse; where either seam has none (a seam held on disclosed continuity, on tier-3-only corroboration, or inside a §7 held-open region), set frontier_flag_considered true and lower confidence to medium_low or lower (never raise confidence in this wave); the whole-poem cap stays separate and hard (a whole-poem span sits at medium_low or low with the flag and the cap disclosure).",
    "CWO-13": "Read every Hebrew splice back inside its own sentence (the scan lists the runs with context): the paired English gloss covers exactly the words spliced, and a paired translation quotation covers the same clause the splice covers and no wider; widen the splice or narrow the gloss until they match (E-15: one closed curly pair per WEB run, re-cut before nested marks).",
}


def main():
    rows_path, scan_path = Path(sys.argv[1]), Path(sys.argv[2])
    rows_list = [json.loads(l) for l in rows_path.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    rows = {r["decision_id"]: r for r in rows_list}
    scan = json.load(open(scan_path, encoding="utf-8"))["orders"]
    boss = json.load(open(HERE / "reviews" / "boss_lam_b1.json", encoding="utf-8-sig"))
    CWO_TEXT = {c["id"]: {k: c[k] for k in ("id", "arm", "predicate", "scope", "test") if k in c} for c in boss["corpus_wide_orders"]}
    assert set(CWO_TEXT) == set(EXACT) | set(HEUR), sorted(CWO_TEXT)
    rec_ruling = next((r for r in boss["rulings"] if r.get("decision") == "record"), None)
    assert rec_ruling and rec_ruling["id"] == "B1-8", "record ruling B1-8 not found"
    for k in CWO_TEXT:
        CWO_TEXT[k]["boss_record_ruling"] = {"id": rec_ruling["id"], "grounds": rec_ruling.get("grounds"), "consequence": rec_ruling.get("consequence")}
        CWO_TEXT[k]["orchestrator_instruction"] = INSTR[k]
    per_row = defaultdict(list)
    for cwo in EXACT:
        by = defaultdict(list)
        for c in scan[cwo]["candidates"]:
            by[c["row"]].append({k: v for k, v in c.items() if k != "row"})
        for rid, ev in by.items():
            per_row[rid].append({"cwo": cwo, "arm": "exact", "evidence": ev, "instruction": INSTR[cwo]})
    for cwo in HEUR:
        for c in scan[cwo]["candidates"]:
            per_row[c["row"]].append({"cwo": cwo, "arm": "heuristic", "evidence": {k: v for k, v in c.items() if k != "row"}, "instruction": INSTR[cwo]})
    assert set(per_row) == set(rows), f"scope mismatch: {sorted(set(rows) ^ set(per_row))}"
    clusters = json.load(open(HERE / "review_clusters.json", encoding="utf-8-sig"))["clusters"]
    out_dir = HERE / "cwo"; out_dir.mkdir(exist_ok=True)
    slices, seen = [], set()
    for k, cl in enumerate(clusters, 1):
        ch = [rid for rid in cl["row_ids"] if rid in rows]
        assert ch == cl["row_ids"], f"cluster {cl['id']} rows missing from the corpus: {sorted(set(cl['row_ids']) - set(rows))}"
        assert len(ch) <= 8 and not (set(ch) & seen); seen |= set(ch)
        sl = {"schema": "lam_cwo_orders_slice.v1", "agent": f"cwo{k:02d}", "attempt_id": f"lam_cwo_{k:02d}_a1", "cluster": cl["id"], "output_file": f"cwo/cwo_{k:02d}.jsonl", "row_ids": ch,
              "orders": {rid: {"row_id": rid, "op": "replace", "current_row": rows[rid], "items": sorted(per_row[rid], key=lambda it: int(it["cwo"].split("-")[1])),
                               "cwo_texts": {it["cwo"]: CWO_TEXT[it["cwo"]] for it in per_row[rid]}} for rid in ch}}
        (out_dir / f"orders_cwo_{k:02d}.json").write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        slices.append({"slice": sl["agent"], "attempt_id": sl["attempt_id"], "cluster": cl["id"], "rows": ch, "exact_items": sum(1 for rid in ch for it in per_row[rid] if it["arm"] == "exact"),
                       "cwos": sorted({it["cwo"] for rid in ch for it in per_row[rid]}, key=lambda x: int(x.split("-")[1]))})
    assert seen == set(rows)
    parity = {}
    for cwo in EXACT + HEUR:
        ro = sorted({rid for rid, its in per_row.items() if any(it["cwo"] == cwo for it in its)}, key=lambda r: rows[r]["chunk_index_in_book"])
        parity[cwo] = {"arm": CWO_TEXT[cwo]["arm"], "ordered": True, "candidates_from_scan": (len(scan[cwo]["candidates"]) if cwo in EXACT else f"scope {len(scan[cwo]['candidates'])} rows (heuristic screen)"), "rows_ordered": ro, "rows_ordered_count": len(ro)}
    rec = {"schema": "lam_cwo_orders.v1", "corpus": str(rows_path), "scan": str(scan_path), "rows_in_corpus": len(rows), "rows_ordered": len(per_row), "slices": slices, "parity": parity,
           "law": "E-18: every CWO carried to execution as its OWN sweep (exact arms tool-first from the scan; heuristic arms over the whole scope as sonnet sweep slices); executed/ordered parity is recorded at the wave close by re-running _cwo_scan.py over the revised corpus and reconciling the authors' per-item dispositions (_cwo_parity.py)"}
    (HERE / "cwo_orders.v1.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"rows_ordered": len(per_row), "slices": [{k: v for k, v in s.items() if k != "rows"} | {"rows": len(s["rows"])} for s in slices], "parity_counts": {k: v["candidates_from_scan"] for k, v in parity.items()}}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
