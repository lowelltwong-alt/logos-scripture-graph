#!/usr/bin/env python3
"""CWO-wave landing census (Jer, m8-mesh-r3 + OW-1/OW-2/OW-3; E-18 execution parity) - run per slice
as each deliverable lands and again at wave close. Per slice: output parses per line; every op is
"replace"; every row is inside the slice's assignment, lands at most once; full 22-field schema with type
parity against rows_v2; decision_id == writer_decision_id; chunk_index_in_book, span, decision_id
UNCHANGED (hard); parent_collection/unit_type/confidence changes are FLAGS (dependent-field re-open must be
ordered); no unexpanded {placeholder}; register purge grep over prose fields (hard); every assigned row
carrying an EXACT-arm item must land (an omitted row may carry heuristic items only - reported for
reconciliation with the author's final-message dispositions); normalize dry-run fixed=0 defects=0;
CWO-1 re-check: ngram7 --gate 10 --full-ids over the pooled corpus (rows_v2 with this slice's rows replaced,
written to a PRIVATE temp dir) must list NONE of this slice's CWO-1 rows under any offending gram.
Digits are the tools' COUNTS. Usage: _cwo_census.py cwo01 [cwo02 ...]  (slice ids; default = all)"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
CWO = HERE / "cwo"
PY = sys.executable
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}")
REGISTER = re.compile(r"\b(peer|boss|reviewer|orchestrator|CWO-\d|B\d-\d+|rows_v2|orders_cwo|ngram7|collate\.py|sweep\.py|validator|erratum|repair(?:ed|s)?\b)", re.I)
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess", "wj_or_red_letter_considered")
HARD_IMMUTABLE = ("decision_id", "chunk_index_in_book", "span", "book", "model_id", "writer_part", "writer_decision_id", "writer_attempt_id")
FLAG_FIELDS = ("parent_collection", "unit_type", "confidence", "review_status")

corpus = {}
for line in open(HERE / "rows_v2.jsonl", encoding="utf-8"):
    if line.strip():
        r = json.loads(line)
        corpus[r["decision_id"]] = r
FIELDS = set(next(iter(corpus.values())).keys())
TYPES = {k: type(v) for k, v in next(iter(corpus.values())).items()}

ARGS = list(sys.argv[1:])
FULL_SIM = None
EXTRA = {}
if "--full-sim" in ARGS:
    i = ARGS.index("--full-sim"); FULL_SIM = Path(ARGS[i + 1]); ARGS = ARGS[:i] + ARGS[i + 2:]
if "--extra-layer" in ARGS:
    i = ARGS.index("--extra-layer")
    for l in Path(ARGS[i + 1]).read_text(encoding="utf-8-sig").splitlines():
        if l.strip():
            x = json.loads(l); EXTRA[x["decision_id"]] = {k: v for k, v in x.items() if k != "_op"}
    ARGS = ARGS[:i] + ARGS[i + 2:]
slices = sorted(p for p in CWO.glob("orders_cwo_[0-9][0-9].json"))
wanted = set(ARGS)
results, hard_fail = {}, False
census = {"slices": 0, "rows_ordered": 0, "rows_landed": 0, "rows_omitted_heuristic_only": 0, "flags": 0}
for f in slices:
    o = json.load(open(f, encoding="utf-8"))
    sl = o["agent"]
    if wanted and sl not in wanted:
        continue
    probs, flags = [], []
    out_path = HERE / o["output_file"]
    census["slices"] += 1
    census["rows_ordered"] += len(o["row_ids"])
    if not out_path.is_file():
        results[sl] = {"status": "ABSENT", "problems": ["output ABSENT"]}
        hard_fail = True
        continue
    landed = {}
    for i, line in enumerate(out_path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            probs.append(f"line {i}: unparseable ({e})"); continue
        rid = obj.get("decision_id")
        if obj.get("_op") != "replace":
            probs.append(f"line {i} ({rid}): op {obj.get('_op')!r} != replace")
        if rid in landed:
            probs.append(f"{rid}: appears more than once")
        landed[rid] = obj
        if rid not in o["row_ids"]:
            probs.append(f"{rid}: NOT in this slice's assignment"); continue
        keys = set(obj.keys()) - {"_op"}
        if keys != FIELDS:
            probs.append(f"{rid}: schema mismatch missing={sorted(FIELDS - keys)} extra={sorted(keys - FIELDS)}"); continue
        cur = corpus[rid]
        for k in FIELDS:
            if type(obj[k]) is not TYPES[k]:
                probs.append(f"{rid}.{k}: type {type(obj[k]).__name__} != {TYPES[k].__name__}")
        for k in HARD_IMMUTABLE:
            if obj[k] != cur[k]:
                probs.append(f"{rid}.{k}: IMMUTABLE field changed {cur[k]!r} -> {obj[k]!r}")
        for k in FLAG_FIELDS:
            if obj[k] != cur[k]:
                flags.append(f"{rid}.{k}: dependent field changed {cur[k]!r} -> {obj[k]!r} (must be ordered by an item)")
        for k in PROSE:
            v = obj[k]
            if isinstance(v, str):
                if PLACEHOLDER.search(v):
                    probs.append(f"{rid}.{k}: unexpanded placeholder {PLACEHOLDER.search(v).group(0)}")
                m = REGISTER.search(v)
                if m and not REGISTER.search(cur[k]):
                    probs.append(f"{rid}.{k}: register token introduced {m.group(0)!r}")
        if obj == {**cur, "_op": "replace"} or {k: obj[k] for k in FIELDS} == cur:
            flags.append(f"{rid}: emitted byte-identical to rows_v2 (no change)")
    omitted = [r for r in o["row_ids"] if r not in landed and r not in EXTRA]
    omitted_bad = [r for r in omitted if any(it["arm"] == "exact" for it in o["orders"][r]["items"])]
    if omitted_bad:
        probs.append(f"rows with EXACT-arm items not landed: {omitted_bad}")
    census["rows_landed"] += len([r for r in landed if r in o["row_ids"]])
    census["rows_omitted_heuristic_only"] += len(omitted) - len(omitted_bad)
    norm = subprocess.run([PY, str(TOOLS / "normalize_hebrew_in_json.py"), str(out_path)], capture_output=True, text=True, encoding="utf-8", cwd=str(TOOLS))
    try:
        nout = json.loads(norm.stdout)
        if nout.get("fixed", 0) or nout.get("defect_count", 0):
            probs.append(f"nfd: fixed={nout.get('fixed')} defects={nout.get('defect_count')}")
    except json.JSONDecodeError:
        probs.append(f"normalize unparseable: {norm.stdout[-200:]} {norm.stderr[-200:]}")
    # CWO-1 pooled re-check (private temp dir; never under SP)
    cwo1_rows = [r for r in o["row_ids"] if any(it["cwo"] == "CWO-1" for it in o["orders"][r]["items"])]
    ng_summary = None
    if cwo1_rows:
        with tempfile.TemporaryDirectory(prefix="cwo_census_") as td:
            sim = Path(td) / "sim.jsonl"
            if FULL_SIM is not None:
                sim = FULL_SIM   # wave close: pool every slice against the FULL revised corpus (all slices + layers)
            else:
              with open(sim, "w", encoding="utf-8", newline="\n") as fh:
                for rid, row in corpus.items():
                    use = {k: landed[rid][k] for k in FIELDS} if rid in landed and rid in o["row_ids"] else row
                    if rid in EXTRA and rid in o["row_ids"]: use = EXTRA[rid]
                    fh.write(json.dumps(use, ensure_ascii=False) + "\n")
            ng = subprocess.run([PY, str(TOOLS / "ngram7.py"), str(sim), "--gate", "10", "--full-ids"], capture_output=True, text=True, encoding="utf-8", cwd=str(TOOLS))
            try:
                ngj = json.loads(ng.stdout)
                still = {}
                for g in ngj.get("offending_7grams", []):
                    hit = sorted(set(g.get("row_ids", [])) & set(cwo1_rows))
                    if hit:
                        still[g["gram"]] = hit
                ng_summary = {"offending_grams_corpuswide": len(ngj.get("offending_7grams", [])), "slice_cwo1_rows": len(cwo1_rows), "slice_rows_still_under_a_gram": still}
                if still:
                    probs.append(f"CWO-1: {len(still)} listed gram(s) still cover this slice's rows: {still}")
            except json.JSONDecodeError:
                probs.append(f"ngram7 unparseable: {ng.stdout[-200:]} {ng.stderr[-200:]}")
    status = "PASS" if not probs else "FAIL"
    hard_fail = hard_fail or bool(probs)
    census["flags"] += len(flags)
    results[sl] = {"status": status, "problems": probs, "flags": flags, "rows_ordered": len(o["row_ids"]), "rows_landed": len(landed),
                   "omitted": omitted, "cwo1_check": ng_summary, "output_sha256": __import__("hashlib").sha256(out_path.read_bytes()).hexdigest()}
print(json.dumps({"census_status": "FAIL" if hard_fail else "PASS", "census": census, "results": results}, ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
