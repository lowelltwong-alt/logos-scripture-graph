#!/usr/bin/env python3
"""Plan the SIGNALS sweep and the one remaining role-token annotation repair. Plan only; applied by apply_proposal.py.

observed_substrate_signals is outside the authoring pass's writable scope by design, so six executions could report a
false structured signal and none could repair it. A report is evidence, not an order: every removal here is MEASURED on
the pinned witness first, and an element the measurement supports is KEPT however many agents asked for its removal.

Measurements, each from the witness bytes (pointing stripped to the consonantal skeleton, sliced never typed):
  wordevent.strict_onset  the row's FIRST verse carries the word-event formula skeleton ויהי דבר יהוה אלי לאמר
  oath.as_i_live          some verse of the span carries the oath skeleton חי אני
  closure.formula_final   the row's LAST verse ENDS on the utterance skeleton נאם אדני יהוה (verse-final, nothing after)
The role-token repair: P09-003's WARRANT-onset:interior entry must name the device (clause 6 v2); MT 38:2 opens
בן אדם שים פניך, so the annotation names son of man and the set-your-face opener, within the six-word form.

usage: python plan_signals_and_token_fix.py
"""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
OSHB = EZ / "Ezek_oshb.txt"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
heb = {}
for line in OSHB.read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        k, t = line.split("\t", 1)
        heb[k] = t


def skel(s):
    """consonantal skeleton: strip pointing and accents, collapse maqqef and whitespace"""
    s = "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))
    return re.sub(r"[\s־]+", " ", s).strip()


WORDEVENT = skel("ויהי דבר יהוה אלי לאמר")
OATH = skel("חי אני")
UTTER = skel("נאם אדני יהוה")
SPAN = re.compile(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$")
# WEB->MT for the one zone; outside it the keys are identical
offs = json.loads((EZ / "web_mt_offset_map.json").read_text(encoding="utf-8"))
w2m = {}
for pair in (offs.get("zone_pairs") or []):
    w, m = str(pair.get("web", "")), str(pair.get("mt", ""))
    if w.startswith("web:") and m.startswith("oshb:"):
        w2m[w.split(":", 1)[1]] = m.split(":", 1)[1]
for v in range(1, 33):
    w2m["Ezek.21.%d" % v] = "Ezek.21.%d" % (v + 5)


def verses_of(span):
    import sys
    sys.path.insert(0, str(EZ / "tools"))
    from ezek_lib import LAST_VERSE
    c1, v1, c2, v2 = (int(x) for x in SPAN.match(span).groups())
    out, c, v = [], c1, v1
    while (c, v) <= (c2, v2):
        out.append("Ezek.%d.%d" % (c, v))
        c, v = (c, v + 1) if v < LAST_VERSE[c] else (c + 1, 1)
    return out


def mt(k):
    return w2m.get(k, k)


def measure(rid, element):
    vs = verses_of(rows[rid]["span"])
    first, last = mt(vs[0]), mt(vs[-1])
    if element == "wordevent.strict_onset":
        t = skel(heb.get(first, ""))
        return {"element": element, "supported": WORDEVENT in t, "verse_tested": first,
                "test": "the row's first verse carries the word-event formula skeleton"}
    if element == "oath.as_i_live":
        hit = [k for k in vs if OATH in skel(heb.get(mt(k), ""))]
        return {"element": element, "supported": bool(hit), "verses_with_the_oath": hit,
                "test": "some verse of the span carries the oath skeleton"}
    if element == "closure.formula_final":
        t = skel(heb.get(last, ""))
        return {"element": element, "supported": t.endswith(UTTER), "verse_tested": last, "tail": t[-40:],
                "test": "the row's last verse ends on the utterance skeleton with nothing after it"}
    return {"element": element, "supported": None, "test": "no measurement defined; kept"}


REPORTED = {"P03-003": ["wordevent.strict_onset"], "P03-004": ["wordevent.strict_onset"],
            "P03-005": ["wordevent.strict_onset", "oath.as_i_live"],
            "P03-021": ["closure.formula_final", "oath.as_i_live"]}
proposal, report = {}, []
for rid, elements in REPORTED.items():
    live = list(rows[rid].get("observed_substrate_signals") or [])
    keep = list(live)
    for e in elements:
        if e not in live:
            report.append({"row": rid, "element": e, "action": "NOT PRESENT", "measurement": None})
            continue
        m = measure(rid, e)
        if m["supported"] is False:
            keep.remove(e)
            report.append({"row": rid, "element": e, "action": "REMOVE", "measurement": m})
        else:
            report.append({"row": rid, "element": e, "action": "KEEP - the measurement supports it", "measurement": m})
    if keep != live:
        proposal[rid] = {"observed_substrate_signals": keep}
# the role-token annotation
P9 = "P09-003"
refs = list(rows[P9]["boundary_evidence_refs"])
old = [i for i, e in enumerate(refs) if "[WARRANT-onset:interior]" in e and "Ezek.38.2" in e]
token_fix = None
if len(old) == 1:
    i = old[0]
    new = "oshb:Ezek.38.2 [WARRANT-onset:interior] son of man set-your-face"
    t38 = skel(heb.get("Ezek.38.2", ""))
    if skel("בן אדם") in t38 and skel("שים פניך") in t38:
        refs[i] = new
        proposal.setdefault(P9, {})["boundary_evidence_refs"] = refs
        token_fix = {"row": P9, "was": rows[P9]["boundary_evidence_refs"][i], "now": new,
                     "why": "clause 6 v2 permits :interior only when the annotation names the device; MT 38:2 opens with both",
                     "measured": "the skeletons of 'son of man' and 'set your face' both stand in MT 38:2",
                     "annotation_words": len(new.split("]", 1)[1].split())}
out = {"schema": "ezek_signals_and_token_fix.v1", "rows_sha256": sha(ROWS), "witness_sha256": sha(OSHB),
       "signals_report": report, "role_token_fix": token_fix, "proposal_rows": sorted(proposal)}
(HERE / "signals_and_token_fix.report.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
p = HERE / "signals_and_token_fix.proposal.json"
p.write_text(json.dumps(proposal, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"rows": sorted(proposal), "removals": [(r["row"], r["element"]) for r in report if r["action"] == "REMOVE"],
                  "kept": [(r["row"], r["element"], r["measurement"]) for r in report if r["action"].startswith("KEEP")],
                  "token_fix": token_fix, "proposal_sha256": sha(p)}, ensure_ascii=False, indent=1))
