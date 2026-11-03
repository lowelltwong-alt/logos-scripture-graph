"""Apply a controlling round's byte-exact fix-up orders directly from its rulings file (TOKEN_ECONOMY_RULES TE-1).

Use only when every author order in the rulings carries exact spans: the words are the controlling agent's, so a mechanical
apply has no transcription step and no author lane. The tool refuses when any author order has no exact span, when a span does
not occur exactly once, or when a change falls outside the orders' licences. The next check still runs in full.

usage (cwd anywhere):
  python -B campaign/_apply_exact_orders.py --book 1Cor --rulings R.json --rows IN.jsonl --rows-sha SHA --out-rows OUT.jsonl
      --stage fixup4_applied --range 1Cor.1.1-1Cor.16.24 --sweep review/cwo_sweep_1cor.py --work DIR [--dry-run]
Writes OUT and OUT with .manifest.json. Prints one JSON object.
"""
import argparse, copy, hashlib, json, os, re, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
SP = Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).resolve().relative_to(SP.parent.parent.parent.parent.parent)).replace("\\", "/")


def line(r):
    return json.dumps(r, ensure_ascii=False) + "\n"


def count(obj, s):
    if isinstance(obj, str):
        return obj.count(s)
    if isinstance(obj, list):
        return sum(count(x, s) for x in obj)
    if isinstance(obj, dict):
        return sum(count(v, s) for v in obj.values())
    return 0


def sub(obj, old, new):
    if isinstance(obj, str):
        return obj.replace(old, new)
    if isinstance(obj, list):
        return [sub(x, old, new) for x in obj]
    if isinstance(obj, dict):
        return {k: sub(v, old, new) for k, v in obj.items()}
    return obj


def apply_span(rows, sp, ruling):
    row = rows.get(sp["row"])
    if row is None:
        raise SystemExit("REFUSED: no row %s (%s)" % (sp["row"], ruling))
    m = re.fullmatch(r"(\w+)\[(\d+)\]", sp["field"])
    name, idx = (m.group(1), int(m.group(2))) if m else (sp["field"], None)
    if name not in row:
        raise SystemExit("REFUSED: %s has no field %s (%s)" % (sp["row"], name, ruling))
    if "append" in sp:
        if not isinstance(row[name], list) or idx is not None:
            raise SystemExit("REFUSED: append needs a whole list field (%s)" % ruling)
        row[name].append(sp["append"])
        return (sp["row"], name, len(row[name]) - 1)
    old, new = sp["replace_exactly_once"], sp["with"]
    target = row[name] if idx is None else row[name][idx]
    n = count(target, old)
    if n != 1:
        raise SystemExit("REFUSED: span found %d times in %s.%s (%s): %s" % (n, sp["row"], sp["field"], ruling, old[:60]))
    if idx is None:
        row[name] = sub(target, old, new)
        return (sp["row"], name, None)
    row[name][idx] = sub(target, old, new)
    return (sp["row"], name, idx)


def diff(pre, post):
    out = set()
    if set(pre) != set(post):
        raise SystemExit("REFUSED: row id set changed")
    for rid, a in pre.items():
        b = post[rid]
        if list(a) != list(b):
            raise SystemExit("REFUSED: key order or key set changed in %s" % rid)
        for k in a:
            if a[k] == b[k]:
                continue
            if isinstance(a[k], list) and isinstance(b[k], list):
                for i in range(max(len(a[k]), len(b[k]))):
                    if i >= len(a[k]) or i >= len(b[k]) or a[k][i] != b[k][i]:
                        out.add((rid, k, i))
            else:
                out.add((rid, k, None))
    return out


def checks(f, work, bk, rng, sweep):
    def run(*x):
        return subprocess.run([sys.executable, "-B", *[str(v) for v in x]], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(work))

    def jsn(s):
        try:
            return json.loads(s[s.index("{"):])
        except ValueError:
            return {}

    s = jsn(run(bk / "tools/run_validator_suite.py", f).stdout)
    per = s.get("per_check")
    if not isinstance(per, dict) or not per:
        raise SystemExit("REFUSED: the suite printed no per_check")
    out = {"suite": {"hard_status": s.get("hard_status"), "triage_flags": s.get("triage_flags"),
                     "not_green": {k: v for k, v in per.items() if v != "GREEN" and not (k == "greek_normalize_dryrun" and "defects=0" in v)}}}
    if "refs_mirror" in out["suite"]["not_green"]:
        rep = json.loads(Path(str(f) + ".validator_report.json").read_text(encoding="utf-8"))
        out["suite"]["refs_mirror_worklist"] = [[x.get("decision_id"), x.get("citation")] if isinstance(x, dict) else x for x in rep["refs_mirror"]["worklist_citations"]]
    n = jsn(run(bk / "tools/ngram7.py", f, "--gate", "10", "--full-ids").stdout)
    out["ngram7"] = {"status": n.get("status"), "offending": n.get("offending_7grams")}
    t = run(bk / "tools/check_tiling.py", f, "--range", rng)
    out["tiling"] = {"rc": t.returncode, "tail": t.stdout.strip()[-120:]}
    sw = Path(str(f) + ".cwo.json")
    w = run(sweep, f, "--out", sw)
    if w.returncode != 0:
        raise SystemExit("REFUSED: sweep rc %d %s" % (w.returncode, w.stderr[-200:]))
    c = json.loads(sw.read_text(encoding="utf-8"))
    out["sweep"] = {"A": c["A"]["hits"], "B": c["B"]["hits"], "CWO02": c["CWO02"]["fail"], "CWO04": c["CWO04"]["by_class"], "CWO05": c["CWO05"]["hits"],
                    "CWO06": c["CWO06"]["hits"], "CWO07": c["CWO07"]["unlisted"]}
    return out


