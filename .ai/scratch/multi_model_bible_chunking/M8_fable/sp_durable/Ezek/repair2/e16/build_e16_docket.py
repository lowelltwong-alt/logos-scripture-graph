#!/usr/bin/env python3
"""#e16 DOCKET COLLECTOR: every item any record routes to #e16, gathered from the record itself, with its source path.

Why a collector and not a summary: routings to #e16 are written in the e13 queue, in #e15, and in each REPAIR-2
adjudication, in different shapes (strings, dicts, list entries). A docket typed from memory repeats E-38 (the census
cannot see what was not recorded where it looks) and the E-35 addendum (a count carried without its members). This
walks each named record, keeps the SMALLEST enclosing entry that mentions #e16, and dedupes by content.

The CONF-CAL audit member's docket (repair2/step7/confcal_audit.v2.json rows_for_e16) is attached as its own class,
with its basis per face, when the member has been run.

usage: python build_e16_docket.py [--out <json>]
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
OUT = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else HERE / "e16_docket.v1.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
MENTION = re.compile(r"#e16\b|\be16\b", re.I)
SOURCES = [
    EZ / "ezek_controlling_agent_queue_e13.v1.jsonl",
    EZ / "ezek_controlling_agent_ruling_e15.v1.json",
    EZ / "repair2" / "step2_reconciliation" / "adjudication_a1" / "adjudication.json",
    EZ / "repair2" / "step3" / "adjudication_a1" / "adjudication.json",
    EZ / "author" / "repair2_step4c" / "adjudication" / "adjudication.json",
    EZ / "author" / "repair2_step5" / "h1_adjudication" / "adjudication.json",
    EZ / "author" / "repair2_step5" / "h2_adjudication" / "adjudication.json",
    EZ / "author" / "repair2_step6" / "h1_adjudication" / "adjudication.json",
    EZ / "author" / "repair2_step6" / "h2_adjudication" / "adjudication.json",
]
found, seen, absent = [], set(), []


LIMIT = 4000


def record(o, path, src):
    s = json.dumps(o, ensure_ascii=False)
    key = hashlib.sha256(s.encode("utf-8")).hexdigest()
    if key not in seen:
        seen.add(key)
        found.append({"source": str(src.relative_to(EZ)), "path": path, "entry": o,
                      "rows_named": sorted(set(re.findall(r"P\d\d-\d\d\d", s)))})


def smallest(o, path, src):
    """Record the SMALLEST enclosing object (dict, or a list element) under LIMIT characters that mentions #e16.
    A container over the limit is descended into; a string is recorded on its own only when its parent is over it."""
    s = json.dumps(o, ensure_ascii=False)
    if not MENTION.search(s):
        return
    if isinstance(o, (dict, list)) and len(s) > LIMIT:
        items = o.items() if isinstance(o, dict) else enumerate(o)
        for k, v in items:
            sub = "%s.%s" % (path, k) if isinstance(o, dict) else "%s[%d]" % (path, k)
            if isinstance(v, (dict, list)):
                smallest(v, sub, src)
            elif MENTION.search(json.dumps(v, ensure_ascii=False)):
                record(v, sub, src)
        return
    if isinstance(o, dict):
        record(o, path, src)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if MENTION.search(json.dumps(v, ensure_ascii=False)):
                record(v, "%s[%d]" % (path, i), src)
    else:
        record(o, path, src)


for src in SOURCES:
    if not src.is_file():
        absent.append(str(src.relative_to(EZ)))
        continue
    if src.suffix == ".jsonl":
        for n, l in enumerate(src.read_text(encoding="utf-8").splitlines()):
            if l.strip():
                d = json.loads(l)
                smallest(d, "%s(line %d)" % (d.get("id", ""), n + 1), src)
    else:
        smallest(json.loads(src.read_text(encoding="utf-8")), "", src)

# drop an entry whose serialisation contains another found entry from the same source (keep the smaller)
ser = [json.dumps(f["entry"], ensure_ascii=False) for f in found]
keep = [f for i, f in enumerate(found)
        if not any(j != i and found[j]["source"] == f["source"] and len(ser[j]) < len(ser[i]) and ser[j] in ser[i] for j in range(len(found)))]
cc = EZ / "repair2" / "step7" / "confcal_audit.v2.json"
confcal = None
if cc.is_file():
    c = json.loads(cc.read_text(encoding="utf-8"))
    confcal = {"source": str(cc.relative_to(EZ)), "sha256": sha(cc), "rows_sha256": c["inputs"]["rows_sha256"],
               "rows_for_e16": [{k: x[k] for k in ("row", "span_mt", "grade", "derived_range", "state", "disagreeing_faces")} for x in c["rows_for_e16"]],
               "rows_needing_a_reader": len(c["rows_needing_a_reader"])}
out = {"schema": "ezek_e16_docket.v1", "sources_read": {str(s.relative_to(EZ)): (sha(s) if s.is_file() else "ABSENT") for s in SOURCES},
       "sources_absent_at_build": absent, "routed_entries": len(keep),
       "rows_named": sorted({r for f in keep for r in f["rows_named"]}), "entries": keep, "confcal_audit": confcal}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"routed_entries": len(keep), "by_source": {s: sum(1 for f in keep if f["source"] == s) for s in sorted({f["source"] for f in keep})},
                  "rows_named": len(out["rows_named"]), "absent": absent,
                  "confcal_rows_for_e16": len(confcal["rows_for_e16"]) if confcal else "UNAVAILABLE", "out": str(OUT), "sha256": sha(OUT)}, indent=1))
