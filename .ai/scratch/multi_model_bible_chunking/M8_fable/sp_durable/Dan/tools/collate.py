#!/usr/bin/env python3
"""Quote collator CLI (byte / NFD / accent-stripped / skeleton tiers), Dan.

Usage:
  collate.py --ref oshb:Dan.3.31 --quote "<hebrew string>"      (MT numbering)
  collate.py --ref Dan.4.1 --quote "..."                       (bare/web: = WEB
                                                                numbering; mapped
                                                                to MT internally)
  collate.py --ref Dan.1.5-Dan.1.11 --quote "..."   (range = concatenated window)
  collate.py --json file.json            (batch: [{"ref":..,"quote":..}, ...])

CONVENTION: bare refs and web: refs are WEB numbering; MT numbering requires
the oshb: prefix. Dan is NOT an identity book (byte-proven;
web_mt_offset_map.json): TWO offset zones, pure renumbering, NO split -
MT 3:31-33 = WEB 4:1-3 / MT 4:1-34 = WEB 4:4-37 and MT 6:1 = WEB 5:31 /
MT 6:2-29 = WEB 6:1-28 — bare/web: refs pass through web_to_mt() internally,
so a WEB ch-4 ref collates against the CORRECT shifted MT verse; every WEB
verse has exactly one WLC counterpart (injective crosswalk).

Campaign rule: only 'byte' tier is quotation-grade for pointed text. 'nfd' means
the bytes must be re-spliced from source (normalize_hebrew_in_json.py --write).
'accent_stripped' and 'skeleton' are citation/mention grade and must be labeled
as such in prose. 'none' is a defect.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dan_lib import MT_LAST_VERSE, collate_hebrew, expand_ref_token, load_verse_maps, web_to_mt


def collate_one(ref: str, quote: str, oshb) -> dict:
    is_oshb = ref.startswith("oshb:")
    tok = ref.replace("oshb:", "").replace("web:", "")
    if is_oshb:
        pairs = expand_ref_token(tok, MT_LAST_VERSE)
    else:
        web_pairs = expand_ref_token(tok)
        pairs = []
        for c, v in web_pairs:
            mt = web_to_mt(c, v)
            if mt is None:                 # None only for out-of-range input
                return {"ref": ref, "tier": "bad_ref"}
            if not pairs or pairs[-1] != mt:   # dedupe guard (inert in Dan:
                pairs.append(mt)               # the crosswalk is injective)
    if not pairs:
        return {"ref": ref, "tier": "bad_ref"}
    window = " ".join(oshb[f"Dan.{c}.{v}"]["text"] for c, v in pairs if f"Dan.{c}.{v}" in oshb)
    langs = {oshb.get(f"Dan.{c}.{v}", {}).get("language", "Hebrew") for c, v in pairs}
    return {"ref": ref, "mt_window": f"Dan.{pairs[0][0]}.{pairs[0][1]}-{pairs[-1][0]}.{pairs[-1][1]}",
            "tier": collate_hebrew(quote, window),
            "language": langs.pop() if len(langs) == 1 else "Mixed"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref")
    ap.add_argument("--quote")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()
    _, oshb = load_verse_maps()
    if args.json:
        items = json.loads(args.json.read_text(encoding="utf-8"))
        results = [collate_one(it["ref"], it["quote"], oshb) for it in items]
        worst = any(r["tier"] in ("none", "bad_ref", "no_wlc_verse") for r in results)
        print(json.dumps({"results": results, "status": "RED" if worst else "GREEN"},
                         ensure_ascii=False, indent=1))
        return 1 if worst else 0
    r = collate_one(args.ref, args.quote, oshb)
    print(json.dumps(r, ensure_ascii=False))
    return 1 if r["tier"] in ("none", "bad_ref", "no_wlc_verse") else 0


if __name__ == "__main__":
    raise SystemExit(main())
