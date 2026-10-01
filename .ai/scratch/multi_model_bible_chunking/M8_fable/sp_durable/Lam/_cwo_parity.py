#!/usr/bin/env python3
"""CWO execution-parity record (Lam; CAMPAIGN_CLOSE_GATE item 5): per order, arm, pre-wave scan candidates, rows
ordered, the authors' per-item dispositions (edited / clean, from the collected final messages), the POST-wave scan
candidates over the revised corpus (every EXACT arm must return 0 -> exact_arm_residual empty) and the heuristic arms'
reconciliation (every ordered row carries a disposition). Writes cwo/cwo_parity.<corpus>.json; never overwrites one. Digits are the tools' COUNTS.
Usage: _cwo_parity.py --pre <scan_pre.json> --post <scan_post.json> --finals <_lam_cwo_final_msgs.json> [--orders cwo_orders.v1.json]"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = sys.argv[1:]
def arg(k, d=None): return A[A.index(k) + 1] if k in A else d
pre = json.load(open(arg("--pre"), encoding="utf-8"))
post = json.load(open(arg("--post"), encoding="utf-8"))
finals = json.load(open(arg("--finals"), encoding="utf-8"))
orders = json.load(open(HERE / arg("--orders", "cwo_orders.v1.json"), encoding="utf-8"))
EXACT = {"CWO-1", "CWO-2", "CWO-4", "CWO-6", "CWO-10"}
disp = {}
for aid, fm in finals.items():
    for it in fm.get("items", []):
        disp.setdefault(it.get("cwo"), {}).setdefault(it.get("row"), []).append(it.get("action"))
parity, residual, unreconciled = {}, [], {}
for cwo, p in orders["parity"].items():
    pre_c = pre["orders"][cwo]["candidates"]; post_c = post["orders"][cwo]["candidates"]
    d = disp.get(cwo, {})
    rec = {"arm": p["arm"], "ordered_rows": p["rows_ordered_count"], "rows_ordered": p["rows_ordered"],
           "pre_wave_candidates": len(pre_c) if cwo in EXACT else f"scope {len(pre_c)} rows",
           "post_wave_candidates": len(post_c) if cwo in EXACT else f"scope {len(post_c)} rows (heuristic; reconciled by disposition)",
           "dispositions": {"edited": sum(1 for r, acts in d.items() if any(a == "edited" for a in acts)), "clean": sum(1 for r, acts in d.items() if all(a == "clean" for a in acts)), "rows_with_disposition": len(d)}}
    if cwo in EXACT:
        rec["post_wave_candidate_rows"] = sorted({c["row"] for c in post_c})
        if post_c:
            residual.append({"cwo": cwo, "candidates": len(post_c), "rows": rec["post_wave_candidate_rows"]})
    miss = sorted(set(p["rows_ordered"]) - set(d))
    if miss:
        unreconciled[cwo] = miss
    rec["rows_without_disposition"] = miss
    parity[cwo] = rec
out = {"schema": "lam_cwo_parity.v1", "pre_scan": arg("--pre"), "post_scan": arg("--post"), "post_corpus": post.get("corpus"), "post_corpus_sha256": hashlib.sha256(Path(post["corpus"]).read_bytes()).hexdigest() if Path(post.get("corpus", "")).exists() else None,
       "parity": parity, "exact_arm_residual": residual, "heuristic_rows_without_disposition": unreconciled,
       "status": "GREEN" if not residual and not unreconciled else "RED",
       "law": "E-18: every corpus-wide order executed as its OWN sweep; exact arms verified by the deterministic re-scan (0 candidates); heuristic arms verified by per-row author disposition + the second-generation spot lane"}
# 2026-09-07: this tool used to write a FIXED filename, so a re-run over a later corpus silently replaced
# a record the cycle log had already pinned. It now names the record for the corpus it reconciles and
# REFUSES to overwrite: an existing file of the same name means a parity record for that corpus already
# exists, and replacing it would be exactly the history rewriting that defect produced.
_stem = Path(post.get("corpus", "unknown")).name.replace(".jsonl", "") or "unknown"
_dst = HERE / "cwo" / f"cwo_parity.{_stem}.json"
if _dst.exists() and hashlib.sha256(_dst.read_bytes()).hexdigest() != hashlib.sha256(
        json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")).hexdigest():
    raise SystemExit(f"REFUSING to overwrite an existing parity record with different content: {_dst.name}. "
                     "A parity record for this corpus already exists; re-run parity over the corpus you "
                     "actually mean to reconcile, or version it explicitly.")
_dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"parity_record": _dst.name, "corpus": post.get("corpus"), "status": out["status"]}, indent=1))
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps({k: (v if k != "parity" else {c: {x: r[x] for x in ("arm", "ordered_rows", "pre_wave_candidates", "post_wave_candidates", "dispositions")} for c, r in v.items()}) for k, v in out.items() if k not in ("law",)}, ensure_ascii=False, indent=1))
sys.exit(0 if out["status"] == "GREEN" else 1)
