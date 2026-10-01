#!/usr/bin/env python3
"""ROLE-TOKEN member (STAGED for REPAIR-2 step 4): verifies DEF-A4-ARGUED clause 6 v2 on every tokened refs entry.

THE RULE, from #e15 Q5 clause 6 v2, quoted:
  "WARRANT-onset, WARRANT-close and WARRANT-rival carry a face qualifier: ':near' (the seam verse inside the unit
   the seam bounds - the row's first verse for its onset, its last verse for its close, the candidate onset verse for
   a rival), ':far' (the adjacent verse across the seam), ':interior' (an in-span verse the warrant rests on that is
   neither ... permitted for WARRANT-close and WARRANT-onset only when the annotation names the device) ... For
   WARRANT-onset and WARRANT-close the member DERIVES the face from (verse, span) and FAILS LOUD on a mismatch, so the
   qualifier is verified, not free text. For WARRANT-rival the seam is not in the schema, so the annotation's first
   token names the seam pair ... and the member checks the ref's verse is one side of the pair and the qualifier
   matches that side."
  "WARRANT-absence ... and DISCLOSURE-absence ... WARRANT-absence-over-range is retained as a deprecated alias the
   member accepts and maps to WARRANT-absence."

WHY A SEPARATE MEMBER. The mirroring member is pinned by running work and judges MIRRORING, never weight; this member
judges the TOKEN. Keeping them apart means installing this one cannot change a single refs_mirror verdict.

MODES. --phase pre (today): a qualifier that IS present must verify; an unqualified warrant is counted, not flagged,
because step 4's sweep installs the qualifiers. --phase post (after step 4): an unqualified WARRANT-onset/close/rival
is itself a flag. The ch 20/21 zone is never computed: an entry touching it is verified on its web: face only when it
is written dual, and its MT face is not re-derived by arithmetic.

usage: python check_role_tokens.py <rows.jsonl> [--phase pre|post]
       python check_role_tokens.py --selftest
"""
import json
import re
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
sys.path.insert(0, str(EZ / "tools"))

VOCAB = {"WARRANT-onset", "WARRANT-close", "WARRANT-rival", "WARRANT-absence", "DISCLOSURE-absence",
         "DISCLOSURE-kq", "DISCLOSURE-mark", "DISCLOSURE-paseq", "DISCLOSURE-note", "DISCLOSURE-device", "QUOTE",
         "ANCHOR"}
ALIASES = {"WARRANT-absence-over-range": "WARRANT-absence"}
QUALIFIED = {"WARRANT-onset", "WARRANT-close", "WARRANT-rival"}
DEVICE_WORD = re.compile(r"samekh|petuchah|setumah|\bpe\b|messenger|utterance|recognition|refrain|word[- ]event|"
                         r"dateline|son of man|transport|paseq|ketiv|qere|K/Q|qinah|colophon|hand|oath|formula|mark",
                         re.I)
REF = r"(oshb|web):Ezek\.(\d{1,2})\.(\d{1,3})(?:-Ezek\.(\d{1,2})\.(\d{1,3}))?"
ENTRY = re.compile(r"^" + REF + r"(?: = " + REF + r")? \[([A-Za-z-]+)(?::([a-z]+))?\]\s*(.*)$")
SPANV = re.compile(r"Ezek\.(\d{1,2})\.(\d{1,3})")
SEAM = re.compile(r"^(\d{1,2})\.(\d{1,3})/(\d{1,2})\.(\d{1,3})\b")
ZONE_WEB = {(20, v) for v in range(45, 50)} | {(21, v) for v in range(1, 33)}


def chapters():
    inv = json.loads((EZ / "verse_inventory.json").read_text(encoding="utf-8"))
    if inv.get("numbering_face") != "WEB":
        raise SystemExit("REFUSED: verse_inventory numbering face is not WEB")
    return {int(k): int(v) for k, v in inv["chapters"].items()}


CH = None


def prev_v(c, v):
    return (c, v - 1) if v > 1 else ((c - 1, CH[c - 1]) if c - 1 in CH else None)


def next_v(c, v):
    return (c, v + 1) if v < CH[c] else ((c + 1, 1) if c + 1 in CH else None)


