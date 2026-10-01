#!/usr/bin/env python3
"""REPAIR-2 step 4, the MECHANICAL arm: derive the face qualifier for wave-installed WARRANT-onset/close tokens.

THE ORDER, from #e15 Q5 clause 6 v2 retro_qualification: "every WARRANT-onset and WARRANT-close token this wave
installed receives its derived face qualifier by a mechanical sweep (derivable from verse and span; adds
information; changes no claim), distinct-checked. WARRANT-rival tokens receive the qualifier and seam pair in the
author repair batch (author work: the seam must be read off the SRA). Pre-wave descriptive entries are still not
re-tokenised."

THE FACES, from the same clause: ':near' is the seam verse INSIDE the unit the seam bounds - the row's first
verse for its onset, its last verse for its close. ':far' is the adjacent verse across the seam. ':interior' is
an in-span verse the warrant rests on that is neither, and for WARRANT-onset/close it is permitted ONLY when the
annotation names the device. The member "DERIVES the face from (verse, span) and FAILS LOUD on a mismatch, so
the qualifier is verified, not free text" - so this sweep refuses rather than guesses, and every refusal is
listed for the author batch.

WHY THE ZONE IS EXCLUDED BY NAME AND NOT BY ARITHMETIC. WEB and MT do not number Ezekiel alike: the offset map
records that the five verses WEB prints as 20:45-49 are MT 21:1-5, and MT 21:6-37 is WEB 21:1-32, with equal
totals at 1273 - "a shift, not a gap". The map's own tier-0 clause: "any structured ref touching WEB 20:45-49,
WEB ch 21, or MT ch 21 MUST carry an explicit dual or numeric qualifier". #e15 ruled the re-face mechanical only
"outside the zone ... (identity numbering)". So every ref or span touching the zone is ROUTED to the author
batch and nothing is computed for it. Crossing faces by arithmetic is the one thing this tool must never do.

THE COUNTS ARE READ FROM THEIR CARRIER and the face is asserted, because the carrier obliges it: verse_inventory
declares numbering_face WEB and says "Any tool that does verse arithmetic from these counts MUST assert the face
it expects rather than assume it". A chapter-opening verse's far side is the LAST verse of the previous chapter,
which cannot be known without those counts.
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
PREWAVE = EZ / "repair" / "rows_v7_cwo24.jsonl.pre_25cdba568d98"
INV = EZ / "verse_inventory.json"
OFF = EZ / "web_mt_offset_map.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

inv = json.loads(INV.read_text(encoding="utf-8"))
if inv.get("numbering_face") != "WEB":
    raise SystemExit("REFUSED: verse_inventory declares numbering_face %r; this sweep asserts WEB and will not "
                     "do verse arithmetic against another face." % inv.get("numbering_face"))
CH = {int(k): int(v) for k, v in inv["chapters"].items()}
off = json.loads(OFF.read_text(encoding="utf-8"))
if not off["rule"].get("identity_outside_the_zone"):
    raise SystemExit("REFUSED: the offset map no longer declares identity outside the zone")

# THE ZONE, taken from the map's own tier-0 clause rather than restated as numbers of mine
ZONE_WEB = {(20, v) for v in range(45, 50)} | {(21, v) for v in range(1, 33)}
ZONE_MT = {(21, v) for v in range(1, 38)}


def in_zone(face, c, v):
    return (c, v) in (ZONE_MT if face == "oshb" else ZONE_WEB)


VREF = re.compile(r"\b(oshb|web):Ezek\.(\d{1,2})\.(\d{1,3})\b")
SPANV = re.compile(r"Ezek\.(\d{1,2})\.(\d{1,3})")
TOK = re.compile(r"\[(WARRANT-onset|WARRANT-close)(:near|:far|:interior)?\]")
DEVICE = re.compile(r"samekh|petuchah|setumah|\bpe\b|parashah|messenger|utterance|recognition|refrain|"
                    r"word[- ]event|dateline|son of man|transport|paseq|ketiv|qere|K/Q|qinah|colophon|"
                    r"hand of|mouth|oath|sign|formula|mofet|\bmark\b", re.I)


def prev_verse(c, v):
    """The verse immediately before (c, v) in WEB numbering, crossing a chapter boundary by the carrier."""
    if v > 1:
        return (c, v - 1)
    if c - 1 in CH:
        return (c - 1, CH[c - 1])
    return None


def next_verse(c, v):
    if c in CH and v < CH[c]:
        return (c, v + 1)
    if c + 1 in CH:
        return (c + 1, 1)
    return None


def load(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


cur = {r["decision_id"]: r for r in load(ROWS)}
pre = {r["decision_id"]: r for r in load(PREWAVE)}

plan, routed, refused, tally = [], [], [], Counter()
for rid, r in cur.items():
    span = str(r.get("span", ""))
    vs = SPANV.findall(span)
    if not vs:
        continue
    first = (int(vs[0][0]), int(vs[0][1]))
    last = (int(vs[-1][0]), int(vs[-1][1]))
    prewave_entries = set(pre.get(rid, {}).get("boundary_evidence_refs") or [])
    span_touches_zone = any(in_zone("web", c, v) for c, v in
                            [(int(a), int(b)) for a, b in vs])
    for i, e in enumerate(r.get("boundary_evidence_refs") or []):
        m = TOK.search(e)
        if not m:
            continue
        token, qual = m.group(1), m.group(2)
        tally["%s_total" % token] += 1
        if qual:
            tally["already_qualified"] += 1
            continue
        if e in prewave_entries:
            # "Pre-wave descriptive entries are still not re-tokenised." Not mine to touch.
            tally["pre_wave_left_alone"] += 1
            continue
        vm = VREF.search(e)
        if not vm:
            refused.append({"row": rid, "index": i, "entry": e[:110], "token": token,
                            "why": "the entry carries no faced verse reference, so no face can be derived"})
            tally["refused"] += 1
            continue
        face, c, v = vm.group(1), int(vm.group(2)), int(vm.group(3))
        if in_zone(face, c, v) or span_touches_zone:
            routed.append({"row": rid, "index": i, "entry": e[:110], "token": token,
                           "why": ("the reference or the row's span touches the ch 20/21 zone, where WEB and MT "
                                   "do not number alike; the offset map requires an explicit dual or numeric "
                                   "qualifier there and #e15 makes the mechanical sweep valid only outside the "
                                   "zone. Routed to the author batch; nothing computed.")})
            tally["routed_to_author_zone"] += 1
            continue
        want, why = None, None
        if token == "WARRANT-onset":
            if (c, v) == first:
                want, why = ":near", "the reference is the row's first verse - the seam verse inside the unit"
            elif (c, v) == prev_verse(*first):
                want, why = ":far", "the reference is the verse immediately before the row's first verse"
            elif first < (c, v) <= last:
                if DEVICE.search(e):
                    want, why = ":interior", ("an in-span verse the warrant rests on, and the annotation names "
                                              "a device, which clause 6 v2 requires for an interior face")
                else:
                    refused.append({"row": rid, "index": i, "entry": e[:110], "token": token,
                                    "why": ("the reference is interior to the span and the annotation names no "
                                            "device; clause 6 v2 permits :interior on a warrant ONLY when the "
                                            "annotation names the device, so this needs an author")})
                    tally["refused"] += 1
                    continue
        else:
            if (c, v) == last:
                want, why = ":near", "the reference is the row's last verse - the seam verse inside the unit"
            elif (c, v) == next_verse(*last):
                want, why = ":far", "the reference is the verse immediately after the row's last verse"
            elif first <= (c, v) < last:
                if DEVICE.search(e):
                    want, why = ":interior", ("an in-span verse the warrant rests on, and the annotation names "
                                              "a device, which clause 6 v2 requires for an interior face")
                else:
                    refused.append({"row": rid, "index": i, "entry": e[:110], "token": token,
                                    "why": ("the reference is interior to the span and the annotation names no "
                                            "device; clause 6 v2 permits :interior on a warrant ONLY when the "
                                            "annotation names the device, so this needs an author")})
                    tally["refused"] += 1
                    continue
        if want is None:
            refused.append({"row": rid, "index": i, "entry": e[:110], "token": token,
                            "span": span, "verse": "%s:Ezek.%d.%d" % (face, c, v),
                            "why": ("the verse is neither the seam verse, nor the verse across the seam, nor "
                                    "in-span - so no face is derivable and the member must FAIL LOUD rather "
                                    "than choose one (#e15 Q5)")})
            tally["FAILED_LOUD_no_face_derivable"] += 1
            continue
        plan.append({"row": rid, "index": i, "token": token, "qualifier": want, "why": why,
                     "entry_before": e,
                     "entry_after": e.replace("[%s]" % token, "[%s%s]" % (token, want), 1)})
        tally["derived%s" % want] += 1

out = {
    "schema": "ezek_face_qualification_plan.v1",
    "order": ("#e15 Q5 clause 6 v2 retro_qualification - the mechanical arm of REPAIR-2 step 4. This is a DRY "
              "RUN: it derives and reports, and writes nothing to the corpus."),
    "what_is_mine_and_what_is_the_authors": (
        "mine: the face of a wave-installed WARRANT-onset or WARRANT-close token, derived from (verse, span). "
        "The authors': every WARRANT-rival qualifier and seam pair, everything inside the ch 20/21 zone, and "
        "every entry this sweep refuses. Pre-wave descriptive entries are not re-tokenised at all."),
    "inputs": {"rows": ROWS.name, "rows_sha256": sha(ROWS),
               "pre_wave_rows": PREWAVE.name, "pre_wave_sha256": sha(PREWAVE),
               "verse_inventory_sha256": sha(INV), "numbering_face_asserted": "WEB",
               "offset_map_sha256": sha(OFF)},
    "tally": dict(tally),
    "derivable_now": plan,
    "routed_to_the_author_batch_zone": routed,
    "refused_needs_an_author": refused,
    "tier": "MEASURED: the faces are derived from the rows' own spans and the carrier's verse counts; every "
            "undecidable case is listed rather than resolved",
}
p = HERE / "face_qualification_plan.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"tally": dict(tally), "derivable_now": len(plan), "routed_zone": len(routed),
                  "refused": len(refused), "plan_sha256": sha(p)}, indent=1))
for x in refused[:10]:
    print("  REFUSED %-9s %s" % (x["row"], x["why"][:96]))
for x in plan[:8]:
    print("  %-9s %-15s%-11s %s" % (x["row"], x["token"], x["qualifier"], x["entry_before"][:70]))
