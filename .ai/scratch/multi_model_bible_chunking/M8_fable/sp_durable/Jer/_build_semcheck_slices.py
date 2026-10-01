#!/usr/bin/env python3
"""Build the r3 targeted independent semantic-check slices for a repaired SHIPPED book
(OWNER_REPAIR_ADVANCE_2026-09-06 item 2: independently check changed semantic warrants/spans and
affected neighbours). Reads the landed repair packets, the plan orders, the shipped corpus and the
sweep's simulated post-repair corpus (for post-repair neighbours); writes
SP/REPAIR/<Book>/semcheck_slices/slice_sc_<Book>_NN.json (<=8 changed rows each) and the opus
launch messages to <scratch>/_semcheck_launch_msgs.json (paths from ONE verified prefix;
outputs verified ABSENT).
Usage: _build_semcheck_slices.py <Book> <sweep_out_dir>"""
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


def load_rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def must(p: str) -> str:
    assert Path(p).exists(), "MISSING referenced path: " + p
    return p


def main():
    book, out_dir = sys.argv[1], Path(sys.argv[2]).resolve()
    rep = SP / "REPAIR" / book
    shipped = {r["decision_id"]: r for r in load_rows(M8 / "book_chunks" / book / "chunks.jsonl")}
    sim = load_rows(out_dir / f"sim_{book}.jsonl")
    sim_idx = {r["decision_id"]: i for i, r in enumerate(sim)}
    orders = {}
    for sl in sorted(rep.glob("orders_rep_*.json")):
        o = json.load(open(sl, encoding="utf-8"))
        for rid, od in o["orders"].items():
            orders[rid] = od
    changed = []
    r2 = "--r2" in sys.argv          # targeted second-cycle check: only the rows the r2 packet changed
    packets = sorted(rep.glob(f"repair_{book}_r[2-9]*.jsonl")) if r2 else sorted(rep.glob(f"repair_{book}_[0-9][0-9].jsonl"))
    for p in packets:
        for obj in load_rows(p):
            if obj.get("_op") == "retire":
                continue
            rid = obj["decision_id"]
            i = sim_idx[rid]
            od = orders[rid]
            changed.append({
                "decision_id": rid, "op": obj["_op"], "packet": p.name,
                "shipped_row": shipped.get(rid), "repaired_row": {k: v for k, v in obj.items() if k != "_op"},
                "order": {"op": od["op"], "span_target": od.get("span_target"), "unit_type_target": od.get("unit_type_target"),
                          "span_ruling_orchestrator": next((it.get("span_ruling_orchestrator") for it in od["items"] if it.get("span_ruling_orchestrator")), None),
                          "items": [({k: it.get(k) for k in ("item_id", "docket", "classification", "class", "filed_severity", "latest",
                                                              "claim", "auditor_grounds", "proposed_change", "adjudicator_grounds")}
                                     if "finding" not in it else
                                     {k: it.get(k) for k in ("source", "verdict", "finding", "checker_grounds", "routed_from", "target_fields", "routing_note")})
                                    for it in od["items"]],
                          "partner_pull_in": od.get("partner_pull_in", False), "current_row_source": od.get("current_row_source"),
                          "retired_partner": [o2["row"] for it in od["items"] if it.get("span_ruling_orchestrator") for o2 in it["span_ruling_orchestrator"]["orders"] if o2["op"] == "retire"]},
                "repaired_row_as_shipped": sim[i],
                "pipeline_owned_fields_note": "chunk_index_in_book is renumbered 1..N by span order and final_sha256 (row content address) is recomputed for every changed row by the deterministic sweep/apply; judge those two fields on repaired_row_as_shipped, never on the packet row",
                "neighbour_prev_post_repair": sim[i - 1] if i > 0 else None,
                "neighbour_next_post_repair": sim[i + 1] if i + 1 < len(sim) else None,
            })
    # the repair author's own reported discrepancies (repair_attempt_receipts.jsonl) ride with the row
    disc = {}
    rec = rep / "repair_attempt_receipts.jsonl"
    if rec.is_file():
        for l in rec.read_text(encoding="utf-8").splitlines():
            if l.strip():
                o = json.loads(l)
                for dd in o.get("discrepancies", []) or []:
                    disc.setdefault(dd.get("order"), []).append({"attempt_id": o.get("attempt_id"), **dd})
    for c in changed:
        c["author_reported_discrepancies"] = disc.get(c["decision_id"], [])
    changed.sort(key=lambda c: sim_idx[c["decision_id"]])
    sdir = rep / "semcheck_slices"
    sdir.mkdir(exist_ok=True)
    tools = must(SPW + rf"\{book}\tools")
    toolkit = next(p for p in ("TOOLKIT.md", "TOOLKIT_AUDIT.md") if (Path(tools) / p).is_file())
    brief = must(SPW + r"\REPAIR\SEMCHECK_BRIEF.md")
    pre = (SC / "_e13_preamble.txt").read_text(encoding="utf-8").strip()
    E19a = (f"E-19 AFFIRMATIVE LINE: SP\\REPAIR\\{book}\\ already exists - write your deliverable directly; never run any "
            "existence check or listing against it or any shared SP directory; your slice and output files are named by exact path below; other checkers' outputs are a hard boundary.")
    E19b = ("E-19 EXACT-PATH LAW: every file you need is named by exact path in this message and in the brief - "
            "glob/wildcard/recursive listing or search outside your own private scratch is banned; an unresolvable path is REPORTED in your final message, never searched for.")
    msgs = {}
    slices = []
    for n in range(0, len(changed), 8):
        k = n // 8 + 1
        rows = changed[n:n + 8]
        tag = f"r2{k:02d}" if r2 else f"{k:02d}"
        sl = {"schema": "m8_repair_semcheck_slice.v1", "book": book, "slice": f"sc_{book}_{tag}", "attempt_id": f"sc_{book}_{tag}_a1",
              "output_file": f"REPAIR/{book}/semcheck_{book}_{tag}.json", "row_ids": [c["decision_id"] for c in rows], "rows": rows,
              "cycle": (2 if r2 else 1),
              "sweep_report": str(out_dir / f"sweep_{book}.json"),
              "sweep_report_sha256": hashlib.sha256((out_dir / f"sweep_{book}.json").read_bytes()).hexdigest()}
        sp = sdir / f"slice_{sl['slice']}.json"
        sp.write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        slices.append(sl["slice"])
        out_w = SPW + "\\" + sl["output_file"].replace("/", "\\")
        assert not Path(out_w).exists(), "output already present: " + out_w
        msgs[sl["attempt_id"]] = f"""{pre}

{E19a}
{E19b}

You are INDEPENDENT SEMANTIC CHECKER {sl['slice']} (attempt id {sl['attempt_id']}) in the OW-2 backlog repair lane of the M8_fable campaign, checking repaired rows of the SHIPPED {book} corpus under the owner's standing ruling OWNER_REPAIR_ADVANCE_2026-09-06. Model: claude-opus-5; effort ORDERED high, NOT VERIFIED (recorded honestly). Read the brief FIRST and follow it exactly:
BRIEF (exact path): {brief}
YOUR SLICE (exact path; {len(rows)} changed rows, ids in order: {', '.join(sl['row_ids'])}; each carries the shipped row, the repaired row, the orders that produced it with every docket item's auditor + adjudicator grounds and the orchestrator's span ruling where one applies, and the post-repair neighbours): {must(str(sp))}
YOUR ONLY DELIVERABLE (exact path; one JSON object; write it directly): {out_w}
Shipped corpus (READ-ONLY): {must(M8W + rf"\book_chunks\{book}\chunks.jsonl")}
Staged tools (USE; run FROM this directory): {tools}
Hazard catalog (MANDATORY PRE-READ): {must(tools + "\\" + toolkit)}
pmarks inventory: {must(SPW + rf"\{book}\pmarks_{book}.json")}
Owner-ruled strategy (LAW): {must(M8W + rf"\book_strategy\{book}.md")}
The deterministic sweep over the simulated post-repair corpus PASSED ({sl['sweep_report']}); a deterministic pass is NOT semantic verification - your checks are what machines cannot see.

RULES YOU MUST APPLY (from the brief): per changed row verify from bytes (collate at the named tier; sweeps with object + unit named) that every docket item's defect is cured and the test that killed the original now passes; that every installed claim, count, tier label and device claim re-derives from the source witnesses (a byte-false, over-tiered or speculative replacement is a FAIL finding); the OW-3 BOTH-SIDES SEAM LAW on every respan/merge/split/new row and every re-argued boundary (quote the preceding close and following onset, tier named; neighbours ruled coherently; tiling survives; dependent fields coherent); the E-17 second-generation checklist (unswept universals, warrant substitution, cross-row contradiction, register bleed, gloss overshoot, unexpanded {{placeholder}} tokens, tier-4 metadata doing driver/corroboration work); disclosed uncertainty; neighbour coherence. verdict pass | fail per row; findings carry severity, class, field, defective text, byte evidence (spliced, tier named) and a one-sentence cure; grounds is ONE STRING; you edit nothing anywhere. M7, every other model lane (M1..M7), A/B lanes and comparison data are FORBIDDEN. Private scratch ONLY in a uniquely-named subdirectory of your own session scratchpad named {sl['attempt_id']}_private; write nothing else under SP; never write into the worktree; never run git.

FINAL MESSAGE = raw JSON only (no prose, no fences), per the brief's contract, with "attempt_id":"{sl['attempt_id']}".
"""
    p = SC / "_semcheck_launch_msgs.json"
    existing = json.load(open(p, encoding="utf-8")) if p.is_file() else {}
    existing.update(msgs)
    p.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"book": book, "changed_rows": len(changed), "slices": slices, "packets": [q.name for q in packets]}, indent=1))


if __name__ == "__main__":
    main()
