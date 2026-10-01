#!/usr/bin/env python3
"""FIXUP-2 work orders for Ezekiel, one file per part (ezek_controlling_rulings_a1#e9 ruling S2-ROUTING). Deterministic: it embeds per
row, VERBATIM, every item that binds the row, judges nothing and never edits a row. Modeled on _build_fixup_orders_ezek.py (FIXUP-1).

Item sources, per #e9 S2-ROUTING (3):
  - Ruling orders addressed to author_fixup in the --rulings files (#e9). An order naming rows or exact spans binds to those rows; one
    naming neither is a general writing rule, carried as brief_rules. General writing rules of the --rule-rulings files (#e6, #e7) are
    carried as brief_rules too. Their row-bound orders were FIXUP-1's and are never re-issued.
  - S2's findings routed to author_fixup, verbatim (id, severity, row_or_artifact, claim, evidence, suggested_fix), bound to the part's
    rows they name. S2-03 is carried AS EXECUTED by CWO-EZ-19 (#e9 S2-04), bound to P08-007 only with the sweep manifest's pointer;
    its remaining order is #e9 S2-04's author_fixup order.
  - The CWO-EZ-21 author half, from the sweep manifests' routed_to_author_wave* lists, stamped with the manifest's CWO id.
  - S2-14 mark items: every mark_symmetry_gap flag in the suite report over the exact chain-head bytes whose part is in the wave, with
    the row, the pmarks key, the mark type and the role. #e9 S2-14 names the 5 interior marks and the 1 closing mark; every other flag
    is a front-seam mark. The report's flags must equal those of the report #e9 ruled on (--ruled-report). The two p05 flags go to
    the primaries' triage list in the index, never to orders.
Parts: the parts with at least one item, which must equal the nine #e9 names. Attempt ids ezek_author_fixup2_pNN_a1, execution #e1.
Writes <out>/orders_ezek_author_fixup2_<part>_a1.json and <out>/orders_index.json after the in-flight pin guard. A differing existing
file is never replaced. --dry-run writes nothing.

Usage: _build_fixup2_orders_ezek.py --rows repair/rows_v4_cwo21.jsonl --report <suite report over those exact bytes>
       --ruled-report repair/suite_v4_6c843b14/rows.jsonl.validator_report.json
       --rulings ezek_controlling_agent_rulings_e9.v1.json
       --rule-rulings ezek_controlling_agent_rulings_e6.v1.json ezek_controlling_agent_rulings_e7.v1.json
       --cwo-manifests repair/rows_v4_cwo19.manifest.json repair/rows_v4_cwo20.manifest.json repair/rows_v4_cwo21.manifest.json
       --out fixup2 [--dry-run]"""
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
S2 = EZ / "ezek_fixup_wave_review_S2.json"
RID = re.compile(r"\bP\d{2}-\d{3}\b")
WAVE, ORDERED_BY = "FIXUP-2", "ezek_controlling_rulings_a1#e9 ruling S2-ROUTING"
INTERIOR = {("P01-008", "Ezek.4.12"), ("P01-008", "Ezek.4.14"), ("P03-010", "Ezek.17.8"), ("P04-008", "Ezek.21.18"), ("P08-012", "Ezek.36.21")}
CLOSE = {("P08-013", "Ezek.36.32")}
ROLE_TEXT = ["P01-008 samekh after 4:12 and after 4:14", "P03-010 samekh after 17:8", "P04-008 pe after MT 21:18",
             "P08-012 samekh after 36:21", "P08-013 samekh after 36:32"]
TRIAGE = {("P05-004", "Ezek.22.31"), ("P05-008", "Ezek.24.14")}


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