def check_rows(rows, phase):
    global CH
    CH = CH or chapters()
    flags, counts = [], {"tokened_entries": 0, "qualified": 0, "unqualified_warrants": 0, "rivals": 0,
                         "zone_entries_not_derived": 0, "entries_read": 0}
    for r in rows:
        rid = r.get("decision_id")
        vs = SPANV.findall(str(r.get("span", "")))
        if not vs:
            continue
        first, last = (int(vs[0][0]), int(vs[0][1])), (int(vs[-1][0]), int(vs[-1][1]))
        for e in r.get("boundary_evidence_refs") or []:
            counts["entries_read"] += 1
            m = ENTRY.match(e)
            if not m:
                continue                                  # pre-wave descriptive entries carry no token
            g = m.groups()
            token, qual, note = ALIASES.get(g[10], g[10]), g[11], g[12]
            counts["tokened_entries"] += 1
            f = lambda why: flags.append({"row": rid, "entry": e, "problem": why})          # noqa: E731
            if token not in VOCAB:
                f("token [%s] is not in the clause 6 v2 vocabulary" % g[10])
                continue
            if qual and token not in QUALIFIED:
                f("a face qualifier is defined only for WARRANT-onset, WARRANT-close and WARRANT-rival")
                continue
            if token in QUALIFIED and not qual:
                counts["unqualified_warrants"] += 1
                if phase == "post":
                    f("an unqualified %s after step 4 - clause 6 v2 requires :near, :far or :interior" % token)
                continue
            if qual:
                counts["qualified"] += 1
                if qual not in ("near", "far", "interior", "merge"):
                    f("qualifier :%s is not :near, :far, :interior or :merge" % qual)
                    continue
                if qual == "merge" and token != "WARRANT-rival":
                    f(":merge is defined only for WARRANT-rival (#e16 C1)")
                    continue
            face = g[0]
            cv = (int(g[1]), int(g[2]))
            if face == "oshb" or cv in ZONE_WEB or (cv[0] in (20, 21) and g[5] is None and cv[0] == 21):
                if cv in ZONE_WEB or cv[0] == 21:
                    counts["zone_entries_not_derived"] += 1
                    continue
            if token in ("WARRANT-onset", "WARRANT-close"):
                if token == "WARRANT-onset":
                    derived = "near" if cv == first else ("far" if cv == prev_v(*first) else
                                                          ("interior" if first < cv <= last else None))
                else:
                    derived = "near" if cv == last else ("far" if cv == next_v(*last) else
                                                         ("interior" if first <= cv < last else None))
                if derived is None:
                    f("the verse is neither the seam verse, the verse across the seam, nor in span - no face derives")
                elif derived != qual:
                    f("qualifier :%s but the verse against the span derives :%s" % (qual, derived))
                elif qual == "interior" and not DEVICE_WORD.search(note):
                    f(":interior is permitted only when the annotation names the device")
            elif token == "WARRANT-rival":
                counts["rivals"] += 1
                sm = SEAM.match(note.strip())
                if not sm:
                    f("a WARRANT-rival annotation's first token names the seam pair, e.g. '33.11/33.12'")
                    continue
                a, b = (int(sm.group(1)), int(sm.group(2))), (int(sm.group(3)), int(sm.group(4)))
                # #e16 C1/C2: a MERGE rival contests the row's OWN seam - the pair is that seam, the reference is the
                # absorbed material, and no near/far polarity applies
                own_onset, own_close = (prev_v(*first), first), (last, next_v(*last))
                is_own = (a, b) in (own_onset, own_close)
                ref_end = (int(g[3]), int(g[4])) if g[3] else cv
                if next_v(*a) != b:
                    f("the seam pair %s/%s is not two adjacent verses" % (a, b))
                elif qual == "merge":
                    counts["merge_rivals"] = counts.get("merge_rivals", 0) + 1
                    if not is_own:
                        f("a :merge rival's pair must be the row's own onset or close seam (#e16 C1)")
                    elif (a, b) == own_close and cv != b:
                        f("a close-seam :merge reference must begin on the verse after the row's last verse (#e16 C1)")
                    elif (a, b) == own_onset and ref_end != a:
                        f("an onset-seam :merge reference must end on the verse before the row's first verse (#e16 C1)")
                elif is_own:
                    f("the pair %s/%s is the row's own seam - a merge rival is written :merge (#e16 C2)" % (a, b))
                elif cv not in (a, b):
                    f("the ref's verse is not one side of the seam pair it names")
                elif (cv == b and qual != "near") or (cv == a and qual != "far"):
                    f("the rival's candidate onset verse is :near and the verse behind it :far - this entry has :%s"
                      % qual)
    return flags, counts


