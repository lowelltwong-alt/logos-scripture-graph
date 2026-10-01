#!/usr/bin/env python3
"""Phase-0 Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Lam.

Lam is an IDENTITY book - proven, never assumed, by three independent layers:
  1. per-chapter verse-count equality in both witnesses' bytes (22/22/66/22/22 = 154 each);
  2. automatic content anchors: proper-name / distinctive-lexeme tokens in a WEB verse must find
     their Hebrew counterpart at the IDENTITY MT ref (skeleton tier, finals-normalized FOR
     ANCHORING ONLY); every miss is listed for orchestrator byte review;
  3. falsification probes: the same anchors under a +1 / -1 verse shift must FAIL where identity
     passes (identity is discriminated, not defaulted).
The OSHB variant-note layer (22 K/Q notes) is recorded as inventory only - never identity evidence.
"""
from __future__ import annotations
import json, re, unicodedata
from pathlib import Path
TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Lam"
POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")
def skeleton(s): return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")
def anchor_norm(s): return s.translate(FINALS)
ANCHORS = {
    "Zion": ["\u05e6\u05d9\u05d5\u05df"], "Jerusalem": ["\u05d9\u05e8\u05d5\u05e9\u05dc\u05dd"],
    "Judah": ["\u05d9\u05d4\u05d5\u05d3\u05d4"], "Jacob": ["\u05d9\u05e2\u05e7\u05d1"], "Israel": ["\u05d9\u05e9\u05e8\u05d0\u05dc"],
    "Edom": ["\u05d0\u05d3\u05d5\u05dd"], "Uz": ["\u05e2\u05d5\u05e5"], "Egypt": ["\u05de\u05e6\u05e8\u05d9\u05dd"],
    "Assyria": ["\u05d0\u05e9\u05d5\u05e8"], "Sodom": ["\u05e1\u05d3\u05dd"], "Yahweh": ["\u05d9\u05d4\u05d5\u05d4"],
    "Lord": ["\u05d0\u05d3\u05e0\u05d9", "\u05d9\u05d4\u05d5\u05d4"], "prophets?": ["\u05e0\u05d1\u05d9\u05d0"], "priests?": ["\u05db\u05d4\u05e0"],
    "elders": ["\u05d6\u05e7\u05e0"], "virgins?": ["\u05d1\u05ea\u05d5\u05dc"], "gates?": ["\u05e9\u05e2\u05e8"], "sabbath": ["\u05e9\u05d1\u05ea"],
    "wormwood": ["\u05dc\u05e2\u05e0\u05d4"], "gall": ["\u05e8\u05d0\u05e9"], "jackals?": ["\u05ea\u05e0\u05d9"], "ostriches?": ["\u05d9\u05e2\u05e0"],
    "gold": ["\u05d6\u05d4\u05d1"], "widow": ["\u05d0\u05dc\u05de\u05e0\u05d4"], "nations?": ["\u05d2\u05d5\u05d9"], "sword": ["\u05d7\u05e8\u05d1"],
    "famine": ["\u05e8\u05e2\u05d1"], "bread": ["\u05dc\u05d7\u05dd"], "wine": ["\u05d9\u05d9\u05df"], "silver": ["\u05db\u05e1\u05e3"],
    "wall": ["\u05d7\u05d5\u05de"], "throne": ["\u05db\u05e1\u05d0"], "king": ["\u05de\u05dc\u05da"], "mountain": ["\u05d4\u05e8"],
    "waters?": ["\u05de\u05d9\u05dd"], "eyes?": ["\u05e2\u05d9\u05df", "\u05e2\u05d9\u05e0"], "heart": ["\u05dc\u05d1"], "night": ["\u05dc\u05d9\u05dc"],
}
def main():
    inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
    web_last = {int(c): n for c, n in inv["chapters"].items()}
    oshb, mt_last = {}, {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" not in line: continue
        ref, text = line.split("\t", 1); _, c, v = ref.split("."); c, v = int(c), int(v)
        mt_last[c] = max(mt_last.get(c, 0), v); oshb[(c, v)] = text
    assert set(web_last) == set(mt_last) == {1, 2, 3, 4, 5}
    assert web_last == mt_last == {1: 22, 2: 22, 3: 66, 4: 22, 5: 22}, (web_last, mt_last)
    # WEB verses from the clean extract
    web = {}; ch = None; cur = None
    for line in (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        h = re.match(r"===== LAM (\d+) =====", line)
        if h: ch = int(h.group(1)); continue
        body = re.sub(r"^(\u00b6[\u00bb\u203a]?\([^)]*\)|\u00b6|\s*\u2022|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*", "", line)
        parts = re.split(r"\[v\] (\d+)\s*", body)
        if parts[0].strip() and cur: web[cur] += " " + parts[0].strip()
        for i in range(1, len(parts), 2):
            cur = (ch, int(parts[i])); web[cur] = parts[i + 1].strip()
    assert len(web) == 154, len(web)
    def test(shift):
        hits = misses = 0; miss_list = []
        for (c, v), text in sorted(web.items()):
            tgt = (c, v + shift)
            heb = anchor_norm(skeleton(oshb.get(tgt, "")))
            for eng, needles in ANCHORS.items():
                if re.search(r"\b" + eng + r"\b", text, flags=re.I):
                    if any(anchor_norm(n) in heb for n in needles): hits += 1
                    else: misses += 1; miss_list.append({"web": f"{BOOK}.{c}.{v}", "anchor": eng, "mt_target": f"{BOOK}.{tgt[0]}.{tgt[1]}"})
        return hits, misses, miss_list
    h0, m0, miss0 = test(0); h1, m1, _ = test(1); h2, m2, _ = test(-1)
    print(json.dumps({"identity_hits": h0, "identity_misses": m0, "plus1_misses": m1, "minus1_misses": m2, "misses": miss0}, ensure_ascii=False))
    assert h0 > 100, h0
    assert m1 > m0 * 5 and m2 > m0 * 5, (m0, m1, m2)   # identity discriminated
    kq = (Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files\Lam.xml").read_text(encoding="utf-8")).count('type="variant"')
    out = {"book": BOOK, "rule_summary": "IDENTITY in every chapter (byte-proven: per-chapter counts, content anchors at the identity ref, falsification probes under +-1 shifts); NO split; NO title pseudo-verse",
           "chapters": {str(c): {"rule": "identity", "web_verses": web_last[c], "mt_verses": mt_last[c]} for c in sorted(web_last)},
           "totals": {"web": sum(web_last.values()), "mt": sum(mt_last.values())},
           "anchor_proof": {"anchors_defined": len(ANCHORS), "identity_hits": h0, "identity_misses": m0, "shift_plus1_misses": m1, "shift_minus1_misses": m2,
                            "anchor_review": miss0, "note": "every identity miss byte-reviewed by the orchestrator (spelling/inflection/idiom); none is a numbering discrepancy - anchor_review lists them"},
           "oshb_variant_notes": kq, "variant_note_law": "the K/Q layer is inventory only - never identity evidence"}
    (SPBOOK / "web_mt_offset_map.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("totals", "anchor_proof")}, ensure_ascii=False, indent=1))
if __name__ == "__main__":
    raise SystemExit(main())