def author_orders(doc, tag_default):
    xid = doc.get("execution_id") or tag_default
    tag = xid.split("#")[-1] if "#" in xid else tag_default
    out = []
    for r in doc.get("rulings", []):
        n = 0
        for o in r.get("orders", []):
            if str(o.get("to", "")).startswith("author_fixup"):
                n += 1
                out.append({"ref": "%s:%s#%d" % (tag, r["id"], n), "execution": xid, "ruling_id": r["id"], "ruling": r.get("ruling"),
                            "decision": r.get("decision"), "reason": r.get("reason"), "evidence": r.get("evidence", []),
                            "order": o["order"], "exact_spans": o.get("exact_spans", [])})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--ruled-report", required=True)
    ap.add_argument("--rulings", nargs="+", required=True)
    ap.add_argument("--rule-rulings", nargs="*", default=[])
    ap.add_argument("--cwo-manifests", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    absp = lambda s: Path(s) if Path(s).is_absolute() else EZ / s   # noqa: E731
    rows_p, rep_p, ruled_rep_p, out_dir = EZ / a.rows, absp(a.report), absp(a.ruled_report), absp(a.out)
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    rep, ruled_rep = json.loads(rep_p.read_text(encoding="utf-8")), json.loads(ruled_rep_p.read_text(encoding="utf-8"))
    rep_rows_file = Path(rep["rows_file"])
    if not rep_rows_file.is_file() or sha(rep_rows_file) != sha(rows_p):
        raise SystemExit("ABORT: the report was not produced over the exact bytes of %s" % a.rows)
    rul_paths, rule_paths, man_paths = [EZ / p for p in a.rulings], [EZ / p for p in a.rule_rulings], [EZ / p for p in a.cwo_manifests]
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
    order_of = {r["decision_id"]: i for i, r in enumerate(rows)}
    part_of = {r["decision_id"]: r["writer_part"] for r in rows}
    spans = {r["span"]: r["decision_id"] for r in rows}
    items = {r["decision_id"]: [] for r in rows}
    part_findings, problems = {}, []

    def add(did, item):
        if did not in items:
            problems.append("item for unknown row %r: %s" % (did, json.dumps(item, ensure_ascii=False)[:160]))
            return
        if item not in items[did]:
            items[did].append(item)

    # ---- 1. #e9 ruling orders to author_fixup, and the general writing rules ----
    orders, cwo_text, routing, s14 = [], {}, None, None
    for p in rul_paths:
        d = json.loads(p.read_text(encoding="utf-8"))
        for c in d.get("corpus_wide_orders", []):
            cwo_text[c["id"]] = {k: c.get(k) for k in ("predicate", "fields", "remedy", "coverage_report")} | {"issued_by": d.get("execution_id")}
        for r in d.get("rulings", []):
            if r.get("id") == "S2-ROUTING":
                routing = {"execution": d.get("execution_id"), "ruling": r.get("ruling"), "decision": r["decision"]}
            if r.get("id") == "S2-14":
                s14 = r["decision"]
        orders += author_orders(d, p.stem)
    if routing is None or s14 is None:
        raise SystemExit("ABORT: no S2-ROUTING or S2-14 ruling in the rulings files given")
    m = re.search(r"PARTS: nine - ((?:p\d\d, )+p\d\d)\.", routing["decision"])
    if not m:
        raise SystemExit("ABORT: S2-ROUTING (1) does not name the nine parts in the expected form")
    ruled_parts = [x.strip() for x in m.group(1).split(",")]
    for t in ROLE_TEXT:
        if t not in s14:
            raise SystemExit("ABORT: #e9 S2-14 does not carry the role text %r" % t)
    orders_by_ref = {o["ref"]: o for o in orders}
    brief_rules = []
    for o in orders:
        named = [d for d in RID.findall(o["order"]) if d in by_id]
        on_span = [spans[s] for s in o["exact_spans"] if s in spans]
        missing = [s for s in o["exact_spans"] if s not in spans and not any(s in x for d in named for x in strings(by_id[d]))]
        hit = [d for d in named if d in on_span] or on_span or named
        if not hit and not RID.findall(o["order"]) and not o["exact_spans"]:
            brief_rules.append(o["ref"])
            continue
        if missing:
            problems.append("%s names spans no current row carries and no named row's text holds (no span change is allowed): %s" % (o["ref"], missing))
        if not hit:
            problems.append("%s binds to no current row" % o["ref"])
        for d in sorted(set(hit), key=order_of.get):
            add(d, {"kind": "ruling_order", "ref": o["ref"], "op": "replace", "target_span": by_id[d]["span"]})
    for p in rule_paths:
        for o in author_orders(json.loads(p.read_text(encoding="utf-8")), p.stem):
            if not RID.findall(o["order"]) and not o["exact_spans"]:
                orders_by_ref[o["ref"]] = o
                brief_rules.append(o["ref"])

    # ---- 2. S2's routed findings ----
    s2 = json.loads(S2.read_text(encoding="utf-8"))
    m19 = next((mp for mp in man_paths if str(mans[mp].get("cwo", "")).startswith("CWO-EZ-19")), None)
    for f in s2["new_findings"]:
        parts = [x.split(":", 1)[1] for x in f["route"].split("|") if x.startswith("author_fixup:")]
        if not parts:
            continue
        named = set(RID.findall(str(f.get("row_or_artifact", ""))))
        entry = {"kind": "s2_finding", "id": f["id"], "severity": f["severity"], "route": f["route"],
                 "row_or_artifact": f["row_or_artifact"], "claim": f["claim"], "evidence": f["evidence"], "suggested_fix": f.get("suggested_fix")}
        if f["id"] == "S2-03":
            if m19 is None:
                raise SystemExit("ABORT: S2-03 is carried as executed by CWO-EZ-19, but no CWO-EZ-19 manifest was given")
            entry = dict(entry, kind="s2_finding_executed",
                         executed_by={"cwo": "CWO-EZ-19", "manifest": "repair/" + m19.name, "sha256": sha(m19)},
                         note=("#e9 ruling S2-04: the drop of closure.pe is executed by CWO-EZ-19 on P08-002, P08-003 and P08-007; p08 "
                               "carries S2-03 as executed, and its only remaining order is #e9 S2-04's author_fixup order (an optional "
                               "content closure key on P08-007); no other oss change"))
            named = {"P08-007"}
        for part in parts:
            hit = sorted((d for d in named if part_of.get(d) == part), key=order_of.get)
            if hit:
                for d in hit:
                    add(d, entry)
            else:
                part_findings.setdefault(part, []).append(entry)

    # ---- 3. author items routed by the CWO sweep manifests ----
    for mp in man_paths:
        mm = mans[mp]
        cwo = str(mm.get("cwo", "")).split(" ")[0] or mp.stem
        for key, val in mm.items():
            if key.startswith("routed_to_author_wave") and isinstance(val, list):
                for it in val:
                    add(it.get("row") if isinstance(it, dict) else None,
                        {"kind": "cwo_item", "cwo": cwo, "routed_by": "repair/%s %s" % (mp.name, key), "verbatim": it})

    # ---- 4. S2-14 mark items ----
    def gaps(r):
        return [f for f in r["mark_symmetry"]["flags"] if f.get("rule") == "mark_symmetry_gap"]
    now, ruled = gaps(rep), gaps(ruled_rep)
    key = lambda f: (f["decision_id"], f["undisclosed_mt_key"])   # noqa: E731
    if Counter(map(key, now)) != Counter(map(key, ruled)):
        raise SystemExit("ABORT: the mark_symmetry_gap flags over the chain head differ from the %d #e9 ruled on: added %s, gone %s"
                         % (len(ruled), sorted(set(map(key, now)) - set(map(key, ruled))), sorted(set(map(key, ruled)) - set(map(key, now)))))
    roles, triage, in_wave = Counter(), [], []
    for f in now:
        k = key(f)
        role = "interior" if k in INTERIOR else "close" if k in CLOSE else "front seam"
        roles[role] += 1
        rec = {"row": k[0], "pmarks_key": k[1], "mark_types": f.get("mark_types"), "role": role, "row_cites_marks": f.get("row_cites_marks")}
        if part_of[k[0]] not in ruled_parts:
            triage.append(rec)
            continue
        in_wave.append(rec)
        add(k[0], {"kind": "mark_item", "id": "S2-14", "ordered_by": "ezek_controlling_rulings_a1#e9 ruling S2-14", **rec})
    if dict(roles) != {"front seam": 50, "interior": 5, "close": 1} or {(t["row"], t["pmarks_key"]) for t in triage} != TRIAGE \
            or len(in_wave) != 54 or len({x["row"] for x in in_wave}) != 50:
        raise SystemExit("ABORT: the S2-14 classification is not #e9's (roles %s; triage %s; in-wave %d flags on %d rows)"
                         % (dict(roles), sorted((t["row"], t["pmarks_key"]) for t in triage), len(in_wave), len({x["row"] for x in in_wave})))

    # ---- write one file per part ----
    src = {"rulings": [{"path": "Ezek/" + p.name, "sha256": sha(p)} for p in rul_paths],
           "rule_rulings": [{"path": "Ezek/" + p.name, "sha256": sha(p)} for p in rule_paths],
           "rows": {"path": "Ezek/" + a.rows, "sha256": sha(rows_p)},
           "suite_report": {"path": str(rep_p), "sha256": sha(rep_p), "rows_file_sha256": sha(rep_rows_file)},
           "ruled_report": {"path": str(ruled_rep_p), "sha256": sha(ruled_rep_p)},
           "s2_review": {"path": "Ezek/" + S2.name, "sha256": sha(S2)},
           "cwo_manifests": [{"path": "Ezek/" + str(mp.relative_to(EZ)).replace("\\", "/"), "sha256": sha(mp)} for mp in man_paths]}
    parts = []
    for r in rows:
        if r["writer_part"] not in parts:
            parts.append(r["writer_part"])
    index = {"schema": "m8_fixup_orders_index.v1", "wave": WAVE, "book": "Ezek", "ordered_by": ORDERED_BY, "sources": src, "parts": {},
             "parts_without_items": [], "primaries_triage_mark_flags": triage, "problems": problems,
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
        if not entries and not part_findings.get(part):
            index["parts_without_items"].append(part)
            continue
        aid = "ezek_author_fixup2_%s_a1" % part
        used_refs = sorted({it["ref"] for e in entries for it in e["items"] if it.get("kind") == "ruling_order"})
        used_cwos = sorted({it["cwo"] for e in entries for it in e["items"] if it.get("cwo")})
        counts = Counter()
        for e in entries:
            for it in e["items"]:
                counts[it.get("cwo") or it.get("id") if it["kind"] in ("s2_finding", "s2_finding_executed", "mark_item") else it.get("cwo") or it["kind"]] += 1
        counts["part_findings"] = len(part_findings.get(part, []))
        docs[part] = {"schema": "m8_fixup_orders.v1", "wave": WAVE, "book": "Ezek", "part": part, "attempt_id": aid, "execution_id": aid + "#e1",
                      "ordered_by": ORDERED_BY, "fixup2_ruling": routing, "sources": src,
                      "ruling_orders": {k: orders_by_ref[k] for k in used_refs},
                      "brief_rules": {k: orders_by_ref[k] for k in brief_rules},
                      "corpus_wide_orders": {k: cwo_text[k] for k in used_cwos if k in cwo_text},
                      "part_findings": part_findings.get(part, []),
                      "part_rows": [{"decision_id": r["decision_id"], "span": r["span"]} for r in prow],
                      "rows_with_orders": entries, "new_rows": [], "retire": [], "holds": [],
                      "item_counts": dict(sorted(counts.items()))}
        missing_cwo = [k for k in used_cwos if k not in cwo_text]
        if missing_cwo:
            problems.append("%s: CWO ids with no order text in the rulings given: %s" % (part, missing_cwo))
    if sorted(docs) != sorted(ruled_parts):
        problems.append("parts with items %s differ from the nine #e9 names %s" % (sorted(docs), sorted(ruled_parts)))
    summary = {p: {"rows_with_orders": len(d["rows_with_orders"]), "item_counts": d["item_counts"]} for p, d in docs.items()}
    if a.dry_run or problems:
        print(json.dumps({"mode": "DRY_RUN" if a.dry_run else "REFUSED_PROBLEMS", "parts": summary, "parts_without_items": index["parts_without_items"],
                          "triage": triage, "brief_rules": brief_rules, "problems": problems}, ensure_ascii=False, indent=1))
        return 1 if problems else 0
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
    print(json.dumps({"mode": "WRITTEN", "index_sha256": sha(ip), "parts": summary, "triage": triage, "problems": problems}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
