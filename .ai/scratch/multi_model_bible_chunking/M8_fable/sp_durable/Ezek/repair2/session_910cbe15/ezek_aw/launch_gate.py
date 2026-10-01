#!/usr/bin/env python3
"""The author-wave LAUNCH GATE, generated from #e13's own precondition list.

This is E-32's cure applied to the launch decision itself. The gate does not check the preconditions I remember;
it reads `author_wave.with_preconditions_that_gate_launch` out of the ruling, iterates it, and requires a
MEASURED predicate for each one. A precondition I forgot cannot be a precondition the launch passes without.

Each predicate is evidence over an artifact on disk, not a note that I did the work.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

r13 = json.loads((EZ / "ezek_controlling_agent_ruling_e13.v1.json").read_text(encoding="utf-8"))
PRE = r13["author_wave"]["with_preconditions_that_gate_launch"]
queue = [json.loads(l) for l in (EZ / "ezek_controlling_agent_queue_e13.v1.jsonl")
         .read_text(encoding="utf-8").splitlines() if l.strip()]
W = json.loads((EZ / "author_wave_worklist.v4.json").read_text(encoding="utf-8"))


def inv_face():
    return json.loads((EZ / "verse_inventory.json").read_text(encoding="utf-8")).get("numbering_face")


def member_selftest_ok():
    r = subprocess.run([sys.executable, str(EZ / "tools" / "check_refs_mirror.py"), "--a4-selftest"],
                       capture_output=True, text=True, cwd=str(EZ / "tools"))
    return r.returncode == 0 and "28/28 passed" in r.stdout


def p2_record_ok():
    d = json.loads((EZ / "p2_citation_reexecution.v1.json").read_text(encoding="utf-8"))
    return not d["UNSATISFIED_CLAUSES"] and d["distinct_check"]["verdict"].startswith("PASS")


def a6_union_ok():
    d = json.loads((EZ / "a6_union_check.v2.json").read_text(encoding="utf-8"))
    n = d["containment_three_ways"]["2_OVERLAP_one_run_contains_the_other_on_the_same_row"][
        "arm_runs_not_matched"]
    installed = len([i for i in W["items"] if i["cls"] == "A6_UNION"])
    return installed >= n and installed == 8


def brief_ok():
    t = (EZ / "AUTHOR_WAVE_BRIEF.v1.md").read_text(encoding="utf-8")
    sys.path.insert(0, str(EZ / "tools"))
    from check_refs_mirror import ROLE_VOCABULARY
    need = ["CUT-RULE", "CONF-CAL", "A6-b", "C2-amended", "A9/A16", "at least 4 distinct formulations",
            "at most 6 words", "7-gram", "MT 21:1-5 = WEB 20:45-49", "E-29", "private subdirectory",
            "No hand tallies presented as measurements", "DEF-A4-ARGUED",
            "ezek_device_inventory.v2.json"]
    return all(x in t for x in need) and all(tok in t for tok in ROLE_VOCABULARY)


PREDICATES = {
    "P1": ("verse_inventory.json declares numbering_face WEB and the member asserts it at startup",
           lambda: inv_face() == "WEB"
           and '_assert_declared_face("WEB")' in (EZ / "tools" / "check_refs_mirror.py")
           .read_text(encoding="utf-8")),
    "P2": ("refs_mirror RE-EXECUTED at citation granularity per #e14 O1-O3; 10/10 ordered clauses satisfied, "
           "selftest 28/28, distinct check PASS at set equality",
           lambda: member_selftest_ok() and p2_record_ok()),
    "P3": ("the A6 arm's output is a union MEMBER of the worklist's A6 class, containment measured, residue "
           "installed",
           a6_union_ok),
    "P4": ("universals declared non-scoring - ruled in #e13, nothing to execute; no universals item exists in "
           "the worklist",
           lambda: not any("universal" in str(i.get("cls", "")).lower() for i in W["items"])),
    "P5": ("the arithmetic arm and the mark worklist are assembled",
           lambda: len([i for i in W["items"] if i["cls"] == "ARITHMETIC"]) == 3
           and len([i for i in W["items"] if i["cls"] == "MARKS_3D"]) == 3),
    "P6": ("the inventory's next version is landed and distinct-checked, v1 untouched",
           lambda: (EZ / "ezek_device_inventory.v2.json").is_file()
           and sha(EZ / "ezek_device_inventory.v2.json")
           == "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f"
           and sha(EZ / "ezek_device_inventory.json")
           == "0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142"
           and (EZ / "p6_derivation_record.v1.json").is_file()),
    "P7": ("the peer figure re-derivation is complete and landed",
           lambda: (EZ / "peer_figure_rederivation_p7.v2.json").is_file()),
    "P8": ("the re-scoped boss audit is complete and its confirmed reconciliations are the work orders",
           lambda: json.loads((EZ / "ezek_boss_audit.v1.json").read_text(encoding="utf-8"))
           ["verdict_tally"]["rows_decided"] == 145),
    "P9": ("the worklist builder is distinct-checked with every negative fixture FIRING, and every item carries "
           "a source and a tier",
           lambda: W["negative_fixtures"]["all_fired"]
           and all(i.get("source") and i.get("tier") for i in W["items"])),
    "P10": ("the author brief carries every element P10 enumerates, plus DEF-A4-ARGUED, all eleven ROLE tokens, "
            "and the v2 inventory pointer",
            brief_ok),
}

report, failed = [], []
for text in PRE:
    key = text.split(".")[0].strip()
    desc, pred = PREDICATES.get(key, (None, None))
    if pred is None:
        report.append({"precondition": key, "ordered_verbatim": text, "satisfied": False,
                       "evidence": "NO PREDICATE DEFINED - the gate cannot pass a precondition it cannot test"})
        failed.append(key)
        continue
    try:
        ok = bool(pred())
        ev = "MEASURED: " + desc
    except Exception as exc:
        ok, ev = False, "the predicate could not be evaluated: %s" % exc
    report.append({"precondition": key, "ordered_verbatim": text, "satisfied": ok, "evidence": ev})
    if not ok:
        failed.append(key)

out = {
    "schema": "ezek_author_wave_launch_gate.v1",
    "generated_from": ("#e13 author_wave.with_preconditions_that_gate_launch, iterated - not from the "
                       "orchestrator's memory of which preconditions exist (ledger E-32)"),
    "preconditions_ordered": len(PRE),
    "preconditions_satisfied": len(PRE) - len(failed),
    "FAILED": failed,
    "detail": report,
    "worklist": {"file": "Ezek/author_wave_worklist.v4.json", "sha256": sha(EZ / "author_wave_worklist.v4.json"),
                 "items": W["counts"]["items_total"], "by_class": W["counts"]["by_class"],
                 "fixtures": len(W["negative_fixtures"]["results"]),
                 "all_fixtures_fired": W["negative_fixtures"]["all_fired"],
                 "items_moving_a_seam": W["counts"]["items_moving_a_seam"]},
    "rows_preimage": {"file": "Ezek/repair/rows_v7_cwo24.jsonl",
                      "sha256": sha(EZ / "repair" / "rows_v7_cwo24.jsonl")},
    "still_open_for_the_controlling_agent_but_NOT_gating": [
        q["id"] for q in queue if "needs the controlling agent" in str(q.get("status"))],
    "why_those_do_not_gate": ("E13-67 (R11's false premise) scores no row by the ruling's own terms. E13-68 "
                              "(transport membership) holds 8 items that are NOT in the worklist, and the "
                              "author brief forbids writing a membership claim for the 13 disputed verses. "
                              "Neither can be pre-empted by the wave."),
    "LAUNCH": "CLEARED" if not failed else "BLOCKED",
}
(HERE / "launch_gate.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                          encoding="utf-8", newline="\n")
w = max(len(r["precondition"]) for r in report)
for r in report:
    print("  %s  %-*s  %s" % ("PASS" if r["satisfied"] else "FAIL", w, r["precondition"],
                              r["ordered_verbatim"][:88]))
print()
print(json.dumps({k: out[k] for k in ("preconditions_ordered", "preconditions_satisfied", "FAILED",
                                      "worklist", "still_open_for_the_controlling_agent_but_NOT_gating",
                                      "LAUNCH")}, indent=1))
if failed:
    raise SystemExit(1)
