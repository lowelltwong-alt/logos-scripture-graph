"""S1-07 fixtures for the ngram7 device-key strip, run on scratch copies of the rows (E-67).
F1: current combined rows GREEN; the gram "month or day word not a date" is not an offender.
F2: equality. Per row: stripped grams are a subset of unstripped grams (no new gram), and every gram lost by the strip
    contains a token of a key that occurs in that row (so it overlaps a key occurrence). Globally: for every gram that
    is not lost in any row, the row set is identical with and without the strip; the per-row union equals the tool's own
    --dump-grams output in both modes.
F3: must-still-fail. Ten synthetic rows sharing the spaced prose "month or day word not a date", no key identifier: RED.
    Control: the same ten rows with the key identifier instead go GREEN.
Writes fixtures_s1_07.result.json; prints one line."""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TOOLS = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Dan\tools")
NG = TOOLS / "ngram7.py"
ROWS = HERE / "rows.jsonl"
GRAM = "month or day word not a date"
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")


def run(*args):
    p = subprocess.run([sys.executable, "-B", str(NG), *map(str, args)], capture_output=True, text=True,
                       encoding="utf-8", env=ENV)
    return json.loads(p.stdout), p.returncode


res = {"ngram7_sha256": hashlib.sha256(NG.read_bytes()).hexdigest(),
       "rows_sha256": hashlib.sha256(ROWS.read_bytes()).hexdigest()}

# F1
f1, rc1 = run(ROWS)
off = [o["gram"] for o in f1["offending_7grams"]]
res["F1"] = {"status": f1["status"], "rc": rc1, "device_keys_stripped": f1["device_keys_stripped"],
             "offenders": off, "worst_reuse": f1["worst_reuse"][:3],
             "pass": f1["status"] == "GREEN" and GRAM not in off and f1["device_keys_stripped"] == 72}
base, _ = run(ROWS, "--no-key-strip")
res["F1"]["pre_strip_status"] = base["status"]
res["F1"]["pre_strip_offenders"] = [(o["gram"], o["rows"]) for o in base["offending_7grams"]]

# F2
sys.path.insert(0, str(TOOLS))
import ngram7 as N  # noqa: E402

keys_re, _ = N.device_key_pattern()
web, _ = N.load_verse_maps()
wt = re.findall(r"[a-z]+", N.norm_english(" ".join(d["text"] for d in web.values())).lower())
W7 = {" ".join(wt[i:i + 7]) for i in range(len(wt) - 6)}


def grams_of(segs):
    out = set()
    for seg in segs:
        seg = N.HEB_RUN.sub(" ", seg)
        seg = re.sub(r"“[^”]*”", " ", seg)
        seg = N.REF_TOKENS.sub(" ", seg)
        t = re.findall(r"[a-z]+", N.norm_english(seg).lower())
        out |= {" ".join(t[i:i + 7]) for i in range(len(t) - 6)} - W7
    return out


rows = [json.loads(x) for x in ROWS.read_text(encoding="utf-8").splitlines() if x.strip()]
g_s, g_u, lost_any, bad = {}, {}, set(), []
for r in rows:
    rid, s = r["decision_id"], N.prose(r)
    A, B = grams_of(keys_re.split(s)), grams_of([s])
    ktoks = set()
    for m in keys_re.finditer(s):
        ktoks |= set(m.group(0).lower().split("_"))
    if A - B:
        bad.append({"row": rid, "new_grams": sorted(A - B)[:3]})
    for g in B - A:
        lost_any.add(g)
        if not set(g.split()) & ktoks:
            bad.append({"row": rid, "lost_without_key_token": g})
    for g in A:
        g_s.setdefault(g, set()).add(rid)
    for g in B:
        g_u.setdefault(g, set()).add(rid)
diff = [g for g in g_u if g not in lost_any and g_u[g] != g_s.get(g, set())]
d_s, _ = run(ROWS, "--dump-grams")
d_u, _ = run(ROWS, "--dump-grams", "--no-key-strip")
tool_match = ({g: sorted(v) for g, v in g_s.items()} == d_s and {g: sorted(v) for g, v in g_u.items()} == d_u)
res["F2"] = {"grams_stripped": len(g_s), "grams_unstripped": len(g_u), "grams_lost": len(lost_any),
             "violations": bad[:10], "non_overlapping_rowset_diffs": diff[:10], "per_row_union_equals_tool": tool_match,
             "gram_left_offender_list": GRAM in lost_any or len(g_s.get(GRAM, ())) < 10,
             "pass": not bad and not diff and tool_match}

# F3
syn = HERE / "syn_spaced.jsonl"
syn_k = HERE / "syn_key.jsonl"
syn.write_text("".join(json.dumps({"decision_id": "SYN-%02d" % i, "rationale":
                                   "Case %d: the month or day word not a date appears in note %d." % (i, i)}) + "\n"
                       for i in range(10)), encoding="utf-8")
syn_k.write_text("".join(json.dumps({"decision_id": "SYN-%02d" % i, "rationale":
                                     "Case %d: the month_or_day_word_not_a_date appears in note %d." % (i, i)}) + "\n"
                         for i in range(10)), encoding="utf-8")
f3, rc3 = run(syn)
f3k, _ = run(syn_k)
res["F3"] = {"spaced_status": f3["status"], "rc": rc3, "spaced_offenders": [o["gram"] for o in f3["offending_7grams"]],
             "control_key_status": f3k["status"],
             "pass": f3["status"] == "RED" and GRAM in [o["gram"] for o in f3["offending_7grams"]]
             and f3k["status"] == "GREEN"}
res["ALL_PASS"] = all(res[k]["pass"] for k in ("F1", "F2", "F3"))
(HERE / "fixtures_s1_07.result.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("ALL_PASS", res["ALL_PASS"], "| F1", res["F1"]["pass"], res["F1"]["pre_strip_status"], "->", f1["status"],
      "| F2", res["F2"]["pass"], len(bad), len(diff), tool_match, "| F3", res["F3"]["pass"])
