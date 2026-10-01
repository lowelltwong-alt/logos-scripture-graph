#!/usr/bin/env python3
"""Build verse_map_web.json, verse_map_oshb.json, consonantal_index.json for
Dan (run ONCE by the orchestrator at staging; agents consume the JSONs).

Hand-ported from the Ezek builder (sp_durable/Ezek/tools/build_verse_maps.py),
which was adapted from the Jer builder. Not produced by _adapt_tools_dan.py:
every Ezekiel fact in the builder is an assertion, and each is re-measured
here rather than swapped. Dan specifics, measured on the staged inputs before
this file was written (scratch measure_dan_web.py, 2026-09-23) and ASSERTED
below so that drift fails loudly:
  - NO editorial apparatus lines of ANY class in the WEB Dan extract (zero
    [SPEAKER]/[HEADING]/[SUPERSCRIPTION]/[MAJOR-SECTION] lines). Footnotes
    stand inline as a BARE "[fn]" at 10 sites in 9 verses - the same count as
    the USFM's 10 footnote spans - and are stripped by norm_english.
  - TWO-ZONE NON-IDENTITY numbering, NO split (web_mt_offset_map.json):
    MT 3:31-33 = WEB 4:1-3; MT 4:1-34 = WEB 4:4-37; MT 6:1 = WEB 5:31;
    MT 6:2-29 = WEB 6:1-28. 66 verses on each face. Totals 357 / 357, so the
    round-trip audit is exact equality both directions - web_to_mt is
    INJECTIVE in Dan.
  - LANGUAGE layer: Aramaic from MT/WEB 2:4 word 5 through 7:28; 2:4 itself
    is 'mixed' (read dan_lib.MIXED_VERSES, never guess a half). Per map:
    157 Hebrew, 1 mixed, 199 Aramaic. language_of is numbering-invariant, so
    a zone verse carries the same language on both faces (asserted).
  - The staged OSHB carries no maqaf codepoint: staging drops every <seg>
    with its content (_stage_phase0_dan.py). Reported, not asserted, as in Ezek.
  - Paragraph-continuation folding + the per-verse raw-vs-folded token audit
    (lesson M8-LOG-0002) are UNCHANGED from the Jer and Ezek builders.
"""
from __future__ import annotations

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from dan_lib import (BOOK, LAST_VERSE, MIXED_VERSES, MT_LAST_VERSE, SPBOOK, TOOLS,
                     language_of, mt_to_web, mt_to_web_all, nfd, norm_english,
                     skeleton, strip_accents, web_to_mt)

FN = re.compile(r"\[fn(?: [^\]]*)?\]")
TOTAL = 357
# (WEB, MT) pairs at every zone edge, and identity verses just outside each zone
ZONE_EDGES = [((4, 1), (3, 31)), ((4, 3), (3, 33)), ((4, 4), (4, 1)), ((4, 37), (4, 34)),
              ((5, 31), (6, 1)), ((6, 1), (6, 2)), ((6, 28), (6, 29))]
IDENTITY_EDGES = [(3, 30), (5, 30), (7, 1)]
LANGUAGE_TALLY = {"Hebrew": 157, "mixed": 1, "Aramaic": 199}


