#!/usr/bin/env python3
"""Greek normalize DRY-RUN over one rows file (JSONL). Never writes; reports what a normalizer would change.

Per quote {"ref", "greek", "tier"} collated at its cited ref:
  ok       byte match
  fixed    matches only after NFC (E-01: a fixed > 0 dry-run is HARD in run_suite)
  mention  matches only at accent_stripped/skeleton AND the row claims that tier (a deliberate mention)
  defect   no match, or a weaker-than-claimed match
Swete isolation arm (owner terms 2026-09-29): every Greek run in any string field is shingled (5 skeleton words);
a shingle that occurs in the staged Swete files and in neither NT witness is a defect "swete_wording". Only
hashes are compared; no Swete text is printed.

Usage: normalize_greek_in_json.py rows.jsonl | --selftest     Prints ONE JSON object (counts + status).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import greek_lib as g

_SW: set[str] | None = None
_NT: set[str] | None = None


def swete_only(text: str) -> bool:
    global _SW, _NT
    if _SW is None:
        _SW, _NT = g.swete_skeleton_shingles(), g.nt_skeleton_shingles()
    for run in g.GREEK_RUN.findall(text):
        ws = g.skeleton(run).split()
        for i in range(len(ws) - 4):
            h = hashlib.sha1(" ".join(ws[i:i + 5]).encode("utf-8")).hexdigest()
            if h in _SW and h not in _NT:
                return True
    return False


def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


def dryrun(rows: list[dict]) -> dict:
    c = {"ok": 0, "fixed": 0, "mention": 0}
    defects = []
    for i, row in enumerate(rows):
        did = row.get("decision_id", f"row{i}")
        for q in row.get("quotes", []):
            toks = list(g.parse_refs(q.get("ref", "")))
            keys = g.expand_ref(*toks[0][1:]) if len(toks) == 1 and toks[0][1] != "web" else None
            if keys is None:
                defects.append({"row": did, "kind": "quote_ref_unusable", "ref": q.get("ref")})
                continue
            sp, bk = toks[0][1], toks[0][2]
            tier = g.collate_greek(q.get("greek", ""), " ".join(g.load(sp)[bk][k] for k in keys))
            claimed = q.get("tier", "byte")
            if tier == "byte":
                c["ok"] += 1
            elif tier == "nfc":
                c["fixed"] += 1
            elif tier != "none" and claimed in g.TIER_RANK and g.TIER_RANK[tier] <= g.TIER_RANK[claimed]:
                c["mention"] += 1
            else:
                defects.append({"row": did, "kind": "quote_unmatched_or_overclaimed", "ref": q["ref"],
                                "measured": tier, "claimed": claimed})
        if any(swete_only(s) for s in _strings(row)):
            defects.append({"row": did, "kind": "swete_wording"})
    bad = bool(defects) or c["fixed"] > 0
    return {"status": "RED" if bad else "GREEN", **c, "defect_count": len(defects), "defects": defects[:30]}


def selftest() -> int:
    fx = Path(__file__).resolve().parent.parent / "fixture"
    rows = lambda n: [json.loads(l) for l in (fx / n).read_text(encoding="utf-8").splitlines() if l.strip()]
    fails = []
    r = dryrun(rows("rows.good.jsonl"))
    if r["status"] != "GREEN" or r["mention"] != 1:
        fails.append(f"good fixture: {r}")
    nfd = [x for x in rows("rows.bad.jsonl") if x["decision_id"] == "B-NFD"]
    if dryrun(nfd)["fixed"] != 1:
        fails.append("B-NFD must count fixed=1")
    # Swete arm: build an in-memory row from a Swete-only shingle; nothing is written or printed
    t = (g.SUB / "swete_lxx_REFERENCE_ONLY" / "tlg0527.tlg053.1st1K-grc1.xml").read_text(encoding="utf-8")
    import re
    body = g.skeleton(re.sub(r"<[^>]+>", " ", re.sub(r"<note.*?</note>", " ", t[t.find("<body"):], flags=re.S)))
    ws = body.split()
    nt = g.nt_skeleton_shingles()
    probe = next(" ".join(ws[i:i + 6]) for i in range(len(ws) - 6)
                 if hashlib.sha1(" ".join(ws[i:i + 5]).encode()).hexdigest() not in nt)
    if dryrun([{"decision_id": "SW", "text": probe}])["defect_count"] != 1:
        fails.append("Swete-only wording not detected")
    if dryrun([{"decision_id": "NT", "text": g.verse("rp", "Phlm", 1, 3)}])["defect_count"] != 0:
        fails.append("NT wording falsely flagged as Swete")
    print(json.dumps({"status": "GREEN" if not fails else "RED", "selftest": "normalize_greek_in_json",
                      "fails": fails}, ensure_ascii=False))
    return 0 if not fails else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
        print(json.dumps({"status": "RED", "usage": "normalize_greek_in_json.py rows.jsonl | --selftest"}))
        return 2
    try:
        p = Path(sys.argv[1])
        r = dryrun([json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()])
    except (g.SubstrateError, OSError, json.JSONDecodeError) as e:
        print(json.dumps({"status": "RED", "error": str(e)[:300]}))
        return 1
    print(json.dumps({"file": Path(sys.argv[1]).name, **r}, ensure_ascii=False))
    return 0 if r["status"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
