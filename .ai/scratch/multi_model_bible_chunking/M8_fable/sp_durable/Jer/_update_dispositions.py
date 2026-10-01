#!/usr/bin/env python3
"""Dispositions-ledger updater (OW-3 item 4 + OWNER_REPAIR_ADVANCE_2026-09-06 items 2-3).
Marks docket items resolved with independent post-repair evidence, preserving the pre-feedback
baseline verdicts and appending a history entry per change; recomputes the summary; replaces the
'jer_resume_gate' text with the live ledger evaluation. Atomic replace with the pre-digest pinned.
Modes:
  --book <Book>   resolve every item on rows the book's repair receipt lists as changed/retired
                  (disposition resolved_repaired; evidence = repair receipt + sweep + semcheck)
  --no-change     resolve the plan's REJECTED / SPAN_REJECTED items (resolved_no_change) and the
                  retained LOW items (resolved_retained_low) with the plan's grounds
Usage: _update_dispositions.py --book Song | --no-change   [--dry-run]"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
LEDGERS = ["receipts/OW2_isa_lf_remediation_dispositions.v1.json",
           "receipts/OW2_five_book_remediation_dispositions.v1.json",
           "receipts/OW2_prov38_remediation_dispositions.v1.json"]
BY = "orchestrator claude-fable-5 under OWNER_REPAIR_ADVANCE_2026-09-06 (delegated judgment)"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def gate_text(d):
    opn = sum(1 for i in d["items"] if i.get("disposition") == "open")
    return (f"OW-2D evaluated from this ledger: {opn} item(s) OPEN of {len(d['items'])}; the Jeremiah resume wait was superseded by "
            "OWNER_REPAIR_ADVANCE_2026-09-06 (Jeremiah proceeds under OW-4); OW-2D remains the ledger evaluation for the backlog")


def apply(ledger_path: Path, changes: dict, dry: bool):
    """changes: item_id -> {disposition, repair_applied, post_repair_evidence, grounds}"""
    pre = sha(ledger_path)
    d = json.load(open(ledger_path, encoding="utf-8"))
    n = 0
    now = datetime.now(timezone.utc).isoformat()
    for it in d["items"]:
        c = changes.get(it["item_id"])
        if not c or it.get("disposition") != "open":
            continue
        it.setdefault("history", []).append({"at": now, "from": "open", "to": c["disposition"], "by": BY})
        it["disposition"] = c["disposition"]
        it["repair_applied"] = c["repair_applied"]
        it["post_repair_evidence"] = c["post_repair_evidence"]
        it["resolution_grounds"] = c["grounds"]
        it["label"] = "post-feedback"
        n += 1
    if n:
        s = d.setdefault("summary", {})
        s["open"] = sum(1 for i in d["items"] if i.get("disposition") == "open")
        s["resolved"] = len(d["items"]) - s["open"]
        s["repairs_applied"] = sum(1 for i in d["items"] if i.get("repair_applied"))
        s["resolved_no_change"] = sum(1 for i in d["items"] if i.get("disposition") == "resolved_no_change")
        s["resolved_retained_low"] = sum(1 for i in d["items"] if i.get("disposition") == "resolved_retained_low")
        d["jer_resume_gate"] = gate_text(d)
        d.setdefault("ledger_history", []).append({"at": now, "pre_sha256": pre, "items_changed": n, "by": BY})
        if not dry:
            tmp = ledger_path.with_suffix(".json.updtmp")
            tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
            assert sha(ledger_path) == pre, "ledger changed under us"
            os.replace(tmp, ledger_path)
    return {"ledger": ledger_path.name, "pre_sha256": pre[:16], "post_sha256": (sha(ledger_path)[:16] if not dry else "dry"), "items_changed": n,
            "open_now": sum(1 for i in d["items"] if i.get("disposition") == "open")}


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    plan = json.load(open(M8 / "receipts" / "OW2_repair_plan.v1.json", encoding="utf-8"))
    changes = {}
    if "--book" in args:
        book = args[args.index("--book") + 1]
        rp = M8 / "receipts" / f"OW2_repairs_{book}.v1.json"
        rec = json.load(open(rp, encoding="utf-8"))
        touched = set(rec["changes"]["replaced_or_respanned"]) | set(rec["changes"]["new_rows"]) | set(rec["changes"]["retired"])
        ev = {"repair_receipt": {"path": rp.relative_to(M8).as_posix(), "sha256": sha(rp)},
              "sweep": rec["evidence"]["sweep_report"], "semcheck_packets": rec["evidence"]["semcheck_packets"],
              "repair_packets": rec["evidence"]["repair_packets"], "role_separation": "repair author (sonnet) != deterministic checker (orchestrator sweep) != semantic checker (opus)"}
        # map docket items to shipped rows via the plan slices
        for sl in sorted((M8.parent.parent.parent.parent / "dummy").glob("*")):
            pass
        from glob import glob
        rep = Path(__file__).resolve().parent.parent / "REPAIR" / book
        for sl in sorted(rep.glob("orders_rep_*.json")):
            o = json.load(open(sl, encoding="utf-8"))
            for rid, od in o["orders"].items():
                if rid not in touched:
                    continue
                for it in od["items"]:
                    cl = it.get("classification")   # r2 finding entries carry no docket classification and are skipped here
                    disp = "resolved_repaired" if cl in ("REPAIR", "SPAN_ACCEPTED", "LOW") else None
                    if disp:
                        changes[it["item_id"]] = {"disposition": disp, "repair_applied": True, "post_repair_evidence": ev,
                                                  "grounds": f"repaired on row {rid} (op {od['op']}) by the {book} repair wave; independent post-repair evidence attached" + (f"; span ruling: {it['span_ruling_orchestrator']['reasons'][:300]}" if it.get("span_ruling_orchestrator") else "")}
                for src in od.get("span_ops_from", []):
                    if src not in changes:
                        rul = plan["span_rulings"].get(src)
                        if rul:
                            changes[src] = {"disposition": "resolved_repaired", "repair_applied": True, "post_repair_evidence": ev,
                                            "grounds": f"span ruling ACCEPT executed on row {rid} (op {od['op']}): {rul['reasons'][:300]}"}
    if "--no-change" in args:
        for iid in plan["resolved_no_change_items"]:
            changes[iid] = {"disposition": "resolved_no_change", "repair_applied": False,
                            "post_repair_evidence": {"plan": "receipts/OW2_repair_plan.v1.json", "kind": "evidence-backed rejection (adjudicator verdict refute / final severity none)"},
                            "grounds": "an evidence-backed rejection is resolved-no-change, not an applied repair (OWNER_REPAIR_ADVANCE_2026-09-06 item 3); the adjudicator's byte-cited grounds stand in the docket"}
        for iid in plan["retained_low_items_not_repaired"]:
            changes[iid] = {"disposition": "resolved_retained_low", "repair_applied": False,
                            "post_repair_evidence": {"plan": "receipts/OW2_repair_plan.v1.json", "kind": "low finding retained with explicit handling"},
                            "grounds": "final severity low on a row not otherwise repaired: retained with explicit handling (OW-3), no repair required under the ruling's completed-books-not-perfection standard; never counted as a medium/high defect for OW-2D"}
    out = [apply(M8 / l, changes, dry) for l in LEDGERS]
    print(json.dumps({"dry_run": dry, "changes_requested": len(changes), "ledgers": out}, indent=1))


if __name__ == "__main__":
    main()
