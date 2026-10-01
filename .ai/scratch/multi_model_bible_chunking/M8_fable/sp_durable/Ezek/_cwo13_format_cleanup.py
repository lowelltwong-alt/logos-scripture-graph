#!/usr/bin/env python3
"""CWO-EZ-13 (ezek_controlling_rulings_a1#e4), run as its own deterministic sweep: a lossless format clean-up of
boundary_evidence_refs strings. The order and predicate are read from the rulings file and carried verbatim in the manifest.

PREDICATE (whole corpus, never by row list): every boundary_evidence_refs string containing the byte sequence 'hebrew: None'
or the list repr ['SAMEKH'] or ['PE'].
CHANGE: the segment 'hebrew: None' is removed with its separator ('; ' or ', ' before it, or after it when it opens the
parenthetical); ['SAMEKH'] becomes samekh and ['PE'] becomes pe, with the surrounding text kept.

Before anything is written, the exact output bytes are probed with the validator suite in a scratch directory, and the run
aborts unless:
  - no predicate byte sequence is left in boundary_evidence_refs;
  - every touched entry matches the strict R1 shape (CANON_REF) after the change; the shape before is recorded too;
  - no field other than boundary_evidence_refs changed;
  - citation_sweep's problems and check_marks' flags are unchanged;
  - SUITE PARITY: every check's report is identical between the input and output bytes, with ONE accounted exception.
    check_universals' lexicon is case-insensitive, so it reads the placeholder's word 'None' as the universal claim 'none'.
    Its flags, compared by (path, claim), may differ only by removals of claim 'None' at a touched path, at most one per
    'hebrew: None' segment removed there. Nothing may be added, claims_seen may drop by at most the segments removed, its
    other keys are identical, and the suite summary's triage count drops by exactly the universals flags removed.
A real run requires --install-receipt: every file that receipt installed must still carry its installed digest, so the
parity assertions are bound to the tool bytes the gate names. --dry-run evaluates everything, writes the full report to the
scratch directory, and writes nothing under SP.

Usage: _cwo13_format_cleanup.py --in repair/rows_v3_cwo12.jsonl --out repair/rows_v3_cwo13.jsonl --expect-in <sha256>
       --scratch <session scratchpad> (--install-receipt <receipt> | --dry-run)"""
import argparse
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
sys.path.insert(0, str(EZ))
from _sweep_common import dump_rows, load_rows, sha, sha_bytes, summary, write_sweep  # noqa: E402

TOOLS, CAMPAIGN = EZ / "tools", EZ.parent / "campaign"
RULINGS_E4 = EZ / "ezek_controlling_agent_rulings_e4.v1.json"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
SUITE_TOOLS = ("run_validator_suite.py", "citation_sweep.py", "normalize_hebrew_in_json.py", "check_web_quotes.py",
               "check_refs_mirror.py", "check_marks.py", "check_universals.py", "check_language_zones.py", "ngram7.py",
               "cap_sweep.py", "check_register.py", "ezek_lib.py")
_spec = importlib.util.spec_from_file_location("cwo_coverage_ezek", EZ / "_cwo_coverage_ezek.py")
_cov = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cov)
CANON_REF = _cov.CANON_REF
HEB_NONE = "hebrew: None"
SEP_BEFORE = re.compile(r"[;,] ?hebrew: None(?!\w)")
SEP_AFTER = re.compile(r"hebrew: None[;,] ?")
REPRS = (("['SAMEKH']", "samekh"), ("['PE']", "pe"))
UNIV_MAY_MOVE = ("claims_seen", "flag_count", "flags")


def clean(s):
    new = SEP_AFTER.sub("", SEP_BEFORE.sub("", s))
    for old, rep in REPRS:
        new = new.replace(old, rep)
    return new


def in_predicate(s):
    return isinstance(s, str) and (HEB_NONE in s or any(o in s for o, _ in REPRS))


def canon(xs):
    return sorted(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in xs)


def claims(u):
    return Counter((f["path"], f["claim"]) for f in u.get("flags", []))


