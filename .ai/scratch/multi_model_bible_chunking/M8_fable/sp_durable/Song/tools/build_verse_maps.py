#!/usr/bin/env python3
"""Build verse_map_web.json, verse_map_oshb.json, consonantal_index.json,
speaker_headings_web.json for Song (run ONCE by the orchestrator at staging;
agents consume the JSONs).

Song specifics vs the Eccl builder:
  - The WEB Song extract carries [SPEAKER: ...] apparatus lines (modern
    editorial voice headings — owner addendum TIER 4, never evidence).
    They are STRIPPED from verse text and cataloged separately into
    ../speaker_headings_web.json keyed by the WEB verse each heading
    precedes, with the tier-4 warning embedded, so claims can be audited
    AGAINST leaning on them. No [HEADING]/[SUPERSCRIPTION]/[MAJOR-SECTION]
    lines exist in WEB Song (asserted).
  - NON-IDENTITY numbering: MT 7:1 = WEB 6:13; MT 7:2-14 = WEB 7:1-13
    (byte-proven; see build_offset_map.py). The round-trip audit exercises
    the REAL crosswalk in both directions including the seam.
  - Paragraph-continuation folding + the per-verse raw-vs-folded token audit
    (lesson M8-LOG-0002) are UNCHANGED — Song is poetry-dominant, but the
    ch-7 opening carries a prose ¶, so the fold machinery stays armed.
"""
from __future__ import annotations

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from song_lib import (BOOK, LAST_VERSE, MT_LAST_VERSE, SPBOOK, TOOLS,
                      language_of, mt_to_web, mt_to_web_all, nfd, norm_english,
                      skeleton, strip_accents, web_to_mt)


def build_web():
    raw = (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8")
    verses: dict[str, dict] = {}
    speaker_headings: dict[str, list[str]] = {}
    pending_speakers: list[str] = []
    ch = None
    cur = None
    para_pending = False
    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue
        h = re.match(r"===== SONG (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None; para_pending = False
            continue
        sp = re.match(r"\s*\[SPEAKER:\s*([^\]]+)\]\s*$", line)
        if sp:
            pending_speakers.append(sp.group(1).strip())
            continue
        assert not re.match(r"\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING)", line.strip()), \
            f"unexpected structural annotation in Song extract: {line[:60]}"
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
            verses[cur] = {"text": text, "para_before": opened_para or para_pending,
                           "continuation_paragraphs": 0,
                           "poetry_lines": opened_poetry if i == 1 else 0,
                           "language": language_of(ch, v),
                           "mt": f"{BOOK}.{mt[0]}.{mt[1]}" if mt else None}
            if pending_speakers:
                speaker_headings[cur] = pending_speakers
                pending_speakers = []
            opened_para = False; para_pending = False
            i += 2
        if m and not body.strip() and len(parts) == 1 and line.lstrip().startswith("¶"):
            para_pending = True
    assert not pending_speakers, f"trailing SPEAKER headings unattached: {pending_speakers}"
    for k, v in verses.items():
        v["clean"] = norm_english(v["text"])
    return verses, speaker_headings


def build_oshb():
    out: dict[str, dict] = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        ref, text = line.split("\t", 1)
        _, c, v = ref.split(".")
        c, v = int(c), int(v)
        w = mt_to_web(c, v)
        out[ref] = {"text": text, "language": "Hebrew",
                    "web": f"{BOOK}.{w[0]}.{w[1]}" if w else None}
    return out


def main() -> int:
    web, speaker_headings = build_web()
    oshb = build_oshb()
    assert len(web) == 117, f"WEB fold produced {len(web)} verses"
    assert len(oshb) == 117, f"OSHB map has {len(oshb)} verses"
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in web, f"missing WEB {c}.{v}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in oshb, f"missing OSHB {c}.{v}"
    # crosswalk round-trip audit, range-guarded, BOTH directions + the seam
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            mt = web_to_mt(c, v)
            assert mt is not None, f"web_to_mt None at WEB {c}.{v}"
            assert mt_to_web(*mt) == (c, v), f"round-trip fail WEB {c}.{v} -> MT {mt}"
            assert mt_to_web_all(*mt) == [(c, v)], f"mt_to_web_all fail {mt}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            w = mt_to_web(c, v)
            assert w is not None, f"mt_to_web None at MT {c}.{v}"
            assert web_to_mt(*w) == (c, v), f"round-trip fail MT {c}.{v} -> WEB {w}"
    assert web_to_mt(6, 13) == (7, 1) and mt_to_web(7, 1) == (6, 13), "seam rule broken"
    assert web_to_mt(7, 13) == (7, 14) and mt_to_web(7, 14) == (7, 13), "ch7 tail rule broken"
    assert web_to_mt(6, 12) == (6, 12) and web_to_mt(8, 1) == (8, 1), "zone edge identity broken"
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
        got_text = re.sub(r"\[fn [^\]]*\]", " ", web[key]["text"])
        got = len(re.findall(r"[A-Za-z]+", got_text))
        if got != want:
            mismatch.append({"verse": key, "raw": want, "folded": got})
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
    (SPBOOK / "speaker_headings_web.json").write_text(
        json.dumps({
            "book": BOOK,
            "tier": 4,
            "warning": ("WEB [SPEAKER: ...] apparatus — MODERN EDITORIAL voice "
                        "headings (owner addendum tier 4). NEVER boundary evidence, "
                        "NEVER voice-attribution evidence, NEVER counterevidence by "
                        "absence. Cataloged ONLY so claims can be audited against "
                        "leaning on them. Keys = the WEB verse each heading "
                        "immediately precedes."),
            "headings_before_web_verse": speaker_headings,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
    maqaf_raw = (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").count("\u05BE")
    poetry_verses = sum(1 for d in web.values() if d["poetry_lines"])
    para_folds = sum(d["continuation_paragraphs"] for d in web.values())
    print(json.dumps({"web_verses": len(web), "oshb_verses": len(oshb),
                      "round_trip": "OK (6:13|7:1 crosswalk, range-guarded, both directions)",
                      "token_audit": f"PASS {len(raw_counts)}/{len(raw_counts)}",
                      "maqaf_codepoints_in_staged_oshb": maqaf_raw,
                      "verses_opening_poetry_lines": poetry_verses,
                      "continuation_paragraph_folds": para_folds,
                      "speaker_heading_sites": len(speaker_headings),
                      "status": "OK"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
