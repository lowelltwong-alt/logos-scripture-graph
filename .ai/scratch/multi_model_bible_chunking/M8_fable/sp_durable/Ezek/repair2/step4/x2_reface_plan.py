#!/usr/bin/env python3
"""STEP 4 - X2: the deterministic re-face of MT-borne device entries from web: to oshb: OUTSIDE the zone. Plan only.

#e15 Q5 face_of_the_evidence: "an MT-borne device (mark, paseq, K/Q, note, formula membership) is cited on the oshb:
face; a WEB quotation on the web: face; inside the ch 20/21 zone every entry is dual as already ruled. Outside the zone
this is a deterministic re-face (identity numbering) and runs as a MECHANICAL sweep with a distinct check."

WHAT IS MECHANICAL: changing the face prefix of an entry whose token is DISCLOSURE-kq / -mark / -paseq / -note /
-device, when the verse lies outside the zone. Nothing else in the entry changes.

THE DISTINCT CHECK, from inputs the prefix swap does not consult:
  1. identity numbering holds at that verse by the offset map's own function (web_to_mt), never by assumption;
  2. the device the token names EXISTS on that MT verse in the pinned record (a mark in pmarks.marks, a paseq in
     pmarks.paseq, a K/Q in pmarks.kq, a note in pmarks.notes_other); DISCLOSURE-device is checked against the census
     only as class membership of the verse. An entry whose device is NOT found is ROUTED to an author, never re-faced -
     re-facing a false claim would dress it in the authoritative face.

usage: python x2_reface_plan.py
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "tools"))
import ezek_lib as LIB                                                         # noqa: E402

ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
inv = json.loads((EZ / "ezek_device_inventory.v2.json").read_text(encoding="utf-8"))
census = set()


def collect(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "verses_mt" and isinstance(v, list):
                census.update(v)
            else:
                collect(v)


collect(inv)
ENTRY = re.compile(r"^web:Ezek\.(\d{1,2})\.(\d{1,3})(-Ezek\.\d{1,2}\.\d{1,3})? \[(DISCLOSURE-(?:kq|mark|paseq|note|device))\] (.*)$")
ZONE_WEB = {(20, v) for v in range(45, 50)} | {(21, v) for v in range(1, 33)}


def device_exists(token, key):
    return {"DISCLOSURE-mark": key in pm["marks"], "DISCLOSURE-paseq": key in pm["paseq"],
            "DISCLOSURE-kq": key in pm["kq"], "DISCLOSURE-note": key in pm["notes_other"],
            "DISCLOSURE-device": key in census}[token]


rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
plan, routed, tally = [], [], Counter()
for r in rows:
    for e in r.get("boundary_evidence_refs") or []:
        m = ENTRY.match(e)
        if not m:
            continue
        c, v, rng, token = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
        tally["candidates"] += 1
        if (c, v) in ZONE_WEB or c in (20, 21) and rng:
            routed.append({"row": r["decision_id"], "entry": e, "why": "touches the zone - dual form is author work"})
            tally["routed_zone"] += 1
            continue
        if LIB.web_to_mt(c, v) != (c, v):
            routed.append({"row": r["decision_id"], "entry": e, "why": "identity numbering does NOT hold here by web_to_mt"})
            tally["routed_not_identity"] += 1
            continue
        key = "Ezek.%d.%d" % (c, v)
        if not device_exists(token, key):
            routed.append({"row": r["decision_id"], "entry": e,
                           "why": "the device [%s] is NOT recorded on MT %d:%d - re-facing would dress an unsupported "
                                  "claim in the authoritative face; an author decides" % (token, c, v)})
            tally["routed_device_not_found"] += 1
            continue
        plan.append({"row": r["decision_id"], "entry_before": e, "entry_after": "oshb:" + e[len("web:"):],
                     "distinct_check": {"web_to_mt_identity": True, "device_recorded_on_mt_verse": True}})
        tally["re_face"] += 1

out = {"schema": "ezek_step4_x2_reface_plan.v1", "rows_sha256": sha(ROWS), "tally": dict(tally), "plan": plan,
       "routed_to_authors": routed,
       "tier": "MEASURED: identity by the offset map's function and device existence in the pinned record"}
p = HERE / "x2_reface_plan.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"tally": dict(tally), "plan_sha256": sha(p)}, indent=1))
for x in routed[:10]:
    print("  ROUTED %-8s %s | %s" % (x["row"], x["why"][:70], x["entry"][:60]))
