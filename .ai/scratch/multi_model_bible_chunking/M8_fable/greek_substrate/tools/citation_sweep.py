#!/usr/bin/env python3
"""Greek citation sweep over decision rows (JSONL). HARD member of run_suite.

Per row:
  span        "web:Book.C.V[-Book.C.V]": both ends must be verses WEB prints (range guard; WEB empty markers such
              as Acts 8:37 do not exist) -> span_end_absent
  ref tokens  every web:/rp:/sbl: token anywhere in the row, including range ends, must exist in ITS witness
              -> ref_absent_in_witness
  quotes      [{"ref", "greek", "tier"}]: the quote must collate at the cited ref (-> quote_not_at_ref) and at a
              tier at least as strong as the claimed one (E-05 overclaim -> tier_overclaim); nfc-tier matches are
              counted as nfd_degraded (E-01)
  disclosure  every crosswalk exception inside the span, plus exceptions in the span's last chapter beyond its
              end when the span ends on WEB's last verse of that chapter, must appear in
              "verse_existence_disclosure" -> missing_disclosure

Usage: citation_sweep.py rows.jsonl | --selftest     Prints one JSON object; status GREEN or RED.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import greek_lib as g


def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            if k != "greek":
                yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


def required_disclosures(book: str, c1: int, v1: int, c2: int, v2: int) -> list[str]:
    web = g.load_web()[book]
    last_in_ch = max(v for c, v in web if c == c2)
    out = []
    for e in g.crosswalk(book):
        if len(e) == 4 and e["web"] and e["rp"] and e["sbl"]:
            continue
        c, v = map(int, e["ref"].split(".")[1:])
        if (c1, v1) <= (c, v) <= (c2, v2) or (c == c2 and v > v2 and v2 == last_in_ch and not e["web"]):
            out.append(e["ref"])
    return out


def sweep(rows: list[dict]) -> dict:
    defects, nfd = [], 0
    for i, row in enumerate(rows):
        did = row.get("decision_id", f"row{i}")
        span = list(g.parse_refs(str(row.get("span", ""))))
        if len(span) != 1 or span[0][1] != "web":
            defects.append({"row": did, "kind": "span_unparseable", "span": row.get("span")})
        else:
            _, _, bk, c1, v1, c2, v2 = span[0]
            if g.expand_ref("web", bk, c1, v1, c2, v2) is None:
                defects.append({"row": did, "kind": "span_end_absent", "span": row["span"]})
            else:
                have = set(row.get("verse_existence_disclosure", []))
                miss = [r for r in required_disclosures(bk, c1, v1, c2, v2) if r not in have]
                if miss:
                    defects.append({"row": did, "kind": "missing_disclosure", "refs": miss})
        for s in _strings({k: v for k, v in row.items() if k != "span"}):
            for tok, sp, bk, c1, v1, c2, v2 in g.parse_refs(s):
                if g.expand_ref(sp, bk, c1, v1, c2, v2) is None:
                    defects.append({"row": did, "kind": "ref_absent_in_witness", "ref": tok})
        for q in row.get("quotes", []):
            toks = list(g.parse_refs(q.get("ref", "")))
            if len(toks) != 1 or toks[0][1] == "web":
                defects.append({"row": did, "kind": "quote_ref_invalid", "ref": q.get("ref")})
                continue
            _, sp, bk, c1, v1, c2, v2 = toks[0]
            keys = g.expand_ref(sp, bk, c1, v1, c2, v2)
            if keys is None:
                continue                                   # already reported as ref_absent_in_witness
            tier = g.collate_greek(q.get("greek", ""), " ".join(g.load(sp)[bk][k] for k in keys))
            claimed = q.get("tier", "byte")
            if tier == "none":
                defects.append({"row": did, "kind": "quote_not_at_ref", "ref": q["ref"]})
            elif claimed not in g.TIER_RANK or g.TIER_RANK[tier] > g.TIER_RANK[claimed]:
                defects.append({"row": did, "kind": "tier_overclaim", "ref": q["ref"], "claimed": claimed,
                                "measured": tier})
            if tier == "nfc":
                nfd += 1
    return {"status": "GREEN" if not defects and not nfd else "RED", "rows": len(rows),
            "defect_count": len(defects), "nfd_degraded_count": nfd, "defects": defects[:30]}


def load_rows(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def selftest() -> int:
    fx = Path(__file__).resolve().parent.parent / "fixture"
    fails = []
    r = sweep(load_rows(fx / "rows.good.jsonl"))
    if r["status"] != "GREEN":
        fails.append(f"good fixture not GREEN: {r['defects'][:3]}")
    for row in load_rows(fx / "rows.bad.jsonl"):
        member, kind = row["_expect"]
        got = sweep([row])
        kinds = {d["kind"] for d in got["defects"]}
        if member == "citation_sweep" and kind not in kinds:
            fails.append(f"{row['decision_id']}: expected {kind}, got {sorted(kinds)}")
        if member == "normalize_dryrun" and got["nfd_degraded_count"] != 1:
            fails.append(f"{row['decision_id']}: expected nfd_degraded_count 1")
    print(json.dumps({"status": "GREEN" if not fails else "RED", "selftest": "citation_sweep", "fails": fails},
                     ensure_ascii=False))
    return 0 if not fails else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
        print(json.dumps({"status": "RED", "usage": "citation_sweep.py rows.jsonl | --selftest"}))
        return 2
    try:
        r = sweep(load_rows(Path(sys.argv[1])))
    except (g.SubstrateError, OSError, json.JSONDecodeError) as e:
        print(json.dumps({"status": "RED", "error": str(e)[:300]}))
        return 1
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["status"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
