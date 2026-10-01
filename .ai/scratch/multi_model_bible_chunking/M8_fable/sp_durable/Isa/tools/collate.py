#!/usr/bin/env python3
"""Quote collator CLI (byte / NFD / accent-stripped / skeleton tiers), Isa.

Usage:
  collate.py --ref oshb:Isa.3.7 --quote "<hebrew string>"      (MT numbering)
  collate.py --ref Isa.4.1 --quote "..."                       (bare/web: = WEB
                                                                numbering; mapped
                                                                to MT internally)
  collate.py --ref Isa.1.5-Isa.1.11 --quote "..."   (range = concatenated window)
  collate.py --json file.json            (batch: [{"ref":..,"quote":..}, ...])

CONVENTION: bare refs and web: refs are WEB numbering; MT numbering requires
the oshb: prefix. Isa is NOT an identity book (byte-proven;
web_mt_offset_map.json): MT 8:23 = WEB 9:1 / MT 9:1-20 = WEB 9:2-21 (zone
A) and MT 63:19 spans WEB 63:19 + 64:1 / MT 64:1-11 = WEB 64:2-12 (zone B,
the SPLIT) — bare/web: refs pass through web_to_mt() internally, so a WEB
ch-9 or ch-64 ref collates against the CORRECT shifted MT verse; every WEB
verse has a WLC counterpart (WEB 63:19 and WEB 64:1 BOTH collate against
the split verse MT 63:19's full bytes — a quote from either half reaches
byte tier there).

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
from isa_lib import MT_LAST_VERSE, collate_hebrew, expand_ref_token, load_verse_maps, web_to_mt


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
            if not pairs or pairs[-1] != mt:   # split-aware: WEB 63:19 and
                pairs.append(mt)               # 64:1 share MT 63:19 — no
                                               # doubled window verse
    if not pairs:
        return {"ref": ref, "tier": "bad_ref"}
    window = " ".join(oshb[f"Isa.{c}.{v}"]["text"] for c, v in pairs if f"Isa.{c}.{v}" in oshb)
    return {"ref": ref, "mt_window": f"Isa.{pairs[0][0]}.{pairs[0][1]}-{pairs[-1][0]}.{pairs[-1][1]}",
            "tier": collate_hebrew(quote, window), "language": "Hebrew"}


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
