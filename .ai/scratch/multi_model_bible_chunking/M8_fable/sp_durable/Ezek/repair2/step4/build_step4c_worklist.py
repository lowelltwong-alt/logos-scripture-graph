#!/usr/bin/env python3
"""REPAIR-2 step 4c worklist (author vocabulary batch), every item measured PENDING or DONE on the current rows.

SOURCES
  RT   - the hard role_tokens member run in POST phase: its flag list IS the set of warrants still unqualified
  ABS  - #e15 4_vocabulary: '*-absence re-tokenisation of the ANCHOR absences at 40:38, 41:9 (x2)'. MEASURED on the rows:
         one ANCHOR at 40:38 (P10-016) and one at 41:9 (P10-007), whose device_notes also states the 41:9 absence in
         prose. The '(x2)' is read as those two occurrences - INFERRED, and recorded as such.
  X2R  - the X2 re-face's routed entries (a device no census class records on that MT verse)
  ADJ2 - step-2 adjudication carried obligations marked step 4
  ADJ3 - step-3 adjudication items routed to step 4
  E15  - #e15 per-row repairs that re-face or qualify an entry, tested by whether the named web: entry still stands

STATUS: PENDING (the entry or token the item names still stands as it was) | DONE (measured changed) | READER.
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
items = []


def add(src, rid, kind, order, status, entry=None, extra=None):
    items.append(dict({"id": "S4-%03d" % (len(items) + 1), "source": src, "row": rid, "kind": kind, "order": order,
                       "status": status, "entry": entry}, **(extra or {})))


# RT
rt_t = (HERE / "role_tokens_post_on_32f33f05.json").read_text(encoding="utf-8")
rt = json.loads(rt_t[rt_t.find("{"):])
if rt.get("counts", {}).get("entries_read", 0) == 0:
    raise SystemExit("REFUSED: the member read no entries (E-36)")
face = json.loads((HERE / "face_qualification_plan.v1.json").read_text(encoding="utf-8"))
routed = {x["entry"][:110]: x["why"] for x in face["routed_to_the_author_batch_zone"] + face["refused_needs_an_author"]}
for f in rt["flags"]:
    tok = re.search(r"\[([A-Za-z-]+)", f["entry"]).group(1)
    kind = "rival_seam_pair_and_qualifier" if tok == "WARRANT-rival" else "warrant_qualifier_needing_a_reader"
    order = ("qualify this WARRANT-rival: its annotation's first token names the seam pair 'C.V/C.V' read off the "
             "rejected-alternative field, and the qualifier is :near on the rival's candidate onset verse, :far on the "
             "verse behind it" if tok == "WARRANT-rival" else
             "qualify this %s: %s" % (tok, routed.get(f["entry"][:110], "derive the face from verse and span")))
    add("RT", f["row"], kind, order, "PENDING", f["entry"])

# ABS
for rid, v in (("P10-016", "40.38"), ("P10-007", "41.9")):
    hit = [e for e in rows[rid]["boundary_evidence_refs"] if ("Ezek.%s " % v) in e and "[ANCHOR]" in e]
    add("ABS", rid, "absence_retokenisation",
        "re-tokenise the ANCHOR absence at %s: WARRANT-absence if the boundary rests on the absence, DISCLOSURE-absence "
        "if it is recorded but the boundary does not rest on it (#e15 Q5); keep the claim, verify the census is EMPTY at "
        "the verse" % v.replace(".", ":"), "PENDING" if hit else "DONE", hit[0] if hit else None)

# X2R
x2 = json.loads((HERE / "x2_reface_plan.v1.json").read_text(encoding="utf-8"))
for x in x2["routed_to_authors"]:
    add("X2R", x["row"], "device_claim_not_in_census",
        "the entry names a device no census class records on its MT verse (%s): choose the token the record supports "
        "(ANCHOR for a content statement, DISCLOSURE-absence for a recorded absence) and put it on the right face"
        % x["why"][:80], "PENDING" if x["entry"] in rows[x["row"]]["boundary_evidence_refs"] else "DONE", x["entry"])

# ADJ2 / ADJ3
a2 = json.loads((EZ / "repair2" / "step2_reconciliation" / "adjudication_a1" / "adjudication.json").read_text(encoding="utf-8"))
for rid, r in (a2.get("rows") or {}).items():
    for c in r.get("carried_obligations") or []:
        if str(c.get("step")) == "4":
            add("ADJ2", rid, "carried_vocabulary", c["what"], "READER")
a3 = json.loads((EZ / "repair2" / "step3" / "adjudication_a1" / "adjudication.json").read_text(encoding="utf-8"))
for x in (a3.get("routed") or []):
    s = json.dumps(x, ensure_ascii=False)
    if re.search(r"step[ _-]?4", s, re.I):
        m = re.search(r"P\d{2}-\d{3}", s)
        add("ADJ3", m.group(0) if m else "?", "carried_vocabulary", s[:400], "READER")

# E15 per-row re-face / qualify repairs, tested on the named web: entries
r15 = json.loads((EZ / "ezek_controlling_agent_ruling_e15.v1.json").read_text(encoding="utf-8"))
blocks = dict(r15["q1_redecision_threshold"].get("per_row", {}))
blocks.update({k: v for k, v in r15["q3_confidence_defects"].items() if re.fullmatch(r"P\d{2}-\d{3}", k)})
blocks.update({k: v for k, v in r15["q4_findings_of_fact"].items() if re.fullmatch(r"P\d{2}-\d{3}", k)})
for rid, b in blocks.items():
    reps = b.get("repairs") or b.get("repair") or []
    reps = [reps] if isinstance(reps, str) else reps
    for rep in reps:
        if not re.search(r"re-face|qualify|re-gloss|DISCLOSURE-device|WARRANT-rival", rep):
            continue
        webrefs = re.findall(r"web:Ezek\.\d+\.\d+(?:-Ezek\.\d+\.\d+)?", rep)
        live = rows[rid]["boundary_evidence_refs"]
        pending = [w for w in webrefs if any(e.startswith(w + " ") for e in live)]
        status = "PENDING" if pending else ("DONE" if webrefs else "READER")
        add("E15", rid, "ruled_reface_or_qualify", rep, status, None, {"web_entries_still_standing": pending})

from collections import Counter
out = {"schema": "ezek_repair2_step4c_worklist.v1", "rows_sha256": sha(ROWS), "items": items,
       "tally_by_source": dict(Counter(i["source"] for i in items)),
       "tally_by_status": dict(Counter(i["status"] for i in items)),
       "rows_with_owed_items": sorted({i["row"] for i in items if i["status"] != "DONE"}),
       "note_on_the_x2_count": ("#e15 says '41:9 (x2)'; the rows carry ONE 41:9 ANCHOR entry (P10-007) plus the same "
                                "absence in that row's prose. Read as those two occurrences - INFERRED."),
       "tier": "status MEASURED on the current rows; READER items carry no pass"}
p = HERE / "step4c_worklist.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("tally_by_source", "tally_by_status")}, indent=1),
      "rows with owed items:", len(out["rows_with_owed_items"]), "sha:", sha(p)[:12])
