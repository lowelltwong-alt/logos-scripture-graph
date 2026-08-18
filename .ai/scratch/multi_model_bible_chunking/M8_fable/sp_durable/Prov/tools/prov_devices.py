#!/usr/bin/env python3
"""Rebuilds ../prov_device_inventory.json from bytes (orchestrator-run at
staging; agents consume the JSON). Every count NAMES its object (Esth
lesson b). All refs identity WEB=MT.

Sections:
  collection_seams   — the tier-1 header spine, byte-swept (mishle/divrei/
                       gam-elleh verse-initial data + full header quotes)
  acrostic_31_10_31  — eshet-chayil first-letter table from skeleton bytes
  bni_address        — 'my son' (בני) vocative verse list (lecture frame)
  yhwh_density       — per-chapter verse counts containing token יהוה
  tov_openers        — verses whose skeleton opens with טוב (better-than class)
  antithetic_texture — per-chapter WEB ', but ' verse counts (heuristic
                       English-side texture; NOT evidence, staging signal)
  catchword_adjacency— per-chapter count of adjacent-verse pairs sharing >=1
                       content token (skeleton tier, stoplist-filtered;
                       heuristic staging signal for the granularity gate)
  parashah_distribution / kq_distribution — from ../pmarks_Prov.json
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prov_lib import BOOK, LAST_VERSE, SPBOOK, TOOLS, load_pmarks, skeleton

STOP = {"לא", "אל", "את", "על", "כי", "מן", "אם", "גם", "כל", "אשר", "הוא",
        "היא", "יש", "אין", "או", "פן", "בל", "לו", "לך", "בו", "בה", "מה",
        "זה", "זאת", "עם", "עד", "אך", "רק", "כן", "כה", "אף"}


def main() -> int:
    oshb: dict[str, str] = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            ref, text = line.split("\t", 1)
            oshb[ref] = text
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    sk = {ref: skeleton(t) for ref, t in oshb.items()}
    toks = {ref: s.split() for ref, s in sk.items()}

    # --- collection seams ---
    mishle = [r for r, t in toks.items() if t and t[0] == "משלי"]
    divrei = [r for r, t in toks.items() if t and t[0] == "דברי"]
    gam_elleh = [r for r, t in toks.items() if len(t) >= 2 and t[0] == "גם" and t[1] == "אלה"]
    interior_divrei_hakhamim = [r for r, s in sk.items() if "דברי חכמים" in s]
    seams = {
        "note": "tier-1 header spine; quotes are skeleton-tier here — writers re-collate pointed bytes via collate.py",
        "mishle_verse_initial": {"refs": mishle, "count_object": "verses whose first skeleton token is משלי", "count": len(mishle)},
        "divrei_verse_initial": {"refs": divrei, "count_object": "verses whose first skeleton token is דברי", "count": len(divrei)},
        "gam_elleh_verse_initial": {"refs": gam_elleh, "count_object": "verses opening גם אלה", "count": len(gam_elleh)},
        "divrei_hakhamim_anywhere": {"refs": interior_divrei_hakhamim, "count_object": "verses containing the skeleton phrase דברי חכמים", "count": len(interior_divrei_hakhamim)},
        "headers": {r: sk[r] for r in sorted(set(mishle + divrei + gam_elleh + interior_divrei_hakhamim),
                                             key=lambda x: (int(x.split(".")[1]), int(x.split(".")[2])))},
    }

    # --- acrostic ---
    alefbet = [chr(c) for c in range(0x05D0, 0x05EA + 1)
               if chr(c) not in "ךםןףץ"]
    table = []
    for i, v in enumerate(range(10, 32)):
        ref = f"{BOOK}.31.{v}"
        first = toks[ref][0]
        table.append({"ref": ref, "expected_letter": alefbet[i],
                      "first_word_skeleton": first, "ok": first[0] == alefbet[i]})
    assert all(row["ok"] for row in table), "acrostic derivation failed"

    # --- bni address ---
    bni = [r for r, t in toks.items() if "בני" in t[:2]]
    bni_by_ch = collections.Counter(int(r.split(".")[1]) for r in bni)

    # --- yhwh density ---
    yhwh = [r for r, t in toks.items() if "יהוה" in t]
    yhwh_by_ch = collections.Counter(int(r.split(".")[1]) for r in yhwh)

    # --- tov openers ---
    tov = [r for r, t in toks.items() if t and t[0] == "טוב"]

    # --- antithetic texture (English-side heuristic) ---
    but_by_ch = collections.Counter()
    for ref, d in web.items():
        if ", but " in d["clean"].lower() or d["clean"].lower().startswith("but "):
            but_by_ch[int(ref.split(".")[1])] += 1

    # --- catchword adjacency (heuristic staging signal) ---
    adj_by_ch = {}
    pairs_by_ch = {}
    for c in sorted(LAST_VERSE):
        shared = 0
        pairs = LAST_VERSE[c] - 1
        for v in range(1, LAST_VERSE[c]):
            a = {t for t in toks[f"{BOOK}.{c}.{v}"] if len(t) >= 2 and t not in STOP}
            b = {t for t in toks[f"{BOOK}.{c}.{v+1}"] if len(t) >= 2 and t not in STOP}
            if a & b:
                shared += 1
        adj_by_ch[str(c)] = shared
        pairs_by_ch[str(c)] = pairs

    pm = load_pmarks()
    para_by_ch = collections.Counter()
    for ref, ms in pm["marks"].items():
        para_by_ch[int(ref.split(".")[1])] += len(ms)
    kq_by_ch = collections.Counter()
    for ref, n in pm["kq"].items():
        kq_by_ch[int(ref.split(".")[1])] += n

    out = {
        "book": BOOK,
        "built": "Phase 0, 2026-08-18, from staged bytes (orchestrator)",
        "collection_seams": seams,
        "acrostic_31_10_31": {
            "note": "eshet-chayil: 22 verses, full alef-bet IN ORDER, derived from skeleton bytes (like Ps 119)",
            "table": table,
            "count_object": "first letters of MT 31:10-31 first words",
            "result": "22/22 regular",
        },
        "bni_address": {
            "refs": sorted(bni, key=lambda x: (int(x.split(".")[1]), int(x.split(".")[2]))),
            "count_object": "verses with token בני among the first two skeleton tokens",
            "count": len(bni), "by_chapter": dict(sorted(bni_by_ch.items())),
        },
        "yhwh_density": {
            "count_object": "verses containing skeleton token יהוה (exact token, unprefixed)",
            "total_verses": len(yhwh), "by_chapter": dict(sorted(yhwh_by_ch.items())),
            "note": "prefixed forms (ליהוה, ביהוה, מיהוה) NOT counted here — sweep separately when cited",
        },
        "tov_openers": {
            "refs": sorted(tov, key=lambda x: (int(x.split(".")[1]), int(x.split(".")[2]))),
            "count_object": "verses whose first skeleton token is exactly טוב",
            "count": len(tov),
        },
        "antithetic_texture": {
            "count_object": "WEB verses containing ', but ' (or opening 'But ') per chapter — ENGLISH-SIDE HEURISTIC texture, never evidence",
            "by_chapter": dict(sorted(but_by_ch.items())),
        },
        "catchword_adjacency": {
            "count_object": "adjacent-verse pairs sharing >=1 content token (skeleton tier, len>=2, stoplist-filtered) per chapter — HEURISTIC staging signal for the granularity gate; writers re-derive specific chains from bytes",
            "shared_pairs_by_chapter": adj_by_ch,
            "total_pairs_by_chapter": pairs_by_ch,
        },
        "parashah_distribution": {
            "count_object": "PE/SAMEKH segs per chapter (WLC single witness; tier-3 weak in Writings)",
            "by_chapter": dict(sorted(para_by_ch.items())),
        },
        "kq_distribution": {
            "count_object": "ketiv/qere variant notes per chapter",
            "by_chapter": dict(sorted(kq_by_ch.items())),
        },
    }
    (SPBOOK / "prov_device_inventory.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({
        "mishle": mishle, "divrei": divrei, "gam_elleh": gam_elleh,
        "divrei_hakhamim": interior_divrei_hakhamim,
        "acrostic": "22/22", "bni_total": len(bni),
        "bni_by_ch": dict(sorted(bni_by_ch.items())),
        "yhwh_by_ch": dict(sorted(yhwh_by_ch.items())),
        "tov_openers": len(tov),
        "but_by_ch": dict(sorted(but_by_ch.items())),
        "catchword_shared_pairs": adj_by_ch,
        "parashah_by_ch": dict(sorted(para_by_ch.items())),
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
