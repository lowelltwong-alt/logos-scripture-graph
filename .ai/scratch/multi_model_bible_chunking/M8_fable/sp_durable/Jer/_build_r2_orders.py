#!/usr/bin/env python3
"""Bounded SECOND repair cycle for a shipped book (OWNER_REPAIR_ADVANCE_2026-09-06 item 2: after one
bounded cycle, diagnose rather than repeat blindly). v2 (2026-09-06, E-24):
- collects every semcheck finding (FAIL rows + low findings on pass rows; compatible field-level
  cures are batched) plus the orchestrator's recorded follow-ups for the book;
- a finding on a PIPELINE-OWNED field (chunk_index_in_book renumbered by span order; final_sha256
  content address recomputed by the sweep) is RECORDED, never ordered;
- a finding whose field names ANOTHER row (cross-row: ID / neighbour ID / partner row ID) is ROUTED
  to that row so a seam-pair cure lands on both rows; a routed row with no first-cycle repaired row
  is ordered against its SHIPPED row (partner pull-in, recorded with the reporting row);
- the cycle is split into <=8-row slices (r2 alone, or r2a, r2b, ...), each with its own attempt id,
  orders file, output packet and sonnet launch message. Every r2* packet SUPERSEDES the r1 row in
  the sweep; a targeted r2 semcheck follows.
Usage: _build_r2_orders.py <Book>"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
SC = SP.parent
SPW = str(SP)
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
M8W = str(M8)
PIPELINE_OWNED = ("chunk_index_in_book", "final_sha256")
ROW_ID = re.compile(r"M8-[A-Za-z0-9]+-\d{3}[a-z]?")


def load_rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def must(p: str) -> str:
    assert Path(p).exists(), "MISSING referenced path: " + p
    return p


def main():
    book = sys.argv[1]
    rep = SP / "REPAIR" / book
    shipped = {r["decision_id"]: r for r in load_rows(M8 / "book_chunks" / book / "chunks.jsonl")}
    field_names = set(next(iter(shipped.values())).keys())
    repaired = {}
    for p in sorted(rep.glob(f"repair_{book}_[0-9][0-9].jsonl")):
        for o in load_rows(p):
            if o.get("_op") != "retire":
                repaired[o["decision_id"]] = ({k: v for k, v in o.items() if k != "_op"}, p.name)
    items, not_author, routed = {}, [], []
    for s in sorted(rep.glob(f"semcheck_{book}_[0-9][0-9].json")):
        d = json.load(open(s, encoding="utf-8"))
        for r in d["rows"]:
            rid = r["decision_id"]
            for f in r.get("findings", []):
                fld = str(f.get("field", ""))
                head = fld.split(" ")[0].split("/")[0].strip()
                if head in PIPELINE_OWNED and not ROW_ID.search(fld):
                    not_author.append({"row": rid, "field": fld, "severity": f.get("severity"), "source": s.name,
                                       "resolution": "pipeline-owned field: cured deterministically by the sweep (renumber / recompute) and verified by its coherence gate; not an author order"})
                    continue
                targets = [t for t in ROW_ID.findall(fld) if t != rid] or [rid]
                named_fields = [fn for fn in field_names if fn in fld and fn not in PIPELINE_OWNED]
                for t in targets:
                    entry = {"source": s.name, "verdict": r["verdict"], "finding": f, "checker_grounds": r.get("grounds", "")[:1500]}
                    if t != rid:
                        entry["routed_from"] = rid
                        entry["target_fields"] = named_fields or ["see the finding text"]
                        entry["routing_note"] = (f"raised on {rid}'s check; cure lands on THIS row ({t}) so the seam pair / neighbourhood is argued at one tier on both rows")
                        routed.append({"from": rid, "to": t, "field": fld, "severity": f.get("severity"), "source": s.name})
                    items.setdefault(t, []).append(entry)
    fu = SC / "_repair_followups.json"
    if fu.is_file():
        for e in json.load(open(fu, encoding="utf-8")).get(book, []):
            items.setdefault(e["row"], []).append({"source": "orchestrator follow-up", "verdict": "n/a",
                                                     "finding": {"severity": "medium", "class": e["class"], "field": e["field"], "defective_text": "", "byte_evidence": e.get("source", ""), "proposed_cure": f"cure the named defect in {e['field']} (register: no toolkit filenames or staged-file stems in row prose)"}})
    orders, partners = {}, []
    for rid, its in items.items():
        cur, src = repaired.get(rid, (None, None))
        partner = cur is None
        if partner:
            assert rid in shipped, f"{rid}: routed target is not a shipped row"
            cur, src = shipped[rid], "shipped (partner pull-in: no first-cycle order on this row)"
            partners.append(rid)
        orders[rid] = {"row_id": rid, "book": book, "op": "replace", "span_target": None, "unit_type_target": None, "parent_collection_target": None,
                       "insert_after": None, "current_row": cur, "current_row_source": src, "items": its, "span_ops_from": [], "low_items_folded": [],
                       "partner_pull_in": partner,
                       "instruction": ("SECOND CYCLE - PARTNER ROW pulled in by the independent checker's seam-pair / neighbourhood finding on the row named in routed_from: cure exactly the listed finding on THIS row (current_row is the SHIPPED row, untouched by the first cycle); every other field stays byte-identical to current_row; no span change."
                                       if partner else
                                       "SECOND CYCLE: cure every listed finding exactly (the checker's byte evidence and one-sentence cure are the controlling text; re-derive from bytes before installing); every other field stays byte-identical to current_row; no span change.")}
    ids = sorted(orders, key=lambda r: orders[r]["current_row"]["chunk_index_in_book"])
    tags = ["r2"] if len(ids) <= 8 else [f"r2{chr(97 + i)}" for i in range((len(ids) + 7) // 8)]
    d = json.load(open(SC / "_repair_launch_msgs.json", encoding="utf-8"))
    base = next(v for k, v in d.items() if v["book"] == book)["message"]
    out_summary = []
    for n, tag in enumerate(tags):
        sids = ids[n * 8:(n + 1) * 8]
        sl = {"schema": "m8_repair_orders_slice.v1", "book": book, "slice": f"rep_{book}_{tag}", "attempt_id": f"rep_{book}_{tag}_a1",
              "output_file": f"REPAIR/{book}/repair_{book}_{tag}.jsonl", "row_ids": sids, "orders": {i: orders[i] for i in sids},
              "authority": {"ruling": "OWNER_REPAIR_ADVANCE_2026-09-06.md", "sha256": hashlib.sha256((M8 / "OWNER_REPAIR_ADVANCE_2026-09-06.md").read_bytes()).hexdigest()},
              "cycle": 2, "cycle_slices": tags, "supersedes_rows_from": sorted({repaired[i][1] for i in sids if i in repaired}),
              "partner_pull_ins": [i for i in sids if orders[i]["partner_pull_in"]],
              "findings_not_ordered": not_author, "findings_routed": routed}
        op = rep / f"orders_rep_{book}_{tag}.json"
        op.write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        out_w = SPW + f"\\REPAIR\\{book}\\repair_{book}_{tag}.jsonl"
        assert not Path(out_w).exists(), "output already present: " + out_w
        out = []
        for ln in base.split("\n"):
            if ln.startswith("You are REPAIR AUTHOR"):
                ln = f"You are REPAIR AUTHOR rep_{book}_{tag} (attempt id rep_{book}_{tag}_a1), the BOUNDED SECOND CYCLE of the OW-2 backlog repair lane for the SHIPPED {book} corpus under the owner's standing ruling OWNER_REPAIR_ADVANCE_2026-09-06. Model: claude-sonnet-5; effort ORDERED session-default, NOT VERIFIED (recorded honestly). Read the brief FIRST and follow it exactly:"
            elif ln.startswith("YOUR ORDERS FILE"):
                ln = (f"YOUR ORDERS FILE (exact path; READ FIRST; {len(sids)} rows, ids in order: {', '.join(sids)}; every order is a field-level replace; current_row is the FIRST-cycle REPAIRED row, or - for a PARTNER ROW pulled in by a seam-pair finding (partner_pull_in true) - the SHIPPED row; each entry lists the independent semantic checker's findings (severity, class, field, defective text, byte evidence, one-sentence cure; a routed finding names the row it was raised on and the fields it lands on here) and any orchestrator follow-up - cure every listed finding exactly and change nothing else): {must(str(op))}")
            elif ln.startswith("YOUR ONLY DELIVERABLE"):
                ln = f"YOUR ONLY DELIVERABLE (exact path; one JSON object per line; write it directly): {out_w}"
            elif ln.startswith(" Your slice carries NO span op") or ln.startswith(" SPAN OPS in your slice"):
                ln = " Your slice carries NO span op (second-cycle field-level cures only)."
            elif ln.startswith("FINAL MESSAGE"):
                ln = f"FINAL MESSAGE = raw JSON only (no prose, no fences), per the brief's contract, with \"attempt_id\":\"rep_{book}_{tag}_a1\"."
            elif "_private" in ln and "Private scratch ONLY" in ln:
                ln = re.sub(r"named rep_\w+_private", f"named rep_{book}_{tag}_a1_private", ln)
            out.append(ln)
        msg = "\n".join(out)
        assert f"rep_{book}_{tag}_a1" in msg and f"orders_rep_{book}_{tag}.json" in msg and out_w in msg
        d[f"rep_{book}_{tag}_a1"] = {"book": book, "slice": f"rep_{book}_{tag}", "rows": sids, "output": out_w, "message": msg}
        out_summary.append({"slice": f"rep_{book}_{tag}", "rows": sids, "partners": sl["partner_pull_ins"], "items": {i: len(orders[i]["items"]) for i in sids}})
    (SC / "_repair_launch_msgs.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"book": book, "slices": out_summary, "findings_not_ordered": not_author, "findings_routed": routed}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
