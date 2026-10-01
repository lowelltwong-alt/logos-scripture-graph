#!/usr/bin/env python3
"""OW-2 item-4 fresh full sweep after a repair wave (Lam, m8-mesh-r3 + OW-1; the Jer build re-keyed to Lam.N.N spans and the Lam.1.1-Lam.5.22 range).

The repair authors are never the final checkers: this orchestrator-run tool
builds a SIMULATED post-wave corpus (frozen corpus + the wave's author
patch files, applied in memory), writes it to a PRIVATE out dir (never the
shared SP), and runs the FULL fresh sweep over it: the 10-member Tier-0
suite + the E-23 punctuation-boundary sweep + whole-book tiling. FLAGS
members are reported as DELTAS against a fresh baseline run over the
frozen corpus, so wave-introduced candidates stand out (second-generation
detection, deterministic arm).

Usage: _wave_repair_sweep.py OUT_DIR author_aNN.jsonl [more patch files...]
Exit 1 on any HARD failure or tiling break; deltas are triage flags.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
SPAN = re.compile(r"^Lam\.(\d+)\.(\d+)-Lam\.(\d+)\.(\d+)$")


def span_key(row):
    m = SPAN.match(row["span"])
    assert m, f"bad span {row.get('span')} on {row.get('decision_id')}"
    return (int(m.group(1)), int(m.group(2)))


def load_rows(p: Path):
    return [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines()
            if l.strip()]


def run_suite(rows_path: Path):
    r = subprocess.run([sys.executable, str(TOOLS / "run_validator_suite.py"),
                        str(rows_path)], capture_output=True, text=True,
                       encoding="utf-8")
    rep_path = rows_path.with_name(rows_path.name + ".validator_report.json")
    rep = json.loads(rep_path.read_text(encoding="utf-8-sig"))
    return rep


def flags_count(rep):
    out = {}
    for name, m in rep.get("members", rep).items() if isinstance(rep, dict) else []:
        if isinstance(m, dict):
            for k in ("flag_count", "flags", "count"):
                if isinstance(m.get(k), int):
                    out[name] = m[k]
                    break
    return out


def main():
    args = list(sys.argv[1:])
    base_name = "draft_rows_combined.jsonl"   # default unchanged (author waves); opt-in --base <file> for later waves (2026-09-06 s3: CWO wave over rows_v2)
    if "--base" in args:
        i = args.index("--base"); base_name = args[i + 1]; args = args[:i] + args[i + 2:]
    out_dir = Path(args[0])
    patches = [Path(a) for a in args[1:]]
    assert patches, "no patch files given"
    out_dir.mkdir(parents=True, exist_ok=True)

    frozen = load_rows(HERE / base_name)
    by_id = {r["decision_id"]: r for r in frozen}
    n0 = len(frozen)
    applied = {"replace": 0, "retire": 0, "new_row": 0}
    for p in patches:
        for obj in load_rows(p):
            op = obj.pop("_op")
            rid = obj.get("decision_id") or obj.get("writer_decision_id")
            if op == "replace":
                assert rid in by_id, f"replace target {rid} missing"
                by_id[rid] = obj
            elif op == "retire":
                assert rid in by_id, f"retire target {rid} missing"
                del by_id[rid]
            elif op == "new_row":
                assert rid not in by_id, f"new_row {rid} already exists"
                by_id[rid] = obj
            applied[op] += 1
    sim = sorted(by_id.values(), key=span_key)
    for i, r in enumerate(sim, 1):
        r["chunk_index_in_book"] = i

    sim_path = out_dir / "sim_wave_corpus.jsonl"
    with open(sim_path, "w", encoding="utf-8") as f:
        for r in sim:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    tiling = subprocess.run([sys.executable, str(TOOLS / "check_tiling.py"),
                             str(sim_path), "--range", "Lam.1.1-Lam.5.22"],
                            capture_output=True, text=True, encoding="utf-8")
    tiling_ok = tiling.returncode == 0

    base_path = out_dir / "baseline_frozen.jsonl"
    base_path.write_bytes((HERE / base_name).read_bytes())
    rep_base = run_suite(base_path)
    rep_sim = run_suite(sim_path)

    punct = {}
    for name, path in (("baseline", base_path), ("sim", sim_path)):
        pr = subprocess.run([sys.executable, str(TOOLS / "_punct_boundary_sweep.py"),
                             str(path)], capture_output=True, text=True,
                            encoding="utf-8")
        try:
            punct[name] = json.loads(pr.stdout).get("flag_count")
        except json.JSONDecodeError:
            punct[name] = f"unparseable: {pr.stdout[-120:]}"

    MEMBERS = ["citation_sweep", "hebrew_normalize_dryrun", "web_quotes",
               "refs_mirror", "mark_symmetry", "universals", "language_zones",
               "ngram7", "cap_sweep", "register"]

    def member_status(rep, m):
        v = rep.get(m)
        return v.get("status") if isinstance(v, dict) else v

    base_status = rep_base.get("summary", {}).get("hard_status")
    sim_status = rep_sim.get("summary", {}).get("hard_status")
    statuses = {m: {"baseline": member_status(rep_base, m),
                    "sim": member_status(rep_sim, m)} for m in MEMBERS}
    # a HARD member RED on sim but not on baseline = wave-introduced failure;
    # RED on both (e.g. the standing ngram7 CWO-1 condition) is recorded, not
    # failed here — its cure is the ordered corpus-wide sweep
    sim_only_red = [m for m in MEMBERS
                    if statuses[m]["sim"] == "RED"
                    and statuses[m]["baseline"] != "RED"]
    nfd_hard = bool(rep_sim.get("summary", {}).get("nfd_hard_e01"))

    def flags_only(rep):
        out = {}
        for m in MEMBERS:
            v = rep.get(m)
            if isinstance(v, dict) and isinstance(v.get("flag_count"), int):
                out[m] = v["flag_count"]
        return out

    base_flags = flags_only(rep_base)
    sim_flags = flags_only(rep_sim)
    deltas = {k: sim_flags.get(k, 0) - base_flags.get(k, 0)
              for k in set(base_flags) | set(sim_flags)
              if sim_flags.get(k, 0) != base_flags.get(k, 0)}

    hard_fail = (not tiling_ok) or bool(sim_only_red) or nfd_hard
    print(json.dumps({
        "sweep": "FAIL" if hard_fail else "PASS",
        "applied": applied, "rows": {"before": n0, "after": len(sim)},
        "tiling": "GREEN" if tiling_ok else
                  f"RED: {(tiling.stdout or tiling.stderr)[-300:]}",
        "hard_status": {"baseline": base_status, "sim": sim_status},
        "sim_only_red_members": sim_only_red,
        "red_on_both_recorded_not_failed": [
            m for m in MEMBERS if statuses[m]["sim"] == "RED"
            and statuses[m]["baseline"] == "RED"],
        "member_statuses": statuses,
        "flags_delta_sim_minus_baseline": deltas,
        "punct_e23": punct,
        "reports": {"sim": str(sim_path) + ".validator_report.json",
                    "baseline": str(base_path) + ".validator_report.json"}},
        ensure_ascii=False, indent=1))
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
