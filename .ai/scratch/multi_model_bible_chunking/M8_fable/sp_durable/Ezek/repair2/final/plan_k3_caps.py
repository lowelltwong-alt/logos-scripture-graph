#!/usr/bin/env python3
"""Plan the #e17 K3 grade CAPS. Plan only; applied after the final merge through the harness's set_confidence operation.

K3 (#e17 class_rulings, verbatim in part): "a naming caps a row at medium_low (it blocks moves to medium or high ...) but it
does not hold a row at LOW". The section-7 check (Ezek/repair2/e16/section7_check.v1.json) MEASURED, with the strategy text
quoted, which rows' spans or containing regions section 7 names. A row that check found named and that carries a grade
ABOVE medium_low exceeds the cap. Raised independently by both blind lanes of final slice 1 (GRADE_QUESTION on P01-012,
P03-009, P06-002). A row #e17 decided by name is excluded (its decision governs); a retired row is excluded.

usage: python plan_k3_caps.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
S7 = EZ / "repair2" / "e16" / "section7_check.v1.json"
R17 = EZ / "author" / "e17" / "ruling_e17.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
ORDER = ["low", "medium_low", "medium", "high"]
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
s7 = json.loads(S7.read_text(encoding="utf-8"))
r17 = json.loads(R17.read_text(encoding="utf-8-sig"))
k3 = next(c for c in (r17["class_rulings"] if isinstance(r17["class_rulings"], list) else r17["class_rulings"].values()) if c["id"] == "K3")
decided = {d["row"] for d in r17["grade_decisions"]}
caps, skipped = [], []
for x in s7["records"]:
    if x.get("verdict") != "BLOCKED":
        continue
    rid = x["row"]
    if rid not in rows:
        skipped.append({"row": rid, "why": "retired"})
        continue
    g = rows[rid]["confidence"]
    if rid in decided:
        skipped.append({"row": rid, "why": "#e17 decided this row's grade by name"})
    elif ORDER.index(g) > ORDER.index("medium_low"):
        caps.append({"row": rid, "from": g, "to": "medium_low", "section7_text_checked": x.get("section7_text_checked"), "why_named": x.get("why")})
out = {"schema": "ezek_k3_caps_plan.v1", "rows_sha256": sha(ROWS), "section7_check_sha256": sha(S7), "ruling_e17_sha256": sha(R17),
       "k3_ruling_verbatim": k3["ruling"], "caps": caps, "skipped": skipped,
       "raised_by": "both blind lanes of final slice 1 (GRADE_QUESTION on P01-012, P03-009, P06-002)"}
p = HERE / "k3_caps_plan.v1.json"
data = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
if p.exists() and p.read_bytes() != data:
    raise SystemExit("REFUSED: %s exists with different bytes (E-41)" % p.name)
p.write_bytes(data)
print(json.dumps({"caps": [(c["row"], c["from"]) for c in caps], "skipped": skipped, "sha256": sha(p)}, indent=1))
