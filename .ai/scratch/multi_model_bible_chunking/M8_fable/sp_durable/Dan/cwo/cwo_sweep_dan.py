"""CWO-DAN-01..04 corpus-wide sweeps, predicates and field scopes READ from the installed controlling rulings (never
retyped). Prints one JSON coverage report per order; CWO-DAN-03 hits carry a proposed disposition that the orchestrator
confirms by hand (never auto-suppressed). usage: cwo_sweep_dan.py rows.jsonl [--out report.json]"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
RUL = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Dan\review"
           r"\dan_controlling_agent_rulings_E1.v1.json")
d = json.loads(RUL.read_text(encoding="utf-8"))
cwo = {c["id"]: c for c in d["corpus_wide_orders"]}
PROSE = ["boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals",
         "literature_type_guess"]
SCOPE = {"CWO-DAN-01": None, "CWO-DAN-02": PROSE + ["boundary_evidence_refs"], "CWO-DAN-03": None,
         "CWO-DAN-04": PROSE}
for k, fields in SCOPE.items():  # the field lists above must be the ones the ruling names
    if fields and not all(f in cwo[k]["fields"] for f in fields):
        raise SystemExit("REFUSED: field scope of %s does not match the ruling text" % k)


def pred(k):
    p = cwo[k]["predicate"]
    m = re.match(r"regex (.*) \(Python re(?:, (IGNORECASE))?(?:, no flags)?\)$", p)
    if not m:
        raise SystemExit("REFUSED: cannot parse predicate of " + k)
    return re.compile(m.group(1), re.I if m.group(2) else 0)


def strings(o, path):
    if isinstance(o, dict):
        for kk, v in o.items():
            yield from strings(v, path + "." + kk)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, "%s[%d]" % (path, i))
    elif isinstance(o, str):
        yield path, o


ZONES = [("MT", 3, 31, 33), ("MT", 4, 1, 34), ("MT", 6, 1, 1), ("MT", 6, 2, 29), ("WEB", 4, 1, 37), ("WEB", 5, 31, 31),
         ("WEB", 6, 1, 28)]


def dispose(match, s, at):
    ctx = s[max(0, at - 40):at]
    if re.search(r"Maccabees|Jeremiah|Ezekiel|Isaiah|Genesis|Revelation|Matthew|Mark|Luke|Ezra|Nehemiah|Chronicles|"
                 r"Kings|Psalm", ctx + match):
        return "other_book?"
    nums = [int(x) for x in re.findall(r"\d+", match)]
    # zone takes precedence over seam_pair: the tail of a pair inside a numbering zone is still a zone ref
    # (the earlier order filed 7 Daniel 4 zone tails as seam_pair; regression: tf/test_cwo_zone_precedence.py)
    if len(nums) >= 2 and any(c == nums[0] and lo <= nums[1] <= hi for _, c, lo, hi in ZONES if c in (3, 4, 5, 6)):
        return "zone?"
    if re.fullmatch(r"\d{1,2}\.\d{1,2}", match) and re.search(r"\d{1,2}\.\d{1,2}\s*/\s*$", ctx):
        return "seam_pair?"
    return "plain?"


rows_path = Path(sys.argv[1])
rows = [json.loads(x) for x in rows_path.read_text(encoding="utf-8").splitlines() if x.strip()]
rep = {"rows_file": str(rows_path), "rows_sha256": hashlib.sha256(rows_path.read_bytes()).hexdigest(),
       "rulings_sha256": hashlib.sha256(RUL.read_bytes()).hexdigest(), "rows": len(rows), "orders": {}}
for k in ("CWO-DAN-01", "CWO-DAN-02", "CWO-DAN-03", "CWO-DAN-04"):
    rx, hits, nstr = pred(k), [], 0
    for r in rows:
        for top, v in r.items():
            if SCOPE[k] is not None and top not in SCOPE[k]:
                continue
            for path, s in strings(v, top):
                nstr += 1
                for m in rx.finditer(s):
                    h = {"row": r["decision_id"], "field": path, "match": m.group(0)}
                    if k == "CWO-DAN-03":
                        h["proposed"] = dispose(m.group(0), s, m.start())
                        h["context"] = s[max(0, m.start() - 50):m.end() + 20]
                    hits.append(h)
    by_row = {}
    for h in hits:
        by_row.setdefault(h["row"], 0)
        by_row[h["row"]] += 1
    rep["orders"][k] = {"strings_scanned": nstr, "hit_count": len(hits), "hits_by_row": by_row, "hits": hits}
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
if out:
    Path(out).write_bytes((json.dumps(rep, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print(json.dumps({k: {"hits": v["hit_count"], "rows": sorted(v["hits_by_row"])} for k, v in rep["orders"].items()}))
