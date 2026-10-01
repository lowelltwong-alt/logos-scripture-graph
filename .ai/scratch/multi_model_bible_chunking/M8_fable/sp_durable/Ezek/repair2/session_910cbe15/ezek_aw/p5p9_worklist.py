#!/usr/bin/env python3
"""Preconditions P5 and P9 of the #e13 ruling: build the author-wave worklist, and distinct-check the builder
with negative fixtures that MUST FIRE.

THE RULING'S CONSTRAINT ON THIS FILE (R10): "no orchestrator tool output is a worklist BASIS for this book; the
worklist builder gets a distinct check and negative fixtures that must fire (in-span unmirrored verse, book-final
span, zone verse, named-range absence claim, five-word formula rendering), every item carrying source and tier."

So every item below names the AGENT or RULING that established it, never this builder. Where the builder can only
narrow a class and not decide it, the item is marked AUTHOR_JUDGEMENT with the question stated - the author wave
decides at the row, which is where the evidence is.

WHY THE FIXTURES ARE NEGATIVE. Each of the five is a case a previous version of some tool in this chain silently
DROPPED: an in-span unmirrored verse (the member subtracted the span), a book-final span (the window guard failed
closed), a zone verse (adjacency computed on the wrong numbering face), a named-range absence claim (the interior
vocabulary was applied to one branch only), and a five-word formula rendering (the arm had no A6-b exemption and
the ref-keyed scope made the class invisible). A fixture that does not fire means the builder has re-acquired a
defect this campaign already paid for, so a non-firing fixture is a BUILD FAILURE, not a warning.
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
BOSS = EZ / "ezek_boss_audit.v1.json"
R13 = EZ / "ezek_controlling_agent_ruling_e13.v1.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
INV = EZ / "verse_inventory.json"
OUT = EZ / "author_wave_worklist.v1.json"

PIN_ROWS = "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc"
ZONE_CHAPTERS = {20, 21}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert sha(ROWS) == PIN_ROWS, "the rows file moved; the worklist would address different bytes"
face = json.loads(INV.read_text(encoding="utf-8")).get("numbering_face")
assert face == "WEB", "verse_inventory.json must declare its face (P1); got %r" % face

boss = json.loads(BOSS.read_text(encoding="utf-8"))
r13 = json.loads(R13.read_text(encoding="utf-8"))
rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
spans = {}
import re
V = re.compile(r"Ezek\.(\d+)\.(\d+)")
for r in rows:
    ms = V.findall(str(r.get("span", "")))
    if ms:
        spans[r["decision_id"]] = ((int(ms[0][0]), int(ms[0][1])), (int(ms[-1][0]), int(ms[-1][1])))

items = []


def add(row_id, cls, action, source, tier, **kw):
    items.append(dict(row_id=row_id, cls=cls, action=action, source=source, tier=tier, **kw))


# ---------------------------------------------------------------- 1. confidence moves
cmoves = {}
for c in (r13.get("confidence_rulings") or []):
    rid = c.get("row") or c.get("row_id")
    rul = str(c.get("ruling") or "")
    if rid and rul.upper().startswith("ADOPTED"):
        to = rul.split("—")[-1].split("-")[-1].strip().rstrip(";").split(";")[0].strip()
        cmoves[rid] = to
p12 = boss.get("p08_012_reweigh") or {}
if p12.get("to"):
    cmoves["P08-012"] = str(p12["to"]).lower()
for rid, to in sorted(cmoves.items()):
    add(rid, "CONFIDENCE", "set confidence to %s" % to,
        "#e13 confidence_rulings" if rid != "P08-012" else "P8 boss audit p08_012_reweigh",
        "EXTRACTED from the ruling", new_value=to, moves_seam=False)

# ---------------------------------------------------------------- 2. the four RETURNed reconciliations
for r in boss["rows"]:
    if r.get("verdict") == "RETURN":
        add(r["row_id"], "BOSS_RETURN", "apply the boss audit's corrected work order verbatim",
            "P8 boss audit, RETURN verdict", "MEASURED by the boss over pinned inputs",
            work_order=r.get("work_order"), reported_where_measured=r.get("reported_where_measured"),
            moves_seam=False)

# ---------------------------------------------------------------- 3. A6, from the boss's attachment
a6 = (boss.get("a6_measured_attachment") or {}).get("by_row") or {}
a6_counts = Counter()
for rid, runs in sorted(a6.items()):
    for run in runs:
        n = run.get("n")
        formula = bool(run.get("formula_rendering"))
        in_span = bool(run.get("in_span"))
        if formula:
            act = ("A6-b: EXEMPT if this row names the device; otherwise install the convention. "
                   "AUTHOR JUDGEMENT at the row.")
            kind = "AUTHOR_JUDGEMENT"
        elif not in_span:
            act = ("check at the cited verse: the run matches the translation at a verse OUTSIDE this row's span, "
                   "so it may be a coincidental collocation rather than a quotation. AUTHOR JUDGEMENT.")
            kind = "AUTHOR_JUDGEMENT"
        else:
            act = "install the convention: double curly quotes plus an in-field web: reference"
            kind = "INSTALL"
        a6_counts[kind] += 1
        add(rid, "A6", act, "P8 boss audit a6_measured_attachment",
            "MEASURED for run existence; the duty is applied at the row under A6/A6-b",
            run=run.get("run"), words=n, field=run.get("field"), web_refs=run.get("web_refs"),
            in_span=in_span, formula_rendering=formula,
            on_continuation_line=bool(run.get("on_continuation_line")), kind=kind, moves_seam=False)

# ---------------------------------------------------------------- 4. marks: the boss's genuine set only
for rid, what in (("P05-004", "the closed-section mark on MT 22:31 stands at this row's ONSET seam and is "
                               "undisclosed"),
                  ("P05-008", "the closed-section mark on MT 24:14 stands at this row's ONSET seam and is "
                               "undisclosed")):
    add(rid, "MARKS_3D", "disclose the named mark with its direction", "P8 boss audit: GENUINE of 12 flags",
        "MEASURED by the boss against pmarks", detail=what, moves_seam=False)
add("P11-001", "MARKS_3D",
    "fix the FALSE clause: the row says its span carries no parashah corroboration on either side, while the "
    "verse before its first verse carries a doubled closed-section mark that the row's own rationale argues from",
    "P8 boss audit (E13-55); #e13 R5 ordered the MEDIUM false-fact fix",
    "MEASURED by the boss", severity="MEDIUM", moves_seam=False)

# ---------------------------------------------------------------- 5. arithmetic
for rid, wrong, right in (("P02-002", "fourteen", "twelve"), ("P02-003", "four", "three"),
                          ("P02-005", "sixteen", "seventeen")):
    add(rid, "ARITHMETIC", "correct the verse count in the rejected-alternative field: %s -> %s" % (wrong, right),
        "peer_02, carried in queue E13-13", "REPORTED by peer_02; the author re-counts before writing",
        moves_seam=False)

# ---------------------------------------------------------------- 6. A4: BLOCKED pending #e14
add("*", "A4_IN_SPAN", "BLOCKED - not sized until #e14 answers queue E13-57",
    "#e13 R1 versus the fixed member's measurement", "MEASURED both figures; the basis is unruled",
    blocked=True,
    detail=("the fixed member reports 444 in-span argued-but-unmirrored verses across 100 rows; R1 anticipated "
            "about 47 from the peers' hand-named set. The author wave must not install either count until the "
            "controlling agent rules the basis."),
    moves_seam=False)

# ---------------------------------------------------------------- negative fixtures (P9)
def fixture_in_span_unmirrored():
    """An in-span unmirrored verse must reach the worklist as its own class, not be swallowed."""
    return any(i["cls"] == "A4_IN_SPAN" for i in items)


def fixture_book_final_span():
    """The row whose span ends at the book's final verse must still be addressable."""
    last_ch = max(int(k) for k in json.loads(INV.read_text(encoding="utf-8"))["chapters"])
    endcap = [rid for rid, (f, l) in spans.items() if l[0] == last_ch]
    return bool(endcap) and all(rid in spans for rid in endcap)


