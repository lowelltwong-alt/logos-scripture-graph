#!/usr/bin/env python3
"""Author-wave worklist v2: the A4 class UNBLOCKED at citation granularity, plus #e14's Q2 and Q3 orders.

WHAT CHANGED FROM v1 AND WHY, because a version table that lists changes the artifact does not contain is
ledger row E-30 and I have already committed its sibling once this session:
  1. A4 was ONE BLOCKED placeholder. It is now 292 CITATION items - 142 in-span, 3 mixed, 147 at-seam - from
     the re-executed member, distinct-checked against the controlling agent's recount at SET EQUALITY.
     #e14 O4's union with the peers' hand-named verses adds ZERO further items, measured in o4_union.v2.json.
  2. Every A4 item carries role_token UNASSIGNED and the 11-token ROLE_VOCABULARY. DEF-A4-ARGUED clause 6
     makes the token mandatory on an install and forbids the tool from guessing it.
  3. The CONFIDENCE values are now VALIDATED against the corpus's measured scale. v1 shipped P09-011 with the
     value "only close does NOT satisfy limb (b)" - its parser split the ruling text on the hyphen inside
     "mark-only" - so v1 would have instructed the author to write that string into a confidence field.
  4. #e14 Q2's wording order for P08-012 and P08-013 is a new WORDING class. Q2 also HOLDS all three rows at
     MEDIUM, so no confidence item moves on its account.
  5. The four BOSS_RETURN items now carry their C1 reproduction, the C2 sidecar instruction and the C3
     spot-wave marking, per #e14 Q3.
  6. Two RANGE fixtures join the negative-fixture set, as O2's second sentence requires.

WHY THE FIXTURES ARE A BUILD GATE AND NOT A REPORT. Each one is a case some tool in this chain silently
dropped. A fixture that stops firing means the builder has re-acquired a defect this campaign already paid for,
so a non-firing fixture FAILS THE BUILD.
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
sys.path.insert(0, str(EZ / "tools"))
from check_refs_mirror import ROLE_VOCABULARY                              # noqa: E402

HERE = Path(__file__).resolve().parent
BOSS = EZ / "ezek_boss_audit.v1.json"
R13 = EZ / "ezek_controlling_agent_ruling_e13.v1.json"
R14 = EZ / "ezek_controlling_agent_ruling_e14.v1.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
INV = EZ / "verse_inventory.json"
RUN = HERE / "refs_mirror_citation_run2.json"
UNION = HERE / "o4_union.v2.json"
C1 = HERE / "c1_boss_fact_reproduction.v1.json"
CHECK = HERE / "distinct_check_p2.v1.json"
OUT = EZ / "author_wave_worklist.v2.json"

PIN_ROWS = "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc"
ZONE_CHAPTERS = {20, 21}
# the corpus's measured confidence scale (#e13: high 32 / medium 47 / medium_low 50 / low 16). A value outside
# it is a parse failure, not a new grade.
SCALE = {"high", "medium", "medium_low", "low"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert sha(ROWS) == PIN_ROWS, "the rows file moved; the worklist would address different bytes"
face = json.loads(INV.read_text(encoding="utf-8")).get("numbering_face")
assert face == "WEB", "verse_inventory.json must declare its face (P1); got %r" % face

boss = json.loads(BOSS.read_text(encoding="utf-8"))
r13 = json.loads(R13.read_text(encoding="utf-8"))
r14 = json.loads(R14.read_text(encoding="utf-8"))
run = json.loads(RUN.read_text(encoding="utf-8"))
union = json.loads(UNION.read_text(encoding="utf-8"))
c1 = json.loads(C1.read_text(encoding="utf-8"))
chk = json.loads(CHECK.read_text(encoding="utf-8"))

assert chk["verdict"].startswith("PASS"), "the P2 distinct check must PASS before its output becomes a worklist"
assert c1["all_four_reproduce"], "#e14 C1: a fact that does not reproduce STOPS its row"
assert union["CONCLUSION"]["items_the_union_adds_beyond_the_members_292_citations"] == 0

import re                                                                   # noqa: E402
rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
V = re.compile(r"Ezek\.(\d+)\.(\d+)")
spans = {}
for r in rows:
    ms = V.findall(str(r.get("span", "")))
    if ms:
        spans[r["decision_id"]] = ((int(ms[0][0]), int(ms[0][1])), (int(ms[-1][0]), int(ms[-1][1])))

items = []


def add(row_id, cls, action, source, tier, **kw):
    items.append(dict(row_id=row_id, cls=cls, action=action, source=source, tier=tier, **kw))


# ---------------------------------------------------------------- 1. confidence moves, VALIDATED
def confidence_value(ruling_text):
    """The grade a confidence ruling adopts, or None.

    v1's parser was `text.split("—")[-1].split("-")[-1]`, which on "ADOPTED — medium; the condition is
    resolved: a mark-only close does NOT satisfy limb (b)" returned "only close does NOT satisfy limb (b)" -
    it split on the hyphen inside "mark-only". The grade is the FIRST clause after the em-dash, and it is then
    checked against the corpus's measured scale, so a parse failure surfaces as a refusal instead of being
    written into a row.
    """
    if "—" not in ruling_text:
        return None
    tail = ruling_text.split("—", 1)[1]
    cand = tail.split(";")[0].strip().strip(".").lower()
    return cand if cand in SCALE else None


cmoves, cmove_src = {}, {}
for c in (r13.get("confidence_rulings") or []):
    rid = c.get("row") or c.get("row_id")
    rul = str(c.get("ruling") or "")
    if not rid or not rul.upper().startswith("ADOPTED"):
        continue
    val = confidence_value(rul)
    if val is None:
        raise SystemExit("REFUSED: could not parse a valid grade for %s from %r. v1 shipped an unvalidated "
                         "string here; an unparsed grade is a STOP, never a guess." % (rid, rul[:120]))
    cmoves[rid], cmove_src[rid] = val, "#e13 confidence_rulings"
p12 = boss.get("p08_012_reweigh") or {}
if p12.get("to"):
    v = str(p12["to"]).strip().lower()
    assert v in SCALE, "the boss audit's P08-012 grade %r is off the scale" % v
    cmoves["P08-012"], cmove_src["P08-012"] = v, "P8 boss audit p08_012_reweigh, HELD at MEDIUM by #e14 Q2"
for rid, to in sorted(cmoves.items()):
    add(rid, "CONFIDENCE", "set confidence to %s" % to, cmove_src[rid],
        "EXTRACTED from the ruling; the grade is validated against the corpus's measured scale",
        new_value=to, moves_seam=False,
        held_by_e14_q2=(rid in ("P07-001", "P08-012", "P08-013")))

# ---------------------------------------------------------------- 2. #e14 Q2 wording orders
for o in (r14["q2_conf_cal"].get("author_wave_wording_orders") or []):
    rid_part = o.split(":")[0]
    targets = [t.strip() for t in rid_part.replace(" and ", ",").split(",") if t.strip().startswith("P")]
    if not targets or "no order beyond" in o:
        continue
    for rid in targets:
        add(rid, "WORDING", o.split(":", 1)[1].strip(), "#e14 Q2 author_wave_wording_orders",
            "the ruling's order, on MEASURED bytes", moves_seam=False,
            confidence_unchanged=True,
            why=("the shared-shape premise behind BOSS-ESC-2 was dissolved by the bytes: 36:23's recognition "
                 "clause runs to the silluq with the formula tokens mid-verse, so it is an ordinary licensed "
                 "refrain-grade close and not the weak mid-verse shape"))

# ---------------------------------------------------------------- 3. the four RETURNed reconciliations (Q3)
c1_by_row = {c["row"]: c for c in c1["reproductions"]}
for r in boss["rows"]:
    if r.get("verdict") != "RETURN":
        continue
    rid = r["row_id"]
    rep = c1_by_row.get(rid)
    add(rid, "BOSS_RETURN", "apply the boss audit's corrected work order verbatim",
        "P8 boss audit, RETURN verdict; #e14 Q3 rules it RETURN-WITH-CORRECTION and sends it straight to the "
        "author wave with conditions C1-C3",
        "MEASURED by the boss over a pinned input AND independently REPRODUCED from that input by the "
        "orchestrator under C1",
        work_order=r.get("work_order"), reported_where_measured=r.get("reported_where_measured"),
        moves_seam=False,
        c1_reproduction={"reproduces": rep["reproduces"], "how": rep["how"],
                         "found": rep["found"], "expected": rep["expected"]} if rep else "MISSING",
        c2_sidecar=("record this row in the SUPERSEDED-BY-BOSS-MEASUREMENT sidecar with BOTH readings and the "
                    "input path and digest; the peer packet is NOT edited"),
        c3_spot_wave="FULL COVERAGE regardless of the field-change test, as the compensating second read",
        return_verdict="RETURN-WITH-CORRECTION")

# ---------------------------------------------------------------- 4. A6, from the boss's attachment
a6 = (boss.get("a6_measured_attachment") or {}).get("by_row") or {}
a6_counts = Counter()
for rid, runs in sorted(a6.items()):
    for runrec in runs:
        n = runrec.get("n")
        formula = bool(runrec.get("formula_rendering"))
        in_span = bool(runrec.get("in_span"))
        if formula:
            act = ("A6-b: EXEMPT if this row names the device; otherwise install the convention. "
                   "AUTHOR JUDGEMENT at the row.")
            kind = "AUTHOR_JUDGEMENT"
        elif not in_span:
            act = ("check at the cited verse: the run matches the translation at a verse OUTSIDE this row's "
                   "span, so it may be a coincidental collocation rather than a quotation. AUTHOR JUDGEMENT.")
            kind = "AUTHOR_JUDGEMENT"
        else:
            act = "install the convention: double curly quotes plus an in-field web: reference"
            kind = "INSTALL"
        a6_counts[kind] += 1
        add(rid, "A6", act, "P8 boss audit a6_measured_attachment",
            "MEASURED for run existence; the duty is applied at the row under A6/A6-b",
            run=runrec.get("run"), words=n, field=runrec.get("field"), web_refs=runrec.get("web_refs"),
            in_span=in_span, formula_rendering=formula,
            on_continuation_line=bool(runrec.get("on_continuation_line")), kind=kind, moves_seam=False)

# ---------------------------------------------------------------- 5. marks
for rid, what in (("P05-004", "the closed-section mark on MT 22:31 stands at this row's ONSET seam and is "
                               "undisclosed"),
                  ("P05-008", "the closed-section mark on MT 24:14 stands at this row's ONSET seam and is "
                               "undisclosed")):
    add(rid, "MARKS_3D", "disclose the named mark with its direction", "P8 boss audit: GENUINE of 12 flags",
        "MEASURED by the boss against pmarks", detail=what, moves_seam=False)
add("P11-001", "MARKS_3D",
    "fix the FALSE clause: the row says its span carries no parashah corroboration on either side, while the "
    "verse before its first verse carries a doubled closed-section mark that the row's own rationale argues from",
    "P8 boss audit (E13-55); #e13 R5 ordered the MEDIUM false-fact fix", "MEASURED by the boss",
    severity="MEDIUM", moves_seam=False)

# ---------------------------------------------------------------- 6. arithmetic
for rid, wrong, right in (("P02-002", "fourteen", "twelve"), ("P02-003", "four", "three"),
                          ("P02-005", "sixteen", "seventeen")):
    add(rid, "ARITHMETIC", "correct the verse count in the rejected-alternative field: %s -> %s" % (wrong, right),
        "peer_02, carried in queue E13-13", "REPORTED by peer_02; the author re-counts before writing",
        moves_seam=False)

# ---------------------------------------------------------------- 7. A4 at CITATION granularity - UNBLOCKED
CLS_ACTION = {
    "IN_SPAN": "install ONE boundary_evidence_refs entry for this citation",
    "MIXED": "install ONE boundary_evidence_refs entry for this citation (it spans the seam and the span)",
    "AT_SEAM": "install ONE boundary_evidence_refs entry for this citation (a seam-facing claim)",
}
for i in run["worklist_citations"]:
    add(i["decision_id"], "A4_CITATION",
        "%s: %s. A RANGE citation takes a RANGE entry. Then choose exactly one ROLE token." % (
            CLS_ACTION[i["class"]], i["citation"]),
        "the re-executed refs_mirror member (#e14 O1-O3), distinct-checked at set equality against the "
        "controlling agent's own recount",
        "MEASURED: the citation is argued in the row's prose and no refs entry covers it under DEF-A4-ARGUED "
        "clause 3",
        citation=i["citation"], citation_kind=i["kind"], a4_class=i["class"],
        verse_count=i["verse_count"], verses_web=i["verses_web"],
        field=i["field"], raw=i["raw"], repeats_in_row=i["repeats_in_row"],
        role_token="UNASSIGNED", role_vocabulary=list(ROLE_VOCABULARY),
        role_rule=("choose EXACTLY ONE token. A WARRANT token on a verse the rationale does not rest on is a "
                   "defect the spot wave checks; an ANCHOR token is never a boundary claim. Then free text "
                   "under the rotation rule: at least 4 formulations, at most 6 words."),
        moves_seam=False)

# ---------------------------------------------------------------- negative fixtures (P9 + O2)
def fixture_in_span_unmirrored():
    """An in-span unmirrored CITATION must reach the worklist as its own class, not be swallowed."""
    return any(i["cls"] == "A4_CITATION" and i["a4_class"] == "IN_SPAN" for i in items)


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


def fixture_range_is_one_item():
    """#e14 O2, first half, at the WORKLIST level: a range citation appears as ONE item naming the range, never
    as one item per verse of the range. This is the fixture for the clause that was reported applied and never
    implemented - about 300 of the old 444 figures were range interiors (ledger E-31).

    THE FIRST FORMULATION OF THIS FIXTURE WAS WRONG AND THE BUILD GATE CAUGHT IT, which is worth keeping in the
    source because it is the difference between testing the ruling and testing my paraphrase of it. It asserted
    that no single-verse item may sit inside a same-row range item, and it failed on 33 legitimate cases: a row
    argues Ezek.4.1 as its ONSET in boundary_rationale and 4:1-17 as a RIVAL SPAN in
    strongest_rejected_alternative. Those are different verse-sets, so DEF-A4-ARGUED clause 2 makes them two
    citations - the dedupe rule collapses the same verse-set cited twice, not a verse that also falls inside a
    range. A fixture that forbade them would have deleted real claims.

    What O2 actually requires is tested here instead: each distinct (row, field, raw-text) range citation
    yields exactly ONE item, so no range has been expanded into its verses; and no two items on one row carry
    the same verse-set, which is clause 2's dedupe rule.
    """
    a4 = [i for i in items if i["cls"] == "A4_CITATION"]
    rng = [i for i in a4 if i["citation_kind"] == "range"]
    if not rng:
        return False
    # (a) one item per range citation: no (row, field, raw) range appears twice
    seen = Counter((i["row_id"], i["field"], i["raw"]) for i in rng)
    expanded = [k for k, n in seen.items() if n > 1]
    # (b) clause 2's dedupe: no two items on one row share a verse-set
    dupes = [k for k, n in Counter((i["row_id"], tuple(i["verses_web"])) for i in a4).items() if n > 1]
    # (c) and the range items really do name a span, not a verse
    named = all("-" in i["citation"] and i["verse_count"] > 1 for i in rng)
    return not expanded and not dupes and named


def fixture_mirrored_range_absent():
    """#e14 O2, second half: a range whose refs cover EITHER endpoint must produce NO worklist item. Verified
    against live data - the four verses the peers named that this build does not install are exactly the
    interior/first-endpoint verses of ranges mirrored at their other endpoint (o4_union.v2.json)."""
    cat = union["every_superset_verse_accounted_for"].get(
        "inside_a_range_citation_mirrored_at_its_OTHER_endpoint", 0)
    named = union["the_last_category_in_full"]
    return cat > 0 and all(d["second_endpoint_mirrored"] or d["first_endpoint_mirrored"] for d in named) \
        and not any(i["cls"] == "A4_CITATION" and i["citation"] == d["citation"] and i["row_id"] == d["row"]
                    for d in named for i in items)


def fixture_role_token_unassigned():
    """No A4 item may arrive with a ROLE token already chosen: DEF-A4-ARGUED clause 6 puts that judgement where
    a person writes it, and a tool that guessed it would encode a judgement it cannot audit."""
    a4 = [i for i in items if i["cls"] == "A4_CITATION"]
    return bool(a4) and all(i["role_token"] == "UNASSIGNED" for i in a4)


def fixture_confidence_on_scale():
    """Every confidence value must be on the corpus's measured scale. v1 shipped "only close does NOT satisfy
    limb (b)" as P09-011's grade; this fixture is that defect's regression."""
    cv = [i for i in items if i["cls"] == "CONFIDENCE"]
    return bool(cv) and all(i["new_value"] in SCALE for i in cv)