def receipt_gate(path):
    p = Path(path)
    rec = json.loads(p.read_text(encoding="utf-8"))
    if rec.get("schema") != "m8_tool_install_receipt.v1" or rec.get("book") != "Ezek":
        raise SystemExit("ABORT: %s is not an Ezek tool install receipt" % p.name)
    bound = {}
    for name, f in rec["files"].items():
        if f.get("state") != "installed":
            continue
        loc = (EZ.parent / name) if name.startswith("campaign/") else next((d / name for d in (TOOLS, EZ, CAMPAIGN) if (d / name).exists()), None)
        if loc is None or sha(loc) != f["after"]:
            raise SystemExit("ABORT: %s does not carry the digest %s... that receipt %s installed" % (name, f["after"][:16], rec.get("batch")))
        bound[name] = f["after"]
    return {"batch": rec.get("batch"), "receipt": p.name, "receipt_sha256": sha(p), "ordered_by": rec.get("ordered_by"), "files_bound": bound}


def probe(rows, td):
    body = dump_rows(rows)
    p = Path(td) / "rows.jsonl"
    rep_p = Path(str(p) + ".validator_report.json")
    p.write_bytes(body)
    if rep_p.exists():
        rep_p.unlink()
    r = subprocess.run([sys.executable, str(TOOLS / "run_validator_suite.py"), str(p)], capture_output=True, text=True,
                       encoding="utf-8", env=ENV, cwd=str(TOOLS))
    if not rep_p.exists():
        raise SystemExit("ABORT: the suite wrote no report (exit %s): %s" % (r.returncode, r.stderr[-600:]))
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    rep.pop("rows_file", None)
    return sha_bytes(body), rep


