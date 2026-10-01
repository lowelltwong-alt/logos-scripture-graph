#!/usr/bin/env python3
"""Amend Dan/verse_inventory.json with its numbering-face declaration (Ezek #e13 ruling R2, carried forward).

WHY. The Ezek inventory gained numbering_face / numbering_face_basis / numbering_face_obligation_on_consumers by
AMENDMENT after its staging (declared 2026-09-16). Daniel's staging script was written without that amendment, so the
Daniel inventory carried a face and named none; Dan/tools/check_role_tokens.py refused on it ("verse_inventory
numbering face is not WEB"), which is the consumer assertion the ruling requires.

WHAT. MEASURES the face before declaring it: every per-chapter count must equal the WEB side of web_mt_verse_check.json,
every divergent chapter (the check's own list) must carry the WEB figure and differ from the MT one, and the total must
be the WEB total. Only then does it write. E-44: the prior bytes are kept as verse_inventory.json.pre_<sha12>, the
write is atomic (temp file + os.replace), and a second run on an already-declared file is a no-op that re-verifies.
The obligation text is copied from the Ezek inventory at run time, never retyped.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
INV = SP / "verse_inventory.json"
CHECK = SP / "web_mt_verse_check.json"
EZEK_INV = SP.parent / "Ezek" / "verse_inventory.json"


def measure(inv: dict, check: dict) -> dict:
    per = {int(c): p for c, p in check["per_chapter"].items()}
    chapters = {int(c): n for c, n in inv["chapters"].items()}
    if set(per) != set(chapters):
        raise SystemExit("REFUSED: chapter sets differ between the inventory and the verse check")
    bad = [c for c in chapters if chapters[c] != per[c]["web"]]
    if bad:
        raise SystemExit("REFUSED: chapters %s do not carry the WEB figure" % bad)
    div = sorted(check["divergent_chapters"])
    if not div or any(per[c]["web"] == per[c]["mt"] for c in div) or \
            any(per[c]["web"] != per[c]["mt"] for c in chapters if c not in div):
        raise SystemExit("REFUSED: the verse check's divergent-chapter list does not match its own figures")
    if inv["total_verses"] != sum(p["web"] for p in per.values()):
        raise SystemExit("REFUSED: total_verses is not the WEB total")
    return {"divergent_chapters": div}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    raw = INV.read_bytes()
    inv = json.loads(raw.decode("utf-8"))
    check = json.loads(CHECK.read_text(encoding="utf-8"))
    m = measure(inv, check)
    if inv.get("numbering_face") == "WEB":
        print(json.dumps({"verdict": "ALREADY_DECLARED", "measured": m}))
        return 0
    if "numbering_face" in inv:
        raise SystemExit("REFUSED: a different numbering_face is already declared: %r" % inv["numbering_face"])
    ezek = json.loads(EZEK_INV.read_text(encoding="utf-8"))
    div = ", ".join(str(c) for c in m["divergent_chapters"])
    inv["numbering_face"] = "WEB"
    inv["numbering_face_basis"] = (
        "MEASURED, not asserted: every per-chapter count in this file equals the WEB side of web_mt_verse_check.json "
        "and the chapters where the two witnesses diverge (%s) carry the WEB figure, not the MT one. Declared under "
        "the Ezek #e13 ruling R2, carried forward at Daniel Phase 0: the Daniel staging script omitted the declaration "
        "and check_role_tokens.py refused on the omission." % div)
    inv["numbering_face_obligation_on_consumers"] = ezek["numbering_face_obligation_on_consumers"]
    inv["declared_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    sha12 = hashlib.sha256(raw).hexdigest()[:12]
    pre = INV.with_name(INV.name + ".pre_" + sha12)
    if pre.exists() and pre.read_bytes() != raw:
        raise SystemExit("REFUSED: %s exists with different bytes" % pre.name)
    pre.write_bytes(raw)
    tmp = INV.with_name(INV.name + ".tmp")
    tmp.write_text(json.dumps(inv, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    os.replace(tmp, INV)
    new = INV.read_bytes()
    print(json.dumps({"verdict": "DECLARED", "measured": m, "pre": pre.name,
                      "sha256_before": hashlib.sha256(raw).hexdigest(), "sha256_after": hashlib.sha256(new).hexdigest()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
