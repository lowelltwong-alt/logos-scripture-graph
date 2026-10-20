#!/usr/bin/env python3
"""Deterministic validation of one 1 Corinthians writer part (W1..W6).

A DETERMINISTIC PASS IS NOT SEMANTIC VERIFICATION. This tool proves form, not judgment: whether each boundary is
well-formed, disclosed and byte-true, never whether it is right. It WRITES NOTHING; it prints one JSON object.
Ported 2026-10-19 in shape from Dan/writer_lanes/_validate_writer_part_dan.py; every 1 Corinthians fact is read from
1 Corinthians' own files (strategy_plan_1Cor.json, the staged witnesses, pmarks_1Cor.json through cor_lib). The zone,
K/Q and Hebrew arms of the Daniel tool are gone (1 Corinthians has no numbering zone, no language zone and no Hebrew
witness); the Greek arm and the strategy §10 conventions that a row check can test are new.

Checks (problems make the verdict RED; warnings are for the orchestrator's review and never turn it RED):
  SCHEMA     the 23 fields; unit_type in book_strategy_1Cor.md §6's closed 14; confidence in the closed 4;
             non_authorizing true; book "1Cor", model_id, review_status, writer_part and language "G" fixed;
             decision_id "<part>-NNN" and chunk_index_in_book ascending from 1, in span order
  TILING     the rows cover the part's WEB range exactly (strategy_plan_1Cor.json parts)
  SEAMS      no row straddles a parent start; parent_collection opens with the id of the parent that holds the row
  REFS       no oshb: or mt: token and no Hebrew character anywhere (§8.1; 0 Hebrew code points in the witnesses);
             a bare C:V that is not a 1 Corinthians verse is a WARNING (it may be another book's ref, e.g. Hos 13:14)
  GREEK      every Greek run of two or more Greek letters (cor_lib.GREEK_RUN) stands byte-exact in 1Cor_rp.txt or
             1Cor_sbl.txt; one that stands only once SBLGNT's critical signs are removed is a WARNING (disclose the
             sign); any other run is a problem (§8.2: never type Greek; E-01). A row carrying Greek carries both
             attribution lines (§8.14: "Robinson-Pierpont" with "Unlicense", "SBLGNT" with "CC BY 4.0")
  C2         a Greek run that is not byte-exact and shares 4 consecutive skeleton tokens with the RP or SBLGNT text of
             the row's verses or one verse either side is an unquoted witness run (§8.15) - a problem. NARROWER than
             §10 C2: every byte-exact run is exempt here, tagged or not; the strategy exempts only a tagged quotation
  C3         no row seam at 6:12/6:13, 6:13/6:14, 7:1/7:2, 8:1/8:2, 8:4/8:5, 8:8/8:9, 10:23/10:24; a row holding
             6:13, 7:1, 8:1, 8:4 or 8:8 carries the phrase "slogan extent contested"
  C4         each verse of TOPIC_MARKER_PAIRS (7:1, 7:25, 8:1, 12:1, 16:1, 16:12) opens a row
  C5         NARROWED PREDICATE: a Greek run byte-exact in the RP of a verse (in the row's span or one either side)
             listed in rp_sbl_differences, whose skeleton does not stand in that verse's SBLGNT skeleton, needs an
             sbl:1Cor token, the words "SBL reads" / "SBLGNT reads", or a byte-exact SBLGNT-only run of that verse
             in the same row (this predicate is the orchestrator's ASSUMED reading of §10 C5)
  C6         rows of P01 carry frame_prescript or frame_thanksgiving; rows of P13 carry frame_closing; no other row
             carries a frame type
  C7         no row seam at 11:26/11:27 or 15:7/15:8, and no row opens at 11:3 (§5 P08, D2)
  C8         the row holding 16:22 carries the RP form and the SBLGNT division, both sliced from the witnesses here
  C9         a row holding any of 14:33-14:36 carries "14:33b", "transposition" and "variant site"; the words
             "transpos..." never stand in boundary_rationale or boundary_evidence_refs (no seam rests on them)
  GRANULARITY  one-verse rows and rows above 15 verses are warnings (15 is an ASSUMED review prompt, not a rule)
  HINGES     neither or both of 1:17 and 1:18 opening a row is a warning (§7 I1); the rows holding 15:50 and 15:51
             not naming both verses is a warning (§8.12)
  E-65       the words Dan, Daniel, Ezek or Ezekiel in a row are a warning

usage: _validate_writer_part_1cor.py ROWS.jsonl --part W1..W6 [--attempt ATTEMPT_ID]
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
BK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BK / "tools"))
import cor_lib  # noqa: E402

FIELDS = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "boundary_rationale",
          "boundary_evidence_refs", "strongest_rejected_alternative", "literature_type_guess", "confidence",
          "strong_or_hebrew_tags_used", "wj_or_red_letter_considered", "frontier_flag_considered",
          "non_authorizing", "review_status", "parent_collection", "unit_type", "writer_part",
          "writer_decision_id", "writer_attempt_id", "observed_substrate_signals", "device_notes", "language"]
UNIT_TYPES = {"frame_prescript", "frame_thanksgiving", "frame_closing", "appeal", "report_response", "topic_response",
              "argument_step", "objection_reply", "example", "inset", "tradition_with_application",
              "slogan_with_response", "exhortation", "travel_and_commendation"}
FRAME_OPEN, FRAME_CLOSE = {"frame_prescript", "frame_thanksgiving"}, {"frame_closing"}
CONFIDENCE = {"high", "medium", "medium_low", "low"}
SPAN = re.compile(r"1Cor\.(\d+)\.(\d+)-1Cor\.(\d+)\.(\d+)$")
BARE_CV = re.compile(r"(?<![\w.:])(\d{1,2}):(\d{1,3})(?![\d])")
HEBREW = re.compile(r"[֐-׿יִ-ﭏ]")
FOREIGN_TOK = re.compile(r"\b(oshb|mt):")
E65 = re.compile(r"\b(Dan|Daniel|Ezek|Ezekiel)\b")
SLOGAN_NO_SEAM = [(6, 12), (6, 13), (7, 1), (8, 1), (8, 4), (8, 8), (10, 23)]      # seam after each (C3)
SLOGAN_DISCLOSE = [(6, 13), (7, 1), (8, 1), (8, 4), (8, 8)]
TOPIC = [(7, 1), (7, 25), (8, 1), (12, 1), (16, 1), (16, 12)]                    # C4
TRAD_NO_SEAM = [(11, 26), (15, 7)]                                              # seam after each (C7)
NOT_ONSET = [(11, 3)]                                                           # §5 P08 (D2)
BLOCK = [(14, 33), (14, 34), (14, 35), (14, 36)]                                # C9


def cv(s):
    c, v = s.split(":")
    return int(c), int(v)


def strings(x, path=""):
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, list):
        for i, y in enumerate(x):
            yield from strings(y, "%s[%d]" % (path, i))
    elif isinstance(x, dict):
        for k, y in x.items():
            yield from strings(y, "%s.%s" % (path, k) if path else k)


def greek_letters(s):
    return sum(1 for ch in s if cor_lib.is_letter(ch) and ("Ͱ" <= ch <= "Ͽ" or "ἀ" <= ch <= "῿"))


def grams(text, n=4):
    t = cor_lib.skeleton(text).split()
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--part", required=True, choices=["W1", "W2", "W3", "W4", "W5", "W6"])
    ap.add_argument("--attempt")
    a = ap.parse_args()

    plan = json.loads((BK / "strategy_plan_1Cor.json").read_text(encoding="utf-8"))
    part = next(p for p in plan["parts"] if p["id"] == a.part)
    parents = [(p["id"], cv(p["start"]), cv(p["end"])) for p in plan["parents"]]
    last = cor_lib.LAST_VERSE
    order = [(c, v) for c in sorted(last) for v in range(1, last[c] + 1)]
    pos = {x: i for i, x in enumerate(order)}
    wit = cor_lib.load_witnesses()
    rp, sbl = wit["rp"], wit["sbl"]
    rp_all, sbl_all = "\n".join(rp.values()), "\n".join(sbl.values())
    sbl_unsigned = re.sub("[" + cor_lib.SIGLA + "]", "", sbl_all)
    diff = {tuple(int(n) for n in r.split(".")[1:]) for r in cor_lib.load_pmarks()["rp_sbl_differences"]}
    rp_1622 = " ".join(rp[(16, 22)].split()[-2:]).rstrip(".")
    sbl_1622 = re.search("⸂[^⸃]*⸃", sbl[(16, 22)]).group(0)
    if not rp_1622.startswith("Μαρ") or not sbl_1622.startswith("⸂Μαρ"):
        raise SystemExit("ERROR: the 16:22 slices did not resolve on the witness bytes")

    rows = [json.loads(x) for x in Path(a.rows).read_text(encoding="utf-8").splitlines() if x.strip()]
    problems, warnings = [], []
    want = order[pos[cv(part["start"])]:pos[cv(part["end"])] + 1]
    wset = set(want)
    seen, spans, starts, holder = {}, [], set(), {}
    for n, r in enumerate(rows, 1):
        did = r.get("decision_id")
        missing = [f for f in FIELDS if f not in r]
        extra = [f for f in r if f not in FIELDS]
        if missing:
            problems.append("%s: missing fields %s" % (did, missing))
        if extra:
            problems.append("%s: fields outside the 23 %s" % (did, extra))
        fixed = {"book": "1Cor", "model_id": "M8_fable", "review_status": "pending", "writer_part": a.part,
                 "non_authorizing": True, "decision_id": "%s-%03d" % (a.part, n), "chunk_index_in_book": n,
                 "language": "G"}
        if a.attempt:
            fixed["writer_attempt_id"] = a.attempt
        for k, v in fixed.items():
            if r.get(k) != v:
                problems.append("%s: %s is %r, expected %r" % (did, k, r.get(k), v))
        if r.get("unit_type") not in UNIT_TYPES:
            problems.append("%s: unit_type %r is not in the closed 14" % (did, r.get("unit_type")))
        if r.get("confidence") not in CONFIDENCE:
            problems.append("%s: confidence %r is not in the closed 4" % (did, r.get("confidence")))
        m = SPAN.match(r.get("span") or "")
        vs = []
        if not m:
            problems.append("%s: unparseable span %r" % (did, r.get("span")))
        else:
            s, e = (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))
            if s not in pos or e not in pos or pos[s] > pos[e]:
                problems.append("%s: span %r is not a WEB range" % (did, r["span"]))
            else:
                vs = order[pos[s]:pos[e] + 1]
                spans.append((pos[s], did))
                starts.add(s)
        for x in vs:
            if x in seen:
                problems.append("overlap at %d:%d (%s and %s)" % (x + (seen[x], did)))
            seen[x] = did
            holder[x] = r
        blob = json.dumps(r, ensure_ascii=False)
        if vs:
            home = [pid for pid, ps, pe in parents if pos[ps] <= pos[vs[0]] <= pos[pe]][0]
            for pid, ps, _ in parents:
                if ps != vs[0] and ps in vs:
                    problems.append("%s: straddles the parent seam before %s (%d:%d)" % (did, pid, *ps))
            pc = str(r.get("parent_collection") or "")
            if re.match(r"P\d\d\b", pc) is None or pc[:3] != home:
                problems.append("%s: parent_collection %r does not open with %s" % (did, pc[:30], home))
            ut = r.get("unit_type")
            if home == "P01" and ut not in FRAME_OPEN:
                problems.append("%s: a P01 row carries %r, not frame_prescript or frame_thanksgiving (C6)" % (did, ut))
            elif home == "P13" and ut not in FRAME_CLOSE:
                problems.append("%s: a P13 row carries %r, not frame_closing (C6)" % (did, ut))
            elif home not in ("P01", "P13") and ut in FRAME_OPEN | FRAME_CLOSE:
                problems.append("%s: frame type %r outside P01/P13 (C6)" % (did, ut))
            for x in SLOGAN_DISCLOSE:
                if x in vs and "slogan extent contested" not in blob.lower():
                    problems.append("%s: holds %d:%d without \"slogan extent contested\" (C3)" % (did, *x))
            if any(x in vs for x in BLOCK):
                low = blob.lower()
                for ph in ("14:33b", "transposition", "variant site"):
                    if ph not in low:
                        problems.append("%s: holds part of 14:33-14:36 without %r (C9)" % (did, ph))
                seam_text = json.dumps([r.get("boundary_rationale"), r.get("boundary_evidence_refs")],
                                       ensure_ascii=False).lower()
                if "transpos" in seam_text:
                    problems.append("%s: the transposition stands in boundary_rationale or boundary_evidence_refs; "
                                    "disclose it in device_notes only (C9)" % did)
            if (16, 22) in vs and not (rp_1622 in blob and sbl_1622 in blob):
                problems.append("%s: holds 16:22 without both the RP form and the SBLGNT division (C8)" % did)
            if len(vs) == 1:
                warnings.append("%s: one-verse row; needs a justified disclosure (§6)" % did)
            if len(vs) > 15:
                warnings.append("%s: %d verses; confirm it is one complete argumentative move (§6)" % (did, len(vs)))
            ctx = [order[i] for i in range(max(0, pos[vs[0]] - 1), min(len(order), pos[vs[-1]] + 2))]
            ctx_grams = set()
            for x in ctx:
                ctx_grams |= grams(rp[x]) | grams(sbl[x])
        else:
            ctx = []
            ctx_grams = set()
        has_greek = False
        row_runs = [q for _, s in strings(r) for q in (x.strip(" ,.·;·’ʼ")
                                                       for x in cor_lib.GREEK_RUN.findall(s)) if greek_letters(q) >= 2]
        for path, s in strings(r):
            if path == "span":
                continue
            if HEBREW.search(s):
                problems.append("%s %s: Hebrew character in a 1 Corinthians row" % (did, path))
            if FOREIGN_TOK.search(s):
                problems.append("%s %s: oshb: or mt: token (§8.1)" % (did, path))
            if E65.search(s):
                warnings.append("%s %s: names %s (E-65)" % (did, path, E65.search(s).group(0)))
            for t in BARE_CV.finditer(s):
                x = (int(t.group(1)), int(t.group(2)))
                if x not in pos:
                    warnings.append("%s %s: bare C:V %s is not a 1 Corinthians verse (another book's ref?)" %
                                    (did, path, t.group(0)))
            for run in cor_lib.GREEK_RUN.findall(s):
                run = run.strip(" ,.·;·’ʼ")
                if greek_letters(run) < 2:
                    continue
                has_greek = True
                if run in rp_all or run in sbl_all:
                    for x in ctx:
                        if x in diff and run in rp[x] and cor_lib.skeleton(run) not in cor_lib.skeleton(sbl[x]) and \
                                not re.search(r"sbl:1Cor\.|SBL(GNT)? reads", blob) and \
                                not any(q in sbl[x] and q not in rp[x] for q in row_runs):
                            problems.append("%s %s: RP run at %d:%d differs in SBLGNT and the row has no sbl: token "
                                            "or \"SBL reads\" note (C5): %r" % (did, path, *x, run[:30]))
                            break
                    continue
                if run in sbl_unsigned:
                    warnings.append("%s %s: Greek run stands in SBLGNT only without its critical signs; disclose "
                                    "the sign: %r" % (did, path, run[:30]))
                    continue
                if grams(run) & ctx_grams:
                    problems.append("%s %s: unquoted witness run of 4+ tokens, not byte-sliced (C2): %r" %
                                    (did, path, run[:30]))
                else:
                    problems.append("%s %s: Greek run in neither witness byte-exact (never type Greek; E-01): %r" %
                                    (did, path, run[:30]))
        if has_greek and not all(k in blob for k in ("Robinson-Pierpont", "Unlicense", "SBLGNT", "CC BY 4.0")):
            problems.append("%s: carries Greek without both attribution lines (§8.14)" % did)

    if [p for p, _ in spans] != sorted(p for p, _ in spans):
        problems.append("rows are not in span order")
    seams = {order[pos[x] - 1] for x in starts if pos[x] > 0}
    for x in SLOGAN_NO_SEAM + TRAD_NO_SEAM:
        if x in seams and x in wset:
            problems.append("row seam after %d:%d, which the strategy forbids (C3/C7)" % x)
    for x in NOT_ONSET:
        if x in starts:
            problems.append("a row opens at %d:%d, which §5 says is not an onset (C7, D2)" % x)
    for x in TOPIC:
        if x in wset and x not in starts:
            problems.append("%d:%d is a topic-marker verse and opens no row (C4)" % x)
    if (1, 17) in wset and ((1, 17) in starts) == ((1, 18) in starts):
        warnings.append("1:17 and 1:18: open exactly one of them as the hinge row (§7 I1)")
    if (15, 50) in wset:
        hold = [holder.get(x) for x in ((15, 50), (15, 51)) if holder.get(x)]
        if not any("15:50" in json.dumps(h, ensure_ascii=False) and "15:51" in json.dumps(h, ensure_ascii=False)
                   for h in hold):
            warnings.append("no row holding 15:50 or 15:51 names both verses; the rival reading is to be disclosed "
                            "(§8.12)")
    miss = [x for x in want if x not in seen]
    over = [x for x in seen if x not in wset]
    if miss:
        problems.append("TILING GAP: %d verses uncovered, first %s" % (len(miss), miss[:5]))
    if over:
        problems.append("TILING OVERRUN: %d verses outside the part, first %s" % (len(over), over[:5]))
    print(json.dumps({
        "part": a.part, "rows_file": str(a.rows), "rows": len(rows), "assigned_verses": len(want),
        "covered_verses": len(seen), "tiling": "EXACT" if not miss and not over else "BROKEN",
        "confidence_spread": {k: sum(1 for r in rows if r.get("confidence") == k) for k in sorted(CONFIDENCE)},
        "unit_types_used": sorted({str(r.get("unit_type")) for r in rows}),
        "problems": problems, "warnings": warnings, "verdict": "GREEN" if not problems else "RED",
        "limit": "a deterministic pass is NOT semantic verification; it proves form, not judgment",
    }, ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