def selftest():
    global CH
    CH = chapters()
    row = {"decision_id": "T", "span": "Ezek.33.10-Ezek.33.20", "boundary_evidence_refs": [
        "oshb:Ezek.33.10 [WARRANT-onset:near] the ve'attah re-address opens",
        "oshb:Ezek.33.9 [WARRANT-onset:far] samekh behind the onset",
        "oshb:Ezek.33.20 [WARRANT-close:near] verdict clause closes",
        "web:Ezek.33.21 [WARRANT-close:far] dateline opens the next",
        "oshb:Ezek.33.12 [WARRANT-rival:near] 33.11/33.12 ve'attah same audience",
        "oshb:Ezek.33.11 [WARRANT-rival:far] 33.11/33.12 pe behind the rival",
        "oshb:Ezek.33.13 [WARRANT-absence] no formula inside 33:13",
        "oshb:Ezek.33.14 [WARRANT-absence-over-range] alias accepted",
        "this row's pre-wave descriptive entry carries no token"]}
    bad = dict(row, boundary_evidence_refs=[
        "oshb:Ezek.33.10 [WARRANT-onset:far] mislabelled onset",
        "oshb:Ezek.33.15 [WARRANT-close:interior] no device named",
        "oshb:Ezek.33.12 [WARRANT-rival:near] ve'attah without a seam pair",
        "oshb:Ezek.33.12 [WARRANT-rival:far] 33.11/33.12 wrong side",
        "oshb:Ezek.33.13 [DISCLOSURE-mark:near] qualifier on a disclosure",
        "oshb:Ezek.33.13 [WARRANT-maybe] unknown token"])
    unq = dict(row, boundary_evidence_refs=["oshb:Ezek.33.10 [WARRANT-onset] onset"])
    ch_open = {"decision_id": "C", "span": "Ezek.18.1-Ezek.18.4",
               "boundary_evidence_refs": ["oshb:Ezek.17.24 [WARRANT-onset:far] refrain behind the chapter"]}
    # #e16 tool-order fixtures for the :merge arm (rows shaped as P03-011, P01-006, P03-012)
    fwd = {"decision_id": "P03-011", "span": "Ezek.17.11-Ezek.17.18",
           "boundary_evidence_refs": ["web:Ezek.17.19-Ezek.17.21 [WARRANT-rival:merge] 17.18/17.19 forward merge weighed here"]}
    fwd_near = dict(fwd, boundary_evidence_refs=["web:Ezek.17.19-Ezek.17.21 [WARRANT-rival:near] 17.18/17.19 forward merge weighed here"])
    back = {"decision_id": "P01-006", "span": "Ezek.3.16-Ezek.3.21",
            "boundary_evidence_refs": ["oshb:Ezek.3.12-Ezek.3.15 [WARRANT-rival:merge] 3.15/3.16 backward extension weighed, declined"]}
    back_short = dict(back, boundary_evidence_refs=["oshb:Ezek.3.12-Ezek.3.14 [WARRANT-rival:merge] 3.15/3.16 backward extension"])
    not_own = {"decision_id": "P03-012", "span": "Ezek.17.19-Ezek.17.21",
               "boundary_evidence_refs": ["oshb:Ezek.17.11-Ezek.17.18 [WARRANT-rival:merge] 17.10/17.11 merge"]}
    merge_on_close = dict(row, boundary_evidence_refs=["oshb:Ezek.33.20 [WARRANT-close:merge] not a rival"])
    merge_cases = [("#e16: a forward :merge on the row's own close seam PASSES", not check_rows([fwd], "post")[0]),
                   ("#e16: the same entry with :near FAILS (own seam)", len(check_rows([fwd_near], "post")[0]) == 1),
                   ("#e16: a backward :merge on the row's own onset seam PASSES", not check_rows([back], "post")[0]),
                   ("#e16: a backward :merge whose reference stops short FAILS", len(check_rows([back_short], "post")[0]) == 1),
                   ("#e16: a :merge whose pair is not an own seam FAILS", len(check_rows([not_own], "post")[0]) == 1),
                   ("#e16: :merge on a non-rival token FAILS", len(check_rows([merge_on_close], "post")[0]) == 1)]
    g_flags, g_counts = check_rows([row], "pre")
    b_flags, _ = check_rows([bad], "pre")
    u_pre, _ = check_rows([unq], "pre")
    u_post, _ = check_rows([unq], "post")
    c_flags, _ = check_rows([ch_open], "pre")
    cases = [("a correct row raises no flag", not g_flags and g_counts["qualified"] == 6),
             ("every one of six planted defects is flagged", len(b_flags) == 6),
             ("an unqualified warrant is counted, not flagged, before step 4", not u_pre),
             ("an unqualified warrant IS flagged after step 4", len(u_post) == 1),
             ("the far face of a chapter-opening onset is the previous chapter's last verse", not c_flags),
             ("the denominator is nonzero", g_counts["entries_read"] == 9)] + merge_cases
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed,
                      "planted_defects_flagged": [x["problem"][:70] for x in b_flags]}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    # THE PHASE IS PINNED IN A FILE BESIDE THE MEMBER, not read from the environment: a suite run that forgot an
    # environment variable would silently judge leniently. An absent or unreadable phase file means STRICT (post).
    if "--phase" in sys.argv:
        phase = sys.argv[sys.argv.index("--phase") + 1]
    else:
        try:
            phase = json.loads((Path(__file__).resolve().parent / "role_tokens_phase.json")
                               .read_text(encoding="utf-8")).get("phase", "post")
        except Exception:
            phase = "post"
    if phase not in ("pre", "post"):
        raise SystemExit("REFUSED: phase must be pre or post, got %r" % phase)
    rows = [json.loads(l) for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if l.strip()]
    flags, counts = check_rows(rows, phase)
    if counts["entries_read"] == 0:
        raise SystemExit("REFUSED: zero refs entries read (E-36)")
    print(json.dumps({"member": "role_tokens", "phase": phase, "counts": counts, "flag_count": len(flags),
                      "flags": flags, "status": "GREEN" if not flags else "FLAGS"}, ensure_ascii=False, indent=1))
    return 0 if not flags else 1


if __name__ == "__main__":
    raise SystemExit(main())