ap = argparse.ArgumentParser()
for k in ("--book", "--rulings", "--rows", "--rows-sha", "--out-rows", "--stage", "--range", "--sweep", "--work"):
    ap.add_argument(k, required=True)
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
bk = SP / a.book
if sha(a.rows) != a.rows_sha:
    raise SystemExit("REFUSED: rows digest %s" % sha(a.rows)[:12])
raw = Path(a.rows).read_text(encoding="utf-8").splitlines(keepends=True)
order = [json.loads(x) for x in raw]
if [line(r) for r in order] != raw:
    raise SystemExit("REFUSED: the rows file does not round-trip byte for byte")
pre = {r["decision_id"] if "decision_id" in r else r["id"]: r for r in order}
if len(pre) != len(order):
    raise SystemExit("REFUSED: duplicate row ids")
post = copy.deepcopy(pre)
rul = json.loads(Path(a.rulings).read_text(encoding="utf-8"))
touched, spans = set(), 0
for ru in rul["rulings"]:
    for o in ru.get("orders") or []:
        if not o["to"].startswith("author_fixup"):
            continue
        if not o.get("exact_spans"):
            raise SystemExit("REFUSED: %s has an author order with no exact span; this tool does not apply it" % ru["id"])
        for sp in o["exact_spans"]:
            touched.add(apply_span(post, sp, ru["id"]))
            spans += 1
moved = diff(pre, post)
if moved - touched or touched - moved:
    raise SystemExit("REFUSED: changed elements differ from licensed elements: %s" % sorted(map(str, moved ^ touched))[:6])
# Resolved: the checks run with cwd=work, so a relative --work would name its own files from inside itself.
work = Path(a.work).resolve()
os.makedirs(work, exist_ok=True)
before, after = work / "before.jsonl", work / "after.jsonl"
before.write_bytes(Path(a.rows).read_bytes())
after.write_text("".join(line(post[k]) if k in post else "" for k in pre), encoding="utf-8", newline="\n")
res_pre = checks(before, work, bk, a.range, SP.joinpath(a.book, a.sweep))
res_post = checks(after, work, bk, a.range, SP.joinpath(a.book, a.sweep))
same = {k: res_pre["sweep"][k] == res_post["sweep"][k] for k in ("CWO04", "CWO05", "CWO06", "CWO07")}
result = {"spans_applied": spans, "elements_changed": len(moved), "rows_changed": len({x[0] for x in moved}), "rows_total": len(pre),
          "unchanged_rows_byte_equal": sum(1 for k in pre if pre[k] == post[k]), "pre": res_pre, "post": res_post, "sweep_equal_to_pre": same}
ok = res_post["suite"]["hard_status"] == "GREEN" and res_post["ngram7"]["status"] == "GREEN" and res_post["tiling"]["rc"] == 0 and res_post["sweep"]["CWO07"] == 0
result["ok"] = ok
if ok and not a.dry_run:
    Path(a.out_rows).write_bytes(after.read_bytes())
    man = str(a.out_rows).replace(".jsonl", ".manifest.json")
    Path(man).write_text(json.dumps({"schema": "m8_rows_manifest.v1", "book": a.book, "stage": a.stage, "method": "deterministic apply from the rulings' exact spans; no author lane",
                                     "applied_by": "campaign/_apply_exact_orders.py", "tool_sha256": sha(__file__),
                                     "source_rows": {"path": rel(a.rows), "sha256": a.rows_sha}, "rulings": {"path": rel(a.rulings), "sha256": sha(a.rulings)},
                                     "elements_changed": sorted([list(x) for x in moved], key=str), "applied": sha(a.out_rows), "suite_on_copy": res_post},
                                    ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    result["applied_sha256"] = sha(a.out_rows)
print(json.dumps(result, ensure_ascii=False))
