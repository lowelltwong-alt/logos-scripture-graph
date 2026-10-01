#!/usr/bin/env python3
"""CWO-wave landing census (Lam, m8-mesh-r3 + OW-1/OW-2/OW-3/OW-5; E-18 execution parity) - run per slice as each
deliverable lands and again at wave close. Per slice: output parses per line; every op is "replace"; every row is
inside the slice's assignment, lands at most once; full 22-field schema with type parity against the base corpus;
decision_id == writer_decision_id; HARD-immutable fields unchanged (decision_id, chunk_index_in_book, span, book,
model_id, writer_*, parent_collection, unit_type, review_status); confidence / frontier_flag_considered changes are
listed (admitted only under CWO-12, downward / False->True - the apply guard enforces the direction); no unexpanded
{placeholder}; register purge grep over prose fields (hard); every assigned row carrying an EXACT-arm item must land
(an omitted row may carry heuristic items only - reported for reconciliation with the author's final-message
dispositions, read from --finals when given); normalize dry-run fixed=0 defects=0. The 7-gram gate and the validator
suite run over the pooled simulation in _wave_repair_sweep.py (--base). Digits are the tools' COUNTS.
Usage: _cwo_census.py --base rows_v2.jsonl [cwo01 cwo02 ...] [--finals <_lam_cwo_final_msgs.json>]"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
CWO = HERE / "cwo"
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}")
REGISTER = re.compile(r"\b(peer|boss|reviewer|orchestrator|CWO-\d+|B\d-\d+|rows_v\d|orders_cwo|ngram7|collate\.py|sweep\.py|validator|erratum|scan evidence|the scan)\b", re.I)
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess", "wj_or_red_letter_considered")
HARD_IMMUTABLE = ("decision_id", "chunk_index_in_book", "span", "book", "model_id", "writer_part", "writer_decision_id", "writer_attempt_id", "parent_collection", "unit_type", "review_status")
FLAG_FIELDS = ("confidence", "frontier_flag_considered")

A = list(sys.argv[1:])
BASE = A[A.index("--base") + 1] if "--base" in A else "rows_v2.jsonl"
FINALS = A[A.index("--finals") + 1] if "--finals" in A else None
for flag in ("--base", "--finals"):
    if flag in A:
        i = A.index(flag); A = A[:i] + A[i + 2:]
corpus = {}
for line in open(HERE / BASE, encoding="utf-8-sig"):
    if line.strip():
        r = json.loads(line); corpus[r["decision_id"]] = r
FIELDS = set(next(iter(corpus.values())).keys())
TYPES = {k: type(v) for k, v in next(iter(corpus.values())).items()}
finals = json.load(open(FINALS, encoding="utf-8")) if FINALS else {}
slices = A or sorted(p.stem.replace("orders_", "").replace("cwo_", "cwo") for p in CWO.glob("orders_cwo_[0-9][0-9].json"))
results, hard_fail = {}, False
census = {"slices": 0, "rows_landed": 0, "rows_changed": 0, "exact_rows_missing": 0, "heuristic_only_omitted": 0, "confidence_changes": 0, "frontier_flag_changes": 0}
for sl in slices:
    n = sl.replace("cwo", "")
    plan = json.load(open(CWO / f"orders_cwo_{n}.json", encoding="utf-8"))
    out_path = HERE / plan["output_file"]
    probs, flags = [], []
    if not out_path.exists():
        results[sl] = {"status": "FAIL", "problems": ["output MISSING"]}; hard_fail = True; continue
    exact_rows = {rid for rid in plan["row_ids"] if any(it["arm"] == "exact" for it in plan["orders"][rid]["items"])}
    landed, changed = {}, {}
    for i, line in enumerate(out_path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            probs.append(f"line {i}: unparseable ({e})"); continue
        rid = obj.get("decision_id")
        if obj.get("_op") != "replace":
            probs.append(f"{rid}: op {obj.get('_op')!r} != replace"); continue
        if rid in landed:
            probs.append(f"{rid}: appears more than once")
        landed[rid] = obj
        if rid not in plan["row_ids"]:
            probs.append(f"{rid}: NOT in this slice's assignment"); continue
        body = {k: v for k, v in obj.items() if k != "_op"}
        missing = FIELDS - set(body); extra = set(body) - FIELDS
        if missing: probs.append(f"{rid}: missing fields {sorted(missing)}")
        if extra: probs.append(f"{rid}: extra fields {sorted(extra)}")
        for k, v in body.items():
            if k in TYPES and type(v) is not TYPES[k]:
                probs.append(f"{rid}: field {k} type {type(v).__name__} != {TYPES[k].__name__}")
        if body.get("decision_id") != body.get("writer_decision_id"):
            probs.append(f"{rid}: decision_id != writer_decision_id")
        if PLACEHOLDER.search(json.dumps(body, ensure_ascii=False)):
            probs.append(f"{rid}: unexpanded placeholder token")
        cur = corpus.get(rid)
        if cur is None:
            probs.append(f"{rid}: not in the base corpus"); continue
        for k in HARD_IMMUTABLE:
            if body.get(k) != cur.get(k):
                probs.append(f"{rid}: hard-immutable {k} changed {cur.get(k)!r} -> {body.get(k)!r}")
        for k in FLAG_FIELDS:
            if body.get(k) != cur.get(k):
                flags.append(f"{rid}: {k} {cur.get(k)!r} -> {body.get(k)!r}")
                census["confidence_changes" if k == "confidence" else "frontier_flag_changes"] += 1
        for f in PROSE:
            v = body.get(f, "")
            if isinstance(v, str):
                m = REGISTER.search(v)
                if m and not REGISTER.search(cur.get(f, "") or ""):
                    probs.append(f"{rid}: register token {m.group(0)!r} INTRODUCED in {f}")
        ch = [k for k in cur if json.dumps(body.get(k), ensure_ascii=False, sort_keys=True) != json.dumps(cur.get(k), ensure_ascii=False, sort_keys=True)]
        changed[rid] = ch
    not_landed = [rid for rid in plan["row_ids"] if rid not in landed]
    missing_exact = sorted(r for r in not_landed if r in exact_rows)
    if missing_exact:
        probs.append(f"EXACT-arm rows not landed: {missing_exact}")
    heur_omitted = sorted(r for r in not_landed if r not in exact_rows)
    fm = finals.get(plan["attempt_id"], {})
    disp = {}
    for it in fm.get("items", []):
        disp.setdefault(it.get("row"), []).append(f"{it.get('cwo')}:{it.get('action')}")
    for r in heur_omitted:
        if fm and r not in disp:
            flags.append(f"{r}: heuristic-only row omitted with NO disposition in the final message")
    unchanged = sorted(r for r, c in changed.items() if not c)
    if unchanged:
        flags.append(f"byte-identical replace rows: {unchanged}")
    norm = subprocess.run([sys.executable, str(TOOLS / "normalize_hebrew_in_json.py"), str(out_path)], capture_output=True, text=True, encoding="utf-8")
    try:
        nout = json.loads(norm.stdout)
        if nout.get("fixed", 0) or nout.get("defect_count", 0):
            probs.append(f"nfd: fixed={nout.get('fixed')} defects={nout.get('defect_count')}")
    except json.JSONDecodeError:
        probs.append(f"normalize unparseable: {norm.stdout[-200:]} {norm.stderr[-200:]}")
    status = "PASS" if not probs else "FAIL"
    hard_fail |= bool(probs)
    results[sl] = {"status": status, "attempt_id": plan["attempt_id"], "assigned": len(plan["row_ids"]), "landed": len(landed), "changed": sum(1 for c in changed.values() if c),
                   "exact_rows": sorted(exact_rows), "heuristic_only_omitted": heur_omitted, "changed_fields_histogram": {f: sum(1 for c in changed.values() if f in c) for f in sorted({x for c in changed.values() for x in c})},
                   "dispositions_by_row": disp, "problems": probs, "flags": flags}
    census["slices"] += 1; census["rows_landed"] += len(landed); census["rows_changed"] += sum(1 for c in changed.values() if c)
    census["exact_rows_missing"] += len(missing_exact); census["heuristic_only_omitted"] += len(heur_omitted)
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps({"base": BASE, "census_status": "FAIL" if hard_fail else "PASS", "census": census, "results": results}, ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
