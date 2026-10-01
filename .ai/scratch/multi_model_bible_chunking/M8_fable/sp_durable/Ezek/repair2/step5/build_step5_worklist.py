#!/usr/bin/env python3
"""REPAIR-2 step-5 WORKLIST: the register prose pass (#e15 Q9(c)), built from data, never from a summary.

#e15 Q9(c) orders author work over: the row-instances the spot lanes listed, every instance the three register arms
surface, and the five sentences E13-86 repaired for grammar only - each field rewritten to state the substance, READ
BACK AS ENGLISH, register member before and after. E13-86 adds that the orchestrator's own register substitution
edited fields nobody read back. So the worklist has six sources, each read from its record:

  REG       register flags on the rows at build time, per row and field, flags carried as data
  READBACK  prose fields changed by the orchestrator's register repair, substitution-residue and grammar sweeps,
            measured by diffing each sweep's pre-image backup against its post-image (the next sweep's pre-image, or
            the live rows), with every post-image digest checked against the sweep receipt before it is trusted
  SPOT      the spot lanes' REGISTER cross-row pattern rows and their non-OK register-type checklist findings
  ROUTED    entries the step-3 and step-4c adjudications routed to step 5, verbatim
  NEARFAR   the step-4c lanes' observation that some rejected-alternative prose uses near/far in the older sense -
            carried only where the step-4c adjudication did not already route it
  WEBQ      web_quotes member flags on the rows at build time (quotation case or apostrophe mismatches)

Nothing here decides a rewrite. Items are orders-as-data for two blind author lanes and a Fable adjudicator.

usage: python build_step5_worklist.py [--probe]
  --probe  build before the step-4c adjudication has landed; writes to the scratch probe path, never the durable one
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sys.path.insert(0, str(EZ / "repair2" / "step2_reconciliation"))
import check_candidate_v2 as V2                                                # noqa: E402

PROBE = "--probe" in sys.argv
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_probe")
OUT = (SCR if PROBE else HERE) / "step5_worklist.v1.json"
WORK = (SCR if PROBE else HERE) / "_build_work"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
PID = re.compile(r"P\d\d-\d\d\d")
READBACK_SWEEPS = ("author_wave_register_repair", "author_wave_substitution_residue", "author_wave_grammar_repair")
ADJ4C = EZ / "author" / "repair2_step4c" / "adjudication" / "adjudication.json"


def load(p):
    return {r["decision_id"]: r for r in (json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip())}


rows = load(ROWS)
items = []


def add(cls, row, fields, data, source):
    if row not in rows:
        raise SystemExit("REFUSED: %s item names a row the corpus does not carry: %r (source %s)" % (cls, row, source))
    items.append({"id": None, "class": cls, "row": row, "fields_hint": sorted(fields), "data": data,
                  "source": source, "status": "PENDING"})


# REG
reg_total = 0
for rid, r in sorted(rows.items()):
    by_field = {}
    for f in V2.CR.scan_row(r, "c"):
        by_field.setdefault(f["field"], []).append({k: f[k] for k in ("class", "match", "context")})
    for field, fl in sorted(by_field.items()):
        reg_total += len(fl)
        add("REG", rid, [field], {"register_flags": fl}, "check_register on the rows at build time")

# READBACK
recs = [json.loads(l) for l in (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
for i, rec in enumerate(recs):
    if rec.get("sweep") not in READBACK_SWEEPS:
        continue
    pre = EZ / "repair" / rec["preimage_backup"]
    post = (EZ / "repair" / recs[i + 1]["preimage_backup"]) if i + 1 < len(recs) else None
    if post is None or sha(post) != rec["postimage_sha256_measured_from_disk"]:
        raise SystemExit("REFUSED: the post-image of sweep %s does not match its receipt; no diff is trusted" % rec["sweep"])
    if sha(pre) != rec["preimage_sha256"]:
        raise SystemExit("REFUSED: the pre-image backup of sweep %s does not match its receipt" % rec["sweep"])
    a, b = load(pre), load(post)
    changed = [(rid, f) for rid in sorted(b) for f in PROSE if a.get(rid, {}).get(f) != b[rid].get(f)]
    if len(changed) < 1 or len({c[0] for c in changed}) != rec["rows_touched"]:
        raise SystemExit("REFUSED: sweep %s diff finds %d rows; its receipt says %s" % (rec["sweep"], len({c[0] for c in changed}), rec["rows_touched"]))
    for rid, f in changed:
        add("READBACK", rid, [f], {"sweep": rec["sweep"], "field_was_edited_by": rec.get("whose_defect") or "the orchestrator",
                                   "what_the_sweep_was": rec.get("what_this_was")}, "sweep receipt + backup diff")

# SPOT
for n in ("s01", "s02", "s03"):
    p = EZ / "reviews" / "spot" / ("ezek_spot_%s_findings.json" % n)
    s = json.loads(p.read_text(encoding="utf-8"))
    for pat in s.get("cross_row_patterns") or []:
        if str(pat.get("pattern", "")).upper().startswith("REGISTER"):
            for rid in pat.get("rows") or []:
                add("SPOT", rid, PROSE[:3], {"lane": n, "pattern": pat["pattern"], "detail": pat.get("detail")}, str(p.relative_to(EZ)))
    for rid, v in (s.get("per_row") or {}).items():
        for k, c in (v.get("checklist") or {}).items():
            if isinstance(c, dict) and c.get("verdict") != "OK" and re.search(r"(?i)regist|§8|section 8|narrat|barred", json.dumps(c, ensure_ascii=False)):
                add("SPOT", rid, PROSE[:3], {"lane": n, "checklist_item": k, "finding": c}, str(p.relative_to(EZ)))

# ROUTED
adj3 = json.loads((EZ / "repair2" / "step3" / "adjudication_a1" / "adjudication.json").read_text(encoding="utf-8"))
for e in adj3["routed"]:
    if "step 5" in str(e.get("to", "")).lower():
        for rid in sorted(set(PID.findall(str(e.get("row", ""))))):
            add("ROUTED", rid, PROSE[:3], {"from_adjudication": "step 3", "entry": e}, "repair2/step3/adjudication_a1/adjudication.json")
routed_4c_rows = set()
if ADJ4C.is_file():
    adj4 = json.loads(ADJ4C.read_text(encoding="utf-8"))
    for e in adj4.get("routed") or []:
        t = json.dumps(e, ensure_ascii=False)
        if re.search(r"(?i)step[ -]?5|prose pass|register", t):
            for rid in sorted(set(PID.findall(t))):
                routed_4c_rows.add(rid)
                add("ROUTED", rid, PROSE[:3], {"from_adjudication": "step 4c", "entry": e}, str(ADJ4C.relative_to(EZ)))
elif not PROBE:
    raise SystemExit("REFUSED: the step-4c adjudication has not landed at %s; build with --probe only" % ADJ4C)

# NEARFAR (lane observations; only where step 4c's adjudication did not route the row)
la = json.loads((EZ / "author" / "repair2_step4c" / "lane_a" / "discharge.json").read_text(encoding="utf-8"))
lb = json.loads((EZ / "author" / "repair2_step4c" / "lane_b" / "discharge.json").read_text(encoding="utf-8"))
obs = [o for o in la.get("observations_for_the_adjudicator") or [] if "NEAR/FAR" in o] + \
      [lb.get("class_findings", {}).get("prose_near_far_usage", "")]
for rid in sorted({x for o in obs for x in PID.findall(o)} - routed_4c_rows):
    add("NEARFAR", rid, ["strongest_rejected_alternative"], {"observations": obs,
        "rule": "clause 6 v2: for a rival, near is the candidate onset verse and far the verse behind it"},
        "author/repair2_step4c/lane_{a,b}/discharge.json (lane observations, not adjudicated)")

# WEBQ - the suite member on a copy of the rows
WORK.mkdir(parents=True, exist_ok=True)
copy = WORK / "rows_for_webq.jsonl"
copy.write_bytes(ROWS.read_bytes())
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
subprocess.run([sys.executable, "-B", str(EZ / "tools" / "run_validator_suite.py"), str(copy)], cwd=str(EZ / "tools"),
               capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
rep = json.loads(Path(str(copy) + ".validator_report.json").read_text(encoding="utf-8"))
wq = rep.get("web_quotes")
if not isinstance(wq, dict):
    raise SystemExit("REFUSED: the suite report carries no web_quotes member; keys %s" % sorted(rep))
lists = [k for k, v in wq.items() if isinstance(v, list)]
wq_items = [x for k in lists for x in wq[k] if isinstance(x, dict)]
order = [json.loads(l)["decision_id"] for l in copy.read_text(encoding="utf-8").splitlines() if l.strip()]
for x in wq_items:
    m = re.fullmatch(r"\[(\d+)\]\.([a-z_]+)(?:\[\d+\])?", str(x.get("path", "")))
    if not m:
        raise SystemExit("REFUSED: a web_quotes flag whose path is not '[row index].field': %r" % x.get("path"))
    add("WEBQ", order[int(m.group(1))], [m.group(2)], {"web_quotes_flag": x}, "web_quotes member on the rows at build time")
if len([i for i in items if i["class"] == "WEBQ"]) != len(wq_items):
    raise SystemExit("REFUSED: %d web_quotes flags but a different number of WEBQ items (E-36)" % len(wq_items))

for n, it in enumerate(items, 1):
    it["id"] = "S5-%03d" % n
by_class = {}
for it in items:
    by_class[it["class"]] = by_class.get(it["class"], 0) + 1
rows_owed = sorted({it["row"] for it in items})
out = {"schema": "ezek_repair2_step5_worklist.v1", "probe": PROBE, "rows_sha256": sha(ROWS),
       "step4c_adjudication_landed": ADJ4C.is_file(), "register_flags_at_build": reg_total,
       "web_quotes_flags_at_build": len(wq_items), "items_by_class": by_class, "rows_owed": len(rows_owed),
       "high_rows_owed": sorted(r for r in rows_owed if rows[r].get("confidence") == "high"),
       "what_a_rewrite_may_do": "state the substance of a barred referent; read back as English; change no claim, "
                                "grade, span, identity or signal", "items": items}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("probe", "rows_sha256", "step4c_adjudication_landed", "register_flags_at_build",
                                      "web_quotes_flags_at_build", "items_by_class", "rows_owed", "high_rows_owed")}, indent=1))
print("worklist:", OUT, "sha256:", sha(OUT))
