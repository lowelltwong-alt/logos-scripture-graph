#!/usr/bin/env python3
"""WEB <-> RP <-> SBLGNT verse-existence crosswalk (derived, NON-TEXTUAL: flags only, no witness wording).

Every verse number printed by any of the three witnesses gets web/rp/sbl existence flags; entries where all three
print the verse are counted, not listed. The summary MEASURES OW-31's working claim that RP verse existence is
one-to-one with WEB (rp_web_one_to_one) and lists every counter-example.

Usage: build_crosswalk.py OUT.json [Book ...]      (default: all 27 NT books)
       build_crosswalk.py --selftest
Prints one JSON object. E-20: a flag-shaped first argument other than --selftest writes nothing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import greek_lib as g


def build(books: list[str]) -> dict:
    per, agree = {}, 0
    rp_not_web, web_not_rp = [], []
    for b in books:
        cw = g.crosswalk(b)
        agree += sum(1 for e in cw if e["web"] and e["rp"] and e["sbl"] and len(e) == 4)
        per[b] = [e for e in cw if not (e["web"] and e["rp"] and e["sbl"] and len(e) == 4)]
        rp_not_web += [e["ref"] for e in cw if e["rp"] and not e["web"]]
        web_not_rp += [e["ref"] for e in cw if e["web"] and not e["rp"]]
    return {"crosswalk": "greek_substrate web/rp/sbl verse existence", "version": 1, "tier": "MEASURED",
            "witness_pins": "see ../STAGING_RECEIPT.v1.json", "books": books,
            "verses_printed_by_all_three_unflagged": agree, "exceptions": per,
            "summary": {"rp_web_one_to_one": not rp_not_web and not web_not_rp,
                        "rp_not_web": rp_not_web, "web_not_rp": web_not_rp,
                        "web_empty_markers": [f"{b}.{c}.{v}" for b, c, v in sorted(g.WEB_EMPTY) if b in books],
                        "rp_merged_from_separate_file": {f"{b}.{c}.{v}": f for (b, c, v), f in
                                                         sorted(g.RP_MERGED.items()) if b in books},
                        "rp_separate_file_differs": len([k for k in g.RP_SEPARATE_DIFFERS if k[0] in books])}}


def selftest() -> int:
    fails = []
    x = build(g.BOOKS)
    s = x["summary"]
    if s["rp_web_one_to_one"]:
        fails.append("one-to-one claim should be refuted on the staged bytes")
    # MEASURED 2026-09-29: the only existence difference is Acts 24:7, present in RP solely via ACT24.csv
    if s["rp_not_web"] != ["Acts.24.7"] or s["web_not_rp"] != []:
        fails.append("RP/WEB existence differences changed from the measured set")
    if "Luke.17.36" in s["web_not_rp"] or "Luke.17.36" in s["rp_not_web"]:
        fails.append("Luke 17:36 is printed by neither WEB nor RP")
    if not all(e["ref"] != "Phlm.1.1" for e in x["exceptions"]["Phlm"]):
        fails.append("Phlm 1:1 should be unflagged")
    tj = {e["ref"]: e for e in x["exceptions"]["3John"]}
    if tj.get("3John.1.15") != {"ref": "3John.1.15", "web": False, "rp": False, "sbl": True}:
        fails.append("3John 1:15 SBL-only entry")
    print(json.dumps({"status": "GREEN" if not fails else "RED", "selftest": "build_crosswalk", "fails": fails,
                      "measured_rp_not_web": s["rp_not_web"], "measured_web_not_rp": s["web_not_rp"]}))
    return 0 if not fails else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        print(json.dumps({"status": "RED", "usage": "build_crosswalk.py OUT.json [Book ...] | --selftest",
                          "error": "first argument must be the output path; nothing written"}))
        return 2
    books = sys.argv[2:] or g.BOOKS
    bad = [b for b in books if b not in g.BOOKS]
    if bad:
        print(json.dumps({"status": "RED", "error": f"unknown books {bad}"}))
        return 2
    try:
        x = build(books)
    except g.SubstrateError as e:
        print(json.dumps({"status": "RED", "error": str(e)}))
        return 1
    Path(sys.argv[1]).write_text(json.dumps(x, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"status": "GREEN", "out": sys.argv[1], **{k: x["summary"][k] for k in
                                                                 ("rp_web_one_to_one", "rp_not_web", "web_not_rp")}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
