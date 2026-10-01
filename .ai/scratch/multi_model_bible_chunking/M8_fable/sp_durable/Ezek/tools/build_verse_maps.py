#!/usr/bin/env python3
"""Build verse_map_web.json, verse_map_oshb.json, consonantal_index.json for
Ezek (run ONCE by the orchestrator at staging; agents consume the JSONs).

Adapted from the Jer builder (sp_durable/Jer/tools/build_verse_maps.py). Ezek
specifics, measured on the staged inputs before this file was written and
ASSERTED below so that drift fails loudly:
  - NO editorial apparatus lines of ANY class in the WEB Ezek extract (zero
    [SPEAKER]/[HEADING]/[SUPERSCRIPTION]/[MAJOR-SECTION] lines; the USFM carries
    no heading markers). Footnotes stand inline as a BARE "[fn]" at 38 sites in
    33 verses - the same 38 as the USFM's footnote spans, verse by verse - and
    are stripped by norm_english. (Jer's extract wrote "[fn ...]" instead; a
    builder that strips only that form fails the token audit here.)
  - ONE-ZONE NON-IDENTITY numbering, NO split (byte-proven in
    ../web_mt_offset_map.json): MT 21:1-5 = WEB 20:45-49; MT 21:6-37 =
    WEB 21:1-32. Totals 1273 / 1273, so the round-trip audit is exact equality
    both directions - web_to_mt is INJECTIVE in Ezek.
  - LANGUAGE layer: Hebrew throughout (pmarks morph_prefix_tally is H only);
    the builder asserts there is no Aramaic verse in either map.
  - Paragraph-continuation folding + the per-verse raw-vs-folded token audit
    (lesson M8-LOG-0002) are UNCHANGED from the Jer builder.
"""
from __future__ import annotations

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from ezek_lib import (BOOK, LAST_VERSE, MT_LAST_VERSE, SPBOOK, TOOLS,
                      language_of, mt_to_web, mt_to_web_all, nfd, norm_english,
                      skeleton, strip_accents, web_to_mt)

FN = re.compile(r"\[fn(?: [^\]]*)?\]")


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
        h = re.match(r"===== EZEK (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None; para_pending = False
            continue
        assert not re.match(r"\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()), \
            f"unexpected structural annotation in Ezek extract: {line[:60]}"
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
    assert len(web) == 1273, f"WEB fold produced {len(web)} verses"
    assert len(oshb) == 1273, f"OSHB map has {len(oshb)} verses"
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
    # seam + zone-edge assertions
    assert web_to_mt(20, 45) == (21, 1) and mt_to_web(21, 1) == (20, 45), "zone head rule broken"
    assert web_to_mt(20, 49) == (21, 5) and mt_to_web(21, 5) == (20, 49), "zone WEB-ch20 tail rule broken"
    assert web_to_mt(21, 1) == (21, 6) and mt_to_web(21, 6) == (21, 1), "zone WEB-ch21 head rule broken"
    assert web_to_mt(21, 32) == (21, 37) and mt_to_web(21, 37) == (21, 32), "zone tail rule broken"
    assert web_to_mt(20, 44) == (20, 44) and web_to_mt(22, 1) == (22, 1), "zone edge identity broken"
    assert web_to_mt(19, LAST_VERSE[19]) == (19, LAST_VERSE[19]), "pre-zone identity broken"
    # language layer: Hebrew throughout
    assert not any(d["language"] == "Aramaic" for d in web.values()), "Aramaic verse in WEB map"
    assert not any(d["language"] == "Aramaic" for d in oshb.values()), "Aramaic verse in OSHB map"
    # footnote layer: the bare [fn] form, 38 sites, none surviving normalization
    fn_sites = sum(len(FN.findall(d["text"])) for d in web.values())
    assert fn_sites == 38, f"expected 38 footnote sites in the folded WEB map, found {fn_sites}"
    assert not any("[fn" in d["clean"] for d in web.values()), "a footnote marker survived norm_english"
    # per-verse token audit: folded WEB map vs raw USFM (alphabetic tokens)
    raw_usfm = (SPBOOK / f"{BOOK}_web.usfm").read_text(encoding="utf-8")
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
    assert len(raw_counts) == 1273, f"token audit saw {len(raw_counts)} USFM verses"
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
                      "round_trip": "OK (one-zone crosswalk, injective, range-guarded, both directions)",
                      "token_audit": f"PASS {len(raw_counts)}/{len(raw_counts)}",
                      "footnote_sites": fn_sites,
                      "maqaf_codepoints_in_staged_oshb": maqaf_raw,
                      "verses_opening_poetry_lines": poetry_verses,
                      "continuation_paragraph_folds": para_folds,
                      "fold_verses": fold_verses,
                      "languages": sorted({d["language"] for d in oshb.values()}),
                      "status": "OK"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