FIXTURES = [
    ("an in-span unmirrored citation reaches the worklist", fixture_in_span_unmirrored,
     "the member used to subtract the row's own span, making the class invisible"),
    ("the book-final span is addressable", fixture_book_final_span,
     "the window guard used to fail closed and bin every reference out-of-window"),
    ("a zone row is present and reachable", fixture_zone_verse,
     "adjacency was computed on the WEB face where the prose argues on the MT face"),
    ("the named-range absence claim is carried", fixture_named_range_absence,
     "the interior vocabulary was applied to the span-scoped branch only"),
    ("a five-word formula rendering is carried as author judgement", fixture_five_word_formula,
     "the arm had no A6-b exemption and its ref-keyed scope hid the class"),
    ("O2: each range citation is ONE item naming a span, and no row carries a duplicate verse-set",
     fixture_range_is_one_item,
     "the orchestrator reported 'a range counts as one citation' as applied and never implemented it; about "
     "300 of the 444 reported verses were range interiors (ledger E-31)"),
    ("O2: a range mirrored at EITHER endpoint produces no item at all", fixture_mirrored_range_absent,
     "the same unimplemented clause; per-verse comparison flagged every interior verse of a range whose "
     "endpoint the refs already named"),
    ("no A4 item arrives with a ROLE token already chosen", fixture_role_token_unassigned,
     "a tool that guesses the evidentiary role encodes a judgement it cannot audit (DEF-A4-ARGUED clause 6)"),
    ("every confidence value is on the corpus's measured scale", fixture_confidence_on_scale,
     "v1's parser split the ruling text on the hyphen inside 'mark-only' and shipped a sentence fragment as "
     "P09-011's grade"),
]
results = [{"fixture": n, "fired": bool(fn()), "guards_against": why} for n, fn, why in FIXTURES]
failed = [r for r in results if not r["fired"]]

