"""TF-5 test of CWO-1COR-06 and -07 in cwo_sweep_1cor.py. Each of the ten E4 plants (plants06.py, sha c67ed4a6) mutates the
rows and is run through the sweep itself, the expected change is the plant's own, and the sweep's hits must equal the
reference's (cwo06_ref.py, sha f8dce30c) on every mutated row set. On ROWS the counts must equal the E4 baseline, and with
--pre the sweep's A, B, CWO02, CWO04 and CWO05 must equal the pre-TF-5 tool's on every file given. Writes only under --work.
usage: test_cwo0607.py SWEEP.py ROWS.jsonl --work DIR [--pre OLD_SWEEP.py [--also OTHER_ROWS.jsonl]]
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cwo06_ref as ref  # noqa: E402

PLANT_SHA = "c67ed4a6657955b7f0f0367c9b30dc10ad3e3400df1e11be8078e5809a2c337b"
REF_SHA = "f8dce30cb6ece8c0cc05bb153618248968518ae602952584528b955e1e97c5e3"
BASE = {"hits": 18, "rows": 17, "unlisted": 63, "unlisted_rows": 25, "plants": 10}
args = sys.argv
sweep_py, rows_p, work = Path(args[1]), Path(args[2]), Path(args[args.index("--work") + 1])
pre = Path(args[args.index("--pre") + 1]) if "--pre" in args else None
also = Path(args[args.index("--also") + 1]) if "--also" in args else None
work.mkdir(parents=True, exist_ok=True)
fails, cache = [], {}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run_sweep(script, rows_file, out):
    p = subprocess.run([sys.executable, "-B", str(script), str(rows_file), "--out", str(out)], capture_output=True, text=True,
                       encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if p.returncode:
        raise SystemExit("sweep failed: " + p.stderr[-400:])
    return json.loads(Path(out).read_text(encoding="utf-8"))


def of(rows):
    """The sweep's two lists on ROWS, run through the sweep as a file; checked equal to the reference each time."""
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    k = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if k not in cache:
        p = work / ("rows_%s.jsonl" % k[:12])
        p.write_text(text, encoding="utf-8", newline="\n")
        res = run_sweep(sweep_py, p, work / ("out_%s.json" % k[:12]))
        cache[k] = res["CWO06"]["list"], res["CWO07"]["list"]
        if cache[k] != (ref.sweep06(rows), ref.sweep07(rows)):
            fails.append("sweep differs from the reference on the row set %s" % k[:12])
    return cache[k]


class Shim:
    SP, RP, SBL, DIFF, SITES, toks = ref.SP, ref.RP, ref.SBL, ref.DIFF, ref.SITES, staticmethod(ref.toks)
    sweep06 = staticmethod(lambda rows: of(rows)[0])
    sweep07 = staticmethod(lambda rows: of(rows)[1])


if sha(HERE / "cwo06_ref.py") != REF_SHA:
    fails.append("reference digest")
plants_py = HERE / "plants06.py"
if sha(plants_py) != PLANT_SHA:
    fails.append("plants digest")
src = plants_py.read_text(encoding="utf-8-sig")
src = src[:src.index('print("plants"')].replace("import cwo06_ref as c", "c = SHIM")
saved = list(sys.argv)
g = {"__file__": str(plants_py), "__name__": "plants06", "SHIM": Shim}
exec(compile(src, str(plants_py), "exec"), g)
sys.argv = saved
passed, n = sum(g["ok"]), len(g["ok"])
if (passed, n) != (BASE["plants"], BASE["plants"]):
    fails.append("plants %d of %d" % (passed, n))
res = run_sweep(sweep_py, rows_p, work / "rows_out.json")
got = {"hits": res["CWO06"]["hits"], "rows": res["CWO06"]["rows"], "unlisted": res["CWO07"]["unlisted"],
       "unlisted_rows": res["CWO07"]["rows"]}
for k, v in got.items():
    if BASE[k] != v:
        fails.append("%s %s, baseline %s" % (k, v, BASE[k]))
unchanged = {}
if pre:
    for name, p in (("rows", rows_p), ("also", also)):
        if p is None:
            continue
        a, b = run_sweep(pre, p, work / ("pre_%s.json" % name)), run_sweep(sweep_py, p, work / ("post_%s.json" % name))
        keys = [k for k in ("A", "B", "CWO02", "CWO04", "CWO05") if k in a]
        unchanged[name] = {k: a[k] == b[k] for k in keys}
        if len(keys) != 5 or not all(unchanged[name].values()):
            fails.append("an existing section changed on %s: %s" % (name, unchanged[name]))
print(json.dumps({"plants": n, "plants_pass": passed, "row_sets_run": len(cache), **got, "by_kind": res["CWO06"]["by_kind"],
                  "range_token": res["CWO06"]["range_token"], "unchanged": unchanged, "fails": fails,
                  "verdict": "GREEN" if not fails else "RED"}, ensure_ascii=False))
sys.exit(1 if fails else 0)
