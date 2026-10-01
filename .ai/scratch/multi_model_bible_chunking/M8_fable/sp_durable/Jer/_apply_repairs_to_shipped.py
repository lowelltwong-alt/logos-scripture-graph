#!/usr/bin/env python3
"""Guarded application of a passed repair wave to a SHIPPED book (OWNER_REPAIR_ADVANCE_2026-09-06
item 2; OW-3: pre-feedback baseline preserved, every change labeled post-feedback).

GATES (fail-closed, in order): the sweep report for EXACTLY the landed packet set says PASS; every
semcheck packet for the book is present with fail == 0 (or --allow-rows names rows whose FAIL was
re-repaired and re-swept); the shipped corpus still hashes to the plan's pin; the baseline copy
does not already exist with different bytes.
APPLIES: writes receipts/baselines/<Book>_chunks_prefeedback_<sha8>.jsonl (write-once); rebuilds
book_chunks/<Book>/chunks.jsonl from the simulated corpus (same logic as the sweep: replace /
respan / retire / new_row, span order, chunk_index renumbered 1..N); replaces the book's contiguous
block in whole_bible_chunk_map.jsonl line-for-line (every other line byte-identical); updates the
three sidecars for changed rows in place (retired rows' sidecar lines removed; changed rows' span /
confidence / signals refreshed) and lists NEW low-band rows needing bespoke sidecar text in the
receipt as a follow-up; writes receipts/OW2_repairs_<Book>.v1.json with pre/post hashes, the
packet/sweep/semcheck evidence hashes, the rows changed, and a completion_receipt_supersession block.
Usage: _apply_repairs_to_shipped.py <Book> <sweep_out_dir> [--allow-rows id,id] [--dry-run]"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SIDECARS = ("low_confidence_register.jsonl", "frontier_escalation_queue.jsonl", "atlas_candidate_feed.jsonl")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def atomic_write(path: Path, text: str):
    tmp = path.with_suffix(path.suffix + ".applytmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def main():
    args = sys.argv[1:]
    book, out_dir = args[0], Path(args[1]).resolve()
    dry = "--dry-run" in args
    allow = set(args[args.index("--allow-rows") + 1].split(",")) if "--allow-rows" in args else set()
    rep = SP / "REPAIR" / book
    plan = json.load(open(M8 / "receipts" / "OW2_repair_plan.v1.json", encoding="utf-8"))
    shipped_path = M8 / "book_chunks" / book / "chunks.jsonl"
    pre_sha = sha(shipped_path)
    assert pre_sha == plan["shipped_corpora_sha256"][book], f"shipped {book} corpus no longer matches the plan pin"
    packets = sorted(rep.glob(f"repair_{book}_[0-9][0-9].jsonl")) + sorted(rep.glob(f"repair_{book}_r[2-9]*.jsonl"))
    sweep = json.load(open(out_dir / f"sweep_{book}.json", encoding="utf-8"))
    assert sweep["sweep"] == "PASS", "sweep not PASS"
    assert sweep["patches"] == [p.name for p in packets], f"sweep covered {sweep['patches']} but landed packets are {[p.name for p in packets]}"
    sem = sorted(rep.glob(f"semcheck_{book}_[0-9][0-9].json")) + sorted(rep.glob(f"semcheck_{book}_r[2-9]*.json"))
    assert sem, "no semcheck packets"
    latest = {}   # the LATEST verdict per row wins (a second-cycle packet supersedes the first-cycle verdict)
    for s in sem:
        d = json.load(open(s, encoding="utf-8"))
        for r in d["rows"]:
            latest[r["decision_id"]] = (r["verdict"], s.name)
    sem_rows = set(latest)
    fails = [(n, rid) for rid, (v, n) in latest.items() if v != "pass" and rid not in allow]
    assert not fails, f"semcheck FAIL rows not re-repaired: {fails}"
    changed_ids = {o["decision_id"] for p in packets for o in load_rows(p) if o.get("_op") != "retire"}
    missing = changed_ids - sem_rows
    assert not missing, f"changed rows without a semcheck verdict: {sorted(missing)}"

    sim = load_rows(out_dir / f"sim_{book}.jsonl")
    retired = [o["decision_id"] for p in packets for o in load_rows(p) if o.get("_op") == "retire"]
    new_rows = [o["decision_id"] for p in packets for o in load_rows(p) if o.get("_op") == "new_row"]
    old_rows = load_rows(shipped_path)
    old_by = {r["decision_id"]: r for r in old_rows}

    # baseline (write-once)
    bdir = M8 / "receipts" / "baselines"
    bpath = bdir / f"{book}_chunks_prefeedback_{pre_sha[:8]}.jsonl"
    if bpath.is_file():
        assert sha(bpath) == pre_sha, "baseline exists with different bytes"
    payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sim)
    post_sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    # whole-bible map block
    map_path = M8 / "whole_bible_chunk_map.jsonl"
    lines = map_path.read_text(encoding="utf-8").split("\n")
    idx = [i for i, l in enumerate(lines) if l.strip() and json.loads(l).get("book") == book]
    assert idx and idx == list(range(idx[0], idx[-1] + 1)), f"{book} block in the map is not contiguous"
    assert len(idx) == len(old_rows), f"map block {len(idx)} rows vs shipped {len(old_rows)}"
    new_lines = lines[:idx[0]] + [json.dumps(r, ensure_ascii=False) for r in sim] + lines[idx[-1] + 1:]
    map_pre = sha(map_path)

    # sidecars: refresh changed rows in place; drop retired; list new low-band rows
    side_changes = {}
    low_band = {"medium_low", "low"}
    pending_new_low = []
    sim_by = {r["decision_id"]: r for r in sim}
    for name in SIDECARS:
        p = M8 / name
        sl = p.read_text(encoding="utf-8").split("\n")
        out, dropped, refreshed, present = [], 0, 0, set()
        for l in sl:
            if not l.strip():
                out.append(l); continue
            o = json.loads(l)
            if o.get("book") != book:
                out.append(l); continue
            cid = o.get("chunk_decision_id")
            present.add(cid)
            if cid in retired:
                dropped += 1; continue
            if cid in changed_ids:
                r = sim_by[cid]
                o["span"], o["confidence"], o["observed_substrate_signals"] = r["span"], r["confidence"], r.get("observed_substrate_signals", o.get("observed_substrate_signals"))
                refreshed += 1
                out.append(json.dumps(o, ensure_ascii=False)); continue
            out.append(l)
        for cid in changed_ids:
            if sim_by[cid]["confidence"] in low_band and cid not in present:
                pending_new_low.append(cid)
        side_changes[name] = {"pre_sha256": sha(p), "text": "\n".join(out), "dropped": dropped, "refreshed": refreshed}
    pending_new_low = sorted(set(pending_new_low))

    receipt = {
        "schema": "m8_ow2_shipped_repairs.v1", "book": book, "applied_at": datetime.now(timezone.utc).isoformat(),
        "authority": {"ruling": "OWNER_REPAIR_ADVANCE_2026-09-06.md", "sha256": sha(M8 / "OWNER_REPAIR_ADVANCE_2026-09-06.md"), "plan": "receipts/OW2_repair_plan.v1.json", "plan_sha256": sha(M8 / "receipts" / "OW2_repair_plan.v1.json")},
        "label": "POST-FEEDBACK repairs; the pre-feedback baseline is preserved byte-for-byte at the baseline path",
        "baseline": {"path": bpath.relative_to(M8).as_posix(), "sha256": pre_sha},
        "shipped_corpus": {"path": f"book_chunks/{book}/chunks.jsonl", "pre_sha256": pre_sha, "post_sha256": post_sha,
                            "rows_pre": len(old_rows), "rows_post": len(sim)},
        "changes": {"replaced_or_respanned": sorted(changed_ids - set(new_rows)), "new_rows": new_rows, "retired": retired},
        "evidence": {"repair_packets": {p.name: sha(p) for p in packets},
                     "sweep_report": {"path": str(out_dir / f"sweep_{book}.json"), "sha256": sha(out_dir / f"sweep_{book}.json"), "result": "PASS"},
                     "semcheck_packets": {s.name: sha(s) for s in sem}, "semcheck_allow_rows": sorted(allow)},
        "whole_bible_chunk_map": {"pre_sha256": map_pre, "block_rows_pre": len(idx), "block_rows_post": len(sim)},
        "sidecars": {n: {"pre_sha256": v["pre_sha256"], "dropped": v["dropped"], "refreshed": v["refreshed"]} for n, v in side_changes.items()},
        "sidecar_followup_new_low_band_rows_needing_bespoke_text": pending_new_low,
        "completion_receipt_supersession": {"historical_receipt": f"receipts/{book}_completion.json", "historical_receipt_sha256": sha(M8 / "receipts" / f"{book}_completion.json"),
                                            "note": "the historical completion receipt stands unmodified; its chunk_file_sha256 pin identifies the PRE-FEEDBACK corpus (= the baseline above); this receipt records the post-feedback identity"},
        "non_authorizing": True,
    }
    if dry:
        print(json.dumps({k: receipt[k] for k in ("book", "changes", "shipped_corpus", "sidecar_followup_new_low_band_rows_needing_bespoke_text")}, ensure_ascii=False, indent=1)); return 0
    bdir.mkdir(exist_ok=True)
    if not bpath.is_file():
        bpath.write_bytes(shipped_path.read_bytes())
    assert sha(bpath) == pre_sha
    atomic_write(shipped_path, payload)
    assert sha(shipped_path) == post_sha
    atomic_write(map_path, "\n".join(new_lines))
    for name, v in side_changes.items():
        atomic_write(M8 / name, v["text"])
        receipt["sidecars"][name]["post_sha256"] = sha(M8 / name)
    receipt["whole_bible_chunk_map"]["post_sha256"] = sha(map_path)
    rp = M8 / "receipts" / f"OW2_repairs_{book}.v1.json"
    assert not rp.is_file(), "repair receipt already exists for this book"
    rp.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"applied": book, "rows": receipt["shipped_corpus"], "post_sha256": post_sha, "receipt": str(rp), "receipt_sha256": sha(rp),
                      "sidecar_followup": pending_new_low}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
