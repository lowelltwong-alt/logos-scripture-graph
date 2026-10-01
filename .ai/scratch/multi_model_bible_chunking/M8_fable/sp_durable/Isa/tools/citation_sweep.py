#!/usr/bin/env python3
"""Isa citation sweep + dual-cite arithmetic checker (deterministic Tier-0).

Isa facts (Phase 0 byte-verified; ../web_mt_offset_map.json is authority):
Isa is NOT an identity book and carries TWO offset zones with DIFFERENT
shapes. ZONE A (chs 8-9, renumbering): MT 8:23 = WEB 9:1; MT 9:1-20 =
WEB 9:2-21. ZONE B (chs 63-64, a SPLIT): MT 63:19 spans WEB 63:19 + WEB
64:1; MT 64:1-11 = WEB 64:2-12. Every other chapter identity; totals WEB
1292 / MT 1291 / 66 chapters. There are NO title pseudo-refs: Isa.N.0 is
ALWAYS invalid (Isa 1:1, the chazon superscription, is an ordinary counted
verse in BOTH witnesses). Therefore:
 - web:Isa.C.V and oshb:Isa.C.V are DIFFERENT ref spaces in chs 8-9 and
   63-64; each is range-guarded against its own witness space
 - RANGES are validated INCLUDING the end: both ends in range, start <= end,
   and single-verse spans must use the X-X form
 - any dual ref "web:Isa.a.b = oshb:Isa.c.d" must satisfy
   web_to_mt(a,b) == (c,d); "oshb:Isa.c.d = web:Isa.a.b" must satisfy
   (a,b) IN mt_to_web_all(c,d) — the SPLIT verse MT 63:19 legitimately
   pairs with EITHER WEB 63:19 or WEB 64:1; "(MT n:m)" / "(WEB n:m)"
   qualifiers likewise via the crosswalk
 - OFFSET-ZONE DISCLOSURE (orchestrator Tier-0 rule, Phase 0; the Song R1
   pattern, pending gate ratification): a structured ref whose verses touch
   an offset zone (WEB ch 9, WEB ch 64, or WEB 63:19 for web: refs; MT
   8:23, MT ch 9, MT 63:19, or MT ch 64 for oshb: refs) MUST carry an
   explicit dual or numeric qualifier in that entry — bare coordinates are
   ambiguous across witnesses exactly there (and the split verse is
   ambiguous even at EQUAL numerals: web:Isa.63.19 is HALF of
   oshb:Isa.63.19). Elsewhere duals stay optional, but a written dual must
   be arithmetically right.
 - petuchah/setumah claims are VALIDATED against the marks inventory (WLC
   Isa carries the campaign's LARGEST parashah layer: 41 PE + 168 SAMEKH
   over 209 verses — Prophets: tier-3 weak): claimed TYPE must match the
   bytes (PE never conflated with SAMEKH), single-witness disclosure
   required, and lookups happen at the MT KEY (web: refs are
   crosswalk-mapped first)
 - SELAH claims are ERRORS ANYWHERE (no selah exists in Isa); likewise
   reversed-nun, suspended-letter, and LARGE-letter claims — WLC Isa
   carries exactly ONE special-letter seg: a SMALL NUN at MT 44:14. A
   small-letter claim is validated against that inventory (valid ONLY at
   MT 44:14); everywhere else it is a fabrication. (The famous MT 9:6
   medial final-mem in לםרבה is in the LETTER BYTES, not a seg — prose may
   discuss it as K/Q apparatus, never as a small/large-letter seg.)
 - paseq claims must match the inventory (95 segs / 87 verses; seg layer,
   never quotable as verse bytes; COUNT-ONLY); single-witness disclosure
   required
 - ketiv/qere claims at a ref must match the kq inventory (53 notes / 49
   verses — the campaign's largest; TWO inside zone A: MT 9:2 and MT 9:6;
   NONE in zone B — the split verse MT 63:19 is NOT K/Q-bearing)
 - cross-tradition material in boundary_evidence_refs is an ERROR: LXX /
   Septuagint / Old Greek / Vulgate / Peshitta / Targum / DSS / Qumran /
   1QIsa. Isa note: the great Isaiah scroll (1QIsa-a) is a famous witness —
   it remains cross-tradition METADATA in prose only, never a refs entry
 - HEBREW-QUOTE BINDING: every Hebrew run quoted in a row's prose must
   byte-collate against the verse of the NEAREST oshb: ref in the same field
   (pointed quotes must reach BYTE tier; nfd -> the WARN class nfd_degraded =
   copy-degradation to be cured by normalize_hebrew_in_json; unpointed runs
   reach skeleton). A Hebrew quote with no oshb: ref in its field is flagged.
 - no ref may leave the Isa substrate
REV-ROUND ARMS carried from the upgraded Ps/Prov/Eccl/Song tool:
 - prose_pair_check validates prose dual-cites INCLUDING range forms with
   per-endpoint CROSSWALK arithmetic (LIVE here, split-aware)
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
from isa_lib import (LAST_VERSE, MT_LAST_VERSE, SPLIT_MT, collate_hebrew,
                     expand_ref_token, load_pmarks, mt_to_web, mt_to_web_all,
                     web_quote_found, web_to_mt)

TOOLS = Path(__file__).resolve().parent
SP = TOOLS.parent

REF_RE = re.compile(
    r"^(web|oshb):Isa\.(\d+)\.(\d+)(?:-(?:Isa\.)?(\d+)(?:\.(\d+))?)?(.*)$")
CROSS = re.compile(r"\bLXX\b|\bSeptuagint\b|\bOld Greek\b|\bVulgate\b|\bGallican\b"
                   r"|\bPeshitta\b|\bTargum\b|\bDSS\b|\bQumran\b|\b1QIsa|\b4Q\d|\b11Q", re.I)
HEB_RUN = re.compile(r"[֑-״]{2,}(?:[ ־][֑-״]+)*")
POINTED = re.compile(r"[ְ-ּׁׂ֑-֯]")
OSHB_REF = re.compile(r"oshb:Isa\.(\d+)\.(\d+)")
PROSE_PAIR = re.compile(
    r"web:Isa\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Isa\.)?(?:(\d+)\.)?(\d+))?"
    r"\s*[=(]+\s*(?:=\s*)?"
    r"oshb:Isa\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Isa\.)?(?:(\d+)\.)?(\d+))?")
QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:Isa\.\d+\.\d+(?:-(?:Isa\.)?\d+(?:\.\d+)?)?")
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
    """A WEB/MT pairing is right iff the crosswalk maps it (split-aware: the
    WEB member must be one of the MT verse's halves)."""
    return web_to_mt(wc, wv) == (oc, ov) and (wc, wv) in mt_to_web_all(oc, ov)


def web_pairs_in_offset_zone(pairs) -> bool:
    return any(c == 9 or c == 64 or (c, v) == (63, 19) for c, v in pairs)


def mt_pairs_in_offset_zone(pairs) -> bool:
    return any((c == 8 and v == 23) or c == 9 or (c, v) == SPLIT_MT or c == 64
               for c, v in pairs)


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
        # X-X span-form arm: row spans use the full Isa.a.b-Isa.c.d form
        span = row.get("span")
        if isinstance(span, str) and span.strip():
            s = span.strip().replace("web:", "")
            if not re.match(r"^Isa\.\d+\.\d+-Isa\.\d+\.\d+$", s):
                problems.append(f"{did}: span not in full X-X form "
                                f"(Isa.a.b-Isa.c.d, single verses included): {span!r}")
        for ref in row.get("boundary_evidence_refs", []):
            if CROSS.search(ref):
                problems.append(f"{did}: cross-tradition material in "
                                f"boundary_evidence_refs: {ref!r}")
                continue
            m = REF_RE.match(ref)
            if not m:
                problems.append(f"{did}: non-Isa or malformed ref {ref!r}")
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
                problems.append(f"{did}: {ref!r} — Isa.{ch}.0 is always invalid "
                                f"(no title pseudo-verses exist in Isa)")
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

            # dual/qualifier arithmetic via the crosswalk (split-aware)
            has_disclosure = False
            pair = re.search(r"=\s*oshb:Isa\.(\d+)\.(\d+)", tail)
            if kind == "web" and pair:
                has_disclosure = True
                got = (int(pair.group(1)), int(pair.group(2)))
                want = web_to_mt(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book — expected oshb:Isa.{want[0]}.{want[1]}): {ref!r}")
            wpair = re.search(r"=\s*web:Isa\.(\d+)\.(\d+)", tail)
            if kind == "oshb" and wpair:
                has_disclosure = True
                got = (int(wpair.group(1)), int(wpair.group(2)))
                wants = mt_to_web_all(ch, v)
                if got not in wants:
                    exp = " or ".join(f"web:Isa.{a}.{b}" for a, b in wants)
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book — expected {exp}): {ref!r}")
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
                    wants = mt_to_web_all(ch, v)
                    if (int(woff.group(1)), int(woff.group(2))) not in wants:
                        exp = " or ".join(f"WEB {a}:{b}" for a, b in wants)
                        problems.append(f"{did}: WEB qualifier wrong (crosswalk — "
                                        f"expected {exp}): {ref!r}")
            # the split verse also accepts an explicit half-word disclosure
            if not has_disclosure and re.search(
                    r"\b(?:first|second)\s+half\b|\bsplit\b", tail, re.I) and \
                    ((kind == "web" and (ch, v) in ((63, 19), (64, 1))) or
                     (kind == "oshb" and (ch, v) == SPLIT_MT)):
                has_disclosure = True

            # OFFSET-ZONE DISCLOSURE arm
            zone_pairs = [(ch, v), end_pair]
            in_zone = (web_pairs_in_offset_zone(zone_pairs) if kind == "web"
                       else mt_pairs_in_offset_zone(zone_pairs))
            if in_zone and not has_disclosure:
                problems.append(
                    f"{did}: offset-zone ref lacks dual-cite/qualifier "
                    f"disclosure (WEB ch 9 / WEB ch 64 / WEB 63:19 and MT 8:23 / "
                    f"MT ch 9 / MT 63:19 / MT ch 64 are DIFFERENT or PARTIAL "
                    f"numbering spaces — bare coordinates are ambiguous "
                    f"there): {ref!r}")

            # MT key for inventory lookups (web: refs crosswalk-mapped first)
            if kind == "web":
                mtc, mtv = web_to_mt(ch, v)
            else:
                mtc, mtv = ch, v
            key = f"Isa.{mtc}.{mtv}"

            # marks arm — claims validated under TYPE against the rich layer
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
                                    f"disclosure (tier-3 in Prophets): {ref!r}")
            if re.search(r"\bselah\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims selah — NO selah exists "
                                f"in Isa (Psalter device; fabrication)")
            if re.search(r"\b(?:inverted|reversed)[\s-]*nun\b|\bsuspended\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a reversed-nun/suspended "
                                f"seg — WLC Isa carries neither")
            # patch i1 parity with check_marks: letter-name whitelist, no
            # catch-all [a-z]+ arm (the "small vessel" WEB-English class)
            if re.search(r"\b(?:large|x-large)\s+(?:letter|nun|ayin|mem|yod|waw|vav|kaf|pe|"
                         r"tsadi|qof|resh|shin|tav|aleph|alef|bet|gimel|dalet|he|het|tet|"
                         r"lamed|samekh|zayin)\b"
                         r"|\bmajuscule\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a large letter — WLC Isa "
                                f"carries NO large-letter segs (its only special "
                                f"letter is the small nun at MT 44:14)")
            if re.search(r"\b(?:small|x-small)\s+(?:letter|nun|ayin|mem|yod|waw|vav|kaf|pe|"
                         r"tsadi|qof|resh|shin|tav|aleph|alef|bet|gimel|dalet|he|het|tet|"
                         r"lamed|samekh|zayin)\b"
                         r"|\bze[i']?ira\b|\bminuscule\b", tail, re.I):
                if not small_letter_keys.get(key):
                    problems.append(f"{did}: {ref!r} claims a small letter but WLC "
                                    f"Isa's only special-letter seg is the small "
                                    f"nun at Isa.44.14 (nothing at {key})")
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
        # "web:Isa.a.b = oshb:Isa.c.d" asserts arithmetic wherever it
        # appears; crosswalk book — validated per endpoint for ranges,
        # split-aware (WEB 63:19 and WEB 64:1 both pair with MT 63:19).
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
                            f"(crosswalk book — WEB 9:1 = MT 8:23, WEB 9:2-21 = "
                            f"MT 9:1-20, WEB 63:19 + 64:1 = MT 63:19, WEB 64:2-12 "
                            f"= MT 64:1-11): {m.group(0)!r}")
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
                        vkey = f"Isa.{near.group(1)}.{near.group(2)}"
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
                                t = web_texts.get(f"Isa.{c2}.{v2}", {}).get("text", "")
                                if not t or not web_quote_found(span, [t]):
                                    continue
                                mt = web_to_mt(c2, v2)
                                mtk = f"Isa.{mt[0]}.{mt[1]}"
                                if kq.get(mtk):
                                    covered_kq.setdefault(
                                        mtk,
                                        f"{path} {span[:60]!r} via web:Isa.{c2}.{v2}")
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