doc = {
    "schema": "m8_author_wave_worklist.v2",
    "supersedes": "author_wave_worklist.v1.json (kept; never overwritten)",
    "preconditions": "P5, P9, and P2 RE-EXECUTED per #e14 O1-O3 with its distinct check PASSING",
    "built_at": datetime.now(timezone.utc).isoformat(),
    "what_changed_from_v1": [
        "A4 was one BLOCKED placeholder; it is now %d CITATION items (142 in-span, 3 mixed, 147 at-seam)"
        % len([i for i in items if i["cls"] == "A4_CITATION"]),
        "every A4 item carries role_token UNASSIGNED and the 11-token ROLE_VOCABULARY (DEF-A4-ARGUED clause 6)",
        "confidence values are VALIDATED against the measured scale; v1 shipped a sentence fragment as "
        "P09-011's grade",
        "#e14 Q2's wording order for P08-012 and P08-013 is a new WORDING class",
        "the four BOSS_RETURN items carry their C1 reproduction, C2 sidecar instruction and C3 spot-wave "
        "marking",
        "four new negative fixtures: two for O2's range rule, one for the unassigned ROLE token, one for the "
        "confidence scale",
    ],
    "bound_to": {"rows": "repair/rows_v7_cwo24.jsonl", "rows_sha256": sha(ROWS), "rows_is_the_pinned_value": True,
                 "boss_audit_sha256": sha(BOSS), "ruling_e13_sha256": sha(R13), "ruling_e14_sha256": sha(R14),
                 "member_sha256": sha(EZ / "tools" / "check_refs_mirror.py"),
                 "verse_inventory_face": face},
    "what_this_is_not": ("not a basis. R10 holds that no orchestrator tool output is a worklist basis for this "
                         "book; #e14 O5 CLARIFIES that for A4 the basis is the RULE, which is fully mechanical "
                         "once DEF-A4-ARGUED defines 'argued citation', so the member's output is the rule's "
                         "application. R10(1) continues to govern members whose rule is not mechanical - "
                         "universals, A6-b judgement, mark direction - and those items remain AUTHOR_JUDGEMENT."),
    "a4_basis": {
        "order": "#e14 O4",
        "member_citations": len([i for i in items if i["cls"] == "A4_CITATION"]),
        "union_with_the_peers_hand_named_verses_adds": 0,
        "how_that_was_established": union["why_a_superset_and_not_the_47"],
        "distinct_check": {"method": chk["distinct_check"]["method"] if "distinct_check" in chk
                           else "set equality against the controlling agent's recount",
                           "matched": chk["set_comparison"]["items_matched_exactly"],
                           "differences": chk["set_comparison"]["items_in_recount_only"]
                           + chk["set_comparison"]["items_in_rerun_only"]},
        "role_vocabulary": list(ROLE_VOCABULARY),
    },
    "negative_fixtures": {
        "why": ("each fixture is a case some tool in this chain silently DROPPED. A fixture that does not fire "
                "means the builder has re-acquired a defect this campaign already paid for, so a non-firing "
                "fixture is a BUILD FAILURE and not a warning."),
        "results": results, "all_fired": not failed,
    },
    "counts": {
        "items_total": len(items),
        "by_class": dict(Counter(i["cls"] for i in items)),
        "a4_by_class": dict(Counter(i["a4_class"] for i in items if i["cls"] == "A4_CITATION")),
        "a4_by_kind": dict(Counter(i["citation_kind"] for i in items if i["cls"] == "A4_CITATION")),
        "a6_by_kind": dict(a6_counts),
        "rows_touched": len({i["row_id"] for i in items if i["row_id"] != "*"}),
        "blocked_classes": [i["cls"] for i in items if i.get("blocked")],
        "items_moving_a_seam": sum(1 for i in items if i.get("moves_seam")),
    },
    "spot_wave_full_coverage_additions": [i["row_id"] for i in items if i["cls"] == "BOSS_RETURN"],
    "order_of_execution_from_the_ruling": (r13.get("author_wave") or {}).get("order"),
    "honest_limits": [
        "The A6 class is the boss's MEASURED run list; whether each run owes the convention is applied at the "
        "row under A6/A6-b, which is why formula renderings and out-of-span matches are AUTHOR_JUDGEMENT.",
        "Every A4 item's ROLE token is UNASSIGNED by design. The member measured mirroring; the evidentiary "
        "role is the author's judgement and the spot wave checks it.",
        "The arithmetic items are REPORTED by a peer; the author re-counts before writing.",
        "No item in this worklist moves a seam. If the author wave finds one that would, it stops and escalates.",
        "The A4 at-seam class (147) is larger than the in-span class (145). Both are installs of one entry per "
        "citation; neither is a seam move.",
    ],
    "items": items,
}

OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"written": OUT.name, "sha256": sha(OUT), "bytes": OUT.stat().st_size,
                  "counts": doc["counts"],
                  "fixtures": [{"fired": r["fired"], "fixture": r["fixture"]} for r in results],
                  "BUILD": "FAILED - a fixture did not fire" if failed else "OK - all %d fixtures fired"
                           % len(results)}, indent=1, ensure_ascii=False))
if failed:
    raise SystemExit(1)