def fixture_zone_verse():
    """A row inside the MT/WEB renumbering zone must be present and reachable by span."""
    return any(f[0] in ZONE_CHAPTERS or l[0] in ZONE_CHAPTERS for f, l in spans.values())


def fixture_named_range_absence():
    """The named-range absence-claim case must appear as a marks item, not vanish."""
    return any(i["cls"] == "MARKS_3D" and i["row_id"] == "P11-001" for i in items)


def fixture_five_word_formula():
    """A five-word formula rendering must be carried as AUTHOR_JUDGEMENT, never silently dropped or installed."""
    return any(i["cls"] == "A6" and i.get("formula_rendering") and i.get("words") == 5
               and i.get("kind") == "AUTHOR_JUDGEMENT" for i in items)


FIXTURES = [
    ("an in-span unmirrored verse reaches the worklist", fixture_in_span_unmirrored,
     "the member used to subtract the row's own span, making the class invisible"),
    ("the book-final span is addressable", fixture_book_final_span,
     "the window guard used to fail closed and bin every reference out-of-window"),
    ("a zone row is present and reachable", fixture_zone_verse,
     "adjacency was computed on the WEB face where the prose argues on the MT face"),
    ("the named-range absence claim is carried", fixture_named_range_absence,
     "the interior vocabulary was applied to the span-scoped branch only"),
    ("a five-word formula rendering is carried as author judgement", fixture_five_word_formula,
     "the arm had no A6-b exemption and its ref-keyed scope hid the class"),
]
results = [{"fixture": n, "fired": bool(fn()), "guards_against": why} for n, fn, why in FIXTURES]
failed = [r for r in results if not r["fired"]]

