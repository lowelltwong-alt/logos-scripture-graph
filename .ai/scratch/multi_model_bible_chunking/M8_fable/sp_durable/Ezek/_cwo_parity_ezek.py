#!/usr/bin/env python3
"""CWO execution parity for Ezekiel's close: one record, bound to ONE corpus sha256, showing that every corpus-wide order
(CWO-EZ-01..24) still holds over the bytes that will be assembled (E-18). It is the Ezekiel form of the Lamentations
close-tool gate `cwo/cwo_parity.<corpus-stem>.json` (post_corpus_sha256 equal, exact_arm_residual empty, status GREEN).

WHY A NEW TOOL. Each per-stage coverage tool binds to the rows image that was live when it ran. Three cannot simply be
pointed at the final corpus:
  - the stage-bound s2/e10 tools write to fixed repair/cwo_coverage_<stage> directories, which already hold the v7
    records over 25cdba56, and they refuse to overwrite them;
  - the FIXUP-1 tool (CWO-EZ-14..18) aborts unless the suite stands at its TOOLFIX-2/TOOLFIX-5 install digests, which
    #e16's tool order has since moved.
This tool re-runs what can be re-run as-is, runs the stage-bound tools in a temporary mirror, and evaluates the rest from
their own predicates. The needles are imported from the tools that own them.

WHAT EACH CWO GETS
  01, 02, 04-09  The generic tool, re-run over the corpus.
  19-23          The stage-bound tools, run in a temporary mirror (tool bytes copied and sha-recorded).
  14-18          The FIXUP-1 tool's predicates, read from the corpus's own validator report, with its needles imported.
                 The live suite digests are recorded beside the install digests they no longer equal.
  24             The manifest's 18 pairs, each under its own post-check rule.
  03, 10         The CWO-EZ-10 scan, re-run. Its narrowed test (c) is #e3's re-evaluation of CWO-EZ-03's predicate.
  11, 12, 13     Their sweep predicates, re-evaluated. For 11 this is under ruling e14's role-token amendment.
  Rewritten pairs A pair of 23 or 24 whose new bytes a later RULED wave rewrote is traced through the saved pre-images
                 (in mtime order) to the last image that held them. It is then attributed to the record that names that
                 image as its pre-image, and the tool checks that the record does name it. Evidence tiers: the naming is
                 EXTRACTED; that the named wave rewrote the bytes is INFERRED from the image succession; that the old
                 defect bytes are absent from the whole field is MEASURED.

NEVER OVERWRITES. Everything is built in a temporary directory first, then installed. An existing file with the same
bytes is left in place; if its bytes differ, the tool refuses.

usage: _cwo_parity_ezek.py --rows rows_v8_final.jsonl [--dry | --check]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
REPAIR = EZ / "repair"
PY = sys.executable
ENV = dict(os.environ, PYTHONUTF8="1")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, EZ / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cov = load("cwo_coverage_ezek", "_cwo_coverage_ezek.py")
_fx = load("cwo_coverage_fixup1_ezek", "_cwo_coverage_fixup1_ezek.py")
_arms = load("cwo22_arms", "_cwo22_arms.py")

GENERIC = ("CWO-EZ-01", "CWO-EZ-02") + tuple("CWO-EZ-%02d" % n for n in range(4, 10))
STAGE_BOUND = (("_cwo_coverage_s2_ezek.py", "CWO-EZ-19", True), ("_cwo_coverage_s2_ezek.py", "CWO-EZ-20", False),
               ("_cwo_coverage_s2_ezek.py", "CWO-EZ-21", False), ("_cwo_coverage_e10_ezek.py", "CWO-EZ-22", False),
               ("_cwo_coverage_e10_ezek.py", "CWO-EZ-23", False))
MIRROR_FILES = ("_cwo_coverage_s2_ezek.py", "_cwo_coverage_e10_ezek.py", "_cwo22_arms.py",
                "ezek_controlling_agent_rulings_e9.v1.json", "ezek_controlling_agent_rulings_e10.v1.json")
STAGE_LABEL = "v7"   # the tools' own directory label; inside the mirror, so the live v7 records are never touched
CWO24_MANIFEST = REPAIR / "rows_v7_cwo24.manifest.json"
CWO11_MANIFEST = REPAIR / "rows_v3_cwo11.manifest.json"
CWO12_MANIFEST = REPAIR / "rows_v3_cwo12.manifest.json"
CWO13_MANIFEST = REPAIR / "rows_v3_cwo13.manifest.json"
CWO03_LAST = REPAIR / "cwo03_scan_report.json"
CWO14_LAST = REPAIR / "cwo_coverage_v7" / "CWO-EZ-14.json"   # holds the install digests the FIXUP-1 tool demands
RULING_E14 = EZ / "ezek_controlling_agent_ruling_e14.v1.json"
E14_KEY = "6_role_token_mandatory"
RETILE_E17 = EZ / "repair2" / "e17" / "retile_e17.manifest.json"
NEEDLES_13 = (", hebrew: None", "['SAMEKH']", "['PE']")
_rt = load("check_role_tokens", "tools/check_role_tokens.py")   # the suite member that owns the e14 entry grammar


def role_token(e):
    m = _rt.ENTRY.match(e)
    return bool(m) and (m.groups()[10] in _rt.VOCAB or m.groups()[10] in _rt.ALIASES)
FIELD_IDX = re.compile(r"^(\w+)\[(\d+)\]$")
# last image that held a pair's new bytes -> the records that name that image as their pre-image
ATTRIBUTION = {
    "03327cf4fda4": ("author/final/s1_adjudication/adjudication.json",),
    "a2e51d689bcb": ("author/repair2_step6/h1_adjudication/adjudication.json",
                     "author/repair2_step6/h2_adjudication/adjudication.json"),
    "836bdf2c9d5f": ("repair2/session_910cbe15/ezek_aw/author_wave_apply.v1.json",),
    "f5315a8ac649": ("repair2/e17/retile_e17.manifest.json",),
    "1238eb2443c2": ("repair2/step2_reconciliation/adjudication_a1/adjudication.json",),
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).relative_to(EZ)).replace("\\", "/")


def read_rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def whole_field(row, field):
    """The field as one string. A list-indexed field is read over the WHOLE list, because retiles shift indices: the
    old-absence check becomes stricter, and presence is only used to locate an image."""
    m = FIELD_IDX.match(field)
    v = row.get(m.group(1) if m else field)
    if isinstance(v, list):
        return "\n".join(x for x in v if isinstance(x, str))
    return v if isinstance(v, str) else ""


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, encoding="utf-8")
    return r.returncode


def images():
    out = []
    pre = sorted(REPAIR.glob("rows_v7_cwo24.jsonl.pre_*"), key=lambda p: p.stat().st_mtime)
    for p in pre + [REPAIR / "rows_v7_cwo24.jsonl"]:
        h = sha(p)
        if p.name.startswith("rows_v7_cwo24.jsonl.pre_") and not h.startswith(p.name.rsplit("_", 1)[1]):
            raise SystemExit("ABORT: %s is not the image its name says (%s)" % (p.name, h[:12]))
        out.append((h[:12], {r["decision_id"]: r for r in read_rows(p)}))
    return out


def trace(imgs, corpus_by_id, row, field, old, new):
    """Where did a pair's new bytes go? Returns the evidence for a ruled rewrite, or None when unattributable."""
    last = None
    for h, rows in imgs:
        if row in rows and new and new in whole_field(rows[row], field):
            last = h
    records = []
    for r in ATTRIBUTION.get(last, ()):
        text = (EZ / r).read_text(encoding="utf-8")
        records.append({"record": r, "sha256": sha(EZ / r), "names_the_image": last in text})
    old_absent = row not in corpus_by_id or old not in whole_field(corpus_by_id[row], field)
    ok = bool(records) and all(x["names_the_image"] for x in records) and old_absent
    return {"row": row, "field": field, "new_last_held_in_image": last, "rewritten_by": records,
            "old_bytes_absent_on_corpus": old_absent, "attributed": ok,
            "tier": "naming EXTRACTED; rewrite INFERRED from image succession; old-absence MEASURED"}


