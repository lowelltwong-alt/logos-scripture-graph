#!/usr/bin/env python3
"""Build a verified WEB<->MT verse crosswalk for one book (Tier-0, deterministic).

Method: WEB order and MT (OSHB/WLC) order are walked index-by-index. If total verse
counts match, the mapping is 1:1 in order and segments are emitted wherever the
chapter.verse labels diverge. If totals differ, a structured source-gap record is
written instead (never invented alignment) and original-language reviews of affected
spans must verdict insufficient_evidence until resolved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--book-dir", type=Path, required=True, help="dir containing verse_inventory.json and <Book>_oshb.txt")
    args = parser.parse_args()
    book = args.book
    d = args.book_dir

    inv = json.loads((d / "verse_inventory.json").read_text(encoding="utf-8"))
    web_refs = []
    for ch, last in inv["chapters"].items():
        for v in range(1, last + 1):
            web_refs.append((int(ch), v))

    mt_refs = []
    for line in (d / f"{book}_oshb.txt").read_text(encoding="utf-8").splitlines():
        ref = line.split("\t")[0]
        _, ch, v = ref.split(".")
        mt_refs.append((int(ch), int(v)))

    out = {"book": book, "built_by": "deterministic_crosswalk_builder_tier0",
           "web_total": len(web_refs), "mt_total": len(mt_refs), "non_authorizing": True}

    if len(web_refs) != len(mt_refs):
        web_ch: dict[int, int] = {}
        for ch, v in web_refs:
            web_ch[ch] = max(web_ch.get(ch, 0), v)
        mt_ch: dict[int, int] = {}
        for ch, v in mt_refs:
            mt_ch[ch] = max(mt_ch.get(ch, 0), v)
        if set(web_ch) != set(mt_ch):
            out.update({
                "status": "source_gap_chapter_sets_differ",
                "instruction": "Original-language reviews touching unaligned regions must verdict insufficient_evidence; do not invent alignment.",
            })
            (d / "web_mt_crosswalk.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
            print(json.dumps(out, indent=1))
            return 0
        clean_file = d / f"{book}_web_clean.txt"
        clean = clean_file.read_text(encoding="utf-8") if clean_file.is_file() else ""
        chapters = []
        ambiguous = 0
        for ch in sorted(web_ch):
            w, m = web_ch[ch], mt_ch[ch]
            if w == m:
                chapters.append({"chapter": ch, "web_verses": w, "mt_verses": m, "relation": "identical"})
                continue
            ambiguous += 1
            entry = {"chapter": ch, "web_verses": w, "mt_verses": m,
                     "relation": f"mt_extra_{m - w}" if m > w else f"web_extra_{w - m}",
                     "citation_rule": "dual WEB/MT reference required; verse-boundary difference inside this chapter — sub-verse mapping claims need explicit care or insufficient_evidence"}
            if m > w and clean:
                # typical cause: MT numbers the superscription as verse 1(-2)
                block = clean.split(f"===== {book.upper()} {ch} =====")
                has_superscription = len(block) > 1 and "[SUPERSCRIPTION:" in block[1].split("=====")[0]
                entry["web_superscription_present"] = has_superscription
                if has_superscription:
                    entry["likely_mapping"] = f"MT {ch}:1..{m - w} = WEB superscription; WEB {ch}:V = MT {ch}:V+{m - w}"
            chapters.append(entry)
        out.update({
            "status": "verified_chapter_level",
            "note": "Totals differ; chapter-level alignment verified from hard verse counts. Chapters marked non-identical require dual citation; exact sub-verse claims inside them default to insufficient_evidence unless separately established.",
            "ambiguous_chapters": ambiguous,
            "chapters": chapters,
        })
        (d / "web_mt_crosswalk.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
        print(json.dumps({k: out[k] for k in ("book", "web_total", "mt_total", "status", "ambiguous_chapters")}, indent=1))
        return 0

    segments = []
    seg = None
    for idx, (w, m) in enumerate(zip(web_refs, mt_refs)):
        same = (w == m)
        if seg is None or seg["identical"] != same:
            if seg:
                segments.append(seg)
            seg = {"identical": same, "web_start": f"{book}.{w[0]}.{w[1]}", "mt_start": f"{book}.{m[0]}.{m[1]}",
                   "web_end": f"{book}.{w[0]}.{w[1]}", "mt_end": f"{book}.{m[0]}.{m[1]}"}
        else:
            seg["web_end"] = f"{book}.{w[0]}.{w[1]}"
            seg["mt_end"] = f"{book}.{m[0]}.{m[1]}"
    if seg:
        segments.append(seg)

    out.update({
        "status": "verified",
        "alignment": [
            ({"web": f"{s['web_start']}-{s['web_end']}", "mt": "identical"} if s["identical"]
             else {"web": f"{s['web_start']}-{s['web_end']}", "mt": f"{s['mt_start']}-{s['mt_end']}"})
            for s in segments
        ],
        "note": "All original-language citations inside non-identical segments must state both WEB and MT references.",
    })
    (d / "web_mt_crosswalk.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
