#!/usr/bin/env python3
"""CWO execution parity for Daniel's close: one record, bound to ONE corpus sha256, showing that every corpus-wide order
(CWO-DAN-01..04, controlling ruling E1 as E2 amended it) still holds over the bytes that will be assembled (E-18, close-gate
item 5). It is the Daniel form of Ezekiel's `cwo/cwo_parity.<corpus-stem>.json` (post_corpus_sha256 equal,
exact_arm_residual empty, status GREEN).

WHAT EACH CWO GETS
  01, 02, 04  cwo/cwo_sweep_dan.py, re-run over the corpus. Its predicates and field scopes are READ from ruling E1, never
              retyped. Zero hits required.
  03          The same sweep, then cwo/cwo03_dispose.py (zone precedence). Zero zone hits required (E2). Every other hit
              keeps its disposition class and is counted, never suppressed. The suite's language_zones member, to which
              E12 ties this order, is read from the corpus's own validator report as a second witness.
  01 again    The suite's placeholders member (ruling S1-02) is read from the same report as a second witness.

SUPPLEMENTARY, NOT AN ORDER. The id arm of CWO-DAN-02 matches a one-digit part number only (W1-001 .. W9-999). Daniel has a
part W10. This tool also counts a widened arm (one or two digits) over the same fields and reports it beside the order.
The widened arm is this tool's own measure, not the ruling's predicate; a hit there is reported as a FINDING and sets
status FINDING, because a row id in prose is the defect the order names.

NEVER OVERWRITES. An existing output with the same bytes is left in place; if its bytes differ, the tool refuses.
Usage: _cwo_parity_dan.py [--check]      (--check: recompute and compare with the installed record, write nothing)
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
DAN = Path(__file__).resolve().parent
CORPUS = "rows_v1_final.jsonl"
STEM = CORPUS.replace(".jsonl", "")
CWO = DAN / "cwo"
COV = CWO / ("coverage_" + STEM)
REC = CWO / ("cwo_parity.%s.json" % STEM)
SUITE = DAN / (CORPUS + ".validator_report.json")
TOOLS = ("cwo_sweep_dan.py", "cwo03_dispose.py")
E1 = DAN / "review" / "dan_controlling_agent_rulings_E1.v1.json"
E2 = DAN / "review" / "dan_controlling_agent_rulings_E2.v1.json"
E12 = DAN / "review" / "dan_controlling_agent_rulings_E12.v1.json"
CWO02_FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals",
                "literature_type_guess", "boundary_evidence_refs")
WIDE_ID = re.compile(r"\bW\d{1,2}-\d{3}\b")
CR, LF = b"\r", b"\n"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(o):
    return (json.dumps(o, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def strs(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from strs(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from strs(x)


def lf(p):
    return Path(p).read_bytes().replace(CR + LF, LF)


def compute(tmp):
    corpus = DAN / CORPUS
    csha = sha(corpus)
    sweep_p, disp_p = tmp / "cwo_sweep.json", tmp / "cwo03_dispositions.json"
    for cmd in ([CWO / TOOLS[0], CORPUS, "--out", sweep_p], [CWO / TOOLS[1], sweep_p, disp_p]):
        r = subprocess.run([sys.executable, "-B"] + [str(c) for c in cmd], capture_output=True, cwd=str(DAN))
        if r.returncode != 0:
            raise SystemExit("REFUSED: %s exit %d: %s" % (Path(cmd[0]).name, r.returncode, r.stderr.decode("utf-8", "replace")[-400:]))
    sweep_b, disp_b = lf(sweep_p), lf(disp_p)
    sweep, disp = json.loads(sweep_b.decode("utf-8")), json.loads(disp_b.decode("utf-8"))
    if CR in SUITE.read_bytes() or CR in corpus.read_bytes():  # E-73: a digest is recorded on LF bytes only
        raise SystemExit("REFUSED: CR byte in the corpus or its validator report; convert to LF before recording a digest")
    suite = json.loads(SUITE.read_bytes().decode("utf-8"))
    rows = [json.loads(x) for x in corpus.read_bytes().decode("utf-8").splitlines() if x.strip()]
    wide = []
    for r in rows:
        for f in CWO02_FIELDS:
            for s in strs(r.get(f)):
                for m in WIDE_ID.finditer(s):
                    wide.append({"row": r["writer_decision_id"], "field": f, "match": m.group(0)})
    orders = sweep["orders"]
    zone = [h for h in disp["hits"] if h.get("disposition") == "zone"]
    lz, ph = suite.get("language_zones", {}), suite.get("placeholders", {})
    parity, residual = {}, []
    for k in ("CWO-DAN-01", "CWO-DAN-02", "CWO-DAN-04"):
        hits = orders[k].get("hits") or []
        n = orders[k]["hit_count"]
        parity[k] = {"arm": "exact", "method": "cwo/cwo_sweep_dan.py over the corpus; predicate and fields read from ruling E1",
                     "status": "COVERED" if n == 0 else "RESIDUAL", "residual_count": n, "tier": "MEASURED"}
        if n:
            residual.append({"order": k, "hits": hits if isinstance(hits, list) else n})
    parity["CWO-DAN-03"] = {
        "arm": "exact on the zone class; every other class counted",
        "method": "cwo/cwo_sweep_dan.py then cwo/cwo03_dispose.py (zone precedence); E2: zone hits must be 0",
        "status": "COVERED" if not zone else "RESIDUAL", "hit_count": orders["CWO-DAN-03"]["hit_count"],
        "counts_by_disposition": disp["counts"], "residual_count": len(zone), "tier": "MEASURED",
        "disposition_tier": "the class of each hit is the aid tool's mechanical proposal; verse-only hits are listed in the "
                            "dispositions record for reading against the row's range (INFERRED, not a hand reading)"}
    if zone:
        residual.append({"order": "CWO-DAN-03", "hits": zone})
    second = {"placeholders_member": {"status": ph.get("status"), "flag_count": ph.get("flag_count"), "order": "CWO-DAN-01"},
              "language_zones_member": {"status": lz.get("status"), "flag_count": lz.get("flag_count"), "order": "CWO-DAN-03 (E12)"}}
    second_ok = ph.get("status") == "GREEN" and lz.get("status") == "GREEN" and not lz.get("flag_count")
    ok = (not residual and sweep["rows"] == len(rows) == 75 and sweep["rows_sha256"] == csha and second_ok
          and suite.get("rows_file") == CORPUS and suite["summary"]["hard_status"] == "GREEN")
    rec = {
        "schema": "dan_cwo_parity.v1", "book": "Dan", "post_corpus": CORPUS, "post_corpus_sha256": csha, "rows": len(rows),
        "suite_report": {"path": SUITE.name, "sha256": sha(SUITE), "hard_status": suite["summary"]["hard_status"],
                         "binding": "the report names the rows file, not its digest; it was written by the suite run over this corpus "
                                    "and is re-read here (REPORTED by the suite, digest MEASURED here)"},
        "parity": parity, "second_witnesses": second, "exact_arm_residual": residual, "routed_open": [],
        "supplementary_widened_id_arm": {"pattern": WIDE_ID.pattern, "fields": list(CWO02_FIELDS), "hit_count": len(wide), "hits": wide,
                                         "note": "not the ruling's predicate; this tool's own measure (see the docstring)"},
        "status": "GREEN" if ok and not wide else ("FINDING" if ok else "RED"),
        "tools": {t: sha(CWO / t) for t in TOOLS},
        "rulings": {p.name: sha(p) for p in (E1, E2, E12)},
        "side_records": {"cwo_sweep.json": hashlib.sha256(sweep_b).hexdigest(),
                         "cwo03_dispositions.json": hashlib.sha256(disp_b).hexdigest()},
        "coverage_dir": "cwo/coverage_%s/" % STEM,
        "law": "E-18: every corpus-wide order checked again as its own sweep over the corpus being closed",
        "limits": ["CWO-DAN-03's non-zone classes are a mechanical proposal, not a hand reading of each hit.",
                   "The id arm of CWO-DAN-02 as ruled matches a one-digit part only; the widened arm is reported separately.",
                   "The suite members are second witnesses read from the report, not re-run here."],
    }
    return rec, {"cwo_sweep.json": sweep_b, "cwo03_dispositions.json": disp_b}


def install(p, b):
    if CR in b:
        raise SystemExit("REFUSED: CR byte in %s" % p.name)
    if p.exists():
        if p.read_bytes() != b:
            raise SystemExit("REFUSED: %s exists with different bytes" % p)
        return "kept"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b)
    return "written"


def main():
    with tempfile.TemporaryDirectory() as t:
        rec, side = compute(Path(t))
    b = dump(rec)
    if "--check" in sys.argv:
        same = REC.exists() and REC.read_bytes() == b and all((COV / n).exists() and (COV / n).read_bytes() == sb for n, sb in side.items())
        print(json.dumps({"check": "MATCH" if same else "DIFFERS", "status": rec["status"], "record_sha256": hashlib.sha256(b).hexdigest()}))
        return 0 if same and rec["status"] == "GREEN" else 1
    acts = {n: install(COV / n, sb) for n, sb in side.items()}
    acts[REC.name] = install(REC, b)
    print(json.dumps({"status": rec["status"], "post_corpus_sha256": rec["post_corpus_sha256"],
                      "residual": len(rec["exact_arm_residual"]), "cwo03": rec["parity"]["CWO-DAN-03"]["counts_by_disposition"],
                      "widened_id_hits": rec["supplementary_widened_id_arm"]["hit_count"], "installed": acts,
                      "record_sha256": hashlib.sha256(b).hexdigest()}, ensure_ascii=False))
    return 0 if rec["status"] == "GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
