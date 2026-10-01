#!/usr/bin/env python3
"""Does my A4 member miss bare dotted list members? Lane 03 says yes, on P04-001. Measure the extent.

THE CLAIM. P04-001's prose reads "oshb:Ezek.20.9, 20.14 and 20.22". My member's patterns are an Ezek.C.V token,
a bare C:V cite with a COLON, an "MT C:V" qualifier, and a v./vv. expression. None of them matches `20.14` -
a DOTTED continuation of an OSIS-style list - so the member extracts the first member of that list and silently
drops the other two.

WHY IT MATTERS RATHER THAN BEING A CURIOSITY. DEF-A4-ARGUED clause 1 defines an argued citation as any verse
anchor a prose field carries, and clause 2 makes a comma/"and" list one citation PER MEMBER. A list of three
verses is three citations. If the member sees one, the A4 class is INCOMPLETE and the worklist under-covers -
which is the same shape as E-32 (an artifact built from part of the order) arriving from the opposite direction:
not a class I forgot, but a class my own extractor cannot see.

THE MEASUREMENT IS DELIBERATELY NOISY-SIDE-UP. A bare dotted pair also appears in decimals, in version strings
and in figures, so this collects every candidate and then partitions them into (a) those inside an OSIS-style
list context, which are almost certainly citations, and (b) everything else, printed for a human read. I would
rather report a noisy superset with its partition than a clean number I cannot justify.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(EZ / "tools"))
from check_refs_mirror import SKIP_KEYS, prose_refs, a4_window, covered       # noqa: E402
from ezek_lib import expand_ref_token, LAST_VERSE                             # noqa: E402

rows = [json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl")
        .read_text(encoding="utf-8").splitlines() if l.strip()]

# a dotted pair NOT preceded by "Ezek." and not part of a longer dotted run
BARE_DOT = re.compile(r"(?<!Ezek\.)(?<![\d.])(\d{1,3})\.(\d{1,3})(?![\d.])")
# "in a list context" = an OSIS-style token appears earlier in the same string
OSIS_CTX = re.compile(r"(?:oshb:|web:)?Ezek\.\d+\.\d+")

found, by_row = [], Counter()
for r in rows:
    rid = r["decision_id"]
    own = set(expand_ref_token(str(r.get("span", "")).replace("web:", "")))
    win, _ = a4_window(own)
    cov = covered(r)
    argued = prose_refs(r, {c for c, _ in own})

    def walk(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in SKIP_KEYS:
                    continue
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
        elif isinstance(o, str):
            has_osis = bool(OSIS_CTX.search(o))
            for m in BARE_DOT.finditer(o):
                c, v = int(m.group(1)), int(m.group(2))
                if c not in LAST_VERSE or not (1 <= v <= LAST_VERSE[c]):
                    continue                      # not a real verse in this book
                p = (c, v)
                found.append({
                    "row": rid, "field": key, "token": m.group(0),
                    "in_a_list_context": has_osis,
                    "context": o[max(0, m.start() - 55):m.end() + 40].replace("\n", " "),
                    "already_extracted_by_the_member": p in argued,
                    "in_the_a4_window": p in win,
                    "mirrored_in_refs": p in cov,
                })
                by_row[rid] += 1
    walk(r)

listish = [f for f in found if f["in_a_list_context"]]
missed = [f for f in listish if not f["already_extracted_by_the_member"]]
missed_in_window = [f for f in missed if f["in_the_a4_window"]]
missed_unmirrored = [f for f in missed_in_window if not f["mirrored_in_refs"]]

out = {
    "schema": "ezek_a4_extraction_gap.v1",
    "raised_by": "author lane 03, on P04-001",
    "the_gap": ("the member's patterns are an Ezek.C.V token, a bare C:V cite with a COLON, an 'MT C:V' "
                "qualifier, and a v./vv. expression. A DOTTED continuation of an OSIS-style list - '20.14' in "
                "'oshb:Ezek.20.9, 20.14 and 20.22' - matches none of them, so the member takes the first "
                "member of such a list and drops the rest."),
    "why_it_matters": ("DEF-A4-ARGUED clause 1 makes any verse anchor a citation and clause 2 makes a list one "
                       "citation PER MEMBER. A three-verse list is three citations. Where the member sees one, "
                       "the A4 class is incomplete - E-32's shape from the opposite direction: not a class I "
                       "forgot, but a class my extractor cannot see."),
    "method": ("collect every bare dotted pair that names a real verse of this book, then partition by whether "
               "an OSIS-style token appears earlier in the same string. A noisy superset with its partition "
               "beats a clean number I cannot justify."),
    "candidates_total": len(found),
    "in_a_list_context": len(listish),
    "of_those_already_extracted": len(listish) - len(missed),
    "MISSED_BY_THE_MEMBER": len(missed),
    "missed_and_in_the_a4_window": len(missed_in_window),
    "missed_in_window_and_UNMIRRORED": len(missed_unmirrored),
    "rows_affected": sorted({f["row"] for f in missed_unmirrored}),
    "the_unmirrored_in_window_cases": missed_unmirrored,
    "missed_but_already_mirrored_so_no_worklist_item_is_owed":
        [{k: f[k] for k in ("row", "field", "token", "context")} for f in missed_in_window
         if f["mirrored_in_refs"]][:20],
    "candidates_NOT_in_a_list_context_for_a_human_read":
        [{k: f[k] for k in ("row", "field", "token", "context")} for f in found
         if not f["in_a_list_context"]][:25],
    "tier": "MEASURED over the pinned rows; whether each candidate IS a citation is a reading, and the context "
            "strings are provided for it",
}
(HERE / "a4_extraction_gap.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("candidates_total", "in_a_list_context", "of_those_already_extracted",
                                      "MISSED_BY_THE_MEMBER", "missed_and_in_the_a4_window",
                                      "missed_in_window_and_UNMIRRORED", "rows_affected")}, indent=1))
print()
for f in missed_unmirrored:
    print("  %-9s %-28s %-8s %s" % (f["row"], f["field"], f["token"], f["context"][:88]))