def build(rows_p, td):
    rows = read_rows(rows_p)
    by_id = {r["decision_id"]: r for r in rows}
    rep_p = Path(str(rows_p) + ".validator_report.json")
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    if rep.get("rows_file") != rows_p.name or rep["summary"].get("hard_status") != "GREEN":
        raise SystemExit("ABORT: %s is not a hard-GREEN report over %s" % (rep_p.name, rows_p.name))
    if rep_p.stat().st_mtime < rows_p.stat().st_mtime:
        raise SystemExit("ABORT: the validator report is older than the corpus")
    parity, tools, side = {}, {}, {}

    # 01, 02, 04-09: the generic tool
    gen = td / "generic"
    rc = run([PY, str(EZ / "_cwo_coverage_ezek.py"), "--rows", str(rows_p), "--report", str(rep_p), "--out", str(gen)], EZ)
    tools["_cwo_coverage_ezek.py"] = sha(EZ / "_cwo_coverage_ezek.py")
    for cid in GENERIC:
        d = json.loads((gen / (cid + ".json")).read_text(encoding="utf-8"))
        assert d["rows_file"]["sha256"] == sha(rows_p), cid
        parity[cid] = {"arm": "exact", "method": "generic coverage tool re-run over the corpus (exit %d)" % rc,
                       "status": "COVERED" if d["verdict"] == "COVERED" and not d["residual_count"] else "RESIDUAL",
                       "residual_count": d["residual_count"], "residual": d["residual"],
                       "triage_flags": len(d["triage_flags"]), "record": "generic/%s.json" % cid}

    # 19-23: the stage-bound tools in a temporary mirror
    mir = td / "mirror"
    (mir / "repair").mkdir(parents=True)
    for f in MIRROR_FILES:
        shutil.copyfile(EZ / f, mir / f)
        tools[f] = sha(EZ / f)
        assert sha(mir / f) == tools[f]
    shutil.copyfile(rows_p, mir / rows_p.name)
    shutil.copyfile(rep_p, mir / rep_p.name)
    sb = td / "stage_bound"
    sb.mkdir()
    for tool, cid, needs_report in STAGE_BOUND:
        cmd = [PY, tool, "--cwo", cid, "--stage", STAGE_LABEL, "--rows", rows_p.name]
        if needs_report:
            cmd += ["--suite-report", rep_p.name]
        rc = run(cmd, mir)
        d = json.loads((mir / "repair" / ("cwo_coverage_" + STAGE_LABEL) / (cid + ".json")).read_text(encoding="utf-8"))
        assert d["rows_file"]["sha256"] == sha(rows_p), cid
        shutil.copyfile(mir / "repair" / ("cwo_coverage_" + STAGE_LABEL) / (cid + ".json"), sb / (cid + ".json"))
        parity[cid] = {"arm": "exact", "method": "%s run in a temporary mirror, stage label %s (exit %d)" % (tool, STAGE_LABEL, rc),
                       "tool_verdict": d["verdict"], "record": "stage_bound/%s.json" % cid}
        if cid == "CWO-EZ-23":
            parity[cid].update(pairs_verified=d["pairs_verified"], pairs_ordered=len(d["pair_checks"]))
        else:
            parity[cid].update(residual_count=d.get("residual_count", d.get("hit_count")), residual=d.get("residual", []))
            parity[cid]["status"] = "COVERED" if d["verdict"] == "COVERED" else "RESIDUAL"
    imgs = images()
    pairs23 = {p["n"]: p for p in _arms.pairs()}
    failed = [c for c in json.loads((sb / "CWO-EZ-23.json").read_text(encoding="utf-8"))["pair_checks"] if c["new_count"] != 1 or c["old_count"]]
    rewrites = []
    for c in failed:
        p = pairs23[c["pair"]]
        t = trace(imgs, by_id, p["row"], p["field"], p["old"], p["new"])
        rewrites.append(dict(pair=c["pair"], **t))
    bad = [r for r in rewrites if not r["attributed"]]
    parity["CWO-EZ-23"].update(
        status="COVERED" if not failed else ("COVERED_WITH_RULED_REWRITES" if not bad else "RESIDUAL"),
        ruled_rewrites=rewrites, residual_count=len(bad), residual=bad)

    # 14-18: the FIXUP-1 predicates over the corpus's own report
    cs = rep["citation_sweep"]
    cs_all = [str(p) for p in (cs.get("problems") or []) + (cs.get("nfd_degraded") or []) + (cs.get("prose_pair_problems") or [])]
    nd, wq = rep["hebrew_normalize_dryrun"], rep["web_quotes"].get("flags") or []
    res = {
        "CWO-EZ-14": list(rep["register"].get("flags") or []),
        "CWO-EZ-15": ([{"normalizer_defect": x} for x in nd.get("defects") or []]
                      + ([{"normalizer_fixed": nd["fixed"]}] if nd.get("fixed") else [])
                      + [{"citation_sweep": p} for p in cs_all if _fx.CWO16_MARK not in p and any(n in p for n in _fx.CWO15_PROBLEM)]),
        "CWO-EZ-16": [{"citation_sweep": p} for p in cs_all if _fx.CWO16_MARK in p],
        "CWO-EZ-17": [f for f in wq if str(f.get("issue", "")).startswith(_fx.E15D)],
        "CWO-EZ-18": [f for f in wq if f.get("issue") == _fx.NO_REF],
    }
    i13 = next(i for i, r in enumerate(rows) if r["decision_id"] == _fx.R1_ROW)
    entry = rows[i13]["boundary_evidence_refs"][_fx.R1_INDEX]
    reported = json.loads(CWO11_MANIFEST.read_text(encoding="utf-8"))["reported_not_touched"]
    on_row = [f for f in wq if f.get("issue") == _fx.NO_REF and str(f.get("path", "")).startswith("[%d]." % i13)]
    reshaped = bool(_cov.CANON_REF.match(entry.strip()))
    c01 = json.loads((gen / "CWO-EZ-01.json").read_text(encoding="utf-8"))
    names_same = any(t.get("row") == _fx.R1_ROW and t.get("entry") == entry for t in c01.get("triage_flags") or [])
    fc_ok = not on_row and (not [p for p in cs_all if p.split(":", 1)[0] == _fx.R1_ROW] if reshaped else names_same)
    fc = {"ordered_by": "ezek_controlling_rulings_a1#e7 ruling CWO18-R1-1", "row": _fx.R1_ROW,
          "entry_on_corpus": entry, "entry_cwo11_reported_not_touched": [x["entry"] for x in reported if x["row"] == _fx.R1_ROW],
          "reshaped_to_strict_r1_shape": reshaped, "no_ref_class_on_row_all_fields": len(on_row),
          "cwo01_triage_names_same_entry": names_same, "satisfied": fc_ok}
    if not fc_ok:
        res["CWO-EZ-18"].append({"e7_final_check": "not satisfied"})
    install = json.loads(CWO14_LAST.read_text(encoding="utf-8"))["suite_members_at_toolfix2_install_digest"]
    live = {m: sha(EZ / m) for m in install}
    for cid in ("CWO-EZ-14", "CWO-EZ-15", "CWO-EZ-16", "CWO-EZ-17", "CWO-EZ-18"):
        parity[cid] = {"arm": "exact", "method": "the FIXUP-1 tool's predicate, needles imported from it, over the corpus's validator report",
                       "status": "COVERED" if not res[cid] else "RESIDUAL", "residual_count": len(res[cid]), "residual": res[cid]}
    parity["CWO-EZ-18"]["e7_final_check"] = fc
    tools["_cwo_coverage_fixup1_ezek.py"] = sha(EZ / "_cwo_coverage_fixup1_ezek.py")
    suite = {"members_live": live, "members_at_install": install,
             "members_moved_since_install": sorted(m for m in install if live[m] != install[m]),
             "why_the_fixup1_tool_is_not_rerun": "it aborts by design unless every member stands at its install digest"}

    # 24: the manifest's pairs under their own rules
    man24 = json.loads(CWO24_MANIFEST.read_text(encoding="utf-8"))
    rules = {c["n"]: c["rule"] for c in man24["post_checks"]}
    retile = json.loads(RETILE_E17.read_text(encoding="utf-8"))
    succ = {rid: [v["decision_id"] for v in retile["new_row_ids"].values() if rid in v["from"]] for rid in retile["retired"]}
    checks24, res24 = [], []
    for p in man24["pairs"]:
        c = {"pair": p["n"], "row": p["row"], "field": p["field"], "kind": p["kind"], "rule": rules[p["n"]]}
        if p["row"] in by_id:
            v = whole_field(by_id[p["row"]], p["field"])
            c["old_absent"] = p["old"] not in v
            c["new_occurrences"] = v.count(p["new"]) if p["kind"] != "deletion" else None
            c["holds"] = c["old_absent"] and (p["kind"] == "deletion" or c["new_occurrences"] == 1)
            if not c["holds"] and c["old_absent"]:
                c["ruled_rewrite"] = trace(imgs, by_id, p["row"], p["field"], p["old"], p["new"])
                c["holds_by_ruled_rewrite"] = c["ruled_rewrite"]["attributed"]
        else:
            s = succ.get(p["row"], [])
            c["row_retired_by"] = {"record": rel(RETILE_E17), "sha256": sha(RETILE_E17), "successors": s,
                                   "retired_listed": p["row"] in retile["retired"]}
            c["old_absent_in_successors_same_field"] = all(p["old"] not in whole_field(by_id[x], p["field"]) for x in s if x in by_id)
            c["holds_by_ruled_retile"] = bool(s) and c["row_retired_by"]["retired_listed"] and c["old_absent_in_successors_same_field"]
        if not (c.get("holds") or c.get("holds_by_ruled_rewrite") or c.get("holds_by_ruled_retile")):
            res24.append(c)
        checks24.append(c)
    sup = [c["pair"] for c in checks24 if not c.get("holds") and c not in res24]
    parity["CWO-EZ-24"] = {"arm": "exact", "method": "the manifest's 18 pairs under their recorded post-check rules",
                           "record": rel(CWO24_MANIFEST), "record_sha256": sha(CWO24_MANIFEST),
                           "status": "RESIDUAL" if res24 else ("COVERED_WITH_RULED_REWRITES" if sup else "COVERED"),
                           "pair_checks": checks24, "pairs_superseded_by_ruled_waves": sup,
                           "residual_count": len(res24), "residual": res24}

    # 03, 10: the CWO-EZ-10 scan
    scan = td / "cwo10_scan_report.json"
    rc = run([PY, str(EZ / "_cwo10_scan.py"), "--rows", str(rows_p), "--out", str(scan)], EZ)
    tools["_cwo10_scan.py"] = sha(EZ / "_cwo10_scan.py")
    s10 = json.loads(scan.read_text(encoding="utf-8"))
    routed = s10.get("routed_to_controlling_agent") or []
    parity["CWO-EZ-10"] = {"arm": "scan", "method": "_cwo10_scan.py re-run over the corpus (exit %d)" % rc,
                           "record": "cwo10_scan_report.json", "rows_scanned": s10["rows_scanned"],
                           "status": "COVERED" if not routed else "ROUTED", "residual_count": len(routed), "residual": routed,
                           "limit": s10.get("limit")}
    parity["CWO-EZ-03"] = {"arm": "scan", "method": "re-evaluated through CWO-EZ-10, whose record states it is 'the CWO-EZ-03 "
                           "predicate re-evaluated on the new spans' with #e3's narrowed test (c)",
                           "last_own_record": rel(CWO03_LAST), "last_own_record_sha256": sha(CWO03_LAST),
                           "status": parity["CWO-EZ-10"]["status"], "residual_count": len(routed), "residual": routed}

    # 11, 12, 13: sweep predicates
    strict = tagged = 0
    out11, kept = [], []
    for r in rows:
        for i, e in enumerate(r.get("boundary_evidence_refs") or []):
            if not (isinstance(e, str) and _cov.WITNESS_PREFIX.match(e)):
                continue
            if _cov.CANON_REF.match(e.strip()):
                strict += 1
            elif role_token(e):
                tagged += 1
            elif any(x["row"] == r["decision_id"] and x["field"] == "boundary_evidence_refs[%d]" % i for x in reported):
                # the one entry CWO-EZ-11 reported untouched; later ruled sweeps (20, 18) re-quoted it, so it is matched
                # by position, and its own check is CWO-EZ-18's #e7 final check on the same entry
                kept.append({"row": r["decision_id"], "index": i, "entry_now": e,
                             "entry_when_reported": [x["entry"] for x in reported if x["row"] == r["decision_id"]]})
            else:
                out11.append({"row": r["decision_id"], "index": i, "entry": e[:160]})
    e14 = RULING_E14.read_text(encoding="utf-8")
    tools["tools/check_role_tokens.py"] = sha(EZ / "tools" / "check_role_tokens.py")
    parity["CWO-EZ-11"] = {"arm": "exact", "method": "every witness-prefixed boundary_evidence_refs entry is in the strict R1 shape, or "
                           "matches ruling e14's role-token grammar (ENTRY and VOCAB imported from tools/check_role_tokens.py), "
                           "or is the one entry CWO-EZ-11 reported untouched",
                           "amended_by": {"record": rel(RULING_E14), "sha256": sha(RULING_E14), "key": E14_KEY, "key_present": ('"%s"' % E14_KEY) in e14},
                           "strict_r1_entries": strict, "role_token_entries": tagged, "reported_untouched_entry": kept,
                           "reported_untouched_entry_final_check": parity["CWO-EZ-18"]["e7_final_check"]["satisfied"],
                           "suite_role_tokens_status": rep.get("role_tokens", {}).get("status"),
                           "status": "COVERED" if not out11 and ('"%s"' % E14_KEY) in e14 else "RESIDUAL",
                           "residual_count": len(out11), "residual": out11}
    labels = json.loads(CWO12_MANIFEST.read_text(encoding="utf-8"))["labels_after"]
    per_parent = {}
    for r in rows:
        per_parent.setdefault(str(r.get("parent_collection")).split(" ", 1)[0], set()).add(r.get("parent_collection"))
    out12 = [{"row": r["decision_id"], "label": r.get("parent_collection")} for r in rows if r.get("parent_collection") not in labels]
    out12 += [{"parent": k, "labels": sorted(v)} for k, v in per_parent.items() if len(v) > 1]
    parity["CWO-EZ-12"] = {"arm": "exact", "method": "every row's parent label is one of the manifest's canonical labels, one label per parent",
                           "record": rel(CWO12_MANIFEST), "labels_in_use": len({r.get("parent_collection") for r in rows}),
                           "status": "COVERED" if not out12 else "RESIDUAL", "residual_count": len(out12), "residual": out12}
    ruled13 = json.loads(CWO13_MANIFEST.read_text(encoding="utf-8"))["ruled_order"]
    assert all(n in ruled13 for n in NEEDLES_13), "a CWO-EZ-13 needle is not in the ruled order"
    out13 = [{"row": r["decision_id"], "index": i} for r in rows for i, e in enumerate(r.get("boundary_evidence_refs") or [])
             if isinstance(e, str) and any(n in e for n in NEEDLES_13)]
    parity["CWO-EZ-13"] = {"arm": "exact", "method": "none of the ruled order's needles remains in any boundary_evidence_refs entry",
                           "needles": list(NEEDLES_13), "record": rel(CWO13_MANIFEST),
                           "status": "COVERED" if not out13 else "RESIDUAL", "residual_count": len(out13), "residual": out13}

    order = sorted(parity, key=lambda k: int(k.rsplit("-", 1)[1]))
    parity = {k: parity[k] for k in order}
    exact = [dict(cwo=k, **x) if isinstance(x, dict) else {"cwo": k, "item": x}
             for k, v in parity.items() if v["status"] == "RESIDUAL" for x in v["residual"]]
    routed_open = [k for k, v in parity.items() if v["status"] == "ROUTED"]
    for p in sorted(td.rglob("*.json")):
        if "mirror" not in p.parts:
            side[str(p.relative_to(td)).replace("\\", "/")] = sha(p)
    body = {"schema": "ezek_cwo_parity.v1", "book": "Ezek", "post_corpus": rel(rows_p), "post_corpus_sha256": sha(rows_p),
            "rows": len(rows), "suite_report": {"path": rel(rep_p), "sha256": sha(rep_p)},
            "parity": parity, "exact_arm_residual": exact, "routed_open": routed_open,
            "status": "GREEN" if not exact and not routed_open else "NOT_GREEN",
            "tools": tools, "suite_digests": suite, "side_records": side,
            "coverage_dir": "cwo/coverage_%s/" % rows_p.stem,
            "law": "E-18: every corpus-wide order checked again as its own sweep over the corpus being closed",
            "limits": ["CWO-EZ-14..18 are evaluated with the live suite, not the TOOLFIX install digests; the members that moved are listed.",
                       "The scan arms (03, 10) report messenger formulae but cannot judge an addressee change.",
                       "The pre-image walk orders the saved images by file mtime.",
                       "A ruled rewrite shows that a ruled wave replaced a pair's new bytes. It does not re-judge that wave's prose; "
                       "the close checkers do."]}
    return json.dumps(body, ensure_ascii=False, indent=1) + "\n"


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise SystemExit("REFUSED: %s exists with different bytes; never overwritten" % rel(path))
        return "same bytes, left"
    path.write_bytes(data)
    return "written"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True, help="the corpus, relative to Ezek/")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dry", action="store_true", help="build and summarise; install nothing")
    a = ap.parse_args()
    rows_p = EZ / a.rows
    out = EZ / "cwo" / ("cwo_parity.%s.json" % rows_p.stem)
    cov = EZ / "cwo" / ("coverage_%s" % rows_p.stem)
    with tempfile.TemporaryDirectory(prefix="ezek_cwo_parity_") as t:
        td = Path(t)
        body = build(rows_p, td).encode("utf-8")
        side = [p for p in sorted(td.rglob("*.json")) if "mirror" not in p.relative_to(td).parts]
        if a.dry:
            d = json.loads(body)
            print(json.dumps({"status": d["status"], "per_cwo": {k: [v["status"], v.get("residual_count")] for k, v in d["parity"].items()},
                              "exact_arm_residual": d["exact_arm_residual"][:6], "routed_open": d["routed_open"]}, ensure_ascii=False, indent=1))
            return
        if a.check:
            same = out.is_file() and out.read_bytes() == body and all(
                (cov / p.relative_to(td)).is_file() and (cov / p.relative_to(td)).read_bytes() == p.read_bytes() for p in side)
            print("MATCH" if same else "DIFFERS")
            return
        for p in side:
            write_new(cov / p.relative_to(td), p.read_bytes())
        state = write_new(out, body)
    d = json.loads(out.read_text(encoding="utf-8"))
    print(json.dumps({"record": rel(out), "record_state": state, "sha256": sha(out), "status": d["status"],
                      "post_corpus_sha256": d["post_corpus_sha256"],
                      "per_cwo": {k: [v["status"], v.get("residual_count")] for k, v in d["parity"].items()},
                      "exact_arm_residual": len(d["exact_arm_residual"]), "routed_open": d["routed_open"]}, indent=1))


if __name__ == "__main__":
    main()
