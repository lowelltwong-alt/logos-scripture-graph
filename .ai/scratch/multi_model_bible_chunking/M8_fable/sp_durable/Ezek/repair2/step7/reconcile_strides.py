#!/usr/bin/env python3
"""Reconcile the two blind step-7 readings of each stride into one record, and the three strides into the step-7 result.

This is a COMPARISON, not an adjudication: per row and checklist item it pairs the two verdicts and marks agreement;
every DEFECT either reader raised is kept with both readers' evidence (a one-reader defect is a candidate, never
dropped - the final remediation lanes re-measure each before anything is written); QUESTIONs and CONF-CAL answers
from both readers are kept side by side for #e16. Refuses unless both readers of a stride have landed and each
answered every row of the slice.

usage: python reconcile_strides.py [--stride <n>]   (default: every stride whose two readers have landed)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
A = EZ / "author" / "repair2_step7"
ITEMS = ("orders_executed", "conclusion_changed", "claims_true", "new_absolutes", "quotations", "role_tokens",
         "register_and_english", "confidence")
SEV = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, None: 0}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731


def load(stride, lane):
    p = A / ("s%d_lane_%s" % (stride, lane)) / "findings.json"
    return (json.loads(p.read_text(encoding="utf-8-sig")), sha(p)) if p.is_file() else (None, None)


def verdict(x):
    return str((x or {}).get("verdict", "MISSING")).upper()


def normalise(row):
    """Readers wrote two layouts: items at row level with severity inside each item (one reader), or items nested under
    'items' with a row-level 'defects' list carrying the severities (another). Both become {item: {verdict, severity,
    evidence, ...}}; a row-level defect whose item verdict was not DEFECT is kept as DEFECT (the list is the finding)."""
    items = dict(row.get("items") or {k: v for k, v in row.items() if k in ITEMS})
    for d in row.get("defects") or []:
        it = d.get("item")
        if it not in ITEMS:
            continue
        cur = dict(items.get(it) or {})
        cur["verdict"] = "DEFECT"
        sev = d.get("severity")
        if SEV.get(sev, 0) > SEV.get(cur.get("severity"), 0):
            cur["severity"] = sev
        cur.setdefault("row_level_defects", []).append(d)
        items[it] = cur
    for q in row.get("questions") or []:
        it = q.get("item") if isinstance(q, dict) else None
        if it in ITEMS and verdict(items.get(it)) == "OK":
            cur = dict(items[it])
            cur["verdict"] = "QUESTION"
            cur.setdefault("row_level_questions", []).append(q)
            items[it] = cur
    return items


def extracted_defects(f):
    return sum(1 for row in f["per_row"].values() for v in normalise(row).values() if verdict(v) == "DEFECT")


def reported_defects(f):
    t = f.get("findings_total_by_severity") or {}
    return sum(v for v in t.values() if isinstance(v, int))


def reconcile(stride):
    (fa, sa), (fb, sb) = load(stride, "a"), load(stride, "b")
    if fa is None or fb is None:
        return None
    rows = sorted(json.loads((HERE / ("step7_spot_lane_%d.v1.json" % stride)).read_text(encoding="utf-8"))["slices"])
    counts = {}
    for name, f in (("A", fa), ("B", fb)):
        ext, rep = extracted_defects(f), reported_defects(f)
        counts[name] = {"extracted_item_defects": ext, "reader_reported_total": rep}
        if rep > 0 and ext == 0:
            raise SystemExit("REFUSED (E-36): reader %s of stride %d reports %d defects and the reconciler extracted none - "
                             "its findings layout is not being read" % (name, stride, rep))
    out_rows, defects, questions = {}, [], []
    for rid in rows:
        ra, rb = normalise(fa["per_row"].get(rid) or {}), normalise(fb["per_row"].get(rid) or {})
        if not ra or not rb:
            raise SystemExit("REFUSED: stride %d row %s missing from a reader" % (stride, rid))
        rec = {}
        for it in ITEMS:
            va, vb = verdict(ra.get(it)), verdict(rb.get(it))
            sev = max(SEV.get((ra.get(it) or {}).get("severity"), 0), SEV.get((rb.get(it) or {}).get("severity"), 0))
            state = ("AGREE_" + va) if va == vb else ("SPLIT_%s_%s" % (va, vb))
            rec[it] = {"state": state, "A": ra.get(it), "B": rb.get(it)}
            if "DEFECT" in (va, vb):
                defects.append({"row": rid, "item": it, "stride": stride, "agreement": "BOTH" if va == vb == "DEFECT" else ("A_ONLY" if va == "DEFECT" else "B_ONLY"),
                                "max_severity": [k for k, v in SEV.items() if v == sev][0], "A": ra.get(it), "B": rb.get(it)})
            elif "QUESTION" in (va, vb):
                questions.append({"row": rid, "item": it, "stride": stride, "A": ra.get(it), "B": rb.get(it)})
        out_rows[rid] = rec
    confcal = {rid: {"A": (fa.get("confcal_answers") or {}).get(rid), "B": (fb.get("confcal_answers") or {}).get(rid)} for rid in rows}
    return {"stride": stride, "readers": {"A": {"sha256": sa, **counts["A"]}, "B": {"sha256": sb, **counts["B"]}}, "rows": len(rows),
            "defects": defects, "questions": questions, "confcal_answers": confcal,
            "cross_row_patterns": {"A": fa.get("cross_row_patterns"), "B": fb.get("cross_row_patterns")},
            # readers named this section three ways (outside_scope_observations_by_severity, out_of_scope_observations,
            # outside_checklist); a first version read two and dropped the third reader's findings silently (E-36)
            "outside_scope": ({"A": fa.get("outside_scope_observations_by_severity") or fa.get("outside_scope_observations"),
                               "B": fb.get("outside_scope_observations_by_severity") or fb.get("outside_scope_observations")}
                              if LEGACY else
                              {"A": {k: v for k, v in fa.items() if re.search(r"out(side)?_?(of_)?scope|outside_checklist", k)},
                               "B": {k: v for k, v in fb.items() if re.search(r"out(side)?_?(of_)?scope|outside_checklist", k)}}),
            "per_row": out_rows}


# VERSIONING: v1 files are the reconciliation #e16 was launched on and are PINNED by it; they are reproduced only with
# --legacy (the first outside-scope extraction) and must match their recorded digests. The widened extraction writes
# v2 files. A generator never rewrites a file a running agent pins (a first re-run did, and was restored byte-for-byte).
LEGACY = "--legacy" in sys.argv
VER = "v1" if LEGACY else "v2"
strides = [int(sys.argv[sys.argv.index("--stride") + 1])] if "--stride" in sys.argv else [1, 2, 3]
done = {}
for s in strides:
    r = reconcile(s)
    if r is None:
        print("stride %d: both readers not yet landed" % s)
        continue
    p = HERE / ("step7_reconciled_stride%d.%s.json" % (s, VER))
    data = json.dumps(r, ensure_ascii=False, indent=1).encode("utf-8")
    if p.is_file() and p.read_bytes() != data and "--overwrite" not in sys.argv:
        raise SystemExit("REFUSED: %s exists with different bytes; a running agent may pin it - run the in-flight guard "
                         "on it and pass --overwrite, or write a new version" % p.name)
    p.write_bytes(data)
    done[s] = r
    tally = {}
    for d in r["defects"]:
        k = "%s/%s" % (d["agreement"], d["max_severity"])
        tally[k] = tally.get(k, 0) + 1
    print(json.dumps({"stride": s, "rows": r["rows"], "defects": len(r["defects"]), "by_agreement_and_severity": tally,
                      "questions": len(r["questions"]), "out": p.name, "sha256": sha(p)}, indent=1))
if all((HERE / ("step7_reconciled_stride%d.%s.json" % (s, VER))).is_file() for s in (1, 2, 3)):
    allr = [json.loads((HERE / ("step7_reconciled_stride%d.%s.json" % (s, VER))).read_text(encoding="utf-8")) for s in (1, 2, 3)]
    comb = {"schema": "ezek_repair2_step7_reconciled.v1", "rows": sum(r["rows"] for r in allr),
            "defects": [d for r in allr for d in r["defects"]], "questions": [q for r in allr for q in r["questions"]],
            "confcal_answers": {k: v for r in allr for k, v in r["confcal_answers"].items()},
            "strides": {r["stride"]: {"readers": r["readers"], "cross_row_patterns": r["cross_row_patterns"], "outside_scope": r["outside_scope"]} for r in allr}}
    p = HERE / ("step7_reconciled.%s.json" % VER)
    data = json.dumps(comb, ensure_ascii=False, indent=1).encode("utf-8")
    if p.is_file() and p.read_bytes() != data and "--overwrite" not in sys.argv:
        raise SystemExit("REFUSED: %s exists with different bytes; a running agent may pin it - run the in-flight guard "
                         "on it and pass --overwrite, or write a new version" % p.name)
    p.write_bytes(data)
    print("combined:", p.name, sha(p), "| rows", comb["rows"], "| defects", len(comb["defects"]), "| questions", len(comb["questions"]))
