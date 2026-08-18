#!/usr/bin/env python3
"""Prov citation sweep + dual-cite arithmetic checker (deterministic Tier-0).

Prov facts (Phase 0 byte-verified; ../web_mt_offset_map.json is authority):
WEB 915 / MT 915 — IDENTITY at every chapter (per-chapter counts, 123
content anchors with the one miss byte-reviewed, zero OSHB KJV-variance
notes, and the 31:10-31 acrostic as a 22-point ch-31 anchor). There are NO
title pseudo-refs: Prov.N.0 is ALWAYS invalid; the collection headers are
ordinary counted verses. Therefore:
 - web:Prov.C.V and oshb:Prov.C.V share one numbering space; both are
   range-guarded against it
 - RANGES are validated INCLUDING the end (lesson-j range-END arm): both ends
   in range, start <= end, and single-verse spans must use the X-X form
 - any dual ref "web:Prov.a.b = oshb:Prov.c.d" must satisfy (a,b) == (c,d)
   (identity); same for "(MT n:m)" / "(WEB n:m)" qualifiers. Duals are never
   REQUIRED in an identity book — but a written dual must be arithmetically
   right
 - petuchah/setumah/pe/samekh claims are VALIDATED against the marks
   inventory (Prov carries 51 PE + 1 SAMEKH — Writings parashah, tier-3
   weak): claimed TYPE must match the bytes (PE never conflated with
   SAMEKH), and single-witness disclosure is required
 - SELAH claims are ERRORS ANYWHERE (no selah exists in Prov); likewise
   reversed-nun and suspended-letter claims (no such segs in WLC Prov)
 - small-letter claims must sit at Prov.16.28 (the one x-small nun) with
   single-witness disclosure
 - paseq claims must match the inventory (60 segs / 57 verses; seg layer,
   never quotable as verse bytes); single-witness disclosure required
 - ketiv/qere claims at a ref must match the kq inventory (69 notes / 63
   verses) — the lesson-j K/Q arm
 - cross-tradition material in boundary_evidence_refs is an ERROR: LXX /
   Septuagint / Old Greek / Vulgate / Peshitta / Targum / DSS / Qumran.
   Extra Prov hazard: LXX REORDERS 24:23-34 and chs 30-31 — Greek ordering
   is cross-tradition metadata; prose comparisons need an explicit
   crosswalk statement and it never enters refs
 - HEBREW-QUOTE BINDING (lesson-j collate arm): every Hebrew run quoted in a
   row's prose must byte-collate against the verse of the NEAREST oshb: ref
   in the same field (pointed quotes must reach BYTE tier; nfd -> the WARN
   class nfd_degraded = copy-degradation to be cured by
   normalize_hebrew_in_json; unpointed runs reach skeleton). A Hebrew quote
   with no oshb: ref in its field is flagged.
 - no ref may leave the Prov substrate
REV-ROUND ARMS carried from the upgraded Ps tool (attempt revround_tools_ps_r1):
 - pointed Hebrew runs must reach BYTE tier; nfd -> nfd_degraded WARN
 - prose_pair_check validates prose dual-cites INCLUDING range forms with
   per-endpoint arithmetic (identity here)
 - prose-dual context window +-120 chars
 - input: .jsonl OR pretty-printed JSON array/object (sibling rows_from)
 - kq_web_quote_warn: a curly-quoted WEB span bound to a web: ref that covers
   a K/Q verse, with no ketiv/qere keyword anywhere in the row
(The Ps prose-dual ARM for non-identity psalms is a verified NO-OP in an
identity book and is omitted; prose PAIR arithmetic is retained.)
Usage: citation_sweep.py [rows_file] (default freeze/frozen_rows_final.jsonl;
also accepts any JSONL or JSON-array file of rows with boundary_evidence_refs)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prov_lib import (LAST_VERSE, MT_LAST_VERSE, collate_hebrew,
                      expand_ref_token, load_pmarks, web_quote_found,
                      web_to_mt)

TOOLS = Path(__file__).resolve().parent
SP = TOOLS.parent

REF_RE = re.compile(
    r"^(web|oshb):Prov\.(\d+)\.(\d+)(?:-(?:Prov\.)?(\d+)(?:\.(\d+))?)?(.*)$")
CROSS = re.compile(r"\bLXX\b|\bSeptuagint\b|\bOld Greek\b|\bVulgate\b|\bGallican\b"
                   r"|\bPeshitta\b|\bTargum\b|\bDSS\b|\bQumran\b|\b4Q\d|\b11Q", re.I)
HEB_RUN = re.compile(r"[֑-״]{2,}(?:[ ־][֑-״]+)*")
POINTED = re.compile(r"[ְ-ּׁׂ֑-֯]")
OSHB_REF = re.compile(r"oshb:Prov\.(\d+)\.(\d+)")
PROSE_PAIR = re.compile(
    r"web:Prov\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Prov\.)?(?:(\d+)\.)?(\d+))?"
    r"\s*[=(]+\s*(?:=\s*)?"
    r"oshb:Prov\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Prov\.)?(?:(\d+)\.)?(\d+))?")
QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:Prov\.\d+\.\d+(?:-(?:Prov\.)?\d+(?:\.\d+)?)?")
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


def ident_ok(wc: int, wv: int, oc: int, ov: int) -> bool:
    """Identity book: a WEB/MT pairing is right iff the coordinates match
    and are in range."""
    return (wc, wv) == (oc, ov) and web_to_mt(wc, wv) == (oc, ov)


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
        # X-X span-form arm: row spans use the full Prov.a.b-Prov.c.d form
        span = row.get("span")
        if isinstance(span, str) and span.strip():
            s = span.strip().replace("web:", "")
            if not re.match(r"^Prov\.\d+\.\d+-Prov\.\d+\.\d+$", s):
                problems.append(f"{did}: span not in full X-X form "
                                f"(Prov.a.b-Prov.c.d, single verses included): {span!r}")
        for ref in row.get("boundary_evidence_refs", []):
            if CROSS.search(ref):
                problems.append(f"{did}: cross-tradition material in "
                                f"boundary_evidence_refs: {ref!r}")
                continue
            m = REF_RE.match(ref)
            if not m:
                problems.append(f"{did}: non-Prov or malformed ref {ref!r}")
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
                problems.append(f"{did}: {ref!r} — Prov.{ch}.0 is always invalid "
                                f"(no title pseudo-verses exist in Prov)")
                continue
            if not (1 <= v <= last):
                problems.append(f"{did}: {ref!r} out of range for {kind.upper()} numbering")
                continue
            # range-END arm (lesson j)
            if e1 is not None:
                ec, ev = (ch, int(e1)) if e2 is None else (int(e1), int(e2))
                elast = space.get(ec)
                if elast is None or not (1 <= ev <= elast):
                    problems.append(f"{did}: range END out of range: {ref!r}")
                elif (ec, ev) < (ch, v):
                    problems.append(f"{did}: range END precedes start: {ref!r}")

            pair = re.search(r"=\s*oshb:Prov\.(\d+)\.(\d+)", tail)
            if kind == "web" and pair:
                got = (int(pair.group(1)), int(pair.group(2)))
                if got != (ch, v):
                    problems.append(f"{did}: dual-cite arithmetic wrong (identity "
                                    f"book — expected oshb:Prov.{ch}.{v}): {ref!r}")
            wpair = re.search(r"=\s*web:Prov\.(\d+)\.(\d+)", tail)
            if kind == "oshb" and wpair:
                got = (int(wpair.group(1)), int(wpair.group(2)))
                if got != (ch, v):
                    problems.append(f"{did}: dual-cite arithmetic wrong (identity "
                                    f"book — expected web:Prov.{ch}.{v}): {ref!r}")
            off = re.search(r"\(MT\s+(\d+)[:.](\d+)", tail)
            if off:
                if kind != "web":
                    problems.append(f"{did}: MT qualifier on a non-web ref: {ref!r}")
                elif (int(off.group(1)), int(off.group(2))) != (ch, v):
                    problems.append(f"{did}: MT qualifier wrong (identity book — "
                                    f"expected MT {ch}:{v}): {ref!r}")
            woff = re.search(r"\(WEB\s+(\d+)[:.](\d+)", tail)
            if woff:
                if kind != "oshb":
                    problems.append(f"{did}: WEB qualifier on a non-oshb ref: {ref!r}")
                elif (int(woff.group(1)), int(woff.group(2))) != (ch, v):
                    problems.append(f"{did}: WEB qualifier wrong (identity book — "
                                    f"expected WEB {ch}:{v}): {ref!r}")

            key = f"Prov.{ch}.{v}"

            # marks arm — INVERTED from Ps: Prov HAS a parashah layer; claims
            # are validated against the inventory under the claimed TYPE
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
                                f"in Prov (Psalter device; fabrication)")
            if re.search(r"\b(?:inverted|reversed)[\s-]*nun\b|\bsuspended\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a reversed-nun/suspended "
                                f"seg — WLC Prov carries neither")
            if re.search(r"\bsmall\s+(?:letter|nun)\b|\bze[i']?ira\b", tail, re.I):
                if key != "Prov.16.28":
                    problems.append(f"{did}: {ref!r} claims a small letter but the "
                                    f"only x-small seg in WLC Prov is the nun at "
                                    f"Prov.16.28")
                if "single-witness" not in tail:
                    problems.append(f"{did}: small-letter ref lacks single-witness disclosure: {ref!r}")
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
        # "web:Prov.a.b = oshb:Prov.c.d" asserts arithmetic wherever it
        # appears; identity book — the pair must be coordinate-equal,
        # per endpoint for ranges.
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
                    ok = ident_ok(wc, wv1, oc, ov1)
                    if wv2 is not None or ov2 is not None:
                        we = (wc2, wv2) if wv2 is not None else (wc, wv1)
                        oe = (oc2, ov2) if ov2 is not None else (oc, ov1)
                        ok = ok and ident_ok(we[0], we[1], oe[0], oe[1])
                    if not ok:
                        prose_pair_problems.append(
                            f"{did}: prose dual-cite arithmetic wrong in {path} "
                            f"(identity book — WEB and MT coordinates must be "
                            f"equal): {m.group(0)!r}")
        prose_pair_check(row)

        # ---- Hebrew-quote binding arm (lesson j) over every prose field ----
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
                        vkey = f"Prov.{near.group(1)}.{near.group(2)}"
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

        # ---- K/Q WEB-quote arm (WARN, OL-c30 gate hole) ----
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
                                t = web_texts.get(f"Prov.{c2}.{v2}", {}).get("text", "")
                                if not t or not web_quote_found(span, [t]):
                                    continue
                                if kq.get(f"Prov.{c2}.{v2}"):
                                    covered_kq.setdefault(
                                        f"Prov.{c2}.{v2}",
                                        f"{path} {span[:60]!r} via web:Prov.{c2}.{v2}")
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
