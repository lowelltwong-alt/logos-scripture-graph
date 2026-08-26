#!/usr/bin/env python3
"""Paragraph-mark/segment-disclosure symmetry checker (casing-normalized) for Song rows.

Song (Writings) carries a RICH WLC parashah layer — 1 petuchah (MT 8:10) +
19 setumah over 20 marked verses (the layer shadows the refrain skeleton:
SAMEKH at all three adjuration sites MT 2:7/3:5/8:4, at the mutual-belonging
sites MT 6:3/7:11, at 5:1 — the tier does NOT rise for that: tier-3 weak in
the Writings, always), byte-extracted into ../pmarks_Song.json — the
paragraph-mark machinery applies with the fabrication pivot kept WIDE:
 0. SELAH claims are fabrications in Song (Psalter device; zero occurrences).
    Likewise reversed-nun, suspended-letter, AND small/large-letter claims —
    WLC Song carries NO special-letter segs at all (unlike Prov's 16:28 nun).
 1. Any petuchah/setumah claim naming a verse must match the marks inventory
    under the CORRECT mark type — PE and SAMEKH are never conflated (owner
    addendum). NON-IDENTITY BOOK: a cited verse number near a claim is
    checked under BOTH readings (direct MT and WEB-crosswalk-mapped MT) —
    outside chs 6-7 the readings coincide; a claim passes if EITHER carries
    the mark. NEAREST-MATCH diagnostics: a failed claim reports whether
    MT V±1 carries a mark — the off-by-one signature.
 2. SYMMETRY (unconditional): every span-relevant mark (front seam start-1,
    interior, end verse — WEB span crosswalk-mapped to MT keys) must be
    disclosed in the row's prose whether or not the prose engages the mark
    layer — tier-3 weak corroboration still requires disclosure when present
    (r3 contract: "all interior+edge marks vs pmarks").
 3. ABSENCE ARM, SPAN-SCOPED: "no petuchah/setumah" claims are checked
    against the marks inventory WITHIN the span-relevant (MT-mapped) set.
 4. ketiv/qere prose claims naming a verse must match the kq inventory
    (4 notes / 4 verses: MT 1:17, 2:11, 2:13, 4:9, MT-keyed; dual-reading
    like rule 1; NONE sit in the offset zone — the seam verse MT 7:1 =
    WEB 6:13 is NOT K/Q-bearing, unlike Eccl's seam).
 5. PASEQ-POSITION arm (WARN only): pmarks paseq is COUNT-ONLY (12 segs /
    12 verses; no offsets); intra-verse position claims are unsourceable.
Known limitation (Ezra finding, unchanged): the prose-window heuristic is
unreliable in BOTH directions in dense multi-ref prose — WARN-level only;
prose symmetry is model territory; structured-refs cites = citation_sweep.
Usage: check_marks.py rows.jsonl [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from song_lib import (LAST_VERSE, MT_LAST_VERSE, expand_ref_token,
                      load_pmarks, web_to_mt)

PARAMARK = re.compile(r"\b(petuchah|setumah)\b", re.I)
# bare pe/samekh flag only in mark-talk context (they are also letter names)
PARAMARK_LETTER = re.compile(r"\b(pe|samekh)\b(?!\w)", re.I)
MARKISH_CTX = re.compile(r"\b(?:mark|paragraph|division|petuchah|setumah|"
                         r"seg\b|layout|parashah)", re.I)
SELAH = re.compile(r"\bselah\b", re.I)
FABRICATED_SEGS = re.compile(r"\b(?:inverted|reversed)[\s-]?nun\b|"
                             r"\bsuspended\s+(?:letter|ayin|nun)\b", re.I)
SPECIAL_LETTER = re.compile(r"\b(?:small|large|x-small|x-large)\s+(?:letter|nun|ayin)\b|"
                            r"\bnun\s+ze[i']?ira\b|\bmajuscule\b|\bminuscule\b", re.I)
KQ = re.compile(r"\b(?:ketiv|qere|K/Q)\b", re.I)
VERSE_NEAR = re.compile(r"Song\.(\d+)\.(\d+)")
RANGE = re.compile(r"Song\.\d+\.\d+(?:-(?:Song\.)?\d+(?:\.\d+)?)?")
ABSENCE = re.compile(
    r"\bno\s+(?:petuchah|setumah|parashah|paragraph\s+mark)\b|"
    r"\bwithout\s+(?:a\s+|any\s+)?(?:petuchah|setumah|parashah)\b|"
    r"\blacks?\s+(?:a\s+|any\s+)?(?:petuchah|setumah|parashah)\b|"
    r"\b(?:petuchah|setumah|parashah)\b[^.;]{0,40}?\b(?:is|are)?\s*(?:absent|lacking)\b|"
    r"\b(?:absent|absence)\b[^.;]{0,40}?\b(?:petuchah|setumah|parashah)\b|"
    r"\b(?:petuchah|setumah|parashah)\b[^.;]{0,25}?\babsent\s+from\b", re.I)
PASEQ_POS = re.compile(
    r"\bpaseq\b[^.;]{0,60}?\b(?:after|before|between|precedes|follows|divides|"
    r"separates|splits|mid[\s-]?verse|caesura|colon|cola|hemistich|atnach|"
    r"athnach|first\s+half|second\s+half|word[\s-]?index|offset|midpoint)\b|"
    r"\b(?:after|before|between|mid[\s-]?verse|caesura|colon|cola|hemistich|"
    r"atnach|athnach|word[\s-]?index|offset|midpoint)\b[^.;]{0,60}?\bpaseq\b|"
    r"\b(?:mid[\s-]?verse|verse[\s-](?:initial|final|medial)|first|second|"
    r"third)\s+paseq\b|"
    r"\bpaseq\b[^.;]{0,40}?\b(?:position|placement|located|location|stands\s+"
    r"(?:after|before|between|at))\b", re.I)
PASEQ_POS_NEG = re.compile(
    r"\bnot\s+a\s+positional\b|\bno\s+(?:offset|placement|position|word[\s-]?index)\b|"
    r"\brecords?\s+no\b|\bcount[\s-]only\b|\bbare\s+count\b", re.I)


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def span_pairs(row):
    """Row span pairs in WEB numbering."""
    span = row.get("span") or ""
    m = RANGE.search(span if isinstance(span, str) else "")
    if not m:
        refs = row.get("boundary_evidence_refs", [])
        allp = []
        for r in refs:
            if r.startswith("oshb:"):
                continue
            for mm in RANGE.finditer(r):
                allp.extend(expand_ref_token(mm.group(0)))
        return sorted(set(allp))
    return expand_ref_token(m.group(0))


def relevant(pairs, inv):
    """Inventory entries relevant to a WEB span (front seam + interior + end),
    looked up at the CROSSWALK-MAPPED MT keys."""
    if not pairs:
        return {}
    want = {}
    c0, v0 = pairs[0]
    prev = (c0, v0 - 1) if v0 > 1 else (c0 - 1, LAST_VERSE.get(c0 - 1, 0))
    for c, v in [prev] + pairs:
        if not (c in LAST_VERSE and 1 <= v <= LAST_VERSE.get(c, 0)):
            continue
        mt = web_to_mt(c, v)
        if mt is None:
            continue
        k = f"Song.{mt[0]}.{mt[1]}"
        if inv.get(k):
            want[k] = inv[k]
    return want


def prose_of(row) -> str:
    parts = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k != "boundary_evidence_refs":
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            parts.append(o)
    walk(row)
    return "\n".join(parts)


def near_diag(inv, c, v):
    hits = [f"Song.{c}.{x}" for x in (v - 1, v + 1) if inv.get(f"Song.{c}.{x}")]
    return {"adjacent_mt_inventory_hits": hits} if hits else {}


def readings(c: int, v: int) -> list[tuple[int, int]]:
    """Both MT readings of a cited verse number: direct MT, and WEB->MT
    mapped. Coincide outside chs 6-7."""
    out = []
    if c in MT_LAST_VERSE and 1 <= v <= MT_LAST_VERSE[c]:
        out.append((c, v))
    mt = web_to_mt(c, v)
    if mt and mt not in out:
        out.append(mt)
    return out


def main() -> int:
    pm = load_pmarks()
    marks, kq = pm["marks"], pm["kq"]
    flags = []
    warns = []
    n = cited = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict):
                continue
            n += 1
            did = row.get("decision_id", "?")
            text = prose_of(row) + " " + " ".join(row.get("boundary_evidence_refs", []))
            # Rule 0: fabricated seg classes for Song
            for m in SELAH.finditer(text):
                flags.append({"decision_id": did, "rule": "selah_claim_in_song",
                              "note": "NO selah exists in Song (Psalter device)",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            for m in FABRICATED_SEGS.finditer(text):
                flags.append({"decision_id": did, "rule": "nonexistent_seg_claim_in_song",
                              "claim": m.group(0),
                              "note": "WLC Song carries no reversed-nun or suspended-letter segs",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            for m in SPECIAL_LETTER.finditer(text):
                flags.append({"decision_id": did, "rule": "special_letter_claim_in_song",
                              "claim": m.group(0),
                              "note": "WLC Song carries NO small/large-letter segs at all",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            # Rule 1: petuchah/setumah claims bind to the NEAREST windowed ref
            # under the CORRECT mark type, dual-reading (MT direct + WEB-mapped)
            markish = list(PARAMARK.finditer(text)) + [
                m for m in PARAMARK_LETTER.finditer(text)
                if MARKISH_CTX.search(text[max(0, m.start() - 60):m.start() + 60])]
            if markish:
                cited += 1
            for m in markish:
                word = m.group(0).lower()
                want_type = "PE" if word in ("petuchah", "pe") else "SAMEKH"
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                if not cands:
                    continue
                rel = m.start() - lo
                cands.sort(key=lambda vm: abs(vm.start() - rel))
                if any(want_type in marks.get(f"Song.{rc}.{rv}", [])
                       for vm in cands
                       for rc, rv in readings(int(vm.group(1)), int(vm.group(2)))):
                    continue
                if ABSENCE.search(ctx):
                    continue
                vm = cands[0]
                c, v = int(vm.group(1)), int(vm.group(2))
                got = {f"Song.{rc}.{rv}": marks.get(f"Song.{rc}.{rv}", [])
                       for rc, rv in readings(c, v)}
                flags.append({"decision_id": did, "rule": "paragraph_mark_claim",
                              "claimed": want_type, "verse_cited": f"Song.{c}.{v}",
                              "inventory_under_both_readings": got,
                              "note": ("mark TYPE mismatch — PE and SAMEKH are never conflated"
                                       if any(got.values()) else "no mark at the cited verse under either reading"),
                              **near_diag(marks, c, v)})
            # Rule 3: absence arm, span-scoped
            for am in ABSENCE.finditer(text):
                have = relevant(span_pairs(row), marks)
                if have:
                    flags.append({"decision_id": did, "rule": "false_mark_absence_claim",
                                  "claim_context": text[max(0, am.start() - 60):am.start() + 80],
                                  "span_relevant_marks_mt_keys": have})
                    break
            # Rule 2: symmetry over the span-relevant set (unconditional)
            want = relevant(span_pairs(row), marks)
            for ref, types in want.items():
                _, c, v = ref.split(".")
                near = re.compile(rf"{re.escape(ref)}|\b{c}[:.]{v}\b")
                disclosed = any(
                    PARAMARK.search(text[max(0, m.start() - 160):m.start() + 160])
                    or PARAMARK_LETTER.search(text[max(0, m.start() - 160):m.start() + 160])
                    for m in near.finditer(text))
                if not disclosed:
                    flags.append({"decision_id": did, "rule": "mark_symmetry_gap",
                                  "undisclosed_mt_key": ref, "mark_types": types,
                                  "row_cites_marks": bool(markish)})
            # WARN: paseq position assertions (inventory is count-only)
            for pm_ in PASEQ_POS.finditer(text):
                lo = max(0, pm_.start() - 120)
                ctx = text[lo:pm_.end() + 120]
                if PASEQ_POS_NEG.search(ctx):
                    continue
                warns.append({"decision_id": did, "rule": "paseq_position_warn",
                              "claim": pm_.group(0)[:120],
                              "note": "pmarks paseq is COUNT-ONLY (no offsets/"
                                      "word indices) — position is unsourceable",
                              "claim_context": text[lo:pm_.end() + 80]})
            # Rule 4: K/Q prose claims bind to the NEAREST windowed ref,
            # dual-reading (MT direct + WEB-mapped)
            for m in KQ.finditer(text):
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                if not cands:
                    continue
                rel = m.start() - lo
                cands.sort(key=lambda vm: abs(vm.start() - rel))
                if any(kq.get(f"Song.{rc}.{rv}")
                       for vm in cands
                       for rc, rv in readings(int(vm.group(1)), int(vm.group(2)))):
                    continue
                vm = cands[0]
                c, v = int(vm.group(1)), int(vm.group(2))
                flags.append({"decision_id": did, "rule": "kq_claim",
                              "verse_cited": f"Song.{c}.{v}", **near_diag(kq, c, v)})
    print(json.dumps({"rows_checked": n, "rows_citing_marks": cited,
                      "flag_count": len(flags), "flags": flags,
                      "warn_count": len(warns), "warns": warns,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
