#!/usr/bin/env python3
"""Micro-round landing census (Jer, m8-mesh-r3 + OW-1/OW-2/OW-3/OW-5) - run per slice as each deliverable lands
and again at round close. Base corpus rows_v3.jsonl (sha16 pinned). Per slice: output parses per line; every op is
"replace"; every row is inside the slice's assignment, lands exactly once (every ordered row must land - the micro
round has no heuristic-only rows); full schema with type parity against rows_v3; IMMUTABLE fields byte-equal
(the _apply_micro.py set: decision_id, book, model_id, chunk_index_in_book, span, parent_collection, unit_type,
confidence, writer_*, non_authorizing, wj_or_red_letter_considered, frontier_flag_considered); every changed field
inside the micro-open set; no unexpanded {placeholder}; register tokens INTRODUCED into prose fields (hard);
normalize dry-run fixed=0 defects=0; 7-gram gate: ngram7 --gate 10 --full-ids over the pooled corpus (rows_v3 with
this slice's rows replaced, written to a PRIVATE temp dir) must list NONE of this slice's rows under any offending
gram (with --full-sim <file> at round close: pool every slice). Digits are the tools' COUNTS.
Usage: _micro_census.py [m01 m02 ...] [--full-sim <sim.jsonl>] [--finals <_micro_final_msgs.json>]   (slice ids; default = all;
with --finals a byte-identical row whose every ordered item the author REPORTED is a flag, not a failure)"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
SPOT = HERE / "spot"
PY = sys.executable
PIN = "bd04e0b572b3d1b0"
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}")
REGISTER = re.compile(r"\b(peer|boss|reviewer|orchestrator|spot wave|spot reviewer|micro round|micro author|S[1-7]-\d+|CWO-\d+|B\d-\d+|rows_v[0-9]|orders_micro|orders_cwo|ngram7|collate\.py|sweep\.py|validator|erratum|proposed cure|repair(?:ed|s)?)\b", re.I)
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess", "wj_or_red_letter_considered")
IMMUTABLE = ("decision_id", "book", "model_id", "chunk_index_in_book", "span", "parent_collection", "unit_type", "confidence",
             "writer_part", "writer_decision_id", "writer_attempt_id", "non_authorizing", "wj_or_red_letter_considered", "frontier_flag_considered")
OPEN = {"boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals", "boundary_evidence_refs",
        "literature_type_guess", "strong_or_hebrew_tags_used", "review_status"}

raw = (HERE / "rows_v3.jsonl").read_bytes()
sha16 = hashlib.sha256(raw).hexdigest()[:16]
assert sha16 == PIN, f"rows_v3 sha {sha16} != pinned {PIN}"
corpus = {}
for line in raw.decode("utf-8").splitlines():
    if line.strip():
        r = json.loads(line)
        corpus[r["decision_id"]] = r
FIELDS = set(next(iter(corpus.values())).keys())
TYPES = {k: type(v) for k, v in next(iter(corpus.values())).items()}

ARGS = list(sys.argv[1:])
FULL_SIM = None
if "--full-sim" in ARGS:
    i = ARGS.index("--full-sim"); FULL_SIM = Path(ARGS[i + 1]); ARGS = ARGS[:i] + ARGS[i + 2:]
FINALS = {}
if "--finals" in ARGS:
    i = ARGS.index("--finals"); FINALS = json.loads(Path(ARGS[i + 1]).read_text(encoding="utf-8-sig")); ARGS = ARGS[:i] + ARGS[i + 2:]
slices = sorted(SPOT.glob("orders_micro_[0-9][0-9].json"))
wanted = set(ARGS)
results, hard_fail = {}, False
census = {"slices": 0, "rows_ordered": 0, "rows_landed": 0, "rows_omitted": 0, "rows_changed": 0, "changed_fields_histogram": {}}
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
        for k in IMMUTABLE:
            if obj[k] != cur[k]:
                probs.append(f"{rid}.{k}: IMMUTABLE field changed {cur[k]!r} -> {obj[k]!r}")
        changed = [k for k in FIELDS if json.dumps(obj[k], ensure_ascii=False, sort_keys=True) != json.dumps(cur[k], ensure_ascii=False, sort_keys=True)]
        oos = [k for k in changed if k not in OPEN and k not in IMMUTABLE]
        if oos:
            probs.append(f"{rid}: changed fields outside the micro-open set: {oos}")
        if changed:
            census["rows_changed"] += 1
            for k in changed:
                census["changed_fields_histogram"][k] = census["changed_fields_histogram"].get(k, 0) + 1
        else:
            acts = [it.get("action") for it in FINALS.get(o["attempt_id"], {}).get("items", []) if it.get("row") == rid]
            if acts and all(a == "reported" for a in acts):
                flags.append(f"{rid}: emitted byte-identical to rows_v3 - every ordered item on this row REPORTED by the author ({len(acts)}); reviewed by the postcheck")
            else:
                probs.append(f"{rid}: emitted byte-identical to rows_v3 (no cure installed; author items on this row: {acts or 'none given'}; every ordered finding must be cured or reported)")
        if PLACEHOLDER.search(json.dumps({k: obj[k] for k in FIELDS}, ensure_ascii=False)):
            probs.append(f"{rid}: unexpanded placeholder")
        for k in PROSE:
            v = obj[k]
            if isinstance(v, str):
                m = REGISTER.search(v)
                if m and not REGISTER.search(cur[k]):
                    probs.append(f"{rid}.{k}: register token introduced {m.group(0)!r}")
    omitted = [r for r in o["row_ids"] if r not in landed]
    if omitted:
        probs.append(f"ordered rows not landed: {omitted}")
    census["rows_landed"] += len([r for r in landed if r in o["row_ids"]])
    census["rows_omitted"] += len(omitted)
    norm = subprocess.run([PY, str(TOOLS / "normalize_hebrew_in_json.py"), str(out_path)], capture_output=True, text=True, encoding="utf-8", cwd=str(TOOLS))
    try:
        nout = json.loads(norm.stdout)
        if nout.get("fixed", 0) or nout.get("defect_count", 0):
            probs.append(f"nfd: fixed={nout.get('fixed')} defects={nout.get('defect_count')}")
    except json.JSONDecodeError:
        probs.append(f"normalize unparseable: {norm.stdout[-200:]} {norm.stderr[-200:]}")
    ng_summary = None
    with tempfile.TemporaryDirectory(prefix="micro_census_") as td:
        sim = Path(td) / "sim.jsonl"
        if FULL_SIM is not None:
            sim = FULL_SIM
        else:
            with open(sim, "w", encoding="utf-8", newline="\n") as fh:
                for rid, row in corpus.items():
                    use = {k: landed[rid][k] for k in FIELDS} if rid in landed and rid in o["row_ids"] and set(landed[rid]) - {"_op"} == FIELDS else row
                    fh.write(json.dumps(use, ensure_ascii=False) + "\n")
        ng = subprocess.run([PY, str(TOOLS / "ngram7.py"), str(sim), "--gate", "10", "--full-ids"], capture_output=True, text=True, encoding="utf-8", cwd=str(TOOLS))
        try:
            ngj = json.loads(ng.stdout)
            still = {}
            for g in ngj.get("offending_7grams", []):
                hit = sorted(set(g.get("row_ids", [])) & set(o["row_ids"]))
                if hit:
                    still[g["gram"]] = hit
            ng_summary = {"offending_grams_corpuswide": len(ngj.get("offending_7grams", [])), "slice_rows": len(o["row_ids"]), "slice_rows_under_a_gram": still}
            if still:
                probs.append(f"7-gram gate: {len(still)} listed gram(s) cover this slice's rows: {still}")
        except json.JSONDecodeError:
            probs.append(f"ngram7 unparseable: {ng.stdout[-200:]} {ng.stderr[-200:]}")
    status = "PASS" if not probs else "FAIL"
    hard_fail = hard_fail or bool(probs)
    results[sl] = {"status": status, "problems": probs, "flags": flags, "rows_ordered": len(o["row_ids"]), "rows_landed": len(landed), "omitted": omitted,
                   "ngram7_check": ng_summary, "output_sha256": hashlib.sha256(out_path.read_bytes()).hexdigest()}
print(json.dumps({"census_status": "FAIL" if hard_fail else "PASS", "base": "rows_v3.jsonl", "base_sha16": sha16, "census": census, "results": results}, ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
