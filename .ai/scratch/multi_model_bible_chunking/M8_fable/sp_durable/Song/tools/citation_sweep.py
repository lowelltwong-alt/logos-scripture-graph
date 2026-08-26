#!/usr/bin/env python3
"""Song citation sweep + dual-cite arithmetic checker (deterministic Tier-0).

Song facts (Phase 0 byte-verified; ../web_mt_offset_map.json is authority):
Song is NOT an identity book. MT 7:1 = WEB 6:13; MT 7:2-14 = WEB 7:1-13;
every other chapter identity; totals 117 = 117 / 8 chapters. There are NO
title pseudo-refs: Song.N.0 is ALWAYS invalid (Song 1:1, the superscription,
is an ordinary counted verse in BOTH witnesses). Therefore:
 - web:Song.C.V and oshb:Song.C.V are DIFFERENT ref spaces in chs 6-7; each
   is range-guarded against its own witness space
 - RANGES are validated INCLUDING the end: both ends in range, start <= end,
   and single-verse spans must use the X-X form
 - any dual ref "web:Song.a.b = oshb:Song.c.d" must satisfy
   web_to_mt(a,b) == (c,d); "(MT n:m)" / "(WEB n:m)" qualifiers likewise via
   the crosswalk
 - OFFSET-ZONE DISCLOSURE (orchestrator Tier-0 rule, Phase 0; inverted from
   the identity-book convention): a structured ref whose verses touch the
   offset zone (WEB 6:13 or WEB ch 7 for web: refs; MT ch 7 for oshb: refs)
   MUST carry an explicit dual or numeric qualifier in that entry — bare
   coordinates are ambiguous across witnesses exactly there. Elsewhere duals
   stay optional, but a written dual must be arithmetically right.
 - petuchah/setumah claims are VALIDATED against the marks inventory (WLC
   Song carries exactly 1 PE at MT 8:10 and 19 SAMEKH — a RICH Writings
   parashah layer that shadows the refrain skeleton, still tier-3 weak):
   claimed TYPE must match the bytes (PE never conflated with SAMEKH),
   single-witness disclosure required, and lookups happen at the MT KEY
   (web: refs are crosswalk-mapped first; MT 7:11 = WEB 7:10 is marked)
 - SELAH claims are ERRORS ANYWHERE (no selah exists in Song); likewise
   reversed-nun, suspended-letter, AND small/large-letter claims — WLC Song
   carries NO special-letter segs at all (like Eccl; unlike Prov's 16:28 nun)
 - paseq claims must match the inventory (12 segs / 12 verses; seg layer,
   never quotable as verse bytes); single-witness disclosure required
 - ketiv/qere claims at a ref must match the kq inventory (4 notes / 4
   verses — MT 1:17, 2:11, 2:13, 4:9; NONE in the offset zone; the seam
   verse MT 7:1 = WEB 6:13 is NOT K/Q-bearing, unlike Eccl's seam)
 - cross-tradition material in boundary_evidence_refs is an ERROR: LXX /
   Septuagint / Old Greek / Vulgate / Peshitta / Targum / DSS / Qumran.
   Song note: LXX numbering FOLLOWS MT at the 6:13/7:1 seam; the English
   division follows the Vulgate family — crosswalk METADATA in prose only
 - HEBREW-QUOTE BINDING: every Hebrew run quoted in a row's prose must
   byte-collate against the verse of the NEAREST oshb: ref in the same field
   (pointed quotes must reach BYTE tier; nfd -> the WARN class nfd_degraded =
   copy-degradation to be cured by normalize_hebrew_in_json; unpointed runs
   reach skeleton). A Hebrew quote with no oshb: ref in its field is flagged.
 - no ref may leave the Song substrate
REV-ROUND ARMS carried from the upgraded Ps/Prov tool:
 - prose_pair_check validates prose dual-cites INCLUDING range forms with
   per-endpoint CROSSWALK arithmetic (LIVE here, not identity)
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
from song_lib import (LAST_VERSE, MT_LAST_VERSE, collate_hebrew,
                      expand_ref_token, load_pmarks, mt_to_web,
                      web_quote_found, web_to_mt)

TOOLS = Path(__file__).resolve().parent
SP = TOOLS.parent

REF_RE = re.compile(
    r"^(web|oshb):Song\.(\d+)\.(\d+)(?:-(?:Song\.)?(\d+)(?:\.(\d+))?)?(.*)$")
CROSS = re.compile(r"\bLXX\b|\bSeptuagint\b|\bOld Greek\b|\bVulgate\b|\bGallican\b"
                   r"|\bPeshitta\b|\bTargum\b|\bDSS\b|\bQumran\b|\b4Q\d|\b11Q", re.I)
HEB_RUN = re.compile(r"[֑-״]{2,}(?:[ ־][֑-״]+)*")
POINTED = re.compile(r"[ְ-ּׁׂ֑-֯]")
OSHB_REF = re.compile(r"oshb:Song\.(\d+)\.(\d+)")
PROSE_PAIR = re.compile(
    r"web:Song\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Song\.)?(?:(\d+)\.)?(\d+))?"
    r"\s*[=(]+\s*(?:=\s*)?"
    r"oshb:Song\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Song\.)?(?:(\d+)\.)?(\d+))?")
QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:Song\.\d+\.\d+(?:-(?:Song\.)?\d+(?:\.\d+)?)?")
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
    """A WEB/MT pairing is right iff the crosswalk maps it, both in range."""
    return web_to_mt(wc, wv) == (oc, ov) and mt_to_web(oc, ov) == (wc, wv)


def web_pairs_in_offset_zone(pairs) -> bool:
    return any((c == 6 and v == 13) or c == 7 for c, v in pairs)


def mt_pairs_in_offset_zone(pairs) -> bool:
    return any(c == 7 for c, _ in pairs)


def main() -> int:
    rows_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SP / "freeze" / "frozen_rows_final.jsonl"
    pm = load_pmarks()
    marks, paseq, kq = pm["marks"], pm["paseq"], pm["kq"]
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
        # X-X span-form arm: row spans use the full Song.a.b-Song.c.d form
        span = row.get("span")
        if isinstance(span, str) and span.strip():
            s = span.strip().replace("web:", "")
            if not re.match(r"^Song\.\d+\.\d+-Song\.\d+\.\d+$", s):
                problems.append(f"{did}: span not in full X-X form "
                                f"(Song.a.b-Song.c.d, single verses included): {span!r}")
        for ref in row.get("boundary_evidence_refs", []):
            if CROSS.search(ref):
                problems.append(f"{did}: cross-tradition material in "
                                f"boundary_evidence_refs: {ref!r}")
                continue
            m = REF_RE.match(ref)
            if not m:
                problems.append(f"{did}: non-Song or malformed ref {ref!r}")
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
                problems.append(f"{did}: {ref!r} — Song.{ch}.0 is always invalid "
                                f"(no title pseudo-verses exist in Song)")
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

            # dual/qualifier arithmetic via the crosswalk
            has_disclosure = False
            pair = re.search(r"=\s*oshb:Song\.(\d+)\.(\d+)", tail)
            if kind == "web" and pair:
                has_disclosure = True
                got = (int(pair.group(1)), int(pair.group(2)))
                want = web_to_mt(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book — expected oshb:Song.{want[0]}.{want[1]}): {ref!r}")
            wpair = re.search(r"=\s*web:Song\.(\d+)\.(\d+)", tail)
            if kind == "oshb" and wpair:
                has_disclosure = True
                got = (int(wpair.group(1)), int(wpair.group(2)))
                want = mt_to_web(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book — expected web:Song.{want[0]}.{want[1]}): {ref!r}")
            off = re.search(r"\(MT\s+(\d+)[:.](\d+)", tail)
            if off:
                if kind != "web":
                    problems.append(f"{did}: MT qualifier on a non-web ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = web_to_mt(ch, v)
                    if (int(off.group(1)), int(off.group(2))) != want:
                        problems.append(f"{did}: MT qualifier wrong (crosswalk — "
                                        f"expected MT {want[0]}:{want[1]}): {ref!r}")
            woff = re.search(r"\(WEB\s+(\d+)[:.](\d+)", tail)
            if woff:
                if kind != "oshb":
                    problems.append(f"{did}: WEB qualifier on a non-oshb ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = mt_to_web(ch, v)
                    if (int(woff.group(1)), int(woff.group(2))) != want:
                        problems.append(f"{did}: WEB qualifier wrong (crosswalk — "
                                        f"expected WEB {want[0]}:{want[1]}): {ref!r}")

            # OFFSET-ZONE DISCLOSURE arm
            zone_pairs = [(ch, v), end_pair]
            in_zone = (web_pairs_in_offset_zone(zone_pairs) if kind == "web"
                       else mt_pairs_in_offset_zone(zone_pairs))
            if in_zone and not has_disclosure:
                problems.append(
                    f"{did}: offset-zone ref lacks dual-cite/qualifier "
                    f"disclosure (WEB 6:13 + WEB ch 7 / MT ch 7 are DIFFERENT "
                    f"numbering spaces — bare coordinates are ambiguous "
                    f"there): {ref!r}")

            # MT key for inventory lookups (web: refs crosswalk-mapped first)
            if kind == "web":
                mtc, mtv = web_to_mt(ch, v)
            else:
                mtc, mtv = ch, v
            key = f"Song.{mtc}.{mtv}"

            # marks arm — nearly-empty layer; claims validated under TYPE
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
                                    f"disclosure (tier-3 in Writings): {ref!r}")
            if re.search(r"\bselah\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims selah — NO selah exists "
                                f"in Song (Psalter device; fabrication)")
            if re.search(r"\b(?:inverted|reversed)[\s-]*nun\b|\bsuspended\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a reversed-nun/suspended "
                                f"seg — WLC Song carries neither")
            if re.search(r"\b(?:small|large|x-small|x-large)\s+(?:letter|nun|ayin|"
                         r"[a-z]+)\b|\bze[i']?ira\b|\bmajuscule\b|\bminuscule\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a small/large letter — "
                                f"WLC Song carries NO special-letter segs at all")
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
        # "web:Song.a.b = oshb:Song.c.d" asserts arithmetic wherever it
        # appears; crosswalk book — validated per endpoint for ranges.
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
                            f"(crosswalk book — WEB 6:13 + WEB 7:1-13 map to MT 7:1-14): "
                            f"{m.group(0)!r}")
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
                        vkey = f"Song.{near.group(1)}.{near.group(2)}"
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
                            f"(copy degradation — cure with "
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

        # ---- K/Q WEB-quote arm (WARN) — MT keys via the crosswalk ----
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
                                t = web_texts.get(f"Song.{c2}.{v2}", {}).get("text", "")
                                if not t or not web_quote_found(span, [t]):
                                    continue
                                mt = web_to_mt(c2, v2)
                                mtk = f"Song.{mt[0]}.{mt[1]}"
                                if kq.get(mtk):
                                    covered_kq.setdefault(
                                        mtk,
                                        f"{path} {span[:60]!r} via web:Song.{c2}.{v2}")
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
