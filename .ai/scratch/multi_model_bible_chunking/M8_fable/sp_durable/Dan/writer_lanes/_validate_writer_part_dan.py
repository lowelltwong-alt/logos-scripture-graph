#!/usr/bin/env python3
"""Deterministic validation of one Daniel writer part (W1..W6).

A DETERMINISTIC PASS IS NOT SEMANTIC VERIFICATION. This tool proves form, not judgment: whether each boundary is
well-formed, disclosed and byte-true, never whether it is right. It WRITES NOTHING; it prints one JSON object.
Ported in shape from Ezekiel's writer-part validator; every Daniel fact is read from Daniel's own files.

Checks (problems make the verdict RED; warnings are for the orchestrator's review and never turn it RED):
  SCHEMA     the 23 fields (Ezekiel's 22 plus `language`); unit_type in book_strategy_Dan.md §6's closed 8;
             confidence in the closed 4; non_authorizing true; book, model_id, review_status and writer_part fixed;
             decision_id "<part>-NNN" and chunk_index_in_book ascending from 1, in span order
  TILING     the rows cover the part's WEB range exactly (strategy_plan_Dan.json parts), counted over
             verse_inventory.json
  SEAMS      no row straddles a parent start (strategy_plan_Dan.json parents); parent_collection opens with the
             id of the parent that holds the row
  LANGUAGE   the `language` field equals the row's languages from dan_language_zones.json (through dan_lib):
             H or A when one language, mixed otherwise; a row covering 2:4 names 2:4
  ZONES      every mention of a zone verse is a web:Dan./oshb:Dan. pair and the pair's arithmetic holds
             (dan_lib.web_to_mt); a bare C:V or bare Dan.C.V on a zone verse, or a bare C:V that is not a WEB
             verse, is a problem; a mention qualified only by "MT " or "WEB " is a warning
  HEBREW     every Hebrew or Aramaic run (dan_lib.HEB_RUN) is in Dan_oshb.txt, or a Qere of the pmarks K/Q layer
             with its "/" separators removed; a match by consonantal skeleton only (dan_lib.skeleton) is a warning
  GRANULARITY  one-verse rows that are not summary_notice, and rows above 9 verses, are warnings (§6)
  K/Q        a covered K/Q verse that the row never names is a warning
  E-65       the string "Ezek" anywhere in a row is a warning

usage: _validate_writer_part_dan.py ROWS.jsonl --part W1..W6 [--attempt ATTEMPT_ID]
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
import dan_lib  # noqa: E402

FIELDS = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "boundary_rationale",
          "boundary_evidence_refs", "strongest_rejected_alternative", "literature_type_guess", "confidence",
          "strong_or_hebrew_tags_used", "wj_or_red_letter_considered", "frontier_flag_considered",
          "non_authorizing", "review_status", "parent_collection", "unit_type", "writer_part",
          "writer_decision_id", "writer_attempt_id", "observed_substrate_signals", "device_notes", "language"]
UNIT_TYPES = {"narrative", "dialogue", "royal_proclamation", "doxology_or_prayer", "dream_or_vision_report",
              "interpretation", "heavenly_discourse", "summary_notice"}
CONFIDENCE = {"high", "medium", "medium_low", "low"}
LANG = {"Hebrew": "H", "Aramaic": "A", "mixed": "mixed"}
SPAN = re.compile(r"Dan\.(\d+)\.(\d+)-Dan\.(\d+)\.(\d+)$")
TOK = r"`?(web|oshb):Dan\.(\d+)\.(\d+)`?"
RNG = TOK + r"(?:\s*[-–]\s*" + TOK + r")?"
PAIR = re.compile(RNG + r"\s*=\s*" + RNG)
ANY_TOK = re.compile(r"(web|oshb):Dan\.(\d+)\.(\d+)")
BARE_DAN = re.compile(r"(?<![:\w])Dan\.(\d+)\.(\d+)")
BARE_CV = re.compile(r"(?<![\w.:])(\d{1,2}):(\d{1,3})(?!\d)")


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--part", required=True, choices=["W1", "W2", "W3", "W4", "W5", "W6"])
    ap.add_argument("--attempt")
    a = ap.parse_args()

    plan = json.loads((BK / "strategy_plan_Dan.json").read_text(encoding="utf-8"))
    part = next(p for p in plan["parts"] if p["id"] == a.part)
    parents = [(p["id"], cv(p["start"]), cv(p["end"])) for p in plan["parents"]]
    last = dan_lib.LAST_VERSE
    order = [(c, v) for c in sorted(last) for v in range(1, last[c] + 1)]
    pos = {x: i for i, x in enumerate(order)}
    oshb = dict(l.split("\t", 1) for l in (BK / "Dan_oshb.txt").read_text(encoding="utf-8").splitlines() if l)
    raw_all = "\n".join(oshb.values())
    sk_all = dan_lib.skeleton(raw_all)
    pm = json.loads((BK / "pmarks_Dan.json").read_text(encoding="utf-8"))
    kq_raw = " ".join(s for _, s in strings(pm["kq"])).replace("/", "")
    kq_sk = dan_lib.skeleton(kq_raw)
    web_zone = {w for w in order if dan_lib.web_to_mt(*w) != w}
    mt_zone = {m for m in (dan_lib.web_to_mt(*w) for w in web_zone)}

    rows = [json.loads(l) for l in Path(a.rows).read_text(encoding="utf-8").splitlines() if l.strip()]
    problems, warnings = [], []
    want = order[pos[cv(part["start"])]:pos[cv(part["end"])] + 1]
    seen, spans = {}, []
    for n, r in enumerate(rows, 1):
        did = r.get("decision_id")
        missing = [f for f in FIELDS if f not in r]
        extra = [f for f in r if f not in FIELDS]
        if missing:
            problems.append("%s: missing fields %s" % (did, missing))
        if extra:
            problems.append("%s: fields outside the 23 %s" % (did, extra))
        fixed = {"book": "Dan", "model_id": "M8_fable", "review_status": "pending", "writer_part": a.part,
                 "non_authorizing": True, "decision_id": "%s-%03d" % (a.part, n), "chunk_index_in_book": n}
        if a.attempt:
            fixed["writer_attempt_id"] = a.attempt
        for k, v in fixed.items():
            if r.get(k) != v:
                problems.append("%s: %s is %r, expected %r" % (did, k, r.get(k), v))
        if r.get("unit_type") not in UNIT_TYPES:
            problems.append("%s: unit_type %r is not in the closed 8" % (did, r.get("unit_type")))
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
        for x in vs:
            if x in seen:
                problems.append("overlap at %d:%d (%s and %s)" % (x + (seen[x], did)))
            seen[x] = did
        blob = json.dumps(r, ensure_ascii=False)
        if vs:
            home = [pid for pid, ps, pe in parents if pos[ps] <= pos[vs[0]] <= pos[pe]][0]
            for pid, ps, _ in parents:
                if ps != vs[0] and ps in vs:
                    problems.append("%s: straddles the parent seam before %s (%d:%d)" % (did, pid, *ps))
            pc = str(r.get("parent_collection") or "")
            if re.match(r"[A-Z]+", pc) is None or re.match(r"[A-Z]+", pc).group(0) != home:
                problems.append("%s: parent_collection %r does not open with %s" % (did, pc[:30], home))
            langs = {LANG[dan_lib.language_of(*dan_lib.web_to_mt(*x))] for x in vs}
            exp = langs.pop() if len(langs) == 1 else "mixed"
            if r.get("language") != exp:
                problems.append("%s: language %r, the zones file gives %r" % (did, r.get("language"), exp))
            if (2, 4) in vs and "2:4" not in blob:
                problems.append("%s: covers 2:4 without naming it" % did)
            if len(vs) == 1 and r.get("unit_type") != "summary_notice":
                warnings.append("%s: one-verse row that is not summary_notice; needs a justified disclosure" % did)
            if len(vs) > 9:
                warnings.append("%s: %d verses, above 9; needs the single-speech-act statement (§6)" % (did, len(vs)))
            for x in vs:
                mt = "Dan.%d.%d" % dan_lib.web_to_mt(*x)
                if mt in pm["kq"] and mt not in blob and "%d:%d" % x not in blob and \
                        "%d:%d" % dan_lib.web_to_mt(*x) not in blob:
                    warnings.append("%s: covers K/Q verse %s (MT) without naming it" % (did, mt))
        if "Ezek" in blob:
            warnings.append("%s: names Ezek (E-65: no Ezekiel figure passes as Daniel's)" % did)

        for path, s in strings(r):
            if path == "span":
                continue
            covered = []
            for pm_ in PAIR.finditer(s):
                g = pm_.groups()
                left = [(g[0], int(g[1]), int(g[2]))] + ([(g[3], int(g[4]), int(g[5]))] if g[3] else [])
                right = [(g[6], int(g[7]), int(g[8]))] + ([(g[9], int(g[10]), int(g[11]))] if g[9] else [])
                faces = {f for f, _, _ in left} | {f for f, _, _ in right}
                if len(left) != len(right) or {f for f, _, _ in left} == {f for f, _, _ in right} or \
                        len({f for f, _, _ in left}) != 1 or faces != {"web", "oshb"}:
                    problems.append("%s %s: malformed pair %r" % (did, path, pm_.group(0)[:60]))
                    continue
                for (f1, c1, v1), (_, c2, v2) in zip(left, right):
                    w, o = ((c1, v1), (c2, v2)) if f1 == "web" else ((c2, v2), (c1, v1))
                    if dan_lib.web_to_mt(*w) != o:
                        problems.append("%s %s: wrong dual web %d:%d = oshb %d:%d" % (did, path, *w, *o))
                covered.append(pm_.span())
            inside = lambda i: any(p <= i < q for p, q in covered)  # noqa: E731
            for t in ANY_TOK.finditer(s):
                f, c, v = t.group(1), int(t.group(2)), int(t.group(3))
                if not inside(t.start()) and (((c, v) in web_zone) if f == "web" else ((c, v) in mt_zone)):
                    problems.append("%s %s: zone ref %s without its dual" % (did, path, t.group(0)))
            for t in BARE_DAN.finditer(s):
                if (int(t.group(1)), int(t.group(2))) in web_zone | mt_zone and not inside(t.start()):
                    problems.append("%s %s: bare zone token %s" % (did, path, t.group(0)))
            for t in BARE_CV.finditer(s):
                x = (int(t.group(1)), int(t.group(2)))
                pre = s[max(0, t.start() - 4):t.start()]
                if pre.endswith(("MT ", "WEB ")):
                    if x in web_zone or x in mt_zone:
                        warnings.append("%s %s: zone verse qualified only as %r" % (did, path, pre.strip() + " " +
                                                                                   t.group(0)))
                    continue
                if x in web_zone:
                    problems.append("%s %s: bare C:V %s on a zone verse; write the web:/oshb: pair" %
                                    (did, path, t.group(0)))
                elif x not in pos and x[0] <= 12 and x[1] >= 1:
                    problems.append("%s %s: bare C:V %s is not a WEB verse" % (did, path, t.group(0)))
            for run in dan_lib.HEB_RUN.findall(s):
                run = run.strip()
                if len(run) < 2 or run in raw_all or run in kq_raw:
                    continue
                sk = dan_lib.skeleton(run)
                if sk in sk_all or sk in kq_sk:
                    warnings.append("%s %s: Hebrew run matches by skeleton only: %r" % (did, path, run[:30]))
                else:
                    problems.append("%s %s: Hebrew run in neither the verse bytes nor the K/Q layer: %r" %
                                    (did, path, run[:30]))
    if [p for p, _ in spans] != sorted(p for p, _ in spans):
        problems.append("rows are not in span order")
    miss = [x for x in want if x not in seen]
    over = [x for x in seen if x not in set(want)]
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
