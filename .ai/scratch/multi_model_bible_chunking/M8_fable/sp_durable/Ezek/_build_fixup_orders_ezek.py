#!/usr/bin/env python3
"""FIXUP-1 work orders for Ezekiel, one file per part (ruling FIXUP-1 of ezek_controlling_rulings_a1#e4, with the later controlling
executions given on the command line). Deterministic: it embeds per row, VERBATIM, every item that binds the row, judges nothing
and never edits a row.

Item sources, per #e4 FIXUP-1 (1):
  - Ruling orders addressed to author_fixup, from the rulings files given. Each is embedded once under ruling_orders and
    referenced per row. FIXUP-1 (3) allows no span change, so every op is 'replace' (content only).
  - #e4 FIXUP-1's decision-only additions, as part_additions for the parts they name.
  - Every S1 finding routed to the part, verbatim (claim, evidence, suggested fix). It binds to the part's rows it names, or is
    carried at part level when it names none. S1-05 also binds to the rows its evidence quotes, which carries P07-009, P09-002
    and P10-007 with S1's quoted text (#e5 REG-TF2-1).
  - S1's per-row defect text from respans, content_orders and cwo_sample (verdict 'defect'), verbatim. A row S1 names that
    no longer stands in the chain head (retired by the author wave) is listed in the index, never as a problem.
  - The corpus-wide items from a suite report proven to cover the exact chain-head bytes, each stamped with its CWO id:
    CWO-EZ-14 (register flags); CWO-EZ-15 (collate and normalizer boundary defects); CWO-EZ-16 (refs-entry Hebrew binding);
    CWO-EZ-17 (e15d). Every other HARD finding is carried too. A normalizer defect binds only to the rows where the run
    stands as a whole Hebrew run, never to rows where it is part of a longer run.
  - The author items that CWO sweep manifests route (their routed_to_author_wave* keys), stamped with the manifest's CWO id.
    A manifest counts when it chains to the chain head (CWO-EZ-13 -> CWO-EZ-18 -> head).
  - A ruling order to author_fixup that names no row and no exact span is a general writing rule (#e6): it is carried
    verbatim as brief_rules in every part's orders and in the index, never bound to a row. An exact span may also be entry
    text inside a named row (#e7 CWO18-R1-1); it is never a span change.
  - #e7 CWO18-R1-1 (6): the CWO-EZ-18 items at a pinned outside refs entry are delivered as ONE entry-level item, with the
    entry's bytes before and after the sweep and the ruling's reshape note verbatim.
Parts: every part with at least one item (FIXUP-1 (2)). Attempt ids ezek_author_fixup_pNN_a1, execution #e1 (FIXUP-1 (6)).
Writes <out>/orders_ezek_author_fixup_<part>_a1.json and <out>/orders_index.json after the in-flight pin guard. A differing
existing file is never replaced. --dry-run writes nothing.

Usage: _build_fixup_orders_ezek.py --rows repair/<chain head>.jsonl --report <suite report over those exact bytes>
       --rulings ezek_controlling_agent_rulings_e4.v1.json ezek_controlling_agent_rulings_e5.v1.json [...]
       [--cwo-manifests repair/<sweep>.manifest.json ...] --out fixup1 [--dry-run]"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import HEB_RUN  # noqa: E402

S1 = EZ / "ezek_author_wave_spot_review_S1.json"
RID = re.compile(r"\bP\d{2}-\d{3}\b")
ADDITION = re.compile(r"(p\d{2} - .+?)(?=; p\d{2} - |\. \(2\) )")
CWO15_PROBLEM = ("does not collate against any nearby cited ref",)
EVIDENCE_BOUND = {"S1-05"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


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
    ap.add_argument("--rulings", nargs="+", required=True)
    ap.add_argument("--cwo-manifests", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows_p = EZ / a.rows
    rep_p = Path(a.report) if Path(a.report).is_absolute() else EZ / a.report
    out_dir = Path(a.out) if Path(a.out).is_absolute() else EZ / a.out
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    rep_rows_file = Path(rep["rows_file"])
    if not rep_rows_file.is_file() or sha(rep_rows_file) != sha(rows_p):
        raise SystemExit("ABORT: the report was not produced over the exact bytes of %s" % a.rows)
    rul_paths = [EZ / p for p in a.rulings]
    man_paths = [EZ / p for p in a.cwo_manifests]
    # a manifest counts when it produced or consumed the chain head, or produced the input of a manifest that counts
    mans = {mp: json.loads(mp.read_text(encoding="utf-8")) for mp in man_paths}
    linked, grew = {sha(rows_p)}, True
    while grew:
        grew = False
        for m in mans.values():
            o_, i_ = m.get("output", {}).get("sha256"), m.get("input", {}).get("sha256")
            if (o_ in linked or i_ in linked) and not {o_, i_} <= linked:
                linked |= {o_, i_}
                grew = True
    for mp, m in mans.items():
        if m.get("output", {}).get("sha256") not in linked and m.get("input", {}).get("sha256") not in linked:
            raise SystemExit("ABORT: %s does not chain to the chain head %s" % (mp.name, a.rows))
    by_id = {r["decision_id"]: r for r in rows}
    by_wid = {r["writer_decision_id"]: r["decision_id"] for r in rows}
    order_of = {r["decision_id"]: i for i, r in enumerate(rows)}
    part_of = {r["decision_id"]: r["writer_part"] for r in rows}
    spans = {r["span"]: r["decision_id"] for r in rows}
    runs_of = {r["decision_id"]: {x.strip() for s in strings(r) for x in HEB_RUN.findall(s)} for r in rows}
    items = {r["decision_id"]: [] for r in rows}
    part_findings, part_additions, problems, s1_rows_absent = {}, {}, [], []

    def add(did, item):
        if did not in items:
            problems.append("item for unknown row %r: %s" % (did, json.dumps(item, ensure_ascii=False)[:160]))
            return
        if item not in items[did]:
            items[did].append(item)

    # ---- 1. ruling orders to author_fixup, and FIXUP-1's decision-only additions ----
    orders, cwo_text, fixup1 = [], {}, None
    for p in rul_paths:
        d = json.loads(p.read_text(encoding="utf-8"))
        xid = d.get("execution_id") or p.name
        tag = xid.split("#")[-1] if "#" in xid else p.stem
        for c in d.get("corpus_wide_orders", []):
            cwo_text[c["id"]] = {"order": c.get("order"), "predicate": c.get("predicate"), "why": c.get("why"), "issued_by": xid}
        for r in d.get("rulings", []):
            if r.get("id") == "FIXUP-1" and fixup1 is None:
                fixup1 = {"execution": xid, "ruling": r.get("ruling"), "decision": r["decision"]}
            n = 0
            for o in r.get("orders", []):
                if str(o.get("to", "")).startswith("author_fixup"):
                    n += 1
                    orders.append({"ref": "%s:%s#%d" % (tag, r["id"], n), "execution": xid, "ruling_id": r["id"], "ruling": r.get("ruling"),
                                   "decision": r.get("decision"), "reason": r.get("reason"), "evidence": r.get("evidence", []),
                                   "order": o["order"], "exact_spans": o.get("exact_spans", [])})
    if fixup1 is None:
        raise SystemExit("ABORT: no FIXUP-1 ruling in the rulings files given")
    for frag in ADDITION.findall(fixup1["decision"]):
        part_additions.setdefault(frag[:3], []).append({"from": "%s ruling FIXUP-1 (1)" % fixup1["execution"], "addition": frag})
    orders_by_ref = {o["ref"]: o for o in orders}
    brief_rules = []
    for o in orders:
        named = [d for d in RID.findall(o["order"]) if d in by_id]
        on_span = [spans[s] for s in o["exact_spans"] if s in spans]
        # an exact span may also be entry text inside a named row (#e7 CWO18-R1-1); it is never a span change
        missing = [s for s in o["exact_spans"] if s not in spans and not any(s in x for d in named for x in strings(by_id[d]))]
        if missing:
            problems.append("%s names spans no current row carries (FIXUP-1 (3) allows no span change): %s" % (o["ref"], missing))
        hit = [d for d in named if d in on_span] or on_span or named
        if not hit and not RID.findall(o["order"]) and not o["exact_spans"]:
            brief_rules.append(o["ref"])   # a general writing rule (#e6): every part's orders carry it verbatim
            continue
        if not hit:
            problems.append("%s binds to no current row" % o["ref"])
        for d in sorted(set(hit), key=order_of.get):
            add(d, {"kind": "ruling_order", "ref": o["ref"], "op": "replace", "target_span": by_id[d]["span"]})

    # ---- 2. S1: routed findings and per-row defect text ----
    s1 = json.loads(S1.read_text(encoding="utf-8"))
    for f in s1["new_findings"]:
        parts = [x.split(":", 1)[1] for x in f["route"].split("|") if x.startswith("author_fixup:")]
        named = set(RID.findall(str(f.get("row_or_artifact", ""))))
        if f["id"] in EVIDENCE_BOUND:
            named |= set(RID.findall(str(f.get("evidence", ""))))
        entry = {"kind": "s1_finding", "id": f["id"], "severity": f["severity"], "route": f["route"],
                 "row_or_artifact": f["row_or_artifact"], "claim": f["claim"], "evidence": f["evidence"],
                 "suggested_fix": f.get("suggested_fix")}
        for part in parts:
            hit = sorted((d for d in named if part_of.get(d) == part), key=order_of.get)
            if hit:
                for d in hit:
                    add(d, entry)
            else:
                part_findings.setdefault(part, []).append(entry)

    def s1_row(did, item):
        if did in by_id:
            add(did, item)
        else:
            s1_rows_absent.append({"row": did, "source": item["source"], "findings": item["findings"]})

    for key in ("respans", "content_orders"):
        for e in s1.get(key, []):
            if e.get("verdict") != "defect":
                continue
            for d in RID.findall(str(e.get("row", ""))):
                s1_row(d, {"kind": "s1_row_defect", "source": "S1 " + key, "ref": e.get("ruling") or e.get("order"), "findings": e.get("findings", [])})
    for e in s1.get("cwo_sample", {}).get("rows", []):
        if e.get("verdict") == "defect":
            s1_row(e.get("row"), {"kind": "s1_row_defect", "source": "S1 cwo_sample", "cwos": e.get("cwos"), "findings": e.get("findings", [])})

    # ---- 3. corpus-wide items and HARD findings from the suite report ----
    cs = rep["citation_sweep"]
    for p in cs.get("problems", []) + cs.get("nfd_degraded", []) + cs.get("prose_pair_problems", []):
        d = p.split(":", 1)[0]
        item = {"kind": "hard_finding", "member": "citation_sweep", "finding": p}
        if "[CWO-EZ-16]" in p:
            item["cwo"] = "CWO-EZ-16"
        elif any(s in p for s in CWO15_PROBLEM):
            item["cwo"] = "CWO-EZ-15"
        add(d, item)
    for run, n in Counter(rep["hebrew_normalize_dryrun"].get("defects", [])).items():
        hits = [did for did, rs in runs_of.items() if run.strip() in rs]
        if not hits:
            problems.append("normalizer defect bound to no row as a whole run: %r" % run)
        for d in hits:
            add(d, {"kind": "hard_finding", "member": "normalizer (E-01)", "cwo": "CWO-EZ-15", "listed": n,
                    "finding": "Hebrew run not standing on word boundaries in the verse bytes or the K/Q note layer: %s" % run})
    for f in rep["cap_sweep"].get("failures", []):
        add(by_wid.get(f.split(" ", 1)[0]), {"kind": "hard_finding", "member": "cap_sweep (E-02)", "finding": f})
    for f in rep["register"].get("flags", []):
        add(by_wid.get(f["decision_id"], f["decision_id"]), {"kind": "cwo_item", "cwo": "CWO-EZ-14", "field": f.get("field"),
                                                             "class": f.get("class"), "match": f.get("match"), "context": f.get("context")})
    for f in rep["web_quotes"].get("flags", []):
        if "e15d" in str(f.get("issue")):
            add(f.get("decision_id"), {"kind": "cwo_item", "cwo": "CWO-EZ-17", "field": f.get("field"), "issue": f.get("issue")})

    # ---- 4. author items routed by CWO sweep manifests ----
    r1_note = None   # ezek_controlling_rulings_a1#e7 CWO18-R1-1 (6): one entry-level item per pinned outside refs entry
    for p in rul_paths:
        d = json.loads(p.read_text(encoding="utf-8"))
        for r in d.get("rulings", []):
            if r.get("id") == "CWO18-R1-1":
                t = r["decision"]
                i0, i1 = t.find("plus this note: '"), t.find(".' Whether the author reshapes gates nothing.")
                if i0 < 0 or i1 < 0:
                    raise SystemExit("ABORT: CWO18-R1-1 carries no reshape note in the expected form")
                r1_note = {"ordered_by": "%s ruling CWO18-R1-1 (6)" % d.get("execution_id"), "note": t[i0 + len("plus this note: '"):i1 + 1]}
    for mp in man_paths:
        m = json.loads(mp.read_text(encoding="utf-8"))
        cwo = str(m.get("cwo", "")).split(" ")[0] or mp.stem
        entry_paths = ({e["path"]: e for e in (m.get("assert_r1_shape_after") or {}).get("outside_entries_reported", [])}
                       if r1_note else {})
        grouped = {}
        for key, val in m.items():
            if key.startswith("routed_to_author_wave") and isinstance(val, list):
                for it in val:
                    if isinstance(it, dict) and it.get("path") in entry_paths:
                        grouped.setdefault(it["path"], []).append({"routed_by": "repair/%s %s" % (mp.name, key), "verbatim": it})
                        continue
                    add(it.get("row") if isinstance(it, dict) else None,
                        {"kind": "cwo_item", "cwo": cwo, "routed_by": "repair/%s %s" % (mp.name, key), "verbatim": it})
        for path, its in grouped.items():
            e = entry_paths[path]
            add(e["row"], {"kind": "cwo_item", "cwo": cwo, "entry_level": True, "ordered_by": r1_note["ordered_by"], "path": path,
                           "entry_bytes_before_sweep": e["old"], "entry_bytes_after_sweep": e["new"], "items": its,
                           "note": r1_note["note"]})
        if entry_paths and set(grouped) != set(entry_paths):
            problems.append("%s: pinned outside entries with no routed items to merge: %s" % (mp.name, sorted(set(entry_paths) - set(grouped))))

    # ---- write one file per part ----
    src = {"rulings": [{"path": "Ezek/" + p.name, "sha256": sha(p)} for p in rul_paths],
           "rows": {"path": "Ezek/" + a.rows, "sha256": sha(rows_p)},
           "suite_report": {"path": str(rep_p), "sha256": sha(rep_p), "rows_file_sha256": sha(rep_rows_file)},
           "s1_review": {"path": "Ezek/" + S1.name, "sha256": sha(S1)},
           "cwo_manifests": [{"path": "Ezek/" + str(mp.relative_to(EZ)).replace("\\", "/"), "sha256": sha(mp)} for mp in man_paths]}
    parts = []
    for r in rows:
        if r["writer_part"] not in parts:
            parts.append(r["writer_part"])
    index = {"schema": "m8_fixup_orders_index.v1", "book": "Ezek", "ordered_by": "%s ruling FIXUP-1" % fixup1["execution"],
             "sources": src, "parts": {}, "parts_without_items": [], "s1_rows_not_in_chain_head": s1_rows_absent, "problems": problems,
             "brief_rules": {k: orders_by_ref[k] for k in brief_rules}}
    docs = {}
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
        if not entries and not part_findings.get(part) and not part_additions.get(part):
            index["parts_without_items"].append(part)
            continue
        aid = "ezek_author_fixup_%s_a1" % part
        used_refs = sorted({it["ref"] for e in entries for it in e["items"] if it.get("kind") == "ruling_order"})
        used_cwos = sorted({it["cwo"] for e in entries for it in e["items"] if it.get("cwo")})
        counts = Counter()
        for e in entries:
            for it in e["items"]:
                counts[it.get("cwo") or it["kind"]] += 1
        counts["part_findings"] = len(part_findings.get(part, []))
        counts["part_additions"] = len(part_additions.get(part, []))
        docs[part] = {"schema": "m8_fixup_orders.v1", "book": "Ezek", "part": part, "attempt_id": aid, "execution_id": aid + "#e1",
                      "ordered_by": "%s ruling FIXUP-1" % fixup1["execution"], "fixup1_ruling": fixup1, "sources": src,
                      "ruling_orders": {k: orders_by_ref[k] for k in used_refs},
                      "brief_rules": {k: orders_by_ref[k] for k in brief_rules},
                      "corpus_wide_orders": {k: cwo_text[k] for k in used_cwos if k in cwo_text},
                      "part_additions": part_additions.get(part, []), "part_findings": part_findings.get(part, []),
                      "part_rows": [{"decision_id": r["decision_id"], "span": r["span"]} for r in prow],
                      "rows_with_orders": entries, "new_rows": [], "retire": [], "holds": [],
                      "item_counts": dict(sorted(counts.items()))}
        missing_cwo = [k for k in used_cwos if k not in cwo_text]
        if missing_cwo:
            problems.append("%s: CWO ids with no order text in the rulings given: %s" % (part, missing_cwo))
    summary = {p: {"rows_with_orders": len(d["rows_with_orders"]), "item_counts": d["item_counts"]} for p, d in docs.items()}
    if a.dry_run:
        print(json.dumps({"mode": "DRY_RUN", "parts": summary, "parts_without_items": index["parts_without_items"],
                          "s1_rows_not_in_chain_head": [x["row"] for x in s1_rows_absent], "brief_rules": brief_rules,
                          "problems": problems}, ensure_ascii=False, indent=1))
        return
    targets = [out_dir / ("orders_%s.json" % d["attempt_id"]) for d in docs.values()] + [out_dir / "orders_index.json"]
    g = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek"] + sum([["--target", str(t)] for t in targets], []),
                       capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if g.returncode != 0:
        raise SystemExit("ABORT: an orders target is pinned:\n" + g.stdout)
    out_dir.mkdir(parents=True, exist_ok=True)
    for part, doc in docs.items():
        p = out_dir / ("orders_%s.json" % doc["attempt_id"])
        body = json.dumps(doc, ensure_ascii=False, indent=1)
        if p.exists() and p.read_text(encoding="utf-8") != body:
            raise SystemExit("ABORT: %s exists with different content; orders are never silently replaced" % p.name)
        p.write_text(body, encoding="utf-8", newline="\n")
        index["parts"][part] = {"file": p.name, "sha256": sha(p), **summary[part]}
    ip = out_dir / "orders_index.json"
    body = json.dumps(index, ensure_ascii=False, indent=1)
    if ip.exists() and ip.read_text(encoding="utf-8") != body:
        raise SystemExit("ABORT: orders_index.json exists with different content")
    ip.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"mode": "WRITTEN", "index_sha256": sha(ip), "parts": summary, "parts_without_items": index["parts_without_items"],
                      "problems": problems}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
