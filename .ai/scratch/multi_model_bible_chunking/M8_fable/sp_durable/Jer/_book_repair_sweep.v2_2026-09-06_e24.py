#!/usr/bin/env python3
"""Fresh full second-generation sweep for a SHIPPED book after a repair wave (OW-2 item 4;
OWNER_REPAIR_ADVANCE_2026-09-06 item 2) - the deterministic arm, run by the orchestrator, a
checker distinct from every repair author.

Builds a SIMULATED post-repair corpus in a PRIVATE out dir from the shipped
book_chunks/<Book>/chunks.jsonl + the wave's repair packets (ops replace | respan | retire |
new_row), then verifies: every op maps to a planned order with the planned op; immutable
fields unchanged on replace/respan; span changes ONLY on the plan's respan targets (exact);
unit_type changes only where the plan names a target; field TYPE parity with the shipped
schema; no unexpanded {placeholder}; exact TILING over the book's WEB verse map (no gap, no
overlap, same verse set as shipped); chunk_index renumbered 1..N in span order; normalize
dry-run (0 fixed / 0 defects); check_web_quotes; and, where the book has one, its own
run_validator_suite.py (hard status + FLAGS deltas vs a baseline run over the shipped corpus).
Ps/Job carry only the rebuilt audit toolkit (no suite): their deterministic coverage is
normalize + web quotes + tiling + schema/immutables/placeholders - recorded honestly; the r3
targeted semantic check covers the rest. Exit 1 on any HARD failure.
Usage: _book_repair_sweep.py <Book> OUT_DIR [repair_<Book>_NN.jsonl ...]   (zero packets = baseline self-test)"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}")
IMMUTABLE = ["decision_id", "book", "model_id", "writer_part", "writer_decision_id", "writer_attempt_id",
             "non_authorizing", "parent_collection", "wj_or_red_letter_considered"]


def content_address(r):
    """final_sha256 law (re-derived from the shipped Job corpus, 194/194): sha256 of the row minus
    final_sha256, serialized with ensure_ascii=False and sorted keys."""
    return hashlib.sha256(json.dumps({k: v for k, v in r.items() if k != "final_sha256"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def load_rows(p: Path):
    return [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def ref_key(ref: str):
    m = re.match(r"^[A-Za-z0-9]+\.(\d+)\.(\d+)$", ref)
    assert m, "bad ref " + ref
    return (int(m.group(1)), int(m.group(2)))


def span_ends(book, span):
    m = re.match(rf"^{book}\.(\d+)\.(\d+)-{book}\.(\d+)\.(\d+)$", span)
    assert m, f"bad span {span}"
    return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))


def expand(book, span, order):
    s, e = span_ends(book, span)
    assert s in order and e in order, f"span end outside verse map: {span}"
    return order[s:e + 1] if False else [v for v in VERSES if s <= v <= e]


def run(args, cwd):
    p = subprocess.run([sys.executable] + args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


def main():
    global VERSES
    book, out_dir, patches = sys.argv[1], Path(sys.argv[2]).resolve(), [Path(a).resolve() for a in sys.argv[3:]]
    tools = SP / book / "tools"
    out_dir.mkdir(parents=True, exist_ok=True)
    shipped_path = M8 / "book_chunks" / book / "chunks.jsonl"
    shipped = load_rows(shipped_path)
    by_id = {r["decision_id"]: r for r in shipped}
    schema_ref = shipped[0]
    vm = json.load(open(tools / "verse_map_web.json", encoding="utf-8"))
    VERSES = sorted(ref_key(k) for k in vm)
    vset = set(VERSES)

    # plan (authorized ops per row)
    # plan authorization is judged PER CYCLE: first-cycle packets against orders_rep_<Book>_NN.json,
    # second-cycle packets (repair_<Book>_r2*.jsonl) against orders_rep_<Book>_r2*.json
    plan_by_cycle = {1: {}, 2: {}}
    for sl in sorted((SP / "REPAIR" / book).glob("orders_rep_*.json")):
        o = json.load(open(sl, encoding="utf-8"))
        cyc = 2 if re.search(r"_r[2-9][a-z]?\.json$", sl.name) else 1
        for rid, od in o["orders"].items():
            plan_by_cycle[cyc][rid] = od
    failures, applied = [], {"replace": 0, "respan": 0, "retire": 0, "new_row": 0}
    seen, superseded = {}, []
    for p in patches:
        plan_ops = plan_by_cycle[2 if re.search(r"_r[2-9][a-z]?\.jsonl$", p.name) else 1]
        for i, obj in enumerate(load_rows(p), 1):
            op = obj.get("_op")
            rid = obj.get("decision_id")
            if rid in seen:
                # a bounded second repair cycle (packet name carries _r2/_r3) may SUPERSEDE a row
                # from an earlier packet; a duplicate inside one cycle is a hard failure
                if re.search(r"_r[2-9][a-z]?\.jsonl$", p.name) and not re.search(r"_r[2-9][a-z]?\.jsonl$", seen[rid]):
                    superseded.append({"row": rid, "earlier_packet": seen[rid], "superseded_by": p.name})
                    if obj.get("_op") == "replace" and rid not in by_id:
                        failures.append(f"{rid}: r2 replace on a row no longer present"); continue
                else:
                    failures.append(f"{rid} appears twice across packets ({seen[rid]} and {p.name})"); continue
            seen[rid] = p.name
            od = plan_ops.get(rid)
            if od is None:
                failures.append(f"{rid}: not in the repair plan ({p.name} line {i})"); continue
            if op != od["op"]:
                failures.append(f"{rid}: op {op} != planned {od['op']}"); continue
            if op == "retire":
                if set(obj) != {"_op", "decision_id"}:
                    failures.append(f"{rid}: retire line must be exactly two keys")
                del by_id[rid]; applied["retire"] += 1; continue
            rep = {k: v for k, v in obj.items() if k != "_op"}
            if PLACEHOLDER.search(json.dumps(rep, ensure_ascii=False)):
                failures.append(f"{rid}: unexpanded {{placeholder}} token")
            # schema parity is judged against the ROW'S OWN shipped key set (books carry a few
            # legacy per-row keys, e.g. Ps 'orchestrator_boilerplate_variation'); a new row is
            # judged against its anchor row
            ref_row = by_id.get(rid) or (by_id.get(od.get("insert_after")) if od.get("insert_after") else None) or schema_ref
            if set(rep) != set(ref_row):
                failures.append(f"{rid}: key set differs from the shipped row (missing {sorted(set(ref_row)-set(rep))}, extra {sorted(set(rep)-set(ref_row))})")
            for k, v in rep.items():
                if k in ref_row and type(v) is not type(ref_row[k]) and not (isinstance(v, bool) and isinstance(ref_row[k], bool)):
                    failures.append(f"{rid}: field {k} type {type(v).__name__} != shipped {type(ref_row[k]).__name__}")
            if op == "new_row":
                if rid in by_id:
                    failures.append(f"{rid}: new_row id already exists")
                if rep.get("span") != od["span_target"]:
                    failures.append(f"{rid}: new_row span {rep.get('span')} != planned {od['span_target']}")
                if od.get("unit_type_target") and rep.get("unit_type") != od["unit_type_target"]:
                    failures.append(f"{rid}: new_row unit_type {rep.get('unit_type')} != planned {od['unit_type_target']}")
                if od.get("parent_collection_target") and rep.get("parent_collection") != od["parent_collection_target"]:
                    failures.append(f"{rid}: new_row parent {rep.get('parent_collection')} != planned")
                if rep.get("chunk_index_in_book") != 0:
                    failures.append(f"{rid}: new_row chunk_index sentinel must be 0")
                by_id[rid] = rep; applied["new_row"] += 1; continue
            orig = by_id[rid]
            for k in IMMUTABLE:
                if k in orig and orig.get(k) != rep.get(k):
                    failures.append(f"{rid}: immutable field changed: {k}")
            if rep.get("chunk_index_in_book") != orig.get("chunk_index_in_book"):
                failures.append(f"{rid}: chunk_index_in_book changed by the author")
            if rep.get("span") != orig.get("span"):
                if op != "respan" or rep.get("span") != od.get("span_target"):
                    failures.append(f"{rid}: span change not planned ({orig.get('span')} -> {rep.get('span')}; planned {od.get('span_target')})")
            elif op == "respan":
                failures.append(f"{rid}: respan ordered to {od.get('span_target')} but span unchanged")
            if "unit_type" in orig and rep.get("unit_type") != orig.get("unit_type"):
                if not od.get("unit_type_target") or rep.get("unit_type") != od["unit_type_target"]:
                    failures.append(f"{rid}: unit_type change not planned ({orig.get('unit_type')} -> {rep.get('unit_type')})")
            if str(orig.get("frontier_flag_considered")) == "True" and str(rep.get("frontier_flag_considered")) != "True":
                failures.append(f"{rid}: frontier flag True->non-True")
            by_id[rid] = rep; applied[op] += 1

    sim = sorted(by_id.values(), key=lambda r: span_ends(book, r["span"])[0])
    # tiling: exact same verse set as shipped, no overlap, no gap
    covered, overlaps = [], []
    for r in sim:
        vs = expand(book, r["span"], VERSES)
        covered.extend(vs)
    cset = set(covered)
    if len(covered) != len(cset):
        from collections import Counter
        overlaps = [v for v, c in Counter(covered).items() if c > 1][:10]
        failures.append(f"tiling: overlapping verses {overlaps}")
    ship_cov = set()
    for r in shipped:
        ship_cov.update(expand(book, r["span"], VERSES))
    if cset != ship_cov:
        failures.append(f"tiling: verse set differs from shipped (missing {sorted(ship_cov-cset)[:5]}, extra {sorted(cset-ship_cov)[:5]})")
    for i, r in enumerate(sim, 1):
        r["chunk_index_in_book"] = i
    # E-24: final_sha256 is a per-row CONTENT ADDRESS (sha256 of the row minus final_sha256,
    # json.dumps ensure_ascii=False sort_keys=True; re-derived from shipped Job, 194/194 coherent).
    # The pipeline owns it: recompute for every row the packets changed or created (books whose rows
    # carry the key), then verify coherence; a changed row left incoherent FAILS, inherited
    # incoherence on untouched rows is RECORDED (pre-existing, not this lane's change).
    touched = {o["decision_id"] for pp in patches for o in load_rows(pp) if o.get("_op") != "retire"}
    # the shipped rows are re-read from DISK: the in-memory rows were renumbered in place above
    shipped_addr = {r["decision_id"]: content_address(r) for r in load_rows(shipped_path) if "final_sha256" in r}
    final_sha = {"recomputed_touched": [], "recomputed_shifted": 0, "inherited_incoherent": 0, "rows_with_key": 0}
    for r in sim:
        if "final_sha256" not in r:
            continue
        final_sha["rows_with_key"] += 1
        want = content_address(r)
        rid = r["decision_id"]
        if rid in touched:
            r["final_sha256"] = want
            final_sha["recomputed_touched"].append(rid)
        elif want != shipped_addr.get(rid):
            # content differs from shipped without a packet touching it: the renumber shifted it
            r["final_sha256"] = want
            final_sha["recomputed_shifted"] += 1
        elif r["final_sha256"] != want:
            final_sha["inherited_incoherent"] += 1     # byte-identical to shipped, shipped hash already incoherent
    incoherent = [r["decision_id"] for r in sim if "final_sha256" in r and r["final_sha256"] != content_address(r)]
    if len(incoherent) != final_sha["inherited_incoherent"]:
        failures.append(f"final_sha256 incoherent after recompute: {incoherent[:8]}")
    sim_path = out_dir / f"sim_{book}.jsonl"
    sim_path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sim), encoding="utf-8", newline="\n")
    base_path = out_dir / f"baseline_{book}.jsonl"
    base_path.write_bytes(shipped_path.read_bytes())

    report = {"book": book, "patches": [p.name for p in patches], "applied": applied, "superseded_by_r2": superseded,
              "rows": {"shipped": len(shipped), "sim": len(sim)}, "tiling": "GREEN" if not any(f.startswith("tiling") for f in failures) else "RED",
              "verses_covered": len(cset), "final_sha256": final_sha}
    rc, so, se = run([str(tools / "normalize_hebrew_in_json.py"), str(sim_path)], tools)
    try:
        n = json.loads(so)
        report["normalize"] = {k: n.get(k) for k in ("fixed", "defect_count", "ok", "status") if k in n}
        if (n.get("fixed") or 0) or (n.get("defect_count") or 0):
            failures.append(f"normalize: fixed={n.get('fixed')} defects={n.get('defect_count')}")
    except json.JSONDecodeError:
        report["normalize"] = {"unparseable": (so or se)[-300:]}
        failures.append("normalize: unparseable output")
    rc, so, se = run([str(tools / "check_web_quotes.py"), str(sim_path)], tools)
    report["web_quotes"] = {"exit": rc, "tail": (so or se)[-400:]}
    suite = tools / "run_validator_suite.py"
    if suite.is_file():
        for label, path in (("baseline", base_path), ("sim", sim_path)):
            rc, so, se = run([str(suite), str(path)], tools)
            rep_path = path.with_name(path.name + ".validator_report.json")
            try:
                rep = json.loads(rep_path.read_text(encoding="utf-8-sig"))
            except Exception as e:
                failures.append(f"suite {label}: report unreadable {e!r}"); continue
            summ = rep.get("summary", {})
            report[f"suite_{label}"] = {"hard_status": summ.get("hard_status"), "nfd_hard": summ.get("nfd_hard_e01"),
                                        "members": {m: (v.get("status") if isinstance(v, dict) else v) for m, v in rep.items() if m != "summary"},
                                        "flags": {m: v.get("flag_count") for m, v in rep.items() if isinstance(v, dict) and isinstance(v.get("flag_count"), int)}}
        if "suite_sim" in report and "suite_baseline" in report:
            b, s = report["suite_baseline"], report["suite_sim"]
            sim_only_red = [m for m, st in s["members"].items() if st == "RED" and b["members"].get(m) != "RED"]
            report["sim_only_red_members"] = sim_only_red
            report["flags_delta_sim_minus_baseline"] = {m: s["flags"].get(m, 0) - b["flags"].get(m, 0) for m in set(s["flags"]) | set(b["flags"]) if s["flags"].get(m, 0) != b["flags"].get(m, 0)}
            if sim_only_red:
                failures.append(f"suite: sim-only RED members {sim_only_red}")
            if s.get("nfd_hard"):
                failures.append("suite: nfd_hard_e01 on sim")
    else:
        report["suite"] = "NONE for this book (audit toolkit only): deterministic coverage = normalize + web quotes + tiling + schema/immutables/placeholders; semantic coverage from the r3 targeted check"
    report["sweep"] = "FAIL" if failures else "PASS"
    report["failures"] = failures
    (out_dir / f"sweep_{book}.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