def build_web():
    raw = (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8")
    verses: dict[str, dict] = {}
    ch = None
    cur = None
    para_pending = False
    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue
        h = re.match(r"===== DAN (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None; para_pending = False
            continue
        assert not re.match(r"\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()), \
            f"unexpected structural annotation in Dan extract: {line[:60]}"
        body = line
        opened_para = False
        opened_poetry = 0
        m = re.match(r"^(¶[»›]?\([^)]*\)|¶|\s*•|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*(.*)$", line)
        if m:
            opened_para = line.lstrip().startswith("¶")
            if re.match(r"^\s*\|q[123]", line):
                opened_poetry = 1
            body = m.group(2)
        parts = re.split(r"\[v\] (\d+)\s*", body)
        if parts[0].strip() and cur:
            verses[cur]["text"] += " " + parts[0].strip()
            if opened_para:
                verses[cur]["continuation_paragraphs"] += 1
            if opened_poetry:
                verses[cur]["poetry_lines"] += 1
        elif not parts[0].strip() and opened_para and len(parts) > 1:
            para_pending = True
        i = 1
        while i < len(parts):
            v = int(parts[i]); text = parts[i + 1].strip()
            cur = f"{BOOK}.{ch}.{v}"
            mt = web_to_mt(ch, v)
            entry = {"text": text, "para_before": opened_para or para_pending,
                     "continuation_paragraphs": 0,
                     "poetry_lines": opened_poetry if i == 1 else 0,
                     "language": language_of(ch, v),
                     "mt": f"{BOOK}.{mt[0]}.{mt[1]}" if mt else None}
            verses[cur] = entry
            opened_para = False; para_pending = False
            i += 2
        if m and not body.strip() and len(parts) == 1 and line.lstrip().startswith("¶"):
            para_pending = True
    for k, v in verses.items():
        v["clean"] = norm_english(v["text"])
    return verses


def build_oshb():
    out: dict[str, dict] = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        ref, text = line.split("\t", 1)
        _, c, v = ref.split(".")
        c, v = int(c), int(v)
        w = mt_to_web(c, v)
        entry = {"text": text, "language": language_of(c, v),
                 "web": f"{BOOK}.{w[0]}.{w[1]}" if w else None}
        out[ref] = entry
    return out


def main() -> int:
    web = build_web()
    oshb = build_oshb()
    assert len(web) == TOTAL, f"WEB fold produced {len(web)} verses"
    assert len(oshb) == TOTAL, f"OSHB map has {len(oshb)} verses"
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in web, f"missing WEB {c}.{v}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in oshb, f"missing OSHB {c}.{v}"
    # crosswalk round-trip audit, range-guarded, both directions (INJECTIVE)
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            mt = web_to_mt(c, v)
            assert mt is not None, f"web_to_mt None at WEB {c}.{v}"
            assert mt_to_web(*mt) == (c, v), \
                f"round-trip fail WEB {c}.{v} -> MT {mt} -> {mt_to_web(*mt)}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            webs = mt_to_web_all(c, v)
            assert len(webs) == 1, f"injectivity broken at MT {c}.{v}: {webs}"
            assert web_to_mt(*webs[0]) == (c, v), \
                f"round-trip fail MT {c}.{v} -> WEB {webs[0]} -> {web_to_mt(*webs[0])}"
    # seam + zone-edge assertions (both zones), and the zone size on each face
    for w, m in ZONE_EDGES:
        assert web_to_mt(*w) == m and mt_to_web(*m) == w, f"zone edge rule broken at WEB {w} / MT {m}"
    for cv in IDENTITY_EDGES:
        assert web_to_mt(*cv) == cv and mt_to_web(*cv) == cv, f"zone edge identity broken at {cv}"
    zone_web = sum(1 for k, d in web.items() if d["mt"] != k)
    zone_mt = sum(1 for k, d in oshb.items() if d["web"] != k)
    assert zone_web == 66 and zone_mt == 66, f"zone size WEB {zone_web} / MT {zone_mt}, expected 66 / 66"
    # language layer: the measured tally on each face, the same language on both faces of every verse
    for name, mp in (("WEB", web), ("OSHB", oshb)):
        tally = {lang: sum(1 for d in mp.values() if d["language"] == lang) for lang in LANGUAGE_TALLY}
        assert tally == LANGUAGE_TALLY and sum(tally.values()) == TOTAL, f"{name} language tally {tally}"
    for k, d in web.items():
        assert oshb[d["mt"]]["language"] == d["language"], f"language differs across faces at WEB {k}"
    assert set(MIXED_VERSES) == {(2, 4)} and web[f"{BOOK}.2.4"]["language"] == "mixed", "mixed-verse layer broken"
    # footnote layer: the bare [fn] form, 10 sites in 9 verses, none surviving normalization
    fn_sites = sum(len(FN.findall(d["text"])) for d in web.values())
    fn_verses = sum(1 for d in web.values() if FN.search(d["text"]))
    assert (fn_sites, fn_verses) == (10, 9), f"expected 10 footnote sites in 9 verses, found {fn_sites} in {fn_verses}"
    assert not any("[fn" in d["clean"] for d in web.values()), "a footnote marker survived norm_english"
    # per-verse token audit: folded WEB map vs raw USFM (alphabetic tokens)
    raw_usfm = (SPBOOK / f"{BOOK}_web.usfm").read_text(encoding="utf-8")
    assert len(re.findall(r"\\f \+", raw_usfm)) == fn_sites, "USFM footnote spans differ from the extract's sites"
    raw_counts: dict[str, int] = {}
    kept = [l for l in raw_usfm.splitlines()
            if not re.match(r'\\(s\d?|r|d|sp|ms\d?|mr)\b', l)]
    chp = None
    vs = None
    for tok in re.split(r'(\\c \d+|\\v \d+)', "\n".join(kept)):
        mc = re.match(r'\\c (\d+)', tok or '')
        if mc:
            chp = int(mc.group(1)); vs = None; continue
        mv = re.match(r'\\v (\d+)', tok or '')
        if mv:
            vs = int(mv.group(1)); continue
        if chp and vs:
            body = re.sub(r'\\f \+ .*?\\f\*', ' ', tok, flags=re.S)
            body = re.sub(r'\|strong="[^"]*"', ' ', body)
            body = re.sub(r'\\\+?[a-z0-9]+\*?', ' ', body)
            key = f"{BOOK}.{chp}.{vs}"
            raw_counts[key] = raw_counts.get(key, 0) + len(re.findall(r"[A-Za-z]+", body))
    mismatch = []
    for key, want in raw_counts.items():
        got_text = FN.sub(" ", web[key]["text"])
        got = len(re.findall(r"[A-Za-z]+", got_text))
        if got != want:
            mismatch.append({"verse": key, "raw": want, "folded": got})
    assert len(raw_counts) == TOTAL, f"token audit saw {len(raw_counts)} USFM verses"
    assert not mismatch, f"token audit fail ({len(mismatch)}): {mismatch[:5]}"
    cons = {ref: {"skeleton": skeleton(d["text"]),
                  "accent_stripped": strip_accents(d["text"]),
                  "nfd": nfd(d["text"]),
                  "language": d["language"]}
            for ref, d in oshb.items()}
    (TOOLS / "verse_map_web.json").write_text(
        json.dumps(web, ensure_ascii=False, indent=1), encoding="utf-8")
    (TOOLS / "verse_map_oshb.json").write_text(
        json.dumps(oshb, ensure_ascii=False, indent=1), encoding="utf-8")
    (TOOLS / "consonantal_index.json").write_text(
        json.dumps(cons, ensure_ascii=False, indent=1), encoding="utf-8")
    maqaf_raw = (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").count("\u05BE")
    poetry_verses = sum(1 for d in web.values() if d["poetry_lines"])
    para_folds = sum(d["continuation_paragraphs"] for d in web.values())
    fold_verses = sorted(k for k, d in web.items() if d["continuation_paragraphs"])
    print(json.dumps({"web_verses": len(web), "oshb_verses": len(oshb),
                      "round_trip": "OK (two-zone crosswalk, injective, range-guarded, both directions)",
                      "zone_verses_each_face": zone_web,
                      "token_audit": f"PASS {len(raw_counts)}/{len(raw_counts)}",
                      "footnote_sites": fn_sites, "footnote_verses": fn_verses,
                      "maqaf_codepoints_in_staged_oshb": maqaf_raw,
                      "verses_opening_poetry_lines": poetry_verses,
                      "continuation_paragraph_folds": para_folds,
                      "fold_verses": fold_verses,
                      "languages": LANGUAGE_TALLY,
                      "status": "OK"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