def differing(rep_in, rep_out, skip=()):
    out = {}
    for k in sorted(set(rep_in) | set(rep_out)):
        a, b = rep_in.get(k), rep_out.get(k)
        if k in skip or a == b:
            continue
        out[k] = sorted(kk for kk in set(a) | set(b) if a.get(kk) != b.get(kk)) if isinstance(a, dict) and isinstance(b, dict) else "value"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--expect-in", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--install-receipt")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    in_path, out_path, scratch = EZ / a.inp, EZ / a.out, Path(a.scratch)
    if not scratch.is_dir():
        raise SystemExit("ABORT: --scratch %s is not a directory" % scratch)
    if not a.dry_run and not a.install_receipt:
        raise SystemExit("ABORT: a real run requires --install-receipt (the gate sequences the TOOLFIX-2 install first)")
    tools_bound = receipt_gate(a.install_receipt) if a.install_receipt else None
    if sha(in_path) != a.expect_in:
        raise SystemExit("ABORT: %s is %s, not the expected chain head %s" % (a.inp, sha(in_path)[:16], a.expect_in[:16]))
    e4 = json.loads(RULINGS_E4.read_text(encoding="utf-8"))
    ruled = next(c for c in e4["corpus_wide_orders"] if c["id"] == "CWO-EZ-13")
    for phrase in ("hebrew: None", "['SAMEKH']", "['PE']", "strict R1 shape", "no field other than boundary_evidence_refs changed"):
        if phrase not in ruled["order"] + ruled["predicate"]:
            raise SystemExit("ABORT: %r is not in the CWO-EZ-13 the rulings file carries" % phrase)
    ruled_none_ids = set(re.findall(r"P\d{2}-\d{3}", ruled["predicate"]))
    m = re.search(r"(\d+) p06 rows", ruled["predicate"])
    ruled_repr_rows = int(m.group(1)) if m else None

    rows_in = load_rows(in_path)
    rows_out = copy.deepcopy(rows_in)
    changes, shape, hit_none, hit_repr, outside, none_segments = [], [], {}, {}, [], Counter()
    for ri, r in enumerate(rows_out):
        ids = (r["decision_id"], r.get("writer_decision_id"))
        for k, v in r.items():
            if k != "boundary_evidence_refs" and in_predicate(json.dumps(v, ensure_ascii=False)):
                outside.append({"row": ids[0], "field": k})
        refs = r.get("boundary_evidence_refs")
        if not isinstance(refs, list):
            continue
        for i, e in enumerate(refs):
            if not in_predicate(e):
                continue
            new = clean(e)
            if HEB_NONE in e:
                hit_none[ids[0]] = ids[1]
                none_segments["[%d].boundary_evidence_refs[%d]" % (ri, i)] += e.count(HEB_NONE)
            if any(o in e for o, _ in REPRS):
                hit_repr[ids[0]] = ids[1]
            refs[i] = new
            changes.append({"row": ids[0], "field": "boundary_evidence_refs[%d]" % i, "old": e, "new": new})
            shape.append({"row": ids[0], "index": i, "r1_before": bool(CANON_REF.match(e)), "r1_after": bool(CANON_REF.match(new))})
    problems = []
    left = [(r["decision_id"], e) for r in rows_out for e in r.get("boundary_evidence_refs") or [] if in_predicate(e)]
    if left:
        problems.append("predicate byte sequences left after the clean-up: %s" % left[:5])
    not_r1 = [s for s in shape if not s["r1_after"]]
    if not_r1:
        problems.append("touched entries outside the strict R1 shape after the change: %s" % not_r1[:8])
    other = [ri["decision_id"] for ri, ro in zip(rows_in, rows_out)
             if {k: v for k, v in ri.items() if k != "boundary_evidence_refs"} != {k: v for k, v in ro.items() if k != "boundary_evidence_refs"}]
    if other:
        problems.append("fields other than boundary_evidence_refs changed on %s" % other[:5])

    with tempfile.TemporaryDirectory(dir=scratch, prefix="cwo13_probe_") as td:
        in_probe_sha, rep_in = probe(rows_in, td)
        out_sha, rep_out = probe(rows_out, td)
    cs_n = len(rep_in["citation_sweep"].get("problems", []))
    cm_n = len(rep_in["mark_symmetry"].get("flags", []))
    if canon(rep_in["citation_sweep"].get("problems", [])) != canon(rep_out["citation_sweep"].get("problems", [])):
        problems.append("citation_sweep problems changed")
    if canon(rep_in["mark_symmetry"].get("flags", [])) != canon(rep_out["mark_symmetry"].get("flags", [])):
        problems.append("check_marks flags changed")
    ui, uo = rep_in["universals"], rep_out["universals"]
    u_removed, u_added = claims(ui) - claims(uo), claims(uo) - claims(ui)
    seg_total = sum(none_segments.values())
    claims_drop = ui.get("claims_seen", 0) - uo.get("claims_seen", 0)
    flags_drop = ui.get("flag_count", 0) - uo.get("flag_count", 0)
    unexplained = [[p, c, n] for (p, c), n in u_added.items()] + \
                  [[p, c, n] for (p, c), n in u_removed.items() if c.lower() != "none" or n > none_segments.get(p, 0)]
    u_other = sorted(k for k in set(ui) | set(uo) if k not in UNIV_MAY_MOVE and ui.get(k) != uo.get(k))
    if unexplained or u_other or not 0 <= claims_drop <= seg_total or flags_drop != sum(u_removed.values()):
        problems.append("check_universals moved beyond the removed 'None' placeholders: unexplained %s; other keys %s; claims_seen "
                        "drop %d of at most %d; flag_count drop %d against %d removed" % (unexplained[:6], u_other, claims_drop, seg_total,
                                                                                         flags_drop, sum(u_removed.values())))
    parity = differing(rep_in, rep_out, skip=("universals", "summary"))
    if parity:
        problems.append("suite parity broken: %s" % parity)
    si, so = rep_in.get("summary", {}), rep_out.get("summary", {})
    if si.get("hard_status") != so.get("hard_status") or si.get("nfd_hard_e01") != so.get("nfd_hard_e01") or \
            si.get("triage_flags", 0) - so.get("triage_flags", 0) != flags_drop:
        problems.append("the suite summary moved other than by the universals flags removed: %s -> %s" % (si, so))

    none_ids = set(hit_none) | {w for w in hit_none.values() if w}
    extra = {
        "ruled_order": ruled["order"], "ruled_predicate": ruled["predicate"],
        "rows_by_class": {"hebrew_none": [{"decision_id": d, "writer_decision_id": w} for d, w in sorted(hit_none.items())],
                          "list_repr": [{"decision_id": d, "writer_decision_id": w} for d, w in sorted(hit_repr.items())]},
        "against_the_ruling_today": {"hebrew_none_rows_named": sorted(ruled_none_ids),
                                     "hebrew_none_rows_match": ruled_none_ids <= none_ids and len(hit_none) == len(ruled_none_ids),
                                     "list_repr_rows_stated": ruled_repr_rows, "list_repr_rows_found": len(hit_repr)},
        "predicate_sequences_outside_boundary_evidence_refs_not_edited": outside,
        "assert_no_predicate_sequence_left": not left,
        "assert_r1_shape_after": {"touched_entries": len(shape), "outside_r1_after": len(not_r1),
                                  "outside_r1_before": sum(1 for s in shape if not s["r1_before"])},
        "assert_only_boundary_evidence_refs_changed": not other,
        "assert_citation_sweep_problems_unchanged": {"problems": cs_n},
        "assert_check_marks_flags_unchanged": {"flags": cm_n},
        "assert_suite_parity": {
            "checks_compared": sorted(rep_in),
            "differences_outside_universals_and_summary": parity,
            "universals_accounted": {
                "rule": ("flags compared by (path, claim): only removals of claim 'None' at a touched path, at most one per 'hebrew: None' "
                         "segment removed there; nothing added; claims_seen drops by at most the segments removed; other keys identical; "
                         "the summary's triage count drops by exactly the flags removed"),
                "hebrew_none_segments_removed": seg_total,
                "claims_seen": [ui.get("claims_seen"), uo.get("claims_seen")], "flag_count": [ui.get("flag_count"), uo.get("flag_count")],
                "flags_removed": [{"path": p, "claim": c, "n": n} for (p, c), n in sorted(u_removed.items())],
                "flags_added": [{"path": p, "claim": c, "n": n} for (p, c), n in sorted(u_added.items())]},
            "summary_in": si, "summary_out": so},
        "probe": {"output_sha256": out_sha, "input_bytes_reproduced": in_probe_sha == a.expect_in,
                  "tools_sha256": {n: sha(TOOLS / n) for n in SUITE_TOOLS}},
        "tools_bound_to_install_receipt": tools_bound,
        "old_and_new_bytes_per_change": True,
    }
    if a.dry_run or problems:
        report = {"verdict": ("DRY RUN - nothing written under SP" if not problems else "ABORT - nothing written"), "problems": problems,
                  "changes": changes, "shape": shape} | extra
        rp = scratch / "cwo13_dry_run.json"
        rp.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print(json.dumps({"verdict": report["verdict"], "problems": problems, "change_count": len(changes),
                          "rows_changed": len({c["row"] for c in changes}), "against_the_ruling_today": extra["against_the_ruling_today"],
                          "outside": len(outside), "r1": extra["assert_r1_shape_after"], "parity_differences": parity,
                          "universals": {"segments": seg_total, "claims_seen": [ui.get("claims_seen"), uo.get("claims_seen")],
                                         "flags_removed": sum(u_removed.values()), "flags_added": sum(u_added.values())},
                          "summary_in": si, "summary_out": so, "input_bytes_reproduced": extra["probe"]["input_bytes_reproduced"],
                          "would_write_sha256": out_sha, "report": str(rp)}, ensure_ascii=False, indent=1))
        raise SystemExit(1 if problems else 0)
    mf = write_sweep("CWO-EZ-13", in_path, out_path, rows_in, rows_out, changes, extra,
                     ordered_by=("ezek_controlling_rulings_a1#e4", RULINGS_E4))
    if mf["output"]["sha256"] != out_sha:
        raise SystemExit("ABORT: the written bytes differ from the probed bytes")
    print(json.dumps(summary(mf), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
