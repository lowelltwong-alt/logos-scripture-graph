#!/usr/bin/env python3
"""Verify every APPARATUS CLAIM on a zone row in the landed adjudication proposals, against the MT-numbered marks file.

WHY (orchestrator defect, found by the slice-5 adjudicator). The witness extract this orchestrator built fell back to a
verse's WEB key when its MT key held no apparatus entry. Outside the chapter 20-21 zone the two keys are the same, so
nothing moved; inside it, WEB 21:3 (= MT 21:8) picked up the paseq recorded at MT 21:3 (= WEB 20:47). Two lanes then
wrote a paseq that does not exist. The adjudicator refused to carry it, but the same false attachment could have reached
any row whose span touches the zone, so every apparatus claim on those rows is re-measured here before the merge is
applied.

A claim is any mention of samekh, pe, petuchah, setumah, paseq, ketiv or qere in a proposed field, with the verse
reference nearest to it. The marks file is MT-numbered; a claim written on the WEB face is mapped through the pinned
offset map before it is tested.

usage: python verify_zone_apparatus_claims.py
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
A = EZ / "author" / "final"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
rows = {r["decision_id"]: r for r in (json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
offs = json.loads((EZ / "web_mt_offset_map.json").read_text(encoding="utf-8"))
web_to_mt = {}
for pair in (offs.get("zone_pairs") or []):
    w, m = str(pair.get("web", "")), str(pair.get("mt", ""))
    if w.startswith("web:") and m.startswith("oshb:"):
        web_to_mt[w.split(":", 1)[1]] = m.split(":", 1)[1]
zr = ((offs.get("rule") or {}).get("zone") or {})
for v in range(1, int(zr.get("web_chapter_21_verses", 32)) + 1):
    web_to_mt["Ezek.21.%d" % v] = "Ezek.21.%d" % (v + 5)
marks = pm.get("marks") or {}
paseq = set(pm.get("paseq") or [])
kq = set((pm.get("kq") or {}).keys() if isinstance(pm.get("kq"), dict) else (pm.get("kq") or []))
ZONE_WEB = {("Ezek.20.%d" % v) for v in range(45, 50)} | {("Ezek.21.%d" % v) for v in range(1, 33)}
SPANV = re.compile(r"Ezek\.(\d{1,2})\.(\d{1,3})")
CLAIM = re.compile(r"(samekh|setumah|petuchah|\bpe\b|paseq|ketiv|qere|K/Q)", re.I)
REF = re.compile(r"(?:(oshb|web):)?Ezek\.(\d{1,2})\.(\d{1,3})|(?<![\d.:])(\d{1,2}):(\d{1,3})(?![\d])")


def zone_row(rid):
    r = rows.get(rid) or {}
    vs = SPANV.findall(str(r.get("span", "")))
    if not vs:
        return False
    (c1, v1), (c2, v2) = (int(vs[0][0]), int(vs[0][1])), (int(vs[-1][0]), int(vs[-1][1]))
    return any((c1, v1) <= (int(k.split(".")[1]), int(k.split(".")[2])) <= (c2, v2) for k in ZONE_WEB)


def refs_near(text, pos):
    best = None
    for m in REF.finditer(text):
        if abs(m.start() - pos) < 160:
            if m.group(2):
                face, c, v = m.group(1), m.group(2), m.group(3)
            else:
                face, c, v = None, m.group(4), m.group(5)
            # a bare numeral is on whichever face the words just before it name; the rows write 'MT 21:10' and
            # 'web:Ezek.21.5' side by side in the zone, and reading either as the other is the very defect under test
            lead = text[max(0, m.start() - 24):m.start()]
            if face is None:
                face = "oshb" if re.search(r"\bMT\b|oshb", lead) else ("web" if re.search(r"\bWEB\b|web:", lead) else None)
            key = "Ezek.%s.%s" % (c, v)
            mt = key if face == "oshb" else (web_to_mt.get(key, key) if face == "web" else key)
            cand = {"as_written": m.group(0), "face": face or "unprefixed", "mt_key": mt, "distance": abs(m.start() - pos)}
            if best is None or cand["distance"] < best["distance"]:
                best = cand
    return best


findings, checked = [], 0
for k in range(1, 7):
    p = A / ("s%d_adjudication" % k) / "proposal.json"
    if not p.is_file():
        continue
    prop = json.loads(p.read_text(encoding="utf-8"))
    for rid, fields in prop.items():
        if not zone_row(rid):
            continue
        for f, val in fields.items():
            for text in (val if isinstance(val, list) else [val]):
                if not isinstance(text, str):
                    continue
                for m in CLAIM.finditer(text):
                    checked += 1
                    near = refs_near(text, m.start())
                    if not near:
                        continue
                    word, mt = m.group(1).lower(), near["mt_key"]
                    if word in ("samekh", "setumah"):
                        ok = str(marks.get(mt, "")).upper().find("SAMEKH") >= 0
                    elif word in ("pe", "petuchah"):
                        ok = str(marks.get(mt, "")).upper().find("PE") >= 0
                    elif word == "paseq":
                        ok = mt in paseq
                    else:
                        ok = mt in kq
                    if not ok:
                        findings.append({"slice": "s%d" % k, "row": rid, "field": f, "claim_word": m.group(1),
                                         "reference_as_written": near["as_written"], "mt_key_tested": mt,
                                         "apparatus_at_that_mt_key": {"mark": marks.get(mt), "paseq": mt in paseq, "kq": mt in kq},
                                         "context": text[max(0, m.start() - 110):m.start() + 110]})
out = {"schema": "ezek_zone_apparatus_verification.v1", "rows_sha256": sha(EZ / "repair" / "rows_v7_cwo24.jsonl"),
       "pmarks_sha256": sha(EZ / "pmarks_Ezek.json"), "claims_checked_on_zone_rows": checked,
       "unsupported_claims": findings,
       "note": ("a finding is a claim whose nearest reference resolves to an MT verse the apparatus does not support; an "
                "absence claim ('no samekh stands here') reads as unsupported here and is judged by hand")}
p = HERE / "zone_apparatus_verification.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"claims_checked": checked, "unsupported": len(findings),
                  "rows": sorted({f["row"] for f in findings}), "sha256": sha(p)}, indent=1))
for f in findings[:8]:
    print(" -", f["row"], f["field"], f["claim_word"], f["reference_as_written"], "->", f["mt_key_tested"], "|", f["context"][:130].replace("\n", " "))