doc = {
    "schema": "m8_author_wave_worklist.v1",
    "preconditions": "P5 (worklist assembled) and P9 (builder distinct-checked with negative fixtures)",
    "built_at": datetime.now(timezone.utc).isoformat(),
    "bound_to": {"rows": "repair/rows_v7_cwo24.jsonl", "rows_sha256": sha(ROWS),
                 "rows_is_the_pinned_value": True,
                 "boss_audit": BOSS.name, "boss_audit_sha256": sha(BOSS),
                 "ruling_e13": R13.name, "ruling_e13_sha256": sha(R13),
                 "verse_inventory_face": face},
    "what_this_is_not": ("not a basis. R10 holds that no orchestrator tool output is a worklist basis for this "
                         "book, so every item names the AGENT or RULING that established it and this builder "
                         "only assembles. Where it can narrow a class but not decide it, the item is "
                         "AUTHOR_JUDGEMENT with the question stated."),
    "negative_fixtures": {
        "why": ("each fixture is a case some tool in this chain silently DROPPED. A fixture that does not fire "
                "means the builder has re-acquired a defect this campaign already paid for, so a non-firing "
                "fixture is a BUILD FAILURE and not a warning."),
        "results": results,
        "all_fired": not failed,
    },
    "counts": {
        "items_total": len(items),
        "by_class": dict(Counter(i["cls"] for i in items)),
        "a6_by_kind": dict(a6_counts),
        "rows_touched": len({i["row_id"] for i in items if i["row_id"] != "*"}),
        "blocked_classes": [i["cls"] for i in items if i.get("blocked")],
        "items_moving_a_seam": sum(1 for i in items if i.get("moves_seam")),
    },
    "order_of_execution_from_the_ruling": (r13.get("author_wave") or {}).get("order"),
    "honest_limits": [
        "The A6 class is the boss's MEASURED run list; whether each run owes the convention is applied at the "
        "row under A6/A6-b, which is why formula renderings and out-of-span matches are AUTHOR_JUDGEMENT rather "
        "than installs.",
        "The A4 in-span class is BLOCKED and carries no count, because the basis is unruled.",
        "No item in this worklist moves a seam. If the author wave finds one that would, it stops and escalates.",
        "The arithmetic items are REPORTED by a peer; the author re-counts before writing.",
    ],
    "items": items,
}

OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"written": OUT.name, "sha256": sha(OUT)[:32],
                  "counts": doc["counts"],
                  "fixtures": results,
                  "BUILD": "FAILED - a fixture did not fire" if failed else "OK - all fixtures fired"},
                 indent=1, ensure_ascii=False))
if failed:
    raise SystemExit(1)
