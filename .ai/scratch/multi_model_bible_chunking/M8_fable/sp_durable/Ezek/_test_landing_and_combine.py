#!/usr/bin/env python3
"""Regression test for _land_writer_part.py and _combine_writer_parts.py.

Both tools will process real landings, so both are exercised here first - entirely inside a temp directory, with a
stub capture index, so the real durable tree is never touched.

LANDING HANDLER
  S1  a fresh GREEN draft lands                      -> LANDED, persisted with parity, one receipt, a note
  S2  the identical draft re-lands                    -> no-op; receipt NOT duplicated; existing note NOT overwritten
  S3  DIFFERENT bytes over an already-landed part     -> REFUSED; the durable draft is untouched
  S4  a RED draft (tiling gap) as execution e2        -> LANDED_RED; preserved in writer/red/; NOT promoted
  S5  an OW-8 record naming a different execution     -> REFUSED before anything is written

COMBINE
  C1  parts missing                                   -> REFUSED, naming them
  C2  all eleven parts tile the book                  -> GREEN, 1273 verses exactly once
  C3  one part overruns into the next                 -> RED, OVERLAP reported

Usage: _test_landing_and_combine.py     exit 0 = GREEN, exit 1 = RED
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SP = Path(__file__).resolve().parent
STUB = ('import json, sys\n'
        'print(json.dumps({"verdict": "GREEN", "rows": 0, "distinct_jobs": 0, "problems": []} '
        'if "--check" in sys.argv else {"executions_indexed": 0}))\n')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(script, *args):
    r = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8")
    try:
        return r.returncode, json.loads(r.stdout)
    except Exception:
        return r.returncode, {"_raw": r.stdout[:300], "_err": r.stderr[:300]}


def stage(tmp):
    ez = tmp / "Ezek"
    (ez / "writer").mkdir(parents=True)
    (tmp / "campaign").mkdir()
    (tmp / "campaign" / "_capture_index.py").write_text(STUB, encoding="utf-8")
    for f in ("writer_parts.json", "verse_inventory.json", "pmarks_Ezek.json", "Ezek_oshb.txt",
              "_validate_writer_part.py", "_land_writer_part.py", "_combine_writer_parts.py"):
        shutil.copy(SP / f, ez / f)
    return ez


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    real_p01 = SP / "writer" / "draft_p01.jsonl"
    if not real_p01.is_file():
        print(json.dumps({"verdict": "RED", "why": "needs the landed pilot draft writer/draft_p01.jsonl as a fixture"}))
        return 1
    checks = []
    tmp = Path(tempfile.mkdtemp())
    try:
        # ================= LANDING HANDLER =================
        ez = stage(tmp)
        land = ez / "_land_writer_part.py"
        src = tmp / "incoming_p01.jsonl"
        shutil.copy(real_p01, src)
        rec = tmp / "rec_e1.json"
        rec.write_text(json.dumps({"execution_id": "ezek_writer_p01_a1#e1", "outcome": {"changed": [{"what": "rows"}]},
                                   "e19_selfreport": "ran no listing, no glob"}), encoding="utf-8")
        receipts = ez / "writer" / "ezek_writer_attempt_receipts.jsonl"
        note = ez / "evidence_notes" / "ezek_writer_p01_a1%23e1.json"

        rc, o = run(land, "--part", "p01", "--source", str(src), "--record", str(rec), "--tokens", "1")
        durable = ez / "writer" / "draft_p01.jsonl"
        checks += [
            ("S1 fresh GREEN draft is LANDED", rc == 0 and o.get("verdict") == "LANDED"),
            ("S1 persisted with parity", durable.is_file() and sha(durable) == sha(src)),
            ("S1 exactly one receipt", receipts.is_file() and len(receipts.read_text(encoding="utf-8").splitlines()) == 1),
            ("S1 evidence note written", note.is_file()),
        ]

        n = json.loads(note.read_text(encoding="utf-8"))
        n["sentinel"] = "richer existing note"
        note.write_text(json.dumps(n), encoding="utf-8")
        rc, o = run(land, "--part", "p01", "--source", str(src), "--record", str(rec), "--tokens", "1")
        checks += [
            ("S2 identical re-land is a no-op", rc == 0 and any("identical bytes" in x for x in o.get("actions", []))),
            ("S2 receipt NOT duplicated", len(receipts.read_text(encoding="utf-8").splitlines()) == 1),
            ("S2 existing evidence note NOT overwritten",
             json.loads(note.read_text(encoding="utf-8")).get("sentinel") == "richer existing note"),
        ]

        before = sha(durable)
        rows = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
        rows[0]["boundary_rationale"] += " x"
        mod = tmp / "modified_p01.jsonl"
        mod.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        rc, o = run(land, "--part", "p01", "--source", str(mod), "--record", str(rec), "--tokens", "1")
        checks += [
            ("S3 different bytes over a landed part are REFUSED", rc == 1 and o.get("verdict") == "REFUSED"),
            ("S3 the durable draft is untouched", sha(durable) == before),
        ]

        red_rows = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()][:-1]
        red_src = tmp / "red_p01.jsonl"
        red_src.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in red_rows), encoding="utf-8")
        rec2 = tmp / "rec_e2.json"
        rec2.write_text(json.dumps({"execution_id": "ezek_writer_p01_a1#e2"}), encoding="utf-8")
        rc, o = run(land, "--part", "p01", "--source", str(red_src), "--record", str(rec2), "--tokens", "1",
                    "--execution", "e2")
        red_file = ez / "writer" / "red" / "draft_p01.e2.jsonl"
        checks += [
            ("S4 a RED draft is LANDED_RED", rc == 2 and o.get("verdict") == "LANDED_RED"),
            ("S4 the RED draft is preserved, not discarded", red_file.is_file() and sha(red_file) == sha(red_src)),
            ("S4 the RED draft is NOT promoted over the green one", sha(durable) == before),
        ]

        rc, o = run(land, "--part", "p01", "--source", str(src), "--record", str(rec), "--tokens", "1",
                     "--execution", "e2")
        checks += [
            ("S5 a record naming another execution is REFUSED", rc == 1 and o.get("verdict") == "REFUSED"
             and any("not" in x for x in o.get("refusals", []))),
        ]

        # ================= COMBINE =================
        shutil.rmtree(tmp / "Ezek")
        shutil.rmtree(tmp / "campaign")
        ez = stage(tmp)
        comb = ez / "_combine_writer_parts.py"
        rc, o = run(comb)
        checks += [("C1 missing parts are REFUSED and named",
                    rc == 1 and o.get("verdict") == "REFUSED" and len(o.get("missing", [])) == 11)]

        parts = json.loads((ez / "writer_parts.json").read_text(encoding="utf-8"))["rows"]
        for p in parts:
            row = {"decision_id": "%s-001" % p["part_id"].upper(), "span": p["web_range"], "confidence": "low"}
            (ez / "writer" / ("draft_%s.jsonl" % p["part_id"])).write_text(json.dumps(row) + "\n", encoding="utf-8")
        rc, o = run(comb)
        checks += [("C2 eleven tiling parts combine GREEN over 1273 verses",
                    rc == 0 and o.get("verdict") == "GREEN" and o.get("verses_covered") == 1273 and o.get("rows") == 11)]

        p02 = ez / "writer" / "draft_p02.jsonl"
        row = json.loads(p02.read_text(encoding="utf-8"))
        row["span"] = "Ezek.8.1-Ezek.15.1"
        p02.write_text(json.dumps(row) + "\n", encoding="utf-8")
        rc, o = run(comb)
        checks += [("C3 an overrun into the next part is RED with OVERLAP",
                    rc == 1 and o.get("verdict") == "RED" and any("OVERLAP" in x for x in o.get("problems", [])))]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [n for n, ok in checks if not ok]
    print(json.dumps({"checks": len(checks), "passed": len(checks) - len(failed), "failed": failed,
                      "results": [{"check": n, "ok": ok} for n, ok in checks],
                      "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
