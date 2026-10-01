#!/usr/bin/env python3
"""Lam citation sweep + dual-cite arithmetic checker (deterministic Tier-0).

Lam facts (Phase 0 byte-verified; ../web_mt_offset_map.json is authority):
Lam is an IDENTITY book: WEB and MT agree verse-for-verse in all five
chapters (22/22/66/22/22 = 154 each), NO offset zone, NO split; there are
NO title pseudo-refs: Lam.N.0 is ALWAYS invalid (Lam 1:1, the eikhah
opening, is an ordinary counted verse in BOTH witnesses). Therefore:
 - web:Lam.C.V and oshb:Lam.C.V share ONE ref space; each is still
   range-guarded against its witness's chapter table
 - RANGES are validated INCLUDING the end: both ends in range, start <= end,
   and single-verse spans must use the X-X form
 - any dual ref "web:Lam.a.b = oshb:Lam.c.d" must satisfy (a,b) == (c,d)
   (the identity crosswalk); "(MT n:m)" / "(WEB n:m)" qualifiers likewise
 - the OFFSET-ZONE DISCLOSURE arm is INERT (no zone exists) - kept for API
   parity; a written dual must still be arithmetically right
 - petuchah/setumah claims are VALIDATED against the marks inventory (WLC
   Lam: 5 PE + 84 SAMEKH over 89 verses - Writings: tier-3 weak): claimed
   TYPE must match the bytes (PE never conflated with SAMEKH),
   single-witness disclosure required, lookups at the MT key (= WEB key)
 - SELAH claims are ERRORS ANYWHERE (no selah exists in Lam); likewise
   reversed-nun, suspended-letter, LARGE-letter AND SMALL-letter claims -
   WLC Lam carries NO special-letter seg of any class (other_segs EMPTY)
 - paseq claims must match the inventory (11 segs / 10 verses; seg layer,
   never quotable as verse bytes; COUNT-ONLY); single-witness disclosure
   required
 - ketiv/qere claims at a ref must match the kq inventory (22 notes / 20
   verses; doubled-note verses 4:3 and 5:7)
 - cross-tradition material in boundary_evidence_refs is an ERROR: LXX /
   Septuagint / Old Greek / Vulgate / Peshitta / Targum / DSS / Qumran /
   4QLam / 3QLam / 5QLam. Lam note: LXX Lamentations carries a prose
   Jeremiah-ascription before 1:1 that MT/WLC and WEB do NOT carry - all of
   it stays cross-tradition METADATA in prose only, never a refs entry
 - HEBREW-QUOTE BINDING: every Hebrew run quoted in a row's prose must
   byte-collate against the verse of the NEAREST oshb: ref in the same field
   (pointed quotes must reach BYTE tier; nfd -> the nfd_degraded class =
   copy-degradation cured by normalize_hebrew_in_json - HARD at the writer
   gate per E-01; unpointed runs reach skeleton). A Hebrew quote with no
   oshb: ref in its field is flagged.
 - no ref may leave the Lam substrate
REV-ROUND ARMS carried from the upgraded Ps/Prov/Eccl/Song/Isa tool:
 - prose_pair_check validates prose dual-cites INCLUDING range forms with
   per-endpoint arithmetic (identity here)
 - prose-dual context window +-120 chars
 - input: .jsonl OR pretty-printed JSON array/object (sibling rows_from)
 - kq_web_quote_warn: a curly-quoted WEB span bound to a web: ref that covers
   a K/Q verse (MT key via crosswalk), with no ketiv/qere keyword in the row
Usage: citation_sweep.py [rows_file] (default freeze/frozen_rows_final.jsonl;
also accepts any JSONL or JSON-array file of rows with boundary_evidence_refs)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lam_lib import (LAST_VERSE, MT_LAST_VERSE, collate_hebrew,
                     expand_ref_token, load_pmarks, mt_to_web, mt_to_web_all,
                     web_quote_found, web_to_mt)

TOOLS = Path(__file__).resolve().parent
SP = TOOLS.parent

REF_RE = re.compile(
    r"^(web|oshb):Lam\.(\d+)\.(\d+)(?:-(?:Lam\.)?(\d+)(?:\.(\d+))?)?(.*)$")
CROSS = re.compile(r"\bLXX\b|\bSeptuagint\b|\bOld Greek\b|\bVulgate\b|\bGallican\b"
                   r"|\bPeshitta\b|\bTargum\b|\bDSS\b|\bQumran\b|\b4QLam|\b3QLam|\b5QLam"
                   r"|\b4Q\d|\b11Q|\b2Q\d", re.I)
HEB_RUN = re.compile(r"[֑-״]{2,}(?:[ ־][֑-״]+)*")
POINTED = re.compile(r"[ְ-ּׁׂ֑-֯]")
OSHB_REF = re.compile(r"oshb:Lam\.(\d+)\.(\d+)")
PROSE_PAIR = re.compile(
    r"web:Lam\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Lam\.)?(?:(\d+)\.)?(\d+))?"
    r"\s*[=(]+\s*(?:=\s*)?"
    r"oshb:Lam\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Lam\.)?(?:(\d+)\.)?(\d+))?")
QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:Lam\.\d+\.\d+(?:-(?:Lam\.)?\d+(?:\.\d+)?)?")
KQ_WORD = re.compile(r"\b(?:ketiv|qere|K/Q)\b", re.I)
MARK_WORD = re.compile(r"\b(petuchah|setumah)\b|\b(pe|samekh)\b(?!\w)", re.I)


def rows_from(p: Path):
    """Sibling-tool input contract: .jsonl one row per line, or a
    pretty-printed JSON array / {"decisions": [...]} object."""
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        if "decisions" in data:
            return data["decisions"]
        return [v for v in data.values() if isinstance(v, dict)]
    return data


def pair_ok_web_to_mt(wc: int, wv: int, oc: int, ov: int) -> bool:
    """A WEB/MT pairing is right iff the crosswalk maps it (identity in Lam)."""
    return web_to_mt(wc, wv) == (oc, ov)


def web_pairs_in_offset_zone(pairs) -> bool:
    return False   # Lam: no offset zone (identity book)


def mt_pairs_in_offset_zone(pairs) -> bool:
    return False   # Lam: no offset zone (identity book)


def main() -> int:
    rows_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SP / "freeze" / "frozen_rows_final.jsonl"
    pm = load_pmarks()
    marks, paseq, kq = pm["marks"], pm["paseq"], pm["kq"]
    small_letter_keys = {k: v for k, v in pm.get("other_segs", {}).items()}
    problems: list[str] = []
    prose_dual_warns: list[str] = []
    prose_pair_problems: list[str] = []
    nfd_degraded: list[str] = []
    kq_web_quote_warns: list[str] = []
    rows = rows_from(rows_path)

    oshb_texts = None
    web_texts = None

    for row in rows:
        did = row.get("decision_id", "?")
        # X-X span-form arm: row spans use the full Lam.a.b-Lam.c.d form
        span = row.get("span")
        if isinstance(span, str) and span.strip():
            s = span.strip().replace("web:", "")
            if not re.match(r"^Lam\.\d+\.\d+-Lam\.\d+\.\d+$", s):
                problems.append(f"{did}: span not in full X-X form "
                                f"(Lam.a.b-Lam.c.d, single verses included): {span!r}")
        for ref in row.get("boundary_evidence_refs", []):
            if CROSS.search(ref):
                problems.append(f"{did}: cross-tradition material in "
                                f"boundary_evidence_refs: {ref!r}")
                continue
            m = REF_RE.match(ref)
            if not m:
                problems.append(f"{did}: non-Lam or malformed ref {ref!r}")
                continue
            kind = m.group(1)
            ch, v = int(m.group(2)), int(m.group(3))
            e1, e2, tail = m.group(4), m.group(5), m.group(6)
            space = LAST_VERSE if kind == "web" else MT_LAST_VERSE
            last = space.get(ch)
            if last is None:
                problems.append(f"{did}: {ref!r} chapter out of range")
                continue
            if v == 0:
                problems.append(f"{did}: {ref!r} - Lam.{ch}.0 is always invalid "
                                f"(no title pseudo-verses exist in Lam)")
                continue
            if not (1 <= v <= last):
                problems.append(f"{did}: {ref!r} out of range for {kind.upper()} numbering")
                continue
            # range-END arm
            end_pair = (ch, v)
            if e1 is not None:
                ec, ev = (ch, int(e1)) if e2 is None else (int(e1), int(e2))
                elast = space.get(ec)
                if elast is None or not (1 <= ev <= elast):
                    problems.append(f"{did}: range END out of range: {ref!r}")
                elif (ec, ev) < (ch, v):
                    problems.append(f"{did}: range END precedes start: {ref!r}")
                else:
                    end_pair = (ec, ev)

            # dual/qualifier arithmetic via the crosswalk (identity book)
            has_disclosure = False
            pair = re.search(r"=\s*oshb:Lam\.(\d+)\.(\d+)", tail)
            if kind == "web" and pair:
                has_disclosure = True
                got = (int(pair.group(1)), int(pair.group(2)))
                want = web_to_mt(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book - expected oshb:Lam.{want[0]}.{want[1]}): {ref!r}")
            wpair = re.search(r"=\s*web:Lam\.(\d+)\.(\d+)", tail)
            if kind == "oshb" and wpair:
                has_disclosure = True
                got = (int(wpair.group(1)), int(wpair.group(2)))
                want = mt_to_web(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book - expected web:Lam.{want[0]}.{want[1]}): {ref!r}")
            off = re.search(r"\(MT\s+(\d+)[:.](\d+)", tail)
            if off:
                if kind != "web":
                    problems.append(f"{did}: MT qualifier on a non-web ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = web_to_mt(ch, v)
                    if (int(off.group(1)), int(off.group(2))) != want:
                        problems.append(f"{did}: MT qualifier wrong (crosswalk - "
                                        f"expected MT {want[0]}:{want[1]}): {ref!r}")
            woff = re.search(r"\(WEB\s+(\d+)[:.](\d+)", tail)
            if woff:
                if kind != "oshb":
                    problems.append(f"{did}: WEB qualifier on a non-oshb ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = mt_to_web(ch, v)
                    if (int(woff.group(1)), int(woff.group(2))) != want:
                        problems.append(f"{did}: WEB qualifier wrong (crosswalk - "
                                        f"expected WEB {want[0]}:{want[1]}): {ref!r}")

            # OFFSET-ZONE DISCLOSURE arm
            zone_pairs = [(ch, v), end_pair]
            in_zone = (web_pairs_in_offset_zone(zone_pairs) if kind == "web"
                       else mt_pairs_in_offset_zone(zone_pairs))
            if in_zone and not has_disclosure:
                problems.append(
                    f"{did}: offset-zone ref lacks dual-cite/qualifier "
                    f"disclosure (inert in Lam: identity book, no zone; "
                    f"numbering spaces - bare coordinates are ambiguous "
                    f"there): {ref!r}")

            # MT key for inventory lookups (web: refs crosswalk-mapped first)
            if kind == "web":
                mtc, mtv = web_to_mt(ch, v)
            else:
                mtc, mtv = ch, v
            key = f"Lam.{mtc}.{mtv}"

            # marks arm - claims validated under TYPE against the rich layer
            mm = MARK_WORD.search(tail)
            if mm:
                word = (mm.group(1) or mm.group(2)).lower()
                want_type = "PE" if word in ("petuchah", "pe") else "SAMEKH"
                got_types = marks.get(key, [])
                if want_type not in got_types:
                    problems.append(
                        f"{did}: {ref!r} claims {word} but the marks inventory "
                        f"has {got_types or 'none'} at {key} "
                        f"(PE and SAMEKH are never conflated)")
                if "single-witness" not in tail:
                    problems.append(f"{did}: parashah-mark ref lacks single-witness "
                                    f"disclosure (tier-3 in the Writings): {ref!r}")
            if re.search(r"\bselah\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims selah - NO selah exists "
                                f"in Lam (Psalter device; fabrication)")
            if re.search(r"\b(?:inverted|reversed)[\s-]*nun\b|\bsuspended\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a reversed-nun/suspended "
                                f"seg - WLC Lam carries neither")
            # patch i1 parity with check_marks: letter-name whitelist, no
            # catch-all [a-z]+ arm (the "small vessel" WEB-English class)
            if re.search(r"\b(?:large|x-large)\s+(?:letter|nun|ayin|mem|yod|waw|vav|kaf|pe|"
                         r"tsadi|qof|resh|shin|tav|aleph|alef|bet|gimel|dalet|he|het|tet|"
                         r"lamed|samekh|zayin)\b"
                         r"|\bmajuscule\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a large letter - WLC Lam "
                                f"carries NO special-letter segs of any class")
            if re.search(r"\b(?:small|x-small)\s+(?:letter|nun|ayin|mem|yod|waw|vav|kaf|pe|"
                         r"tsadi|qof|resh|shin|tav|aleph|alef|bet|gimel|dalet|he|het|tet|"
                         r"lamed|samekh|zayin)\b"
                         r"|\bze[i']?ira\b|\bminuscule\b", tail, re.I):
                if not small_letter_keys.get(key):
                    problems.append(f"{did}: {ref!r} claims a small letter but WLC "
                                    f"Lam carries NO special-letter segs of any class "
                                    f"(nothing at {key})")
                elif "single-witness" not in tail:
                    problems.append(f"{did}: small-letter ref lacks single-witness "
                                    f"disclosure: {ref!r}")
            if re.search(r"\bpaseq\b", tail, re.I):
                if not paseq.get(key):
                    problems.append(f"{did}: {ref!r} claims paseq but OSHB carries "
                                    f"none at {key}")
                if "single-witness" not in tail:
                    problems.append(f"{did}: paseq ref lacks single-witness disclosure: {ref!r}")
            if re.search(r"\b(?:ketiv|qere|K/Q)\b", tail, re.I) and not kq.get(key):
                problems.append(f"{did}: {ref!r} claims ketiv/qere but the kq "
                                f"inventory has none at {key}")

        # ---- prose EXPLICIT-PAIR arithmetic arm: a written
        # "web:Lam.a.b = oshb:Lam.c.d" asserts arithmetic wherever it
        # appears; crosswalk book - validated per endpoint for ranges.
        def prose_pair_check(o, path="row"):
            if isinstance(o, dict):
                for k2, v2 in o.items():
                    if k2 != "boundary_evidence_refs":
                        prose_pair_check(v2, f"{path}.{k2}")
            elif isinstance(o, list):
                for i, v2 in enumerate(o):
                    prose_pair_check(v2, f"{path}[{i}]")
            elif isinstance(o, str):
                for m in PROSE_PAIR.finditer(o):
                    g = m.groups()
                    wc, wv1 = int(g[0]), int(g[1])
                    wc2 = int(g[2]) if g[2] else wc
                    wv2 = int(g[3]) if g[3] else None
                    oc, ov1 = int(g[4]), int(g[5])
                    oc2 = int(g[6]) if g[6] else oc
                    ov2 = int(g[7]) if g[7] else None
                    ok = pair_ok_web_to_mt(wc, wv1, oc, ov1)
                    if wv2 is not None or ov2 is not None:
                        we = (wc2, wv2) if wv2 is not None else (wc, wv1)
                        oe = (oc2, ov2) if ov2 is not None else (oc, ov1)
                        ok = ok and pair_ok_web_to_mt(we[0], we[1], oe[0], oe[1])
                    if not ok:
                        prose_pair_problems.append(
                            f"{did}: prose dual-cite arithmetic wrong in {path} "
                            f"(identity book - WEB and MT coincide): {m.group(0)!r}")
        prose_pair_check(row)

        # ---- Hebrew-quote binding arm over every prose field ----
        def walk(o, path="row"):
            nonlocal oshb_texts
            if isinstance(o, dict):
                for k2, v2 in o.items():
                    if k2 != "boundary_evidence_refs":
                        walk(v2, f"{path}.{k2}")
            elif isinstance(o, list):
                for i, v2 in enumerate(o):
                    walk(v2, f"{path}[{i}]")
            elif isinstance(o, str):
                runs = [r for r in HEB_RUN.findall(o)
                        if len(re.sub(r"[^א-ת]", "", r)) >= 3]
                if not runs:
                    return
                refs = list(OSHB_REF.finditer(o))
                if oshb_texts is None:
                    oshb_texts = json.loads(
                        (TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
                for run in runs:
                    if not refs:
                        problems.append(f"{did}: Hebrew quote {run[:25]!r}… in "
                                        f"{path} has NO oshb: ref in its field")
                        continue
                    pos = o.find(run)
                    end = pos + len(run)
                    def keyf(mm):
                        follows = 0 <= mm.start() - end <= 40
                        dist = min(abs(mm.start() - pos), abs(mm.start() - end))
                        return (not follows, dist)
                    cands = sorted(refs, key=keyf)[:3]
                    pointed = bool(POINTED.search(run))
                    best = None
                    ok = False
                    nfd_hit = None
                    vkey = None
                    for near in cands:
                        vkey = f"Lam.{near.group(1)}.{near.group(2)}"
                        src = oshb_texts.get(vkey, {}).get("text", "")
                        tier = collate_hebrew(run, src)
                        if best is None:
                            best = (vkey, tier)
                        if (tier == "byte") if pointed else tier != "none":
                            ok = True
                            break
                        if pointed and tier == "nfd" and nfd_hit is None:
                            nfd_hit = vkey
                    if not ok and nfd_hit is not None:
                        vkey = nfd_hit
                        nfd_degraded.append(
                            f"{did}: pointed Hebrew quote {run[:25]!r}… in {path} "
                            f"collates against oshb:{nfd_hit} at NFD tier only "
                            f"(copy degradation - cure with "
                            f"normalize_hebrew_in_json.py --write)")
                    elif not ok:
                        problems.append(
                            f"{did}: Hebrew quote {run[:25]!r}… in {path} does not "
                            f"collate against any nearby cited ref (best "
                            f"oshb:{best[0]}, tier={best[1]}, "
                            f"{'pointed' if pointed else 'unpointed'})")
                    if (ok or nfd_hit is not None) and kq.get(vkey) and not re.search(
                            r"\b(?:ketiv|qere|K/Q)\b", o, re.I):
                        prose_dual_warns.append(
                            f"{did}: Hebrew quote in {path} binds to K/Q verse "
                            f"oshb:{vkey} with no ketiv/qere disclosure in-field")
        walk(row)

        # ---- K/Q WEB-quote arm (WARN) - MT keys via the crosswalk ----
        if not KQ_WORD.search(json.dumps(row, ensure_ascii=False)):
            covered_kq: dict[str, str] = {}

            def kq_web_walk(o, path="row"):
                nonlocal web_texts
                if isinstance(o, dict):
                    for k2, v2 in o.items():
                        if k2 != "boundary_evidence_refs":
                            kq_web_walk(v2, f"{path}.{k2}")
                elif isinstance(o, list):
                    for i, v2 in enumerate(o):
                        kq_web_walk(v2, f"{path}[{i}]")
                elif isinstance(o, str):
                    refs = [(m.start(), m.group(0)[4:]) for m in WREF.finditer(o)]
                    if not refs:
                        return
                    for qm in QUOTE.finditer(o):
                        span = qm.group(1).strip()
                        if len(span.split()) < 2:
                            continue
                        if len(re.findall(r"[֐-׿]", span)) > len(
                                re.findall(r"[A-Za-z]", span)):
                            continue
                        near = [r for pos, r in refs
                                if abs(pos - qm.start()) <= 200
                                or abs(pos - qm.end()) <= 200]
                        if not near:
                            continue
                        if web_texts is None:
                            web_texts = json.loads(
                                (TOOLS / "verse_map_web.json").read_text(
                                    encoding="utf-8"))
                        for r in near:
                            for c2, v2 in expand_ref_token(r):
                                t = web_texts.get(f"Lam.{c2}.{v2}", {}).get("text", "")
                                if not t or not web_quote_found(span, [t]):
                                    continue
                                mt = web_to_mt(c2, v2)
                                mtk = f"Lam.{mt[0]}.{mt[1]}"
                                if kq.get(mtk):
                                    covered_kq.setdefault(
                                        mtk,
                                        f"{path} {span[:60]!r} via web:Lam.{c2}.{v2}")
            kq_web_walk(row)
            for mtk, where in covered_kq.items():
                kq_web_quote_warns.append(
                    f"{did}: WEB quote covers K/Q verse oshb:{mtk} with no "
                    f"ketiv/qere disclosure anywhere in the row ({where})")

    print(json.dumps({"rows": len(rows), "rows_file": rows_path.name, "problems": problems,
                      "prose_dual_warn_count": len(prose_dual_warns),
                      "prose_pair_problem_count": len(prose_pair_problems),
                      "prose_pair_problems": prose_pair_problems[:20],
                      "prose_dual_warns": prose_dual_warns[:20],
                      "nfd_degraded_count": len(nfd_degraded),
                      "nfd_degraded": nfd_degraded[:20],
                      "kq_web_quote_warn_count": len(kq_web_quote_warns),
                      "kq_web_quote_warns": kq_web_quote_warns[:20],
                      "status": "GREEN" if not problems else "RED"}, ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
