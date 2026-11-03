#!/usr/bin/env python3
"""Collate a Greek quote against the verse(s) a ref names, in ONE witness (rp or sbl).

Returns the strongest tier (byte > nfc > accent_stripped > skeleton > none; see greek_lib). The ref is
range-guarded against its own witness: an end that the witness does not print is refused (status RED), never
clamped. Swete is not a collation witness here (reference-only, owner terms 2026-09-29).

Usage: collate.py REF "QUOTE"        e.g. collate.py rp:3John.1.1 "Ὁ πρεσβύτερος"
       collate.py --selftest
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import greek_lib as g


def collate_ref(ref: str, quote: str) -> dict:
    toks = list(g.parse_refs(ref))
    if len(toks) != 1 or toks[0][0] != ref.strip():
        return {"status": "RED", "error": f"not one ref token: {ref!r}"}
    _, sp, bk, c1, v1, c2, v2 = toks[0]
    if sp == "web":
        return {"status": "RED", "error": "web is English; collate Greek against rp or sbl"}
    keys = g.expand_ref(sp, bk, c1, v1, c2, v2)
    if keys is None:
        return {"status": "RED", "ref": ref, "error": "ref end not printed by that witness (range guard)"}
    src = " ".join(g.load(sp)[bk][k] for k in keys)
    return {"status": "GREEN", "ref": ref, "verses": len(keys), "tier": g.collate_greek(quote, src)}


def selftest() -> int:
    fails = []
    rp31 = g.verse("rp", "3John", 1, 1)
    w = rp31.split()
    cases = [
        (("rp:3John.1.1", " ".join(w[:3])), "byte"),
        (("rp:3John.1.1", g.strip_accents(" ".join(w[:3]))), "accent_stripped"),
        (("rp:3John.1.1-1.2", w[0] + " … " + g.verse("rp", "3John", 1, 2).split()[1]), "byte"),
        (("rp:3John.1.15", w[0]), None),
        (("sbl:3John.1.15", g.verse("sbl", "3John", 1, 15).split()[0]), "byte"),
        (("web:3John.1.1", "x"), None),
    ]
    for (ref, q), want in cases:
        r = collate_ref(ref, q)
        got = r.get("tier") if r["status"] == "GREEN" else None
        if got != want:
            fails.append(f"{ref}: want {want} got {got}")
    print(json.dumps({"status": "GREEN" if not fails else "RED", "selftest": "collate", "fails": fails}))
    return 0 if not fails else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) != 3 or sys.argv[1].startswith("-"):
        print(json.dumps({"status": "RED", "usage": "collate.py REF \"QUOTE\" | --selftest"}))
        return 2
    r = collate_ref(sys.argv[1], sys.argv[2])
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["status"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
