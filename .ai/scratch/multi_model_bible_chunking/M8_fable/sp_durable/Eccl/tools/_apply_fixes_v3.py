#!/usr/bin/env python3
"""Orchestrator: build rows_v3 = rows_v2 + micro-fix replacements + the s5
deterministic observed_substrate_signals normalization (oss FIELD ONLY;
prose leaks are author-cured). Emits a full before/after diff of every
normalized oss entry for audit."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (SPBOOK / "rows_v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by_id = {r["writer_decision_id"]: i for i, r in enumerate(rows)}

replaced = 0
for name in ("p01_fixes.jsonl", "p02p03_fixes.jsonl"):
    for l in (SPBOOK / "author" / name).read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        e = json.loads(l)
        op = e.pop("_op")
        assert op == "replace", f"unexpected op {op} in micro-fix batch"
        wid = e["writer_decision_id"]
        assert wid in by_id, f"fix targets unknown row {wid}"
        missing = set(rows[by_id[wid]].keys()) - set(e.keys())
        assert not missing, f"{wid} fix drops fields: {missing}"
        rows[by_id[wid]] = e
        replaced += 1

# --- s5 oss normalization (deterministic; field-scoped) ---
PMARKS_MAP = {"kq": "kq_distribution.sites", "paseq": "paseq_sites"}
FILE_PREFIX = {
    "eccl_device_inventory.json": "", "eccl_device_inventory": "",
    "web_mt_offset_map.json": "offset_crosswalk", "web_mt_offset_map": "offset_crosswalk",
    "risk_signals.jsonl": "substrate_risk_flags", "risk_signals": "substrate_risk_flags",
    "book_observation.jsonl": "substrate_book_observation", "book_observation": "substrate_book_observation",
    "span_features.jsonl": "substrate_span_features", "span_features": "substrate_span_features",
    "verse_inventory.json": "verse_inventory_counts", "verse_inventory": "verse_inventory_counts",
}

def normalize_entry(s: str):
    toks = s.split(" ", 1)
    head = toks[0]
    rest = toks[1] if len(toks) > 1 else ""
    if head in ("pmarks_Eccl.json", "pmarks_Eccl"):
        sub = rest.split(" ", 1)
        key = sub[0].rstrip(":").lower()
        tail = sub[1] if len(sub) > 1 else ""
        mapped = PMARKS_MAP.get(key)
        if mapped:
            return f"{mapped}: {tail}".rstrip()
        return f"parashah_distribution.sites: {rest}".rstrip()
    if head in FILE_PREFIX:
        label = FILE_PREFIX[head]
        if not label:                       # device inventory: rest already keys
            return rest.strip() or s
        return f"{label}: {rest}".rstrip()
    return s

diff = []
for r in rows:
    oss = r.get("observed_substrate_signals")
    if not isinstance(oss, list):
        continue
    new = []
    for e in oss:
        n = normalize_entry(e) if isinstance(e, str) else e
        if n != e:
            diff.append({"row": r["writer_decision_id"], "before": e, "after": n})
        new.append(n)
    r["observed_substrate_signals"] = new

out = SPBOOK / "rows_v3.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
(SPBOOK / "oss_normalization_diff.json").write_text(
    json.dumps(diff, ensure_ascii=False, indent=1), encoding="utf-8")
resid = [d for d in diff if ".json" in d["after"] or ".jsonl" in d["after"]]
print(json.dumps({"rows": len(rows), "fix_replacements": replaced,
                  "oss_entries_normalized": len(diff),
                  "residual_file_refs_after": len(resid),
                  "sample": diff[:3], "out": out.name}, ensure_ascii=False, indent=1))
