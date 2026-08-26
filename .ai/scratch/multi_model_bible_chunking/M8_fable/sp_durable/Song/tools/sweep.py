#!/usr/bin/env python3
"""Book-wide occurrence sweep (backs every universal/exclusivity claim), Song.

Usage:
  sweep.py --heb "וַיַּעַשׂ"          pointed form: byte, accent-stripped, and
                                      skeleton hit-lists over OSHB
  sweep.py --skel "כתב"               consonantal search only
  sweep.py --web "house of God"       case-insensitive phrase over folded WEB
Prints counts + verse refs. NUMBERING: --heb/--skel hit refs are MT (OSHB)
refs, each annotated with its WEB counterpart; --web hit refs are WEB refs.
Cite in prose as e.g. "sweep: N book-wide" (the universals checker requires a
DIGIT in the citation).

COUNT UNITS (lesson j): default counts are VERSE counts — the number of
VERSES containing >=1 hit, NOT token occurrences. Pass --tokens for token
occurrence totals; every prose citation must NAME its unit ("sweep: 7 verses"
vs "sweep: 9 occurrences in 7 verses").

CAUTION: --skel is a contiguous consonantal SUBSTRING search, not a
root/lemma search — spellings with infixed matres lectionis differ (כתב does
NOT match כתוב). For a root-level claim, sweep each attested spelling and say
so. skeleton() maps maqaf to SPACE (Song toolkit convention) on BOTH query and
source, so maqaf-vs-space spelling does not affect skeleton hits.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from song_lib import load_verse_maps, norm_english, skeleton, strip_accents


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--heb")
    ap.add_argument("--skel")
    ap.add_argument("--web")
    ap.add_argument("--tokens", action="store_true",
                    help="also report token-occurrence totals (default counts are VERSE counts)")
    args = ap.parse_args()
    web, oshb = load_verse_maps()
    out = {}
    if args.web:
        needle = norm_english(args.web).lower()
        hits = [r for r, d in web.items() if needle in d["clean"].lower()]
        out = {"query": args.web, "mode": "web_phrase", "numbering": "WEB",
               "count_unit": "verses", "count": len(hits), "refs": hits}
        if args.tokens:
            out["token_occurrences"] = sum(
                web[r]["clean"].lower().count(needle) for r in hits)
    elif args.heb or args.skel:
        q = args.heb or args.skel
        tiers = {"byte": [], "accent_stripped": [], "skeleton": []}
        for r, d in oshb.items():
            t = d["text"]
            if args.heb and q in t:
                tiers["byte"].append(r)
            if args.heb and strip_accents(q) in strip_accents(t):
                tiers["accent_stripped"].append(r)
            if skeleton(q) in skeleton(t):
                tiers["skeleton"].append(r)
        web_alias = {r: oshb[r]["web"] for r in tiers["skeleton"]}
        if not args.heb:
            # --skel mode never evaluates byte/accent tiers — omit them so a
            # raw-JSON reader cannot mistake them for "0 matches" (OL-c08)
            tiers.pop("byte"); tiers.pop("accent_stripped")
        out = {"query": q, "mode": "hebrew", "numbering": "MT_with_web_alias",
               "count_unit": "verses",
               "counts": {k: len(v) for k, v in tiers.items()},
               "refs": tiers, "web_refs": web_alias}
        if args.tokens:
            sq = skeleton(q)
            out["token_occurrences_skeleton"] = sum(
                skeleton(oshb[r]["text"]).count(sq) for r in tiers["skeleton"])
    else:
        ap.error("one of --heb/--skel/--web required")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
