#!/usr/bin/env python3
"""Book-wide occurrence sweep (backs every universal/exclusivity claim), 1Cor.

Usage:
  sweep.py --greek "ἀγάπη"      byte, accent-stripped, and skeleton hit-lists
                               over the RP witness
  sweep.py --skel QUERY        greek_lib skeleton() search only
  sweep.py --web "you in"   case-insensitive phrase over folded WEB
Prints counts + verse refs. NUMBERING: --greek/--skel hit refs are RP refs,
each annotated with its WEB counterpart (the same numbers: 1Cor is identity);
--web hit refs are WEB refs. Cite in prose as e.g. "sweep: N book-wide" (the
universals checker requires a DIGIT in the citation).

COUNT UNITS (lesson j): default counts are VERSE counts — the number of
VERSES containing >=1 hit, NOT token occurrences. Pass --tokens for token
occurrence totals; every prose citation must NAME its unit ("sweep: 7 verses"
vs "sweep: 9 occurrences in 7 verses").

CAUTION: --skel is a contiguous SUBSTRING search over greek_lib skeleton()
forms, not a root/lemma search: inflected and elided spellings differ. For a
root-level claim, sweep each attested spelling and say so. skeleton() is
applied to BOTH query and source.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cor_lib import load_verse_maps, norm_english, skeleton, strip_accents


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--greek")
    ap.add_argument("--skel")
    ap.add_argument("--web")
    ap.add_argument("--tokens", action="store_true",
                    help="also report token-occurrence totals (default counts are VERSE counts)")
    args = ap.parse_args()
    web, rp = load_verse_maps()   # 1Cor: the second map is RP
    out = {}
    if args.web:
        needle = norm_english(args.web).lower()
        hits = [r for r, d in web.items() if needle in d["clean"].lower()]
        out = {"query": args.web, "mode": "web_phrase", "numbering": "WEB",
               "count_unit": "verses", "count": len(hits), "refs": hits}
        if args.tokens:
            out["token_occurrences"] = sum(
                web[r]["clean"].lower().count(needle) for r in hits)
    elif args.greek or args.skel:
        q = args.greek or args.skel
        tiers = {"byte": [], "accent_stripped": [], "skeleton": []}
        for r, d in rp.items():
            t = d["text"]
            if args.greek and q in t:
                tiers["byte"].append(r)
            if args.greek and strip_accents(q) in strip_accents(t):
                tiers["accent_stripped"].append(r)
            if skeleton(q) in skeleton(t):
                tiers["skeleton"].append(r)
        web_alias = {r: rp[r]["web"] for r in tiers["skeleton"]}
        if not args.greek:
            # --skel mode never evaluates byte/accent tiers — omit them so a
            # raw-JSON reader cannot mistake them for "0 matches" (OL-c08)
            tiers.pop("byte"); tiers.pop("accent_stripped")
        out = {"query": q, "mode": "greek", "numbering": "RP_with_web_alias",
               "count_unit": "verses",
               "counts": {k: len(v) for k, v in tiers.items()},
               "refs": tiers, "web_refs": web_alias}
        if args.tokens:
            sq = skeleton(q)
            out["token_occurrences_skeleton"] = sum(
                skeleton(rp[r]["text"]).count(sq) for r in tiers["skeleton"])
    else:
        ap.error("one of --greek/--skel/--web required")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
