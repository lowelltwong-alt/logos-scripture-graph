#!/usr/bin/env python3
"""Judge each lane's candidate with the PINNED SUITE, against a baseline taken first. Scratch-only.

WHY THE SUITE AND NOT MY GATE. check_candidate.py runs two members. The pinned suite runs all of them - the
citation sweep's sentence-scoped Hebrew collation, the web-quote member, marks symmetry, tiling, universals.
A lane can be ALL_CLEAN on two members and break a third, which is precisely how the author wave went from
GREEN to RED (E-34). So every candidate is run through the whole suite before reconciliation, and the verdict
is the DELTA per member against the live rows - never the candidate's absolute status, because the live rows
already carry known flags that are not the lane's doing.

WHY A BASELINE FIRST. I once ran the suite for the first time only AFTER mutating, and had to recover the
baseline from per-sweep backups (E13-79). The baseline here is the live rows copied byte-for-byte, digest
checked, and judged by the same suite in the same run.

usage: python suite_candidates.py a [b ...]
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
LIVE = EZ / "repair" / "rows_v7_cwo24.jsonl"
SUITE = EZ / "tools" / "run_validator_suite.py"
WORK = HERE / "suite_runs"
EXPECT_LIVE = "1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425"
PROSE = {"boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess"}
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731

live_b = LIVE.read_bytes()
if sha(live_b) != EXPECT_LIVE:
    raise SystemExit("REFUSED: the live rows moved (%s); a candidate built on a different base is not "
                     "comparable to the lanes' gate runs" % sha(live_b))
WORK.mkdir(exist_ok=True)


def run_suite(rows_path):
    # UTF-8 MODE FOR THE WHOLE PROCESS TREE. The suite decodes each member's stdout as UTF-8, but on Windows a
    # piped child writes in the ANSI codepage unless UTF-8 mode is on, so a member printing Hebrew produced
    # undecodable bytes and the suite crashed reading None. The environment is inherited by every member.
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    proc = subprocess.run([sys.executable, str(SUITE), str(rows_path)], cwd=str(SUITE.parent),
                          capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    rep = Path(str(rows_path) + ".validator_report.json")
    if not rep.exists():
        raise SystemExit("the suite wrote no report for %s; stderr: %s" % (rows_path.name, proc.stderr[-600:]))
    return json.loads(rep.read_text(encoding="utf-8")), proc.returncode


def build(lane):
    prop = json.loads((HERE / ("lane_%s" % lane) / "proposal.json").read_text(encoding="utf-8"))
    rows = [json.loads(l) for l in live_b.decode("utf-8").splitlines() if l.strip()]
    by = {r["decision_id"]: r for r in rows}
    for rid, fields in prop.items():
        if rid not in by:
            raise SystemExit("REFUSED: lane %s proposes for an unknown row %s" % (lane, rid))
        for f, v in fields.items():
            if f not in PROSE:
                raise SystemExit("REFUSED: lane %s proposes a non-prose field %s on %s" % (lane, f, rid))
            by[rid][f] = v
    out = WORK / ("candidate_%s.jsonl" % lane)
    # the same serialisation the corpus uses, one JSON object per line, UTF-8, LF
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8",
                   newline="\n")
    return out, sorted(prop)


SKIP_KEYS = {"_exit", "rows_file", "file", "stdout", "stderr"}


def _strip_file(x):
    if isinstance(x, dict):
        return {k: _strip_file(v) for k, v in x.items() if k not in ("file", "rows_file")}
    if isinstance(x, list):
        return [_strip_file(v) for v in x]
    return x


def members(rep):
    """Every member the report carries, as {member: {"scalars": {...}, "lists": {field: [canonical items]}}}.

    THE SHAPE IS READ, NOT GUESSED. My first reader looked for a `members` key, found none, and - because of the
    zero-denominator refusal built after E-36 - refused instead of printing "no member moved". The members are
    TOP-LEVEL keys beside `summary`. And a COUNT comparison is not enough: a lane can clear one flag and add a
    different one with the count unchanged, so every list a member reports is compared ITEM BY ITEM.
    """
    out = {}
    for name, m in rep.items():
        if name == "summary" or not isinstance(m, dict):
            continue
        scal, lists = {}, {}
        for k, v in m.items():
            if k in SKIP_KEYS:
                continue
            if isinstance(v, list):
                # every flag item carries the NAME of the rows file it was read from, so a baseline item and the
                # identical candidate item never compared equal and the first diff reported every flag as
                # both added and removed. The file name is identity of the RUN, not of the finding.
                lists[k] = sorted(json.dumps(_strip_file(x), ensure_ascii=False, sort_keys=True) for x in v)
            else:
                scal[k] = json.dumps(v, ensure_ascii=False, sort_keys=True)
        out[name] = {"scalars": scal, "lists": lists}
    return out


def diff_member(b, c):
    from collections import Counter
    d = {}
    for k in sorted(set(b["scalars"]) | set(c["scalars"])):
        if b["scalars"].get(k) != c["scalars"].get(k):
            d.setdefault("scalars", {})[k] = {"baseline": b["scalars"].get(k, "<absent>")[:300],
                                              "candidate": c["scalars"].get(k, "<absent>")[:300]}
    for k in sorted(set(b["lists"]) | set(c["lists"])):
        bc, cc = Counter(b["lists"].get(k, [])), Counter(c["lists"].get(k, []))
        added, removed = list((cc - bc).elements()), list((bc - cc).elements())
        if added or removed:
            d.setdefault("lists", {})[k] = {"added": [json.loads(x) for x in added][:40],
                                            "removed": [json.loads(x) for x in removed][:40],
                                            "added_n": len(added), "removed_n": len(removed)}
    return d


base = WORK / "baseline_live.jsonl"
base.write_bytes(live_b)
if sha(base.read_bytes()) != EXPECT_LIVE:
    raise SystemExit("REFUSED: the baseline copy does not match the live rows")
REUSE = "--reuse-reports" in sys.argv
LANES = [a for a in sys.argv[1:] if not a.startswith("--")]
_brep = Path(str(base) + ".validator_report.json")
base_rep = json.loads(_brep.read_text(encoding="utf-8")) if REUSE and _brep.exists() else run_suite(base)[0]
bm = members(base_rep)
if not bm:
    raise SystemExit("REFUSED: could not read any member from the suite report - its shape is not the one "
                     "this reader expects, and a comparison over zero members is not a comparison (E-36). Top "
                     "keys: %s" % list(base_rep.keys()))

summary = {"baseline": {"rows_sha256": EXPECT_LIVE, "summary": base_rep.get("summary"),
                        "members": sorted(bm)}}
for lane in LANES:
    cand, touched = build(lane)
    _crep = Path(str(cand) + ".validator_report.json")
    rep = json.loads(_crep.read_text(encoding="utf-8")) if REUSE and _crep.exists() else run_suite(cand)[0]
    cm = members(rep)
    delta, compared_lists = {}, 0
    empty = {"scalars": {}, "lists": {}}
    for name in sorted(set(bm) | set(cm)):
        b, c = bm.get(name, empty), cm.get(name, empty)
        compared_lists += len(set(b["lists"]) | set(c["lists"]))
        dm = diff_member(b, c)
        if dm:
            delta[name] = dm
    if compared_lists == 0:
        raise SystemExit("REFUSED: zero flag lists compared for lane %s (E-36)" % lane)
    summary["lane_" + lane] = {
        "candidate_sha256": sha(cand.read_bytes()), "rows_touched": touched,
        "summary": rep.get("summary"), "members_compared": len(set(bm) | set(cm)),
        "flag_lists_compared": compared_lists,
        "members_that_changed": delta,
        "verdict": ("NO MEMBER MOVED against the baseline" if not delta else
                    "%d member(s) moved - read each before reconciling" % len(delta)),
    }
(WORK / "suite_delta.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8",
                                       newline="\n")
print(json.dumps(summary, ensure_ascii=False, indent=1)[:5000])
